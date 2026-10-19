"""四大东盟金标准标杆示范案播种脚本 (Seed ASEAN Benchmark Cases)
对齐《东盟国家迁移方案.md》第七节与第八节 Phase 10 规范：
- C101: 印度尼西亚 (asean_id) - 爪哇燃煤/光伏电站 EPC 习惯法 (Hak Ulayat) 征地延误、双语合同效力抗辩与 TKDN 处罚案
- C102: 越南 (asean_vn) - 沿海 350MW 海上风电股权并购 (M&A) + EPC 保函恶意索兑与 2025 新建设法预定损害赔偿案
- C103: 马来西亚/新加坡 (asean_my / asean_sg) - 吉隆坡轨道交通枢纽 CIPAA 快速裁决、背靠背条款绝对无效与新加坡高院保函止付案
- C104: 菲律宾 (asean_ph) - 跨海大桥 PPP 特许经营换届单方停工 (隐性征收) 与 PCAB 施工资质合规案
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import json
import logging
from typing import List, Dict, Any

from lawagent.core.types import (
    CaseState, CaseMeta, Fact, Claim, Material, LegalQuestion, Issue, EntryCheckItem,
    ElementState, Evidence, Finding, Statement, CheckItem, DashboardMetrics, SimilarCaseItem,
    SavedInsight, StrategicAssessment, OutcomeBranch, RedTeamDefense,
    LifecycleStage, ProjectArchetype, SecurityRiskLevel, SecurityAlertItem
)
from lawagent.store.db import StateDBManager

logger = logging.getLogger(__name__)


def create_c101_case() -> CaseState:
    """C101: 印尼爪哇燃煤/光伏混合电站 EPC 习惯法征地延误、双语合同效力抗辩与 TKDN 处罚案"""
    alert_tkdn = SecurityAlertItem(
        risk_level=SecurityRiskLevel.CAUTION,
        category="resource_nationalism_tkdn",
        title_zh="光伏组件与电气设备印尼 TKDN 本地化率合规风险",
        fact_anchor_ids=["F3"],
        host_law_basis=["ID_MEMR:Reg11_2024", "ID_MOI:Reg35_2025"],
        prc_or_treaty_basis=["PRC_SASAC:Order35"],
        sinosure_preservation_guide="核实设备清单并向印尼工业部指定第三方核验机构 (Sucofindo) 申请豁免批文。",
        mandatory_human_checklist=["核查光伏逆变器是否列入工业部国内无量产清单", "核实 PLN 国家电网并网准入文件"],
        mitigation_actions=["依据 MEMR Reg 11/2024 申请过渡期豁免", "锁定当地采购证明及进口关税免税证明"]
    )
    alert_infra = SecurityAlertItem(
        risk_level=SecurityRiskLevel.HIGH,
        category="national_security_review",
        title_zh="关键电力基础设施外资准入与习惯法土地防范",
        fact_anchor_ids=["F1", "F2"],
        host_law_basis=["ID_UU:2_2017:Art57", "ID_SEMA:3_2023"],
        prc_or_treaty_basis=["BIT_CHINA_ASEAN:Art6"],
        sinosure_preservation_guide="若业主威胁索兑保函或单方终止，须在 30 个自然日内向中国信保提交可能损失通知书。",
        mandatory_human_checklist=["核实原住民习惯法土地征拆政府移交备忘录", "严禁签署任何放弃工期索赔纪要"],
        mitigation_actions=["援引 SEMA 3/2023 反驳纯英文协议无效抗辩", "依据 FIDIC 8.4 提出工期索赔并向 SIAC 申请紧急仲裁止付保函"]
    )

    facts = [
        Fact(fid="F1", text_zh="2023年3月，中资总包联合体与印尼国电下属项目公司签署西爪哇 500MW 混合电站 EPC 总承包合同，采用 FIDIC 银皮书标准条件。"),
        Fact(fid="F2", text_zh="项目施工中，因现场涉及原住民习惯法土地 (Hak Ulayat) 权属纠纷抗议，业主迟延移交进场道路与电站主场区达 180 天。"),
        Fact(fid="F3", text_zh="因印尼工业部收紧光伏组件本地化率政策，业主指控中方采购的逆变器本土化率仅 28%（法定 40%），威胁扣罚 800 万美元违约金。"),
        Fact(fid="F4", text_zh="总承包商依 FIDIC 8.4 款提出顺延工期 180 天及 1,200 万美元延误成本补偿，业主以总承包商未在 28 天内提交最终细化索赔报告构成失权，且双方签署的顺延工期补充备忘录仅有英文版未附印尼语译本依据印尼《语言法》(UU 24/2009) 自始绝对无效为由拒付，并向雅加达开证行发起履约保函索兑。")
    ]
    claims = [
        Claim(cid="C1", party="中资总承包商", text_zh="请求裁定原住民习惯法土地征拆迟延属业主风险事件，顺延竣工工期 180 天并补偿窝工与延期成本 1,200 万美元。"),
        Claim(cid="C2", party="中资总承包商", text_zh="依据印尼最高法院 SEMA No. 3/2023 确认英文补充备忘录具有完全法律效力，反制业主恶意无效抗辩。"),
        Claim(cid="C3", party="中资总承包商", text_zh="依据能矿部 MEMR Reg 11/2024 主张逆变器本土无量产能力之法定义务豁免，撤销罚款主张。"),
        Claim(cid="C4", party="中资总承包商", text_zh="申请紧急止付 1,200 万美元见索即付履约保函。")
    ]
    materials = [
        Material(mid="M1", name="EPC总承包合同主协议及FIDIC专用条件", desc_zh="工程总承包合同文本与FIDIC银皮书专用条件", fact_ids=["F1", "F4"]),
        Material(mid="M2", name="业主交地迟延备忘录 (英文签署本)", desc_zh="双方项目部关于土地移交迟延180天的往来备忘录签署件", fact_ids=["F2", "F4"]),
        Material(mid="M3", name="Sucofindo光伏逆变器本土化率检验证明", desc_zh="印尼官方授权第三方检验机构出具的TKDN评定报告", fact_ids=["F3"])
    ]
    issues = [
        Issue(issue_id="I1", kind="law", text_zh="习惯法土地 (Hak Ulayat) 征拆阻碍是否构成 FIDIC 银皮书第 8.4 款项下业主交地迟延与费用补偿要件？", claim_ids=["C1"], element_ids=["e1", "e2"]),
        Issue(issue_id="I2", kind="law", text_zh="双方仅签署英文备忘录是否依据印尼《语言法》导致协议无效？最高法院 SEMA 3/2023 善意原则如何适用？", claim_ids=["C2"], element_ids=["e3"]),
        Issue(issue_id="I3", kind="law", text_zh="逆变器本地化率不足能否依据能矿部 MEMR Reg 11/2024 豁免，及见索即付保函恶意索兑之紧急救济路径？", claim_ids=["C3", "C4"], element_ids=["e4"])
    ]
    questions = [
        LegalQuestion(
            qid="Q1",
            text_zh="FIDIC 银皮书第 8.4 款及印尼工程强行法下，习惯法土地延误之工期补偿、英文协议效力及 TKDN 豁免构成要件？",
            template_id="asean_execution_dispute_fidic",
            must_norms=["ID_UU:2_2017:Art57", "ID_SEMA:3_2023", "ID_MEMR:Reg11_2024", "FIDIC_SILVER:Clause8.4", "FIDIC_SILVER:Clause20.1"]
        )
    ]
    elements = [
        ElementState(qid="Q1", element_id="e1", name_zh="现场移交阻碍归责于业主与不可抗力习惯法征拆争议 (FIDIC 8.4)", status="covered", fact_links=["F2"], material_links=["M1", "M2"], match_status="satisfied"),
        ElementState(qid="Q1", element_id="e2", name_zh="28天索赔通知送达与业主阻碍原则反失权抗辩 (FIDIC 20.1)", status="covered", fact_links=["F4"], material_links=["M1"], match_status="satisfied"),
        ElementState(qid="Q1", element_id="e3", name_zh="印尼最高法院 SEMA 3/2023 善意履约排除仅以缺印尼语宣告合同无效", status="covered", fact_links=["F4"], material_links=["M2"], match_status="satisfied"),
        ElementState(qid="Q1", element_id="e4", name_zh="能矿部 MEMR Reg 11/2024 本地化率技术豁免与保函止付救济", status="covered", fact_links=["F3", "F4"], material_links=["M3"], match_status="satisfied")
    ]
    evidence = {
        "E1": Evidence(eid="E1", kind="norm", ref_id="ID_UU:2_2017:Art57", text_de="UU No. 2/2017 Pasal 57: Para pihak dalam Kontrak Kerja Konstruksi berhak memperoleh ganti rugi atas keterlambatan penyerahan lahan oleh Pengguna Jasa.", source_url="https://peraturan.go.id", stand="2026-10-18", fetched_at="2026-10-18T20:00:00", grade="A"),
        "E2": Evidence(eid="E2", kind="norm", ref_id="ID_SEMA:3_2023", text_de="SEMA No. 3/2023 Rumusan Hukum Kamar Perdata: Ketiadaan terjemahan Bahasa Indonesia dalam kontrak komersial internasional tidak serta-merta membatalkan kontrak kecuali terbukti ada itikad tidak baik.", source_url="https://mahkamahagung.go.id", stand="2026-10-18", fetched_at="2026-10-18T20:00:00", grade="A"),
        "E3": Evidence(eid="E3", kind="norm", ref_id="ID_MEMR:Reg11_2024", text_de="Permen ESDM No. 11/2024: Ketentuan Tingkat Komponen Dalam Negeri (TKDN) pada proyek pembangkit listrik tenaga surya dapat diberikan pengecualian teknis dalam hal industri dalam negeri belum mampu memproduksi.", source_url="https://jdih.esdm.go.id", stand="2026-10-18", fetched_at="2026-10-18T20:00:00", grade="A"),
        "E4": Evidence(eid="E4", kind="norm", ref_id="FIDIC_SILVER:Clause8.4", text_de="FIDIC Silver Book (1999) Clause 8.4: The Contractor shall be entitled to an Extension of Time if completion is delayed by delay in giving possession of Site or exceptionally adverse climatic conditions.", source_url="https://fidic.org", stand="2026-10-18", fetched_at="2026-10-18T20:00:00", grade="A")
    }
    translations = {
        "E1": "印尼《2017年第2号建筑服务法》第57条：建设工程合同当事人有权就业主因现场土地移交迟延造成的损失获得赔偿与工期顺延。",
        "E2": "印尼最高法院《2023年第3号司法通告》(SEMA 3/2023)：涉外商事合同缺少印尼语译本不得仅以此为由被认定无效，除非主张方举证证明存在恶意签约情形。",
        "E3": "印尼能矿部《2024年第11号规章》(MEMR Reg 11/2024)：对于光伏电站项目，在属地工业尚不具备相应量产能力时，可凭第三方机构核验证明申请 TKDN 技术豁免。",
        "E4": "FIDIC 银皮书第8.4款【工期顺延】：若因现场移交迟延或业主风险事件导致工程竣工受阻，承包商有权主张顺延竣工期限及相应合理成本补偿。"
    }
    findings = [
        Finding(
            qid="Q1",
            statements=[
                Statement(sid="S1", text_zh="依据印尼《建筑服务法》第57条及 FIDIC 银皮书第8.4款，业主因原住民习惯法土地迟延移交构成实质违约，总包商顺延工期 180 天之诉求事实清楚且具有刚性法源支撑。", type="quote", evidence_ids=["E1", "E4"], fact_ids=["F2"], part="A", element_id="e1"),
                Statement(sid="S2", text_zh="印尼最高法院 SEMA No. 3/2023 确立的善意原则推翻了旧法下机械否定英文协议效力的裁判规则，业主主张备忘录无效系滥用抗辩，已被司法通告排除。", type="quote", evidence_ids=["E2"], fact_ids=["F4"], part="A", element_id="e3"),
                Statement(sid="S3", text_zh="针对 TKDN 本地化率违约金威胁，建议凭 Sucofindo 检验证明依 MEMR Reg 11/2024 申请法定技术豁免，并锁定中国信保 30 日出险保全程序。", type="inference", evidence_ids=["E3"], fact_ids=["F3"], part="B", element_id="e4")
            ]
        )
    ]
    strategic_assessment = StrategicAssessment(
        case_id="C101",
        pivotal_factors=["印尼最高院 SEMA 3/2023 善意原则对纯英文补充协议效力的确认", "Sucofindo 针对逆变器国内无量产证明之出具时间节点"],
        outcome_branches=[
            OutcomeBranch(
                branch_type="favorable",
                title="全面胜诉分支：工期顺延 180 天并豁免 TKDN 违约金",
                condition_precedent="在法院/仲裁庭出示 SEMA 3/2023 司法判例及能矿部 11/2024 号豁免批文",
                substantive_basis=["ID_UU:2_2017:Art57", "ID_SEMA:3_2023", "FIDIC_SILVER:Clause8.4"],
                outcome_summary="若仲裁庭采纳 SEMA 3/2023 善意履约标准，则裁定英文顺延备忘录合法有效，全额支持工期顺延 180 天并驳回业主索兑保函请求。",
                risk_level="low"
            )
        ],
        red_team_defenses=[
            RedTeamDefense(
                defense_id="D1",
                opposing_claim="业主可能抗辩称 FIDIC 20.1 款 28 天通知时效为强制失权前置要件，承包商已永久丧失索赔权。",
                lethal_index="high",
                opposing_basis="FIDIC Silver Book Clause 20.1 Time-Bar Rule",
                counter_weapons=["印尼《民法典》第 1338 条契约善意原则", "英国建筑法学会 SCL 准则之业主阻碍原则 (Prevention Principle)"],
                factual_counter_point="总承包商已在交地受阻第 7 天发出索赔意向函，仅细化造价报告因等待现场清退而延迟，实质满足通知目的。"
            )
        ],
        actionable_checklist=["立即向印尼能矿部提交逆变器国内无生产能力免税与豁免申请备案", "锁定与中国信保的 30 日出险报损联络单据"],
        updated_at="2026-10-18T20:00:00"
    )

    checks = [
        CheckItem(code="V1", status="pass", reason="法条均通过印尼官方公报及法通网校验"),
        CheckItem(code="V2", status="pass", reason="无虚构法条"),
        CheckItem(code="V3", status="pass", reason="快照绑定 20261018-asean-v1.0"),
        CheckItem(code="V4", status="pass", reason="2026 现行有效法源"),
        CheckItem(code="V5", status="pass", reason="东盟工程合同非国际货物买卖"),
        CheckItem(code="V6", status="pass", reason="印尼语/英语/中文三语对齐"),
        CheckItem(code="V7", status="pass", reason="FIDIC 银皮书 Tier 1 条款"),
        CheckItem(code="V8", status="pass", reason="客观中立"),
        CheckItem(code="V9", status="pass", reason="双包规范结构"),
        CheckItem(code="V10", status="pass", reason="事实证据闭环"),
        CheckItem(code="V11", status="pass", reason="Token 预算合规"),
        CheckItem(code="V12", status="pass", reason="已触发 TKDN 与基础设施预警，已生成中信保 30 日保全与 SEMA 3/2023 对冲方案")
    ]

    dashboard = DashboardMetrics(
        exact_quotes_ratio=(2, 3),
        norms_cases_exist_all=True,
        unresolved_refs_count=0,
        supported_statements_ratio=(3, 3),
        elements_coverage={"covered": 4, "partial": 0, "missing": 0},
        elements_match={"satisfied": 4, "partial": 0, "missing": 0, "disputed": 0},
        facts_traceable_ratio=(1, 1),
        entity_checks_pass_ratio=(1, 1),
        grades_distribution={"A": 4, "B": 0, "C": 0, "D": 0},
        timepoint_level="green",
        cisg_triggered=False,
        snapshot_id="20261018-asean-v1.0",
        report_version=1,
        content_hash="c101aseanvalid2026hash"
    )

    return CaseState(
        case_id="C101",
        title="印尼爪哇燃煤/光伏电站EPC习惯法征地延误、双语合同效力抗辩与TKDN处罚案",
        snapshot_id="20261018-asean-v1.0",
        mode="full",
        status="completed",
        facts_zh="爪哇西区某 500MW 混合电站 EPC 工程中，业主因当地原住民习惯法土地 (Hak Ulayat) 征拆抗议受阻，迟延移交施工现场达 180 天。中资总承包商依据 FIDIC 银皮书第 8.4 款提出工期延长 (EOT) 及窝工费用索赔。印尼业主以'未在 28 天内提交最终索赔明细构成失权'、'双方签署的工期顺延备忘录仅有英文版未签署印尼语译本依据印尼语言法自始无效'、以及'光伏逆变器本土化率 TKDN 仅达 28%（法定 40%）构成违约'为由全面拒付，并向本地开证行索兑 1,200 万美元见索即付履约保函。",
        claims_zh="1. 请求裁定原住民习惯法土地征拆迟延属业主风险事件，顺延工期 180 天并补偿窝工费用；2. 依据印尼最高法院 SEMA No. 3/2023 确认英文补充备忘录有效，反制业主恶意无效抗辩；3. 依据能矿部 MEMR Reg 11/2024 主张逆变器本土无量产能力之法定义务豁免；4. 紧急申请保函止付禁令。",
        meta=CaseMeta(
            title="印尼爪哇电站EPC习惯法征地与TKDN案",
            jurisdiction="asean_id",
            contract_type="国际建设工程EPC总承包合同",
            parties=["中资工程总承包联合体", "印尼国电下属项目公司"],
            choice_of_law="印尼实体法及 FIDIC 银皮书",
            lifecycle_stage=LifecycleStage.EXECUTION_DISPUTE,
            project_archetypes=[ProjectArchetype.EPC_CONTRACTING, ProjectArchetype.JV_CONSORTIUM],
            fidic_book_edition="1999_SILVER",
            host_country="印度尼西亚"
        ),
        security_alerts=[alert_infra, alert_tkdn],
        facts=facts,
        claims=claims,
        materials=materials,
        issues=issues,
        questions=questions,
        elements=elements,
        evidence=evidence,
        translations=translations,
        findings=findings,
        checks=checks,
        strategic_assessment=strategic_assessment,
        dashboard=dashboard
    )


def create_c102_case() -> CaseState:
    """C102: 越南沿海 350MW 海上风电股权并购 (M&A) + EPC 保函恶意索兑案"""
    alert_creeping = SecurityAlertItem(
        risk_level=SecurityRiskLevel.CRITICAL,
        category="creeping_expropriation",
        title_zh="越南电价补贴过渡期调整与特许权收益倒挂风险",
        fact_anchor_ids=["F2"],
        host_law_basis=["VN_LAW:135_2025_QH15:Art86", "VN_DECREE:210_2026_ND_CP"],
        prc_or_treaty_basis=["BIT_CHINA_ASEAN:Art6"],
        sinosure_preservation_guide="若东道国政策追溯下调上网电价致现金流断裂，须在 30 个自然日内向中国信保提交可能损失通知书，并启动《中越投资保护协定》磋商程序。",
        mandatory_human_checklist=["核实工贸部 MOIT 最新电价核准批文", "审查购电协议 PPA 与 EPC 合同电价传导条款"],
        mitigation_actions=["依据越南 2025 新建设法第 86.2 条将延误违约金上限严格锁定在合同金额 12%", "向 SIAC 申请紧急仲裁员保函止付令"]
    )

    facts = [
        Fact(fid="F1", text_zh="中资央企拟收购越南平顺省 350MW 沿海海上风电项目公司 70% 股权并承担 EPC 关联总承包。"),
        Fact(fid="F2", text_zh="项目履约期间，受越南工贸部 (MOIT) 关于 FIT 上网电价过渡期政策下调影响，项目公司面临投资收益率倒挂，且因季风台风遭遇不可抗力延误。"),
        Fact(fid="F3", text_zh="越南业主在商业运营日 (COD) 前夕，突发向新加坡星展银行发起 10% 见索即付履约保函全额索兑，并依据旧合同约定主张每日万分之五无上限的逾期违约金。")
    ]
    claims = [
        Claim(cid="C1", party="中资投资总包方", text_zh="依据越南《2025年新建设法》第 86.2 条及《第210/2026/ND-CP号建设合同法令》主张工期违约金上限严格受限于合同造价 12% 法定封顶。"),
        Claim(cid="C2", party="中资投资总包方", text_zh="依据台风不可抗力事由豁免逾期违约责任。"),
        Claim(cid="C3", party="中资投资总包方", text_zh="向 SIAC 申请紧急仲裁员 (EA) 全球保函止付临时禁令。")
    ]
    materials = [
        Material(mid="M1", name="越南海上风电股权收购协议(SPA)与关联EPC合同", desc_zh="平顺350MW风电项目收购协议及关联EPC工程总承包合同文本", fact_ids=["F1", "F3"]),
        Material(mid="M2", name="越南国家气象水文台台风不可抗力公报", desc_zh="越南官方气象局发布的台风不可抗力极端气候公报", fact_ids=["F2"])
    ]
    issues = [
        Issue(issue_id="I1", kind="law", text_zh="越南《2025新建设法》第 86.2 条预定违约金法定 12% 封顶是否具有强行法优先效力？", claim_ids=["C1"], element_ids=["e1"]),
        Issue(issue_id="I2", kind="law", text_zh="商业运营日前夕突发全额索兑履约保函是否构成 SIAC 紧急仲裁止付要件？", claim_ids=["C3"], element_ids=["e2"])
    ]
    questions = [
        LegalQuestion(
            qid="Q1",
            text_zh="越南 2025 新建设法下预定违约金封顶强行法适用与保函紧急仲裁止付构成要件？",
            template_id="asean_vn_wind_dispute",
            must_norms=["VN_LAW:135_2025_QH15:Art86", "VN_DECREE:210_2026_ND_CP", "BIT_CHINA_ASEAN:Art6"]
        )
    ]
    elements = [
        ElementState(qid="Q1", element_id="e1", name_zh="违约金计算超越法定 12% 强制封顶红线 (越南新建设法 86.2 条)", status="covered", fact_links=["F3"], material_links=["M1"], match_status="satisfied"),
        ElementState(qid="Q1", element_id="e2", name_zh="SIAC 紧急仲裁员管辖与履约保函恶意索兑不可弥补之损害", status="covered", fact_links=["F3"], material_links=["M1", "M2"], match_status="satisfied")
    ]
    evidence = {
        "E1": Evidence(eid="E1", kind="norm", ref_id="VN_LAW:135_2025_QH15:Art86", text_de="Luật Xây dựng số 135/2025/QH15 Điều 86.2: Mức phạt vi phạm hợp đồng xây dựng do các bên thỏa thuận nhưng không vượt quá 12% giá trị phần hợp đồng bị vi phạm.", source_url="https://vanban.chinhphu.vn", stand="2026-10-18", fetched_at="2026-10-18T20:00:00", grade="A"),
        "E2": Evidence(eid="E2", kind="norm", ref_id="VN_DECREE:210_2026_ND_CP", text_de="Nghị định số 210/2026/NĐ-CP: Hợp đồng EPC trong lĩnh vực năng lượng tái tạo phải quy định rõ cơ chế phân bổ rủi ro thay đổi chính sách giá điện và giới hạn bồi thường thiệt hại ấn định trước.", source_url="https://thuvienphapluat.vn", stand="2026-10-18", fetched_at="2026-10-18T20:00:00", grade="A")
    }
    translations = {
        "E1": "越南《2025年新建设法》（Law 135/2025/QH15）第86.2条：建设合同的违约罚金由双方协商约定，但最高不得超过违约合同部分价值的 12%。",
        "E2": "越南政府《第210/2026/ND-CP号建设合同法令》：可再生能源领域 EPC 合同必须明确约定电价政策变更风险分担机制与预定损害赔偿上限。"
    }
    findings = [
        Finding(
            qid="Q1",
            statements=[
                Statement(sid="S1", text_zh="依据越南《2025年新建设法》第 86.2 条，业主主张无上限日万分之五违约金违反越南工程强行法，依法必须严格受限于违规造价 12% 之法定最高封顶线。", type="quote", evidence_ids=["E1"], fact_ids=["F3"], part="A", element_id="e1"),
                Statement(sid="S2", text_zh="针对保函索兑，建议在 SIAC 提交紧急仲裁员申请，结合台风不可抗力气象记录请求发布全球止付令，并依中信保指引做好报损留痕。", type="inference", evidence_ids=["E2"], fact_ids=["F2", "F3"], part="B", element_id="e2")
            ]
        )
    ]
    strategic_assessment = StrategicAssessment(
        case_id="C102",
        pivotal_factors=["越南 2025 新建设法关于 12% 违约金封顶之强行法适用", "台风不可抗力期间对 COD 商运日的合法顺延认定"],
        outcome_branches=[
            OutcomeBranch(
                branch_type="favorable",
                title="违约金封顶裁决与保函成功止付",
                condition_precedent="及时取得 SIAC 紧急仲裁员保全令并出具越南新法法定封顶抗辩",
                substantive_basis=["VN_LAW:135_2025_QH15:Art86"],
                outcome_summary="若仲裁庭支持新建设法第 86.2 条强行法效力，则业主要求的超额违约金将被全部剔除，保函索兑失去实质基础。",
                risk_level="low"
            )
        ],
        actionable_checklist=["向平顺省工贸厅报备台风不可抗力停工记录", "依中越 BIT 协定向越南政府发送条约磋商意向函"],
        updated_at="2026-10-18T20:00:00"
    )

    checks = [
        CheckItem(code="V1", status="pass", reason="法条均通过越南官方公报校验"),
        CheckItem(code="V2", status="pass", reason="无虚构法条"),
        CheckItem(code="V3", status="pass", reason="快照绑定 20261018-asean-v1.0"),
        CheckItem(code="V4", status="pass", reason="越南 2025 新建设法有效"),
        CheckItem(code="V5", status="pass", reason="东盟工程非货物买卖"),
        CheckItem(code="V6", status="pass", reason="越语/英语/中文三语对齐"),
        CheckItem(code="V7", status="pass", reason="FIDIC 核心条款对齐"),
        CheckItem(code="V8", status="pass", reason="客观中立"),
        CheckItem(code="V9", status="pass", reason="双包规范结构"),
        CheckItem(code="V10", status="pass", reason="事实闭环"),
        CheckItem(code="V11", status="pass", reason="Token 预算合规"),
        CheckItem(code="V12", status="pass", reason="已触发电价下调隐性征收预警，已生成中越 BIT 对冲建议")
    ]

    dashboard = DashboardMetrics(
        exact_quotes_ratio=(1, 2),
        norms_cases_exist_all=True,
        unresolved_refs_count=0,
        supported_statements_ratio=(2, 2),
        elements_coverage={"covered": 2, "partial": 0, "missing": 0},
        elements_match={"satisfied": 2, "partial": 0, "missing": 0, "disputed": 0},
        facts_traceable_ratio=(1, 1),
        entity_checks_pass_ratio=(1, 1),
        grades_distribution={"A": 2, "B": 0, "C": 0, "D": 0},
        timepoint_level="green",
        cisg_triggered=False,
        snapshot_id="20261018-asean-v1.0",
        report_version=1,
        content_hash="c102vnwindvalid2026hash"
    )

    return CaseState(
        case_id="C102",
        title="越南沿海350MW海上风电股权并购+EPC关联总包保函恶意索兑案",
        snapshot_id="20261018-asean-v1.0",
        mode="full",
        status="completed",
        facts_zh="中资央企拟收购越南平顺省 350MW 沿海海上风电项目公司 70% 股权并承担 EPC 关联总承包。项目履约期间，受越南工贸部 (MOIT) 关于 FIT 上网电价过渡期政策下调影响，项目公司面临投资收益率倒挂，且因季风台风遭遇不可抗力延误。越南业主在商业运营日 (COD) 前夕，突发向新加坡星展银行发起 10% 见索即付履约保函全额索兑，并依据旧合同约定主张每日万分之五无上限的逾期违约金。",
        claims_zh="1. 依据越南《2025年新建设法》第 86.2 条及《第210/2026/ND-CP号建设合同法令》主张工期违约金上限严格受限于合同造价 12% 法定封顶；2. 依据台风不可抗力事由豁免逾期违约责任；3. 依据中越双边投资保护协定 (BIT) 启动政府间电价追溯下调之公平公正待遇 (FET) 磋商；4. 向 SIAC 申请紧急仲裁员 (EA) 全球保函止付临时禁令。",
        meta=CaseMeta(
            title="越南海上风电股权并购与EPC保函索兑案",
            jurisdiction="asean_vn",
            contract_type="跨境股权收购与关联EPC工程合同",
            parties=["中资央企投资总包方", "越南平顺风电业主公司"],
            choice_of_law="越南法与新加坡SIAC仲裁",
            lifecycle_stage=LifecycleStage.PRE_INVESTMENT,
            project_archetypes=[ProjectArchetype.CROSS_BORDER_MA, ProjectArchetype.EPC_CONTRACTING],
            host_country="越南"
        ),
        security_alerts=[alert_creeping],
        facts=facts,
        claims=claims,
        materials=materials,
        issues=issues,
        questions=questions,
        elements=elements,
        evidence=evidence,
        translations=translations,
        findings=findings,
        checks=checks,
        strategic_assessment=strategic_assessment,
        dashboard=dashboard
    )


def create_c103_case() -> CaseState:
    """C103: 马来西亚吉隆坡轨道交通枢纽 CIPAA 快速法定裁决与背靠背条款绝对无效案"""
    alert_cipaa = SecurityAlertItem(
        risk_level=SecurityRiskLevel.HIGH,
        category="national_security_review",
        title_zh="马来西亚 CIPAA 极速裁决与背靠背付款条款法定无效红线",
        fact_anchor_ids=["F2"],
        host_law_basis=["MY_CIPAA:Sec35", "MY_CIPAA:Sec13", "SG_CASE:BS_Mount_Sophia"],
        prc_or_treaty_basis=["PRC_SASAC:Order35"],
        sinosure_preservation_guide="CIPAA 裁决具有法定极速执行力，若开立银行保函被索兑，须同时向新加坡高院申请显失公平保函止付禁令。",
        mandatory_human_checklist=["核实分包合同中是否包含 Pay-when-paid 条款", "核查 AIAC 裁决答辩 10 日法定截止时效"],
        mitigation_actions=["向马方业主发起 CIPAA 快速裁决追偿 4,500 万令吉", "依据 BS Mount Sophia 先例申请保函止付禁令"]
    )

    facts = [
        Fact(fid="F1", text_zh="吉隆坡轻轨与商业综合交通枢纽 EPC 工程中，马方业主拖欠中资总承包商第 14 期至 18 期工程进度款达 4,500 万令吉。"),
        Fact(fid="F2", text_zh="中资总承包商因未获业主付款，援引总分包合同中约定的'收到业主款项后方可付款（Pay-when-paid / 背靠背）'条款，暂缓向属地土著机电分包商支付款项。"),
        Fact(fid="F3", text_zh="该土著分包商依据马来西亚《2012年建筑业付款与快速裁决法》（CIPAA 2012）向 AIAC 发起极速裁决，主张背靠背条款依据 CIPAA 第 35 条自始绝对无效，要求总承包商 21 天内付清全款。"),
        Fact(fid="F4", text_zh="与此同时，马方业主向新加坡开证行申请索兑中资总承包商开立的履约保函。")
    ]
    claims = [
        Claim(cid="C1", party="中资总承包商", text_zh="确认 CIPAA 2012 第 35 条强行法下背靠背条款无效法律后果及工程抗辩权。"),
        Claim(cid="C2", party="中资总承包商", text_zh="依据 CIPAA 第 13 条主张向业主快速追偿 4,500 万令吉并执行法定停工权。"),
        Claim(cid="C3", party="中资总承包商", text_zh="依据新加坡高等法院 BS Mount Sophia / JBE Properties 先例确立之'显失公平（Unconscionability）'标准，向新加坡高院申请保函止付禁令。")
    ]
    materials = [
        Material(mid="M1", name="吉隆坡轻轨项目EPC主合同及分包协议", desc_zh="轻轨交通枢纽EPC主合同与机电专业分包协议文本", fact_ids=["F1", "F2"]),
        Material(mid="M2", name="AIAC快速裁决通知书及催告清单", desc_zh="亚洲国际仲裁中心AIAC登记之CIPAA法定快速裁决申请书", fact_ids=["F3", "F4"])
    ]
    issues = [
        Issue(issue_id="I1", kind="law", text_zh="CIPAA 2012 第 35 条是否强制否定涉外总分包背靠背付款条款？总承包商应如何向业主追偿？", claim_ids=["C1", "C2"], element_ids=["e1"]),
        Issue(issue_id="I2", kind="law", text_zh="业主在严重拖欠工程款情况下索兑保函，是否构成新加坡法下 BS Mount Sophia 确立的显失公平 (Unconscionability) 止付标准？", claim_ids=["C3"], element_ids=["e2"])
    ]
    questions = [
        LegalQuestion(
            qid="Q1",
            text_zh="马来西亚 CIPAA 35 条反背靠背效力及新加坡 BS Mount Sophia 保函止付标准？",
            template_id="asean_my_cipaa_dispute",
            must_norms=["MY_CIPAA:Sec35", "MY_CIPAA:Sec13", "SG_CASE:BS_Mount_Sophia"]
        )
    ]
    elements = [
        ElementState(qid="Q1", element_id="e1", name_zh="CIPAA 2012 第 35 条宣告背靠背付款条款绝对无效 (Void)", status="covered", fact_links=["F2", "F3"], material_links=["M1"], match_status="satisfied"),
        ElementState(qid="Q1", element_id="e2", name_zh="新加坡高院 BS Mount Sophia 确立之独立保函显失公平止付要件", status="covered", fact_links=["F1", "F4"], material_links=["M1", "M2"], match_status="satisfied")
    ]
    evidence = {
        "E1": Evidence(eid="E1", kind="norm", ref_id="MY_CIPAA:Sec35", text_de="CIPAA 2012 Section 35(1): Any conditional payment clause, including pay when paid or pay if paid, shall be void and of no effect in any construction contract.", source_url="https://lom.agc.gov.my", stand="2026-10-18", fetched_at="2026-10-18T20:00:00", grade="A"),
        "E2": Evidence(eid="E2", kind="norm", ref_id="MY_CIPAA:Sec13", text_de="CIPAA 2012 Section 13: An adjudication decision is immediately binding and enforceable as a High Court judgment, entitling the claimant to suspend works.", source_url="https://lom.agc.gov.my", stand="2026-10-18", fetched_at="2026-10-18T20:00:00", grade="A"),
        "E3": Evidence(eid="E3", kind="case", ref_id="SG_CASE:BS_Mount_Sophia", text_de="BS Mount Sophia Pte Ltd v Join-Aim Pte Ltd [2012] SGCA 28: Singapore law recognizes unconscionability as a separate ground from fraud for restraining calls on performance bonds.", source_url="https://elitigation.sg", stand="2026-10-18", fetched_at="2026-10-18T20:00:00", grade="A")
    }
    translations = {
        "E1": "马来西亚《2012年建筑业付款与快速裁决法》（CIPAA）第35条：任何附条件的付款条款，包括“按期付款（pay when paid）”或“若付即付（pay if paid）”，在所有建设工程合同中一律无效且不具法律效力。",
        "E2": "CIPAA 2012 第13条：快速裁决决定自作出起立即具备强制约束力，可作为高等法院判决直接执行，且胜诉方有权据此行使工程停工权。",
        "E3": "新加坡上诉法院 *BS Mount Sophia v Join-Aim* [2012] SGCA 28：新加坡法律明确承认“显失公平（Unconscionability）”可独立于欺诈作为法院裁定禁止索兑见索即付履约保函的合法裁判事由。"
    }
    findings = [
        Finding(
            qid="Q1",
            statements=[
                Statement(sid="S1", text_zh="依据马来西亚《CIPAA 2012》第 35 条，总包商针对本地分包商主张的背靠背付款条款已被该国强行法绝对废止，分包商极速裁决胜算极高；总包商必须依据第 13 条同时向马方业主发起反向快速裁决追讨 4,500 万令吉并主张合规抗辩。", type="quote", evidence_ids=["E1", "E2"], fact_ids=["F1", "F2", "F3"], part="A", element_id="e1"),
                Statement(sid="S2", text_zh="鉴于马方业主在恶意拖欠数千万工程进度款的同时强行索兑保函，完全契合新加坡 *BS Mount Sophia* 先例项下的显失公平 (Unconscionability) 标准，建议立即向新加坡高院申请保函紧急止付禁令进行资金保全与反制抗辩。", type="quote", evidence_ids=["E3"], fact_ids=["F1", "F4"], part="B", element_id="e2")
            ]
        )
    ]
    strategic_assessment = StrategicAssessment(
        case_id="C103",
        pivotal_factors=["CIPAA 35 条背靠背条款绝对无效强行法", "新加坡 BS Mount Sophia 显失公平保函止付标准"],
        outcome_branches=[
            OutcomeBranch(
                branch_type="favorable",
                title="保函成功止付并对业主实现快速裁决强制执行与资产保全",
                condition_precedent="在新加坡高院举证业主严重拖欠进度款之恶意行为并取得 injunction",
                substantive_basis=["SG_CASE:BS_Mount_Sophia", "MY_CIPAA:Sec13"],
                outcome_summary="若新加坡高院认定业主滥用索兑权构成显失公平，将签发止付禁令完成资金保全；同时总包商在马来西亚获得 4,500 万令吉快速裁决并享有法定停工抗辩权。",
                risk_level="low"
            )
        ],
        actionable_checklist=["向新加坡高等法院递交紧急保函止付禁令申请状并保全资产", "在 AIAC 启动针对马方业主的 CIPAA 快速追偿与抗辩程序"],
        updated_at="2026-10-18T20:00:00"
    )

    checks = [
        CheckItem(code="V1", status="pass", reason="法条均通过马/新官方库校验"),
        CheckItem(code="V2", status="pass", reason="无虚构法条"),
        CheckItem(code="V3", status="pass", reason="快照绑定 20261018-asean-v1.0"),
        CheckItem(code="V4", status="pass", reason="CIPAA 与 BS Mount Sophia 有效"),
        CheckItem(code="V5", status="pass", reason="东盟工程非货物买卖"),
        CheckItem(code="V6", status="pass", reason="英文与中文双语对齐"),
        CheckItem(code="V7", status="pass", reason="保函与背靠背强行法对齐"),
        CheckItem(code="V8", status="pass", reason="客观中立"),
        CheckItem(code="V9", status="pass", reason="双包规范结构"),
        CheckItem(code="V10", status="pass", reason="事实闭环"),
        CheckItem(code="V11", status="pass", reason="Token 预算合规"),
        CheckItem(code="V12", status="pass", reason="已触发 CIPAA 强行法预警，已生成新加坡高院保函止付对冲方案")
    ]

    dashboard = DashboardMetrics(
        exact_quotes_ratio=(2, 2),
        norms_cases_exist_all=True,
        unresolved_refs_count=0,
        supported_statements_ratio=(2, 2),
        elements_coverage={"covered": 2, "partial": 0, "missing": 0},
        elements_match={"satisfied": 2, "partial": 0, "missing": 0, "disputed": 0},
        facts_traceable_ratio=(1, 1),
        entity_checks_pass_ratio=(1, 1),
        grades_distribution={"A": 3, "B": 0, "C": 0, "D": 0},
        timepoint_level="green",
        cisg_triggered=False,
        snapshot_id="20261018-asean-v1.0",
        report_version=1,
        content_hash="c103mycipaavalid2026hash"
    )

    return CaseState(
        case_id="C103",
        title="马来西亚吉隆坡轨道交通枢纽CIPAA法定快速裁决与背靠背付款绝对无效案",
        snapshot_id="20261018-asean-v1.0",
        mode="full",
        status="completed",
        facts_zh="吉隆坡轻轨与商业综合交通枢纽 EPC 工程中，马方业主拖欠中资总承包商第 14 期至 18 期工程进度款达 4,500 万令吉。中资总承包商因未获业主付款，援引总分包合同中约定的'收到业主款项后方可付款（Pay-when-paid / 背靠背）'条款，暂缓向属地土著机电分包商支付款项。该土著分包商依据马来西亚《2012年建筑业付款与快速裁决法》（CIPAA 2012）向 AIAC 发起极速裁决，主张背靠背条款依据 CIPAA 第 35 条自始绝对无效，要求总承包商 21 天内付清全款。与此同时，马方业主向新加坡开证行申请索兑中资总承包商开立的履约保函。",
        claims_zh="1. 确认 CIPAA 2012 第 35 条强行法下背靠背条款无效法律后果及工程抗辩权；2. 依据 CIPAA 第 13 条主张向业主快速追偿 4,500 万令吉并执行法定停工权；3. 依据新加坡高等法院 BS Mount Sophia / JBE Properties 先例确立之'显失公平（Unconscionability）'标准，向新加坡高院申请保函止付禁令。",
        meta=CaseMeta(
            title="马来西亚轨道枢纽CIPAA裁决与保函止付案",
            jurisdiction="asean_my",
            contract_type="国际工程EPC总承包与专业分包合同",
            parties=["中资总承包商", "马来西亚业主与属地分包商"],
            choice_of_law="马来西亚实体法与新加坡法律",
            lifecycle_stage=LifecycleStage.EXECUTION_DISPUTE,
            project_archetypes=[ProjectArchetype.EPC_CONTRACTING],
            host_country="马来西亚"
        ),
        security_alerts=[alert_cipaa],
        facts=facts,
        claims=claims,
        materials=materials,
        issues=issues,
        questions=questions,
        elements=elements,
        evidence=evidence,
        translations=translations,
        findings=findings,
        checks=checks,
        strategic_assessment=strategic_assessment,
        dashboard=dashboard
    )


def create_c104_case() -> CaseState:
    """C104: 菲律宾跨海大桥 PPP 特许经营换届单方停工 (隐性征收) 与 PCAB 资质合规案"""
    alert_expropriation = SecurityAlertItem(
        risk_level=SecurityRiskLevel.CRITICAL,
        category="creeping_expropriation",
        title_zh="菲律宾跨海大桥特许经营政府换届单方废约与隐性征收预警",
        fact_anchor_ids=["F2"],
        host_law_basis=["PH_RA:11966:PPP_Code", "PH_SC:GR217590_ManilaWater"],
        prc_or_treaty_basis=["BIT_CHINA_ASEAN:Art6", "PRC_SASAC:Order35"],
        sinosure_preservation_guide="政府换届后单方发布停工令并拒绝补偿构成准征收 (Creeping Expropriation)，必须在 30 个自然日内向中国信保正式提交可能损失通知书并保全代位求偿权。",
        mandatory_human_checklist=["核实菲律宾公共工程与公路部 DPWH 停工令行政文书", "核验 PCAB 施工执照年审备案及合资协议股权架构"],
        mitigation_actions=["依据菲律宾《PPP法典》(RA 11966) 主张提前终止补偿金（含沉没成本与合理预期收益）", "援引最高院 Manila Water 案判例驳回外资持股违规抗辩", "启动中菲双边投资协定 ICSID 国际投资仲裁"]
    )
    alert_sec = SecurityAlertItem(
        risk_level=SecurityRiskLevel.HIGH,
        category="national_security_review",
        title_zh="战略海峡基础设施外资国安审查与公共服务法合规",
        fact_anchor_ids=["F2"],
        host_law_basis=["PH_RA:11659"],
        prc_or_treaty_basis=["PRC_DATA_SEC:Art36"],
        sinosure_preservation_guide="战略工程地质图纸若遭境外调证，严格受限于我国数据安全法第 36 条，严禁未经审批出境。",
        mandatory_human_checklist=["审查施工图纸与地质测绘数据是否涉及主权海域敏感信息"],
        mitigation_actions=["聘请菲律宾本土合规顾问出具 RA 11659 国家安全审查非核心要害审查意见"]
    )

    facts = [
        Fact(fid="F1", text_zh="中资基建联合体与菲律宾公共工程与公路部 (DPWH) 签署某战略跨海大桥 30 年 PPP 特许经营协议并总包施工。"),
        Fact(fid="F2", text_zh="菲律宾新一届政府换届后，国家安全委员会以项目靠近敏感海军基地且涉及关键基础设施国家安全审查为由，单方发布行政停工令暂停特许权协议，并拒绝按照原合同补偿前期投资沉没成本。"),
        Fact(fid="F3", text_zh="同时，菲律宾当地承包商行业协会向菲律宾建筑业执照委员会 (PCAB) 举报中资联合体外资持股超标、违反施工资质牌照红线，主张特许经营合同因违法自始无效。")
    ]
    claims = [
        Claim(cid="C1", party="中资基建联合体", text_zh="依据菲律宾《PPP法典》（RA 11966，全面替代旧 BOT 法）主张政府单方终止特许经营权之公允重置成本与预期收益法定补偿。"),
        Claim(cid="C2", party="中资基建联合体", text_zh="依据菲律宾最高法院里程碑判例 PCAB v. Manila Water (G.R. No. 217590) 确立之规则，反驳外资持股超标导致资质无效的主张。"),
        Claim(cid="C3", party="中资基建联合体", text_zh="依据《中菲双边投资协定》(BIT) 第 4 条启动征收补偿国际仲裁 (ICSID)。"),
        Claim(cid="C4", party="中资基建联合体", text_zh="依照中国信保（Sinosure）海外投资违约险指引在 30 日内提交可能损失通知书并保全代位求偿权。")
    ]
    materials = [
        Material(mid="M1", name="菲律宾跨海大桥PPP特许经营协议与政府保证函", desc_zh="公私合营PPP特许权主协议与菲律宾财政部政府保证函", fact_ids=["F1", "F2"]),
        Material(mid="M2", name="DPWH行政停工令与国家安全委员会备忘录", desc_zh="菲律宾公工部单方行政暂停特许权通知书", fact_ids=["F2"]),
        Material(mid="M3", name="PCAB特别施工许可证及最高法院Manila Water判决引述", desc_zh="菲律宾建筑业执照委员会特别资质证书及Manila Water先例", fact_ids=["F3"])
    ]
    issues = [
        Issue(issue_id="I1", kind="law", text_zh="菲律宾《PPP法典》(RA 11966) 下政府因国家安全单方提前终止特许经营权的法定补偿构成要件？", claim_ids=["C1", "C3"], element_ids=["e1"]),
        Issue(issue_id="I2", kind="law", text_zh="菲律宾最高法院 Manila Water 先例如何推翻外资持股限制并保障 PCAB 执照有效性？", claim_ids=["C2"], element_ids=["e2"])
    ]
    questions = [
        LegalQuestion(
            qid="Q1",
            text_zh="菲律宾 PPP 法典下政府换届废约补偿标准与 Manila Water 先例资质抗辩？",
            template_id="asean_ph_ppp_expropriation",
            must_norms=["PH_RA:11966:PPP_Code", "PH_SC:GR217590_ManilaWater", "BIT_CHINA_ASEAN:Art6"]
        )
    ]
    elements = [
        ElementState(qid="Q1", element_id="e1", name_zh="菲律宾《PPP法典》(RA 11966) 政府原因终止法定补偿要件（实际投资+合理溢价）", status="covered", fact_links=["F1", "F2"], material_links=["M1", "M2"], match_status="satisfied"),
        ElementState(qid="Q1", element_id="e2", name_zh="最高法院 PCAB v. Manila Water 废除外资常规执照股权限制先例效力", status="covered", fact_links=["F3"], material_links=["M3"], match_status="satisfied")
    ]
    evidence = {
        "E1": Evidence(eid="E1", kind="norm", ref_id="PH_RA:11966:PPP_Code", text_de="Republic Act No. 11966 (The PPP Code of the Philippines): In case of unilateral termination by the Government for reasons other than Contractor default, the Implementing Agency shall pay fair compensation covering sunk costs, demobilization, and loss of reasonable expected future earnings.", source_url="https://officialgazette.gov.ph", stand="2026-10-18", fetched_at="2026-10-18T20:00:00", grade="A"),
        "E2": Evidence(eid="E2", kind="case", ref_id="PH_SC:GR217590_ManilaWater", text_de="Philippine Contractors Accreditation Board (PCAB) v. Manila Water Company, Inc., G.R. No. 217590: The Supreme Court held that nationality restrictions imposed on regular contractor licenses under PCAB rules were unconstitutional and void.", source_url="https://sc.judiciary.gov.ph", stand="2026-10-18", fetched_at="2026-10-18T20:00:00", grade="A"),
        "E3": Evidence(eid="E3", kind="norm", ref_id="BIT_CHINA_ASEAN:Art6", text_de="ASEAN-China Comprehensive Economic Cooperation Investment Agreement Article 6: Neither Contracting Party shall expropriate or nationalize investments unless for public purpose, non-discriminatory, and upon prompt, adequate and effective compensation.", source_url="https://asean.org", stand="2026-10-18", fetched_at="2026-10-18T20:00:00", grade="A")
    }
    translations = {
        "E1": "菲律宾共和国《公私合营法典》（RA 11966，PPP Code）：若政府因非承包商违约原因单方面终止特许协议，执行机构必须向项目公司支付公允补偿金，全额覆盖前期沉没成本、遣散费用及合理的预期未来收益损失。",
        "E2": "菲律宾最高法院 *PCAB 诉 Manila Water 公司* 案（G.R. No. 217590）：最高法院裁定 PCAB 规章中对常规承包商许可证强加的 60% 菲律宾国籍股权限制违宪并无效，外资企业有权依法平等获取工程执照。",
        "E3": "《中国-东盟全面经济合作框架协议投资协议》第6条【征收与补偿】：任何缔约方均不得对缔约另一方投资者的投资采取征收、国有化或具有同等效力的间接征收措施，除非出于公共利益、基于非歧视原则并给予迅速、充分、有效的公允市场价值补偿。"
    }
    findings = [
        Finding(
            qid="Q1",
            statements=[
                Statement(sid="S1", text_zh="依据菲律宾《PPP法典》(RA 11966) 及中国-东盟 BIT 投资协定第 6 条，菲政府单方以国家安全为由暂停特许权协议构成实质性单方废约与隐性征收，项目公司依法享有全额追偿前期沉没成本与公允未来收益的法定权利。", type="quote", evidence_ids=["E1", "E3"], fact_ids=["F1", "F2"], part="A", element_id="e1"),
                Statement(sid="S2", text_zh="菲律宾最高法院在 *PCAB v. Manila Water* 里程碑判例中已判定外资股权比例限制规则违宪无效，当地行会以资质违法为由主张特许经营合同无效的指控在法律上不能成立。", type="quote", evidence_ids=["E2"], fact_ids=["F3"], part="A", element_id="e2"),
                Statement(sid="S3", text_zh="针对特许权单方停工风险，严格执行中国信保 30 日内提交可能损失通知书程序，为后续向 ICSID 申请国际投资仲裁及中信保保全代位求偿权夯实证据闭环。", type="inference", evidence_ids=["E3"], fact_ids=["F2"], part="B", element_id="e1")
            ]
        )
    ]
    strategic_assessment = StrategicAssessment(
        case_id="C104",
        pivotal_factors=["菲律宾新 PPP 法典 RA 11966 之单方终止补偿机制", "最高法院 Manila Water 判例对外资承包资质的保障效力"],
        outcome_branches=[
            OutcomeBranch(
                branch_type="favorable",
                title="公允投资补偿与中信保全额赔付双重保障",
                condition_precedent="在 30 日出险时限内完成信保报损留痕并递交 ICSID 投资仲裁意向通知",
                substantive_basis=["PH_RA:11966:PPP_Code", "BIT_CHINA_ASEAN:Art6"],
                outcome_summary="若菲政府拒绝协议补偿，中资联合体可依据中菲 BIT 向 ICSID 提起国际投资仲裁，主张公允市场价值征收补偿，并由中信保海外投资险保全兜底。",
                risk_level="low"
            )
        ],
        actionable_checklist=["在 30 个自然日内向中国信保提交海外投资险正式《可能损失通知书》", "向菲律宾国家安全委员会与 DPWH 发送条约保护抗辩律师函"],
        updated_at="2026-10-18T20:00:00"
    )

    checks = [
        CheckItem(code="V1", status="pass", reason="法条均通过菲律宾官方公报与最高法院判例库校验"),
        CheckItem(code="V2", status="pass", reason="无虚构法条"),
        CheckItem(code="V3", status="pass", reason="快照绑定 20261018-asean-v1.0"),
        CheckItem(code="V4", status="pass", reason="RA 11966 与 Manila Water 判例有效"),
        CheckItem(code="V5", status="pass", reason="东盟工程非货物买卖"),
        CheckItem(code="V6", status="pass", reason="英文与中文双语对齐"),
        CheckItem(code="V7", status="pass", reason="FIDIC 与 PPP 法典对齐"),
        CheckItem(code="V8", status="pass", reason="客观中立"),
        CheckItem(code="V9", status="pass", reason="双包规范结构"),
        CheckItem(code="V10", status="pass", reason="事实闭环"),
        CheckItem(code="V11", status="pass", reason="Token 预算合规"),
        CheckItem(code="V12", status="pass", reason="已触发特许经营单方废约重大隐性征收预警，已生成中信保 30 日出险报损保全与 ICSID 仲裁对冲策略")
    ]

    dashboard = DashboardMetrics(
        exact_quotes_ratio=(2, 3),
        norms_cases_exist_all=True,
        unresolved_refs_count=0,
        supported_statements_ratio=(3, 3),
        elements_coverage={"covered": 2, "partial": 0, "missing": 0},
        elements_match={"satisfied": 2, "partial": 0, "missing": 0, "disputed": 0},
        facts_traceable_ratio=(1, 1),
        entity_checks_pass_ratio=(1, 1),
        grades_distribution={"A": 3, "B": 0, "C": 0, "D": 0},
        timepoint_level="green",
        cisg_triggered=False,
        snapshot_id="20261018-asean-v1.0",
        report_version=1,
        content_hash="c104phpppvalid2026hash"
    )

    return CaseState(
        case_id="C104",
        title="菲律宾跨海大桥PPP特许经营换届单方停工与PCAB资质合规案",
        snapshot_id="20261018-asean-v1.0",
        mode="full",
        status="completed",
        facts_zh="中资基建联合体与菲律宾公共工程与公路部 (DPWH) 签署某战略跨海大桥 30 年 PPP 特许经营协议并总包施工。菲律宾新一届政府换届后，国家安全委员会以项目靠近敏感海军基地且涉及关键基础设施国家安全审查为由，单方发布行政停工令暂停特许权协议，并拒绝按照原合同补偿前期投资沉没成本。同时，菲律宾当地承包商行业协会向菲律宾建筑业执照委员会 (PCAB) 举报中资联合体外资持股超标、违反施工资质牌照红线，主张特许经营合同因违法自始无效。",
        claims_zh="1. 依据菲律宾《PPP法典》（RA 11966，全面替代旧 BOT 法）主张政府单方终止特许经营权之公允重置成本与预期收益法定补偿；2. 依据菲律宾最高法院里程碑判例 PCAB v. Manila Water (G.R. No. 217590) 确立之规则，反驳外资持股超标导致资质无效的主张；3. 依据《中菲双边投资协定》(BIT) 第 4 条启动征收补偿国际仲裁 (ICSID)；4. 依照中国信保（Sinosure）海外投资违约险指引在 30 日内提交可能损失通知书并保全代位求偿权。",
        meta=CaseMeta(
            title="菲律宾跨海大桥PPP特许经营换届单方停工案",
            jurisdiction="asean_ph",
            contract_type="跨海大桥特许经营(PPP)+EPC总承包",
            parties=["中资基建联合体", "菲律宾公工部 DPWH"],
            choice_of_law="菲律宾法与中菲双边投资协定",
            lifecycle_stage=LifecycleStage.PRE_INVESTMENT,
            project_archetypes=[ProjectArchetype.PPP_CONCESSION, ProjectArchetype.EPC_CONTRACTING],
            host_country="菲律宾"
        ),
        security_alerts=[alert_expropriation, alert_sec],
        facts=facts,
        claims=claims,
        materials=materials,
        issues=issues,
        questions=questions,
        elements=elements,
        evidence=evidence,
        translations=translations,
        findings=findings,
        checks=checks,
        strategic_assessment=strategic_assessment,
        dashboard=dashboard
    )


def seed_asean_demo_cases(db: StateDBManager, overwrite: bool = False):
    """向数据库播种 C101~C104 东盟四大金标准标杆案例"""
    existing_ids = {c.case_id for c in db.list_cases()}
    
    cases_map = [
        ("C101", create_c101_case),
        ("C102", create_c102_case),
        ("C103", create_c103_case),
        ("C104", create_c104_case)
    ]
    for cid, fn in cases_map:
        if cid not in existing_ids or overwrite:
            case = fn()
            db.save_case(case, title=case.title)
            logger.info(f"Successfully seeded ASEAN Case {cid}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    db = StateDBManager("data/state.sqlite")
    seed_asean_demo_cases(db, overwrite=True)
    print("ASEAN demonstration cases C101~C104 seeded successfully!")
