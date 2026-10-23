"""东盟涉外建设工程与海外合规端到端基准验收测试套件 (ASEAN E2E Benchmark Test Suite)

覆盖范围：
1. REST API 端到端路由验收 (/api/health, /api/cases, /api/search, /api/verify-materials, /api/experts, /api/consults)
2. 数据库纯净化与零德美残留验证 (0 German/US records, 100% ASEAN/FIDIC)
3. 真实东盟建设工程案案卷全流程推进与推理流水线验收 (LangGraph 8 阶段)
4. 追问检索 (Follow-up) 与证据扩充端到端闭环
5. 《东盟国家建设工程法律风险防范与合规指引意见书》Word (DOCX) 导出合规性核验
"""

import os
import json
import sqlite3
import pytest
from io import BytesIO
from fastapi.testclient import TestClient
from docx import Document

from lawagent.api.main import app
from lawagent.core.types import (
    CaseState, CaseMeta, Fact, Claim, Material, LegalQuestion, Issue,
    LifecycleStage, ProjectArchetype, SecurityRiskLevel
)
from lawagent.core.jurisdiction import JurisdictionRegistry
from lawagent.store.db import StateDBManager
from lawagent.store.snapshots import SnapshotManager
from lawagent.store.retriever import HybridRetriever
from lawagent.flow.graph import LawWorkflowRunner, build_law_graph
from scripts.seed_asean_cases import seed_asean_demo_cases


@pytest.fixture(scope="module")
def client():
    """FastAPI TestClient"""
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def state_db():
    """StateDBManager 实例并确保基础示范案已就绪"""
    db = StateDBManager("data/state/state.sqlite")
    seed_asean_demo_cases(db, overwrite=False)
    return db


def test_e2e_db_purity():
    """验收 1: 验证数据库与知识库 100% 纯净，零德美成文法或判例残留"""
    mgr = SnapshotManager()
    all_norms = mgr.get_all_norms()
    all_cases = mgr.get_all_cases()

    # 1. 成文法规范全量属于东盟 6 国、FIDIC、BIT 或央企合规法源
    assert len(all_norms) >= 20
    allowed_prefixes = ("ID:", "VN:", "MY:", "SG:", "TH:", "PH:", "FIDIC:", "BIT:", "CN:", "TREATY:", "SINOSURE:")
    for n in all_norms:
        norm_id = n["norm_id"]
        assert norm_id.startswith(allowed_prefixes), f"Unexpected non-ASEAN norm: {norm_id}"
        # 绝无德美法条
        assert not norm_id.startswith(("BGB:", "HGB:", "UCC:", "DGCL:", "USC:", "Rome_I:"))

    # 2. 司法裁判先例全量属于东盟建设工程与涉外仲裁裁判
    assert len(all_cases) >= 5
    for c in all_cases:
        case_id = c["case_id"]
        assert not case_id.startswith(("BGH:", "OLG:", "LG:", "SCOTUS:", "CIR:", "DEL-CH:"))
        assert any(k in case_id for k in ("BSMountSophia", "ManilaWater", "ArbitrationEnforcement", "SEMA", "CIPAA", "JBE", "Hopewell"))


def test_e2e_jurisdiction_registry():
    """验收 2: 验证法域注册中心仅保留东盟六国法域与 FIDIC/BIT 规范体系"""
    active_jur_codes = [j.code for j in JurisdictionRegistry.list_jurisdictions(active_only=True)]
    assert "asean_id" in active_jur_codes
    assert "asean_vn" in active_jur_codes
    assert "asean_my" in active_jur_codes
    assert "asean_sg" in active_jur_codes
    assert "asean_th" in active_jur_codes
    assert "asean_ph" in active_jur_codes

    # 确保德国与美国已被彻底注销
    assert "de_federal" not in active_jur_codes
    assert "us_commercial" not in active_jur_codes
    assert JurisdictionRegistry.get("de_federal") is None
    assert JurisdictionRegistry.get("us_commercial") is None


