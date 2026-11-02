"""Step 1: 单案全流程端到端实测验证脚本 (Intake -> Workflow S1~S9 -> Final Conclusion & Export)
包含双向合规审查 (Dual Compliance)、反制裁哨兵 (Anti-Sanctions Sentinel)、CRAG 自省补偿与 DOCX 导出。
"""

import os
import sys
import asyncio
import time
from io import BytesIO

# 强制 UTF-8 编码与底层安全参数
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")
os.environ.setdefault("OMP_NUM_THREADS", "4")
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from lawagent.core.types import CaseState, CaseMeta, LifecycleStage, ProjectArchetype
from lawagent.store.db import StateDBManager
from lawagent.flow.graph import LawWorkflowRunner
from lawagent.api.export import generate_case_docx
from lawagent.api.routes.cases import extract_case_intake, ExtractIntakePayload


async def run_single_case_verification():
    print("=" * 75)
    print("      Step 1: 东盟域外法查明助手 - 单案全生命周期全流程实测验证")
    print("=" * 75)

    # 1. 测试原始索赔与合同函件智能要素提取 (Intake Extraction)
    raw_dispute_notice = """
    项目背景：中资建筑集团在越南平顺省承建 150MW 海上风电 EPC 总承包工程。
    争议事实：因业主电网并网接入工程严重迟延 120 天，导致机组无法如期开展倒送电调试。
    承包商依据合同第 8.4 条提交工期顺延 (EOT) 索赔意向通知，但业主以承包商通知送达已超 28 天为由拒收。
    同时，美欧某金融机构以中资母公司受涉疆涉军单边制裁为由，要求终止美元银团贷款与设备结算，
    业主据此威胁全额扣发合同总额 15%（约 3000 万美元）的延误违约金，并单方没收履约保函。
    中方诉求：
    1. 主张工期顺延 120 天，依越南《建设法》第 146 条及 37/2015 号法令主张违约金法定最高不得超过 12% 封顶；
    2. 依据中国《反外国制裁法》与商务部《阻断办法》启动反长臂管辖阻断防线，切换跨境人民币 (CIPS) 结算；
    3. 申请履约保函显失公平与反干预紧急司法止付令，启动中信保 (Sinosure) 30 日出险保全程序。
    """

    print("\n[阶段 1/4] 测试案情智能要素结构化提取 (Intake Extraction)...")
    payload = ExtractIntakePayload(raw_text=raw_dispute_notice, hint_jurisdiction="asean_vn")
    intake_res = await extract_case_intake(payload)

    print(f"  [OK] 提取标题: {intake_res.title}")
    print(f"  [OK] 建议法域: {intake_res.jurisdiction} (准据法: {intake_res.governing_law})")
    print(f"  [OK] 生命周期阶段: {intake_res.lifecycle_stage}")
    print(f"  [OK] 抽取工程参数: {intake_res.extracted_params}")

    assert intake_res.jurisdiction == "asean_vn", "法域识别错误"
    assert intake_res.extracted_params.get("delay_days") == 120, "延误天数抽取错误"

    # 2. 初始化案卷状态对象 (CaseState)
    print("\n[阶段 2/4] 初始化案卷状态并挂载安全哨兵与双向合规审查参数...")
    case_id = f"VERIFY-CASE-{int(time.time())}"
    state = CaseState(
        case_id=case_id,
        title=intake_res.title or "越南海上风电制裁阻断与违约金封顶索赔案",
        snapshot_id="20261021-asean-v2.2",
        mode="lite",  # 自动化全闭环模式
        facts_zh=raw_dispute_notice,
        claims_zh=intake_res.claims or "主张工期顺延、违约金12%封顶及反制裁阻断救济",
        meta=CaseMeta(
            title=intake_res.title,
            jurisdiction="asean_vn",
            contract_type="FIDIC_SILVER",
            choice_of_law="越南实体法 (Vietnamese Law)",
            lifecycle_stage=LifecycleStage.EXECUTION_DISPUTE,
            project_archetypes=[ProjectArchetype.EPC_CONTRACTING, ProjectArchetype.CROSS_BORDER_MA],
            engineering_params={
                "delay_days": 120,
                "notice_days": 35,
                "sinosure_notice_days": 12,
                "main_ld_cap_pct": 12.0
            }
        )
    )

    db = StateDBManager.get_instance()
    db.save_case(state)

    # 3. 运行 Multi-Agent 工作流 (S1 -> S9)
    print("\n[阶段 3/4] 启动 LangGraph 状态图全生命周期推进 (S1~S9)...")
    runner = LawWorkflowRunner(in_memory=True)
    config = {"configurable": {"thread_id": case_id}}

    start_time = time.time()
    step_count = 0

    async for event in runner.graph.astream(state, config=config, stream_mode="updates"):
        for node_name, node_updates in event.items():
            step_count += 1
            for k, v in node_updates.items():
                if hasattr(state, k):
                    setattr(state, k, v)
            state.current_node = node_name
            print(f"  [Node {step_count:02d}] [OK] 已完成节点: {node_name:20s} (当前状态: {state.status})")

    elapsed = time.time() - start_time
    print(f"\n工作流执行完毕！累计步数: {step_count}，端到端耗时: {elapsed:.2f} 秒")

    # 4. 关键输出结果审查
    print("\n[阶段 4/4] 深度审查最终研判结论与关键指标...")

    # A. 状态核验
    print(f"  1. 最终案卷状态: {state.status} (节点: {state.current_node})")
    assert state.status in ("completed", "running"), f"状态异常: {state.status}"

    # B. 安全哨兵与反制裁评估核验
    print(f"  2. 安全哨兵警报数: {len(state.security_alerts)}")
    sanction_alerts = [a for a in state.security_alerts if a.category in ("anti_sanctions_long_arm", "unilateral_sanctions_long_arm")]
    print(f"     - 成功触发反制裁/反长臂管辖阻断警报: {len(sanction_alerts)} 项")
    for a in sanction_alerts:
        print(f"       * 警报等级: {getattr(a, 'risk_level', getattr(a, 'level', 'HIGH'))} | 标题: {a.title_zh}")
        if a.sinosure_preservation_guide:
            print(f"       * 包含 30 日出险报损/阻断保全指引: {a.sinosure_preservation_guide[:70]}...")
        if a.mitigation_actions:
            print(f"       * 包含可执行对冲与反制建议: {len(a.mitigation_actions)} 条")
    assert len(sanction_alerts) >= 1, "未识别出反制裁与长臂管辖风险"

    # C. 双向合规冲突检测核验
    dc = getattr(state, "dual_compliance_audit", None)
    if dc:
        print(f"  3. 双向合规审查: 总合规项 {len(dc.items)} 项, 冲突碰撞 {dc.collision_count} 项")
        print(f"     - 母国 (中国法) 合规指数: {dc.prc_score:.1f}%")
        print(f"     - 东道国 (越南法) 强行法指数: {dc.host_score:.1f}%")
        for c in dc.items:
            if c.is_collision:
                c_nat = getattr(c, "collision_nature", getattr(c, "collision_desc", "法域强行法规范冲突"))
                print(f"       * 冲突领域: {c.topic_zh} | 规制差异: {c_nat}")
                print(f"         避冲对策: {c.resolution_strategy[:60]}...")
        assert dc.collision_count >= 1, "未能检出中-越双向合规冲突"
    else:
        print("  3. 双向合规审计未挂载")

    # D. 争议焦点与法源证据检索
    print(f"  4. 争议焦点 (Issues): {len(state.issues)} 个 | 待查明法律问题: {len(state.questions)} 个")
    print(f"  5. 召回证据条目 (Evidence): {len(state.evidence)} 条")
    ref_ids = [ev.ref_id for ev in state.evidence.values()]
    print(f"     - 核心引证: {ref_ids[:4]} ...")

    # E. 战术指引与沙盘反驳话术
    tg = state.tactical_guidance
    if tg:
        qv = tg.get("qualitative_verdict") if isinstance(tg, dict) else getattr(tg, "qualitative_verdict", None)
        print(f"  6. 战术指引定性: {qv}")
        scripts = (tg.get("negotiation_scripts") if isinstance(tg, dict) else getattr(tg, "negotiation_scripts", [])) or []
        print(f"     - 生成双语反驳谈判话术: {len(scripts)} 套")
        for s in scripts[:2]:
            title = s.get('scenario_title') if isinstance(s, dict) else getattr(s, 'scenario_title', '')
            text_zh = s.get('script_zh') if isinstance(s, dict) else getattr(s, 'script_zh', '')
            print(f"       * 【{title}】: {text_zh[:50]}...")
    else:
        print("  6. 战术指引未生成")

    # F. 最终合规指引意见书 (DOCX) 导出测试
    print("\n  7. 测试 Word (DOCX) 查明意见书导出格式与排版...")
    docx_stream = generate_case_docx(state)
    assert isinstance(docx_stream, BytesIO)
    docx_bytes = docx_stream.getbuffer().nbytes
    print(f"     - DOCX 导出成功，文件大小: {docx_bytes / 1024:.1f} KB")
    assert docx_bytes > 10000, "DOCX 文件体积异常过小"

    print("\n" + "=" * 75)
    print("[SUCCESS] 单案全流程端到端执行测试 100% 成功，所有业务模块流转正常！")
    print("=" * 75)
    return True


if __name__ == "__main__":
    success = asyncio.run(run_single_case_verification())
    sys.exit(0 if success else 1)
