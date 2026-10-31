import sqlite3
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

db_path = 'data/snapshots/20261021-asean-v2.2/law.sqlite'
conn = sqlite3.connect(db_path)
c = conn.cursor()

print("--- 1. 重复 norm_id (L1 vs L2) ---")
c.execute('SELECT norm_id FROM norms')
l1_norms = set(r[0] for r in c.fetchall())
c.execute('SELECT norm_id FROM reference_norms')
l2_norms = set(r[0] for r in c.fetchall())
common_norms = l1_norms.intersection(l2_norms)
print(f"L1 total: {len(l1_norms)}, L2 total: {len(l2_norms)}")
print(f"Common norms ({len(common_norms)}):", sorted(list(common_norms)))

print("\n--- 2. edges 重复与前缀 ---")
c.execute('SELECT src, dst, rel, count(*) FROM edges GROUP BY src, dst, rel HAVING count(*) > 1')
dup_edges = c.fetchall()
print(f"Duplicate edges groups: {len(dup_edges)}")
for d in dup_edges[:5]:
    print(d)

c.execute("SELECT count(*) FROM edges WHERE src LIKE 'NORM:%' OR dst LIKE 'NORM:%' OR src LIKE 'CASE:%' OR dst LIKE 'CASE:%'")
prefix_edges = c.fetchone()[0]
print(f"Edges with NORM: or CASE: prefix: {prefix_edges} / 125")
c.execute("SELECT src, dst, rel FROM edges WHERE src LIKE 'NORM:%' OR dst LIKE 'NORM:%' OR src LIKE 'CASE:%' OR dst LIKE 'CASE:%' LIMIT 5")
for r in c.fetchall():
    print(r)

print("\n--- 3. L1 cases 表中的 REF_CASE: 及重复案例 ---")
c.execute("SELECT case_id, court, az FROM cases WHERE case_id LIKE 'REF_CASE:%'")
ref_cases_in_l1 = c.fetchall()
print(f"REF_CASE in L1 cases ({len(ref_cases_in_l1)}):")
for r in ref_cases_in_l1:
    print(r[0], "|", r[1], "|", r[2])

c.execute("SELECT case_id, court, az FROM cases WHERE az LIKE '%[2015] SGCA 30%'")
print("Cases with [2015] SGCA 30:", c.fetchall())

print("\n--- 4. L2 reference_edges 拓扑断链 ---")
c.execute('SELECT case_id FROM reference_cases')
l2_cases = set(r[0] for r in c.fetchall())
c.execute('SELECT src, dst, rel FROM reference_edges')
ref_edges = c.fetchall()
print(f"reference_edges total: {len(ref_edges)}")
for src, dst, rel in ref_edges:
    src_in_l2 = (src in l2_norms) or (src in l2_cases)
    dst_in_l2 = (dst in l2_norms) or (dst in l2_cases)
    if not src_in_l2 or not dst_in_l2:
        src_in_l1 = (src in l1_norms) or (src in [r[0] for r in c.execute('SELECT case_id FROM cases').fetchall()])
        dst_in_l1 = (dst in l1_norms) or (dst in [r[0] for r in c.execute('SELECT case_id FROM cases').fetchall()])
        print(f"Broken in L2: {src} -> {dst} ({rel}) | src: L2={src_in_l2}, L1={src_in_l1} | dst: L2={dst_in_l2}, L1={dst_in_l1}")

print("\n--- 7. L1 elements_json 填充情况 ---")
c.execute("SELECT count(*) FROM norms WHERE elements_json IS NULL OR elements_json = '' OR elements_json = '[]'")
empty_elems = c.fetchone()[0]
print(f"L1 norms with empty elements_json: {empty_elems} / {len(l1_norms)}")

conn.close()

print("\n--- 8. kb/asean 静态文件状态 ---")
for f in ["data/kb/asean/commentary.json", "data/kb/asean/timepoints.yaml", "data/kb/asean/glossary.csv"]:
    if os.path.exists(f):
        with open(f, "r", encoding="utf-8") as fp:
            lines = len(fp.readlines())
        print(f"{f}: {lines} lines, {os.path.getsize(f)} bytes")
    else:
        print(f"{f}: NOT FOUND")

