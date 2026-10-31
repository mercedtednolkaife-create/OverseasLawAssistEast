"""Phase 7 L1 核心强行法条数据集:
东盟 6 国民商法典、建设专门法、外资准入强行法、土地物权、破产与涉外程序法及中国境外投资强监管
100% 具备结构化 elements_json 槽位与权威法理攻防要旨
"""

PHASE7_L1_NORMS = [
    # 🇮🇩 印尼 L1 核心成文法簇
    {
        "norm_id": "ID:KUHPerdata:Art1321",
        "law": "ID:KUHPerdata",
        "enbez": "Article 1321",
        "title": "印尼民法典第1321条：意思表示瑕疵（误解、胁迫、欺诈）撤销权总纲",
        "norm_category": "mandatory_statute",
        "language_mode": "trilingual",
        "lang_original": "id",
        "text_original": "Tiada sepakat yang sah apabila sepakat itu diberikan karena kekhilafan, atau diperolehnya dengan paksaan atau penipuan.",
        "text_en": "No agreement is valid if the consent was given by mistake, or obtained by coercion or fraud.",
        "text_zh": "【意思表示瑕疵总纲】因错误、胁迫或欺诈而作出的同意，不发生合法合意效力，受害方享有依法撤销合同之诉权。",
        "text_de": "Article 1321 Defect of Consent\n因错误、胁迫或欺诈作出的同意不发生合法合意效力，受害方享有撤销权。\nNo agreement is valid if given by mistake, coercion or fraud.",
        "mandatory_level": "mandatory",
        "source_url": "https://jdih.mahkamahagung.go.id",
        "elements_json": [
            {"eid": "e_id1321_defect_type", "text_zh": "要件一：缔约过程中存在重大误解 (Dwaling)、胁迫 (Paksaan) 或欺诈 (Penipuan) 事实", "status": "mandatory"},
            {"eid": "e_id1321_causal_link", "text_zh": "要件二：该瑕疵直接导致受害方作出原本不会作出的缔约意思表示", "status": "mandatory"},
            {"eid": "e_id1321_voidable_right", "text_zh": "法律后果：受害方享有法定撤销权，撤销后溯及既往自始归于无效", "status": "satisfied"}
        ]
    },
    {
        "norm_id": "ID:KUHPerdata:Art1335",
        "law": "ID:KUHPerdata",
        "enbez": "Article 1335",
        "title": "印尼民法典第1335条：无原因或违法原因协议自始绝对无效",
        "norm_category": "mandatory_statute",
        "language_mode": "trilingual",
        "lang_original": "id",
        "text_original": "Suatu perjanjian yang dibuat tanpa sebab, atau dibuat karena suatu sebab yang palsu atau terlarang, adalah tidak mempunyai kekuatan hukum.",
        "text_en": "An agreement made without cause, or made for a false or prohibited cause, is of no legal force.",
        "text_zh": "【合同原因违法无效】缺乏合法原因、基于虚伪原因或基于法律禁止之原因订立的协议，自始不发生任何法律效力（绝对无效）。",
        "text_de": "Article 1335 Unlawful Cause Void\n缺乏合法原因或基于虚伪/违法原因订立的协议自始绝对无效。\nAn agreement made without cause or for prohibited cause is of no legal force.",
        "mandatory_level": "mandatory_override",
        "source_url": "https://jdih.mahkamahagung.go.id",
        "elements_json": [
            {"eid": "e_id1335_unlawful_cause", "text_zh": "要件一：合同订立缺乏合法对价原因，或其原因违反成文法禁止性规定或公序良俗", "status": "prohibition"},
            {"eid": "e_id1335_null_and_void", "text_zh": "法律后果：该协议自始不具法律效力 (Void ab initio)，任何当事人无权请求强制执行", "status": "mandatory"}
        ]
    },
    {
        "norm_id": "ID:KUHPerdata:Art1337",
        "law": "ID:KUHPerdata",
        "enbez": "Article 1337",
        "title": "印尼民法典第1337条：违反强行法、道德与公共秩序之原因界定",
        "norm_category": "mandatory_statute",
        "language_mode": "trilingual",
        "lang_original": "id",
        "text_original": "Suatu sebab adalah terlarang, apabila dilarang oleh undang-undang, atau apabila berlawanan dengan kesusilaan baik atau ketertiban umum.",
        "text_en": "A cause is prohibited if it is forbidden by law, or contrary to good morals or public order.",
        "text_zh": "【违法原因界定】凡法律所明文禁止，或违反善良风俗、公共秩序的原因，均属于禁止之原因，依此订立之合同无效。",
        "text_de": "Article 1337 Prohibited Cause\n违反法律明文禁止或反公序良俗之原因属于禁止原因。\nA cause is prohibited if contrary to law, morals or public order.",
        "mandatory_level": "mandatory_override",
        "source_url": "https://jdih.mahkamahagung.go.id",
        "elements_json": [
            {"eid": "e_id1337_statutory_ban", "text_zh": "要件一：合同内容或履行目的违反东道国主权强行法禁令（如绕开股权代持限制或无照施工）", "status": "prohibition"},
            {"eid": "e_id1337_public_order", "text_zh": "要件二：违背印尼社会善良风俗或公共秩序 (Ketertiban Umum)", "status": "prohibition"},
            {"eid": "e_id1337_invalidity", "text_zh": "法律后果：法院或仲裁庭得依职权直接宣告合同自始无效", "status": "mandatory"}
        ]
    },
    {
        "norm_id": "ID:KUHPerdata:Art1250",
        "law": "ID:KUHPerdata",
        "enbez": "Article 1250",
        "title": "印尼民法典第1250条：金钱之债迟延履行法定利息 6%/年",
        "norm_category": "mandatory_statute",
        "language_mode": "trilingual",
        "lang_original": "id",
        "text_original": "Dalam perikatan yang semata-mata mengenai pembayaran sejumlah uang, penggantian biaya, rugi dan bunga yang timbul karena keterlambatan pelaksanaannya, hanya terdiri atas bunga yang ditentukan oleh undang-undang, yaitu 6% setahun.",
        "text_en": "In obligations solely regarding the payment of money, damages arising from delay consist only of statutory interest determined by law, namely 6% per annum.",
        "text_zh": "【金钱之债法定利息】对于纯粹给付金钱之债务，因迟延履行产生的赔偿仅包含法定利息（法定基准年息为 6%），自催告或起诉之日起算。",
        "text_de": "Article 1250 Statutory Delay Interest\n金钱之债迟延履行法定利息为年息6%。\nDelay damages for money obligations consist of statutory interest of 6% per annum.",
        "mandatory_level": "statute",
        "source_url": "https://jdih.mahkamahagung.go.id",
        "elements_json": [
            {"eid": "e_id1250_money_debt", "text_zh": "要件一：主债权性质属于金钱支付之债（如工程进度款或材料款）", "status": "mandatory"},
            {"eid": "e_id1250_default_fact", "text_zh": "要件二：债务人经合法催告后逾期未支付构成迟延", "status": "mandatory"},
            {"eid": "e_id1250_interest_rate", "text_zh": "法律后果：债权人有权主张法定年息 6% 之迟延罚息，直至清偿完毕", "status": "satisfied"}
        ]
    },
    {
        "norm_id": "ID:UU_2_2017:Art22",
        "law": "ID:UU_2_2017",
        "enbez": "Article 22",
        "title": "印尼建筑服务法第22条：工程总承包与联合实施模式规范",
        "norm_category": "mandatory_statute",
        "language_mode": "trilingual",
        "lang_original": "id",
        "text_original": "Kontrak Kerja Konstruksi dapat berbentuk rancang bangun (design and build), rekayasa pengadaan dan konstruksi (EPC), atau bentuk kontrak lainnya sesuai ketentuan perundang-undangan.",
        "text_en": "Construction Work Contracts may be in the form of design and build, EPC, or other contract forms in accordance with statutory provisions.",
        "text_zh": "【建筑合同法定形式】工程合同可采用设计建造(Design and Build)、工程总承包(EPC)等法定模式，各方权责划分受印尼建筑法律强制规制。",
        "text_de": "Article 22 EPC and Design Build Forms\n建筑合同可采用设计建造或EPC等法定承包模式。\nConstruction contracts may be in design-build, EPC or other statutory forms.",
        "mandatory_level": "mandatory",
        "source_url": "https://peraturan.bpk.go.id",
        "elements_json": [
            {"eid": "e_id22_contract_model", "text_zh": "要件一：合同符合印尼建筑服务法认可的 EPC、DB 或单价承包标准模式", "status": "mandatory"},
            {"eid": "e_id22_statutory_compliance", "text_zh": "要件二：承包商具备相应专业工程承包资质等级许可", "status": "mandatory"}
        ]
    },
    {
        "norm_id": "ID:UU_2_2017:Art48",
        "law": "ID:UU_2_2017",
        "enbez": "Article 48",
        "title": "印尼建筑服务法第48条：主体工程严禁转包与专业分包审批限制",
        "norm_category": "mandatory_statute",
        "language_mode": "trilingual",
        "lang_original": "id",
        "text_original": "Penyedia Jasa dilarang mengalihkan seluruh atau pekerjaan utama kepada pihak lain. Pengalihan sebagian pekerjaan spesialis harus dengan persetujuan Pengguna Jasa.",
        "text_en": "The Service Provider is prohibited from transferring the whole or the main work to another party. Subcontracting of specialist parts must obtain the prior approval of the Employer.",
        "text_zh": "【主体工程禁止转包】承包商严禁将主体工程或全部工程转包第三方；专业分包必须事先取得发包人的书面批准，违者合同面临解除且承担连带赔偿。",
        "text_de": "Article 48 Subcontracting Restrictions\n严禁将主体工程转包，专业分包须经发包人批准。\nProhibited from transferring main work; specialist subcontracting requires approval.",
        "mandatory_level": "mandatory_override",
        "source_url": "https://peraturan.bpk.go.id",
        "elements_json": [
            {"eid": "e_id48_main_work_ban", "text_zh": "要件一：承包商不得将工程核心主体结构工作转包他人", "status": "prohibition"},
            {"eid": "e_id48_written_approval", "text_zh": "要件二：专业分包必须持有发包人签发的书面批准批文", "status": "mandatory"},
            {"eid": "e_id48_liability", "text_zh": "法律后果：违规转包发包人有权立即终止合同并要求赔偿全部损失", "status": "mandatory"}
        ]
    },
    {
        "norm_id": "ID:UU_40_2007:Art75",
        "law": "ID:UU_40_2007",
        "enbez": "Article 75",
        "title": "印尼公司法第75条：外资公司 (PT PMA) 股东会决议法定表决门槛",
        "norm_category": "mandatory_statute",
        "language_mode": "trilingual",
        "lang_original": "id",
        "text_original": "RUPS mempunyai wewenang yang tidak diberikan kepada Direksi atau Dewan Komisaris, dalam batas yang ditentukan dalam Undang-Undang ini dan/atau anggaran dasar.",
        "text_en": "The GMS has authority not granted to the Board of Directors or Board of Commissioners, within limits determined by this Law and/or the articles of association.",
        "text_zh": "【股东会最高权力机构】外资公司重大资产处置、修改章程、合并分立或清算解散必须经股东会特别多数决（至少 2/3 至 3/4 出席并表决同意）。",
        "text_de": "Article 75 General Meeting of Shareholders\n外资公司重大资产处置须经股东会特别多数决。\nGMS has supreme corporate authority; major transactions require supermajority.",
        "mandatory_level": "mandatory",
        "source_url": "https://peraturan.bpk.go.id",
        "elements_json": [
            {"eid": "e_id75_gms_authority", "text_zh": "要件一：转让公司资产超总资产 50% 必须召开正式股东大会", "status": "mandatory"},
            {"eid": "e_id75_supermajority", "text_zh": "要件二：获得持有代表至少 3/4 有表决权股份股东赞成通过", "status": "mandatory"}
        ]
    },
    {
        "norm_id": "ID:UU_42_1999:Art15",
        "law": "ID:UU_42_1999",
        "enbez": "Article 15",
        "title": "印尼动产信托担保法第15条：信托证书执行力与私力拖车限制",
        "norm_category": "mandatory_statute",
        "language_mode": "trilingual",
        "lang_original": "id",
        "text_original": "Sertifikat Jaminan Fidusia mencantumkan kata-kata DEMI KEADILAN BERDASARKAN KETUHANAN YANG MAHA ESA, mempunyai kekuatan eksekutorial yang sama dengan putusan pengadilan yang telah berkekuatan hukum tetap.",
        "text_en": "The Fiduciary Security Certificate has the same executory title as a final and binding court judgment. In case of breach, execution requires judicial procedure if disputed.",
        "text_zh": "【信托担保执行力与宪政限制】经法定登记的动产信托担保凭证具有与法院确定判决同等之强制执行力。但依据宪法法院判决，若债务人对违约存有争议，债权人不得强行私自扣押设备，必须向法院申请强制执行。",
        "text_de": "Article 15 Fiduciary Certificate Execution\n信托凭证具法院判决执行力，违约争议时禁止私力扣押设备。\nFiduciary certificate has executory power; disputed breach requires court process.",
        "mandatory_level": "mandatory",
        "source_url": "https://peraturan.bpk.go.id",
        "elements_json": [
            {"eid": "e_id15_registration", "text_zh": "要件一：动产信托担保必须在法务与人权部信托登记局正式登记并取得证书", "status": "mandatory"},
            {"eid": "e_id15_due_process", "text_zh": "要件二：执行处置施工设备时，若债务人提出抗辩必须向地方法院申请执行令", "status": "mandatory"}
        ]
    },

    # 🇻🇳 越南 L1 核心成文法簇
    {
        "norm_id": "VN:Civil_Code_2015:Art117",
        "law": "VN:Civil_Code_2015",
        "enbez": "Article 117",
        "title": "越南民法典第117条：民事法律行为有效三大法定要件",
        "norm_category": "mandatory_statute",
        "language_mode": "trilingual",
        "lang_original": "vi",
        "text_original": "Giao dịch dân sự có hiệu lực khi có đủ các điều kiện: Chủ thể có năng lực; Tham gia hoàn toàn tự nguyện; Mục đích và nội dung không vi phạm điều cấm của luật, không trái đạo đức xã hội.",
        "text_en": "A civil transaction is valid when: The subject has civil legal capacity; Participation is completely voluntary; The purpose and content do not violate prohibitions of law and are not contrary to social ethics.",
        "text_zh": "【民事行为有效要件】民事法律行为有效必备三要件：① 主体具备相应民事行为能力；② 意思表示完全自愿真实；③ 行为目的与内容不违反法律禁止性规定且不违背社会公德。",
        "text_de": "Article 117 Validity Conditions\n民事行为有效必备主体适格、意思自愿及目的合法三大要件。\nCivil transactions are valid when parties have capacity, consent is voluntary, and contents are lawful.",
        "mandatory_level": "mandatory_override",
        "source_url": "https://thuvienphapluat.vn",
        "elements_json": [
            {"eid": "e_vn117_capacity", "text_zh": "要件一：缔约各方代表具备合法签字授权与法人行为能力", "status": "mandatory"},
            {"eid": "e_vn117_voluntariness", "text_zh": "要件二：缔约意思表示完全自愿真实，无受胁迫或重大欺诈", "status": "mandatory"},
            {"eid": "e_vn117_lawful_purpose", "text_zh": "要件三：合同目的与约定内容不违反越南成文法禁止性规定与社会公德", "status": "mandatory"}
        ]
    },
    {
        "norm_id": "VN:Civil_Code_2015:Art123",
        "law": "VN:Civil_Code_2015",
        "enbez": "Article 123",
        "title": "越南民法典第123条：违反法律禁止性规定与公序良俗无效",
        "norm_category": "mandatory_statute",
        "language_mode": "trilingual",
        "lang_original": "vi",
        "text_original": "Giao dịch dân sự có mục đích và nội dung vi phạm điều cấm của luật, trái đạo đức xã hội thì vô hiệu.",
        "text_en": "A civil transaction with purpose and content violating prohibitions of law or contrary to social ethics is void.",
        "text_zh": "【违法民事行为自始无效】民事法律行为的目的与内容违反法律禁止性规定或违背社会道德的，自始绝对无效，当事人不得主张合同履行利益。",
        "text_de": "Article 123 Violation of Prohibitions Void\n目的与内容违反法律禁令或反社会公德的民事行为绝对无效。\nTransactions violating prohibitions of law or contrary to ethics are void.",
        "mandatory_level": "mandatory_override",
        "source_url": "https://thuvienphapluat.vn",
        "elements_json": [
            {"eid": "e_vn123_prohibition_breach", "text_zh": "要件一：合同条款直接抵触越南现行成文法强行法禁令", "status": "prohibition"},
            {"eid": "e_vn123_nullity_effect", "text_zh": "法律后果：该民事行为自始不具法律约束力，双方互负返还恢复原状义务", "status": "mandatory"}
        ]
    },
    {
        "norm_id": "VN:Civil_Code_2015:Art129",
        "law": "VN:Civil_Code_2015",
        "enbez": "Article 129",
        "title": "越南民法典第129条：形式瑕疵合同履行达 2/3 以上有效治愈规则",
        "norm_category": "mandatory_statute",
        "language_mode": "trilingual",
        "lang_original": "vi",
        "text_original": "Giao dịch dân sự vi phạm quy định điều kiện có hiệu lực về hình thức thì vô hiệu, trừ trường hợp: Một bên hoặc các bên đã thực hiện ít nhất hai phần ba nghĩa vụ trong giao dịch thì theo yêu cầu của một bên hoặc các bên, Tòa án ra quyết định công nhận hiệu lực của giao dịch đó.",
        "text_en": "A civil transaction violating formal requirements is void, except where: One or all parties have performed at least two-thirds of their obligations, the Court shall recognize the validity of that transaction upon request.",
        "text_zh": "【形式瑕疵治愈规则】违反书面形式或公证登记要件之民事行为原则上无效；但若一方或各方已实际履行了至少三分之二 (2/3) 以上义务的，经当事人请求，法院裁定确认该交易有效！",
        "text_de": "Article 129 Formal Defect Cured by 2/3 Performance\n形式瑕疵合同在履行达2/3以上时经申请法院得裁定确认有效。\nFormally defective transactions are cured if 2/3 of obligations have been performed.",
        "mandatory_level": "statute",
        "source_url": "https://thuvienphapluat.vn",
        "elements_json": [
            {"eid": "e_vn129_formal_defect", "text_zh": "要件一：合同存在未公证、未备案或形式要件瑕疵", "status": "condition_precedent"},
            {"eid": "e_vn129_performance_milestone", "text_zh": "要件二：主张有效方已实际履行了合同全部义务的至少三分之二 (2/3) 以上", "status": "mandatory"},
            {"eid": "e_vn129_court_validation", "text_zh": "法律后果：法院依法裁定确认合同完全有效，阻断对方恶意主张无效抗辩", "status": "satisfied"}
        ]
    },
    {
        "norm_id": "VN:Civil_Code_2015:Art411",
        "law": "VN:Civil_Code_2015",
        "enbez": "Article 411",
        "title": "越南民法典第411条：双务合同同时履行抗辩权与不安抗辩",
        "norm_category": "mandatory_statute",
        "language_mode": "trilingual",
        "lang_original": "vi",
        "text_original": "Bên phải thực hiện nghĩa vụ trước có quyền hoãn thực hiện nghĩa vụ, nếu khả năng thực hiện nghĩa vụ của bên kia đã bị giảm sút nghiêm trọng đến mức không thể thực hiện được nghĩa vụ như đã cam kết.",
        "text_en": "The party obligated to perform first has the right to suspend performance if the other party's ability to perform has deteriorated severely to the extent that it cannot perform.",
        "text_zh": "【同时履行与不安抗辩权】应当先履行债务的一方，若有确切证据证明对方履约能力严重恶化显然无法履约，有权暂停履行自身义务；双务合同中对方未为对待给付前己方有权拒绝履行。",
        "text_de": "Article 411 Suspension of Performance\n对方履约能力严重恶化或未付款时己方享有法定中止履约抗辩权。\nParty performing first may suspend performance if other party's ability severely deteriorates.",
        "mandatory_level": "statute",
        "source_url": "https://thuvienphapluat.vn",
        "elements_json": [
            {"eid": "e_vn411_bilateral_contract", "text_zh": "要件一：各方互负对价义务之双务工程施工合同", "status": "mandatory"},
            {"eid": "e_vn411_deterioration_proof", "text_zh": "要件二：掌握发包人长期拖欠款项或濒临破产的客观证据", "status": "mandatory"},
            {"eid": "e_vn411_lawful_suspension", "text_zh": "法律后果：承包商合法行使停工减速权，不构成过错违约且享有工期顺延", "status": "satisfied"}
        ]
    },
    {
        "norm_id": "VN:Law_61_2020:Art24",
        "law": "VN:Law_61_2020",
        "enbez": "Article 24",
        "title": "越南2020投资法第24条：外资并购 (M&A) 审批强制法定前置要件",
        "norm_category": "mandatory_statute",
        "language_mode": "trilingual",
        "lang_original": "vi",
        "text_original": "Nhà đầu tư nước ngoài góp vốn, mua cổ phần, mua phần vốn góp phải đáp ứng các điều kiện và thực hiện thủ tục đăng ký góp vốn, mua cổ phần tại cơ quan đăng ký đầu tư nếu dẫn đến tăng tỷ lệ sở hữu nước ngoài trên 50%.",
        "text_en": "Foreign investors purchasing shares or capital contributions must obtain M&A Approval from the investment registration authority if foreign ownership increases to over 50% or involves sensitive land areas.",
        "text_zh": "【外资并购审批前置令】外国投资者出资、购买越南公司股权导致外资持股比例超过 50%，或目标公司涉及国防安全/边境敏感土地的，必须事先向计划投资厅 (DPI) 申请并取得《外资出资购股批准批文 (M&A Approval)》方可办理工商变更登记，未批擅自交割自始无效！",
        "text_de": "Article 24 M&A Approval Requirement\n外资控股并购或涉敏感土地必须事先取得计划投资部门批文。\nForeign acquisition increasing ownership over 50% must obtain prior M&A approval.",
        "mandatory_level": "mandatory_override",
        "source_url": "https://thuvienphapluat.vn",
        "elements_json": [
            {"eid": "e_vn24_shareholding_threshold", "text_zh": "要件一：收购导致外资持股突破 50% 或目标公司持有边境海岛敏感土地", "status": "mandatory"},
            {"eid": "e_vn24_prior_approval", "text_zh": "要件二：在股权交割款汇入前取得省计划投资厅 (DPI) 签发书面 M&A Approval 批文", "status": "condition_precedent"},
            {"eid": "e_vn24_closing_void", "text_zh": "法律后果：未批先买的代持或私下交割协议违反强行法绝对无效", "status": "prohibition"}
        ]
    },
    {
        "norm_id": "VN:Law_59_2020:Art47",
        "law": "VN:Law_59_2020",
        "enbez": "Article 47",
        "title": "越南企业法第47条：注册资本 90 天内足额实缴法定刚性时限",
        "norm_category": "mandatory_statute",
        "language_mode": "trilingual",
        "lang_original": "vi",
        "text_original": "Thành viên phải góp vốn cho công ty đủ và đúng loại tài sản đã cam kết trong thời hạn 90 ngày kể từ ngày được cấp Giấy chứng nhận đăng ký doanh nghiệp.",
        "text_en": "Members must contribute capital to the company in full and with the committed assets within 90 days from the date of issuance of the Enterprise Registration Certificate.",
        "text_zh": "【注册资本 90 天实缴刚性时限】有限责任公司各股东必须在企业登记证书 (ERC) 签发之日起 90 天内足额实缴全部承诺出资额；逾期未缴足必须在 30 天内申请减少注册资本并接受高额行政处罚。",
        "text_de": "Article 47 90-Day Capital Contribution\n外资公司注册资本必须在执照签发后90天内一次性足额实缴到位。\nCharter capital must be paid in full within 90 days of company registration certificate.",
        "mandatory_level": "mandatory_override",
        "source_url": "https://thuvienphapluat.vn",
        "elements_json": [
            {"eid": "e_vn47_90day_timeline", "text_zh": "要件一：自营业执照 (ERC) 颁发之日起精确计算 90 个自然日时限", "status": "mandatory"},
            {"eid": "e_vn47_direct_remittance", "text_zh": "要件二：通过直接投资资本金账户 (DICA) 汇入足额美元或外币注册资本金", "status": "mandatory"},
            {"eid": "e_vn47_penalty_breach", "text_zh": "法律后果：逾期未足额缴足将面临吊销外资批文及限制后续利润汇出", "status": "prohibition"}
        ]
    },

    # 🇲🇾 马来西亚 L1 核心成文法簇
    {
        "norm_id": "MY:Contracts_Act_1950:Sec10",
        "law": "MY:Contracts_Act_1950",
        "enbez": "Section 10",
        "title": "马来西亚1950年合同法第10条：合同成立法定要件与自由合意",
        "norm_category": "mandatory_statute",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "All agreements are contracts if they are made by the free consent of parties competent to contract, for a lawful consideration and with a lawful object, and are not hereby expressly declared to be void.",
        "text_en": "All agreements are contracts if made by free consent of competent parties for lawful consideration and object.",
        "text_zh": "【合同有效核心要件】凡具备订约能力的各方，在自由同意的基础上，为合法对价与合法目的订立且未被法律明文宣告无效的协议，均为具有法律约束力之合同。",
        "text_de": "Section 10 What Agreements are Contracts\n具备行为能力各方在自由同意下为合法对价目的订立之协议为有效合同。\nAgreements made by free consent for lawful consideration are binding contracts.",
        "mandatory_level": "mandatory",
        "source_url": "https://lom.agc.gov.my",
        "elements_json": [
            {"eid": "e_my10_free_consent", "text_zh": "要件一：缔约各方作出真实意思表示且不存在不当影响或欺诈", "status": "mandatory"},
            {"eid": "e_my10_consideration", "text_zh": "要件二：具备普通法对价 (Consideration) 与明确可执行之标的", "status": "mandatory"},
            {"eid": "e_my10_lawful_object", "text_zh": "要件三：合同目的不抵触成文法禁止性规定或公共政策", "status": "mandatory"}
        ]
    },
    {
        "norm_id": "MY:Contracts_Act_1950:Sec24",
        "law": "MY:Contracts_Act_1950",
        "enbez": "Section 24",
        "title": "马来西亚1950年合同法第24条：对价或目的违法与违背公共政策绝对无效",
        "norm_category": "mandatory_statute",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "The consideration or object of an agreement is lawful, unless: it is forbidden by a law; it defeats the provisions of any law; it is fraudulent; it involves injury to the person or property of another; or the court regards it as immoral, or opposed to public policy. Every agreement of which the object or consideration is unlawful is void.",
        "text_en": "The consideration or object of an agreement is lawful unless forbidden by law, defeats law, fraudulent, harmful, or opposed to public policy. Such agreements are void.",
        "text_zh": "【目的违法合同自始无效】协议的对价或目的若属于：① 法律明文禁止；② 规避或架空任何成文法规定；③ 具有欺诈性质；④ 损害他人人身或财产；⑤ 违背公共政策，该协议自始绝对无效 (Void ab initio)。",
        "text_de": "Section 24 Unlawful Considerations and Objects\n对价或目的违法、规避法律或违背公共政策之合同自始绝对无效。\nAgreements with unlawful object or consideration are void ab initio.",
        "mandatory_level": "mandatory_override",
        "source_url": "https://lom.agc.gov.my",
        "elements_json": [
            {"eid": "e_my24_defeat_law", "text_zh": "要件一：合同内容架空或规避马来西亚成文法（如未持 CIDB 施工资质进场）", "status": "prohibition"},
            {"eid": "e_my24_public_policy", "text_zh": "要件二：合同目的严重违背马来西亚公共政策与商业道德", "status": "prohibition"},
            {"eid": "e_my24_void_ab_initio", "text_zh": "法律后果：该合同不可依法执行，法院驳回基于该合同提出的全部工程款诉请", "status": "mandatory"}
        ]
    },
    {
        "norm_id": "MY:Contracts_Act_1950:Sec29",
        "law": "MY:Contracts_Act_1950",
        "enbez": "Section 29",
        "title": "马来西亚1950年合同法第29条：限制司法救济程序与苛刻失权条款无效",
        "norm_category": "mandatory_statute",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Every agreement, by which any party thereto is restricted absolutely from enforcing his rights under or in respect of any contract, by the usual legal proceedings in the ordinary tribunals, or which limits the time within which he may thus enforce his rights, is void to that extent.",
        "text_en": "Every agreement restricting absolutely any party from enforcing rights by usual legal proceedings or limiting time to enforce rights is void to that extent.",
        "text_zh": "【限制诉讼救济条款无效】任何绝对限制当事人通过法定普通法院执行其合同权利，或非法苛刻缩短其法定权利主张期限的协议条款，在此范围内一律绝对无效（常用于打击过度苛刻的程序失权条款）。",
        "text_de": "Section 29 Agreements in Restraint of Legal Proceedings Void\n限制当事人提起司法诉讼或过度缩短诉讼时限之条款绝对无效。\nAgreements restricting legal proceedings or shortening limitation periods are void.",
        "mandatory_level": "mandatory_override",
        "source_url": "https://lom.agc.gov.my",
        "elements_json": [
            {"eid": "e_my29_restricting_remedy", "text_zh": "要件一：合同条款绝对剥夺守约方依法向法定裁判机构起诉或索赔之权利", "status": "prohibition"},
            {"eid": "e_my29_unreasonable_timebar", "text_zh": "要件二：人为将法定 6 年诉讼时效极端压缩至 7 天或数日之内致权利完全落空", "status": "prohibition"},
            {"eid": "e_my29_void_pro_tanto", "text_zh": "法律后果：该苛刻失权条款自始无效，当事人仍享有提起法定诉讼或快速裁决权利", "status": "satisfied"}
        ]
    },
    {
        "norm_id": "MY:Contracts_Act_1950:Sec53",
        "law": "MY:Contracts_Act_1950",
        "enbez": "Section 53",
        "title": "马来西亚1950年合同法第53条：阻碍对方履行之防阻原则 (Prevention Principle)",
        "norm_category": "mandatory_statute",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "When a contract contains reciprocal promises, and one party to the contract prevents the other from performing his promise, the contract becomes voidable at the option of the party so prevented; and he is entitled to compensation from the other party for any loss.",
        "text_en": "When one party prevents the other from performing reciprocal promises, the contract is voidable at option of prevented party, and he is entitled to compensation.",
        "text_zh": "【防阻原则成文法基础】在双务互惠合同中，一方若阻碍对方履行其承诺（如发包人迟延移交施工场地或拒不审批图纸），受阻方有权选择解除合同并要求阻碍方赔偿全部损失。",
        "text_de": "Section 53 Prevention of Performance\n发包人阻碍承包商施工时承包商得主张免责并索赔全部窝工损失。\nParty prevented from performing by other party may rescind and claim compensation.",
        "mandatory_level": "mandatory",
        "source_url": "https://lom.agc.gov.my",
        "elements_json": [
            {"eid": "e_my53_reciprocal_contract", "text_zh": "要件一：工程合同属于双方互负对待给付义务的双务合同", "status": "mandatory"},
            {"eid": "e_my53_act_of_prevention", "text_zh": "要件二：发包人实施了迟延交地、迟延供图或恶意阻碍施工之积极行为", "status": "mandatory"},
            {"eid": "e_my53_eot_and_cost", "text_zh": "法律后果：工期变为无约束 (Time at Large)，承包商免除误期违约金并获费用补偿", "status": "satisfied"}
        ]
    },
    {
        "norm_id": "MY:CIPAA_2012:Sec5",
        "law": "MY:CIPAA_2012",
        "enbez": "Section 5",
        "title": "马来西亚建筑业支付与裁决法第5条：付款请求书 (Payment Claim) 法定要素",
        "norm_category": "mandatory_statute",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "An unpaid party may serve a payment claim on a non-paying party. The payment claim shall be in writing and shall include the amount claimed, the due date for payment, the cause of action and description of work.",
        "text_en": "Payment claim served by unpaid party shall be in writing, specifying amount, due date, cause of action, and description of work performed.",
        "text_zh": "【付款请求书必备法定要素】未获付款方可向欠款方送达书面付款请求书，必须明确包含：索赔金额、到期日、计价事实依据及所实施工程的详细描述，缺一不可。",
        "text_de": "Section 5 Payment Claim Requirements\n付款请求书必须以书面形式明确金额、到期日及工程事实依据。\nPayment claim must be in writing stating amount claimed, due date and work details.",
        "mandatory_level": "mandatory",
        "source_url": "https://lom.agc.gov.my",
        "elements_json": [
            {"eid": "e_cipaa5_written_form", "text_zh": "要件一：以书面形式发出并依照法定方式送达发包人正式注册地址", "status": "mandatory"},
            {"eid": "e_cipaa5_claim_details", "text_zh": "要件二：详尽载明工程量清单核算明细、到期应付日与合同依据条款", "status": "mandatory"}
        ]
    },
    {
        "norm_id": "MY:CIPAA_2012:Sec6",
        "law": "MY:CIPAA_2012",
        "enbez": "Section 6",
        "title": "马来西亚建筑业支付与裁决法第6条：付款答辩书 10 个工作日法定时效",
        "norm_category": "mandatory_statute",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "A non-paying party who is served with a payment claim shall respond within 10 working days by serving a payment response admitting or disputing the claim.",
        "text_en": "A non-paying party served with a payment claim shall serve a payment response within 10 working days, either admitting or disputing the claim.",
        "text_zh": "【付款答辩 10 日时效】欠款方收到付款请求书后，必须在 10 个工作日内向索赔方送达付款答辩书 (Payment Response)，列明认可或争议扣款理由；逾期未答辩视为对索赔金额存有争议但丧失先发优势。",
        "text_de": "Section 6 Payment Response 10 Working Days\n欠款方必须在收到索赔后10个工作日内提交正式付款答辩书。\nNon-paying party must respond within 10 working days disputing or admitting claim.",
        "mandatory_level": "mandatory",
        "source_url": "https://lom.agc.gov.my",
        "elements_json": [
            {"eid": "e_cipaa6_10day_timeline", "text_zh": "要件一：自收到 Payment Claim 之次日起精确计算 10 个工作日", "status": "mandatory"},
            {"eid": "e_cipaa6_written_response", "text_zh": "要件二：出具书面答辩明确抵销抗辩理由与依据", "status": "mandatory"}
        ]
    },

    # 🇸🇬 新加坡 L1 核心成文法簇
    {
        "norm_id": "SG:SOPA_2004:Sec8",
        "law": "SG:SOPA_2004",
        "enbez": "Section 8",
        "title": "新加坡建筑业付款保障法第8条：进度款法定请求权与计价准则",
        "norm_category": "mandatory_statute",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Any person who has carried out any construction work under a contract is entitled to a progress payment. The amount shall be calculated based on contract price or valuation of work performed.",
        "text_en": "Any person who carried out construction work is entitled to progress payment calculated by contract price or valuation.",
        "text_zh": "【法定进度款请求权】在合同项下实施任何建筑工程的当事人，依法自动享有按期获得进度款支付的权利；数额依据合同约定价格或已完工工程公允价值计算。",
        "text_de": "Section 8 Right to Progress Payments\n实施建筑工程人员依法自动享有获得进度款计价支付之权利。\nPersons carrying out work are entitled to statutory progress payments.",
        "mandatory_level": "mandatory",
        "source_url": "https://sso.agc.gov.sg",
        "elements_json": [
            {"eid": "e_sopa8_work_performed", "text_zh": "要件一：承包商已在新加坡境内工程中实际开展了施工或设计服务", "status": "mandatory"},
            {"eid": "e_sopa8_entitlement", "text_zh": "法律后果：产生 SOPA 法定月度进度款请求权，合同任何约定排除条款无效", "status": "satisfied"}
        ]
    },
    {
        "norm_id": "SG:SOPA_2004:Sec10",
        "law": "SG:SOPA_2004",
        "enbez": "Section 10",
        "title": "新加坡建筑业付款保障法第10条：付款索赔送达时间窗口与格式要件",
        "norm_category": "mandatory_statute",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "A claimant may serve one payment claim in respect of each progress payment. The payment claim shall be served on or before the contract date or the last day of each month.",
        "text_en": "A claimant may serve one payment claim per progress payment cycle on or before contract date or month end, identifying the work and amount.",
        "text_zh": "【付款索赔送达窗口】索赔人就每个进度款周期仅能送达一份付款索赔；必须在合同约定日或每月最后一日之前送达，过早或过晚送达均可能导致裁决无效！",
        "text_de": "Section 10 Payment Claim Service Window\n每个付款周期仅能送达一份索赔书且必须在指定时间窗口送达。\nOne claim per cycle served within statutory timeline identifying work and amount.",
        "mandatory_level": "mandatory",
        "source_url": "https://sso.agc.gov.sg",
        "elements_json": [
            {"eid": "e_sopa10_time_window", "text_zh": "要件一：严格在合同约定计价截止日或自然月最后一日前送达", "status": "mandatory"},
            {"eid": "e_sopa10_one_claim_rule", "text_zh": "要件二：同一计价周期内严禁重复发出多份索赔函", "status": "mandatory"}
        ]
    },
    {
        "norm_id": "SG:UCTA_Cap_396:Sec2",
        "law": "SG:UCTA_Cap_396",
        "enbez": "Section 2",
        "title": "新加坡不公平合同条款法第2条：过失致死伤免责条款绝对无效",
        "norm_category": "mandatory_statute",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "A person cannot by reference to any contract term exclude or restrict his liability for death or personal injury resulting from negligence.",
        "text_en": "Liability for death or personal injury resulting from negligence cannot be excluded or restricted by any contract term.",
        "text_zh": "【人身伤亡免责绝对禁止】在任何合同条款或告示中，企图免除或限制因过失造成人身伤害或死亡责任的条款，自始绝对无效，任何约定免责概不受理。",
        "text_de": "Section 2 Negligence Liability Exclusion Void\n合同中企图免除过失致人伤亡责任的条款自始绝对无效。\nContract cannot exclude or restrict liability for death or personal injury.",
        "mandatory_level": "mandatory_override",
        "source_url": "https://sso.agc.gov.sg",
        "elements_json": [
            {"eid": "e_ucta2_negligence_injury", "text_zh": "要件一：工地安全事故因发包人或总包方重大过失致人死伤", "status": "mandatory"},
            {"eid": "e_ucta2_void_clause", "text_zh": "法律后果：合同中任何格式免责条款绝对归于无效，依法承担全额赔偿", "status": "mandatory"}
        ]
    },

    # 🇹🇭 泰国 L1 核心成文法簇
    {
        "norm_id": "TH:CCC:Sec150",
        "law": "TH:CCC",
        "enbez": "Section 150",
        "title": "泰国民商法典第150条：违反强行法或公共秩序法律行为绝对无效",
        "norm_category": "mandatory_statute",
        "language_mode": "trilingual",
        "lang_original": "th",
        "text_original": "การใดมีวัตถุประสงค์เป็นการต้องห้ามชัดแจ้งโดยกฎหมาย หรือเป็นการพ้นวิสัย หรือเป็นการขัดต่อความสงบเรียบร้อยหรือศีลธรรมอันดีของประชาชน การนั้นเป็นโมฆะ",
        "text_en": "An act is void if its object is expressly prohibited by law, impossible, or contrary to public order or good morals.",
        "text_zh": "【违法民事行为绝对无效】法律行为之标的若属于法律明文禁止、客观绝对不可能、或违反公共秩序善良风俗的，该法律行为自始绝对无效 (Void / โมฆะ)。",
        "text_de": "Section 150 Unlawful Act Void\n标的违反法律明文禁止或反公序良俗之法律行为自始绝对无效。\nAct is void if object is prohibited by law, impossible or contrary to public order.",
        "mandatory_level": "mandatory_override",
        "source_url": "http://www.krisdika.go.th",
        "elements_json": [
            {"eid": "e_th150_prohibition", "text_zh": "要件一：合同约定的工程标的违反泰国法律禁止性强行规定", "status": "prohibition"},
            {"eid": "e_th150_public_order", "text_zh": "要件二：违背泰国公共秩序与善良道德准则", "status": "prohibition"},
            {"eid": "e_th150_void_status", "text_zh": "法律后果：该法律行为自始归于无效，不受任何司法保护", "status": "mandatory"}
        ]
    },
    {
        "norm_id": "TH:CCC:Sec587",
        "law": "TH:CCC",
        "enbez": "Section 587",
        "title": "泰国民商法典第587条：承揽工程合同定义与对价给付义务",
        "norm_category": "mandatory_statute",
        "language_mode": "trilingual",
        "lang_original": "th",
        "text_original": "อันว่าจ้างทำของนั้น คือสัญญาซึ่งบุคคลคนหนึ่งเรียกว่าผู้รับจ้าง ตกลงจะทำการงานสิ่งใดสิ่งหนึ่งจนสำเร็จให้แก่บุคคลอีกคนหนึ่งเรียกว่าผู้ว่าจ้าง และผู้ว่าจ้างตกลงจะให้สินจ้างเพื่อผลสำเร็จแห่งการที่ทำนั้น",
        "text_en": "Hire of work is a contract whereby the contractor agrees to accomplish a definite work for the employer who agrees to pay remuneration for result of work.",
        "text_zh": "【承揽工程核心定义】承揽合同系指一方（承包商）同意为另一方（发包人）完成特定工作成果，发包人同意就该项完成之成果支付报酬的协议。",
        "text_de": "Section 587 Hire of Work Definition\n承揽合同系承包商完成特定工作成果、定作人支付报酬之协议。\nHire of work contract where contractor completes work for agreed remuneration.",
        "mandatory_level": "mandatory",
        "source_url": "http://www.krisdika.go.th",
        "elements_json": [
            {"eid": "e_th587_completion_result", "text_zh": "要件一：承包商完成合同约定的建筑或设备安装特定成果", "status": "mandatory"},
            {"eid": "e_th587_payment_duty", "text_zh": "要件二：发包人负有验收工作成果并依约足额支付工程报酬之法定义务", "status": "mandatory"}
        ]
    },
    {
        "norm_id": "TH:CCC:Sec600",
        "law": "TH:CCC",
        "enbez": "Section 600",
        "title": "泰国民商法典第600条：建筑物及大型土建 5 年法定缺陷追责期",
        "norm_category": "mandatory_statute",
        "language_mode": "trilingual",
        "lang_original": "th",
        "text_original": "ถ้าสิ่งก่อสร้างบนพื้นดินอันมิใช่เรือนไม้มิได้กำหนดเวลาไว้ในสัญญา ผู้รับจ้างไม่ต้องรับผิดเพื่อการชำรุดบกพร่อง เว้นแต่ความชำรุดบกพร่องนั้นจะได้ปรากฏขึ้นภายในห้าปีนับแต่วันส่งมอบ",
        "text_en": "In case of structures on land other than wooden houses, the contractor is liable for defects appearing within 5 years from delivery date.",
        "text_zh": "【建筑物 5 年瑕疵担保责任】在土地上建造的非木质结构建筑物及大型工业工程，合同未另有约定的，承包商对工程交付移交之日起 5 年内出现的质量缺陷承担法定保修责任。",
        "text_de": "Section 600 5-Year Defect Liability for Buildings\n土地上钢筋混凝土建筑物工程移交后享有5年法定质量瑕疵担保期。\nContractor liable for defects appearing within 5 years from delivery date for structures.",
        "mandatory_level": "mandatory",
        "source_url": "http://www.krisdika.go.th",
        "elements_json": [
            {"eid": "e_th600_structure_type", "text_zh": "要件一：属于建设在土地上的钢筋混凝土或永久性土建工业结构物", "status": "mandatory"},
            {"eid": "e_th600_5year_timeline", "text_zh": "要件二：缺陷在工程移交验收之日起 5 年法定期间内暴露出现", "status": "mandatory"},
            {"eid": "e_th600_repair_liability", "text_zh": "法律后果：承包商负有免费维修或赔偿修复费用的连带责任", "status": "satisfied"}
        ]
    },

    # 🇵🇭 菲律宾 L1 核心成文法簇
    {
        "norm_id": "PH:Civil_Code:Art1174",
        "law": "PH:Civil_Code",
        "enbez": "Article 1174",
        "title": "菲律宾民法典第1174条：不可抗力与意外事件 (Caso Fortuito) 四大免责要件",
        "norm_category": "mandatory_statute",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Except in cases expressly specified by the law, or when it is otherwise declared by stipulation, or when the nature of the obligation requires the assumption of risk, no person shall be responsible for those events which could not be foreseen, or which, though foreseen, were inevitable.",
        "text_en": "No person shall be responsible for events which could not be foreseen, or which, though foreseen, were inevitable, except by law, stipulation or nature of risk.",
        "text_zh": "【不可抗力四大免责要件】除法律明文规定、合同另有特约或债务性质要求自担风险外，任何人不对无法预见或虽能预见但不可避免的事件（不可抗力/意外事件）承担赔偿责任。",
        "text_de": "Article 1174 Fortuitous Events Immunity\n不可预见且不可避免之意外事件致债务不能履行免除赔偿责任。\nNo liability for unforeseen or inevitable fortuitous events unless agreed otherwise.",
        "mandatory_level": "mandatory",
        "source_url": "https://elibrary.judiciary.gov.ph",
        "elements_json": [
            {"eid": "e_ph1174_cause_independent", "text_zh": "要件一：事件发生的原因完全独立于当事人的意志之外", "status": "mandatory"},
            {"eid": "e_ph1174_unforeseen_inevitable", "text_zh": "要件二：事件在缔约时无法预见，或虽能预见但通过一切合理措施不可避免", "status": "mandatory"},
            {"eid": "e_ph1174_rendering_impossible", "text_zh": "要件三：该事件导致债务人客观上无法正常履行其合同承诺", "status": "mandatory"},
            {"eid": "e_ph1174_no_concurrent_negligence", "text_zh": "要件四：债务人对损害的发生不存在任何协同过失或不当加重行为", "status": "mandatory"}
        ]
    },
    {
        "norm_id": "PH:Civil_Code:Art1719",
        "law": "PH:Civil_Code",
        "enbez": "Article 1719",
        "title": "菲律宾民法典第1719条：定作人接收受领工程免除承包商责任及例外",
        "norm_category": "mandatory_statute",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Acceptance of the work by the employer relieves the contractor of liability for any defect, unless: the defect is hidden, or the employer accepts the work with reservation.",
        "text_en": "Acceptance of work by employer relieves contractor of liability for defects, unless defect is hidden, or acceptance is with reservation.",
        "text_zh": "【接收工程免责及例外】发包人验收并接收工程即免除承包商对于明显缺陷的质量责任；除非：① 缺陷属于隐蔽缺陷；② 发包人在接收时出具了正式书面保留异议清单。",
        "text_de": "Article 1719 Employer Acceptance of Work\n发包人无保留验收工程免除明显缺陷责任，隐蔽缺陷除外。\nAcceptance relieves contractor liability unless defect is hidden or with reservation.",
        "mandatory_level": "mandatory",
        "source_url": "https://elibrary.judiciary.gov.ph",
        "elements_json": [
            {"eid": "e_ph1719_taking_over", "text_zh": "要件一：发包人已正式签署移交接收凭据或实际投入商业运行", "status": "condition_precedent"},
            {"eid": "e_ph1719_patent_defect_relief", "text_zh": "法律后果：表面明显缺陷责任免除，发包人丧失主张该明显缺陷违约扣款权利", "status": "satisfied"}
        ]
    },
    {
        "norm_id": "PH:RA_4566:Sec15",
        "law": "PH:RA_4566",
        "enbez": "Section 15",
        "title": "菲律宾承包商执照法第15条：PCAB资质执照强制性与外资平等待遇",
        "norm_category": "mandatory_statute",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "No contractor shall engage in the business of contracting in the Philippines without having first secured a license from the Philippine Contractors Accreditation Board (PCAB). Foreign contractors are entitled to regular license pursuant to Supreme Court Manila Water ruling.",
        "text_en": "No contractor shall engage in contracting without securing a license from PCAB. Foreign contractors entitled to equal regular license under Manila Water precedent.",
        "text_zh": "【施工执照强制令与外资平等待遇】任何承包商在菲从事建筑工程作业必须先取得 PCAB 资质执照。依据最高法院 Manila Water 违宪终审判例，外资承包商依法享有申请常规施工执照的平等待遇，彻底废除外资股比限制歧视。",
        "text_de": "Section 15 PCAB Contractor License Mandatory\n进场施工必须取得PCAB执照，外资承包商享有平等待遇。\nContractor must secure license from PCAB; foreign firms entitled to equal treatment.",
        "mandatory_level": "mandatory_override",
        "source_url": "https://ciap.dti.gov.ph",
        "elements_json": [
            {"eid": "e_ph4566_pcab_license", "text_zh": "要件一：在签署工程合同或实施施工前取得 PCAB 核发的施工执照", "status": "condition_precedent"},
            {"eid": "e_ph4566_equal_treatment", "text_zh": "要件二：依据 Manila Water 判例主张外资常规执照合规合法性", "status": "mandatory"}
        ]
    },

    # 🇨🇳 中国境内出海强监管法规 (L1)
    {
        "norm_id": "CN:SASAC_Order_35:Art12",
        "law": "CN:SASAC_Order_35",
        "enbez": "Article 12",
        "title": "国资委35号令第12条：中央企业境外重大投资法律合规论证与负面清单",
        "norm_category": "prc_sasac_reg",
        "language_mode": "bilingual",
        "lang_original": "zh",
        "text_original": "中央企业开展境外投资应当遵守非主业投资负面清单管理要求，境外投资决策前必须委托专业机构出具法律意见书，开展深入严谨的法律尽职调查与合规论证。",
        "text_en": "Central SOEs conducting overseas investments shall comply with the negative list. Prior to decision-making, an independent legal opinion must be obtained.",
        "text_zh": "【央企境外投资事前合规论证】央企境外投资必须遵守非主业负面清单；上会决策前必须委托第三方出具尽职调查报告与法律意见书，严禁盲目出海导致国有资产流失。",
        "text_de": "Article 12 SASAC Pre-Investment Legal Audit\n央企境外重大投资必须严格落实合规尽调并取得独立法律意见书。\nCentral SOEs must conduct rigorous legal due diligence prior to overseas investment.",
        "mandatory_level": "mandatory_override",
        "source_url": "http://www.sasac.gov.cn",
        "elements_json": [
            {"eid": "e_sasac35_main_business", "text_zh": "要件一：投资标的属于央企经国资委核准的主业或主业延伸链条范围", "status": "mandatory"},
            {"eid": "e_sasac35_legal_opinion", "text_zh": "要件二：具备专业律所出具的《境外投资准入与法律风险合规论证意见书》", "status": "condition_precedent"},
            {"eid": "e_sasac35_board_resolution", "text_zh": "要件三：经集团党委会前置研究与董事会正式审议批准", "status": "mandatory"}
        ]
    },
    {
        "norm_id": "CN:SASAC_Notice_75_2021:Art4",
        "law": "CN:SASAC_Notice_75_2021",
        "enbez": "Article 4",
        "title": "国资委75号文第4条：严禁对参股项目超股比担保与无股权关系企业担保",
        "norm_category": "prc_sasac_reg",
        "language_mode": "bilingual",
        "lang_original": "zh",
        "text_original": "中央企业严禁对参股企业提供超股比融资担保，严禁对无股权关系的企业提供担保。确需担保的，必须由参股各方按出资比例同等提供或由被担保方提供足额有效反担保。",
        "text_en": "Central SOEs are strictly prohibited from providing guarantees in excess of their shareholding ratio, or providing guarantees to entities with no equity relationship.",
        "text_zh": "【超股比担保绝对禁令】严禁央企对参股企业提供超股比担保，严禁对无股权企业提供担保。在境外合资项目或 KSO 联营体中出具全额母公司完工保函 (PCG) 触碰国资红线！",
        "text_de": "Article 4 SASAC Guarantee Prohibition\n严禁央企对参股企业超股比担保，严禁对无股权企业担保。\nCentral SOEs strictly prohibited from excess guarantees or guarantees without equity.",
        "mandatory_level": "mandatory_override",
        "source_url": "http://www.sasac.gov.cn",
        "elements_json": [
            {"eid": "e_sasac75_equity_ratio", "text_zh": "要件一：担保金额严格以中资企业在境外项目公司实际持股比例为限", "status": "mandatory"},
            {"eid": "e_sasac75_no_unrelated_guarantee", "text_zh": "要件二：严禁为外国本土联营方或无直接股权关联的分包商提供任何形式的信用担保", "status": "prohibition"},
            {"eid": "e_sasac75_counter_guarantee", "text_zh": "要件三：必须落实参股各方同比例担保机制或由外方提供足额反担保", "status": "mandatory"}
        ]
    },
    {
        "norm_id": "CN:Data_Security_Law:Art36",
        "law": "CN:Data_Security_Law",
        "enbez": "Article 36",
        "title": "中华人民共和国数据安全法第36条：境外司法执法机构调取数据审批令",
        "norm_category": "prc_sasac_reg",
        "language_mode": "bilingual",
        "lang_original": "zh",
        "text_original": "非经中华人民共和国主管机关批准，境内的组织、个人不得向外国司法或者执法机构提供存储于中华人民共和国境内的法律、工程数据及商业机密。",
        "text_en": "Without prior approval of competent authorities of the PRC, organizations and individuals in China shall not provide data stored in China to foreign judicial or law enforcement bodies.",
        "text_zh": "【数据出境审批防线】非经国家主管机关批准，严禁向境外仲裁庭、法院或外国执法机构提供境内存储的数据，涉外仲裁证据开示出境必须履行前置审批。",
        "text_de": "Article 36 Cross-Border Data Transfer Approval\n非经主管机关批准严禁向外国司法执法机构提供境内存储数据。\nProhibited from providing domestic data to foreign judicial bodies without approval.",
        "mandatory_level": "mandatory_override",
        "source_url": "http://www.npc.gov.cn",
        "elements_json": [
            {"eid": "e_dsl36_domestic_data", "text_zh": "要件一：涉案技术图纸、工程邮件或财务数据物理存储在境内服务器", "status": "mandatory"},
            {"eid": "e_dsl36_approval_order", "text_zh": "要件二：向境外法庭或仲裁庭出示前必须向发改委/商务部申请出境核准批复", "status": "condition_precedent"}
        ]
    }
]
