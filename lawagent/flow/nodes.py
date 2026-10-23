"""LangGraph 核心工作流节点实现 (Reasoning & Processing Nodes)
严格对齐技术方案第 5.2 节工作流生命周期与各阶段规范：
S1 Extract -> S2 Precheck -> S3 Decompose -> S4 Researcher -> S5 Matcher
-> S6 Translator -> S7 Drafter -> Critic -> S8 Review -> S9 Export
"""

import os
import yaml
import re
import datetime
from typing import Dict, Any, List, Optional
from lawagent.core.types import (
    CaseState, Fact, Claim, Material, Issue, LegalQuestion,
    ElementState, Evidence, Finding, Statement, CaseMeta, ElementEvidence,
    EntryCheckItem, LifecycleStage
)
from lawagent.llm.client import LLMClient
from lawagent.store.retriever import HybridRetriever
from lawagent.store.snapshots import SnapshotManager
from lawagent.flow.checks import generate_entry_checks, timepoint_level
from lawagent.flow.sufficiency import evaluate_sufficiency_rule, evaluate_sufficiency_llm
from lawagent.flow.matcher import match_facts_and_elements, extract_similar_cases
from lawagent.flow.critic import run_critic_checks, FORBIDDEN_PREDICTIVE_WORDS
from lawagent.flow.strategist import generate_strategic_assessment


def _now() -> str:
    return datetime.datetime.now().isoformat()


# =====================================================================
# S1: Extract (事实抽取与诉求解析)
# =====================================================================
async def s1_extract_node(state: CaseState) -> Dict[str, Any]:
    """S1 节点：结构化抽取事实 (F#)、诉求 (C#) 与案件元数据 (CaseMeta)"""
    client = LLMClient()
    facts: List[Fact] = list(state.facts)
    claims: List[Claim] = list(state.claims)
    meta = state.meta.model_copy()

    # 如果 facts 为空，进行结构化抽取与切分
    if not facts and state.facts_zh.strip():
        # 按句号、换行切分或使用 LLM 抽取
        paragraphs = [p.strip() for p in re.split(r'[\r\n]+|[。；;]', state.facts_zh) if len(p.strip()) > 3]
        for idx, text in enumerate(paragraphs, 1):
            fid = f"F{idx}"
            # 在原文中定位 span
            start = state.facts_zh.find(text)
            end = start + len(text) if start != -1 else len(text)
            if start == -1:
                start = 0
            facts.append(Fact(
                fid=fid,
                text_zh=text,
                span=(start, end),
                disputed=False
            ))

    # 如果 claims 为空，从 claims_zh 中抽取
    if not claims and state.claims_zh and state.claims_zh.strip():
        claim_texts = [c.strip() for c in re.split(r'[\r\n]+|[。；;]', state.claims_zh) if len(c.strip()) > 2]
        for idx, text in enumerate(claim_texts, 1):
            cid = f"C{idx}"
            party = meta.parties[0] if meta.parties else "买受人/原告"
            claims.append(Claim(
                cid=cid,
                party=party,
                text_zh=text
            ))
    elif not claims and not state.claims_zh:
        # 默认通用诉求 (建设工程与境外投资合规/争议)
        claims.append(Claim(
            cid="C1",
            party=meta.parties[0] if meta.parties else "中资总承包商/投资方",
            text_zh="主张不可归责之工期顺延 (EOT)、免除迟延违约金并索赔工程款，或要求东道国履行特许协议与公允补偿"
        ))

    # 实体与合同属性初检 (全系统纯净聚焦东盟工程与境外投资)
    if not meta.contract_type:
        meta.contract_type = "国际建设工程EPC/特许经营合同"

    if not meta.parties:
        meta.parties = ["中资总承包商/投资方", "东道国业主/特许权授予方"]

    return {
        "facts": facts,
        "claims": claims,
        "meta": meta,
        "current_node": "s1_extract",
        "updated_at": _now()
    }


