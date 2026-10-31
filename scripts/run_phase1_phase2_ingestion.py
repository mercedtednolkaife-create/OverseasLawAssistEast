"""
run_phase1_phase2_ingestion.py - 阶段一与阶段二联合入库与全量索引流水线
1. 阶段一：入库 15 篇权威标杆判例（L1 10 篇冲刺至 97 篇，L2 5 篇增至 63 篇，全库案例达 160 篇）
2. 阶段二：入库 102+ 条涉外条约与标准规范（FIDIC全矩阵、中国-东盟DTA、6国BIT、中国涉外监管底座、多边公约）
3. 拓扑图谱：写入 edges 与 reference_edges，刷新 edges_top 与 hot_norm_cases，确保 0 dangling edges
4. 质量门禁：校验全部判例字数与 elements_json 完备性
5. 索引重建：重构 L1 与 L2 的 BM25 与 DenseVector 索引
"""
import sys
import json
import sqlite3
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from scripts.implement_phase1_cases import PHASE1_NEW_CASES_L1, PHASE1_NEW_CASES_L2
from scripts.data_phase2_fidic_and_dta import PHASE2_FIDIC_CLAUSES, PHASE2_DTA_TREATIES
from scripts.data_phase2_bit_prc_treaties import (
    PHASE2_BIT_TREATIES, PHASE2_PRC_OUTBOUND_NORMS, PHASE2_MULTILATERAL_TREATIES
)
from scripts.data_phase2_supplements import (
    PHASE2_FIDIC_SUPPLEMENTS, PHASE2_DTA_SUPPLEMENTS, PHASE2_BIT_SUPPLEMENTS,
    PHASE2_PRC_SUPPLEMENTS, PHASE2_MULTI_SUPPLEMENTS, PHASE2_STATUTE_PATCHES,
    PHASE2_EXTRA_TREATIES_AND_STANDARDS
)

from lawagent.store.bm25 import BM25Engine
from lawagent.store.vec import DenseVectorEngine

DB_PATH = Path("data/snapshots/20261021-asean-v2.2/law.sqlite")
INDEX_DIR = Path("data/snapshots/20261021-asean-v2.2/index")
INDEX_L2_DIR = Path("data/snapshots/20261021-asean-v2.2/index_l2")

