"""Phase 4 API & Feature Regression Tests: Dual Compliance, 11-country Matrix, Feedback, Graph Neighborhood."""

import pytest
from fastapi.testclient import TestClient
from lawagent.api.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_comparison_matrix_11_countries(client):
    """验证东盟横向对比矩阵完整覆盖全部 11 个国家"""
    res = client.get("/api/compliance/comparison-matrix")
    assert res.status_code == 200
    data = res.json()
    assert len(data) >= 6

    expected_keys = {"dimension", "id", "vn", "my", "sg", "th", "ph", "kh", "la", "mm", "bn", "tl"}
    for row in data:
        assert expected_keys.issubset(set(row.keys()))


def test_dual_compliance_check_api(client):
    """验证 POST /api/compliance/dual-check 双向合规实时对标"""
    payload = {
        "jurisdiction": "asean_my",
        "facts_zh": "吉隆坡轻轨工程分包合同中约定以发包人付款为前提付款，遭遇拖欠款项并面临单边长臂制裁威胁",
        "declared_equity_pct": 49,
        "declared_tkdn_pct": 35,
        "has_overseas_transfer": True,
        "data_outbound_sensitive": True,
        "has_sanctions_clause": True
    }
    res = client.post("/api/compliance/dual-check", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "prc_score" in data
    assert "host_score" in data
    assert "collision_count" in data
    assert "items" in data
    assert len(data["items"]) >= 2
    assert len(data["approval_chain"]) >= 4
    # 验证识别到背靠背无效和信保争端
    rule_codes = [i["rule_code"] for i in data["items"]]
    assert any("BACK_TO_BACK" in c or "SINOSURE" in c for c in rule_codes)


def test_feedback_to_compliance_api(client):
    """验证案卷实务经验向合规规则库反馈并持久化"""
    case_res = client.get("/api/cases")
    assert case_res.status_code == 200
    cases = case_res.json()
    assert len(cases) > 0
    test_case_id = cases[0]["case_id"]

    payload = {
        "rule_code": "RULE_HOST_PAY_01",
        "feedback_type": "corroboration",
        "comment": "在马来西亚吉隆坡高院最新判例中，即使合同约定外国准据法，CIPAA 35条仍具备强制性管辖效力",
        "suggested_statute": "High Court of Malaya [2025] 3 MLJ 412"
    }
    res = client.post(f"/api/cases/{test_case_id}/feedback-to-compliance", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    assert data["rule_code"] == "RULE_HOST_PAY_01"


def test_graph_neighborhood_api(client):
    """验证 GraphRAG 拓扑邻域查询 (基于 unified_edges)"""
    res = client.get("/api/search/graph-neighborhood?node_id=BN:PWD_Form_Contract:Clause38&hops=1&layer=ALL")
    assert res.status_code == 200
    data = res.json()
    assert data["center_node"] == "BN:PWD_Form_Contract:Clause38"
    assert len(data["nodes"]) >= 1
    assert len(data["edges"]) >= 1
    edge = data["edges"][0]
    assert "source" in edge
    assert "target" in edge
    assert "relation" in edge
