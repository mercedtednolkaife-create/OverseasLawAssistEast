"""阶段 8 单元测试套件 (Phase 8 ASEAN Knowledge Base & Legal GraphRAG Tests)
测试覆盖：
1. 快照库 Schema 升级验证：norms 11 项扩展字段与 risk_communities 表完整性
2. 东盟 6 国 2026 现行有效法源精确检索与三语/双语对齐验证 (SEMA 3/2023, Law 135/2025, CIPAA Sec 35等)
3. FIDIC 银皮书/黄皮书/红皮书 Tier 1 核心争议条款与 Tier 2 基线条款分级区分
4. 央国企国家安全红线与条约保全法源 (国资委35号令第12条, 数据安全法第36条, 中信保30日报损)
5. 三层 Legal GraphRAG 关系图谱与拓扑边遍历 (edges & edges_top)
6. 混合检索召回器对东盟工程条文与 FIDIC 规则的精准召回验证
"""

import pytest
import sqlite3
import json
import os

from lawagent.store.snapshots import SnapshotManager
from lawagent.store.graph import SQLiteGraphStore
from lawagent.store.retriever import HybridRetriever


@pytest.fixture(scope="module")
def snapshot_mgr():
    return SnapshotManager()


@pytest.fixture(scope="module")
def current_snap_id(snapshot_mgr):
    return snapshot_mgr.get_current_snapshot_id()


@pytest.fixture(scope="module")
def db_conn(snapshot_mgr, current_snap_id):
    conn = snapshot_mgr.get_connection(current_snap_id)
    assert conn is not None
    return conn


def test_phase8_schema_and_risk_communities(db_conn):
    """测试 1: 快照库 Schema 升级字段与风险社区表验证"""
    cur = db_conn.cursor()

    # 验证 norms 表包含东盟与 FIDIC 扩展字段
    cur.execute("PRAGMA table_info(norms)")
    columns = [col["name"] for col in cur.fetchall()]
    expected_cols = [
        "language_mode", "lang_original", "text_original", "text_en", "text_zh",
        "translation_source", "norm_category", "fidic_tier", "fidic_edition",
        "elements_json", "mandatory_level"
    ]
    for col in expected_cols:
        assert col in columns, f"norms 表缺少扩展字段: {col}"

    # 验证 risk_communities 表
    cur.execute("SELECT community_id, name_zh, risk_level, host_countries FROM risk_communities")
    rc_rows = cur.fetchall()
    assert len(rc_rows) >= 6
    rc_ids = [r["community_id"] for r in rc_rows]
    assert "RC_TKDN" in rc_ids
    assert "RC_BOND_FRAUD" in rc_ids
    assert "RC_EXPROPRIATION" in rc_ids
    assert "RC_LANGUAGE_VALIDITY" in rc_ids
    assert "RC_EOT_BAR" in rc_ids
    assert "RC_CROSS_BORDER_DATA" in rc_ids


