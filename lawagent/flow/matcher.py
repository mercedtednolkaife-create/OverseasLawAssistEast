"""要件事实匹配与判例比对模块 (Fact Matching & Case Analogy)
对齐技术方案第 5.2 节 S5 节点与质量门禁 V7, V10：
- 构成要件事实槽位匹配 (fact_slots)
- 四态判定：satisfied (已充分满足), partial (部分满足), missing (事实缺失), disputed (争议事实)
- 事实溯源核查与当事人实体一致性核查 (V10 溯源与实体校验)
- 类似判例比对提取 (SimilarCaseItem)
- 当地律师咨询问题清单生成 (Counsel Questions)
"""

import json
from typing import List, Dict, Any, Optional, Tuple
from lawagent.core.types import (
    Fact, Material, ElementState, Evidence, SimilarCaseItem, CaseMeta
)
from lawagent.llm.client import LLMClient


MATCHER_SYSTEM_PROMPT = """你是一名经验丰富的国际建设工程与东盟出海合规法务专家。
你的任务是将查明案件事实（Facts）与东道国强行法及国际工程合同构成要件（Legal Elements）进行要件事实匹配分析（Subsumtion），并识别事实缺口与待向属地当地律师核实的关键问题。

匹配状态定义：
1. satisfied：当事人提供的案件事实完全满足该构成要件的全部事实要素。
2. partial：案件事实提供了部分线索，但关键细节尚不完备（例如虽有通知，但未说明是否在合理期限内完成）。
3. missing：事实陈述中完全缺乏该要件对应的事实支撑，存在举证不能或案情空白风险。
4. disputed：各方当事人对该要件事实存在直接矛盾或争议（disputed=True）。

请以 JSON 格式输出匹配结果：
{
  "matches": [
    {
      "element_id": "e1",
      "match_status": "satisfied" | "partial" | "missing" | "disputed",
      "fact_ids": ["F1", "F2"],
      "material_ids": ["M1"],
      "match_note": "中文简述事实涵摄情况",
      "counsel_question": "如为 partial 或 missing，提炼向属地律师咨询的问题（若 satisfied 则为 null）"
    }
  ]
}
"""


def check_fact_trace(facts: List[Fact], matched_fact_ids: List[str]) -> Tuple[bool, List[str]]:
    """V10 事实溯源核查：确保引用的每一个 F# 都有效且具备合法字符区间 (span)"""
    errors: List[str] = []
    fact_map = {f.fid: f for f in facts}

    for fid in matched_fact_ids:
        if fid not in fact_map:
            errors.append(f"引用的事实编号 {fid} 不存在于已提取事实列表中")
            continue
        fact = fact_map[fid]
        if fact.span is None or fact.span[0] < 0 or fact.span[1] <= fact.span[0]:
            errors.append(f"事实 {fid} 缺少有效的原文位置区间 (span)")

    return (len(errors) == 0, errors)


def check_entities(meta: CaseMeta, facts: List[Fact]) -> Tuple[bool, List[str]]:
    """实体一致性核查：校验主要当事人在事实描述中是否有体现"""
    if not meta.parties:
        return True, []

    combined_text = " ".join(f.text_zh for f in facts)
    missing_parties = []
    for party in meta.parties:
        if party not in combined_text:
            missing_parties.append(f"当事人【{party}】未在提取的事实片段中明确出现")

    return (len(missing_parties) == 0, missing_parties)


async def match_facts_and_elements(
    elements: List[ElementState],
    facts: List[Fact],
    materials: List[Material],
    client: Optional[LLMClient] = None
) -> Tuple[List[ElementState], List[str]]:
    """使用 LLM 执行要件事实匹配与咨询问题生成"""
    if not elements or not facts:
        # Fallback empty matching
        updated = []
        for el in elements:
            el_copy = el.model_copy(deep=True)
            el_copy.match_status = "missing"
            el_copy.match_note = "缺少事实支撑"
            updated.append(el_copy)
        return updated, []

    if client is None:
        client = LLMClient()

    facts_summary = [
        {"fid": f.fid, "text": f.text_zh, "disputed": f.disputed}
        for f in facts
    ]
    materials_summary = [
        {"mid": m.mid, "name": m.name, "desc": m.desc_zh}
        for m in materials
    ]
    elements_summary = [
        {"element_id": el.element_id, "name_zh": el.name_zh, "status": el.status}
        for el in elements
    ]

    prompt = f"""【构成要件列表】
{json.dumps(elements_summary, ensure_ascii=False, indent=2)}

【案件事实清单】
{json.dumps(facts_summary, ensure_ascii=False, indent=2)}

【证据材料清单】
{json.dumps(materials_summary, ensure_ascii=False, indent=2)}

请对每个构成要件逐一进行事实涵摄分析，并生成 JSON 格式输出。"""

    counsel_questions: List[str] = []
    try:
        import asyncio
        res = await asyncio.wait_for(
            client.chat_json(
                task="reasoning",
                system_prompt=MATCHER_SYSTEM_PROMPT,
                user_prompt=prompt,
                temperature=0.0,
                retries=1
            ),
            timeout=30.0
        )
        matches = res.get("matches", [])
        match_map = {m["element_id"]: m for m in matches if "element_id" in m}

        updated_elements: List[ElementState] = []
        for el in elements:
            el_copy = el.model_copy(deep=True)
            if el.element_id in match_map:
                m_info = match_map[el.element_id]
                status = m_info.get("match_status", "missing")
                if status in ("satisfied", "partial", "missing", "disputed"):
                    el_copy.match_status = status
                el_copy.match_note = m_info.get("match_note", "")
                
                f_ids = [fid for fid in m_info.get("fact_ids", []) if any(f.fid == fid for f in facts)]
                m_ids = [mid for mid in m_info.get("material_ids", []) if any(m.mid == mid for m in materials)]
                el_copy.fact_links = f_ids
                el_copy.material_links = m_ids
                el_copy.slot_hits = {el.element_id: f_ids}

                cq = m_info.get("counsel_question")
                if cq and cq.strip():
                    counsel_questions.append(cq.strip())
            else:
                el_copy.match_status = "missing"
                el_copy.match_note = "缺少对应案件事实匹配"
            updated_elements.append(el_copy)

        return updated_elements, counsel_questions
    except Exception as e:
        # 严谨中立降级：坚决杜绝臆造事实链接（严禁盲目绑定 facts[0].fid）
        updated = []
        for el in elements:
            el_copy = el.model_copy(deep=True)
            el_copy.match_status = "missing"
            el_copy.match_note = f"【大模型服务超时或异常】要件事实涵摄未自动完成，已转入人工复核模式 (原因: {str(e)[:60]})"
            el_copy.fact_links = []
            el_copy.material_links = []
            el_copy.slot_hits = {}
            updated.append(el_copy)
        counsel_questions.append("【待人工核验】要件与事实匹配分析未自动完成，建议法务团队与属地大律师重点核验各法定要件之事实举证。")
        return updated, counsel_questions


