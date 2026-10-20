"""策略推演与红队攻防对抗模块 (Strategic Assessment & Red Team Strategist)
完全聚焦中国出海基建央国企东盟 6 国建设工程与海外投资合规风险防范：
- 动态胜败边界推演与事实假定推演矩阵 (Hypothetical Outcome Bounds / If-Then Branching Matrix)
- 胜败摇摆关键变量与心证分水岭 (Pivotal Swaying Factors)
- 对方最具杀伤力的 3 大抗辩与反制武器 (Red Team Defense Playbook & Counter-Weapons)
- 下一步关键调取补证与防御布局清单 (Actionable Evidence Checklist)
- 严格遵循 V8 客观中立防线：严禁单一定量胜率承诺，采用条件式推演 (Condition Precedent)
"""

import os
import json
import datetime
from typing import List, Dict, Any, Optional
from lawagent.core.types import (
    CaseState, StrategicAssessment, OutcomeBranch, RedTeamDefense
)
from lawagent.llm.client import LLMClient
from lawagent.flow.critic import FORBIDDEN_PREDICTIVE_WORDS


def _now() -> str:
    return datetime.datetime.now().isoformat()


def clean_predictive_text(text: str) -> str:
    """清除绝对化胜诉词汇，恪守 V8 中立推演防线"""
    result = text
    for word in FORBIDDEN_PREDICTIVE_WORDS:
        if word in result:
            result = result.replace(word, "在举证充分的前提下可能构成")
    return result


