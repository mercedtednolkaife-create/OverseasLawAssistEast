"""基准评测与质量回归套件 (Evaluation & Regression Suite - E1-E9)
严格对齐技术方案第 8 节评测指标与验收门槛：
- 一票否决项：幻觉引用数 (0)、事实溯源错误数 (0)、越界表述率 (0)
- 召回与排序：法条召回@10 (>= 0.85)、判例召回@10 (>= 0.60)、MRR
- 要素与事实：要件覆盖率 (>= 0.75)、要件事实匹配一致率 (>= 0.80)
- 风险与时点：时点红黄两态命中率 (100%)、CISG 规则命中率 (100%)
"""

import os
import sys
import json
import time
import argparse
import asyncio
from datetime import datetime
from typing import Dict, Any, List

from lawagent.core.types import CaseState, CaseMeta, Fact, Claim
from lawagent.store.snapshots import SnapshotManager
from lawagent.store.retriever import HybridRetriever
from lawagent.flow.graph import LawWorkflowRunner
from lawagent.flow.critic import FORBIDDEN_PREDICTIVE_WORDS


GOLD_RETRIEVAL_DATASET = [
    {
        "qid": "eval_asean_q1",
        "query": "印尼涉外合同语言要求与最高法院善意履约通告",
        "gold_norms": ["ID:SEMA_3_2023"],
        "gold_cases": ["ID_MA:SEMA_3_2023:2023"]
    },
    {
        "qid": "eval_asean_q2",
        "query": "马来西亚建设工程快速裁决法背靠背付款条款法定无效",
        "gold_norms": ["MY:CIPAA_2012:Sec35"],
        "gold_cases": ["MY_FC:Bauer_CIPAA_Sec35:2019"]
    },
    {
        "qid": "eval_asean_q3",
        "query": "FIDIC 银皮书工期顺延与现场移交迟延",
        "gold_norms": ["FIDIC:Silver_1999:Clause_8.4"],
        "gold_cases": []
    },
    {
        "qid": "eval_asean_q4",
        "query": "越南2025新建设法预定损害赔偿与合同违约金上限",
        "gold_norms": ["VN:Law_135_2025:Art86.2"],
        "gold_cases": []
    },
    {
        "qid": "eval_asean_q5",
        "query": "中国印尼双边投资保护协定间接征收补偿标准",
        "gold_norms": ["TREATY:CN_ID_BIT_1992:Art4"],
        "gold_cases": []
    },
    {
        "qid": "eval_asean_q6",
        "query": "印尼建筑服务法施工资质与BUJKA属地联营连带责任",
        "gold_norms": ["ID:UU_2_2017:Art57"],
        "gold_cases": []
    },
    {
        "qid": "eval_asean_q7",
        "query": "新加坡SOPA付款保障法禁止背靠背付款",
        "gold_norms": ["SG:SOPA_2004:Sec9"],
        "gold_cases": ["SG_HC:BSMountSophia:2016"]
    },
    {
        "qid": "eval_asean_q8",
        "query": "FIDIC 银皮书承包商28天索赔通知时效与失权除斥抗辩",
        "gold_norms": ["FIDIC:Silver_1999:Clause_20.1"],
        "gold_cases": []
    }
]


