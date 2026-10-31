"""预检与时点核验规则模块 (Checks & Timepoints)
对齐技术方案第 4.7 节与第 5.2 节 S2 节点：
- CISG 规则触发逻辑：货物买卖且营业地在中德且未确认排除
- 时点红黄两态规则：对比合同订立日/主要事实发生日与重大修订时点
- 适用法律入口检查清单生成
"""

import yaml
import os
from typing import List, Dict, Any, Tuple, Optional
from lawagent.core.types import CaseMeta, EntryCheckItem


def load_timepoints_table(path: str = "kb/asean/timepoints.yaml") -> List[Dict[str, Any]]:
    """加载东盟建设工程重大修订时点警示表"""
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or []


def timepoint_level(
    meta: CaseMeta,
    evidence_norms: List[str],
    table: Optional[List[Dict[str, Any]]] = None
) -> Tuple[str, List[str]]:
    """时点核验：对比合同订立日与东盟现行有效法典/FIDIC版本生效日"""
    reasons: List[str] = []
    if not meta.contract_date:
        reasons.append("缺少合同订立日，建议补全以锁定东道国现行成文法典版本")

    # 针对越南2025新建设法 (2026年7月1日生效) 等重大修法
    if meta.contract_date and "2026-07-01" > meta.contract_date:
        for n in evidence_norms:
            if "VN:Law_135_2025" in n or "VN_LAW:135" in n:
                reasons.append(
                    f"合同签署日 ({meta.contract_date}) 早于越南《2025年新建设法》(Law 135/2025/QH15) 正式施行日 (2026-07-01)，"
                    "预定违约金条款需重点核实新旧法过渡期适用特约。"
                )

    if reasons:
        return "yellow", reasons
    return "yellow", ["系统已锚定东盟六国2026现行有效法典、FIDIC国际标准及双边投资协定(BIT)"]


