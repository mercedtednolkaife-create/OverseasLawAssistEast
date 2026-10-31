# -*- coding: utf-8 -*-
"""
执行数据库审查方案的全量入库、去重提纯与拓扑索引重构脚本
"""

import sys
import sqlite3
import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from scripts.data_review_statutes import L1_STATUTES, L2_STATUTES
from scripts.data_review_cases import L1_CASES, L2_CASES
from scripts.data_review_edges import L1_EDGES, L2_EDGES

DB_PATH = Path("data/snapshots/20261021-asean-v2.2/law.sqlite")

def main():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    print("=== 1. 入库 L1 核心成文法簇 ===")
    for n in L1_STATUTES:
        c.execute("""
            INSERT OR REPLACE INTO norms (
                norm_id, law, enbez, title, heading_path,
                text_de, text_original, text_en, text_zh, source_url,
                snapshot_id, elements_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, '20261021-asean-v2.2', ?)
        """, (
            n["norm_id"], n["law"], n["enbez"], n["title"], n["heading_path"],
            n["text_zh"][:1500], n["text_original"], n["text_en"], n["text_zh"],
            n["source_url"], n["elements_json"]
        ))
        chunk_id = f"CHUNK:NORM:{n['norm_id']}:0"
        ctx_prefix = f"{n['law']} {n['enbez']} {n['title']} | {n['heading_path']}".strip()
        chunk_text = f"{ctx_prefix}\n{n['text_zh']}\n{n['text_en']}\n{n['text_original']}".strip()
        c.execute("""
            INSERT OR REPLACE INTO chunks (chunk_id, kind, ref_id, seq, text, ctx_prefix)
            VALUES (?, 'norm', ?, 0, ?, ?)
        """, (chunk_id, n["norm_id"], chunk_text, ctx_prefix))
        print(f"  + L1 Norm: {n['norm_id']}")

    print("\n=== 2. 入库 L2 广覆盖参考规程 ===")
    for n in L2_STATUTES:
        c.execute("""
            INSERT OR REPLACE INTO reference_norms (
                norm_id, law, enbez, title, heading_path,
                text_de, text_original, text_en, text_zh, source_url,
                snapshot_id, elements_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, '20261021-asean-v2.2', ?)
        """, (
            n["norm_id"], n["law"], n["enbez"], n["title"], n["heading_path"],
            n["text_zh"][:1500], n["text_original"], n["text_en"], n["text_zh"],
            n["source_url"], n["elements_json"]
        ))
        chunk_id = f"CHUNK:REF_NORM:{n['norm_id']}:0"
        ctx_prefix = f"{n['law']} {n['enbez']} {n['title']} | {n['heading_path']}".strip()
        chunk_text = f"{ctx_prefix}\n{n['text_zh']}\n{n['text_en']}".strip()
        c.execute("""
            INSERT OR REPLACE INTO reference_chunks (chunk_id, kind, ref_id, seq, text)
            VALUES (?, 'norm', ?, 0, ?)
        """, (chunk_id, n["norm_id"], chunk_text))
        print(f"  + L2 Norm: {n['norm_id']}")

    print("\n=== 3. 入库 L1 权威真实判例 (德式四要素金标准) ===")
    for cs in L1_CASES:
        c.execute("""
            INSERT OR REPLACE INTO cases (
                case_id, court, senate, decided, az, ecli, doctype,
                leitsatz, tenor, tatbestand, gruende, source_url, snapshot_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, '20261021-asean-v2.2')
        """, (
            cs["case_id"], cs["court"], cs["senate"], cs["decided"], cs["az"], cs["ecli"], cs["doctype"],
            cs["leitsatz"], cs["tenor"], cs["tatbestand"], cs["gruende"], cs["source_url"]
        ))
        cid_clean = cs["case_id"][5:] if cs["case_id"].startswith("CASE:") else cs["case_id"]
        chunk_id = f"CHUNK:CASE:{cid_clean}:0"
        ctx_prefix = f"{cs['court']} {cs['az']} ({cs['decided']}) {cs['doctype']}".strip()
        chunk_text = f"[{cs['case_id']}] | {cs['leitsatz']} | {cs['tenor']} | {cs['tatbestand']} | {cs['gruende']}"
        c.execute("""
            INSERT OR REPLACE INTO chunks (chunk_id, kind, ref_id, seq, text, ctx_prefix)
            VALUES (?, 'case', ?, 0, ?, ?)
        """, (chunk_id, cs["case_id"], chunk_text, ctx_prefix))
        print(f"  + L1 Case: {cs['case_id']} (Leitsatz={len(cs['leitsatz'])}, Gruende={len(cs['gruende'])})")

    print("\n=== 4. 入库 L2 真实公开撤裁与权威投资仲裁 ===")
    for cs in L2_CASES:
        c.execute("""
            INSERT OR REPLACE INTO reference_cases (
                case_id, court, senate, decided, az, ecli, doctype,
                leitsatz, tenor, tatbestand, gruende, source_url, snapshot_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, '20261021-asean-v2.2')
        """, (
            cs["case_id"], cs["court"], cs["senate"], cs["decided"], cs["az"], cs["ecli"], cs["doctype"],
            cs["leitsatz"], cs["tenor"], cs["tatbestand"], cs["gruende"], cs["source_url"]
        ))
        cid_clean = cs["case_id"][9:] if cs["case_id"].startswith("REF_CASE:") else cs["case_id"]
        chunk_id = f"CHUNK:REF_CASE:{cid_clean}:0"
        ctx_prefix = f"{cs['court']} {cs['az']} ({cs['decided']}) {cs['doctype']}".strip()
        chunk_text = f"[{cs['case_id']}] | {cs['leitsatz']} | {cs['tenor']} | {cs['tatbestand']} | {cs['gruende']}"
        c.execute("""
            INSERT OR REPLACE INTO reference_chunks (chunk_id, kind, ref_id, seq, text)
            VALUES (?, 'case', ?, 0, ?)
        """, (chunk_id, cs["case_id"], chunk_text))
        print(f"  + L2 Case: {cs['case_id']} (Leitsatz={len(cs['leitsatz'])}, Gruende={len(cs['gruende'])})")

    print("\n=== 5. 脱水提纯：重定向并清理同案冗余分身 ===")
    duplicate_mappings = [
        # 目标规范主ID -> 冗余分身列表
        ("CASE:MY_FC:Cubic_Electronics_2019", [
            "CASE:MY_FC:CubicElectronics:2019",
            "CASE:MY_FC:Cubic_Electronics_Sec75:2019",
            "CASE:MY_FC:Cubic_Electronics_v_Mars:2019",
            "CASE:MY_FC:Cubic_Electronics_v_Mars_2019"
        ]),
        ("CASE:SG_CA:Denka_Advantech_2020", [
            "CASE:SG_CA:Denka_Advantech_v_Seraya:2020"
        ]),
        ("CASE:TH_SAC:Hopewell_Concession_2022", [
            "CASE:TH_SAC:HopewellConcession:2022",
            "CASE:TH_SAC:No_102_2562_Hopewell_Arbitration:2019"
        ]),
        ("CASE:PH_SC:CE_Construction_v_Araneta_2017", [
            "CASE:PH_SC:CE_Construction_v_Araneta_Center:2017",
            "CASE:PH_SC:G.R.192725_CE_Construction:2017"
        ]),
        ("REF_CASE:ICSID:Churchill_Mining_v_Indonesia:2016", [
            "REF_CASE:ICSID:ARB_12_14_Churchill_Mining_Annulment:2019",
            "REF_CASE:ICSID:ARB_12_14_Churchill_Mining_Award:2016"
        ]),
        ("REF_CASE:ICSID:Fraport_v_Philippines:2014", [
            "REF_CASE:ICSID:ARB_03_25_Fraport_v_Philippines:2014",
            "REF_CASE:ICSID:Fraport_v_Philippines_PIATCO_Airport:2014"
        ]),
        ("REF_CASE:PCA:Walter_Bau_v_Thailand:2009", [
            "REF_CASE:PCA:Case_2008_13_Walter_Bau_v_Thailand:2009",
            "REF_CASE:UNCITRAL:Walter_Bau_v_Thailand_Tollway:2009"
        ])
    ]

    for canonical_id, redundant_ids in duplicate_mappings:
        is_l1 = canonical_id.startswith("CASE:")
        edge_tbl = "edges" if is_l1 else "reference_edges"
        case_tbl = "cases" if is_l1 else "reference_cases"
        chunk_tbl = "chunks" if is_l1 else "reference_chunks"

        for red_id in redundant_ids:
            # 重定向边关系至规范主 ID
            c.execute(f"UPDATE {edge_tbl} SET src = ? WHERE src = ?", (canonical_id, red_id))
            c.execute(f"UPDATE {edge_tbl} SET dst = ? WHERE dst = ?", (canonical_id, red_id))
            # 删除冗余 cases 与 chunks
            c.execute(f"DELETE FROM {case_tbl} WHERE case_id = ?", (red_id,))
            c.execute(f"DELETE FROM {chunk_tbl} WHERE ref_id = ?", (red_id,))
            print(f"  Merged clone: {red_id} -> {canonical_id}")

    # 删除自环边（src == dst）及完全重复边
    c.execute("DELETE FROM edges WHERE src = dst")
    c.execute("DELETE FROM reference_edges WHERE src = dst")

    print("\n=== 6. 拓扑因果关系边入库 ===")
    # 获取有效 L1/L2 实体集合，防止任何悬空边
    valid_l1_norms = set(r[0] for r in c.execute("SELECT norm_id FROM norms").fetchall())
    valid_l1_cases = set(r[0] for r in c.execute("SELECT case_id FROM cases").fetchall())
    valid_l1 = valid_l1_norms | valid_l1_cases

    valid_l2_norms = set(r[0] for r in c.execute("SELECT norm_id FROM reference_norms").fetchall())
    valid_l2_cases = set(r[0] for r in c.execute("SELECT case_id FROM reference_cases").fetchall())
    valid_l2 = valid_l2_norms | valid_l2_cases

    for src, rel, dst in L1_EDGES:
        if src in valid_l1 and dst in valid_l1:
            c.execute("INSERT OR IGNORE INTO edges (src, rel, dst) VALUES (?, ?, ?)", (src, rel, dst))
            print(f"  + L1 Edge: {src} --[{rel}]--> {dst}")
        else:
            print(f"  ! Skip invalid L1 Edge: {src} -> {dst}")

    for src, rel, dst in L2_EDGES:
        if src in valid_l2 and dst in valid_l2:
            c.execute("INSERT OR IGNORE INTO reference_edges (src, rel, dst) VALUES (?, ?, ?)", (src, rel, dst))
            print(f"  + L2 Edge: {src} --[{rel}]--> {dst}")
        else:
            print(f"  ! Skip invalid L2 Edge: {src} -> {dst}")

    print("\n=== 7. 规范化 chunks 表 chunk_id (消除 CHUNK:CASE:CASE: 双重前缀) ===")
    c.execute("SELECT rowid, chunk_id, ref_id FROM chunks WHERE chunk_id LIKE 'CHUNK:CASE:CASE:%'")
    double_prefix_chunks = c.fetchall()
    for rowid, chunk_id, ref_id in double_prefix_chunks:
        # e.g. CHUNK:CASE:CASE:SG_HC:BSMountSophia:2016:0 -> CHUNK:CASE:SG_HC:BSMountSophia:2016:0
        clean_cid = chunk_id.replace("CHUNK:CASE:CASE:", "CHUNK:CASE:")
        c.execute("UPDATE chunks SET chunk_id = ? WHERE rowid = ?", (clean_cid, rowid))
    print(f"  Normalized {len(double_prefix_chunks)} double-prefixed chunks.")

    print("\n=== 8. 刷新物化加速表 edges_top 与 hot_norm_cases ===")
    c.execute("DELETE FROM edges_top")
    c.execute("""
        INSERT INTO edges_top (src, rel, dst, source, reviewed, rk)
        SELECT src, rel, dst, 'L1', 1, ROW_NUMBER() OVER (PARTITION BY src ORDER BY rowid)
        FROM edges
    """)

    c.execute("DELETE FROM hot_norm_cases")
    # 确保 norm_id 严格为法条，case_id 严格为判例，避免判例被写入 norm_id
    c.execute("""
        INSERT INTO hot_norm_cases (norm_id, case_id, rank)
        SELECT src, dst, ROW_NUMBER() OVER (PARTITION BY src ORDER BY min(rowid))
        FROM edges
        WHERE rel IN ('interprets', 'applies', 'applied_in', 'correlates_with', 'overrides', 'overrules')
          AND dst LIKE 'CASE:%'
          AND src NOT LIKE 'CASE:%'
        GROUP BY src, dst
    """)

    # 双向补充：当 edge 记录为 CASE interprets NORM 或 CASE applied_in NORM 时，亦可映射为 NORM -> CASE
    c.execute("""
        INSERT OR IGNORE INTO hot_norm_cases (norm_id, case_id, rank)
        SELECT dst, src, 10 + ROW_NUMBER() OVER (PARTITION BY dst ORDER BY min(rowid))
        FROM edges
        WHERE rel IN ('interprets', 'applies', 'applied_in', 'correlates_with')
          AND src LIKE 'CASE:%'
          AND dst NOT LIKE 'CASE:%'
        GROUP BY dst, src
    """)

    conn.commit()
    conn.close()
    print("\n全量入库、去重提纯与物化表刷新完毕！")

if __name__ == '__main__':
    main()
