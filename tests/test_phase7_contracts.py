"""阶段 7 单元测试套件 (Phase 7 Contracts & ASEAN Foundation Tests)
测试覆盖：
1. 多法域注册中心东盟 6 国激活与欧美法域软屏蔽 (JurisdictionRegistry active_only)
2. 东盟基建与投资并购核心数据类型与安全哨兵模型 (LifecycleStage, ProjectArchetype, SecurityAlertItem)
3. 状态库支持东盟元数据持久化与摘要列表提取 (StateDBManager)
4. 项目生命周期跨阶段平滑流转契约 (POST /api/cases/{case_id}/transition-stage)
5. 法域元数据查询接口契约 (GET /api/jurisdictions)
"""

import pytest
import os
import shutil
from fastapi.testclient import TestClient

from lawagent.core.types import (
    CaseMeta, Fact, Claim, Issue, Material, CaseState, CaseSummary,
    LifecycleStage, ProjectArchetype, SecurityRiskLevel, SecurityAlertItem
)
from lawagent.core.jurisdiction import JurisdictionRegistry
from lawagent.store.db import StateDBManager
from lawagent.api.main import app
from lawagent.api.deps import get_state_db

client = TestClient(app)

TEST_DB_DIR = "test_phase7_runtime_db"
TEST_DB_PATH = os.path.join(TEST_DB_DIR, "state.sqlite")


@pytest.fixture(autouse=True)
def setup_and_teardown_db():
    if os.path.exists(TEST_DB_DIR):
        shutil.rmtree(TEST_DB_DIR, ignore_errors=True)
    os.makedirs(TEST_DB_DIR, exist_ok=True)
    yield
    if os.path.exists(TEST_DB_DIR):
        shutil.rmtree(TEST_DB_DIR, ignore_errors=True)


def test_jurisdiction_registry_asean_and_legacy_shielding():
    """测试东盟6国作为唯一注册法域，德美法域彻底移除"""
    # 获取全量注册法域：必须恰好为东盟 6 国，且全部为 active
    all_jurisdictions = JurisdictionRegistry.list_jurisdictions(active_only=False)
    assert len(all_jurisdictions) == 6
    asean_codes = {j.code for j in all_jurisdictions}
    assert asean_codes == {
        "asean_id", "asean_vn", "asean_my", "asean_sg", "asean_th", "asean_ph"
    }

    # 德美历史法域必须彻底移除，无法被查找到
    assert JurisdictionRegistry.get("de_federal") is None
    assert JurisdictionRegistry.get("us_commercial") is None
    assert "de_federal" not in asean_codes
    assert "us_commercial" not in asean_codes

    # 印尼法域详细元数据验证
    id_meta = JurisdictionRegistry.get("asean_id")
    assert id_meta is not None
    assert id_meta.name_zh == "印度尼西亚工程与投资法"
    assert id_meta.region == "asean"
    assert id_meta.flag == "🇮🇩"
    assert id_meta.is_active is True
    assert "UU_2_2017" in id_meta.default_laws