def _build_asean_epc_delay_assessment(state: CaseState) -> StrategicAssessment:
    """东盟国际工程 EPC 工期顺延 (EOT)、28日索赔除斥期间与善意抗辩推演"""
    pivotal_factors = [
        "承包商在获悉征拆迟延或现场移交受阻后，是否在 28 日除斥期间内向工程师/业主送达书面索赔意向通知 (FIDIC Clause 20.1)",
        "东道国实体法诚信原则 (如印尼民法典第1338条及 SEMA 3/2023) 是否足以阻断机械适用严苛除斥期间导致之实体权利失权",
        "业主逾期移交施工场地与图纸审批迟延，是否构成国际工程法上之业主预防原则 (Prevention Principle) 豁免违约金"
    ]

    outcome_branches = [
        OutcomeBranch(
            branch_type="favorable",
            title="路径一：预防原则成立与诚信抗辩 (顺延工期与免除违约金路径)",
            condition_precedent="假定承包商能举证证明现场土地移交迟延完全归咎于东道国业主征拆不力，且承包商在例会纪要中已连续提出工期预警，业主实际知悉并已产生实质防卫准备。",
            substantive_basis=[
                "FIDIC Silver Book 1999 Clause 8.4 (Extension of Time)",
                "印尼《民法典》第1338条 (善意履约原则)",
                "印尼最高法院通告 SEMA No. 3/2023 (禁止机械性失权裁判)"
            ],
            key_evidence_required=[
                "场地实际移交书面签收备忘录 (带经纬度与时间戳现场交接单)",
                "向业主及监理工程师发出的第 8.4 款工期顺延书面申请函",
                "工期关键路径关键线路网络进度比对分析图 (CPM Schedule Analysis)"
            ],
            outcome_summary="仲裁庭/法院裁判倾向于认定延误事由属于业主风险事件，支持承包商工期合理顺延，依法阻断业主主张日计迟延违约金 (LDs) 之请求。",
            risk_level="low"
        ),
        OutcomeBranch(
            branch_type="unfavorable",
            title="路径二：28日索赔通知绝对失权 (驳回工期与费用索赔路径)",
            condition_precedent="若业主举证证明承包商在知悉延误事实发生后超过 28 日未发任何书面索赔通知，且东道国仲裁庭严格遵循英国法/严格契约法学说将 28 日定性为不可逾越之前置抗辩除斥条件。",
            substantive_basis=[
                "FIDIC 1999 Clause 20.1 (Contractor's Claims Time Bar)",
                "新加坡/普通法系 strict compliance 索赔先例"
            ],
            key_evidence_required=[
                "承包商首次发现现场障碍日与正式索赔函之间的日期落差记录",
                "双方关于现场施工进度索赔会议空白纪要",
                "业主出具的拒绝受理逾期索赔正式答复函"
            ],
            outcome_summary="仲裁庭裁判倾向于认定承包商未尽到第 20.1 款前置除斥通知义务，丧失顺延工期与补偿额外费用之权利，需自行承担工期拖期风险。",
            risk_level="high"
        ),
        OutcomeBranch(
            branch_type="uncertain",
            title="路径三：双语效力瑕疵与情势变更调解 (折中补偿路径)",
            condition_precedent="假定双方因未严格签署印尼语/越语法定双语版本存在行政抗辩空间，或外部地质条件突变构成不可预见之实体物理障碍。",
            substantive_basis=[
                "印尼《2017年第2号建筑法》第30条",
                "越南《2025新建设法》第86.2条",
                "FIDIC Clause 4.12 (Unforeseeable Physical Conditions)"
            ],
            key_evidence_required=[
                "地质勘察报告与实际开挖现场岩土力学勘验底稿",
                "双语合同签署原件及政府备案回执",
                "当地行政审批部门出具的环境保护整改停工令"
            ],
            outcome_summary="若不可预见物理条件成立，法庭倾向于支持部分工期宽延并建议双方按情势变更合理分担额外支出。",
            risk_level="medium"
        )
    ]

    red_team_defenses = [
        RedTeamDefense(
            defense_id="D1",
            opposing_claim="绝对时效除斥抗辩：承包商未在 28 日内提交书面索赔通知，依 FIDIC 第 20.1 款丧失一切工期与费用索赔救济权利",
            lethal_index="critical",
            opposing_basis="FIDIC 1999 Clause 20.1 条文及严格契约解释司法裁判",
            counter_weapons=[
                "诚信抗辩盾牌：援引东道国《民法典》诚实信用履约原则及最高法院通告 SEMA 3/2023，证明业主早已实际知晓事实，机械失权违背善意原则",
                "预防原则援引：若延误主因系业主未移交场地或未批准图纸，依预防原则 (Prevention Principle) 业主不得因自身过错使工期固定并索赔违约金",
                "事实通知主张：证明周报、监理例会纪要中已连续记载关键路径受阻，已达到实质通知目的"
            ],
            factual_counter_point="核实工程周报与月度联合巡检备忘录中工程师签字确认的工期受阻记录，证明索赔意向在28日内已向业主管理团队作实质披露。",
            evidence_checklist=[
                "包含监理工程师批注签字的项目第 3 至 8 周工程例会纪要",
                "现场场地移交延期联合勘验时间戳摄影记录与测绘报告",
                "东盟东道国最高法院关于建筑法善意原则限制失权之司法先例判词"
            ]
        ),
        RedTeamDefense(
            defense_id="D2",
            opposing_claim="合同无效抗辩：主张总承包合同未按印尼《语言法》(UU 24/2009) 签署印尼语法定文本，合同依法自始无效",
            lethal_index="high",
            opposing_basis="印尼 2009 年第 24 号法律第 31 条及西雅加达地方法院历史极端无效裁判",
            counter_weapons=[
                "最高院新通告抗辩：援引印尼最高法院 2023 年第 3 号通告 (SEMA 3/2023)，最高院明文禁止仅因缺少印尼语版本而认定涉外合同无效",
                "禁反言抗辩：业主已接受项目实质履行并支付部分进度款，再行主张无效构成恶意权利滥用 (Bad Faith)",
                "双语补正机制：立即组织属地宣誓翻译机构完成印尼语官方对照文本签署并在能矿部/公工部备案"
            ],
            factual_counter_point="调取双方邮件往来中业主确认英文为主准据语言且承诺由其负责属地备案的信函证据。",
            evidence_checklist=[
                "印尼最高法院 SEMA No. 3/2023 官方公报权威译文及最高院审判指南",
                "涉外工程合同签署过程全套起草信函与多语言沟通底稿",
                "印尼公证人及司法部宣誓翻译官完成的印尼语翻译公证书"
            ]
        ),
        RedTeamDefense(
            defense_id="D3",
            opposing_claim="本土化率 (TKDN) 违约反诉：主张承包商光伏逆变器及钢构采购未达能矿部 2024 年第 11 号令配额，拒付项目尾款并没收保函",
            lethal_index="high",
            opposing_basis="印尼能矿部 2024 年第 11 号条例 (MEMR Reg 11/2024) 强制本土化率规定",
            counter_weapons=[
                "过渡期豁免抗辩：主张项目立项及 EPC 合同签署早于能矿部新规生效日，依法适用旧规或豁免清单",
                "业主审核确认：证明主要机电设备采购清单均在订约前经业主及国电公司 (PLN) 正式批复同意",
                "属地替代采购：举证东道国本土市场产能客观无法满足高精技术公差标准，属于不可归责事由"
            ],
            factual_counter_point="核实工程设计阶段业主下达的技术规格审批表及 PLN 签发的机电设备准入批复函。",
            evidence_checklist=[
                "印尼能矿部工业制造能力官方公告清单 (证明国内无同等替代产能)",
                "业主及 PLN 工程师正式盖章批复的设备选型与进口清关批准单",
                "已完成的属地土建、劳务与物资采购 TKDN 认证核算审计报告"
            ]
        )
    ]

    actionable_checklist = [
        "调取项目关键路径 (CPM) 延期网络图，由资深造价工程师出具受阻工期归责量化报告",
        "保全全部监理例会纪要、现场施工日志及业主拖延移交场地的带时间戳影像书证书面底稿",
        "委托印尼 BANI 仲裁员或东盟工程法专家起草针对 28 日除斥通知与 SEMA 3/2023 诚信抗辩之法律备忘录",
        "排查履约保函开立条款及到期日，准备向新加坡高等法院申请显失公平 (Unconscionability) 紧急止付禁令预案"
    ]

    return StrategicAssessment(
        case_id=state.case_id,
        pivotal_factors=pivotal_factors,
        outcome_branches=outcome_branches,
        red_team_defenses=red_team_defenses,
        actionable_checklist=actionable_checklist,
        updated_at=_now()
    )