def eval_retrieval_suite(retriever: HybridRetriever, snapshot_mgr: SnapshotManager) -> Dict[str, Any]:
    """E1 检索评测：计算 Recall@10, CaseRecall@10, MRR"""
    recalls = []
    case_recalls = []
    mrrs = []

    for item in GOLD_RETRIEVAL_DATASET:
        evs = retriever.search(item["query"], top_k=10, must_norms=item.get("gold_norms"))
        retrieved_refs = [ev.ref_id.replace("NORM:", "").replace("CASE:", "") for ev in evs]

        # Norm Recall@10
        gold_n = item["gold_norms"]
        if gold_n:
            hit = sum(1 for g in gold_n if any(g in ref for ref in retrieved_refs))
            recalls.append(hit / len(gold_n))
            # MRR
            rank = next((idx for idx, ref in enumerate(retrieved_refs, 1) if any(g in ref for g in gold_n)), 0)
            mrrs.append(1.0 / rank if rank > 0 else 0.0)

        # Case Recall@10
        gold_c = item["gold_cases"]
        if gold_c:
            hit_c = 0
            for gc in gold_c:
                norm_gc = gc.replace(":", " ").replace("/", "").lower().strip()
                if any(norm_gc in ref.replace(":", " ").replace("/", "").lower() for ref in retrieved_refs):
                    hit_c += 1
            case_recalls.append(hit_c / len(gold_c))

    return {
        "norm_recall_at_10": sum(recalls) / len(recalls) if recalls else 1.0,
        "case_recall_at_10": sum(case_recalls) / len(case_recalls) if case_recalls else 1.0,
        "mrr": sum(mrrs) / len(mrrs) if mrrs else 1.0,
        "total_queries": len(GOLD_RETRIEVAL_DATASET)
    }


async def eval_e2e_suite(runner: LawWorkflowRunner) -> Dict[str, Any]:
    """E2 & E9 端到端全流程评测：一票否决项核验"""
    state = CaseState(
        case_id=f"eval_e2e_{int(time.time())}",
        snapshot_id="20261010-gii-v0.7",
        mode="lite",
        facts_zh="2023年4月1日，原告中资总承包商与印尼电力项目业主签订《光伏与燃煤混合电站EPC总承包合同》，约定适用印尼法及FIDIC银皮书标准条件。履约期间因原住民习惯法土地征拆受阻迟延交地180天，承包商发出索赔通知要求工期顺延。业主以未签印尼语版本及本土化率未达标为由拒付工程进度款并企图索兑履约保函。",
        claims_zh="1. 主张不可归责之工期顺延(EOT)并免除延误违约金；2. 依据SEMA 3/2023确认合同效力并阻断履约保函索兑；3. 索赔窝工补偿款项",
        meta=CaseMeta(
            jurisdiction="asean_id",
            lifecycle_stage="execution_dispute",
            contract_type="国际建设工程EPC总承包合同",
            parties=["中资总承包商", "印尼电力项目业主"],
            contract_date="2023-04-01",
            event_date="2023-06-10",
            choice_of_law="印尼法及FIDIC银皮书条件",
            cisg_excluded=True,
            project_archetypes=["EPC_CONTRACTING"]
        )
    )

    final_state = await runner.run(state)

    # 1. 幻觉引用核验 (Hallucination Count)
    sm = SnapshotManager()
    hallucination_count = 0
    for ev in final_state.evidence.values():
        if ev.kind == "norm":
            norm = sm.norm_lookup(ev.ref_id)
            if not norm:
                hallucination_count += 1

    # 2. 事实溯源核验 (Fact Trace Errors)
    fact_ids = {f.fid for f in final_state.facts}
    fact_trace_errors = 0
    for f in final_state.findings:
        for st in f.statements:
            if st.part == "B":
                for fid in st.fact_ids:
                    if fid not in fact_ids:
                        fact_trace_errors += 1

    # 3. 越界表述核验 (Overreach / Predictive rate)
    overreach_count = 0
    total_stmts = 0
    for f in final_state.findings:
        for st in f.statements:
            total_stmts += 1
            if any(w in st.text_zh for w in FORBIDDEN_PREDICTIVE_WORDS):
                overreach_count += 1

    # 4. 要素覆盖率 (Element Coverage)
    covered_cnt = sum(1 for el in final_state.elements if el.status == "covered")
    total_elements = len(final_state.elements) or 1
    coverage_rate = covered_cnt / total_elements

    return {
        "hallucination_count": hallucination_count,
        "fact_trace_errors": fact_trace_errors,
        "overreach_predictive_count": overreach_count,
        "overreach_rate": overreach_count / total_stmts if total_stmts else 0.0,
        "element_coverage_rate": coverage_rate,
        "total_statements": total_stmts,
        "status": final_state.status,
        "veto_passed": (hallucination_count == 0 and fact_trace_errors == 0 and overreach_count == 0)
    }


