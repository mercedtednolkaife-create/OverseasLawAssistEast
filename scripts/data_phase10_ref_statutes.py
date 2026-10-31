# -*- coding: utf-8 -*-
"""
data_phase10_ref_statutes.py - 52 条 L2 涉外参考规程与多边条约数据库
涵盖：
1. 国际工程与贸易公约惯例 (FIDIC 2017, URDG 758, ISP98, CISG) - 13条
2. 双边投资条约与避免双重征税协定 (BIT, DTA, RCEP) - 10条
3. 越南属地行业管理规程 (Decree 15/2021, Decree 10/2021, Decision 21/2023, Circular 02/2023, Law 43/2013) - 5条
4. 印尼属地能矿采购规程 (Permen PUPR 14/2020, UU 3/2020, Permen ESDM 11/2020, Perpres 12/2021, PP 35/2021) - 5条
5. 马来西亚行业管理规程 (PAM 2018, CIDB 2000, Income Tax 107A, Employment Act 60K, Environmental Quality 34A) - 5条
6. 新加坡行业管理规程 (REDAS 2016, SIA 2016, WSHA Cap 354A, EFMA Sec 9, ITA Sec 45) - 5条
7. 泰国公共采购与税收规程 (Public Procurement 2560, Revenue Code 70, Factory Act 2535, Consumer Protection 35_2) - 4条
8. 菲律宾仲裁税收劳务规程 (CIAC Rules 2019, RR 11-2018, EIS PD 1586, DOLE DO 174-17, Anti-Dummy CA 108) - 5条
合计 52 条，100% 结构化 elements_json 槽位覆盖！
"""
import json