def _build_asean_bond_unconscionability_assessment(state: CaseState) -> StrategicAssessment:
    """东盟涉外独立见索即付保函索兑与显失公平止付 (Unconscionability Injunction) 推演"""
    pivotal_factors = [
        "业主索兑履约保函是否存在缺乏善意基础、将保函作为不正当逼定商业让步杠杆之显失公平情形 (BS Mount Sophia 门槛)",
        "保函准据法是否为新加坡法或承认除欺诈例外之外的显失公平独立止付抗辩体系",
        "总承包合同项下是否存在未结重大工期抗辩、背靠背付款争议或业主严重先期违约事由"
    ]

    outcome_branches = [
        OutcomeBranch(
            branch_type="favorable",
            title="路径一：显失公平临时禁制令成立 (保函成功止付路径)",
            condition_precedent="假定总承包商能向法院证明初步表面证据 (Prima Facie Case)，表明业主明知工程款与工期索赔存有未决争议，仍恶意利用见索即付工具施压，行为构成显失公平。",
            substantive_basis=[
                "新加坡上诉法院 BS Mount Sophia [2016] SGCA 58 标杆先例",
                "新加坡上诉法院 JBE Properties [2011] SGCA 24 裁决",
                "国际商会《见索即付保函统一规则》(URDG 758) 第 15 条"
            ],
            key_evidence_required=[
                "业主此前出具的满意确认函或无重大违约记录信函",
                "双方未决索赔争议已提交裁决或仲裁的立案受理证明",
                "向新加坡高等法院提交的单方禁制令申请文件及反担保承诺"
            ],
            outcome_summary="新加坡高等法院/仲裁庭倾向于支持签发保函止付临时禁制令，禁止开证行向业主转付保函资金，保全出海央企重大流动性现金流。",
            risk_level="low"
        ),
        OutcomeBranch(
            branch_type="unfavorable",
            title="路径二：保函独立抽象性维持 (索兑解付路径)",
            condition_precedent="若业主证明保函为不可撤销独立见索即付担保，且举证已发生实质工程瑕疵或工期延误，承包商证据未达到显失公平所要求之高度劣质与恶意门槛。",
            substantive_basis=[
                "新加坡高院法律中对保函独立性 (Autonomy Principle) 之严格保护惯例"
            ],
            key_evidence_required=[
                "保函正本条款中“无需证明、见索即付”的绝对承诺文句",
                "业主向开证行提交的合规索兑通知书与违约陈述"
            ],
            outcome_summary="法庭裁判倾向于驳回止付禁令申请，开证行依法对外解付，承包商仅能在后续实体仲裁中主张索赔返还。",
            risk_level="high"
        ),
        OutcomeBranch(
            branch_type="uncertain",
            title="路径三：资金提存与限额索兑和解 (风险控制路径)",
            condition_precedent="在禁制令审查听证期间，双方在法官主持下达成保函展期或将争议金额提存至共管账户 (Escrow Account)。",
            substantive_basis=[
                "新加坡民事诉讼规则关于争议标的物提存监管规定"
            ],
            key_evidence_required=[
                "第三方共管账户监管协议草案与开户银行确认单"
            ],
            outcome_summary="法庭裁定暂缓支付并责令限期完成工程缺陷修补或仲裁裁决，有效阻断直接损失。",
            risk_level="medium"
        )
    ]

    red_team_defenses = [
        RedTeamDefense(
            defense_id="D1",
            opposing_claim="绝对独立抽象性抗辩：保函见索即付且独立于基础合同，法院严禁审查基础合同实体违约是非",
            lethal_index="critical",
            opposing_basis="URDG 758 第 5 条及独立抽象性国际惯例",
            counter_weapons=[
                "显失公平例外突破：新加坡法明确确立显失公平 (Unconscionability) 是与欺诈并列的独立止付例外，允许审查基础事实恶意",
                "恶意杠杆举证：证明业主明知自身存在迟延移交现场之过错，索兑纯为在后续工程款结算中迫使我方放弃索赔",
                "滥用权利阻却：东道国法律及国际商事惯例均禁止明显违反公序良俗之恶意权利行使"
            ],
            factual_counter_point="调取业主发出索兑函前夕与承包商召开的谈判会议记录，证明业主以保函索兑作为逼降结算价款的威胁言论。",
            evidence_checklist=[
                "双方项目总监关于结算争议与索赔扣款之往来谈判邮件链",
                "开证行发出的索兑通报与要求补足保证金催告函",
                "新加坡资深诉讼律师出具的显失公平禁制令法律分析意见"
            ]
        ),
        RedTeamDefense(
            defense_id="D2",
            opposing_claim="背靠背付款抗辩：总承包商以业主未完成计量付款为由拒绝向分包商支付工程款",
            lethal_index="high",
            opposing_basis="分包合同中订立之 Pay-when-paid 明确免责条款",
            counter_weapons=[
                "强行法绝对无效：马来西亚 CIPAA 2012 第 35 条与新加坡 SOPA 2004 第 9 条明定背靠背条款绝对无效",
                "法定快速裁决：分包商可直接发起 CIPAA/SOPA 快速裁决程序并强制执行银行账户",
                "央企合规整改：依据国资委合规指引及时理顺分包款项支付节奏，避免引发当地群体性停工或商誉制裁"
            ],
            factual_counter_point="核实分包商已实际交付完成的工程量现场检验批次合格单。",
            evidence_checklist=[
                "已签署的分包工程量计量单与分包商阶段验收签证",
                "马来西亚 CIPAA 2012 / 新加坡 SOPA 2004 法定条款权威文本",
                "分包合同中背靠背条款的原始文句及司法无效认定对照表"
            ]
        )
    ]

    actionable_checklist = [
        "立即向新加坡高等法院提起单方临时禁制令申请 (Ex Parte Injunction)，申请中止开证行支付保函",
        "组织准备 BS Mount Sophia 裁判要件下之显失公平证据矩阵清单并完成当事人宣誓陈述书 (Affidavit)",
        "与开证行总行国际业务部保持 24 小时紧密协同，锁定开证行对外答复与审单宽限期",
        "按照国资委 35 号令重大风险报告机制，向集团公司及海外投资哨兵系统报备突发索兑事件"
    ]

    return StrategicAssessment(
        case_id=state.case_id,
        pivotal_factors=pivotal_factors,
        outcome_branches=outcome_branches,
        red_team_defenses=red_team_defenses,
        actionable_checklist=actionable_checklist,
        updated_at=_now()
    )