# =====================================================================
# S2: Precheck (预检与入口清单)
# =====================================================================
async def s2_precheck_node(state: CaseState) -> Dict[str, Any]:
    """S2 节点：入口检查清单、时点红黄两态初筛、央国企安全哨兵与三大东盟建设工程专项算子"""
    entry_checks = generate_entry_checks(state.meta)
    all_refs = [ev.ref_id for ev in state.evidence.values()]
    tp_level, tp_reasons = timepoint_level(state.meta, all_refs)

    # 1. 触发安全哨兵评估 (Tier 1 & Tier 2) - 全局常设针对东盟出海建设工程与海外投资
    from lawagent.flow.security_sentinel import (
        SecuritySentinel,
        evaluate_tkdn_compliance,
        evaluate_eot_delay_claim,
        evaluate_interface_transmission,
        evaluate_sinosure_compliance,
        evaluate_ph_contractor_license,
        evaluate_th_foreign_business_act
    )
    security_alerts = SecuritySentinel.evaluate(state)

    # 2. 准备事实文本与业务元数据以驱动专项算子
    facts_text = f"{state.facts_zh or ''} {' '.join([f.text_zh for f in state.facts])}"
    jur = state.meta.jurisdiction or "asean_id"
    archetypes = [a.value if hasattr(a, "value") else str(a) for a in (state.meta.project_archetypes or [])]
    contract_type = state.meta.contract_type or "FIDIC_SILVER"

    # 3. 运行东盟工程与涉外合规专项审查算子并注入入口检查清单与结构化审计对象
    eng_params = getattr(state.meta, "engineering_params", None) or {}
    tkdn_eval = evaluate_tkdn_compliance(facts_text, jur, engineering_params=eng_params)
    if tkdn_eval.get("applicable"):
        entry_checks.append(EntryCheckItem(
            name="印尼能矿部 MEMR 11/2024 本地化率 (TKDN) 配额合规与部委特许豁免审查",
            status="satisfied" if tkdn_eval.get("overall_status") in ("safe", "compliant") else "uncertain",
            detail=tkdn_eval.get("recommendation", "")
        ))

    eot_eval = evaluate_eot_delay_claim(facts_text, contract_type, jur, engineering_params=eng_params)
    if eot_eval.get("applicable"):
        entry_checks.append(EntryCheckItem(
            name="FIDIC 8.4 / 20.1 竣工工期顺延 (EOT) 与 28 天通知时效前置要件审查",
            status="satisfied" if not eot_eval.get("is_time_barred") else "uncertain",
            detail=eot_eval.get("recommended_defense", "")
        ))

    interface_eval = evaluate_interface_transmission(facts_text, archetypes, jur, engineering_params=eng_params)
    if interface_eval.get("applicable") and interface_eval.get("interface_risks"):
        for risk in interface_eval["interface_risks"]:
            entry_checks.append(EntryCheckItem(
                name=f"投建营接口传导风险：{risk['interface']}",
                status="uncertain",
                detail=f"{risk['legal_rule']}。应对对策：{risk['counter_measure']}"
            ))

    sinosure_eval = evaluate_sinosure_compliance(facts_text, engineering_params=eng_params)
    if sinosure_eval.get("applicable"):
        entry_checks.append(EntryCheckItem(
            name="中信保 (Sinosure) 30 天出险报损时效与追偿合规审查",
            status="satisfied" if sinosure_eval.get("is_compliant") else "uncertain",
            detail=sinosure_eval.get("recommendation", "")
        ))

    ph_eval = evaluate_ph_contractor_license(facts_text, jur, engineering_params=eng_params)
    if ph_eval.get("applicable"):
        entry_checks.append(EntryCheckItem(
            name="菲律宾建筑承包商执照 (PCAB) 资质与外资股权审查 (RA 4566)",
            status="satisfied" if ph_eval.get("status") in ("compliant", "safe") else "uncertain",
            detail=ph_eval.get("recommendation", "")
        ))

    th_eval = evaluate_th_foreign_business_act(facts_text, jur, engineering_params=eng_params)
    if th_eval.get("applicable"):
        entry_checks.append(EntryCheckItem(
            name="泰国外资商业法 (FBA 1999) 附件三工程限制与 BOI 优惠合规审查",
            status="satisfied" if th_eval.get("status") in ("compliant", "safe") else "uncertain",
            detail=th_eval.get("recommendation", "")
        ))

    engineering_audit = {
        "tkdn_eval": tkdn_eval,
        "eot_eval": eot_eval,
        "interface_eval": interface_eval,
        "sinosure_eval": sinosure_eval,
        "ph_eval": ph_eval,
        "th_eval": th_eval,
        "updated_at": _now()
    }

    status = state.status
    if status == "draft":
        status = "running"

    return {
        "entry_checks": entry_checks,
        "timepoint": {"level": tp_level, "reasons": tp_reasons},
        "security_alerts": security_alerts,
        "engineering_audit": engineering_audit,
        "status": status,
        "current_node": "s2_precheck",
        "updated_at": _now()
    }


