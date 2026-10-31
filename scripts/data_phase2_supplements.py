"""
data_phase2_supplements.py - Phase 2 补充模块：
补齐前次编写遗漏的 38 条涉外条约与标准规范，使 Phase 2 规范总数完整达到 102 条：
1. 9 条 FIDIC 核心条款 (使 FIDIC 达到 32 条)
2. 5 条 DTA 核心条款 (使 DTA 达到 13 条)
3. 3 条 6国 BIT 核心条款 (使 BIT 达到 17 条)
4. 8 条 中国出海强监管规范 (使 PRC 出海监管达到 20 条)
5. 13 条 多边条约、国际仲裁规则与采购制裁规范 (使多边条约达到 20 条)
以及判例配套的 3 条属地成文法 (PH Art 1713, TH Sec 215, MY Sec 19H)
所有规范 100% 结构化填充 elements_json
"""
import json

PHASE2_FIDIC_SUPPLEMENTS = [
    {
        "table": "reference_norms",
        "norm_id": "FIDIC:Silver_1999:Clause_1.1",
        "law": "FIDIC:Silver_1999",
        "enbez": "Clause 1.1",
        "title": "FIDIC银皮书第1.1款：基准日Base Date与不可预见风险定义",
        "heading_path": "FIDIC EPC/交钥匙合同条件 (Silver Book 1999) > 第1条 一般规定 > 定义",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Base Date means the date 28 days prior to the latest date for submission of the Tender. 'Unforeseeable' means not reasonably foreseeable by an experienced contractor by the date for submission of the Tender.",
        "text_en": "Base Date is 28 days prior to tender submission; Unforeseeable means not reasonably foreseeable by an experienced contractor by tender date.",
        "text_zh": "【基准日与不可预见性法定界限】：基准日（Base Date）是指投标截止日前第28天的日期。‘不可预见（Unforeseeable）’是指在投标截止日之前一个有经验的承包商无法合理预见的风险事件。【实务启示】：基准日是东道国法律变更（13.7款）和税费调差的绝对时间分界线；凡在基准日之后发生的新设税费或环保法令，总包商均享有工期和费用索赔权！",
        "norm_category": "fidic_standard",
        "mandatory_level": "contract_default",
        "elements_json": json.dumps([
            {"eid": "e_fidic11_base_date_calc", "text_zh": "要件一：精确锁定投标递交截止日前整28天作为法律与技术参数基准日", "status": "condition_precedent"},
            {"eid": "e_fidic11_experienced_contractor", "text_zh": "要件二：以具备相应资质能力的‘有经验承包商’专业认知作为预见性客观标准", "status": "mandatory"},
            {"eid": "e_fidic11_risk_allocation", "text_zh": "法律后果：基准日后外部法律税费变动风险由雇主承担并赋予承包商调价权", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "FIDIC:Silver_1999:Clause_1.3",
        "law": "FIDIC:Silver_1999",
        "enbez": "Clause 1.3",
        "title": "FIDIC银皮书第1.3款：往来函件书面送达与电子通讯效力",
        "heading_path": "FIDIC EPC/交钥匙合同条件 (Silver Book 1999) > 第1条 一般规定 > 通讯交流",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Communications: Wherever these Conditions provide for the giving or issuing of approvals, certificates, consents, determinations, notices and requests, these communications shall be in writing and delivered by hand, sent by mail or courier, or transmitted using any agreed systems of electronic transmission.",
        "text_en": "Notices and determinations must be in writing and properly delivered by hand, courier, or agreed electronic transmission systems.",
        "text_zh": "【书面通知送达要件与失权抗辩根基】：凡合同约定的批准、证书、同意、确定、通知和请求，必须采用书面形式，并通过当面签收、专人快递或合同约定电子系统送达指定地址。【实务启示】：索赔预警通告必须严格遵照第1.3款送达！现场工程师口头承诺在法律上自始无效，必须形成书面纪要并由代表签字确认！",
        "norm_category": "fidic_standard",
        "mandatory_level": "contract_default",
        "elements_json": json.dumps([
            {"eid": "e_fidic13_written_form", "text_zh": "要件一：通讯内容形成书面纸质文件或双方约定的正式电子文档", "status": "condition_precedent"},
            {"eid": "e_fidic13_proper_service", "text_zh": "要件二：送达至合同专用条件明确指定的代表处或授权接收人", "status": "mandatory"},
            {"eid": "e_fidic13_valid_effect", "text_zh": "法律后果：满足法定期限起算条件，阻断逾期失权异议", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "FIDIC:Silver_1999:Clause_1.5",
        "law": "FIDIC:Silver_1999",
        "enbez": "Clause 1.5",
        "title": "FIDIC银皮书第1.5款：合同文件优先解释顺序与条款冲突裁决",
        "heading_path": "FIDIC EPC/交钥匙合同条件 (Silver Book 1999) > 第1条 一般规定 > 文件优先次序",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Priority of Documents: The documents forming the Contract are to be taken as mutually explanatory of one another. For the purposes of interpretation, the priority of the documents shall be: (a) Contract Agreement, (b) Particular Conditions, (c) General Conditions, (d) Employer's Requirements, (e) Tender and any other documents.",
        "text_en": "Contract documents are mutually explanatory; Contract Agreement and Particular Conditions take strict precedence over General Conditions and Employer's Requirements.",
        "text_zh": "【合同文件优先解释顺序】：构成合同的文件应视为互为说明。如有歧义，优先次序依次为：① 合同协议书，② 专用条件，③ 通用条件，④ 雇主要求，⑤ 投标书及其他文件。【实务启示】：专用条件高于雇主要求！若雇主要求中暗藏严苛的单方扣款霸王条款，只要中资企业在专用条件中做了对等保护修改，专用条件即具有优先压制效力！",
        "norm_category": "fidic_standard",
        "mandatory_level": "contract_default",
        "elements_json": json.dumps([
            {"eid": "e_fidic15_document_ambiguity", "text_zh": "要件一：不同合同组成文件就同一权利义务存在文字冲突或实质歧义", "status": "condition_precedent"},
            {"eid": "e_fidic15_order_hierarchy", "text_zh": "要件二：严格依据第1.5款法定层级顺序比对文件效力高低", "status": "mandatory"},
            {"eid": "e_fidic15_override_lower", "text_zh": "法律后果：高顺位文件自动覆盖并排除低顺位文件的抵触内容", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "FIDIC:Silver_1999:Clause_1.13",
        "law": "FIDIC:Silver_1999",
        "enbez": "Clause 1.13",
        "title": "FIDIC银皮书第1.13款：遵守东道国成文法与主规划许可分工",
        "heading_path": "FIDIC EPC/交钥匙合同条件 (Silver Book 1999) > 第1条 一般规定 > 遵守法律",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Compliance with Laws: The Contractor shall comply with applicable Laws. Unless otherwise stated in the Particular Conditions: (a) the Employer shall have obtained planning, zoning or similar permission for the Permanent Works, and (b) the Contractor shall give all notices, pay all taxes, and obtain all permits required by the Laws in relation to the execution of the Works.",
        "text_en": "Employer is strictly responsible for planning and zoning permissions; Contractor handles execution permits, taxes, and operational compliance.",
        "text_zh": "【主规划规划许可与施工许可法定职责划分】：承包商应遵守适用法律。除非专用条件另有约定：① 雇主应为永久工程取得城市规划、用地许可及类似主批文；② 承包商应办理施工许可证、缴纳税费并遵守工程实施相关规范。【实务启示】：中资EPC总包切忌包揽永久用地规划与土地征用批文！一旦雇主未取得规划许可导致政府叫停施工，总包商依此条享有工期与成本全额索赔权！",
        "norm_category": "fidic_standard",
        "mandatory_level": "contract_default",
        "elements_json": json.dumps([
            {"eid": "e_fidic113_employer_planning", "text_zh": "要件一：雇主未能在开工前取得法定的永久工程规划选址与土地征用主许可", "status": "condition_precedent"},
            {"eid": "e_fidic113_contractor_exec_permits", "text_zh": "要件二：承包商已全面履行自身施工阶段作业报备与安全技术合规义务", "status": "mandatory"},
            {"eid": "e_fidic113_employer_default", "text_zh": "法律后果：认定雇主违反先决义务，承包商享有停工豁免与工期索赔权", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "FIDIC:Silver_1999:Clause_2.1",
        "law": "FIDIC:Silver_1999",
        "enbez": "Clause 2.1",
        "title": "FIDIC银皮书第2.1款：现场进入与占有权迟延索赔工期与费用利润",
        "heading_path": "FIDIC EPC/交钥匙合同条件 (Silver Book 1999) > 第2条 雇主 > 现场进入与占有权",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Right of Access to the Site: The Employer shall give the Contractor right of access to, and possession of, all parts of the Site within the time stated in the Contract. If the Contractor suffers delay and/or incurs Cost as a result of a failure by the Employer to give any such right, the Contractor shall be entitled to EOT and payment of any such Cost plus reasonable profit.",
        "text_en": "Employer must grant timely Site access and possession; failure entitles Contractor to EOT and payment of Cost plus reasonable profit.",
        "text_zh": "【现场移交迟延索赔工期与利润】：雇主应在合同约定时间内向承包商移交现场全部区域的进入权与占有权。若雇主迟延移交导致承包商延误或增加成本，承包商享有顺延竣工工期、补偿实际费用并加计合理利润之法定索赔权！【实务启示】：海外征地清障往往迟缓，中资总包必须将‘移交完整且无障碍施工现场’列为工期起算前提，严防未交地即算工期的倒挂陷阱！",
        "norm_category": "fidic_standard",
        "mandatory_level": "contract_default",
        "elements_json": json.dumps([
            {"eid": "e_fidic21_handover_schedule", "text_zh": "要件一：合同约定的进场日期届满而雇主未完成征地拆迁交付现场", "status": "condition_precedent"},
            {"eid": "e_fidic21_delay_cost_incurred", "text_zh": "要件二：承包商人员机械窝工并产生实质性工期延误与费用增加", "status": "mandatory"},
            {"eid": "e_fidic21_cost_plus_profit", "text_zh": "法律后果：依法顺延总工期，全额补偿人员设备闲置成本并加计合理利润", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "FIDIC:Silver_1999:Clause_2.4",
        "law": "FIDIC:Silver_1999",
        "enbez": "Clause 2.4",
        "title": "FIDIC银皮书第2.4款：雇主资金安排证明与28天不提供承包商停工解约权",
        "heading_path": "FIDIC EPC/交钥匙合同条件 (Silver Book 1999) > 第2条 雇主 > 雇主的资金安排",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Employer's Financial Arrangements: The Employer shall submit, within 28 days after receiving any request from the Contractor, reasonable evidence that financial arrangements have been made and are being maintained which will enable the Employer to pay the Contract Price punctually. If the Employer fails to submit such evidence, the Contractor may suspend work under Sub-Clause 16.1 or terminate under Sub-Clause 16.2.",
        "text_en": "Employer must provide reasonable financial evidence within 28 days of Contractor's request; failure empowers Contractor to suspend or terminate.",
        "text_zh": "【雇主资金能力审查与法定抗辩权】：承包商有权随时要求雇主出具合理的资金安排证明。雇主必须在收到请求后28天内提交其具备按期支付合同价款能力的真实银行授信或融资证明；若雇主逾期无法提供，承包商有权依据第16.1款暂停施工或依据第16.2款单方解除合同并追索损失！【实务启示】：海外业主资金链恶化时的止损王牌！一旦业主拖欠款项，立即依据第2.4款发函调取资信证明，不给则顺理成章合法停工！",
        "norm_category": "fidic_standard",
        "mandatory_level": "contract_default",
        "elements_json": json.dumps([
            {"eid": "e_fidic24_written_request", "text_zh": "要件一：承包商就雇主资金保障履约能力正式发出书面索证函件", "status": "condition_precedent"},
            {"eid": "e_fidic24_28days_expiration", "text_zh": "要件二：雇主在法定 28 天期限届满后仍未出具银行放款或承兑支持材料", "status": "mandatory"},
            {"eid": "e_fidic24_suspension_termination", "text_zh": "法律后果：承包商即刻享有法定暂停施工权、工期顺延权及单方终局解约权", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "FIDIC:Silver_1999:Clause_8.5",
        "law": "FIDIC:Silver_1999",
        "enbez": "Clause 8.5",
        "title": "FIDIC银皮书第8.5款：行政当局造成的延误索赔工期顺延",
        "heading_path": "FIDIC EPC/交钥匙合同条件 (Silver Book 1999) > 第8条 开工、延误和暂停 > 当局造成的延误",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Delays Caused by Authorities: If the Contractor has diligently followed procedures laid down by relevant legally constituted authorities in the Country, and such authorities delay or disrupt the Contractor's work, and the delay or disruption was Unforeseeable, then this delay or disruption will be considered as a cause of delay under Sub-Clause 8.4 [Extension of Time for Completion].",
        "text_en": "Delays caused by host state public authorities constitute grounds for EOT under Sub-Clause 8.4, provided Contractor diligently followed procedures.",
        "text_zh": "【行政当局延误索赔工期豁免违约金】：若承包商已勤勉遵守了东道国合法成立的主管当局所规定的程序，但该等行政当局迟延或中断了工程实施（如海关设备扣押、环保部门审查超期、市政迁改迟延），且该延误属于不可预见的，则该延误依法构成第8.4款项下的工期顺延（EOT）事由！【实务启示】：破除业主‘外力延误由总包全担’的利器！中资总包只要证明自身申请手续合规无瑕疵，属地官僚机构的拖延即可全额转化为免扣违约金的工期延长！",
        "norm_category": "fidic_standard",
        "mandatory_level": "contract_default",
        "elements_json": json.dumps([
            {"eid": "e_fidic85_diligent_compliance", "text_zh": "要件一：承包商已及时且合规地向东道国主管行政机关递交全部审批申请", "status": "condition_precedent"},
            {"eid": "e_fidic85_unforeseeable_disruption", "text_zh": "要件二：行政机关审批超期或关停行政行为系不可预见且超出通常时限", "status": "mandatory"},
            {"eid": "e_fidic85_eot_entitlement", "text_zh": "法律后果：承包商享有免于承担误期违约金之全额工期顺延权", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "FIDIC:Red_1999:Clause_4.12",
        "law": "FIDIC:Red_1999",
        "enbez": "Clause 4.12",
        "title": "FIDIC红皮书第4.12款：不可预见物质与地质条件全额索赔工期与成本",
        "heading_path": "FIDIC 施工合同条件 (Red Book 1999) > 第4条 承包商 > 不可预见的物质条件",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Unforeseeable Physical Conditions: If the Contractor encounters adverse physical conditions which he considers to have been Unforeseeable, the Contractor shall give notice to the Engineer. To the extent that the Contractor suffers delay and/or incurs Cost, the Contractor shall be entitled subject to Sub-Clause 20.1 to: (a) EOT, and (b) payment of any such Cost.",
        "text_en": "Contractor is entitled to EOT and Cost compensation for encountering unforeseeable adverse physical conditions, contrasting with Silver Book risks.",
        "text_zh": "【红皮书地下不可预见地质条件索赔】：承包商遇到其认为不可预见的不利物质与地下地质条件（如流沙、溶洞、未勘明断裂带）时，通知工程师后享有顺延工期及实际支出成本补偿之法定索赔权。【实务启示】：红皮书与银皮书的核心分野！银皮书第4.12款将全部地下未知风险强行归于总承包商；中资企业承接单价合同必须牢牢依据红皮书4.12索赔地质超标费用！",
        "norm_category": "fidic_standard",
        "mandatory_level": "contract_default",
        "elements_json": json.dumps([
            {"eid": "e_fidic_r412_unforeseeable_geology", "text_zh": "要件一：现场开挖揭示的不良地质条件超出了地勘报告与有经验专业认知范围", "status": "condition_precedent"},
            {"eid": "e_fidic_r412_timely_engineer_notice", "text_zh": "要件二：在遭遇该地质条件后第一时间向驻地工程师签发正式索赔通知", "status": "mandatory"},
            {"eid": "e_fidic_r412_eot_and_cost", "text_zh": "法律后果：承包商全额享有实际工期顺延及地质加固处置成本补偿", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "FIDIC:Silver_1999:Clause_15.5",
        "law": "FIDIC:Silver_1999",
        "enbez": "Clause 15.5",
        "title": "FIDIC银皮书第15.5款：雇主便利终止权严禁为自建或转包第三方而行使",
        "heading_path": "FIDIC EPC/交钥匙合同条件 (Silver Book 1999) > 第15条 由雇主终止 > 雇主终止合同的权利",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Employer's Entitlement to Termination: The Employer shall be entitled to terminate the Contract, at any time for the Employer's convenience, by giving notice of such termination to the Contractor. The Employer shall not terminate the Contract under this Sub-Clause in order to execute the Works himself or to arrange for the Works to be executed by another contractor.",
        "text_en": "Employer may terminate for convenience but is strictly prohibited from doing so to execute the works himself or award to another contractor.",
        "text_zh": "【雇主任意解除权之恶意替换承包商红线】：雇主有权为自身便利随时解除合同。但雇主严禁为了‘自行施工’或‘转包给其他竞争对手承包商’而援引本款便利终止合同！雇主违规解约构成普通法恶意毁约，承包商有权追索全部合同预期利润损失（Expectation Damages）！【实务启示】：严防海外业主‘偷窃中资方案后踢开中资换本地队伍’！若业主无正当理由便利解约并另请他人，总承包商可直接诉请包含全部所失利润的巨额赔偿！",
        "norm_category": "fidic_standard",
        "mandatory_level": "contract_default",
        "elements_json": json.dumps([
            {"eid": "e_fidic155_convenience_notice", "text_zh": "要件一：雇主未举证承包商违约而依据自身商业考量签发便利解除通知", "status": "condition_precedent"},
            {"eid": "e_fidic155_malicious_replacement", "text_zh": "要件二：雇主在解约后自行接管施工或将剩余工程重新发包给关联第三方", "status": "mandatory"},
            {"eid": "e_fidic155_expectation_damages", "text_zh": "法律后果：认定雇主便利解约权滥用构成实质毁约，判令赔偿承包商全部预期利润", "status": "prohibition"}
        ], ensure_ascii=False)
    }
]

PHASE2_DTA_SUPPLEMENTS = [
    {
        "table": "reference_norms",
        "norm_id": "DTA:CN_SG:Art5_PE",
        "law": "DTA:CN_SG",
        "enbez": "Art 5",
        "title": "中新双边税收协定第五条：建筑工程常设机构6个月门槛",
        "heading_path": "中国-新加坡避免双重征税协定 (DTA) > 第5条 常设机构",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "A building site or construction, installation or assembly project constitutes a permanent establishment only if it lasts more than 6 months.",
        "text_en": "A building site, construction, installation or assembly project constitutes PE in Singapore only if lasting over 6 months.",
        "text_zh": "【中新建筑工程常设机构6个月界限】：中国居民企业在新加坡设立的建筑工地、建筑、安装或装配工程，仅在存续时间连续或累计超过6个月时方构成新加坡常设机构（PE）。【实务启示】：未达6个月的技术安装和调试，依协定受保护免向新加坡税务局（IRAS）缴纳17%的企业所得税！",
        "norm_category": "tax_treaty",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_dtasg5_six_months_threshold", "text_zh": "要件一：在新加坡境内的施工作业或安装项目存续时间累计超6个月", "status": "condition_precedent"},
            {"eid": "e_dtasg5_iras_taxation", "text_zh": "要件二：依法在新加坡设立营业地或由项目部代扣代缴公司税款", "status": "mandatory"},
            {"eid": "e_dtasg5_offshore_exemption", "text_zh": "法律后果：未达6个月免纳在岸公司税，超6个月仅对归属利润征税", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "DTA:CN_SG:Art7_Business_Profits",
        "law": "DTA:CN_SG",
        "enbez": "Art 7",
        "title": "中新双边税收协定第七条：营业利润归属原则与离岸设备免税",
        "heading_path": "中国-新加坡避免双重征税协定 (DTA) > 第7条 营业利润",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "The profits of an enterprise of a Contracting State shall be taxable only in that State unless the enterprise carries on business in the other Contracting State through a permanent establishment. Only profits attributable to that PE may be taxed in Singapore.",
        "text_en": "Profits of Chinese enterprise are taxable only in China unless carried on through PE in Singapore, and only attributable profits may be taxed.",
        "text_zh": "【中新营业利润与EPC离岸设备拆分免税】：中国企业的营业利润仅在中国征税，除非通过在新加坡的常设机构开展业务。即便设有常设机构，新加坡仅有权对‘直接归属于该常设机构’的利润征税。【实务启示】：中资企业承揽涉新 EPC 工程，离岸设计及在中国境内制造交付的成套装备，全额免受新加坡所得税征管！",
        "norm_category": "tax_treaty",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_dtasg7_offshore_revenue", "text_zh": "要件一：设备制造及物权转移全过程发生在新加坡境外离岸管辖地", "status": "condition_precedent"},
            {"eid": "e_dtasg7_arm_length_pricing", "text_zh": "要件二：离岸供货与在岸建安服务定价符合独立交易公平原则", "status": "mandatory"},
            {"eid": "e_dtasg7_iras_no_nexus", "text_zh": "法律后果：新加坡税务局严禁对离岸设备货款强行合并计税", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "DTA:CN_ID:Art5_PE",
        "law": "DTA:CN_ID",
        "enbez": "Art 5",
        "title": "中印尼双边税收协定第五条：建筑安装常设机构6个月门槛",
        "heading_path": "中国-印度尼西亚双边税收协定 (DTA) > 第5条 常设机构",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "A building site, a construction, assembly or installation project or supervisory activities in connection therewith constitutes a permanent establishment only if it lasts more than 6 months.",
        "text_en": "Construction site or installation project in Indonesia constitutes PE only if lasting over 6 months.",
        "text_zh": "【中印尼建筑工程常设机构6个月判定】：中国企业在印尼的建筑、安装、装配项目或工程监理活动，仅在超过6个月时构成印尼常设机构（BUT）。【实务启示】：未满6个月的指导作业免于设立代表处，超6个月则必须在印尼设立外国建筑企业办事处（BUJKA）并申报纳税！",
        "norm_category": "tax_treaty",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_dtaid5_duration_test", "text_zh": "要件一：印尼境内工程承包活动实际持续时间累计达到或超过6个月", "status": "condition_precedent"},
            {"eid": "e_dtaid5_bujka_registration", "text_zh": "要件二：办理公共工程部与税务局合规登记建立常设机构BUT", "status": "mandatory"},
            {"eid": "e_dtaid5_tax_liability", "text_zh": "法律后果：对常设机构按最终所得税（PPh Final）征税，未满6个月全额豁免", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "DTA:CN_ID:Art12_Royalties",
        "law": "DTA:CN_ID",
        "enbez": "Art 12",
        "title": "中印尼双边税收协定第十二条：特许权使用费与技术服务费10%上限",
        "heading_path": "中国-印度尼西亚双边税收协定 (DTA) > 第12条 特许权使用费",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Royalties arising in Indonesia and paid to a resident of China may be taxed in Indonesia, but the tax so charged shall not exceed 10% of the gross amount of the royalties.",
        "text_en": "Indonesian withholding tax on royalties paid to Chinese resident shall not exceed 10% of gross amount.",
        "text_zh": "【中印尼特许权与技术服务费预提所得税上限】：印尼对支付给中国居民企业的特许权使用费（含专利技术使用许可、工业商业经验传授）所征收的预提所得税（WHT），依法不得超过总额的10%（印尼国内法通常为20%）。【实务启示】：中资央企向印尼电站或矿山输出专有技术、收取许可费时，必须出具中国税务居民身份证明（COR/DGT-1），直接将预提税砍半至10%！",
        "norm_category": "tax_treaty",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_dtaid12_valid_cor", "text_zh": "要件一：向印尼税务主管机关正式递交由中国国税局出具的税收居民身份证明", "status": "condition_precedent"},
            {"eid": "e_dtaid12_genuine_ip", "text_zh": "要件二：技术许可与软件使用费具备真实经济合理性与专有知识属性", "status": "mandatory"},
            {"eid": "e_dtaid12_cap_10_percent", "text_zh": "法律后果：印尼境内支付方强制适用 10% 优惠税率扣缴，严禁适用 20% 国内法税率", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "DTA:CN_VN:Art7_Business_Profits",
        "law": "DTA:CN_VN",
        "enbez": "Art 7",
        "title": "中越双边税收协定第七条：营业利润与离岸设备供货免税",
        "heading_path": "中国-越南双边税收协定 (DTA) > 第7条 营业利润",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "The profits of an enterprise of a Contracting State shall be taxable only in that State unless the enterprise carries on business in Vietnam through a permanent establishment. Only profits attributable to that PE may be taxed in Vietnam.",
        "text_en": "Profits of Chinese enterprise are taxable only in China unless through PE in Vietnam; only attributable profits are subject to Vietnamese tax.",
        "text_zh": "【中越营业利润与EPC总承包离岸供货免税】：中国企业的营业利润仅在中国征税，除非在越南设有常设机构。在越南设立常设机构的，越南税务局仅能对归属于该常设机构的在岸劳务利润征税。【实务启示】：越南外国承包商税（FCT）包含增值税与企业所得税；中资企业通过离岸签订设备供货合同（E），离岸供货部分免征在越所得税！",
        "norm_category": "tax_treaty",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_dtavn7_onshore_offshore_split", "text_zh": "要件一：EPC合同严格拆分为离岸设备供货合同与在岸技术服务施工合同", "status": "condition_precedent"},
            {"eid": "e_dtavn7_customs_fob_delivery", "text_zh": "要件二：设备供货以FOB/CIF离岸条款交收且在越南境外完成所有权移转", "status": "mandatory"},
            {"eid": "e_dtavn7_fct_exemption", "text_zh": "法律后果：离岸设备款受协定保护免征在越外国承包商企业所得税", "status": "prohibition"}
        ], ensure_ascii=False)
    }
]

PHASE2_BIT_SUPPLEMENTS = [
    {
        "table": "reference_norms",
        "norm_id": "TREATY:CN_VN_BIT_1992:Art4_Expropriation",
        "law": "TREATY:CN_VN_BIT_1992",
        "enbez": "Art 4",
        "title": "中越双边投资协定第四条：征收、征用补偿标准与可自由转移",
        "heading_path": "中越双边投资保护协定 (BIT 1992) > 第4条 征收与补偿",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Expropriation: Investments shall not be expropriated or nationalised except for a public purpose, under domestic legal procedures, on a non-discriminatory basis and against compensation. Such compensation shall amount to the real value of the investment immediately before the expropriation.",
        "text_en": "Expropriation permitted only for public purpose, non-discriminatory, and with compensation equivalent to real value of investment immediately before expropriation.",
        "text_zh": "【中越BIT征收法定补偿与实际真实价值原则】：缔约任何一方对投资者的投资不得实行国有化或征收，除非符合：① 为了公共利益，② 依照国内法律程序，③ 非歧视性，④ 给予补偿。该补偿应等于‘宣布征收前一刻投资财产的实际真实价值（Real Value）’，并计入自征收之日起至支付日的正常利息，且补偿款可自由兑换汇出！【实务启示】：越南政府若无偿废止中资光伏/风电特许权（PPA）或强行回收土地，已构成征收，央企可依此款索赔全额实际价值！",
        "norm_category": "bit_treaty",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_bit_vn4_state_taking", "text_zh": "要件一：东道国行政机关撤销特许权或强行没收投资者合法资产构成实质征收", "status": "condition_precedent"},
            {"eid": "e_bit_vn4_real_value_assessment", "text_zh": "要件二：以征收决定宣布前一刻的资产公允市场价值计算损害赔偿金", "status": "mandatory"},
            {"eid": "e_bit_vn4_full_compensation_interest", "text_zh": "法律后果：东道国政府负有支付全额真实价值并加计利息且自由汇出之国家责任", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "TREATY:CN_MY_BIT_1988:Art3_FET",
        "law": "TREATY:CN_MY_BIT_1988",
        "enbez": "Art 3",
        "title": "中马双边投资协定第三条：公正与公平待遇(FET)与最惠国待遇",
        "heading_path": "中马双边投资协定 (BIT 1988) > 第3条 投资待遇",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Investments of investors of either Contracting Party shall at all times be accorded fair and equitable treatment and shall enjoy full protection and security in the territory of the other Contracting Party.",
        "text_en": "Investments shall at all times receive fair and equitable treatment (FET) and enjoy full protection and security in Malaysia.",
        "text_zh": "【中马投资公正与公平待遇标准】：缔约任何一方的投资者在缔约另一方的领土内的投资，应始终享受公正与公平的待遇（Fair and Equitable Treatment, FET），并享受充分的保护与安全。【实务启示】：国际投资仲裁的万能利剑！当大马政府突然撕毁重大基建采购合同、朝令夕改撤销外资准入许可或司法程序存在恶意拖延时，中资企业均可援引 FET 认定东道国违反国际法信赖保护原则！",
        "norm_category": "bit_treaty",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_bit_my3_legitimate_expectation", "text_zh": "要件一：投资者基于东道国政府正式批准批文与立法政策形成合理投资信赖", "status": "condition_precedent"},
            {"eid": "e_bit_my3_arbitrary_revocation", "text_zh": "要件二：东道国无正当理由溯及既往撕毁许可或改变核心监管规则", "status": "mandatory"},
            {"eid": "e_bit_my3_fet_breach", "text_zh": "法律后果：认定东道国违反公正公平待遇国际法义务并触发国际仲裁国家赔偿", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "TREATY:CN_TH_BIT_1985:Art5_Expropriation",
        "law": "TREATY:CN_TH_BIT_1985",
        "enbez": "Art 5",
        "title": "中泰双边投资协定第五条：征收法定条件、市价补偿与自由汇出",
        "heading_path": "中泰双边投资协定 (BIT 1985) > 第5条 征收",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Neither Contracting Party shall take any measures of expropriation against investments of investors of the other Contracting Party unless the measures are taken for public purpose, under legal procedures and against compensation. Such compensation shall be effectively realisable and freely transferable without delay.",
        "text_en": "Expropriation must be for public purpose, under legal procedures, with compensation effectively realisable and freely transferable without delay.",
        "text_zh": "【中泰征收与合理市场价值赔偿保障】：缔约任何一方不得对缔约另一方投资者的投资采取征收措施，除非为了公共利益、依照国内法律程序并给予合理补偿。补偿金应能有效兑现、无迟延地自由汇出，并计入自征收之日起的合理商业利息。【实务启示】：泰国因环保抗议或政局变动强行接管中资工厂或没收设备时，总包商依此条享有索赔充分、有效、及时补偿的国际公法直接诉权！",
        "norm_category": "bit_treaty",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_bit_th5_regulatory_taking", "text_zh": "要件一：泰国政府采取没收、征用或实质性剥夺资产控制权的行政措施", "status": "condition_precedent"},
            {"eid": "e_bit_th5_no_adequate_payment", "text_zh": "要件二：东道国未按照公允市场价值及时支付有效赔偿金", "status": "mandatory"},
            {"eid": "e_bit_th5_free_transfer_right", "text_zh": "法律后果：东道国承担金钱赔偿责任，并保障赔偿金可自由兑换外币出境", "status": "prohibition"}
        ], ensure_ascii=False)
    }
]

PHASE2_PRC_SUPPLEMENTS = [
    {
        "table": "norms",
        "norm_id": "CN:Foreign_Related_Civil_Relations:Art14_Legal_Person",
        "law": "CN:Foreign_Related_Civil_Relations",
        "enbez": "Art 14",
        "title": "涉外民事关系法律适用法第十四条：法人权利能力与注册登记地法",
        "heading_path": "中华人民共和国涉外民事关系法律适用法 > 第二章 人身关系 > 法人及其分支机构",
        "language_mode": "bilingual",
        "lang_original": "zh",
        "text_original": "法人及其分支机构的民事权利能力、民事行为能力、内部组织机构、股东权利义务等事项，适用登记地法律。法人的经常居所地与登记地不一致的，可以适用经常居所地法律。法人的主营业地，可以视为法人的经常居所地。",
        "text_en": "Capacity, internal organization, shareholder rights of a legal person shall be governed by law of registration place or habitual residence.",
        "text_zh": "【跨国企业法人权利能力与注册登记地法冲突规则】：涉外合资企业（JV/SPV）的民事权利能力、行为能力、内部治理架构（董事会职权、股东表决比例）等事项，强制适用注册登记地法律！【实务启示】：中国央企在新加坡或印尼设立的 SPV，其章程修改、董事信义义务、股权转让要件一律适用新加坡或印尼公司法，严禁套用中国《公司法》规则，否则决议自始无效！",
        "norm_category": "crossborder_litigation",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_cn_col14_registration_lex_societatis", "text_zh": "要件一：纠纷标的属于法人设立资格、股权结构、内部决议效力等公司法范畴", "status": "condition_precedent"},
            {"eid": "e_cn_col14_lex_loci_incorporation", "text_zh": "要件二：查明目标法人设立时的境外注册登记管辖法域（Lex Societatis）", "status": "mandatory"},
            {"eid": "e_cn_col14_mandatory_foreign_law", "text_zh": "法律后果：强制适用属地公司法判定内部治理效力，排除中国公司法直接适用", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "CN:SPC_Foreign_Law_Ascertainment_2023:Art5_Burden_of_Proof",
        "law": "CN:SPC_Foreign_Law_Ascertainment_2023",
        "enbez": "Art 5",
        "title": "最高法外法查明规定第五条：当事人举证责任与法院依职权查明",
        "heading_path": "最高人民法院关于适用涉外民事关系法律适用法若干问题的解释（二） > 域外法查明责任与途径",
        "language_mode": "bilingual",
        "lang_original": "zh",
        "text_original": "当事人选择适用域外法的，应当提供该域外法。当事人无法提供或者人民法院依职权查明域外法的，人民法院可以通过下列途径协助查明：由当事人提供、通过外交途径、通过司法协助途径、通过法律查明服务机构或者中外法律专家提供。",
        "text_en": "Parties choosing foreign law bear burden of proving it; court may assist ascertainment via legal institutions or expert witnesses.",
        "text_zh": "【涉外案件域外法举证责任分配与权威查明路径】：合同当事人协议选择适用东盟域外法（如新加坡法、印尼法）的，主张方应当承担提供该法条与判例之举证责任。无法提供且穷尽查明手段仍不能查明的，法院方可适用中国法裁判。【实务启示】：涉外审判重大规则！中资企业在涉外涉外仲裁或涉外诉讼中必须主动委托专业域外法查明机构出具法律查明报告，否则承担举证不能的不利后果！",
        "norm_category": "crossborder_litigation",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_cn_fla5_party_choice", "text_zh": "要件一：合同各方根据意思自治原则明示约定适用东盟属地法", "status": "condition_precedent"},
            {"eid": "e_cn_fla5_burden_production", "text_zh": "要件二：主张适用外法的一方按期向法庭递交成文法文本及专家法律意见书", "status": "mandatory"},
            {"eid": "e_cn_fla5_admissibility", "text_zh": "法律后果：确立外法作为裁判准据之正当性，阻断法官径行适用中国法代审", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "CN:SPC_Foreign_Law_Ascertainment_2023:Art8_Expert_Witness",
        "law": "CN:SPC_Foreign_Law_Ascertainment_2023",
        "enbez": "Art 8",
        "title": "最高法外法查明规定第八条：域外法律专家证人出庭与质证",
        "heading_path": "最高人民法院关于适用涉外民事关系法律适用法若干问题的解释（二） > 专家证人质证规则",
        "language_mode": "bilingual",
        "lang_original": "zh",
        "text_original": "当事人对域外法的内容及其理解与适用有争议的，可以聘请域外法专家出具法律意见书或者申请专家出庭接受质询。人民法院应当组织当事人对域外法律专家意见进行质证。",
        "text_en": "Parties may retain foreign legal experts to provide opinions or testify in court; courts shall organize cross-examination on expert reports.",
        "text_zh": "【域外法律专家证人质证与法律意见采信审查】：各方对东盟法条理解存在分歧的，可申请外法专家（如新加坡大律师、印尼宣誓执业律师）出庭接受质证。法庭重点审查专家执业资历、利益关联性及援引判例的权威性。【实务启示】：中国法院涉外审判新标杆！重大涉外基建争议必须聘请目标国顶级大律师出具 Expert Legal Opinion，在庭审对抗中彻底击溃对手的片面法条解读！",
        "norm_category": "crossborder_litigation",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_cn_fla8_expert_qualification", "text_zh": "要件一：出庭专家具备东道国合法执业资格或顶尖法学法典研究资历", "status": "condition_precedent"},
            {"eid": "e_cn_fla8_cross_examination", "text_zh": "要件二：就法条原意、司法判例前例及实务演变在庭审中接受充分对质", "status": "mandatory"},
            {"eid": "e_cn_fla8_judicial_reliance", "text_zh": "法律后果：法庭依法采信专家报告作为认定案件事实与法律后果之依据", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "CN:Data_Security_Law:Art36_Crossborder_Data",
        "law": "CN:Data_Security_Law",
        "enbez": "Art 36",
        "title": "中华人民共和国数据安全法第三十六条：向境外司法仲裁机构提供境内数据前置审批",
        "heading_path": "中华人民共和国数据安全法 > 第五章 数据安全保护义务 > 涉外数据司法调取限制",
        "language_mode": "bilingual",
        "lang_original": "zh",
        "text_original": "非经中华人民共和国主管机关批准，境内的组织、个人不得向外国司法或者执法机构提供存储于中华人民共和国境内的数据。",
        "text_en": "Without prior approval from PRC competent authorities, no organization or individual may provide data stored within PRC to foreign judicial or law enforcement authorities.",
        "text_zh": "【向境外司法仲裁提供境内工程数据前置审批红线】：未经中国主管机关正式批准，任何企业不得向境外司法或仲裁机构提供存储于境内的财务账册、技术图纸、商业往来等电子数据！违者处以最高500万元罚款并责令停业整顿！【实务启示】：央企海外诉讼合规底线！在新加坡高院进行普通法“证据开示（Discovery）”时，涉及中国境内服务器的项目往来邮件与设计文件，必须先报司法部及行业主管部委审批！",
        "norm_category": "crossborder_litigation",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_cn_dsl36_stored_in_china", "text_zh": "要件一：涉案核心工程财务数据与通信记录物理存储于中国境内服务器", "status": "condition_precedent"},
            {"eid": "e_cn_dsl36_foreign_order", "text_zh": "要件二：境外法院或仲裁庭签发强行证据出示令或调查令（Subpoena）", "status": "mandatory"},
            {"eid": "e_cn_dsl36_approval_barrier", "text_zh": "法律后果：未经国家部委审批严禁私自出境，对外依法享有强行法免于出示抗辩", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "CN:Sinosure_Policy:Clause_30_Notice",
        "law": "CN:Sinosure_Policy",
        "enbez": "Clause 30",
        "title": "中国信保海外投资保险通用条款第三十条：出险后30日内书面通知前置要件",
        "heading_path": "中国出口信用保险公司海外投资保险条款 > 第七章 索赔与理赔 > 险情通报时限",
        "language_mode": "bilingual",
        "lang_original": "zh",
        "text_original": "被保险人知道或应当知道发生可能导致本保单项下损失的政治风险、政府征收、汇兑限制或合同违约事件之日起，必须在30日内向保险人（中国信保）发出正式书面险情通报；逾期未通报致使保险人无法采取减损措施的，保险人有权拒赔。",
        "text_en": "Insured must formally notify Sinosure in writing within 30 days of becoming aware of political risk, expropriation, or breach, or forfeit claim.",
        "text_zh": "【中国信保30日法定险情报告与索赔权保全】：出海央企获知东道国政府征收、外汇限制、内战暴乱或项目业主重大违约后，必须在30个日历天内向中国信保递交书面险情通知；逾期未报导致损失扩大的，信保依法享有全额或部分拒赔权！【出海实务】：央企海外特许权遭遇东道国政府毁约时，必须立即启动“信保30天双轨报案机制”，绝不可因私下与业主协商而错过报案窗口！",
        "norm_category": "crossborder_litigation",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_sinosure30_risk_event", "text_zh": "要件一：东道国发生政变、汇兑管制、行政征收或业主恶意毁约险情", "status": "condition_precedent"},
            {"eid": "e_sinosure30_30days_deadline", "text_zh": "要件二：在知道或应当知道险情之日起 30 日内正式呈递书面出险报案书", "status": "mandatory"},
            {"eid": "e_sinosure30_indemnity_right", "text_zh": "法律后果：锁定理赔权益，触发信保代位追偿与国家主权间外交照会支持", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "CN:SASAC_Order_35:Art25_Post_Investment_Risk",
        "law": "CN:SASAC_Order_35",
        "enbez": "Art 25",
        "title": "国资委35号令第二十五条：境外投资重大项目全过程跟踪与投后风险预警",
        "heading_path": "中央企业境外投资监督管理办法 (国资委令第35号) > 第四章 境外投资项目实施与监督 > 投后跟踪评估",
        "language_mode": "bilingual",
        "lang_original": "zh",
        "text_original": "中央企业应当对实施中的重大境外投资项目开展全过程跟踪管理，组织开展投后评价。对投资金额大、发生重大安全事故、严重亏损或者受到所在国重大司法调查的境外项目，中央企业应当及时向国资委报告并采取有效处置措施。",
        "text_en": "Central SOEs shall conduct whole-process overseas tracking and post-investment evaluation, reporting major losses or foreign judicial investigations to SASAC.",
        "text_zh": "【国资委重大境外投资全过程跟踪与司法调查即时报告红线】：央企境外重大工程发生超过投资总额20%的严重亏损、遭遇东道国重大司法诉讼或反腐败调查时，必须在第一时间向国资委呈报风险处置方案，严禁瞒报拖报！【实务启示】：项目部法务合规必须设立即时风险报告台账，遭遇东盟国家高院立案或停工令，必须同步启动集团总部及国资委报备！",
        "norm_category": "outbound_investment",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_sasac35_art25_major_loss", "text_zh": "要件一：境外项目面临严重超期超支、特许权被收回或外国司法调查", "status": "condition_precedent"},
            {"eid": "e_sasac35_art25_emergency_filing", "text_zh": "要件二：向企业总部风险委员会及国务院国资委提交专项处置应急预案", "status": "mandatory"},
            {"eid": "e_sasac35_art25_accountability", "text_zh": "法律后果：合规免责保护；反之若瞒报虚报直接追究项目主要负责人领导责任", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "CN:Anti_Foreign_Sanctions_Law:Art6_Countermeasures",
        "law": "CN:Anti_Foreign_Sanctions_Law",
        "enbez": "Art 6",
        "title": "反外国制裁法第六条：查封扣押冻结制裁主体境内财产之反制措施",
        "heading_path": "中华人民共和国反外国制裁法 > 反制措施体系与司法执行",
        "language_mode": "bilingual",
        "lang_original": "zh",
        "text_original": "国务院相应部门可以决定采取下列一种或者几种反制措施：（一）不予签发签证、不准入境；（二）查封、扣押、冻结在我国境内的动产、不动产和其他各类财产；（三）禁止或者限制我国境内的组织、个人与其进行有关交易、合作等活动；（四）其他必要措施。",
        "text_en": "Competent departments may order freezing, seizing assets in China of entities involved in discriminatory foreign sanctions.",
        "text_zh": "【反外国制裁查封冻结财产与境内阻断】：外国国家基于长臂管辖对中国央企实施制裁的，国家有权直接查封、扣押、冻结该外国企业在中国境内的银行账户、股权及不动产！【实务启示】：涉外跨国诉讼的战略威慑武器！外资业主若配合外国歧视性限制撕毁中资合同，中资企业可申请司法反制，查封其在华合资公司财产！",
        "norm_category": "crossborder_litigation",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_afsl6_foreign_sanction_order", "text_zh": "要件一：外国实体或金融机构执行针对中资企业的非法外国制裁措施", "status": "condition_precedent"},
            {"eid": "e_afsl6_in_china_assets", "text_zh": "要件二：被反制对象在中国境内拥有银行存款、股权或合资合作资产", "status": "mandatory"},
            {"eid": "e_afsl6_seizure_freezing", "text_zh": "法律后果：国务院部门依法签发冻结禁令，中国法院强制执行查封保全", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "CN:MOFCOM_Security_Review_2011:Art5_Scope",
        "law": "CN:MOFCOM_Security_Review_2011",
        "enbez": "Art 5",
        "title": "商务部外资并购安全审查规定第五条：关键基础设施与实质控制权审查",
        "heading_path": "商务部实施外国投资者并购境内企业安全审查制度的规定 > 审查范围与控制权界定",
        "language_mode": "bilingual",
        "lang_original": "zh",
        "text_original": "对外国投资者并购境内企业，应从交易的实质内容和实际影响来判断是否属于安全审查范围；外国投资者不得以代持、信托、多层次再投资、租赁、质押或者协议控制（VIE）等任何方式实质规避国家安全审查。",
        "text_en": "Substance-over-form test applies to national security review; foreign investors cannot bypass review via nominee, trust, or contractual arrangements.",
        "text_zh": "【国家安全审查穿透式实质审查与协议代持穿透】：外国投资者并购涉及交通基建、关键能源装备企业的，必须进行国家安全审查；严禁通过股权代持、离岸信托或协议控制（VIE）等方式规避安审！【实务启示】：中国审查标准对外资交易具有穿透效力，在东盟境内合资反向并购时具有参照合规意义！",
        "norm_category": "outbound_investment",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_mofcom_nsr5_substance_over_form", "text_zh": "要件一：并购标的涉及关键能源港口交通基建或国防核心产业链", "status": "condition_precedent"},
            {"eid": "e_mofcom_nsr5_evasion_structure", "text_zh": "要件二：通过多层嵌套或名义代持架构实质规避国家监管部门审查", "status": "mandatory"},
            {"eid": "e_mofcom_nsr5_unwinding_order", "text_zh": "法律后果：交易自始无效，主管部委责令限期转让股权并剥离核心资产", "status": "prohibition"}
        ], ensure_ascii=False)
    }
]

PHASE2_MULTI_SUPPLEMENTS = [
    {
        "table": "reference_norms",
        "norm_id": "TREATY:New_York_1958:Art_V_Non_Enforcement",
        "law": "TREATY:New_York_1958",
        "enbez": "Art V",
        "title": "1958年纽约公约第五条：拒绝承认与执行外国仲裁裁决的7大排他性法定事由",
        "heading_path": "承认及执行外国仲裁裁决公约 (New York Convention 1958) > 第5条 拒绝执行事由",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Recognition and enforcement of the award may be refused only if: (a) parties were under incapacity or agreement invalid; (b) lack of proper notice or unable to present case; (c) award deals with dispute not contemplated by submission; (d) arbitral authority or procedure not in accordance with agreement; (e) award has not yet become binding or has been set aside; or if the court finds: (i) subject matter not arbitrable, or (ii) contrary to public policy.",
        "text_en": "Enforcement of foreign arbitral awards may be refused strictly and exclusively on the 7 grounds under Art V, including lack of due process, excess of jurisdiction, and public policy.",
        "text_zh": "【纽约公约7大排他性拒绝执行抗辩事由】：被申请执行人仅在证明存在以下情形时法院方可拒绝执行：① 仲裁协议当事人无行为能力或协议无效；② 未获仲裁员指定通知或未能申辩（正当程序瑕疵）；③ 裁决越权或超裁；④ 仲裁庭组成或程序违背约定；⑤ 裁决已被撤销或尚未发生约束力；以及法院依职权认定：⑥ 争议不具备可仲裁性；⑦ 执行违背东道国公共政策（Public Policy）。【实务启示】：国际工程仲裁裁决在东盟落地执行的核心攻防准则！东道国法院对实体裁决无权进行实质重新审理，中资企业可依此条全力推进域外裁决落地清偿！",
        "norm_category": "international_treaty",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_nyc5_exhaustive_grounds", "text_zh": "要件一：被执行方负有证明符合第五条第1款五项程序抗辩事由之绝对举证责任", "status": "condition_precedent"},
            {"eid": "e_nyc5_public_policy_threshold", "text_zh": "要件二：法官依职权审查仅限基本公共道德、主权秩序与不可仲裁性红线", "status": "mandatory"},
            {"eid": "e_nyc5_pro_enforcement_bias", "text_zh": "法律后果：恪守有利于执行（Pro-Enforcement）原则，严禁进行实体重新审理", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "TREATY:ICSID_1965:Art_52_Annulment",
        "law": "TREATY:ICSID_1965",
        "enbez": "Art 52",
        "title": "华盛顿公约第五十二条：ICSID 国际投资裁决特别撤销程序5大事由",
        "heading_path": "解决国家与他国国民间投资争端公约 (ICSID Convention 1965) > 第五章 裁决的解释、修改和撤销 > 第52条 撤销程序",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Either party may request annulment of the award by an application in writing addressed to the Secretary-General on one or more of the following grounds: (a) that the Tribunal was not properly constituted; (b) that the Tribunal has manifestly exceeded its powers; (c) that there was corruption on the part of a member of the Tribunal; (d) that there has been a serious departure from a fundamental rule of procedure; or (e) that the award has failed to state the reasons on which it is based.",
        "text_en": "Either party may apply for annulment of ICSID award strictly on 5 grounds: improper constitution, manifest excess of powers, corruption, serious procedural breach, or failure to state reasons.",
        "text_zh": "【ICSID 裁决特别撤销委员会5大排他事由】：任何一方可在收到裁决后120天内申请设立专责委员会（Ad Hoc Committee）撤销裁决，仅限5项事由：① 仲裁庭组成不当；② 仲裁庭显然超越其权限；③ 仲裁员有受贿等腐败行为；④ 严重背离基本程序规则；⑤ 裁决未陈述其所依据的理由。【实务启示】：东道国政府败诉后常利用第52条发起撤销程序阻延执行。中资企业在起诉东道国政府前必须确保仲裁请求严格限定于条约授权范围，防范被‘超越权限’撤销！",
        "norm_category": "international_treaty",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_icsid52_120days_deadline", "text_zh": "要件一：在正式裁决书送达当日起 120 个日历天内向秘书长正式递交申请", "status": "condition_precedent"},
            {"eid": "e_icsid52_manifest_excess", "text_zh": "要件二：证明仲裁庭错误适用准据法或越权管辖达到‘显而易见’的严重程度", "status": "mandatory"},
            {"eid": "e_icsid52_annulment_finality", "text_zh": "法律后果：专责委员会仅有权决定全部或部分撤销裁决，无权自为替代判决", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "TREATY:ICSID_1965:Art_54_Enforcement",
        "law": "TREATY:ICSID_1965",
        "enbez": "Art 54",
        "title": "华盛顿公约第五十四条：缔约国强制将 ICSID 裁决视为本国终审判决执行",
        "heading_path": "解决国家与他国国民间投资争端公约 (ICSID Convention 1965) > 第六章 裁决的承认和执行 > 第54条 执行义务",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Each Contracting State shall recognize an award rendered pursuant to this Convention as binding and enforce the pecuniary obligations imposed by that award within its territories as if it were a final judgment of a court in that State.",
        "text_en": "Each Contracting State must enforce the pecuniary obligations of an ICSID award as if it were a final judgment of its highest domestic court.",
        "text_zh": "【ICSID 裁决等同缔约国国内法院终审判决强制执行】：每一个公约缔约国（包括印尼、大马、新加坡、菲律宾等）必须承认 ICSID 裁决具有约束力，并在其领土内将裁决确定的金钱给付义务‘视同该国本国法院的终审判决’予以强制执行！东道国法院严禁以‘公共政策’为由拒绝执行！【出海实务】：中资企业对东道国政府发起 ISDS 仲裁的最大后盾！一旦获得 ICSID 胜诉金钱裁决，可直接在全球160多个缔约国查封东道国海外非外交商业资产！",
        "norm_category": "international_treaty",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_icsid54_certified_award", "text_zh": "要件一：向执行地主管法院提交由 ICSID 秘书长核证的真实裁决副本", "status": "condition_precedent"},
            {"eid": "e_icsid54_pecuniary_obligation", "text_zh": "要件二：执行申请标的属于裁决书判令东道国支付的金钱债务及利息", "status": "mandatory"},
            {"eid": "e_icsid54_automatic_domestic_force", "text_zh": "法律后果：免除一切实质审查与公共政策抗辩，直接转化为本国执行令强执", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "TREATY:CAFTA_2009:Art_4_National_Treatment",
        "law": "TREATY:CAFTA_2009",
        "enbez": "Art 4",
        "title": "中国-东盟自贸区投资协议第四条：国民待遇及实质平等待遇",
        "heading_path": "中国-东盟全面经济合作框架协议投资协议 (CAFTA 2009) > 第4条 国民待遇",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "National Treatment: Each Party shall accord to investors of any other Party, and to covered investments, in like circumstances, treatment no less favourable than that it accords to its own investors and their investments with respect to the admission, establishment, acquisition, management, conduct, operation and sale.",
        "text_en": "Parties shall accord National Treatment to covered investors and investments in like circumstances regarding operation and disposition.",
        "text_zh": "【中国-东盟自贸区投资国民待遇原则】：东盟各成员国在同等情形下，给予中国投资者及其投资的待遇，不得低于给予其本国投资者及其投资的待遇（涵盖设立、收购、经营、管理及处分全流程）。【实务启示】：东盟国家若在政府采购、施工许可证颁发或电网并网优先权上对本地企业优待而歧视中资企业，直接违反 CAFTA 国民待遇义务！",
        "norm_category": "international_treaty",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_cafta4_like_circumstances", "text_zh": "要件一：中资企业与东道国本土承包企业在同一经济部门或工程领域开展作业", "status": "condition_precedent"},
            {"eid": "e_cafta4_discriminatory_burden", "text_zh": "要件二：东道国政策设立了仅针对外资的歧视性准入壁垒或运营苛捐杂税", "status": "mandatory"},
            {"eid": "e_cafta4_state_treaty_breach", "text_zh": "法律后果：认定东道国违反 CAFTA 国际公法义务并触发政府间磋商与赔偿", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "TREATY:CAFTA_2009:Art_7_FET",
        "law": "TREATY:CAFTA_2009",
        "enbez": "Art 7",
        "title": "中国-东盟自贸区投资协议第七条：公平与公正待遇标准及最低国际法保护底线",
        "heading_path": "中国-东盟全面经济合作框架协议投资协议 (CAFTA 2009) > 第7条 投资待遇 (FET)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Each Party shall accord to covered investments fair and equitable treatment and full protection and security. For greater certainty, fair and equitable treatment includes the obligation not to deny justice in criminal, civil or administrative adjudicatory proceedings in accordance with due process of law.",
        "text_en": "Host parties must accord fair and equitable treatment and full protection and security, strictly prohibiting denial of justice in judicial proceedings.",
        "text_zh": "【CAFTA公平公正待遇与禁止司法拒绝原则】：缔约各方必须给予中资受保护投资公正与公平的待遇以及充分保护与安全；包括不得在刑事、民事或行政审判程序中依正当法律程序拒绝司法（Denial of Justice）！【实务启示】：海外诉讼遭到东道国法院恶意久拖不决、明显司法偏袒或地方保护裁定撤销合法仲裁裁决时，中资企业可依此款直诉东道国政府承担国家责任！",
        "norm_category": "international_treaty",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_cafta7_denial_of_justice", "text_zh": "要件一：东道国司法或行政救济途径存在恶意阻碍、程序违法或荒谬裁判", "status": "condition_precedent"},
            {"eid": "e_cafta7_exhaustion_or_futility", "text_zh": "要件二：当事人已穷尽当地合理救济途径或举证证明救济显然无望徒劳", "status": "mandatory"},
            {"eid": "e_cafta7_international_liability", "text_zh": "法律后果：触发国际公法上的国家责任，判决东道国全额赔偿中资投资损失", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "TREATY:ACIA_2009:Art_19_Denial_of_Benefits",
        "law": "TREATY:ACIA_2009",
        "enbez": "Art 19",
        "title": "东盟全面投资协定第十九条：无实质商业活动的空壳公司利益拒绝条款",
        "heading_path": "东盟全面投资协定 (ACIA 2009) > 第19条 利益的拒绝 (Denial of Benefits)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Denial of Benefits: A Member State may deny the benefits of this Agreement to an investor of another Member State that is an enterprise of such other Member State and to investments of that investor if the enterprise is owned or controlled by persons of a non-Member State and has no substantial business activities in the territory of any Member State.",
        "text_en": "Member State may deny treaty benefits if the investing company is owned by non-ASEAN entities and lacks substantial business operations in ASEAN.",
        "text_zh": "【东盟利益拒绝条款与第三国空壳持股穿透审查】：东盟成员国（如印尼、泰国）有权拒绝给予某投资者协定利益，如果该企业虽然注册在东盟另一成员国（如新加坡 SPV），但实际上由非成员国（如中国母公司）控制且在注册地‘没有实质性商业活动（No Substantial Business Activities）’！【实务启示】：架构合规关键！中资企业借道新加坡设立控股平台转投印尼/越南时，新加坡公司必须配备常驻董事、本地办公场所并实际报税，杜绝‘无员工空壳’被直接剥夺条约保护权！",
        "norm_category": "international_treaty",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_acia19_shell_company", "text_zh": "要件一：投资主体虽具有东盟某国注册形态但属于零雇员零资产的过桥通道公司", "status": "condition_precedent"},
            {"eid": "e_acia19_ultimate_beneficial_owner", "text_zh": "要件二：东道国启动穿透审查认定其实际控制人属于非协定缔约第三方", "status": "mandatory"},
            {"eid": "e_acia19_strip_benefits", "text_zh": "法律后果：东道国合法行使利益拒绝权，剥夺其启动国际投资仲裁之条约管辖权", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "TREATY:ACIA_2009:Art_14_Expropriation",
        "law": "TREATY:ACIA_2009",
        "enbez": "Art 14",
        "title": "东盟全面投资协定第十四条：直接征收、间接征收认定与迅速有效补偿",
        "heading_path": "东盟全面投资协定 (ACIA 2009) > 第14条 征收与补偿",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "A Member State shall not expropriate or nationalise covered investments except for a public purpose, in a non-discriminatory manner, on payment of prompt, adequate and effective compensation, and in accordance with due process of law. Compensation shall be equivalent to the fair market value of the expropriated investment.",
        "text_en": "Expropriation prohibited unless for public purpose, non-discriminatory, under due process, and with prompt, adequate, effective fair market value compensation.",
        "text_zh": "【ACIA迅速、充分、有效补偿标准与间接征收认定】：东盟成员国严禁直接或间接征收受保护投资，除非满足公共目的、非歧视、正当法律程序并支付‘迅速、充分、有效（Prompt, Adequate and Effective）’的补偿。补偿额必须等于征收发生前的公允市场价值（Fair Market Value），并计入合理商业利息。【实务启示】：东道国通过恶意变更环保标准或撤销税收减免导致项目公司彻底丧失经济价值的，构成‘间接征收（Indirect Expropriation）’，总承包商可索赔公允市值！",
        "norm_category": "international_treaty",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_acia14_deprivation_of_economic_value", "text_zh": "要件一：政府监管行为实质性彻底摧毁了投资项目的核心经济收益与商业营运能力", "status": "condition_precedent"},
            {"eid": "e_acia14_fair_market_value", "text_zh": "要件二：由独立国际评估机构按照贴现现金流法（DCF）评定项目公允市值", "status": "mandatory"},
            {"eid": "e_acia14_hull_formula", "text_zh": "法律后果：适用赫尔公式判决赔偿，补偿款无任何汇兑障碍即可自由汇出", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "RCEP:2020:Art_10_4_FET",
        "law": "RCEP:2020",
        "enbez": "Art 10.4",
        "title": "RCEP投资章第10.4条：最低待遇标准与充分保护和安全",
        "heading_path": "区域全面经济伙伴关系协定 (RCEP 2020) > 第10章 投资 > 第10.4条 投资待遇标准",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Standard of Treatment: Each Party shall accord to covered investments fair and equitable treatment and full protection and security in accordance with customary international law, including the police protection required by international law.",
        "text_en": "Each Party shall accord fair and equitable treatment and full protection and security under customary international law, including police protection.",
        "text_zh": "【RCEP最低国际法待遇与警察保护义务】：各缔约方应依照习惯国际法给予受保护投资公平公正待遇及充分保护和安全（Full Protection and Security, FPS）。东道国负有采取合理必要治安与执法措施保护中资工程现场免遭暴徒破坏、非法冲击与打砸抢之法定义务！【出海实务】：海外施工遭遇当地社区恶意阻工、聚众围堵项目部而属地警方放任不管时，中资总包可直接认定东道国违反 FPS 警察保护义务，诉请国家公法赔偿！",
        "norm_category": "international_treaty",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_rcep104_physical_attack", "text_zh": "要件一：施工现场遭遇外部群体暴力冲击、设备毁损或人员人身安全威胁", "status": "condition_precedent"},
            {"eid": "e_rcep104_police_inaction", "text_zh": "要件二：正式向东道国警方报警求助而当局消极怠工或故意放任损害发生", "status": "mandatory"},
            {"eid": "e_rcep104_fps_state_liability", "text_zh": "法律后果：认定东道国违反国际法充分保护和安全义务，承担财产重置赔偿", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "RCEP:2020:Art_10_13_Transfers",
        "law": "RCEP:2020",
        "enbez": "Art 10.13",
        "title": "RCEP第10.13条：资金、利润与清算资产跨境无迟延自由转移保障",
        "heading_path": "区域全面经济伙伴关系协定 (RCEP 2020) > 第10章 投资 > 第10.13条 转移",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Transfers: Each Party shall permit all transfers relating to a covered investment to be made freely and without delay into and out of its territory. Such transfers include: (a) contributions to capital; (b) profits, dividends, interest, capital gains; (c) payments made under a contract, including loan agreements; (d) proceeds from sale or liquidation.",
        "text_en": "Parties shall permit capital, dividends, contract payments, and liquidation proceeds to be transferred freely and without delay at market exchange rate.",
        "text_zh": "【RCEP跨境资金与利润自由汇出条约保障】：各缔约方必须允许与投资相关的一切资金转移自由且无迟延地进出其领土，包括：股息、红利、特许权使用费、工程承包合同价款、以及清算收益；且应以转移时的公允市场汇率进行兑换。【实务启示】：打破东盟个别国家（如印尼外汇强制留存 DHE、老挝/缅甸外汇锁死）的国际法盾牌！央企可援引 RCEP 排除东道国央行针对正当工程款出境的非合理行政外汇管制！",
        "norm_category": "international_treaty",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_rcep1013_legitimate_funds", "text_zh": "要件一：拟出境资金属于工程结算盈余、分红利润或依法清算分配款", "status": "condition_precedent"},
            {"eid": "e_rcep1013_arbitrary_forex_control", "text_zh": "要件二：东道国银行或外汇管理局无合法抗辩由实施长达数月的购汇汇出限制", "status": "mandatory"},
            {"eid": "e_rcep1013_free_transfer_mandate", "text_zh": "法律后果：东道国行为构成条约违约，责令立即放行资金并赔偿汇率波动损失", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "ICC:URDG_758:Art_15_Requirements_for_Demand",
        "law": "ICC:URDG_758",
        "enbez": "Art 15",
        "title": "见索即付保函统一规则第15条：索赔书单据符合性严格表面审查",
        "heading_path": "国际商会见索即付保函统一规则 (URDG 758) > 第15条 索赔要求",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Requirements for Demand: A demand under the guarantee shall be supported by such other documents as the guarantee specifies, and in any event by a statement by the beneficiary indicating in what respect the applicant is in breach of its obligations under the underlying relationship.",
        "text_en": "Demand must strictly comply with guarantee terms and state in what respect the applicant breached its obligations.",
        "text_zh": "【见索即付保函索赔书严格单据相符要件】：受益人（雇主）提交的索赔通知，必须附带保函明文规定的全部单据；且在任何情形下，索赔书必须包含‘明确陈述被保证人（承包商）在基础合同项下究竟在何种具体方面违约’的违约声明！【出海实务】：阻截业主恶意索兑的黄金关卡！海外业主若仅发出一纸‘请立即付款’的空白索赔函而未载明具体违约事由，开证行依法必须拒付！中资法务可即刻在境内外法院申请紧急止付禁令！",
        "norm_category": "international_treaty",
        "mandatory_level": "contract_default",
        "elements_json": json.dumps([
            {"eid": "e_urdg15_specific_breach_statement", "text_zh": "要件一：受益人索赔文书中必须包含明确指出违约款项与违约事实的具体声明", "status": "condition_precedent"},
            {"eid": "e_urdg15_strict_compliance", "text_zh": "要件二：索赔单据的签发人、签署形态及日期与保函约定做到严格‘单函一致’", "status": "mandatory"},
            {"eid": "e_urdg15_rejection_of_demand", "text_zh": "法律后果：任何微小不符即构成不符点，担保行有权且必须依法拒绝付款", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "ICC:URDG_758:Art_20_Partial_Demand",
        "law": "ICC:URDG_758",
        "enbez": "Art 20",
        "title": "见索即付保函统一规则第20条：部分索兑与多次索兑有效性",
        "heading_path": "国际商会见索即付保函统一规则 (URDG 758) > 第20条 部分索赔和多次索赔",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Partial Demand and Multiple Demands: A demand may be made for less than the full amount available under the guarantee (partial demand). More than one demand may be made (multiple demands). The phrase 'multiple demands prohibited' or similar means that only one demand may be made.",
        "text_en": "Partial demands and multiple demands are permitted unless explicitly excluded by the phrase 'multiple demands prohibited'.",
        "text_zh": "【保函部分索兑与分步承付规则】：受益人可以就低于保函有效金额的款项提出索赔（部分索赔），且可以提出多次索赔；除非保函明文注明‘禁止多次索赔’。【实务启示】：合同谈判防守绝招！中资总包开具大额预付款或履约保函时，应在保函特别条款中加注‘Multiple demands prohibited（禁止多次索赔）’或‘Partial demand prohibited’，迫使业主只能单次行权，极大提高其索兑顾虑与违约成本！",
        "norm_category": "international_treaty",
        "mandatory_level": "contract_default",
        "elements_json": json.dumps([
            {"eid": "e_urdg20_partial_amount", "text_zh": "要件一：受益人根据基础合同当前实际争议金额仅主张部分保函份额", "status": "condition_precedent"},
            {"eid": "e_urdg20_no_prohibition_clause", "text_zh": "要件二：保函正文中未包含明确排除多次或部分索兑的限制性特别约定", "status": "mandatory"},
            {"eid": "e_urdg20_balance_retention", "text_zh": "法律后果：开证行就主张部分承付，保函剩余有效额度继续对后续履约保持担保效力", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "MDB:Sanctions:Fraud_and_Corruption_Guidelines",
        "law": "MDB:Sanctions",
        "enbez": "Guidelines",
        "title": "世界银行多边金融机构制裁守则：欺诈、腐败、串标与妨碍调查认定",
        "heading_path": "世界银行防止和打击欺诈与腐败准则 (World Bank Sanctions Guidelines) > 制裁违规行为定义",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Sanctionable Practices include: Corrupt Practice (offering anything of value to influence an official); Fraudulent Practice (misrepresentation or omission of facts to mislead); Collusive Practice (arrangement between bidders to establish artificial prices); Coercive Practice; and Obstructive Practice (deliberately destroying evidence or threatening witnesses).",
        "text_en": "Sanctionable practices include corrupt, fraudulent, collusive, coercive, and obstructive practices, leading to debarment across all multilateral development banks.",
        "text_zh": "【世行5大可制裁违规行为界定与合规穿透】：世行、亚行等五大多边金融机构对以下5类行为实施跨行联合除名（Cross-Debarment）：① 腐败行为（向官员行贿）；② 欺诈行为（在投标文件或履约报告中隐瞒或虚构业绩/财务数据）；③ 串标行为（多家中资投标前达成价格协议）；④ 胁迫行为；⑤ 妨碍调查行为（删除邮件、销毁账册或拒绝世行廉政局 INT 调查询问）。【实务启示】：海外工程投标合规最高压线！一旦被认定欺诈，企业将面临全球数年联合禁标，海外市场面临系统性瘫痪风险！",
        "norm_category": "international_treaty",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_mdb_guidelines_knowing_misrep", "text_zh": "要件一：在资格预审或投标书中故意提供虚假业绩合同或人员资质证书", "status": "condition_precedent"},
            {"eid": "e_mdb_guidelines_material_influence", "text_zh": "要件二：该虚假陈述对评标委员会授标决策产生了实质性诱导影响", "status": "mandatory"},
            {"eid": "e_mdb_guidelines_global_debarment", "text_zh": "法律后果：触发世行等五大行全球黑名单联合除名制裁（Cross-Debarment）", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "UNCITRAL:Model_Law_1985:Art_34_Setting_Aside",
        "law": "UNCITRAL:Model_Law_1985",
        "enbez": "Art 34",
        "title": "联合国国际商事仲裁示范法第34条：申请撤销仲裁裁决的排他性法定事由",
        "heading_path": "联合国国际贸易法委员会国际商事仲裁示范法 (UNCITRAL Model Law) > 第七章 对裁决的抗辩 > 第34条 撤销裁决申请",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Application for setting aside: Recourse to a court against an arbitral award may be made only by an application for setting aside strictly within 3 months of receipt of award, on limited grounds: invalid arbitration agreement, violation of natural justice, ultra vires, improper tribunal composition, non-arbitrability, or violation of public policy.",
        "text_en": "Application for setting aside arbitral award must be made within 3 months exclusively on grounds of invalidity, natural justice, excess of jurisdiction, or public policy.",
        "text_zh": "【联合国仲裁示范法3个月撤裁除斥期与撤裁事由排他性】：向法院申请撤销仲裁裁决是针对裁决的唯一司法救济途径；必须在收到裁决书之日起3个月内提出，且仅限以下事由：① 仲裁协议无效；② 违反自然公正法则（未获通知或无法陈述）；③ 超裁；④ 仲裁庭组成违背约定；⑤ 争议不具备可仲裁性；⑥ 违背仲裁地公共政策。【实务启示】：新加坡法（IAA）与马来西亚法（Arbitration Act）均全盘吸收本条！3个月除斥期一旦逾期，撤裁权利终局消灭！",
        "norm_category": "international_treaty",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_ml34_three_months_strict", "text_zh": "要件一：在收到终局仲裁裁决书当日起严格 3 个月内向仲裁地高院立案", "status": "condition_precedent"},
            {"eid": "e_ml34_natural_justice_breach", "text_zh": "要件二：举证证明仲裁庭拒绝审阅核心抗辩证据导致实质性程序不公", "status": "mandatory"},
            {"eid": "e_ml34_exclusive_recourse", "text_zh": "法律后果：法院判决撤销或发回重新仲裁，且法院严禁对案件事实实体改判", "status": "prohibition"}
        ], ensure_ascii=False)
    }
]

# 补充 3 条判例专属引用的成文法条，杜绝悬空边
PHASE2_STATUTE_PATCHES = [
    {
        "table": "norms",
        "norm_id": "PH:Civil_Code:Art1713",
        "law": "PH:Civil_Code",
        "enbez": "Art 1713",
        "title": "菲律宾民法典第1713条：承揽合同与工程施工合同法定定义",
        "heading_path": "菲律宾民法典 (Civil Code RA 386) > 第四卷 债务与合同 > 承揽与建筑工程专章",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "By the contract for a piece of work the contractor binds himself to execute a piece of work for the employer, in consideration of a certain price or compensation. The contractor may either employ only his labor or skill, or also furnish the material.",
        "text_en": "In a contract for a piece of work, contractor binds himself to execute work for employer for a price, either providing labor/skill alone or furnishing materials.",
        "text_zh": "【菲律宾工程承揽合同法定定义与包工包料性质】：在承揽工程合同中，承包商承担为雇主完成某项特定工程的法律义务，雇主支付约定价款或对价。承包商可以仅提供劳务与技能，亦可包工包料同时提供建筑材料。【实务启示】：菲律宾境内所有 EPC 及分包合同的民商法母法底座，确立固定总价与包工包料下的严格履约交付基准！",
        "norm_category": "construction_dispute",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_ph1713_valid_consent", "text_zh": "要件一：双方就工程施工范围与对价报酬达成真实一致的意思表示", "status": "condition_precedent"},
            {"eid": "e_ph1713_contractor_undertaking", "text_zh": "要件二：总包商承担包工包料或专业技能施工之终局交付责任", "status": "mandatory"},
            {"eid": "e_ph1713_binding_contract", "text_zh": "法律后果：确立承揽合同法律关系，受菲律宾民法典承揽专章严格规制", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "TH:CCC:Sec215",
        "law": "TH:CCC",
        "enbez": "Sec 215",
        "title": "泰国民商法典第215条：债务人不履行或未按本旨履行债务之损害赔偿责任",
        "heading_path": "泰国民商法典 (Civil and Commercial Code) > 债编 > 债务不履行",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "When the debtor does not perform the obligation in accordance with the true intent and purpose of the obligation, the creditor may claim compensation for any damages arising therefrom.",
        "text_en": "When debtor fails to perform obligation in accordance with true intent, creditor may claim compensation for damages arising therefrom.",
        "text_zh": "【债务不履行与损害赔偿法定请求权基础】：债务人未能依照债务的真实意图和目的履行债务的，债权人有权要求赔偿由此产生的任何实际损害。【实务启示】：泰国合同法违约索赔通用法定请求权基础！当发包人因环评受阻迟延移交场地时，中资承包商依此条诉请业主赔偿全部窝工与延期损失！",
        "norm_category": "breach_remedy",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_th215_breach_of_obligation", "text_zh": "要件一：债务人存在违反合同明示或默示约定履行义务之客观违约行为", "status": "condition_precedent"},
            {"eid": "e_th215_actual_damages", "text_zh": "要件二：守约方因该违约行为遭受了直接经济损失或工期延误增加成本", "status": "mandatory"},
            {"eid": "e_th215_compensation_mandate", "text_zh": "法律后果：违约方依法负有赔偿受害方全部因果关系直接损失之民事责任", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "MY:Arbitration_Act_2005:Sec19H",
        "law": "MY:Arbitration_Act_2005",
        "enbez": "Sec 19H",
        "title": "马来西亚2005年仲裁法第19H条：仲裁庭临时措施与裁决的法院强制执行",
        "heading_path": "马来西亚仲裁法 (Arbitration Act 2005, Act 646) > 仲裁庭临时措施 > 第19H条 临时措施执行",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "An interim measure issued by an arbitral tribunal shall be recognised as binding and, unless otherwise provided by the arbitral tribunal, enforced upon application to the High Court, irrespective of the country in which it was issued.",
        "text_en": "Interim measures issued by an arbitral tribunal shall be recognised as binding and enforced upon application to the High Court.",
        "text_zh": "【仲裁庭临时措施与保函止付裁决高院强制执行】：仲裁庭（包括紧急仲裁员 EA）签发的临时措施命令，应被承认为具有约束力；当事人向马来西亚高等法院提出申请后，高院应予以直接强制执行！【实务启示】：中资承包商在 SIAC 或 AIAC 获得阻止大马业主恶意索兑保函的紧急仲裁裁决后，可直接依第19H条申请大马高院强制执行，阻断银行对外打款！",
        "norm_category": "crossborder_litigation",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_my19h_valid_interim_order", "text_zh": "要件一：仲裁庭或紧急仲裁员已就保全财产或维持现状签发正式书面临时裁决", "status": "condition_precedent"},
            {"eid": "e_my19h_high_court_application", "text_zh": "要件二：正式向马来西亚高等法院递交登记与强制执行仲裁临时命令申请", "status": "mandatory"},
            {"eid": "e_my19h_judicial_enforcement", "text_zh": "法律后果：高等法院赋予临时措施判决同等效力，指令银行及各方严格执行", "status": "prohibition"}
        ], ensure_ascii=False)
    }
]


PHASE2_EXTRA_TREATIES_AND_STANDARDS = [
    {
        "table": "reference_norms",
        "norm_id": "DTA:CN_MY:Art5_PE",
        "law": "DTA:CN_MY",
        "enbez": "Art 5",
        "title": "中马双边税收协定第五条：建筑工程常设机构6个月门槛",
        "heading_path": "中国-马来西亚双边避免双重征税协定 (DTA) > 第5条 常设机构",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "A building site, construction, installation or assembly project constitutes a permanent establishment only if it exists for more than 6 months.",
        "text_en": "Construction, installation or assembly project constitutes PE in Malaysia only if lasting over 6 months.",
        "text_zh": "【中马建筑安装工程常设机构6个月判定】：中国企业在马来西亚设立的建筑工地、建筑、安装或装配项目，仅在存续超过6个月时方构成在马常设机构（PE）。【实务启示】：未达6个月的技术安装和调试，依协定受保护免向马来西亚内陆税收局（LHDN）缴纳24%的公司所得税！",
        "norm_category": "tax_treaty",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_dtamy5_duration_threshold", "text_zh": "要件一：马来西亚境内工程作业或安装项目实际存续超过6个月", "status": "condition_precedent"},
            {"eid": "e_dtamy5_lhdn_compliance", "text_zh": "要件二：依法在马来西亚税局登记并按规定申报公司所得税", "status": "mandatory"},
            {"eid": "e_dtamy5_tax_protection", "text_zh": "法律后果：未满6个月免纳在岸公司税，超6个月仅对归属利润征税", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "DTA:CN_TH:Art12_Royalties",
        "law": "DTA:CN_TH",
        "enbez": "Art 12",
        "title": "中泰双边税收协定第十二条：特许权使用费预提税限制10%",
        "heading_path": "中国-泰国双边避免双重征税协定 (DTA) > 第12条 特许权使用费",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Royalties arising in Thailand and paid to a resident of China may be taxed in Thailand, but the tax so charged shall not exceed 10% of the gross amount of the royalties.",
        "text_en": "Thai withholding tax on royalties paid to Chinese resident shall not exceed 10% of gross amount.",
        "text_zh": "【中泰特许权使用费与专有技术预提所得税上限】：泰国对支付给中国居民企业的特许权使用费（含专利技术使用许可、工业商业经验传授）所征收的预提所得税，依法不得超过总额的10%（泰国国内法通常为15%）。【实务启示】：中资企业向泰国项目提供专有技术收取许可费时，出具中国税务居民证明（COR）即可锁定10%优惠税率！",
        "norm_category": "tax_treaty",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_dtath12_cor_submission", "text_zh": "要件一：向泰国税务局正式呈递经主管税务机关公证的中国税收居民身份证明", "status": "condition_precedent"},
            {"eid": "e_dtath12_genuine_technical_knowhow", "text_zh": "要件二：技术许可合同真实且对价符合国际公允独立交易定价原则", "status": "mandatory"},
            {"eid": "e_dtath12_withholding_cap", "text_zh": "法律后果：泰国支付方强制适用 10% 优惠税率扣缴，严禁适用 15% 国内法税率", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "DTA:CN_VN:Art12_Royalties",
        "law": "DTA:CN_VN",
        "enbez": "Art 12",
        "title": "中越双边税收协定第十二条：特许权使用费预提税限制10%",
        "heading_path": "中国-越南双边税收协定 (DTA) > 第12条 特许权使用费",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Royalties arising in Vietnam and paid to a resident of China may be taxed in Vietnam, but the tax so charged shall not exceed 10% of the gross amount of the royalties.",
        "text_en": "Vietnamese withholding tax on royalties paid to Chinese resident shall not exceed 10% of gross amount.",
        "text_zh": "【中越特许权使用费与技术转让预提税上限】：越南对支付给中国居民企业的特许权使用费征收的外国承包商税（FCT），依法不得超过总额的10%。【实务启示】：总包商拆分软件著作权许可与工程设计费，依协定可享受低税负通道！",
        "norm_category": "tax_treaty",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_dtavn12_valid_documentation", "text_zh": "要件一：完备提交中越DTA协定待遇申请表及中方税收居民证书", "status": "condition_precedent"},
            {"eid": "e_dtavn12_qualifying_royalties", "text_zh": "要件二：款项属于专利、商标、专有技术或技术图纸许可使用对价", "status": "mandatory"},
            {"eid": "e_dtavn12_tax_rate_cap", "text_zh": "法律后果：越南税务机关限制征税比例不得超过合同支付额的 10%", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "DTA:CN_PH:Art12_Royalties",
        "law": "DTA:CN_PH",
        "enbez": "Art 12",
        "title": "中菲双边税收协定第十二条：特许权使用费预提税限制10%",
        "heading_path": "中国-菲律宾双边避免双重征税协定 (DTA) > 第12条 特许权使用费",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Royalties arising in the Philippines and paid to a resident of China may be taxed in the Philippines, but the tax so charged shall not exceed 10% of the gross amount of the royalties.",
        "text_en": "Philippine withholding tax on royalties paid to Chinese resident shall not exceed 10% of gross amount.",
        "text_zh": "【中菲特许权使用费预提税上限】：菲律宾对支付给中国居民企业的特许权使用费征税不得超过10%（菲律宾国内法高达25%）。【实务启示】：向菲律宾国税局（BIR）提前递交税务协定优惠裁定（TTRA）申请，防止发包人全额按25%代扣！",
        "norm_category": "tax_treaty",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_dtaph12_ttra_filing", "text_zh": "要件一：向菲律宾国际税务署（ITAD）提交税收协定优惠核准申请", "status": "condition_precedent"},
            {"eid": "e_dtaph12_beneficial_ownership", "text_zh": "要件二：中国受款人属于该特许权使用费之最终受益所有人（Beneficial Owner）", "status": "mandatory"},
            {"eid": "e_dtaph12_reduced_wht", "text_zh": "法律后果：强行阻断 25% 国内高额预提税，依法减按 10% 税率征收", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "DTA:CN_SG:Art12_Royalties",
        "law": "DTA:CN_SG",
        "enbez": "Art 12",
        "title": "中新双边税收协定第十二条：特许权使用费预提税优惠限制6%",
        "heading_path": "中国-新加坡避免双重征税协定 (DTA) > 第12条 特许权使用费",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Royalties arising in a Contracting State and paid to a resident of the other Contracting State may be taxed in that other State. However, such royalties may also be taxed in the Contracting State in which they arise, but the tax so charged shall not exceed 6% of the gross amount.",
        "text_en": "Singapore withholding tax on royalties paid to Chinese resident shall not exceed 6% of gross amount.",
        "text_zh": "【中新特许权使用费6%超低优惠税率】：新加坡对支付给中国企业的特许权使用费，征收预提所得税上限仅为6%（东盟六国中最低税率！）。【实务启示】：区域研发中心与知识产权平台架构的黄金枢纽！中资央企通过新加坡技术公司向东盟各国授权技术，可大幅压低整体税负！",
        "norm_category": "tax_treaty",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_dtasg12_singapore_source", "text_zh": "要件一：特许权使用费由新加坡居民企业支付并产生于新加坡境内", "status": "condition_precedent"},
            {"eid": "e_dtasg12_valid_certificate", "text_zh": "要件二：出具中国国税局开具的中国税收居民身份合规证明", "status": "mandatory"},
            {"eid": "e_dtasg12_6_percent_cap", "text_zh": "法律后果：强制执行 6% 超低预提所得税税率，保障企业资金高效回流", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "DTA:CN_ID:Art10_Dividends",
        "law": "DTA:CN_ID",
        "enbez": "Art 10",
        "title": "中印尼双边税收协定第十条：股息预提所得税限制10%",
        "heading_path": "中国-印度尼西亚双边税收协定 (DTA) > 第10条 股息",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Dividends paid by a company which is a resident of Indonesia to a resident of China may be taxed in Indonesia, but the tax so charged shall not exceed 10% of the gross amount of the dividends.",
        "text_en": "Indonesian withholding tax on dividends paid to Chinese resident company shall not exceed 10% of gross amount.",
        "text_zh": "【中印尼股息利润分配10%预提税上限】：印尼外资项目公司（PT PMA）向中国母公司分红派息时，印尼预提税上限为10%（印尼国内法为20%）。【实务启示】：项目完工利润汇回关键！出具 DGT-1 证明并申报享受 DTA 待遇，直接为央企节省10个点的真金白银现金流！",
        "norm_category": "tax_treaty",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_dtaid10_dividend_resolution", "text_zh": "要件一：印尼子公司股东大会依法作出合法有效的利润分配派息决议", "status": "condition_precedent"},
            {"eid": "e_dtaid10_dgt1_submission", "text_zh": "要件二：按期向印尼税务局系统上传中方母公司合规 DGT-1 表格", "status": "mandatory"},
            {"eid": "e_dtaid10_reduced_withholding", "text_zh": "法律后果：印尼子公司按 10% 代扣代缴分红税，保障剩余 90% 股息全额出境", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "FIDIC:Red_1999:Clause_14.1",
        "law": "FIDIC:Red_1999",
        "enbez": "Clause 14.1",
        "title": "FIDIC红皮书第14.1款：合同价格测量核定与单价包干机制",
        "heading_path": "FIDIC 施工合同条件 (Red Book 1999) > 第14条 合同价格和付款 > 合同价格",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "The Contract Price shall be agreed or determined under Sub-Clause 12.3 and be subject to adjustments in accordance with the Contract; and the Contractor shall pay all taxes, duties and fees required to be paid by him under the Contract.",
        "text_en": "Contract Price in Red Book is determined by actual measurement under Clause 12.3 and subject to contract adjustments.",
        "text_zh": "【红皮书单价合同实际工程量复测结算基准】：红皮书下的中标合同金额仅是估算总价，最终合同价格必须依据第12.3款按照承包商实际完成的合格工程量重新测量计算并调整！【实务启示】：与银皮书‘固定总价风险自担’彻底不同！红皮书下任何土方增量、地基加深，中资施工总包均有权按实测工程量全额索要追加工程款！",
        "norm_category": "fidic_standard",
        "mandatory_level": "contract_default",
        "elements_json": json.dumps([
            {"eid": "e_fidic_r141_actual_measurement", "text_zh": "要件一：驻地监理工程师依据第12条程序对现场实际施工尺寸与方量进行联合测量", "status": "condition_precedent"},
            {"eid": "e_fidic_r141_boq_unit_rate", "text_zh": "要件二：测量合格方量与投标工程量清单（BOQ）单价相乘核算价款", "status": "mandatory"},
            {"eid": "e_fidic_r141_final_price_adjust", "text_zh": "法律后果：以实测最终金额作为合同结算总价，发包人不得以估算总价拒付", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "FIDIC:Yellow_1999:Clause_5.4",
        "law": "FIDIC:Yellow_1999",
        "enbez": "Clause 5.4",
        "title": "FIDIC黄皮书第5.4款：技术标准与东道国法律规程变动工期费用索赔",
        "heading_path": "FIDIC 生产设备和设计-建造合同条件 (Yellow Book 1999) > 第5条 设计 > 技术标准和法规",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Technical Standards and Regulations: The design, the Contractor's Documents, the execution and the completed Works shall comply with the Country's national specifications, technical standards, building, construction and environmental Laws. If changed standards come into effect in the Country after the Base Date, the Contractor shall give notice to the Engineer and shall be entitled to EOT and Cost compensation.",
        "text_en": "Contractor entitled to EOT and Cost compensation if host country technical standards or environmental regulations change after Base Date.",
        "text_zh": "【基准日后东道国技术标准与环保规程变动索赔工期与成本】：工程设计与施工必须符合东道国技术规程与环保法。若在基准日（Base Date）之后，东道国出台了新的环保排污、消防或建筑强制规范，导致设计返工或施工变更，承包商通知工程师后享有顺延工期及实际支出成本补偿之索赔权！【实务启示】：应对东盟各国‘朝令夕改’的技术法规壁垒之有力武器！基准日后的新规改建费，全额由雇主买单！",
        "norm_category": "fidic_standard",
        "mandatory_level": "contract_default",
        "elements_json": json.dumps([
            {"eid": "e_fidic_y54_post_base_date_change", "text_zh": "要件一：东道国技术监督部门在投标基准日之后正式颁布实施新的强制标准", "status": "condition_precedent"},
            {"eid": "e_fidic_y54_design_revision_incurred", "text_zh": "要件二：承包商为符合新标准被迫修改图纸、增配设备或调整工艺流程", "status": "mandatory"},
            {"eid": "e_fidic_y54_eot_and_cost", "text_zh": "法律后果：依据第13.7款调增合同价格并全额补偿设计返工导致的工期延误", "status": "prohibition"}
        ], ensure_ascii=False)
    }
]
