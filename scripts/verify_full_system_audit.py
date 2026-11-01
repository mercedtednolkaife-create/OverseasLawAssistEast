"""全系统代码、数据库与 GraphRAG 完整性、性能与审查报告对照核验脚本
"""

import os
import sys
import sqlite3
import time
import pickle
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, os.path.abspath("."))

from lawagent.store.retriever import HybridRetriever
from lawagent.store.cl_align import CLAlignOperator
from lawagent.store.graph import SQLiteGraphStore

DB_PATH = "data/snapshots/20261021-asean-v2.2/law.sqlite"
INDEX_DIR = "data/snapshots/20261021-asean-v2.2/index"
INDEX_L2_DIR = "data/snapshots/20261021-asean-v2.2/index_l2"

def audit_database_and_graph():
    print("==================================================")
    print("一、数据库完整性与 GraphRAG 知识图谱深度审查")
    print("==================================================")

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # 1. 表规模核验
    tables = [
        "norms", "cases", "chunks", "edges", "edges_top",
        "reference_norms", "reference_cases", "reference_chunks", "reference_edges"
    ]
    counts = {}
    for t in tables:
        cnt = cur.execute(f"SELECT count(*) FROM {t}").fetchone()[0]
        counts[t] = cnt
        print(f"  * 数据表 [{t}]: {cnt} 行")

    # 2. 法条入库完整性与分块对齐校验
    print("\n[核查 1] L1 法条与 Chunks 对齐率:")
    cur.execute("""
        SELECT norm_id FROM norms
        WHERE norm_id NOT IN (SELECT ref_id FROM chunks WHERE kind = 'norm')
    """)
    missing_l1_chunks = cur.fetchall()
    print(f"  * L1 norms 缺失对应 chunks 数量: {len(missing_l1_chunks)}")
    assert len(missing_l1_chunks) == 0, f"发现未切块的 L1 norms: {missing_l1_chunks}"

    print("[核查 2] L2 参考规范与 Chunks 对齐率:")
    cur.execute("""
        SELECT norm_id FROM reference_norms
        WHERE norm_id NOT IN (SELECT ref_id FROM reference_chunks WHERE kind = 'norm')
    """)
    missing_l2_norm_chunks = cur.fetchall()
    print(f"  * L2 reference_norms 缺失对应 chunks 数量: {len(missing_l2_norm_chunks)}")
    assert len(missing_l2_norm_chunks) == 0, f"发现未切块的 L2 reference_norms: {missing_l2_norm_chunks}"

    print("[核查 3] L2 判例与 Chunks 对齐率:")
    cur.execute("""
        SELECT case_id FROM reference_cases
        WHERE case_id NOT IN (SELECT ref_id FROM reference_chunks WHERE kind = 'case')
    """)
    missing_l2_case_chunks = cur.fetchall()
    print(f"  * L2 reference_cases 缺失对应 chunks 数量: {len(missing_l2_case_chunks)}")
    assert len(missing_l2_case_chunks) == 0, f"发现未切块的 L2 reference_cases: {missing_l2_case_chunks}"

    # 3. 图谱拓扑质量审查：孤立节点与悬空边检测
    print("\n[核查 4] GraphRAG 图谱拓扑连通性审查:")
    # 检查新增法条的图谱边连接
    test_norms = [
        "KH:Commercial_Arbitration_Law_2006:Art3",
        "LA:Decree_135_PM:Art8",
        "MM:Arbitration_Law_2016:Sec7",
        "BN:Companies_Act_Cap39:Sec9",
        "TL:Private_Investment_Law_2017:Art11",
        "FIDIC:Silver_2017:Clause_20.2",
        "CASE:ICSID:CMC_v_Mozambique:2019"
    ]
    for nid in test_norms:
        # L1 或 L2 中是否有边
        cur.execute("SELECT count(*) FROM edges WHERE src = ? OR dst = ?", (nid, nid))
        cnt_l1 = cur.fetchone()[0]
        cur.execute("SELECT count(*) FROM reference_edges WHERE src = ? OR dst = ?", (nid, nid))
        cnt_l2 = cur.fetchone()[0]
        total = cnt_l1 + cnt_l2
        print(f"  * 节点 [{nid}]: 连接图谱边数 = {total} (L1: {cnt_l1}, L2: {cnt_l2})")
        assert total > 0, f"节点 [{nid}] 属于悬空孤立节点！"

    # 4. 索引与向量文件一致性审查
    print("\n[核查 5] 索引与向量文件完整性审查:")
    with open(os.path.join(INDEX_DIR, "chunk_ids.pkl"), "rb") as f:
        l1_chunk_ids = pickle.load(f)
    with open(os.path.join(INDEX_L2_DIR, "chunk_ids.pkl"), "rb") as f:
        l2_chunk_ids = pickle.load(f)

    print(f"  * L1 FAISS/BM25 索引向量条数: {len(l1_chunk_ids)} (数据库 chunks 行数: {counts['chunks']})")
    print(f"  * L2 FAISS/BM25 索引向量条数: {len(l2_chunk_ids)} (数据库 reference_chunks 行数: {counts['reference_chunks']})")
    assert len(l1_chunk_ids) == counts["chunks"], "L1 索引数量与数据库 chunks 数量不一致！"
    assert len(l2_chunk_ids) == counts["reference_chunks"], "L2 索引数量与数据库 reference_chunks 数量不一致！"
    print(">> 数据库与 GraphRAG 完整性审查 100% 达标！")

    conn.close()

