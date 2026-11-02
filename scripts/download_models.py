"""BAAI 深度模型高速预下载器 (ModelScope 国内官方源保障)
支持一键预载入:
1. BAAI/bge-m3 (多语言稠密语义向量计算模型)
2. BAAI/bge-reranker-v2-m3 (Cross-Encoder 跨语言交互重排模型)

面向中国大陆地区开发者与本地化部署优化，全量优先直连阿里云魔搭社区 (ModelScope) 高速 CDN。
"""

import os
import sys
import time
import logging

# 确保在 Windows 控制台环境下支持 UTF-8 打印
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("download_models")

# 确保项目根目录在 sys.path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from lawagent.store.models_loader import (
    resolve_model_path,
    check_models_ready,
    MODELSCOPE_MODEL_MAP
)


def ensure_modelscope_installed():
    """检测并自动尝试安装 modelscope"""
    try:
        import modelscope
        return True
    except ImportError:
        logger.info("未检测到 modelscope 库，尝试自动通过国内镜像源安装...")
        import subprocess
        cmd = [sys.executable, "-m", "pip", "install", "modelscope>=1.15.0", "-i", "https://pypi.tuna.tsinghua.edu.cn/simple"]
        ret = subprocess.call(cmd)
        return ret == 0


def download_model(model_name: str) -> str:
    """通过 ModelScope 下载指定模型并返回本地路径"""
    logger.info(f"正在检查/下载模型: {model_name} ...")
    start_t = time.time()
    
    # 首先检查是否已经存在本地有效缓存
    existing_path = resolve_model_path(model_name, prefer_modelscope=False)
    if os.path.isdir(existing_path) and any(
        os.path.exists(os.path.join(existing_path, f))
        for f in ["model.safetensors", "pytorch_model.bin", "model.bin"]
    ):
        logger.info(f"[OK] 本地已存在完整模型权重: {existing_path}")
        return existing_path

    # 通过 ModelScope 高速下载
    if not ensure_modelscope_installed():
        raise RuntimeError("无法安装或导入 modelscope，请手动执行: pip install modelscope")

    from modelscope.hub.snapshot_download import snapshot_download
    ms_id = MODELSCOPE_MODEL_MAP.get(model_name, model_name)
    logger.info(f"正在通过 ModelScope (魔搭社区) 高速拉取权重: {ms_id} (预计 1~2 分钟)...")
    local_dir = snapshot_download(ms_id)
    elapsed = time.time() - start_t
    logger.info(f"[OK] 模型 {model_name} 下载就绪: {local_dir} (耗时: {elapsed:.1f}s)")
    return local_dir


def main():
    print("=" * 70)
    print("      东盟域外法查明助手 - BAAI 深度模型 ModelScope 国内高速初始化")
    print("=" * 70)
    print("提示: 系统稠密向量检索与 Cross-Encoder 深度重排依赖以下两个核心模型:")
    print("  1. BAAI/bge-m3 (约 2.2GB)")
    print("  2. BAAI/bge-reranker-v2-m3 (约 2.2GB)")
    print("全量优先接入阿里云魔搭社区 (ModelScope)，支持断点续传与国内高带宽。\n")

    models = ["BAAI/bge-m3", "BAAI/bge-reranker-v2-m3"]
    all_success = True

    for m in models:
        try:
            p = download_model(m)
            print(f"[OK] {m} -> {p}\n")
        except Exception as e:
            logger.error(f"[FAIL] 模型 {m} 下载失败: {e}\n")
            all_success = False

    if all_success:
        print("=" * 70)
        print("[SUCCESS] 全部 BAAI 深度模型均已就绪！系统稠密检索与重排功能已完整可用。")
        print("=" * 70)
        return 0
    else:
        print("=" * 70)
        print("[WARNING] 部分模型未完成下载。您可以稍后重新运行此脚本重试。")
        print("=" * 70)
        return 1


if __name__ == "__main__":
    sys.exit(main())
