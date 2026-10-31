import sqlite3

conn = sqlite3.connect('data/snapshots/20261021-asean-v2.2/law.sqlite')
cur = conn.cursor()

print("--- Current DTA norms ---")
for r in cur.execute("SELECT norm_id FROM reference_norms WHERE norm_id LIKE 'DTA:%'").fetchall():
    print(r[0])

print("\n--- Current BIT norms ---")
for r in cur.execute("SELECT norm_id FROM reference_norms WHERE norm_id LIKE '%BIT%' UNION SELECT norm_id FROM norms WHERE norm_id LIKE '%BIT%'").fetchall():
    print(r[0])

print("\n--- Current PRC outbound norms ---")
for r in cur.execute("SELECT norm_id FROM norms WHERE norm_id LIKE 'CN:%' OR norm_id LIKE 'SINOSURE:%'").fetchall():
    print(r[0])

print("\n--- Current FIDIC clauses ---")
for r in cur.execute("SELECT norm_id FROM reference_norms WHERE norm_id LIKE 'FIDIC:%' UNION SELECT norm_id FROM norms WHERE norm_id LIKE 'FIDIC:%'").fetchall():
    print(r[0])

conn.close()