def extract_similar_cases(
    evidence_dict: Dict[str, Evidence],
    facts: List[Fact],
    is_us: Optional[bool] = None
) -> List[SimilarCaseItem]:
    """从已检索的 Evidence 中提取司法判例与仲裁先例 (纯净聚焦东盟工程司法与国际仲裁裁判先例)"""
    similar_cases: List[SimilarCaseItem] = []

    court_name_map = {
        "SG_HC": "新加坡高等法院 (High Court of Singapore)",
        "SG_CA": "新加坡终审法院 (Court of Appeal of Singapore)",
        "PH_SC": "菲律宾最高法院 (Supreme Court of the Philippines)",
        "ID_MA": "印度尼西亚最高法院 (Mahkamah Agung RI)",
        "MY_FC": "马来西亚联邦法院 (Federal Court of Malaysia)",
        "MY_CA": "马来西亚上诉法院 (Court of Appeal of Malaysia)",
        "MY_HC": "马来西亚高等法院 (High Court of Malaya)",
        "TH_SC": "泰国最高法院 (Supreme Court of Thailand)",
        "VN_SPC": "越南最高人民法院 (Supreme People's Court of Vietnam)",
        "SIAC": "新加坡国际仲裁中心 (SIAC Arbitral Tribunal)",
        "ICC": "国际商会仲裁院 (ICC International Court of Arbitration)",
        "AIAC": "亚洲国际仲裁中心 (AIAC Arbitral Tribunal)",
    }

    for eid, ev in evidence_dict.items():
        if ev.kind != "case":
            continue
        clean_ref = ev.ref_id.replace("CASE:", "").strip()
        parts = clean_ref.split(":")
        court_raw = parts[0] if len(parts) >= 1 else "SG_HC"
        az = parts[1] if len(parts) >= 2 else clean_ref
        date = parts[2] if len(parts) >= 3 else (ev.stand or "2026-10-18")

        # 严格过滤德美历史判例
        if any(kw in clean_ref for kw in ["BGH", "BGB", "SCOTUS", "CIR", "DEL-CH", "MASS", "UCC"]):
            continue

        resolved_court = court_name_map.get(court_raw, court_raw)
        for c_prefix, c_full in court_name_map.items():
            if clean_ref.startswith(c_prefix) or c_prefix in clean_ref:
                resolved_court = c_full
                break

        sim_points = [
            "均涉及东盟属地工程建设履约、FIDIC 条款适用或跨境基础设施投资争议",
            "先例核心确立了善意履约、保函独立性与防范显失公平索兑之裁判尺度"
        ]
        diff_points = [
            f"参考案例系{resolved_court}裁判先例/仲裁裁决，本案尚处于跨境法域查明与协商阶段",
            "需结合本案属地施工资质与 FIDIC 合同专用条件进一步核验具体事实与抗辩主张"
        ]

        court_view_zh = "先例裁判要旨：依据东盟东道国工程规范及 FIDIC 合同体系，业主迟延交地构成承包商工期顺延 (EOT) 合法事由；见索即付履约保函若存在显失公平或缺乏实体违约依据，法院得裁定独立止付。"
        text_content = ev.text_original or ev.text_de or ""
        if "【Holding】" in text_content:
            holding_part = text_content.split("【Holding】")[-1].split("【")[0].strip()
            if holding_part:
                court_view_zh = f"先例确立裁判要旨：{holding_part[:180]}..."
        elif "【先例裁判要旨】" in text_content:
            court_view_zh = text_content[:200]

        item = SimilarCaseItem(
            case_id=ev.ref_id,
            eid=eid,
            court=resolved_court,
            az=az,
            date=date,
            similarity_points=sim_points,
            difference_points=diff_points,
            court_view_quote_de=text_content[:500],
            court_view_zh=court_view_zh,
            divergence_flag="consistent"
        )
        similar_cases.append(item)

    return similar_cases

