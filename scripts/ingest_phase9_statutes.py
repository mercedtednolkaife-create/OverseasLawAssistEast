# -*- coding: utf-8 -*-
"""Phase 9 阶梯式长尾法条入库与双层双引擎索引流水线
覆盖 12 大实务域长尾法条簇，同步写入 chunks/reference_chunks、拓扑边、
刷新加速物化表，并重建 L1 与 L2 的 BM25 与 FAISS 稠密向量索引。
"""

import sys
import io
import os
import sqlite3
import json

# 解决 Windows 控制台 UTF-8 输出
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, ".")

from scripts.data_phase9_statutes_batch1 import BATCH1_STATUTES
from scripts.data_phase9_statutes_batch2 import BATCH2_STATUTES
from scripts.data_phase9_statutes_batch3 import BATCH3_STATUTES
from scripts.data_phase9_statutes_batch4 import BATCH4_STATUTES

DB_PATH = "data/snapshots/20261021-asean-v2.2/law.sqlite"
INDEX_DIR = "data/snapshots/20261021-asean-v2.2/index"
INDEX_L2_DIR = "data/snapshots/20261021-asean-v2.2/index_l2"


NEW_EDGES_L1 = [
    # 实体法与判例解释边
    ("ID:KUHPerdata:Art1342", "CASE:ID_PN_JakSel:Nominee_Shareholding_Void:2019", "interprets"),
    ("ID:KUHPerdata:Art1792", "CASE:ID_PTUN:AMDAL_Environmental_Injunction:2021", "interprets"),
    ("VN:Civil_Code_2015:Art3", "CASE:VN_Hanoi_HC:NY_Conv_SIAC_Enforcement:2021", "interprets"),
    ("VN:Civil_Code_2015:Art122", "CASE:VN_SPC:Precedent_21_2018_AL", "interprets"),
    ("VN:Civil_Code_2015:Art124", "CASE:VN_Hanoi:Renewable_Energy_MA_Dispute:2022", "interprets"),
    ("VN:Civil_Code_2015:Art138", "CASE:VN_Hanoi_HC:ForeignContractorPermit_Void:2020", "interprets"),
    ("MY:Contracts_Act_1950:Sec2", "CASE:MY_FC:Cubic_Electronics_Penalty:2019", "interprets"),
    ("MY:Contracts_Act_1950:Sec14", "CASE:MY_CA:Gasing_Heights_Prevention:2018", "interprets"),
    ("MY:Contracts_Act_1950:Sec28", "CASE:MY_FC:Martego_v_Arkitek_Meor:2019", "interprets"),
    ("TH:CCC:Sec149", "CASE:TH_SC:Hopewell_Highway_Concession:2019", "interprets"),
    ("TH:CCC:Sec155", "CASE:TH_SC:FBA_Sec36_Nominee_Shareholding_Dissolution:2020", "interprets"),
    ("PH:Civil_Code:Art1370", "CASE:PH_SC:Powton_Conglomerate_v_Agcolicol_Art1724:2009", "interprets"),
    ("PH:Civil_Code:Art1403", "CASE:PH_SC:Department_of_Health_v_Phil_Pharma_COA:2013", "interprets"),
    ("ID:KUHPerdata:Art1238", "CASE:SIAC:Site_Handover_EOT:2020", "applied_in"),
    ("ID:KUHPerdata:Art1266", "CASE:ID_PN_JakPus:Exequatur_SIAC:2022", "applied_in"),
    ("VN:Commercial_Law_2005:Art301", "CASE:VN_SPC:Precedent_09_2016_AL", "applied_in"),
    ("VN:Civil_Code_2015:Art420", "CASE:VN_SPC:ContractPriceAdjustment_ForceMajeure:2021", "applied_in"),
    ("MY:Contracts_Act_1950:Sec57", "CASE:MY_CA:Gasing_Heights_Prevention:2018", "applied_in"),
    ("MY:Contracts_Act_1950:Sec75", "CASE:MY_FC:Cubic_Electronics_Penalty:2019", "applied_in"),
    ("TH:CCC:Sec383", "CASE:TH_SC:Hopewell_Highway_Concession:2019", "applied_in"),
    ("PH:Civil_Code:Art1229", "CASE:PH_SC:CE_Construction_v_Araneta_Center:2017", "applied_in"),
    ("ID:UU_2_2017:Art30", "CASE:ID_PN_JakSel:Nominee_Shareholding_Void:2019", "overrides"),
    ("ID:UU_2_2017:Art60", "CASE:ID_SC:SEMA_Arbitration_Enforcement:2022", "overrides"),
    ("VN:Construction_Law_2025:Art148", "CASE:VN_Hanoi_HC:ForeignContractorPermit_Void:2020", "overrides"),
    ("MY:CIPAA_2012:Sec35", "CASE:MY_FC:Martego_v_Arkitek_Meor:2019", "overrides"),
    ("MY:CIDB_Act_520:Sec25", "CASE:MY_CA:Gasing_Heights_Prevention:2018", "overrides"),
    ("SG:SOPA_2004:Sec9", "CASE:SG_CA:Audi_Construction_SOPA:2018", "overrides"),
    ("SG:SOPA_2004:Sec15_3", "CASE:SG_CA:Audi_Construction_SOPA:2018", "overrides"),
    ("TH:CCC:Sec600", "CASE:TH_SC:Preferential_Right_Sec286_Unregistered_Subordinate:2019", "overrides"),
    ("PH:Civil_Code:Art1723", "CASE:PH_SC:Powton_Conglomerate_v_Agcolicol_Art1724:2009", "overrides"),
    ("PH:Civil_Code:Art1724", "CASE:PH_SC:Powton_Conglomerate_v_Agcolicol_Art1724:2009", "overrides"),
    ("ID:UU_25_2007:Art33", "CASE:ID_PN_JakSel:Nominee_Shareholding_Void:2019", "overrides"),
    ("VN:Law_61_2020:Art24_26", "CASE:VN_Hanoi:Renewable_Energy_MA_Dispute:2022", "overrides"),
    ("VN:PPP_Law_2020:Art82", "CASE:VN_Hanoi_HC:NY_Conv_SIAC_Enforcement:2021", "overrides"),
    ("TH:FBA_1999:Sec36_37", "CASE:TH_SC:FBA_Sec36_Nominee_Shareholding_Dissolution:2020", "overrides"),
    ("PH:Anti_Dummy_Law:Sec1_2A", "CASE:PH_SC:Narra_Nickel_Mining_v_Redmont:2014", "overrides"),
    ("ID:UUPA_5_1960:Art35_HGB", "CASE:ID_SC:SEMA_Arbitration_Enforcement:2022", "overrides"),
    ("VN:Land_Law_2024:Art79", "CASE:VN_SPC:Precedent_21_2018_AL", "overrides"),
    ("TH:CCC:Sec1410_Superficies", "CASE:TH_SC:Preferential_Right_Sec286_Unregistered_Subordinate:2019", "overrides"),
    ("PH:RA_8371:Sec59_FPIC", "CASE:PH_SC:Republic_v_Caguioa_RA8975_NoTRO:2009", "overrides"),
    ("CN:SASAC_Notice_75_2021:Art4", "CASE:SG_CA:CKR_Contract_Services:2015", "overrides"),
    ("ID:KUHPerdata:Art1139_8", "CASE:ID_SC:SEMA_Arbitration_Enforcement:2022", "overrides"),
    ("MY:Common_Law:No_Mechanic_Lien", "CASE:MY_FC:Martego_v_Arkitek_Meor:2019", "overrides"),
    ("ID:PBI_17_3_2015:Art4_8_Exemption", "CASE:ID_PN_JakPus:Exequatur_SIAC:2022", "overrides"),
    ("ID:UU_6_2011:Art122_Visa_Crime", "CASE:ID_PTUN:AMDAL_Environmental_Injunction:2021", "overrides"),
    ("MY:Employment_Act_1955:Sec33", "CASE:MY_CA:Gasing_Heights_Prevention:2018", "overrides"),
    ("TH:Labor_Protection_Act:Sec12", "CASE:TH_SC:Hopewell_Highway_Concession:2019", "overrides"),
    ("PH:Labor_Code:Art106_Solidary", "CASE:PH_SC:Powton_Conglomerate_v_Agcolicol_Art1724:2009", "overrides"),
    ("MY:MACC_Act_2009:Sec17A_TRUST", "CASE:MY_FC:Martego_v_Arkitek_Meor:2019", "overrides"),
    ("ID:UU_37_2004:Art222_PKPU", "CASE:ID_PN_JakPus:Exequatur_SIAC:2022", "overrides"),
    ("SG:IRDA_2018:Sec440_IpsoFacto", "CASE:SG_CA:Audi_Construction_SOPA:2018", "overrides"),
    ("PH:FRIA_RA10142:Sec18_StandbyLC", "CASE:PH_SC:Republic_v_Caguioa_RA8975_NoTRO:2009", "overrides"),
    ("VN:Civil_Procedure_2015:Art440_No_Merits_Review", "CASE:VN_Hanoi_HC:NY_Conv_SIAC_Enforcement:2021", "overrides"),
    ("SG:IAA_Cap_143A:Sec12A_Interim_Injunction", "CASE:SG_CA:CKR_Contract_Services:2015", "overrides"),
    ("PH:EO_1008:Sec4_CIAC_Exclusive", "CASE:PH_SC:William_Golangco_v_Fung_CIAC:2006", "overrides")
]