def test_asean_core_types_and_security_alerts():
    """测试东盟基建数据类型、业态多选与安全哨兵强类型模型"""
    alert = SecurityAlertItem(
        risk_level=SecurityRiskLevel.HIGH,
        category="national_security_review",
        title_zh="印尼关键矿产与能源项目外资国安审查及51%强制本土化剥离风险",
        fact_anchor_ids=["F1", "F3"],
        host_law_basis=["UU_3_2020", "UU_2_2017"],
        prc_or_treaty_basis=["CN_ID_BIT_1992_ART4", "SASAC_ORDER_35_ART12"],
        sinosure_preservation_guide="须于政治风险事件发生后30日内向中国信保递交可能损失通知书并保全特许权合同原件",
        mandatory_human_checklist=["核实印尼投资部BKPM准入负面清单第B.1条", "排查当地合资方KSO联营体股权穿透架构"],
        mitigation_actions=["引入印尼主权财富基金INA参股10%作为政治保护伞", "在新加坡SIAC设立境外争议解决前置机制"]
    )
    assert alert.risk_level == SecurityRiskLevel.HIGH
    assert len(alert.fact_anchor_ids) == 2
    assert "UU_3_2020" in alert.host_law_basis

    meta = CaseMeta(
        title="中资雅万走廊高架公路特许经营与EPC项目",
        jurisdiction="asean_id",
        contract_type="FIDIC 1999 银皮书 EPC 总承包",
        parties=["中国某海外工程建设集团有限公司", "印尼PT Nusantara Infrastructure Tbk"],
        contract_date="2022-03-15",
        lifecycle_stage=LifecycleStage.PRE_INVESTMENT,
        project_archetypes=[ProjectArchetype.EPC_CONTRACTING, ProjectArchetype.PPP_CONCESSION],
        fidic_book_edition="1999_SILVER",
        host_country="ID"
    )
    assert meta.lifecycle_stage == LifecycleStage.PRE_INVESTMENT
    assert ProjectArchetype.PPP_CONCESSION in meta.project_archetypes
    assert meta.host_country == "ID"

    # CaseState 挂载 security_alerts 校验
    state = CaseState(
        case_id="case_asean_test_001",
        snapshot_id="snap_asean_001",
        meta=meta,
        facts_zh="中资企业中标印尼西爪哇省收费公路BOT特许经营与EPC交钥匙工程。",
        claims=[Claim(cid="C1", party="发包人", text_zh="要求总承包商承担属地征地延迟导致的工期滞后违约赔偿")],
        facts=[Fact(fid="F1", text_zh="因印尼地方习惯法土地争议导致红线交付延迟280天")],
        security_alerts=[alert]
    )
    assert len(state.security_alerts) == 1
    assert state.security_alerts[0].risk_level == SecurityRiskLevel.HIGH


def test_statedb_persistence_with_asean_metadata():
    """测试状态库对东盟扩展字段的读写与 CaseSummary 提取"""
    db = StateDBManager(db_path=TEST_DB_PATH)

    meta = CaseMeta(
        title="越南河内轻轨二期EPC总承包项目",
        jurisdiction="asean_vn",
        lifecycle_stage=LifecycleStage.EXECUTION_DISPUTE,
        project_archetypes=[ProjectArchetype.EPC_CONTRACTING],
        host_country="VN",
        parent_case_id="case_vn_parent_001"
    )
    state = CaseState(
        case_id="case_vn_child_002",
        snapshot_id="snap_asean_001",
        meta=meta,
        parent_case_id="case_vn_parent_001",
        facts_zh="越南轻轨项目因越方建设标准与业主签认延迟发生窝工索赔。",
        facts=[Fact(fid="F1", text_zh="业主代表未按FIDIC第3.5款在42天内作出工期顺延决定")]
    )

    db.save_case(state)

    # 读取并验证
    loaded = db.get_case("case_vn_child_002")
    assert loaded is not None
    assert loaded.meta.jurisdiction == "asean_vn"
    assert loaded.meta.lifecycle_stage == LifecycleStage.EXECUTION_DISPUTE
    assert loaded.parent_case_id == "case_vn_parent_001"
    assert ProjectArchetype.EPC_CONTRACTING in loaded.meta.project_archetypes

    # 测试 list_cases 返回结构
    summaries = db.list_cases()
    assert len(summaries) == 1
    summary = summaries[0]
    assert summary.case_id == "case_vn_child_002"
    assert summary.lifecycle_stage == "execution_dispute"
    assert summary.jurisdiction == "asean_vn"
    assert summary.project_archetypes == ["EPC_CONTRACTING"]
    assert summary.parent_case_id == "case_vn_parent_001"