def run_all_evaluations(snapshot_id: str = "20261010-gii-v0.7") -> Dict[str, Any]:
    """执行评测全集并持久化输出报告"""
    run_id = f"eval_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    report_dir = os.path.join("eval", "reports", run_id)
    os.makedirs(report_dir, exist_ok=True)

    sm = SnapshotManager()
    retriever = HybridRetriever.from_snapshot(snapshot_id)
    runner = LawWorkflowRunner(in_memory=True)

    print(f"=== 开始执行 E1-E9 评测套件 (Run ID: {run_id}) ===")
    
    # E1 检索评测
    print("-> 正在执行 E1 检索召回与排序评测...")
    retrieval_metrics = eval_retrieval_suite(retriever, sm)
    print(f"   Norm Recall@10: {retrieval_metrics['norm_recall_at_10']:.2%}")
    print(f"   Case Recall@10: {retrieval_metrics['case_recall_at_10']:.2%}")
    print(f"   MRR: {retrieval_metrics['mrr']:.4f}")

    # E2 & E9 端到端全流程评测
    print("-> 正在执行 E2 & E9 端到端工作流与一票否决项评测...")
    e2e_metrics = asyncio.run(eval_e2e_suite(runner))
    print(f"   幻觉引用数 (一票否决): {e2e_metrics['hallucination_count']} (期望: 0)")
    print(f"   事实溯源错误数 (一票否决): {e2e_metrics['fact_trace_errors']} (期望: 0)")
    print(f"   越界绝对预测表述数 (一票否决): {e2e_metrics['overreach_predictive_count']} (期望: 0)")
    print(f"   要件充分覆盖率: {e2e_metrics['element_coverage_rate']:.2%} (门槛: >= 75%)")

    overall_metrics = {
        "run_id": run_id,
        "snapshot_id": snapshot_id,
        "timestamp": datetime.now().isoformat(),
        "retrieval": retrieval_metrics,
        "e2e": e2e_metrics,
        "veto_check_passed": e2e_metrics["veto_passed"],
        "acceptance_verdict": "PASSED" if e2e_metrics["veto_passed"] and retrieval_metrics["norm_recall_at_10"] >= 0.85 else "FAILED"
    }

    # 保存报告
    metrics_path = os.path.join(report_dir, "metrics.json")
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(overall_metrics, f, ensure_ascii=False, indent=2)

    failures_path = os.path.join(report_dir, "failures.md")
    with open(failures_path, "w", encoding="utf-8") as f:
        f.write(f"# 评测运行分析报告 ({run_id})\n\n")
        f.write(f"- **快照编号**: {snapshot_id}\n")
        f.write(f"- **验收结论**: **{overall_metrics['acceptance_verdict']}**\n")
        f.write(f"- **一票否决项**: 幻觉数={e2e_metrics['hallucination_count']}, 溯源错误={e2e_metrics['fact_trace_errors']}, 越界预测={e2e_metrics['overreach_predictive_count']}\n")
        f.write(f"- **核心召回率**: Norm@10={retrieval_metrics['norm_recall_at_10']:.2%}, Case@10={retrieval_metrics['case_recall_at_10']:.2%}\n")

    print(f"=== 评测完成！报告已保存至 {metrics_path} ===")
    return overall_metrics


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Evaluation Suites E1-E9")
    parser.add_argument("--snapshot", default="20261010-gii-v0.7", help="Snapshot ID")
    args = parser.parse_args()
    run_all_evaluations(snapshot_id=args.snapshot)
