"""多语言稠密向量引擎 (Dense Vector Search Engine)
对齐技术方案第 4.4 节：
- 使用 BGE-M3 / SentenceTransformer 进行跨语言语义嵌入 (中文问句直接检索德语法条/判决)
- 向量 L2 归一化后使用 FAISS IndexFlatIP (余弦相似度)
- 本地 NVIDIA GPU (CUDA) 加速推理，支持优雅缓存与增量检索
"""

import os
import pickle
import numpy as np
import faiss
import torch
from typing import List, Tuple, Optional, Dict, Any
from sentence_transformers import SentenceTransformer


class DenseVectorEngine:
    def __init__(
        self,
        model_name: str = "BAAI/bge-m3",
        index_dir: str = "data/snapshots/20261021-asean-v2.2/index",
        device: Optional[str] = None
    ):
        self.model_name = model_name
        self.index_dir = index_dir
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model: Optional[SentenceTransformer] = None
        self.index: Optional[faiss.IndexFlatIP] = None
        self.chunk_ids: List[str] = []
        self.chunk_metadata: Dict[str, Dict[str, Any]] = {}
        os.makedirs(self.index_dir, exist_ok=True)

    def _ensure_model(self):
        if self.model is None:
            try:
                from lawagent.store.models_loader import load_sentence_transformer
                self.model = load_sentence_transformer(self.model_name, device=self.device)
                if self.model:
                    self.model.max_seq_length = 512
            except Exception as e:
                logger.warning(f"Dense 向量模型 {self.model_name} 载入异常或处于离线环境，平滑回退至 BM25+图检索: {e}")
                self.model = None

    def build_from_chunks(self, chunks: List[Dict[str, Any]], batch_size: int = 12):
        """批量编码分块文本并建立 FAISS 索引"""
        self._ensure_model()
        if self.model is None:
            return
        texts = [c["text"] for c in chunks]
        self.chunk_ids = [c["chunk_id"] for c in chunks]
        self.chunk_metadata = {
            c["chunk_id"]: {
                "kind": c.get("kind"),
                "ref_id": c.get("ref_id"),
                "law": c.get("law", ""),
            }
            for c in chunks
        }

        # 编码向量 (GPU batch)
        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=True,
            normalize_embeddings=True,
            device=self.device
        )
        embeddings = np.array(embeddings, dtype=np.float32)

        # 构建 FAISS 内积索引 (对于单位向量等同于余弦相似度)
        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dim)
        self.index.add(embeddings)

        self.save()

    def save(self):
        """保存 FAISS 索引与 chunk_ids/metadata 映射"""
        if self.index is not None:
            faiss_path = os.path.join(self.index_dir, "faiss.index")
            faiss.write_index(self.index, faiss_path)
        with open(os.path.join(self.index_dir, "chunk_ids_vec.pkl"), "wb") as f:
            pickle.dump(self.chunk_ids, f)
        with open(os.path.join(self.index_dir, "chunk_meta_vec.pkl"), "wb") as f:
            pickle.dump(self.chunk_metadata, f)

    def load(self) -> bool:
        """加载已构建的 FAISS 向量索引"""
        faiss_path = os.path.join(self.index_dir, "faiss.index")
        ids_path = os.path.join(self.index_dir, "chunk_ids_vec.pkl")
        meta_path = os.path.join(self.index_dir, "chunk_meta_vec.pkl")

        if not (os.path.exists(faiss_path) and os.path.exists(ids_path)):
            return False

        self.index = faiss.read_index(faiss_path)
        with open(ids_path, "rb") as f:
            self.chunk_ids = pickle.load(f)
        if os.path.exists(meta_path):
            try:
                with open(meta_path, "rb") as f:
                    self.chunk_metadata = pickle.load(f)
            except Exception:
                self.chunk_metadata = {}
        return True

    def search(
        self,
        query: str,
        top_k: int = 50,
        law_filter: Optional[str] = None,
        kind_filter: Optional[str] = None,
        chunk_metadata: Optional[Dict[str, Any]] = None,
    ) -> List[Tuple[str, float]]:
        """执行稠密向量检索，支持国别/法典过滤与类型过滤，返回 [(chunk_id, cosine_score), ...] 降序列表"""
        if self.index is None:
            if not self.load():
                return []

        self._ensure_model()
        if self.model is None:
            return []
        with torch.inference_mode():
            q_emb = self.model.encode([query], normalize_embeddings=True, device=self.device)
        q_emb = np.array(q_emb, dtype=np.float32)

        meta_source = chunk_metadata or self.chunk_metadata
        fetch_k = min(max(top_k * 5, 100), self.index.ntotal) if (law_filter or kind_filter) else min(top_k, self.index.ntotal)
        scores, indices = self.index.search(q_emb, fetch_k)

        results: List[Tuple[str, float]] = []
        clean_law = law_filter.replace("asean_", "").upper() if law_filter else None

        for score, idx in zip(scores[0], indices[0]):
            if idx < 0 or idx >= len(self.chunk_ids):
                continue
            cid = self.chunk_ids[idx]

            # 类别过滤 (norm vs case)
            if kind_filter:
                cid_kind = "case" if ":CASE:" in cid else ("norm" if ":NORM:" in cid else None)
                if not cid_kind and meta_source and cid in meta_source:
                    raw_k = meta_source[cid].get("kind", "")
                    cid_kind = "case" if raw_k in ("case", "reference_case") else ("norm" if raw_k in ("norm", "reference_norm") else raw_k)
                if cid_kind and cid_kind != kind_filter:
                    continue

            # 法域过滤
            if clean_law:
                cid_upper = cid.upper()
                matched = False
                if f":{clean_law}" in cid_upper or f"_{clean_law}" in cid_upper or cid_upper.startswith(clean_law):
                    matched = True
                elif meta_source and cid in meta_source:
                    m_law = str(meta_source[cid].get("law") or "").upper()
                    m_ref = str(meta_source[cid].get("ref_id") or "").upper()
                    if clean_law in m_law or clean_law in m_ref:
                        matched = True
                # TREATY, FIDIC, INTL, ICSID, CN母国监管与双边协定等通用规则不应被排除
                if any(common_p in cid_upper for common_p in (":FIDIC:", ":TREATY:", ":ACIA:", ":CAFTA:", ":RCEP:", ":ICSID:", ":PCA:", ":SIAC:", ":CN:", ":SINOSURE:", ":DTA:", ":MDB:", ":INTL:")):
                    matched = True
                if not matched:
                    continue

            results.append((cid, float(score)))
            if len(results) >= top_k:
                break

        return results