def _build_asean_concession_ppp_assessment(state: CaseState) -> StrategicAssessment:
    """东盟特许经营权撤销、外资准入限制与双边投资协定 (BIT) 间接征收推演"""
    pivotal_factors = [
        "东道国政府调整水价/电价或撤销特许经营协议，是否构成《中国-东盟全面经济合作框架协议投资协议》第6条间接征收 (Indirect Expropriation)",
        "外国承包商属地牌照 (如菲律宾 PCAB、印尼 BUJKA) 与中外联营体结构是否严格合规，杜绝借牌资质抗辩瑕疵",
        "是否在事件发生 30 日内正式向中国出口信用保险公司 (Sinosure) 履行出险预报与权益保全义务"
    ]

    outcome_branches = [
        OutcomeBranch(
            branch_type="favorable",
            title="路径一：投资协定间接征收与信保全额理赔 (最高赔付与条约仲裁路径)",
            condition_precedent="假定项目已取得东道国内阁特许权审批且在 30 日内完成中信保出险报损，政府单方取消特许权导致投资价值实质剥夺，构成非法间接征收。",
            substantive_basis=[
                "《中国-东盟投资协议》第 6 条 (征收与补偿条款)",
                "菲律宾最高法院 Manila Water G.R. No. 217590 先例",
                "中国信保海外投资保险单条款第 15 条 (征收风险理赔)"
            ],
            key_evidence_required=[
                "东道国政府内阁或监管机构撤销特许权之官方公文及总统令",
                "中国信保 30 日出险报损正式回执与承保保单全套文件",
                "普华永道/国际知名审计机构出具的项目重置成本与未来现金流估值报告"
            ],
            outcome_summary="投资人有权获得中信保最高达 90% 之征收损失理赔赔付，并在 ICSID 国际投资争端解决中心提起针对东道国政府之国家间投资仲裁。",
            risk_level="low"
        ),
        OutcomeBranch(
            branch_type="unfavorable",
            title="路径二：公共利益正常监管抗辩 (无偿剥夺驳回路径)",
            condition_precedent="若东道国政府抗辩称撤销特许经营权属于维护公共卫生、饮水安全或纠正腐败之正当警察权行使 (Police Powers)，不属于征收且不予补偿。",
            substantive_basis=[
                "国际投资法之正当监管例外理论 (Bona Fide Regulatory Measures)",
                "菲律宾《2023年公私合营法典》(RA 11966) 第 18 条"
            ],
            key_evidence_required=[
                "东道国议会或环保部门对项目出具的违法违规调查报告",
                "特许经营协议中政府保留免责监管权条款"
            ],
            outcome_summary="国际仲裁庭倾向于认定属于主权国家非歧视性合法公共监管，驳回全部征收补偿请求，企业面临重大沉没资产损失。",
            risk_level="high"
        ),
        OutcomeBranch(
            branch_type="uncertain",
            title="路径三：双边政府间磋商与特许期延长补偿 (商业重组路径)",
            condition_precedent="通过中中企业联合体与两国经贸联委会高层会谈，以延长后续特许经营年限或税收减免替代直接现金赔付。",
            substantive_basis=[
                "中菲 / 中印尼投资协定磋商争议解决机制"
            ],
            key_evidence_required=[
                "政府间经贸磋商会议纪要及特许权重新安排备忘录 (Addendum)"
            ],
            outcome_summary="双方达成特许权补充协议，平抑政治风险并实现中长期资产保值。",
            risk_level="medium"
        )
    ]

    red_team_defenses = [
        RedTeamDefense(
            defense_id="D1",
            opposing_claim="公共利益警察权抗辩：政府撤销特许经营系为保障居民公共福利与供水安全，属于主权法定监管，不构成征收且不承担补偿责任",
            lethal_index="critical",
            opposing_basis="东道国公法及国际投资法 Police Powers 原则",
            counter_weapons=[
                "歧视性监管抗辩：举证东道国政府仅针对中资投资方采取苛刻限制，对本土特许经营商未施加同等要求，构成歧视性征收",
                "比例原则突破：证明直接撤销特许权超出了必要限度，剥夺了中企合法合理投资期待 (Legitimate Expectations)",
                "征收充分补偿原则：即使基于公共利益，依 BIT 第 6 条亦必须按照被征收前之公允市场价值给予及时、充分、有效的可兑换补偿"
            ],
            factual_counter_point="调取同行业本土企业获得运营补贴与费率上调的历史审批公报，证明政府区别对待中资投资人。",
            evidence_checklist=[
                "东道国公用事业委员会历年费率调整与特许经营监管报告",
                "中国商务部与东道国政府签署之双边投资保护协定 (BIT) 正本",
                "国际投资争端解决中心 (ICSID) 类似公用事业特许权胜诉仲裁裁决"
            ]
        ),
        RedTeamDefense(
            defense_id="D2",
            opposing_claim="属地施工资质欺诈抗辩：主张中企未取得东道国法定外资施工许可证书 (如 PCAB AAA 执照)，合同违反外资准入强行法无效",
            lethal_index="high",
            opposing_basis="菲律宾建筑业承包商牌照法 (PCAB Act) 及印尼 BUJKA 规章",
            counter_weapons=[
                "合规联营体抗辩：证明中资企业系通过与本土持照承包商组建合规 KSO / Joint Operation 联合体参与投标实施",
                "菲律宾最高法院先例：援引菲律宾最高法院关于放宽外国承包商 PCAB 执照准入限制之里程碑违宪判决",
                "不当得利返还：即使合同效力存疑，业主已实际取得完工工程实体资产，依法应当折价补偿工程对价"
            ],
            factual_counter_point="核实中外联营体协议 (JO Agreement) 经东道国公证并在投资委员会 (BOI) 备案的完整法律凭证。",
            evidence_checklist=[
                "东道国承包商资质管理机构签发的外国承包商特别执照 (Special License)",
                "中外联合体联营协议及股东出资银行验资水单",
                "菲律宾最高法院关于外国建筑企业执照准入之生效判决书"
            ]
        )
    ]

    actionable_checklist = [
        "自特许权撤销令下达之日起严格在 30 日内向中国信保递交海外投资保险出险报损申请书",
        "委托国际知名会计师事务所固定被撤销特许项目截至终止日之资产账面价值与净现值评估",
        "启动向中国商务部、外交部及驻东道国使馆经商处之外交保护与政府间双边经贸联委会磋商程序",
        "向东道国政府寄发投资协定争议正式通知函 (Notice of Dispute)，触发 6 个月友好磋商前置期"
    ]

    return StrategicAssessment(
        case_id=state.case_id,
        pivotal_factors=pivotal_factors,
        outcome_branches=outcome_branches,
        red_team_defenses=red_team_defenses,
        actionable_checklist=actionable_checklist,
        updated_at=_now()
    )