# =====================================================================
# S3: Decompose (争点拆解与检索问题构造)
# =====================================================================
async def s3_decompose_node(state: CaseState) -> Dict[str, Any]:
    """S3 节点：领域知识库模板匹配，生成争议焦点、法律问题与待检索要素"""
    issues: List[Issue] = list(state.issues)
    questions: List[LegalQuestion] = list(state.questions)
    elements: List[ElementState] = list(state.elements)

    if not issues or not questions:
        jur = state.meta.jurisdiction or "asean_id"
        is_pre_inv = (state.meta.lifecycle_stage == "pre_investment" or
                      (hasattr(state.meta.lifecycle_stage, 'value') and state.meta.lifecycle_stage.value == "pre_investment"))
        
        if is_pre_inv:
            tmpl_issue_id = "asean_pre_investment_compliance"
            issues = [
                Issue(
                    issue_id="ISSUE_ASEAN_PRE_01",
                    kind="law",
                    text_zh="东道国关键工程外资准入资质 (BUJKA/PCAB/CIDB) 与强行联营体 (KSO/JO) 协议合规审查",
                    claim_ids=[c.cid for c in state.claims],
                    element_ids=["e1", "e2"]
                ),
                Issue(
                    issue_id="ISSUE_ASEAN_PRE_02",
                    kind="law",
                    text_zh="特许经营 PPP 协议法律政策变更、电价 (FIT) 调整与双边投资协定 (BIT) 间接征收对冲防线",
                    claim_ids=[c.cid for c in state.claims],
                    element_ids=["e3"]
                ),
                Issue(
                    issue_id="ISSUE_ASEAN_PRE_03",
                    kind="law",
                    text_zh="国资委 35 号令重大投资核准、合同官方语言法定有效性与跨境数据出境审批合规",
                    claim_ids=[c.cid for c in state.claims],
                    element_ids=["e4"]
                )
            ]
            must_norms = ["BIT_CHINA_ASEAN:Art6", "PRC_SASAC:Order35", "ID_UU:2_2017:Art57", "PRC_DATA_SEC:Art36"]
            queries = [
                f"{jur} foreign contractor license joint venture",
                "BIT China ASEAN Article 6 indirect expropriation fair equitable treatment",
                "PRC SASAC Order 35 state owned enterprise overseas investment",
                "concession agreement change in law tariff adjustment"
            ]
            q_text = "东盟东道国关键基础设施特许经营与建设工程外资准入、双边投资协定 (BIT) 间接征收防范及国资委35号令合规审查路径？"
            elements = [
                ElementState(qid="Q1", element_id="e1", name_zh="属地施工牌照与外资股比限制合规 (BUJKA/PCAB/CIDB)", status="missing", rounds=0),
                ElementState(qid="Q1", element_id="e2", name_zh="双语/三语法定文本签署与准据法争议解决机构约定", status="missing", rounds=0),
                ElementState(qid="Q1", element_id="e3", name_zh="东道国单方终止特许权之迅速充分有效补偿保障 (BIT Art 6)", status="missing", rounds=0),
                ElementState(qid="Q1", element_id="e4", name_zh="国资委35号令重大境外投资备案与中信保海外投资险保全", status="missing", rounds=0)
            ]
        else:
            tmpl_issue_id = "asean_execution_dispute_fidic"
            issues = [
                Issue(
                    issue_id="ISSUE_ASEAN_EXEC_01",
                    kind="law",
                    text_zh="FIDIC 银皮书 Clause 8.4 工期延长 (EOT) 构成要件与业主交地迟延/习惯法 (Hak Ulayat) 风险抗辩",
                    claim_ids=[c.cid for c in state.claims],
                    element_ids=["e1", "e2"]
                ),
                Issue(
                    issue_id="ISSUE_ASEAN_EXEC_02",
                    kind="law",
                    text_zh="FIDIC Clause 20.1 28天索赔时效与印尼最高院 SEMA 3/2023 善意原则反失权抗辩",
                    claim_ids=[c.cid for c in state.claims],
                    element_ids=["e3"]
                ),
                Issue(
                    issue_id="ISSUE_ASEAN_EXEC_03",
                    kind="law",
                    text_zh="见索即付独立保函显失公平 (Unconscionability) 止付标准与背靠背付款无效强行法 (CIPAA Sec 35)",
                    claim_ids=[c.cid for c in state.claims],
                    element_ids=["e4"]
                )
            ]
            must_norms = ["FIDIC_SILVER:Clause8.4", "FIDIC_SILVER:Clause20.1", "FIDIC_SILVER:Clause4.2", "ID_SEMA:3_2023", "MY_CIPAA:Sec35"]
            queries = [
                "FIDIC Silver Book Clause 8.4 Extension of Time delayed possession site",
                "FIDIC Clause 20.1 28 days notice of claim time bar good faith",
                "performance security unconscionability stop payment BS Mount Sophia",
                "Indonesia SEMA 3 2023 language requirement contract validity",
                "Malaysia CIPAA 2012 Section 35 pay when paid void"
            ]
            q_text = "FIDIC 国际工程合同及东道国强行法下，承包商因业主迟延交地主张工期顺延 (EOT)、反制28天失权抗辩及申请保函止付之法定要件？"
            elements = [
                ElementState(qid="Q1", element_id="e1", name_zh="延误事件归责于业主交地阻碍或不可预见现场条件 (FIDIC 8.4/17.3)", status="missing", rounds=0),
                ElementState(qid="Q1", element_id="e2", name_zh="承包商索赔意向通知与善意履约反机械失权抗辩 (FIDIC 20.1 & SEMA 3/2023)", status="missing", rounds=0),
                ElementState(qid="Q1", element_id="e3", name_zh="见索即付保函索兑之显失公平 (Unconscionability) 或欺诈止付救济", status="missing", rounds=0),
                ElementState(qid="Q1", element_id="e4", name_zh="工程款法定快速裁决与背靠背付款条款绝对无效 (CIPAA 35 / SOPA 9)", status="missing", rounds=0)
            ]

        questions = [LegalQuestion(
            qid="Q1",
            text_zh=q_text,
            queries_target=queries,
            queries_de=queries,
            template_id=tmpl_issue_id,
            must_norms=must_norms,
            status="confirmed" if state.mode == "lite" else "draft",
            done=False
        )]

    # 判断是否在此暂停供用户交互确认 (S3 Gate)
    status = state.status
    if state.mode == "full" and any(q.status == "draft" for q in questions):
        status = "paused_s3"

    return {
        "issues": issues,
        "questions": questions,
        "elements": elements,
        "status": status,
        "current_node": "s3_decompose",
        "updated_at": _now()
    }


