"""混合检索与证据中心召回器 (HybridRetriever)
对齐技术方案第 3.6 节与第 4.4 节：
1. 精确通道：问句中包含 § 或案号时，直接通过 norm_lookup / case_lookup 精确置顶
2. 混合召回：BM25 (德语分词+复合词拆分) top 50 与 BGE-M3 向量 top 50
3. RRF 融合：倒数排名融合取 top 30
4. 图扩展：沿 CITES 与 APPLIES 边扩展候选池
5. 重排截断：bge-reranker 深度交互打分，取 top 8
6. 证据封装：格式化为满足《司法解释（二）》第三条要素的 Evidence 对象
"""

import re
from datetime import datetime
from collections import defaultdict
from typing import List, Dict, Any, Optional, Tuple

import os
import csv
import sqlite3
from lawagent.core.types import Evidence
from lawagent.store.snapshots import SnapshotManager
from lawagent.store.bm25 import BM25Engine
from lawagent.store.vec import DenseVectorEngine
from lawagent.store.rerank import Reranker
from lawagent.store.graph import SQLiteGraphStore

RE_NORM_EXACT = re.compile(
    r"(UU_\d+_\d+|SEMA_\d+_\d+|CIPAA_\d+|SOPA_\d+|Law_\d+_\d+|RA_\d+|FIDIC|BIT|SASAC|CN_ID_BIT|CN_VN_BIT|CN_PH_BIT|SINOSURE|KUHPerdata|CCC|Act_\d+|MEMR_\d+|Decree_\d+)\s*(?:§|Art\.?|Section\s*|Sec\.?|Clause\s*)?\s*([0-9a-zA-Z\-\:\.]+)",
    re.IGNORECASE,
)
RE_CASE_EXACT = re.compile(
    r"\b(BS Mount Sophia|JBE Properties|Sumatec|Manila Water|Martego|Bauer|Hopewell|SEMA\s*3/2023|PCAB)\b",
    re.IGNORECASE,
)



def rrf_fusion(rank_lists: List[List[Tuple[str, float]]], k: int = 60) -> List[Tuple[str, float]]:
    """互惠排名融合 (Reciprocal Rank Fusion)"""
    scores = defaultdict(float)
    for rank_list in rank_lists:
        for r, (cid, _) in enumerate(rank_list):
            scores[cid] += 1.0 / (k + r + 1)
    sorted_items = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_items


