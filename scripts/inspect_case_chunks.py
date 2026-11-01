import sys
from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

import sqlite3

conn = sqlite3.connect('data/snapshots/20261021-asean-v2.2/law.sqlite')
conn.row_factory = sqlite3.Row

print("--- L1 Case Chunks in DB ---")
for r in conn.execute("SELECT chunk_id, kind, ref_id, seq, length(text) as l, substr(text, 1, 100) as t FROM chunks WHERE kind = 'case' LIMIT 5").fetchall():
    print(dict(r))

print("--- Total case chunks in DB ---")
print(conn.execute("SELECT count(*) FROM chunks WHERE kind = 'case'").fetchone()[0])
print("--- Total cases in DB ---")
print(conn.execute("SELECT count(*) FROM cases").fetchone()[0])

from lawagent.store.chunker import chunk_cases
sample_case = [dict(r) for r in conn.execute("SELECT * FROM cases LIMIT 1").fetchall()]
chunks_gen = chunk_cases(sample_case)
print("--- Generated chunks for 1 case using chunk_cases() ---")
for c in chunks_gen:
    print(c['chunk_id'], c['seq'], len(c['text']), c['ctx_prefix'])
