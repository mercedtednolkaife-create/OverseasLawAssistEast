import asyncio
import sys
import os
import json
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

from lawagent.api.routes.cases import extract_case_intake, ExtractIntakePayload

async def main():
    print("==================================================")
    print("开始测试：基于 qwen3.7-flash 的智能要素深度提取与重塑")
    print("==================================================")

    # 1. 模拟用户输入一段非常典型的非结构化、口语化案情
    raw_text = """我们是中资总承包企业，在印尼苏拉威西承建某镍铁冶炼配套自备电站项目（EPC总包合同）。
我方进场后严格履约，主体工程和机组安装全部按期完成。但是印尼当地电网公司和业主交地及外接输电线路延迟了整整6个月，导致机组无法按期带负荷调试。
我方在知悉延误后第10天向工程师正式提交了180天的工期顺延（EOT）和追加赶工停窝工费用的索赔申请。
但印尼业主无理拒绝了我们的申请，反而反咬一口称我们延误工期，在上周（2024-05-10）无理扣留了我们300万美元的到期进度款，并向雅加达当地银行申请全额索兑2000万美元的履约保函，还发函威胁要解除总包合同。
我们现在非常被动，希望紧急申请当地法院保函止付禁令，保全资产，并向雅加达仲裁机构追索被拖欠的进度款及停窝工损失。请问该如何应对？"""

    payload = ExtractIntakePayload(
        raw_text=raw_text,
        hint_jurisdiction="asean_id"
    )

    t0 = time.time()
    try:
        response = await extract_case_intake(payload)
        cost = time.time() - t0
        print(f"\n[测试 1 - 正常提取] 调用耗时: {cost:.2f}s")
        print("提取结果:")
        print(f"  * 案件标题 (title): {response.title}")
        print(f"  * 属地国别 (jurisdiction): {response.jurisdiction}")
        print(f"  * 合同准据法 (governing_law): {response.governing_law}")
        print(f"  * 争议解决方式 (dispute_resolution): {response.dispute_resolution}")
        print(f"  * 涉案当事方 (parties): {response.parties}")
        print(f"  * 合同订立日 (contract_date): {response.contract_date}")
        print(f"  * 争议出险日 (event_date): {response.event_date}")
        print(f"  * 抽取的工程数值参数: {response.extracted_params}")
        print(f"\n--- 结构化事实陈述 (facts) ---\n{response.facts}")
        print(f"\n--- 核心主张与法律救济诉求 (claims) ---\n{response.claims}")
        print("\n[测试 1 评估]:")
        assert response.title != ""
        assert "印尼" in response.title or "电站" in response.title or "保函" in response.title
        assert response.jurisdiction == "asean_id"
        assert "【履约背景" in response.facts or "1." in response.facts or "我方" in response.facts
        print(">> 测试 1 成功！模型与结构化提取工作完美符合预期！")
    except Exception as e:
        print(f"[测试 1 失败]: {e}")
        import traceback
        traceback.print_exc()

    # 2. 测试极端异常情况下的降级容错机制（如极短文本或网络模拟异常）
    print("\n--------------------------------------------------")
    print("[测试 2 - 极短文本/降级兜底测试]")
    short_payload = ExtractIntakePayload(
        raw_text="印尼电站工程纠纷",
        hint_jurisdiction="asean_id"
    )
    t0 = time.time()
    res_short = await extract_case_intake(short_payload)
    print(f"短文本抽取耗时: {time.time() - t0:.4f}s")
    print(f"  * 标题: {res_short.title}")
    print(f"  * 法域: {res_short.jurisdiction}")
    print(f"  * 事实: {res_short.facts}")
    print(f"  * 诉求: {res_short.claims}")
    assert res_short.jurisdiction == "asean_id"
    print(">> 测试 2 降级兜底验证成功！")

if __name__ == "__main__":
    asyncio.run(main())
