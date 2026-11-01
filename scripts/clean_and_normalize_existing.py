import sqlite3
import os

DB_PATH = "data/snapshots/20261021-asean-v2.2/law.sqlite"

def clean_database():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    print("1. Deduplicating edges...")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS edges_temp AS
        SELECT src, dst, rel, min(source) as source, min(span) as span, max(confidence) as confidence, max(reviewed) as reviewed, min(snapshot_id) as snapshot_id
        FROM edges
        GROUP BY src, dst, rel;
    """)
    cur.execute("DELETE FROM edges;")
    cur.execute("INSERT INTO edges SELECT * FROM edges_temp;")
    cur.execute("DROP TABLE edges_temp;")

    print("2. Deduplicating reference_edges...")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS ref_edges_temp AS
        SELECT min(edge_id) as edge_id, src, dst, rel, min(description) as description
        FROM reference_edges
        GROUP BY src, dst, rel;
    """)
    cur.execute("DELETE FROM reference_edges;")
    cur.execute("INSERT INTO reference_edges SELECT * FROM ref_edges_temp;")
    cur.execute("DROP TABLE ref_edges_temp;")

    print("3. Updating Vietnamese speculative laws to authentic enacted statutes...")
    # VN:Law_135_2025:Art86.2 -> VN:Construction_Law_2014_Amended_2020:Art146
    # VN:Law_135_2025:Art146 -> VN:Construction_Law_2014_Amended_2020:Art138
    # VN:Decree_210_2026:Art18 -> VN:Decree_37_2015_ND_CP:Art18
    # VN:Construction_Law_2025:Art148 -> VN:Construction_Law_2014_Amended_2020:Art148
    vn_updates = [
        ("VN:Law_135_2025:Art86.2", "VN:Construction_Law_2014_Amended_2020:Art146", "越南建设法第146条（工程合同违约与赔偿，原预演编号映射）"),
        ("VN:Law_135_2025:Art146", "VN:Construction_Law_2014_Amended_2020:Art138", "越南建设法第138条（建设工程合同总则与强制性条款）"),
        ("VN:Decree_210_2026:Art18", "VN:Decree_37_2015_ND_CP:Art18", "越南第37/2015/ND-CP号法令第18条（经第50/2021修订，预付款担保与扣回）"),
        ("VN:Construction_Law_2025:Art148", "VN:Construction_Law_2014_Amended_2020:Art148", "越南建设法第148条（建设工程承包商资质等级与外资承包许可）"),
    ]
    for old_id, new_id, new_title in vn_updates:
        cur.execute("UPDATE norms SET norm_id = ?, title = ? WHERE norm_id = ?", (new_id, new_title, old_id))
        cur.execute("UPDATE edges SET src = ? WHERE src = ?", (new_id, old_id))
        cur.execute("UPDATE edges SET dst = ? WHERE dst = ?", (new_id, old_id))
        cur.execute("UPDATE hot_norm_cases SET norm_id = ? WHERE norm_id = ?", (new_id, old_id))

    print("4. Cleaning boilerplate text in cases...")
    boilerplate_leitsatz = "本案裁决确立了具有约束力的司法裁判准则，对涉外工程合同违约救济、抗辩事由认定及跨境争议解决具有重要的先例指导价值。"
    cur.execute("SELECT case_id, leitsatz FROM cases WHERE leitsatz LIKE ?", (f"%{boilerplate_leitsatz}%",))
    for cid, ls in cur.fetchall():
        cleaned_ls = ls.replace(boilerplate_leitsatz, "").strip().strip("。") + "。"
        cur.execute("UPDATE cases SET leitsatz = ? WHERE case_id = ?", (cleaned_ls, cid))

    cur.execute("SELECT case_id, leitsatz FROM reference_cases WHERE leitsatz LIKE ?", (f"%{boilerplate_leitsatz}%",))
    for cid, ls in cur.fetchall():
        cleaned_ls = ls.replace(boilerplate_leitsatz, "").strip().strip("。") + "。"
        cur.execute("UPDATE reference_cases SET leitsatz = ? WHERE case_id = ?", (cleaned_ls, cid))

    print("5. Merging duplicate case IDs...")
    case_merges = [
        # (remove_id, keep_id)
        ("CASE:ID_MA:Waive1266_Termination:2018", "CASE:ID_MA:Putusan_MA_1582_K_Pdt_2018:2019"),
        ("CASE:ID_MA:Nominee_Shareholding_Void_UU25_Art33:2019", "CASE:ID_MA:Putusan_MA_3020_K_Pdt_2018_Nominee:2019"),
        ("CASE:PH_SC:G.R.217590_ManilaWater:2020", "CASE:PH_SC:PCAB_v_Manila_Water_2020"),
        ("CASE:SG_HC:BSMountSophia:2016", "CASE:SG_CA:BS_Mount_Sophia:2012"),
    ]
    for remove_id, keep_id in case_merges:
        # Check if both exist
        cur.execute("SELECT count(*) FROM cases WHERE case_id = ?", (remove_id,))
        if cur.fetchone()[0] > 0:
            # Avoid UNIQUE constraint collision in edges
            cur.execute("""
                DELETE FROM edges
                WHERE src = ? AND dst IN (SELECT dst FROM edges WHERE src = ?)
            """, (remove_id, keep_id))
            cur.execute("UPDATE edges SET src = ? WHERE src = ?", (keep_id, remove_id))
            cur.execute("UPDATE edges SET dst = ? WHERE dst = ?", (keep_id, remove_id))

            # Avoid UNIQUE constraint collision in hot_norm_cases
            cur.execute("""
                DELETE FROM hot_norm_cases
                WHERE case_id = ? AND norm_id IN (SELECT norm_id FROM hot_norm_cases WHERE case_id = ?)
            """, (remove_id, keep_id))
            cur.execute("UPDATE hot_norm_cases SET case_id = ? WHERE case_id = ?", (keep_id, remove_id))
            cur.execute("DELETE FROM cases WHERE case_id = ?", (remove_id,))

    conn.commit()
    conn.close()
    print("Clean and normalization complete.")

if __name__ == "__main__":
    clean_database()