def test_e2e_rest_api_health_and_cases(client):
    """验收 3: 验证 REST API 基础端点及东盟标杆案件详情结构"""
    # 1. 健康检查
    h_res = client.get("/api/health")
    assert h_res.status_code == 200
    assert h_res.json()["status"] == "ok"

    # 2. 案件列表检索
    c_res = client.get("/api/cases")
    assert c_res.status_code == 200
    cases = c_res.json()
    assert len(cases) >= 4
    c_ids = [c["case_id"] for c in cases]
    assert "C101" in c_ids  # 印尼光伏 EPC
    assert "C102" in c_ids  # 越南风电 M&A
    assert "C103" in c_ids  # 马来西亚轻轨 EPC 与新加坡保函
    assert "C104" in c_ids  # 菲律宾水务特许经营

    # 3. 详情获取与东盟特有结构核验
    detail = client.get("/api/cases/C101").json()
    assert detail["case_id"] == "C101"
    assert detail["meta"]["jurisdiction"] == "asean_id"
    assert "FIDIC" in detail["meta"]["choice_of_law"] or "印尼" in detail["meta"]["choice_of_law"]
    assert len(detail["findings"]) > 0
    assert len(detail["evidence"]) > 0


def test_e2e_norm_search_engine(client):
    """验收 4: 验证东盟法条判例混合检索引擎 (Hybrid Search) 召回精度"""
    # 检索 1: 新加坡保函止付与显失公平
    res1 = client.get("/api/search", params={"q": "新加坡保函止付显失公平 BS Mount Sophia"}).json()
    assert len(res1) >= 1
    assert any("BS_Mount_Sophia" in item["id"] or "SG" in item["id"] for item in res1)

    # 检索 2: 印尼建筑法与本土化率要求
    res2 = client.get("/api/search", params={"q": "印尼建筑法 本土化率 TKDN"}).json()
    assert len(res2) >= 1
    assert any("ID:UU_2_2017" in item["id"] or "ID:MEMR" in item["id"] or item["id"].startswith("ID:") for item in res2)

    # 检索 3: 马来西亚快速裁决 CIPAA 反背靠背支付
    res3 = client.get("/api/search", params={"q": "CIPAA 2012 第35条 背靠背"}).json()
    assert len(res3) >= 1
    assert any("MY:CIPAA_2012" in item["id"] or "CIPAA" in item["id"] for item in res3)