def test_asean_six_countries_2026_statutes_lookup(snapshot_mgr):
    """测试 2: 东盟6国2026现行有效法源精确检索与双语/三语文本完整性"""
    # 1. 印度尼西亚：SEMA 3/2023 (三语模式)
    id_norm = snapshot_mgr.norm_lookup("ID:SEMA_3_2023")
    assert id_norm is not None
    assert id_norm["language_mode"] == "trilingual"
    assert id_norm["lang_original"] == "id"
    assert "iktikad tidak baik" in id_norm["text_original"]
    assert "bad faith" in id_norm["text_en"]
    assert "司法部法通网权威译本" in id_norm["text_zh"]
    assert id_norm["translation_source"] == "MOJ_FATONG_2026"

    # 2. 越南：2025新建设法第86.2条 (三语模式)
    vn_norm = snapshot_mgr.norm_lookup("VN:Law_135_2025:Art86.2")
    assert vn_norm is not None
    assert vn_norm["language_mode"] == "trilingual"
    assert vn_norm["lang_original"] == "vi"
    assert "liquidated damages" in vn_norm["text_original"].lower()
    assert "预定损害赔偿" in vn_norm["text_zh"]
    assert "12%" in vn_norm["text_zh"]

    # 3. 马来西亚：CIPAA 2012 第35条 (双语模式)
    my_norm = snapshot_mgr.norm_lookup("MY:CIPAA_2012:Sec35")
    assert my_norm is not None
    assert my_norm["language_mode"] == "bilingual"
    assert my_norm["mandatory_level"] == "mandatory_override"
    assert "Prohibition of conditional payment" in my_norm["text_original"]
    assert "背靠背" in my_norm["text_zh"]
    assert "自始绝对无效" in my_norm["text_zh"]

    # 4. 新加坡：SOPA 2004 第9条 (双语模式)
    sg_norm = snapshot_mgr.norm_lookup("SG:SOPA_2004:Sec9")
    assert sg_norm is not None
    assert "pay-when-paid provision" in sg_norm["text_original"]
    assert "7 至 14 天" in sg_norm["text_zh"]

    # 5. 菲律宾：RA 11966 新PPP法典第18条 (双语模式)
    ph_norm = snapshot_mgr.norm_lookup("PH:RA_11966:Sec18")
    assert ph_norm is not None
    assert "Republic Act No. 7718, is hereby repealed" in ph_norm["text_original"]
    assert "废除实施三十余年的旧 BOT 法案" in ph_norm["text_zh"]

    # 6. 泰国：外商经营法 FBA 附表三 (三语模式)
    th_norm = snapshot_mgr.norm_lookup("TH:FBA_1999:List3")
    assert th_norm is not None
    assert th_norm["language_mode"] == "trilingual"
    assert "Nominee" in th_norm["text_original"]
    assert "49%" in th_norm["text_zh"]
    assert "代持股权" in th_norm["text_zh"]


def test_fidic_tiers_differentiation(snapshot_mgr):
    """测试 3: FIDIC 银皮书 Tier 1 核心争议条款与 Tier 2 基线条款分级区分"""
    # Tier 1 核心争议条款: Clause 20.1 (承包商索赔失权)
    cl20_1 = snapshot_mgr.norm_lookup("FIDIC:Silver_1999:Clause_20.1")
    assert cl20_1 is not None
    assert cl20_1["fidic_tier"] == "core_dispute"
    assert cl20_1["fidic_edition"] == "1999_SILVER"
    assert "28 days" in cl20_1["text_original"]
    assert "除斥期间" in cl20_1["text_zh"] or "28 天" in cl20_1["text_zh"]

    # Tier 1 核心争议条款: Clause 8.4 (工期顺延 EOT)
    cl8_4 = snapshot_mgr.norm_lookup("FIDIC:Silver_1999:Clause_8.4")
    assert cl8_4 is not None
    assert cl8_4["fidic_tier"] == "core_dispute"

    # Tier 1 核心争议条款: Clause 4.2 (履约保函索兑限制)
    cl4_2 = snapshot_mgr.norm_lookup("FIDIC:Silver_1999:Clause_4.2")
    assert cl4_2 is not None
    assert cl4_2["fidic_tier"] == "core_dispute"

    # Tier 2 基线参考条款: Clause 13.7 (法律变更调价)
    cl13_7 = snapshot_mgr.norm_lookup("FIDIC:Silver_1999:Clause_13.7")
    assert cl13_7 is not None
    assert cl13_7["fidic_tier"] == "baseline_reference"


