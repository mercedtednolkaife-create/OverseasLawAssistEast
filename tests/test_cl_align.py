"""CL-Align 跨法系多语种概念对齐算子单元测试"""

import pytest
from fastapi.testclient import TestClient
from lawagent.store.cl_align import CLAlignOperator
from lawagent.api.main import app


def test_cl_align_operator_singleton():
    op1 = CLAlignOperator.get_instance()
    op2 = CLAlignOperator.get_instance()
    assert op1 is op2
    assert len(op1.glossary_terms) >= 150


def test_cl_align_common_law_liquidated_damages():
    op = CLAlignOperator.get_instance()
    res = op.align("关于违约金酌减的裁判尺度", jurisdiction="asean_sg")
    assert "liquidated damages" in res.expanded_tokens
    assert "penalty doctrine" in res.expanded_tokens
    assert any("普通法系无" in d for d in res.cross_legal_system_doctrines)
    assert "liquidated damages" in res.reformulated_query


def test_cl_align_vietnam_penalty_cap():
    op = CLAlignOperator.get_instance()
    res = op.align("商业合同违约金上限与酌减标准", jurisdiction="asean_vn")
    assert "mức phạt vi phạm" in res.expanded_tokens
    assert any("8%" in d for d in res.cross_legal_system_doctrines)


def test_cl_align_malaysia_pay_when_paid():
    op = CLAlignOperator.get_instance()
    res = op.align("总包分包背靠背付款条款效力", jurisdiction="asean_my")
    assert "pay when paid void" in res.expanded_tokens or "conditional payment void" in res.expanded_tokens
    assert any("自始绝对无效" in d for d in res.cross_legal_system_doctrines)


def test_cl_align_brunei_sovereign_immunity():
    op = CLAlignOperator.get_instance()
    res = op.align("文莱政府工程主权豁免抗辩", jurisdiction="asean_bn")
    assert any("84C" in t for t in res.expanded_tokens)
    assert any("绝对主权豁免" in d for d in res.cross_legal_system_doctrines)


def test_cl_align_timor_leste_visto():
    op = CLAlignOperator.get_instance()
    res = op.align("公共工程追加款事前审计与付款签证", jurisdiction="asean_tl")
    assert any("Visto" in t for t in res.expanded_tokens)
    assert any("事前核准签证" in d for d in res.cross_legal_system_doctrines)


def test_cl_align_api_endpoint():
    client = TestClient(app)
    resp = client.get("/api/search/align", params={"q": "违约金酌减", "jurisdiction": "asean_sg"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["original_query"] == "违约金酌减"
    assert data["jurisdiction"] == "asean_sg"
    assert len(data["expanded_tokens"]) > 0
    assert len(data["cross_legal_system_doctrines"]) > 0
