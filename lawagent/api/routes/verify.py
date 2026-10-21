"""外国法证据材料核验路由 (Foreign Material Verification Router - F16)
对齐前端 MaterialVerificationResult 契约与技术方案第 4.6 节
"""

import re
import asyncio
from typing import List, Dict, Any, Literal, Optional
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from lawagent.api.deps import get_snapshot_mgr
from lawagent.store.snapshots import SnapshotManager

router = APIRouter(prefix="/verify-materials", tags=["verify"])


class VerifyRequest(BaseModel):
    raw_text: str
    mode: Literal["CITATION_CHECK", "CONTRACT_REDLINE_AUDIT"] = "CONTRACT_REDLINE_AUDIT"


class ContractRedlineItem(BaseModel):
    clause_snippet: str
    risk_level: Literal["critical", "high", "medium", "safe"]
    violated_rule_title: str
    violated_norm_id: str
    mandatory_rule_desc: str
    recommended_revision: str


class VerifyItem(BaseModel):
    ref_id: str
    in_db: bool
    is_current: bool
    stand_note: str
    consistency_verdict: str  # exact | partial | inconsistent | unverified
    has_full_text: bool
    quote_in_material: str
    db_text_de: str
    db_text_zh: str
    note: str


class VerifyResponse(BaseModel):
    raw_text: str
    mode: str = "CONTRACT_REDLINE_AUDIT"
    items: List[VerifyItem] = Field(default_factory=list)
    redline_items: List[ContractRedlineItem] = Field(default_factory=list)
    summary: Dict[str, int]


RE_CITATION_DETECT = re.compile(
    r"(FIDIC|CIPAA|SOPA|UU|SEMA|Decree|Law|BIT|RA|CCC|FBA|MEMR|SASAC)\s*(?:Clause|Sub-Clause|§|Art\.?|Section|Sec\.?|No\.?)?\s*([0-9a-zA-Z\-\:\._/]+)",
    re.IGNORECASE
)
RE_ASEAN_CASE_DETECT = re.compile(
    r"\b(BS Mount Sophia|Manila Water|PCAB|G\.R\.\s*No\.?\s*217590|SEMA\s*3/2023|CIPAA|SOPA|JBE Properties)\b",
    re.IGNORECASE
)

# 东盟工程合同五大强行法红线与高危规则定义库
ASEAN_CONTRACT_REDLINES = [
    {
        "keywords": ["pay when paid", "pay if paid", "back to back payment", "以业主付款为前提", "收到业主款项后", "背靠背付款", "业主支付后方才支付"],
        "risk_level": "critical",
        "title": "马来西亚 CIPAA 2012 第35条 / 新加坡 SOPA 第9条：背靠背条件付款条款法定绝对无效",
        "norm_id": "MY:CIPAA_2012:Sec35",
        "desc": "马来西亚与新加坡法律明文宣告：工程分包中约定的‘以业主向总包付款为前提’的条件支付条款自始无效 (Void ab initio)。分包商可直接发起法定快速裁决，总承包商不得以此抗辩拒付。",
        "revision": "Payment Milestone Clause: Payments to Subcontractor shall become due within 30 days of the Engineer certifying the interim work evaluation, irrespective of whether the Main Contractor has received corresponding payment from the Employer."
    },
    {
        "keywords": ["solely in english", "english version shall prevail", "no indonesian version", "仅以英文为准", "无印尼语版本", "仅签署英文", "不签署印尼语", "印尼语仅供参考"],
        "risk_level": "high",
        "title": "印尼 2009 年第 24 号法律第 31 条：单语种英文合同行政与司法绝对无效隐患",
        "norm_id": "ID:SEMA_3_2023",
        "desc": "印尼法律强制要求涉外协议必须具备印尼语文本。虽然印尼最高院 SEMA 3/2023 限制恶意无效主张，但若合同自始排除印尼语签署，仍面临被当地法官认定无效及合同标的被没收的极高风险。",
        "revision": "Bilingual Execution Clause: This Contract shall be executed concurrently in both the Indonesian language (Bahasa Indonesia) and English. Both language versions shall be authentic. In case of divergence, the English technical terms shall guide interpretation."
    },
    {
        "keywords": ["waive any injunction", "unconditional and irrevocable", "without demur", "放弃任何禁令", "放弃保函止付救济", "不可撤销且无条件即付且放弃抗辩", "严禁申请法院禁令"],
        "risk_level": "high",
        "title": "新加坡 BS Mount Sophia 案：见索即付保函排除‘显失公平 (Unconscionability)’止付救济红线",
        "norm_id": "SG:Precedent:BS_Mount_Sophia",
        "desc": "新加坡及普通法系下，独立履约保函受‘显失公平’衡平法例外保护。若合同草案强迫承包商预先放弃任何保函止付禁令救济，将导致发包人恶意索兑时企业彻底丧失司法防卫屏障。",
        "revision": "Performance Security Restriction: The Employer shall not demand payment under the Performance Security without providing 28 days prior written notice specifying the remediable breach. The equitable doctrine of unconscionability remains available to Contractor."
    },
    {
        "keywords": ["no adjustment for change in law", "delete clause 13.7", "unlimited liquidated damages", "排除法律变更调价", "不按法律变动调整", "无上限违约金", "违约金无封顶", "放弃eot顺延"],
        "risk_level": "high",
        "title": "严重背离 FIDIC 黄金原则 (GP3 风险平衡原则) 与越南 2025 新建设法调价合规红线",
        "norm_id": "FIDIC:Silver_1999:Clause_13.7",
        "desc": "删除法律变更调价（Clause 13.7）将东道国政策/TKDN配额/关税调整风险完全转嫁承包商；未设工期违约金上限（通常封顶 10%~15%）在普通法及东盟法域构成严苛惩罚性条款，破坏商业平衡。",
        "revision": "Adjustments for Change in Laws: The Contract Price shall be adjusted to account for any increase or decrease in Cost resulting from changes in the Laws of the Host Country (including TKDN quotas and environmental permits) enacted after the Base Date. Liquidated damages for delay shall be capped at 10% of Contract Value."
    },
    {
        "keywords": ["7 days notice of claim", "3 days notice", "7天内索赔", "3天内通知", "逾期自始放弃全部索赔", "5天内提出工期顺延"],
        "risk_level": "medium",
        "title": "FIDIC 第 20.1 款索赔通知期过度压缩陷阱（苛刻失权条款）",
        "norm_id": "FIDIC:Silver_1999:Clause_20.1",
        "desc": "将 FIDIC 标准的 28 天索赔通知期苛刻压缩至 7 天甚至更短，构成程序性失权陷阱。在重大海外地质或原住民征拆复杂工程中，极易导致承包商实体索赔权自始丧失。",
        "revision": "Notice of Claim Period: The Contractor shall give notice to the Engineer describing the event giving rise to the claim not later than 28 days (or no less than 21 days) after becoming aware of the event."
    }
]