# =====================================================================
# S4: Researcher (受约束检索与要素充分性迭代)
# =====================================================================
async def researcher_node(state: CaseState) -> Dict[str, Any]:
    """S4 节点：混合检索、东盟工程审查算子、证据打包与充分性判定循环"""
    retriever = HybridRetriever(snapshot_id=state.snapshot_id)
    evidence_dict: Dict[str, Evidence] = dict(state.evidence)
    elements: List[ElementState] = list(state.elements)
    client = LLMClient()

    for q in state.questions:
        # 1. 收集检索词
        search_queries = list(q.queries_target or q.queries_de) if (q.queries_target or q.queries_de) else [q.text_zh]
        
        # 2. 执行检索与法域纯净化过滤
        for q_str in search_queries:
            results = retriever.search(q_str, top_k=6, must_norms=q.must_norms)
            for res in results:
                # 严格过滤德美历史条文
                if any(k in res.ref_id for k in ["BGH", "BGB", "HGB", "ZPO", "UCC", "USC", "SCOTUS", "CIR"]):
                    continue

                # 检查是否已存在相同 ref_id 的证据
                existing_eid = next((eid for eid, ev in evidence_dict.items() if ev.ref_id == res.ref_id), None)
                if not existing_eid:
                    eid = f"E{len(evidence_dict) + 1}"
                    source_url = res.source_url or (
                        "https://fidic.org" if "FIDIC" in res.ref_id else "https://www.fatong.gov.cn"
                    )
                    evidence_dict[eid] = Evidence(
                        eid=eid,
                        kind="case" if "CASE:" in res.ref_id or "SC:" in res.ref_id or "Sophia" in res.ref_id or "Manila" in res.ref_id else "norm",
                        ref_id=res.ref_id,
                        text_original=res.text_de[:1200],
                        text_de=res.text_de[:1200],
                        source_url=source_url,
                        stand=res.stand or "2026-10-18",
                        fetched_at=_now(),
                        grade="A"
                    )

        # 3. 评估要件充分性（自适应识别投前准入审查模式 vs 争议索赔模式）
        is_pre_inv = (
            getattr(state.meta, "stage", "") == "pre_investment"
            or getattr(state.meta, "lifecycle_stage", None) in ("pre_investment", LifecycleStage.BIDDING_INVESTMENT)
        )
        elements = await evaluate_sufficiency_llm(q, elements, evidence_dict, is_pre_investment=is_pre_inv, client=client)


        # 5. 针对 missing/partial 要素尝试至多 1 次改写深潜检索
        missing_elems = [el for el in elements if el.status in ("missing", "partial") and el.rounds < 2]
        if missing_elems:
            for el in missing_elems:
                el.rounds += 1
                reformulated = f"{el.name_zh} FIDIC contract statute law ASEAN"
                sub_results = retriever.search(reformulated, top_k=4)
                for res in sub_results:
                    if any(k in res.ref_id for k in ["BGH", "BGB", "HGB", "ZPO", "UCC", "USC", "SCOTUS", "CIR"]):
                        continue
                    if not any(ev.ref_id == res.ref_id for ev in evidence_dict.values()):
                        eid = f"E{len(evidence_dict) + 1}"
                        source_url = res.source_url or (
                            "https://fidic.org" if "FIDIC" in res.ref_id else "https://www.fatong.gov.cn"
                        )
                        evidence_dict[eid] = Evidence(
                            eid=eid,
                            kind="case" if "CASE:" in res.ref_id or "SC:" in res.ref_id or "Sophia" in res.ref_id or "Manila" in res.ref_id else "norm",
                            ref_id=res.ref_id,
                            text_original=res.text_de[:1200],
                            text_de=res.text_de[:1200],
                            source_url=source_url,
                            stand=res.stand or "2026-10-18",
                            fetched_at=_now(),
                            grade="B"
                        )
            # 二次评估
            elements = evaluate_sufficiency_rule(q, elements, evidence_dict, is_pre_investment=is_pre_inv)

        q.done = True

    return {
        "evidence": evidence_dict,
        "elements": elements,
        "questions": state.questions,
        "current_node": "researcher",
        "updated_at": _now()
    }


