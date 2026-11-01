"""模型安全加载与国内高速镜像下载保障模块 (Model Loader)
对齐技术方案第 4.4 节与审查报告 v2 优化建议：
1. 本地优先：检测本地绝对路径与 Hugging Face/ModelScope 本地缓存目录，无网络开销；
2. 镜像加速：若本地未命中需下载，优先使用 ModelScope (魔搭社区) 或国内高速镜像 (hf-mirror.com)；
3. 平滑回退：捕获所有网络与解析异常，确保系统离线与弱网环境绝对稳定运行。
"""

import os
import logging
from typing import Optional, Any

logger = logging.getLogger(__name__)

# ModelScope (魔搭社区) 官方/官方同步模型 ID 映射表
MODELSCOPE_MODEL_MAP = {
    "BAAI/bge-m3": "BAAI/bge-m3",
    "BAAI/bge-reranker-v2-m3": "BAAI/bge-reranker-v2-m3"
}

def setup_download_mirrors():
    """在中国大陆网络环境下自动配置合规镜像端点，避免 huggingface.co 握手超时"""
    if not os.environ.get("HF_ENDPOINT"):
        os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

def resolve_model_path(model_name: str, prefer_modelscope: bool = True) -> str:
    """解析模型路径：支持本地路径、本地缓存或国内高速下载源"""
    # 1. 直接指定本地目录
    if os.path.exists(model_name):
        return model_name

    # 2. 深度穿透探测 Hugging Face 本地快照目录 (支持 default_cache_path / TRANSFORMERS_CACHE / 自定义盘符)
    safe_name = model_name.replace("/", "--")
    possible_roots = []
    try:
        from transformers.utils.hub import default_cache_path, TRANSFORMERS_CACHE
        if default_cache_path:
            possible_roots.append(str(default_cache_path))
        if TRANSFORMERS_CACHE:
            possible_roots.append(str(TRANSFORMERS_CACHE))
    except Exception:
        pass

    possible_roots.extend([
        os.environ.get("HF_HOME", ""),
        os.environ.get("HF_HUB_CACHE", ""),
        os.environ.get("TORCH_HOME", ""),
        "F:/torchcache/huggingface/hub",
        "D:/torchcache/huggingface/hub",
        os.path.expanduser("~/.cache/huggingface/hub"),
    ])

    import glob
    for root in possible_roots:
        if not root or not os.path.exists(root):
            continue
        model_dir = os.path.join(root, f"models--{safe_name}")
        if os.path.exists(model_dir):
            # 优先返回具体 snapshots 目录下的实体权重文件路径
            snapshots_dir = os.path.join(model_dir, "snapshots")
            if os.path.exists(snapshots_dir):
                snaps = [s for s in glob.glob(os.path.join(snapshots_dir, "*")) if os.path.isdir(s)]
                # 优先挑选包含完整 SentenceTransformer / CrossEncoder 结构的快照 (modules.json 或 config.json)
                st_snaps = [s for s in snaps if os.path.exists(os.path.join(s, "modules.json"))]
                cfg_snaps = [s for s in snaps if os.path.exists(os.path.join(s, "config.json"))]
                best_snaps = st_snaps or cfg_snaps or snaps
                if best_snaps:
                    # 返回最新快照绝对路径，彻底切断所有外部网络连接与握手等待
                    latest_snap = sorted(best_snaps, key=os.path.getmtime, reverse=True)[0]
                    return latest_snap
            return model_dir

    # 3. 若已安装 ModelScope，国内环境优先调用 snapshot_download
    if prefer_modelscope:
        try:
            from modelscope.hub.snapshot_download import snapshot_download
            ms_id = MODELSCOPE_MODEL_MAP.get(model_name, model_name)
            logger.info(f"正在通过 ModelScope (魔搭社区) 高速载入模型: {ms_id} ...")
            local_dir = snapshot_download(ms_id)
            logger.info(f"ModelScope 模型载入就绪: {local_dir}")
            return local_dir
        except Exception as e:
            logger.info(f"跳过 ModelScope 加载 (环境未安装或载入跳过: {e})，切换至镜像源")

    # 4. 配置国内镜像源加速 HuggingFace 原生下载
    setup_download_mirrors()
    return model_name

def load_sentence_transformer(model_name: str, device: str) -> Any:
    """安全加载 Dense 语义向量模型 (SentenceTransformer)"""
    from sentence_transformers import SentenceTransformer
    resolved_path = resolve_model_path(model_name)
    if os.path.isdir(resolved_path):
        return SentenceTransformer(resolved_path, device=device)
    try:
        # 优先使用本地文件，避免非预期网络检查
        return SentenceTransformer(resolved_path, device=device, local_files_only=True)
    except Exception:
        setup_download_mirrors()
        return SentenceTransformer(resolved_path, device=device)

def load_cross_encoder(model_name: str, max_length: int = 512, device: str = "cpu") -> Any:
    """安全加载 Cross-Encoder 深度交互重排模型 (CrossEncoder)"""
    from sentence_transformers import CrossEncoder
    resolved_path = resolve_model_path(model_name)
    if os.path.isdir(resolved_path):
        return CrossEncoder(resolved_path, max_length=max_length, device=device)
    try:
        # 优先使用本地文件
        return CrossEncoder(resolved_path, max_length=max_length, device=device, local_files_only=True)
    except Exception:
        setup_download_mirrors()
        return CrossEncoder(resolved_path, max_length=max_length, device=device)
