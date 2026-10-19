"""德国法律规范与联邦法院判例全文检索路由 (Search Router)
对齐前端 NormOrCaseItem 契约与技术方案第 4.4 节
"""

from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from lawagent.api.deps import get_snapshot_mgr, get_retriever
from lawagent.store.snapshots import SnapshotManager
from lawagent.store.retriever import HybridRetriever

router = APIRouter(prefix="/search", tags=["search"])


class NormOrCaseItem(BaseModel):
    id: str
    kind: str
    law: Optional[str] = None
    enbez: Optional[str] = None
    title: str = ""
    heading_path: Optional[str] = None
    court: Optional[str] = None
    decided: Optional[str] = None
    az: Optional[str] = None
    text_de: str = ""
    text_original: Optional[str] = None
    text_en: Optional[str] = None
    text_zh: Optional[str] = None
    text_zh_machine: str = ""
    language_mode: Optional[str] = "bilingual"
    translation_source: Optional[str] = "MOJ_FATONG_2026"
    fidic_tier: Optional[str] = None
    fidic_edition: Optional[str] = None
    stand: Optional[str] = None
    has_pending_amend: Optional[bool] = False
    source_url: str = ""


@router.get("", response_model=List[NormOrCaseItem])
def search_norms_and_cases(
    q: str = Query("", description="搜索关键词、条号或案号"),
    law: Optional[str] = Query(None, description="法典或机构过滤，如 FIDIC, CIPAA, UU_2_2017"),
    court: Optional[str] = Query(None, description="法院/仲裁庭过滤，如 SGHC, BANI, AIAC"),
    kind: Optional[str] = Query("all", description="类型过滤: all, norm, case"),
    snapshot_mgr: SnapshotManager = Depends(get_snapshot_mgr),
    retriever: HybridRetriever = Depends(get_retriever)
):
    """搜索东盟六国成文法典、FIDIC 国际工程标准条款与司法判例先例"""
    query = q.strip()
    items: List[NormOrCaseItem] = []

    # 1. 当问句为空时，提供核心东盟成文法条与金标准裁判先例
    if not query:
        conn = snapshot_mgr.get_connection()
        if law and conn:
            cursor = conn.cursor()
            if kind != "case":
                cursor.execute("SELECT norm_id FROM norms WHERE law = ? LIMIT 25", (law,))
                for row in cursor.fetchall():
                    norm = snapshot_mgr.norm_lookup(row[0])
                    if norm:
                        items.append(NormOrCaseItem(
                            id=norm["norm_id"],
                            kind="norm",
                            law=norm["law"],
                            enbez=norm["enbez"],
                            title=norm["title"] or f"{norm['law']} {norm['enbez']}",
                            heading_path=norm.get("heading_path"),
                            text_de=norm.get("text_zh") or norm["text_de"][:1500],
                            text_original=norm.get("text_original"),
                            text_en=norm.get("text_en"),
                            text_zh=norm.get("text_zh"),
                            text_zh_machine=norm.get("text_zh") or f"【释义】针对 {norm['norm_id']} 之法定要件",
                            language_mode=norm.get("language_mode", "bilingual"),
                            translation_source=norm.get("translation_source", "MOJ_FATONG_2026"),
                            fidic_tier=norm.get("fidic_tier"),
                            fidic_edition=norm.get("fidic_edition"),
                            stand=norm.get("stand"),
                            has_pending_amend=bool(norm.get("has_pending_amend")),
                            source_url=norm["source_url"]
                        ))
            if kind != "norm":
                cursor.execute("SELECT case_id FROM cases WHERE court LIKE ? OR case_id LIKE ? LIMIT 10", (f"%{law}%", f"%{law}%"))
                for row in cursor.fetchall():
                    case_data = snapshot_mgr.case_lookup(row[0])
                    if case_data:
                        items.append(NormOrCaseItem(
                            id=case_data["case_id"],
                            kind="case",
                            court=case_data["court"],
                            az=case_data["az"],
                            decided=case_data["decided"],
                            title=f"{case_data['court']} {case_data['az']} ({case_data['decided']})",
                            text_de=case_data.get("leitsatz") or (case_data.get("gruende") or "")[:1500],
                            text_original=case_data.get("gruende"),
                            text_en=case_data.get("tenor"),
                            text_zh=case_data.get("leitsatz"),
                            text_zh_machine=f"【裁判要旨】{case_data['court']} 司法裁判要旨",
                            source_url=case_data["source_url"]
                        ))
            return items

        # 未指定特定法典时，默认返回东盟 6 国核心法条与 FIDIC 国际工程标准条款
        core_norms = [
            "ID:UU_2_2017:Art57", "ID:SEMA_3_2023", "ID:MEMR_11_2024", "ID:KUHPerdata:Art1338",
            "VN:Law_135_2025:Art86.2", "VN:Law_135_2025:Art146", "VN:Decree_210_2026:Art18",
            "MY:CIPAA_2012:Sec35", "MY:CIPAA_2012:Sec13", "MY:Act_520_CIDB:Sec25",
            "SG:SOPA_2004:Sec9", "SG:Precedent:BS_Mount_Sophia", "SG:Precedent:JBE_Properties",
            "TH:CCC:Sec596", "TH:FBA_1999:List3",
            "PH:RA_11966:Sec18", "PH:Precedent:PCAB_v_Manila_Water",
            "FIDIC:Silver_1999:Clause_20.1", "FIDIC:Silver_1999:Clause_8.4", "FIDIC:Silver_1999:Clause_4.2", "FIDIC:Silver_1999:Clause_13.7",
            "CN:SASAC_Order_35:Art12", "CN:Data_Security_Law:Art36",
            "TREATY:CN_ID_BIT_1992:Art4", "SINOSURE:Overseas_Policy:Art15"
        ]
        if kind != "case":
            for cid in core_norms:
                norm = snapshot_mgr.norm_lookup(cid)
                if norm:
                    items.append(NormOrCaseItem(
                        id=norm["norm_id"],
                        kind="norm",
                        law=norm["law"],
                        enbez=norm["enbez"],
                        title=norm["title"] or f"{norm['law']} {norm['enbez']}",
                        heading_path=norm.get("heading_path"),
                        text_de=norm.get("text_zh") or norm["text_de"][:1500],
                        text_original=norm.get("text_original"),
                        text_en=norm.get("text_en"),
                        text_zh=norm.get("text_zh"),
                        text_zh_machine=norm.get("text_zh") or f"【释义】针对 {norm['norm_id']} 之法定要件",
                        language_mode=norm.get("language_mode", "bilingual"),
                        translation_source=norm.get("translation_source", "MOJ_FATONG_2026"),
                        fidic_tier=norm.get("fidic_tier"),
                        fidic_edition=norm.get("fidic_edition"),
                        stand=norm.get("stand"),
                        has_pending_amend=bool(norm.get("has_pending_amend")),
                        source_url=norm["source_url"]
                    ))

        if kind != "norm":
            core_cases = [
                "CASE:SG_HC:BSMountSophia:2016",
                "CASE:SG_CA:JBEProperties:2011",
                "CASE:ID_MA:SEMA_3_2023:2023",
                "CASE:PH_SC:G.R.217590_ManilaWater:2020",
                "CASE:MY_FC:Bauer_CIPAA_Sec35:2019",
                "CASE:VN_SPC:ArbitrationEnforcement:2021",
                "CASE:TH_SAC:HopewellConcession:2022"
            ]
            for case_id in core_cases:
                case_data = snapshot_mgr.case_lookup(case_id)
                if case_data:
                    items.append(NormOrCaseItem(
                        id=case_data["case_id"],
                        kind="case",
                        court=case_data["court"],
                        az=case_data["az"],
                        decided=case_data["decided"],
                        title=f"{case_data['court']} {case_data['az']} ({case_data['decided']})",
                        text_de=case_data.get("leitsatz") or (case_data.get("gruende") or "")[:1500],
                        text_original=case_data.get("gruende"),
                        text_en=case_data.get("tenor"),
                        text_zh=case_data.get("leitsatz"),
                        text_zh_machine=f"【裁判要旨】{case_data['court']} 司法裁判要旨",
                        source_url=case_data["source_url"]
                    ))
        return items

    # 2. 混合检索召回
    kind_filter = kind if kind in ("norm", "case") else None
    evidences = retriever.search(query, top_k=20, law_filter=law, kind_filter=kind_filter)

    for ev in evidences:
        if ev.kind == "norm":
            norm = snapshot_mgr.norm_lookup(ev.ref_id)
            if norm:
                items.append(NormOrCaseItem(
                    id=norm["norm_id"],
                    kind="norm",
                    law=norm["law"],
                    enbez=norm["enbez"],
                    title=norm["title"] or f"{norm['law']} {norm['enbez']}",
                    heading_path=norm.get("heading_path"),
                    text_de=norm.get("text_zh") or norm["text_de"][:1500],
                    text_original=norm.get("text_original"),
                    text_en=norm.get("text_en"),
                    text_zh=norm.get("text_zh"),
                    text_zh_machine=norm.get("text_zh") or f"【释义】针对 {norm['norm_id']} 之法定要件",
                    language_mode=norm.get("language_mode", "bilingual"),
                    translation_source=norm.get("translation_source", "MOJ_FATONG_2026"),
                    fidic_tier=norm.get("fidic_tier"),
                    fidic_edition=norm.get("fidic_edition"),
                    stand=norm.get("stand"),
                    has_pending_amend=bool(norm.get("has_pending_amend")),
                    source_url=norm["source_url"]
                ))
        else:
            case_data = snapshot_mgr.case_lookup(ev.ref_id)
            if case_data:
                items.append(NormOrCaseItem(
                    id=case_data["case_id"],
                    kind="case",
                    court=case_data["court"],
                    az=case_data["az"],
                    decided=case_data["decided"],
                    title=f"{case_data['court']} {case_data['az']} ({case_data['decided']})",
                    text_de=case_data.get("leitsatz") or (case_data.get("gruende") or "")[:1500],
                    text_original=case_data.get("gruende"),
                    text_en=case_data.get("tenor"),
                    text_zh=case_data.get("leitsatz"),
                    text_zh_machine=f"【裁判要旨】{case_data['court']} 建设工程裁判要旨",
                    source_url=case_data["source_url"]
                ))

    return items
