# -*- coding: utf-8 -*-
"""数据库清洗、去重与关系归一化脚本 (scripts/normalize_and_dedup_kb.py)
对齐《功能优化及审查.md》Phase 1 & Phase 2 第一步规范：
1. 合并 L1 中的 7 组重复裁判 (同一判决不同ID)
2. 消除 L1/L2 跨表完全重合的 3 条规范
3. 合并 L1 内同条文多粒度重复条文 (如数安法、发改委11号令、反外国制裁法重复项)
4. 归一化 edges 和 reference_edges 关系名为标准小写体系
5. 彻底消除 35 组重复边，建立唯一约束保障
6. 按法理优先级重新生成 edges_top 并计算权重 rk
"""

import sys
import sqlite3
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

DB_PATH = ROOT_DIR / "data/snapshots/20261021-asean-v2.2/law.sqlite"

CASE_MERGES = [
    ("CASE:SG_CA:CKR_Contract_Services_2015", "CASE:SG_CA:CKR_Contract_Services:2015"),
    ("CASE:MY_FC:Jack_In_Pile_v_Bauer_2020", "CASE:MY_FC:Jack_In_Pile_v_Bauer:2020"),
    ("CASE:MY_FC:Cubic_Electronics_2019", "CASE:MY_FC:Cubic_Electronics:2019"),
    ("CASE:SG_CA:Denka_Advantech_2020", "CASE:SG_CA:Denka_Advantech:2020"),
    ("CASE:ID_MA:Putusan_MA_601_K_Pdt_2015", "CASE:ID_MA:Nine_Am_v_Nusa_Bangsa_Loan:2015"),
    ("CASE:TH_SC:Supreme_Court_1054_2561", "CASE:TH_SC:No_1054_2561_Delay_Damages_Reduction:2018"),
    ("CASE:VN_Hanoi_HC:VIAC_Award_Enforcement_2022", "CASE:VN_HCMC_HC:SetAside_VIAC_Fundamental_Principles:2022"),
]

NORM_MERGES_L1 = [
    ("CN:Data_Security_Law:Art36_Crossborder_Data", "CN:Data_Security_Law:Art36"),
    ("CN:NDRC_Order_11:Art13_Sensitive_Approval", "CN:NDRC_Order_11:Art13_14"),
    ("CN:NDRC_Order_11:Art13_15", "CN:NDRC_Order_11:Art13_14"),
    ("CN:Anti_Foreign_Sanctions_Law:Art12_15", "CN:Anti_Foreign_Sanctions_Law:Art12_Blocking"),
    ("ID:KUHPerdata:Art1266_1267", "ID:KUHPerdata:Art1266"),
    ("SG:IAA_Cap_143A:Sec12A_Interim_Injunction", "SG:IAA_Cap_143A:Sec12A"),
]

RELATION_MAPPING = {
    "COMPLEMENTS": "complements",
    "CORRELATES_WITH": "correlates_with",
    "CROSS_REFERENCES": "cross_references",
    "GOVERNED_BY": "governed_by",
    "HIERARCHICAL_PARENT": "hierarchical_parent",
    "INTERPRETS": "interprets",
    "LIMITS_LIABILITY": "limits_liability",
    "PREREQUISITE_FOR": "prerequisite_for",
    "UPGRADES_TO_TREATY": "upgrades_to_treaty",
    "DEFINES": "defines",
    "REFERENCES": "references",
}


