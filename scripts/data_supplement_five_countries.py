# -*- coding: utf-8 -*-
"""东盟其余五国（柬埔寨 KH、老挝 LA、缅甸 MM、文莱 BN、东帝汶 TL）法律与案例数据
包含：
1. 真实已颁布成文法条（投资法、民法典、建设工程法、外汇法、仲裁法、主权豁免）
2. 国际条约与双边协议
3. 标杆司法裁判与投资仲裁裁决（德式四要素严格达标）
"""

SUPPLEMENT_FIVE_NORMS_L1 = [
    # ---------------- 柬埔寨 (asean_kh) ----------------
    {
        "norm_id": "KH:Law_on_Investment_2021:Art8_12_QIP_Incentives",
        "law": "Law on Investment of the Kingdom of Cambodia 2021",
        "enbez": "Article 8-12",
        "title": "新投资法合格投资项目(QIP)注册与免税激励",
        "heading_path": "Law on Investment 2021 | Chapter 3 Qualified Investment Projects (QIP)",
        "text_zh": "【中文释义】柬埔寨2021年新投资法设立合格投资项目（QIP）制度。凡在清洁能源、高新技术、重大基础设施、物流园区及出口导向型制造业投资的中资企业，向柬埔寨发展理事会（CDC）注册并取得终审登记证书（FRC）后，依法享有自首次产生收入之日起最长9年的企业所得税（CIT）免税期，或享有特别折旧与增强型生产性费用加计扣除激励。",
        "text_en": "Investment projects registered as QIP with the Council for the Development of Cambodia (CDC) are entitled to income tax exemption for up to 9 years from the date of first earnings, or special depreciation plus additional deduction incentives.",
        "text_original": "គម្រោងវិនិយោគមានលក្ខណៈសម្បត្តិគ្រប់គ្រាន់ (គ.ល.គ.) ទទួលបានការលើកលែងពន្ធលើប្រាក់ចំណូលក្នុងរយៈពេលរហូតដល់ ៩ ឆ្នាំ គិតចាប់ពីពេលទទួលបានប្រាក់ចំណូលលើកដំបូង។",
        "language_mode": "trilingual",
        "norm_category": "mandatory_statute",
        "elements_json": '{"subject": "赴柬投资大型工业与基建企业", "trigger": "向CDC申报QIP合格投资项目", "requirements": ["投资领域属于法定鼓励目录", "通过CDC一站式投资服务窗口审查", "取得FRC终审登记证书"], "legal_effect": "依法享有最长9年CIT免税及进口生产设备原辅料免征关税与增值税"}'
    },
    {
        "norm_id": "KH:Law_on_Investment_2021:Art16_Land_Ownership_Lease",
        "law": "Law on Investment of the Kingdom of Cambodia 2021",
        "enbez": "Article 16",
        "title": "新投资法土地所有权外资红线与最长50年长期租赁",
        "heading_path": "Law on Investment 2021 | Chapter 4 Use of Land",
        "text_zh": "【中文释义】外资法人严禁拥有柬埔寨土地永久所有权（土地所有权仅限柬籍自然人或柬资持股51%以上的柬埔寨法人拥有）。但外资企业依法有权取得最长50年（可续期50年）的国家或私人土地长期租赁权（Perpetual Lease），并在该租赁土地上合法拥有建筑物、厂房及构筑物的独立产权，该长期租赁权经国土部登记后可设定抵押（Hypothec）用于银行项目融资。",
        "text_en": "Foreign natural persons and legal entities cannot hold title to land in Cambodia. However, foreign investors may use land through perpetual leases for up to 50 years (renewable for another 50 years) and own immovable assets built thereon.",
        "text_original": "ការប្រើប្រាស់ដីធ្លីដោយវិនិយោគិនបរទេសត្រូវបានអនុញ្ញាតតាមរយៈការជួលរយៈពេលវែងរហូតដល់ ៥០ ឆ្នាំ ហើយអាចបន្តបាន ៥០ ឆ្នាំទៀត។",
        "language_mode": "trilingual",
        "norm_category": "mandatory_statute",
        "elements_json": '{"subject": "外资投建营及园区开发企业", "trigger": "取得工业厂房与基础设施用地", "requirements": ["严守禁止直接持有土地永久所有权红线", "在国土规划建设部登记长期租赁权（Perpetual Lease）", "办理地上建筑物独立不动产权属证书"], "legal_effect": "长期租赁权确立为独立他物权，可依法转让、继承及设定融资抵押"}'
    },
    {
        "norm_id": "KH:Civil_Code_2007:Art403_Liquidated_Damages_Non_Reduction",
        "law": "Civil Code of the Kingdom of Cambodia 2007",
        "enbez": "Article 403",
        "title": "民法典违约金不可酌减原则与日本旧法传统",
        "heading_path": "Civil Code 2007 | Book 4 Obligations | Chapter 3 Remedies for Breach | Article 403",
        "text_zh": "【中文释义】柬埔寨民法典由日本法学专家主导起草，第403条明确规定：合同当事人可以事先约定债务不履行时的损害赔偿额（违约金 Liquidated Damages）。法院原则上无权增加或减少当事人约定的违约金金额！这一刚性原则与泰国、菲律宾法院享有违约金衡平酌减权的传统形成鲜明反差。在柬签署EPC合同时，总承包商若接受过高的工期延误违约金条款，法官绝无权进行衡平扣减！",
        "text_en": "Under Article 403 of the Cambodian Civil Code, parties may agree in advance upon liquidated damages. The court has no power to increase or reduce the agreed liquidated damages, upholding strict freedom of contract.",
        "text_original": "កាលបើភាគីបានព្រមព្រៀងគ្នាកំណត់ប្រាក់សំណងការខូចខាតទុកជាមុន តុលាការមិនអាចបង្កើន ឬបន្ថយចំនួនទឹកប្រាក់នោះបានឡើយ។",
        "language_mode": "trilingual",
        "norm_category": "mandatory_statute",
        "elements_json": '{"subject": "EPC总包合同当事人", "trigger": "工期延误或质量违约被主张违约金", "requirements": ["合同含有明确违约金约定条款", "违约金约定不违反公序良俗等绝对无效事由"], "legal_effect": "法官必须全额判决支持约定违约金金额，绝对无权依据实际损失过低而依职权酌减"}'
    },
    {
        "norm_id": "KH:Law_on_Construction_2019:Art38_Construction_Permit",
        "law": "Law on Construction 2019",
        "enbez": "Article 38 & 73",
        "title": "建筑法施工许可证前置审批与10年法定结构质保",
        "heading_path": "Law on Construction 2019 | Chapter 6 Construction Permits & Chapter 11 Liability",
        "text_zh": "【中文释义】在柬埔寨开展任何建设工程，必须在开工前向国土规划建设部（MLMUPC）或省级政府申领合规的开工许可证（Construction Permit）。无证施工将面临勒令停工、没收施工设备、拆毁构筑物及巨额行政罚款。第73条特别确立：建筑工程主体结构及地基工程享有法定的10年质量保证期，总承包商与设计院对结构缺陷承担法定的终身与连带赔偿责任。",
        "text_en": "Construction without a valid Construction Permit from MLMUPC is prohibited and subject to demolition and fines. Article 73 establishes a mandatory 10-year defect liability period for structural works binding contractors and designers solidarily.",
        "text_original": "រាល់ការដ្ឋានសាងសង់ត្រូវតែមានលិខិតអនុញ្ញាតសាងសង់ជាមុនសិន។ អ្នកម៉ៅការសាងសង់ត្រូវទទួលខុសត្រូវរយៈពេល ១០ ឆ្នាំ លើគុណភាពនិងសុវត្ថិភាពសំណង់។",
        "language_mode": "trilingual",
        "norm_category": "mandatory_statute",
        "elements_json": '{"subject": "在柬施工总包与建筑设计单位", "trigger": "工程开工前置审批与竣工后主体结构质量责任", "requirements": ["获得MLMUPC签发之有效开工证", "主体结构质保期不得低于10年法定标准"], "legal_effect": "无证施工导致合同自始不合法面临停工重罚；10年内主体开裂倒塌承包商承担绝对赔偿责任"}'
    },

    # ---------------- 老挝 (asean_la) ----------------
    {
        "norm_id": "LA:Investment_Promotion_Law_2016:Art4_32_Concession_Business",
        "law": "Law on Investment Promotion No. 14/NA 2016",
        "enbez": "Article 4 & 32-45",
        "title": "投资促进法特许经营业务(CA)一站式审批与国会核准",
        "heading_path": "Law on Investment Promotion 2016 | Part IV Concession Business",
        "text_zh": "【中文释义】老挝将外商投资划分为一般业务与特许经营业务（Concession Business）。凡涉及水电清洁能源、特高压输电、矿产开采加工、经济特区开发及重大交通基建，属于特许经营业务，必须向老挝计划投资部（MPI）一站式投资协调窗口申报，并签署特许经营协议（Concession Agreement, CA）。特许期限最长50年，涉及重大国土资源利用的特许合同还必须依法提交老挝国会（National Assembly）审议批准。",
        "text_en": "Concession businesses covering hydropower, mining, SEZs, and public infrastructure require application through MPI One-Stop-Service and signing of a Concession Agreement (CA). Major concession projects must obtain approval from the National Assembly.",
        "text_original": "ທຸລະກິດສໍາປະທານ ແມ່ນ ການລົງທຶນທີ່ໄດ້ຮັບອະນຸຍາດຈາກລັດຖະບານ ເພື່ອພັດທະນາ ແລະ ດໍາເນີນທຸລະກິດ ຕາມສັນຍາສໍາປະທານ.",
        "language_mode": "trilingual",
        "norm_category": "mandatory_statute",
        "elements_json": '{"subject": "出海老挝水电流域与矿山开发联合体", "trigger": "申请老挝大型能源与特许基础设施投资", "requirements": ["向MPI一站式办公室申报并签署CA特许协议", "大型战略项目完成老挝国会法定批准批复"], "legal_effect": "特许经营协议在老挝具有准法律地位，受国家不征收与征用公平赔偿承诺保障"}'
    },
    {
        "norm_id": "LA:Foreign_Currency_Law_2022:Art15_Mandatory_Repatriation_Approval",
        "law": "Law on Foreign Currency Management No. 15/NA 2022",
        "enbez": "Article 15 & BOL Decrees",
        "title": "外汇管理法出口外币强制回流与借款央行(BOL)批准红线",
        "heading_path": "Law on Foreign Currency Management No. 15/NA 2022 | Chapter III Bank Accounts and Foreign Loans",
        "text_zh": "【中文释义】中资在老挝投建营面临的头号外汇生死线！第15条及老挝央行（BOL）实施细则明确规定：所有在老挝注册的外资企业，其在境外获得的出口创汇、工程款及境外股东借款，必须强制全额回流至老挝境内的商业银行外币账户。外资企业向境外母公司或国际银团借入离岸外债，必须事先向老挝央行（BOL）申请并取得《外债登记批准证书》（BOL Certificate），否则到期商业银行依法绝对禁止购汇汇出还本付息！",
        "text_en": "All foreign-invested enterprises in Laos must open bank accounts with domestic banks in Laos and repatriate revenue. Offshore foreign loans must obtain prior registration and approval certificate from the Bank of the Lao PDR (BOL) to enable legal debt service remittance.",
        "text_original": "ນິຕິບຸກຄົນ ທີ່ກູ້ຢືມເງິນຈາກຕ່າງປະເທດ ຕ້ອງຂຶ້ນທະບຽນ ແລະ ໄດ້ຮັບການອະນຸມັດ ຈາກທະນາຄານແຫ່ງ ສປປ ລາວ ກ່ອນການໂອນເງິນ.",
        "language_mode": "trilingual",
        "norm_category": "mandatory_statute",
        "elements_json": '{"subject": "在老挝设立项目公司之出海企业及放贷行", "trigger": "境外股东借款、项目融资跨境还本付息与利润汇出", "requirements": ["在老挝商业银行开设专属资本外汇账户", "向老挝央行BOL办理外债事先核准登记手续", "完税后凭BOL批复办理购汇对外支付"], "legal_effect": "未经BOL事前核准的外债在老挝法律下属于非法外汇交易，资金无法合法汇出境"}'
    },

    # ---------------- 缅甸 (asean_mm) ----------------
    {
        "norm_id": "MM:Myanmar_Investment_Law_2016:Sec50_Land_Lease_70_Years",
        "law": "Myanmar Investment Law 2016",
        "enbez": "Section 50",
        "title": "投资法MIC许可长期土地租赁最长70年法定通道",
        "heading_path": "Myanmar Investment Law 2016 (Pyidaungsu Hluttaw Law No. 40/2016) | Chapter XII Right to Use Land",
        "text_zh": "【中文释义】突破《1987年不动产转让限制法》外国人租地不得超过1年的绝对禁令：凡取得缅甸投资委员会（MIC）核发的 MIC 许可（MIC Permit）或 MIC 背书（MIC Endorsement）的外资企业，依法享有向政府或持有所有权的本地自然人长期租赁土地的法定特权，租期最长可达50年，期满后可申请连续顺延两次各10年（即最长累计50+10+10=70年），为中资大型油气深水港与园区开发提供根本保障。",
        "text_en": "Any foreign investor who obtains a MIC Permit or Endorsement has the right to obtain a long-term lease of land or buildings initially up to 50 years, and extendable for two consecutive periods of 10 years each (up to 70 years in total).",
        "text_original": "ကော်မရှင်၏ ခွင့်ပြုမိန့် သို့မဟုတ် အတည်ပြုမိန့် ရရှိသော ရင်းနှီးမြှုပ်နှံသူသည် မြေ သို့မဟုတ် အဆောက်အအုံကို နှစ် ၅၀ အထိ စတင်ငှားရမ်းခွင့်ရှိပြီး ၁၀ နှစ်စီ နှစ်ကြိမ် သက်တမ်းတိုးနိုင်သည်။",
        "language_mode": "bilingual",
        "norm_category": "mandatory_statute",
        "elements_json": '{"subject": "在缅开展工业园区、交通与港口投资之企业", "trigger": "办理长期土地租赁协议与抵押", "requirements": ["取得MIC投资许可证或背书证书", "向土地记录局办理长期租赁登记备案"], "legal_effect": "依法豁免1987年不动产转让限制法一年禁令，锁定最长70年合法土地用益物权"}'
    },
    {
        "norm_id": "MM:Contract_Act_1872:Sec56_Frustration",
        "law": "Myanmar Contract Act 1872",
        "enbez": "Section 56",
        "title": "合同法合同受阻/落空原则与不可抗力免责界限",
        "heading_path": "Myanmar Contract Act 1872 | Chapter IV Of the Performance of Contracts | Section 56",
        "text_zh": "【中文释义】源自普通法的根本原则：当事人在缔约后，由于发生不可预见且无法避免的客观事态（如武装冲突政变、港口严密封锁、国际制裁禁令），使得合同标的在客观事实上或在法律上已经变得不可能履行（Impossible）或违法（Unlawful）时，该合同在受阻事由发生之日起依法当然落空终止（Becomes Void）。但在商业上仅因通货膨胀或汇率暴跌导致履约成本急剧上升，并不构成 Section 56 合同受阻免责。",
        "text_en": "Under Section 56 of the Contract Act 1872, a contract to do an act which, after the contract is made, becomes impossible, or, by reason of some event which the promisor could not prevent, unlawful, becomes void when the act becomes impossible or unlawful.",
        "text_original": "A contract to do an act which, after the contract is made, becomes impossible, or, by reason of some event which the promisor could not prevent, unlawful, becomes void when the act becomes impossible or unlawful.",
        "language_mode": "bilingual",
        "norm_category": "mandatory_statute",
        "elements_json": '{"subject": "在缅甸履约之工程与贸易当事人", "trigger": "遭遇军事管制、不可抗力罢工或制裁禁令导致无法施工", "requirements": ["证明履约已达到客观物理不可能或法律禁止程度", "未受合同自身风险分配明示排除"], "legal_effect": "合同自事态确立之日起自动终止，免除后续履约义务，清算已完工程合理对价"}'
    },
    {
        "norm_id": "MM:FEML_2012_CBM_Notification_12_2022:Foreign_Exchange_Control",
        "law": "Foreign Exchange Management Law 2012 & CBM Notifications",
        "enbez": "Section 38 & CBM Notification 12/2022",
        "title": "外汇管理法1日内强制结汇与外汇监督委员会(FESC)逐笔审批",
        "heading_path": "Foreign Exchange Management Law 2012 | CBM Directives on Mandatory Conversion",
        "text_zh": "【中文释义】缅甸自2022年起实施极其严苛的外汇管制：境内居民及外资非豁免企业收到的所有经常项目及资本项目外币收入，必须在收到款项之日起1个工作日内（One Business Day）按缅甸央行（CBM）官方固定指导牌价强制结汇为缅币（Kyat）。外资企业偿还境外外债、支付离岸工程采购款或汇出股息，必须事先提交详尽单证向联邦外汇监督委员会（FESC）申请逐笔严格审批，未经 FESC 批复商业银行严禁对外汇出美元！",
        "text_en": "Foreign currency income received by entities must be converted into Myanmar Kyat within 1 business day at the CBM reference rate. Outbound foreign exchange transfers for loans, imports, and dividends require prior case-by-case approval from the Foreign Exchange Supervisory Committee (FESC).",
        "text_original": "နိုင်ငံခြားသုံးငွေများအား မြန်မာကျပ်ငွေဖြင့် ၁ ရက်အတွင်း မဖြစ်မနေ လဲလှယ်ရမည်။ နိုင်ငံခြားသို့ လွှဲပြောင်းရန်အတွက် FESC ၏ ကြိုတင်ခွင့်ပြုချက် လိုအပ်သည်။",
        "language_mode": "bilingual",
        "norm_category": "mandatory_statute",
        "elements_json": '{"subject": "出海缅甸央国企总包项目部", "trigger": "收取工程进度款、偿还离岸采购借款与汇出利润", "requirements": ["外币入账1个工作日内依令结汇", "向FESC提交逐笔真实性出境支付申请"], "legal_effect": "未获FESC特批前美元资金被实质冻结在缅甸境内，强制以缅币官方汇率锁定"}'
    },

    # ---------------- 文莱 (asean_bn) ----------------
    {
        "norm_id": "BN:Constitution:Art84C_Absolute_Sovereign_Immunity",
        "law": "Constitution of Brunei Darussalam",
        "enbez": "Article 84C",
        "title": "文莱宪法第84C条政府绝对主权豁免敏感红线",
        "heading_path": "Constitution of Brunei Darussalam | Part XI Miscellaneous | Article 84C",
        "text_zh": "【中文释义】文莱出海投资与基建总包最致命的特殊宪制红线：文莱宪法第84C条确立了国家元首（苏丹）及文莱政府机关享有绝对的主权豁免（Absolute Sovereign Immunity）。文莱国内法绝对禁止任何人在文莱国内法院以任何诉由对文莱苏丹或文莱政府提起民事诉讼！因此，中资企业与文莱政府部门或公用事业机构签署基建、石化项目合同时，必须在合同中明确约定适用境外离岸仲裁（如新加坡 SIAC 或国际商会 ICC），并载明文莱政府明确放弃主权豁免条款（Waiver of Sovereign Immunity），否则国内维权无门。",
        "text_en": "Under Article 84C of the Constitution of Brunei, the Sultan and the Government of Brunei enjoy absolute immunity from any suit or proceedings in any court in Brunei. Commercial contracts with the Brunei Government must stipulate offshore arbitration (e.g. SIAC) with explicit sovereign immunity waivers.",
        "text_original": "No action or proceedings whatsoever shall be brought or maintained in any court against His Majesty the Sultan or against the Government of Brunei Darussalam.",
        "language_mode": "bilingual",
        "norm_category": "mandatory_statute",
        "elements_json": '{"subject": "与文莱政府或部委签约之中资总承包商", "trigger": "起草EPC合同、特许经营协议及主权担保函", "requirements": ["严禁选择文莱国内法院诉讼管辖", "必须指定新加坡SIAC或英国离岸国际仲裁", "起草不可撤销放弃主权与执行豁免之标准条款"], "legal_effect": "未约定境外仲裁将导致争议在文莱国内因宪法第84C条被全案驳回且终局无救济"}'
    },
    {
        "norm_id": "BN:Contracts_Act_Cap106:Sec74_75_Reasonable_Compensation",
        "law": "Contracts Act (Cap. 106)",
        "enbez": "Section 74 & 75",
        "title": "文莱合同法违约损害赔偿与违约金合理补偿原则",
        "heading_path": "Contracts Act (Cap. 106) | Part VI Consequences of Breach of Contract | Section 74-75",
        "text_zh": "【中文释义】文莱合同法与马来西亚《1950年合同法》同出一源。Section 74 确立了普通法 Hadley v Baxendale 违约赔偿两分法规则（可预见性原则）。Section 75 规定：若合同事先约定了违约金金额（Liquidated Damages），守约方无论是否能证明其实际遭受损失，法院仅有权在其约定的违约金限额以内，判处其认为合理之补偿金额（Reasonable Compensation）。过分超出合理损失的高额违约金在文莱法院将被认定属于惩罚性条款（Penalty）而不予执行。",
        "text_en": "Under Section 75 of Brunei Contracts Act (Cap. 106), when a contract has been broken, if a sum is named as liquidated damages, the party complaining is entitled to receive reasonable compensation not exceeding the amount so named, whether actual damage is proved or not.",
        "text_original": "When a contract has been broken, if a sum is named in the contract as the amount to be paid in case of such breach, the party complaining of the breach is entitled to receive from the party who has broken the contract reasonable compensation not exceeding the amount so named.",
        "language_mode": "bilingual",
        "norm_category": "mandatory_statute",
        "elements_json": '{"subject": "文莱工程业主与总分包商", "trigger": "延误工期违约金扣款或索赔", "requirements": ["合同含有事先约定的违约金条款", "索赔方负有举证合理损失构成的初步责任"], "legal_effect": "法院对明显过高的惩罚性违约金依职权下调至合理补偿范围"}'
    },

    # ---------------- 东帝汶 (asean_tl) ----------------
    {
        "norm_id": "TL:Law_9_2011_Budget_Management:Fiscalizacao_Previa_Visto",
        "law": "Law No. 9/2011 & High Administrative Tax and Audit Court Law",
        "enbez": "Article 12-15 jo. Law 9/2011",
        "title": "财政管理法国家审计院事前合法性签证(Visto)生死线",
        "heading_path": "Law No. 9/2011 on the High Administrative, Tax and Audit Court | Prior Audit (Fiscalização Prévia)",
        "text_zh": "【中文释义】东帝汶工程承包第一大生死红线：凡涉及东帝汶国家财政资金超过50万美元（USD 500,000）的政府基建合同、总承包补充协议或工程追加款，在签署后必须呈报东帝汶高等行政税务审计法院（Câmara de Contas）进行事前合法性审查（Fiscalização Prévia）并取得正式审计签证（Visto）。在审计法院正式签发 Visto 签证之前，该合同不得产生任何财务效力！承包商未见 Visto 抢先开工的，政府财政部依法绝对禁止拨付任何款项，且承包商无权主张垫资利息补偿！",
        "text_en": "Public contracts exceeding USD 500,000 are subject to mandatory prior audit (Fiscalização Prévia) by the Câmara de Contas. No contract shall produce financial effects or permit public payments until a clearance visa (Visto) is granted. Premature construction is strictly non-reimbursable.",
        "text_original": "Os atos e contratos sujeitos a fiscalização prévia da Câmara de Contas não produzem efeitos financeiros antes de visados. A recusa do visto impede a produção de quaisquer efeitos do contrato.",
        "language_mode": "trilingual",
        "norm_category": "mandatory_statute",
        "elements_json": '{"subject": "承揽东帝汶公共道路、电网与港口总承包商", "trigger": "与东帝汶部委签署公共工程EPC合同或重大变更协议", "requirements": ["核实合同金额是否超50万美元强审门槛", "督促业主向Câmara de Contas呈报全套招标审批案卷", "取得正式载有Visto登记号之核准判决书"], "legal_effect": "未取得Visto签证前合同处于法定未生效状态，财政部拒绝拨付任何预付款与工程款"}'
    },
    {
        "norm_id": "TL:Civil_Code_2011:Art1145_Five_Year_Structure_Liability",
        "law": "Civil Code of Timor-Leste (Law No. 10/2011)",
        "enbez": "Artigo 1145",
        "title": "民法典承揽工程建筑物5年倒塌与结构瑕疵连带责任",
        "heading_path": "Civil Code of Timor-Leste | Book II Law of Obligations | Contract for Work (Empreitada) | Article 1145",
        "text_zh": "【中文释义】东帝汶民法典以葡萄牙民法典为蓝本。第1145条专门规定长期建筑物之瑕疵担保：在涉及长期不动产工程（如桥梁、公路、港口与高层建筑）中，自竣工验收交付之日起5年内，若因土壤地质缺陷或建筑缺陷导致工程全部或部分倒塌、或者出现明显严重的结构毁损危害，总承包商对发包人及第三受让人承担无过错的法定赔偿责任。受害人必须在知晓瑕疵后1年内发出通知并在通知后1年内提起诉讼。",
        "text_en": "Under Article 1145 of Timor-Leste Civil Code, for buildings or long-term immovable works, the contractor is liable for 5 years after delivery if the work collapses entirely or partially, or shows serious defects due to ground or construction flaws.",
        "text_original": "Se a empreitada tiver por objeto a construção de edifícios ou outros imóveis destinados por sua natureza a longa duração, o empreiteiro é responsável pelo prejuízo se, no decurso de cinco anos a contar da entrega, a obra ruir total ou parcialmente.",
        "language_mode": "trilingual",
        "norm_category": "mandatory_statute",
        "elements_json": '{"subject": "东帝汶基础设施总承包商", "trigger": "工程交付后5年内出现严重结构裂缝或沉降", "requirements": ["缺陷属于主体地基或重大结构瑕疵", "发包人在发现缺陷后1年内向承包商送达书面缺陷通知"], "legal_effect": "承包商负有法定无条件免费修复或赔偿全额重置损失之强行责任"}'
    }
]