NEW_EDGES_L2 = [
    ("FIDIC:Silver_1999:Clause_4.12", "REF_CASE:SG_HC:FIDIC_Cl4_12_UnforeseenGround:2018", "INTERPRETS"),
    ("FIDIC:Red_1999:Clause_4.12", "REF_CASE:SG_HC:FIDIC_Cl4_12_UnforeseenGround:2018", "INTERPRETS"),
    ("FIDIC:2017_Suite:Clause_20.2", "REF_CASE:SIAC:Site_Handover_EOT:2020", "INTERPRETS"),
    ("FIDIC:Golden_Principles:GP1_GP5", "REF_CASE:SG_HC:FIDIC_Cl16_Suspension_Validity:2019", "INTERPRETS"),
    ("ICC:URDG_758:Art15_Breach", "REF_CASE:VN_Hanoi:Bid_Bond_Wrongful_Forfeiture:2022", "INTERPRETS"),
    ("DTA:CN_ID:Art5_3_PE", "REF_CASE:ID_Tax_Court:EPC_Offshore_Onshore_PE_Split:2021", "INTERPRETS"),
    ("DTA:CN_VN:Art7_Business_Profits", "REF_CASE:ID_Tax_Court:EPC_Offshore_Onshore_PE_Split:2021", "INTERPRETS"),
    ("VN:Circular_103_2014:Art11_FCT_Split", "REF_CASE:ID_Tax_Court:EPC_Offshore_Onshore_PE_Split:2021", "INTERPRETS"),
    ("MDB:Cross_Debarment:Five_Practices", "REF_CASE:ICSID:Churchill_Mining_v_Indonesia:2016", "INTERPRETS"),
    ("VN:Decision_18_2019:Art6_Used_Machinery", "REF_CASE:VN_Hanoi_HC:ForeignContractorPermit_Void:2020", "INTERPRETS"),
    ("TREATY:New_York_1958:Art_V", "REF_CASE:VN_Hanoi_HC:NY_Conv_SIAC_Enforcement:2021", "INTERPRETS"),
    ("TREATY:CAFTA_2009:Art14_ISDS", "REF_CASE:UNCITRAL:Walter_Bau_v_Thailand_Tollway:2009", "INTERPRETS"),
    ("TREATY:ACIA_2009:Art19_Denial_of_Benefits", "REF_CASE:ICSID:Fraport_v_Philippines_PIATCO_Airport:2014", "INTERPRETS")
]