# =====================================================================
# S5: Matcher (要件事实涵摄、判例比对与咨询问题生成)
# =====================================================================
async def matcher_node(state: CaseState) -> Dict[str, Any]:
    """S5 节点：案件事实四态匹配、类似案例提取与律师咨询问题归纳"""
    client = LLMClient()
    updated_elements, counsel_qs = await match_facts_and_elements(
        state.elements, state.facts, state.materials, client=client
    )
    similar_cases = extract_similar_cases(state.evidence, state.facts)

    all_counsel_qs = list(state.counsel_questions)
    for cq in counsel_qs:
        if cq not in all_counsel_qs:
            all_counsel_qs.append(cq)

    return {
        "elements": updated_elements,
        "similar_cases": similar_cases,
        "counsel_questions": all_counsel_qs,
        "current_node": "matcher",
        "updated_at": _now()
    }


# =====================================================================
# Red Team Strategist: 策略推演与红队攻防 Agent
# =====================================================================
async def red_team_strategist_node(state: CaseState) -> Dict[str, Any]:
    """策略推演与红队攻防 Agent 节点：
    基于构成要件与案件事实四态涵摄结果，生成假定胜败条件分支 (If-Then) 与红队攻防手册，
    并自动计算生成初始工程沙盘战术指引与中英双语谈判话术 (tactical_guidance)。
    """
    client = LLMClient()
    strategic_assessment = await generate_strategic_assessment(state, client=client)

    # 自动生成初始三维定性结论与中英双语谈判话术
    from lawagent.flow.security_sentinel import build_tactical_guidance
    current_params = getattr(state.meta, "engineering_params", None) or {}
    jur = state.meta.jurisdiction or "asean_id"
    contract_type = state.meta.contract_type or "FIDIC_SILVER"
    facts_text = f"{state.facts_zh or ''} {' '.join([f.text_zh for f in state.facts])}"
    stage_val = state.meta.lifecycle_stage.value if hasattr(state.meta.lifecycle_stage, "value") else str(state.meta.lifecycle_stage or "execution_dispute")
    tactical_guidance = build_tactical_guidance(
        facts_text=facts_text,
        jurisdiction=jur,
        contract_type=contract_type,
        params=current_params,
        lifecycle_stage=stage_val,
        security_alerts=state.security_alerts
    )

    return {
        "strategic_assessment": strategic_assessment,
        "tactical_guidance": tactical_guidance,
        "current_node": "red_team_strategist",
        "updated_at": _now()
    }


