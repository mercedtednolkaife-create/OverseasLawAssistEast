import sqlite3

conn = sqlite3.connect('data/snapshots/20261021-asean-v2.2/law.sqlite')
c = conn.cursor()

c.execute('SELECT DISTINCT seq FROM chunks')
print('chunks seqs:', c.fetchall())

c.execute('SELECT DISTINCT seq FROM reference_chunks')
print('reference_chunks seqs:', c.fetchall())

c.execute('SELECT DISTINCT kind, count(*) FROM reference_chunks GROUP BY kind')
print('reference_chunks kind counts:', c.fetchall())

c.execute('SELECT count(*), count(distinct src || "|" || dst || "|" || rel) FROM edges')
print('edges count vs distinct:', c.fetchall())

c.execute('SELECT count(*), count(distinct src || "|" || dst || "|" || rel) FROM reference_edges')
print('reference_edges count vs distinct:', c.fetchall())

c.execute('SELECT count(*) FROM norm_versions')
print('norm_versions count:', c.fetchall())

c.execute("SELECT norm_id FROM norms WHERE norm_id LIKE '%2025%' OR norm_id LIKE '%2026%'")
print('future laws:', c.fetchall())

# Check island nodes
c.execute("""
SELECT count(*) FROM norms WHERE norm_id NOT IN (SELECT src FROM edges UNION SELECT dst FROM edges)
""")
print('L1 isolated norms:', c.fetchone()[0])

c.execute("""
SELECT count(*) FROM cases WHERE case_id NOT IN (SELECT src FROM edges UNION SELECT dst FROM edges)
""")
print('L1 isolated cases:', c.fetchone()[0])

c.execute("""
SELECT count(*) FROM reference_norms WHERE ref_id NOT IN (SELECT src FROM reference_edges UNION SELECT dst FROM reference_edges)
""")
print('L2 isolated reference_norms:', c.fetchone()[0])

c.execute("""
SELECT count(*) FROM reference_cases WHERE case_id NOT IN (SELECT src FROM reference_edges UNION SELECT dst FROM reference_edges)
""")
print('L2 isolated reference_cases:', c.fetchone()[0])

conn.close()
