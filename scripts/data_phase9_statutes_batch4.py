# -*- coding: utf-8 -*-
"""Phase 9 阶梯式长尾法条扩充 - Batch 4 (实务域 10、11、12)
实务域 10: 招投标、环境影响评价(EIA/AMDAL)、海关设备进出口与反腐败
实务域 11: 破产重整(PKPU/IRDA)、清算与联营体暴雷资产隔离
实务域 12: 国际私法、商事仲裁、司法审查、主权豁免与投资条约(ISDS)
严格遵循《数据库审查.md》第五部分字段规范与 elements_json 结构化标准。
"""

import json

BATCH4_STATUTES = [
    # =========================================================================
    # 实务域 10: 招投标、环评、海关二手设备与反腐败 (L1+L2)
    # =========================================================================
    {
        "table": "reference_norms",
        "norm_id": "MDB:Cross_Debarment:Five_Practices",
        "law": "MDB:Cross_Debarment",
        "enbez": "Enforcement Framework",
        "title": "多边开发银行跨行联合除名协议：五大可制裁不当行为构成要件",
        "heading_path": "世界银行、亚洲开发银行等五大多边开发银行 (MDBs) 跨行联合除名框架协议",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Agreement for Mutual Enforcement of Debarment Decisions: Participating MDBs (World Bank, ADB, EBRD, IDB, AfDB) mutually enforce debarment decisions exceeding 1 year against entities engaging in: (1) Corrupt Practice (offering/giving anything of value to influence); (2) Fraudulent Practice (misrepresenting facts including subcontractor capacity or past credentials); (3) Collusive Practice (bid-rigging); (4) Coercive Practice; and (5) Obstructive Practice (destroying audit evidence).",
        "text_en": "MDB Cross-Debarment Agreement mutually enforces bans exceeding 1 year across World Bank, ADB, EBRD, AfDB, IDB for Corrupt, Fraudulent, Collusive, Coercive, or Obstructive practices.",
        "text_zh": "【多边开发银行（MDB）跨行联合除名与全球封杀】：世界银行、亚洲开发银行、欧洲复兴开发银行、泛美开发银行与非洲开发银行五大 MDB 签署的《相互执行除名决定协议》规定：凡被任一开发银行因实施五大不当行为之一（腐败行为、欺诈行为——含虚假申报业绩或伪造项目经理履历、串通围标行为、胁迫行为、妨碍世行审计调查行为）而处以超过 1 年除名（Debarment）制裁的企业，其他所有多边金融机构将自动在同一期间全球同步联合封杀除名！【出海实务攻防】：中国基建央国企海外投标最高红线！若投标联合体中的个别分包商或代理人存在虚报设备清单或业绩造假，一旦被世行诚信局（INT）认定构成 Fraudulent Practice，将连累整个集团母公司及其所有各级子公司在全球范围内被剥夺所有 MDB 资助项目的投标资格！",
        "norm_category": "multilateral_treaty",
        "mandatory_level": "mandatory_override",
        "elements_json": json.dumps([
            {"eid": "e_mdb_sanctionable_conduct", "text_zh": "要件一：在多边开发银行出资项目中实施腐败、造假陈述、围标串标或妨碍调查", "status": "condition_precedent"},
            {"eid": "e_mdb_sanctions_board_decision", "text_zh": "要件二：经世行或亚行制裁委员会正式裁定处以超过12个月的除名公开惩戒", "status": "mandatory"},
            {"eid": "e_mdb_global_cross_blacklist", "text_zh": "法律后果：触发五大多边金融机构全球自动联合封杀，在除名期内全面禁入任何招标", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "VN:Decision_18_2019:Art6_Used_Machinery",
        "law": "VN:Decision_18_2019",
        "enbez": "Art 6",
        "title": "越南总理第18/2019号决定：严禁进口超10年二手工程机械设备",
        "heading_path": "越南政府总理第18/2019/QD-TTg号决定 > 进口二手机械设备技术规定",
        "language_mode": "trilingual",
        "lang_original": "vi",
        "text_original": "Tiêu chí nhập khẩu máy móc, thiết bị đã qua sử dụng: Tuổi thiết bị không vượt quá 10 năm; Được sản xuất theo tiêu chuẩn phù hợp với Quy chuẩn kỹ thuật quốc gia (QCVN) về an toàn, tiết kiệm năng lượng và bảo vệ môi trường, hoặc tiêu chuẩn của các quốc gia G7 về an toàn, môi trường.",
        "text_en": "Imported used machinery and equipment must NOT exceed 10 years of age, and must comply with Vietnamese National Technical Regulations (QCVN) or G7 standards.",
        "text_zh": "【二手机械设备进口严禁超10年制造年限（出海隐蔽实务盲区）】：进口至越南的二手工程机械、发电与生产线设备，必须同时满足两大硬性技术门槛：① 设备自制造年份起算至今的“设备年龄（Age of Equipment）”绝对不得超过 10 年；② 制造标准必须符合越南国家技术规范（QCVN），或者符合 G7 国家在安全、节能与环保方面的技术标准，且清关前必须取得指定独立检验机构出具的检验合规证书！【出海实务攻防】：中资工程局出海越南，习惯将国内已完工项目的二手盾构机、大型吊车或特种拌合站调往越南工地；若该设备出厂已超过10年，即便保养良好，越南海关亦依法绝对禁止报关进口，企业将面临全额退运、高额滞港费及海关巨额行政罚款！",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory_override",
        "elements_json": json.dumps([
            {"eid": "e_vn_used_machinery_import", "text_zh": "要件一：计划调配申报进口属于已在境外使用过的二手工程施工设备与机具", "status": "condition_precedent"},
            {"eid": "e_vn_ten_year_age_limit", "text_zh": "要件二：严格核算铭牌出厂制造年份与申报年份之差不得跨越10年法定红线", "status": "mandatory"},
            {"eid": "e_vn_customs_rejection_penalty", "text_zh": "法律后果：超10年设备海关强制拒绝清关并责令限期退运，构成违禁进口行政处罚", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "MY:MACC_Act_2009:Sec17A_TRUST",
        "law": "MY:MACC_Act_2009",
        "enbez": "Sec 17A",
        "title": "马来西亚反贪污法第17A条：商业组织严格刑事责任与TRUST合规抗辩",
        "heading_path": "马来西亚2009年反贪污委员会法 (MACC Act 694) > 第IV部 腐败犯罪 > 商业机构法定义务",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Corporate Liability: A commercial organization commits an offense if a person associated with it corruptly gives, agrees to give, or offers any gratification to any person with intent to obtain or retain business or an advantage. The organization faces a fine of not less than 10 times the value of gratification or RM 1,000,000, and directors face up to 20 years imprisonment, unless the organization proves that it had in place ADEQUATE PROCEDURES (T.R.U.S.T.) to prevent such conduct.",
        "text_en": "MACC Sec 17A imposes strict corporate liability for bribery by associated persons, punishable by 10x fine or 20 years jail for directors, unless proving Adequate Procedures (T.R.U.S.T.).",
        "text_zh": "【企业反腐败严格刑事责任与董事连带坐牢（T.R.U.S.T. 防御抗辩）】：若与商业组织关联的任何人（含雇员、劳务代理人、分包商、合资伙伴）为获取或保留业务而向任何人行贿，法律直接推定该工程公司及其全体董事、高级管理人员构成刑事犯罪！处罚措施包括：不低于贿赂金额 10 倍或 100 万林吉特的巨额罚款，董事及负责人面临最高 20 年监禁！企业免于刑事定罪的唯一法定抗辩是：证明企业在事发前已实际落地并执行了符合首相署指引的‘充分反腐合规程序’（T.R.U.S.T. 体系）！【出海实务攻防】：中企在马承建工程，严禁通过所谓‘本地公关顾问’向政客或审批官员输送政治献金或回扣；中资马来分公司必须在公司内部建立完备的合规手册、举报通道与尽调档案，确保在遭遇恶意指控时能依据 T.R.U.S.T. 体系主张免责！",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory_override",
        "elements_json": json.dumps([
            {"eid": "e_my17a_corrupt_gratification", "text_zh": "要件一：公司的员工、分包商或联营体代理人为了商业项目向他人提供不当利益", "status": "condition_precedent"},
            {"eid": "e_my17a_corporate_attribution", "text_zh": "要件二：法定直接推定总包商法人机构及全体董事共同构成刑事犯罪", "status": "mandatory"},
            {"eid": "e_my17a_trust_defense", "text_zh": "法律后果：除非企业举证事前已建立并有效运行T.R.U.S.T.充分程序，否则承担双重刑罚", "status": "prohibition"}
        ], ensure_ascii=False)
    },

    # =========================================================================
    # 实务域 11: 破产重整(PKPU/IRDA)、清算与联营暴雷隔离 (L1)
    # =========================================================================
    {
        "table": "norms",
        "norm_id": "ID:UU_37_2004:Art222_PKPU",
        "law": "ID:UU_37_2004",
        "enbez": "Art 222",
        "title": "印尼破产与延期偿债法第222条：PKPU两名债权人无门槛极速冻结机制",
        "heading_path": "印尼2004年第37号破产与延期偿债法 > 第三编 延期偿付债务责任 (PKPU)",
        "language_mode": "trilingual",
        "lang_original": "id",
        "text_original": "Penundaan Kewajiban Pembayaran Utang (PKPU): Debitor yang mempunyai lebih dari 1 (satu) Kreditor dan tidak dapat atau memperkirakan tidak akan dapat melanjutkan membayar utang-utangnya yang sudah dapat ditagih, dapat memohon PKPU. Kreditor yang memperkirakan bahwa Debitor tidak dapat melanjutkan membayar utangnya juga dapat memohon agar kepada Debitor diberikan PKPU.",
        "text_en": "PKPU under Art 222: A debtor with more than 1 creditor who cannot pay due debts, or creditors thereof, may apply for PKPU, triggering automatic stay within 3 to 20 days.",
        "text_zh": "【PKPU延期偿债申请门槛与商战冻结武器】：只要债务人存在 2 名以上债权人，且其中至少存在 1 笔已到期可执行的到期债务未能偿还——法律不设最低未偿金额门槛！债务人自身或任何债权人均可直接向商事法院申请启动 PKPU（债务重组与延期清偿）；法院必须在 3 至 20 个工作日内极速裁定准许临时 PKPU；一旦裁定，即刻依法触发全面的自动诉讼与资产执行冻结令（Moratorium）！【出海实务攻防】：印尼商战中最具杀伤力的法律武器！当中资总承包商被业主恶意拖欠千万美元工程款时，可联合另一家受损材料商向商事法院极速申请对业主启动 PKPU 破产重组；业主若不提出令人满意的分期付款方案，将面临在 270 天后被法院强制宣告直接破产清盘的灭顶之灾，从而迫使其回到谈判桌！",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory_override",
        "elements_json": json.dumps([
            {"eid": "e_id222_two_creditor_rule", "text_zh": "要件一：债务人企业客观存在两名或两名以上合法债权人主体", "status": "condition_precedent"},
            {"eid": "e_id222_at_least_one_due_debt", "text_zh": "要件二：存在至少一笔已到履行期且经催告未获清偿的到期应付债务事实", "status": "mandatory"},
            {"eid": "e_id222_automatic_stay_effect", "text_zh": "法律后果：商事法院极速裁决进入PKPU状态，全面中止诉讼、执行与个别债务划扣", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "SG:IRDA_2018:Sec440_IpsoFacto",
        "law": "SG:IRDA_2018",
        "enbez": "Sec 440",
        "title": "新加坡破产与解散法第440条：Ipso Facto重整解约限制与豁免清单",
        "heading_path": "新加坡2018年破产、重组与解散法 (IRDA Act 40/2018) > 重整拯救专章 > 合同保护",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Restriction on Ipso Facto clauses: No person may terminate, amend, or claim an accelerated payment under any agreement with a company, by reason only of the company commencing proceedings for a compromise or arrangement, or being placed under judicial management. Any contractual provision permitting termination solely due to insolvency proceedings is unenforceable during the restructuring period.",
        "text_en": "IRDA Sec 440 invalidates Ipso Facto clauses terminating contracts solely due to restructuring proceedings, subject to prescribed statutory exceptions.",
        "text_zh": "【Ipso Facto 条款限制重锤与重整期间合同保护】：在新加坡进入司法管理（Judicial Management）或方案重组（Scheme of Arrangement）期间，任何交易对手严禁仅因该公司‘申请破产重整、进入司法管理或出现资不抵债事实’而单方终止合同、修改合同条款或主张债务加速到期；合同中约定一旦进入重组程序即自动解除的条款（Ipso Facto Clauses）在法定保护期间内一律不可强制执行！【出海实务攻防】：中资企业与新加坡业主签约，若合同约定‘业主申请重整时总包商有权立即解约并扣留设备’，一旦业主进入 IRDA 重整，第440条直接剥夺总包商的单方解约权！但总包商必须核查《IRDA 排除合同条例》，确认是否属于特定衍生品或豁免基建合同范围，或者以业主‘发生其他实质性欠款违约’为由行使解约权。",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory_override",
        "elements_json": json.dumps([
            {"eid": "e_sg440_restructuring_commenced", "text_zh": "要件一：新加坡公司已依法向高等法院申请批准债务和解方案或进入司法管理", "status": "condition_precedent"},
            {"eid": "e_sg440_ipso_facto_reliance", "text_zh": "要件二：相对人主张解除合同或加速到期的唯一理由系因债务人申请破产重组", "status": "mandatory"},
            {"eid": "e_sg440_unenforceability_shield", "text_zh": "法律后果：解约与加速到期主张在法定保护期内不予执行，合同依法维持有效存续", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "PH:FRIA_RA10142:Sec18_StandbyLC",
        "law": "PH:FRIA_RA10142",
        "enbez": "Sec 18",
        "title": "菲律宾财务重整法第18条：独立保函与连带保证人排除破产冻结令",
        "heading_path": "菲律宾2010年财务重整与破产法 (FRIA RA 10142) > 第二章 法院监督重整 > 冻结令范围例外",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Exceptions to Stay or Suspension Order: The Stay or Suspension Order shall not apply: (1) to the enforcement of claims against sureties and other persons solidarily liable with the debtor, and third party or accommodation mortgagors; and (2) to any form of actions of customers of the debtor to recover securities held by the debtor; and (3) to actions against letters of credit and performance bank guarantees issued by a financial institution.",
        "text_en": "FRIA Sec 18 explicitly exempts actions against sureties, third-party guarantors, and letters of credit / performance bank guarantees from the Stay Order.",
        "text_zh": "【破产重整冻结令之独立保函与连带保证人豁免】：菲律宾地区审判法院（RTC）签发的重整开始令与诉讼执行冻结令（Stay or Suspension Order），明文排除下列事项的适用：① 针对与债务人承担连带清偿责任的连带保证人（Surety / Co-debtor）及第三方抵押人的索赔追索；② 针对金融机构向受益人开立的独立信用证与履约银行保函（Standby Letters of Credit and Bank Guarantees）的索兑与兑付行为，完全不受破产冻结令的限制！【出海实务攻防】：在菲律宾承建工程，若分包商或联营伙伴向法院申请进入破产重整并取得 Stay Order，企图以此阻断总包商索兑保函，总承包商可坚决援引第18条第(3)款，指出独立保函系银行独立债务，不受重整冻结限制，开立行必须如期依令兑付！",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_ph18_fria_stay_issued", "text_zh": "要件一：菲律宾破产管辖法院已对主债务人正式签发全面诉讼与执行保全冻结令", "status": "condition_precedent"},
            {"eid": "e_ph18_independent_instrument", "text_zh": "要件二：受保护权利系金融机构向权利人开具的独立见索即付保函或第三方保证", "status": "mandatory"},
            {"eid": "e_ph18_carve_out_enforcement", "text_zh": "法律后果：银行保函与连带担保责任完全豁免于冻结令之外，债权人有权继续全额执行", "status": "prohibition"}
        ], ensure_ascii=False)
    },

    # =========================================================================
    # 实务域 12: 国际私法、商事仲裁、司法审查、主权豁免与投资条约(ISDS) (L1+L2)
    # =========================================================================
    {
        "table": "reference_norms",
        "norm_id": "TREATY:New_York_1958:Art_V",
        "law": "TREATY:New_York_1958",
        "enbez": "Art V",
        "title": "1958年纽约公约第5条：拒绝承认与执行外国仲裁裁决七项法定事由",
        "heading_path": "《承认及执行外国仲裁裁决公约》(1958年纽约公约) > 外国裁决之执行审查",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Recognition and enforcement of the award may be refused: (1) At the request of the party against whom it is invoked, if that party furnishes proof of: (a) incapacity of parties or invalidity of arbitration agreement; (b) lack of proper notice or inability to present case; (c) award deals with a difference not contemplated or beyond scope; (d) arbitral authority or procedure not in accordance with agreement; (e) award has not yet become binding or has been set aside. (2) If the competent authority finds that: (a) subject matter not capable of settlement by arbitration; (b) recognition would be contrary to public policy.",
        "text_en": "New York Convention Art V sets out the exclusive 7 grounds for refusing recognition and enforcement of foreign arbitral awards, including lack of due process and public policy violation.",
        "text_zh": "【拒绝承认执行外国仲裁裁决全球穷尽七项法定事由】：被申请人举证证明：① 仲裁协议当事人无行为能力或协议依准据法无效；② 未获得委任仲裁员或仲裁程序的适当通知，或因他故未能陈述意见（违反正当程序）；③ 裁决事项超出仲裁协议范围；④ 仲裁庭组成或仲裁程序违反当事人协议；⑤ 裁决对当事人尚无拘束力或已被仲裁地管辖法院依法撤销。法院依职权审查：⑥ 争议依该国法律不具可仲裁性；⑦ 承认或执行裁决有违该国‘公共秩序（Public Policy）’。【出海实务攻防】：在东盟 6 国执行 SIAC/ICC 或国内贸仲外国裁决，东道国法院审查权限严格受限于上述 7 项事由，严禁进行实体重审；中企应严把程序合规关，确保送达全流程存证，阻断败诉方滥用公共政策抗辩！",
        "norm_category": "multilateral_treaty",
        "mandatory_level": "mandatory_override",
        "elements_json": json.dumps([
            {"eid": "e_ny_art_v_foreign_award", "text_zh": "要件一：在非执行地国作出的符合《纽约公约》受案范围的商事仲裁裁决", "status": "condition_precedent"},
            {"eid": "e_ny_art_v_exclusive_grounds", "text_zh": "要件二：抗辩方仅得援引第5条严格列举的7项穷尽法定抗辩事由提起抗辩", "status": "mandatory"},
            {"eid": "e_ny_art_v_enforcement_order", "text_zh": "法律后果：未满足第5条撤裁抗辩条件的，东道国法院负有国际公约强制执行判令法定义务", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "TREATY:CAFTA_2009:Art14_ISDS",
        "law": "TREATY:CAFTA_2009",
        "enbez": "Art 14",
        "title": "中国-东盟投资协议第14条：中国母公司直投唯一区域多边ISDS争端解决",
        "heading_path": "《中国-东盟全面经济合作框架协议投资协议》(CAFTA 2009) > 投资者与东道国争端解决",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Settlement of Investment Disputes between a Party and an Investor of another Party (Art 14): Investor may submit a dispute to: (a) competent courts of the host Party; (b) international conciliation; (c) international arbitration under ICSID Convention (if applicable), or UNCITRAL Arbitration Rules, or any other arbitration institution agreed upon, after a 6-month consultation cooling-off period.",
        "text_en": "CAFTA Investment Agreement Art 14 provides the legal basis for Chinese parent companies to bring ISDS claims against ASEAN states via ICSID or UNCITRAL arbitration.",
        "text_zh": "【中国母公司直接投资唯一区域多边 ISDS 保护伞（纠正 ACIA 适用谬误）】：中国不是《东盟全面投资协定》(ACIA) 缔约国！中国大陆母公司直接赴东盟 6 国投资基建与能源项目，唯一能够适用的区域多边投资协定是《中国-东盟投资协议》(CAFTA Investment Agreement)！第14条确立：若东道国政府违约、征收或侵害外资，中国投资者在履行 6 个月友好磋商冷静期（Cooling-off Period）后，有权将东道国直接告上国际仲裁庭（根据东道国缔约状态选择 ICSID 或 UNCITRAL 仲裁规则）！【出海实务攻防】：系统严格区隔直投（适用 CAFTA / 双边 BIT）与通过新加坡/大马 SPV 间接投资（适用 ACIA + Art 19 实质经营审查）的管辖权路径！",
        "norm_category": "multilateral_treaty",
        "mandatory_level": "mandatory_override",
        "elements_json": json.dumps([
            {"eid": "e_cafta14_covered_investor", "text_zh": "要件一：主体为在中华人民共和国境内设立并根据中国法律运营的法人投资者", "status": "condition_precedent"},
            {"eid": "e_cafta14_six_month_cooling", "text_zh": "要件二：就东道国政府措施提出条约违约抗议并已正式履行满6个月书面磋商冷静期", "status": "mandatory"},
            {"eid": "e_cafta14_isds_tribunal", "text_zh": "法律后果：投资者享有排他性条约请求权，直接启动针对东道国政府的独立国际仲裁", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "TREATY:ACIA_2009:Art19_Denial_of_Benefits",
        "law": "TREATY:ACIA_2009",
        "enbez": "Art 19",
        "title": "东盟投资协定第19条：利益拒绝条款与SPV实质性商业运营审查",
        "heading_path": "东盟全面投资协定 (ACIA 2009) > 一般例外与管辖限制",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Denial of Benefits: A Member State may deny the benefits of this Agreement to an investor of another Member State that is an enterprise of that other Member State and to investments of that investor if: (a) the enterprise is owned or controlled by persons of a non-Member State; and (b) the enterprise has NO SUBSTANTIAL BUSINESS OPERATIONS in the territory of the Member State under whose law it is constituted.",
        "text_en": "ACIA Art 19 allows a host state to deny treaty benefits to an ASEAN SPV owned by non-ASEAN (e.g. Chinese) investors if the SPV has NO substantial business operations.",
        "text_zh": "【利益拒绝条款（Denial of Benefits）与 SPV 离岸空壳刺破风险】：东道国成员国有权对另一东盟成员国的企业投资者拒绝给予本协定项下的全部投资保护待遇，如果：(a) 该企业最终由非东盟成员国（如中国）的自然人或法人实际拥有或控制；且 (b) 该企业在其设立地成员国（如新加坡或马来西亚）境内‘无实质性商业运营（No Substantial Business Operations）’！【出海实务攻防】：中资企业搭建‘中国母公司 -> 新加坡 SPV -> 印尼/越南电站项目’架构以图适用 ACIA 优惠保护时，新加坡 SPV 决不能仅仅是一个信箱式空壳（Letterbox Company）！必须在新加坡租赁实际办公场所、聘用常驻管理人员、开展实质商业流水运营，否则东道国政府在 ISDS 仲裁中可随时援引第19条阻断全部条约管辖权！",
        "norm_category": "multilateral_treaty",
        "mandatory_level": "mandatory_override",
        "elements_json": json.dumps([
            {"eid": "e_acia19_non_asean_ownership", "text_zh": "要件一：新加坡或大马SPV项目公司最终由非东盟国（如中国大陆）实际控制人穿透持有", "status": "condition_precedent"},
            {"eid": "e_acia19_lack_substantial_operations", "text_zh": "要件二：该SPV在注册地缺乏实体办公室、员工、真实业务支出等实质商业运营要素", "status": "mandatory"},
            {"eid": "e_acia19_denial_of_treaty", "text_zh": "法律后果：东道国有权依法激活第19条拒绝给予条约保护，国际仲裁庭驳回管辖权", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "VN:Civil_Procedure_2015:Art440_No_Merits_Review",
        "law": "VN:Civil_Procedure_2015",
        "enbez": "Art 440",
        "title": "越南民事诉讼法第440条：法院承认执行外国仲裁裁决严禁实体重审",
        "heading_path": "越南2015年民事诉讼法典 (Law 92/2015/QH13) > 第三十五章 承认与执行外国仲裁裁决程序",
        "language_mode": "trilingual",
        "lang_original": "vi",
        "text_original": "Khi xét đơn yêu cầu, Hội đồng xét đơn không được xét xử lại nội dung tranh chấp mà chỉ kiểm tra tính hợp pháp của phán quyết trọng tài nước ngoài theo các căn cứ quy định tại Điều 439 của Bộ luật này để ra quyết định.",
        "text_en": "When considering an application, the Court panel SHALL NOT re-examine the substantive merits of the dispute, but solely review legal grounds under Article 439.",
        "text_zh": "【法院司法审查严禁实体重审（No Merits Review）法定义务】：越南人民法院在组成三人合议庭审理承认与执行外国仲裁裁决（如 SIAC、ICC 或 VIAC 涉外裁决）申请时，合议庭法律上绝对严禁对当事人基础争议的实体内容进行重新实体审理或再审（Không được xét xử lại nội dung tranh chấp）；法院仅得严格依照本法典第439条（对齐纽约公约第5条）穷尽列举的程序性合法要件实施司法合规核验！【出海实务攻防】：越南司法实践中，败诉的越南国有业主往往企图向越南高级法院哭诉‘裁决在事实认定或赔偿金额计算上存在重大错误’以阻挠执行；中资胜诉方可依据第440条刚性条款，当庭申请法官依法排除对实体事实争议的纠缠，强制推进裁决承认令与执行令签发！",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory_override",
        "elements_json": json.dumps([
            {"eid": "e_vn440_foreign_award_application", "text_zh": "要件一：胜诉方已依法向越南有管辖权的高级人民法院提交裁决承认与执行申请书", "status": "condition_precedent"},
            {"eid": "e_vn440_prohibition_substantive_review", "text_zh": "要件二：法律强制禁止越南主审法官对仲裁庭认定的事实与证据说理重新审判", "status": "mandatory"},
            {"eid": "e_vn440_recognition_order", "text_zh": "法律后果：裁决合法性仅依第439条程序审查，程序无瑕疵的必须无条件签发执行命令", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "SG:IAA_Cap_143A:Sec12A_Interim_Injunction",
        "law": "SG:IAA_Cap_143A",
        "enbez": "Sec 12A",
        "title": "新加坡国际仲裁法第12A条：高院与仲裁庭签发全球资产冻结与保函止付令",
        "heading_path": "新加坡国际仲裁法 (IAA Cap 143A) > 第II部 国际商事仲裁 > 法院支持仲裁之临时保全措施",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Court-ordered interim measures: The General Division of the High Court has power to make orders on interim measures for the purpose of and in relation to an arbitration, including: (a) orders for preserving, custody or sale of property; (b) restraining the dissipation of assets (Worldwide Mareva Injunction); and (c) interim injunctions including restraining call on performance guarantees or letters of credit.",
        "text_en": "Singapore IAA Sec 12A empowers the High Court to issue interim injunctions, including Worldwide Mareva asset freezes and injunctions restraining calls on guarantees.",
        "text_zh": "【法院与仲裁庭签发临时禁令与保函止付权限（Sec 12A 全球保全权）】：新加坡高等法院普通分院有权针对国内外正在进行或即将进行的国际仲裁签发具有法定执行力的临时保全措施命令，包括：(a) 现场工程财产、图纸材料的保全与强制扣押；(b) 全球资产冻结令（Worldwide Mareva Injunction，严禁对方转移隐匿全球账户资金）；(c) 临时禁制令，包括在符合显失公平或欺诈标准时签发‘紧急止付独立履约保函或信用证的司法禁令’！【出海实务攻防】：在东盟工程争议发生时，若东道国业主企图恶意索兑由新加坡银行开出的数千万美元见索即付履约保函，中资企业可在向 SIAC 提起仲裁的同时，依据第12A条在 24~48 小时内向新加坡高院紧急申请单方面保函止付禁令（Ex-parte Injunction），强行阻断银行资金划转！",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_sg12a_arbitration_nexus", "text_zh": "要件一：争议属于提交或拟提交新加坡SIAC、ICC等机构之合法有效国际商事仲裁", "status": "condition_precedent"},
            {"eid": "e_sg12a_prima_facie_case", "text_zh": "要件二：申请人证明存在显失公平、资产转移紧迫风险或不可弥补损害之强表面证据", "status": "mandatory"},
            {"eid": "e_sg12a_binding_injunction", "text_zh": "法律后果：法院依法签发具备全球强制执行威慑力的司法禁制令或保函立即止付令", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "PH:EO_1008:Sec4_CIAC_Exclusive",
        "law": "PH:EO_1008",
        "enbez": "Sec 4",
        "title": "菲律宾建筑业仲裁法第4条：CIAC强制排他管辖权与排除境外仲裁",
        "heading_path": "菲律宾建筑业仲裁法 (Executive Order No. 1008) > 菲律宾建筑业仲裁委员会管辖权",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Jurisdiction: The Construction Industry Arbitration Commission (CIAC) shall have original and EXCLUSIVE JURISDICTION over disputes arising from, or in connection with, contracts entered into by parties involved in construction in the Philippines, whether government or private, provided the parties agree to submit the dispute to voluntary arbitration. The jurisdiction of the CIAC may include but is not limited to violation of specifications, delay, maintenance and defects, and default.",
        "text_en": "CIAC possesses ORIGINAL AND EXCLUSIVE JURISDICTION over all construction disputes in the Philippines if there is an arbitration agreement, effectively overriding foreign forums.",
        "text_zh": "【菲律宾 CIAC 建筑仲裁强制原始排他管辖权（重大涉外管辖陷阱）】：凡在菲律宾境内发生的一切建设工程合同争议（无论是政府项目还是私人工程），只要当事人在合同中存在任何同意将争议提交仲裁解决的意思表示，菲律宾建筑业仲裁委员会（CIAC）依法享有原始且排他的绝对管辖权（Original and Exclusive Jurisdiction）！【出海实务攻防】：菲律宾涉外工程争议解决最大深水区！中企若在菲工程合同中约定‘争议提交新加坡 SIAC 或瑞士 ICC 仲裁’，在菲律宾最高法院大法庭判例体系下（如 Global Medical 案、PCAB 案），菲本土业主若直接向马尼拉 CIAC 起诉，CIAC 将强制确认其享有排他管辖权，即便有明确的境外仲裁约定亦不能对抗 CIAC 的法定管辖权！承包商必须提前布局双重管辖应对策略！",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory_override",
        "elements_json": json.dumps([
            {"eid": "e_ph_ciac_construction_dispute", "text_zh": "要件一：争议标的产生于在菲律宾境内实施的公共或私营建设工程项目活动", "status": "condition_precedent"},
            {"eid": "e_ph_ciac_arbitration_agreement", "text_zh": "要件二：合同文本中载有任何形式的将争议提交仲裁解决的书面合意条款", "status": "mandatory"},
            {"eid": "e_ph_ciac_exclusive_jurisdiction", "text_zh": "法律后果：CIAC依法强制享有原始且排他的法定裁判管辖权，阻断普通境外仲裁抗辩", "status": "prohibition"}
        ], ensure_ascii=False)
    }
]
