import sqlite3

conn = sqlite3.connect('data/snapshots/20261021-asean-v2.2/law.sqlite')
cur = conn.cursor()

print("=== L1 norms by jurisdiction prefix ===")
for r in cur.execute("SELECT substr(norm_id, 1, instr(norm_id, ':') - 1) as jur, count(*) FROM norms GROUP BY jur ORDER BY count(*) DESC").fetchall():
    print(f"  {r[0]}: {r[1]}")

print("\n=== L2 reference_norms by prefix ===")
for r in cur.execute("SELECT substr(norm_id, 1, instr(norm_id, ':') - 1) as jur, count(*) FROM reference_norms GROUP BY jur ORDER BY count(*) DESC").fetchall():
    print(f"  {r[0]}: {r[1]}")

print("\n=== Cases breakdown ===")
for tbl in ['cases', 'reference_cases']:
    print(f"-- {tbl} --")
    rows = cur.execute(f"SELECT case_id FROM {tbl}").fetchall()
    counts = {}
    for (cid,) in rows:
        prefix = cid.split(':')[1] if ':' in cid else 'other'
        country = prefix.split('_')[0]
        counts[country] = counts.get(country, 0) + 1
    for k, v in sorted(counts.items(), key=lambda x: -x[1]):
        print(f"  {k}: {v}")

conn.close()