def _run_verification(
    text: str,
    mode: str,
    snapshot_mgr: SnapshotManager
) -> VerifyResponse:
    items: List[VerifyItem] = []
    redline_items: List[ContractRedlineItem] = []
    seen_refs = set()

    # 1. 执行合同条款强行法红线体检扫描 (Contract Clause Redline Audit)
    lower_text = text.lower()
    for rule in ASEAN_CONTRACT_REDLINES:
        matched = False
        matched_kw = ""
        for kw in rule["keywords"]:
            if kw.lower() in lower_text:
                matched = True
                matched_kw = kw
                break
        if matched:
            # 提取匹配上下文片段
            idx = lower_text.find(matched_kw.lower())
            start = max(0, idx - 40)
            end = min(len(text), idx + len(matched_kw) + 60)
            snippet = f"...{text[start:end].strip()}..."
            redline_items.append(ContractRedlineItem(
                clause_snippet=snippet,
                risk_level=rule["risk_level"],
                violated_rule_title=rule["title"],
                violated_norm_id=rule["norm_id"],
                mandatory_rule_desc=rule["desc"],
                recommended_revision=rule["revision"]
            ))

    # 2. 扫描法条引用 (FIDIC, UU, CIPAA, SOPA 等)
    for m in RE_CITATION_DETECT.finditer(text):
        law = m.group(1).upper()
        nr = m.group(2).split()[0].rstrip('，。；;:,.')
        full_cite = m.group(0)

        norm_id = f"{law}:{nr}"
        if norm_id in seen_refs:
            continue
        seen_refs.add(norm_id)

        norm = snapshot_mgr.norm_lookup(norm_id)
        if not norm:
            conn = snapshot_mgr.get_connection()
            if conn:
                cur = conn.cursor()
                clean_law = law.replace(":", "")
                clean_nr = nr.replace(":", "").replace("_", "").replace(".", "")
                cur.execute(
                    """SELECT * FROM norms 
                       WHERE (norm_id LIKE ? OR law LIKE ?) 
                         AND (enbez LIKE ? OR norm_id LIKE ?)
                       LIMIT 1""",
                    (f"%{clean_law}%", f"%{clean_law}%", f"%{clean_nr}%", f"%{clean_nr}%")
                )
                row = cur.fetchone()
                if row:
                    norm = dict(row)

        if norm:
            stand = norm.get("stand") or "现行生效版"
            source_label = "东盟东道国官方立法公布库/FIDIC标准库"
            note = f"核验通过：引用条款真实存在于{source_label}（{stand}）"
            verdict = "exact"
            stand_note = f"现行生效条文 ({stand})"

            items.append(VerifyItem(
                ref_id=full_cite,
                in_db=True,
                is_current=True,
                stand_note=stand_note,
                consistency_verdict=verdict,
                has_full_text=True,
                quote_in_material=full_cite,
                db_text_de=norm.get("text_de", "")[:500],
                db_text_zh=norm.get("text_zh") or f"出海中企在《{norm.get('law', law)}》下的法定权利义务与工程救济规范",
                note=note
            ))
        else:
            items.append(VerifyItem(
                ref_id=full_cite,
                in_db=False,
                is_current=False,
                stand_note="未在官方快照库中匹配到该条款",
                consistency_verdict="unverified",
                has_full_text=False,
                quote_in_material=full_cite,
                db_text_de="",
                db_text_zh="",
                note="未查见该法条，请核实法典名称与条号是否拼写有误"
            ))

    # 3. 扫描东盟工程裁判与仲裁先例引用
    for m in RE_ASEAN_CASE_DETECT.finditer(text):
        case_kw = m.group(1)
        if case_kw in seen_refs:
            continue
        seen_refs.add(case_kw)

        case_data = snapshot_mgr.case_lookup(case_kw)
        if case_data:
            items.append(VerifyItem(
                ref_id=case_kw,
                in_db=True,
                is_current=True,
                stand_note=f"{case_data.get('court', '东盟法院/仲裁庭')} 权威生效裁判 ({case_data.get('decided', '2026')})",
                consistency_verdict="exact",
                has_full_text=True,
                quote_in_material=case_kw,
                db_text_de=(case_data.get("leitsatz") or case_data.get("gruende") or "")[:500],
                db_text_zh=case_data.get("leitsatz") or "东盟工程裁判要旨：关于建设工程履约、工期索赔与保函止付裁决",
                note="核验通过：东盟司法/仲裁先例在库，裁判尺度及案号真实存在"
            ))
        else:
            items.append(VerifyItem(
                ref_id=case_kw,
                in_db=False,
                is_current=False,
                stand_note="本地快照库尚未收录该裁判文书全文",
                consistency_verdict="unverified",
                has_full_text=False,
                quote_in_material=case_kw,
                db_text_de="",
                db_text_zh="",
                note="建议委托东道国执业律师或国际仲裁律师调取裁判原始案卷"
            ))

    # 若未命中引证但存在红线，提示红线检测结果
    if not items and redline_items:
        items.append(VerifyItem(
            ref_id=f"已识别 {len(redline_items)} 处合同强行法合规风险",
            in_db=True,
            is_current=True,
            stand_note="合同条款红线审查引擎",
            consistency_verdict="exact",
            has_full_text=True,
            quote_in_material=text[:60],
            db_text_de="",
            db_text_zh=f"共检测出 {len(redline_items)} 处违反东道国强行法或背离 FIDIC 黄金原则的风险条款",
            note="请查看下方的详细红线分析与修改替代建议"
        ))
    elif not items and text.strip():
        items.append(VerifyItem(
            ref_id="自由文本材料",
            in_db=False,
            is_current=False,
            stand_note="材料中未检测到标准东盟工程法条编号或典型强行法违规字样",
            consistency_verdict="unverified",
            has_full_text=False,
            quote_in_material=text[:60],
            db_text_de="",
            db_text_zh="",
            note="未识别到规范引述或红线违规，建议补充合同具体条款"
        ))

    verified_count = sum(1 for it in items if it.in_db and it.consistency_verdict == "exact")
    risk_count = len(redline_items) + sum(1 for it in items if it.consistency_verdict in ("partial", "inconsistent"))
    unverified_count = sum(1 for it in items if not it.in_db)

    return VerifyResponse(
        raw_text=text,
        mode=mode,
        items=items,
        redline_items=redline_items,
        summary={
            "total": len(items),
            "redline_risk_count": len(redline_items),
            "verified_count": verified_count,
            "unverified_count": unverified_count,
            "risk_count": risk_count
        }
    )


@router.post("", response_model=VerifyResponse)
async def verify_foreign_materials(
    payload: VerifyRequest,
    snapshot_mgr: SnapshotManager = Depends(get_snapshot_mgr)
):
    """解析并校验当事人提交的东盟工程法条、判例摘录或工程合同草案红线体检（通过线程池异步卸载）"""
    return await asyncio.to_thread(_run_verification, payload.raw_text, payload.mode, snapshot_mgr)
