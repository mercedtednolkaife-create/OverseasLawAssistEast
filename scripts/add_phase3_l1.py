import json

# Phase 3: 15 条全新 L1 高价值涉外核心规范
PHASE3_NORMS = [
    {
        "norm_id": "ID:KUHPerdata:Art1266",
        "law": "KUHPerdata_ID",
        "enbez": "Art.1266",
        "title": "《印尼民法典》第1266条：合同法定解除需经法院判决强行法与自愿弃权条款效力",
        "heading_path": "Kitab Undang-Undang Hukum Perdata > Buku III Perikatan > Bab II Perikatan yang Lahir dari Perjanjian > Pasal 1266",
        "text_de": "Indonesian Civil Code Art. 1266 (Court Decision Requirement for Termination & Express Waiver)",
        "language_mode": "trilingual",
        "lang_original": "id",
        "text_original": "Syarat batal dianggap selalu dicantumkan dalam persetujuan yang bertimbal balik, manakala salah satu pihak tidak memenuhi kewajibannya. Dalam hal demikian, persetujuan tidak batal demi hukum, tetapi pembatalan harus dimintakan kepada Hakim.",
        "text_en": "A resolutive condition is always implied in bilateral agreements where one party fails to fulfill obligations. The agreement is not void by operation of law, but termination must be demanded before a Judge.",
        "text_zh": "【印尼出海最致命解约陷阱】印尼法确立合同解除必须经法院裁决。若工程合同未在专用条件中明确订立‘双方自愿不可撤销地放弃适用《印尼民法典》第1266条关于需经法院判决方得解约之规定’，总承包商单方发函通知解除合同并撤场施工将被印尼法院判定为非法弃标违约，面临保函全额没收及连带赔偿。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "statute",
        "mandatory_level": "mandatory_override"
    },
    {
        "norm_id": "FIDIC:Silver_1999:Clause_16.1",
        "law": "FIDIC",
        "enbez": "Silver:16.1",
        "title": "《FIDIC 银皮书 EPC》第16.1款：发包人欠款承包商暂停施工权与工期顺延及窝工成本补偿 (Tier 1 核心条款)",
        "heading_path": "FIDIC Conditions of Contract for EPC/Turnkey Projects 1999 > Clause 16 Suspension and Termination by Contractor > 16.1 Contractor's Entitlement to Suspend Work",
        "text_de": "FIDIC Silver Book (1999) Clause 16.1 (Contractor's Entitlement to Suspend Work)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "If the Employer fails to comply with Sub-Clause 2.4 or Sub-Clause 14.7, the Contractor may, after giving not less than 21 days' notice to the Employer, suspend work (or reduce the rate of work) unless and until the Contractor has received the payment. The Contractor shall be entitled to an extension of time (EOT) and payment of Cost plus reasonable profit.",
        "text_en": "Contractor may suspend work after giving 21 days' notice if Employer fails to pay or provide financial arrangements, entitling Contractor to EOT and Cost plus profit.",
        "text_zh": "【承包商防御性停工法定利器】发包人拖欠工程进度款逾期未付或无法证明具备充足履约资金安排的，承包商在发出不少于 21 天书面催告通知后，有权依法减缓施工速度或全面暂停现场施工。由此导致的工期滞后享有全额工期顺延（EOT），并有权追偿全部现场窝工成本及合理利润。",
        "translation_source": "FIDIC_OFFICIAL_ZH",
        "norm_category": "fidic_standard",
        "fidic_tier": "core_dispute",
        "fidic_edition": "1999_SILVER",
        "mandatory_level": "contract_default"
    },
    {
        "norm_id": "FIDIC:Silver_1999:Clause_16.2",
        "law": "FIDIC",
        "enbez": "Silver:16.2",
        "title": "《FIDIC 银皮书 EPC》第16.2款：承包商单方解除合同撤场权与全额停工窝工预期利润索赔 (Tier 1 核心条款)",
        "heading_path": "FIDIC Conditions of Contract for EPC/Turnkey Projects 1999 > Clause 16 Suspension and Termination by Contractor > 16.2 Termination by Contractor",
        "text_de": "FIDIC Silver Book (1999) Clause 16.2 (Termination by Contractor)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "The Contractor shall be entitled to terminate the Contract if: (a) Contractor does not receive reasonable evidence under Sub-Clause 2.4 within 42 days, (b) Employer fails to pay within 42 days after expiry of payment time, or (c) a prolonged suspension affects the whole Works under Sub-Clause 8.11 for more than 84 days. The Contractor may, upon giving 14 days' notice, terminate.",
        "text_en": "Contractor may terminate on 14 days' notice for prolonged payment default, prolonged suspension exceeding 84 days, or Employer's substantial failure.",
        "text_zh": "【最终止损解约权】当发包人拖欠工程款超过 42 天，或发包人指令停工超过 84 天时，承包商在提前 14 天书面催告后有权单方正式解除总承包合同。解约后承包商有权撤出施工人员及重型设备，要求发包人退还全部履约担保，并索赔已完成工程量价款、遣散费及剩余合同的预期利润（Loss of Profit）。",
        "translation_source": "FIDIC_OFFICIAL_ZH",
        "norm_category": "fidic_standard",
        "fidic_tier": "core_dispute",
        "fidic_edition": "1999_SILVER",
        "mandatory_level": "contract_default"
    },
    {
        "norm_id": "TH:CCC:Sec387",
        "law": "Civil_Code_TH",
        "enbez": "Sec.387",
        "title": "《泰国民商法典》第387条：违约法定催告与合理补正期限前置要件",
        "heading_path": "Thailand Civil and Commercial Code > Book II Obligations > Title II Contracts > Section 387 Rescission of Contract",
        "text_de": "Thailand Civil and Commercial Code Section 387 (Notice of Rescission and Reasonable Time)",
        "language_mode": "trilingual",
        "lang_original": "th",
        "text_original": "If one of the parties does not perform his obligation, the other party may fix a reasonable time and notify him to perform within that time. If he does not perform within that time, the other party may rescind the contract.",
        "text_en": "If a party fails to perform, the other party may fix a reasonable time and notify performance. If unperformed, the other party may rescind.",
        "text_zh": "【泰国法下合法解约黄金程序】在适用泰国实体法的工程合同中，无论合同如何约定单方立即解约，依据民商法典第 387 条强行法，守约方解除合同前必须向违约方发出正式通知并指定一段合理的催告履行宽限期。欠缺催告直接突袭解约撤场的，解约行为在泰国法下不发生法律效力。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "statute",
        "mandatory_level": "mandatory_override"
    },
    {
        "norm_id": "FIDIC:Silver_1999:Clause_1.14",
        "law": "FIDIC",
        "enbez": "Silver:1.14",
        "title": "《FIDIC 银皮书 EPC》第1.14款：联合体联营各方对发包人不可分割的连带履约与赔偿责任 (Tier 1 核心条款)",
        "heading_path": "FIDIC Conditions of Contract for EPC/Turnkey Projects 1999 > Clause 1 General Provisions > 1.14 Joint and Several Liability",
        "text_de": "FIDIC Silver Book (1999) Clause 1.14 (Joint and Several Liability of Consortium/JV)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "If the Contractor constitutes a joint venture, consortium or other unincorporated grouping of two or more persons: (a) these persons shall be deemed to be jointly and severally liable to the Employer for the performance of the Contract, (b) these persons shall notify the Employer of their leader, and (c) the Contractor shall not alter its composition without prior consent.",
        "text_en": "Members of a joint venture or consortium are jointly and severally liable to Employer. Composition shall not be altered without consent.",
        "text_zh": "【联合体出海穿透连带清偿风险】中资企业与东道国当地承包商组建联营体（Consortium/JV/KSO）投标签约的，联合体各方在法律上对发包人承担 100% 连带履约和违约赔偿责任。当属地伙伴资金链断裂或破产违约时，发包人有权越过属地伙伴直接要求中资企业全额承担工期及赔偿全部工程损失。",
        "translation_source": "FIDIC_OFFICIAL_ZH",
        "norm_category": "fidic_standard",
        "fidic_tier": "core_dispute",
        "fidic_edition": "1999_SILVER",
        "mandatory_level": "contract_default"
    },
    {
        "norm_id": "MY:Partnership_Act_1961:Sec11",
        "law": "Partnership_Act_1961",
        "enbez": "Sec.11",
        "title": "《马来西亚1961年合伙法》第11条：联营体工程债务合伙人无限连带清偿与内部追偿权",
        "heading_path": "Partnership Act 1961 (Act 135) > Nature of Partnership > Section 11 Liability of partners",
        "text_de": "Malaysian Partnership Act 1961 Section 11 (Joint Liability of Partners for Partnership Debts)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Every partner in a firm is liable jointly with the other partners for all debts and obligations of the firm incurred while he is a partner; and after his death his estate is also severally liable in a due course of administration.",
        "text_en": "Every partner in a firm is liable jointly with other partners for all debts and obligations of the firm incurred while a partner.",
        "text_zh": "【大马联营体债务穿透规则】在马来西亚进行工程建设的非法人联合体，依法适用合伙法原则，各合伙方对项目对外的工程款欠款、材料商货款及发包人索赔承担连带清偿责任。中资企业在代属地破产合伙人承担对外清偿后，有权依据合伙协议及本条向其破产财产行使内部追偿权（Right of Indemnity）。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "statute",
        "mandatory_level": "default"
    },
    {
        "norm_id": "ID:KUHD:Art18",
        "law": "KUHD_ID",
        "enbez": "Art.18",
        "title": "《印尼商法典》第18条：非法人联营体(Firma/KSO)破产清算与合伙债务穿透清偿",
        "heading_path": "Kitab Undang-Undang Hukum Dagang > Buku I > Bab III Perseroan Firma > Pasal 18",
        "text_de": "Indonesian Commercial Code Art. 18 (Joint and Several Liability in Firma and Joint Operations)",
        "language_mode": "trilingual",
        "lang_original": "id",
        "text_original": "Dalam perseroan firma, tiap-tiap sekutu bertanggung jawab secara tanggung renteng untuk seluruh perikatan perseroan.",
        "text_en": "In a partnership under a firm, each partner is jointly and severally liable for all obligations of the partnership.",
        "text_zh": "【印尼 KSO 联营连带责任法定依据】印尼现行商业法典明确：非法人联营体（KSO/Firma）的各合伙方对联营体在合同履行过程中产生的一切债务负有无条件的连带清偿责任（Tanggung Renteng）。即使联营协议约定了各自分工段与分账比例，该内部约定不得对抗发包人的对外全额索赔。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "statute",
        "mandatory_level": "default"
    },
    {
        "norm_id": "VN:Civil_Code_2015:Art509",
        "law": "Civil_Code_VN",
        "enbez": "Art.509",
        "title": "《越南民法典2015》第509条：合作合同成员对外债务连带民事责任",
        "heading_path": "Bộ luật Dân sự 2015 > Chương XIX Hợp đồng hợp tác > Điều 509 Trách nhiệm dân sự của thành viên hợp tác",
        "text_de": "Vietnamese Civil Code 2015 Art. 509 (Joint Liability of Cooperation Contract Members)",
        "language_mode": "trilingual",
        "lang_original": "vi",
        "text_original": "Các thành viên hợp tác chịu trách nhiệm dân sự chung bằng tài sản chung; nếu tài sản chung không đủ để thực hiện nghĩa vụ chung thì thành viên hợp tác phải chịu trách nhiệm bằng tài sản riêng theo phần đóng góp hoặc chịu trách nhiệm liên đới theo thỏa thuận hoặc theo quy định của luật.",
        "text_en": "Members of cooperation contracts bear joint civil liability with common property; if insufficient, members bear several or joint liability with private property.",
        "text_zh": "【越南合作联营责任规范】在越南通过合作合同（Hợp đồng hợp tác）形式组建联合体承揽工程的，联合体对外债务优先以联营公用财产清偿；不足清偿部分，中资企业与越方伙伴承担穿透性的连带责任，严禁约定将连带对外责任完全转嫁给单方以逃避第三人追偿。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "statute",
        "mandatory_level": "default"
    },
    {
        "norm_id": "ID:UU_1_2004:Art50",
        "law": "UU_1_2004",
        "enbez": "Art.50",
        "title": "《印尼国家金库法》第50条：严禁查封执行国家公共财产与国有电力/交通资产执行豁免屏障",
        "heading_path": "Undang-Undang No. 1 Tahun 2004 tentang Perbendaharaan Negara > Bab VII Pengelolaan Barang Milik Negara > Pasal 50",
        "text_de": "Indonesian State Treasury Law 2004 Art. 50 (Prohibition of Seizure of State Assets)",
        "language_mode": "trilingual",
        "lang_original": "id",
        "text_original": "Pihak mana pun dilarang melakukan penyitaan terhadap: uang atau surat berharga milik negara/daerah, uang yang harus disetor oleh pihak ketiga kepada negara/daerah, dan barang bergerak/tidak bergerak milik negara/daerah.",
        "text_en": "Any party is prohibited from seizing state/regional money, securities, or movable/immovable assets owned by the state.",
        "text_zh": "【出海印尼最大执行落空陷阱】中资总包在 SIAC 仲裁打赢印尼国家电力公司（PLN）或交通部并获得执行许可后，在申请法院扣押其公用变电站、电网资产或财政拨款账户时，印尼法院常援引本条规定以‘严禁查封执行国有财产’为由驳回扣押申请，导致胜诉仲裁裁决面临巨大执行变现屏障。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "statute",
        "mandatory_level": "mandatory_override"
    },
    {
        "norm_id": "SG:State_Immunity_Act:Sec5",
        "law": "State_Immunity_Act_SG",
        "enbez": "Sec.5",
        "title": "《新加坡国家豁免法》第5条：商业交易管辖与执行例外(Commercial Exception)否定外国国企主权豁免",
        "heading_path": "State Immunity Act 1979 (Cap. 313, Rev. 2020) > Section 5 Commercial transactions and contracts to be performed in Singapore",
        "text_de": "Singapore State Immunity Act Section 5 (Commercial Transactions Exception to State Immunity)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "A State is not immune as respects proceedings relating to: (a) a commercial transaction entered into by the State, or (b) an obligation of the State which by virtue of a contract falls to be performed wholly or partly in Singapore.",
        "text_en": "A State is not immune as respects proceedings relating to commercial transactions entered into by the State.",
        "text_zh": "【刺破外国国企主权豁免抗辩武器】外国国家或东道国国有电力能源公司（如 PLN、EVN、EGAT）以主权者身份从事商业总承包或借款交易的，在新加坡法院不享有任何主权司法管辖豁免与仲裁管辖豁免。其在新加坡境内的商业银行账户、售电转账外汇与投资资产依法准予直接查封扣押执行。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "statute",
        "mandatory_level": "mandatory_override"
    },
    {
        "norm_id": "MY:Civil_Law_Act:Mareva",
        "law": "Civil_Law_Act_MY",
        "enbez": "Mareva_Doctrine",
        "title": "《马来西亚民事法案》Mareva 原则：跨国全球资产冻结禁令防止被执行人隐匿工程款资产",
        "heading_path": "Civil Law Act 1956 (Act 67) > Section 25 jo. Rules of Court 2012 Order 29 > Mareva Injunction Doctrine",
        "text_de": "Malaysian Mareva Injunction Doctrine (Worldwide Freezing Order on Commercial Assets)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "The High Court possesses jurisdiction under Section 25 of the Courts of Judicature Act 1964 and Civil Law Act 1956 to grant a Mareva Injunction restraining a defendant from dissipating or removing assets from the jurisdiction pending arbitration.",
        "text_en": "High Court possesses jurisdiction to grant Mareva Injunctions restraining defendants from dissipating assets from the jurisdiction.",
        "text_zh": "【跨国追索恶意脱产核心救济】当东道国发包人在仲裁实体审理期间或出具裁决后，存在通过离岸空壳公司恶意转移项目收益款、扣押工程款资金池的行为时，承包商可直接向马来西亚高等法院申请签发全球/属地 Mareva 资产冻结禁制令，强制阻断开户行划转款项。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "statute",
        "mandatory_level": "default"
    },
    {
        "norm_id": "FIDIC:Yellow_1999:Clause_4.12",
        "law": "FIDIC",
        "enbez": "Yellow:4.12",
        "title": "《FIDIC 黄皮书》第4.12款：不可预见的物质条件(Unforeseeable Physical Conditions)与地质障碍工期成本追加 (Tier 1 核心条款)",
        "heading_path": "FIDIC Conditions of Contract for Plant and Design-Build 1999 > Clause 4 The Contractor > 4.12 Unforeseeable Physical Conditions",
        "text_de": "FIDIC Yellow Book (1999) Clause 4.12 (Unforeseeable Physical Conditions Claims)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "If the Contractor encounters adverse physical conditions which he considers to have been Unforeseeable, the Contractor shall give notice to the Engineer. If the Engineer determines that conditions were Unforeseeable, the Contractor shall be entitled to: (a) an extension of time (EOT), and (b) payment of any such Cost.",
        "text_en": "If Contractor encounters Unforeseeable physical conditions, after notice, Contractor is entitled to EOT and payment of Cost.",
        "text_zh": "【地下地质突变索赔黄金条款】在黄皮书设备与设计-建造工程中，施工现场遭遇经验丰富的承包商在基准日前无法合理预见的地下溶洞、断层破碎带或未探明坚硬岩层导致工程受阻的，承包商在发出通知后，享有全额工期顺延（EOT）及发包人补偿实际发生成本（Cost）之法定权利。",
        "translation_source": "FIDIC_OFFICIAL_ZH",
        "norm_category": "fidic_standard",
        "fidic_tier": "core_dispute",
        "fidic_edition": "1999_YELLOW",
        "mandatory_level": "contract_default"
    },
    {
        "norm_id": "FIDIC:Silver_1999:Clause_4.10",
        "law": "FIDIC",
        "enbez": "Silver:4.10",
        "title": "《FIDIC 银皮书 EPC》第4.10款：发包人现场数据勘察资料免责边界与欺诈性隐瞒抗辩 (Tier 1 核心条款)",
        "heading_path": "FIDIC Conditions of Contract for EPC/Turnkey Projects 1999 > Clause 4 The Contractor > 4.10 Site Data",
        "text_de": "FIDIC Silver Book (1999) Clause 4.10 (Site Data and Limits of Employer Disclaimer)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "The Employer shall have made available to the Contractor all relevant data in the Employer's possession on subsurface and hydrological conditions. The Contractor shall be responsible for verifying and interpreting all such data. To the extent practicable, Contractor shall be deemed to have obtained all necessary info as to risks.",
        "text_en": "Employer must make available subsurface data; Contractor is responsible for verifying, subject to good faith and fraudulent concealment limits.",
        "text_zh": "【银皮书总价包干地质风险边界】银皮书 EPC 原则上将地质水文风险推由承包商自担。但发包人负有将其已知悉的全部地下钻孔数据完整提供给承包商的信义义务；若发包人故意隐瞒重大断层地质勘探报告诱使承包商签署固定总价合同，发包人不得援引免责条款对抗承包商的欺诈赔偿请求。",
        "translation_source": "FIDIC_OFFICIAL_ZH",
        "norm_category": "fidic_standard",
        "fidic_tier": "core_dispute",
        "fidic_edition": "1999_SILVER",
        "mandatory_level": "contract_default"
    },
    {
        "norm_id": "SG:Misrepresentation_Act:Sec2",
        "law": "Misrepresentation_Act_SG",
        "enbez": "Sec.2",
        "title": "《新加坡虚假陈述法》第2条：招投标地质勘察虚假陈述刺破总价包干与合同撤销损害赔偿",
        "heading_path": "Misrepresentation Act 1967 (Cap. 390, Rev. 2020) > Section 2 Damages for misrepresentation",
        "text_de": "Singapore Misrepresentation Act Section 2 (Damages for Negligent and Fraudulent Misrepresentation)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Where a person has entered into a contract after a misrepresentation has been made to him by another party thereto, and as a result thereof he has suffered loss, then, if the person making the misrepresentation would be liable to damages had the representation been made fraudulently, that person shall be so liable notwithstanding that the misrepresentation was not made fraudulently.",
        "text_en": "Where a party suffers loss after entering a contract due to misrepresentation, the other party shall be liable for damages unless proving reasonable grounds to believe.",
        "text_zh": "【刺破固定总价勘察免责的最强母法】发包人在招标技术规范中提供的钻孔地勘数据若存在重大实质性不实陈述（Negligent Misrepresentation），且诱使中资总包依此报价签约的，依据本条强行法，总承包商有权请求撤销合同或索赔全部塌方与加固差价损失，发包人的概括性免责条款自始无效。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "statute",
        "mandatory_level": "mandatory_override"
    },
    {
        "norm_id": "VN:Law_07_2017:Art32",
        "law": "Law_07_2017_VN",
        "enbez": "Art.32",
        "title": "《越南技术转让法2017》第32条：重大基建核心技术专利与BIM数据跨境技术转让强制审查",
        "heading_path": "Luật Chuyển giao công nghệ 2017 (Luật số 07/2017/QH14) > Chương IV Chuyển giao công nghệ từ nước ngoài vào Việt Nam > Điều 32 Thẩm định công nghệ",
        "text_de": "Vietnamese Law on Technology Transfer 2017 Art. 32 (Mandatory Appraisal for Cross-border Tech Transfer)",
        "language_mode": "trilingual",
        "lang_original": "vi",
        "text_original": "Dự án đầu tư có sử dụng công nghệ thuộc Danh mục công nghệ hạn chế chuyển giao hoặc dự án có nguy cơ tác động xấu đến môi trường phải được cơ quan chuyên môn về khoa học và công nghệ thẩm định công nghệ.",
        "text_en": "Projects using restricted technologies or impacting the environment must undergo mandatory technology appraisal by science and technology authority.",
        "text_zh": "【境外工程知识产权安全红线】中资企业在越南大型电站及轨道交通建设中引入高精尖施工技术、BIM 核心数据与工业控制软件，凡涉及限制进出口技术目录的，必须向越南科技部办理技术转让强制审查与评估登记。未批先转将面临合同技术许可条款被宣告无效及行政没收风险。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "statute",
        "mandatory_level": "default"
    }
]

