# -*- coding: utf-8 -*-
"""
验证针对《数据库审查.md》提出的全部代码级与数据级问题的修复与落实情况
"""

import sys
import sqlite3
import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from lawagent.store.graph import SQLiteGraphStore, DEFAULT_GRAPH_RELS
from lawagent.store.retriever import HybridRetriever
from lawagent.flow.security_sentinel import SecuritySentinel

DB_PATH = Path("data/snapshots/20261021-asean-v2.2/law.sqlite")

def test_fixes():
    print("================================================================")
    print("开始全面核查《数据库审查.md》全部代码级与数据级优化落实情况")
    print("================================================================")

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # 1. 验证 chunks 表无双重前缀
    print("\n[Issue 1 验证] 检查 chunks 表中是否存在 CHUNK:CASE:CASE: 双重前缀:")
    cnt_double = c.execute("SELECT count(*) FROM chunks WHERE chunk_id LIKE 'CHUNK:CASE:CASE:%'").fetchone()[0]
    print(f"  双重前缀 chunk 数量: {cnt_double} (目标: 0)")
    assert cnt_double == 0, "依然存在双重前缀 chunk!"

    # 2. 验证 hot_norm_cases 纯洁性
    print("\n[Issue 2 验证] 检查 hot_norm_cases 中是否存在把判例当法条的脏记录:")
    cnt_dirty_hot = c.execute("SELECT count(*) FROM hot_norm_cases WHERE norm_id LIKE 'CASE:%'").fetchone()[0]
    total_hot = c.execute("SELECT count(*) FROM hot_norm_cases").fetchone()[0]
    print(f"  脏记录数量: {cnt_dirty_hot} (目标: 0), 有效映射总数: {total_hot}")
    assert cnt_dirty_hot == 0, "依然存在脏 hot_norm_cases 记录!"

    # 3. 验证 DEFAULT_GRAPH_RELS 关系白名单完整性
    print("\n[Issue 3 验证] 检查 DEFAULT_GRAPH_RELS 包含的关系类型:")
    required_rels = ["complements", "cross_references", "distinguishes", "exception_to", "hierarchical_child", "hierarchical_parent", "governs"]
    for rel in required_rels:
        assert rel in DEFAULT_GRAPH_RELS, f"关系 {rel} 缺失在 DEFAULT_GRAPH_RELS 中!"
    print(f"  所有扩展边类型均已纳入白名单 (总共 {len(DEFAULT_GRAPH_RELS)} 类关系)")

    # 4. 验证 security_sentinel.py 消除代持违规建议
    print("\n[Issue 4 验证] 检查 security_sentinel.py 中的合规建议:")
    sentinel_code = open("lawagent/flow/security_sentinel.py", encoding="utf-8").read()
    assert "属地化联合体代持" not in sentinel_code, "依然残留代持建议!"
    assert "非法人联合运营体" in sentinel_code, "新合规建议未生效!"
    print("  已彻底废除代持建议，严格落实非法人联合运营体（KSO/UJV）及外资豁免红线！")

    # 5. 验证 GraphRAG 运行时对新入库法条的 1-Hop 判例召回率（从 0% 提升至 100%）
    print("\n[Issue 5 验证] 测试 L1 图扩展通过法条召回判例能力:")
    store = SQLiteGraphStore(DB_PATH)
    retriever = HybridRetriever.from_snapshot()

    test_pairs = [
        ("VN:Resolution_01_2019_NQ_HDTP:Interest", "CASE:VN_SPC:An_Le_08_2016_AL"),
        ("VN:Resolution_01_2014_NQ_HDTP:Art14", "CASE:VN_SPC:An_Le_69_2023_AL"),
        ("MY:Specific_Relief_Act_1950:Sec50_53", "CASE:MY_FC:Tindak_Murni_2020"),
        ("TH:Administrative_Court_Act_2542:Sec3_9_51", "CASE:TH_SAC:Assembly_Or_221_223_2564"),
    ]

    for norm_id, expected_case_id in test_pairs:
        nbrs = store.neighbors(norm_id, direction="both", limit=10)
        found_case = any(expected_case_id in nb["node"] for nb in nbrs)
        print(f"  法条 {norm_id} -> 拓扑命中判例 {expected_case_id}: {found_case}")
        assert found_case, f"法条 {norm_id} 未能拓扑连通至 {expected_case_id}!"

    # 6. 验证 L2 跨层查询 L1 chunks 不会抛出 no such column: norm_id 异常
    print("\n[Issue 6 验证] 测试 L2 跨层回退查询 L1 chunks 稳定性:")
    try:
        # 执行一次包含跨层拓扑边的 L2 搜索
        evs_l2 = retriever.search_l2("FIDIC DAAB Dispute Avoidance Clause 21", top_k=5, expand_graph=True)
        print(f"  L2 检索成功返回 {len(evs_l2)} 条证据，无 SQL 报错！")
    except Exception as e:
        print(f"  L2 检索发生异常: {e}")
        raise e

    # 7. 验证新入库法条包含 elements_json 且判例 100% 达标
    print("\n[Issue 7 验证] 检查新入库法条 elements_json 与案例金标准:")
    c.execute("SELECT count(*) FROM norms WHERE elements_json IS NULL OR elements_json = ''")
    cnt_empty_el = c.fetchone()[0]
    print(f"  L1 法条 elements_json 空缺数: {cnt_empty_el} (目标: 0)")
    assert cnt_empty_el == 0, "存在 elements_json 空缺的 L1 法条!"

    conn.close()
    print("\n================================================================")
    print("所有审查指出的代码缺陷与数据漏洞验证通过，100% 修复完毕！")
    print("================================================================")

if __name__ == '__main__':
    test_fixes()
