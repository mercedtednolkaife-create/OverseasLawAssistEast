import sqlite3
from collections import defaultdict

conn = sqlite3.connect('data/snapshots/20261021-asean-v2.2/law.sqlite')
conn.row_factory = sqlite3.Row

print("=== Check Duplicate Norms in L1 ===")
l1_norms = conn.execute("SELECT norm_id, law, enbez, title FROM norms").fetchall()
seen_l1 = {}
dups_l1 = []
for n in l1_norms:
    key = (n["law"], n["enbez"])
    if key in seen_l1:
        dups_l1.append((seen_l1[key], n["norm_id"], n["title"]))
    else:
        seen_l1[key] = n["norm_id"]
print(f"L1 norm duplicates by (law, enbez): {len(dups_l1)}")
for d in dups_l1[:10]:
    print("  ", d)

print("\n=== Check Duplicate Cases in L1 ===")
l1_cases = conn.execute("SELECT case_id, court, az, decided FROM cases").fetchall()
seen_cases = {}
dups_cases = []
for c in l1_cases:
    clean_az = (c["az"] or "").replace(" ", "").upper()
    if clean_az and clean_az in seen_cases:
        dups_cases.append((seen_cases[clean_az], c["case_id"], c["court"], c["az"]))
    elif clean_az:
        seen_cases[clean_az] = c["case_id"]
print(f"L1 case duplicates by az: {len(dups_cases)}")
for d in dups_cases[:10]:
    print("  ", d)

print("\n=== Check Vietnamese speculative laws ===")
vn_spec = conn.execute("SELECT norm_id, title FROM norms WHERE norm_id LIKE '%135_2025%' OR norm_id LIKE '%210_2026%' OR norm_id LIKE '%2025%' OR norm_id LIKE '%2026%'").fetchall()
for r in vn_spec:
    print("  ", dict(r))
