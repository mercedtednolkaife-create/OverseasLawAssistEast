"""FastAPI 依赖注入与服务单例管理 (Dependencies)
"""

from typing import Optional, TYPE_CHECKING, Any
from lawagent.store.db import StateDBManager
from lawagent.store.snapshots import SnapshotManager

if TYPE_CHECKING:
    from lawagent.store.retriever import HybridRetriever
    from lawagent.flow.graph import LawWorkflowRunner

_state_db: Optional[StateDBManager] = None
_snapshot_mgr: Optional[SnapshotManager] = None
_retriever: Optional[Any] = None
_runner: Optional[Any] = None


def get_state_db() -> StateDBManager:
    global _state_db
    if _state_db is None:
        _state_db = StateDBManager.get_instance()
    return _state_db


def get_snapshot_mgr() -> SnapshotManager:
    global _snapshot_mgr
    if _snapshot_mgr is None:
        _snapshot_mgr = SnapshotManager()
    return _snapshot_mgr


def get_retriever():
    global _retriever
    if _retriever is None:
        from lawagent.store.retriever import HybridRetriever
        _retriever = HybridRetriever.from_snapshot()
    return _retriever


def get_workflow_runner():
    global _runner
    if _runner is None:
        from lawagent.flow.graph import LawWorkflowRunner
        _runner = LawWorkflowRunner()
    return _runner