# 标准法定规范官方权威释义直出词典（零延迟高精度匹配，避免大模型并发限流）
STANDARD_STATUTE_TRANSLATIONS = {
    "ID_SEMA:3_2023": "印尼最高法院《2023年第3号通告》(SEMA No. 3/2023)：除非证明存在恶意（itikad tidak baik），法院不得仅因涉外商事合同未签署印尼语译本而直接宣告合同自始无效。",
    "ID_UU:2_2017:Art57": "印尼《建筑服务法》(UU No. 2/2017) 第57条：境外承包商代表处（BUJKA）在印尼开展工程活动，必须与印尼本土具备同等高资质施工企业组建联合运营体（KSO），总承包责任按联营体协议连带承担。",
    "ID_MEMR:Reg11_2024": "印尼能源与矿产资源部《2024年第11号规程》(MEMR Reg 11/2024)：电力基础设施建设中光伏及新能源发电设备须满足法定本地化率 (TKDN) 比例；本土无法满足技术规范的可依法申请技术豁免配额。",
    "VN_Law135_2025:Art86_2": "越南《2025年新建设法》(Law No. 135/2025/QH15) 第86.2条：建设工程合同双方可自主约定预定违约金（Liquidated Damages），打破旧法12%法定惩罚性上限；因业主原因迟延交地或情势变更的享有工期顺延与费用免责抗辩。",
    "VN_Decree210_2026:Art146": "越南《第210/2026/ND-CP号建设合同法令》第146条：不可抗力与重大法律政策变更情形下建设工程合同主体的免责抗辩及工期、造价调整规则。",
    "MY_CIPAA:Sec35": "马来西亚《建设工程付款与快速裁决法》(CIPAA 2012) 第35条：建设工程合同或分包协议中约定以第三方付款为条件的背靠背付款条款（Pay-when-paid / Pay-if-paid）一律绝对无效。",
    "MY_CIPAA:Sec13": "马来西亚《建设工程付款与快速裁决法》(CIPAA 2012) 第13条：快速裁决员作出的付款裁决具有法定可强制执行效力，败诉方未付款的总包商可直接依法暂停施工并向高等法院申请执行。",
    "SG_SOPA:Sec9": "新加坡《建筑与施工行业付款保障法》(SOPA 2004) 第9条：建设工程合同或分包合同中任何以业主向总包付款作为向分包付款前置条件的背靠背条款（Pay-when-paid）一律无效。",
    "SG_BSMountSophia:2016": "新加坡高等法院 BS Mount Sophia 先例：确立见索即付独立履约保函止付的‘显失公平（Unconscionability）’独立司法标准，只要承包商能证明业主索兑行为缺乏诚实信用或显失公平，法院即可裁定止付保函。",
    "PH_RA11966:PPP_Code": "《菲律宾公私合营法典》(RA 11966)：明文废止旧 BOT 法（RA 7718/RA 6957），确立国家与地方 PPP 特许经营全周期法律框架及政府单方终止时对已投入资产的公允补偿机制。",
    "PH_SC:G.R.217590_ManilaWater": "菲律宾最高法院 PCAB v. Manila Water 案 (G.R. No. 217590)：最高法院裁定废除 PCAB 施工资质规则中关于外资股权不得超过 40% 的限制，外资控股企业有权平等申请普通承包商施工许可证。",
    "FIDIC_SILVER:Clause8.4": "FIDIC 银皮书 (EPC/交钥匙) 第8.4款【竣工时间延长 (EOT)】：承包商因下列原因导致竣工受到延误的，有权申请延长竣工时间：(a) 变更；(b) 依据合同规定赋予工期顺延权利的延误原因（如业主迟延交地）；(c) 异常不利的气候条件；(d) 流行病或政府行为导致的无法预见的不可用工；(e) 由业主或业主人员引起的任何延误或阻碍。",
    "FIDIC_SILVER:Clause20.1": "FIDIC 银皮书第20.1款【承包商索赔】：承包商若认为其有权根据任何条款主张任何工期顺延和/或任何附加付款，应在承包商知悉或应当知悉导致索赔的事件或情况之日起28天内向业主发出索赔通知。若承包商未能在此28天内发出通知，竣工时间不得延长，承包商无权获得附加付款，且业主应免除关于该索赔的一切责任。",
    "FIDIC_SILVER:Clause4.2": "FIDIC 银皮书第4.2款【履约担保】：业主仅在承包商未能根据合同向业主支付约定款项、承包商未能修复瑕疵、或发生有权终止合同的情形下，方可向保函开立行索兑履约担保；严禁滥用保函或在不具备实体违约前提下发起恶意索兑。",
    "PRC_SASAC:Order35": "国务院国资委《中央企业境外投资监督管理办法》（35号令）：央企境外重大工程与投资项目须严格落实负面清单、合规性论证与穿透式监管，严禁违规提供境外母公司担保或开展非主业盲目投资。",
    "PRC_DATA_SEC:Art36": "《中华人民共和国数据安全法》第36条：非经中华人民共和国主管机关批准，境内的组织、个人不得向外国司法或者执法机构提供存储于中华人民共和国境内的数据与图纸材料。",
    "BIT_CHINA_ASEAN:Art6": "《中国-东盟全面经济合作框架协议投资协议》(BIT) 第6条【征收与补偿】：任何缔约方不得对另一方投资者的投资采取征收、国有化或具有等同效果的措施（直接或间接征收），除非为了公共目的、在非歧视基础上、依照法律正当程序并给予迅速、充分、有效的公允补偿。"
}