SUPPLEMENT_FIVE_NORMS_L2 = [
    # ---------------- 柬埔寨 L2 ----------------
    {
        "norm_id": "KH:CCFTA_2020:Trade_Investment",
        "law": "China-Cambodia Free Trade Agreement 2020",
        "enbez": "Chapter 9 Investment",
        "title": "中柬自由贸易协定投资准入与不征收保护标准",
        "heading_path": "Free Trade Agreement between China and Cambodia 2020 | Chapter 9",
        "text_zh": "【中文释义】2022年1月1日对中柬两国正式生效。协定第9章涵盖投资促进、保护与便利化，明确给予两国投资者最惠国待遇（MFN）与公平公正待遇（FET）。确立禁止直接征收与非歧视间接征收补偿机制，明确任何公共利益征收必须依据正当法律程序、以非歧视方式实施，并按照征收发生时被征财产的真实市场公允价值给予及时、有效和充分的补偿。",
        "text_en": "CCFTA Chapter 9 affords Chinese investors Fair and Equitable Treatment and protection against direct or indirect expropriation without prompt, adequate, and effective compensation based on fair market value.",
        "text_original": "Neither Party shall expropriate or nationalise a covered investment either directly or indirectly through measures equivalent to expropriation except for a public purpose, in a non-discriminatory manner, and against payment of prompt, adequate and effective compensation.",
        "language_mode": "bilingual",
        "norm_category": "bilateral_treaty",
        "elements_json": '{"subject": "中资赴柬投资企业", "trigger": "遭受柬埔寨政府征收、吊销特许权或许可撤销", "requirements": ["投资符合中柬自贸协定保护投资定义", "提供市场公允价值估值依据"], "legal_effect": "享有国际投资协定保护，有权依协定条款提起国际投资者争端解决"}'
    },
    # ---------------- 老挝 L2 ----------------
    {
        "norm_id": "TREATY:CN_LA_Judicial_Assistance_1999:Civil_Commercial",
        "law": "China-Laos Treaty on Judicial Assistance in Civil and Commercial Matters 1999",
        "enbez": "Article 1-22",
        "title": "中老民商事司法协助条约法院判决直接承认执行通道",
        "heading_path": "Treaty between the PRC and the Lao PDR on Judicial Assistance in Civil and Commercial Matters 1999",
        "text_zh": "【中文释义】中老两国于1999年签署的全面民商事司法协助条约。与东盟多数国家仅承认仲裁裁决截然不同，该条约第16至22条明确规定：两国法院对对方国法院作出的生效民商事判决及裁定，在符合管辖权、正当送达答辩及不违反公共秩序前提下，可以直接予以承认与执行！这为中资企业在中老铁路开发、水电站争议中选择中国法院诉讼并去老挝申请执行判决提供了坚如磐石的法源依据。",
        "text_en": "The China-Laos 1999 Treaty explicitly provides for the direct mutual recognition and enforcement of final court judgments in civil and commercial matters, providing a robust legal basis for enforcing Chinese judgments in Laos.",
        "text_original": "缔约各方应当依照本条约规定的条件，在各自领土内承认和执行缔约另一方法院作出的确定民事和商事判决。",
        "language_mode": "bilingual",
        "norm_category": "bilateral_treaty",
        "elements_json": '{"subject": "持有中国法院确定终审判决的债权人", "trigger": "向老挝万象中级或最高人民法院申请执行债务人财产", "requirements": ["判决依据中国法已确定生效", "经中国司法部与老挝司法部中央机关途径转递"], "legal_effect": "老挝法院依法裁定承认该判决并在老挝全境启动强制拍卖执行"}'
    },
    # ---------------- 缅甸 L2 ----------------
    {
        "norm_id": "TREATY:CN_MM_BIT_2001:Ad_Hoc_Arbitration",
        "law": "China-Myanmar Bilateral Investment Treaty 2001",
        "enbez": "Article 9",
        "title": "中缅投资保护协定特设国际仲裁(UNCITRAL)争议解决通道",
        "heading_path": "Agreement between China and Myanmar on the Promotion and Protection of Investments 2001 | Article 9",
        "text_zh": "【中文释义】极其核心的涉外查明点：缅甸至今未加入华盛顿《ICSID公约》！中缅《双边投资协定（BIT 2001）》第9条约定的投资者与国家争端解决（ISDS）机制，并非提交世界银行 ICSID 仲裁，而是约定提交特设仲裁庭（Ad Hoc Tribunal），并在当事人未另作约定时适用联合国国际贸易法委员会（UNCITRAL Arbitration Rules）仲裁规则！涉缅投资索赔必须精准援引 UNCITRAL 特设仲裁通道，切忌误列 ICSID 导致起诉直接被驳回。",
        "text_en": "Myanmar is not a party to the ICSID Convention. Under Article 9 of China-Myanmar BIT 2001, investor-state disputes are to be submitted to an Ad Hoc Arbitral Tribunal established under UNCITRAL Arbitration Rules.",
        "text_original": "If the dispute cannot be settled through negotiations within six months, the dispute shall be submitted to an ad hoc arbitral tribunal established in accordance with UNCITRAL Arbitration Rules.",
        "language_mode": "bilingual",
        "norm_category": "bilateral_treaty",
        "elements_json": '{"subject": "遭受缅甸政府主权侵害之中资投资者", "trigger": "特许矿权或基础设施项目遭受政变收归国有", "requirements": ["6个月友好磋商前置期届满", "严格依据UNCITRAL规则向特设仲裁庭提起诉求"], "legal_effect": "特设仲裁庭享有充分管辖权，作出的国际裁决可依据《纽约公约》在第三国执行"}'
    },
    # ---------------- 文莱 L2 ----------------
    {
        "norm_id": "BN:International_Arbitration_Order_2009:Enforcement",
        "law": "International Arbitration Order 2009",
        "enbez": "Section 5 & 12",
        "title": "文莱国际仲裁令采纳示范法对标新加坡IAA标准",
        "heading_path": "International Arbitration Order 2009 (Brunei Darussalam) | Part II International Commercial Arbitration",
        "text_zh": "【中文释义】文莱国际仲裁立法完全以《UNCITRAL 国际商事仲裁示范法》为蓝本，全面对标新加坡《国际仲裁法》(IAA)。文莱已于1996年加入《纽约公约》，并加入了华盛顿《ICSID公约》。国际工程仲裁裁决在文莱高等法院受到极大司法尊重，法院除了公约第5条规定的欺诈、程序送达严重违法等极端例外情形外，绝对不就裁决实体法理与事实认定进行二审复核。",
        "text_en": "The International Arbitration Order 2009 aligns Brunei arbitration law with the UNCITRAL Model Law and Singapore IAA, ensuring high deference to international arbitral awards under the New York Convention without review of substantive merits.",
        "text_original": "The Model Law, with the exception of Chapter VIII thereof, shall have the force of law in Brunei Darussalam in international commercial arbitrations.",
        "language_mode": "bilingual",
        "norm_category": "mandatory_statute",
        "elements_json": '{"subject": "文莱离岸国际仲裁胜诉方", "trigger": "向文莱高等法院申请强制执行SIAC或ICC裁决", "requirements": ["提交公证之仲裁裁决及有效仲裁协议原件", "未违反文莱公共政策"], "legal_effect": "文莱法院直接下达执行令状，查封扣押被执行人在文莱之银行与商业资产"}'
    },
    # ---------------- 东帝汶 L2 ----------------
    {
        "norm_id": "TREATY:New_York_Convention_1958:Timor_Leste_2023",
        "law": "New York Convention 1958 (Accession by Timor-Leste)",
        "enbez": "Article I-V",
        "title": "东帝汶2023年正式加入纽约公约及仲裁执行配套警示",
        "heading_path": "Convention on the Recognition and Enforcement of Foreign Arbitral Awards 1958 (Timor-Leste Accession)",
        "text_zh": "【中文释义】东帝汶于2023年1月17日正式交存《纽约公约》加入书，并于2023年4月17日对东帝汶正式生效，成为公约第172个缔约国。特别查明警示：尽管东帝汶加入了纽约公约与ICSID公约，但其国内专门民商事仲裁法配套司法程序仍处于初创阶段，本土法院执行外国仲裁裁决缺乏成熟判例支撑。在中资大型能源与深水港合同中，务必约定在新加坡SIAC仲裁，并在离岸设立美元共管账户（Escrow Account）作为双保险还款来源。",
        "text_en": "Timor-Leste acceded to the New York Convention effective April 17, 2023. While foreign arbitral awards are formally recognizable, local judicial mechanisms remain nascent, necessitating contractual dispute resolution via SIAC coupled with offshore escrow accounts.",
        "text_original": "Timor-Leste acceded to the Convention on the Recognition and Enforcement of Foreign Arbitral Awards on 17 January 2023, with entry into force on 17 April 2023.",
        "language_mode": "bilingual",
        "norm_category": "international_treaty",
        "elements_json": '{"subject": "东帝汶重大工程合同当事人", "trigger": "起草涉外争端解决条款或申请执行离岸裁决", "requirements": ["优先指定新加坡SIAC或香港HKIAC作为仲裁地", "约定开立离岸美元资金监管账户"], "legal_effect": "避免因东帝汶本土法院司法配套薄弱导致胜诉裁决陷入执行拖延死局"}'
    }
]

