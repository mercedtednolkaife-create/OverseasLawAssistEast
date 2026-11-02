"""模型安全加载与国内高速镜像下载保障模块 (Model Loader)
对齐技术方案第 4.4 节与中国大陆地区高校/企业部署环境要求：
1. 本地优先：穿透探测 ModelScope (魔搭社区) 与 Hugging Face 本地缓存目录，有缓存则秒级加载、零网络开销；
2. 国内第一源：若本地未命中，100% 优先接入阿里云魔搭社区 (ModelScope) 官方高速 CDN 下载 BAAI 官方模型；
3. 容灾后备：若 ModelScope 异常，回退至国内镜像源 (hf-mirror.com)；
4. 运行保障：杜绝形式化降级；完整校验权重实体 (model.safetensors / pytorch_model.bin)，确保稠密向量检索与重排真实可用。
"""

import os
import glob
import logging
from typing import Optional, Any, List

logger = logging.getLogger(__name__)

# ModelScope (魔搭社区) 官方同步模型 ID 映射表
MODELSCOPE_MODEL_MAP = {
    "BAAI/bge-m3": "BAAI/bge-m3",
    "BAAI/bge-reranker-v2-m3": "BAAI/bge-reranker-v2-m3"
}


def _is_valid_model_dir(dir_path: str) -> bool:
    """核验指定路径是否为包含完整权重的有效模型目录"""
    if not dir_path or not os.path.isdir(dir_path):
        return False
    has_weights = any(
        os.path.exists(os.path.join(dir_path, f))
        for f in ["model.safetensors", "pytorch_model.bin", "model.bin"]
    )
    has_config = os.path.exists(os.path.join(dir_path, "config.json"))
    return has_weights and has_config


def setup_download_mirrors():
    """在中国大陆网络环境下自动配置合规镜像端点，避免 huggingface.co 握手超时"""
    if not os.environ.get("HF_ENDPOINT"):
        os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"


def resolve_model_path(model_name: str, prefer_modelscope: bool = True) -> str:
    """解析模型路径：支持本地路径、ModelScope/HuggingFace 本地缓存探测或国内高速拉取"""
    # 1. 直接指定本地目录
    if _is_valid_model_dir(model_name):
        return model_name

    safe_name = model_name.replace("/", "--")
    ms_model_id = MODELSCOPE_MODEL_MAP.get(model_name, model_name)
    ms_safe_name = ms_model_id.replace("/", "--")

    # 2. 深度穿透探测 ModelScope 本地缓存目录 (~/.cache/modelscope/models/...)
    ms_roots = [
        os.environ.get("MODELSCOPE_CACHE", ""),
        os.path.expanduser("~/.cache/modelscope/models"),
        os.path.expanduser("~/.cache/modelscope/hub"),
        "data/models",
        "data/models/modelscope",
    ]
    for ms_root in ms_roots:
        if not ms_root or not os.path.exists(ms_root):
            continue
        # 匹配 snapshots/* 目录
        possible_ms_dirs = [
            os.path.join(ms_root, ms_safe_name),
            os.path.join(ms_root, ms_model_id),
            os.path.join(ms_root, ms_safe_name, "snapshots", "master"),
        ]
        for p_dir in possible_ms_dirs:
            if _is_valid_model_dir(p_dir):
                return p_dir

        snapshots_dir = os.path.join(ms_root, ms_safe_name, "snapshots")
        if os.path.exists(snapshots_dir):
            snaps = [s for s in glob.glob(os.path.join(snapshots_dir, "*")) if _is_valid_model_dir(s)]
            if snaps:
                return sorted(snaps, key=os.path.getmtime, reverse=True)[0]

    # 3. 深度穿透探测 Hugging Face 本地快照目录 (支持 default_cache_path / TRANSFORMERS_CACHE / 自定义盘符)
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

    for root in possible_roots:
        if not root or not os.path.exists(root):
            continue
        model_dir = os.path.join(root, f"models--{safe_name}")
        if os.path.exists(model_dir):
            snapshots_dir = os.path.join(model_dir, "snapshots")
            if os.path.exists(snapshots_dir):
                snaps = [s for s in glob.glob(os.path.join(snapshots_dir, "*")) if _is_valid_model_dir(s)]
                if snaps:
                    latest_snap = sorted(snaps, key=os.path.getmtime, reverse=True)[0]
                    return latest_snap
            if _is_valid_model_dir(model_dir):
                return model_dir

    # 4. 若本地未命中，国内环境优先调用 ModelScope 官方高速源下载
    if prefer_modelscope:
        try:
            try:
                import modelscope
            except ImportError:
                import subprocess, sys
                logger.info("正在自动安装 modelscope 国内依赖包 (清华镜像)...")
                subprocess.call([sys.executable, "-m", "pip", "install", "modelscope>=1.15.0", "-i", "https://pypi.tuna.tsinghua.edu.cn/simple", "--quiet"])

            from modelscope.hub.snapshot_download import snapshot_download
            logger.info(f"正在通过 ModelScope (魔搭社区) 高速载入模型: {ms_model_id} (预计 1~2 分钟)...")
            local_dir = snapshot_download(ms_model_id)
            if _is_valid_model_dir(local_dir):
                logger.info(f"ModelScope 官方模型载入就绪: {local_dir}")
                return local_dir
        except Exception as e:
            logger.warning(f"ModelScope 下载出现异常 ({e})，尝试切换至 HuggingFace 国内镜像源")

    # 5. 配置国内镜像源加速 HuggingFace 原生下载 (hf-mirror.com)
    setup_download_mirrors()
    return model_name


def check_models_ready() -> bool:
    """核验系统运行所需的 BAAI 深度模型 (bge-m3, bge-reranker-v2-m3) 是否均已完整就绪"""
    for m in ["BAAI/bge-m3", "BAAI/bge-reranker-v2-m3"]:
        path = resolve_model_path(m, prefer_modelscope=False)
        if not _is_valid_model_dir(path):
            return False
    return True


def load_sentence_transformer(model_name: str, device: str) -> Any:
    """安全加载 Dense 语义向量模型 (SentenceTransformer)"""
    from sentence_transformers import SentenceTransformer
    resolved_path = resolve_model_path(model_name, prefer_modelscope=True)
    if os.path.isdir(resolved_path):
        return SentenceTransformer(resolved_path, device=device)
    try:
        return SentenceTransformer(resolved_path, device=device, local_files_only=True)
    except Exception:
        setup_download_mirrors()
        return SentenceTransformer(resolved_path, device=device)


def load_cross_encoder(model_name: str, max_length: int = 512, device: str = "cpu") -> Any:
    """安全加载 Cross-Encoder 深度交互重排模型 (CrossEncoder)"""
    from sentence_transformers import CrossEncoder
    resolved_path = resolve_model_path(model_name, prefer_modelscope=True)
    if os.path.isdir(resolved_path):
        return CrossEncoder(resolved_path, max_length=max_length, device=device)
    try:
        return CrossEncoder(resolved_path, max_length=max_length, device=device, local_files_only=True)
    except Exception:
        setup_download_mirrors()
        return CrossEncoder(resolved_path, max_length=max_length, device=device)
