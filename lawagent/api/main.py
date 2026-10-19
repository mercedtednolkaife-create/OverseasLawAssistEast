"""FastAPI 主应用入口 (Main Application)
挂载 CORS 中间件、业务路由子模块与应用生命周期钩子
"""

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from lawagent.api.routes import cases, search, verify, consults
from lawagent.store.db import StateDBManager
from lawagent.store.snapshots import SnapshotManager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 初始化数据表并播种东盟示范案例
    db = StateDBManager.get_instance()
    db.list_experts()  # 触发专家名录自动播种
    from scripts.seed_asean_cases import seed_asean_demo_cases
    seed_asean_demo_cases(db)
    yield


app = FastAPI(
    title="涉外法查明Agent (Overseas Law Assist Agent - ASEAN Engineering)",
    description="涉外法查明助手：聚焦中国出海基建央国企东盟建设工程合规与风险防范，证据链溯源与客观中立咨询防线",
    version="1.0.0",
    lifespan=lifespan
)

# 配置全局跨域访问 (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载 API 子路由 (同时挂载 /api 与根路由以适配各种代理环境)
app.include_router(cases.router, prefix="/api")
app.include_router(search.router, prefix="/api")
app.include_router(verify.router, prefix="/api")
app.include_router(consults.router, prefix="/api")

app.include_router(cases.router)
app.include_router(search.router)
app.include_router(verify.router)
app.include_router(consults.router)


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