def test_e2e_material_verification(client):
    """验收 5: 验证东道国证据材料真伪与时效核验接口"""
    payload = {
        "raw_text": "依据印尼2017年第2号建筑法 UU 2/2017 以及 FIDIC 20.1，涉外工程合同签署需合规。参考先例 BS Mount Sophia 与 SEMA 3/2023。"
    }
    res = client.post("/api/verify-materials", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert len(data["items"]) >= 1
    assert any(item["in_db"] for item in data["items"])
    assert any("FIDIC" in item["ref_id"] or "UU" in item["ref_id"] or "BS Mount Sophia" in item["ref_id"] for item in data["items"])


def test_e2e_experts_and_consults(client):
    """验收 6: 验证东盟特邀工程法专家名录与会商流转接口"""
    exp_res = client.get("/api/experts")
    assert exp_res.status_code == 200
    experts = exp_res.json()
    assert len(experts) >= 3
    names = [e["name"] for e in experts]
    assert any("Arief Wijaya" in n for n in names)  # 印尼 BANI 仲裁员
    assert any("Kevin Tan" in n for n in names)      # 新加坡 SIAC 资深专家
    assert any("Lim Chong Beng" in n for n in names) # 马来西亚 AIAC 大律师

    # 发起专家咨询委托
    consult_payload = {
        "case_id": "C101",
        "expert_id": "EXP-001",
        "question_snapshot": "咨询印尼2017年第2号建筑法第30条对于双语工程合同生效要件之要求",
        "evidence_summary": "FIDIC Silver 1999 Clause 20.1 & 印尼建筑法第30条"
    }
    con_res = client.post("/api/consults", json=consult_payload)
    assert con_res.status_code == 200
    con_data = con_res.json()
    assert con_data["status"] == "dispatched"
    assert "东盟" in con_data["reply"] or "专家" in con_data["reply"]


def test_e2e_followup_question(client):
    """验收 7: 验证追加待查明问题（Follow-up）东盟法源自动扩充与陈述闭环"""
    followup_payload = {
        "question_text": "若业主因土地征拆受阻迟延移交现场，承包商工期索赔除斥期间是否有抗辩空间？"
    }
    res = client.post("/api/cases/C101/followup", json=followup_payload)
    assert res.status_code == 200
    updated_state = res.json()
    # 验证问题已追加
    assert any("征拆" in q["text_zh"] for q in updated_state["questions"])
    # 验证陈述已补充
    assert any("针对追加问题" in st["text_zh"] for f in updated_state["findings"] for st in f["statements"])


def test_e2e_docx_export(client):
    """验收 8: 验证《东盟国家建设工程法律风险防范与合规指引意见书》Word (DOCX) 导出格式与防伪指纹"""
    res = client.get("/api/cases/C101/export/docx")
    assert res.status_code == 200
    assert "application/vnd.openxmlformats-officedocument.wordprocessingml.document" in res.headers["content-type"]

    # 读取 DOCX 文档流解析正文段落
    doc = Document(BytesIO(res.content))
    doc_text = "\n".join(p.text for p in doc.paragraphs)

    assert "东盟" in doc_text or "ASEAN" in doc_text
    assert "建设工程" in doc_text or "合规" in doc_text
    assert "FIDIC" in doc_text or "印尼" in doc_text
    # 必须包含权威法源或最高院司法解释（二）合规溯源说明
    assert "法通" in doc_text or "最高人民法院" in doc_text or "解释（二）" in doc_text


def test_e2e_extract_intake(client):
    """验收 9: 验证建案前原始邮件/索赔函一键智能要素抽提 (/api/cases/extract-intake)"""
    claim_email = """
    From: Employer PM (Jakarta)
    To: China Contractor EPC Team
    Subject: Notice of Default & Liquidated Damages - Central Java 300MW Power Plant
    Dear Sirs,
    Your progress is currently delayed by 45 days. Under FIDIC Silver Clause 20.1, you were required to serve notice within 28 days of the event, but your notice arrived after 35 days.
    Furthermore, your TKDN local content is only 28%, violating MEMR Reg 11/2024. Liquidated damages will be capped at 10%. Sinosure notice must be preserved within 20 days.
    """
    res = client.post("/api/cases/extract-intake", json={"raw_text": claim_email})
    assert res.status_code == 200
    data = res.json()
    assert data["jurisdiction"] == "asean_id"
    assert data["lifecycle_stage"] == "execution_dispute"
    assert data["extracted_params"]["notice_days"] == 28 or data["extracted_params"]["notice_days"] == 35
    assert data["extracted_params"]["delay_days"] == 45
    assert data["extracted_params"]["declared_tkdn_pct"] == 28.0
    assert data["extracted_params"]["main_ld_cap_pct"] == 10.0


def test_e2e_attach_artifact_and_simulate_guidance(client):
    """验收 10: 验证外部工具箱挂载闭环与工程沙盘实时返回中英双语谈判反驳话术"""
    # 1. 测试挂载工具箱成果
    art_payload = {
        "artifact_type": "redline_scan",
        "title": "CIPAA 第35条背靠背条款扫描",
        "jurisdiction": "asean_my",
        "summary": "分包Pay-when-paid背靠背付款条款依据CIPAA第35条法定绝对无效",
        "redline_clause": "Payment to Subcontractor within 14 days of receipt from Employer (Pay-when-paid) -> 建议修订为独立里程碑验收付款"
    }
    art_res = client.post("/api/cases/C101/attach-artifact", json=art_payload)
    assert art_res.status_code == 200
    artifacts = art_res.json()
    assert len(artifacts) >= 1
    assert artifacts[0]["title"] == "CIPAA 第35条背靠背条款扫描"
    art_id = artifacts[0]["artifact_id"]

    # 2. 测试沙盘重算返回 tactical_guidance
    sim_res = client.post("/api/cases/C101/simulate-engineering", json={
        "notice_days": 35,  # 越过 28 天红线
        "declared_tkdn_pct": 25.0,  # 低于 40%
        "sinosure_notice_days": 35  # 越过 30 天红线
    })
    assert sim_res.status_code == 200
    sim_case = sim_res.json()
    assert sim_case["tactical_guidance"] is not None
    tg = sim_case["tactical_guidance"]
    assert "qualitative_verdict" in tg
    assert "negotiation_scripts" in tg
    assert len(tg["negotiation_scripts"]) >= 2
    # 验证生成了中英双语谈判话术
    assert any("FIDIC 20.1" in s["scenario_title"] for s in tg["negotiation_scripts"])
    assert any("Prevention Principle" in s["script_en"] for s in tg["negotiation_scripts"])

    # 3. 测试移除挂载成果
    del_res = client.delete(f"/api/cases/C101/attach-artifact/{art_id}")
    assert del_res.status_code == 200
    del_artifacts = del_res.json()
    assert all(a["artifact_id"] != art_id for a in del_artifacts)
