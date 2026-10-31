import sqlite3
import json

conn = sqlite3.connect('data/snapshots/20261021-asean-v2.2/law.sqlite')
cur = conn.cursor()

# 1. 基础体量
norms_l1 = cur.execute('SELECT count(*) FROM norms').fetchone()[0]
norms_l2 = cur.execute('SELECT count(*) FROM reference_norms').fetchone()[0]
cases_l1 = cur.execute('SELECT count(*) FROM cases').fetchone()[0]
cases_l2 = cur.execute('SELECT count(*) FROM reference_cases').fetchone()[0]
chunks_l1 = cur.execute('SELECT count(*) FROM chunks').fetchone()[0]
chunks_l2 = cur.execute('SELECT count(*) FROM reference_chunks').fetchone()[0]
edges_l1 = cur.execute('SELECT count(*) FROM edges').fetchone()[0]
edges_l2 = cur.execute('SELECT count(*) FROM reference_edges').fetchone()[0]

# 2. 重复检查 (L1 norms vs L2 reference_norms)
overlap_norms = cur.execute('SELECT norm_id FROM norms WHERE norm_id IN (SELECT norm_id FROM reference_norms)').fetchall()

# 3. elements_json 检查 (L1 norms)
empty_elements = cur.execute("SELECT count(*) FROM norms WHERE elements_json IS NULL OR elements_json = '' OR elements_json = '[]'").fetchone()[0]

# 4. 拓扑悬空边
all_nodes = (
    set(r[0] for r in cur.execute('SELECT norm_id FROM norms').fetchall()) |
    set(r[0] for r in cur.execute('SELECT case_id FROM cases').fetchall()) |
    set(r[0] for r in cur.execute('SELECT norm_id FROM reference_norms').fetchall()) |
    set(r[0] for r in cur.execute('SELECT case_id FROM reference_cases').fetchall())
)
dangling_edges = [r for r in cur.execute('SELECT src, dst FROM edges').fetchall() if r[0] not in all_nodes or r[1] not in all_nodes]
dangling_ref_edges = [r for r in cur.execute('SELECT src, dst FROM reference_edges').fetchall() if r[0] not in all_nodes or r[1] not in all_nodes]

# 5. 判例字数
short_cases = []
for tbl in ['cases', 'reference_cases']:
    rows = cur.execute(f"SELECT case_id FROM {tbl} WHERE length(leitsatz) < 150 OR length(tenor) < 150 OR length(tatbestand) < 200 OR length(gruende) < 350").fetchall()
    short_cases.extend(rows)

print("=== 数据库全景终审核查数据 ===")
print(f"L1 核心强行法条 (norms): {norms_l1}")
print(f"L2 参考规程条约 (reference_norms): {norms_l2}")
print(f"全库总法条数: {norms_l1 + norms_l2}")
print(f"L1 标杆判例 (cases): {cases_l1}")
print(f"L2 参考判例 (reference_cases): {cases_l2}")
print(f"全库裁判文书总数: {cases_l1 + cases_l2}")
print(f"L1 语义分块 (chunks): {chunks_l1}")
print(f"L2 语义分块 (reference_chunks): {chunks_l2}")
print(f"L1 拓扑边数 (edges): {edges_l1}")
print(f"L2 拓扑边数 (reference_edges): {edges_l2}")
print(f"L1/L2 重复法条数: {len(overlap_norms)}")
print(f"L1 elements_json 空壳数: {empty_elements}")
print(f"edges 拓扑悬空边数: {len(dangling_edges)}")
print(f"reference_edges 拓扑悬空边数: {len(dangling_ref_edges)}")
print(f"低于金标准案例数: {len(short_cases)}")
conn.close()