class HybridRetriever:
    def __init__(
        self,
        snapshot_mgr: Optional[SnapshotManager] = None,
        bm25_engine: Optional[BM25Engine] = None,
        vec_engine: Optional[DenseVectorEngine] = None,
        graph_store: Optional[SQLiteGraphStore] = None,
        reranker: Optional[Reranker] = None,
        glossary_path: Optional[str] = "kb/asean/glossary.csv",
        snapshot_id: Optional[str] = None
    ):
        self.snapshot_mgr = snapshot_mgr or SnapshotManager()
        self.snapshot_id = snapshot_id or self.snapshot_mgr.get_current_snapshot_id()
        index_dir = os.path.join(self.snapshot_mgr.base_dir, self.snapshot_id, "index")
        index_l2_dir = os.path.join(self.snapshot_mgr.base_dir, self.snapshot_id, "index_l2")

        if bm25_engine is None:
            self.bm25 = BM25Engine(index_dir=index_dir)
            self.bm25.load()
        else:
            self.bm25 = bm25_engine

        if vec_engine is None:
            vec = DenseVectorEngine(index_dir=index_dir)
            if vec.load():
                self.vec = vec
            else:
                self.vec = None
        else:
            self.vec = vec_engine

        # L2 广覆盖参考库双引擎 (BM25 + FAISS Dense Vector)
        self.bm25_l2: Optional[BM25Engine] = None
        self.vec_l2: Optional[DenseVectorEngine] = None
        if os.path.exists(index_l2_dir):
            try:
                b_l2 = BM25Engine(index_dir=index_l2_dir)
                if b_l2.load():
                    self.bm25_l2 = b_l2
            except Exception:
                self.bm25_l2 = None

            try:
                v_l2 = DenseVectorEngine(index_dir=index_l2_dir)
                if v_l2.load():
                    self.vec_l2 = v_l2
            except Exception:
                self.vec_l2 = None

        if graph_store is None:
            self.graph = SQLiteGraphStore(self.snapshot_mgr.get_connection(self.snapshot_id))
        else:
            self.graph = graph_store

        self.reranker = reranker or Reranker(enabled=False)
        self.glossary_path = glossary_path
        self._load_glossary()

    @classmethod
    def from_snapshot(
        cls,
        snapshot_id: Optional[str] = None,
        base_dir: str = "data/snapshots",
        enable_vec: bool = True
    ) -> "HybridRetriever":
        return cls(snapshot_id=snapshot_id)

    def _load_glossary(self):
        self.glossary_zh_to_de: Dict[str, str] = {
            "工期顺延": "Extension of Time EOT Clause 8.4 delayed possession site",
            "工期延误": "delay Extension of Time EOT Clause 8.4",
            "索赔时效": "Clause 20.1 28 days notice of claim time bar",
            "索赔通知": "Clause 20.1 28 days notice of claim",
            "失权": "time-bar bar from any remedy good faith SEMA 3 2023",
            "保函止付": "performance security bond unconscionability stop payment BS Mount Sophia",
            "履约保函": "performance security bond Clause 4.2",
            "显失公平": "unconscionability unconscionable BS Mount Sophia JBE Properties",
            "本地化率": "TKDN Tingkat Komponen Dalam Negeri MEMR Reg 11 2024",
            "外资准入": "foreign contractor license BUJKA PCAB CIDB joint venture",
            "联合体": "KSO Kerja Sama Operasi Joint Operation UU 2 2017",
            "联营体": "KSO Kerja Sama Operasi Joint Operation BUJKA",
            "背靠背": "pay-when-paid CIPAA Section 35 SOPA Section 9 void",
            "间接征收": "indirect expropriation BIT China ASEAN Article 6",
            "征收补偿": "expropriation compensation prompt adequate effective",
            "特许经营": "concession agreement PPP RA 11966 Law 135 2025",
            "语言效力": "SEMA 3 2023 UU 24 2009 language validity bad faith",
            "预定违约金": "liquidated damages LDs Law 135 2025 Decree 210 2026",
            "国资监管": "PRC SASAC Order 35 state-owned enterprise investment",
            "数据安全": "PRC Data Security Law Article 36 cross-border transfer",
            "建设工程": "construction services contract FIDIC Silver Book",
            "总承包": "EPC turnkey contractor FIDIC Silver Book",
        }
        if self.glossary_path and os.path.exists(self.glossary_path):
            try:
                with open(self.glossary_path, "r", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        zh = (row.get("zh") or "").strip()
                        target = (row.get("target") or row.get("en") or row.get("de") or "").strip()
                        if zh and target:
                            clean_zh = zh.split("/")[0].split("(")[0].strip()
                            if len(clean_zh) >= 2:
                                self.glossary_zh_to_de[clean_zh] = target
            except Exception:
                pass

    def expand_query(self, query: str) -> str:
        """利用术语库将中文工程法律问句扩充东盟法规及 FIDIC 核心对应用语"""
        extra_terms = []
        for zh_term, target_term in self.glossary_zh_to_de.items():
            if zh_term in query and target_term not in query:
                extra_terms.append(target_term)
        if extra_terms:
            return f"{query} {' '.join(extra_terms[:2])}"
        return query

    def search(
        self,
        query: str,
        top_k: int = 8,
        law_filter: Optional[str] = None,
        kind_filter: Optional[str] = None,
        expand_graph: bool = True,
        snapshot_id: Optional[str] = None,
        must_norms: Optional[List[str]] = None,
        layer: str = "AUTO"
    ) -> List[Evidence]:
        """端到端双层混合检索主流程 (支持 L1 高优先级与 L2 广覆盖参考层级联)"""
        # 若显式请求仅检索 L2 广覆盖参考层
        if layer == "L2":
            return self.search_l2(query, top_k=top_k, law_filter=law_filter, kind_filter=kind_filter, snapshot_id=snapshot_id)

        evidences: List[Evidence] = []
        seen_refs = set()
        exact_chunks: List[str] = []

        # ---------------------------------------------------------
        # 0. 优先保障必选法条 (must_norms 置顶)
        # ---------------------------------------------------------
        if must_norms:
            for mn in must_norms:
                clean_ref = mn.replace("NORM:", "").strip()
                norm = self.snapshot_mgr.norm_lookup(clean_ref, snapshot_id=snapshot_id)
                if norm and norm["norm_id"] not in seen_refs:
                    seen_refs.add(norm["norm_id"])
                    ev = Evidence(
                        eid=f"E{len(evidences) + 1}",
                        kind="norm",
                        role="law",
                        ref_id=norm["norm_id"],
                        text_de=(norm.get("text_zh") or norm.get("text_en") or norm.get("text_de") or "")[:1500],
                        text_original=norm.get("text_original"),
                        text_en=norm.get("text_en"),
                        text_zh=norm.get("text_zh"),
                        language_mode=norm.get("language_mode", "bilingual"),
                        translation_source=norm.get("translation_source"),
                        source_url=norm["source_url"],
                        stand=norm.get("stand"),
                        fetched_at=datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                        grade="A"
                    )
                    evidences.append(ev)

        # ---------------------------------------------------------
        # 1. 确定性精确通道 (置顶)
        # ---------------------------------------------------------
        for m in RE_NORM_EXACT.finditer(query):
            law, nr = m.group(1).upper(), m.group(2)
            norm = self.snapshot_mgr.norm_lookup(law, f"§{nr}", snapshot_id)
            if norm and norm["norm_id"] not in seen_refs:
                seen_refs.add(norm["norm_id"])
                ev = Evidence(
                    eid=f"E{len(evidences) + 1}",
                    kind="norm",
                    role="law",
                    ref_id=norm["norm_id"],
                    text_de=(norm.get("text_zh") or norm.get("text_en") or norm.get("text_de") or "")[:1500],
                    text_original=norm.get("text_original"),
                    text_en=norm.get("text_en"),
                    text_zh=norm.get("text_zh"),
                    language_mode=norm.get("language_mode", "bilingual"),
                    translation_source=norm.get("translation_source"),
                    source_url=norm["source_url"],
                    stand=norm.get("stand"),
                    fetched_at=datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                    grade="A"
                )
                evidences.append(ev)

        for m in RE_CASE_EXACT.finditer(query):
            az = m.group(1)
            case_data = self.snapshot_mgr.case_lookup(az, snapshot_id)
            if case_data and case_data["case_id"] not in seen_refs:
                seen_refs.add(case_data["case_id"])
                ev = Evidence(
                    eid=f"E{len(evidences) + 1}",
                    kind="case",
                    role="law",
                    ref_id=case_data["case_id"],
                    text_de=(case_data.get("leitsatz") or case_data.get("gruende") or "")[:1500],
                    text_original=case_data.get("gruende"),
                    text_en=case_data.get("tenor"),
                    text_zh=case_data.get("leitsatz"),
                    source_url=case_data["source_url"],
                    stand=case_data.get("decided"),
                    fetched_at=datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                    grade="A"
                )
                evidences.append(ev)

        if len(evidences) >= top_k:
            return evidences[:top_k]

        # ---------------------------------------------------------
        # 2. BM25 与 Dense 向量检索
        # ---------------------------------------------------------
        expanded_q = self.expand_query(query)
        bm25_res = self.bm25.search(expanded_q, top_k=50, kind_filter=kind_filter, law_filter=law_filter)
        vec_res = []
        l1_top_vec_score = 0.0
        if self.vec is not None:
            try:
                vec_res = self.vec.search(query, top_k=50)
                if vec_res:
                    l1_top_vec_score = float(vec_res[0][1])
            except Exception:
                vec_res = []

        rank_lists = [bm25_res]
        if vec_res:
            rank_lists.append(vec_res)

        # ---------------------------------------------------------
        # 3. RRF 融合 (取 top 30)
        # ---------------------------------------------------------
        fused = rrf_fusion(rank_lists, k=60)[:30]

        # ---------------------------------------------------------
        # 4. 图扩展 (APPLIES 关联判例与 conflicts_with / overrides / interprets 关联法源)
        # ---------------------------------------------------------
        candidate_cids = [cid for cid, _ in fused]
        if expand_graph and self.graph:
            top_norm_ids = [
                self.bm25.chunk_metadata[cid]["ref_id"]
                for cid in candidate_cids[:5]
                if cid in self.bm25.chunk_metadata and self.bm25.chunk_metadata[cid]["kind"] == "norm"
            ]
            for nid in top_norm_ids:
                hot_cases = self.graph.get_hot_cases_for_norm(nid, limit=3)
                for hcase in hot_cases:
                    case_cid = f"CHUNK:CASE:{hcase}:0"
                    if case_cid not in candidate_cids:
                        candidate_cids.append(case_cid)

            # 真正动态图扩展：通过 graph.expand 发现冲突法条、上位法与适用先例
            if top_norm_ids:
                try:
                    expanded_nodes = self.graph.expand(
                        top_norm_ids,
                        max_hops=1,
                        limit=5
                    )
                    for item in expanded_nodes:
                        raw_node = item.get("node", "").replace("NORM:", "").replace("CASE:", "").strip()
                        norm_cid = f"CHUNK:NORM:{raw_node}:0"
                        case_cid = f"CHUNK:CASE:{raw_node}:0"
                        if norm_cid in self.bm25.chunk_metadata and norm_cid not in candidate_cids:
                            candidate_cids.append(norm_cid)
                        elif case_cid in self.bm25.chunk_metadata and case_cid not in candidate_cids:
                            candidate_cids.append(case_cid)
                except Exception:
                    pass

        # ---------------------------------------------------------
        # 5. 重排打分 (取 top 8)
        # ---------------------------------------------------------
        conn = self.snapshot_mgr.get_connection(snapshot_id)
        candidates_data = []
        for cid in candidate_cids:
            cur = conn.cursor()
            cur.execute("SELECT chunk_id, kind, ref_id, text FROM chunks WHERE chunk_id = ?", (cid,))
            row = cur.fetchone()
            if row:
                candidates_data.append({
                    "chunk_id": row["chunk_id"],
                    "kind": row["kind"],
                    "ref_id": row["ref_id"],
                    "text": row["text"],
                    "rrf_score": next((s for c, s in fused if c == cid), 0.015)
                })

        # 候选重排取充足数量以保障去重后填满 top_k 条不同法条/裁判
        rerank_pool_size = max(top_k * 3, 16)
        reranked = self.reranker.rerank(query, candidates_data, top_k=rerank_pool_size)

        # ---------------------------------------------------------
        # 6. 构造 Evidence 对象
        # ---------------------------------------------------------
        for cdata, score in reranked:
            ref_id = cdata["ref_id"]
            if ref_id in seen_refs:
                continue
            seen_refs.add(ref_id)

            kind = cdata["kind"]
            if kind == "norm":
                norm = self.snapshot_mgr.norm_lookup(ref_id, snapshot_id=snapshot_id)
                if norm:
                    ev = Evidence(
                        eid=f"E{len(evidences) + 1}",
                        kind="norm",
                        role="law",
                        ref_id=ref_id,
                        text_de=(norm.get("text_zh") or norm.get("text_en") or cdata["text"])[:1500],
                        text_original=norm.get("text_original"),
                        text_en=norm.get("text_en"),
                        text_zh=norm.get("text_zh"),
                        language_mode=norm.get("language_mode", "bilingual"),
                        translation_source=norm.get("translation_source"),
                        source_url=norm["source_url"],
                        stand=norm.get("stand"),
                        fetched_at=datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                        grade="A"
                    )
                    evidences.append(ev)
            else:
                case_data = self.snapshot_mgr.case_lookup(ref_id, snapshot_id=snapshot_id)
                if case_data:
                    ev = Evidence(
                        eid=f"E{len(evidences) + 1}",
                        kind="case",
                        role="law",
                        ref_id=ref_id,
                        text_de=cdata["text"][:1500],
                        text_original=case_data.get("gruende"),
                        text_en=case_data.get("tenor"),
                        text_zh=case_data.get("leitsatz"),
                        source_url=case_data["source_url"],
                        stand=case_data.get("decided"),
                        fetched_at=datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                        grade="A"
                    )
                    evidences.append(ev)

            if len(evidences) >= top_k:
                break

        # ---------------------------------------------------------
        # 7. 双层架构级联补齐 (Cascade to L2 Reference KB)
        # ---------------------------------------------------------
        if layer in ("AUTO", "ALL"):
            if layer == "ALL":
                l2_evs = self.search_l2(
                    query=query,
                    top_k=min(top_k, 5),
                    law_filter=law_filter,
                    kind_filter=kind_filter,
                    snapshot_id=snapshot_id
                )
                for l2_ev in l2_evs:
                    if l2_ev.ref_id not in seen_refs:
                        seen_refs.add(l2_ev.ref_id)
                        evidences.append(l2_ev)
            elif layer == "AUTO":
                needed = top_k - len(evidences)
                l2_probe_score = 0.0
                if self.vec_l2 is not None:
                    try:
                        probe_res = self.vec_l2.search(query, top_k=1)
                        if probe_res:
                            l2_probe_score = float(probe_res[0][1])
                    except Exception:
                        pass

                should_cascade = (
                    (needed > 0)
                    or (l2_probe_score >= 0.70 and l2_probe_score > l1_top_vec_score)
                    or (l1_top_vec_score < 0.65 and l2_probe_score >= 0.60)
                )
                if should_cascade:
                    fetch_k = max(needed, 2)
                    l2_evs = self.search_l2(
                        query=query,
                        top_k=fetch_k,
                        law_filter=law_filter,
                        kind_filter=kind_filter,
                        snapshot_id=snapshot_id
                    )
                    valid_l2 = [ev for ev in l2_evs if ev.ref_id not in seen_refs]
                    if valid_l2:
                        if needed > 0:
                            evidences.extend(valid_l2[:needed])
                        else:
                            # L1 虽填满 top_k，但 L2 相关性显著更优；保留 L1 前部最强项，将尾部替换为 L2 最优前 1~2 项
                            num_replace = min(len(valid_l2), 2)
                            evidences = evidences[:top_k - num_replace] + valid_l2[:num_replace]

        return evidences[:top_k] if layer != "ALL" else evidences

    def search_l2(
        self,
        query: str,
        top_k: int = 5,
        law_filter: Optional[str] = None,
        kind_filter: Optional[str] = None,
        snapshot_id: Optional[str] = None,
        expand_graph: bool = True
    ) -> List[Evidence]:
        """对第二层广覆盖参考知识库 (L2 Reference KB) 执行 BM25 + FAISS 稠密向量双通道混合检索 + 轻量级 GraphRAG 拓扑扩展"""
        if self.bm25_l2 is None and self.vec_l2 is None:
            return []

        evidences: List[Evidence] = []
        seen_refs = set()

        expanded_q = self.expand_query(query)
        bm25_res = []
        if self.bm25_l2 is not None:
            try:
                bm25_res = self.bm25_l2.search(expanded_q, top_k=30, kind_filter=kind_filter, law_filter=law_filter)
            except Exception:
                bm25_res = []

        vec_res = []
        if self.vec_l2 is not None:
            try:
                vec_res = self.vec_l2.search(query, top_k=30)
            except Exception:
                vec_res = []

        rank_lists = []
        if bm25_res:
            rank_lists.append(bm25_res)
        if vec_res:
            rank_lists.append(vec_res)

        if not rank_lists:
            return []

        fused = rrf_fusion(rank_lists, k=60)[:30]
        conn = self.snapshot_mgr.get_connection(snapshot_id)
        if not conn:
            return []

        candidate_cids = [cid for cid, _ in fused]

        # ---------------------------------------------------------
        # L2 轻量级 GraphRAG 拓扑扩展: 沿 reference_edges 发现跨法域条约、关联规程与裁判
        # ---------------------------------------------------------
        if expand_graph:
            top_ref_ids = []
            cur = conn.cursor()
            for cid in candidate_cids[:5]:
                cur.execute("SELECT ref_id FROM reference_chunks WHERE chunk_id = ?", (cid,))
                r = cur.fetchone()
                if r:
                    top_ref_ids.append(r["ref_id"] if isinstance(r, sqlite3.Row) else r[0])

            if top_ref_ids:
                try:
                    placeholders = ",".join("?" for _ in top_ref_ids)
                    cur.execute(
                        f"""SELECT dst AS node FROM reference_edges WHERE src IN ({placeholders})
                            UNION
                            SELECT src AS node FROM reference_edges WHERE dst IN ({placeholders})
                            LIMIT 8""",
                        [*top_ref_ids, *top_ref_ids]
                    )
                    linked_nodes = [row[0] for row in cur.fetchall()]
                    for node in linked_nodes:
                        norm_cid = f"CHUNK:REF_NORM:{node}:0"
                        case_cid = f"CHUNK:REF_CASE:{node}:0"
                        if norm_cid not in candidate_cids:
                            cur.execute("SELECT 1 FROM reference_chunks WHERE chunk_id = ?", (norm_cid,))
                            if cur.fetchone():
                                candidate_cids.append(norm_cid)
                        elif case_cid not in candidate_cids:
                            cur.execute("SELECT 1 FROM reference_chunks WHERE chunk_id = ?", (case_cid,))
                            if cur.fetchone():
                                candidate_cids.append(case_cid)
                except Exception:
                    pass

        cur = conn.cursor()
        for cid in candidate_cids:
            cur.execute("SELECT chunk_id, kind, ref_id, text FROM reference_chunks WHERE chunk_id = ?", (cid,))
            row = cur.fetchone()
            if not row:
                continue

            ref_id = row["ref_id"]
            if ref_id in seen_refs:
                continue
            seen_refs.add(ref_id)

            kind = row["kind"]
            if kind == "reference_norm":
                norm = self.snapshot_mgr.norm_lookup(ref_id, snapshot_id=snapshot_id)
                if norm:
                    ev = Evidence(
                        eid=f"E_L2_{len(evidences) + 1}",
                        kind="norm",
                        role="law",
                        layer="L2",
                        ref_id=norm["norm_id"],
                        text_de=(norm.get("text_zh") or norm.get("text_en") or row["text"])[:1500],
                        text_original=norm.get("text_original"),
                        text_en=norm.get("text_en"),
                        text_zh=norm.get("text_zh"),
                        language_mode=norm.get("language_mode", "bilingual"),
                        translation_source=norm.get("translation_source", "MOJ_FATONG_2026"),
                        source_url=norm.get("source_url", "https://www.fatong.gov.cn"),
                        stand=norm.get("stand"),
                        fetched_at=datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                        grade="B"
                    )
                    evidences.append(ev)
            elif kind == "reference_case":
                case_data = self.snapshot_mgr.case_lookup(ref_id, snapshot_id=snapshot_id)
                if case_data:
                    ev = Evidence(
                        eid=f"E_L2_{len(evidences) + 1}",
                        kind="case",
                        role="law",
                        layer="L2",
                        ref_id=case_data["case_id"],
                        text_de=row["text"][:1500],
                        text_original=case_data.get("gruende"),
                        text_en=case_data.get("tenor"),
                        text_zh=case_data.get("leitsatz"),
                        source_url=case_data.get("source_url", ""),
                        stand=case_data.get("decided"),
                        fetched_at=datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                        grade="B"
                    )
                    evidences.append(ev)

            if len(evidences) >= top_k:
                break

        return evidences

    def similar_cases(
        self,
        fact_summary: str,
        norm_ids: Optional[List[str]] = None,
        top_k: int = 5,
        snapshot_id: Optional[str] = None
    ) -> List[Evidence]:
        """以案情事实检索类似判例的事实部分 (Tatbestand) 并标记为 role='similar'"""
        candidates = self.search(
            query=f"Tatbestand {fact_summary}",
            top_k=top_k * 2,
            kind_filter="case",
            snapshot_id=snapshot_id
        )
        similar_evs: List[Evidence] = []
        for ev in candidates:
            if ev.kind == "case":
                similar_ev = ev.model_copy(update={"role": "similar"})
                similar_evs.append(similar_ev)
            if len(similar_evs) >= top_k:
                break
        return similar_evs
