"""CRAG 自省式检索充分性门禁与跨层补偿循环单元测试"""

import pytest
import asyncio
from lawagent.core.types import (
    CaseState, CaseMeta, LegalQuestion, ElementState, Evidence, ElementEvidence
)
from lawagent.flow.sufficiency import compute_sufficiency_score
from lawagent.flow.nodes import researcher_node


def test_compute_sufficiency_score():
    elems = [
        ElementState(qid="Q1", element_id="e1", name_zh="要件1", status="covered"),
        ElementState(qid="Q1", element_id="e2", name_zh="要件2", status="partial"),
        ElementState(qid="Q1", element_id="e3", name_zh="要件3", status="missing"),
        ElementState(qid="Q1", element_id="e4", name_zh="要件4", status="covered"),
    ]
    # score = (1.0 + 0.5 + 0.0 + 1.0) / 4 = 2.5 / 4 = 0.625
    tau, cov, par, mis = compute_sufficiency_score(elems)
    assert tau == 0.625
    assert cov == 2
    assert par == 1
    assert mis == 1


def test_compute_sufficiency_score_all_covered():
    elems = [
        ElementState(qid="Q1", element_id="e1", name_zh="要件1", status="covered"),
        ElementState(qid="Q1", element_id="e2", name_zh="要件2", status="covered"),
    ]
    tau, cov, par, mis = compute_sufficiency_score(elems)
    assert tau == 1.0
    assert cov == 2
    assert par == 0
    assert mis == 0


@pytest.mark.asyncio
async def test_crag_gate_triggered_and_compensates():
    """测试当要件存在缺失时，CRAG 门禁自动触发并进行跨层补偿与轨迹记录"""
    state = CaseState(
        case_id="CRAG_TEST_001",
        snapshot_id="20261021-asean-v2.2",
        facts_zh="承包商在马来西亚进行工程施工，由于业主迟延导致工期延误，双方就背靠背付款与违约金扣除产生争议。",
        meta=CaseMeta(
            jurisdiction="asean_my",
            contract_type="FIDIC_SILVER"
        ),
        questions=[
            LegalQuestion(
                qid="Q1",
                text_zh="马来西亚法下背靠背付款条款是否有效以及延误工期顺延请求权基础",
                queries_target=["pay when paid void CIPAA", "extension of time FIDIC"],
                status="confirmed",
                must_norms=[]
            )
        ],
        elements=[
            ElementState(qid="Q1", element_id="e1", name_zh="背靠背条款法定效力", status="missing"),
            ElementState(qid="Q1", element_id="e2", name_zh="工期顺延通知要件", status="partial", gap_note="缺少FIDIC或标准合同通知时效法条")
        ],
        evidence={}
    )

    result = await researcher_node(state)
    assert "crag_trace" in result
    trace = result["crag_trace"]
    assert trace["triggered"] is True
    assert trace["threshold"] == 0.75
    assert "post_tau" in trace
    # 验证引入了跨层法源或补偿法条
    assert len(result["evidence"]) > 0
    assert len(trace["reformulated_queries"]) > 0


@pytest.mark.asyncio
async def test_crag_gate_triggered_on_partial_threshold():
    """测试当无missing但存在partial且tau处于0.75临界点时，平滑放宽的CRAG门禁亦能精准触发"""
    state = CaseState(
        case_id="CRAG_TEST_PARTIAL_002",
        snapshot_id="20261021-asean-v2.2",
        facts_zh="中国企业在老挝投资水电站工程特许权项目中，遭遇国家电网因系统故障紧急弃电，双方就照付不议补偿与工期免责发生争议。",
        meta=CaseMeta(
            jurisdiction="asean_la",
            contract_type="FIDIC_SILVER"
        ),
        questions=[
            LegalQuestion(
                qid="Q1",
                text_zh="老挝电力法下电网紧急调度弃电的免责效力及特许权经济补偿",
                queries_target=["Electricity Law Lao Curtailment dispatch", "concession economic compensation"],
                status="confirmed",
                must_norms=[]
            )
        ],
        elements=[
            # 1 covered + 1 partial: tau = (1.0 + 0.5)/2 = 0.75, mis = 0, par = 1
            ElementState(qid="Q1", element_id="e1", name_zh="特许经营权合同基础", status="covered"),
            ElementState(qid="Q1", element_id="e2", name_zh="国家电网紧急调度免责要件", status="partial", gap_note="需补全老挝电力法调度免责与补偿规范")
        ],
        evidence={}
    )

    result = await researcher_node(state)
    assert "crag_trace" in result
    trace = result["crag_trace"]
    # 验证平滑放宽门禁 (par > 0 and pre_tau <= 0.80) 生效
    assert trace["triggered"] is True
    assert len(result["evidence"]) > 0