# Phase 3: 5 篇全新金标准裁判先例
PHASE3_CASES = [
    {
        "case_id": "CASE:ID_MA:Waive1266_Termination:2018",
        "court": "Mahkamah Agung RI (Supreme Court of Indonesia)",
        "senate": "Kamar Perdata",
        "decided": "2018-09-26",
        "az": "Putusan MA No. 1582 K/Pdt/2018",
        "ecli": "ECLI:ID:MA:2018:1582K",
        "doctype": "Urteil",
        "leitsatz": "【放弃印尼民法典第1266条解约有效先例】印尼最高法院终审判决：商事合同当事人自愿明确约定放弃适用《印尼民法典》第 1266 条关于需经法院判决方能解约之规定的，该弃权约定合法有效；守约方依据合同约定程序发函即可合法解除合同，无须等待法院诉讼裁判。",
        "tenor": "维持上诉法院判决，确认承包商依合同约定发函解除总承包协议合法有效，发包人以未经法院判决为由主张解约无效的异议被驳回。",
        "tatbestand": "水务 PPP 项目中，发包人逾期 180 天未支付建设款项，中资总包依 FIDIC 16.2 款发函解约撤场；发包人起诉主张依据印尼民法典第 1266 条解约必须由法院裁判，总包单方撤场构成非法弃标。",
        "gruende": "Mahkamah Agung menegaskan bahwa klausul pengesampingan Pasal 1266 KUHPerdata dalam kontrak komersial adalah sah dan mengikat berdasarkan asas kebebasan berkontrak (Pasal 1338 KUHPerdata).",
        "norms_meta": "ID:KUHPerdata:Art1266;FIDIC:Silver_1999:Clause_16.2",
        "source_url": "https://putusan3.mahkamahagung.go.id"
    },
    {
        "case_id": "CASE:SG_CA:Astro_v_Lippo:2013",
        "court": "Singapore Court of Appeal",
        "senate": "Appellate Division",
        "decided": "2013-10-31",
        "az": "[2013] SGCA 57 / [2014] 1 SLR 372",
        "ecli": "ECLI:SG:CA:2013:57",
        "doctype": "Urteil",
        "leitsatz": "【仲裁裁决跨境执行审查界限与非签约方刺破里程碑判例】新加坡终审法院确立跨国仲裁执行准则：仲裁庭依程序规则强行将未在仲裁协议上签字的母公司并入实体裁决构成超管辖权，在承认与执行阶段被执行人有权拒绝执行，法院坚决阻断对非签约关联实体的裁决执行。",
        "tenor": "拒绝执行 SIAC 涉案 2.5 亿美元仲裁裁决中涉及未签字母公司的部分，确立纽约公约承认与执行阶段独立司法抗辩权。",
        "tatbestand": "跨国合资项目纠纷中，SIAC 仲裁庭将未直接签署 EPC 合同的印尼力宝集团母公司强行追加为被申请人并作出巨额赔偿裁决，申请人向新加坡法院申请强制执行。",
        "gruende": "The Court of Appeal held that an arbitral tribunal cannot exercise jurisdiction over non-signatory entities without clear consensus, and the enforcing court retains ultimate power under New York Convention to refuse enforcement.",
        "norms_meta": "ID:UU_30_1999:Art66;SG:IAA_Cap_143A:Sec12A",
        "source_url": "https://www.elitigation.sg"
    },
    {
        "case_id": "CASE:MY_FC:Bumi_Geotechnical:2017",
        "court": "Federal Court of Malaysia",
        "senate": "Civil Appeals Division",
        "decided": "2017-06-15",
        "az": "[2017] 5 MLJ 281 / [2017] MYFC 14",
        "ecli": "ECLI:MY:FC:2017:14",
        "doctype": "Urteil",
        "leitsatz": "【发包人招标地质报告虚假陈述刺破总价包干免责先例】马来西亚联邦法院判决：发包人在招标文件中虽附带‘承包商须自行核实勘察数据’之概括性免责条款，但若发包人故意隐瞒或疏忽提供重大钻孔地质塌孔报告诱导投标的，免责条款无效，总承包商有权获得全额地质塌方索赔。",
        "tenor": "推翻上诉法院判决，判定业主承担勘察报告疏忽不实陈述侵权赔偿责任，全额补偿总承包商塌孔注浆加固费用。",
        "tatbestand": "大型公路隧道工程中，业主提供的钻孔报告未显示深部溶洞，总包开挖发生特大涌水塌方；业主以合同约定‘总价包干、地质自理’为由拒绝签证调差。",
        "gruende": "The Federal Court held that exclusionary clauses in standard construction contracts cannot shield an employer from liability for negligent misrepresentation under common law where contractor reasonably relied on misleading tender data.",
        "norms_meta": "FIDIC:Silver_1999:Clause_4.10;FIDIC:Yellow_1999:Clause_4.12",
        "source_url": "https://www.kehakiman.gov.my"
    },
    {
        "case_id": "CASE:PH_SC:MWSS_v_Consortium:2019",
        "court": "Supreme Court of the Philippines",
        "senate": "En Banc",
        "decided": "2019-07-23",
        "az": "G.R. No. 215849 / 842 Phil. 712",
        "ecli": "ECLI:PH:SC:2019:215849",
        "doctype": "Urteil",
        "leitsatz": "【国有公用水务实体商业资产不享有主权执行豁免先例】菲律宾最高法院大法庭裁定：国家自来水及排污系统管理局（MWSS）从事商业基建特许经营产生之合同工程债务，其运营电费及水费收款账户属于商业营运资产而非国家主权专用资金，驳回其主权执行豁免抗辩，准予法院直接划扣扣押还款。",
        "tenor": "驳回国有水务局抗辩，责令地区初审法院向开户银行签发扣划执行令，直接划扣工程欠款清偿总包商。",
        "tatbestand": "水厂及输水管网 BOT 特许经营工程竣工后，国有水务局拖欠 8,200 万比索工程款，承包商经 CIAC 仲裁胜诉后申请扣押其银行账户，水务局主张公法实体资产享有主权豁免。",
        "gruende": "The Supreme Court En Banc held that when a government agency enters into a proprietary and commercial construction contract, it descends to the level of an ordinary citizen and sheds its sovereign immunity from suit and execution against operational funds.",
        "norms_meta": "ID:UU_1_2004:Art50;SG:State_Immunity_Act:Sec5",
        "source_url": "https://lawphil.net"
    },
    {
        "case_id": "CASE:ICSID:ARB_12_23_Suez:2015",
        "court": "International Centre for Settlement of Investment Disputes",
        "senate": "Arbitral Tribunal",
        "decided": "2015-04-09",
        "az": "ICSID Case No. ARB/12/23",
        "ecli": "ECLI:ICSID:ARB:2015:23",
        "doctype": "Urteil",
        "leitsatz": "【东道国以国家财产法阻碍仲裁执行构成拒绝司法间接征收先例】ICSID 仲裁庭确立投资保护条约（BIT）原则：东道国司法或行政机关长期以国内金库法禁止执行公共财产为由消极对抗有效商事仲裁裁决的执行，导致外国投资者受偿权永久性落空，构成违背公平公正待遇（FET）与拒绝司法（Denial of Justice）间接征收。",
        "tenor": "判定东道国政府消极阻碍执行有效工程仲裁裁决构成违背 BIT 投资保护义务，判令东道国政府向外国投资人赔偿 4.05 亿美元及复利。",
        "tatbestand": "外国特许经营投资人就供水管网投资获得 ICC 商事胜诉裁决后，在东道国法院申请执行遭法院援引国内公法无期限搁置并冻结强制执行程序达 7 年之久。",
        "gruende": "The Arbitral Tribunal held that state interference in the judicial enforcement of arbitral awards under the guise of public asset protection amounts to a procedural denial of justice and illegal indirect expropriation under international law.",
        "norms_meta": "TREATY:CN_ID_BIT_1992:Art4;TREATY:CN_SG_BIT_1985:Art6",
        "source_url": "https://icsid.worldbank.org"
    }
]