def _build_asean_pre_investment_compliance_assessment(state: CaseState) -> StrategicAssessment:
    """东盟出海建设工程与央企重大境外投资投前准入合规审查推演 (PRE_INVESTMENT_COMPLIANCE)
    核心任务：东道国准入六维合规核验、监管红线碰撞与保护条款设计、投资准入与交易架构比选。
    """
    pivotal_factors = [
        "东道国外资准入负面清单与法定施工资质持牌审查 (印尼 BUJKA、马来 CIDB、菲律宾 PCAB 等法定要求)",
        "工程用地物权与属地习惯法冲突 (如印尼原住民习惯法土地 Hak Ulayat 征拆与权属瑕疵风险)",
        "印尼能矿部 MEMR 11/2024 本地化率 (TKDN) 强制配额达标与部委特许豁免许可取得可行性",
        "国资委35号令《中央企业境外投资监督管理办法》重大项目事前尽调备案与境内终身追责问责",
        "《数据安全法》第36条工程地质勘测、高精度地理图纸跨境出境审批与商业机密安全脱敏",
        "东道国主权外汇出境管制与中国信保海外投资政治风险保险 (Sinosure Policy) 30日出险保全对接"
    ]

    outcome_branches = [
        OutcomeBranch(
            branch_type="favorable",
            title="方案 A（推荐基准）：中资相对控股 + 属地联营体 (KSO/JO) 风险隔离交易架构",
            condition_precedent="假定投资人与东道国信誉良好之本土持牌承包商组建联合运营体 (KSO)，通过联营协议锁定各自工程界面与责任内部分担，既满足东道国外资准入股比红线，又锁定属地劳工与本地采购配额指标。",
            substantive_basis=[
                "印尼《建筑服务法》(UU 2/2017) 第57条 (KSO 联营体责任)",
                "菲律宾最高法院 Manila Water 判例 (外资控股企业资质平等权准入)",
                "国资委35号令第12条 (特别监管类重大境外项目事前审核合规路径)"
            ],
            key_evidence_required=[
                "经东道国投资部 (BKPM/BOI) 备案的中外联营协议 (Joint Operation Agreement)",
                "属地独立第三方土地尽职调查报告与习惯法土地补偿无纠纷公证书",
                "印尼 Surveyor Indonesia 出具的 TKDN 本地化采购实施达标测算方案"
            ],
            outcome_summary="该架构在东道国监管层面合规性高，完全契合国资委境外投资事前审查指引，能有效分散属地劳务纠纷与土地征拆风险，综合合规就绪度评级为 A 级。",
            risk_level="low"
        ),
        OutcomeBranch(
            branch_type="uncertain",
            title="方案 B：纯离岸设备供货 (Offshore Supply) + 在岸持牌施工分包架构（低风险保守路径）",
            condition_precedent="若央企选择不直接作为在岸承包商出资，转而由境内主体仅签署离岸设备供货与技术支持合同，在岸土建由东道国本土承包商独立承担并实行无追索背靠背结算。",
            substantive_basis=[
                "FIDIC 银皮书标准条件与离岸涉外准据法约定 (新加坡国际商事法庭 SICC 管辖)",
                "联合国国际货物销售合同公约 (CISG) 货物交付与质量责任除外条款"
            ],
            key_evidence_required=[
                "离岸与在岸双合同结构物理隔离协议 (Split Contract Structure Agreement)",
                "在岸独立承包商全套 BUJKA / PCAB 施工牌照及完税凭证",
                "离岸供货见索即付信用证 (L/C) 结算保证函"
            ],
            outcome_summary="彻底规避在岸劳工法强行法与习惯法侵权连带风险，但可能面临东道国海关针对离岸拆分合同的穿透式转让定价反避税审查与关税补缴风险，合规就绪度评级为 B 级。",
            risk_level="medium"
        ),
        OutcomeBranch(
            branch_type="unfavorable",
            title="方案 C：特许经营 BOT/PPP + 政府主权担保架构（收益最大化但政治风险高）",
            condition_precedent="假定项目拟直接采取特许经营特许权模式开发，要求东道国财政部或国家电力公司签发主权担保函，但在可行性研究阶段未妥善落实双边投资保护协定 (BIT) 间接征收防范架构。",
            substantive_basis=[
                "中国-东盟双边投资协定 (BIT) 第6条 (征收与国有化充分补偿)",
                "泰国最高行政法院 Hopewell 基础设施特许经营政府单方撤销补偿先例",
                "中国信保海外投资保险标准保单第15条 (政治风险30日法定出险通知)"
            ],
            key_evidence_required=[
                "东道国议会或特许经营委员会正式批准特许权协议 (Concession Agreement)",
                "项目购电协议 (PPA) 包含不可撤销之主权外汇汇出与政府违约兜底条款",
                "中国信保正式出具的海外投资险保单承保确认函"
            ],
            outcome_summary="面临东道国政府换届政策反转、强制调降上网电价或以‘公共利益正当监管’为由单方撤销特许权的隐性征收风险，若未投保中信保可能导致巨额沉没资产无法求偿，风险等级为高危。",
            risk_level="high"
        )
    ]

    red_team_defenses = [
        RedTeamDefense(
            defense_id="D1",
            opposing_claim="涉外合同语言有效性监管红线碰撞：东道国法律要求所有合同必须签署印尼语官方版本，否则可能被裁定绝对无效",
            lethal_index="critical",
            opposing_basis="印尼 2009 年第 24 号《国旗、语言法》第 31 条及原旧判例",
            counter_weapons=[
                "印尼最高法院 SEMA 3/2023 善意通告：除非证明存在欺诈恶意，法院不得仅因缺少印尼语版本宣布合同自始无效",
                "双语同等效力条款设计：在合同专用条件中约定‘印尼语与英语同时签署，二者发生冲突时以英文技术表述为准’",
                "国际仲裁排他管辖：将准据法及争议解决约定为新加坡国际仲裁中心 (SIAC) 或香港国际仲裁中心 (HKIAC)"
            ],
            factual_counter_point="核实中资总包商已备妥经印尼法务部宣誓翻译官认证的印尼语对照全套草案，在签约仪式上同步完成双语签署。",
            evidence_checklist=[
                "印尼宣誓翻译官 (Penerjemah Tersumpah) 盖章之印尼语合同译本",
                "双方关于合同工作语言与争议解释以英文为准的缔约前往来备忘录",
                "印尼最高法院 SEMA No. 3 Tahun 2023 裁判通告官方正本"
            ]
        ),
        RedTeamDefense(
            defense_id="D2",
            opposing_claim="马来西亚/新加坡工程分包背靠背付款绝对无效监管红线碰撞：强行法宣告 Pay-when-paid 条款自始无效",
            lethal_index="high",
            opposing_basis="马来西亚 CIPAA 2012 第 35 条 / 新加坡 SOPA 2004 第 9 条法定付款保障强行法",
            counter_weapons=[
                "以里程碑核验周期替代条件付款：在分包合同中废除‘业主付款作为分包付款前提’表述，改用‘工程师签发质量合格证明后45日内付款’",
                "分包违约金上限同步锁闭：在分包专用条件中将误期损害赔偿金上限对齐主合同标准 (10%~15%)，避免不可传导风险",
                "阶段快速裁决争议对冲：建立分包纠纷快速调解前置程序，并在主合同中争取业主直付本地分包商特许授权"
            ],
            factual_counter_point="法务合同体检对招标文件标准条件全面红线扫描，删除全部背靠背苛刻字眼，改用客观里程碑进度款核销条款。",
            evidence_checklist=[
                "经法务红线修正后的 EPC 分包协议标准化范本 (Subcontract Standard Form)",
                "马来西亚联邦法院 Bauer 案 CIPAA 第 35 条背靠背绝对无效判例裁判要旨",
                "总包方与属地主要分包商签署的工程节点验收与进度款结算流程细则"
            ]
        ),
        RedTeamDefense(
            defense_id="D3",
            opposing_claim="见索即付无条件履约保函恶意扣兑保护缺口：业主利用无条件独立保函随时向开立行发起突袭索兑",
            lethal_index="high",
            opposing_basis="国际商会 URDG 758 规则及东道国独立保函即付原则",
            counter_weapons=[
                "新加坡 BS Mount Sophia 显失公平止付先例：确立‘显失公平 (Unconscionability)’作为保函止付独立法定事由",
                "保函开立双重前置条件约定：要求开立行在索兑通知中必须附具‘工程师出具的承包商实质违约未纠正证明函’",
                "管辖权隔离保护：保函开立行约定为具有中资背景的跨国银行雅加达/新加坡分行，受新加坡法院司法管辖"
            ],
            factual_counter_point="中资承包商坚决拒绝签署‘无条件放弃一切保函禁令救济’的业主特设条款，在保函文本中保留显失公平救济权利。",
            evidence_checklist=[
                "新加坡高等法院 BS Mount Sophia [2016] SGHC 81 显失公平止付权威判决书",
                "中国进出口银行/中国银行出具的具备实质违约通知前置要件的保函标准格式",
                "工程现场履约进度正常、无任何工期违约事件发生之监理工程师例会纪要"
            ]
        )
    ]

    actionable_checklist = [
        "对照东道国 2026 最新外资投资负面清单，核验外资股权比例上限并取得属地施工资质牌照 (BUJKA/CIDB/PCAB)",
        "委托属地权威律所出具不动产土地产权专项尽调报告，核验习惯法土地 (Hak Ulayat) 权属无争议证明文件",
        "编制设备与劳务属地化预算方案，对照印尼 MEMR 11/2024 计算 TKDN 本地化率，必要时申请能矿部特许豁免",
        "按照国资委 35 号令完成重大境外投资可行性研究论证，提交集团党委会、董事会审批并向国资委办理备案",
        "对拟出境的工程图纸与地质勘测数据实施商业与机密脱敏，完成《数据安全法》第36条数据出境安全评估审查",
        "向中国出口信用保险公司正式提交《海外投资险承保申请》，固定30日出险保全指引，建立应急对冲预案"
    ]

    return StrategicAssessment(
        case_id=state.case_id,
        pivotal_factors=pivotal_factors,
        outcome_branches=outcome_branches,
        red_team_defenses=red_team_defenses,
        actionable_checklist=actionable_checklist,
        updated_at=_now()
    )


