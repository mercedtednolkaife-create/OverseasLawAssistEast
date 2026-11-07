"""FastAPI 主应用入口 (Main Application)
挂载 CORS 中间件、业务路由子模块与应用生命周期钩子
"""

import os
import logging
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 设置底层环境参数，避免 PyTorch 与 FAISS 在 AMD CPU / 多运行时下 OpenMP 冲突与无限制占满核心
os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")
os.environ.setdefault("OMP_NUM_THREADS", "4")
os.environ.setdefault("MKL_NUM_THREADS", "4")

try:
    import torch
    if not torch.cuda.is_available():
        torch.set_num_threads(min(4, os.cpu_count() or 4))
        try:
            torch.set_num_interop_threads(1)
        except RuntimeError:
            pass
except ImportError:
    pass

logger = logging.getLogger(__name__)

from lawagent.api.routes import cases, search, verify, consults, compliance
from lawagent.store.db import StateDBManager
from lawagent.store.snapshots import SnapshotManager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 初始化数据表并播种东盟示范案例
    db = StateDBManager.get_instance()
    db.list_experts()  # 触发专家名录自动播种
    from scripts.seed_asean_cases import seed_asean_demo_cases
    seed_asean_demo_cases(db)

    # 检索单例与深度模型预热（异步后台线程执行，确保 Port 8000 立即处于监听就绪状态且不阻塞事件循环）
    if not os.environ.get("PYTEST_CURRENT_TEST"):
        async def _async_warmup_and_heal():
            try:
                from lawagent.api.deps import get_retriever
                retriever = get_retriever()
                logger.info("系统启动预热: 执行后台微型跨层检索与重排预热...")
                await asyncio.to_thread(retriever.search, "ASEAN construction contract dispute", top_k=1)
                logger.info("系统启动预热完成: 检索索引与深度模型已就绪")
            except Exception as e:
                logger.warning("系统启动检索预热跳过: %s", e)

            # 预热完毕后再执行启动自愈机制：检查并断点续推未完成的后台案件
            try:
                from lawagent.api.deps import get_workflow_runner
                from lawagent.api.routes.cases import _run_workflow_background
                runner = get_workflow_runner()
                cases_list = db.list_cases()
                for c in cases_list:
                    if c.status == "running":
                        logger.info("系统启动自愈: 发现未完成案件 %s，从断点自动续推...", c.case_id)
                        asyncio.create_task(_run_workflow_background(c.case_id, db, runner))
            except Exception as e:
                logger.warning("系统启动自愈检查发生异常: %s", e)

        asyncio.create_task(_async_warmup_and_heal())

    yield


app = FastAPI(
    title="澜衡智枢-域外法查明助手 (Lanheng SmartHub - Overseas Law Assist Agent)",
    description="澜衡智枢-域外法查明助手：聚焦算电协同与海外基建投资合规、涉外法查明、证据链溯源与双向合规审查",
    version="1.0.0",
    lifespan=lifespan
)

# 配置全局跨域访问 (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载 API 子路由 (同时挂载 /api 与根路由以适配各种代理环境)
app.include_router(cases.router, prefix="/api")
app.include_router(search.router, prefix="/api")
app.include_router(verify.router, prefix="/api")
app.include_router(consults.router, prefix="/api")
app.include_router(compliance.router, prefix="/api")

# (已移除根路径重复挂载，API 统一收敛至 /api 前缀以对齐规范)


@app.get("/api/health")
@app.get("/health")
def healthcheck():
    return {"status": "ok", "service": "lawagent.api", "version": "1.0.0"}


@app.get("/api/jurisdictions")
@app.get("/jurisdictions")
def get_jurisdictions(active_only: bool = True):
    """获取支持的法域元数据列表（默认仅返回活跃推荐法域）"""
    from lawagent.core.jurisdiction import JurisdictionRegistry
    items = JurisdictionRegistry.list_jurisdictions(active_only=active_only)
    return [
        {
            "code": j.code,
            "name_zh": j.name_zh,
            "primary_language": j.primary_language,
            "citation_standard": j.citation_standard,
            "default_laws": j.default_laws,
            "is_active": j.is_active,
            "flag": j.flag,
            "region": j.region,
            "language_mode": j.language_mode,
            "description_zh": j.description_zh,
        }
        for j in items
    ]