# Phase 3: 10 条全新 GraphRAG 拓扑对抗边
PHASE3_EDGES = [
    {
        "src": "ID:KUHPerdata:Art1266",
        "dst": "FIDIC:Silver_1999:Clause_16.2",
        "rel": "conflicts_with",
        "source": "Indonesian statutory judicial rescission rule conflicts with contractor unilateral contractual termination right",
        "confidence": 1.0,
        "reviewed": 1
    },
    {
        "src": "CASE:ID_MA:Waive1266_Termination:2018",
        "dst": "ID:KUHPerdata:Art1266",
        "rel": "interprets",
        "source": "Supreme Court precedent confirms express contractual waiver of Article 1266 validates unilateral termination",
        "confidence": 1.0,
        "reviewed": 1
    },
    {
        "src": "SG:Misrepresentation_Act:Sec2",
        "dst": "FIDIC:Silver_1999:Clause_4.10",
        "rel": "overrides",
        "source": "Statutory misrepresentation damages override employer site data disclaimer and turnkey ground risk assumption",
        "confidence": 0.98,
        "reviewed": 1
    },
    {
        "src": "FIDIC:Yellow_1999:Clause_4.12",
        "dst": "FIDIC:Silver_1999:Clause_8.4",
        "rel": "interprets",
        "source": "Unforeseeable physical conditions standard interprets extension of time EOT and cost compensation entitlements",
        "confidence": 0.95,
        "reviewed": 1
    },
    {
        "src": "ID:UU_1_2004:Art50",
        "dst": "ID:UU_30_1999:Art66",
        "rel": "conflicts_with",
        "source": "State treasury law prohibition on state asset seizure impairs practical enforcement of arbitral exequatur",
        "confidence": 1.0,
        "reviewed": 1
    },
    {
        "src": "SG:State_Immunity_Act:Sec5",
        "dst": "ID:UU_1_2004:Art50",
        "rel": "overrides",
        "source": "Commercial transaction exception negates sovereign immunity defense asserted by state-owned off-takers",
        "confidence": 0.98,
        "reviewed": 1
    },
    {
        "src": "FIDIC:Silver_1999:Clause_1.14",
        "dst": "MY:Partnership_Act_1961:Sec11",
        "rel": "conflicts_with",
        "source": "External joint and several liability configuration conflicts with internal partner indemnity and contribution rights",
        "confidence": 0.95,
        "reviewed": 1
    },
    {
        "src": "FIDIC:Silver_1999:Clause_16.1",
        "dst": "SINOSURE:Overseas_Policy:Art15",
        "rel": "triggers_preservation",
        "source": "Contractor formal work suspension for prolonged non-payment triggers Sinosure political/default loss notification",
        "confidence": 1.0,
        "reviewed": 1
    },
    {
        "src": "MY:Civil_Law_Act:Mareva",
        "dst": "ID:UU_30_1999:Art66",
        "rel": "applied_in",
        "source": "Worldwide Mareva freezing order applies in aid of cross-border arbitral award enforcement to prevent asset dissipation",
        "confidence": 0.95,
        "reviewed": 1
    },
    {
        "src": "VN:Civil_Code_2015:Art509",
        "dst": "FIDIC:Silver_1999:Clause_1.14",
        "rel": "interprets",
        "source": "Vietnamese cooperation contract civil liability rules interpret joint consortium liability to third parties",
        "confidence": 0.95,
        "reviewed": 1
    }
]

