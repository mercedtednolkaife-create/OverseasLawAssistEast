# -*- coding: utf-8 -*-
"""全量多段切块生成与双层索引重构脚本 (Multi-level Chunking & Dual-layer Index Rebuild)
1. 采用德式四要素分块（seq=0 摘要与主文、seq=1 事实 Tatbestand、seq=2+ 裁判理由）
2. 彻底消灭一案一块与 512 截断丢失事实缺陷
3. 统一收敛 L2 kind 字段为标准 'norm' 与 'case'（消除过滤失效缺陷）
4. 刷新 edges_top 物化加速表
5. 全量重构 L1 与 L2 的 BGE-M3 稠密向量索引 (FAISS) 与 BM25 词法倒排索引
"""

import sys
from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

import sqlite3
import json
from lawagent.store.chunker import chunk_norms, chunk_cases
from lawagent.store.bm25 import BM25Engine
from lawagent.store.vec import DenseVectorEngine

DB_PATH = Path("data/snapshots/20261021-asean-v2.2/law.sqlite")
INDEX_DIR = Path("data/snapshots/20261021-asean-v2.2/index")
INDEX_L2_DIR = Path("data/snapshots/20261021-asean-v2.2/index_l2")

def main():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    print("=== 1. 读取数据库并执行 L1 多段分块 ===")
    l1_norms_rows = [dict(r) for r in cur.execute("SELECT * FROM norms").fetchall()]
    l1_cases_rows = [dict(r) for r in cur.execute("SELECT * FROM cases").fetchall()]

    l1_norm_chunks = chunk_norms(l1_norms_rows)
    l1_case_chunks = chunk_cases(l1_cases_rows)
    all_l1_chunks = l1_norm_chunks + l1_case_chunks

    cur.execute("DELETE FROM chunks;")
    for ch in all_l1_chunks:
        cur.execute("""
            INSERT OR REPLACE INTO chunks (chunk_id, kind, ref_id, seq, text, ctx_prefix)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            ch["chunk_id"],
            "norm" if ch["kind"] == "norm" else "case",
            ch["ref_id"],
            ch["seq"],
            ch["text"],
            ch.get("ctx_prefix", "")
        ))
    conn.commit()
    print(f"L1 切块写入完成: 总切块数 {len(all_l1_chunks)} (其中案例切块数: {len(l1_case_chunks)})")

    print("\n=== 2. 读取数据库并执行 L2 多段分块 (统一收敛 kind 为 norm/case) ===")
    l2_norms_rows = [dict(r) for r in cur.execute("SELECT * FROM reference_norms").fetchall()]
    l2_cases_rows = [dict(r) for r in cur.execute("SELECT * FROM reference_cases").fetchall()]

    l2_norm_chunks = chunk_norms(l2_norms_rows)
    l2_case_chunks = chunk_cases(l2_cases_rows)
    all_l2_chunks = l2_norm_chunks + l2_case_chunks

    cur.execute("DELETE FROM reference_chunks;")
    for ch in all_l2_chunks:
        # Standardize kind to 'norm' and 'case'
        k = "norm" if ch["kind"] in ("norm", "reference_norm") else "case"
        cur.execute("""
            INSERT OR REPLACE INTO reference_chunks (chunk_id, kind, ref_id, seq, text)
            VALUES (?, ?, ?, ?, ?)
        """, (
            ch["chunk_id"],
            k,
            ch["ref_id"],
            ch["seq"],
            ch["text"]
        ))
    conn.commit()
    print(f"L2 切块写入完成: 总切块数 {len(all_l2_chunks)} (其中案例切块数: {len(l2_case_chunks)})")

    print("\n=== 3. 刷新 edges_top 物化加速表 ===")
    cur.execute("DELETE FROM edges_top;")
    cur.execute("""
        INSERT INTO edges_top (src, dst, rel, source, reviewed, rk)
        SELECT src, dst, rel, source, reviewed,
               ROW_NUMBER() OVER (PARTITION BY src ORDER BY confidence DESC) as rk
        FROM edges;
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_top_src ON edges_top(src, rel);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_top_dst ON edges_top(dst, rel);")
    conn.commit()
    cur.execute("SELECT count(*) FROM edges_top;")
    print(f"edges_top 物化加速表行数: {cur.fetchone()[0]}")

    print("\n=== 4. 重构 L1 BM25 与 DenseVector 索引 ===")
    bm25_l1 = BM25Engine(index_dir=INDEX_DIR)
    bm25_l1.build_from_chunks(all_l1_chunks)
    print("[OK] L1 BM25 索引重构完成")

    vec_l1 = DenseVectorEngine(index_dir=INDEX_DIR)
    vec_l1.build_from_chunks(all_l1_chunks, batch_size=16)
    print("[OK] L1 BGE-M3 向量索引重构完成")

    print("\n=== 5. 重构 L2 BM25 与 DenseVector 索引 ===")
    bm25_l2 = BM25Engine(index_dir=INDEX_L2_DIR)
    bm25_l2.build_from_chunks(all_l2_chunks)
    print("[OK] L2 BM25 索引重构完成")

    vec_l2 = DenseVectorEngine(index_dir=INDEX_L2_DIR)
    vec_l2.build_from_chunks(all_l2_chunks, batch_size=16)
    print("[OK] L2 BGE-M3 向量索引重构完成")

    conn.close()
    print("\n==================================================")
    print("多层分块生成与双层索引重构全流程圆满成功！")
    print("==================================================")

if __name__ == "__main__":
    main()
