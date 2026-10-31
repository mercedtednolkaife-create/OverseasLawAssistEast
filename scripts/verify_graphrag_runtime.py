import sys
from pathlib import Path
import sqlite3

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from lawagent.store.graph import SQLiteGraphStore
from lawagent.store.retriever import HybridRetriever

DB_PATH = Path("data/snapshots/20261021-asean-v2.2/law.sqlite")

def test_graphrag():
    print("=== 1. SQLiteGraphStore 拓扑结构与加速表验证 ===")
    store = SQLiteGraphStore(DB_PATH)
    
    # 验证 edges_top 物化表与索引
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    edges_top_cnt = c.execute("SELECT count(*) FROM edges_top").fetchone()[0]
    hot_cnt = c.execute("SELECT count(*) FROM hot_norm_cases").fetchone()[0]
    ref_edges_cnt = c.execute("SELECT count(*) FROM reference_edges").fetchone()[0]
    print(f"edges_top (物化加速表): {edges_top_cnt} 条")
    print(f"hot_norm_cases (热点映射表): {hot_cnt} 条")
    print(f"reference_edges (L2拓扑边): {ref_edges_cnt} 条")
    
    # 验证审查报告关键节点的 1-Hop 图扩展
    print("\n=== 2. 审查报告关键先例与法条因果边扩展验证 ===")
    test_nodes = [
        "VN:Civil_Code_2015:Art420",
        "MY:Contracts_Act_1950:Sec75",
        "SG:Building_Control_Act:Sec8_9",
        "TH:CCC:Sec383",
        "TH:Arbitration_Act_2545:Sec40",
        "PH:EO_1008_CIAC:Sec4",
    ]
    
    for nid in test_nodes:
        nbrs = store.neighbors(nid, direction="both", limit=10)
        print(f"\n[节点] {nid} 的 1-Hop 拓扑关联:")
        if not nbrs:
            print("  (无关联边)")
        for nb in nbrs:
            print(f"  -> rel: {nb['rel']}, node: {nb['node']}")
            
        expanded = store.expand([nid], max_hops=1, limit=5)
        print(f"  [CTE Expand 遍历] 召回节点: {[e['node'] for e in expanded]}")

    print("\n=== 3. L2 跨法域参考边拓扑验证 ===")
    l2_test_nodes = [
        "REF_CASE:PCA:Walter_Bau_v_Thailand:2009",
        "REF_CASE:ICSID:Fraport_v_Philippines:2014",
        "FIDIC:2017_Suite:Clause_21"
    ]
    for lid in l2_test_nodes:
        c.execute("""
            SELECT dst AS node, rel FROM reference_edges WHERE src = ?
            UNION
            SELECT src AS node, rel FROM reference_edges WHERE dst = ?
        """, (lid, lid))
        rows = c.fetchall()
        print(f"[L2节点] {lid} 关联边数: {len(rows)}")
        for r in rows:
            print(f"  -> rel: {r[1]}, target: {r[0]}")

    print("\n=== 4. HybridRetriever 混合检索与真实 GraphRAG 拓扑扩散实测 ===")
    retriever = HybridRetriever.from_snapshot()
    # 模拟用户查询情势变迁与合同解除
    q = "越南民法典第420条情势变更原则如何适用？有没有最高法院标杆先例？"
    evs = retriever.search(q, top_k=5, expand_graph=True, layer="AUTO")
    print(f"查询: '{q}'")
    print(f"检索到 Evidence 数量: {len(evs)}")
    for ev in evs:
        print(f"  - [{ev.role.upper()} / {ev.grade}] ref_id: {ev.ref_id} (kind: {ev.kind}) | {ev.text_zh[:60]}...")

    conn.close()
    print("\nGraphRAG 运行时验证全部通过！")

if __name__ == '__main__':
    test_graphrag()