def test_api_jurisdictions_endpoint():
    """测试 GET /api/jurisdictions 接口契约"""
    response = client.get("/api/jurisdictions")
    assert response.status_code == 200
    jurisdictions = response.json()
    assert isinstance(jurisdictions, list)
    assert len(jurisdictions) >= 6

    # 验证东盟国家激活状态
    id_item = next((j for j in jurisdictions if j["code"] == "asean_id"), None)
    assert id_item is not None
    assert id_item["is_active"] is True
    assert id_item["flag"] == "🇮🇩"
    assert id_item["region"] == "asean"


def test_api_case_lifecycle_stage_transition():
    """测试 POST /api/cases/{case_id}/transition-stage 跨阶段平滑流转"""
    db = get_state_db()

    parent_id = "case_asean_parent_101"
    parent_state = CaseState(
        case_id=parent_id,
        snapshot_id="snap_asean_001",
        status="completed",
        facts_zh="中资央企与马来西亚当地投控机构设立合资公司(JV)，签署SHA股东协议与EPC框架合同，投资开发深水港及临港产业园。",
        meta=CaseMeta(
            title="马来西亚东海岸工业园合资开发项目",
            jurisdiction="asean_my",
            lifecycle_stage=LifecycleStage.PRE_INVESTMENT,
            project_archetypes=[ProjectArchetype.PPP_CONCESSION, ProjectArchetype.JV_CONSORTIUM],
            host_country="MY"
        ),
        facts=[
            Fact(fid="F1", text_zh="当地州政府变更工业用地出让附带条件，要求增加土著(Bumiputera)股权比例至30%"),
            Fact(fid="F2", text_zh="港口特许经营协议前置审批遭遇环保部DOE补充环评要求")
        ],
        claims=[
            Claim(cid="C1", party="中资央企", text_zh="要求合资方赔偿政策变更导致的土地交付推迟损失")
        ],
        security_alerts=[
            SecurityAlertItem(
                risk_level=SecurityRiskLevel.HIGH,
                category="resource_nationalism_tkdn",
                title_zh="马来西亚土著股权配额与环评前置审批审查",
                fact_anchor_ids=["F1"],
                host_law_basis=["Act_125_Companies"],
                mandatory_human_checklist=["核查州政府工业用地出让合同附加协议"],
                mitigation_actions=["启动股东特别协议纠纷调解"]
            )
        ]
    )
    db.save_case(parent_state)

    try:
        # 调用跨阶段流转接口流转至模式二(履约索赔与争议解决)
        transition_payload = {
            "target_stage": "execution_dispute",
            "override_title": "马来西亚东海岸工业园合资开发项目(履约索赔与仲裁争议阶段)",
            "transition_note": "由于土著股权要求突变导致工期实质受阻，转入争议索赔阶段"
        }
        trans_resp = client.post(f"/api/cases/{parent_id}/transition-stage", json=transition_payload)
        assert trans_resp.status_code == 200
        child_case = trans_resp.json()

        # 验证子案件契约
        child_id = child_case["case_id"]
        assert child_id != parent_id
        assert child_case["parent_case_id"] == parent_id
        assert child_case["meta"]["parent_case_id"] == parent_id
        assert child_case["meta"]["lifecycle_stage"] == "execution_dispute"
        assert "(履约索赔与仲裁争议阶段)" in child_case["meta"]["title"]
        assert child_case["meta"]["jurisdiction"] == "asean_my"
        assert len(child_case["facts"]) == 2
        assert child_case["facts"][0]["fid"] == "F1"
        assert len(child_case["claims"]) == 1
        assert child_case["claims"][0]["cid"] == "C1"
        # 验证安全预警与跨阶段备忘录继承
        assert len(child_case["security_alerts"]) == 1
        assert child_case["security_alerts"][0]["category"] == "resource_nationalism_tkdn"
        assert any("跨阶段流转备忘录" in ins.get("title", "") for ins in child_case["saved_insights"])
    finally:
        db.delete_case(parent_id)
        if 'child_id' in locals():
            db.delete_case(child_id)