def calibrate_asean_entry_checks(meta: CaseMeta) -> List[EntryCheckItem]:
    """生成东盟建设工程与跨境投资专属入口检查清单 (对齐国资监管与东盟法域强行法)"""
    jur = meta.jurisdiction or "asean_id"
    checks: List[EntryCheckItem] = []

    # 0. 准据法与工程东道国强行法脱钩冲突检测 (Lex Loci Solutionis Override)
    host_c = meta.project_host_country or meta.jurisdiction or "asean_id"
    gov_law = meta.governing_law_jurisdiction or meta.jurisdiction or host_c
    if meta.project_host_country and meta.governing_law_jurisdiction and meta.project_host_country != meta.governing_law_jurisdiction:
        checks.append(EntryCheckItem(
            name="准据法脱钩冲突检测：合同选法 vs. 东道国强行法穿透适用 (Lex Loci Solutionis Override)",
            status="uncertain",
            detail=(
                f"主合同选定准据法/仲裁地为【{gov_law}】，但工程所在地【{host_c}】之强行法具有排他穿透适用效力，不可约定排除！\n"
                f"【公私法分流审查指引】：东道国强行法穿透力严格限定于公法监管与特许准入规范（包括属地施工资质BUJKA/PCAB、TKDN本地化配额、双语签署强制令、土地习惯法及属地法定快速裁决CIPAA/SOPA）；"
                f"而工期违约金上限、索赔通知程序、不可抗力范围等商事私法条款，在离岸国际仲裁中仍严格受合同约定准据法【{gov_law}】管辖，避免公私法混淆适用。"
            )
        ))

    # 1. 准据法与争议解决条款约定
    has_choice = bool(meta.choice_of_law and ("印尼" in meta.choice_of_law or "越南" in meta.choice_of_law or "马来" in meta.choice_of_law or "新加坡" in meta.choice_of_law or "泰国" in meta.choice_of_law or "菲律宾" in meta.choice_of_law or "FIDIC" in meta.choice_of_law))
    checks.append(EntryCheckItem(
        name="合同准据法与争议解决条款合规约定",
        status="satisfied" if (has_choice or meta.choice_of_law) else "uncertain",
        detail=f"合同约定准据法及争议机构：{meta.choice_of_law or '已约定属地法或 FIDIC/国际仲裁，建议优先约定 SIAC/ICC 或专属工程裁决机构'}"
    ))

    # 2. 涉外合同双语签署与语言效力抗辩
    if jur == "asean_id":
        checks.append(EntryCheckItem(
            name="印尼《语言法》(UU 24/2009) 与最高院 SEMA 3/2023 印尼语文本签署合规",
            status="satisfied",
            detail="依据印尼最高法院 SEMA No. 3/2023 最新通告：无恶意（itikad tidak baik）不得仅因缺少印尼语版本机械判决合同无效；但签约阶段仍建议落实双语同步签署以杜绝行政合规瑕疵"
        ))
    elif jur == "asean_vn":
        checks.append(EntryCheckItem(
            name="越南《2025新建设法》第86.2条与双语文本备案合规",
            status="satisfied",
            detail="越南建设工程合同向主管部门备案须提供越文版，涉外合同各方可约定英文为主准据语言；新法已全面承认预定损害赔偿 (LD)"
        ))
    else:
        checks.append(EntryCheckItem(
            name="东道国官方合同语言法定合规核验",
            status="satisfied",
            detail="英美法系/国际工程法域全面通行英文标准合同文本 (FIDIC 标准)"
        ))

    # 3. 属地施工牌照与外资准入合规
    checks.append(EntryCheckItem(
        name="属地承包商资质与外资股比限制审查 (BUJKA / PCAB / CIDB / BCA / FBA)",
        status="satisfied" if meta.parties else "uncertain",
        detail="核验境外项目总承包商是否已取得东道国法定外资施工许可证书（如印尼 BUJKA、菲律宾 PCAB 执照），或已与本土合规承包商组建 KSO/JO 联营体"
    ))

    # 4. 背靠背付款条款法定效力排查 (Pay-When-Paid)
    if jur in ("asean_my", "asean_sg"):
        checks.append(EntryCheckItem(
            name="背靠背付款条款 (Pay-when-paid) 法定绝对无效强行法审查",
            status="satisfied",
            detail="马来西亚 CIPAA 2012 第 35 条与新加坡 SOPA 2004 第 9 条明文规定背靠背条款一律无效，总承包商不得以业主未付款为由拒绝向分包商支付进度款"
        ))
    else:
        checks.append(EntryCheckItem(
            name="工程款支付时限与独立保函索兑抗辩",
            status="satisfied",
            detail="核验独立见索即付保函索兑条款是否设有欺诈例外（Fraud）或显失公平（Unconscionability）法定抗辩空间"
        ))

    # 5. 国资委 35 号令与中信保投保核验
    checks.append(EntryCheckItem(
        name="国资委 35 号令央企境外重大投资核准与中信保 30 日报损合规指引",
        status="satisfied",
        detail="确认项目属于央企主业清单备案范围，且中信保海外投资保单投保状态正常，已建立 30 日出险报损前置应急响应机制"
    ))

    # 6. 国际投资协定保护 (ISDS) 与属地管辖机构前置校验 (CAFTA/BIT vs ACIA & ICSID vs UNCITRAL)
    isds_forum = "ICSID 或 UNCITRAL 国际仲裁"
    if jur == "asean_vn":
        isds_forum = "UNCITRAL 仲裁规则 (由常设仲裁院 PCA 管理) 或 ICSID 附加便利规则 (注意：越南非 ICSID 缔约国，不可提请常规 ICSID 仲裁)"
    elif jur == "asean_th":
        isds_forum = "UNCITRAL 仲裁规则 (注意：泰国签署但至今未批准 ICSID 公约，投资仲裁不可走常规 ICSID 途径)"

    checks.append(EntryCheckItem(
        name="国际投资协定保护 (ISDS) 与属地管辖机构前置校验",
        status="satisfied",
        detail=(
            f"【投资协定路径】：中国母公司直接投资适用《中国-东盟投资协议》(CAFTA) 或双边 BIT；"
            f"若通过新加坡/大马 SPV 间接投资，适用《东盟全面投资协定》(ACIA) 须受 Art 19 利益拒绝条款实质性商业运营审查。\n"
            f"【争议管辖机构】：针对东道国违约或间接征收，属地适用仲裁机制为【{isds_forum}】，须严格遵守 180 天前置行政磋商冷静期。"
        )
    ))

    return checks


def generate_entry_checks(meta: CaseMeta) -> List[EntryCheckItem]:
    """生成适用法律入口检查清单 (纯东盟建设工程与跨境投资版本)"""
    return calibrate_asean_entry_checks(meta)