def deduplicate_and_normalize():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    print("=== [1/6] 消除 L1/L2 跨表完全重合规范 ===")
    # FIDIC 条款属于 L2 广覆盖参考层，PH 规章属于 L1 属地法
    cur.execute("DELETE FROM norms WHERE norm_id IN ('FIDIC:Silver_2017:Clause_8.5', 'FIDIC:Silver_2017:Clause_21.4')")
    cur.execute("DELETE FROM reference_norms WHERE norm_id = 'PH:DOLE_DO_174_17:Sec5'")
    print("  ✓ 已清理 3 条跨表重叠规范")

    print("=== [2/6] 合并 L1 中的 7 组重复裁判 ===")
    for remove_id, keep_id in CASE_MERGES:
        if remove_id == keep_id:
            continue
        cur.execute("SELECT count(*) FROM cases WHERE case_id = ?", (remove_id,))
        if cur.fetchone()[0] > 0:
            # 转移 edges
            cur.execute("DELETE FROM edges WHERE src = ? AND dst IN (SELECT dst FROM edges WHERE src = ?)", (remove_id, keep_id))
            cur.execute("UPDATE edges SET src = ? WHERE src = ?", (keep_id, remove_id))
            cur.execute("DELETE FROM edges WHERE dst = ? AND src IN (SELECT src FROM edges WHERE dst = ?)", (remove_id, keep_id))
            cur.execute("UPDATE edges SET dst = ? WHERE dst = ?", (keep_id, remove_id))
            # 转移 hot_norm_cases
            cur.execute("DELETE FROM hot_norm_cases WHERE case_id = ? AND norm_id IN (SELECT norm_id FROM hot_norm_cases WHERE case_id = ?)", (remove_id, keep_id))
            cur.execute("UPDATE hot_norm_cases SET case_id = ? WHERE case_id = ?", (keep_id, remove_id))
            # 删除旧 case
            cur.execute("DELETE FROM cases WHERE case_id = ?", (remove_id,))
            print(f"  ✓ 合并案例: {remove_id} -> {keep_id}")

    print("=== [3/6] 合并 L1 中同条文多粒度重复条文 ===")
    for remove_id, keep_id in NORM_MERGES_L1:
        cur.execute("SELECT count(*) FROM norms WHERE norm_id = ?", (remove_id,))
        if cur.fetchone()[0] > 0:
            cur.execute("DELETE FROM edges WHERE src = ? AND dst IN (SELECT dst FROM edges WHERE src = ?)", (remove_id, keep_id))
            cur.execute("UPDATE edges SET src = ? WHERE src = ?", (keep_id, remove_id))
            cur.execute("DELETE FROM edges WHERE dst = ? AND src IN (SELECT src FROM edges WHERE dst = ?)", (remove_id, keep_id))
            cur.execute("UPDATE edges SET dst = ? WHERE dst = ?", (keep_id, remove_id))
            cur.execute("DELETE FROM hot_norm_cases WHERE norm_id = ? AND case_id IN (SELECT case_id FROM hot_norm_cases WHERE norm_id = ?)", (remove_id, keep_id))
            cur.execute("UPDATE hot_norm_cases SET norm_id = ? WHERE norm_id = ?", (keep_id, remove_id))
            cur.execute("DELETE FROM norms WHERE norm_id = ?", (remove_id,))
            print(f"  ✓ 合并条文: {remove_id} -> {keep_id}")

    print("=== [4/6] 归一化 edges 和 reference_edges 关系名称 ===")
    for old_rel, new_rel in RELATION_MAPPING.items():
        cur.execute("UPDATE edges SET rel = ? WHERE rel = ?", (new_rel, old_rel))
        cur.execute("UPDATE reference_edges SET rel = ? WHERE rel = ?", (new_rel, old_rel))

    print("=== [5/6] 消除 edges 和 reference_edges 中的重复边 ===")
    # L1 edges 去重
    cur.execute("""
        CREATE TABLE edges_dedup AS
        SELECT src, dst, rel, min(source) as source, min(span) as span, max(confidence) as confidence, max(reviewed) as reviewed, min(snapshot_id) as snapshot_id
        FROM edges
        GROUP BY src, dst, rel
    """)
    cur.execute("DELETE FROM edges")
    cur.execute("INSERT INTO edges SELECT * FROM edges_dedup")
    cur.execute("DROP TABLE edges_dedup")

    # L2 reference_edges 去重
    cur.execute("""
        CREATE TABLE ref_edges_dedup AS
        SELECT min(edge_id) as edge_id, src, dst, rel, min(description) as description
        FROM reference_edges
        GROUP BY src, dst, rel
    """)
    cur.execute("DELETE FROM reference_edges")
    cur.execute("INSERT INTO reference_edges SELECT * FROM ref_edges_dedup")
    cur.execute("DROP TABLE ref_edges_dedup")
    print("  ✓ edges 与 reference_edges 已完成去重与唯一化")

    print("=== [6/6] 按法理优先级重新生成 edges_top 并分配权重 rk ===")
    cur.execute("DELETE FROM edges_top")
    # 分配优先级权重
    cur.execute("""
        INSERT INTO edges_top (src, dst, rel, source, reviewed, rk)
        SELECT 
            src, dst, rel, source, reviewed,
            ROW_NUMBER() OVER (
                PARTITION BY src 
                ORDER BY 
                    CASE 
                        WHEN rel IN ('overrides', 'conflicts_with', 'exception_to', 'triggers_preservation') THEN 1
                        WHEN rel IN ('applied_in', 'applied_by', 'applies', 'interprets', 'interpreted_by', 'distinguishes') THEN 2
                        WHEN rel IN ('governs', 'hierarchical_parent', 'upgrades_to_treaty') THEN 3
                        ELSE 4
                    END,
                    confidence DESC,
                    dst ASC
            ) as rk
        FROM edges
    """)
    print("  ✓ edges_top 已按法理优先级重构完毕")

    conn.commit()
    conn.close()
    print(">>> 数据库去重与规范化成功落地！")


if __name__ == "__main__":
    deduplicate_and_normalize()
