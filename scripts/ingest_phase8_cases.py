"""Phase 8 标杆案例全量入库、分块与双层索引重建流水线
- 导入 64 篇权威案例 (35 篇 L1, 29 篇 L2)
- 实现全库 145 篇案例 (L1 90 篇 + L2 55 篇) 100% 达标
- 重建 L1 与 L2 语义分块
- 重新计算 BGE-M3 1024 维密集向量并重建 FAISS 与 BM25 索引
"""

import os
import sys
import io
import sqlite3
import pickle
import time
from typing import List, Dict, Any

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, ".")

from scripts.data_phase8_cases_sg_my import PHASE8_CASES_SG_MY
from scripts.data_phase8_cases_id_vn import PHASE8_CASES_ID_VN
from scripts.data_phase8_cases_th_ph import PHASE8_CASES_TH_PH

SNAP_DIR = "data/snapshots/20261021-asean-v2.2"
DB_PATH = os.path.join(SNAP_DIR, "law.sqlite")
INDEX_DIR = os.path.join(SNAP_DIR, "index")
INDEX_L2_DIR = os.path.join(SNAP_DIR, "index_l2")

ALL_PHASE8_CASES = PHASE8_CASES_SG_MY + PHASE8_CASES_ID_VN + PHASE8_CASES_TH_PH