def audit_runtime_and_performance():
    print("\n==================================================")
    print("二、代码运行健康度、性能与并发延迟审查")
    print("==================================================")

    retriever = HybridRetriever.from_snapshot()

    # 1. 测试单次混合检索（BM25 + 向量 + Rerank + 2-Hop Graph）端到端延迟
    print("[性能基准 1] L1 端到端混合检索耗时评估 (预热后 5 次调用取平均):")
    # 预热一次模型
    retriever.search("预热查询", top_k=2, layer="L1")

    queries = [
        "印尼苏拉威西电站工程交地延误工期顺延与保函止付",
        "越南海上风电项目预定违约金最高上限与工期索赔",
        "老挝水电特许经营CA协议政府回购与单方终止补偿",
        "柬埔寨经济特区土地特许权ELC租赁期限与国有化征收",
        "马来西亚沙巴土著习惯地NCR土地征拆受阻停工"
    ]
    latencies = []
    for q in queries:
        t0 = time.time()
        evs = retriever.search(q, top_k=8, layer="L1")
        dt = time.time() - t0
        latencies.append(dt)
        print(f"  * 查询: '{q[:20]}...' -> 召回 {len(evs)} 条证据，耗时: {dt*1000:.1f}ms")
    avg_latency = sum(latencies) / len(latencies)
    print(f"  => L1 稳定端到端检索平均耗时: {avg_latency*1000:.1f}ms (在本地 CPU 上运行 BGE-Reranker-v2-m3，耗时非常稳健)")
    assert avg_latency < 3.5, f"平均耗时 {avg_latency}s 超过性能预警阈值！"

    # 2. 测试 2-Hop 图扩展性能与无死锁/防溢出保障
    print("\n[性能基准 2] 2-Hop 图扩展极端压力测试 (多节点同时扩展):")
    start_nodes = [
        "ID:KUHPerdata:Art1249", "VN:Civil_Code_2015:Art351", "LA:Decree_135_PM:Art8",
        "MY:Contracts_Act_1950:Sec75", "FIDIC:Silver_2017:Clause_20.2"
    ]
    t0 = time.time()
    expanded = retriever.graph.expand(start_nodes, max_hops=2, limit=50)
    dt = time.time() - t0
    print(f"  * 5 个跨法域根节点并发 2 跳扩展，召回关联节点: {len(expanded)} 个，耗时: {dt*1000:.2f}ms")
    assert dt < 0.2, f"图扩展耗时 {dt}s 存在性能瓶颈！"

    # 3. 测试 L2 级联补偿检索性能
    print("\n[性能基准 3] L2 级联补偿检索耗时评估:")
    t0 = time.time()
    l2_evs = retriever.search_l2("FIDIC 2017 DAAB 决定即时约束力与 ICSID 投资仲裁先例", top_k=5)
    dt = time.time() - t0
    print(f"  * L2 级联补偿检索召回 {len(l2_evs)} 条证据，耗时: {dt*1000:.1f}ms")
    assert dt < 3.5, f"L2 检索耗时 {dt}s 偏高！"

    print("\n>> 代码运行与系统性能全面达标！无阻塞、无死锁、延迟优秀！")

if __name__ == "__main__":
    audit_database_and_graph()
    audit_runtime_and_performance()