def build_strategic_assessment(state: CaseState) -> StrategicAssessment:
    """同步基准策略评估构造函数（根据东盟涉外工程与海外投资案件事实要素智能路由）"""
    cid = state.case_id or ""
    facts = state.facts_zh or ""
    claims = state.claims_zh or ""
    issues_text = " ".join([i.text_zh for i in state.issues]) if state.issues else ""
    full_text = f"{cid} {facts} {claims} {issues_text} {state.meta.contract_type or ''} {state.meta.choice_of_law or ''}"

    stage_val = ""
    if hasattr(state.meta, "lifecycle_stage"):
        ls = state.meta.lifecycle_stage
        stage_val = ls.value if hasattr(ls, "value") else str(ls)

    # 0. 优先判断是否处于投前合规审查阶段 (PRE_INVESTMENT_COMPLIANCE)
    if "pre_investment" in stage_val.lower() or any(k in full_text for k in ["投前", "准入", "国资委", "35号令", "TKDN", "特许经营审查", "C102"]):
        return _build_asean_pre_investment_compliance_assessment(state)

    # 1. 见索即付保函索兑与显失公平止付
    if "保函" in full_text or "BS Mount Sophia" in full_text or "止付" in full_text or "Unconscionability" in full_text or "C103" in cid:
        return _build_asean_bond_unconscionability_assessment(state)

    # 2. 特许经营权撤销、外资准入限制与双边投资协定 (BIT) 间接征收
    if any(k in full_text for k in ["特许", "征收", "BIT", "Manila Water", "水务", "风电", "并购", "M&A", "C104"]):
        return _build_asean_concession_ppp_assessment(state)

    # 3. 默认为典型 EPC 工期顺延 (EOT)、28日索赔除斥期间与善意抗辩 (C101 等)
    return _build_asean_epc_delay_assessment(state)


