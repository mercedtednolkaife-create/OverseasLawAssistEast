import pytest
from unittest.mock import AsyncMock, patch
from lawagent.api.routes.cases import extract_case_intake, ExtractIntakePayload

@pytest.mark.asyncio
async def test_intake_extract_short_fallback():
    """测试短文本直接平滑走规则降级逻辑"""
    payload = ExtractIntakePayload(
        raw_text="印尼电站工程延误争议，业主无故扣留款项。",
        hint_jurisdiction="asean_id"
    )
    res = await extract_case_intake(payload)
    assert res.jurisdiction == "asean_id"
    assert res.governing_law == "asean_id"
    assert res.lifecycle_stage == "execution_dispute"
    assert "印尼" in res.title
    assert res.contract_date is not None

@pytest.mark.asyncio
async def test_intake_extract_mock_llm_success():
    """测试大模型提取成功时的结构化整合与列表规整"""
    mock_ai_response = {
        "title": "中资企业诉印尼业主保函恶意索兑与工期延误纠纷案",
        "facts": [
            "【履约背景】：中资总承包商按期推进主体施工。",
            "【争议事件】：业主电网接入延迟6个月，并突袭申请索兑2000万美元履约保函。",
            "【当前处境】：面临资金被截断风险。"
        ],
        "claims": [
            "申请紧急司法止付禁令，阻却履约保函索兑；",
            "主张工期顺延180天并追加停窝工索赔；",
            "确认业主单方解约行为无效。"
        ],
        "parties": "申请人：中资总承包商；被申请人：印尼业主",
        "suggested_jurisdiction": "asean_id",
        "governing_law": "asean_id",
        "lifecycle_stage": "execution_dispute",
        "project_archetype": "EPC_CONTRACTING",
        "contract_date": "2024-03-15",
        "event_date": "2024-05-10",
        "dispute_resolution": "SIAC"
    }

    payload = ExtractIntakePayload(
        raw_text="这是一段超过15个字符的复杂案情描述，中资企业在印尼苏拉威西开展项目，遭受保函索兑和电网延误...",
        hint_jurisdiction="asean_id"
    )

    with patch("lawagent.llm.client.LLMClient.chat_json", new_callable=AsyncMock) as mock_chat:
        mock_chat.return_value = mock_ai_response
        res = await extract_case_intake(payload)

        assert res.title == "中资企业诉印尼业主保函恶意索兑与工期延误纠纷案"
        assert res.jurisdiction == "asean_id"
        assert "【履约背景】" in res.facts
        assert "1. 申请紧急司法止付禁令" in res.claims
        assert "2. 主张工期顺延180天" in res.claims
        assert res.dispute_resolution == "SIAC"
        assert res.contract_date == "2024-03-15"
        assert res.event_date == "2024-05-10"

@pytest.mark.asyncio
async def test_intake_extract_mock_llm_failure_graceful_degrade():
    """测试大模型调用超时或报错时无缝平滑降级至规则提取，确保100%不中断建案"""
    payload = ExtractIntakePayload(
        raw_text="这是一段超过15个字符的复杂案情描述，中资企业在越南河内遭遇业主违约扣除履约保函...",
        hint_jurisdiction="asean_vn"
    )

    with patch("lawagent.llm.client.LLMClient.chat_json", new_callable=AsyncMock) as mock_chat:
        mock_chat.side_effect = TimeoutError("DashScope upstream timeout")
        res = await extract_case_intake(payload)

        # 验证降级后仍能返回完整有效对象，绝不抛出 500
        assert res.jurisdiction == "asean_vn"
        assert res.title != ""
        assert res.facts != ""
        assert res.claims != ""
        assert res.contract_date is not None