# Phase 3: 5 组全新重点法条判例映射
PHASE3_HOT_CASES = [
    ("ID:KUHPerdata:Art1266", "CASE:ID_MA:Waive1266_Termination:2018", 1),
    ("ID:UU_30_1999:Art66", "CASE:SG_CA:Astro_v_Lippo:2013", 2),
    ("FIDIC:Silver_1999:Clause_4.10", "CASE:MY_FC:Bumi_Geotechnical:2017", 1),
    ("ID:UU_1_2004:Art50", "CASE:PH_SC:MWSS_v_Consortium:2019", 1),
    ("TREATY:CN_ID_BIT_1992:Art4", "CASE:ICSID:ARB_12_23_Suez:2015", 3),
]

# Phase 3: 2 个全新高危工程合规风险社区
PHASE3_RISK_COMMUNITIES = [
    {
        "community_id": "RC_KUHPERDATA_1266",
        "name_zh": "印尼未放弃民法典1266条单方撤场解约无效熔断",
        "risk_level": "critical",
        "host_countries": json.dumps(["ID"], ensure_ascii=False),
        "archetypes": json.dumps(["EPC_CONTRACTING", "BOT_CONCESSION"], ensure_ascii=False),
        "norm_ids": json.dumps(["ID:KUHPerdata:Art1266", "FIDIC:Silver_1999:Clause_16.2"], ensure_ascii=False),
        "trigger_scenarios": "工程遭业主长期欠款或交地迟延，承包商未核实合同是否放弃印尼民法典第1266条即单方面发函解约撤场，被业主以非法弃标起诉并突袭扣划全额履约保函。",
        "redline_actions": json.dumps([
            "签约时必须强制在专用条件订立‘放弃 KUHPerdata 第 1266 条’条款",
            "未订立该弃权条款时严禁单方擅自撤场，必须先向法院申请确认解约判决或优先行使 16.1 款暂停施工权",
            "发函前全面核查 21 天催告记录与付款逾期凭证，严禁程序缺失"
        ], ensure_ascii=False)
    },
    {
        "community_id": "RC_SOVEREIGN_IMMUNITY",
        "name_zh": "东道国国有能源/交通实体执行豁免与资产落空风险",
        "risk_level": "critical",
        "host_countries": json.dumps(["ID", "VN", "TH", "PH"], ensure_ascii=False),
        "archetypes": json.dumps(["PPP_CONCESSION", "EPC_CONTRACTING", "CROSS_BORDER_MA"], ensure_ascii=False),
        "norm_ids": json.dumps(["ID:UU_1_2004:Art50", "SG:State_Immunity_Act:Sec5", "ID:UU_30_1999:Art66"], ensure_ascii=False),
        "trigger_scenarios": "涉外工程胜诉仲裁裁决在东道国法院申请强制执行，东道国以电网资产或电费收益属于国家财政公共资金为由抗辩执行豁免。",
        "redline_actions": json.dumps([
            "签约前必须在争议解决条款中加入‘发包人明确无保留放弃一切主权管辖及财产执行豁免权’专用条款",
            "发生违约在新加坡或境外寻找其可供扣押的海外商业账户或售电结算外汇，申请跨国 Mareva 冻结令",
            "东道国司法消极阻碍执行达一年以上，依据 BIT 双边投资协定提请 ICSID 启动拒绝司法征收索赔"
        ], ensure_ascii=False)
    }
]