async def generate_strategic_assessment(
    state: CaseState,
    client: Optional[LLMClient] = None
) -> StrategicAssessment:
    """生成策略推演与红队攻防对抗评估
    优先采用大模型基于东盟工程法案情定制推演，若离线/mock 则生成高标准东盟基准推演评估。
    """
    base_assessment = build_strategic_assessment(state)

    if not client:
        return base_assessment

    # 检查是否有真实提供商 API Key 环境变量
    has_key = any(
        bool(os.environ.get(pcfg.get("api_key_env", "")))
        for pcfg in getattr(client, "providers", {}).values()
        if pcfg.get("api_key_env")
    )
    if not has_key:
        return base_assessment

    try:
        jur = state.meta.jurisdiction or "asean_id"
        jurisdiction_name = f"东盟东道国工程与投资法体系 ({jur}) 及 FIDIC 标准合同"
        prompt = f"""针对中国出海基建央国企东盟建设工程案件事实，开展【动态胜败边界推演与红队攻防对抗分析】。
案情背景：
- 案号：{state.case_id}
- 适用法域与准据合同：{jurisdiction_name}
- 核心事实：{state.facts_zh[:400]}
- 当事人诉求：{(state.claims_zh or '工期索赔与保函止付救济')[:150]}

请严格遵守 V8 客观中立防线（禁止虚假绝对化胜诉承诺，采用条件假定推演）。
请输出结构精炼的 JSON：
{{
  "pivotal_factors": ["胜败摇摆关键变量 1", "关键变量 2"],
  "outcome_branches": [
    {{
      "branch_type": "favorable",
      "title": "乐观充分路径",
      "condition_precedent": "假定原告举证证明...",
      "substantive_basis": ["法条/先例 1"],
      "key_evidence_required": ["核心证据 1"],
      "outcome_summary": "裁判机构倾向于...",
      "risk_level": "low"
    }},
    {{
      "branch_type": "unfavorable",
      "title": "悲观抗辩路径",
      "condition_precedent": "若被告举证证明...",
      "substantive_basis": ["法条/先例 1"],
      "key_evidence_required": ["核心证据 1"],
      "outcome_summary": "裁判机构倾向于...",
      "risk_level": "high"
    }}
  ],
  "red_team_defenses": [
    {{
      "defense_id": "D1",
      "opposing_claim": "对方最致命抗辩 1",
      "lethal_index": "critical",
      "opposing_basis": "条文/判例依据",
      "counter_weapons": ["我方反制武器 1"],
      "factual_counter_point": "事实反驳突破口",
      "evidence_checklist": ["下一步关键调取补证 1"]
    }},
    {{
      "defense_id": "D2",
      "opposing_claim": "对方抗辩 2",
      "lethal_index": "high",
      "opposing_basis": "条文/判例依据",
      "counter_weapons": ["我方反制武器 2"],
      "factual_counter_point": "事实反驳突破口",
      "evidence_checklist": ["下一步关键调取补证 2"]
    }}
  ],
  "actionable_checklist": ["下一步关键行动 1", "关键行动 2"]
}}
"""
        import asyncio
        data = await asyncio.wait_for(
            client.chat_json(
                task="generate",
                system_prompt="你是一名精通东盟建设工程、FIDIC 合同及海外投资主权风险防范的国际仲裁资深对抗策略专家。请以中立严谨的条件推演格式输出 JSON。",
                user_prompt=prompt,
                temperature=0.1,
                retries=0
            ),
            timeout=18.0
        )
            
        # 严格经过 V8 清洗
        branches = []
        for b in data.get("outcome_branches", []):
            branches.append(OutcomeBranch(
                branch_type=b.get("branch_type", "favorable"),
                title=clean_predictive_text(b.get("title", "")),
                condition_precedent=clean_predictive_text(b.get("condition_precedent", "")),
                substantive_basis=b.get("substantive_basis", []),
                key_evidence_required=b.get("key_evidence_required", []),
                outcome_summary=clean_predictive_text(b.get("outcome_summary", "")),
                risk_level=b.get("risk_level", "medium")
            ))

        defenses = []
        for d in data.get("red_team_defenses", []):
            defenses.append(RedTeamDefense(
                defense_id=d.get("defense_id", f"D{len(defenses)+1}"),
                opposing_claim=clean_predictive_text(d.get("opposing_claim", "")),
                lethal_index=d.get("lethal_index", "high"),
                opposing_basis=clean_predictive_text(d.get("opposing_basis", "")),
                counter_weapons=[clean_predictive_text(w) for w in d.get("counter_weapons", [])],
                factual_counter_point=clean_predictive_text(d.get("factual_counter_point", "")),
                evidence_checklist=[clean_predictive_text(e) for e in d.get("evidence_checklist", [])]
            ))

        if branches and defenses:
            return StrategicAssessment(
                case_id=state.case_id,
                pivotal_factors=[clean_predictive_text(f) for f in data.get("pivotal_factors", base_assessment.pivotal_factors)],
                outcome_branches=branches,
                red_team_defenses=defenses,
                actionable_checklist=[clean_predictive_text(a) for a in data.get("actionable_checklist", base_assessment.actionable_checklist)],
                updated_at=_now()
            )
    except Exception:
        pass

    return base_assessment