def test_prc_security_regulations_and_treaties(snapshot_mgr):
    """测试 4: 央国企国家安全红线、BIT 投资条约与中信保 30 日报损条款"""
    # 国资委35号令第12条
    sasac12 = snapshot_mgr.norm_lookup("CN:SASAC_Order_35:Art12")
    assert "负面清单" in sasac12["text_original"]
    assert "国资监管红线" in sasac12["text_zh"]

    # 数据安全法第36条
    dsl36 = snapshot_mgr.norm_lookup("CN:Data_Security_Law:Art36")
    assert dsl36 is not None
    assert dsl36["norm_category"] == "prc_sasac_reg"
    assert "外国司法或者执法机构" in dsl36["text_original"]
    assert "数据出境安全评估" in dsl36["text_zh"]

    # 中国-印尼双边投资保护协定第4条
    bit_id = snapshot_mgr.norm_lookup("TREATY:CN_ID_BIT_1992:Art4")
    assert bit_id is not None
    assert bit_id["norm_category"] == "bit_treaty"
    assert "expropriate" in bit_id["text_original"]
    assert "征收" in bit_id["text_zh"]

    # 中信保30日报损条款
    sinosure15 = snapshot_mgr.norm_lookup("SINOSURE:Overseas_Policy:Art15")
    assert sinosure15 is not None
    assert "三十（30）日" in sinosure15["text_original"]
    assert "可能损失通知书" in sinosure15["text_zh"]


def test_legal_graphrag_three_layer_edges(db_conn):
    """测试 5: 三层 Legal GraphRAG 关系图谱与拓扑边遍历"""
    graph_store = SQLiteGraphStore(db_conn)

    # 1. 冲突边 (conflicts_with): CIPAA 第35条否定 FIDIC 背靠背条款
    cipaa_neighbors = graph_store.neighbors("MY:CIPAA_2012:Sec35", rels=["conflicts_with"])
    assert len(cipaa_neighbors) >= 1
    assert any("FIDIC:Silver_1999:Clause_14.8" in n["node"] for n in cipaa_neighbors)

    # 2. 解释边 (interprets): SEMA 3/2023 限制印尼语言法无效抗辩
    sema_neighbors = graph_store.neighbors("ID:SEMA_3_2023", rels=["interprets"])
    assert len(sema_neighbors) >= 1
    assert any("ID:UU_2_2017:Art57" in n["node"] for n in sema_neighbors)

    # 3. 保全联动边 (triggers_preservation): BIT 征收联动中信保 30 日报损
    bit_neighbors = graph_store.neighbors("TREATY:CN_ID_BIT_1992:Art4", rels=["triggers_preservation"])
    assert len(bit_neighbors) >= 1
    assert any("SINOSURE:Overseas_Policy:Art15" in n["node"] for n in bit_neighbors)

    # 4. 强制覆盖边 (overrides): 2025新建设法覆盖旧罚金上限法令
    vn_neighbors = graph_store.neighbors("VN:Law_135_2025:Art86.2", rels=["overrides"])
    assert len(vn_neighbors) >= 1
    assert any("VN:Decree_210_2026:Art18" in n["node"] for n in vn_neighbors)


def test_hybrid_retriever_exact_asean_recall():
    """测试 6: 混合检索召回器对东盟工程条文与 FIDIC 规则的精准召回验证"""
    retriever = HybridRetriever.from_snapshot()

    # 精确条文通道识别: FIDIC 20.1
    res_fidic = retriever.search("承包商延误工期索赔通知依 FIDIC Clause 20.1 是否失权")
    assert len(res_fidic) > 0
    ref_ids = [ev.ref_id for ev in res_fidic]
    assert any("FIDIC:Silver_1999:Clause_20.1" in ref for ref in ref_ids)

    # 精确条文通道识别: CIPAA 35 背靠背
    res_cipaa = retriever.search("马来西亚工程款追索根据 CIPAA Sec 35 背靠背付款条款效力")
    assert len(res_cipaa) > 0
    ref_ids_cipaa = [ev.ref_id for ev in res_cipaa]
    assert any("MY:CIPAA_2012:Sec35" in ref for ref in ref_ids_cipaa)