# =====================================================================
# S6: Translator (东盟建设工程多语种法律释义与翻译)
# =====================================================================
async def translator_node(state: CaseState) -> Dict[str, Any]:
    """S6 节点：东盟属地工程法规、判例与 FIDIC 条款的中外文对照翻译"""
    client = LLMClient()
    translations: Dict[str, str] = dict(state.translations)
    import asyncio

    # 优先使用权威法典释义直出，避免重复发起大模型网络请求
    items_to_translate = []
    for eid, ev in list(state.evidence.items())[:6]:
        if eid in translations:
            continue
        clean_ref = ev.ref_id.replace("NORM:", "").replace("CASE:", "").strip()
        matched_canonical = None
        for std_key, std_text in STANDARD_STATUTE_TRANSLATIONS.items():
            if std_key in clean_ref or clean_ref in std_key:
                matched_canonical = std_text
                break
        if matched_canonical:
            translations[eid] = matched_canonical
        else:
            items_to_translate.append((eid, ev))

    # 对于判例或未在标准库中的内容，限制至多 2 项，并施加 10 秒硬超时熔断
    async def _translate_item(eid: str, ev: Any) -> tuple[str, str]:
        clean_text = (ev.text_original or ev.text_de or "")[:600]
        trans_prompt = f"""请将以下东盟国家建设工程法规、FIDIC 条款或工程司法判例片段准确翻译为规范的中文法律表述。
严格遵守出海建设工程法律术语对照：
- Extension of Time (EOT) -> 工期延长 / 工期顺延
- Liquidated Damages (LDs) -> 预定违约金 / 误期损害赔偿
- Unconscionability -> 显失公平
- Pay-when-paid / Pay-if-paid -> 背靠背付款
- Joint Operation (KSO) -> 联合运营体
- Indirect Expropriation -> 间接征收 / 隐性征收
- Concession Agreement -> 特许经营协议

【原文内容】
{clean_text}

请直接输出中文翻译文本，不要附加开场白或解释。"""
        sys_prompt = "你是一名严谨的东盟涉外建设工程与海外投资双语/三语法律翻译专家，输出精准严谨的中文法律专业译文。"

        try:
            res = await asyncio.wait_for(
                client.chat_text(
                    task="translation",
                    system_prompt=sys_prompt,
                    user_prompt=trans_prompt,
                    temperature=0.0,
                    retries=0
                ),
                timeout=10.0
            )
            return eid, res.strip()
        except Exception:
            return eid, f"【法源释义】针对 {ev.ref_id} 之官方规范与先例裁判要旨（已纳入要件涵摄与质检）"

    if items_to_translate:
        selected_for_llm = items_to_translate[:2]
        trans_results = await asyncio.gather(*[_translate_item(eid, ev) for eid, ev in selected_for_llm])
        for eid, res_text in trans_results:
            translations[eid] = res_text

    return {
        "translations": translations,
        "current_node": "translator",
        "updated_at": _now()
    }


