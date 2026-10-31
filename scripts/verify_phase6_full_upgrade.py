"""Phase 6 L1深化扩充、L2全量FIDIC/多边条约与轻量GraphRAG全链路验收脚本
"""

import os
import sys
import time
import sqlite3

sys.path.insert(0, os.path.abspath("."))
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from lawagent.store.snapshots import SnapshotManager
from lawagent.store.retriever import HybridRetriever


def verify_phase6_system():
    print("=" * 80)
    print("🔍 检验 1: 物理数据库与多维知识库指标核查 (L1 核心层 + L2 广覆盖层)")
    print("=" * 80)

    mgr = SnapshotManager()
    snap_id = mgr.get_current_snapshot_id()
    conn = mgr.get_connection(snap_id)
    cur = conn.cursor()

    cur.execute("SELECT count(*) FROM norms")
    l1_norms_count = cur.fetchone()[0]
    cur.execute("SELECT count(*) FROM cases")
    l1_cases_count = cur.fetchone()[0]
    cur.execute("SELECT count(*) FROM chunks")
    l1_chunks_count = cur.fetchone()[0]
    cur.execute("SELECT count(*) FROM edges")
    l1_edges_count = cur.fetchone()[0]
    cur.execute("SELECT count(*) FROM risk_communities")
    l1_rc_count = cur.fetchone()[0]

    cur.execute("SELECT count(*) FROM reference_norms")
    l2_norms_count = cur.fetchone()[0]
    cur.execute("SELECT count(*) FROM reference_cases")
    l2_cases_count = cur.fetchone()[0]
    cur.execute("SELECT count(*) FROM reference_chunks")
    l2_chunks_count = cur.fetchone()[0]
    cur.execute("SELECT count(*) FROM reference_edges")
    l2_edges_count = cur.fetchone()[0]

    print(f"• [L1 核心层] 法条规范数: {l1_norms_count} (目标 >= 170)")
    print(f"• [L1 核心层] 标杆判例数: {l1_cases_count} (目标 >= 40)")
    print(f"• [L1 核心层] 拓扑边条数: {l1_edges_count}")
    print(f"• [L1 核心层] 风险社区数: {l1_rc_count}")
    print(f"• [L1 核心层] Chunks总数: {l1_chunks_count}")

    print(f"• [L2 广覆盖] 参考法条数: {l2_norms_count} (目标 >= 110)")
    print(f"• [L2 广覆盖] 参考裁判数: {l2_cases_count} (目标 >= 20)")
    print(f"• [L2 广覆盖] 轻量图谱边: {l2_edges_count} (目标 >= 40)")
    print(f"• [L2 广覆盖] Chunks总数: {l2_chunks_count}")

    assert l1_norms_count >= 170, f"L1 法条数未达标: {l1_norms_count}"
    assert l1_cases_count >= 40, f"L1 裁判数未达标: {l1_cases_count}"
    assert l2_norms_count >= 110, f"L2 参考法条未达标: {l2_norms_count}"
    assert l2_cases_count >= 20, f"L2 参考裁判未达标: {l2_cases_count}"
    assert l2_edges_count >= 40, f"L2 轻量拓扑边未达标: {l2_edges_count}"
    print("✓ 检验 1 全部物理指标达标！\n")

    print("=" * 80)
    print("🔍 检验 2: L1 核心层新增法典规范与裁决判例检索能力")
    print("=" * 80)
    retriever = HybridRetriever(snapshot_id=snap_id)

    l1_test_cases = [
        ("越南民事合同缔约磋商恶意终止缔约过失信赖利益赔偿", "VN:Civil_Code_2015:Art397"),
        ("印尼合同成立四大要件因果关系与欺诈撤销举证责任", "ID:KUHPerdata:Art1320"),
        ("越南新土地法清洁施工现场实体移交法定期限与工期顺延", "VN:Land_Law_2024:Art124"),
        ("印尼公共利益征地村民阻碍施工清洁现场移交法定义务", "ID:UU_2_2012:Art14"),
        ("越南民事诉讼法承认外国仲裁裁决禁止法院实体再审", "VN:Civil_Procedure_Code_2015:Art440"),
        ("印尼最高法院司法通令SEMA涉外商事仲裁裁决强制执行令", "ID:SEMA_3_2023:Arbitration_Enforcement"),
        ("新加坡国际仲裁中心电厂征地迟延现场未清场索赔胜诉案", "CASE:SIAC:Site_Handover_EOT:2020"),
        ("越南河内高级法院承认与执行SIAC涉外建设工程仲裁裁决案", "CASE:VN_Hanoi_HC:NY_Conv_SIAC_Enforcement:2021"),
    ]

    for q, expected in l1_test_cases:
        t0 = time.perf_counter()
        evs = retriever.search(q, top_k=3, layer="L1")
        dt = (time.perf_counter() - t0) * 1000
        ref_ids = [e.ref_id for e in evs]
        matched = any(expected in r for r in ref_ids)
        print(f"✓ 问句 [{q[:32]}...] -> 耗时 {dt:.1f}ms")
        print(f"   预期命中: {expected}")
        print(f"   实际召回 Top 3: {ref_ids}")
        assert matched, f"L1 未命中: {expected} in {ref_ids}"
    print("🎉 检验 2 全部通过！L1 核心层深化规范命中率 100%！\n")

    print("=" * 80)
    print("🔍 检验 3: L2 广覆盖参考层 (ACIA多边条约 / 招投标 / 环保 / FIDIC全款项) 检索与轻量GraphRAG拓扑扩展")
    print("=" * 80)

    l2_test_cases = [
        ("东盟全面投资协定ACIA公正平等待遇FET与完全保护安全", "ACIA:2009:Art11_FET"),
        ("东盟投资协定ACIA投资者直诉东道国政府ISDS国际仲裁", "ACIA:2009:Art27_ISDS_Scope"),
        ("越南新招投标法外资参标强制本土分包与投标保函没收限制", "VN:Law_22_2023:Art5_Foreign_Bidder"),
        ("印尼政府采购Perpres总统令本地化率TKDN强制优先权KSO", "ID:Perpres_16_2018:Art20_TKDN"),
        ("印尼重大基建工程AMDAL环境影响评价强制许可", "ID:UU_32_2009:Art22_AMDAL"),
        ("印尼劳工法合法罢工7日书面通知前置与非法罢工抗辩", "ID:UU_13_2003:Art140_Notice_of_Strike"),
        ("越南担保法令应收工程款质押登记对抗一般债权优先受偿", "VN:Decree_21_2021:Art14_Pledge_Receivables"),
        ("FIDIC银皮书第2.1款雇主现场移交迟延索赔工期与利润", "FIDIC:Silver_1999:Clause_2.1"),
        ("FIDIC银皮书第15.5款雇主出于自身便利终止合同严禁转包他人", "FIDIC:Silver_1999:Clause_15.5"),
        ("FIDIC银皮书第16.1款承包商未获付款21天通告合法停工权", "FIDIC:Silver_1999:Clause_16.1"),
        ("FIDIC银皮书第17.6款责任限制双方互免间接损失总责任合同价封顶", "FIDIC:Silver_1999:Clause_17.6"),
        ("中印尼双边税收协定股息利息10%协定优惠税率PPh26", "DTA:CN_ID:Art10_11_Dividends_Interest"),
        ("世界银行ICSID丘吉尔矿业诉印尼政府特许权非法征收仲裁案", "REF_CASE:ICSID:Churchill_Mining_v_Indonesia:2016"),
        ("新加坡高院裁定承包商依FIDIC第16.1款停工合法阻断违约金", "REF_CASE:SG_HC:FIDIC_Cl16_Suspension_Validity:2019"),
    ]

    for q, expected in l2_test_cases:
        t0 = time.perf_counter()
        evs = retriever.search_l2(q, top_k=4, expand_graph=True)
        dt = (time.perf_counter() - t0) * 1000
        ref_ids = [e.ref_id for e in evs]
        matched = any(expected in r for r in ref_ids)
        print(f"✓ 问句 [{q[:32]}...] -> 耗时 {dt:.1f}ms")
        print(f"   预期命中: {expected}")
        print(f"   实际召回 Top 4: {ref_ids}")
        assert matched, f"L2 未命中: {expected} in {ref_ids}"
    print("🎉 检验 3 全部通过！L2 广覆盖层与 FIDIC 全款项体系命中率 100%！\n")

    print("=" * 80)
    print("🔍 检验 4: 双层智能级联机制 (AUTO 调度与层级隔离)")
    print("=" * 80)
    # 核心违约高优先级问句 -> 应 100% 封闭在 L1
    core_q = "印尼合同违约履约催告前置令与间接损失免除"
    evs_core = retriever.search(core_q, top_k=3, layer="AUTO")
    assert all(e.layer != "L2" for e in evs_core), f"核心问句被误级联: {[e.ref_id for e in evs_core]}"
    print(f"✓ 核心高优先级问句: 命中均为 L1，纯度 100% ({[e.ref_id for e in evs_core]})")

    # 跨国多边条约与 FIDIC 问句 -> 智能无缝级联下沉至 L2 召回 Grade B
    broad_q = "项目特许经营权被东道国政府非法撤销能否直接依据条约提起ICSID国际仲裁索赔"
    evs_broad = retriever.search(broad_q, top_k=3, layer="AUTO")
    assert any(e.layer == "L2" for e in evs_broad), f"边缘问句未触发级联: {[e.ref_id for e in evs_broad]}"
    print(f"✓ 边缘条约与特许权问句: 成功触发智能级联召回 L2 参考证据: {[e.ref_id for e in evs_broad]}")

    print("\n" + "=" * 80)
    print("🏆 Phase 6 L1 深化 + L2 FIDIC/多边条约 + 轻量 GraphRAG 拓扑网络验收 100% 全部通过！")
    print("=" * 80)


if __name__ == "__main__":
    verify_phase6_system()
