import sqlite3
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

db_path = 'data/snapshots/20261021-asean-v2.2/law.sqlite'
conn = sqlite3.connect(db_path)
cur = conn.cursor()

tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
print('=== law.sqlite 数据表及条数 ===')
for t in tables:
    cnt = cur.execute(f"SELECT count(*) FROM {t}").fetchone()[0]
    print(f"  {t}: {cnt}")

print('\n=== norms 表结构 ===')
for col in cur.execute("PRAGMA table_info(norms)").fetchall():
    print(f"  {col[1]} ({col[2]})")

print('\n=== reference_norms 表结构 ===')
for col in cur.execute("PRAGMA table_info(reference_norms)").fetchall():
    print(f"  {col[1]} ({col[2]})")