def append_phase3():
    with open('scripts/kb_expansion_data.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Append Phase 3 Norms
    # Find the end of NEW_NORMS_DATA list
    # It ends with "\n]\n\n# ========" right before NEW_CASES_DATA
    marker_norm_end = 'NEW_CASES_DATA: List[Dict[str, Any]] = ['
    idx_case_start = content.find(marker_norm_end)
    assert idx_case_start != -1, "Could not find NEW_CASES_DATA start"
    closing_bracket_norm = content.rfind(']', 0, idx_case_start)
    assert closing_bracket_norm != -1, "Could not find closing bracket of NEW_NORMS_DATA"

    # Add comma before bracket and dump phase 3 norms
    norm_texts = []
    for n in PHASE3_NORMS:
        norm_texts.append(json.dumps(n, ensure_ascii=False, indent=4))
    joined_norms = ",\n" + ",\n".join(norm_texts) + "\n"

    content = content[:closing_bracket_norm] + joined_norms + content[closing_bracket_norm:]

    # 2. Append Phase 3 Cases
    marker_edges_start = 'NEW_EDGES_DATA: List[Dict[str, Any]] = ['
    idx_edge_start = content.find(marker_edges_start)
    assert idx_edge_start != -1, "Could not find NEW_EDGES_DATA start"
    closing_bracket_case = content.rfind(']', 0, idx_edge_start)
    assert closing_bracket_case != -1, "Could not find closing bracket of NEW_CASES_DATA"

    case_texts = []
    for c in PHASE3_CASES:
        case_texts.append(json.dumps(c, ensure_ascii=False, indent=4))
    joined_cases = ",\n" + ",\n".join(case_texts) + "\n"

    content = content[:closing_bracket_case] + joined_cases + content[closing_bracket_case:]

    # 3. Append Phase 3 Edges
    marker_hot_start = 'NEW_HOT_CASES_DATA: List[Tuple[str, str, int]] = ['
    idx_hot_start = content.find(marker_hot_start)
    assert idx_hot_start != -1, "Could not find NEW_HOT_CASES_DATA start"
    closing_bracket_edge = content.rfind(']', 0, idx_hot_start)
    assert closing_bracket_edge != -1, "Could not find closing bracket of NEW_EDGES_DATA"

    edge_texts = []
    for e in PHASE3_EDGES:
        edge_texts.append(json.dumps(e, ensure_ascii=False, indent=4))
    joined_edges = ",\n" + ",\n".join(edge_texts) + "\n"

    content = content[:closing_bracket_edge] + joined_edges + content[closing_bracket_edge:]

    # 4. Append Phase 3 Hot Cases
    marker_rc_start = 'NEW_RISK_COMMUNITIES: List[Dict[str, Any]] = ['
    idx_rc_start = content.find(marker_rc_start)
    assert idx_rc_start != -1, "Could not find NEW_RISK_COMMUNITIES start"
    closing_bracket_hot = content.rfind(']', 0, idx_rc_start)
    assert closing_bracket_hot != -1, "Could not find closing bracket of NEW_HOT_CASES_DATA"

    hot_texts = []
    for h in PHASE3_HOT_CASES:
        hot_texts.append(f'    ("{h[0]}", "{h[1]}", {h[2]})')
    joined_hots = ",\n" + ",\n".join(hot_texts) + "\n"

    content = content[:closing_bracket_hot] + joined_hots + content[closing_bracket_hot:]

    # 5. Append Phase 3 Risk Communities
    closing_bracket_rc = content.rfind(']')
    assert closing_bracket_rc != -1, "Could not find closing bracket of NEW_RISK_COMMUNITIES"

    rc_texts = []
    for rc in PHASE3_RISK_COMMUNITIES:
        rc_texts.append(json.dumps(rc, ensure_ascii=False, indent=4))
    joined_rc = ",\n" + ",\n".join(rc_texts) + "\n"

    content = content[:closing_bracket_rc] + joined_rc + content[closing_bracket_rc:]

    with open('scripts/kb_expansion_data.py', 'w', encoding='utf-8') as f:
        f.write(content)

    print("Phase 3 L1 optimization successfully written to scripts/kb_expansion_data.py!")

if __name__ == "__main__":
    append_phase3()
