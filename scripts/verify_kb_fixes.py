import sys
import sqlite3
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from lawagent.store.snapshots import SnapshotManager
from lawagent.store.graph import SQLiteGraphStore
from lawagent.store.retriever import HybridRetriever

def verify_all():
    print("=" * 70)
    print("🔍 开始验证本地数据库修复与 GraphRAG 增强效果")
    print("=" * 70)

    mgr = SnapshotManager()
    snap_id = mgr.get_current_snapshot_id()
    conn = mgr.get_connection(snap_id)
    cur = conn.cursor()

    # 1. 检查条文与判例规模
    n_norms = cur.execute("SELECT count(*) FROM norms").fetchone()[0]
    n_cases = cur.execute("SELECT count(*) FROM cases").fetchone()[0]
    n_chunks = cur.execute("SELECT count(*) FROM chunks").fetchone()[0]
    n_edges = cur.execute("SELECT count(*) FROM edges").fetchone()[0]
    n_edges_top = cur.execute("SELECT count(*) FROM edges_top").fetchone()[0]
    print(f"\n1. 数据库最新规模:")
    print(f"   - 权威法条 (norms): {n_norms} (预期: 33)")
    print(f"   - 裁判判例 (cases): {n_cases} (预期: 7)")
    print(f"   - 文本分块 (chunks): {n_chunks} (预期: 54)")
    print(f"   - 基础拓扑边 (edges): {n_edges}")
    print(f"   - 物化一跳边 (edges_top): {n_edges_top}")
    assert n_norms == 33, f"Norms count mismatch: {n_norms}"
    assert n_chunks == 54, f"Chunks count mismatch: {n_chunks}"

    # 2. 检查图谱边悬挂外键 (Dangling Edges)
    print("\n2. 检验图谱边引用完整性 (悬挂外键排查):")
    dangling_count = 0
    for edge in cur.execute("SELECT src, dst, rel FROM edges").fetchall():
        src_norm = cur.execute("SELECT norm_id FROM norms WHERE norm_id = ?", (edge[0],)).fetchone()
        src_case = cur.execute("SELECT case_id FROM cases WHERE case_id = ?", (edge[0],)).fetchone()
        dst_norm = cur.execute("SELECT norm_id FROM norms WHERE norm_id = ?", (edge[1],)).fetchone()
        dst_case = cur.execute("SELECT case_id FROM cases WHERE case_id = ?", (edge[1],)).fetchone()

        src_valid = bool(src_norm or src_case)
        dst_valid = bool(dst_norm or dst_case)
        status = "✓ VALID" if (src_valid and dst_valid) else "✗ DANGLING"
        print(f"   [{status}] {edge[0]} --[{edge[2]}]--> {edge[1]}")
        if not (src_valid and dst_valid):
            dangling_count += 1
    assert dangling_count == 0, f"Found {dangling_count} dangling edges!"
    print(f"   -> 悬挂边校验通过！0 悬挂，100% 闭环有效。")

    # 3. 验证 GraphRAG 双向图漫游与扩展 (expand)
    print("\n3. 检验 GraphStore 双向图漫游与关系扩展:")
    graph = SQLiteGraphStore(conn)

    # 3.1 从 FIDIC 14.8 款逆向扩展冲突的属地强行法
    expanded = graph.expand(["FIDIC:Silver_1999:Clause_14.8"], max_hops=1)
    nodes = [item["node"] for item in expanded]
    print(f"   -> 从 FIDIC 14.8 (背靠背付款) 扩展出的关联法源: {nodes}")
    assert any("CIPAA" in n for n in nodes), "Failed to expand to CIPAA!"
    assert any("SOPA" in n for n in nodes), "Failed to expand to SOPA!"
    print("   ✓ 成功沿 conflicts_with 边逆向穿透识别出马来西亚 CIPAA Sec 35 与新加坡 SOPA Sec 9 强行法！")

    # 3.2 从数据安全法第 36 条正向扩展
    expanded_ds = graph.expand(["CN:Data_Security_Law:Art36"], max_hops=1)
    nodes_ds = [item["node"] for item in expanded_ds]
    print(f"   -> 从数据安全法第36条扩展出的关联法源: {nodes_ds}")
    assert any("SG:IAA_Cap_143A:Sec12A" in n for n in nodes_ds), "Failed to expand to SG IAA Sec 12A!"
    print("   ✓ 成功沿 overrides 边识别出新加坡国际仲裁法第 12A 条调证保全冲突！")

    # 4. 验证 norm_lookup 别名与跨格式兼容映射
    print("\n4. 检验 SnapshotManager.norm_lookup 别名容错解析:")
    test_cases = [
        ("ID_MEMR:Reg11_2024", "ID:MEMR_11_2024"),
        ("ID_UU:2_2017:Art57", "ID:UU_2_2017:Art57"),
        ("FIDIC_SILVER:Clause8.4", "FIDIC:Silver_1999:Clause_8.4"),
        ("FIDIC_SILVER:Clause14.8", "FIDIC:Silver_1999:Clause_14.8"),
        ("VN_Law135_2025:Art86_2", "VN:Law_135_2025:Art86.2"),
        ("MY_CIPAA:Sec35", "MY:CIPAA_2012:Sec35"),
        ("SG_SOPA:Sec9", "SG:SOPA_2004:Sec9"),
        ("SG_IAA:Sec12A", "SG:IAA_Cap_143A:Sec12A"),
        ("PH_RA11966:PPP_Code", "PH:RA_11966:Sec18"),
        ("PRC_DATA_SECURITY:Art36", "CN:Data_Security_Law:Art36"),
    ]
    for input_id, expected_norm_id in test_cases:
        res = mgr.norm_lookup(input_id)
        assert res is not None, f"Failed to lookup: {input_id}"
        assert res["norm_id"] == expected_norm_id, f"Expected {expected_norm_id}, got {res['norm_id']}"
        print(f"   ✓ 格式映射: '{input_id}' => '{res['norm_id']}' (成功命中)")

    # 5. 验证 HybridRetriever 端到端检索与图漫游联动
    print("\n5. 检验 HybridRetriever 混合检索与 GraphRAG 联动:")
    retriever = HybridRetriever(snapshot_mgr=mgr, graph_store=graph)
    evs = retriever.search("背靠背分包付款协议与 FIDIC 14.8 条款法律效力", top_k=5)
    print(f"   -> 检索召回证据数: {len(evs)}")
    ref_ids = [e.ref_id for e in evs]
    print(f"   -> 召回法源列表: {ref_ids}")
    # 检验是否同时召回了 FIDIC 14.8 及对应的强行法 CIPAA / SOPA
    assert any("FIDIC" in r for r in ref_ids), "Missing FIDIC clause in retrieval!"
    assert any("CIPAA" in r or "SOPA" in r or "Bauer" in r for r in ref_ids), "Missing CIPAA/SOPA/Bauer in retrieval!"
    print("   ✓ HybridRetriever 成功通过图漫游融合检索出国际标准合同及对抗性属地强行法与先例！")

    print("\n" + "=" * 70)
    print("🎉 本地数据库与 GraphRAG 增强验证全部通过！无逻辑错误，无悬挂外键！")
    print("=" * 70)

if __name__ == "__main__":
    verify_all()
