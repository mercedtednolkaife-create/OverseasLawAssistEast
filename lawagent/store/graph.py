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
    "interprets",
    "interpreted_by",
    "applied_in",
    "triggers_preservation",
    "CITES",
    "cites",
    "APPLIES",
    "applies",
    "DEFINES",
    "correlates_with",
    "references",
    "governs"
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
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """获取直连邻居节点 (支持 out / in / both，同时兼容裸 ID 与带 NORM:/CASE: 前缀 ID)"""
        # 构建节点 ID 的多重变体，确保无论库中是裸 ID 还是带前缀均可精准召回
        id_variants = [node_id]
        if node_id.startswith("NORM:"):
            id_variants.append(node_id[5:])
        else:
            id_variants.append(f"NORM:{node_id}")
        if node_id.startswith("CASE:"):
            id_variants.append(node_id[5:])
        id_variants = list(dict.fromkeys(id_variants))

        conn = self._get_conn()
        cur = conn.cursor()

        query_rels = rels if rels else DEFAULT_GRAPH_RELS
        placeholders_rels = ",".join("?" for _ in query_rels)
        placeholders_ids = ",".join("?" for _ in id_variants)

        if direction == "out":
            sql = f"""SELECT dst as node, rel, source FROM edges_top
                      WHERE src IN ({placeholders_ids}) AND rel IN ({placeholders_rels})
                      ORDER BY rk ASC LIMIT ?"""
            cur.execute(sql, [*id_variants, *query_rels, limit])
        elif direction == "in":
            sql = f"""SELECT src as node, rel, source FROM edges_top
                      WHERE dst IN ({placeholders_ids}) AND rel IN ({placeholders_rels})
                      ORDER BY rk ASC LIMIT ?"""
            cur.execute(sql, [*id_variants, *query_rels, limit])
        else:  # both
            sql = f"""SELECT dst as node, rel, source FROM edges_top
                      WHERE src IN ({placeholders_ids}) AND rel IN ({placeholders_rels})
                      UNION ALL
                      SELECT src as node, rel, source FROM edges_top
                      WHERE dst IN ({placeholders_ids}) AND rel IN ({placeholders_rels})
                      LIMIT ?"""
            cur.execute(sql, [*id_variants, *query_rels, *id_variants, *query_rels, limit])

        return [dict(r) for r in cur.fetchall()]

    def expand(
        self,
        start_ids: List[str],
        max_hops: int = 2,
        rels: Optional[List[str]] = None,
        limit: int = 60
    ) -> List[Dict[str, Any]]:
        """执行 1~2 跳双向递归 CTE 图扩展 (严格控制扇出与最大条数，同时兼容带前缀与裸 ID)"""
        if not start_ids:
            return []

        clean_starts = set()
        for sid in start_ids:
            clean_starts.add(sid)
            if sid.startswith("NORM:"):
                clean_starts.add(sid[5:])
            else:
                clean_starts.add(f"NORM:{sid}")
            if sid.startswith("CASE:"):
                clean_starts.add(sid[5:])
        clean_starts_list = list(clean_starts)

        allowed_rels = rels or DEFAULT_GRAPH_RELS
        rel_clause = ",".join(f"'{r}'" for r in allowed_rels)

        conn = self._get_conn()
        cur = conn.cursor()

        # 构建起始节点 UNION 查询
        start_unions = " UNION ALL ".join(f"SELECT '{s}' AS node, 0 AS depth" for s in clean_starts_list)

        sql = f"""
        WITH RECURSIVE walk(node, depth) AS (
            {start_unions}
            UNION
            SELECT CASE WHEN e.src = w.node THEN e.dst ELSE e.src END, w.depth + 1
            FROM walk w
            JOIN edges_top e ON (e.src = w.node OR e.dst = w.node)
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
