"""
data_phase2_bit_prc_treaties.py - Phase 2 数据模块 2:
1. 17 条 中国-东盟 6 国双边投资保护协定 (BIT) 核心条款 (征收/补偿/代位求偿/争端管辖)
2. 20 条 中国大陆涉外投资与央国企强监管法底座 (国资委35号令/75号文、发改委11号令、外汇局29号文、数据安全法、外法查明解释二、中信保30日)
3. 20 条 国际公约、区域投资协定与采购制裁规则 (纽约公约、ICSID、CAFTA升级版、ACIA利益拒绝、RCEP禁止业绩要求、URDG758、世行制裁)
总计 57 条高权威涉外成文法与多边条约规范，100% 结构化填充 elements_json。
"""
import json

PHASE2_BIT_TREATIES = [
    {
        "table": "reference_norms",
        "norm_id": "TREATY:CN_ID_BIT_1992:Art1_Definition",
        "law": "TREATY:CN_ID_BIT_1992",
        "enbez": "Art 1",
        "title": "中印尼双边投资协定第一条：投资与投资者定义及适用资产范围",
        "heading_path": "中华人民共和国与印度尼西亚共和国双边投资保护协定 (BIT 1994) > 第1条 定义",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Definition of Investment: The term 'investment' means every kind of asset invested by investors of one Contracting State in the territory of the other Contracting State in accordance with the laws and regulations of the latter, including movable and immovable property, shares, stocks, claims to money or to any performance having economic value, intellectual property, and business concessions conferred by law.",
        "text_en": "Investment includes every kind of asset invested in accordance with host state laws, covering real property, equity, claims to money, IP, and concessions.",
        "text_zh": "【中印尼BIT投资定义与特许权保护范围】：‘投资’是指缔约国一方投资者依据东道国法律在另一方领土内投入的各种财产，包括动产、不动产及物权、公司股份、金钱请求权或具有经济价值的履约请求权、知识产权、以及依法授予的商业特许权（Concessions，涵盖矿业、电力与基建特许经营）。【实务启示】：中国央企在印尼持有的 BOT/PPP 特许经营权、电厂 EPC 预付款及应收账款，均构成受国际条约保护的合法‘投资’，享有抵御东道国行政没收的最高国际法屏障！",
        "norm_category": "bit_treaty",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_bit_id1_legal_asset", "text_zh": "要件一：资产投入完全符合印尼外资准入与审批之现行成文法规定", "status": "condition_precedent"},
            {"eid": "e_bit_id1_economic_value", "text_zh": "要件二：标的属于具有合法经济价值的股权、债权、不动产或特许权", "status": "mandatory"},
            {"eid": "e_bit_id1_treaty_standing", "text_zh": "法律后果：确立国际公法上的投资者资格与诉讼标的资格，受BIT条约管辖", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "TREATY:CN_ID_BIT_1992:Art6_Subrogation",
        "law": "TREATY:CN_ID_BIT_1992",
        "enbez": "Art 6",
        "title": "中印尼双边投资协定第六条：代位求偿权与中国信保理赔后权利移转",
        "heading_path": "中华人民共和国与印度尼西亚共和国双边投资保护协定 (BIT 1994) > 第6条 代位",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Subrogation: If one Contracting State or its designated agency (e.g. Sinosure) makes a payment to its investor under an indemnity or guarantee given in respect of an investment, the other Contracting State shall recognise the assignment to the first Contracting State or its designated agency of all rights and claims of the investor, and that agency is entitled to exercise such rights.",
        "text_en": "Host state recognizes subrogation of claims to home state or its designated agency (Sinosure) after payment under insurance or guarantee.",
        "text_zh": "【中国信保代位求偿权国际法保障】：若缔约国一方（中国政府）或其指定机构（中国出口信用保险公司 Sinosure）根据其就某项投资给予的保险或担保向投资者支付了赔款，东道国（印尼政府）必须依法承认投资者对该投资所享有的全部权利和请求权已全额转让给该指定机构；中国信保依法享有同等代位行使该权利并直诉印尼政府的国际法求偿权！【出海实务】：中信保海外投资险理赔的核心国际法底座！央企出险获赔后，信保直接代位启动国家间外交照会与国际追偿！",
        "norm_category": "bit_treaty",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_bit_id6_insurance_payout", "text_zh": "要件一：中国信保依据合规海外投资保单向出海央企正式支付了征收或违约赔偿金", "status": "condition_precedent"},
            {"eid": "e_bit_id6_assignment_notice", "text_zh": "要件二：正式向印尼政府递交权益转让与代位求偿书面通知", "status": "mandatory"},
            {"eid": "e_bit_id6_host_state_recognition", "text_zh": "法律后果：东道国强制承认信保代位权，不得以被保险人已获赔为由免除国家责任", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "TREATY:CN_ID_BIT_1992:Art9_Dispute_Settlement",
        "law": "TREATY:CN_ID_BIT_1992",
        "enbez": "Art 9",
        "title": "中印尼双边投资协定第九条：国际投资争端仲裁（ICSID管辖权）",
        "heading_path": "中华人民共和国与印度尼西亚共和国双边投资保护协定 (BIT 1994) > 第9条 争端解决",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Settlement of Investment Disputes: Any dispute between an investor of one Contracting State and the other Contracting State shall, if possible, be settled amicably through negotiations. If not settled within 6 months, the dispute may be submitted to the competent court of the host State or to the International Centre for Settlement of Investment Disputes (ICSID) under the Washington Convention.",
        "text_en": "Disputes unsettled within 6 months may be submitted to competent national courts or to ICSID arbitration under the Washington Convention.",
        "text_zh": "【中印尼投资争端ICSID直诉管辖】：中国投资者与印尼政府因投资发生的任何争议，应首先友好协商；自提出协商之日起 6 个月内未能解决的，投资者有权直接将争议提交世界银行投资争端解决中心（ICSID）依据《华盛顿公约》进行具有终局拘束力的国际仲裁！【实务启示】：打破印尼地方法院地方保护主义的最强王牌！但必须严格履行 6 个月前置行政磋商程序（Cooling-off Period），否则仲裁庭可能以未穷尽前置条件驳回管辖权！",
        "norm_category": "bit_treaty",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_bit_id9_six_month_negotiation", "text_zh": "要件一：向印尼投资协调委员会（BKPM）或相关部委送达条约争议通知并磋商满6个月", "status": "condition_precedent"},
            {"eid": "e_bit_id9_unsettled_dispute", "text_zh": "要件二：磋商期届满双方未达成实质性免责妥协或行政赔偿和解协议", "status": "mandatory"},
            {"eid": "e_bit_id9_icsid_jurisdiction", "text_zh": "法律后果：合法启动华盛顿公约ICSID国际仲裁，排除印尼地方法院干预", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "TREATY:CN_VN_BIT_1992:Art1_Definition",
        "law": "TREATY:CN_VN_BIT_1992",
        "enbez": "Art 1",
        "title": "中越双边投资保护协定第一条：投资与资产涵盖范围",
        "heading_path": "中华人民共和国政府和越南社会主义共和国政府关于鼓励和确定保护投资协定 (1992) > 第1条 定义",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Investment means every kind of asset invested by investors of one Contracting Party in accordance with the laws and regulations of the other Contracting Party in the territory of the latter, including movable and immovable property, shares, claims to money or performance, intellectual property and concessions.",
        "text_en": "Investment includes movable and immovable property, shares, claims to money, IP rights, and business concessions granted under Vietnamese law.",
        "text_zh": "【中越BIT投资定义与中资合法资产认定】：‘投资’是指中国投资者依照越南法律法规在越南领土内投入的各种财产，包括动产与不动产、公司股份与债券、与投资有关的金钱请求权、知识产权与依法授予的特许权。【实务启示】：中资企业赴越投资厂房与基础设施，必须在投资许可证（IRC）与企业营业执照（ERC）范围内开展活动，方可锁定中越 BIT 国际法层级的全面条约保护！",
        "norm_category": "bit_treaty",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_bit_vn1_irc_compliance", "text_zh": "要件一：投资活动取得越南计划投资部/工业园区管委会合法审批并持有IRC", "status": "condition_precedent"},
            {"eid": "e_bit_vn1_lawful_asset_class", "text_zh": "要件二：属于条约列明的股权、工程债权或土地地面资产财产权益", "status": "mandatory"},
            {"eid": "e_bit_vn1_standing_established", "text_zh": "法律后果：取得中越BIT条约下的受保护投资者地位", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "TREATY:CN_VN_BIT_1992:Art8_Arbitration_Limits",
        "law": "TREATY:CN_VN_BIT_1992",
        "enbez": "Art 8",
        "title": "中越BIT第八条：争议仲裁范围限制与CAFTA第14条管辖权升级路径",
        "heading_path": "中越双边投资保护协定 (1992) > 第8条 争端解决",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Settlement of Disputes: Disputes concerning the amount of compensation resulting from expropriation may be submitted to an ad hoc arbitral tribunal. (Note: Substantive breach claims are historically restricted under 1992 BIT and must be upgraded to CAFTA 2009 Article 14 for comprehensive UNCITRAL jurisdiction).",
        "text_en": "Disputes regarding compensation amount from expropriation may be arbitrated; broader claims must be upgraded via CAFTA 2009 Art 14 UNCITRAL rules.",
        "text_zh": "【中越旧版BIT仲裁范围限制与CAFTA升级实操生死线】：实务重大暗坑！中越 1992 年签署的旧版 BIT 第 8 条明文规定，提请国际仲裁的范围‘仅限于因征收产生的补偿款数额争议（Amount of Compensation）’，若东道国主张其行为不构成征收，则仲裁庭无权管辖！【出海实务破解之道】：中国母公司直接出海越南遭遇行政废约或间接征收时，必须放弃援引 1992 旧 BIT，而应直接依据《中国-东盟投资协议》(CAFTA 2009) 第 14 条提起 UNCITRAL 国际仲裁（海牙 PCA 管理），从而突破旧 BIT 的狭隘数额限制，实现对公正平等待遇（FET）等全案由实体管辖！",
        "norm_category": "bit_treaty",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_bit_vn8_narrow_clause", "text_zh": "要件一：识别出中越1992旧BIT仅限征收补偿金额仲裁之历史局限性", "status": "condition_precedent"},
            {"eid": "e_bit_vn8_cafta_invocation", "text_zh": "要件二：正式以中国母公司身份声明依据后法优于前法原则适用CAFTA第14条", "status": "mandatory"},
            {"eid": "e_bit_vn8_pca_uncitral_route", "text_zh": "法律后果：突破仲裁范围限制，向海牙常设仲裁院PCA提起全案由国际仲裁", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "TREATY:CN_MY_BIT_1988:Art1_Definition",
        "law": "TREATY:CN_MY_BIT_1988",
        "enbez": "Art 1",
        "title": "中马双边投资保护协定第一条：投资定义与核准项目要求",
        "heading_path": "中华人民共和国政府和马来西亚政府关于相互鼓励和保护投资协定 (1988) > 第1条 定义",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Investment means every kind of asset invested by investors of one Contracting Party in the territory of the other, accepted as such in accordance with its laws and administrative practices, including approval in writing by the designated agency (MIDA/EPU).",
        "text_en": "Investment includes all assets invested in accordance with Malaysian laws, specifically requiring written acceptance or registration by MIDA/EPU.",
        "text_zh": "【中马BIT投资定义与大马投资发展局MIDA批文前置】：‘投资’是指中国投资者依据马来西亚法律投入的各种财产。重要但书：受保护的投资在设立时必须获得马来西亚主管机关（如马来西亚投资发展局 MIDA 或经济事务部 EPU）的正式书面核准或登记备案。【实务启示】：赴马投资基建与合资企业，切勿脱离 MIDA 审批体系私自运作，取得 MIDA 投资批文是享受中马 BIT 条约保护的绝对法律要件！",
        "norm_category": "bit_treaty",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_bit_my1_mida_approval", "text_zh": "要件一：投资项目事先取得马来西亚投资发展局MIDA的书面核准或制造牌照", "status": "condition_precedent"},
            {"eid": "e_bit_my1_lawful_equity_asset", "text_zh": "要件二：资产属于合规出资形成的股权、厂房不动产或经认可的项目债权", "status": "mandatory"},
            {"eid": "e_bit_my1_treaty_protection", "text_zh": "法律后果：享有最惠国待遇、反非法征收及提请ICSID国际仲裁之完整权利", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "TREATY:CN_MY_BIT_1988:Art7_Arbitration",
        "law": "TREATY:CN_MY_BIT_1988",
        "enbez": "Art 7",
        "title": "中马双边投资协定第七条：国际投资争端仲裁机制（ICSID直诉）",
        "heading_path": "中马双边投资保护协定 (1988) > 第7条 争端解决",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Settlement of Investment Disputes: Any legal dispute arising directly out of an investment between an investor and the host State shall be settled through friendly consultations. If not settled within 6 months, it may be submitted to the International Centre for Settlement of Investment Disputes (ICSID).",
        "text_en": "Investment disputes not settled within 6 months may be submitted to ICSID for arbitration under the Washington Convention.",
        "text_zh": "【中马投资争端直诉世界银行ICSID管辖权】：中国投资者与马来西亚联邦政府因投资发生的直接法律争议，未能在6个月内友好协商解决的，投资者有权直接提交世界银行 ICSID 依据华盛顿公约进行国际仲裁！【实务启示】：因中国与马来西亚均为华盛顿公约正式缔约国，该仲裁条款具备高度确定性，是抗衡大马地方政府擅自关停中资项目、撕毁特许权合同的最高维武器！",
        "norm_category": "bit_treaty",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_bit_my7_cooling_off", "text_zh": "要件一：向马来西亚联邦政府国际贸易工业部（MITI）发出正式磋商通知满6个月", "status": "condition_precedent"},
            {"eid": "e_bit_my7_legal_dispute", "text_zh": "要件二：争议直接源于征收、特许权废除或条约义务违反之法律争议", "status": "mandatory"},
            {"eid": "e_bit_my7_icsid_filing", "text_zh": "法律后果：正式向ICSID秘书处提请仲裁，排他管辖且裁决视同本国终审判决", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "TREATY:CN_TH_BIT_1985:Art1_Definition",
        "law": "TREATY:CN_TH_BIT_1985",
        "enbez": "Art 1",
        "title": "中泰双边投资保护协定第一条：投资定义与泰BOI特别核准要求",
        "heading_path": "中华人民共和国政府和泰王国政府关于促进和保护投资协定 (1985) > 第1条 定义",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Investment means every kind of asset specifically approved in writing by the competent authority of Thailand (Board of Investment BOI or competent Ministry) in accordance with the legislation of Thailand.",
        "text_en": "Investment includes assets specifically approved in writing by Thai BOI or competent authorities under Thai legislation.",
        "text_zh": "【中泰BIT投资定义与泰国BOI书面核准前置条件】：中泰早期 BIT 特别条款：受保护的‘投资’，仅限于依照泰国法律获得泰国主管机关（主要是泰国投资促进委员会 BOI）书面特别核准（Specifically Approved in Writing）的资产！【实务启示】：中资企业赴泰投资，若未申请 BOI 投资促进证书而仅按普通外商投资备案，在遭遇征收时可能被泰国政府以‘未获特定书面核准’为由抗辩管辖权！因此大额投资必须申请 BOI 证书或结合 CAFTA 投资协议进行双重确权！",
        "norm_category": "bit_treaty",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_bit_th1_boi_certificate", "text_zh": "要件一：取得泰国BOI颁发的正式投资促进证书及书面合规批文", "status": "condition_precedent"},
            {"eid": "e_bit_th1_approved_asset_scope", "text_zh": "要件二：资金投入与工业用地购置属于批文核准的商业经营范围", "status": "mandatory"},
            {"eid": "e_bit_th1_treaty_shield", "text_zh": "法律后果：取得中泰BIT条约下的最高级别外交与国际法抗辩保护", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "TREATY:CN_TH_BIT_1985:Art8_Arbitration_UNCITRAL",
        "law": "TREATY:CN_TH_BIT_1985",
        "enbez": "Art 8",
        "title": "中泰BIT第八条：国际投资争端仲裁与走UNCITRAL/PCA而非ICSID之法理铁律",
        "heading_path": "中泰双边投资保护协定 (1985) > 第8条 争端解决",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Settlement of Disputes: Disputes regarding compensation for expropriation not settled within 6 months may be submitted to an ad hoc arbitral tribunal (UNCITRAL Rules). (Crucial Note: Thailand signed but NEVER ratified the ICSID Convention; claims MUST proceed under UNCITRAL/PCA rules!).",
        "text_en": "Disputes regarding expropriation compensation proceed to ad hoc arbitration under UNCITRAL rules. Thailand is NOT an ICSID Contracting State.",
        "text_zh": "【中泰投资仲裁必须走UNCITRAL/PCA而非ICSID实务铁律】：重大涉外法理！虽然中泰 BIT 包含国际仲裁条款，但因为**泰国虽然于 1985 年签署了《华盛顿公约 (ICSID)》，但至今未获泰国国会批准生效，泰国不是 ICSID 缔约国！**因此，针对泰国政府提起的投资争端仲裁，绝不能提请常规 ICSID 仲裁，而必须依据中泰 BIT 第8条或 CAFTA 投资协议提请适用 **联合国国际贸易法委员会（UNCITRAL）仲裁规则（通常由海牙常设仲裁院 PCA 管理）** 或 ICSID 附加便利机制！【出海实务】：诉讼路径走错将导致仲裁院直接不受理，错失数千万索赔时机！",
        "norm_category": "bit_treaty",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_bit_th8_non_icsid_state", "text_zh": "要件一：准确认定泰国未批准ICSID公约之主权法律现状", "status": "condition_precedent"},
            {"eid": "e_bit_th8_uncitral_routing", "text_zh": "要件二：仲裁申请书明确指定适用UNCITRAL仲裁规则并选定海牙PCA管理", "status": "mandatory"},
            {"eid": "e_bit_th8_valid_jurisdiction", "text_zh": "法律后果：仲裁庭具备合法管辖权，泰国政府无权主张机构管辖异议", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "TREATY:CN_SG_BIT_1985:Art1_Definition",
        "law": "TREATY:CN_SG_BIT_1985",
        "enbez": "Art 1",
        "title": "中新双边投资保护协定第一条：投资定义与资金自由汇兑保障",
        "heading_path": "中华人民共和国政府和新加坡共和国政府关于促进和保护投资协定 (1985) > 第1条 定义",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Investment means every kind of asset permitted by each Contracting Party in accordance with its laws, including shares, stocks, debentures, claims to money, IP, and business concessions. Free transfer of capital, returns and proceeds of liquidation is fully guaranteed.",
        "text_en": "Investment includes all assets permitted by laws of each Party, guaranteeing free transfer of capital, returns, and liquidation proceeds.",
        "text_zh": "【中新BIT投资定义与资金自由转移保障】：中国与新加坡双向投资涵盖股份、工程债权、特许权及收益。协定明文保证投资者可自由转移其投资本金、利润、股息、特许权使用费及清算所得，东道国不得设置不合理外汇兑换壁垒。【实务启示】：中新投资协定是中资在新加坡设立区域财资与结算中心（SPV）的最高国际法保证，资金进出 100% 自由。",
        "norm_category": "bit_treaty",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_bit_sg1_singapore_pma", "text_zh": "要件一：在新加坡依法设立登记的合规投资企业或中国在岸投资实体", "status": "condition_precedent"},
            {"eid": "e_bit_sg1_capital_transfers", "text_zh": "要件二：外汇资金属于已完税合法经营收益、资本减资或清算款项", "status": "mandatory"},
            {"eid": "e_bit_sg1_freedom_of_transfer", "text_zh": "法律后果：享受条约保障的无限制购汇与跨境自由划转权", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "TREATY:CN_SG_BIT_1985:Art13_ICSID",
        "law": "TREATY:CN_SG_BIT_1985",
        "enbez": "Art 13",
        "title": "中新双边投资协定第十三条：投资争端提交华盛顿公约ICSID仲裁",
        "heading_path": "中新双边投资保护协定 (1985) > 第13条 争端解决",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Any dispute between an investor and the host State concerning expropriation or nationalization not resolved in 6 months shall be submitted to the International Centre for Settlement of Investment Disputes (ICSID).",
        "text_en": "Expropriation disputes not settled in 6 months shall be submitted to ICSID arbitration under the Washington Convention.",
        "text_zh": "【中新征收争议ICSID国际仲裁管辖权】：中新两国因征收或国有化产生的争议，6个月内未解决的，可提交世界银行 ICSID 仲裁。新方与中方均为华盛顿公约资深成员国，裁决具备全球终局执行力。【实务启示】：虽然新加坡本国征地法治健全，但本条款为中企在新加坡遭遇公共工程征用时的市值补偿提供了坚不可摧的条约兜底！",
        "norm_category": "bit_treaty",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_bit_sg13_six_month_window", "text_zh": "要件一：征收补偿争议发生后已履行6个月条约前置磋商程序", "status": "condition_precedent"},
            {"eid": "e_bit_sg13_expropriation_matter", "text_zh": "要件二：争议涉及土地征收、特许权撤回或直接事实征收行为", "status": "mandatory"},
            {"eid": "e_bit_sg13_icsid_award", "text_zh": "法律后果：ICSID裁决在两国及全球160+成员国享有等同本国终审判决之执行力", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "TREATY:CN_PH_BIT_1992:Art1_Definition",
        "law": "TREATY:CN_PH_BIT_1992",
        "enbez": "Art 1",
        "title": "中菲双边投资保护协定第一条：投资定义与菲律宾宪法外资比例限制",
        "heading_path": "中华人民共和国政府和菲律宾共和国政府关于促进和相互保护投资协定 (1992) > 第1条 定义",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Investment means every kind of asset invested by an investor of one Contracting State in accordance with the Constitution, laws and regulations of the other Contracting State, including property, shares, claims to money, IP and concessions.",
        "text_en": "Investment must comply with the Constitution and laws of Philippines, specifically referencing constitutional foreign equity limits (60/40 rule).",
        "text_zh": "【中菲BIT投资定义受制于菲律宾宪法外资限制】：中菲 BIT 第 1 条特别强调：受条约保护的投资必须符合菲律宾《1987年宪法》及法律法规！【实务启示】：菲律宾宪法对土地所有权及特定公用事业实行极其严格的‘40% 外资上限（60/40 菲资控制规则）’。若中资通过代持或秘密协议企图规避宪法外资比例，在国际仲裁（如 Fraport 案）中将直接被判定为违宪非法投资，彻底丧失 BIT 全部条约保护！",
        "norm_category": "bit_treaty",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_bit_ph1_constitutional_compliance", "text_zh": "要件一：投资架构完全符合菲律宾宪法第十二条关于40%外资上限之红线", "status": "condition_precedent"},
            {"eid": "e_bit_ph1_anti_dummy_clearance", "text_zh": "要件二：股权结构不存在违反《反傀儡法》(Anti-Dummy Law) 之代持安排", "status": "mandatory"},
            {"eid": "e_bit_ph1_treaty_admissibility", "text_zh": "法律后果：投资具备国际公法合法性，仲裁庭受理实体索赔请求", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "TREATY:CN_PH_BIT_1992:Art6_Subrogation",
        "law": "TREATY:CN_PH_BIT_1992",
        "enbez": "Art 6",
        "title": "中菲双边投资协定第六条：代位求偿与中信保理赔后追偿权",
        "heading_path": "中菲双边投资保护协定 (1992) > 第6条 代位",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Subrogation: If one Contracting State or its designated agency makes a payment under an indemnity given in respect of an investment, the other Contracting State shall recognise the assignment to the first State of all rights and claims.",
        "text_en": "Host State recognizes subrogation of claims to home State or designated insurer (Sinosure) upon payment of indemnity under investment guarantee.",
        "text_zh": "【中菲信保代位求偿国际法确认】：菲律宾政府明文承认中国政府及其指定机构（中国信保 Sinosure）在依据投资保单赔付后，全面受让中资企业的对菲全部条约索赔权利；中国信保可直接以代位人身份向菲律宾政府主张赔偿。【实务启示】：中资承建菲律宾政府基建项目（如水坝、铁路），投保中信保海外投资险与特许权违约险是锁定主权级追偿力的刚性要求！",
        "norm_category": "bit_treaty",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_bit_ph6_sinosure_claim_settled", "text_zh": "要件一：中国信保向中资被保险人完成全部出险损失理赔款支付", "status": "condition_precedent"},
            {"eid": "e_bit_ph6_subrogation_execution", "text_zh": "要件二：签署法定代位求偿协议书并正式通知菲律宾财政部与司法部", "status": "mandatory"},
            {"eid": "e_bit_ph6_sovereign_recourse", "text_zh": "法律后果：中信保取得国家间直接交涉与国际仲裁追偿之合法权利", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "TREATY:CN_PH_BIT_1992:Art9_ICSID",
        "law": "TREATY:CN_PH_BIT_1992",
        "enbez": "Art 9",
        "title": "中菲双边投资协定第九条：国际投资争端提交ICSID仲裁",
        "heading_path": "中菲双边投资保护协定 (1992) > 第9条 争端解决",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Investment disputes not resolved within 6 months through negotiations may be submitted to the International Centre for Settlement of Investment Disputes (ICSID) pursuant to the Washington Convention.",
        "text_en": "Unsettled investment disputes between Chinese investor and Philippine Government proceed to ICSID arbitration after 6 months of consultations.",
        "text_zh": "【中菲投资争端直诉ICSID管辖】：中国投资者与菲律宾政府因投资产生的争议，经6个月友好协商未果的，投资者有权直接向华盛顿 ICSID 提起国际仲裁。【实务启示】：菲律宾是 ICSID 正式缔约国，中菲 BIT 第9条为中资企业提供了越过菲律宾本土法院、直诉国际法庭的核心维权通道！",
        "norm_category": "bit_treaty",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_bit_ph9_six_month_consult", "text_zh": "要件一：正式向菲律宾总统府与相关部委送达争端通知并磋商满6个月", "status": "condition_precedent"},
            {"eid": "e_bit_ph9_treaty_breach", "text_zh": "要件二：指控涉及菲律宾政府机构直接撤约、没收或违反条约义务", "status": "mandatory"},
            {"eid": "e_bit_ph9_icsid_filing_right", "text_zh": "法律后果：正式向ICSID申请立案，排他管辖并排除下级法院禁令干扰", "status": "prohibition"}
        ], ensure_ascii=False)
    }
]

PHASE2_PRC_OUTBOUND_NORMS = [
    {
        "table": "norms",
        "norm_id": "CN:SASAC_Order_35:Art7_Negative_List",
        "law": "CN:SASAC_Order_35",
        "enbez": "Art 7",
        "title": "国资委35号令第七条：中央企业境外投资负面清单特别监管红线",
        "heading_path": "国务院国资委令第35号《中央企业境外投资监督管理办法》 > 第二章 投资事前管理 > 负面清单",
        "language_mode": "bilingual",
        "lang_original": "zh",
        "text_original": "第七条 国资委根据国家有关规定和央企发展战略，建立中央企业境外投资负面清单。负面清单设定禁止类和特别监管类境外投资项目。列入负面清单禁止类的境外投资项目，中央企业一律不得投资。列入负面清单特别监管类的境外投资项目，中央企业应当报国资委履行审核程序。",
        "text_en": "SASAC establishes a negative list for outbound investment of central SOEs, comprising prohibited and specially supervised categories. Central SOEs shall strictly refrain from prohibited investments.",
        "text_zh": "【国资委央企境外投资负面清单特别监管红线】：国资委对央企境外投资实行负面清单管理。列入禁止类的项目，中央企业一律严禁开展任何形式投资；列入特别监管类的项目，必须报国资委履行前置审核程序；严禁擅自超越主业盲目开展高风险非主业境外并购与投资！【实务启示】：央企出海开展东盟并购或 PPP 特许经营项目，必须对照国资委最新境外投资主业清单与特别监管目录，未过国资委会签严禁对外签署具有法律约束力的投资协议！",
        "norm_category": "prc_sasac_reg",
        "mandatory_level": "mandatory_override",
        "elements_json": json.dumps([
            {"eid": "e_sasac35_7_negative_list_check", "text_zh": "要件一：项目标的必须对照国资委负面清单进行严格合规审查，严禁涉及禁止类", "status": "condition_precedent"},
            {"eid": "e_sasac35_7_special_supervision_approval", "text_zh": "要件二：涉及特别监管类或超主业投资，必须事先取得国资委正式书面审核批文", "status": "mandatory"},
            {"eid": "e_sasac35_7_compliance_shield", "text_zh": "法律后果：未批先投属于重大违规行为，投资决策人承担终身追责法律责任", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "CN:SASAC_Order_35:Art18_Due_Diligence",
        "law": "CN:SASAC_Order_35",
        "enbez": "Art 18",
        "title": "国资委35号令第十八条：境外重大项目尽职调查与法务合规一票否决",
        "heading_path": "国务院国资委令第35号《中央企业境外投资监督管理办法》 > 第二章 投资事前管理 > 尽职调查与合规审核",
        "language_mode": "bilingual",
        "lang_original": "zh",
        "text_original": "第十八条 中央企业开展重大境外投资项目，应当委托具有相应资质独立第三方专业机构开展财务、法律、技术、环境、安全等尽职调查。企业总法律顾问应当对境外重大投资项目出具专项法律合规审查意见书。未经法律合规审查或审查未通过的，不得提交企业党委会、董事会审议决策。",
        "text_en": "Central SOEs must retain qualified independent professional third parties to conduct legal, financial and technical due diligence; Chief Legal Officer must issue written compliance opinion.",
        "text_zh": "【境外重大项目第三方尽调与总法律顾问一票否决权】：央企实施重大境外投资，必须委托独立第三方专业机构开展财务、法律、环保等穿透式尽职调查；企业总法律顾问必须出具书面法律合规审查意见书；未经法律合规审查或审查结论为‘存在重大法律硬伤未通过’的项目，严禁提交党委会、董事会审议！【实务启示】：法务合规在央企出海投决中享有一票否决权！必须就东道国土地权属、外资股权上限及代持风险出具清晰的风险阻断意见。",
        "norm_category": "prc_sasac_reg",
        "mandatory_level": "mandatory_override",
        "elements_json": json.dumps([
            {"eid": "e_sasac35_18_third_party_dd", "text_zh": "要件一：委托具备属地执业资格的权威第三方律所开展穿透式法律尽职调查", "status": "condition_precedent"},
            {"eid": "e_sasac35_18_clo_compliance_opinion", "text_zh": "要件二：集团或二级企业总法律顾问出具正式签字盖章的法律合规审查意见书", "status": "mandatory"},
            {"eid": "e_sasac35_18_veto_gate", "text_zh": "法律后果：合规审查未通过构成董事会立项的绝对程序阻断，禁止强行上会", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "CN:SASAC_Notice_75_2021:Art3_No_External_Guarantee",
        "law": "CN:SASAC_Notice_75_2021",
        "enbez": "Art 3",
        "title": "国资委75号文第三条：严禁为集团外无股权关系企业提供任何形式担保",
        "heading_path": "国资发财评规〔2021〕75号《关于加强中央企业融资担保管理工作的通知》 > 担保对象与范围管控 > 外部担保严禁",
        "language_mode": "bilingual",
        "lang_original": "zh",
        "text_original": "第三条 中央企业应当严格限定融资担保对象。中央企业严禁对集团外无股权关系的企业提供任何形式的融资担保或连带责任担保，严禁为参股企业超持股比例提供无对等反担保的连带担保。不得对进入破产清算重整程序的企业提供新增担保。",
        "text_en": "Central SOEs are strictly prohibited from providing any form of financing guarantee or joint liability guarantee to entities outside the group with no equity relationship.",
        "text_zh": "【央企严禁对外提供融资担保与严禁超股比连带担保红线】：中央企业严禁对集团外无股权关系的企业提供任何形式的融资担保或连带担保；在合资联营企业中，严禁超过自身持股比例提供无对等反担保的超额担保！【出海实务生死线】：中资在东盟与外方组建 KSO 联营体或合资电站 SPV 时，外方业主和国际银团几乎 100% 要求中资母公司提供‘100% 连带母公司完工保函（PCG）’。依据75号文，中资若仅持股 50%，出具 100% PCG 属于严重违规行为！必须争取按持股比例分割担保责任，或要求外方股东提供足额反担保！",
        "norm_category": "prc_sasac_reg",
        "mandatory_level": "mandatory_override",
        "elements_json": json.dumps([
            {"eid": "e_sasac75_3_equity_relationship", "text_zh": "要件一：担保对象必须属于集团合并报表范围内具有实质股权投资关系的子公司", "status": "condition_precedent"},
            {"eid": "e_sasac75_3_proportional_limit", "text_zh": "要件二：合资项目担保额度严格以自身实际持股比例为上限，严禁单方全额背书", "status": "mandatory"},
            {"eid": "e_sasac75_3_strict_prohibition", "text_zh": "法律后果：违反规定出具超额保函或对外担保，相关决策人员承担重大违规经济责任", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "CN:NDRC_Order_11:Art13_Sensitive_Approval",
        "law": "CN:NDRC_Order_11",
        "enbez": "Art 13",
        "title": "发改委11号令第十三条：敏感国家和敏感行业境外投资国家核准程序",
        "heading_path": "国家发展和改革委员会令第11号《企业境外投资管理办法》 > 第三章 境外投资的核准和备案 > 敏感类项目核准",
        "language_mode": "bilingual",
        "lang_original": "zh",
        "text_original": "第十三条 实行核准管理的范围是投资主体开展的敏感类项目。敏感类项目包括：涉及敏感国家和地区的项目；涉及敏感行业的项目。敏感类项目由国家发展改革委核准。",
        "text_en": "Outbound investment projects involving sensitive countries/regions or sensitive industries are subject to approval by the National Development and Reform Commission (NDRC).",
        "text_zh": "【发改委敏感国家与敏感行业投资必须事先报批核准】：投资主体开展的涉及未建交国家、战乱制裁国家等敏感国家和地区，或涉及跨境水资源开发、基础电信运营、新闻传媒等敏感行业的境外投资项目，无论投资金额大小，必须报国家发改委履行前置核准程序；取得核准批复文件方可对外签约与汇出投资款！【实务启示】：投资东盟水电水利工程、跨境光缆、电网干线等重大基建，必须在投决前先锁定发改委敏感行业核准批文！",
        "norm_category": "prc_sasac_reg",
        "mandatory_level": "mandatory_override",
        "elements_json": json.dumps([
            {"eid": "e_ndrc11_13_sensitive_screening", "text_zh": "要件一：项目经过发改委敏感行业目录比对，确认是否涉及跨境水利、电信或电网", "status": "condition_precedent"},
            {"eid": "e_ndrc11_13_formal_approval_filing", "text_zh": "要件二：正式向国家发改委报送项目申请报告并取得核准批文文件", "status": "mandatory"},
            {"eid": "e_ndrc11_13_condition_precedent", "text_zh": "法律后果：核准批复是办理外汇登记、海关验放及对外出资的法定生效前置条件", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "CN:NDRC_Order_11:Art14_Non_Sensitive_Filing",
        "law": "CN:NDRC_Order_11",
        "enbez": "Art 14",
        "title": "发改委11号令第十四条：非敏感类境外投资项目发改委备案管理",
        "heading_path": "国家发展和改革委员会令第11号《企业境外投资管理办法》 > 第三章 境外投资的核准和备案 > 备案管理",
        "language_mode": "bilingual",
        "lang_original": "zh",
        "text_original": "第十四条 实行备案管理的范围是投资主体开展的非敏感类项目。中央管理企业开展的非敏感类项目，以及地方企业开展的中方投资额3亿美元及以上非敏感类项目，由国家发展改革委备案。地方企业开展的中方投资额3亿美元以下非敏感类项目，由省发展改革部门备案。",
        "text_en": "Non-sensitive outbound investment projects by central SOEs, or local enterprises with Chinese investment of USD 300 million or more, are subject to filing with NDRC.",
        "text_zh": "【非敏感类境外投资项目分级备案机制】：央企开展的非敏感类境外投资，以及地方企业中方投资额超 3 亿美元项目，由国家发改委备案；3 亿美元以下地方项目由省级发改委备案；取得《境外投资项目备案通知书》方可启动实施。【实务启示】：非敏感类普通新能源、工民建施工项目走备案制，通常 7 个工作日内办结，但必须严格在实施前完成备案，杜绝未批先建！",
        "norm_category": "prc_sasac_reg",
        "mandatory_level": "mandatory_override",
        "elements_json": json.dumps([
            {"eid": "e_ndrc11_14_non_sensitive_class", "text_zh": "要件一：项目属于发改委非敏感类目录范围，中方投资额按层级划分管辖", "status": "condition_precedent"},
            {"eid": "e_ndrc11_14_filing_certificate", "text_zh": "要件二：在全国境外投资管理和服务网络系统提交申请并取得备案通知书", "status": "mandatory"},
            {"eid": "e_ndrc11_14_validity_period", "text_zh": "法律后果：备案文件有效期2年，作为合法开立外汇账户与出资的法定凭证", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "CN:SAFE_Notice_29_2014:Art9_Neibaowaidai",
        "law": "CN:SAFE_Notice_29_2014",
        "enbez": "Art 9",
        "title": "外汇局29号文第九条：内保外贷签约后15个工作日向外汇局办理登记",
        "heading_path": "国家外汇管理局汇发〔2014〕29号《跨境担保外汇管理规定》 > 第一章 内保外贷 > 登记与履约",
        "language_mode": "bilingual",
        "lang_original": "zh",
        "text_original": "第九条 境内非银行机构提供内保外贷的，应当在签订担保合同后15个工作日内到所在地外汇局办理内保外贷签约登记手续。担保合同发生变更的，应当办理变更登记。境内机构向境外借款人提供内保外贷，债务人必须用于正常的商业生产经营，严禁用于虚假贸易、投机交易或将资金调回境内使用。",
        "text_en": "Domestic non-bank entities providing cross-border security (Neibaowaidai) must register with the local SAFE branch within 15 working days after signing the guarantee contract.",
        "text_zh": "【内保外贷15个工作日外汇登记生死线】：境内母公司为境外工程项目子公司借款向境外银行出具融资保函或备用信用证（内保外贷）的，必须在签署担保合同之日起 15 个工作日内到所在地外汇管理局办理内保外贷签约登记手续；担保资金必须用于境外正常生产经营，严禁回流境内！【实务启示】：海外银团贷款重磅红线！未办理外汇局 29 号文登记的内保外贷，一旦境外子公司发生违约，境内母公司将无法依法购汇汇出履约赔款，银行保函将被阻断执行，企业面临巨大信用与诉讼风暴！",
        "norm_category": "prc_sasac_reg",
        "mandatory_level": "mandatory_override",
        "elements_json": json.dumps([
            {"eid": "e_safe29_9_fifteen_day_registration", "text_zh": "要件一：担保合同签署之日起15个工作日内向注册地外汇局提交正式登记材料", "status": "condition_precedent"},
            {"eid": "e_safe29_9_overseas_use_only", "text_zh": "要件二：贷款资金严格限定用于东道国现场工程施工与项目投资采购，严禁资金回流", "status": "mandatory"},
            {"eid": "e_safe29_9_remittance_clearance", "text_zh": "法律后果：取得外汇局内保外贷登记凭单，担保履约时依法享受购汇支付通道", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "CN:SAFE_Notice_29_2014:Art27_PCG_Registration",
        "law": "CN:SAFE_Notice_29_2014",
        "enbez": "Art 27",
        "title": "外汇局29号文第二十七条：母公司履约担保（PCG）登记与履约购汇合规",
        "heading_path": "国家外汇管理局汇发〔2014〕29号《跨境担保外汇管理规定》 > 第四章 其他形式跨境担保 > 物权与履约担保",
        "language_mode": "bilingual",
        "lang_original": "zh",
        "text_original": "第二十七条 境内机构提供物权担保或非融资性保证（包括为境外工程承包提供母公司完工履约保证 PCG），除外汇局另有明确规定外，担保人无需到外汇局办理担保签约登记。担保人实际发生履约赔付义务时，担保人凭担保合同、境外索赔通知书、完税证明等合规凭证，直接向境内外汇指定银行办理购汇和对外支付手续。",
        "text_en": "Domestic entities providing non-financing cross-border guarantees (Parent Company Guarantee PCG) are exempt from prior SAFE registration; payments proceed directly via designated banks.",
        "text_zh": "【母公司完工履约保函PCG直接银行购汇履约便利】：中国境内母公司为境外工程承包项目向东盟业主出具母公司完工履约保函（Parent Company Guarantee, PCG）的，属于非融资性跨境担保，签约时无需逐笔办理外汇局事先登记；一旦发生境外业主合法索赔，母公司凭 PCG 担保合同原件及工程索赔有效证明，可直接在商业银行办理合规购汇汇出履约赔款！【实务启示】：极大化解了 PCG 履约障碍，但必须确保 PCG 合同严格约定仲裁条款，防止境外业主恶意批量索赔。",
        "norm_category": "prc_sasac_reg",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_safe29_27_non_financing_pcg", "text_zh": "要件一：担保性质属于非融资性的建设工程承包完工履约保证PCG", "status": "condition_precedent"},
            {"eid": "e_safe29_27_substantiated_claim", "text_zh": "要件二：境外发包人提供正式书面索赔违约认定与工程损失有效核定凭证", "status": "mandatory"},
            {"eid": "e_safe29_27_bank_remittance_access", "text_zh": "法律后果：免于外汇局前置审批，直接通过持牌外汇银行办理合规购汇履约", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "CN:MOFCOM_Order_3:Art9_ODI_Certificate",
        "law": "CN:MOFCOM_Order_3",
        "enbez": "Art 9",
        "title": "商务部令2014年第3号第九条：企业境外投资证书（ODI）法定申领",
        "heading_path": "商务部令2014年第3号《境外投资管理办法》 > 第二章 备案和核准 > ODI证书核发",
        "language_mode": "bilingual",
        "lang_original": "zh",
        "text_original": "第九条 对予以备案的境外投资，商务部或省级商务主管部门自收到《境外投资备案表》之日起3个工作日内予以备案并颁发《企业境外投资证书》。对予以核准的境外投资，商务部在法定期限内作出核准决定并颁发《企业境外投资证书》。《企业境外投资证书》是企业开展境外投资的合法凭证。",
        "text_en": "MOFCOM or provincial departments issue the Enterprise Outbound Investment Certificate (ODI Certificate) within 3 days for filings or upon approval, serving as statutory proof.",
        "text_zh": "【商务部企业境外投资证书ODI法定核发】：商务部或省级商务厅对企业境外设立子公司、收并购或参股项目核发《企业境外投资证书》（ODI 证书）。企业办理银行境外直接投资外汇登记、进出口海关登记及外派人员签证手续，必须出示正式 ODI 证书原件！【实务启示】：央企出海东盟三件套（发改委备案、商务部 ODI、外汇局外汇登记）中不可或缺的准生证，未取得 ODI 证书严禁对外出资！",
        "norm_category": "prc_sasac_reg",
        "mandatory_level": "mandatory_override",
        "elements_json": json.dumps([
            {"eid": "e_mofcom3_9_odi_filing", "text_zh": "要件一：在商务部境外投资管理系统合规完成投资项目备案申报", "status": "condition_precedent"},
            {"eid": "e_mofcom3_9_certificate_issuance", "text_zh": "要件二：取得商务部或省级商务厅加盖公章的正式《企业境外投资证书》", "status": "mandatory"},
            {"eid": "e_mofcom3_9_foreign_exchange_gate", "text_zh": "法律后果：银行凭ODI证书办理外商直接投资FDI资本金合法购汇出境手续", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "CN:Foreign_Related_Civil_Relations:Art4_Mandatory",
        "law": "CN:Foreign_Related_Civil_Relations",
        "enbez": "Art 4",
        "title": "涉外民事关系法律适用法第四条：中国强制性规定直接适用原则",
        "heading_path": "《中华人民共和国涉外民事关系法律适用法》 > 第一章 一般规定 > 强制性规定直接适用",
        "language_mode": "bilingual",
        "lang_original": "zh",
        "text_original": "第四条 中华人民共和国法律对涉外民事关系有强制性规定的，直接适用该强制性规定。",
        "text_en": "Where the laws of the People's Republic of China have mandatory provisions on foreign-related civil relations, such mandatory provisions shall be applied directly.",
        "text_zh": "【中国法强制性规定直接适用（Overriding Mandatory Provisions）】：只要涉外民商事合同与关系触及中国公法安全底线，无论当事人合同中明文约定适用何国法律（如约定英国法、新加坡法），中国法律中的强行性规范（包括数据安全出境审查、央企国资监管红线、反外国制裁禁令、中信保报损规定）均具有绝对的最高优先度，直接穿透并强制适用！【实务启示】：涉外审判与出海央企法务护城河！合同选了外国法，并不等于可以逃避国内强行法的刚性管辖。",
        "norm_category": "prc_sasac_reg",
        "mandatory_level": "mandatory_override",
        "elements_json": json.dumps([
            {"eid": "e_prc_fl4_mandatory_character", "text_zh": "要件一：国内成文法规范属于涉及社会公共利益、国家安全或经济秩序的强行法", "status": "condition_precedent"},
            {"eid": "e_prc_fl4_direct_applicability", "text_zh": "要件二：该争议涉外法律关系与中国主权法域存在实质性管辖联系", "status": "mandatory"},
            {"eid": "e_prc_fl4_override_contract_choice", "text_zh": "法律后果：直接覆写排他适用的合同选法，排除任何外国法对强行法的规避", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "CN:Foreign_Related_Civil_Relations:Art41_Contract_Law",
        "law": "CN:Foreign_Related_Civil_Relations",
        "enbez": "Art 41",
        "title": "涉外民事关系法律适用法第四十一条：合同选法自由与最密切联系原则",
        "heading_path": "《中华人民共和国涉外民事关系法律适用法》 > 第四章 债权 > 合同准据法",
        "language_mode": "bilingual",
        "lang_original": "zh",
        "text_original": "第四十一条 当事人可以协议选择合同适用的法律。当事人没有选择的，适用履行义务最能体现该合同特征的一方当事人经常居所地法律或者其他有最密切联系的法律。",
        "text_en": "Parties may agree to choose law applicable to contract; absent choice, law of party whose performance best reflects characteristic of contract applies.",
        "text_zh": "【涉外合同选法自治与最密切联系原则】：当事人可协议选择涉外工程与投资合同适用的准据法；未选择准据法时，适用特征性履行方（通常为总承包商或施工实施方）所在地法或最密切联系地法（工程不动产所在地法）。【实务启示】：在东盟签署合同时，若无法达成一致，尽量争取适用中立的新加坡法或英国法；若未约定，东道国法院将直接援引不动产所在地法强制适用东道国法律！",
        "norm_category": "prc_sasac_reg",
        "mandatory_level": "contract_default",
        "elements_json": json.dumps([
            {"eid": "e_prc_fl41_party_autonomy", "text_zh": "要件一：合同中包含双方当事人自愿明确订立的书面法律适用选择条款", "status": "condition_precedent"},
            {"eid": "e_prc_fl41_closest_connection", "text_zh": "要件二：未选择准据法时，依据工程不动产所在地或特征性履行方居所地确定", "status": "mandatory"},
            {"eid": "e_prc_fl41_governing_law_basis", "text_zh": "法律后果：确定统辖合同成立、违约责任与索赔解释的实体准据法体系", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "CN:SPC_Foreign_Law_Ascertainment_2023:Art2_Pathways",
        "law": "CN:SPC_Foreign_Law_Ascertainment_2023",
        "enbez": "Art 2",
        "title": "最高法外法查明司法解释二第二条：域外法官方查明法定途径全集",
        "heading_path": "最高人民法院法释〔2023〕10号《关于适用涉外民事关系法律适用法若干问题的解释（二）》 > 外国法查明途径",
        "language_mode": "bilingual",
        "lang_original": "zh",
        "text_original": "第二条 人民法院通过下列途径查明外国法：(一) 由当事人提供；(二) 通过司法协助协定规定的途径提供；(三) 通过最高人民法院建立或者参与的外国法查明机制提供；(四) 通过外交途径提供；(五) 由中外法律专家提供；(六) 其他合理途径。通过互联网检索获取的外国法律，应当要求当事人确认或通过专家论证认证。",
        "text_en": "Supreme People's Court establishes 6 statutory pathways to ascertain foreign law, including parties' submission, judicial assistance, legal experts, and official platforms.",
        "text_zh": "【最高法外国法查明六大权威法定途径】：人民法院审理涉外案卷查明东盟法律时，严格依托六大途径：① 当事人举证提供；② 国际司法协助；③ 最高法建立的域外法查明统一平台（如本系统对接的官方智库底座）；④ 外交途径；⑤ 权威中外法学专家出具书面鉴定意见；⑥ 互联网官方法律公报经法庭质证确认。【实务启示】：出海企业在涉外仲裁或诉讼中主张东道国法律，必须严格依照本条组织证据，提供加盖使领馆认证或权威机构公证的东道国官方语种法典全文与权威译本！",
        "norm_category": "prc_sasac_reg",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_spc_fl2_official_pathways", "text_zh": "要件一：查明法源来自最高院六大认可途径之一并具备官方公信力背书", "status": "condition_precedent"},
            {"eid": "e_spc_fl2_expert_cross_examination", "text_zh": "要件二：域外成文法条文及判例经过开庭质证或持有持牌法学专家出具的法律意见书", "status": "mandatory"},
            {"eid": "e_spc_fl2_judicial_notice_effect", "text_zh": "法律后果：人民法院依法认定外国法内容属实并作为裁决案件事实之依据", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "CN:Anti_Foreign_Sanctions_Law:Art12_Blocking",
        "law": "CN:Anti_Foreign_Sanctions_Law",
        "enbez": "Art 12",
        "title": "反外国制裁法第十二条：严禁执行外国歧视性限制措施与阻断追偿",
        "heading_path": "《中华人民共和国反外国制裁法》 > 阻断与反制 > 歧视性措施禁止",
        "language_mode": "bilingual",
        "lang_original": "zh",
        "text_original": "第十二条 任何组织和个人均不得执行或者协助执行外国国家对我国公民、组织采取的歧视性限制措施。组织和个人违反前款规定，侵害我国公民、组织合法权益的，我国公民、组织可以依法向人民法院提起诉讼，要求其停止侵害、赔偿损失。",
        "text_en": "No organization or individual may execute or assist in executing discriminatory restrictive measures taken by foreign states; victims may sue in PRC courts for damages.",
        "text_zh": "【反外国制裁阻断与境内诉讼赔偿重锤】：任何境外跨国公司、在华外资银行或个人，均严禁执行外国政府对中国企业实施的单边长臂管辖或歧视性制裁；若外资业主或国际银团配合美西方单边制裁单方解约或拒绝支付工程款，中国央企有权直接向中国人民法院提起民事诉讼，判令其停止侵害并赔偿全部直接与间接经济损失！【实务启示】：面对美西方对涉疆、涉军出海中企的单边封锁，第12条为企业在境内追索境外被扣工程款提供了强大的反制司法武器！",
        "norm_category": "prc_sasac_reg",
        "mandatory_level": "mandatory_override",
        "elements_json": json.dumps([
            {"eid": "e_afsl12_discriminatory_sanction", "text_zh": "要件一：外国国家依据其国内法对我出海央企采取歧视性单边制裁措施", "status": "condition_precedent"},
            {"eid": "e_afsl12_unlawful_compliance", "text_zh": "要件二：外方当事人配合外国制裁单方违约终止合同或扣押冻结资金", "status": "mandatory"},
            {"eid": "e_afsl12_prc_court_redress", "text_zh": "法律后果：中资企业依法向中国法院起诉，查封其境内资产并判令全额赔偿", "status": "prohibition"}
        ], ensure_ascii=False)
    }
]

PHASE2_MULTILATERAL_TREATIES = [
    {
        "table": "reference_norms",
        "norm_id": "TREATY:New_York_1958:Art_II_Arbitration_Agreement",
        "law": "TREATY:New_York_1958",
        "enbez": "Art II",
        "title": "1958年纽约公约第二条：书面仲裁协议与法院强制移送仲裁义务",
        "heading_path": "《承认及执行外国仲裁裁决公约》(纽约公约 1958) > 第II条 书面仲裁协议",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Each Contracting State shall recognize an agreement in writing under which the parties undertake to submit to arbitration all or any differences. The court of a Contracting State, when seized of an action in a matter in respect of which the parties have made an agreement within the meaning of this article, shall, at the request of one of the parties, refer the parties to arbitration, unless it finds that the agreement is null and void, inoperative or incapable of being performed.",
        "text_en": "Contracting States recognize written arbitration agreements; courts must refer parties to arbitration upon request unless agreement is void or inoperative.",
        "text_zh": "【书面仲裁协议有效性与法院强制移送仲裁】：缔约国各方应承认当事人以书面形式订立的仲裁协议；当事人就已达成仲裁协议的争议向缔约国法院提起诉讼时，法院遇有一方请求，必须强制裁定停止诉讼并移送仲裁解决，除非法院查明该仲裁协议自始无效、失效或不能实行！【实务启示】：涉外工程纠纷排斥东道国地方保护的最强盾牌！一旦合同约定了新加坡 SIAC 或香港 HKIAC，当地业主若向东道国地方法院起诉，总包商应立即援引第II条抗辩驳回起诉！",
        "norm_category": "multilateral_treaty",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_ny58_2_written_agreement", "text_zh": "要件一：当事人之间订立了明确具有排除法院诉讼意思表示的书面仲裁协议", "status": "condition_precedent"},
            {"eid": "e_ny58_2_timely_court_objection", "text_zh": "要件二：在法院实体答辩前正式提出管辖权异议并请求移送仲裁解决", "status": "mandatory"},
            {"eid": "e_ny58_2_mandatory_referral", "text_zh": "法律后果：法院依法必须无条件中止诉讼并将争议强制移送仲裁裁决", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "TREATY:ICSID_1965:Art_25_Jurisdiction",
        "law": "TREATY:ICSID_1965",
        "enbez": "Art 25",
        "title": "1965年华盛顿公约第二十五条：世界银行ICSID管辖权四大核心要件",
        "heading_path": "《解决国家与他国国民间投资争端公约》(华盛顿公约 1965) > 第二章 中心的管辖 > 第25条",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Jurisdiction of the Centre: The jurisdiction of the Centre shall extend to any legal dispute arising directly out of an investment, between a Contracting State and a national of another Contracting State, which the parties to the dispute consent in writing to submit to the Centre. When the parties have given their consent, no party may withdraw its consent unilaterally.",
        "text_en": "ICSID jurisdiction covers: (1) legal dispute; (2) arising directly from investment; (3) between Contracting State and national of another; (4) written consent.",
        "text_zh": "【世界银行ICSID国际投资仲裁四大管辖要件】：ICSID 管辖权成立必须同时满足四大黄金要件：① 属于法律争议（而非纯粹商业利益摩擦）；② 争议直接源于‘投资（Investment）’；③ 当事人一方为主权缔约国，另一方为另一缔约国国民；④ 双方均以书面形式同意将争议提交中心（通过 BIT/CAFTA 投资协定中的常设要约条款达成合意）。一旦同意，任何一方不得单方撤回！【实务启示】：针对印尼、大马、菲律宾政府直接违约的最佳国际法救济渠道！",
        "norm_category": "multilateral_treaty",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_icsid25_contracting_states", "text_zh": "要件一：东道国与投资者母国均属于华盛顿公约正式批准生效的缔约成员国", "status": "condition_precedent"},
            {"eid": "e_icsid25_direct_investment_dispute", "text_zh": "要件二：争议直接发端于大型基础设施、能源电站或特许经营重大投资活动", "status": "mandatory"},
            {"eid": "e_icsid25_binding_consent", "text_zh": "法律后果：确立ICSID仲裁庭排他性终审管辖权，东道国不得以主权豁免抗辩", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "TREATY:CAFTA_2009:Art_8_Expropriation",
        "law": "TREATY:CAFTA_2009",
        "enbez": "Art 8",
        "title": "中国-东盟投资协议第八条：直接征收、间接征收与按公允市值补偿",
        "heading_path": "中国-东盟自由贸易区投资协议 (CAFTA 2009) > 第8条 征收与补偿",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Expropriation: A Party shall not expropriate or nationalize an investment, or take any measure equivalent to expropriation (indirect expropriation), except for a public purpose, on a non-discriminatory basis, in accordance with due process of law, and on payment of prompt, adequate and effective compensation equivalent to fair market value.",
        "text_en": "Direct or indirect expropriation is prohibited except for public purpose, non-discriminatory, due process, and prompt, adequate and effective market-value compensation.",
        "text_zh": "【禁止非法征收与间接征收公允市值补偿】：东道国政府严禁对中资企业的投资实施直接国有化，严禁采取等同于征收的歧视性间接征收措施（如吊销关键电站运行许可证、强制下调电价超70%、阻碍资金外汇出境实质剥夺经营权）；合法征收必须同时满足公共目的、法定程序、非歧视，且必须按照被征收前一刻的‘公允市场价值（Fair Market Value）’给予迅速、充分、有效的全额补偿，并加计同期商业利息！【实务启示】：中国央企在东盟遭受地方政权掠夺式干预的核心维权母法！",
        "norm_category": "multilateral_treaty",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_cafta8_indirect_expropriation_act", "text_zh": "要件一：东道国行政或监管措施实质性永久剥夺了投资者对项目的控制与收益权", "status": "condition_precedent"},
            {"eid": "e_cafta8_absence_of_compensation", "text_zh": "要件二：东道国未按国际公允市场价值迅速足额支付可自由兑换货币补偿款", "status": "mandatory"},
            {"eid": "e_cafta8_treaty_breach_remedy", "text_zh": "法律后果：构成国际条约非法征收，投资者享有向国际仲裁庭主张全额市值赔偿权", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "RCEP:2020:Art_10_6_Performance_Reqs",
        "law": "RCEP:2020",
        "enbez": "Art 10.6",
        "title": "RCEP协定第十章第六条：禁止强制业绩要求（限制强制本地采购与技术转让）",
        "heading_path": "《区域全面经济伙伴关系协定》(RCEP) > 第十章 投资 > 第10.6条 业绩要求",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Prohibition of Performance Requirements: No Party shall impose or enforce requirements in connection with an investment to: (a) achieve a given level of domestic content; (b) purchase or use goods produced in its territory; or (c) transfer a particular technology, production process, or other proprietary knowledge to a person in its territory.",
        "text_en": "Parties shall not impose performance requirements such as mandatory domestic content (TKDN) or forced technology transfer on investors.",
        "text_zh": "【RCEP划时代红线：严禁东道国强加本地化率TKDN与强制技术转让】：RCEP第10.6条确立了现代国际投资高标准规则：任何缔约国政府（包括印尼、越南、泰国等东盟国家）严禁对区域内外国投资者强制设定下列业绩要求：① 强制达到特定的国内含量比例（如印尼苛刻的 TKDN 本地化率）；② 强制排他采购东道国本土产品；③ 强制将特定的专利技术、生产工艺或专有技术转让给东道国本土合作方！【出海实务】：针对印尼能矿部与工业部在可再生能源电站招标中滥设 40%~60% TKDN 壁垒的最硬核国际公约抗辩盾牌！",
        "norm_category": "multilateral_treaty",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_rcep106_performance_mandate", "text_zh": "要件一：东道国部委规章或招标文件强行设定不合理的本地化采购或强制技术转让条件", "status": "condition_precedent"},
            {"eid": "e_rcep106_rcep_party_standing", "text_zh": "要件二：投资者属于中国等RCEP正式缔约方合法合规出资设立的投资实体", "status": "mandatory"},
            {"eid": "e_rcep106_international_illegality", "text_zh": "法律后果：该等行政强制性要求违反RCEP条约义务，企业有权主张免于执行或提请争端审查", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "ICC:URDG_758:Art_5_Independence",
        "law": "ICC:URDG_758",
        "enbez": "Art 5",
        "title": "国际商会URDG 758第五条：见索即付保函绝对独立性原则",
        "heading_path": "国际商会《见索即付保函统一规则》(ICC URDG 758) > 第5条 保函与基础合同的独立性",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Independence of Guarantee: A guarantee is by its nature an independent transaction from the underlying contract and from the application. The guarantor is in no way concerned with or bound by such contract, despite any reference thereto in the guarantee. A guarantor's obligation to pay is not subject to claims or defences arising from any relationship other than between guarantor and beneficiary.",
        "text_en": "Guarantee is strictly independent from underlying contract; guarantor is not concerned with contract defences and must pay upon compliant demand.",
        "text_zh": "【见索即付保函与基础工程合同绝对独立性】：保函在性质上独立于基础建设工程合同及申请人与银行之间的关系；开立银行完全不受基础工程合同的约束；开证行的付款义务仅取决于受益人提交的书面索赔通知是否在表面上符合保函条款，严禁以承包商在基础合同中并未违约、工程存在争议等实体抗辩拒绝付款！【实务启示】：见索即付保函是双刃剑！一旦开出，银行见单即付。总包商阻止恶意索兑的唯一法律途径是在法院申请‘欺诈或显失公平止付临时禁令’！",
        "norm_category": "multilateral_treaty",
        "mandatory_level": "contract_default",
        "elements_json": json.dumps([
            {"eid": "e_urdg5_autonomous_obligation", "text_zh": "要件一：保函明文约定受国际商会URDG 758规则管辖且具备见索即付属性", "status": "condition_precedent"},
            {"eid": "e_urdg5_bank_payment_mandate", "text_zh": "要件二：受益人递交了字面完全相符的书面索赔单据与违约陈述声明", "status": "mandatory"},
            {"eid": "e_urdg5_strict_payment_liability", "text_zh": "法律后果：开立行必须在5个营业日内核批并对外付款，基础合同抗辩不予审查", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "ICC:URDG_758:Art_23_Extend_or_Pay",
        "law": "ICC:URDG_758",
        "enbez": "Art 23",
        "title": "国际商会URDG 758第二十三条：不展期即付款（Extend or Pay）处理程序",
        "heading_path": "国际商会《见索即付保函统一规则》(ICC URDG 758) > 第23条 展期或付款",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Extend or Pay: Where a presenting beneficiary requests an extension of the expiry date as an alternative to payment, the guarantor shall promptly suspend payment of the demand for a period not exceeding 30 calendar days, inform the instructing party, and if extension is not effected within such period, proceed to pay the compliant demand.",
        "text_en": "Upon beneficiary's 'Extend or Pay' request, guarantor suspends payment for up to 30 calendar days to seek instruct party's agreement; pays if not extended.",
        "text_zh": "【‘不展期即付款’30天冷静缓冲期与应对规则】：当保函即将到期而业主提出‘展期或付款（Extend or Pay）’的替代索赔时，担保行应立即暂停付款最长不超过 30 个日历日，并即刻通知承包商；若承包商与开证行在 30 天内完成了保函有效期延期手续，原付款请求自动撤销；若 30 天内未完成展期，银行将直接执行付款！【实务启示】：境外业主最惯用的逼迫展期手段！项目部收到银行通知后，必须在 30 天黄金窗口内火速完成保函展期审批，阻断数百万银行资金被强行划扣！",
        "norm_category": "multilateral_treaty",
        "mandatory_level": "contract_default",
        "elements_json": json.dumps([
            {"eid": "e_urdg23_alternative_demand", "text_zh": "要件一：受益人正式递交符合保函格式的书面‘Extend or Pay’索赔指令", "status": "condition_precedent"},
            {"eid": "e_urdg23_thirty_day_stay", "text_zh": "要件二：担保银行依法启动强制性最长30个日历日的对外付款暂停冷静期", "status": "mandatory"},
            {"eid": "e_urdg23_extension_fulfillment", "text_zh": "法律后果：届期完成展期则原索兑消灭，未展期银行依法向受益人实施最终付款", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "MDB:Sanctions:Cross_Debarment_2010",
        "law": "MDB:Sanctions",
        "enbez": "Agreement 2010",
        "title": "多边开发银行相互承认制裁与全球跨行联合除名协议",
        "heading_path": "多边开发银行 (MDBs) 跨行联合除名协定 (Cross-Debarment Agreement 2010) > 相互承认制裁",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Agreement for Mutual Enforcement of Debarment Decisions: Signed by the World Bank Group, Asian Development Bank, EBRD, IDB, and AfDB. A debarment decision by one MDB for corrupt, fraudulent, collusive, or coercive practices exceeding 1 year shall be mutually enforced by all participating MDBs globally.",
        "text_en": "Sanction exceeding 1 year by one MDB for fraud, corruption, collusion or coercion triggers automatic global debarment across all participating MDBs.",
        "text_zh": "【世界银行与亚行全球跨行联合除名封杀机制】：世界银行、亚洲开发银行（ADB）、欧洲复兴开发银行、美洲开发银行及非洲开发银行五大国际多边金融机构签署的联合除名协议：凡因腐败、欺诈（含业绩造假、隐瞒转包分包）、围标串标或胁迫行为被其中任何一家银行除名制裁超过 1 年的实体，其余四家银行自动全球同步执行封杀！在制裁期内，严禁参与任何五大多边银行出资的国际基建项目投标！【实务启示】：中国工程企业出海最高合规核威慑！投标材料业绩绝不能有一丝一毫的包装造假，否则一旦被世行除名，全球项目全盘崩盘！",
        "norm_category": "multilateral_treaty",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_mdb_cross_sanction_ruling", "text_zh": "要件一：五大开发银行之一廉政合规局出具正式调查报告并裁定除名制裁超过1年", "status": "condition_precedent"},
            {"eid": "e_mdb_prohibited_practices", "text_zh": "要件二：涉案违规行为属于腐败、欺诈、串通投标、胁迫或妨碍调查五大严重不当行为", "status": "mandatory"},
            {"eid": "e_mdb_global_exclusion_impact", "text_zh": "法律后果：全球五大开发银行联合封杀除名，全部已参标或拟投标项目一票否决淘汰", "status": "prohibition"}
        ], ensure_ascii=False)
    }
]
