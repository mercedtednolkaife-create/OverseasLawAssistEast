"""本体图扩展存储模块 (GraphStore)
对齐技术方案第 4.6 节：
- 使用 SQLite edges_top 物化表与递归 CTE 进行双向受限图遍历 (1~2 跳，扇出上限受控)
- 查询关联判例 (APPLIES / applied_in) 与关联法条 (conflicts_with / overrides / interprets)
- 抽象 GraphStore 协议，支持法源冲突检测与层级扩展
"""

import sqlite3
from typing import List, Dict, Any, Optional, Protocol, runtime_checkable

DEFAULT_GRAPH_RELS = [
    "conflicts_with",
    "overrides",
    "overrules",
    "interprets",
    "interpreted_by",
    "INTERPRETS",
    "applied_in",
    "applied_by",
    "triggers_preservation",
    "CITES",
    "cites",
    "APPLIES",
    "applies",
    "applies_with",
    "DEFINES",
    "defines",
    "correlates_with",
    "CORRELATES_WITH",
    "references",
    "governs",
    "governed_by",
    "complements",
    "COMPLEMENTS",
    "cross_references",
    "CROSS_REFERENCES",
    "distinguishes",
    "exception_to",
    "hierarchical_child",
    "hierarchical_parent",
    "HIERARCHICAL_PARENT",
    "delegates_to",
    "limits_liability",
    "LIMITS_LIABILITY",
    "prerequisite_for",
    "PREREQUISITE_FOR",
    "upgrades_to_treaty",
    "UPGRADES_TO_TREATY",
    "triggers",
    "co_enforced_by",
    "cross_regulatory",
    "enforces",
    "escalates_to",
    "follows",
    "harmonizes_with",
    "implements",
    "interoperates_with",
    "mitigates",
    "precedes",
    "reciprocates_with",
    "regulates",
    "remedied_by",
    "standardizes"
]


@runtime_checkable
class GraphStore(Protocol):
    """图存储接口规范"""
    def neighbors(
        self,
        node_id: str,
        rels: Optional[List[str]] = None,
        direction: str = "out",
        limit: int = 20
    ) -> List[Dict[str, Any]]: ...

    def expand(
        self,
        start_ids: List[str],
        max_hops: int = 2,
        rels: Optional[List[str]] = None,
        limit: int = 60
    ) -> List[Dict[str, Any]]: ...


def _expand_id_aliases(nid: str) -> List[str]:
    """生成节点 ID 的多种跨库别名变体，确保不同命名规范下的边节点均能无损互联"""
    variants = [nid]
    raw = nid
    if raw.startswith("NORM:"):
        raw = raw[5:]
        variants.append(raw)
    elif raw.startswith("CASE:"):
        raw = raw[5:]
        variants.append(raw)
    else:
        variants.append(f"NORM:{raw}")

    # 针对东盟成文法常见异名规范映射
    alias_rules = [
        ("VN:Civil_Code_2015:", "Civil_Code_VN:"),
        ("Civil_Code_VN:", "VN:Civil_Code_2015:"),
        ("TH:CCC:", "Civil_Code_TH:"),
        ("Civil_Code_TH:", "TH:CCC:"),
        ("Civil and Commercial Code:", "TH:CCC:"),
        ("ID:KUHPerdata:", "KUHPerdata:"),
        ("KUHPerdata:", "ID:KUHPerdata:"),
        ("MY:Contracts_Act_1950:", "Contracts_Act_MY:"),
        ("Contracts_Act_MY:", "MY:Contracts_Act_1950:"),
        ("PH:Civil_Code_RA386:", "Civil_Code_PH:"),
        ("Civil_Code_PH:", "PH:Civil_Code_RA386:"),
        ("BN:Constitution:Art84C_Absolute_Sovereign_Immunity", "BN:Constitution:Art84C"),
        ("BN:Constitution:Art84C", "BN:Constitution:Art84C_Absolute_Sovereign_Immunity"),
    ]
    for src_pref, dst_pref in alias_rules:
        if src_pref in raw:
            alt = raw.replace(src_pref, dst_pref)
            variants.append(alt)
            variants.append(f"NORM:{alt}")
            
    return list(dict.fromkeys(variants))