def run_ingestion():
    print("=" * 60)
    print(">>> 启动阶段一与阶段二联合入库流水线...")
    print("=" * 60)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # ----------------------------------------------------
    # Step 1: 写入阶段二成文法与条约规范 (优先写入规范，确保判例关联时目标已存在)
    # ----------------------------------------------------
    all_norms = (
        PHASE2_FIDIC_CLAUSES + PHASE2_DTA_TREATIES +
        PHASE2_BIT_TREATIES + PHASE2_PRC_OUTBOUND_NORMS + PHASE2_MULTILATERAL_TREATIES +
        PHASE2_FIDIC_SUPPLEMENTS + PHASE2_DTA_SUPPLEMENTS + PHASE2_BIT_SUPPLEMENTS +
        PHASE2_PRC_SUPPLEMENTS + PHASE2_MULTI_SUPPLEMENTS + PHASE2_STATUTE_PATCHES +
        PHASE2_EXTRA_TREATIES_AND_STANDARDS
    )
    print(f"\n[Step 1] 正在处理阶段二规范共 {len(all_norms)} 条...")

    l1_norm_count = 0
    l2_norm_count = 0

    for n in all_norms:
        target_table = n.get("table", "reference_norms")
        nid = n["norm_id"]
        law = n.get("law", nid.split(":")[0])
        enbez = n.get("enbez", "")
        title = n.get("title", "")
        heading_path = n.get("heading_path", "")
        language_mode = n.get("language_mode", "bilingual")
        lang_original = n.get("lang_original", "en")
        text_original = n.get("text_original", "")
        text_en = n.get("text_en", "")
        text_zh = n.get("text_zh", "")
        norm_category = n.get("norm_category", "statute")
        mandatory_level = n.get("mandatory_level", "mandatory")
        elements_json = n.get("elements_json", "[]")

        if target_table == "norms":
            cur.execute("""
                INSERT OR REPLACE INTO norms
                (norm_id, law, enbez, title, heading_path, language_mode, lang_original,
                 text_original, text_en, text_zh, norm_category, mandatory_level, elements_json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (nid, law, enbez, title, heading_path, language_mode, lang_original,
                  text_original, text_en, text_zh, norm_category, mandatory_level, elements_json))

            chunk_id = f"CHUNK:NORM:{nid}:0"
            chunk_text = f"[{nid}] {title} | {text_zh} | {text_en} | {text_original}"
            cur.execute("""
                INSERT OR REPLACE INTO chunks (chunk_id, kind, ref_id, seq, text)
                VALUES (?, ?, ?, ?, ?)
            """, (chunk_id, "norm", nid, 0, chunk_text))
            l1_norm_count += 1

        else:
            cur.execute("""
                INSERT OR REPLACE INTO reference_norms
                (norm_id, law, enbez, title, heading_path, language_mode, lang_original,
                 text_original, text_en, text_zh, norm_category, mandatory_level, elements_json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (nid, law, enbez, title, heading_path, language_mode, lang_original,
                  text_original, text_en, text_zh, norm_category, mandatory_level, elements_json))

            chunk_id = f"CHUNK:REF_NORM:{nid}:0"
            chunk_text = f"[{nid}] {title} | {text_zh} | {text_en} | {text_original}"
            cur.execute("""
                INSERT OR REPLACE INTO reference_chunks (chunk_id, kind, ref_id, seq, text)
                VALUES (?, ?, ?, ?, ?)
            """, (chunk_id, "norm", nid, 0, chunk_text))
            l2_norm_count += 1

    print(f"✓ Step 1 完成：写入阶段二规范 (L1: {l1_norm_count} 条, L2: {l2_norm_count} 条)")

    # ----------------------------------------------------
    # Step 2: 写入阶段一标杆裁判文书 (10 篇 L1 + 5 篇 L2)
    # ----------------------------------------------------
    print(f"\n[Step 2] 正在处理阶段一裁判文书共 {len(PHASE1_NEW_CASES_L1) + len(PHASE1_NEW_CASES_L2)} 篇...")

    # 1. 写入 L1 cases
    for c in PHASE1_NEW_CASES_L1:
        cur.execute("""
            INSERT OR REPLACE INTO cases
            (case_id, court, az, decided, leitsatz, tenor, tatbestand, gruende, source_url, norms_meta)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            c["case_id"], c["court"], c["az"], c["decided"],
            c["leitsatz"], c["tenor"], c["tatbestand"], c["gruende"],
            c["source_url"], c["norms_meta"]
        ))
        chunk_id = f"CHUNK:CASE:{c['case_id']}:0"
        chunk_text = f"[{c['case_id']}] {c['court']} {c['az']} {c['leitsatz']} | {c['tatbestand']} | {c['gruende']} | {c['tenor']}"
        cur.execute("""
            INSERT OR REPLACE INTO chunks (chunk_id, kind, ref_id, seq, text)
            VALUES (?, ?, ?, ?, ?)
        """, (chunk_id, "case", c["case_id"], 0, chunk_text))

        # 关联 L1 edges
        if c.get("norms_meta"):
            for nid in [n.strip() for n in c["norms_meta"].split(",") if n.strip()]:
                cur.execute("""
                    INSERT OR REPLACE INTO edges (src, dst, rel, source, reviewed)
                    VALUES (?, ?, ?, ?, ?)
                """, (c["case_id"], nid, "interprets", "PHASE1_CASES", 1))

    # 2. 写入 L2 reference_cases
    for c in PHASE1_NEW_CASES_L2:
        cur.execute("""
            INSERT OR REPLACE INTO reference_cases
            (case_id, court, az, decided, leitsatz, tenor, tatbestand, gruende, source_url, norms_meta)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            c["case_id"], c["court"], c["az"], c["decided"],
            c["leitsatz"], c["tenor"], c["tatbestand"], c["gruende"],
            c["source_url"], c["norms_meta"]
        ))
        chunk_id = f"CHUNK:REF_CASE:{c['case_id']}:0"
        chunk_text = f"[{c['case_id']}] {c['court']} {c['az']} {c['leitsatz']} | {c['tatbestand']} | {c['gruende']} | {c['tenor']}"
        cur.execute("""
            INSERT OR REPLACE INTO reference_chunks (chunk_id, kind, ref_id, seq, text)
            VALUES (?, ?, ?, ?, ?)
        """, (chunk_id, "case", c["case_id"], 0, chunk_text))

        # 关联 L2 reference_edges
        if c.get("norms_meta"):
            for nid in [n.strip() for n in c["norms_meta"].split(",") if n.strip()]:
                cur.execute("""
                    INSERT OR REPLACE INTO reference_edges (src, dst, rel, description)
                    VALUES (?, ?, ?, ?)
                """, (c["case_id"], nid, "INTERPRETS", f"Case {c['case_id']} interprets {nid}"))

    print(f"✓ Step 2 完成：写入阶段一案例 (L1: {len(PHASE1_NEW_CASES_L1)} 篇, L2: {len(PHASE1_NEW_CASES_L2)} 篇)")

    # ----------------------------------------------------
    # Step 3: 刷新加速物化表
    # ----------------------------------------------------
    print("\n[Step 3] 正在刷新图谱加速物化表 edges_top 和 hot_norm_cases...")
    cur.execute("DELETE FROM edges_top")
    cur.execute("""
        INSERT INTO edges_top (src, dst, rel, source, reviewed, rk)
        SELECT src, dst, rel, source, reviewed,
               ROW_NUMBER() OVER (PARTITION BY src ORDER BY rowid ASC) as rk
        FROM edges
    """)
    cur.execute("DELETE FROM hot_norm_cases")
    cur.execute("""
        INSERT OR REPLACE INTO hot_norm_cases (norm_id, case_id, rank)
        SELECT dst AS norm_id, src AS case_id,
               ROW_NUMBER() OVER (PARTITION BY dst ORDER BY rowid ASC) as rank
        FROM edges
        WHERE rel IN ('applies', 'interpreted_by', 'applied_in', 'interprets', 'INTERPRETS')
    """)
    conn.commit()
    print("✓ Step 3 完成：加速物化表已刷新。")

    # ----------------------------------------------------
    # Step 4: 数据库指标统计与悬空边质检
    # ----------------------------------------------------
    print("\n[Step 4] 正在执行全库指标盘点与拓扑图谱悬空边质检...")
    cnt_l1_norms = cur.execute("SELECT count(*) FROM norms").fetchone()[0]
    cnt_l2_norms = cur.execute("SELECT count(*) FROM reference_norms").fetchone()[0]
    cnt_l1_cases = cur.execute("SELECT count(*) FROM cases").fetchone()[0]
    cnt_l2_cases = cur.execute("SELECT count(*) FROM reference_cases").fetchone()[0]
    cnt_l1_edges = cur.execute("SELECT count(*) FROM edges").fetchone()[0]
    cnt_l2_edges = cur.execute("SELECT count(*) FROM reference_edges").fetchone()[0]

    all_norms_in_db = {r[0] for r in cur.execute("SELECT norm_id FROM norms UNION SELECT norm_id FROM reference_norms").fetchall()}
    all_cases_in_db = {r[0] for r in cur.execute("SELECT case_id FROM cases UNION SELECT case_id FROM reference_cases").fetchall()}
    all_valid_nodes = all_norms_in_db | all_cases_in_db

    # 检查 edges 悬空
    dangling_l1 = cur.execute("""
        SELECT e.src, e.dst FROM edges e
        WHERE e.dst NOT IN (
            SELECT norm_id FROM norms 
            UNION SELECT norm_id FROM reference_norms 
            UNION SELECT case_id FROM cases 
            UNION SELECT case_id FROM reference_cases
        )
    """).fetchall()

    # 检查 reference_edges 悬空
    dangling_l2 = cur.execute("""
        SELECT re.src, re.dst FROM reference_edges re
        WHERE re.dst NOT IN (SELECT norm_id FROM reference_norms UNION SELECT norm_id FROM norms UNION SELECT case_id FROM reference_cases UNION SELECT case_id FROM cases)
    """).fetchall()

    # 检查案例四要素达标率
    all_cases = cur.execute("SELECT case_id, leitsatz, tenor, tatbestand, gruende FROM cases UNION SELECT case_id, leitsatz, tenor, tatbestand, gruende FROM reference_cases").fetchall()
    failing_cases = []
    for cid, l, t, tb, g in all_cases:
        if len(l or "") < 150 or len(t or "") < 150 or len(tb or "") < 200 or len(g or "") < 350 or "【出海央企实操攻防启示】" not in (g or ""):
            failing_cases.append(cid)

    # 检查 elements_json 完备率
    all_norms_res = cur.execute("SELECT norm_id, elements_json FROM norms UNION SELECT norm_id, elements_json FROM reference_norms").fetchall()
    missing_elements = [nid for nid, ej in all_norms_res if not ej or ej == "[]"]

    print("-" * 50)
    print(f"成文法与条约规模: L1={cnt_l1_norms}, L2={cnt_l2_norms}, 总计={cnt_l1_norms + cnt_l2_norms} 条")
    print(f"裁判文书案例规模: L1={cnt_l1_cases}, L2={cnt_l2_cases}, 总计={cnt_l1_cases + cnt_l2_cases} 篇")
    print(f"拓扑图谱关系边数: L1 edges={cnt_l1_edges}, L2 reference_edges={cnt_l2_edges}")
    print(f"L1 悬空边数: {len(dangling_l1)} 条")
    print(f"L2 悬空边数: {len(dangling_l2)} 条")
    print(f"金标准案例不合规数: {len(failing_cases)} 篇")
    print(f"elements_json 缺失数: {len(missing_elements)} 条")
    print("-" * 50)

    assert len(dangling_l1) == 0, f"发现 L1 悬空边: {dangling_l1}"
    assert len(dangling_l2) == 0, f"发现 L2 悬空边: {dangling_l2}"
    assert len(failing_cases) == 0, f"发现字数不达标案例: {failing_cases}"
    assert len(missing_elements) == 0, f"发现缺失要素规范: {missing_elements}"
    print("✓ Step 4 质检全部通过：0 悬空边，100% 金标准，100% 结构化要素！")

    conn.close()

    # ----------------------------------------------------
    # Step 5: 全量重建双层向量与 BM25 索引
    # ----------------------------------------------------
    print("\n[Step 5] 正在全量重建 L1 与 L2 索引 (BM25 + DenseVector)...")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    # L1
    l1_rows = conn.execute("SELECT chunk_id, kind, ref_id, seq, text FROM chunks").fetchall()
    l1_chunks = [dict(r) for r in l1_rows]
    print(f"  正在构建 L1 BM25 索引 (共 {len(l1_chunks)} 个 chunks)...")
    bm25_l1 = BM25Engine(index_dir=INDEX_DIR)
    bm25_l1.build_from_chunks(l1_chunks)
    print(f"  正在构建 L1 FAISS 向量索引 (共 {len(l1_chunks)} 个 chunks)...")
    vec_l1 = DenseVectorEngine(index_dir=INDEX_DIR)
    vec_l1.build_from_chunks(l1_chunks, batch_size=16)

    # L2
    l2_rows = conn.execute("SELECT chunk_id, kind, ref_id, seq, text FROM reference_chunks").fetchall()
    l2_chunks = [dict(r) for r in l2_rows]
    print(f"  正在构建 L2 BM25 索引 (共 {len(l2_chunks)} 个 chunks)...")
    bm25_l2 = BM25Engine(index_dir=INDEX_L2_DIR)
    bm25_l2.build_from_chunks(l2_chunks)
    print(f"  正在构建 L2 FAISS 向量索引 (共 {len(l2_chunks)} 个 chunks)...")
    vec_l2 = DenseVectorEngine(index_dir=INDEX_L2_DIR)
    vec_l2.build_from_chunks(l2_chunks, batch_size=16)

    conn.close()
    print("✓ Step 5 完成：双层 BM25 与 FAISS 向量索引全部重建成功！")
    print("=" * 60)
    print("🎉 阶段一与阶段二联合入库圆满完成！")
    print("=" * 60)

if __name__ == "__main__":
    run_ingestion()