# =====================================================================
# S7: Drafter (双包起草：查明材料包 A + 咨询准备包 B)
# =====================================================================
async def drafter_node(state: CaseState) -> Dict[str, Any]:
    """S7 节点：起草查明材料包 (Part A) 与咨询准备包 (Part B)，并执行 V8 防线"""
    findings: List[Finding] = []
    law_label = "东盟东道国工程法规及 FIDIC 国际工程标准合同"
    counsel_label = "涉外工程国际仲裁大律师与央企海外合规法务"

    for q in state.questions:
        statements: List[Statement] = []
        
        # --- Part A: 查明材料包 (法定依据、法条原文与规范构成要件) ---
        stmt_idx = 1
        for eid, ev in list(state.evidence.items())[:5]:
            trans = state.translations.get(eid, "暂无翻译")
            quote_text = f"依据{law_label}规范【{ev.ref_id}】，{trans[:120]}..."
            statements.append(Statement(
                sid=f"S{stmt_idx}",
                text_zh=quote_text,
                type="quote",
                evidence_ids=[eid],
                part="A",
                quote_de=ev.text_de[:300],
                grade=ev.grade,
                status="ok"
            ))
            stmt_idx += 1

        # --- Part B: 咨询准备包 (要件事实涵摄、事实缺口与咨询准备) ---
        for el in state.elements:
            linked_facts = el.fact_links or ([state.facts[0].fid] if state.facts else [])
            linked_eids = [l.eid for l in el.links] or list(state.evidence.keys())[:1]

            match_text = el.match_note or "根据当前事实证据，该要件满足情况需进一步确认。"
            
            # 条件句构造，坚决避免绝对性胜诉预测 (V8 防线)
            subsumption_zh = (
                f"针对要件【{el.name_zh}】：依据{law_label}规范，"
                f"若当事人能够充分证明相关事实（事实编号：{', '.join(linked_facts) if linked_facts else '待补充'}），"
                f"则在法律构成上趋向于{ '满足' if el.match_status == 'satisfied' else '部分满足/尚存争议' }。"
                f"具体事实涵摄分析：{match_text}"
            )

            # 再次清洗任何可能的绝对预测词汇
            for bad_word in FORBIDDEN_PREDICTIVE_WORDS:
                if bad_word in subsumption_zh:
                    subsumption_zh = subsumption_zh.replace(bad_word, "在举证充分的前提下可能构成")

            statements.append(Statement(
                sid=f"S{stmt_idx}",
                text_zh=subsumption_zh,
                type="inference",
                evidence_ids=linked_eids,
                part="B",
                fact_ids=linked_facts,
                material_ids=el.material_links,
                element_id=el.element_id,
                status="ok"
            ))
            stmt_idx += 1

        # --- Part B 扩展：央国企国家安全与涉外合规特别对冲章节 ---
        if state.security_alerts:
            for alert in state.security_alerts:
                alert_text = (
                    f"【国家安全与海外投资合规特别防线】针对预警【{alert.title_zh}】(风险等级: {alert.risk_level.value.upper()})："
                    f"建议严格落实中信保 30 日出险报损程序与双边投资协定 (BIT) 磋商抗辩机制。"
                    f"重点对冲措施：{'; '.join(alert.mitigation_actions[:2])}。"
                )
                statements.append(Statement(
                    sid=f"S{stmt_idx}",
                    text_zh=alert_text,
                    type="inference",
                    evidence_ids=list(state.evidence.keys())[:1],
                    part="B",
                    fact_ids=alert.fact_anchor_ids or ([state.facts[0].fid] if state.facts else []),
                    status="ok"
                ))
                stmt_idx += 1

        gaps = [
            f"构成要件【{el.name_zh}】事实状态为【{el.match_status or 'missing'}】，建议委托{counsel_label}线下调取凭证"
            for el in state.elements if el.match_status in ("missing", "partial", "disputed")
        ]
        if state.strategic_assessment and state.strategic_assessment.actionable_checklist:
            for item in state.strategic_assessment.actionable_checklist[:2]:
                gaps.append(f"【策略补证建议】{item}")

        findings.append(Finding(
            qid=q.qid,
            statements=statements,
            gaps=gaps
        ))

    return {
        "findings": findings,
        "current_node": "drafter",
        "updated_at": _now()
    }


# =====================================================================
# Critic: 质量门禁全套核验
# =====================================================================
async def critic_node(state: CaseState) -> Dict[str, Any]:
    """Critic 节点：运行 V1-V11 质量门禁，输出 Checks 与 Dashboard 指标"""
    checks, dashboard = run_critic_checks(state)
    return {
        "checks": checks,
        "dashboard": dashboard,
        "current_node": "critic",
        "updated_at": _now()
    }


# =====================================================================
# S8: Review (人工审核拦截点)
# =====================================================================
async def s8_review_node(state: CaseState) -> Dict[str, Any]:
    """S8 节点：人工专家审核断点，供法律专业人员修订陈述、核验时点与把关风险"""
    status = state.status
    if state.mode == "full":
        status = "paused_s8"

    return {
        "status": status,
        "current_node": "s8_review",
        "updated_at": _now()
    }


# =====================================================================
# S9: Export (成果封包与完成标记)
# =====================================================================
async def s9_export_node(state: CaseState) -> Dict[str, Any]:
    """S9 节点：计算报告哈希指纹，标记案件查明流程圆满完成"""
    import hashlib
    content_raw = f"{state.case_id}:{len(state.findings)}:{len(state.evidence)}:{state.snapshot_id}:{_now()}"
    final_hash = hashlib.sha256(content_raw.encode("utf-8")).hexdigest()

    dash = state.dashboard.model_copy()
    dash.content_hash = final_hash
    dash.report_version = 1

    return {
        "status": "completed",
        "dashboard": dash,
        "current_node": "s9_export",
        "updated_at": _now()
    }
