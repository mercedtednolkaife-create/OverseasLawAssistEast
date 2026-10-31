# -*- coding: utf-8 -*-
"""Phase 9 阶梯式长尾法条扩充 - Batch 2 (实务域 04、05、06)
实务域 04: FIDIC 国际工程标准合同全款项对比矩阵 (Red / Yellow / Silver 1999 & 2017)
实务域 05: 外资准入、并购公司法、合资治理(JV/SPV)与公私合营(PPP)
实务域 06: 土地物权、征地清障、原住民领地、用林用海与长期租赁
严格遵循《数据库审查.md》第五部分字段规范与 elements_json 结构化标准。
"""

import json

BATCH2_STATUTES = [
    # =========================================================================
    # 实务域 04: FIDIC 国际工程标准合同全款项对比矩阵 (L2)
    # =========================================================================
    {
        "table": "reference_norms",
        "norm_id": "FIDIC:Silver_1999:Clause_4.12",
        "law": "FIDIC:Silver_1999",
        "enbez": "Clause 4.12",
        "title": "FIDIC银皮书第4.12款：不可预见的物质条件承包商自负地质风险",
        "heading_path": "FIDIC银皮书 (EPC交钥匙总价合同 1999版) > 第4条 承包商 > 现场地质条件",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Except as otherwise stated in the Contract: (a) the Contractor shall be deemed to have obtained all necessary information as to risks, contingencies and other circumstances which may influence or affect the Works; (b) by signing the Contract, the Contractor accepts total responsibility for having foreseen all difficulties; and (c) the Contract Price shall not be adjusted to take account of any unforeseen difficulties or costs.",
        "text_en": "Under Silver Book Clause 4.12, Contractor accepts total responsibility for having foreseen all difficulties and costs. The Contract Price shall not be adjusted for unforeseen physical conditions.",
        "text_zh": "【银皮书地质全包干与不可调价原则】：除合同另有规定外，承包商被视为已取得关于可能影响工程的风险、意外及其他情况的全部必要信息；签署合同即视为承包商承担已预见全部困难和费用的完全责任；合同价格不得因任何不可预见的物理困难或费用而进行调整。【对比红/黄皮书】：红皮书与黄皮书第4.12款赋予承包商在遭遇‘经验丰富承包商无法合理预见的地下物理条件’时全额索赔工期顺延（EOT）与费用（Cost）的权利；但银皮书第4.12款彻底颠覆此规则，将全部地下未知地质、岩层硬度、溶洞溶沟风险完全分配由EPC总承包商自负包干！",
        "norm_category": "fidic_standard",
        "fidic_tier": "L2_reference",
        "fidic_edition": "1999_Silver",
        "mandatory_level": "contract_default",
        "elements_json": json.dumps([
            {"eid": "e_fidic_4_12_silver_risk_allocation", "text_zh": "规则要点：银皮书默认排除了红黄皮书不可预见物质条件索赔工期与费用的法定机制", "status": "condition_precedent"},
            {"eid": "e_fidic_4_12_deemed_knowledge", "text_zh": "法律拟制：推定EPC承包商在投标签约前已核查现场并知晓全部地下地质阻碍", "status": "mandatory"},
            {"eid": "e_fidic_4_12_lump_sum_strict", "text_zh": "索赔阻断：承包商不得因地下岩溶、流沙或地质异常主张增加合同价款或顺延工期", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "FIDIC:Red_1999:Clause_4.12",
        "law": "FIDIC:Red_1999",
        "enbez": "Clause 4.12",
        "title": "FIDIC红皮书第4.12款：不可预见的物质条件全额索赔工期与费用",
        "heading_path": "FIDIC红皮书 (施工单价合同 1999版) > 第4条 承包商 > 现场地质条件",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "If the Contractor encounters adverse physical conditions which he considers to have been Unforeseeable, the Contractor shall give notice to the Engineer. If and to the extent that the Contractor suffers delay and/or incurs Cost due to these conditions, the Contractor shall be entitled subject to Sub-Clause 20.1 to: (a) an extension of time, and (b) payment of any such Cost.",
        "text_en": "Under Red Book Clause 4.12, if Contractor encounters Unforeseeable physical conditions, Contractor shall be entitled to EOT and payment of Cost.",
        "text_zh": "【红皮书不可预见物质条件索赔权】：承包商若在施工现场遭遇其认为无法合理预见的异常物理条件（含地下水文、岩溶障碍、地质断层等），应及时向工程师发出通知；承包商因此遭受工期延误或发生额外费用的，有权依据第20.1款主张：(a) 顺延竣工工期（EOT）；及 (b) 将该等额外发生的成本（Cost）全额计入合同价格予以补偿。【实务攻防】：必须在遭遇该地质条件之日起 28 天内递交索赔意向通知，并配合钻孔地勘对比报告证明该情况超出基准日（Base Date）招标地勘资料预期。",
        "norm_category": "fidic_standard",
        "fidic_tier": "L2_reference",
        "fidic_edition": "1999_Red",
        "mandatory_level": "contract_default",
        "elements_json": json.dumps([
            {"eid": "e_fidic_4_12_red_unforeseeable", "text_zh": "要件一：现场物理条件超出有经验承包商在基准日前合理预见范围", "status": "condition_precedent"},
            {"eid": "e_fidic_4_12_red_notice_served", "text_zh": "要件二：承包商在遭遇该地质条件后已向监理工程师送达正式书面通知", "status": "mandatory"},
            {"eid": "e_fidic_4_12_red_eot_and_cost", "text_zh": "法律后果：承包商依法享有工期顺延（EOT）与实际支出成本补偿的双重救济", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "FIDIC:2017_Suite:Clause_20.2",
        "law": "FIDIC:2017_Suite",
        "enbez": "Clause 20.2",
        "title": "FIDIC 2017版第20.2款：双向对等28天索赔除斥期间与14天初步异议",
        "heading_path": "FIDIC 2017年新红/黄/银皮书通用条件 > 第20条 雇主与承包商索赔 > 索赔程序",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "The claiming Party shall give a Notice of Claim to the Engineer, describing the event or circumstance giving rise to the cost, additional payment or EOT, not later than 28 days after the claiming Party became aware, or should have become aware, of the event or circumstance. If the claiming Party fails to give a Notice of Claim within this period of 28 days, the Notice shall not be valid and the claiming Party shall have NO entitlement to any additional payment or EOT.",
        "text_en": "FIDIC 2017 Clause 20.2 imposes fully bilateral 28-day time-bar on BOTH Employer and Contractor claims, with a 14-day notice of dissatisfaction review mechanism.",
        "text_zh": "【2017版双向对等28天索赔失权机制】：打破1999版仅对承包商设28天时效的不平等架构，2017版确立雇主与承包商完全对等的双向索赔规则！任何一方（雇主或承包商）主张索赔，必须在知悉或应当知悉事件后 28 天内发出索赔通知；逾期发出通知的，索赔通知无效且主张方彻底丧失任何工期顺延或追加付款权利；工程师若认为通知逾期，必须在 14 天内发出异议，否则视为初步有效。【实务攻防】：中资承包商可用本条有力制衡业主的反向违约金索赔——若业主未在知悉工程延误后28天内向工程师发函索赔误期违约金，业主同样永久丧失扣留违约金的实体权利！",
        "norm_category": "fidic_standard",
        "fidic_tier": "L2_reference",
        "fidic_edition": "2017_Reprint",
        "mandatory_level": "contract_default",
        "elements_json": json.dumps([
            {"eid": "e_fidic2017_20_2_bilateral_time_bar", "text_zh": "要件一：索赔方（无论雇主或承包商）必须在知悉事件之日起28天内发出书面索赔通知", "status": "condition_precedent"},
            {"eid": "e_fidic2017_20_2_engineer_14day_review", "text_zh": "要件二：工程师若主张通知超期，必须在14天内发出书面初步异议，否则该通知视为有效", "status": "mandatory"},
            {"eid": "e_fidic2017_20_2_forfeiture_equality", "text_zh": "法律后果：双向严格失权，业主逾期未报违约金索赔的，其主张违约金权利同样消灭", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "FIDIC:Golden_Principles:GP1_GP5",
        "law": "FIDIC:Golden_Principles",
        "enbez": "GP1~GP5",
        "title": "FIDIC 2019 五大黄金原则：禁止滥用专用条件颠覆风险平衡",
        "heading_path": "国际咨询工程师联合会 (FIDIC) 官方指南 > FIDIC黄金原则 (Golden Principles 2019)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "The FIDIC Golden Principles (2019): GP1 - The duties, rights, obligations, roles and responsibilities of all the Contract Participants shall be generally as implied in the General Conditions; GP2 - Particular Conditions must be drafted clearly and unambiguously; GP3 - Particular Conditions must not change the balance of risk/reward allocation provided in the General Conditions; GP4 - Time periods specified for notices and determinations must be reasonable; GP5 - Unless there is a conflict with governing law, all formal disputes must be referred to a DAAB for a provisionally binding decision as a condition precedent to arbitration.",
        "text_en": "FIDIC Golden Principles (GP1-GP5) require that Particular Conditions must not alter the fair balance of risk allocation provided in the General Conditions.",
        "text_zh": "【FIDIC 2019 五大黄金原则（防范业主苛刻霸王条款武器）】：① GP1：合同各方权利义务与角色定位必须符合通用条件基本精神；② GP2：专用条件修改必须清晰明确无歧义；③ GP3（最核心）：专用条件严禁改变通用条件设定的风险与回报公允分配平衡（不得将业主风险无限转嫁给承包商）；④ GP4：索赔通知与确定的期限必须合理；⑤ GP5：除强行法冲突外，仲裁前必须设置 DAAB/DAB 争议裁决委员会前置程序。【实务攻防】：在国际多边金融机构（如世行、亚投行、亚行）资助的东盟基建项目中，业主若通过专用条件大肆删削不可抗力补偿、无限扩大无上限赔偿责任，承包商可援引 GP 原则向出资行合规局申诉纠正！",
        "norm_category": "fidic_standard",
        "fidic_tier": "L2_reference",
        "fidic_edition": "2019_Guidelines",
        "mandatory_level": "contract_default",
        "elements_json": json.dumps([
            {"eid": "e_fidic_gp_risk_balance", "text_zh": "准则一：专用条件对通用条件的修改不得实质性破坏合同风险对等分配基础", "status": "condition_precedent"},
            {"eid": "e_fidic_gp_daab_mandate", "text_zh": "准则二：争议解决阶梯中保留常设或特设争端裁决委员会（DAAB）的前置机制", "status": "mandatory"},
            {"eid": "e_fidic_gp_multilateral_defense", "text_zh": "攻防效力：作为对抗业主严重失衡霸王条款、向多边开发银行申诉的权威行业准则", "status": "prohibition"}
        ], ensure_ascii=False)
    },

    # =========================================================================
    # 实务域 05: 外资准入、并购公司法与公私合营(PPP) (L1+L2)
    # =========================================================================
    {
        "table": "norms",
        "norm_id": "ID:UU_25_2007:Art33",
        "law": "ID:UU_25_2007",
        "enbez": "Art 33",
        "title": "印尼投资法第33条：股权代持协议（Nominee）自始绝对无效重锤",
        "heading_path": "印尼2007年第25号投资法 > 第九章 投资者的权利与义务 > 股权归属",
        "language_mode": "trilingual",
        "lang_original": "id",
        "text_original": "Penanam modal dalam negeri dan penanam modal asing yang melakukan penanaman modal dalam bentuk perseroan terbatas dilarang membuat perjanjian dan/atau pernyataan yang menegaskan bahwa kepemilikan saham dalam perseroan terbatas untuk dan atas nama orang lain. Dalam hal penanam modal dalam negeri dan penanam modal asing membuat perjanjian tersebut, perjanjian tersebut dinyatakan BATAL DEMI HUKUM.",
        "text_en": "Domestic and foreign investors are PROHIBITED from making agreements stating that share ownership in a limited liability company is for and on behalf of another party. Any such nominee agreement is VOID BY LAW.",
        "text_zh": "【严禁股权代持（Nominee Agreement）自始绝对无效】：国内外投资者在印尼设立有限责任公司，严禁订立任何确认公司股份系‘代他人持有或以他人名义持有’的代持协议或声明书；若违反本款订立代持协议，该协议自始依法绝对无效（Batal Demi Hukum）！【出海实务攻防】：印尼对外商投资设立的严禁红线！部分中企为规避外资准入限制（如施工配电受限领域），委托印尼当地员工或律师代持 PT 公司股权并签署阴阳借款协议与表决权委托；一旦代持人反水或去世，印尼法院依据第33条直接判令代持协议绝对无效，中方出资全部被认定为非法无效投入，血本无归且面临没收！",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory_override",
        "elements_json": json.dumps([
            {"eid": "e_id33_nominee_contract", "text_zh": "要件一：当事人订立约定由印尼名义股东代外资实际出资人持有股权的协议", "status": "condition_precedent"},
            {"eid": "e_id33_prohibited_statute", "text_zh": "要件二：该代持安排违反印尼《投资法》第33条公法绝对禁止性规定", "status": "mandatory"},
            {"eid": "e_id33_void_by_law", "text_zh": "法律后果：协议自始绝对无效，实际出资人无权诉请确认股东资格或返还股权", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "VN:Law_61_2020:Art24_26",
        "law": "VN:Law_61_2020",
        "enbez": "Art 24~26",
        "title": "越南2020投资法第24-26条：外资并购股权M&A审批法定前置要件",
        "heading_path": "越南2020投资法 (Law 61/2020/QH14) > 第二章 外商投资形式 > 股权收购审批",
        "language_mode": "trilingual",
        "lang_original": "vi",
        "text_original": "Nhà đầu tư nước ngoài mua cổ phần, phần vốn góp của tổ chức kinh tế phải thực hiện thủ tục đăng ký góp vốn, mua cổ phần nếu thuộc một trong các trường hợp: (a) Làm tăng tỷ lệ sở hữu của nhà đầu tư nước ngoài tại tổ chức kinh tế kinh doanh ngành, nghề tiếp cận thị trường có điều kiện; (b) Làm tăng tỷ lệ sở hữu của nhà đầu tư nước ngoài lên trên 50% vốn điều lệ; (c) Tổ chức kinh tế có Giấy chứng nhận quyền sử dụng đất tại đảo, xã biên giới, ven biển.",
        "text_en": "Foreign investors acquiring shares/capital in Vietnamese entities must obtain prior M&A Approval if acquiring >50% ownership or involving sensitive border/coastal land.",
        "text_zh": "【外资收购越南公司股权（M&A Approval）前置审批】：外国投资者收购越南经济组织的股权或出资额，凡属于下列三种情形之一的，必须在办理工商变更前向计划投资厅（DPI）办理出资与股权收购前置注册审批（M&A Approval）：① 涉及外资准入附条件限制行业的；② 导致外国投资者在标的公司持股比例超过 50% 的；③ 标的公司在海岛、边境乡镇、沿海敏感区域持有土地使用权证书的！【出海实务攻防】：中企收购越南新能源电站SPV项目公司，若未事先取得计划投资厅 M&A 批文即私自签署交割协议并划扣股权款，该交易工商不予登记，且资金无法通过 DICA 资本金专户合法购汇汇回！",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory_override",
        "elements_json": json.dumps([
            {"eid": "e_vn24_ma_condition", "text_zh": "要件一：外资收购导致持股超50%或标的公司涉及负面清单行业或边境沿海土地", "status": "condition_precedent"},
            {"eid": "e_vn24_prior_dpi_approval", "text_zh": "要件二：向省级计划投资厅（DPI）提交正式并购投资审查申请并取得书面批复", "status": "mandatory"},
            {"eid": "e_vn24_capital_legality", "text_zh": "法律后果：取得批文方可办理公司法实缴变更及合法开立DICA资本金专户汇出收益", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "VN:PPP_Law_2020:Art82",
        "law": "VN:PPP_Law_2020",
        "enbez": "Art 82",
        "title": "越南2020公私合营法第82条：PPP合同最低收入兜底风险共担机制",
        "heading_path": "越南2020年公私合营投资法 (PPP Law 64/2020/QH14) > 第八章 国家对PPP项目的支持与风险分担",
        "language_mode": "trilingual",
        "lang_original": "vi",
        "text_original": "Cơ chế chia sẻ phần giảm doanh thu: Khi doanh thu thực tế đạt dưới 75% mức doanh thu trong phương án tài chính quy định tại hợp đồng dự án PPP, Nhà nước chia sẻ với nhà đầu tư, doanh nghiệp dự án PPP 50% phần chênh lệch giữa 75% mức doanh thu trong phương án tài chính và doanh thu thực tế.",
        "text_en": "Vietnam PPP Law Art 82 provides a revenue risk sharing mechanism: If actual revenue is <75% of the financial plan, the State shares 50% of the shortfall below 75%.",
        "text_zh": "【PPP最低收入政府兜底风险分担机制】：在国家重大基础设施 PPP 特许经营合同中，当项目特许运营实际收入低于财务方案预期收入的 75% 时，越南政府向投资者和PPP项目公司补贴分担‘75%预期收入与实际收入差额的 50%’！反之，当实际收入超过财务方案预期收入的 125% 时，投资者亦须将超额部分的 50% 上缴国库。【出海实务攻防】：中国出海基建央企投资越南收费公路、港口特许经营项目，可直接依据第82条将该法定收入分担机制锁定在特许经营协议中，阻断东道国因通车流量不足带来的严重财务穿透亏损风险！",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_vn82_ppp_concession", "text_zh": "要件一：项目属于依法签署并备案的国家重大公共基础设施PPP特许经营合同", "status": "condition_precedent"},
            {"eid": "e_vn82_revenue_shortfall", "text_zh": "要件二：年度实际经审计的特许运营收费总收入低于财务协议预定金额的75%", "status": "mandatory"},
            {"eid": "e_vn82_state_subsidy_payout", "text_zh": "法律后果：越南国家财政依法向PPP项目公司直接划拨差额50%的法定财政补偿补贴", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "TH:FBA_1999:Sec36_37",
        "law": "TH:FBA_1999",
        "enbez": "Sec 36~37",
        "title": "泰国外商经营法第36-37条：反代持刑事重锤与强制解散公司令",
        "heading_path": "泰国1999年外商经营法 (FBA B.E. 2542) > 第五章 罚则 > 刑事代持规避责任",
        "language_mode": "trilingual",
        "lang_original": "th",
        "text_original": "คนสัญชาติไทยที่ให้ความช่วยเหลือ สนับสนุน หรือถือหุ้นแทนคนต่างด้าวเพื่อให้คนต่างด้าวประกอบธุรกิจโดยหลีกเลี่ยงกฎหมายนี้ ต้องระวางโทษจำคุกไม่เกินสามปี หรือปรับตั้งแต่หนึ่งแสนบาทถึงหนึ่งล้านบาท หรือทั้งจำทั้งปรับ และให้ศาลสั่งเลิกการประกอบธุรกิจ",
        "text_en": "Thai nationals assisting or holding shares as nominees for foreigners to evade FBA face up to 3 years imprisonment or fine up to 1,000,000 Baht, and the Court shall order dissolution.",
        "text_zh": "【反股权代持刑事惩罚与强制解散】：泰国公民协助、支持或作为挂名股东代外国人持有股份，以协助外国人规避本法规定经营限制性业务的，处最高 3 年有期徒刑或 10 万至 100 万泰铢罚金，或二者并罚；外国实际控制人面临同等刑事处罚；法院必须判令强制解散该公司并按日加处罚金。【出海实务攻防】：泰国对建设工程（附表三第10项）和服务业严打‘泰国人持股51%、中资持股49%但通过优先股与授权委托书控制’的假合资结构；经商贸厅调查查实的，不仅公司被强制清盘注销，中资管理人员亦面临刑事逮捕与出境限制！必须通过申请 BOI 投资促进证书实现合法独资准入！",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory_override",
        "elements_json": json.dumps([
            {"eid": "e_th36_nominee_holding", "text_zh": "要件一：安排泰国自然人或挂名公司代外资持有受限行业法人的表决权股份", "status": "condition_precedent"},
            {"eid": "e_th36_evasion_intent", "text_zh": "要件二：客观目的系规避外商经营法附表三关于外资持股不得超过49%之强行限制", "status": "mandatory"},
            {"eid": "e_th36_criminal_dissolution", "text_zh": "法律后果：判处最高3年监禁+百万罚金，法院签发强制解散清盘令并没收涉案收益", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "PH:Anti_Dummy_Law:Sec1_2A",
        "law": "PH:Anti_Dummy_Law",
        "enbez": "Sec 1 & 2-A",
        "title": "菲律宾反傀儡法第1-2A条：规避外资比例刑事重罚与没收企业财产",
        "heading_path": "菲律宾反傀儡法 (Commonwealth Act No. 108) > 外资规避惩处专章",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Any person who facilitates the simulation of ownership of stocks to evade nationalization laws, or permits any alien to intervene in the management, operation, administration or control of the business, shall be punished by imprisonment for not less than 5 nor more than 15 years, and by a fine, and forfeiture of properties and franchise.",
        "text_en": "Evading nationalized equity limits via dummies or allowing aliens to intervene in management punishable by 5 to 15 years imprisonment, and forfeiture of properties.",
        "text_zh": "【反傀儡法（Anti-Dummy Law）刑事重锤与财产没收】：任何人通过虚构股份所有权（挂名持股 Dummy）协助外籍人规避宪法和法律设定的外国股比限制，或允许外籍人在外资受限企业中介入管理、运营、行政或实际控制的，处 5 年以上 15 年以下有期徒刑，并处罚金；涉案企业的特许权与全部企业财产依法予以强制没收归国有！【出海实务攻防】：菲律宾宪法对公共公用事业（如电网、水务、港口）设 40% 外资持股上限；中企若私下通过秘密股东协议任命外方高管实际操盘受限业务，直接撞上《反傀儡法》刑事红线，在著名的马尼拉机场 T3 航站楼案（Fraport 案）中，正因德国投资者违反本法，导致数亿美元投资全盘被 ICSID 仲裁庭驳回管辖且特许权被菲政府强制没收！",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory_override",
        "elements_json": json.dumps([
            {"eid": "e_ph_dummy_nominee_device", "text_zh": "要件一：利用菲律宾傀儡名义股东掩盖外资在受限国有化行业的实质控制权", "status": "condition_precedent"},
            {"eid": "e_ph_dummy_unlawful_management", "text_zh": "要件二：违规委派外籍人员出任核心运营管理职务直接控制特许经营活动", "status": "mandatory"},
            {"eid": "e_ph_dummy_criminal_forfeiture", "text_zh": "法律后果：处5至15年重度监禁，没收涉案特许权与全部企业资产，条约仲裁驳回管辖", "status": "prohibition"}
        ], ensure_ascii=False)
    },

    # =========================================================================
    # 实务域 06: 土地物权、征地清障、原住民领地与长期租赁 (L1+L2)
    # =========================================================================
    {
        "table": "norms",
        "norm_id": "ID:UUPA_5_1960:Art35_HGB",
        "law": "ID:UUPA_5_1960",
        "enbez": "Art 35",
        "title": "印尼土地法第35条：建筑使用权（HGB）外资最长80年法定权益",
        "heading_path": "印尼1960年第5号土地基本原则法 (UUPA) > 第二编 土地权利类型 > 建筑使用权",
        "language_mode": "trilingual",
        "lang_original": "id",
        "text_original": "Hak Guna Bangunan (HGB) adalah hak untuk mendirikan dan mempunyai bangunan-bangunan atas tanah yang bukan miliknya sendiri. HGB dapat beralih dan dialihkan kepada pihak lain, dan dapat diberikan kepada badan hukum yang didirikan menurut hukum Indonesia dan berkedudukan di Indonesia (termasuk PT PMA).",
        "text_en": "Building Right (HGB) allows PT PMA to construct and own buildings on land for up to 30 years, extendable for 20 years and renewable for 30 years (total 80 years).",
        "text_zh": "【建筑使用权（HGB）法律性质与 80 年阶梯期限】：建筑使用权（Hak Guna Bangunan, HGB）系指在非自有的国家土地或管理权土地上建造并拥有建筑物的物权；依据《创造就业法》及 PP 18/2021 最新规定，合资与外资企业（PT PMA）可依法直接持有 HGB，首次核准最长 30 年，期满可申请延长 20 年，到期后可申请更新 30 年，合计受保护物权期限最长可达 80 年！HGB 证书可依法向土地局办理第一顺位银行不动产抵押权（Hak Tanggungan）。【出海实务攻防】：印尼法律绝对禁止外资持有永久产权土地（Hak Milik），中企建厂、建变电站与开发光伏电站，唯一受物权法完全保护且可融资抵押的合法不动产物权即为 HGB 证书！",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_id35_pt_pma_eligibility", "text_zh": "要件一：主体为在印尼合法注册成立并存续的外商投资有限责任公司（PT PMA）", "status": "condition_precedent"},
            {"eid": "e_id35_bpn_title_registration", "text_zh": "要件二：向国家土地局（BPN）完成 HGB 宗地测量、空间规划核验并取得不动产权证", "status": "mandatory"},
            {"eid": "e_id35_eighty_year_mortgageable", "text_zh": "法律后果：依法享有最长80年排他性地面建筑占有使用权，并享有向银行办理抵押权权能", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "VN:Land_Law_2024:Art79",
        "law": "VN:Land_Law_2024",
        "enbez": "Art 79",
        "title": "越南2024新土地法第79条：国家行政收回土地32类穷尽目录与商业流转界限",
        "heading_path": "越南2024新土地法 (Law 31/2024/QH15) > 第六章 国家收回土地与补偿安置",
        "language_mode": "trilingual",
        "lang_original": "vi",
        "text_original": "Nhà nước thu hồi đất để phát triển kinh tế - xã hội vì lợi ích quốc gia, công cộng trong các trường hợp thật cần thiết sau đây: [Gồm 32 dự án cụ thể: năng lượng quốc gia, công trình giao thông, thủy lợi, khu công nghiệp, hạ tầng kỹ thuật... Dự án thương mại ngoài danh mục này nhà đầu tư phải tự thỏa thuận nhận chuyển nhượng].",
        "text_en": "Vietnam 2024 Land Law Art 79 establishes 32 exhaustive categories where State expropriates land. Projects outside Art 79 must acquire land through 100% voluntary agreement.",
        "text_zh": "【国家行政收地 32 类穷尽项目目录（2024年8月1日实施）】：国家为国家利益、公共利益实施经济社会发展收回土地，严格限定在第79条列举的 32 类重大项目范围内（含国家骨干电网、高速公路、工业园区基础设施、重点能源工程）；凡不在第79条目录内的普通商业项目与部分新能源项目，越南政府一律不负责行政清障征地，外资企业必须自行与沿线千百家农户达成 100% 自愿商业协议流转拿地！【出海实务攻防】：中企出海投资水电、风电、公路前，必须事先委托属地律师对照第79条审查项目是否列入国家收回清单；若未列入，绝不能向业主承诺包干交地进度，否则极易陷入数年无法清场交地的重大违约泥潭！",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory_override",
        "elements_json": json.dumps([
            {"eid": "e_vn79_within_32_catalogue", "text_zh": "要件一：拟建工程项目已正式列入越南2024土地法第79条32类国家收回基础设施清单", "status": "condition_precedent"},
            {"eid": "e_vn79_state_expropriation_role", "text_zh": "要件二：由省级或县级人民委员会依公法程序主导行政征拆、补偿公示与强制清场", "status": "mandatory"},
            {"eid": "e_vn79_voluntary_commercial_risk", "text_zh": "法律后果：清单内项目政府负责交地；清单外项目企业必须自负自愿流转风险", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "TH:CCC:Sec1410_Superficies",
        "law": "TH:CCC",
        "enbez": "Sec 1410",
        "title": "泰国民商法典第1410条：地上权（Superficies）三十年厂房电站物权隔离",
        "heading_path": "泰国民商法典 > 第四编 物权 > 第五章 地上权",
        "language_mode": "trilingual",
        "lang_original": "th",
        "text_original": "เจ้าของที่ดินอาจก่อให้เกิดสิทธิเหนือพื้นดินเป็นคุณแก่บุคคลอื่น โดยให้บุคคลนั้นมีสิทธิเป็นเจ้าของโรงเรือน สิ่งปลูกสร้าง หรือสิ่งเพาะปลูก บนดินหรือใต้ดินนั้นได้",
        "text_en": "Superficies under CCC Sec 1410 grants a person the right to own buildings, structures or plantations upon or under the land owned by another person.",
        "text_zh": "【地上权（Superficies）物权所有权隔离工具】：土地所有权人可为他人设定地上权，使该他人合法拥有该土地地表或地下的房屋、建筑物或附着物的物权所有权；地上权期限最长可达 30 年，或以设定人/取得人的有生之年为限；地上权可在土地厅办理正式物权登记，且可继承与转让。【出海实务攻防】：泰国土地法绝对禁止外资持有土地所有权；中资在泰建厂或投资分布式光伏、地面电站，若仅仅签署普通租赁合同，厂房和设备有被认定为附合于土地归地主所有的物权风险；通过在土地局登记第1410条‘地上权’，中企可独立且排他地享有其投资建造的厂房与发电设备的 100% 物权所有权，有效阻断地主破产查封！",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_th1410_landowner_grant", "text_zh": "要件一：与泰国土地所有权人正式签署期限最长达30年的地上权设立契约", "status": "condition_precedent"},
            {"eid": "e_th1410_land_office_registration", "text_zh": "要件二：向所在府土地厅（Land Office）在土地地契（Chanote）后页完成正式物权登记", "status": "mandatory"},
            {"eid": "e_th1410_independent_ownership", "text_zh": "法律后果：地上权人完全独立拥有土地上建造的厂房与特种工程设备之物权所有权", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "PH:RA_8371:Sec59_FPIC",
        "law": "PH:RA_8371",
        "enbez": "Sec 59",
        "title": "菲律宾原住民权利法第59条：祖传领地（CADT）自由事先知情同意（FPIC）",
        "heading_path": "菲律宾1997年原住民权利法 (IPRA RA 8371) > 原住民祖传领地合规专章",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "All departments and government agencies are strictly enjoined not to issue, renew, or grant any concession, license or lease without a prior certification from the NCIP that the area affected does not overlap with any ancestral domain, or that Free and Prior Informed Consent (FPIC) has been obtained from the ICCs/IPs concerned.",
        "text_en": "No concession, permit or lease shall be issued without prior NCIP certification that no ancestral domain is affected or that FPIC has been secured.",
        "text_zh": "【原住民祖传领地（CADT）自由事先知情同意强制认证】：一切政府部门和机构，严禁签发、续期或批准任何涉及工程特许经营、施工许可、环境批文或土地租赁文件，除非事先取得国家原住民委员会（NCIP）出具的合规证书，证明受影响区域不重叠任何祖传领地（CADT），或者已依法取得涉案原住民社区依传统习俗正式出具的《自由事先知情同意书》（FPIC）及合规谅解备忘录（MOA）。【出海实务攻防】：在菲律宾承建水电站、大坝、矿山与长距离输电线路，若未办理 NCIP 证书而贸然开工，原住民部落可直接向最高法院申请签发终身永久保护令（Writ of Kalikasan），导致项目永久停工、投资全盘沉没！",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory_override",
        "elements_json": json.dumps([
            {"eid": "e_ph59_ancestral_domain_overlap", "text_zh": "要件一：工程项目红线范围涉及或紧邻经登记或主张的土著原住民祖传领地（CADT）", "status": "condition_precedent"},
            {"eid": "e_ph59_fpic_consultation_process", "text_zh": "要件二：在NCIP主持下全面履行部落协商程序并取得原住民部落出具的FPIC认证", "status": "mandatory"},
            {"eid": "e_ph59_precondition_for_permits", "text_zh": "法律后果：取得NCIP证书为一切施工、环保ECC及特许权批文合法有效的刚性前提", "status": "prohibition"}
        ], ensure_ascii=False)
    }
]
