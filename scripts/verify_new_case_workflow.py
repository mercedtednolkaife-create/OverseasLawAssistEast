import asyncio
import os
import sys
import json
import logging
from datetime import datetime

# Windows 控制台编码安全配置
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# 配置日志
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("WorkflowVerification")

from lawagent.core.types import CaseState, CaseMeta, Material
from lawagent.store.db import StateDBManager
from lawagent.flow.nodes import s1_extract_node, s2_precheck_node
from lawagent.flow.graph import LawWorkflowRunner

async def main():
    print("=" * 80)
    print("🚀 启动全新独立案例真实端到端工作流实测（含真实大模型 API 交互与 RAG 检索）")
    print("=" * 80)

    # 1. 初始化数据库与 WorkflowRunner
    db = StateDBManager.get_instance()
    runner = LawWorkflowRunner()

    case_id = f"TEST_VN_{int(datetime.now().timestamp()) % 100000}"
    snapshot_id = "20261021-asean-v2.2"

    facts_text = """2024年10月15日，中资能源海外投资建设联合体与越南国家电力公司 (EVN) 及其平顺省项目公司订立《200MW 沿海光伏与储能电站 EPC 总承包及购电特许经营协议 (PPA)》，约定准据法为越南社会主义共和国实体法，争议由新加坡国际仲裁中心 (SIAC) 仲裁解决。
电站按期建成通过商运测试 (COD) 后，因越南南部区域高压电网输配电容量受限，EVN 自2025年1月起连续下达调度限电令，强制弃光限电 (Curtailment) 比例高达 42%，导致发电收益断崖式下跌，且 EVN 连续 5 期拒付弃光保底补偿金共计 1,850 万美元。
EVN 依据越南工贸部 (MOIT) 电网安全技术调度规程抗辩称：电网阻塞属于不可预见的电网安全防线，且 PPA 专用条款未明确设立‘无条件照付不议 (Take-or-Pay)’责任，故 EVN 不承担弃光电费赔偿；同时以‘未达年核定发电基准’为由向河内开证行提交没收履约保函通知书。"""

    claims_text = """1. 承包商/投资方主张 EVN 长期强制弃光限电构成重大违约，依据《越南民法典》第351条及新建设法，请求补偿弃光电费损失 1,850 万美元并顺延投资回收期；
2. 确认电网阻塞属于电网所有方可归责规划缺陷，排斥不可抗力免责抗辩；
3. 申请紧急裁定止付见索即付履约保函，禁止 EVN 恶意索兑。"""

    meta = CaseMeta(
        jurisdiction="asean_vn",
        contract_type="国际光伏储能 EPC 与 PPA 购电协议",
        parties=["中资出海新能源联合体", "越南国家电力公司 (EVN)"],
        contract_date="2024-10-15",
        event_date="2025-01-10",
        choice_of_law="越南社会主义共和国法律 (Vietnamese Law)",
        lifecycle_stage="execution_dispute",
        dispute_resolution="SIAC",
        engineering_params={
            "curtailment_ratio": 42.0,
            "claim_amount_usd": 18500000,
            "guarantee_bond_at_risk": True
        }
    )

    init_state = CaseState(
        case_id=case_id,
        title=f"越南平顺光伏储能电站 PPA 弃光限电与保函止付索赔案 ({case_id})",
        snapshot_id=snapshot_id,
        mode="lite",
        status="running",
        current_node="s1_extract",
        facts_zh=facts_text,
        claims_zh=claims_text,
        meta=meta,
        created_at=datetime.now().isoformat(),
        updated_at=datetime.now().isoformat()
    )

    # 阶段 1: 同步执行 S1 与 S2
    print("\n[Phase 1] 执行 HTTP 同步创建阶段 (S1 抽取与 S2 预检)...")
    t0 = datetime.now()
    s1_res = await s1_extract_node(init_state)
    for k, v in s1_res.items():
        if hasattr(init_state, k):
            setattr(init_state, k, v)
    print(f"  ✓ S1 抽取完成: 事实段落 {len(init_state.facts)} 条, 诉求 {len(init_state.claims)} 条")

    s2_res = await s2_precheck_node(init_state)
    for k, v in s2_res.items():
        if hasattr(init_state, k):
            setattr(init_state, k, v)
    init_state.current_node = "s2_precheck"
    db.save_case(init_state)
    print(f"  ✓ S2 预检完成: 入口检查清单 {len(init_state.entry_checks)} 项, 安全预警 {len(init_state.security_alerts)} 项 (耗时: {(datetime.now()-t0).total_seconds():.2f}s)")

    # 阶段 2: LangGraph 流式执行剩余工作流
    print("\n[Phase 2] 启动 LangGraph Multi-Agent 后台流式协同工作流...")
    state = init_state
    config = {"configurable": {"thread_id": case_id}}

    completed_nodes = []
    async for output in runner.graph.astream(state, config=config, stream_mode="updates"):
        for node_name, node_output in output.items():
            completed_nodes.append(node_name)
            for k, v in node_output.items():
                if hasattr(state, k):
                    setattr(state, k, v)
            state.current_node = node_name
            db.save_case(state)
            print(f"  ──► 节点 [{node_name}] 执行完毕")

    # 阶段 3: 提取全流程实测数据分析报告
    print("\n" + "=" * 80)
    print("📊 实测结果深度核验与审计报告")
    print("=" * 80)
    print(f"1. 节点执行链路: {' -> '.join(completed_nodes)}")
    print(f"   (确认: 是否跳过了重复的 S1/S2? {'是' if completed_nodes[0] == 's3_decompose' else '否'})")

    print("\n2. S3 争点拆解 Agent 工作情况 (验证是否摆脱印尼 FIDIC 征地模板):")
    for idx, iss in enumerate(state.issues, 1):
        print(f"   - 争点 {idx}: [{iss.issue_id}] {iss.text_zh}")
    for idx, q in enumerate(state.questions, 1):
        print(f"   - 问题 {idx}: [{q.qid}] {q.text_zh}")
        print(f"     检索词: {q.queries_target}")
    for idx, el in enumerate(state.elements, 1):
        print(f"   - 要素 {idx}: [{el.element_id}] {el.name_zh} (状态: {el.status}, 轮次: {el.rounds})")

    print(f"\n3. RAG 混合检索与图谱关联情况:")
    print(f"   - 检索召回 Evidence 总数: {len(state.evidence)}")
    for eid, ev in state.evidence.items():
        print(f"     * [{eid}] ({ev.kind}/{ev.grade}) {ev.ref_id}: {ev.text_de[:100]}...")

    print(f"\n4. 要素证据充分性 (Sufficiency) 评定结果:")
    cov_stats = {"covered": 0, "partial": 0, "missing": 0}
    for el in state.elements:
        cov_stats[el.status] = cov_stats.get(el.status, 0) + 1
        print(f"   - [{el.element_id}] {el.name_zh}: status={el.status}, gap={el.gap_note}")
    print(f"   统计: covered={cov_stats['covered']}, partial={cov_stats['partial']}, missing={cov_stats['missing']}")

    print(f"\n5. S5 Matcher 要件事实涵摄结果 (验证事实关联是否存在假 F1 绑定):")
    for el in state.elements:
        print(f"   - [{el.element_id}] {el.name_zh}: match_status={el.match_status}, fact_links={el.fact_links}")
        print(f"     涵摄说明: {el.match_note}")

    print(f"\n6. 策略推演与红队攻防 (Strategist):")
    if state.strategic_assessment:
        print(f"   - 胜败摇摆关键变量: {state.strategic_assessment.pivotal_factors}")
        print(f"   - 推演分支数: {len(state.strategic_assessment.outcome_branches)}")
        for b in state.strategic_assessment.outcome_branches:
            print(f"     * [{b.branch_type}] {b.title} -> {b.outcome_summary[:80]}...")
        print(f"   - 红队反制武器数: {len(state.strategic_assessment.red_team_defenses)}")
        for d in state.strategic_assessment.red_team_defenses:
            print(f"     * [{d.defense_id}] (杀伤力: {d.lethal_index}) 对方主张: {d.opposing_claim[:60]}...")

    print(f"\n7. Critic 质量门禁与自愈反思情况:")
    for chk in state.checks:
        print(f"   - [{chk.code}] {chk.status}: {chk.reason}")
    print(f"   - Critic 反思重试计数 (state.retry): {state.retry}")

    print("\n" + "=" * 80)
    print("✅ 全新案例端到端真实测试顺利完成！")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(main())
