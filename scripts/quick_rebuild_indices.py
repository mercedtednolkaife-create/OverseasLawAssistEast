import sys
from pathlib import Path
import sqlite3

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from lawagent.store.bm25 import BM25Engine
from lawagent.store.vec import DenseVectorEngine

DB_PATH = Path("data/snapshots/20261021-asean-v2.2/law.sqlite")
INDEX_DIR = Path("data/snapshots/20261021-asean-v2.2/index")
INDEX_L2_DIR = Path("data/snapshots/20261021-asean-v2.2/index_l2")

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row

# L1
l1_rows = conn.execute("SELECT chunk_id, kind, ref_id, seq, text FROM chunks").fetchall()
l1_chunks = [dict(r) for r in l1_rows]
bm25_l1 = BM25Engine(index_dir=INDEX_DIR)
bm25_l1.build_from_chunks(l1_chunks)
vec_l1 = DenseVectorEngine(index_dir=INDEX_DIR)
vec_l1.build_from_chunks(l1_chunks, batch_size=16)

# L2
l2_rows = conn.execute("SELECT chunk_id, kind, ref_id, seq, text FROM reference_chunks").fetchall()
l2_chunks = [dict(r) for r in l2_rows]
bm25_l2 = BM25Engine(index_dir=INDEX_L2_DIR)
bm25_l2.build_from_chunks(l2_chunks)
vec_l2 = DenseVectorEngine(index_dir=INDEX_L2_DIR)
vec_l2.build_from_chunks(l2_chunks, batch_size=16)

conn.close()
print("Indices rebuild complete.")