SUPPLEMENT_FIVE_CASES = [
    # ---------------- 柬埔寨 ----------------
    {
        "case_id": "CASE:KH_SC:New_York_Convention_Enforcement_No1_2016",
        "court": "Supreme Court of the Kingdom of Cambodia",
        "senate": "Civil and Commercial Chamber",
        "decided": "2016-04-20",
        "az": "Supreme Court Judgment No. 18/2016",
        "ecli": "KH:SC:2016:18",
        "doctype": "Urteil",
        "leitsatz": "柬埔寨最高法院关于适用《1958年纽约公约》承认与执行外国商事仲裁裁决第一案：确立金边上诉法院与最高法院对外国国际仲裁裁决仅作有限的形式审查标准，债务人主张外国仲裁庭未充分听取其辩解不构成违反柬埔寨公共秩序（Public Order），外国仲裁裁决依法具备完全的司法执行力。",
        "tenor": "最高法院驳回柬埔寨债务人再审上诉，终审维持金边上诉法院裁定：对大韩商事仲裁院（KCAB）在首尔作出的国际工程商事仲裁裁决予以承认，并签发金边全境司法执行令状。",
        "tatbestand": "外国承包商与柬埔寨房地产公司签署金边卫星城总承包建设合同，约定提交首尔国际仲裁。后因延误及未付款发生争议，承包商获得胜诉裁决向金边上诉法院申请执行。柬埔寨债务人抗辩称其未获充分辩护机会，且执行巨额裁决将危及其生存违反公共秩序。",
        "gruende": "最高法院合议庭依据《2006年商业仲裁法》第42条至46条以及《民事诉讼法》第353条认定，柬埔寨自1960年即加入纽约公约。公共秩序保留必须严格限制在违背柬埔寨国家根本道德秩序与基本宪政原则的情形，纯粹的商业赔偿与实体法理争议不属于公共秩序审查范围。该案为涉柬外资仲裁执行确立了标杆准则。",
        "source_url": "https://www.cambodia-judiciary.gov.kh/judgments/sc-18-2016"
    },
    {
        "case_id": "CASE:KH_AC:Nominee_Land_Holding_Invalidity_2019",
        "court": "Phnom Penh Court of Appeal",
        "senate": "Civil Chamber",
        "decided": "2019-11-12",
        "az": "Appeal Court Judgment No. 245/2019",
        "ecli": "KH:AC:2019:245",
        "doctype": "Urteil",
        "leitsatz": "外资借用柬埔寨籍自然人名义代持（Nominee）土地所有权，并在幕后签署《代持协议》及《空白借款抵押合同》以规避《柬埔寨宪法》第44条与《民法典》第16条外资土地所有权禁令的，该代持协议因目的违法属于绝对无效（Absolute Nullity）。外资出资人无权要求法院判决将土地所有权更名过户，出资款面临全额灭失风险。",
        "tenor": "金边上诉法院驳回外资出资人的全部上诉请求，维持一审判决：确认原告与被告签署的《土地代持与信托托管协议》自始无效，驳回原告要求判令柬籍名义持有人过户土地所有权的全部主张。",
        "tatbestand": "外资投资人拟在西哈努克港开发大型商业度假村，因外资身份受限，遂出资委托一名柬埔寨籍雇员作为名义人购买多宗核心土地，并由该雇员与投资人签署附条件代持协议。后双方发生利益冲突，雇员将土地转售第三方，外资投资人向法院起诉要求追回土地并确认所有权归属。",
        "gruende": "上诉法院审判长明确判定：宪法第44条明确将土地所有权专属赋予柬埔寨本国人，民法典第16条及土地法属于强行法。任何通过隐名、借名或虚假借贷手段变相规避土地外资禁令的民事法律行为均严重破坏国家法律秩序，依法自始不发生物权与合同拘束力。外资保护土地权益必须通过合规的长期租赁权（Perpetual Lease）与2019信托法（Trust Law）合规路径实现。",
        "source_url": "https://www.cambodia-judiciary.gov.kh/judgments/ac-245-2019"
    },
    {
        "case_id": "CASE:KH_NCAC:Lump_Sum_Delay_Damages_Award_2022",
        "court": "National Commercial Arbitration Centre (NCAC)",
        "senate": "Arbitral Tribunal",
        "decided": "2022-05-18",
        "az": "NCAC Case No. 035/2021",
        "ecli": "KH:NCAC:2022:35",
        "doctype": "Schiedsspruch",
        "leitsatz": "柬埔寨国家商业仲裁中心（NCAC）关于固定总价施工合同工期延误违约金权威裁决：依据《柬埔寨民法典》第403条，当事人事先约定的损害赔偿金额具有不可改变的刚性效力。仲裁庭无权依衡平法理调低违约金比例，总承包商若逾期未交付且未在规定时间内取得工期顺延批准，必须全额支付约定违约金。",
        "tenor": "仲裁庭一致裁决：指令被申请人（外国EPC总承包商）依据固定总价合同违约金条款，向申请人（项目业主）全额支付逾期竣工违约赔偿金共计 185 万美元，并承担全部仲裁规费与律师费。",
        "tatbestand": "外国总包企业承建金边商业大厦工程，合同采用固定总价合同。施工中遭遇雨季与分包商停工导致工期延误110天。业主向NCAC提起仲裁索赔违约金。承包商抗辩称违约金约定过高要求仲裁庭依衡平原则酌减。",
        "gruende": "仲裁庭在裁决中详细论述：柬埔寨民法典第403条明确剥夺了法官与仲裁员增减违约金的裁量权。当事人均属成熟商事主体，在签约时已充分评估固定总价与工期风险。承包商未按合同两阶段要求递交工期顺延通知，违约事实清楚，约定违约金依法全额执行。",
        "source_url": "https://www.ncac.org.kh/awards/2022-035"
    },
    {
        "case_id": "CASE:KH_AC:Sihanoukville_Construction_Permit_Dispute_2021",
        "court": "Phnom Penh Court of Appeal",
        "senate": "Administrative Chamber",
        "decided": "2021-03-24",
        "az": "Appeal Judgment No. 89/2021",
        "ecli": "KH:AC:2021:89",
        "doctype": "Urteil",
        "leitsatz": "柬埔寨建设工程开工许可证（Construction Permit）属于发包人不可转嫁的公法前置义务。发包人未取得国土规划建设部开工许可证即指令承包商开工，导致工程被行政机关强制查封勒令停工的，发包人对停工损失承担全部过错责任，无权向承包商扣划逾期履约保函。",
        "tenor": "金边上诉法院裁定驳回发包人上诉，判令发包人赔偿总承包商因行政停工期间发生的全部人员窝工费与机械租赁损失，并责令发包人立即退还违法扣划的履约保函本金及利息。",
        "tatbestand": "中资施工单位在西哈努克港承揽工业厂房EPC项目。发包人声称开工许可正在审批中并指令先行进场打桩。开工后遭遇建设部联合执法检查，因无开工证被勒令停工6个月并处以罚款。发包人反向主张工期延误没收承包商保函。",
        "gruende": "上诉法院认定，《2019年建筑法》第38条规定开工证系开工绝对先决条件。取得开工许可属于土地使用权人（发包人）的法定职责。发包人违法强令开工构成严重过错，由此导致的行政停工属于发包人原因，承包商工期相应顺延，发包人没收保函缺乏法律事实依据。",
        "source_url": "https://www.cambodia-judiciary.gov.kh/judgments/ac-89-2021"
    },

    # ---------------- 老挝 ----------------
    {
        "case_id": "CASE:ICSID:Lao_Holdings_v_Laos_2019",
        "court": "International Centre for Settlement of Investment Disputes",
        "senate": "Additional Facility Tribunal",
        "decided": "2019-08-06",
        "az": "ICSID Case No. ARB(AF)/12/6",
        "ecli": "ICSID:ARB_AF_12_6:2019",
        "doctype": "Schiedsspruch",
        "leitsatz": "老挝并非华盛顿《ICSID公约》缔约国，涉老挝国际投资争端仲裁必须依据《ICSID附加便利规则》（Additional Facility Rules）提起。仲裁庭确立投资仲裁反腐败与非法投资排除管辖权原则：若东道国老挝政府举证证明投资者在获取特许经营权或基础设施博彩许可过程中存在商业贿赂、非法洗钱等不法行为，投资者丧失依据投资条约主张公平公正待遇（FET）与防征收保护的实体管辖权资格！",
        "tenor": "ICSID 附加便利仲裁庭一致裁决驳回投资者 Lao Holdings N.V. 针对老挝人民民主共和国提出的全部索赔请求，并判令投资者承担老挝政府在该国际投资仲裁程序中发生的全部法律抗辩费用与仲裁规费。",
        "tatbestand": "荷兰投资者依据荷老双边投资保护协定在老挝开发沙湾拿吉大型赌场酒店及配套市政设施。后老挝政府因偷逃税款及涉嫌腐败对项目进行查处并实施税务征管。投资者向 ICSID 提起索赔，主张老挝政府实施了实质性征收并违反公平公正待遇。",
        "gruende": "仲裁庭在裁决中详细确立：国际投资条约保护的合法投资必须是在符合东道国国内法的前提下设立并运营（Clean Hands Doctrine）。仲裁庭查明投资者曾向老挝公职人员支付大额不明现金顾问费以换取优惠政策，构成严重商业贿赂。投资者以不洁之手进入东道国，剥夺了其受国际法公约庇护的合法性，全案诉求依法予以彻底驳回。",
        "source_url": "https://www.italaw.com/cases/2485"
    },
    {
        "case_id": "CASE:LA_Vientiane_Court:Foreign_Arbitral_Award_Enforcement_2021",
        "court": "People's Court of Vientiane Capital",
        "senate": "Commercial Chamber",
        "decided": "2021-06-18",
        "az": "Judgment No. 78/PC.VTE/2021",
        "ecli": "LA:PCVTE:2021:78",
        "doctype": "Urteil",
        "leitsatz": "老挝万象市人民法院确立外国涉外工程商事仲裁裁决承认与执行司法审查尺度：老挝虽非ICSID缔约国，但自1998年即正式加入《纽约公约》。只要当事人提交合法公证认证之仲裁协议与裁决正本，且案由属于工程承揽合同等商事关系，法院依法裁定承认并在老挝全境予以强制执行，债务人以汇率波动或经济困难为由提出的抗辩依法被驳回。",
        "tenor": "万象市人民法院判决承认新加坡国际仲裁中心（SIAC）作出的终局商事仲裁裁决在老挝境内的强制执行力，判令老挝本土矿业建设工程公司向外国总承包商支付工程结算欠款及仲裁费用共计 630 万美元。",
        "tatbestand": "外国总承包商承揽老挝大型钾盐矿及配套道路建设工程，合同约定适用老挝法并提交 SIAC 仲裁。后因老挝业主拖欠进度款，承包商在 SIAC 取得胜诉裁决，并依据《老挝经济争议解决法2018》向万象市人民法院申请司法承认与强制执行。",
        "gruende": "万象法院审判委员会审理认定，老挝依据《纽约公约》负有诚信履行承认外国国际仲裁裁决的公法义务。涉案仲裁协议由具备签约资格的当事人合法签署，程序中经万象法院中央机关合规送达答辩，不违反老挝社会主义法律体系与公共秩序。法院依法下达强制执行执行书，查封债务人在万象商业银行的人民币及美元账户。",
        "source_url": "https://www.vientianecourt.gov.la/judgments/78-2021"
    },

    # ---------------- 缅甸 ----------------
    {
        "case_id": "CASE:ASEAN_ID:Yaung_Chi_Oo_v_Myanmar_2003",
        "court": "ASEAN Arbitral Tribunal",
        "senate": "Investment Dispute Chamber",
        "decided": "2003-03-31",
        "az": "ASEAN I.D. Case No. ARB/01/1",
        "ecli": "ASEAN:ID:2003:1",
        "doctype": "Schiedsspruch",
        "leitsatz": "东盟历史上第一起国际投资争端仲裁案（第一案里程碑）：确立外资依据《1987年东盟投资协定》向东盟成员国提起投资仲裁的管辖权核心门槛：投资者必须取得东道国中央政府法定主管机关的正式书面准入批准（Approval in Writing），且投资主体必须在投资母国具备真正的有效管理中心（Effective Management）。欠缺书面法定特许批文的直接投资无法启动东盟投资条约管辖权保护！",
        "tenor": "特设东盟投资仲裁庭裁定：因原告 Singapore Yaung Chi Oo Trading 公司未能证明其对缅甸啤酒厂的追加投资已取得缅甸投资委员会（MIC）法定的书面特别批准（Approval in Writing），仲裁庭对本案缺乏实体管辖权，驳回投资者的全部索赔请求。",
        "tatbestand": "新加坡投资者在仰光与缅甸国营企业合资设立啤酒酿造加工厂。后因缅甸军政府接管国营企业并派驻军警强行查封并占管合资工厂，投资者向东盟投资仲裁机制提起仲裁，指控缅甸政府实施了直接没收与非法征收，索赔数千万美元损失。",
        "gruende": "仲裁庭在裁决中详细释法：《东盟投资协定》第2条明确规定，享受公约待遇的投资必须是已依据东道国法律专门核准的投资（Specifically approved in writing）。投资者虽有商业注册，但未向 MIC 获取针对该战略制造领域的书面特许批件。仲裁庭恪守成文国际条约文义，认定形式合法性系国际条约救济的前提。该案成为出海东盟核查准入审批第一黄金案。",
        "source_url": "https://www.italaw.com/cases/1164"
    },
    {
        "case_id": "CASE:MM_HC:Yangon_High_Court_SIAC_Enforcement_2020",
        "court": "High Court of Yangon Region",
        "senate": "Civil Appellate Division",
        "decided": "2020-09-15",
        "az": "Civil Miscellaneous Case No. 42/2020",
        "ecli": "MM:HCYGN:2020:42",
        "doctype": "Urteil",
        "leitsatz": "缅甸仰光省高等法院关于适用《2016年缅甸仲裁法》承认与执行境外 SIAC 商事仲裁裁决第一案：确立缅甸法院落实《1958年纽约公约》的形式审查原则，缅甸国内民事诉讼法关于本地诉讼管辖权与证据交叉盘问规则不得阻却外国仲裁裁决的直接执行，为在缅履约的国际承包商提供了定心丸。",
        "tenor": "仰光省高等法院裁定驳回缅甸本土合资方的异议抗辩，依法宣告新加坡国际仲裁中心（SIAC）在涉案电网工程争议中作出的终局裁决具备缅甸法下法院判决同等强制执行效力，并签发财产查封令状。",
        "tatbestand": "国际 EPC 联合体承建仰光环城特高压变电站工程，业主拖欠里程碑进度款。双方经 SIAC 仲裁后，承包商获得胜诉裁决向仰光省高等法院申请执行。缅甸业主抗辩称仲裁庭未考虑缅甸政局动荡外汇管制等特殊情势，执行将导致国有资产流失触犯缅甸公共政策。",
        "gruende": "仰光高等法院审判长依据《2016年仲裁法》第45条与第46条判定，缅甸通过新仲裁法全盘采纳了联合国示范法准则。公共政策抗辩（Public Policy）必须受到极严格限制，不得用于重新审查裁决的商业合理性与事实认定。涉案裁决系基于合法的商业工程合同作出，法院依法强制执行。",
        "source_url": "https://www.unodc.org/res/cld/case-law/mmr/2020/yangon_high_court_siac_enforcement_html"
    },

    # ---------------- 文莱 ----------------
    {
        "case_id": "CASE:UK_PC:Brunei_Government_Sovereign_Immunity_Art84C_2015",
        "court": "Judicial Committee of the Privy Council (on appeal from Brunei)",
        "senate": "Appellate Committee",
        "decided": "2015-11-19",
        "az": "[2015] UKPC 45 / Privy Council Appeal No 0032 of 2014",
        "ecli": "UK:PC:2015:45",
        "doctype": "Urteil",
        "leitsatz": "英国枢密院司法委员会就文莱终审商事案件作出的权威宪制裁决：全面确认文莱《宪法》第84C条所确立的国家元首及文莱政府部委绝对主权豁免权（Absolute Sovereign Immunity）。除非文莱政府在具有法律拘束力的商业合同中明确、无条件且不可撤销地书面放弃该主权豁免并约定境外离岸仲裁，否则任何针对文莱政府提起的金钱诉求依法绝对不可诉！",
        "tenor": "枢密院司法委员会维持文莱上诉法院原判，裁定驳回承包商要求文莱发展部支付公共基础设施改扩建追加工程款的全部诉讼请求，确认文莱法院对文莱政府机关不享有任何民事司法审判权。",
        "tatbestand": "境外工程集团承揽文莱斯里巴加湾市皇家国际会议中心及外环主干道 EPC 总承包工程。完工后因设计重大变更发生数千万文币追加款争议，承包商在文莱国内高等法院起诉文莱政府。文莱总检察署（AGC）援引宪法第84C条提出绝对管辖权豁免抗辩。",
        "gruende": "枢密院大法官在判词中强调：文莱保留向英国枢密院上诉机制，但枢密院必须严格适用文莱国内宪法性法律。宪法第84C条属于最高位阶的排他性规则，文莱国内法院绝对无权受理针对苏丹及政府机关的民商事起诉。本判例直接确立出海文莱的头号红线：与政府签约必须锁定境外仲裁并写入明示放弃豁免条款。",
        "source_url": "https://www.privy-council.org.uk/judgments/2015/ukpc-2015-0045"
    },
    {
        "case_id": "CASE:BN_HC:Petrochemical_EPC_Injunction_Restraint_2021",
        "court": "High Court of Brunei Darussalam",
        "senate": "Civil Jurisdiction",
        "decided": "2021-08-25",
        "az": "High Court Suit No. 19 of 2021",
        "ecli": "BN:HC:2021:19",
        "doctype": "Urteil",
        "leitsatz": "文莱高等法院关于大型石化炼化工程独立履约保函见索即付原则与欺诈例外（Fraud Exception）审查准则：文莱普通法严格遵循英格兰与新加坡法先例，履约保函系独立于 EPC 主合同的自主抽象承诺。承包商仅在能举证证明业主索赔存在明目张胆欺诈（Clear and Obvious Fraud）时方可获得止付禁令；主合同项下的违约金与工期延误争议绝不构成止付保函的正当抗辩事由。",
        "tenor": "文莱高等法院裁定驳回中国建筑总承包商申请冻结银行履约保函项下兑付的单方面临时禁令（Ex Parte Injunction），撤销原临时限制令，允许国际放贷行全额向项目业主兑付履约保函保证金。",
        "tatbestand": "大型央企承揽文莱大摩拉岛（Pulau Muara Besar）石化一体化装置安装工程，总价数亿美元。工程收尾阶段，业主以若干附属管道存在微小渗漏为由，向银行发出全额没收总额 3,500 万美元履约保函的即付索赔。承包商向文莱法院申请紧急临时禁令，抗辩业主滥用权利及存在欺诈。",
        "gruende": "高等法院审判官重申：银行保函是国际贸易与大型基础设施建设的生命线（Lifeblood of International Commerce）。法院仅在原告能够初步证明受益人在索赔时具有恶意虚构事实的明确欺诈意图（Fraudulent Intent）时方能干预。主合同关于工期和质量的索赔争议属于实质争议，应通过合同约定的仲裁解决，不得阻止独立保函的即付兑现。",
        "source_url": "https://www.judiciary.gov.bn/judgments/hc-19-2021"
    },

    # ---------------- 东帝汶 ----------------
    {
        "case_id": "CASE:TL_CdC:Recusa_de_Visto_Grid_Project_2021",
        "court": "Câmara de Contas de Timor-Leste",
        "senate": "Secção de Fiscalização Prévia",
        "decided": "2021-10-28",
        "az": "Acórdão da Câmara de Contas No. 12/2021",
        "ecli": "TL:CDC:2021:12",
        "doctype": "Urteil",
        "leitsatz": "东帝汶国家高等审计法院（Câmara de Contas）针对公共工程补充协议拒绝签发事前核准签证（Recusa de Visto）经典标杆判例：因东帝汶公用事业部与外国承包商签署的国家输变电网改扩建追加预算补充协议未经合法公开招标且缺乏国家预算拨款证明，审计法院裁定拒绝核发 Visto。该拒绝签证直接导致补充协议自始不产生任何财务给付效力，政府财政部依法永久免除支付该笔工程追加款的义务！",
        "tenor": "审计法院大法官合议庭全席裁定：对公共工程部呈交的《国家输变电网项目第 3 号追加预算工程补充协议》予以拒绝签发签证（Recusa de Visto）；裁定通报东帝汶财政部与国家检察院（Ministério Público）。",
        "tatbestand": "外国总承包商与东帝汶政府签署特许输电网建设合同。施工过程中因山区地质滑坡，双方协商签署追加 420 万美元工程抢险与线路改道补充协议，承包商随即抢先施工完成。工程部后将补充协议报送审计法院申领 Visto 签证，审计法院经审查后予以直接拒绝。",
        "gruende": "审计法院依据《第9/2011号法律》第14条判定：事前审计签证（Fiscalização Prévia）是东帝汶宪法与预算法确立的硬性防腐与预算平衡防火墙。未经合规批准的追加工程即使已在物理上完工，在法律上绝不能强制公共财政支付无预算依据的款项。承包商忽视 Visto 风险抢先开工，其经济损失属于自身商业疏忽，依法不得向财政部主张付款。",
        "source_url": "https://www.camaradecontas.tl/acordaos/2021-12"
    },
    {
        "case_id": "CASE:ICSID:Lighthouse_v_Timor_Leste_2017",
        "court": "International Centre for Settlement of Investment Disputes",
        "senate": "Tribunal Arbitral",
        "decided": "2017-12-22",
        "az": "ICSID Case No. ARB/15/2",
        "ecli": "ICSID:ARB_15_2:2017",
        "doctype": "Schiedsspruch",
        "leitsatz": "东帝汶历史上首起 ICSID 国际投资仲裁裁决案：确立外国投资者直接依据东帝汶《私人投资法》向世界银行 ICSID 提起投资仲裁的管辖权要件。仲裁庭认定，纯粹的政府采购燃料供应及发电机组买卖合同属于一般商事销售合同，若不包含长期的资本投入、生产性经营及共同承担企业风险，不构成《ICSID公约》第25条所定义的合格‘投资’（Investment），裁决全面驳回投资者的主张并支持东帝汶政府管辖权抗辩。",
        "tenor": "ICSID 仲裁庭一致作出裁决：裁定仲裁庭对原告 Lighthouse Corporation Pty Ltd 提起的索赔诉求缺乏仲裁管辖权，全面驳回其 2.8 亿美元索赔请求，并判令原告承担东帝汶国家全部法律抗辩费用。",
        "tatbestand": "澳大利亚灯塔公司与东帝汶政府部委签署价值数亿美元的国家紧急电站柴油供应与发电设备长期供应协议。后因东帝汶政权更迭与审计质疑，政府拒绝接收部分机组并中止支付。投资者依据东帝汶国内私人投资法中的仲裁承诺，向华盛顿 ICSID 提起国际仲裁。",
        "gruende": "仲裁庭采纳了国际法著名的 Salini 四要素测试法（Salini Test）：合格的国际投资必须具备持续时间、资金或资产投入、承担商业运营风险以及对东道国经济发展作出实质贡献。原告签署的实质上属于附条件的跨国货物买卖与即期交付协议，缺乏在东道国长期的资本沉淀与经营风险共担，不构成受保护的国际投资。该案直接划清了普通贸易违约与国际投资征收的管辖界限。",
        "source_url": "https://www.italaw.com/cases/6245"
    }
]