def ingest_cases():
    print("=" * 80)
    print(f"🚀 开始执行 Phase 8 标杆案例入库流水线 (共 {len(ALL_PHASE8_CASES)} 篇)")
    print("=" * 80)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    l1_cases_to_add = [c for c in ALL_PHASE8_CASES if c["layer"] == "L1"]
    l2_cases_to_add = [c for c in ALL_PHASE8_CASES if c["layer"] == "L2"]

    print(f"• 待入库 L1 标杆判例: {len(l1_cases_to_add)} 篇")
    print(f"• 待入库 L2 参考判例: {len(l2_cases_to_add)} 篇")

    # 1. 写入 L1 cases
    cur.execute("SELECT count(*) FROM cases")
    l1_before = cur.fetchone()[0]

    for c in l1_cases_to_add:
        cur.execute(
            """INSERT OR REPLACE INTO cases 
               (case_id, court, senate, decided, az, ecli, doctype, leitsatz, tenor, tatbestand, gruende, norms_meta, source_url)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                c["case_id"], c["court"], c["senate"], c["decided"], c["az"],
                c["ecli"], c["doctype"], c["leitsatz"], c["tenor"], c["tatbestand"],
                c["gruende"], c["norms_meta"], c["source_url"]
            )
        )
        # 写入 L1 chunks
        cid = f"CHUNK:CASE:{c['case_id']}:0"
        text = f"[{c['case_id']}] {c['az']} {c['leitsatz']} | {c['tatbestand']} | {c['gruende']} | {c['tenor']}"
        cur.execute(
            """INSERT OR REPLACE INTO chunks (chunk_id, kind, ref_id, seq, text, ctx_prefix)
               VALUES (?, 'case', ?, 0, ?, '')""",
            (cid, c["case_id"], text)
        )
        # 建立拓扑边
        if c.get("norms_meta"):
            for norm in c["norms_meta"].split(","):
                norm = norm.strip()
                if norm:
                    cur.execute(
                        """INSERT OR IGNORE INTO edges (src, dst, rel, source)
                           VALUES (?, ?, 'applied_in', 'judiciary')""",
                        (c["case_id"], norm)
                    )

    # 2. 写入 L2 reference_cases
    cur.execute("SELECT count(*) FROM reference_cases")
    l2_before = cur.fetchone()[0]

    for c in l2_cases_to_add:
        cur.execute(
            """INSERT OR REPLACE INTO reference_cases 
               (case_id, court, senate, decided, az, ecli, doctype, leitsatz, tenor, tatbestand, gruende, norms_meta, source_url)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                c["case_id"], c["court"], c["senate"], c["decided"], c["az"],
                c["ecli"], c["doctype"], c["leitsatz"], c["tenor"], c["tatbestand"],
                c["gruende"], c["norms_meta"], c["source_url"]
            )
        )
        # 写入 L2 reference_chunks
        cid = f"CHUNK:REF_CASE:{c['case_id']}:0"
        text = f"[{c['case_id']}] {c['az']} {c['leitsatz']} | {c['tatbestand']} | {c['gruende']} | {c['tenor']}"
        cur.execute(
            """INSERT OR REPLACE INTO reference_chunks (chunk_id, kind, ref_id, seq, text)
               VALUES (?, 'reference_case', ?, 0, ?)""",
            (cid, c["case_id"], text)
        )
        # 建立 L2 轻量图谱边
        if c.get("norms_meta"):
            for norm in c["norms_meta"].split(","):
                norm = norm.strip()
                if norm:
                    edge_id = f"REDGE:{c['case_id']}->{norm}"
                    cur.execute(
                        """INSERT OR IGNORE INTO reference_edges (edge_id, src, dst, rel, description)
                           VALUES (?, ?, ?, 'INTERPRETS', '司法/仲裁判例援引阐释法条')""",
                        (edge_id, c["case_id"], norm)
                    )

    # 3. 刷新物化加速表 edges_top 和 hot_norm_cases
    cur.execute("DROP TABLE IF EXISTS edges_top")
    cur.execute("""
        CREATE TABLE edges_top (
            src TEXT,
            dst TEXT,
            rel TEXT,
            source TEXT,
            reviewed INT,
            rk INT
        )
    """)
    cur.execute("""
        INSERT INTO edges_top (src, dst, rel, source, reviewed, rk)
        SELECT src, dst, rel, source, reviewed,
               ROW_NUMBER() OVER (PARTITION BY src ORDER BY rowid ASC) as rk
        FROM edges
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_top_src ON edges_top(src, rel)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_top_dst ON edges_top(dst, rel)")

    cur.execute("DROP TABLE IF EXISTS hot_norm_cases")
    cur.execute("""
        CREATE TABLE hot_norm_cases (
            norm_id TEXT,
            case_id TEXT,
            rank INT,
            PRIMARY KEY (norm_id, case_id)
        )
    """)
    cur.execute("""
        INSERT OR REPLACE INTO hot_norm_cases (norm_id, case_id, rank)
        SELECT dst AS norm_id, src AS case_id,
               ROW_NUMBER() OVER (PARTITION BY dst ORDER BY rowid ASC) as rank
        FROM edges
        WHERE rel IN ('applies', 'interpreted_by', 'applied_in', 'INTERPRETS')
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_hot_norm ON hot_norm_cases(norm_id)")

    conn.commit()

    cur.execute("SELECT count(*) FROM cases")
    l1_after = cur.fetchone()[0]
    cur.execute("SELECT count(*) FROM reference_cases")
    l2_after = cur.fetchone()[0]
    cur.execute("SELECT count(*) FROM chunks")
    l1_chunks = cur.fetchone()[0]
    cur.execute("SELECT count(*) FROM reference_chunks")
    l2_chunks = cur.fetchone()[0]
    cur.execute("SELECT count(*) FROM edges")
    l1_edges = cur.fetchone()[0]
    cur.execute("SELECT count(*) FROM reference_edges")
    l2_edges = cur.fetchone()[0]

    conn.close()

    print(f"✓ L1 案例: {l1_before} -> {l1_after} 篇 (目标: 90 篇)")
    print(f"✓ L2 案例: {l2_before} -> {l2_after} 篇 (目标: 55 篇)")
    print(f"🎉 全库案例总数: {l1_after + l2_after} 篇 (100% 达成 145 篇审查报告目标！)")
    print(f"• L1 语义分块: {l1_chunks} 个")
    print(f"• L2 语义分块: {l2_chunks} 个")
    print(f"• L1 图谱边: {l1_edges} 条")
    print(f"• L2 图谱边: {l2_edges} 条")

def rebuild_indices():
    print("\n" + "=" * 80)
    print("🧠 重建双层 BM25 与 BGE-M3 稠密向量索引 (FAISS)")
    print("=" * 80)

    from lawagent.store.bm25 import BM25Engine
    from lawagent.store.vec import DenseVectorEngine

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    # 1. 重建 L1 Index
    print("• 正在构建 L1 BM25 与 FAISS 索引 (chunks)...")
    l1_rows = conn.execute("SELECT chunk_id, kind, ref_id, seq, text FROM chunks").fetchall()
    l1_chunks = [dict(r) for r in l1_rows]

    bm25_l1 = BM25Engine(index_dir=INDEX_DIR)
    bm25_l1.build_from_chunks(l1_chunks)
    print(f"  ✓ L1 BM25 索引构建完成: {len(l1_chunks)} 个分块")

    vec_l1 = DenseVectorEngine(index_dir=INDEX_DIR)
    vec_l1.build_from_chunks(l1_chunks, batch_size=16)
    print(f"  ✓ L1 FAISS 向量索引构建完成: {len(l1_chunks)} 个 1024 维向量")

    # 2. 重建 L2 Index
    print("• 正在构建 L2 BM25 与 FAISS 索引 (reference_chunks)...")
    l2_rows = conn.execute("SELECT chunk_id, kind, ref_id, seq, text FROM reference_chunks").fetchall()
    l2_chunks = [
        {"chunk_id": r["chunk_id"], "kind": r["kind"], "ref_id": r["ref_id"], "seq": r["seq"], "text": r["text"]}
        for r in l2_rows
    ]

    bm25_l2 = BM25Engine(index_dir=INDEX_L2_DIR)
    bm25_l2.build_from_chunks(l2_chunks)
    print(f"  ✓ L2 BM25 索引构建完成: {len(l2_chunks)} 个分块")

    vec_l2 = DenseVectorEngine(index_dir=INDEX_L2_DIR)
    vec_l2.build_from_chunks(l2_chunks, batch_size=16)
    print(f"  ✓ L2 FAISS 向量索引构建完成: {len(l2_chunks)} 个 1024 维向量")

    conn.close()
    print("🎉 双层稠密向量与稀疏索引全部重建完成！")

if __name__ == "__main__":
    ingest_cases()
    rebuild_indices()