PHASE10_L2_REFERENCE_NORMS = [
    # ========================================================
    # 1. 国际工程与贸易公约惯例 (13条)
    # ========================================================
    {
        "table": "reference_norms",
        "norm_id": "INTL:FIDIC_2017:Cl20_2",
        "law": "INTL:FIDIC_2017_RedBook",
        "enbez": "Clause 20.2",
        "title": "FIDIC 2017红皮书第20.2款：承包商索赔通知28天严格除斥期间与失权效力",
        "heading_path": "FIDIC Conditions of Contract for Construction (2017 Red Book) > Clause 20 Employer's and Contractor's Claims > Sub-Clause 20.2 Claims For Payment and/or EOT",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Notice of Claim: If the claiming Party considers that it is entitled to any additional payment and/or to EOT, the claiming Party shall give a Notice to the Engineer, describing the event or circumstance giving rise to the claim. The Notice shall be given as soon as practicable, and no later than 28 days after the claiming Party became aware, or should have become aware, of the event or circumstance. If the claiming Party fails to give a Notice of Claim within this period of 28 days, the claiming Party shall not be entitled to any additional payment, the Time for Completion shall not be extended, and the other Party shall be discharged from any liability in connection with the claim.",
        "text_en": "FIDIC 2017 Cl 20.2: Notice of Claim must be given within 28 days of awareness of event; failure discharges the other party from all liability (time-bar).",
        "text_zh": "【FIDIC 2017第20.2款索赔28天绝对时效与除斥失权效力】：当事人主张任何追加付款或工期顺延（EOT）时，必须在知悉或应当知悉索赔事件后严格 28 天内向工程师发出索赔通知；逾期发出通知的，索赔方彻底丧失获得工期顺延及追加付款的一切实体权利，相对方就该索赔的任何责任被排他性永久免除！【出海攻防启示】：国际工程索赔第一除斥铁律！中资项目团队常忙于现场赶工而忽略书面通知程序，导致数千万美元延误与变更索赔因超过 28 天通知期在 DAB 裁决或国际仲裁中被直接裁决失权（Time-Barred）！出海央企现场工程师必须在发现任何阻碍事实之日起 14 天内闭环发出索赔预警函！",
        "norm_category": "claims_procedure",
        "mandatory_level": "directory",
        "fidic_tier": "international_standard",
        "fidic_edition": "2017",
        "elements_json": json.dumps([
            {"eid": "e_fidic20_notice_within_28d", "text_zh": "要件一：承包商知晓或应当知晓索赔事件发生并在严格 28 个日历天内签发首份书面索赔通知", "status": "condition_precedent"},
            {"eid": "e_fidic20_fully_detailed_claim_84d", "text_zh": "要件二：自发出索赔通知后 84 天内提交包含法律合同依据及工期费用详尽支撑材料的全面索赔报告", "status": "mandatory"},
            {"eid": "e_fidic20_statutory_time_bar", "text_zh": "法律后果：逾期未发通知则索赔请求权自始消灭，工程师依法无权审查实体并裁定相对方免责", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "INTL:FIDIC_2017:Cl21_4",
        "law": "INTL:FIDIC_2017_RedBook",
        "enbez": "Clause 21.4",
        "title": "FIDIC 2017红皮书第21.4款：争议避免与裁决委员会DAAB裁定程序与临时拘束力",
        "heading_path": "FIDIC Conditions of Contract for Construction (2017) > Clause 21 Disputes and Arbitration > Sub-Clause 21.4 Obtaining DAAB's Decision",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Obtaining DAAB's Decision: If a dispute arises between the Parties, either Party may refer the dispute to the DAAB. The DAAB shall give its decision within 84 days. The decision shall be binding on both Parties, who shall promptly comply with it whether or not a Party gives a NOD. If no NOD is given within 28 days after receiving the decision, the decision shall become final and binding upon both Parties.",
        "text_en": "DAAB must issue decision within 84 days; decision is immediately binding on both Parties; becomes final and binding if no Notice of Dissatisfaction (NOD) within 28 days.",
        "text_zh": "【DAAB裁定的即时拘束力与28天不满意通知NOD终局门槛】：双方将争议提交 DAAB 后，DAAB 须在 84 天内作出书面裁定；该裁定对双方具有即时拘束力（Binding），不论是否签发不满意通知（NOD），各方均必须立即遵照执行！若任何一方在收到裁定后 28 天内未签发 NOD，该裁定即确立为终局且具有实质拘束力（Final and Binding），当事人可在国际仲裁中直接申请对未履行 DAAB 裁定金钱义务做出中间裁决！【出海攻防启示】：中资承包商索赔现金流破局重器！当业主工程师恶意拖延审批巨额变更签证款时，中资企业提请 DAAB 裁定，取得 DAAB 裁定书后业主若拒绝付款即构成重大违约，中资企业可依此单方暂停施工或在 ICC 仲裁中通过紧急仲裁员程序迅速执行该款项！",
        "norm_category": "claims_procedure",
        "mandatory_level": "directory",
        "fidic_tier": "international_standard",
        "fidic_edition": "2017",
        "elements_json": json.dumps([
            {"eid": "e_fidic21_referral_to_daab", "text_zh": "要件一：当事人就工程师决定产生争议并在合同约定前置协商期后正式提请 DAAB 裁决", "status": "condition_precedent"},
            {"eid": "e_fidic21_immediate_binding_duty", "text_zh": "要件二：DAAB 在 84 天内作出裁定，双方承担无条件立即履行的临时强制拘束力义务", "status": "mandatory"},
            {"eid": "e_fidic21_final_binding_bar_nod", "text_zh": "法律后果：裁决后 28 天内未提交书面 NOD 不满意通知者，裁定自动固化为终局强制效力", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "INTL:FIDIC_2017:Cl14_2",
        "law": "INTL:FIDIC_2017_RedBook",
        "enbez": "Clause 14.2",
        "title": "FIDIC 2017红皮书第14.2款：预付款保函生效要件与进度款扣减摊销规则",
        "heading_path": "FIDIC 2017 Red Book > Clause 14 Contract Price and Payment > Sub-Clause 14.2 Advance Payment",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Advance Payment: The Employer shall make an advance payment, as an interest-free loan for mobilization, when the Contractor submits an Advance Payment Guarantee in the form and issued by an entity approved by the Employer in amounts equal to the Advance Payment. Amortization deductions shall be made at the specified percentage from interim payments until fully repaid.",
        "text_en": "Employer pays mobilization advance payment upon submission of compliant guarantee; repaid through percentage amortizations from interim certificates until fully repaid.",
        "text_zh": "【预付款发放前置保函要件与期中进度款动态冲抵摊销】：发包人应当向承包商支付无息动员预付款；预付款支付的前提要件是承包商提交由发包人认可银行开具的等额预付款保函；预付款将自期中进度款达到约定门槛比例起，按固定扣减百分比逐期冲抵扣回，保函担保金额随着预付款的逐步扣还而等额自动递减！【出海攻防启示】：保函敞口合规监控点！中资总包向业主提交预付款保函时，必须在保函文本中明确嵌入‘担保金额随业主期中扣减摊销金额自动同等核减’（Automatic Reduction Clause），杜绝因业主未主动退函导致中资企业在担保银行长期承担全额授信额度占用与巨额保函手续费敞口！",
        "norm_category": "banking_finance",
        "mandatory_level": "directory",
        "fidic_tier": "international_standard",
        "fidic_edition": "2017",
        "elements_json": json.dumps([
            {"eid": "e_fidic14_valid_guarantee_submitted", "text_zh": "要件一：承包商提交符合合同附录格式且经雇主核准资信银行出具的预付款独立保函", "status": "condition_precedent"},
            {"eid": "e_fidic14_interim_amortization", "text_zh": "要件二：监理工程师在每月期中付款证书（IPC）中按约定百分比逐步扣减摊销预付款金额", "status": "mandatory"},
            {"eid": "e_fidic14_auto_reduction_guarantee", "text_zh": "法律后果：预付款全额扣还时保函法律效力自动终止失效，雇主负有立即原件退还之法定义务", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "INTL:FIDIC_2017:Cl15_2",
        "law": "INTL:FIDIC_2017_RedBook",
        "enbez": "Clause 15.2",
        "title": "FIDIC 2017红皮书第15.2款：雇主因承包商违约终止合同法定14天催告整改程序",
        "heading_path": "FIDIC 2017 Red Book > Clause 15 Termination by Employer > Sub-Clause 15.2 Termination for Contractor's Default",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Termination for Contractor's Default: The Employer shall be entitled to terminate the Contract if the Contractor fails to comply with a Notice to Correct under Sub-Clause 15.1, abandons the Works, or fails to proceed in accordance with Clause 8. In any of these events, the Employer may, by giving 14 days' Notice to the Contractor, terminate the Contract and expel the Contractor from the Site. In the case of bankruptcy or bribery, Employer may terminate immediately.",
        "text_en": "Employer may terminate contract for Contractor default after 14 days' notice upon failure to remedy under Notice to Correct; immediate termination upon bankruptcy or corrupt practice.",
        "text_zh": "【发包人违约终止合同14天正式通知前置程序与排除突袭解约】：发包人唯有在承包商未遵守第15.1款纠正通知（Notice to Correct）、擅自实质性弃标、或无合理借口严重延误未按进度计划施工时，方有权发出 14 天书面解约预先通知并在期满后驱逐承包商出场终止合同；只有在承包商破产倒闭或构成商业行贿贪腐时，方可立即发出通知终止合同！【出海攻防启示】：对抗业主恶意突袭解约的法律盾牌！业主在未按 15.1 款签发纠正通知、或未给足 14 天宽限期即单方通知终止合同并封锁现场扣押设备的，构成‘非法违约终止合同（Repudiatory Breach）’！中资企业可依此反诉业主毁约，索赔全部已完工程款、停窝工损失及预期合同利润！",
        "norm_category": "breach_remedy",
        "mandatory_level": "directory",
        "fidic_tier": "international_standard",
        "fidic_edition": "2017",
        "elements_json": json.dumps([
            {"eid": "e_fidic15_valid_notice_to_correct", "text_zh": "要件一：工程师已依法发出 Sub-Clause 15.1 项下载明具体违约事项与合理补救期限的纠正通知", "status": "condition_precedent"},
            {"eid": "e_fidic15_failure_to_remedy_14d", "text_zh": "要件二：承包商在宽限期内未予补救且雇主正式发出载明 14 天解约倒计时之终止意向通知", "status": "mandatory"},
            {"eid": "e_fidic15_lawful_contract_termination", "text_zh": "法律后果：雇主取得现场清场接管权，承包商有权要求共同清点已完工现场工程量与盘点财产", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "INTL:FIDIC_2017:Cl16_2",
        "law": "INTL:FIDIC_2017_RedBook",
        "enbez": "Clause 16.2",
        "title": "FIDIC 2017红皮书第16.2款：承包商因雇主拖欠付款或严重违约合法停工与单方解除合同程序",
        "heading_path": "FIDIC 2017 Red Book > Clause 16 Suspension and Termination by Contractor > Sub-Clause 16.2 Termination by Contractor",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Termination by Contractor: The Contractor shall be entitled to terminate the Contract if: (a) Contractor does not receive reasonable evidence of financial arrangements under Sub-Clause 2.4 within 42 days; (b) Engineer fails to issue IPC within 56 days; (c) Contractor does not receive amount due under IPC within 42 days of expiry of payment time; (d) Employer substantially fails to perform obligations; (e) prolonged suspension under 8.11 exceeds 84 days. The Contractor may, by giving 14 days' Notice, terminate the Contract.",
        "text_en": "Contractor entitled to terminate upon 14 days' notice if Employer fails to pay certified amount, fails to prove financial arrangements, substantially defaults, or after 84 days suspension.",
        "text_zh": "【承包商因发包人欠款停工与14天解约权索赔预期利润】：承包商在发包人发生以下重大违约事由时有权单方解约：（1）发包人在 42 天内未能出具其资金筹措能力证明；（2）工程师无故在 56 天内未签发期中付款证书；（3）发包人在付款期限届满后超过 42 天仍未付清核定进度款；（4）工程连续停工超过 84 天；承包商在发出 14 天前置书面通知后即可合法解除合同，并有权索赔全部完工工程款、遣散费以及原合同项下合理预期利润损失！【出海攻防启示】：中资承包商维权最强核威慑武器！当东盟业主发生主权信用债务危机或严重资不抵债恶意拖延付款时，中资总包绝不可盲目自掏腰包垫资施工！严格按 16.1 发出停工通知并在满足 16.2 条件后发出 14 天解约通知，合法止损并锁定全部未实现利润索赔！",
        "norm_category": "breach_remedy",
        "mandatory_level": "directory",
        "fidic_tier": "international_standard",
        "fidic_edition": "2017",
        "elements_json": json.dumps([
            {"eid": "e_fidic16_employer_payment_default", "text_zh": "要件一：雇主逾期超 42 天未付清期中进度款，或连续指令暂停停工超过 84 个日历天", "status": "condition_precedent"},
            {"eid": "e_fidic16_contractor_14d_termination_notice", "text_zh": "要件二：承包商向雇主正式发出载明 14 天宽限期限与单方解约意向之后续书面通知", "status": "mandatory"},
            {"eid": "e_fidic16_remedies_loss_of_profit", "text_zh": "法律后果：合同依法自始终止，承包商享有人员设备遣散清场费及全部合理预期利润索赔权", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "INTL:FIDIC_2017:Cl17_1",
        "law": "INTL:FIDIC_2017_RedBook",
        "enbez": "Clause 1.15",
        "title": "FIDIC 2017红皮书第1.15款/第17.6款：合同责任上限(Cap of Liability)与间接损失免责排他性条款",
        "heading_path": "FIDIC Conditions of Contract (2017) > General Provisions > Sub-Clause 1.15 Limitation of Liability",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Limitation of Liability: Neither Party shall be liable to the other Party for loss of use of any Works, loss of profit, loss of any contract or for any indirect or consequential loss or damage. The total liability of the Contractor to the Employer, under or in connection with the Contract, shall not exceed the sum stated in the Contract Data or (if none) the Accepted Contract Amount. This Sub-Clause shall not limit liability in cases of fraud, gross negligence, deliberate default or reckless misconduct.",
        "text_en": "Neither Party liable for loss of profit or indirect/consequential damages; Contractor's total liability capped at Contract Price, except for fraud, gross negligence, or deliberate default.",
        "text_zh": "【合同责任上限与排他性排除间接后果损失条款】：任何一方均无需向相对方赔偿工程使用损失、利润损失、商业机会丧失或任何间接、附随的后果性损害（Indirect or Consequential Loss）；承包商对发包人所承担的全部合同违约责任总额，严格以合同数据表中约定的上限金额（通常为 100% 中标合同额）为封顶限额！但在存在欺诈、重大过失、故意违约或严重鲁莽渎职的情形下，该责任限制条款不予适用！【出海攻防启示】：中资央企海外签约最关键防暴雷阀门！东盟项目业主索赔往往开出天文数字的‘下游工厂停产营业损失’或‘巨额商业违约罚金’；中资企业凭借 Cl 1.15 / 17.6 铁律，可直接在法律上彻底斩断业主的间接损失索赔，并将全部赔付上限死死锁定在合同总额之内！",
        "norm_category": "breach_remedy",
        "mandatory_level": "directory",
        "fidic_tier": "international_standard",
        "fidic_edition": "2017",
        "elements_json": json.dumps([
            {"eid": "e_fidic1_indirect_damages_exclusion", "text_zh": "要件一：发包人主张的经济损失属于生产利润损失、预期经营利益或附随性衍生间接损害", "status": "condition_precedent"},
            {"eid": "e_fidic1_liability_cap_stipulated", "text_zh": "要件二：合同专用条款已明确载明总承包商赔付责任封顶上限百分比或固定总金额", "status": "mandatory"},
            {"eid": "e_fidic1_cap_enforcement_effect", "text_zh": "法律后果：法庭与仲裁庭严格执行责任上限并全部剔除间接损失索赔，除非原告举证证明存在欺诈或重大过失", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "INTL:URDG_758:Art15",
        "law": "INTL:URDG_758",
        "enbez": "Article 15",
        "title": "国际商会URDG 758见索即付独立保函统一规则第15条：索赔陈述必备要素与受益人索赔书合规审查",
        "heading_path": "ICC Uniform Rules for Demand Guarantees (URDG 758) > Article 15 Requirements for Demand",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Requirements for Demand: A demand under the guarantee shall be accompanied by such other documents as the guarantee specifies, and in any event by a statement, by the beneficiary, indicating in what respect the applicant is in breach of its obligations under the underlying relationship. This statement may be in the demand itself or in a separate signed document accompanying or identifying the demand.",
        "text_en": "Demand under URDG 758 must be accompanied by specified documents and a statement by beneficiary indicating in what respect applicant breached underlying contract.",
        "text_zh": "【URDG 758见索即付保函受益人违约声明强制要件】：依据 URDG 758 开立的见索即付独立保函，受益人提出索赔时除必须提交保函列明的单据外，必须在索赔书中明确陈述被保证人（承包商）在基础基础合同关系中具体在何种方面构成了违约！该违约陈述可以直接载于索赔函中，亦可作为单独签署的随附单据提交！【出海攻防启示】：阻断东盟业主恶意索兑保函的最有效程序抓手！许多东盟私人业主或不专业发包人在索兑中资承包商履约保函时，往往仅发出一纸‘立即将全部保函金额汇入我方账户’的简单电报，欠缺明确违约事实陈述。担保行或中资企业可依 Art 15 判定该索赔不满足单据严格相符原则（Non-compliant Demand），担保行依法有权且必须拒绝付款！",
        "norm_category": "banking_finance",
        "mandatory_level": "directory",
        "fidic_tier": "international_standard",
        "fidic_edition": "URDG 758",
        "elements_json": json.dumps([
            {"eid": "e_urdg15_presentation_of_demand", "text_zh": "要件一：受益人向开证行或转开行在保函有效期内递交正式付款索赔函及随附单据", "status": "condition_precedent"},
            {"eid": "e_urdg15_mandatory_breach_statement", "text_zh": "要件二：索赔单据必须明确载明申请人具体违反了基础工程合同哪一项特定履约义务之声明", "status": "mandatory"},
            {"eid": "e_urdg15_rejection_for_noncompliance", "text_zh": "法律后果：索赔陈述缺失或含糊不清的构成单据不符，担保行依法必须拒绝付款并退单", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "INTL:URDG_758:Art20",
        "law": "INTL:URDG_758",
        "enbez": "Article 20",
        "title": "国际商会URDG 758第20条：担保行审单时限（5个营业日）与严格相符单据审查标准",
        "heading_path": "ICC Uniform Rules for Demand Guarantees (URDG 758) > Article 20 Time to Examine Demand",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Time to Examine Demand; Payment: The guarantor shall have five business days following the day of presentation of a demand to examine the demand and determine if it is complying. If the guarantor determines that a demand is complying, it shall pay. If the guarantor determines that a demand is non-complying, it shall give a notice of rejection to the presenter indicating each discrepancy, within the five business days.",
        "text_en": "Guarantor has 5 business days to examine demand; must pay if complying, or issue notice of rejection detailing each discrepancy within 5 business days.",
        "text_zh": "【担保行5个营业日严格审单期限与不符点一次性通知原则】：担保行自收到受益人索赔单据次日起，享有严格的 5 个营业日时间审查单据是否相符；若认定相符，担保行应予付款；若认定不符，担保行必须在 5 个营业日内向提交人发出拒付通知，并在通知中一次性完整列明所依据的全部不符点！逾期未发通知的，担保行丧失主张单据不符之抗辩权！【出海攻防启示】：中资企业紧急申请法院保函止付令的黄金 5 天窗口！业主突袭索兑保函后，中资企业必须在开证行审单的 5 个营业日倒计时内，迅速在属地法院或仲裁地法院提起紧急禁令（Injunction）或欺诈止付申请，将法院止付裁定在第 5 个营业日结转前送达银行柜台，成功拦截保函被强行划扣！",
        "norm_category": "banking_finance",
        "mandatory_level": "directory",
        "fidic_tier": "international_standard",
        "fidic_edition": "URDG 758",
        "elements_json": json.dumps([
            {"eid": "e_urdg20_five_business_days", "text_zh": "要件一：担保行自收到索赔单据次日起启动 5 个银行营业日严格审单审查期", "status": "condition_precedent"},
            {"eid": "e_urdg20_strict_compliance_check", "text_zh": "要件二：审查索赔函签名、印章、公司名称及金额是否与保函文本存在一字不差之表面严格相符", "status": "mandatory"},
            {"eid": "e_urdg20_preclusion_rule", "text_zh": "法律后果：担保行在 5 天内未发出列明全部不符点之拒付通知者，依法不得再主张单据不符抗辩", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "INTL:URDG_758:Art33",
        "law": "INTL:URDG_758",
        "enbez": "Article 33",
        "title": "国际商会URDG 758第33条：保函管辖法律与司法管辖权默认适用开立行分支机构所在地法",
        "heading_path": "ICC Uniform Rules for Demand Guarantees (URDG 758) > Article 33 Governing Law and Jurisdiction",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Governing Law and Jurisdiction: Unless otherwise provided in the guarantee, the governing law of the guarantee shall be the law of the location of the guarantor's branch or office that issued the guarantee. The courts of that location shall have jurisdiction over any dispute.",
        "text_en": "Governing law and jurisdiction of URDG 758 guarantee default to the law and courts of the location of the guarantor's branch that issued the guarantee.",
        "text_zh": "【保函默认适用开立行所在地法律与管辖法院原则】：在独立保函未另行明确约定准据法和管辖法院的情况下，保函的准据法强制默认推定为开立该保函的担保行分支机构所在地法律；有关保函的一切争议，由该分支机构所在地法院专属管辖！【出海攻防启示】：中资央企保函主场管辖权争取秘籍！许多东盟业主合同要求采用东盟属地法律管辖工程。但若总包保函由中资银行总行或香港/新加坡分行直开，并在保函中援引 URDG 758 且未写管辖条款，则保函依法直接受中国法或新加坡法管辖！当业主恶意索赔时，中资企业可直接在中国涉外法院或新加坡高院提起保函止付申请，彻底摆脱东盟当地地方法院的地方保护主义干扰！",
        "norm_category": "banking_finance",
        "mandatory_level": "directory",
        "fidic_tier": "international_standard",
        "fidic_edition": "URDG 758",
        "elements_json": json.dumps([
            {"eid": "e_urdg33_silence_on_governing_law", "text_zh": "要件一：独立保函文本中未设立关于适用的实体准据法与争议解决法院之排他性特别约定", "status": "condition_precedent"},
            {"eid": "e_urdg33_issuing_branch_nexus", "text_zh": "要件二：识别查明签发该保函的担保金融机构营业分支实体之物理真实注册经营所在地", "status": "mandatory"},
            {"eid": "e_urdg33_statutory_default_forum", "text_zh": "法律后果：强制推定适用该发信行分支机构所在地法，由该所在地法院行使争议司法管辖权", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "INTL:ISP98:Rule4_01",
        "law": "INTL:ISP98",
        "enbez": "Rule 4.01",
        "title": "国际备用信用证惯例ISP98规则第4.01条：备用证与基础合同独立抽象性及单据表面审查",
        "heading_path": "International Standby Practices 1998 (ISP98) > Rule 4 Examination > Rule 4.01 Exclusivity and Independence",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Examination for Compliance: An issuer is not responsible for performance or breach of any underlying agreement, whether or not the standby indicates that agreement. The issuer's obligations are independent of any underlying transaction or any defense arising therefrom.",
        "text_en": "ISP98 Rule 4.01: Standby letter of credit is completely independent of underlying agreement; issuer examines documents on their face without regard to underlying disputes.",
        "text_zh": "【备用信用证独立抽象性原则与基础合同争议抗辩阻断】：开证行对任何基础交易协议的实际履行或违约状态概不负责，无论该备用信用证是否提及该基础协议；开证行项下的金钱偿付义务，完全独立于申请人与受益人之间的基础工程合同关系；基础交易合同中的任何抗辩事由（如工程存在瑕疵、工期延误争议），均不得对抗开证行的单据付款义务！【出海攻防启示】：境外融资备用信用证双刃剑！中资承包商为海外业主开立备用信用证（SBLC）作为履约担保时，一旦受益人交单相符，银行必须放款，无法以‘工程质量无问题’为由阻止银行付款；因此，中资企业唯有通过在新加坡或中资属地法院证明受益人构成‘实质欺诈（Fraud Exception）’，方能依法击破独立抽象性防火墙取得禁令！",
        "norm_category": "banking_finance",
        "mandatory_level": "directory",
        "elements_json": json.dumps([
            {"eid": "e_isp98_independent_undertaking", "text_zh": "要件一：开立合法有效受 ISP98 惯例拘束之不可撤销备用信用证法律凭单", "status": "condition_precedent"},
            {"eid": "e_isp98_facially_compliant_demand", "text_zh": "要件二：受益人提交的索偿单据在表面形式上符合备用信用证条款的明文单据要求", "status": "mandatory"},
            {"eid": "e_isp98_estoppel_underlying_defenses", "text_zh": "法律后果：开证行承担绝对无条件偿付义务，基础承揽合同之瑕疵抗辩被排他性阻断排除", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "INTL:CISG:Art25",
        "law": "INTL:CISG",
        "enbez": "Article 25",
        "title": "联合国国际货物销售合同公约CISG第25条：根本违约实质剥夺合同期待利益认定标准",
        "heading_path": "United Nations Convention on Contracts for the International Sale of Goods (CISG 1980) > Part III Sale of Goods > Article 25 Fundamental Breach",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Fundamental Breach: A breach of contract committed by one of the parties is fundamental if it results in such detriment to the other party as substantially to deprive him of what he is entitled to expect under the contract, unless the party in breach did not foresee and a reasonable person of the same kind in the same circumstances would not have foreseen such a result.",
        "text_en": "CISG Art 25: Breach is fundamental if it substantially deprives the other party of contractual expectation, unless unforeseeable by party in breach and a reasonable person.",
        "text_zh": "【根本违约实质剥夺期待利益标准与可预见性免责要件】：一方当事人违反合同的结果，如使另一方当事人蒙受实质性损害，以至于在实质上剥夺了另一方根据合同有权期待得到的核心利益（Substantially Deprived），即构成公约项下的根本违约（Fundamental Breach）；但若违约方缔约时不能预见、且同等资格的理性当事人在相同情况下亦无法预见此种损害后果的，不构成根本违约！【出海攻防启示】：东盟跨境大型机电设备采购解约核心准绳！中资承包商为东盟项目向跨国供应商采购重型燃机、盾构机等关键设备，若设备交付迟延导致整个电站无法按期商业并网投产，即构成 Art 25 根本违约；中资总包可直接宣告合同无效（Avoidance of Contract），全额退货并要求供货商承担下游巨额连带停工损失！",
        "norm_category": "breach_remedy",
        "mandatory_level": "directory",
        "elements_json": json.dumps([
            {"eid": "e_cisg25_substantial_detriment", "text_zh": "要件一：违约方的违约行为造成守约方在实质上丧失了依据买卖合同有权期待的商业核心价值", "status": "condition_precedent"},
            {"eid": "e_cisg25_foreseeability_test", "text_zh": "要件二：违约方在订立合同时能够合理预见该违约后果、或理性第三方在相同条件下亦能预见", "status": "mandatory"},
            {"eid": "e_cisg25_remedy_avoidance", "text_zh": "法律后果：守约方依法享有单方宣告合同无效解约权，并有权行使全额退款退货与损失索赔权", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "INTL:CISG:Art74_77",
        "law": "INTL:CISG",
        "enbez": "Article 74-77",
        "title": "联合国国际货物销售合同公约CISG第74-77条：损害赔偿完全赔偿原则与守约方减损义务",
        "heading_path": "CISG (1980) > Chapter V Provisions Common to Obligations of Seller and Buyer > Section II Damages > Articles 74-77",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Damages and Mitigation: Damages for breach of contract by one party consist of a sum equal to the loss, including loss of profit, suffered by the other party as a consequence of the breach (Art 74). The party who relies on a breach of contract must take such measures as are reasonable in the circumstances to mitigate the loss, including loss of profit, resulting from the breach. If he fails to take such measures, the party in breach may claim a reduction in the damages in the amount by which the loss should have been mitigated (Art 77).",
        "text_en": "CISG Art 74-77: Full compensation includes loss of profit subject to foreseeability; aggrieved party must take reasonable measures to mitigate loss or face damages reduction.",
        "text_zh": "【损害赔偿完全赔偿原则与守约方积极减损义务及减额核减】：一方违约的损害赔偿额，应相当于另一方因违约遭受的全部实际损失加利润损失（Loss of Profit），但不得超过违约方在订约时应当预见的数额；主张违约的一方当事人，必须根据具体情况采取合理措施以减轻因对方违约造成的损失（包括利润损失）；若守约方未采取合理减损措施，违约方有权请求从损害赔偿金额中扣除本可以减轻的损失金额！【出海攻防启示】：中资采购供应链索赔抗辩盾牌！当境外供货商违约断供建筑钢材或管材时，中资项目部切不可坐视工期停摆持续扩大窝工损失；必须立即从属地现货市场进行合理‘替代采购（Cover Purchase）’以减轻损失；否则在后续仲裁中，未采取减损措施部分的主张将被仲裁庭强行核减剔除！",
        "norm_category": "breach_remedy",
        "mandatory_level": "directory",
        "elements_json": json.dumps([
            {"eid": "e_cisg74_actual_and_profit_loss", "text_zh": "要件一：守约方因货物违约遭受了可预见的直接实际财产损失或可预期的商业利润净减损", "status": "condition_precedent"},
            {"eid": "e_cisg77_duty_to_mitigate", "text_zh": "要件二：守约方在获悉违约后是否采取了商业上合理的替代采购或止损措施以遏制损失扩散", "status": "mandatory"},
            {"eid": "e_cisg77_damages_reduction_bar", "text_zh": "法律后果：违约方承担完全赔偿责任；但对守约方怠于减损扩大的损失数额，法庭强制予以全额扣除", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "INTL:CISG:Art79",
        "law": "INTL:CISG",
        "enbez": "Article 79",
        "title": "联合国国际货物销售合同公约CISG第79条：当事人不能控制之客观履行障碍不可抗力免责",
        "heading_path": "CISG (1980) > Section IV Exemptions > Article 79 Impediments Beyond Control",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Exemptions: A party is not liable for a failure to perform any of his obligations if he proves that the failure was due to an impediment beyond his control and that he could not reasonably be expected to have taken the impediment into account at the time of the conclusion of the contract or to have avoided or overcome it or its consequences. The party who fails to perform must give notice to the other party of the impediment within a reasonable time.",
        "text_en": "CISG Art 79: Party exempt from damages if non-performance is due to unforeseeable, unavoidable impediment beyond control; prompt notice required.",
        "text_zh": "【公约第79条客观履行障碍免责三大法定要件与合理通知义务】：当事人对其不履行任何义务不承担赔偿责任，如果他能证明未能履行是由于他所不能控制的客观履行障碍所致（Beyond his control），且无法合理期望他在订立合同时考虑到该障碍、或期望他避免或克服该障碍或其后果；不能履行义务的一方必须在合理时间内向对方发出障碍通知，对方收到通知时方发生免责效力！【出海攻防启示】：跨国工程设备物资海运清关受阻免责护身符！遭遇红海危机航道封锁、战乱禁运或始发港强制封锁等突发外部障碍时，中资设备总包商必须在 48 小时内收集当地商会不可抗力证明（Force Majeure Certificate）并向东盟业主发出正式 Art 79 免责通知，依法阻断业主的延误赔偿金请求权！",
        "norm_category": "breach_remedy",
        "mandatory_level": "directory",
        "elements_json": json.dumps([
            {"eid": "e_cisg79_beyond_control_impediment", "text_zh": "要件一：履约不能直接系因当事人无法合理控制之外部客观自然灾害或战争禁运障碍所致", "status": "condition_precedent"},
            {"eid": "e_cisg79_unforeseeable_and_unavoidable", "text_zh": "要件二：当事人在订立合同时无法合理预见该障碍且在商业上无法采取替代措施予以克服", "status": "mandatory"},
            {"eid": "e_cisg79_damages_exemption", "text_zh": "法律后果：法定免除当事人在障碍持续期间的违约损害赔偿金责任，守约方不得索兑履约保函", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },

    # ========================================================
    # 2. 双边投资条约与避免双重征税协定 (10条)
    # ========================================================
    {
        "table": "reference_norms",
        "norm_id": "TREATY:CN_ID_BIT_1992:Art4_5",
        "law": "TREATY:CN_ID_BIT_1992",
        "enbez": "Article 4-5",
        "title": "中国-印尼双边投资协定第4-5条：公平公正待遇(FET)与直接及间接征收补偿标准",
        "heading_path": "中华人民共和国政府和印度尼西亚共和国政府关于促进和保护投资协定 (1992) > 第4条 投资待遇与第5条 征收与补偿",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "China-Indonesia BIT (1992) Art 4-5: Investments of investors of either Contracting State shall enjoy fair and equitable treatment (FET) and non-discriminatory protection in the territory of the other Contracting State. Neither Contracting State shall expropriate or nationalize investments except for a public purpose, on a non-discriminatory basis, under due process of law, and against prompt, adequate and effective compensation.",
        "text_en": "China-Indonesia BIT guarantees Fair and Equitable Treatment (FET) and prohibits expropriation without prompt, adequate and effective market-value compensation under due process.",
        "text_zh": "【公平公正待遇FET与禁止非法征收及充分有效补偿原则】：缔约任何一方投资者在另一方领土内的投资，应始终享受公平和公正的待遇（FET）以及完全的保护；缔约任何一方对另一方投资者的投资不得采取国有化、征收或具有同等效果的间接征收措施，除非满足四项法定要件：（1）为了公共利益；（2）在非歧视性基础上；（3）依照国内法定法律程序；（4）给予迅速、充分和有效的补偿，补偿额应相当于采取征收前一刻该投资的市场实际价值，并计付利息！【出海攻防启示】：中资央企在印尼大型镍铁冶炼、电站特许经营的最强主权级法律护盾！当印尼政府出台突发性矿业原矿出口禁令、擅自废止已签发矿业特许权（IUP/KK）或强行强令外资强制廉价撤资出让股权时，中资企业有权越过印尼属地法院，直接依据 Art 4-5 向世界银行 ICSID 提请国际投资仲裁，向印尼政府主张数亿美元主权征收赔偿！",
        "norm_category": "bilateral_treaty",
        "mandatory_level": "directory",
        "elements_json": json.dumps([
            {"eid": "e_cn_id_bit_qualifying_investment", "text_zh": "要件一：中国境内企业通过在印尼设立的外商投资公司（PT PMA）或特许权持有合法受保护投资", "status": "condition_precedent"},
            {"eid": "e_cn_id_bit_expropriatory_state_measure", "text_zh": "要件二：印尼政府机关出台行政令吊销许可证或实质性剥夺中资企业核心资产经济价值构成间接征收", "status": "mandatory"},
            {"eid": "e_cn_id_bit_full_market_compensation", "text_zh": "法律后果：东道国政府承担迅速、充分且有效之公允市场价值现金赔偿责任，计付国际公允商业利息", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "TREATY:CN_VN_BIT_1992:Art3_4",
        "law": "TREATY:CN_VN_BIT_1992",
        "enbez": "Article 3-4",
        "title": "中国-越南双边投资协定第3-4条：最惠国待遇(MFN)与征收征用国际法补偿标准",
        "heading_path": "中华人民共和国政府和越南社会主义共和国政府关于鼓励和相互保护投资协定 (1992) > 第3条 投资待遇与第4条 征收",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "China-Vietnam BIT (1992) Art 3-4: Treatment of Investment: Each Contracting Party shall accord to investments made in its territory by investors of the other Contracting Party treatment no less favourable than that accorded to investments of its own investors or investors of any third State (MFN). Expropriation or measures having effect equivalent to expropriation require prompt, adequate and effective compensation convertible and freely transferable.",
        "text_en": "China-Vietnam BIT guarantees Most Favoured Nation (MFN) treatment and protects against uncompensated expropriation, ensuring prompt, adequate and freely transferable compensation.",
        "text_zh": "【最惠国待遇MFN与征收自由汇兑补偿保障】：缔约任何一方给予另一方投资者的投资及其相关活动的待遇，不得低于给予任何第三国投资者的待遇（最惠国待遇 MFN）；对另一方投资者的投资采取征收或国有化措施，必须给予有效补偿，该补偿款项应能有效兑换并在无迟延的情况下自由汇出境！【出海攻防启示】：借道最惠国条款突破争议解决瓶颈！1992 年中越 BIT 原仲裁条款对提交 ICSID 仲裁的事项存在一定限制。中资出海企业遭遇越南地方政府暴力冲击工厂或擅自扣押光伏风电补贴电价时，可通过 Art 3 最惠国待遇条款，借道越南与英国、德国等第三国订立的更宽泛 BIT 仲裁条款，成功将争端提交国际仲裁庭，倒逼越方行政机关妥协！",
        "norm_category": "bilateral_treaty",
        "mandatory_level": "directory",
        "elements_json": json.dumps([
            {"eid": "e_cn_vn_bit_covered_investor", "text_zh": "要件一：中国企业依法在越南投资设立项目公司持有工业土地、厂房设备或新能源发电资产", "status": "condition_precedent"},
            {"eid": "e_cn_vn_bit_discriminatory_or_expropriatory", "text_zh": "要件二：越南主管机关采取了区别于其他外资或剥夺中资企业商业运营特许权之歧视性行政措施", "status": "mandatory"},
            {"eid": "e_cn_vn_bit_freely_transferable_compensation", "text_zh": "法律后果：裁决越南政府向中资投资者全额支付以可兑换外汇结算并自由汇出之赔偿金", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "TREATY:CN_MY_BIT_1988:Art3_6",
        "law": "TREATY:CN_MY_BIT_1988",
        "enbez": "Article 3-6",
        "title": "中国-马来西亚双边投资协定第3-6条：投资资金自由汇出与战争暴乱征收补偿保障",
        "heading_path": "中华人民共和国政府和马来西亚政府关于相互鼓励和保护投资协定 (1988) > 资金汇出与征收补偿",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "China-Malaysia BIT (1988) Art 3-6: Transfer of capital and returns: Each Contracting State shall guarantee investors the free transfer of their capital and the returns from any investments in freely usable currencies without undue delay. Compensation for losses due to war, state of national emergency or civil disturbance shall be accorded non-discriminatory treatment.",
        "text_en": "China-Malaysia BIT guarantees free transfer of capital, profits and loan repayments in convertible currencies, and non-discriminatory compensation for losses during emergencies.",
        "text_zh": "【投资资本与利润收益自由汇出保证及紧急状态损失补偿】：缔约任何一方应保证另一方投资者在遵守其法律规章的前提下，在无不正当迟延的情况下，以自由兑换货币自由转移其资本、投资产生的利润、股息、特许权使用费、技术援助费以及贷款偿还款项！若投资者因战争、国家紧急状态或民众骚乱而蒙受损失，东道国给予的恢复或补偿待遇不得低于任何第三国投资者！【出海攻防启示】：中资马来西亚基建项目资金出境主权盾牌！马来西亚国家银行（BNM）经常动态调整外汇管理通知（FE Notices）。当中资承包商或合资开发商取得巨额工程结算款或股权清算分配款时，若遭遇属地商业银行以‘经常账户资金流审查’为由无理阻挠购汇出境，中资企业可正式援引 BIT 第 6 条主张国际法保护，要求大马财政部与央行开通绿色通道！",
        "norm_category": "bilateral_treaty",
        "mandatory_level": "directory",
        "elements_json": json.dumps([
            {"eid": "e_cn_my_bit_legitimate_capital_return", "text_zh": "要件一：资金属于中资企业在大马投资运营所合法产生的清算资本、股息分红或工程款收益", "status": "condition_precedent"},
            {"eid": "e_cn_my_bit_unreasonable_exchange_barrier", "text_zh": "要件二：属地外汇管制机构出台非正当性限制或过度迟延阻碍资金自由兑换并电汇出境", "status": "mandatory"},
            {"eid": "e_cn_my_bit_guarantee_free_transfer", "text_zh": "法律后果：东道国违反条约法资本自由划转担保义务，中资企业有权诉诸 ICSID 投资仲裁", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "TREATY:CN_TH_BIT_1985:Art3_5",
        "law": "TREATY:CN_TH_BIT_1985",
        "enbez": "Article 3-5",
        "title": "中国-泰国双边投资协定第3-5条：国民待遇与征收征用条件及充分可自由兑换补偿",
        "heading_path": "中华人民共和国政府和泰王国政府关于促进和保护投资协定 (1985) > 第3条 待遇与第5条 征收",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "China-Thailand BIT (1985) Art 3-5: Investments shall enjoy fair treatment and national treatment in accordance with domestic laws. Expropriation shall only be made for public welfare, against compensation without delay, which shall be effectively realizable, freely convertible and transferable.",
        "text_en": "China-Thailand BIT guarantees fair treatment and prohibits expropriation without prompt, effectively realizable and freely convertible compensation.",
        "text_zh": "【中泰投资协定征收限制与可实现自由兑换补偿】：对缔约另一方投资者的投资采取征收或国有化措施，必须出于公共福利目的，并依法支付不得迟延的补偿；该补偿应当是实质上可实现的（Effectively Realizable）、可以自由兑换（Freely Convertible）且可以自由转移的！【出海攻防启示】：中资出海泰国重大铁路、工业园投资的后盾！泰国政治周期多变，曾发生政府换届后单方废止大型交通基础设施特许权合同（如著名 Hopewell 案）。中资企业在泰投资若遭遇新一届内阁无故废止 PPP 合同，除泰国行政法院诉讼外，应立即向泰国总理府与财政部发出 BIT 争端通知书，以国际仲裁风险施压推动政府重启友好协商！",
        "norm_category": "bilateral_treaty",
        "mandatory_level": "directory",
        "elements_json": json.dumps([
            {"eid": "e_cn_th_bit_protected_asset", "text_zh": "要件一：中资企业持有符合泰国法律批准之合资企业股权、长期土地租约或特许经营权资产", "status": "condition_precedent"},
            {"eid": "e_cn_th_bit_state_unilateral_revocation", "text_zh": "要件二：泰国内阁或政府部委单方发布行政命令废止特许权协议且拒绝给予充分市场估值补偿", "status": "mandatory"},
            {"eid": "e_cn_th_bit_international_arbitration_standing", "text_zh": "法律后果：确立提起国际投资仲裁之主体资格，要求泰国国家承担条约违约全部损失赔偿", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "TREATY:CN_PH_BIT_1992:Art3_5",
        "law": "TREATY:CN_PH_BIT_1992",
        "enbez": "Article 3-5",
        "title": "中国-菲律宾双边投资协定第3-5条：投资保护待遇与代位求偿Subrogation法律认可",
        "heading_path": "中华人民共和国政府和菲律宾共和国政府关于鼓励和相互保护投资协定 (1992) > 投资保护与代位求偿",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "China-Philippines BIT (1992) Art 3-5: Protection of Investment and Subrogation: If a Contracting State or its designated Agency (e.g., Sinosure) makes a payment to its own investors under a guarantee or insurance in respect of an investment, the other Contracting State shall recognize the assignment to the former Contracting State of all rights and claims of such investors.",
        "text_en": "China-Philippines BIT recognizes statutory subrogation of national insurer (such as Sinosure) to all rights and claims of investors after insurance claim payout.",
        "text_zh": "【投资征收保护与中国信保SINOSURE官方代位求偿权法定承认】：缔约一方或其指定的机构（如中国出口信用保险公司 Sinosure）根据其对某一投资的担保或保险合同向其本国投资者支付了赔偿金，缔约另一方（菲律宾政府）应当承认该投资者的全部权利和诉求转让给该缔约一方或其指定机构（代位求偿权 Subrogation）！该官方担保机构有权代位行使投资者原享有的全部条约求偿权！【出海攻防启示】：中信保海外代位追索主权级通道！中资央企赴菲承接大型电站或码头项目，若因菲律宾政局变动或业主恶意违约导致保单出险赔付，中国信保在向央企赔付后，可直接依据 BIT 代位向菲律宾主权政府发起国际追偿，将微观商业风险上升为主权级债权清收，彻底卸下中资企业的坏账包袱！",
        "norm_category": "bilateral_treaty",
        "mandatory_level": "directory",
        "elements_json": json.dumps([
            {"eid": "e_cn_ph_bit_insurance_payout", "text_zh": "要件一：中国官方出口信用保险机构已根据涉外工程承保保单向中资出海企业全额支付理赔款", "status": "condition_precedent"},
            {"eid": "e_cn_ph_bit_subrogation_notice", "text_zh": "要件二：官方保险机构向菲律宾政府主管部门发出正式权利转让与代位求偿主权通知", "status": "mandatory"},
            {"eid": "e_cn_ph_bit_state_to_state_standing", "text_zh": "法律后果：保险人合法取得原投资者享有的全部国际法条约索赔实体权利与代位执行管辖权", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "TREATY:CN_ID_DTA_2001:Art5_7",
        "law": "TREATY:CN_ID_DTA_2001",
        "enbez": "Article 5 & 7",
        "title": "中国-印尼避免双重征税协定第5条与第7条：常设机构(PE)183天判定门槛与建筑工地利润归属",
        "heading_path": "中华人民共和国政府和印度尼西亚共和国政府关于对所得避免双重征税和防止偷漏税的协定 (2001) > 第5条 常设机构与第7条 营业利润",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "China-Indonesia DTA (2001) Art 5 & 7: Permanent Establishment and Business Profits: A building site, a construction, assembly or installation project constitutes a permanent establishment (PE) only if it continues for a period of more than 183 days. The profits of an enterprise of a Contracting State shall be taxable only in that State unless the enterprise carries on business in the other Contracting State through a PE situated therein.",
        "text_en": "Building site, construction or installation project constitutes a PE only if exceeding 183 days; profits taxable in host State solely to extent attributable to such PE.",
        "text_zh": "【建筑安装工程常设机构183天判定红线与属地营业利润征税权限制】：建筑工地、建筑、装配或安装工程，唯有在存续时间超过严格 183 天（约6个月）时，方构成税法上的常设机构（Permanent Establishment / PE）；缔约一方企业的营业利润仅在本国征税，除非该企业在另一国通过常设机构开展营业；即使构成常设机构，另一国也仅能对‘直接归属于该常设机构的利润份额’征税，严禁对境外母公司的离岸采购与设计利润实施全面引力征税（Attraction Principle）！【出海攻防启示】：中资总包印尼离岸分拆（Onshore/Offshore Split）税务合规铁律！中资承包商在印尼签署重大 EPC 协议时，必须将合同严格拆分为‘境外设备供货与技术离岸合同（Offshore Supply）’与‘境内建筑安装合同（Onshore Construction）’！依据 DTA 第 7 条，印尼税务局（DJP）仅能对在岸 183 天以上的境内建安实体征税，离岸数十亿美元的高附加值设备供货利润完全免于在印尼缴纳企业所得税！",
        "norm_category": "tax_compliance",
        "mandatory_level": "directory",
        "elements_json": json.dumps([
            {"eid": "e_cn_id_dta_183_days_threshold", "text_zh": "要件一：中资施工队伍或工程项目现场在印尼境内存续施工周期是否累计超过严格 183 天", "status": "condition_precedent"},
            {"eid": "e_cn_id_dta_profit_attribution_scope", "text_zh": "要件二：税务机关核定计税之营业收入是否严格属于直接归属于印尼境内工地之合理施工利润", "status": "mandatory"},
            {"eid": "e_cn_id_dta_offshore_tax_exemption", "text_zh": "法律后果：未满 183 天不构成 PE 免于所得税；构成 PE 者其境外独立设备供货利润免受属地穿透征税", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "TREATY:CN_VN_DTA_1995:Art5_7",
        "law": "TREATY:CN_VN_DTA_1995",
        "enbez": "Article 5 & 7",
        "title": "中国-越南双重征税协定第5条与第7条：建筑工地常设机构6个月判定与外国承包商税核减",
        "heading_path": "中华人民共和国政府和越南社会主义共和国政府关于对所得避免双重征税和防止偷漏税的协定 (1995) > 第5条 常设机构与第7条 营业利润",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "China-Vietnam DTA (1995) Art 5 & 7: Building site, construction, installation or assembly project, or supervisory activities in connection therewith, constitutes a permanent establishment only if it lasts more than 6 months. Profits taxable solely to the extent attributable to that PE.",
        "text_en": "Construction, installation site or supervisory activity in Vietnam constitutes a PE only if lasting over 6 months; profits outside Vietnam are exempt from Vietnamese tax.",
        "text_zh": "【建筑工地与工程监理常设机构6个月门槛与离岸利润免税】：建筑工地、建筑、安装或装配工程，或者与其相关的工程监理活动，唯有在存续时间持续超过 6 个月时，方构成常设机构；只有可归属于该常设机构的利润，越南税务机关方有权征税！【出海攻防启示】：中资企业化解越南外国承包商税（FCT）重复征税的关键！越南国内法对外国承包商征收严苛的 FCT（包含企业所得税 CIT 与增值税 VAT）。中资企业短期派遣专家赴越进行设备调试或技术指导（6个月以内），应依据中越 DTA 第 5 条与第 7 条向越南税务局申请《协定待遇免税核准》（DTA Tax Relief），全额免除 5% 的企业所得税预扣！",
        "norm_category": "tax_compliance",
        "mandatory_level": "directory",
        "elements_json": json.dumps([
            {"eid": "e_cn_vn_dta_6_months_rule", "text_zh": "要件一：中资技术服务或施工人员在越南现场停留作业累计时间在任一连续期间内不超过 6 个月", "status": "condition_precedent"},
            {"eid": "e_cn_vn_dta_treaty_application_filing", "text_zh": "要件二：在越南向主管税务机关正式提交中国税务机关出具之《中国税收居民身份证明》及协定申请", "status": "mandatory"},
            {"eid": "e_cn_vn_dta_cit_exemption_granted", "text_zh": "法律后果：越南依法核准免除该非居民企业在越南所负有的外国承包商税（FCT）中之企业所得税", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "TREATY:CN_MY_DTA_1985:Art5_7",
        "law": "TREATY:CN_MY_DTA_1985",
        "enbez": "Article 5 & 7",
        "title": "中国-马来西亚双重征税协定第5条与第7条：建筑安装常设机构6个月门槛与预扣税抵免",
        "heading_path": "中华人民共和国政府和马来西亚政府关于对所得避免双重征税和防止偷漏税的协定 (1985) > 常设机构与营业利润",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "China-Malaysia DTA (1985) Art 5 & 7: A building site or construction, installation or assembly project constitutes a permanent establishment only if it exists for more than 6 months. Taxes withheld in Malaysia under domestic tax law are creditable against Chinese income tax under Article 23.",
        "text_en": "Construction/installation project constitutes PE in Malaysia only if lasting over 6 months; domestic Withholding Tax creditable against Chinese tax under Art 23.",
        "text_zh": "【建筑工程常设机构6个月判定与预扣税Withholding Tax境外税额全额抵免】：建筑、安装或装配工程存续超过 6 个月方构成常设机构；马来西亚国内法依 1967 年所得税法第 107A 条扣缴的非居民承包商预扣税（10% 服务费加 3% 员工保证金），中资企业可凭马来西亚内陆税收局（LHDN）出具的正式预扣税完税凭单，直接依据协定第 23 条在中国境内年度汇算清缴时全额抵免中国企业所得税！【出海攻防启示】：避免双重纳税现金流回收！大马业主扣除的 10%+3% 预扣税款绝非直接损失！中资出海企业必须责令属地财务团队在缴税次月督导业主向 LHDN 索取正规 CP37 预扣税完税凭据，并在国内税局顺利完成境外税收抵免，彻底盘活千万元税收流动资金！",
        "norm_category": "tax_compliance",
        "mandatory_level": "directory",
        "elements_json": json.dumps([
            {"eid": "e_cn_my_dta_6m_duration", "text_zh": "要件一：大马工程施工项目合同工期或现场实施存续时间超过严格 6 个月法定周期", "status": "condition_precedent"},
            {"eid": "e_cn_my_dta_withholding_proof", "text_zh": "要件二：取得大马内陆税收局（LHDN）依 Sec 107A 盖章核发之正规 CP37 预扣税完税凭单", "status": "mandatory"},
            {"eid": "e_cn_my_dta_foreign_tax_credit", "text_zh": "法律后果：中资母公司在中国主管税务机关依法享受同等税额之境外所得税抵免，杜绝双重课税", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "TREATY:CN_SG_DTA_2007:Art5_7",
        "law": "TREATY:CN_SG_DTA_2007",
        "enbez": "Article 5 & 7",
        "title": "中国-新加坡避免双重征税协定第5条与第7条：建筑工程6个月PE判定与特许权使用费6%优惠税率",
        "heading_path": "中华人民共和国政府和新加坡共和国政府关于对所得避免双重征税和防止偷漏税的协定 (2007) > 常设机构与特许权使用费",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "China-Singapore DTA (2007) Art 5, 7 & 12: A building site, construction, assembly or installation project constitutes a PE only if lasting more than 6 months. Royalties paid for the use of industrial, commercial or scientific equipment enjoy a preferential withholding tax rate of 6% (or 10% for other intellectual property).",
        "text_en": "Construction site constitutes PE only if exceeding 6 months; royalties for equipment leasing or industrial rights taxed at preferential 6% withholding tax rate under Art 12.",
        "text_zh": "【建筑常设机构6个月门槛与工业设备租赁特许权使用费6%优惠税率】：建筑工地、装配或安装工程持续超过 6 个月构成常设机构；根据协定第12条，跨境支付工业、商业或科学设备租赁使用费的特许权使用费预扣税率，由新加坡国内法通常的 15% 大幅压降至协定优惠税率 6%！【出海攻防启示】：中资央企新加坡海外平台设备租赁税务筹划法宝！中资企业在新加坡设立国际业务总部或设备重资产租赁中心，向东盟各国项目出租大型盾构机、起重船等重型工程装备时，依据中新 DTA 能够将设备跨境租金预扣税压降至 6%，大幅降低跨境资产调配税负！",
        "norm_category": "tax_compliance",
        "mandatory_level": "directory",
        "elements_json": json.dumps([
            {"eid": "e_cn_sg_dta_equipment_leasing_nexus", "text_zh": "要件一：交易款项定性为向中资机构跨境租赁重型工程施工机械或工业专利技术特许使用费", "status": "condition_precedent"},
            {"eid": "e_cn_sg_dta_tax_residence_certificate", "text_zh": "要件二：向新加坡国内税务局（IRAS）出具由国家税务总局颁发的《中国税收居民身份证明》", "status": "mandatory"},
            {"eid": "e_cn_sg_dta_preferential_rate_6pct", "text_zh": "法律后果：强制适用协定 6% 封顶优惠预扣税率，免受新加坡国内法 15%~17% 高额税率盘剥", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "TREATY:RCEP:Chapter10_Services",
        "law": "TREATY:RCEP_2020",
        "enbez": "Chapter 10",
        "title": "区域全面经济伙伴关系协定RCEP第10章：建筑与工程服务贸易跨境国民待遇与透明度",
        "heading_path": "Regional Comprehensive Economic Partnership (RCEP 2020) > Chapter 10 Cross-Border Trade in Services > Construction and Engineering Services",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "RCEP Chapter 10 Cross-Border Trade in Services: Each Party shall accord to service suppliers of any other Party treatment no less favourable than that it accords, in like circumstances, to its own service suppliers. National Treatment and Market Access apply to construction and related engineering services sectors listed in Party's schedule without discriminatory numerical quotas or foreign equity caps beyond schedule reservations.",
        "text_en": "RCEP Chapter 10 guarantees National Treatment and Market Access for cross-border construction and engineering service suppliers across ASEAN, China, Japan, Korea, Australia and NZ.",
        "text_zh": "【建筑与工程服务贸易跨境国民待遇与排除非关税壁垒】：各成员方给予任何其他成员方工程服务提供者的待遇，在类似情况下不得低于给予其本国服务提供者的待遇（国民待遇 National Treatment）；在成员方具体承诺表开放的建筑安装工程服务领域，不得维持或采取设立合资企业强制形式、限制外国服务提供者数量或资本比例等未在承诺表中载明的额外限制性歧视措施！【出海攻防启示】：中资建筑服务打破东盟资质壁垒的国际法多边重器！东盟部分国家地方行业协会常出台土政策暗中限制中资企业承揽民营工程；中资企业可援引 RCEP 第 10 章向当地经贸部与竞争委员会提起行政复议，要求依法撤销针对中资工程服务提供者的非关税歧视性许可限制！",
        "norm_category": "bilateral_treaty",
        "mandatory_level": "directory",
        "elements_json": json.dumps([
            {"eid": "e_rcep10_crossborder_construction_service", "text_zh": "要件一：中资持牌工程企业向 RCEP 东盟成员方境内提供总承包施工或技术勘察设计服务", "status": "condition_precedent"},
            {"eid": "e_rcep10_discriminatory_local_restriction", "text_zh": "要件二：东道国行政规章出台超出其 RCEP 负面清单保留承诺范畴之非透明歧视性资质准入门槛", "status": "mandatory"},
            {"eid": "e_rcep10_national_treatment_enforcement", "text_zh": "法律后果：属于违反多边服务贸易承诺之违法行为，东道国应依法纠偏并保障外资平等竞争权", "status": "legal_consequence"}
        ], ensure_ascii=False)
    }
]

PHASE10_L2_REFERENCE_NORMS_PART2 = [
    # ========================================================
    # 3. 越南属地行业管理规程 (5条)
    # ========================================================
    {
        "table": "reference_norms",
        "norm_id": "VN:Decree_15_2021:Art102_104",
        "law": "VN:Decree_15_2021",
        "enbez": "Art 102-104",
        "title": "越南政府第15/2021号条例第102-104条：外国承包商作业许可证(Construction Operating License)与属地联营强制要件",
        "heading_path": "越南政府关于工程建设投资项目管理之第15/2021/ND-CP号条例 > 第八章 外国承包商在越建设活动管理 > 第102-104条 作业许可证与联营",
        "language_mode": "bilingual",
        "lang_original": "vi",
        "text_original": "Nghị định 15/2021/NĐ-CP Điều 102-104: Điều kiện cấp giấy phép hoạt động xây dựng cho nhà thầu nước ngoài: Nhà thầu nước ngoài chỉ được hoạt động xây dựng tại Việt Nam sau khi được cơ quan quản lý nhà nước có thẩm quyền cấp giấy phép hoạt động xây dựng. Nhà thầu nước ngoài phải liên danh với nhà thầu Việt Nam hoặc sử dụng nhà thầu phụ Việt Nam, trừ trường hợp nhà thầu trong nước không đủ năng lực tham gia.",
        "text_en": "Decree 15/2021/ND-CP Art 102-104: Foreign contractors must obtain a Construction Operating License before commencing works in Vietnam, and must enter into a joint venture or subcontract with Vietnamese contractors.",
        "text_zh": "【外国承包商作业许可证与强制属地联营分包要件】：外国承包商唯有在获得越南建设部或省级建设厅核发《建设活动许可证》（Giấy phép hoạt động xây dựng / Construction Operating License）后，方可在越南境内开展施工与工程管理活动；申请该执照的法定强制前置要件是：外国承包商必须与越南本土承包商组建联营体（Liên danh），或者承诺雇佣越南本土分包商；除非本土承包商欠缺实施该工程的专业技术能力！【出海攻防启示】：中资承包商在越未批先建与合同效力合规红线！中资总包在越南中标 EPC 项目后，必须在开工前严格耗时 20 个工作日办妥作业许可证；若未取得执照即擅自进场施工，建设监察总署依法有权查封现场、课处最高 1 亿越盾行政罚款，发包人亦有权以‘非法施工’为由拒绝签发工程进度款支付证书！",
        "norm_category": "construction_regulatory",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_vn_lic_award_qualification", "text_zh": "要件一：外国承包商已正式赢得越南境内工程招标或取得业主合法发包合同文件", "status": "condition_precedent"},
            {"eid": "e_vn_lic_local_partnership_mandate", "text_zh": "要件二：外国总承包商已与越南本土合规承包商签署正式联营协议或分包备忘录", "status": "mandatory"},
            {"eid": "e_vn_lic_issuance_validity", "text_zh": "法律后果：建设行政主管部门颁发作业许可证，确立在越开工结算与调配外籍专家进场合法地位", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "VN:Decree_10_2021:Art18_20",
        "law": "VN:Decree_10_2021",
        "enbez": "Art 18-20",
        "title": "越南政府第10/2021号条例第18-20条：政府投资工程造价指数与官方调差公式",
        "heading_path": "越南政府关于建设投资造价管理之第10/2021/ND-CP号条例 > 建设工程合同价款调整 > 第18-20条 官方调差公式与造价指数",
        "language_mode": "bilingual",
        "lang_original": "vi",
        "text_original": "Nghị định 10/2021/NĐ-CP Điều 18-20: Điều chỉnh giá hợp đồng xây dựng: Việc điều chỉnh giá hợp đồng xây dựng có sử dụng vốn nhà nước phải phù hợp với loại giá hợp đồng, nội dung hợp đồng đã ký kết. Trường hợp điều chỉnh theo phương pháp bù trừ trực tiếp hoặc sử dụng hệ số trượt giá, phải căn cứ vào chỉ số giá xây dựng do Bộ Xây dựng hoặc Ủy ban nhân dân cấp tỉnh công bố tại thời điểm điều chỉnh.",
        "text_en": "Decree 10/2021/ND-CP Art 18-20: Construction contract price adjustment under state-funded projects must apply official construction price indices published by Ministry of Construction or provincial People's Committees.",
        "text_zh": "【政府投资工程调差法定公式与官方造价指数适用】：使用越南国家财政资金、国有企业资本投资的建设工程合同，价款调整必须严格遵循合同约定的调价机制；若采用系数滑移调价公式（Formula Method）或直接补差法，公式中的人工、水泥、钢材、柴油等各项权重系数，必须严格以越南建设部或省级人民委员会在调价当期官方公布的《建设工程价格指数》（Chỉ số giá xây dựng）为排他性计算基准！【出海攻防启示】：中资央企政府项目抗通胀调价铁律！中资企业在越南参与主权借款或国有电力公司（EVN）投资的大型基建时，合同中的调价条款绝不能写笼统的‘协商解决’，必须严格对齐 Decree 10/2021 第 19 条官方调差公式结构，并将各省建设厅发布的月份造价指数作为变量锁定在合同专用条款中，确保上千万美元通胀材料差价得以顺利审计结算！",
        "norm_category": "construction_regulatory",
        "mandatory_level": "directory",
        "elements_json": json.dumps([
            {"eid": "e_vn_price_adj_state_funded", "text_zh": "要件一：建设项目资金来源涉及越南公共财政资金、主权外债或国有企业投资资本", "status": "condition_precedent"},
            {"eid": "e_vn_price_adj_official_indices", "text_zh": "要件二：调差计算严格基于履约期内建设部或省级主管机关定期官方发布之权威造价指数", "status": "mandatory"},
            {"eid": "e_vn_price_adj_audit_settlement", "text_zh": "法律后果：国家审计署与财政主管机关认可该调增造价支出合法性并准予财政预算资金拨付", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "VN:Decision_21_2023_MOIT",
        "law": "VN:Decision_21_2023_MOIT",
        "enbez": "Decision 21/2023",
        "title": "越南工贸部第21/2023号决定：可再生能源过渡期并网电价(Transitional Tariff)折价机制",
        "heading_path": "越南工贸部规范性文件 (Quyết định số 21/QĐ-BCT) > 新能源电力价格框架 > 未赶上FIT过渡期风电光伏临时结算电价",
        "language_mode": "bilingual",
        "lang_original": "vi",
        "text_original": "Quyết định 21/QĐ-BCT (2023): Quy định khung giá phát điện nhà máy điện mặt trời, điện gió chuyển tiếp: Giá trần áp dụng cho nhà máy điện mặt trời mặt đất là 1.184,90 đồng/kWh; điện mặt trời nổi 1.508,27 đồng/kWh; điện gió trên đất liền 1.587,12 đồng/kWh; điện gió trên biển 1.815,95 đồng/kWh. Tập đoàn Điện lực Việt Nam (EVN) và chủ đầu tư đàm phán giá tạm tính bằng 50% giá trần.",
        "text_en": "Decision 21/QĐ-BCT (2023): Tariff framework for transitional solar and wind power plants missing statutory FIT deadlines; sets price ceilings and temporary PPA calculation at 50% of ceiling.",
        "text_zh": "【可再生能源过渡期并网电价天花板与50%临时折价结算机制】：针对未能在法定截止日前实现 COD 商业并网的过渡期风电与光伏电站，越南工贸部（MOIT）出台严苛的最高限价框架：地面光伏最高限价为 1,184.9 越盾/千瓦时（较旧 FIT2 下跌近 30%）；海上风电最高限价 1,815.95 越盾/千瓦时；在双方正式完成最终电价核定谈判前，越南电力集团（EVN）仅按该最高限价的 50% 支付临时过渡电价！【出海攻防启示】：中资出海越南新能源数十亿美元投资的暴风眼！大量中资央企投资或总包的越南光伏风电项目因疫情延期错失 FIT 补贴末班车，落入 Decision 21 严厉压价区间。中资企业必须一方面在 PPA 谈判中咬定上限电价争取追溯补差，另一方面启动海外投资保险与 EPC 延误责任穿透索赔，化解项目公司现金流断裂危机！",
        "norm_category": "energy_mining",
        "mandatory_level": "directory",
        "elements_json": json.dumps([
            {"eid": "e_vn_re_transitional_project", "text_zh": "要件一：光伏或风力发电项目已完成实质建设但因超期未能在法定原优惠 FIT 截止日前取得商业运营 COD", "status": "condition_precedent"},
            {"eid": "e_vn_re_statutory_ceiling_cap", "text_zh": "要件二：发售电双方签订之过渡期购电协议（PPA）价格受制于工贸部 Decision 21 最高天花板", "status": "mandatory"},
            {"eid": "e_vn_re_temporary_50pct_cashflow", "text_zh": "法律后果：EVN 合法执行 50% 临时过渡电价拨付直至部委完成电站最终投资总额审计确权", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "VN:Circular_02_2023_TT_BXD",
        "law": "VN:Circular_02_2023_TT_BXD",
        "enbez": "Circular 02/2023",
        "title": "越南建设部第02/2023号通告：EPC工程总承包合同标准指导通用条款与履约保函要求",
        "heading_path": "越南建设部规程 (Thông tư 02/2023/TT-BXD) > 建设工程合同指引 > EPC工程总承包标准合同模板与履约保证金",
        "language_mode": "bilingual",
        "lang_original": "vi",
        "text_original": "Thông tư 02/2023/TT-BXD: Hướng dẫn chi tiết một số nội dung về hợp đồng xây dựng: Mẫu hợp đồng tổng thầu EPC áp dụng cho các dự án sử dụng vốn nhà nước. Giá trị bảo đảm thực hiện hợp đồng được quy định từ 2% đến 10% giá trị hợp đồng tùy thuộc vào quy mô và tính chất công trình. Thời hạn bảo đảm phải kéo dài cho đến khi hoàn thành toàn bộ nghĩa vụ theo hợp đồng và được nghiệm thu bàn giao.",
        "text_en": "Circular 02/2023/TT-BXD: Regulates standard EPC General Contracting terms for state-funded projects, fixing performance security between 2% and 10% until final handover acceptance.",
        "text_zh": "【EPC工程总承包标准合同指引与履约担保金法定比例区间】：建设部发布的官方 EPC 标准合同范本明确：对于涉及公共资本的 EPC 项目，履约担保金（Performance Guarantee）比例强制限定在合同总价的 2% 至 10% 之间，严禁发包人随意要求开立畸高的保函；担保期限必须持续至总承包商完成全部合同义务并取得工程正式竣工验收交接证书之日！【出海攻防启示】：中资 EPC 总包对抗越南发包人保函霸王条款的利器！个别越南项目业主在招标文件中要求总承包商开具高达 20%~25% 的履约与付款保函；中资企业应引用 Circular 02/2023 坚决要求将保函上限压回 10% 以内，并锁定在取得初验证书（PAC）后保函额度自动缩减一半，大幅节约银行授信成本！",
        "norm_category": "construction_regulatory",
        "mandatory_level": "directory",
        "elements_json": json.dumps([
            {"eid": "e_vn_epc_standard_template", "text_zh": "要件一：工程项目采用设计-采购-施工（EPC）一体化交钥匙模式在越南实施", "status": "condition_precedent"},
            {"eid": "e_vn_epc_statutory_guarantee_cap", "text_zh": "要件二：履约保函开具金额严格遵照法定 2%~10% 区间设立且格式符合规范指引", "status": "mandatory"},
            {"eid": "e_vn_epc_release_upon_handover", "text_zh": "法律后果：发包人在工程通过竣工整体验收交接时负有立即退还履约保函原件之法定义务", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "VN:Law_43_2013_Procurement:Art89",
        "law": "VN:Law_43_2013_Procurement",
        "enbez": "Art 89",
        "title": "越南招标法第89条：公共采购招投标围标借资质禁止行为与黑名单惩戒",
        "heading_path": "越南招投标法 (Law No. 43/2013/QH13) > 招投标中的禁止行为 > 第89条 围标、借牌与行贿禁止",
        "language_mode": "bilingual",
        "lang_original": "vi",
        "text_original": "Luật Đấu thầu số 43/2013/QH13 Điều 89: Các hành vi bị cấm trong đấu thầu: Thông thầu; gian lận trong đấu thầu bao gồm việc trình bày sai lệch năng lực, làm giả tài liệu chứng minh; chuyển nhượng thầu trái phép sau khi trúng thầu; sử dụng tư cách nhà thầu khác để tham dự thầu (mượn tư cách pháp nhân). Nhà thầu vi phạm sẽ bị cấm tham gia hoạt động đấu thầu từ 1 năm đến 5 năm trên toàn quốc.",
        "text_en": "Procurement Law Art 89: Strictly prohibits bid rigging, fraudulent falsification of financial credentials, and unlawful subletting/lending of bidding entity; violators barred from bidding for 1-5 years nationwide.",
        "text_zh": "【招投标严厉禁止行为与全国禁标黑名单追责】：招标法第89条明文列举以下禁止行为：（1）围标串标（Thông thầu）；（2）投标欺诈，包括伪造财务审计报告、虚构人员设备业绩；（3）借用其他法人资质借壳投标（Mượn tư cách）；（4）中标后非法全盘转包！违反本条的承包商，将被越南计划投资部处以没收全部投标保证金、并在 1 年至 5 年内被列入全国公共工程禁标黑名单，情节严重的移送公安机关追究刑事责任！【出海攻防启示】：中资企业出海在越合规最高禁令！中资企业万万不可为了拿下项目而与当地中介商串通‘借壳投标’或伪造国内母公司业绩印章；一旦被越南反贪部门或竞争对手举报查实，不仅面临全国黑名单禁标、全额没收保函，项目公司负责人更将面临越南刑法走私贪腐重罪指控！",
        "norm_category": "construction_regulatory",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_vn_procure_bidding_fraud", "text_zh": "要件一：投标人在招投标过程中存在伪造业绩资质证明、合谋串通报价或擅自借牌行为", "status": "condition_precedent"},
            {"eid": "e_vn_procure_formal_investigation", "text_zh": "要件二：招标主管机关或越南国家监察总署经法定调查程序做出了存在欺诈串通之行政认定", "status": "mandatory"},
            {"eid": "e_vn_procure_nationwide_debarment", "text_zh": "法律后果：强制没收投标保函，中标结果自始绝对无效，并在 1~5 年内列入全国公共工程禁标黑名单", "status": "prohibition"}
        ], ensure_ascii=False)
    },

    # ========================================================
    # 4. 印尼属地能矿采购规程 (5条)
    # ========================================================
    {
        "table": "reference_norms",
        "norm_id": "ID:Permen_PUPR_14_2020:Standard_Bidding",
        "law": "ID:Permen_PUPR_14_2020",
        "enbez": "Standard Bidding",
        "title": "印尼公共工程部第14/2020号部长令：公共工程标准招标文件与本地化率(TKDN)强制扣分机制",
        "heading_path": "印尼公共工程与民用住房部规程 (Permen PUPR No. 14/PRT/M/2020) > 建设工程服务选拔标准与规程 > 本地成分TKDN强制合规",
        "language_mode": "bilingual",
        "lang_original": "id",
        "text_original": "Peraturan Menteri PUPR No. 14/2020: Standar dan Pedoman Pengadaan Jasa Konstruksi melalui Penyedia: Penggunaan produk dalam negeri merupakan kewajiban dengan memperhitungkan Tingkat Komponen Dalam Negeri (TKDN). Peserta tender yang menawarkan TKDN lebih tinggi berhak mendapatkan preferensi harga hingga 25%. Kontraktor asing yang gagal memenuhi komitmen TKDN yang ditawarkan dikenakan sanksi denda finansial dan sanksi daftar hitam.",
        "text_en": "Permen PUPR 14/2020: Standard Procurement Guidelines for Construction: Mandates local content requirement (TKDN); offers up to 25% price preference for high TKDN; penalizes failure with fines and blacklisting.",
        "text_zh": "【印尼公共工程标准采购招标文件与TKDN本地化率强制考核机制】：外国承包商参与印尼政府及国企工程招投标，必须严格计算并申报工程的本地成分含量（TKDN）；提供高 TKDN 的投标企业可依法享有最高达 25% 的评标价格优惠折扣（Price Preference）；但承包商在中标履约后若未能兑现投标承诺的 TKDN 比例，将面临巨额经济违约罚款，严重者被直接取消公共工程总包资质并列入黑名单！【出海攻防启示】：中资企业参与印尼基建投标算分命脉！中资企业不能单凭低价取胜，必须提前与印尼本土持有工业部 TKDN 认证证书的钢厂、水泥厂和设备供应商建立战略采购联盟，在投标模型中将 TKDN 比例精准拉升至 40% 门槛以上，充分吃满 25% 官方评标加分，力克西方竞争对手！",
        "norm_category": "construction_regulatory",
        "mandatory_level": "directory",
        "elements_json": json.dumps([
            {"eid": "e_id_pupr_public_procurement", "text_zh": "要件一：参加印尼公共工程部或国有企业（BUMN）发起之基础设施工程公开招投标", "status": "condition_precedent"},
            {"eid": "e_id_pupr_tkdn_calculation_sheet", "text_zh": "要件二：提交经过第三方认证机构审计合规之本土设备人工建筑材料（TKDN）自评比例清单", "status": "mandatory"},
            {"eid": "e_id_pupr_price_preference_granted", "text_zh": "法律后果：评标委员会依法核准最高 25% 价格折价加分；中标后对未达标差额强制征收违约金", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "ID:UU_3_2020_Minerba:Art102_103",
        "law": "ID:UU_3_2020_Minerba",
        "enbez": "Art 102-103",
        "title": "印尼2020年新矿业法第102-103条：原矿强制在岸冶炼深加工与出口配额绝对禁令",
        "heading_path": "印尼矿产与煤炭开采法修正案 (UU No. 3/2020 amending UU No. 4/2009) > 矿产增值与在岸加工义务 > 第102-103条 强制冶炼与出口管制",
        "language_mode": "bilingual",
        "lang_original": "id",
        "text_original": "Undang-Undang No. 3 Tahun 2020 Pasal 102-103: Pemegang IUP atau IUPK pada tahap kegiatan operasi produksi pertambangan mineral wajib melakukan peningkatan nilai tambah mineral di dalam negeri melalui kegiatan pengolahan dan/atau pemurnian mineral di dalam negeri. Dilarang melakukan penjualan mineral mentah (raw materials/ore) ke luar negeri.",
        "text_en": "Mining Law (UU 3/2020) Art 102-103: Holders of mining permits (IUP/IUPK) are legally obligated to process and refine minerals onshore; outright export ban on raw ores.",
        "text_zh": "【原矿在岸强制冶炼深加工法定义务与出口绝对禁令】：持有矿业营业许可证（IUP/IUPK）的矿山开发企业，必须在印尼境内对所开采的金属矿产实施深加工或在岸冶炼（Smelting），以提高矿产品在境内的附加值；印尼法律绝对禁止对外出口任何形态的原矿石（Raw Ore，特别是镍矿、铝土矿、铜精矿）！违规走私原矿者直接吊销采矿执照并追究刑事责任！【出海攻防启示】：中资镍矿投资在岸建厂的母法渊源！印尼正是凭借此项法律彻底终结了中资企业‘单纯买矿运回国内’的粗放模式，倒逼中资央企及民营巨头（如青山、德龙、华友）在印尼莫罗瓦利、纬达贝等地重资产投资数十座一体化工业园与火法/湿法高压酸浸冶炼厂（HPAL）；在开展新投资前必须确保拥有自建或绑定的合规冶炼厂，绝不可心存原矿出口侥幸！",
        "norm_category": "energy_mining",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_id_minerba_mining_concession", "text_zh": "要件一：在印尼境内持有合法有效之金属矿产开采生产营业许可证（IUP Operasi Produksi）", "status": "condition_precedent"},
            {"eid": "e_id_minerba_onshore_smelter_facility", "text_zh": "要件二：自建或通过协议完全绑定印尼境内已商业投产之在岸冶炼提纯加工工厂设施", "status": "mandatory"},
            {"eid": "e_id_minerba_raw_export_prohibition", "text_zh": "法律后果：严禁向境外直接出口未经提炼的原矿原料，违者海关立即查扣没收并吊销矿业执照", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "ID:Permen_ESDM_11_2020:HPM",
        "law": "ID:Permen_ESDM_11_2020",
        "enbez": "Permen ESDM 11/2020",
        "title": "印尼能矿部第11/2020号令：镍矿官方基准价格(HPM)强制结算公式与转让定价合规",
        "heading_path": "印尼能源与矿产资源部条例 (Permen ESDM No. 11/2020) > 矿产基准价格(HPM)规程 > 镍矿在岸交易定价与履约结算",
        "language_mode": "bilingual",
        "lang_original": "id",
        "text_original": "Peraturan Menteri ESDM No. 11 Tahun 2020: Tata Cara Penetapan Harga Patokan Mineral (HPM) Logam: Pembelian bijih nikel oleh smelter dalam negeri wajib mengacu pada HPM Logam nikel yang ditetapkan setiap bulan oleh Menteri. Kontrak penjualan yang menetapkan harga di bawah HPM dinyatakan batal demi hukum untuk klausul harga dan transaksi wajib disesuaikan dengan HPM. Pihak yang melanggar dikenakan sanksi peringatan tertulis hingga pencabutan izin.",
        "text_en": "Permen ESDM 11/2020: Mandates that domestic nickel ore transactions by smelters must adhere to monthly official Benchmark Mineral Price (HPM); clauses below HPM are legally void.",
        "text_zh": "【镍矿官方基准价HPM强制挂钩与低于指导价买卖条款自始无效】：印尼境内所有镍矿冶炼厂向本地矿山采购镍原矿时，结算交易价格必须严格参照能矿部（ESDM）每月公布的官方金属矿物基准价格（Harga Patokan Mineral / HPM）；任何低于官方 HPM 基准价格的买卖合同价格约定在法律上自始无效，必须强行调整为 HPM 计价！违规低价收购的冶炼厂，将面临责令整改、吊销电力接入乃至关停冶炼厂的行政重罚！【出海攻防启示】：中资在印尼大型镍冶炼厂供应链成本红线！早期部分中资冶炼厂通过长期固定折价协议（Discounted Offtake）向关联矿山低价买矿以压低成本；ESDM 11/2020 号令实施后，该行为被定性为严重违法避税；中资企业必须全盘重构原矿采购合同，全面接入 HPM 浮动公式并由官方认可的独立质检机构（Surveyor，如 Sucofindo/Carsurin）出具化验品位单据，彻底杜绝转让定价被印尼国税局巨额罚款！",
        "norm_category": "energy_mining",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_id_hpm_nickel_ore_purchase", "text_zh": "要件一：在印尼境内发生的镍原矿或高冰镍原料向在岸冶炼厂交付转移之商业买卖行为", "status": "condition_precedent"},
            {"eid": "e_id_hpm_monthly_official_index", "text_zh": "要件二：结算单价严格挂钩能矿部当月发布的伦敦金属交易所（LME）联动 HPM 官方基准价", "status": "mandatory"},
            {"eid": "e_id_hpm_mandatory_price_adjustment", "text_zh": "法律后果：任何低于 HPM 之民间价格协议自动无效，税务局有权强制按 HPM 重新核定征收特许权税及增值税", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "ID:Perpres_12_2021_Procurement:Art65",
        "law": "ID:Perpres_12_2021_Procurement",
        "enbez": "Art 65",
        "title": "印尼总统第12/2021号令：政府公共采购本国产品使用强制配额(TKDN >= 40%)",
        "heading_path": "印尼总统令关于政府货物与服务采购之第12/2021号令 (Perpres No. 12/2021 amending Perpres 16/2018) > 本国产品使用强制配额 > 第65条",
        "language_mode": "bilingual",
        "lang_original": "id",
        "text_original": "Peraturan Presiden No. 12 Tahun 2021 Pasal 65: Penggunaan produk dalam negeri: Kementerian/Lembaga/Pemerintah Daerah wajib mengalokasikan paling sedikit 40% dari nilai anggaran belanja barang/jasa untuk penggunaan produk usaha mikro, usaha kecil, dan/atau koperasi dari hasil produksi dalam negeri. Wajib menggunakan produk dalam negeri apabila terdapat produk yang memiliki penjumlahan nilai TKDN ditambah nilai BMP paling sedikit 40%.",
        "text_en": "Perpres 12/2021 Art 65: Ministries and state agencies must allocate >= 40% procurement budget to domestic products; imported goods strictly prohibited where TKDN + BMP reaches >= 40%.",
        "text_zh": "【政府公共采购本国产品强制门槛TKDN加BMP达到40%严禁采购进口产品】：印尼中央部委、政府机构及地方政府在实施公共财政采购时，必须将采购预算的至少 40% 专项分配给本国中小微企业及合作社产品；当市场上存在本国产品且其本地化率（TKDN）加上企业公司实力加分（BMP）之和达到或超过 40% 时，招标采购部门在法律上被绝对禁止采购任何外国进口产品！【出海攻防启示】：中资央企投标印尼高铁、港口、电网公共采购的设备选用红线！当中资联合体参与印尼公共资金招标时，若投标方案设计中包含大量从中国直接出口的标准电力变压器、电缆或阀门，而印尼当地已有达到 40% TKDN 的替代本土产能，该投标将被印尼采购公署（LKPP）直接按违法采购予以一票否决！必须全面实行机电设备属地化组装或采购！",
        "norm_category": "construction_regulatory",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_id_perpres65_public_budget_source", "text_zh": "要件一：采购资金来源于印尼国家国家预算（APBN）或地方财政预算（APBD）", "status": "condition_precedent"},
            {"eid": "e_id_perpres65_available_local_40pct", "text_zh": "要件二：工业部官方目录中已注册存在本地成分 TKDN + BMP 达到或超过 40% 的同类本国工业产品", "status": "mandatory"},
            {"eid": "e_id_perpres65_import_ban", "text_zh": "法律后果：招标人依法严禁批准进口外国同类设备，外商直接进口投标方案予以直接废标排除", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "ID:PP_35_2021_Labor:Art15_17",
        "law": "ID:PP_35_2021_Labor",
        "enbez": "Art 15-17",
        "title": "印尼政府第35/2021号条例：固定期限劳动合同(PKWT)到期经济补偿金法定计发标准",
        "heading_path": "印尼政府第35/2021号条例 (PP No. 35/2021 Implementing Law No. 11/2020 Cipta Kerja) > 固定期限劳动合同(PKWT) > 第15-17条 到期法定补偿金计发公式",
        "language_mode": "bilingual",
        "lang_original": "id",
        "text_original": "Peraturan Pemerintah No. 35 Tahun 2021 Pasal 15-17: Uang Kompensasi PKWT: Pengusaha wajib memberikan uang kompensasi kepada pekerja/buruh yang mempunyai hubungan kerja berdasarkan PKWT pada saat berakhirnya PKWT. Uang kompensasi diberikan kepada pekerja yang telah mempunyai masa kerja paling sedikit 1 bulan secara terus menerus. Besaran uang kompensasi: PKWT 12 bulan terus menerus diberikan sebesar 1 bulan upah; masa kerja kurang dari atau lebih dari 12 bulan dihitung secara proporsional.",
        "text_en": "PP 35/2021 Art 15-17: Employers must pay statutory severance compensation (Uang Kompensasi) to fixed-term contract workers (PKWT) upon expiration/termination, calculated proportionally to tenure.",
        "text_zh": "【固定期限劳动合同PKWT到期法定经济补偿金强制计发标准】：雇主必须在固定期限劳动合同（PKWT）期满终止时，向连续工作满 1 个月以上的印尼本国员工支付法定经济补偿金（Uang Kompensasi）；连续工作满 12 个月的，支付相当于 1 个月工资的补偿金；工作年限少于或超过 12 个月的，按‘实际工作月数 / 12 × 1个月全额工资’公式同等按比例折算计发！即使合同系因期满自然终止而非解雇，该补偿金依然属于强制法定义务！【出海攻防启示】：中资企业印尼用工成本核算必须计提的刚性支出！过去印尼法下固定合同到期无需补偿，许多中资企业因此未予预提用工准备金；2021 年新规出台后，凡雇佣印尼属地施工工人或项目员工，必须在每月财务报表中按员工月薪的 8.33%（即1/12）足额预提合同期满补偿金专项基金，避免工程竣工遣散数千名印尼员工时爆发大规模罢工或劳资围堵项目部群体性事件！",
        "norm_category": "labor_employment",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_id_pkwt_fixed_term_employment", "text_zh": "要件一：用人单位与印尼本土劳工之间依法签署合法有效之固定期限劳动雇佣合同（PKWT）", "status": "condition_precedent"},
            {"eid": "e_id_pkwt_tenure_over_1m_expired", "text_zh": "要件二：劳工连续在岗工龄满 1 个月以上且合同期限届满或由雇主提前终止", "status": "mandatory"},
            {"eid": "e_id_pkwt_statutory_severance_duty", "text_zh": "法律后果：强制执行按工龄比例全额发放经济补偿金，未足额计发构成拖欠工资行政违法处罚", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },

    # ========================================================
    # 5. 马来西亚行业管理规程 (5条)
    # ========================================================
    {
        "table": "reference_norms",
        "norm_id": "MY:PAM_Subcontract_2018:Cl27",
        "law": "MY:PAM_Subcontract_2018",
        "enbez": "Clause 27",
        "title": "马来西亚建筑师学会PAM标准分包合同第27条：指定分包商(NSC)款项直付与索赔通知",
        "heading_path": "Malaysian Institute of Architects (PAM) Sub-Contract 2018 > Clause 27 Nominated Sub-Contractors (NSC) > Direct Payment and Notice Provisions",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "PAM Sub-Contract 2018 Clause 27: Direct Payment to Nominated Sub-Contractor: The Employer shall be entitled, upon written certificate from the Architect that the Main Contractor has failed to show reasonable cause for withholding payment due to the NSC, to make direct payment to the NSC and deduct such amount from monies due to the Main Contractor.",
        "text_en": "PAM Sub-Contract 2018 Cl 27: Authorizes Employer to make direct payment to Nominated Sub-Contractor (NSC) upon Architect's certificate of Main Contractor's default, deducting from Main Contractor.",
        "text_zh": "【发包人向指定分包商NSC直接付款机制与建筑师证书核准】：在马来西亚 PAM 建筑工程合同体系下，若建筑师（Architect）出具正式书面证明，确认总承包商在收到发包人付款后无正当理由拖欠扣留应当支付给指定分包商（NSC）的到期核定款项，发包人（业主）依法有权越过总承包商，直接将工程款项付至 NSC 银行账户，并从随后应付给总承包商的任何款项中全额同等抵扣！【出海攻防启示】：中资总承包商资金链隔离防火墙！中资总包若在大马承接 PAM 合同住宅商业项目，若对指定分包商（NSC）的施工质量或工期存在合理争议，必须在收到建筑师 IPC 后 7 天内正式提交详细的抗辩异议理由书；切勿无声无息扣留款项，否则发包人启动 Cl 27 直付程序将导致总包丧失对抗分包商的工程款制衡筹码！",
        "norm_category": "construction_regulatory",
        "mandatory_level": "directory",
        "elements_json": json.dumps([
            {"eid": "e_my_pam_nsc_designation", "text_zh": "要件一：分包商系依据雇主或建筑师正式指定程序选定之指定分包商（NSC）", "status": "condition_precedent"},
            {"eid": "e_my_pam_architect_default_certificate", "text_zh": "要件二：建筑师依法核发确认总承包商未在合理期限内展现正当拒付理由之违规凭单", "status": "mandatory"},
            {"eid": "e_my_pam_lawful_direct_payment", "text_zh": "法律后果：发包人享有合法直接向 NSC 拨付工程款权利，并在总承包商应付工程款中同等抵扣", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "MY:CIDB_Standard_Contract_2000:Cl44",
        "law": "MY:CIDB_Standard_Contract_2000",
        "enbez": "Clause 44",
        "title": "马来西亚建筑发展局CIDB标准合同第44条：工期顺延EOT事件认定与关键路径评估",
        "heading_path": "CIDB Standard Form of Contract for Building Works (2000 Edition) > Clause 44 Extension of Time (EOT) > Relevant Events and Critical Path Assessment",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "CIDB 2000 Clause 44: Extension of Time: If the completion of Works is delayed beyond the Completion Date by reason of any of the Relevant Events (force majeure, exceptionally adverse weather, employer delay, architect variations), the Contractor shall give written notice within 30 days. The Superintending Officer (S.O.) shall assess delay impacting the critical path and grant an equitable extension.",
        "text_en": "CIDB 2000 Cl 44: Contractor entitled to EOT for delays caused by Relevant Events impacting critical path, provided written notice is submitted within 30 days.",
        "text_zh": "【CIDB标准合同工期顺延EOT相关事件与30天时限关键路径评估】：因发生法定‘相关事件’（包括不可抗力、异常恶劣气候、发包人迟延交地、主管工程师签发重大工程设计变更等）导致工程竣工日期延误的，承包商必须在延误事件发生后 30 天内提交正式书面通知；监理官（S.O.）应当根据工程施工网络计划对关键路径（Critical Path）的影响进行客观评估，并核定授予公平合理的工期顺延天数！【出海攻防启示】：大马工程延误反索赔技术准绳！中资施工企业必须建立与大马 CIDB 标准完全兼容的 Primavera P6 动态进度计划，任何业主要求的设计变更或现场阻碍，必须在 30 天内同步提交时间影响分析（Time Impact Analysis / TIA），证明延误直接击穿关键路径，锁定 EOT 批复并彻底阻断业主索赔误期罚金（LAD）！",
        "norm_category": "construction_regulatory",
        "mandatory_level": "directory",
        "elements_json": json.dumps([
            {"eid": "e_my_cidb_relevant_delay_event", "text_zh": "要件一：延误事件属于发包人违约、设计变更或异常恶劣天气等合同明载之相关事件范畴", "status": "condition_precedent"},
            {"eid": "e_my_cidb_written_notice_30d", "text_zh": "要件二：承包商在知晓延误后严格 30 天内向监理官（S.O.）提交载明工期影响之正式书面通知", "status": "mandatory"},
            {"eid": "e_my_cidb_eot_award_discharge_lad", "text_zh": "法律后果：监理官核准授予工期顺延天数，雇主在该顺延天数期间丧失扣罚误期损害赔偿金（LAD）之权利", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "MY:Income_Tax_Act_1967:Sec107A_109",
        "law": "MY:Income_Tax_Act_1967",
        "enbez": "Sec 107A & 109",
        "title": "马来西亚1967年所得税法第107A/109条：非居民承包商10%+3%预扣税(Withholding Tax)代扣规程",
        "heading_path": "马来西亚1967年所得税法 (Act 53) > 预扣税制度 > 第107A条 非居民承包商与分包商服务费代扣",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Income Tax Act 1967 Sec 107A: Deduction of tax from contract payment: Where a person is liable to make contract payment to a non-resident contractor in respect of services under a contract, that person shall deduct withholding tax at: (a) 10% of the service portion of the contract payment on account of tax which may be payable by that non-resident contractor; and (b) 3% of the contract payment on account of tax payable by employees of that contractor. Must be remitted to Inland Revenue Board (LHDN) within 1 month.",
        "text_en": "ITA 1967 Sec 107A: Payer must deduct 10% (corporate tax) + 3% (employee tax) withholding tax from service payments to non-resident contractors and remit to LHDN within 30 days.",
        "text_zh": "【非居民外国承包商10%+3%工程款法定预扣代缴制度与30天汇缴期限】：在马来西亚向非税收居民外国承包商支付涉及工程劳务、安装或调试服务款项的发包人或总包商，必须依法代扣代缴预扣税（Withholding Tax）：其中（a）扣缴服务费合同额的 10%，用于折抵该外国承包商的企业所得税；（b）扣缴 3%，作为该外国承包商雇佣员工的个人所得税保证金！该 13% 预扣款项必须在付款之日起严格 1 个月内全额汇缴至马来西亚内陆税收局（LHDN），逾期未扣缴者将被处以 10% 滞纳金罚款，且该笔工程款不得在发包人企业所得税前列支！【出海攻防启示】：中资未设立属地公司的跨境直签合同重大税务现金流陷阱！若中资母公司未在大马设立子公司或登记分包常设机构，大马业主支付进度款时将强制扣除 13% 现金！中资企业在编制投标报价时必须测算该预扣税成本，或在合同中设立‘税收全额总额提升条款’（Gross-Up Clause），确保中方实际到手净金额不受影响！",
        "norm_category": "tax_compliance",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_my_wht_nonresident_contractor", "text_zh": "要件一：合同收款方属于未在马来西亚登记为常设税收居民之外国境外法人承包商", "status": "condition_precedent"},
            {"eid": "e_my_wht_service_portion_deduction", "text_zh": "要件二：发包人对工程款中的技术服务劳务成分依法扣留 10% 企业税与 3% 员工税", "status": "mandatory"},
            {"eid": "e_my_wht_lhdn_remittance_30d", "text_zh": "法律后果：30天内汇缴至 LHDN 并取得 CP37 完税单，未合规扣缴者发包人自负全额追缴与罚款", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "MY:Employment_Act_1955_Amended:Sec60K",
        "law": "MY:Employment_Act_1955_Amended",
        "enbez": "Sec 60K",
        "title": "马来西亚劳工法2022年修正案第60K条：雇佣外籍劳工劳工局事前批准强制要件与合规审查",
        "heading_path": "马来西亚劳工法令 (Employment Act 1955 as amended by Act A1651) > 外籍劳工雇佣管理 > 第60K条 劳工局总监事前批准强制要件",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Employment Act 1955 Sec 60K: Employment of foreign employee: No employer shall employ a foreign employee unless with the prior approval of the Director General of Labour. An employer who employs a foreign employee without prior approval commits an offence and shall, on conviction, be liable to a fine not exceeding RM 100,000 or to imprisonment for a term not exceeding 5 years or to both.",
        "text_en": "Employment Act Sec 60K: Prior approval from Director General of Labour is mandatory before hiring foreign employees; unauthorized employment carries fine up to RM 100,000 or 5 years imprisonment.",
        "text_zh": "【雇佣外籍劳工劳工局事前批准强制要件与高达10万令吉刑事罚则】：2023年全面生效的《劳工法令》第60K条确立了极其严苛的外劳准入规则：任何雇主在正式雇佣任何外籍员工（包括外籍技术工程师、管理人员及建筑劳工）之前，必须事先向马来西亚半岛劳工局（JTK）总监提出申请并获得其正式书面核准！未经批准擅自雇佣外籍员工的雇主构成刑事犯罪，一经定罪，单次违法最高可处以 100,000 令吉罚款、或最高 5 年监禁，或两者兼施！【出海攻防启示】：中资央企外籍中方派遣员工用工刑事红线！中资施工单位过去常持旅游签或商务签证（Social Visit Pass）安排国内工程师进驻大马工地现场指导作业，如今直接触犯 Sec 60K 刑事重罪！中资企业必须严格走完 JTK 事前审批并取得正式工作准证（PVP / Employment Pass）方可安排人员入境作业，防范现场被大马移民局与劳工局突击包围抓捕！",
        "norm_category": "labor_employment",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_my_foreign_employee_hiring", "text_zh": "要件一：在马来西亚注册实体拟雇佣非马来西亚公民身份之外国籍专业人士或普通工人", "status": "condition_precedent"},
            {"eid": "e_my_jtk_prior_written_approval", "text_zh": "要件二：在签订劳动合同及入境上岗前已正式获得马来西亚劳工局总监书面核准批文", "status": "mandatory"},
            {"eid": "e_my_lawful_foreign_employment", "text_zh": "法律后果：取得合法用工资质；未获核准上岗者构成刑事犯罪，最高处以 10 万令吉罚款与 5 年监禁", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "MY:Environmental_Quality_Act_1974:Sec34A",
        "law": "MY:Environmental_Quality_Act_1974",
        "enbez": "Sec 34A",
        "title": "马来西亚1974年环境质量法第34A条：重大基础设施EIA环境影响评价审批前置与开工许可",
        "heading_path": "马来西亚1974年环境质量法 (Act 127) > 环境保护规程 > 第34A条 指定工程环境影响评价(EIA)审查与开工前置",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Environmental Quality Act 1974 Sec 34A: Environmental Impact Assessment (EIA): Any person intending to carry out any prescribed activity (such as construction of dams, railways, ports, power plants, reclamation) shall submit a report to the Director General of Environmental Quality containing an assessment of the impact on environment. No person shall carry out any prescribed activity until the EIA report has been examined and approved.",
        "text_en": "EQA 1974 Sec 34A: Submission and approval of Environmental Impact Assessment (EIA) report by Director General is mandatory before commencing prescribed construction activities.",
        "text_zh": "【重大指定工程环境影响评价EIA报告事前核准法定强制前置】：任何拟实施法律指定活动（Prescribed Activities，包括水电站水坝、港口机场、铁路轨道交通、大型火电光伏电站、填海造陆及重化工厂建设）的投资人或开发商，必须向马来西亚环境局（DOE）总监提交详尽的《环境影响评价报告》（EIA Report）；在 EIA 报告获得环境局正式批准之前，任何企业依法不得开展任何实质性现场开工建设！违者责令立即停工并追究法人刑事责任！【出海攻防启示】：大马重大基础设施投资停工最高风险点！中资企业在承接大马 EPC 工程或联合投资特许经营项目前，必须在合同中明确将‘取得环境局无条件 EIA 批准证书’列为进场开工的先决条件；若业主未取得 EIA 批文即强令总包进场施工，中资企业应坚决拒绝开工，避免成为属地环境违法责任的代罪羊！",
        "norm_category": "construction_regulatory",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_my_eia_prescribed_project_category", "text_zh": "要件一：建设项目属于马来西亚环境规程列明必须进行环境评价之指定大型基础设施范畴", "status": "condition_precedent"},
            {"eid": "e_my_eia_formal_doe_approval", "text_zh": "要件二：取得马来西亚环境局（DOE）总监签发之《环境影响评价正式核准批文（EIA Approval）》", "status": "mandatory"},
            {"eid": "e_my_eia_lawful_site_possession", "text_zh": "法律后果：取得合法进场动土施工民事权利能力，未获批文动工者环境局依法享有强制封场扣押权", "status": "prohibition"}
        ], ensure_ascii=False)
    },

    # ========================================================
    # 6. 新加坡行业管理规程 (5条)
    # ========================================================
    {
        "table": "reference_norms",
        "norm_id": "SG:REDAS_Standard_Conditions:Cl16",
        "law": "SG:REDAS_Standard_Conditions",
        "enbez": "Clause 16",
        "title": "新加坡房地产开发商公会REDAS设计建造总承包条件第16条：工期调整与业主变更估价机制",
        "heading_path": "Real Estate Developers' Association of Singapore (REDAS) Design and Build Conditions (4th Edition) > Clause 16 Variations and Valuation",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "REDAS Design and Build Conditions Clause 16: Valuation of Variations: The Employer's Representative shall ascertain the value of any variation instruction. Valuation shall be based on Contract Rates where work is of similar character; failing which, fair valuation shall be made by taking into account market rates for design, labor and plant. The Contractor shall submit all cost substantiations within 28 days of completing the varied work.",
        "text_en": "REDAS D&B Cl 16: Regulates variation valuation based on contract rates or fair market rates, requiring substantiation within 28 days of completion.",
        "text_zh": "【REDAS设计建造总承包条件变更估价规则与28天费用举证要件】：业主代表（Employer's Representative）应当对签发的变更指令进行估价；若变更工作与原合同工程性质类似，必须严格按合同工程量清单单价（Contract Rates）计价；若不类似或无适用单价，则应参照设计、人工、机械台班的合理市场公允价格（Fair Valuation）进行公平成本核算；承包商必须在完成该变更工作后 28 天内提交详尽的造价支撑单据！【出海攻防启示】：中资设计施工一体化企业在新加坡变更索赔准绳！新加坡民营房建项目广泛采用 REDAS 合同；中资总包面对业主的复杂设计变更，必须把握 28 天费用申报窗口，详尽记录变更图纸引起的额外深化设计工时与高标号材料差价，通过公允市场估价法突破原固定总价，锁定高额变更增量利润！",
        "norm_category": "construction_regulatory",
        "mandatory_level": "directory",
        "elements_json": json.dumps([
            {"eid": "e_sg_redas_formal_variation_order", "text_zh": "要件一：发包人代表向总承包商出具了正式书面设计修改或增减工程量之工程变更指令（VO）", "status": "condition_precedent"},
            {"eid": "e_sg_redas_cost_substantiation_28d", "text_zh": "要件二：承包商在变更施工完成后严格 28 天内向业主代表呈报工料清单及支出凭证报告", "status": "mandatory"},
            {"eid": "e_sg_redas_enforceable_valuation", "text_zh": "法律后果：业主代表出具具有合同效力之变更核定单，该款项依法计入下一期 SOPA 付款证明中强制拨付", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "SG:SIA_Conditions_Contract_2016:Cl31",
        "law": "SG:SIA_Conditions_Contract_2016",
        "enbez": "Clause 31",
        "title": "新加坡建筑师学会SIA合同第31条：建筑师中期付款证书签发与法定终局付款证明争议",
        "heading_path": "Singapore Institute of Architects (SIA) Building Contract (2016) > Clause 31 Interim Payment Certificates > Architect's Certification Duties and Dispute Mechanisms",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "SIA Contract 2016 Clause 31: Interim Payment Certificates: The Architect shall, within 14 days of receipt of the Contractor's payment claim, issue an Interim Payment Certificate stating the amount due. The Employer shall pay the amount certified within the Period of Honouring Certificates (typically 14-21 days). In issuing certificates, the Architect acts independently as a professional certifier.",
        "text_en": "SIA 2016 Cl 31: Architect must issue Interim Payment Certificate within 14 days of payment claim as an independent certifier; Employer must pay certified sum within honoring period.",
        "text_zh": "【SIA合同建筑师独立签发中期付款证书与雇主刚性兑付周期】：建筑师在收到承包商提交的付款主张书后 14 天内，必须独立行使其专业核算职责，向发包人及承包商签发中期付款证书（Interim Certificate），客观载明到期应付金额；发包人必须在合同约定的‘证书兑现期’（通常为 14 至 21 天）内足额支付核定金额；建筑师在签发付款证书时依法处于准仲裁员独立专业地位，发包人不得向其施加商业干预！【出海攻防启示】：中资总包在新加坡高层建筑中回款的核心节点！在 SIA 合同下，发包人必须严格按照建筑师证书付款，无权单方擅自扣减其声称的‘违约罚金’；一旦发包人逾期未付款，中资企业可依此作为确凿金钱债务证据，立即向新加坡建设局 SMC 提起 SOPA 法定快速裁决，实现 30 天内极速全额追讨！",
        "norm_category": "construction_regulatory",
        "mandatory_level": "directory",
        "elements_json": json.dumps([
            {"eid": "e_sg_sia_contractor_payment_claim", "text_zh": "要件一：承包商在合同约定估价日向建筑师提交包含工程量明细之规范期中付款申请单", "status": "condition_precedent"},
            {"eid": "e_sg_sia_architect_independent_cert", "text_zh": "要件二：建筑师在法定 14 天内独立履行专业职责签署并核发《期中付款证书（IPC）》", "status": "mandatory"},
            {"eid": "e_sg_sia_strict_payment_duty", "text_zh": "法律后果：发包人承担在兑现期内无条件全额足额兑付义务，欠缺法律正当理由拒付构成严重违约", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "SG:Workplace_Safety_Act_Cap_354A:Sec12",
        "law": "SG:Workplace_Safety_Act_Cap_354A",
        "enbez": "Sec 12",
        "title": "新加坡工作场所安全与健康法第12条：总承包商施工安全核心首要信义职责与高管刑责",
        "heading_path": "新加坡工作场所安全与健康法 (Workplace Safety and Health Act, Cap. 354A) > 雇主与主要负责人首要信义职责 > 第12条",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Workplace Safety and Health Act (Cap. 354A) Sec 12: General duties of employers: It shall be the duty of every employer to take, so far as is reasonably practicable, such measures as are necessary to ensure the safety and health of his employees at work. Duty includes providing safe working environment, maintaining machinery, implementing risk assessments and safe work procedures. Violation causing death carries fine up to SGD 500,000 and 2 years imprisonment for directors.",
        "text_en": "WSHA Sec 12: Employers hold statutory duty to ensure safety/health at work; failure resulting in fatality exposes corporate entities to SGD 500,000 fine and directors to 2 years imprisonment.",
        "text_zh": "【工作场所安全首要信义职责与伤亡事故董事总经理刑事追责】：总承包商雇主负有在合理可行范围内采取一切必要安全预防措施的法定义务，确保工作场所所有工人的安全与健康；该职责包括：提供安全作业环境、实施动态风险评估（Risk Assessment）、制定安全施工方案（Safe Work Procedures）并配备专业安全员；若因总承包商未尽安全职责导致工人死亡事故，企业最高面临 500,000 新元罚金，公司项目董事、总经理个人依法面临最高 2 年监禁！【出海攻防启示】：新加坡出海总包安全管理‘天字第一号’底线！新加坡人力部（MOM）执法力度全球最严，一旦发生高空坠落或塔吊坍塌亡人事故，MOM 会立即签发全工地《停工令》（Stop Work Order / SWO），不仅导致数月工期瘫痪与巨额违约金，企业高管更将直接被提起刑事公诉！中资企业在新加坡必须实行全员安全一票否决制！",
        "norm_category": "labor_employment",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_sg_wsha_workplace_occupier", "text_zh": "要件一：总承包商作为新加坡建筑施工现场的实际控制人与法定法定用工单位", "status": "condition_precedent"},
            {"eid": "e_sg_wsha_fatal_accident_or_injury", "text_zh": "要件二：现场发生重大安全伤亡事故且查明总承包商存在风险评估疏漏或违规违章指挥", "status": "mandatory"},
            {"eid": "e_sg_wsha_criminal_sanctions", "text_zh": "法律后果：MOM 签发停工令停业整顿，对企业处以巨额罚款，并直接对中资项目经理提起刑事监禁指控", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "SG:MOM_Employment_of_Foreign_Manpower:Sec9",
        "law": "SG:MOM_Employment_of_Foreign_Manpower",
        "enbez": "Sec 9",
        "title": "新加坡人力部外籍劳动力雇佣法第9条：WP/SP外劳配额与劳务税征缴及虚构挂名重罚",
        "heading_path": "新加坡外籍劳动力雇佣法 (Employment of Foreign Manpower Act, Cap. 91A) > 外籍劳工雇佣条件与配额 > 第9条",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Employment of Foreign Manpower Act (Cap. 91A) Sec 9: Regulation of foreign employee quotas and foreign worker levy (FWL): Employers in the construction sector must adhere to the Dependency Ratio Ceiling (DRC) and man-year entitlements (MYE), and pay monthly foreign worker levies. Falsifying local phantom workers to inflate foreign quotas carries fine up to SGD 20,000 and imprisonment up to 2 years.",
        "text_en": "EFMA Sec 9: Enforces foreign worker Dependency Ratio Ceiling (DRC) and monthly levy payments; fictitious 'phantom worker' fraud carries SGD 20,000 fine and 2 years jail.",
        "text_zh": "【外籍劳动力配额比例上限与月度外劳税征缴及虚假幽灵员工刑事重罚】：新加坡人力部（MOM）对建筑业外劳实行极为严格的‘外籍劳动力配额比例上限’（Dependency Ratio Ceiling / DRC，建筑业通常为 1:5）及月度外劳人头税（Foreign Worker Levy / FWL）；严厉禁止建筑企业通过虚构新加坡本地公民缴纳公积金（CPF）制造‘幽灵员工（Phantom Workers）’以非法套取更多外劳配额！虚构挂名者一经查实，最高处以 20,000 新元罚金并处 2 年监禁，并终身永久剥夺外劳雇佣资格！【出海攻防启示】：中资企业外劳合规红线！新加坡本地劳动力严重匮乏，中资总包必须依靠孟加拉、印度等南亚劳工。企业必须严格按合法配额申请准证并足额缴纳每月高昂的外劳税，严禁通过当地黄牛中介搞‘挂名顶人头’；否则一旦被 MOM 调查审计，整个中资公司外劳准证将全盘注销，导致在建数亿新元项目瞬间彻底停工停摆！",
        "norm_category": "labor_employment",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_sg_efma_foreign_work_permit", "text_zh": "要件一：总承包商向新加坡人力部（MOM）申请引入外籍劳工工作准证（Work Permit / S Pass）", "status": "condition_precedent"},
            {"eid": "e_sg_efma_drc_quota_compliance", "text_zh": "要件二：实际聘用外籍劳工数量严格控制在企业真实合法雇佣的本地员工配额比例（DRC）之内", "status": "mandatory"},
            {"eid": "e_sg_efma_monthly_levy_payment", "text_zh": "法律后果：按月如期足额缴纳外劳人头税，违规虚报配额者面临刑事起诉与剥夺雇佣外劳权利", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "SG:Income_Tax_Act_Cap_134:Sec45",
        "law": "SG:Income_Tax_Act_Cap_134",
        "enbez": "Sec 45",
        "title": "新加坡所得税法第45条：向非居民支付特许权使用费与技术服务费预扣税规程",
        "heading_path": "新加坡所得税法 (Income Tax Act, Cap. 134) > 预扣税制度 > 第45条 向非居民付款之预扣税代扣代缴",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Income Tax Act (Cap. 134) Sec 45 & 45A: Withholding of tax in respect of interest, royalties and technical assistance fees paid to non-resident persons: The payer shall deduct tax at the applicable statutory rate (15% on gross, or prevailing corporate rate of 17%) and pay the amount deducted to the Comptroller of Income Tax by the 15th of the second month following payment date.",
        "text_en": "ITA Sec 45: Payer must withhold tax (15% gross or 17% net) on interest, royalties, and technical fees paid to non-residents, remitting to IRAS by the 15th of the second month.",
        "text_zh": "【向非居民支付特许使用费与技术劳务费预扣税代扣代缴与次月申报】：新加坡公司在向非居民境外法人（如位于中国境内的总包母公司或设计院）跨境支付利息、特许权使用费、工业设备租赁费或技术协助服务费时，必须依法履行预扣税义务：法定基准税率为 15%（总额计税）或适用当期企业所得税率 17%（净额计税）；代扣税款必须在款项支付次月 15 日前向新加坡国内税务局（IRAS）进行电子申报并完成划缴！【出海攻防启示】：中资央企新加坡海外平台公司资金跨境回流合规关键！新加坡子公司向国内母公司支付管理费、技术专利费或利息时，若未按 Sec 45 扣缴预扣税，将面临 5% 滞纳金重罚且该笔开支不得在新加坡税前抵扣！中资企业应充分运用《中新双重征税协定》（DTA），将特许权预扣税率成功从 15% 压降至 6%，合规回流资金！",
        "norm_category": "tax_compliance",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_sg_wht_crossborder_payment", "text_zh": "要件一：新加坡本土注册项目公司向中国境内母公司支付技术支持费、设计专利费或借款利息", "status": "condition_precedent"},
            {"eid": "e_sg_wht_timely_remittance_iras", "text_zh": "要件二：在付款发生次月 15 日前向国内税务局（IRAS）提交电子 Form S45 并划缴代扣税金", "status": "mandatory"},
            {"eid": "e_sg_wht_corporate_deduction_benefit", "text_zh": "法律后果：该项境外服务开支获准作为公司所得税前成本列支扣除，合规享受 DTA 协定抵减", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },

    # ========================================================
    # 7. 泰国公共采购与税收规程 (4条)
    # ========================================================
    {
        "table": "reference_norms",
        "norm_id": "TH:Public_Procurement_Act_2560:Sec102",
        "law": "TH:Public_Procurement_Act_2560",
        "enbez": "Sec 102",
        "title": "泰国2017年公共采购法第102条：政府项目履约保函没收与承包商违约弃标黑名单惩戒",
        "heading_path": "泰王国公共采购与物资管理法 (Public Procurement and Supplies Administration Act B.E. 2560) > 违约与制裁措施 > 第102条 保函没收与黑名单弃标认定",
        "language_mode": "bilingual",
        "lang_original": "th",
        "text_original": "พระราชบัญญัติการจัดซื้อจัดจ้างและการบริหารพัสดุภาครัฐ พ.ศ. 2560 มาตรา 102: ในกรณีที่คู่สัญญาไม่สามารถปฏิบัติตามสัญญาได้ หรือละทิ้งงาน ให้หน่วยงานของรัฐมีอำนาจบอกเลิกสัญญา และริบหลักประกันการปฏิบัติตามสัญญา ตลอดจนแจ้งรายชื่อให้เป็นผู้ทิ้งงาน (Blacklist) ต่อปลัดกระทรวงการคลังเพื่อประกาศให้เป็นผู้ทิ้งงานของทางราชการ",
        "text_en": "Procurement Act B.E. 2560 Sec 102: Authorizes state agencies to terminate contract, forfeit performance security, and register defaulting contractor on the official government Blacklist upon abandonment.",
        "text_zh": "【政府公共采购违约终止合同保函没收与财政部全国黑名单惩戒】：承包商未能按照合同履行、无正当理由擅自弃标（Abandonment of Works）或发生重大违约的，泰国政府机构依法享有法定单方解除合同并全额没收履约保证金（Performance Bond）的权力！同时，政府机构必须将违约承包商名单报送财政部常务秘书处，由财政部正式公报将其列为‘国家弃标失信黑名单’（Blacklisted Contractor），永久禁止其参与泰国任何国家公共财政资金项目的投标！【出海攻防启示】：中资央企在泰参与主权公建项目的极高信誉风险防线！中资总包在泰承建国家铁路局（SRT）、高速公路管理局（EXAT）项目时，绝不能因双方发生造价纠纷而擅自中途停工撤场！中途弃标将立即触发 Sec 102，不仅导致数亿泰铢保函被财政部无条件没收，更将全集团中资母公司打入泰国政府采购黑名单，彻底断送在泰国家级工程市场！",
        "norm_category": "construction_regulatory",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_th_procure_substantial_default", "text_zh": "要件一：承包商在泰国政府主权投资工程中发生严重违约延误或实质性撤出人员停工弃标", "status": "condition_precedent"},
            {"eid": "e_th_procure_state_agency_notice", "text_zh": "要件二：政府发包机关正式发出违约整改通知且承包商在法定催告期内未予恢复施工", "status": "mandatory"},
            {"eid": "e_th_procure_forfeiture_and_blacklisting", "text_zh": "法律后果：全额没收履约保函并由财政部将该外国承包商正式列入全国公共工程弃标永久黑名单", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "TH:Revenue_Code:Sec70_70bis",
        "law": "TH:Revenue_Code",
        "enbez": "Sec 70 & 70bis",
        "title": "泰国税法典第70/70条之二：向外国法人支付施工费与利润汇出15%预扣税规程",
        "heading_path": "泰王国税法典 (Thai Revenue Code) > 公司所得税编 > 第70条 向境外非居民付款预扣与第70条之二 利润汇出税",
        "language_mode": "bilingual",
        "lang_original": "th",
        "text_original": "ประมวลรัษฎากร มาตรา 70 และ 70 ทวิ: บริษัทหรือห้างหุ้นส่วนนิติบุคคลที่ตั้งขึ้นตามกฎหมายของต่างประเทศ และมิได้ประกอบกิจการในประเทศไทย แต่ได้รับเงินได้พึงประเมินจากหรือในประเทศไทย ผู้จ่ายเงินมีหน้าที่หักภาษี ณ ที่จ่าย ในอัตราร้อยละ 15 ของเงินได้. และมาตรา 70 ทวิ กำหนดให้เก็บภาษีร้อยละ 10 หรือ 15 จากการจำหน่ายเงินกำไรออกไปจากประเทศไทย",
        "text_en": "Revenue Code Sec 70 & 70bis: Mandates 15% withholding tax on assessable income paid to non-resident foreign companies, and 10% profit remittance tax on branch profits remitted overseas.",
        "text_zh": "【向非居民境外法人付款15%法定预扣税与分支机构利润汇出税】：依据泰国税法典第70条，未在泰国境内设立常设营业机构的外国法人，从泰国境内取得工程服务费、特许权使用费、技术咨询费或租金所得的，泰国付款方必须在支付款项时强制代扣 15% 的公司所得税；依据第 70 条之二，外国公司在泰国设立的分支机构将其在泰税后利润汇出境外的，还须额外缴纳 10% 的利润汇出税（Profit Remittance Tax）！【出海攻防启示】：中资企业赴泰投资出海架构设立核心税务考量！若中资总包以境外母公司名义直接签合同，泰国业主将依法硬扣 15% 现金流；中资企业应设立泰国注册的合资公司（Co., Ltd.），通过在泰合规汇算清缴适用 20% 企业所得税，结合中泰税收协定（DTA）将跨境股息分红预扣税降至 10%，显著降低全生命周期综合税负！",
        "norm_category": "tax_compliance",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_th_tax_nonresident_income", "text_zh": "要件一：泰国付款方依据承揽或服务协议向未在泰设立常设纳税主体的中国境外母公司跨境付款", "status": "condition_precedent"},
            {"eid": "e_th_tax_wht_15pct_deduction", "text_zh": "要件二：付款人依据税法典第 70 条在汇款时代扣 15% 预扣所得税款并向泰国税务局申报（P.N.D.54）", "status": "mandatory"},
            {"eid": "e_th_tax_dta_relief_applicability", "text_zh": "法律后果：出具正规完税凭单；若符合中泰双重征税协定无常设机构条件者可依法申请税收减免退税", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "TH:Factory_Act_BE_2535:Sec12",
        "law": "TH:Factory_Act_BE_2535",
        "enbez": "Sec 12",
        "title": "泰国工厂法第12条：工业厂房开工建设与生产运营前置环评与工业排污许可(Ror.Ngo.4)",
        "heading_path": "泰王国工厂法 (Factory Act B.E. 2535 as amended by Act No. 2 B.E. 2562) > 第三类工厂行政许可 > 第12条 Ror.Ngo.4工厂运营执照强制审批",
        "language_mode": "bilingual",
        "lang_original": "th",
        "text_original": "พระราชบัญญัติโรงงาน พ.ศ. 2535 มาตรา 12: ผู้ใดประสงค์จะตั้งโรงงานจำพวกที่ 3 (โรงงานที่มีแรงม้าเกิน 50 แรงม้า หรือมีคนงานเกิน 50 คน) ต้องได้รับใบอนุญาตจากผู้อนุญาต (รง.4) ก่อนจึงจะตั้งโรงงานได้ และต้องปฏิบัติตามเกณฑ์เกี่ยวกับสิ่งแวดล้อม ความปลอดภัย และการระบายน้ำทิ้ง ห้ามมิให้ประกอบกิจการโรงงานจนกว่าจะได้รับอนุญาต",
        "text_en": "Factory Act Sec 12: Mandatory to obtain Factory Operation License (Ror.Ngo.4) from Department of Industrial Works before constructing and operating Category 3 industrial factories.",
        "text_zh": "【第三类重工业厂房开工前置核准与工业部Ror.Ngo.4工厂执照】：泰国工厂法将使用机械动力超过 50 匹马力或用工超过 50 人的工业生产设施归为‘第三类工厂’（Category 3 Factory，涵盖钢铁、新能源电池、汽车总装、轮胎制造等出海中资核心行业）；该类工厂的投资者，在动工建厂前必须向工业部工业工程厅（DIW）正式递交申请并取得《第4类工厂执照》（รง.4 / Ror.Ngo.4）；未经批准擅自开工或投产的，依法责令立即停产停业，并对负责人处以监禁与高额罚款！【出海攻防启示】：中资制造业出海泰国罗勇工业园等拿地投建必须锁定的政府前置批文！中资企业在泰国购置工业用地后，切勿直接开挖地基或安装设备；必须先行委托具有工业部资质的环境与安全工程顾问公司，办妥 Ror.Ngo.4 工厂执照并经周边社区听证通过，方可开工施工，杜绝‘数亿厂房建成却因环评不合规无法投产’的灾难性后果！",
        "norm_category": "construction_regulatory",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_th_factory_category_3", "text_zh": "要件一：出海投资建设的工厂规模属于机械功率超过 50 马力或员工超过 50 人之第三类工业设施", "status": "condition_precedent"},
            {"eid": "e_th_factory_diw_license_rorngo4", "text_zh": "要件二：取得泰国工业工程厅（DIW）正式核发之《Ror.Ngo.4 工厂设立与运营许可证》", "status": "mandatory"},
            {"eid": "e_th_factory_lawful_commercial_operation", "text_zh": "法律后果：取得合法施工建设与商业通电投产资格，排他性阻断环保部门叫停扣押行政强制措施", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "TH:Consumer_Protection_Act_2522:Sec35_2",
        "law": "TH:Consumer_Protection_Act_2522",
        "enbez": "Sec 35/2",
        "title": "泰国消费者保护法第35条之二：格式合同不平等条款司法规制与免责条款绝对无效",
        "heading_path": "泰王国消费者保护法 (Consumer Protection Act B.E. 2522) > 合同控制编 (Contract Control) > 第35条之二 格式合同不公条款无效",
        "language_mode": "bilingual",
        "lang_original": "th",
        "text_original": "พระราชบัญญัติคุ้มครองผู้บริโภค พ.ศ. 2522 มาตรา 35 ทวิ: ข้อกำหนดในสัญญาที่ควบคุมที่ผู้ประกอบธุรกิจได้ทำกับผู้บริโภค หากมีลักษณะที่เป็นการจำกัดสิทธิหรือหน้าที่ตามปกติ หรือยกเว้นความรับผิดของผู้ประกอบธุรกิจ ให้ถือว่าข้อกำหนดนั้นเป็นโมฆะ หรือให้มีผลบังคับเพียงเท่าที่เป็นธรรมและสมควรแก่กรณี",
        "text_en": "Consumer Protection Act Sec 35/2: Clauses in controlled standardized contracts that unfairly exempt business operators from liability or limit consumer remedies are legally void.",
        "text_zh": "【格式合同不公条款司法介入与经营者免责条款绝对无效】：由企业经营者预先拟定用于与消费者订立的标准格式合同（Controlled Standardized Contracts），若存在排除或限制经营者法定故意重大过错责任、单方免除工程瑕疵修补义务、或赋予经营者单方随意变更工期总价的不平等霸王条款，该特定条款在法律上自始绝对无效（Void），或者法院依法仅在公平成倍限度内予以适用！【出海攻防启示】：中资房企与建筑商在泰开发销售公寓别墅的合规盾牌！中资房地产承包商在向泰国本地买家或小业主交付房屋时，若在购房协议或装修合同中约定‘开发商不对地基沉降承担保修责任’等免责格式条款，将被泰国消费者保护委员会（CPB）及中央民事法院依据 Sec 35/2 直接判决自始无效并处以惩罚性赔偿，必须严格遵循法定保修标准！",
        "norm_category": "corporate_governance",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_th_consumer_standardized_contract", "text_zh": "要件一：合同系由企业经营者单方提供且消费者处于谈判实质弱势地位之标准化格式协议", "status": "condition_precedent"},
            {"eid": "e_th_consumer_unconscionable_exemption", "text_zh": "要件二：条款内容实质性免除开发商施工方核心法定保修质量责任或过度限制消费者合法救济", "status": "mandatory"},
            {"eid": "e_th_consumer_clause_voidness", "text_zh": "法律后果：该霸王免责条款自始绝对无效，法院依法直接判决经营者承担全额修复与赔偿责任", "status": "prohibition"}
        ], ensure_ascii=False)
    },

    # ========================================================
    # 8. 菲律宾仲裁税收劳务规程 (5条)
    # ========================================================
    {
        "table": "reference_norms",
        "norm_id": "PH:CIAC_Arbitration_Rules_2019:Rule4",
        "law": "PH:CIAC_Arbitration_Rules_2019",
        "enbez": "Rule 4",
        "title": "菲律宾CIAC建筑仲裁程序规则第4条：简易程序与仲裁协议默示推定管辖规则",
        "heading_path": "Construction Industry Arbitration Commission (CIAC) Revised Rules of Procedure Governing Construction Arbitration (2019) > Rule 4 Jurisdiction and Arbitral Agreement",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "CIAC Rules of Procedure (2019) Rule 4: Jurisdiction: The CIAC shall have original and exclusive jurisdiction over construction disputes. An agreement to submit a dispute to CIAC arbitration may be express, or implied when a construction contract provides for arbitration or incorporates by reference an arbitration clause, or when parties voluntarily submit without timely jurisdictional objection.",
        "text_en": "CIAC Rules Rule 4: CIAC exercises original and exclusive jurisdiction over Philippine construction disputes; jurisdiction acquired via express agreement, incorporation by reference, or waiver of objection.",
        "text_zh": "【CIAC建筑仲裁专属管辖与默示推定合意程序规则】：CIAC 对发生在菲律宾境内的所有建设承揽争议享有排他性专属管辖权；提交 CIAC 仲裁的协议可以是明示的，亦可通过合同引用外部文件（Incorporation by Reference）中包含仲裁条款的方式成立；若一方提起 CIAC 仲裁而另一方应诉未在答辩期内提出管辖权异议的，推定为自愿接受 CIAC 管辖！仲裁庭必须在签署审理范围书（Terms of Reference / TOR）后严格 6 个月内结案作出终局裁决！【出海攻防启示】：中资承包商在菲快速追索工程欠款第一通道！菲律宾普通地方法院（RTC）审理一审诉讼往往拖延 5 至 8 年；中资企业只要在合同中约定了争议提交仲裁，即可直接向 CIAC 提告，利用其严格的 6 个月结案倒计时机制，迅速对业主的不动产及在岸银行账户申请仲裁前财产保全，以雷霆司法手段迫使业主结清数千万美元拖欠款！",
        "norm_category": "crossborder_litigation",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_ph_ciac_rule4_construction_dispute", "text_zh": "要件一：争议标的属于在菲律宾境内施工建造、工程设计、设备供货或专业承揽范畴", "status": "condition_precedent"},
            {"eid": "e_ph_ciac_rule4_arbitration_clause_or_reference", "text_zh": "要件二：合同约定了自愿仲裁意向条款或通过援引 FIDIC/CIAP 通用条件引入了仲裁条款", "status": "mandatory"},
            {"eid": "e_ph_ciac_rule4_statutory_6m_award", "text_zh": "法律后果：CIAC 依法享有排他性初审管辖权，仲裁庭必须在法定 6 个月内结案签发具有强制执行力裁决", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "PH:BIR_Revenue_Regulation_11_2018:Sec2_57",
        "law": "PH:BIR_Revenue_Regulation_11_2018",
        "enbez": "Sec 2-57",
        "title": "菲律宾税务局RR 11-2018号规程：政府与私人建设工程2%所得税预扣与增值税代扣",
        "heading_path": "菲律宾国内税务局税收规程 (BIR Revenue Regulations No. 11-2018 Implementing TRAIN Law) > 预扣所得税制度 > 第2-57条 建设工程承包商2%扩大预扣税",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "BIR RR 11-2018 Sec 2-57-2: Expanded Withholding Tax on Payments to Contractors: Gross payments made by government or private employers to domestic or resident general engineering, building, or specialty contractors are subject to a mandatory creditable withholding tax of two percent (2%). In addition, payments by government agencies are subject to a final withholding VAT of 5%. Payer must issue BIR Form 2307 to contractor.",
        "text_en": "BIR RR 11-2018: Mandates 2% creditable expanded withholding tax on gross payments to construction contractors, plus 5% withholding VAT for government projects; BIR Form 2307 required.",
        "text_zh": "【建设工程进度款2%法定扩大预扣税与政府项目5%增值税代扣规程】：发包人（无论是政府机构或私人业主）在向各类总承包商或专业分包商支付工程款时，必须强制代扣 2% 的可抵免扩大预扣税（Creditable Withholding Tax / CWT）；对于菲律宾政府投资的公共工程，政府机构还须额外代扣 5% 的最终增值税（Final Withholding VAT）；付款人必须在付款时向承包商出具税务局正式盖章核发的 BIR Form 2307 预扣完税凭单！【出海攻防启示】：中资企业在菲项目现金流税务核销铁律！很多中资项目财务团队发现业主结算单上总被扣去 2% 资金，误以为是业主的合同扣款；这 2% 实属预缴所得税！中资企业必须在每笔付款到账后立即向发包人催要 BIR Form 2307 凭单原件，并在季度和年度企业所得税汇算清缴时据此全额抵减应纳所得税，严防因单据遗失造成 2% 的纯现金流资产永久沉没损失！",
        "norm_category": "tax_compliance",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_ph_bir_construction_payment", "text_zh": "要件一：发包人向菲律宾在岸注册建设工程总承包商拨付工程期中或竣工工程进度款项", "status": "condition_precedent"},
            {"eid": "e_ph_bir_cwt_2pct_mandatory_deduction", "text_zh": "要件二：发包人在汇出款项时依法扣除 2% 扩大预扣税款并按期申报缴纳给国税局（BIR）", "status": "mandatory"},
            {"eid": "e_ph_bir_form_2307_issuance", "text_zh": "法律后果：发包人必须向承包商交付正规 BIR Form 2307，承包商依法享有全额抵扣年度所得税权利", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "PH:PD_1586_EIS_System:Sec4",
        "law": "PH:PD_1586_EIS_System",
        "enbez": "Sec 4",
        "title": "菲律宾第1586号总统令：国家环境影响陈述系统与环境合规证书(ECC)开工前置审批",
        "heading_path": "菲律宾第1586号总统令 (Presidential Decree No. 1586) > 环境影响陈述(EIS)系统 > 第4条 环境合规证书(ECC)法定前置",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Presidential Decree No. 1586 Sec 4: Environmental Compliance Certificate (ECC): No person, partnership or corporation shall undertake or operate any environmentally critical project (ECP) or project within an environmentally critical area (ECA) without first securing an Environmental Compliance Certificate (ECC) issued by the President or the Department of Environment and Natural Resources (DENR). Operating without ECC carries immediate project suspension and fines.",
        "text_en": "PD 1586 Sec 4: Mandates securing an Environmental Compliance Certificate (ECC) from DENR before undertaking environmentally critical projects (ECP) or in critical areas (ECA).",
        "text_zh": "【重大环境敏感项目环境合规证书ECC法定事前强制审批与停工关停处罚】：任何企业在菲律宾境内实施环境关键性项目（Environmentally Critical Projects / ECP，如重工业冶炼、大型电站、港口大桥、高层公建）或在环境脆弱敏感区（ECA）开展施工，在正式动工前必须向菲律宾环境与自然资源部（DENR）下属环境管理局（EMB）申请并取得《环境合规证书》（Environmental Compliance Certificate / ECC）！未经取得 ECC 证书擅自开工施工的，DENR 依法有权立即签发全场停工令（Cease and Desist Order / CDO）并处以巨额连续罚金！【出海攻防启示】：中资企业出海在菲项目动土的第一道主权合规红线！中资总包在与菲方业主签约时，必须在合同条件中明确写明：由发包人自行承担办理取得 DENR 官方 ECC 证书的全部法定义务与费用，并将‘ECC 证书有效交付总包’作为开工令生效的前置先决条件（CP）；严禁在中资团队未核验真实 ECC 批文前盲目动土进场，规避被属地环保警察查封施工现场的惨重法律损失！",
        "norm_category": "construction_regulatory",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_ph_ecc_ecp_project_nexus", "text_zh": "要件一：工程项目属于菲律宾法定环境关键性项目（ECP）或坐落于国家环境敏感脆弱区域（ECA）", "status": "condition_precedent"},
            {"eid": "e_ph_ecc_formal_denr_issuance", "text_zh": "要件二：取得环境与自然资源部（DENR）部长或环境管理局正式签署核发之《环境合规证书（ECC）》", "status": "mandatory"},
            {"eid": "e_ph_ecc_valid_commencement_effect", "text_zh": "法律后果：取得合法开工破土动工民事行政权利，排他性排除环保局（EMB）签发停工令查封现场", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "PH:DOLE_DO_174_17:Sec5",
        "law": "PH:DOLE_DO_174_17",
        "enbez": "Sec 5",
        "title": "菲律宾劳工部第174-17号令：合法劳务外包与违法纯劳务中介(Labor-Only Contracting)严格界定要件",
        "heading_path": "菲律宾劳工与就业部第174-17号令 (DOLE Department Order No. 174, Series of 2017) > 合法承包与禁止违法派遣 > 第5条 纯劳务派遣认定标准",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "DOLE Department Order No. 174-17 Sec 5: Absolute Prohibition of Labor-Only Contracting: Labor-only contracting is prohibited where: (a) The contractor does not have substantial capital (paid-up capital of at least PHP 5,000,000) or does not have investments in the form of tools, equipment, machineries; and (b) The contractor's workers perform activities directly related to the principal business of the employer; or (c) The contractor does not exercise control over the performance of the work. Engaging in labor-only contracting deems the principal the direct employer.",
        "text_en": "DOLE DO 174-17 Sec 5: Strictly prohibits Labor-Only Contracting; contractors must hold >= PHP 5M paid-up capital, maintain equipment, and retain operational control over workers.",
        "text_zh": "【严禁违法劳务派遣Labor-Only三大法定要件与实缴资本500万比索门槛】：菲律宾劳工部（DOLE）第174号令绝对禁止‘纯劳务派遣（Labor-Only Contracting）’，符合下列任一情形即推定为违法派遣：（1）劳务分包商不具备实质性资本（实缴资本必须达到至少 5,000,000 比索，约合 60 万人民币）或欠缺施工工具设备；（2）派遣工人从事发包人核心主营业务；（3）劳务分包商未对施工工人的现场作业实施独立实际管理控制（Control Test）！构成违法劳务派遣的，发包人（中资总包）依法直接被强制定性为所有派遣工人的直聘雇主，须与分包商承担全部工伤、社保及工龄津贴的连带清偿责任！【出海攻防启示】：中资承包商在菲现场用工风控合规生命线！中资施工现场严禁找不合规的包工头‘招点工’；在引进任何菲律宾本土劳务分包商前，必须查验其持有劳工部依法核发的 DO-174 登记证书，并在分包合同中严格锁定：分包商必须在现场设立专属工长自主指挥、自主发放工资、自主配备劳保用品，彻底在法律上与总包切割用工管理控制，防范被菲劳工部穿透认定为‘实质雇主’面临罢工赔偿！",
        "norm_category": "labor_employment",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_ph_dole_substantial_capital_5m", "text_zh": "要件一：劳务分包商在证券交易委员会（SEC）登记的实缴资本金达到至少 5,000,000 比索法定门槛", "status": "condition_precedent"},
            {"eid": "e_ph_dole_independent_supervision_control", "text_zh": "要件二：分包商持有有效 DOLE 执照并对现场施工人员的作息、指令和安全实施独立现场控制", "status": "mandatory"},
            {"eid": "e_ph_dole_avoidance_direct_employer_risk", "text_zh": "法律后果：确认为合法独立工程劳务分包，有效阻断总承包商被直接穿透判定为法定雇主之连带清偿风险", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "PH:Anti_Dummy_Law_CA_108:Sec1_2",
        "law": "PH:Anti_Dummy_Law_CA_108",
        "enbez": "Sec 1-2",
        "title": "菲律宾反挂名法第1-2条：规避宪法外资比例假借菲籍公民代持之刑事惩戒与股权没收",
        "heading_path": "菲律宾联邦法案第108号 (Commonwealth Act No. 108 as amended, Anti-Dummy Law) > 惩治规避国有化与外资限制法案 > 第1-2条 代持挂名刑事责任与资产充公",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Anti-Dummy Law (CA No. 108) Sec 1-2: Penalizing evasion of laws on nationalization: Any citizen of the Philippines who allows his name or citizenship to be used for the purpose of evading any constitutional or legal provision requiring Philippine citizenship for the exercise of any right, franchise or privilege, and any alien or foreigner profiting thereby, shall be punished by imprisonment for not less than 5 nor more than 15 years and a fine. The property, franchise, or shares so acquired shall be forfeited to the State.",
        "text_en": "Anti-Dummy Law Sec 1-2: Criminalizes using Filipino nominees (dummies) to evade foreign ownership caps; imposes 5 to 15 years imprisonment and mandatory civil forfeiture of assets.",
        "text_zh": "【反挂名法刑事重罚与规避外资比例代持股权财产全部充公没收】：任何菲律宾公民允许其姓名或菲籍身份被外国人利用以规避宪法或法律对外资比例的限制（如在受限领域假借菲籍代持人组建 60/40 公司），以及任何实际控制并从中牟利的外国主体，均构成严重刑事犯罪！违法者处以 5 年以上、15 年以下有期徒刑，并处巨额罚金；更为致命的是：通过挂名代持手段非法取得的全部土地、股权、特许权及公司资产，一律依法强制充公没收（Forfeiture to the State）收归菲律宾国有！【出海攻防启示】：中资赴菲出海最高刑事与资产清零雷区！中资企业在菲购买受宪法保护的土地、或投资矿业等 40% 外资上限行业时，个别不法中介常怂恿中资通过菲籍挂名‘代持人’（Dummy）签署阴阳协议控制 60% 股权；该架构一经菲司法部（DOJ）或竞争对手举报查实，不仅代持协议绝对无效、实际出资的中资企业血本无归被国家充公没收，中方负责人更将面临最高 15 年的跨国引渡与牢狱之灾！必须坚决采用合法合规的合资架构或借道 RA 11659 开放领域！",
        "norm_category": "corporate_governance",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_ph_dummy_nationalized_sector", "text_zh": "要件一：投资标的属于菲律宾宪法或特别法严格限制外资比例（如土地持有或受限公用事业）范畴", "status": "condition_precedent"},
            {"eid": "e_ph_dummy_evasion_arrangement", "text_zh": "要件二：查明外国投资者通过菲籍代理人代持、隐秘借贷或表决权协议等阴阳手段规避外资限制", "status": "mandatory"},
            {"eid": "e_ph_dummy_forfeiture_and_imprisonment", "text_zh": "法律后果：所涉股权土地资产依法予以强制没收归国，对实际操纵外籍自然人判处最高 15 年监禁", "status": "prohibition"}
        ], ensure_ascii=False)
    }
]

PHASE10_L2_REFERENCE_NORMS = PHASE10_L2_REFERENCE_NORMS + PHASE10_L2_REFERENCE_NORMS_PART2