class SQLiteGraphStore:
    def __init__(self, db_path_or_conn: Any = "data/snapshots/20261021-asean-v2.2/law.sqlite"):
        if isinstance(db_path_or_conn, sqlite3.Connection):
            self.conn = db_path_or_conn
            self.db_path = None
        else:
            self.db_path = str(db_path_or_conn)
            self.conn = None

    def _get_conn(self) -> sqlite3.Connection:
        if self.conn is not None:
            return self.conn
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def neighbors(
        self,
        node_id: str,
        rels: Optional[List[str]] = None,
        direction: str = "out",
        limit: int = 20,
        layer: str = "ALL"
    ) -> List[Dict[str, Any]]:
        """获取直连邻居节点 (支持 out / in / both，同时兼容裸 ID 与带 NORM:/CASE: 前缀 ID，并融合跨命名别名与跨层视图)"""
        id_variants = _expand_id_aliases(node_id)

        conn = self._get_conn()
        cur = conn.cursor()

        table = "unified_edges" if layer == "ALL" else ("edges_top" if layer == "L1" else "reference_edges")

        query_rels = rels if rels else DEFAULT_GRAPH_RELS
        placeholders_rels = ",".join("?" for _ in query_rels)
        placeholders_ids = ",".join("?" for _ in id_variants)

        order_clause = "ORDER BY rk ASC" if table == "edges_top" else ""

        if direction == "out":
            sql = f"""SELECT dst as node, rel, source FROM {table}
                      WHERE src IN ({placeholders_ids}) AND rel IN ({placeholders_rels})
                      {order_clause} LIMIT ?"""
            cur.execute(sql, [*id_variants, *query_rels, limit])
        elif direction == "in":
            sql = f"""SELECT src as node, rel, source FROM {table}
                      WHERE dst IN ({placeholders_ids}) AND rel IN ({placeholders_rels})
                      {order_clause} LIMIT ?"""
            cur.execute(sql, [*id_variants, *query_rels, limit])
        else:  # both
            sql = f"""SELECT dst as node, rel, source FROM {table}
                      WHERE src IN ({placeholders_ids}) AND rel IN ({placeholders_rels})
                      UNION ALL
                      SELECT src as node, rel, source FROM {table}
                      WHERE dst IN ({placeholders_ids}) AND rel IN ({placeholders_rels})
                      LIMIT ?"""
            cur.execute(sql, [*id_variants, *query_rels, *id_variants, *query_rels, limit])

        return [dict(r) for r in cur.fetchall()]

    def expand(
        self,
        start_ids: List[str],
        max_hops: int = 2,
        rels: Optional[List[str]] = None,
        limit: int = 60,
        layer: str = "ALL"
    ) -> List[Dict[str, Any]]:
        """执行 1~2 跳双向递归 CTE 图扩展 (严格控制扇出与最大条数，同时支持 unified_edges 跨层穿透)"""
        if not start_ids:
            return []

        clean_starts = set()
        for sid in start_ids:
            for variant in _expand_id_aliases(sid):
                clean_starts.add(variant)
        clean_starts_list = list(clean_starts)

        allowed_rels = rels or DEFAULT_GRAPH_RELS
        rel_clause = ",".join(f"'{r}'" for r in allowed_rels)

        conn = self._get_conn()
        cur = conn.cursor()

        table = "unified_edges" if layer == "ALL" else ("edges_top" if layer == "L1" else "reference_edges")

        # 构建起始节点 UNION 查询
        start_unions = " UNION ALL ".join(f"SELECT '{s}' AS node, 0 AS depth" for s in clean_starts_list)

        sql = f"""
        WITH RECURSIVE walk(node, depth) AS (
            {start_unions}
            UNION
            SELECT CASE WHEN e.src = w.node THEN e.dst ELSE e.src END, w.depth + 1
            FROM walk w
            JOIN {table} e ON (e.src = w.node OR e.dst = w.node)
            WHERE w.depth < ? AND e.rel IN ({rel_clause})
        )
        SELECT node, MIN(depth) AS depth
        FROM walk
        WHERE node NOT IN ({','.join(f"'{s}'" for s in clean_starts_list)})
        GROUP BY node
        ORDER BY depth ASC
        LIMIT ?;
        """

        try:
            cur.execute(sql, (max_hops, limit))
            return [dict(r) for r in cur.fetchall()]
        except Exception:
            return []
        except Exception:
            return []

    def get_hot_cases_for_norm(self, norm_id: str, limit: int = 5) -> List[str]:
        """获取适用该法条的热门判例 ID (预计算物化表)"""
        clean_norm = norm_id.replace("NORM:", "")
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute(
            """SELECT case_id FROM hot_norm_cases
               WHERE norm_id = ?
               ORDER BY rank ASC LIMIT ?""",
            (clean_norm, limit)
        )
        return [row[0] for row in cur.fetchall()]
