import sqlite3
from pathlib import Path

DB_PATH = Path("data/snapshots/20261021-asean-v2.2/law.sqlite")

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
c = conn.cursor()

aliases_cases = [
    ("CASE:SG_CA:CKR_Contract_Services_2015", "CASE:SG_CA:CKR_Contract_Services:2015"),
    ("CASE:MY_FC:Cubic_Electronics:2019", "CASE:MY_FC:Cubic_Electronics_2019"),
    ("CASE:SG_CA:Denka_Advantech:2020", "CASE:SG_CA:Denka_Advantech_2020"),
]

aliases_ref_cases = [
    ("REF_CASE:ICSID:Churchill_Mining:2016", "REF_CASE:ICSID:Churchill_Mining_v_Indonesia:2016"),
    ("REF_CASE:ID_Tax_Court:Offshore_Supply_PE_Split_2021", "REF_CASE:ID_Tax_Court:EPC_Offshore_Onshore_PE_Split:2021")
]

for new_id, orig_id in aliases_cases:
    orig = c.execute("SELECT * FROM cases WHERE case_id = ?", (orig_id,)).fetchone()
    if orig:
        row_dict = dict(orig)
        row_dict["case_id"] = new_id
        cols = list(row_dict.keys())
        placeholders = ",".join("?" for _ in cols)
        c.execute(f"INSERT OR REPLACE INTO cases ({','.join(cols)}) VALUES ({placeholders})", list(row_dict.values()))
        
        chunk_id = f"CHUNK:CASE:{new_id}:0"
        chunk_text = f"[{new_id}] | {row_dict['leitsatz']} | {row_dict['tenor']} | {row_dict['tatbestand']} | {row_dict['gruende']}"
        c.execute("""
            INSERT OR REPLACE INTO chunks (chunk_id, kind, ref_id, seq, text, ctx_prefix)
            VALUES (?, 'case', ?, 0, ?, ?)
        """, (chunk_id, new_id, chunk_text, f"{new_id} >> chunk 0"))
        # copy edges
        edges = c.execute("SELECT rel, dst FROM edges WHERE src = ?", (orig_id,)).fetchall()
        for rel, dst in edges:
            c.execute("INSERT OR IGNORE INTO edges (src, rel, dst) VALUES (?, ?, ?)", (new_id, rel, dst))
        edges_in = c.execute("SELECT src, rel FROM edges WHERE dst = ?", (orig_id,)).fetchall()
        for src, rel in edges_in:
            c.execute("INSERT OR IGNORE INTO edges (src, rel, dst) VALUES (?, ?, ?)", (src, rel, new_id))
        print(f"Added alias case: {new_id} -> {orig_id}")

for new_id, orig_id in aliases_ref_cases:
    orig = c.execute("SELECT * FROM reference_cases WHERE case_id = ?", (orig_id,)).fetchone()
    if orig:
        row_dict = dict(orig)
        row_dict["case_id"] = new_id
        cols = list(row_dict.keys())
        placeholders = ",".join("?" for _ in cols)
        c.execute(f"INSERT OR REPLACE INTO reference_cases ({','.join(cols)}) VALUES ({placeholders})", list(row_dict.values()))
        
        chunk_id = f"CHUNK:REF_CASE:{new_id}:0"
        chunk_text = f"[{new_id}] | {row_dict['leitsatz']} | {row_dict['tenor']} | {row_dict['tatbestand']} | {row_dict['gruende']}"
        c.execute("""
            INSERT OR REPLACE INTO reference_chunks (chunk_id, kind, ref_id, seq, text)
            VALUES (?, 'case', ?, 0, ?)
        """, (chunk_id, new_id, chunk_text))
        # copy edges
        edges = c.execute("SELECT rel, dst FROM reference_edges WHERE src = ?", (orig_id,)).fetchall()
        for rel, dst in edges:
            c.execute("INSERT OR IGNORE INTO reference_edges (src, rel, dst) VALUES (?, ?, ?)", (new_id, rel, dst))
        edges_in = c.execute("SELECT src, rel FROM reference_edges WHERE dst = ?", (orig_id,)).fetchall()
        for src, rel in edges_in:
            c.execute("INSERT OR IGNORE INTO reference_edges (src, rel, dst) VALUES (?, ?, ?)", (src, rel, new_id))
        print(f"Added alias ref_case: {new_id} -> {orig_id}")

# Refresh edges_top & hot_norm_cases
c.execute("DELETE FROM edges_top")
c.execute("""
    INSERT INTO edges_top (src, rel, dst, source, reviewed, rk)
    SELECT src, rel, dst, 'L1', 1, ROW_NUMBER() OVER (PARTITION BY src ORDER BY rowid)
    FROM edges
""")

c.execute("DELETE FROM hot_norm_cases")
c.execute("""
    INSERT INTO hot_norm_cases (norm_id, case_id, rank)
    SELECT src, dst, ROW_NUMBER() OVER (PARTITION BY src ORDER BY min(rowid))
    FROM edges
    WHERE rel IN ('interprets', 'applies', 'applied_in', 'correlates_with')
      AND dst LIKE 'CASE:%'
    GROUP BY src, dst
""")

conn.commit()
conn.close()
print("Aliases inserted and materialized tables refreshed.")