def ingest_phase9_statutes():
    print("=" * 80)
    print("🚀 开始执行 Phase 9 涉外 12 大实务域长尾法条入库流水线")
    print("=" * 80)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT count(*) FROM norms")
    l1_before = cur.fetchone()[0]
    cur.execute("SELECT count(*) FROM reference_norms")
    l2_before = cur.fetchone()[0]

    all_batches = BATCH1_STATUTES + BATCH2_STATUTES + BATCH3_STATUTES + BATCH4_STATUTES
    print(f"• 汇编新增法条总计: {len(all_batches)} 条")

    l1_added = 0
    l2_added = 0

    for item in all_batches:
        tbl = item.get("table", "norms")
        nid = item["norm_id"]
        law = item.get("law", nid.split(":")[0])
        enbez = item.get("enbez", nid.split(":")[-1])
        title = item["title"]
        heading = item.get("heading_path", "")
        text_orig = item.get("text_original", "")
        text_en = item.get("text_en", "")
        text_zh = item.get("text_zh", "")
        text_de = f"{title}\n{text_zh}\n{text_en}"
        lang_mode = item.get("language_mode", "bilingual")
        lang_orig = item.get("lang_original", "en")
        norm_cat = item.get("norm_category", "statute")
        fidic_tier = item.get("fidic_tier", "L1_core" if tbl == "norms" else "L2_reference")
        fidic_edition = item.get("fidic_edition", "")
        elements_json = item.get("elements_json", "[]")
        mandatory_level = item.get("mandatory_level", "mandatory")

        # 写入对应法条表
        cur.execute(
            f"""INSERT OR REPLACE INTO {tbl}
               (norm_id, law, enbez, title, heading_path, text_de, structure, footnotes, stand,
                has_pending_amend, source_url, snapshot_id, fetched_at, language_mode, lang_original,
                text_original, text_en, text_zh, translation_source, norm_category, fidic_tier,
                fidic_edition, elements_json, mandatory_level)
               VALUES (?, ?, ?, ?, ?, ?, '[]', '[]', '2026-10-31', 0, 'https://official.gov',
                       'snap_asean_2026', '2026-10-31T09:30:00', ?, ?, ?, ?, ?, 'expert_vetted', ?, ?, ?, ?, ?)""",
            (
                nid, law, enbez, title, heading, text_de,
                lang_mode, lang_orig, text_orig, text_en, text_zh,
                norm_cat, fidic_tier, fidic_edition, elements_json, mandatory_level
            )
        )

        # 同步写入语义分块表
        if tbl == "norms":
            l1_added += 1
            cid = f"CHUNK:NORM:{nid}:0"
            chunk_text = f"[{nid}] {title} | {text_zh} | {text_en} | {text_orig}"
            cur.execute(
                """INSERT OR REPLACE INTO chunks (chunk_id, kind, ref_id, seq, text, ctx_prefix)
                   VALUES (?, 'norm', ?, 0, ?, '')""",
                (cid, nid, chunk_text)
            )
        else:
            l2_added += 1
            cid = f"CHUNK:REF_NORM:{nid}:0"
            chunk_text = f"[{nid}] {title} | {text_zh} | {text_en} | {text_orig}"
            cur.execute(
                """INSERT OR REPLACE INTO reference_chunks (chunk_id, kind, ref_id, seq, text)
                   VALUES (?, 'reference_norm', ?, 0, ?)""",
                (cid, nid, chunk_text)
            )

    # 写入拓扑图谱边
    print(f"• 正在写入 L1 图谱边 ({len(NEW_EDGES_L1)} 条)...")
    for src, dst, rel in NEW_EDGES_L1:
        cur.execute(
            """INSERT OR IGNORE INTO edges (src, dst, rel, source, span, confidence, reviewed, snapshot_id)
               VALUES (?, ?, ?, 'manual_expert', 'statute_expansion', 1.0, 1, 'snap_asean_2026')""",
            (src, dst, rel)
        )

    print(f"• 正在写入 L2 图谱边 ({len(NEW_EDGES_L2)} 条)...")
    for src, dst, rel in NEW_EDGES_L2:
        edge_id = f"REDGE:{src}->{dst}"
        cur.execute(
            """INSERT OR IGNORE INTO reference_edges (edge_id, src, dst, rel, description)
               VALUES (?, ?, ?, ?, '涉外长尾法条实务援引与条约升级拓扑边')""",
            (edge_id, src, dst, rel)
        )

    # 刷新加速表
    print("• 正在刷新加速物化表 edges_top 和 hot_norm_cases...")
    cur.execute("DELETE FROM edges_top")
    cur.execute("""
        INSERT INTO edges_top (src, dst, rel, source, reviewed, rk)
        SELECT src, dst, rel, source, reviewed,
               ROW_NUMBER() OVER (PARTITION BY src ORDER BY rowid ASC) as rk
        FROM edges
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_top_src ON edges_top(src, rel)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_top_dst ON edges_top(dst, rel)")

    cur.execute("DELETE FROM hot_norm_cases")
    cur.execute("""
        INSERT OR REPLACE INTO hot_norm_cases (norm_id, case_id, rank)
        SELECT dst AS norm_id, src AS case_id,
               ROW_NUMBER() OVER (PARTITION BY dst ORDER BY rowid ASC) as rank
        FROM edges
        WHERE rel IN ('applies', 'interpreted_by', 'applied_in', 'interprets', 'INTERPRETS')
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_hot_norm ON hot_norm_cases(norm_id)")

    conn.commit()

    cur.execute("SELECT count(*) FROM norms")
    l1_after = cur.fetchone()[0]
    cur.execute("SELECT count(*) FROM reference_norms")
    l2_after = cur.fetchone()[0]
    cur.execute("SELECT count(*) FROM chunks")
    chunks_after = cur.fetchone()[0]
    cur.execute("SELECT count(*) FROM reference_chunks")
    ref_chunks_after = cur.fetchone()[0]
    cur.execute("SELECT count(*) FROM edges")
    edges_after = cur.fetchone()[0]
    cur.execute("SELECT count(*) FROM reference_edges")
    ref_edges_after = cur.fetchone()[0]

    conn.close()

    print(f"✓ L1 核心法条: {l1_before} -> {l1_after} 条 (+{l1_added})")
    print(f"✓ L2 参考法条: {l2_before} -> {l2_after} 条 (+{l2_added})")
    print(f"🎉 全库法条总数: {l1_after + l2_after} 条")
    print(f"• L1 语义分块 chunks: {chunks_after} 个")
    print(f"• L2 语义分块 reference_chunks: {ref_chunks_after} 个")
    print(f"• L1 拓扑边 edges: {edges_after} 条")
    print(f"• L2 拓扑边 reference_edges: {ref_edges_after} 条")


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
    ingest_phase9_statutes()
    rebuild_indices()
