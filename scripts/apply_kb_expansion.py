import os
import sys

sys.path.insert(0, os.path.abspath("."))
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import json
import sqlite3
from datetime import datetime

from scripts.kb_expansion_data import (
    NEW_NORMS_DATA,
    NEW_CASES_DATA,
    NEW_EDGES_DATA,
    NEW_HOT_CASES_DATA,
    NEW_RISK_COMMUNITIES
)


def apply_database_expansion():
    print("=" * 70)
    print("🚀 开始执行东盟六国法源与判例数据库全量扩充")
    print("=" * 70)

    db_path = "data/snapshots/20261021-asean-v2.2/law.sqlite"
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # 1. 检查数据库现有法源
    cur.execute("SELECT norm_id FROM norms")
    existing_db_norms = {r[0] for r in cur.fetchall()}
    to_add_norms = [n for n in NEW_NORMS_DATA if n["norm_id"] not in existing_db_norms]
    print(f"-> law.sqlite 现有规范: {len(existing_db_norms)} 条")
    print(f"-> 待注入全新法源条文: {len(to_add_norms)} 条 (总预备条文: {len(NEW_NORMS_DATA)} 条)")

    # 2. 检查数据库现有判例
    cur.execute("SELECT case_id FROM cases")
    existing_db_cases = {r[0] for r in cur.fetchall()}
    to_add_cases = [c for c in NEW_CASES_DATA if c["case_id"] not in existing_db_cases]
    print(f"-> law.sqlite 现有先例: {len(existing_db_cases)} 篇")
    print(f"-> 待注入权威司法/仲裁判例: {len(to_add_cases)} 篇 (总预备判例: {len(NEW_CASES_DATA)} 篇)")

    # 3. 检查数据库现有关系边
    cur.execute("SELECT src, dst, rel FROM edges")
    existing_db_edges = {(r[0], r[1], r[2]) for r in cur.fetchall()}
    to_add_edges = [e for e in NEW_EDGES_DATA if (e["src"], e["dst"], e["rel"]) not in existing_db_edges]
    print(f"-> law.sqlite 现有拓扑边: {len(existing_db_edges)} 条")
    print(f"-> 待注入三层拓扑对抗边: {len(to_add_edges)} 条 (总预备边: {len(NEW_EDGES_DATA)} 条)")

    now_str = datetime.now().isoformat()
    snap_id = "20261021-asean-v2.2"

    # 注入全量新法条 (支持增量与全量覆盖更新)
    for item in NEW_NORMS_DATA:
        cur.execute(
            """INSERT INTO norms(
                 norm_id, law, enbez, title, heading_path, text_de, structure, footnotes, stand,
                 has_pending_amend, source_url, snapshot_id, fetched_at,
                 language_mode, lang_original, text_original, text_en, text_zh,
                 translation_source, norm_category, fidic_tier, fidic_edition,
                 elements_json, mandatory_level
               )
               VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
               ON CONFLICT(norm_id) DO UPDATE SET
                 title=excluded.title,
                 heading_path=excluded.heading_path,
                 text_de=excluded.text_de,
                 language_mode=excluded.language_mode,
                 lang_original=excluded.lang_original,
                 text_original=excluded.text_original,
                 text_en=excluded.text_en,
                 text_zh=excluded.text_zh,
                 translation_source=excluded.translation_source,
                 norm_category=excluded.norm_category,
                 fidic_tier=excluded.fidic_tier,
                 fidic_edition=excluded.fidic_edition,
                 elements_json=excluded.elements_json,
                 mandatory_level=excluded.mandatory_level,
                 fetched_at=excluded.fetched_at""",
            (
                item["norm_id"], item["law"], item["enbez"], item["title"], item["heading_path"],
                item.get("text_de", ""), "", "", "2026",
                0, "https://overseas-law.moj.gov.cn/fatong", snap_id, now_str,
                item.get("language_mode", "bilingual"), item.get("lang_original", "en"),
                item.get("text_original", ""), item.get("text_en", ""), item.get("text_zh", ""),
                item.get("translation_source", "MOJ_FATONG_2026"), item.get("norm_category", "statute"),
                item.get("fidic_tier"), item.get("fidic_edition"),
                item.get("elements_json", "[]"), item.get("mandatory_level", "default")
            )
        )
    print(f"✓ 成功向 law.sqlite 注入/更新 {len(NEW_NORMS_DATA)} 条新法源")

    # 注入判例
    for case in NEW_CASES_DATA:
        cur.execute(
            """INSERT INTO cases(
                 case_id, court, senate, decided, az, ecli, doctype,
                 leitsatz, tenor, tatbestand, gruende, norms_meta,
                 source_url, snapshot_id, fetched_at
               )
               VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
               ON CONFLICT(case_id) DO UPDATE SET
                 court=excluded.court,
                 senate=excluded.senate,
                 decided=excluded.decided,
                 az=excluded.az,
                 ecli=excluded.ecli,
                 doctype=excluded.doctype,
                 leitsatz=excluded.leitsatz,
                 tenor=excluded.tenor,
                 tatbestand=excluded.tatbestand,
                 gruende=excluded.gruende,
                 norms_meta=excluded.norms_meta,
                 source_url=excluded.source_url,
                 fetched_at=excluded.fetched_at""",
            (
                case["case_id"], case["court"], case["senate"], case["decided"],
                case["az"], case["ecli"], case["doctype"], case["leitsatz"],
                case["tenor"], case["tatbestand"], case["gruende"],
                case["norms_meta"], case["source_url"], snap_id, now_str
            )
        )
    print(f"✓ 成功向 law.sqlite 注入/更新 {len(NEW_CASES_DATA)} 篇权威司法先例")

    # 注入关系边与 edges_top
    for edge in NEW_EDGES_DATA:
        if (edge["src"], edge["dst"], edge["rel"]) not in existing_db_edges:
            cur.execute(
                """INSERT INTO edges(src, dst, rel, source, span, confidence, reviewed, snapshot_id)
                   VALUES(?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    edge["src"], edge["dst"], edge["rel"], edge["source"],
                    "", edge["confidence"], edge["reviewed"], snap_id
                )
            )
            src_node = edge['src'] if edge['src'].startswith(("NORM:", "CASE:", "CPT:")) else f"NORM:{edge['src']}"
            dst_node = edge['dst'] if edge['dst'].startswith(("NORM:", "CASE:", "CPT:")) else f"NORM:{edge['dst']}"
            cur.execute(
                """INSERT INTO edges_top(src, dst, rel, source, reviewed, rk)
                   VALUES(?, ?, ?, ?, ?, 1)""",
                (src_node, dst_node, edge["rel"], edge["source"], edge["reviewed"])
            )
    print(f"✓ 成功向 law.sqlite 注入/核实拓扑关系边")

    # 注入 hot_norm_cases
    for n_id, c_id, rk in NEW_HOT_CASES_DATA:
        cur.execute("INSERT OR REPLACE INTO hot_norm_cases(norm_id, case_id, rank) VALUES(?, ?, ?)", (n_id, c_id, rk))
    print(f"✓ 成功注入 {len(NEW_HOT_CASES_DATA)} 组热门法条判例映射")

    # 注入 risk_communities
    for rc in NEW_RISK_COMMUNITIES:
        cur.execute(
            """INSERT INTO risk_communities(
                 community_id, name_zh, risk_level, host_countries,
                 archetypes, norm_ids, trigger_scenarios, redline_actions
               )
               VALUES(?, ?, ?, ?, ?, ?, ?, ?)
               ON CONFLICT(community_id) DO UPDATE SET
                 name_zh=excluded.name_zh,
                 risk_level=excluded.risk_level,
                 host_countries=excluded.host_countries,
                 archetypes=excluded.archetypes,
                 norm_ids=excluded.norm_ids,
                 trigger_scenarios=excluded.trigger_scenarios,
                 redline_actions=excluded.redline_actions""",
            (
                rc["community_id"], rc["name_zh"], rc["risk_level"],
                rc["host_countries"], rc["archetypes"], rc["norm_ids"],
                rc["trigger_scenarios"], rc["redline_actions"]
            )
        )
    print(f"✓ 成功注入/更新 {len(NEW_RISK_COMMUNITIES)} 个风险社区")

    conn.commit()

    cur.execute("SELECT count(*) FROM norms")
    total_norms_now = cur.fetchone()[0]
    cur.execute("SELECT count(*) FROM cases")
    total_cases_now = cur.fetchone()[0]
    cur.execute("SELECT count(*) FROM edges")
    total_edges_now = cur.fetchone()[0]
    print(f"\n📊 数据库当前全量规模统计: 法条={total_norms_now}, 判例={total_cases_now}, 拓扑边={total_edges_now}")

    # 4. 重新切块 chunks
    print("\n-> 正在重新生成知识库 Chunks...")
    from lawagent.store.snapshots import SnapshotManager
    from lawagent.store.chunker import build_and_save_chunks
    mgr = SnapshotManager()
    all_norms = mgr.get_all_norms(snap_id)
    all_cases = mgr.get_all_cases(snap_id)
    total_chunks = build_and_save_chunks(conn, all_norms, all_cases)
    print(f"✓ 全量分块生成完毕，总 Chunks 达: {total_chunks}")

    # 5. 重构 BM25 索引
    print("\n-> 正在训练并持久化新版 BM25 词法检索索引...")
    from lawagent.store.bm25 import BM25Engine
    index_dir = os.path.join(mgr.base_dir, snap_id, "index")
    rows = conn.execute("SELECT chunk_id, kind, ref_id, seq, text FROM chunks").fetchall()
    chunks = [dict(r) for r in rows]
    bm25 = BM25Engine(index_dir=index_dir)
    bm25.build_from_chunks(chunks)
    print("✓ 新版 BM25 词法索引重构完成")

    # 6. 重构 FAISS 稠密向量索引
    print("\n-> 正在调用 GPU/BGE-M3 批量生成稠密语义向量并构建 FAISS 索引...")
    from lawagent.store.vec import DenseVectorEngine
    try:
        vec_engine = DenseVectorEngine(index_dir=index_dir)
        vec_engine.build_from_chunks(chunks, batch_size=16)
        print("✓ 新版 FAISS 向量索引构建完成")
    except Exception as e:
        print(f"⚠️ 向量索引构建提示: {e}")

    conn.close()
    print("\n" + "=" * 70)
    print("🎉 数据库扩充与全量索引持久化大功告成！")
    print("=" * 70)


if __name__ == "__main__":
    apply_database_expansion()
