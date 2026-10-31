"""
data_phase10_deep_statutes.py - 《数据库审查.md》最新版终极法条扩充数据模块
涵盖：
1. 65 条 L1 核心强行法条（越南、印尼、马来西亚、新加坡、泰国、菲律宾、中国出海监管）
2. 52 条 L2 参考规程与多边条约（FIDIC 2017、URDG 758、DTA、特别行业规程、外汇与造价公式）
合计 117 条高权威涉外成文法条，100% 结构化填充 2~4 个 elements_json 槽位。
"""
import json

PHASE10_L1_NORMS = [
    # ==========================================
    # 1. 越南 (asean_vn) - 10 条 L1 强行法
    # ==========================================
    {
        "table": "norms",
        "norm_id": "VN:Civil_Code_2015:Art420",
        "law": "VN:Civil_Code_2015",
        "enbez": "Art 420",
        "title": "越南2015年民法典第420条：情势变更原则与司法介入调价终止合同",
        "heading_path": "越南2015年民法典 (Law 91/2015/QH13) > 第三编 债与合同 > 第420条 情势发生实质改变时的合同履行",
        "language_mode": "bilingual",
        "lang_original": "vi",
        "text_original": "Thực hiện hợp đồng khi hoàn cảnh thay đổi cơ bản: Khi hoàn cảnh thay đổi cơ bản do các nguyên nhân khách quan xảy ra sau khi giao kết hợp đồng mà các bên không thể lường trước được, bên có lợi ích bị ảnh hưởng có quyền yêu cầu đàm phán lại. Trường hợp không thể thỏa thuận, một trong các bên có quyền yêu cầu Tòa án chấm dứt hợp đồng hoặc sửa đổi hợp đồng.",
        "text_en": "Performance of contract upon fundamental change of circumstances: If circumstances change fundamentally due to objective events unforeseeable at contract execution, parties may renegotiate; failing agreement, court may modify or terminate contract.",
        "text_zh": "【情势变更原则突破固定总价】：履约过程中因客观情势发生不可预见的重大改变（Hardship），若继续履行原合同将导致一方遭受严重损害，受损方有权要求重新谈判；双方协商不成的，任何一方有权请求法院裁决调整合同价格或解除合同。【出海攻防启示】：中资承包商遭遇钢材水泥等大宗建材价格暴涨时，若原合同为闭口固定总价（Fixed Lump Sum）且无调价公式，Art 420 是在越南法院与 VIAC 仲裁中突破固定总价、请求司法调增工程款的唯一法定抗辩通道！",
        "norm_category": "breach_remedy",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_vn420_unforeseeable_event", "text_zh": "要件一：情势发生实质性改变系因合同订立后发生的客观原因所致且当事人缔约时无法合理预见", "status": "condition_precedent"},
            {"eid": "e_vn420_severe_disadvantage", "text_zh": "要件二：若继续按原约定履行将导致一方当事人的合法利益遭受极其严重的实质损害", "status": "mandatory"},
            {"eid": "e_vn420_judicial_adjustment", "text_zh": "法律后果：双方重新谈判未果时，法院有权裁决依公平原则调整合同价款或终止合同履行", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "VN:Law_31_2024:Art127_128",
        "law": "VN:Law_31_2024",
        "enbez": "Art 127-128",
        "title": "越南2024年新土地法第127-128条：工业用地出租出让与向持牌金融机构抵押限制",
        "heading_path": "越南2024年新土地法 (Law 31/2024/QH15) > 土地使用权权能 > 工业用地转让与抵押",
        "language_mode": "bilingual",
        "lang_original": "vi",
        "text_original": "Tổ chức kinh tế có vốn đầu tư nước ngoài thuê đất trả tiền một lần cho cả thời gian thuê có quyền thế chấp quyền sử dụng đất và tài sản gắn liền với đất tại các tổ chức tín dụng được phép hoạt động tại Việt Nam. Trường hợp thuê đất trả tiền hàng năm chỉ có quyền thế chấp tài sản thuộc sở hữu của mình gắn liền với đất.",
        "text_en": "Foreign-invested enterprises leasing land with lump-sum rental payment may mortgage land use rights and assets to credit institutions licensed in Vietnam; annual rental leases permit mortgage of attached assets only.",
        "text_zh": "【工业用地土地使用权抵押法定限制】：外资企业通过一次性缴纳全部土地租金方式取得的工业用地土地使用权（LUR），方可依法转让或向在越南注册持牌的金融机构设定抵押；若按年缴纳租金，则严禁抵押土地使用权本身，仅能抵押其自有的地上建筑物及设备！【出海攻防启示】：中资央企出海投建电站或厂区项目，若拟向中资银行境内分行组建的银团申请项目融资质押，必须在拿地时明确选择‘一次性缴费’模式并经属地持牌外资银行开具代理行抵押，严防‘按年交租土地抵押自始无效’引发银行提前抽贷暴雷！",
        "norm_category": "property_security",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_vn_lur_lumpsum_rental", "text_zh": "要件一：外资项目公司已依法全额一次性付清整个租赁周期的土地使用权租金", "status": "condition_precedent"},
            {"eid": "e_vn_lur_licensed_creditor", "text_zh": "要件二：抵押权人必须属于在越南境内合法设立并取得营业执照的信贷金融机构", "status": "mandatory"},
            {"eid": "e_vn_lur_mortgage_validity", "text_zh": "法律后果：土地登记主管机关依法办理抵押登记，确立抵押优先受偿权并阻断按年租赁抵押无效抗辩", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "VN:Law_61_2020:Art24_26",
        "law": "VN:Law_61_2020",
        "enbez": "Art 24-26",
        "title": "越南2020年投资法第24-26条：外资并购审批前置与股权名义代持绝对无效",
        "heading_path": "越南2020年投资法 (Law 61/2020/QH14) > 第二章 投资形式 > 外商投资并购核准",
        "language_mode": "bilingual",
        "lang_original": "vi",
        "text_original": "Nhà đầu tư nước ngoài góp vốn, mua cổ phần, mua phần vốn góp phải đáp ứng điều kiện và thực hiện thủ tục đăng ký góp vốn, mua cổ phần tại cơ quan đăng ký đầu tư nếu dẫn đến nắm giữ trên 50% vốn điều lệ hoặc thuộc ngành nghề tiếp cận thị trường có điều kiện. Mọi thỏa thuận nhờ người khác đứng tên hộ (Nominee) nhằm trốn tránh quy định này đều vô hiệu theo quy định pháp luật.",
        "text_en": "Foreign investors acquiring shares exceeding 50% charter capital or in conditional sectors must obtain prior M&A approval from investment registration authority; nominee shareholding agreements bypassing review are null and void.",
        "text_zh": "【外资并购审批与穿透打击名义代持】：外商通过出资或股权受让方式控股超过 50% 或进入限制性准入行业，必须取得越南计划投资厅（DPI）的前置并购批准（M&A Approval）；严禁通过找越南籍自然人或空壳法人代持股权规避外资审查，代持协议在越南法院一律被判定违反公序良俗自始绝对无效！【出海攻防启示】：中资企业在越南通过暗箱代持收购新能源光伏/风电项目公司股权，一旦合伙方反水，越南法院 100% 裁决代持无效，中资投入的数千万美元前期开发款面临全额打水漂！必须走法定合规 M&A Approval 前置审批途径！",
        "norm_category": "foreign_investment",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_vn_inv_threshold_50", "text_zh": "要件一：并购交易导致外资实际持股比例超过 50% 或目标企业涉及海岛、边境敏感土地与外资准入负面清单", "status": "condition_precedent"},
            {"eid": "e_vn_inv_dpi_approval", "text_zh": "要件二：正式向省级计划投资厅递交并购申请并取得书面原则同意通知书（M&A Approval）", "status": "mandatory"},
            {"eid": "e_vn_inv_nominee_nullity", "text_zh": "法律后果：合法取得股东地位；未获审批或采用代持架构者，股权协议自始无效且出资面临行政没收", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "VN:Civil_Procedure_Code_2015:Art111_114",
        "law": "VN:Civil_Procedure_Code_2015",
        "enbez": "Art 111-114",
        "title": "越南2015年民事诉讼法第111-114条：诉前保函止付紧急措施与100%反担保高门槛",
        "heading_path": "越南2015年民事诉讼法典 (Law 92/2015/QH13) > 第八章 紧急临时措施 > 保函止付与反担保",
        "language_mode": "bilingual",
        "lang_original": "vi",
        "text_original": "Tòa án chỉ quyết định áp dụng biện pháp khẩn cấp tạm thời cấm hoặc buộc thực hiện hành vi nhất định (kể cả phong tỏa việc thực hiện nghĩa vụ bảo lãnh ngân hàng) khi người yêu cầu nộp văn bản bảo đảm bằng tài sản hoặc phong tỏa tài khoản ngân hàng tương đương 100% nghĩa vụ tài chính cần bảo đảm.",
        "text_en": "Courts grant interim relief restraining bank guarantee payments only if applicant posts counter-security equal to 100% of the guaranteed amount and proves imminent irreparable harm.",
        "text_zh": "【独立保函止付裁定与100%足额反担保要件】：申请越南法院裁定银行中止支付见索即付保函，申请人必须向法院指定账户缴存相当于保函索兑金额 100% 的现金或等额财产作为反担保，且必须举证证明存在不可弥补的紧迫损害。【出海攻防启示】：越南法院极度偏向开证行与受益人，因商业合同争议申请保函止付几乎不可能获批，且 100% 反担保极大占用现金流！中资总包遭遇越南业主恶意索兑时，切忌寄希望于越南属地法院临时禁令，必须依据主合同仲裁条款迅速向境外仲裁地（如新加坡 SIAC）申请紧急仲裁员（EA）禁令以实施跨国阻截！",
        "norm_category": "crossborder_litigation",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_vn_inj_irreparable_harm", "text_zh": "要件一：举证证明受益人索兑行为存在明显重大欺诈或将给申请人造成不可弥补之严重损害", "status": "condition_precedent"},
            {"eid": "e_vn_inj_100pct_countersecurity", "text_zh": "要件二：向法院提存等同于保函索赔全额的 100% 保证金或提供合规不动产质押反担保", "status": "mandatory"},
            {"eid": "e_vn_inj_stay_order", "text_zh": "法律后果：法院签发诉前行为保全裁定，指令开证银行暂停向受益人打款划付资金", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "VN:Decree_70_2023:Art1_2",
        "law": "VN:Decree_70_2023",
        "enbez": "Art 1-2",
        "title": "越南第70/2023号法令第1-2条：外籍劳工工作许可强制提前15日公开招聘前置",
        "heading_path": "越南政府第70/2023/ND-CP号法令 > 外籍劳工在越工作管理 > 用工公示与工作许可核发",
        "language_mode": "bilingual",
        "lang_original": "vi",
        "text_original": "Kể từ ngày 01 tháng 01 năm 2024, việc tuyển dụng người lao động Việt Nam vào các vị trí dự kiến tuyển dụng người lao động nước ngoài phải được thực hiện thông qua Cổng thông tin điện tử của Cục Việc làm hoặc Trung tâm dịch vụ việc làm ít nhất 15 ngày trước ngày dự kiến báo cáo giải trình nhu cầu sử dụng lao động nước ngoài.",
        "text_en": "Employers recruiting foreign workers must announce vacancies on Employment Department portal at least 15 days prior to submitting foreign labor demand explanation, proving no qualified Vietnamese available.",
        "text_zh": "【外工招聘强制15天本土公示前置程序】：用人单位计划聘用中国技术专家或工程管理人员前，必须提前至少 15 天在越南劳工荣军社会部官方网站或就业中心公开发布招聘信息；只有在证明本土无合格候选人后，主管机关方可审批外籍用工需求报告并核发工作许可（Work Permit）。【出海攻防启示】：彻底封死‘人已到现场再补办证’的灰色空间！严禁中资人员持商务签证（DN签）或旅游签证在项目现场从事设备安装调试作业，一旦遭遇公安部与劳工部联合突击检查，企业将面临高额罚款，技术人员将被直接驱逐出境并列入黑名单！",
        "norm_category": "labor_compliance",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_vn_wp_15days_notice", "text_zh": "要件一：在外籍用工申报前整 15 个日历天在指定公共就业门户网站完成本土招聘公示", "status": "condition_precedent"},
            {"eid": "e_vn_wp_labor_department_approval", "text_zh": "要件二：取得省级劳工荣军社会厅出具的书面外籍用工需求配额批准函件", "status": "mandatory"},
            {"eid": "e_vn_wp_legal_consequence", "text_zh": "法律后果：核发合法作业许可证（Work Permit）；违规无证务工者强制驱逐出境并处企业巨额罚金", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "VN:Civil_Code_2015:Art129",
        "law": "VN:Civil_Code_2015",
        "enbez": "Art 129",
        "title": "越南2015年民法典第129条：形式瑕疵但履行达三分之二以上合同有效治愈规则",
        "heading_path": "越南2015年民法典 (Law 91/2015/QH13) > 民事法律行为 > 第129条 违反形式规定的民事行为之有效性",
        "language_mode": "bilingual",
        "lang_original": "vi",
        "text_original": "Giao dịch dân sự vi phạm quy định điều kiện có hiệu lực về hình thức thì vô hiệu, trừ trường hợp giao dịch đã được thực hiện ít nhất hai phần ba nghĩa vụ thì theo yêu cầu của một bên hoặc các bên, Tòa án ra quyết định công nhận hiệu lực của giao dịch đó.",
        "text_en": "Transactions breaching formal requirements are void, except where at least two-thirds of obligations have been performed, upon application of parties, court shall recognize validity.",
        "text_zh": "【履行达2/3治愈合同形式瑕疵原则】：民事法律行为违反法律规定的公证、书面等形式要件的原则上无效；但若一方或双方当事人已实际履行了合同项下至少三分之二（2/3）以上的实体义务，法院根据当事人请求，依法裁定确认该合同合法有效！【出海攻防启示】：工程结算防赖账核心盾牌！中资分包商签署协议时因未办理法定公证或未由法定代表人亲签存在形式缺陷，若工程已实质完工 70% 以上，业主企图以‘合同形式不合规自始无效’赖账拒付进度款的，中资企业直接依本条请求越南法院强行确认合同有效并支持全额付款！",
        "norm_category": "contract_formation",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_vn129_formal_defect", "text_zh": "要件一：合同存在未办理法定公证、认证或签字盖章手续不全之形式瑕疵", "status": "condition_precedent"},
            {"eid": "e_vn129_two_thirds_performance", "text_zh": "要件二：主张有效方已实际组织施工并完成了合同总标的额三分之二（2/3）以上之主体工程量", "status": "mandatory"},
            {"eid": "e_vn129_cure_validity", "text_zh": "法律后果：法院依裁量权直接确认该合同具备完全合法效力，全面排除相对方形式无效抗辩", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "VN:Civil_Code_2015:Art405_406",
        "law": "VN:Civil_Code_2015",
        "enbez": "Art 405-406",
        "title": "越南2015年民法典第405-406条：格式条款不利解释与不合理免除责任条款法定无效",
        "heading_path": "越南2015年民法典 (Law 91/2015/QH13) > 合同订立 > 格式合同与免责条款效力",
        "language_mode": "bilingual",
        "lang_original": "vi",
        "text_original": "Hợp đồng theo mẫu và điều kiện giao dịch chung: Trường hợp hợp đồng theo mẫu có điều khoản không rõ ràng thì bên đưa ra hợp đồng theo mẫu phải chịu bất lợi khi giải thích điều khoản đó. Điều khoản miễn trừ trách nhiệm của bên đưa ra hợp đồng theo mẫu, tăng trách nhiệm hoặc loại trừ quyền lợi chính đáng của bên kia là vô hiệu.",
        "text_en": "Standard form contracts: Ambiguous terms are interpreted against the drafting party; clauses exempting drafting party's liabilities or unfairly increasing the other party's burdens are void.",
        "text_zh": "【格式霸王条款无效与不利于提供方解释规则】：若格式合同（如业主提供的标准招标文件）中的条款存在歧义，司法机关必须作出不利于起草方（Contra Proferentem）的解释；格式条款中凡是旨在免除起草方重大过错责任、单方增加相对方沉重负担或排除相对方法定正当救济权利的，该条款自始绝对无效！【出海攻防启示】：击碎海外业主霸王条款！越南总包合同常约定‘发包人任何过错均不承担误期窝工赔偿’等单边条款，中资企业在诉讼仲裁中援引 Art 406 直接主张该免责条款显失公平自始无效，索回全额停工损失！",
        "norm_category": "contract_interpretation",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_vn405_standard_form", "text_zh": "要件一：争议条款属于一方当事人预先拟定且未与相对方进行对等协商的标准格式条款", "status": "condition_precedent"},
            {"eid": "e_vn405_unfair_exemption", "text_zh": "要件二：条款实质性免除起草方自身法定过错违约责任或不合理剥夺相对方工期索赔法定权利", "status": "mandatory"},
            {"eid": "e_vn405_clause_nullity", "text_zh": "法律后果：该霸王免责条款依法归于消灭无效，按民法典一般过错赔偿原则确定发包人赔偿责任", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "VN:Civil_Code_2015:Art411",
        "law": "VN:Civil_Code_2015",
        "enbez": "Art 411",
        "title": "越南2015年民法典第411条：双务合同同时履行抗辩权与发包人拖欠工程款承包商停工权",
        "heading_path": "越南2015年民法典 (Law 91/2015/QH13) > 合同履行 > 同时履行抗辩权",
        "language_mode": "bilingual",
        "lang_original": "vi",
        "text_original": "Quyền hoãn thực hiện nghĩa vụ trong hợp đồng song vụ: Bên phải thực hiện nghĩa vụ trước có quyền hoãn thực hiện nghĩa vụ của mình, nếu khả năng thực hiện nghĩa vụ của bên kia đã bị suy giảm nghiêm trọng đến mức không thể thực hiện được nghĩa vụ như đã cam kết cho đến khi bên kia có khả năng thực hiện nghĩa vụ hoặc có biện pháp bảo đảm.",
        "text_en": "Right to withhold performance in bilateral contracts: The party obliged to perform first may suspend its performance if the other party's performance ability is seriously impaired, until performance or security is provided.",
        "text_zh": "【同时履行抗辩权与合法暂停施工抗辩】：在双务合同中，负有先履行义务的一方，在有确切证据证明相对方履行能力严重恶化（如持续拖欠期中进度款、资金链断裂）时，享有依法暂停履行自身施工义务之合法抗辩权（Defense of Refusal to Perform），直至相对方恢复履约能力或提供有效履约担保！【出海攻防启示】：中资承包商海外合法停工的母法护身符！一旦越南业主拖延签发付款凭证超 45 天，中资项目部依据 Art 411 发出正式暂停施工函，阻断业主反诉‘承包商擅自停工构成延误违约’扣罚误期违约金的企图！",
        "norm_category": "breach_remedy",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_vn411_bilateral_contract", "text_zh": "要件一：双方受合法有效之建设工程总承包或分包双务合同约束", "status": "condition_precedent"},
            {"eid": "e_vn411_material_default", "text_zh": "要件二：相对方发生逾期未支付进度款、未提供现场进入权或严重财务恶化之客观违约事实", "status": "mandatory"},
            {"eid": "e_vn411_lawful_suspension", "text_zh": "法律后果：承包商合法行使停工抗辩权，工期相应自动顺延且免于承担一切误期损害赔偿责任", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "VN:Commercial_Law_2005:Art300_301",
        "law": "VN:Commercial_Law_2005",
        "enbez": "Art 300-301",
        "title": "越南2005年商业法第300-301条：商事违约金8%法定上限与约定除斥期",
        "heading_path": "越南2005年商业法 (Law 36/2005/QH11) > 第七章 商事违约救济 > 违约金条款与法定上限",
        "language_mode": "bilingual",
        "lang_original": "vi",
        "text_original": "Phạt vi phạm: Phạt vi phạm là việc bên bị vi phạm yêu cầu bên vi phạm trả một khoản tiền phạt do vi phạm hợp đồng nếu trong hợp đồng có thỏa thuận. Mức phạt đối với vi phạm nghĩa vụ hợp đồng hoặc tổng mức phạt đối với nhiều vi phạm do các bên thỏa thuận trong hợp đồng, nhưng không quá 8% giá trị phần nghĩa vụ hợp đồng bị vi phạm.",
        "text_en": "Penalty for breach: Parties may agree on penalties for breach of contract, provided that the penalty rate shall not exceed 8% of the value of the breached contractual obligation portion.",
        "text_zh": "【商事违约金8%强制封顶红线】：商事合同当事人可约定违约金条款，但违约金总额依法严格不得超过‘发生违约行为对应义务部分合同价值的 8%’！超过 8% 的约定部分在越南法律下自始无效，裁判机关强制依职权削减至 8%！【出海攻防启示】：中资总包遭遇巨额迟延索赔时的防守杀手锏！部分境外业主在合同中约定高达合同总价 15%~20% 的误期违约金（Delay Damages），只要主合同准据法选定为越南商事法，承包商可直接援引 Art 301 强制要求仲裁庭将违约金总额一刀切压减至 8%，瞬间为项目保住数百万美元利润！",
        "norm_category": "breach_remedy",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_vn301_commercial_nature", "text_zh": "要件一：争议各方均具备商事主体资格且合同属于越南商业法管辖的商事工程承包合同", "status": "condition_precedent"},
            {"eid": "e_vn301_contractual_stipulation", "text_zh": "要件二：合同中双方明确约定了针对特定违约事项的预定违约金（Penalty）计取条款", "status": "mandatory"},
            {"eid": "e_vn301_cap_8_percent", "text_zh": "法律后果：强制适用 8% 法定最高上限，超出部分依法被认定无效并强行阻断超额扣减", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "VN:SBV_Circular_12_2022:Art11_15",
        "law": "VN:SBV_Circular_12_2022",
        "enbez": "Art 11-15",
        "title": "越南国家银行第12/2022号通函第11-15条：外债签约30日央行登记与本息出境强制合规",
        "heading_path": "越南国家银行第12/2022/TT-NHNN号通函 > 外债管理 > 中长期外债登记与外汇汇出审查",
        "language_mode": "bilingual",
        "lang_original": "vi",
        "text_original": "Đăng ký khoản vay nước ngoài: Bên đi vay phải thực hiện đăng ký khoản vay trung, dài hạn với Ngân hàng Nhà nước trong thời hạn 30 ngày làm việc kể từ ngày ký thỏa thuận vay hoặc thỏa thuận rút vốn. Mọi giao dịch chuyển tiền trả nợ gốc, lãi ra nước ngoài của khoản vay chưa đăng ký đều bị tổ chức tín dụng từ chối thực hiện.",
        "text_en": "Registration of foreign loans: Borrowers must register medium and long-term foreign loans with the State Bank of Vietnam within 30 working days of signing; banks strictly refuse remitting principal and interest abroad for unregistered loans.",
        "text_zh": "【中长期外债30日强制登记与资金出境红线】：越南外资企业（项目公司）借入期限超过 1 年的中长期外债（含中国母公司股东借款 Shareholder Loan），必须在借贷协议签订后 30 个工作日内向越南国家银行（SBV）办理正式外债登记；未经登记的外债，越南商业银行一律严禁办理还本付息跨境付汇，且借贷协议在司法审查中面临无效风险！【出海攻防启示】：出海工程垫资借款核心合规命脉！中资央企通过母公司向越南 SPV 提供股东借贷用于工程前期垫资，必须督导属地财会团队严格卡死 30 天登记时限，否则项目投产后巨额利息与本金将永久‘锁死在越南境内’无法合规分红汇回！",
        "norm_category": "foreign_exchange",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_vn_sbv12_loan_contract", "text_zh": "要件一：中国境内母公司或金融机构与越南项目实体签署期限超过 1 年的外汇借款协议", "status": "condition_precedent"},
            {"eid": "e_vn_sbv12_30days_registration", "text_zh": "要件二：自借款合同签署当日起严格 30 个工作日内向越南国家银行呈递完备外债登记卷宗", "status": "mandatory"},
            {"eid": "e_vn_sbv12_remittance_permission", "text_zh": "法律后果：取得合规外债确认书并享有合法向境外购汇汇出贷款本金与利息之权利；未登记者全额阻断出境", "status": "prohibition"}
        ], ensure_ascii=False)
    },

    # ==========================================
    # 2. 印度尼西亚 (asean_id) - 10 条 L1 强行法
    # ==========================================
    {
        "table": "norms",
        "norm_id": "ID:KUHPerdata:Art1831_1832",
        "law": "ID:KUHPerdata",
        "enbez": "Art 1831-1832",
        "title": "印尼民法典第1831-1832条：母公司担保先诉抗辩权与特别明示放弃要件",
        "heading_path": "印尼民法典 (KUHPerdata) > 第十九编 保证 > 先诉抗辩权及其例外",
        "language_mode": "bilingual",
        "lang_original": "id",
        "text_original": "Penanggung tidak diwajibkan membayar kepada kreditur kecuali debitur lalai, dalam hal mana barang-barang kepunyaan debitur harus lebih dahulu disita dan dijual untuk melunasi utangnya (Beneficium Excussionis). Penanggung tidak dapat menuntut penyitaan dan penjualan terlebih dahulu jika ia telah melepaskan hak istimewanya itu secara tegas.",
        "text_en": "Guarantor is not bound to pay creditor unless debtor defaults, in which case debtor's assets must first be seized and sold; guarantor cannot claim this benefit if explicitly waived.",
        "text_zh": "【保证人先诉抗辩权与母公司履约保函免责】：一般保证人享有先诉抗辩权（Beneficium Excussionis），债权人在未对主债务人（印尼子公司）财产提起强制执行且执行无果之前，无权直接要求保证人代偿；除非保证人在担保文件中以明示文字特别声明放弃该项法定权利！【出海攻防启示】：央企母公司出海防穿透护盾！境外业主或银团常要求中国母公司出具母公司履约担保（PCG），法务起草时应坚决保留民法典第 1831 条先诉抗辩权，删除‘放弃抗辩权’词句，迫使业主先在印尼起诉项目公司并执行完毕，筑牢母公司隔离防火墙！",
        "norm_category": "property_security",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_id1831_valid_guarantee", "text_zh": "要件一：母公司作为第三方就印尼项目公司的主债务出具了保证担保函件", "status": "condition_precedent"},
            {"eid": "e_id1831_no_explicit_waiver", "text_zh": "要件二：保证合同正文中未包含明确无误的‘声明放弃先诉抗辩权（Waiver of Beneficium Excussionis）’条款", "status": "mandatory"},
            {"eid": "e_id1831_excussionis_defense", "text_zh": "法律后果：保证人享有法定抗辩权，拒绝债权人直接向母公司索款并责令其先行清偿主债务人财产", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "ID:UU_6_2023_CiptaKerja:Art42",
        "law": "ID:UU_6_2023",
        "enbez": "Art 42",
        "title": "印尼创造就业法第42条：外籍用工RPTKA许可与1:1本土学徒配额法定要求",
        "heading_path": "印尼创造就业法 (UU No. 6/2023) > 劳工编 > 外籍劳工雇用与技术转让义务",
        "language_mode": "bilingual",
        "lang_original": "id",
        "text_original": "Setiap pemberi kerja yang mempekerjakan tenaga kerja asing wajib memiliki Rencana Penggunaan Tenaga Kerja Asing (RPTKA) yang disahkan oleh Pemerintah Pusat. Pemberi kerja wajib menunjuk tenaga kerja warga negara Indonesia sebagai tenaga kerja pendamping TKA yang dipekerjakan untuk alih teknologi dan alih keahlian.",
        "text_en": "Employers hiring foreign workers must obtain government-approved RPTKA and designate Indonesian companion workers for technology and skill transfer, strictly prohibiting foreigners in HR positions.",
        "text_zh": "【外工RPTKA用工计划与本土学徒对等配备强制规定】：任何企业聘用外国员工，必须事先取得劳工部批准的外籍员工使用计划（RPTKA）；每聘用一名外籍人员必须配备至少一名印尼本土对接人员（Pendamping）开展技能转让培训，且法律明文严禁外籍劳工担任企业人事管理（HR）岗位！【出海攻防启示】：印尼劳工合规第一高压线！中资火电、电解铝及轨道交通项目建设高峰期，国内派遣大量工程技术专家进场，项目部必须提前 2 个月申办 RPTKA，并与印尼当地学徒签署合规培养协议，绝不可为图省事挂靠办理非技术工种，严防移民局以‘非法就业’封停项目并扣押中方人员！",
        "norm_category": "labor_compliance",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_id_rptka_approval", "text_zh": "要件一：在拟用工前正式取得印尼中央劳工部签发的 RPTKA 正式批准文书", "status": "condition_precedent"},
            {"eid": "e_id_companion_worker", "text_zh": "要件二：为每一位外派中方技术岗位对应配备印尼籍本地学徒并订立技术转移考核档案", "status": "mandatory"},
            {"eid": "e_id_labor_sanctions", "text_zh": "法律后果：确立用工合法性；违者面临行政停工令、每日计罚高额行政罚款及吊销企业涉外经营资格", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "ID:UU_7_2011_Currency:Art21",
        "law": "ID:UU_7_2011",
        "enbez": "Art 21",
        "title": "印尼货币法第21条：印尼境内强制使用盾币结算与离岸外币采购例外",
        "heading_path": "印尼货币法 (UU No. 7/2011) > 第二编 货币使用义务 > 第21条 盾币强制流通与例外",
        "language_mode": "bilingual",
        "lang_original": "id",
        "text_original": "Rupiah wajib digunakan dalam setiap transaksi yang mempunyai tujuan pembayaran, penyelesaian kewajiban lain yang harus dipenuhi dengan uang, dan/atau transaksi keuangan lainnya yang dilakukan di Wilayah Negara Kesatuan Republik Indonesia, kecuali transaksi pembayaran internasional hoặc các dự án cơ sở hạ tầng chiến lược được phê duyệt.",
        "text_en": "Rupiah must be used in all cash and non-cash payment transactions within Indonesia, except international trade payments, international financing, or approved strategic projects.",
        "text_zh": "【印尼境内强制印尼盾结算与EPC双合同拆分法理根基】：在印度尼西亚领土范围内进行的所有支付交易、债务清偿与工程结算，必须强制使用法定货币印尼盾（IDR）；违规使用美元或其他外币结算的，处最高 1 年有期徒刑及 2 亿盾刑事罚金！但涉及境外进出口货物采购的国际交易除外。【出海攻防启示】：中资 EPC 出海印尼最核心的合同架构设计底座！为规避货币法刑事制裁同时防范汇率剧烈贬值，中资承包商必须将 EPC 合同拆分为《离岸设备供货合同》（中国母公司签约，以美元在境外结算，合法免受货币法管辖）与《在岸安装施工合同》（印尼子公司签约，以印尼盾结算），严禁签署单一体内美元大包合同！",
        "norm_category": "foreign_exchange",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_id_currency_in_country", "text_zh": "要件一：交易履约行为与工程施工作业物理发生在印度尼西亚共和国主权领土范围内", "status": "condition_precedent"},
            {"eid": "e_id_currency_split_structure", "text_zh": "要件二：合同双方通过离岸贸易或在岸施工拆分机制将跨国与属地结算进行法律隔离", "status": "mandatory"},
            {"eid": "e_id_currency_compliance", "text_zh": "法律后果：在岸交易强制以印尼盾履行，离岸合同受国际贸易例外豁免保护，杜绝合同无效与刑事责任", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "ID:UU_4_1996_HakTanggungan:Art4",
        "law": "ID:UU_4_1996",
        "enbez": "Art 4",
        "title": "印尼不动产抵押权法第4条：建筑使用权HGB抵押有效性与银团优先受偿权",
        "heading_path": "印尼不动产抵押权法 (UU No. 4/1996) > 抵押标的与设立条件 > 建筑使用权(HGB)抵押",
        "language_mode": "bilingual",
        "lang_original": "id",
        "text_original": "Hak atas tanah yang dapat dibebani Hak Tanggungan adalah: Hak Milik, Hak Guna Usaha, dan Hak Guna Bangunan (HGB). Hak Tanggungan memberikan kedudukan yang diutamakan (preferent) kepada kreditur tertentu terhadap kreditur-kreditur lain.",
        "text_en": "Land rights that can be encumbered by Hak Tanggungan include Hak Milik, HGU, and Hak Guna Bangunan (HGB), granting senior priority (preferent) to registered creditors.",
        "text_zh": "【建筑使用权HGB不动产抵押优先受偿权】：外资企业（PT PMA）合法持有的建筑使用权（HGB），依法属于可设立不动产抵押权（Hak Tanggungan）的法定财产标的；抵押权自土地局完成登记签发抵押证书（Sertifikat Hak Tanggungan）之日起生效，赋予抵押权人对抗所有普通无担保债权人的绝对第一顺位优先受偿权（Preferent Creditor）！【出海攻防启示】：海外电站与工业园区项目融资的定海神针！中资外资企业无法持有土地所有权（Hak Milik），必须取得长达 30+20 年的 HGB，并通过在土地局正式设立 Hak Tanggungan，才能确保境内外银团长期有限追索贷款抵押权合法成立，防范债务违约时厂房土地被属地其他债权人查封侵占！",
        "norm_category": "property_security",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_id_hgb_title_valid", "text_zh": "要件一：抵押人合法持有尚在有效存续期内的建筑使用权（HGB）土地使用权证书", "status": "condition_precedent"},
            {"eid": "e_id_hgb_bapan_registration", "text_zh": "要件二：通过持牌公证人（PPAT）签署正式抵押契约并在国家土地局（BPN）完成电子登记备案", "status": "mandatory"},
            {"eid": "e_id_hgb_senior_priority", "text_zh": "法律后果：确立具有执行力名义的不动产抵押优先权，债务人违约时债权人享有直接申请法院强制拍卖拍卖权", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "ID:Perpres_10_2021_Investment:List3",
        "law": "ID:Perpres_10_2021",
        "enbez": "List 3",
        "title": "印尼2021年第10号总统令：外资准入优先清单与中小施工限制及KSO联合体强制要求",
        "heading_path": "印尼总统令第10/2021号 (jo. Perpres 49/2021) > 投资业务分类 > 附表三 外资与中小微合作限制清单",
        "language_mode": "bilingual",
        "lang_original": "id",
        "text_original": "Bidang usaha yang dicadangkan untuk Koperasi dan UMKM atau bidang usaha yang terbuka untuk Usaha Besar dengan syarat kemitraan: Jasa konstruksi umum dengan nilai proyek di bawah Rp50 Miliar dialokasikan untuk UMKM-K. Untuk proyek berskala besar, badan usaha jasa konstruksi asing (BUJKA) wajib bermitra dalam bentuk Joint Operation (KSO).",
        "text_en": "Construction projects under IDR 50 billion reserved for local SMEs; large projects allow foreign contractors only via Joint Operation (KSO) with 100% domestic partner leading specified works.",
        "text_zh": "【500亿印尼盾以下工程外资禁止与联合体KSO强制配额】：合同金额低于 500 亿印尼盾（约 330 万美元）的常规建筑工程，法定专属保留给印尼本土中小微企业，严禁外商设立独资施工实体介入；超过 500 亿盾的大型工程，外国建筑企业办事处（BUJKA）必须与印尼本土大中型施工企业组建联合体（KSO），且本土联合体方实际承担的工作量比例不得低于法定比例！【出海攻防启示】：中资央企承接印尼中大型基建，切忌以单一独资身份参标！必须严格依照总统令遴选具备相应资质的印尼本土合伙方组建合法合规的 KSO 联合体，在联合体协议中锁定工程实质主导权与现金流专户监管机制！",
        "norm_category": "foreign_investment",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_id_invest_project_value", "text_zh": "要件一：承包项目总合同金额达到 500 亿印尼盾以上之大型复杂基础设施工程规模门槛", "status": "condition_precedent"},
            {"eid": "e_id_invest_kso_agreement", "text_zh": "要件二：与具备印尼公共工程部有效执照的本土持牌企业订立正式联合体合作经营协议（KSO）", "status": "mandatory"},
            {"eid": "e_id_invest_bujka_compliance", "text_zh": "法律后果：取得合法投标资质与公共工程部许可证；未组建 KSO 者投标无效且合同自始绝对无效", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "ID:KUHPerdata:Art1244_1245",
        "law": "ID:KUHPerdata",
        "enbez": "Art 1244-1245",
        "title": "印尼民法典第1244-1245条：不可抗力免责与利息赔偿豁免法定要件",
        "heading_path": "印尼民法典 (KUHPerdata) > 债编 > 不履行之损害赔偿与不可抗力免责",
        "language_mode": "bilingual",
        "lang_original": "id",
        "text_original": "Debitur harus dihukum untuk mengganti biaya, kerugian dan bunga bila ia tak dapat membuktikan bahwa tidak dilaksanakannya perikatan itu disebabkan oleh suatu hal yang tak terduga, yang tak dapat dipertanggungjawabkan kepadanya, sekalipun tidak ada itikad buruk padanya. Tidak ada penggantian biaya, kerugian dan bunga, bila karena keadaan memaksa (overmacht) debitur berhalangan memberikan atau berbuat sesuatu.",
        "text_en": "Debtor is liable for damages unless proving non-performance was caused by unexpected force majeure beyond debtor's responsibility; no damages or interest payable if prevented by overmacht.",
        "text_zh": "【不可抗力免除违约金与利息赔偿法定请求权】：若债务人能举证证明未能按期履行义务系因不可预见且不可归责于其自身的事由（Overmacht / Keadaan Memaksa）所致，债务人依法免于承担损害赔偿责任；因不可抗力导致履行障碍期间，严禁向其索赔任何本金损害赔偿、费用补偿及法定迟延利息！【出海攻防启示】：遭遇印尼火山喷发、海啸或政府政策关停施工时的绝对免责盾牌！总承包商一旦因外部天灾或政府行政行为停工，应立即依本条固定气象、地质及行政公函证据，阻断业主扣押误期违约金及索兑履约保函的全部索赔！",
        "norm_category": "breach_remedy",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_id1244_unforeseen_cause", "text_zh": "要件一：发生特大自然灾害或政府主权行为等无法归责于承包商的不可预见阻碍事件", "status": "condition_precedent"},
            {"eid": "e_id1244_timely_notification", "text_zh": "要件二：在合同及法律规定期限内向定作人签发正式不可抗力预警与书面佐证通知", "status": "mandatory"},
            {"eid": "e_id1244_damages_exemption", "text_zh": "法律后果：法定免除因履行迟延导致的损害赔偿金、惩罚性违约金与逾期利息之给付义务", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "ID:KUHPerdata:Art1250",
        "law": "ID:KUHPerdata",
        "enbez": "Art 1250",
        "title": "印尼民法典第1250条：金钱之债迟延履行法定年利率6%计算规则",
        "heading_path": "印尼民法典 (KUHPerdata) > 债编 > 金钱之债迟延利息",
        "language_mode": "bilingual",
        "lang_original": "id",
        "text_original": "Dalam perikatan yang semata-mata mengenai pembayaran sejumlah uang, penggantian biaya, kerugian dan bunga yang timbul karena keterlambatan pelaksanaannya, hanya terdiri atas bunga yang ditentukan oleh undang-undang, tanpa mengurangi ketentuan undang-undang khusus. Bunga tersebut mulai dihitung sejak hari diajukannya gugatan ke pengadilan.",
        "text_en": "In obligations regarding payment of money, damages for delay consist exclusively of statutory interest (6% per annum), calculated from the day formal legal claim or notice is lodged.",
        "text_zh": "【金钱债务逾期法定利息年化6%排他性规则】：对于纯粹以金钱给付为标的的债权（如工程进度款、退还保函保证金），因迟延履行所产生的损害赔偿，法律规定仅限于法定利息（Statutory Interest，依印尼特别法令通常固定为每年 6%）；除法律另有专门规定外，债权人无权在无约定情形下擅自追加计算复利或惩罚性索赔！【出海攻防启示】：业主恶意拖欠工程款时的利息追索法定底线！中资承包商主张进度款欠款时，若合同未约定超额逾期利息，可直接依据 Art 1250 诉请印尼法院或仲裁庭自催告之日起加计按年 6% 的法定利息，确保资金成本获得全额司法补偿！",
        "norm_category": "breach_remedy",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_id1250_monetary_debt", "text_zh": "要件一：债权标的属于已届清偿期且金额确定之工程款或保证金金钱债务", "status": "condition_precedent"},
            {"eid": "e_id1250_formal_demand", "text_zh": "要件二：债权人已向债务人发出正式书面催告函（Somasi）或提起法院/仲裁立案", "status": "mandatory"},
            {"eid": "e_id1250_statutory_interest", "text_zh": "法律后果：依法按年化 6% 法定利率计付自催告之日起至实际清偿日止的全部利息", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "ID:KUHPerdata:Art1478",
        "law": "ID:KUHPerdata",
        "enbez": "Art 1478",
        "title": "印尼民法典第1478条：未获工程款交付标的物之同时履行抗辩权",
        "heading_path": "印尼民法典 (KUHPerdata) > 买卖与承揽交付义务 > 同时履行抗辩权",
        "language_mode": "bilingual",
        "lang_original": "id",
        "text_original": "Penjual tidak wajib menyerahkan barang, jika pembeli belum membayar harganya, sedangkan penjual tidak telah mengizinkan penundaan pembayaran kepadanya.",
        "text_en": "Seller (contractor) is not obliged to deliver goods or completed works if buyer (employer) has not paid the agreed price, unless deferred payment was agreed.",
        "text_zh": "【未付款前拒绝交付工程之同时履行抗辩权】：在买卖与承揽工程法律关系中，若发包人未依照约定足额支付相应到期工程价款，且承包商未同意发包人延期付款的，承包商依法享有拒绝移交工程实物、拒绝交付调试钥匙之合法抗辩权（Exceptio Non Adimpleti Contractus）！【出海攻防启示】：防止业主‘骗取工程移交后再拒付款项’的最强筹码！工程达到实质竣工时，若业主仍拖欠数百亿印尼盾期中款或变更款，中资总包切忌草率移交现场控制权！依据 Art 1478 牢牢把守厂房大门与控制室，直至业主结清款项或开立不可撤销信用证方可正式放行！",
        "norm_category": "contract_performance",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_id1478_unpaid_due_price", "text_zh": "要件一：发包人未按合同约定期限足额支付经审核到期的工程进度款或节点款", "status": "condition_precedent"},
            {"eid": "e_id1478_no_deferred_consent", "text_zh": "要件二：承包商未作出过任何同意免除或单方延缓该笔款项支付的正式意思表示", "status": "mandatory"},
            {"eid": "e_id1478_withhold_delivery", "text_zh": "法律后果：承包商合法行使留置与拒绝移交占有权，免于承担任何违约交付或延滞交钥匙责任", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "ID:UU_2_2017:Art30_KSO",
        "law": "ID:UU_2_2017",
        "enbez": "Art 30",
        "title": "印尼2017年建筑服务法第30条：外国建筑企业组建联合体KSO资质审查强制规则",
        "heading_path": "印尼2017年建筑服务法 (UU No. 2/2017) > 外国建筑企业办事处(BUJKA) > 第30条 联合体经营强制规范",
        "language_mode": "bilingual",
        "lang_original": "id",
        "text_original": "Kantor Perwakilan Badan Usaha Jasa Konstruksi Asing hanya dapat menyelenggarakan jasa konstruksi melalui kerja sama operasi (KSO) dengan badan usaha jasa konstruksi nasional yang memiliki kualifikasi besar. Badan usaha nasional yang bermitra harus memimpin KSO untuk pekerjaan yang dapat dilaksanakan oleh tenaga kerja nasional.",
        "text_en": "Foreign construction representative offices (BUJKA) must execute construction works solely through Joint Operations (KSO) with qualified national contractors, prioritizing local labor.",
        "text_zh": "【BUJKA外国代表处组建联合体经营强制法理】：外国建筑服务企业在印尼设立的代表处（BUJKA），严禁以自身名义独立承揽施工；必须且仅能与具备大型资质（Kualifikasi Besar）的印尼本国建筑企业组建联合运营体（KSO）；且在技术可由印尼本国劳工完成的作业领域，法律强制要求本土企业担任联合体牵头方！【出海攻防启示】：资质穿透审查防线！中资企业在印尼以 BUJKA 形式运作时，必须审慎核验印尼本土联合体伙伴的企业资质证书（SBU），确保其资质级别满足“Kualifikasi Besar”法定门槛，防止被竞争对手投诉导致联合体投标被公共工程部直接废标！",
        "norm_category": "construction_regulatory",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_id_bujka_rep_office", "text_zh": "要件一：外资承包商以公共工程部合法登记的外国代表处（BUJKA）形态在印尼开展业务", "status": "condition_precedent"},
            {"eid": "e_id_kso_big_qualification", "text_zh": "要件二：联合体本土合作伙伴必须持有公共工程部认证核发的大型级资质证书（SBU Kualifikasi Besar）", "status": "mandatory"},
            {"eid": "e_id_kso_valid_standing", "text_zh": "法律后果：取得合法参标与缔约民事权利能力；违规单边承揽者合同自始无效且办事处予以取缔注销", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "ID:Tax_Law_KSO:PP_51_2008_jo_PP_9_2022",
        "law": "ID:PP_9_2022_Tax",
        "enbez": "PP 9/2022",
        "title": "印尼政府第9/2022号条例：KSO联合体建筑服务最终所得税(PPh Final)穿透计征规程",
        "heading_path": "印尼税法政府条例 (PP No. 9/2022 amending PP 51/2008) > 建筑服务所得税 > 联合体税款代扣代缴与发票",
        "language_mode": "bilingual",
        "lang_original": "id",
        "text_original": "Penghasilan dari usaha jasa konstruksi dikenakan Pajak Penghasilan yang bersifat final. Terhadap Kerja Sama Operasi (KSO) yang memiliki NPWP tersendiri, pemotongan PPh Final dilakukan atas nama KSO; bagi KSO non-NPWP, pemotongan dan penerbitan Faktur Pajak dilakukan secara proporsional oleh masing-masing anggota KSO.",
        "text_en": "Construction income is subject to final income tax (PPh Final). For KSOs with independent tax numbers (NPWP), tax is withheld on KSO; for non-NPWP KSOs, members issue tax invoices proportionally.",
        "text_zh": "【联合体KSO建筑服务最终所得税穿透征收】：印尼对建筑工程施工收入征收排他性最终所得税（PPh Final，大型持证施工税率为 2.65%，无证为 4%）；对于拥有独立税号的联合体（Administrative JO），由发包人统一代扣并向联合体开具完税证明；对于无独立税号联合体，由各成员按合同约定收益比例分别承担连带代扣代缴义务！【出海攻防启示】：印尼联合体税务暴雷防护网！中资企业组建 KSO 时，必须在联合体协议中明文约定采用‘独立税号 KSO’模式并由联合体财务专户代扣代缴 PPh Final，严防因属地合作方挪用工程款未报税，导致印尼税务局（DJP）依据税法连带责任强行穿透冻结中方母公司在岸银行账户！",
        "norm_category": "tax_compliance",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_id_tax_kso_construction_revenue", "text_zh": "要件一：联合体在印尼境内承接工程并自发包人处取得建筑安装工程进度款项收入", "status": "condition_precedent"},
            {"eid": "e_id_tax_kso_npwp_status", "text_zh": "要件二：明确界定联合体属于拥有独立税号（Administrative JO）或穿透分别核算模式", "status": "mandatory"},
            {"eid": "e_id_tax_kso_pph_final_deduction", "text_zh": "法律后果：适用 2.65% 最终税优惠税率闭环纳税，彻底终结企业所得税年度汇算清缴之后续税务穿透追缴", "status": "legal_consequence"}
        ], ensure_ascii=False)
    }
]


PHASE10_L1_NORMS_BATCH2 = [
    # ==========================================
    # 3. 马来西亚 (asean_my) - 10 条 L1 强行法
    # ==========================================
    {
        "table": "norms",
        "norm_id": "MY:Contracts_Act_1950:Sec52_55",
        "law": "MY:Contracts_Act_1950",
        "enbez": "Sec 52-55",
        "title": "马来西亚1950年合同法第52-55条：双务对价履行次序与防阻原则Prevention成文法基石",
        "heading_path": "马来西亚1950年合同法 (Act 136) > 相互承诺履行 > 第52-55条 相互承诺履行次序与阻碍履约之后果",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Order of performance of reciprocal promises: Where the order in which reciprocal promises are to be performed is expressly fixed by the contract, they shall be performed in that order. When a contract contains reciprocal promises, and one party prevents the other from performing his promise, the contract becomes voidable at the option of the party so prevented; and he is entitled to compensation from the other party for any loss.",
        "text_en": "Reciprocal promises must be performed in agreed order; where one party prevents the other from performing, the prevented party may avoid the contract and claim full compensation.",
        "text_zh": "【防阻原则成文法根基与定作人阻碍违约】：在相互承诺的合同中，若合同明确约定了履行次序，各方必须按该顺序履约；若一方当事人阻碍相对方履行其承诺（如雇主未按期交地、工程师迟发图纸阻碍施工），受阻碍方有权选择撤销合同，并有权向阻碍方索赔由此遭受的全部损失！【出海攻防启示】：普通法‘防阻原则（Prevention Principle）’在马来西亚的成文法法理母体！大马业主一旦迟延移交施工面，即构成 Sec 54 项下法定阻碍，中资总包依此条主张工期自动顺延，业主彻底丧失依据原合同扣罚误期违约金（Liquidated Damages）的请求权！",
        "norm_category": "contract_performance",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_my52_reciprocal_order", "text_zh": "要件一：合同约定了发包人先期移交无障碍施工现场或交付图纸的前置履行次序", "status": "condition_precedent"},
            {"eid": "e_my52_prevention_act", "text_zh": "要件二：发包人存在未按期交地或拖延技术审批之客观阻碍承包商施工行为", "status": "mandatory"},
            {"eid": "e_my52_prevention_remedy", "text_zh": "法律后果：承包商享有法定工期顺延与费用赔偿请求权，发包人丧失误期违约金追索权", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "MY:CIPAA_2012:Sec35",
        "law": "MY:CIPAA_2012",
        "enbez": "Sec 35",
        "title": "马来西亚2012年建筑业支付与快速裁决法第35条：反背靠背支付条款法定绝对无效",
        "heading_path": "马来西亚建筑业支付与快速裁决法 (CIPAA 2012, Act 746) > 第四编 一般规定 > 第35条 条件支付条款绝对无效",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Conditional payment: Any conditional payment provision in a construction contract in relation to payment is void. A conditional payment provision includes any provision that makes payment contingent upon the payer receiving payment from a third party (pay-when-paid or pay-if-paid).",
        "text_en": "Any conditional payment provision in a construction contract (including pay-when-paid or pay-if-paid clauses) is void and unenforceable under Malaysian statutory law.",
        "text_zh": "【反背靠背支付条款法定绝对无效重锤】：在马来西亚建设工程合同中，任何形式的‘条件支付条款（Conditional Payment Provision）’自始绝对无效！包括一切约定‘总包商收到业主付款后方向分包商付款（Pay-when-paid / Pay-if-paid）’或以业主签发最终结算为前置条件的条款，在法律上均被强行抹杀，不具任何执行力！【出海攻防启示】：中资总承包商赴马履约的最高风险红线！中资总包在国内习惯性在分包合同中植入‘收到业主进度款后同比例支付分包’条款；但在马来西亚，属地分包商可直接依据 CIPAA Sec 35 宣告该条款无效，并提请快速裁决在 45 天内冻结总包银行账户强行划款！总包必须审慎进行分包现金流匹配，绝不可依赖背靠背防御！",
        "norm_category": "construction_regulatory",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_my_cipaa35_construction_contract", "text_zh": "要件一：合同标的属于马来西亚领土范围内实施的建筑、土木、机电工程施工分包合同", "status": "condition_precedent"},
            {"eid": "e_my_cipaa35_pay_when_paid_clause", "text_zh": "要件二：合同条款中将向分包商的付款条件与总包商自第三方发包人处受领款项挂钩绑定", "status": "mandatory"},
            {"eid": "e_my_cipaa35_statutory_nullity", "text_zh": "法律后果：该背靠背条款被法律强制宣告无效，总包商负有到期无条件直接支付分包工程款之法定义务", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "MY:CIDB_Act_520:Sec25",
        "law": "MY:CIDB_Act_520",
        "enbez": "Sec 25",
        "title": "马来西亚建筑工业发展局法第25条：未持证开展施工投标合同自始无效与刑事制裁",
        "heading_path": "马来西亚建筑工业发展局法 (Lembaga Pembangunan Industri Pembinaan Malaysia Act 520) > 承包商注册 > 第25条 执照强制注册",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "No person shall undertake or complete any construction work unless he is registered with the Lembaga (CIDB) and holds a valid certificate of registration. Any person who contravenes this section commits an offence and shall, on conviction, be liable to a fine of not less than RM 10,000 but not exceeding RM 100,000.",
        "text_en": "No person shall execute or complete construction works without holding a valid CIDB registration certificate; contracts executed by unregistered entities are illegal and void.",
        "text_zh": "【CIDB承包商注册证强制持有与无证合同绝对无效】：任何实体未在建筑工业发展局（CIDB）正式注册并持有有效注册证书（涵盖 G1 至 G7 等级），严禁在马来西亚承揽、投标或组织实施任何工程建设；违者构成刑事犯罪，处 1 万至 10 万令吉刑事罚金，且其签署的工程合同依普通法被认定为违法合同自始绝对无效，承包商无权主张任何工程款！【出海攻防启示】：中资出海大马的准入门票！中资企业投标马来西亚大型基建前，必须以马来西亚子公司或持牌合资公司名义申办 CIDB 最高级别‘G7 资质’（无限金额施工能力），严防因执照未获批提前签约被竞争对手以‘违反公法强行法’起诉撤销合同！",
        "norm_category": "construction_regulatory",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_my_cidb25_construction_activity", "text_zh": "要件一：主体在马来西亚领土范围内开展建设工程的投标、勘察、设计、采购或现场施工作业", "status": "condition_precedent"},
            {"eid": "e_my_cidb25_valid_g7_license", "text_zh": "要件二：已依法取得 CIDB 颁发且尚在有效存续期内的注册承包商等级证书（如 Grade G7）", "status": "mandatory"},
            {"eid": "e_my_cidb25_contract_legality", "text_zh": "法律后果：确立工程合同民商事效力；无证签约者合同自始绝对无效，刑事罚金并没收全部非法收益", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "MY:MACC_Act_2009:Sec17A",
        "law": "MY:MACC_Act_2009",
        "enbez": "Sec 17A",
        "title": "马来西亚反贪污委员会法第17A条：商业组织行贿法定连带刑事责任与充分预防程序抗辩",
        "heading_path": "马来西亚反贪污委员会法 (MACC Act 2009, Act 694) > 腐败犯罪 > 第17A条 商业组织企业刑事责任",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Corporate liability: A commercial organisation commits an offence if a person associated with the commercial organisation corruptly gives, agrees to give, promises or offers to any person any gratification with intent to obtain or retain business. Penalty: fine not less than 10 times the gratification or RM 1 million, or imprisonment up to 20 years. Defense: proving adequate procedures were in place.",
        "text_en": "Commercial organisations are criminally liable for corrupt gratification given by associated persons (subcontractors, agents) to obtain/retain business, unless proving Adequate Procedures defense.",
        "text_zh": "【反贪会商业组织连带刑事追责与充分预防程序抗辩】：若与商业组织关联的人员（包括分包商、顾问、代理人、中间人）为该企业获取或保留工程业务而向任何人实施商业贿赂，该商业组织本身构成连带刑事犯罪！法定处罚为处贿赂金额 10 倍以上或 100 万令吉以上罚金，相关董事与高管面临最高 20 年监禁！企业唯一的法定免责抗辩为证明其已建立符合官方 T.R.U.S.T 框架的‘充分预防程序（Adequate Procedures）’！【出海攻防启示】：中资央企海外廉政最高风险点！东南亚征地清障与许可办理环节常涉及本地‘咨询服务费’，一旦属地中介涉嫌行贿，MACC 将直接穿透追究中资母公司与在岸高管刑事责任！中资项目部必须建立全流程第三方反腐尽调档案并签署反商业贿赂承诺书，激活‘充分预防程序’免责盾牌！",
        "norm_category": "anti_corruption",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_my_macc17a_associated_person", "text_zh": "要件一：行贿行为系由企业的雇员、分包商、联合体伙伴或咨询中介等关联人员实施", "status": "condition_precedent"},
            {"eid": "e_my_macc17a_corrupt_intent", "text_zh": "要件二：行贿主观意图系为中资工程企业获取授标、通过验收或保留特定商业合同利益", "status": "mandatory"},
            {"eid": "e_my_macc17a_adequate_procedures_defense", "text_zh": "法律后果：企业承担企业刑事责任与天价罚金；若已建立合规充分预防程序体系则享有法定刑事豁免", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "MY:Companies_Act_2016:Sec196_216",
        "law": "MY:Companies_Act_2016",
        "enbez": "Sec 196-216",
        "title": "马来西亚2016年公司法第196-216条：常住董事法定要求与少数股东压迫救济权",
        "heading_path": "马来西亚2016年公司法 (Act 777) > 董事管理与小股东保护 > 常住董事与小股东压迫救济",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Every private company shall have at least one director who ordinarily resides in Malaysia by having a principal place of residence in Malaysia. Oppression remedy: Any member may apply to the Court for an order if the affairs of the company are being conducted or the powers of directors are being exercised in a manner oppressive to one or more members.",
        "text_en": "Malaysian private companies must have at least one ordinarily resident director; minority shareholders may petition High Court for relief against commercial oppression or unfair prejudice.",
        "text_zh": "【本地常住董事法定门槛与小股东压迫救济司法机制】：马来西亚私人有限公司（Sdn Bhd）必须至少有一名主要居住地在马来西亚境内的常住董事（Resident Director）；同时，若控股大股东滥用控制权侵害合资公司利益，少数股东依法享有向高等法院申请‘小股东压迫救济（Oppression Remedy）’之法定诉权，法院有权下令大股东按公允估值强制回购股份或直接解散公司！【出海攻防启示】：中马合资企业治理攻防要冲！中资央企与大马土著企业组建合资 SPV 承揽铁路水务项目时，聘用属地常住董事需设置联合签批授权（Dual Sign-off）；同时在合资章程中严密设计表决权保留条款，防止中资作为非控股股东遭遇属地合伙方恶意压迫掏空合资资产！",
        "norm_category": "corporate_governance",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_my_ca196_resident_director", "text_zh": "要件一：合资公司董事会中必须配置符合内陆税收局常住身份标准的本地自然人董事", "status": "condition_precedent"},
            {"eid": "e_my_ca216_oppressive_conduct", "text_zh": "要件二：大股东滥用表决权排挤中方董事知情权、隐匿关联交易或恶意稀释中方股权", "status": "mandatory"},
            {"eid": "e_my_ca216_court_remedy", "text_zh": "法律后果：高等法院裁定签发禁令干预公司治理，责令加害方以无折价公允价格全额收购中资股份", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "MY:Contracts_Act_1950:Sec28_29",
        "law": "MY:Contracts_Act_1950",
        "enbez": "Sec 28-29",
        "title": "马来西亚1950年合同法第28-29条：限制贸易与限制司法诉讼救济程序条款绝对无效",
        "heading_path": "马来西亚1950年合同法 (Act 136) > 无效协议 > 第28-29条 限制贸易与限制司法救济条款绝对无效",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Agreements in restraint of legal proceedings: Every agreement by which any party thereto is restricted absolutely from enforcing his rights under or in respect of any contract, by the usual legal proceedings in the ordinary tribunals, or which limits the time within which he may thus enforce his rights, is void to that extent. (Arbitration agreements excepted).",
        "text_en": "Agreements absolutely restricting a party from enforcing legal rights through ordinary tribunals, or limiting statutory limitation periods, are void to that extent.",
        "text_zh": "【限制司法救济程序与缩减诉讼时效条款无效】：任何旨在绝对限制当事人通过常规司法裁判途径主张其民商事权利、或旨在人为压缩法定诉讼时效期间的合同条款，在法律上自始绝对无效！【出海攻防启示】：反击业主苛刻除斥期条款的重磅法理武器！境外业主常在合同专用条件中约定‘承包商未在争议发生后 7 天内起诉即永久放弃索赔权’等极端条款；在马来西亚法下，此类人为剥夺或限制诉权的约定直接抵触 Sec 29 强行法而归于消灭，中资总包依然享有依据《时效法》享有的 6 年法定诉讼救济期！",
        "norm_category": "contract_formation",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_my29_restraint_clause", "text_zh": "要件一：合同条款中包含了单方剥夺承包商诉权、排除法院管辖或过分缩短法定索赔时效的限制性约定", "status": "condition_precedent"},
            {"eid": "e_my29_statutory_inconsistency", "text_zh": "要件二：该限制性约定实质性侵害了当事人依据成文法享有的一般司法审判救济权利", "status": "mandatory"},
            {"eid": "e_my29_void_pro_tanto", "text_zh": "法律后果：该限制条款在抵触范围内自始绝对无效，全面恢复当事人法定的司法诉讼与仲裁抗辩权利", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "MY:Contracts_Act_1950:Sec40",
        "law": "MY:Contracts_Act_1950",
        "enbez": "Sec 40",
        "title": "马来西亚1950年合同法第40条：拒绝履行全部承诺守约方之单方合同法定解除权",
        "heading_path": "马来西亚1950年合同法 (Act 136) > 合同履行 > 第40条 拒绝履行全部承诺之解除权",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "When a party to a contract has refused to perform, or disabled himself from performing, his promise in its entirety, the promisee may put an end to the contract, unless he has signified, by words or conduct, his acquiescence in its continuance.",
        "text_en": "When a party refuses to perform or disables himself from performing his promise in its entirety, the promisee may terminate the contract unless having acquiesced in its continuance.",
        "text_zh": "【毁约性违约与守约方单方终止合同撤场权】：当一方当事人拒绝履行、或因自身原因导致其完全无法履行其在合同项下的全部承诺时，守约方有权立即宣布单方解除合同并终止履约，除非守约方已通过言词或实际行为明示默示同意继续履行合同！【出海攻防启示】：面对大马业主彻底瘫痪工程时的法定退场利器！当业主无限期暂停工程长达数月且停止支付任何工程款时，承包商依据 Sec 40 发函正式解除合同，依法立即退场并启动清算，索赔全部已投入成本及合同预期利润损失（Loss of Profit）！",
        "norm_category": "breach_remedy",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_my40_repudiatory_breach", "text_zh": "要件一：违约方实施了明示拒绝履约、恶意关停现场或实质性丧失履约能力的根本性违约行为", "status": "condition_precedent"},
            {"eid": "e_my40_no_acquiescence", "text_zh": "要件二：守约方在获知该根本违约后未作出任何同意继续施工或放弃追究的默示行为", "status": "mandatory"},
            {"eid": "e_my40_lawful_termination", "text_zh": "法律后果：守约方享有合法解除合同权利，免除后续一切施工义务并全额索赔预期利润损失", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "MY:Civil_Law_Act_1956:Sec11",
        "law": "MY:Civil_Law_Act_1956",
        "enbez": "Sec 11",
        "title": "马来西亚1956年民事法第11条：法院与仲裁庭裁定判决前与判决后利息之自由裁量权",
        "heading_path": "马来西亚1956年民事法 (Act 67) > 判决利息 > 第11条 判决利息自由裁量权",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Power of Courts to award interest on debts and damages: In any proceedings for the recovery of any debt or damages, the Court may, if it thinks fit, order that there shall be included in the sum for which judgment is given interest at such rate as it thinks fit on the whole or any part of the debt or damages for the whole or any part of the period between the date when the cause of action arose and the date of the judgment.",
        "text_en": "Courts and arbitral tribunals possess statutory discretion to award pre-judgment and post-judgment interest at reasonable commercial rates on debts and damages from cause of action date.",
        "text_zh": "【法院与仲裁庭裁决判决前及判决后利息之法定裁量权】：在任何追索工程债务或损害赔偿的诉讼或仲裁程序中，主审法庭享有法定自由裁量权，在判决金额中计入其认为合理的利息（常规司法实务为年化 5%），计息区间覆盖自诉因发生之日起至判决作出之日（判决前利息）以及自判决作出之日起至实际清偿完毕之日（判决后利息）！【出海攻防启示】：跨境索赔资金成本全面覆盖！工程跨国仲裁往往历时 2~3 年，中资承包商在提起诉讼仲裁请求时，必须明确援引 Sec 11 索要自欠款发生当日起算的全额判决前商业利息，确保数千万美元拖欠款项的资金占用成本获得全额司法支持！",
        "norm_category": "breach_remedy",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_my_cla11_debt_recovery", "text_zh": "要件一：诉讼或仲裁主张的标的属于因违约拖欠产生的明确工程债务或实际损失求偿", "status": "condition_precedent"},
            {"eid": "e_my_cla11_discretionary_prayer", "text_zh": "要件二：在起诉状或仲裁申请书中显式提出了依据第 11 条加计判决前后利息的诉讼请求", "status": "mandatory"},
            {"eid": "e_my_cla11_interest_award", "text_zh": "法律后果：裁决判令加付年化 5% 商业利息，全面填补争议期间资金利息损失", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "MY:BNM_FE_Notices:Notice_2_Borrowing",
        "law": "MY:BNM_FE_Notices",
        "enbez": "Notice 2",
        "title": "马来西亚国家银行外汇管理通知第二号：居民借入超过1亿令吉等额外币贷款前置审批",
        "heading_path": "马来西亚国家银行外汇管理通知 (Bank Negara Malaysia FE Notices) > 借贷管理 > 第2号通知 跨境借贷外汇核准",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "A Resident Entity is permitted to borrow in Foreign Currency up to an aggregate amount of RM 100 million equivalent from non-resident entities. Any borrowing exceeding this prudential limit requires prior formal approval from Bank Negara Malaysia (BNM). Unapproved borrowings are subject to penalties and repatriation restrictions.",
        "text_en": "Resident entities may borrow foreign currency from non-residents up to RM 100 million equivalent; foreign loans exceeding this threshold strictly require BNM prior approval.",
        "text_zh": "【非居民外币贷款超1亿令吉强制BNM审批红线】：马来西亚居民企业（包括中资出海设立的本地全资子公司或合资 SPV），向境外非居民（如中国母公司或境内中资银行）借入外币借款，累计金额上限为 1 亿令吉等值；凡借款总额超出 1 亿令吉的，必须在协议签署并提取资金前取得马来西亚国家银行（BNM）的正式前置审批批文！【出海攻防启示】：中资央企跨境股东借贷资金调拨红线！中资母公司为大马重大轨道交通或港口项目提供大额股东借贷垫资（通常折合数亿美元），若未事先报批 BNM，后续还本付息将被马来西亚商业银行全额拒办出境，且借款协议面临司法执行不能的惨重后果！",
        "norm_category": "foreign_exchange",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_my_bnm_resident_borrower", "text_zh": "要件一：借款人属于在马来西亚境内注册设立的居民法律实体", "status": "condition_precedent"},
            {"eid": "e_my_bnm_threshold_100m", "text_zh": "要件二：向境外非居民借入的外汇贷款余额累计超过 1 亿林吉特等值法定额度", "status": "mandatory"},
            {"eid": "e_my_bnm_approval_necessity", "text_zh": "法律后果：必须取得 BNM 批复函件；未报批借贷属于外汇违法行为，外汇本息严禁汇出境外", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "MY:CIPAA_2012:Sec28_30",
        "law": "MY:CIPAA_2012",
        "enbez": "Sec 28-30",
        "title": "马来西亚CIPAA法第28-30条：快速裁决执行机制未付款工程材料留置与直接向发包人追款",
        "heading_path": "马来西亚建筑业支付与快速裁决法 (CIPAA 2012, Act 746) > 裁决执行 > 直接付款与现场留置权",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Enforcement of adjudication decision: If the principal has failed to pay the adjudicated amount, the winning party may apply for direct payment from principal's principal (employer), suspend works under Section 29, or exercise statutory lien over unfixed materials on site under Section 30.",
        "text_en": "Winning party in CIPAA adjudication may enforce decision by demanding direct payment from the principal employer, suspending works, or exercising statutory lien over unfixed materials.",
        "text_zh": "【CIPAA快速裁决执行三大利器直接向发包人索款与留置权】：在快速裁决中胜诉的承包商或分包商，若被裁决人拒不支付裁决款项，胜诉方享有三大法定硬核救济权力：① 依据第 30 条直接向被裁决人的上位发包人（Employer）发出法定催告，强制发包人从应付工程款余额中直接向胜诉分包商划款！② 依据第 29 条合法暂停施工并顺延工期！③ 对现场未安装的工程设备材料行使法定留置权！【出海攻防启示】：中资分包商突破总包阻碍直诉业主的黄金通道！中资企业在马作为指定分包商若遭遇当地总包赖账，直接启动 CIPAA 快速裁决并在获胜后依据 Sec 30 锁定业主工程款，越过中间总包直接收回血汗钱！",
        "norm_category": "construction_dispute",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_my_cipaa28_favourable_decision", "text_zh": "要件一：已依据 CIPAA 法定程序取得具备约束力的正式胜诉快速裁决书", "status": "condition_precedent"},
            {"eid": "e_my_cipaa28_non_payment", "text_zh": "要件二：被裁决人在法定期限届满后仍未遵照裁决履行金钱清偿义务", "status": "mandatory"},
            {"eid": "e_my_cipaa28_direct_enforcement", "text_zh": "法律后果：有权向终局发包人送达直接付款指令，发包人负有法定连带直接代付义务", "status": "legal_consequence"}
        ], ensure_ascii=False)
    }
]


PHASE10_L1_NORMS_BATCH3 = [
    # ==========================================
    # 4. 新加坡 (asean_sg) - 10 条 L1 强行法
    # ==========================================
    {
        "table": "norms",
        "norm_id": "SG:Building_Control_Act:Sec8_9",
        "law": "SG:Building_Control_Act",
        "enbez": "Sec 8-9",
        "title": "新加坡建筑控制法第8-9条：建设局BCA结构工程监管与无开工许可施工刑事罚则",
        "heading_path": "新加坡建筑控制法 (Building Control Act Cap 29) > 结构工程审批 > 许可前置与停工令",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Application for permit to carry out structural works: No person shall commence or carry out any structural works without a valid permit issued by the Commissioner of Building Control. Any person who contravenes commits an offence and shall be liable on conviction to a fine not exceeding $200,000 or to imprisonment for a term not exceeding 2 years.",
        "text_en": "No person shall carry out structural works without a valid permit from BCA; unauthorized works constitute criminal offences subject to mandatory Stop-Work Orders.",
        "text_zh": "【BCA开工许可证强制申办与无证施工刑事停工令】：在新加坡境内开展任何永久工程或关键临时结构工程施工，总承包商与合格人员（QP）必须事先取得建设局（BCA）签发的开工许可证（Permit to Carry Out Structural Works）；未经许可擅自施工的，构成刑事犯罪，主管官员直接签发法定停工令（Stop-Work Order），并处最高 20 万新元罚款及 2 年监禁！【出海攻防启示】：澄清工期延误归责的铁证！海外业主常因商业规划拖延施工图报审，却催促承包商强行进场；中资总包必须严守 BCA 许可底线，未获 Permit 绝不违规作业，并依据此项公法强行限制向业主主张法定工期顺延！",
        "norm_category": "construction_regulatory",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_sg_bca8_structural_works", "text_zh": "要件一：施工作业属于新加坡建筑控制法管辖的主体结构工程或深基坑支护工程", "status": "condition_precedent"},
            {"eid": "e_sg_bca8_formal_permit", "text_zh": "要件二：通过合资格专业人员（Qualified Person, QP）向建设局正式取得书面开工批文", "status": "mandatory"},
            {"eid": "e_sg_bca8_stop_work_penalty", "text_zh": "法律后果：确立施工合法性；无证施工强制关停现场，且延误工期不可归责于承包商", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "SG:UCTA_Cap_396:Sec2_3",
        "law": "SG:UCTA_Cap_396",
        "enbez": "Sec 2-3",
        "title": "新加坡不公平合同条款法第2-3条：过失免责绝对无效与免责条款合理性测试(Reasonableness)",
        "heading_path": "新加坡不公平合同条款法 (Unfair Contract Terms Act Cap 396) > 责任免除限制 > 人身伤亡与违约合理性测试",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Negligence liability and contractual liability: A person cannot by reference to any contract term exclude or restrict his liability for death or personal injury resulting from negligence. In the case of other loss or damage, a person cannot exclude or restrict his liability for negligence except in so far as the term satisfies the requirement of reasonableness.",
        "text_en": "Liability for death/personal injury from negligence cannot be excluded; other liability exclusion clauses in standard business terms must satisfy the statutory Reasonableness Test.",
        "text_zh": "【免除过失伤亡责任绝对无效与格式免责合理性测试】：在新加坡法律下，任何合同条款企图免除或限制因疏忽/过失导致的人身伤亡责任的，该条款自始绝对无效；对于免除其他财产损失或违约损害的条款，以及基于标准商业格式合同拟定的限制责任条款，必须通过法院的‘合理性测试（Requirement of Reasonableness）’方为有效！【出海攻防启示】：审查 EPC 责任限制条款的法律标尺！业主在格式合同中企图完全排除自身交付图纸迟延过错、或强行要求承包商承担无限连带赔偿的条款，中资企业在诉讼仲裁中可直接依据 UCTA 判定其未通过合理性测试而归于无效，彻底击碎业主的单方霸王免责防线！",
        "norm_category": "contract_interpretation",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_sg_ucta2_standard_terms", "text_zh": "要件一：条款属于发包人单方拟定并提供的一揽子标准格式免责或责任限制条款", "status": "condition_precedent"},
            {"eid": "e_sg_ucta2_reasonableness_test", "text_zh": "要件二：审查当事人缔约时谈判地位是否对等、是否有替代选择以及是否明知风险分配合理性", "status": "mandatory"},
            {"eid": "e_sg_ucta2_clause_invalidity", "text_zh": "法律后果：未满足合理性标准之免责条款依法不产生法律拘束力，按普通法确定完全损害赔偿", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "SG:IRDA_2018:Sec440",
        "law": "SG:IRDA_2018",
        "enbez": "Sec 440",
        "title": "新加坡破产重组与解散法第440条：限制Ipso Facto破产终止条款与施工合同强行维系",
        "heading_path": "新加坡破产、重组与解散法 (Insolvency, Restructuring and Dissolution Act 2018) > 重组保护 > 第440条 限制合同破产解除条款",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Restriction on ipso facto clauses: No provision in any agreement has any effect to the extent that it allows a person to terminate or modify, or claim an accelerated payment under, any agreement with a company, by reason only that the company is insolvent or that proceedings for compromise or arrangement are commenced.",
        "text_en": "Ipso facto clauses permitting contract termination solely by reason of insolvency, judicial management, or scheme of arrangement proceedings are unenforceable.",
        "text_zh": "【限制Ipso Facto破产终止条款与工程合同保护】：任何合同条款，若其赋予一方‘仅仅因为相对方陷入资不抵债、或相对方申请司法管理（Judicial Management）或债务重组安排（Scheme of Arrangement）即可单方解除合同或加速到期’的权利，该条款依法不具有法律效力！【出海攻防启示】：业主财务危机时的退场攻防红线！当中资承包商获悉新加坡业主申请破产重整时，切忌‘仅仅以业主启动债务重组’为由擅自停工解约（否则将构成非法毁约反遭索赔）；必须以‘业主存在实际拖欠到期工程款违约且催告逾期’为实体法违约事由行使解约权，确保退场合法性！",
        "norm_category": "bankruptcy_restructuring",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_sg_irda440_restructuring_filing", "text_zh": "要件一：相对方当事人已正式向新加坡高等法院递交司法管理或债务重组方案申请", "status": "condition_precedent"},
            {"eid": "e_sg_irda440_sole_ground_insolvency", "text_zh": "要件二：解约通知所依据的唯一抗辩事实仅为相对方进入破产保护程序本身", "status": "mandatory"},
            {"eid": "e_sg_irda440_termination_stayed", "text_zh": "法律后果：单方破产解约条款被强行阻断失效，合同关系依法维系直至发生实体违约", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "SG:SOPA_2004:Sec9_15",
        "law": "SG:SOPA_2004",
        "enbez": "Sec 9-15",
        "title": "新加坡SOPA快速裁决法第9-15条：付款索赔送达时限与业主未答辩扣款抗辩失权",
        "heading_path": "新加坡建筑与施工行业付款安全法 (SOPA Cap 30B) > 付款索赔与答辩 > 逾期未答辩失权机制",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Payment claims and payment responses: A respondent who fails to provide a payment response within the prescribed period (21 days) shall not be entitled to dispute the payment claim on any grounds, and shall not raise any reasons for withholding payment in the subsequent adjudication.",
        "text_en": "Respondent failing to serve a timely Payment Response within statutory period (21 days) is strictly precluded from disputing payment claim or raising withholding defenses in SOPA adjudication.",
        "text_zh": "【SOPA付款答辩逾期失权与裁决闪电追款】：承包商依法向业主或总包送达付款索赔（Payment Claim）后，付款人必须在法定 21 天期限内送达正式书面付款答辩（Payment Response）；若付款人逾期未提供付款答辩，法律强制剥夺其在后续快速裁决程序中提出任何扣款、抵销或异议抗辩的事由（Preclusion Rule），裁决员必须直接裁令全额支付索赔金额！【出海攻防启示】：新加坡工程款追索的核动力武器！中资分包商若遭遇总包拖延，应严格按照 SOPA 格式正式送达 Payment Claim；一旦总包疏忽未在 21 天内正式书面答辩，其在法律上彻底丧失反索赔抗辩权，中资企业可在 60 天内取得具备终局执行力的新加坡高院判决令强行划款！",
        "norm_category": "construction_dispute",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_sg_sopa9_valid_claim_service", "text_zh": "要件一：承包商已在合同约定的估价基准日严格遵照 SOPA 格式向相对方送达付款索赔书", "status": "condition_precedent"},
            {"eid": "e_sg_sopa15_expired_no_response", "text_zh": "要件二：付款人未在法定 21 个日历天期限内出具并送达合规的付款答辩书（Payment Response）", "status": "mandatory"},
            {"eid": "e_sg_sopa15_preclusion_rule", "text_zh": "法律后果：裁决员依法直接裁决支持全额索赔，付款人彻底丧失提出工程质量或误期反诉抗辩权", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "SG:ETA_Cap_88:Sec8_11",
        "law": "SG:ETA_Cap_88",
        "enbez": "Sec 8-11",
        "title": "新加坡电子交易法第8-11条：电子工程指令与电子签名法律有效性",
        "heading_path": "新加坡电子交易法 (Electronic Transactions Act Cap 88) > 电子记录与签名 > 电子合同与指令拘束力",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Legal recognition of electronic records and signatures: A record or signature shall not be denied legal effect, validity or enforceability solely on the ground that it is in the form of an electronic record. Electronic communications of variation orders or notices satisfy writing requirements.",
        "text_en": "Electronic records, emails, digital approvals, and electronic signatures possess full legal validity, satisfying statutory writing requirements for contract variations and engineering notices.",
        "text_zh": "【电子通信、项目邮件与电子签名法定完全效力】：任何工程指令、变更协议、索赔通知或批准文件，不得仅因其采用电子形式（如项目管理平台协同记录、往来电子邮件、电子签名 DocuSign）而被否定其法律效力与可执行性；电子文件完全满足普通法关于‘书面形式（In Writing）’的法定要件！【出海攻防启示】：电子证据闭环护身符！海外现代工程普遍采用 Aconex 或 Procore 等数字化协同系统，监理工程师通过邮件或系统签发的工期指令具有不可推翻的合同拘束力；中资项目部应设立专人负责电子档案归档与时间戳固化，作为后续索赔与防阻抗辩的铁证！",
        "norm_category": "contract_formation",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_sg_eta8_electronic_record", "text_zh": "要件一：变更指示、会议纪要或工程预警以清晰可调取的电子邮件或项目协同系统电子记录形态存在", "status": "condition_precedent"},
            {"eid": "e_sg_eta8_identifiable_origin", "text_zh": "要件二：电子通信能够可靠地识别发件人身份并能证明其代表发包人或监理工程师履行职务", "status": "mandatory"},
            {"eid": "e_sg_eta8_statutory_writing", "text_zh": "法律后果：法律确认该电子文件完全具备书面证据效力，排除发包人‘缺少纸质原件签章’之无效抗辩", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "SG:Misrepresentation_Act_Cap_390:Sec2_3",
        "law": "SG:Misrepresentation_Act",
        "enbez": "Sec 2-3",
        "title": "新加坡虚假陈述法第2-3条：地勘数据误述撤销合同与损害赔偿及免责限制",
        "heading_path": "新加坡虚假陈述法 (Misrepresentation Act Cap 390) > 虚假陈述法律后果 > 撤销权与合理性免责限制",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Damages for misrepresentation: Where a person has entered into a contract after a misrepresentation has been made to him by another party, and as a result thereof he has suffered loss, then the other party shall be liable to damages notwithstanding that the misrepresentation was not made fraudulently, unless proving reasonable grounds of belief. Clauses excluding misrepresentation liability are subject to reasonableness test.",
        "text_en": "A party suffering loss due to non-fraudulent misrepresentation (e.g. erroneous site data) is entitled to damages and rescission; clauses excluding misrepresentation liability are void if unreasonable.",
        "text_zh": "【过失虚假陈述法定赔偿与地质免责条款无效抗辩】：当事人因相对方的过失虚假陈述（如业主提供了严重不实的地勘报告或现场地下管线图）而订立合同并遭受严重工期与费用损失的，即使该陈述不构成欺诈，陈述方仍负有赔偿全部损失之法定义务；合同中凡企图免除或限制虚假陈述法律责任的免责条款，必须通过严格的合理性测试，否则自始无效！【出海攻防启示】：突破银皮书地下风险包干的普通法重磅武器！即使合同约定‘承包商自行承担全部地下地质风险且雇主对地勘数据不承担真实性保证’，若能举证发包人提供勘察数据时存在重大过失误述，承包商依本法享有直接追索地质重大偏离额外加固成本之法定索赔权！",
        "norm_category": "breach_remedy",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_sg_misrep2_erroneous_data", "text_zh": "要件一：发包人在招标或签约阶段向承包商提供了存在严重偏差的工程地质水文基础事实陈述", "status": "condition_precedent"},
            {"eid": "e_sg_misrep2_reliance_loss", "text_zh": "要件二：承包商因合理信赖该等不实数据进行报价施工并因此遭受了严重的地质额外处置成本支出", "status": "mandatory"},
            {"eid": "e_sg_misrep2_statutory_damages", "text_zh": "法律后果：发包人依法承担侵权法同等标准之损害赔偿责任，合同中不合理的免责条款依法归于消灭", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "SG:CRTPA_Cap_53B:Sec2_3",
        "law": "SG:CRTPA_Cap_53B",
        "enbez": "Sec 2-3",
        "title": "新加坡合同第三人权利法第2-3条：直接执行权与融资方介入权Step-in规则",
        "heading_path": "新加坡合同（第三人权利）法 (Contracts Rights of Third Parties Act Cap 53B) > 第三人强制执行权 > 融资方介入权",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Right of third party to enforce contractual term: A third party may in his own right enforce a term of the contract if: (a) the contract expressly provides that he may, or (b) the term purports to confer a benefit on him, unless on a proper construction of the contract it appears that the parties did not intend the term to be enforceable by the third party.",
        "text_en": "Third parties may enforce contract terms if expressly provided or purporting to confer a benefit (e.g. project lenders' step-in rights), unless expressly excluded by parties.",
        "text_zh": "【第三人直接请求权与项目融资银团介入权】：非合同签署当事人的第三方，在合同明文赋予其权利或合同条款旨在赋予其利益时，依法享有以自身名义直接向承包商强制执行该合同条款的诉权；除非合同中明文约定排除《合同第三人权利法》的适用！【出海攻防启示】：EPC 总承包商与融资银团直接协议（Direct Agreement）的关键法理依据！中资承包商为海外大型独立发电商（IPP）实施工程时，银团常要求植入融资方介入权（Step-in Rights）；中资企业必须在主合同中严格约定排除 CRTPA 第三人诉权，确保唯有签署了三方直接协议的银团在特定违约且提供付款保证后方可介入，防范非特定第三方随意干预工程！",
        "norm_category": "contract_performance",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_sg_crtpa2_express_term", "text_zh": "要件一：合同条款中明文约定特定第三方享有权利或客观上旨在赋予该第三方实质利益", "status": "condition_precedent"},
            {"eid": "e_sg_crtpa2_no_exclusion_clause", "text_zh": "要件二：合同正文中未包含明确排除适用新加坡《合同第三人权利法》之特别保留条款", "status": "mandatory"},
            {"eid": "e_sg_crtpa2_third_party_standing", "text_zh": "法律后果：该合格第三方依法取得直接向违约当事人提起司法诉讼并主张履约救济之原告诉讼主体资格", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "SG:Civil_Law_Act_Cap_43:Sec12",
        "law": "SG:Civil_Law_Act_Cap_43",
        "enbez": "Sec 12",
        "title": "新加坡民法法典第12条：法院与仲裁庭裁定迟延付款利息之司法自由裁量权",
        "heading_path": "新加坡民法法典 (Civil Law Act Cap 43) > 诉讼程序 > 第12条 债务与损害赔偿利息裁量权",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Interest on debts and damages: In any proceedings tried in any court of record for the recovery of any debt or damages, the court may, if it thinks fit, order that there shall be included in the sum for which judgment is given interest at such rate as it thinks fit on the whole or any part of the debt or damages for the whole or any part of the period between the date when the cause of action arose and the date of the judgment.",
        "text_en": "Courts and arbitral tribunals possess statutory power to award pre-judgment and post-judgment interest at fair commercial rates (typically 5.33% per annum) on debts and damages.",
        "text_zh": "【法院及仲裁庭判决前与判决后利息法定裁决权】：在追索任何工程欠款或损害赔偿的司法审判与国际仲裁中，主审法庭享有完全的自由裁量权，裁定在判决总额中计入自诉因发生之日起至判决作出之日止的判决前利息（常规司法基准为年化 5.33%），以及自判决作出之日起直至实际全额清偿完毕之日的判决后执行利息！【出海攻防启示】：跨境争议解决资金成本全额补偿！新加坡法院与 SIAC 仲裁庭在处理工程进度款拖欠争议时，几乎 100% 支持胜诉方依据 Sec 12 计取自付款期届满之日起算的法定利息，中资企业起诉业主时必须将利息请求列为独立大额索赔项！",
        "norm_category": "breach_remedy",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_sg_cla12_debt_established", "text_zh": "要件一：主审法庭经实体审理认定发包人存在到期未付工程进度款或违约赔偿债务事实", "status": "condition_precedent"},
            {"eid": "e_sg_cla12_interest_claim_made", "text_zh": "要件二：原告或申请人在答辩期内正式提出了加计判决前后法定利息的正式主张", "status": "mandatory"},
            {"eid": "e_sg_cla12_interest_award", "text_zh": "法律后果：法庭依法裁决按年化 5.33% 计付自违约当日起算的利息，彻底弥补拖欠期间利息损失", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "SG:Companies_Act_Cap_50:Sec131",
        "law": "SG:Companies_Act_Cap_50",
        "enbez": "Sec 131",
        "title": "新加坡公司法第131条：公司财产质押与浮动抵押30天ACRA登记强制对抗要件",
        "heading_path": "新加坡公司法 (Companies Act Cap 50) > 担保与抵押登记 > 质押登记除斥期与无效后果",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Registration of charges: Every charge created by a company to secure any debenture, book debts (receivables), or floating charge on undertaking, must be lodged with ACRA within 30 days after creation. Any charge not so registered shall be void against the liquidator and any creditor of the company.",
        "text_en": "Company charges over book debts (construction receivables) or floating charges must be registered with ACRA within 30 days of creation, or become void against liquidator and creditors.",
        "text_zh": "【应收工程款质押与浮动抵押30日ACRA强制登记要件】：新加坡注册公司就其应收账款（工程进度款债权）、不动产或以浮动抵押（Floating Charge）方式设立担保的，必须在担保契约订立后 30 天内向会计与企业管制局（ACRA）办理电子抵押登记；逾期未登记者，该担保物权在法律上直接归于消灭，对清算人（Liquidator）及其他一切债权人绝对无效！【出海攻防启示】：中资银行海外工程银团放款合规生命线！中资承包商为境内母公司银团贷款在新加坡 SPV 设立‘工程应收账款质押’时，项目法务必须在放款前严格完成 ACRA 30天除斥期登记并取得抵押设立证明，防止因未登记导致数亿美元担保在业主破产时沦为毫无优先权的普通信用贷款！",
        "norm_category": "property_security",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_sg_ca131_charge_creation", "text_zh": "要件一：公司为担保自身或关联方债务正式签署了应收工程款质押或资产浮动抵押契约", "status": "condition_precedent"},
            {"eid": "e_sg_ca131_30days_acra_lodgment", "text_zh": "要件二：自担保契约签署生效当日起严格 30 个日历天内向 ACRA 系统提交登记备案并完税", "status": "mandatory"},
            {"eid": "e_sg_ca131_perfection_or_void", "text_zh": "法律后果：取得对世优先受偿效力对抗清算人；未按期登记者担保物权自始无效，退化为普通无担保债权", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "SG:SOPA_2004:Sec23_26",
        "law": "SG:SOPA_2004",
        "enbez": "Sec 23-26",
        "title": "新加坡SOPA快速裁决法第23-26条：裁决生效未获付款工程材料留置权与直接代付",
        "heading_path": "新加坡建筑与施工行业付款安全法 (SOPA Cap 30B) > 裁决强制执行 > 未安装材料留置权与直接付款",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Enforcement of adjudicated amount: Where an adjudicated amount is not paid, the claimant may serve a notice of intention to suspend works, exercise a lien over unfixed materials and goods supplied by the claimant, or obtain an order for direct payment from principal.",
        "text_en": "Claimant with unpaid adjudication determination may exercise statutory lien over unfixed goods supplied on site, suspend works with full cost compensation, or seek direct payment from principal.",
        "text_zh": "【快速裁决未付款救济未安装工程材料留置与直接代付】：快速裁决生效后被裁决人逾期未付款的，胜诉申请人依法享有三大强制救济手段：① 提前 7 天通知后合法暂停施工作业，且工期自动顺延并索赔停工窝工合理成本！② 对其运至现场但尚未安装固定的设备材料行使法定留置权（Lien on Unfixed Goods），留置期间相对方严禁转移设备！③ 申请高院命令由直接发包人从尚未结清的总包款项中向申请人直接划转代付！【出海攻防启示】：中资分包商对付无赖总包的终极绝招！分包商运至现场的数千万高端机电设备，一旦总包拒不支付进度款，中资企业直接依 Sec 25 发函行使法定留置权，封存设备并向业主申请直付，在工程最要害节点卡死总包咽喉！",
        "norm_category": "construction_dispute",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_sg_sopa23_adjudicated_unpaid", "text_zh": "要件一：已取得具法律执行力的 SOPA 正式裁决书且相对方逾期未履行支付义务", "status": "condition_precedent"},
            {"eid": "e_sg_sopa25_unfixed_goods_on_site", "text_zh": "要件二：申请人制造供货且尚未实质性浇筑或焊接入永久工程的独立材料设备尚处于现场占有状态", "status": "mandatory"},
            {"eid": "e_sg_sopa25_statutory_lien", "text_zh": "法律后果：确立排他性法定留置权阻断他人查封，并享有依法向法院申请变卖留置物优先受偿权", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },

    # ==========================================
    # 5. 泰国 (asean_th) - 10 条 L1 强行法
    # ==========================================
    {
        "table": "norms",
        "norm_id": "TH:CCC:Sec383",
        "law": "TH:CCC",
        "enbez": "Sec 383",
        "title": "泰国民商法典第383条：法院与仲裁庭依职权自由裁量酌减过高违约金",
        "heading_path": "泰国民商法典 (Civil and Commercial Code) > 债编 > 违约金条款与司法酌减权",
        "language_mode": "bilingual",
        "lang_original": "th",
        "text_original": "ถ้าเบี้ยปรับที่ริบนั้นสูงเกินส่วน ศาลจะลดลงเป็นจำนวนพอสมควรก็ได้ ในการที่จะวินิจฉัยว่าสมควรเพียงใดนั้น ท่านให้พิเคราะห์ถึงทางได้เสียของเจ้าหนี้ทุกอย่างอันชอบด้วยกฎหมาย ไม่ใช่แต่เพียงทางได้เสียในเชิงทรัพย์สิน",
        "text_en": "If forfeited penalty/liquidated damages is disproportionately high, the court may reduce it to a reasonable amount, considering all legitimate interests of creditor, not merely economic loss.",
        "text_zh": "【法院与仲裁庭依职权自由裁量酌减过高违约金】：如果合同约定的违约金数额极度过高、与债权人因违约遭受的实际损失及合法权益相比显失公平不成比例的，法院或仲裁庭享有依自由心证将其酌情削减至合理数额的绝对法定权力！当事人预先在合同中约定‘放弃请求法院酌减违约金权利’的条款自始绝对无效！【出海攻防启示】：泰国建设工程对抗业主误期违约金（Delay Damages）索赔的最核心实体法王牌！泰国业主常约定每日合同总价 0.1%、甚至按日累计扣留高达 20%~30% 的巨额逾期罚款；在司法或仲裁审理中，中资总包只需证明业主实际遭受的发电收益或租金损失远低于违约金，泰国大理院判例（Dika Judgment）通常依 Sec 383 直接砍掉 50%~70% 的违约金扣减！",
        "norm_category": "breach_remedy",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_th383_disproportionate_penalty", "text_zh": "要件一：合同约定的违约赔偿金额严重脱离定作人因迟延交付实际遭受的真实经济损失", "status": "condition_precedent"},
            {"eid": "e_th383_judicial_examination", "text_zh": "要件二：审查主审法庭综合考量当事人过错程度、行业通常惯例及债权人一切合法商业利益", "status": "mandatory"},
            {"eid": "e_th383_judicial_reduction", "text_zh": "法律后果：法院或仲裁庭强制判决按合理比例大幅削减违约金，阻断发包人超额不当得利扣罚", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "TH:CCC:Sec600_607",
        "law": "TH:CCC",
        "enbez": "Sec 600-607",
        "title": "泰国民商法典第600-607条：承揽工程瑕疵担保责任与发现后1年短期消灭时效",
        "heading_path": "泰国民商法典 (Civil and Commercial Code) > 承揽编 (Hire of Work) > 工程瑕疵担保责任与时效",
        "language_mode": "bilingual",
        "lang_original": "th",
        "text_original": "ผู้รับจ้างต้องรับผิดเพื่อความชำรุดบกพร่องอันปรากฏขึ้นภายในหนึ่งปีนับแต่วันส่งมอบงาน หรือภายในห้าปีถ้าเป็นการก่อสร้างสิ่งปลูกสร้างบนแผ่นดิน แต่ความรับผิดนั้นย่อมระงับไปเมื่อพ้นกำหนดหนึ่งปีนับแต่วันที่ความชำรุดบกพร่องได้ปรากฏขึ้น",
        "text_en": "Contractor is liable for defects appearing within 1 year of handover (5 years for land structures); action must be commenced strictly within 1 year of defect appearance.",
        "text_zh": "【承揽工程瑕疵担保期限与发现缺陷后1年除斥期】：承揽人对工程移交之日起 1 年内出现的瑕疵负担保责任（若系附着于土地的砖石结构大型建筑工程，担保期限为 5 年）；但无论何种情形，发包人主张权利的诉讼必须在‘发现瑕疵之日起严格 1 年内’向法院提起，逾期未起诉的，发包人的瑕疵修补与损害赔偿请求权终局归于消灭！【出海攻防启示】：阻断泰国业主长尾暗病索赔的绝杀防线！工程质保期满移交后，发包人若在日常运维中发现裂缝渗漏等缺陷，往往拖延数年直至整体翻修才向承包商大额索赔；中资项目部只要举证证明业主在 1 年之前已向我方发过维修邮件知悉缺陷，即可依据 Sec 601 主张 1 年除斥期间届满，全额驳回业主数千万泰铢的索赔！",
        "norm_category": "construction_regulatory",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_th600_handover_structure", "text_zh": "要件一：工程已正式完成竣工移交，属于附着于土地之土建基础设施或工业厂房结构物", "status": "condition_precedent"},
            {"eid": "e_th601_defect_appearance_1yr", "text_zh": "要件二：发包人在缺陷显现知晓之日起超过整 1 年未向主管审判机关提起正式法律诉讼", "status": "mandatory"},
            {"eid": "e_th601_claim_extinguished", "text_zh": "法律后果：发包人的质量索赔请求权终局消灭，承包商依法享有完全免于赔偿与修补之诉讼抗辩权", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "TH:FBA_1999:Sec36",
        "law": "TH:FBA_1999",
        "enbez": "Sec 36",
        "title": "泰国外商经营法第36条：严打泰籍名义代持规避外资准入之刑事监禁与强制解散罚则",
        "heading_path": "泰国外商经营法 (Foreign Business Act B.E. 2542) > 罚则 > 第36条 名义代持刑事制裁与强制解散",
        "language_mode": "bilingual",
        "lang_original": "th",
        "text_original": "คนสัญชาติไทยที่ให้ความช่วยเหลือหรือสนับสนุนหรือร่วมประกอบธุรกิจของคนต่างด้าวโดยมิได้รับอนุญาต หรือถือหุ้นแทนคนต่างด้าว (Nominee) เพื่อให้คนต่างด้าวประกอบธุรกิจโดยหลีกเลี่ยงกฎหมาย ต้องระวางโทษจำคุกไม่เกิน 3 ปี หรือปรับตั้งแต่ 100,000 บาท ถึง 1,000,000 บาท และให้ศาลสั่งเลิกกิจการ",
        "text_en": "Thai nationals holding shares as nominees for foreigners to evade FBA restrictions face up to 3 years imprisonment, fines up to THB 1 million, and mandatory court-ordered corporate dissolution.",
        "text_zh": "【外商经营法反代持刑事重锤与法院强制解散公司】：任何泰国籍公民或法人，协助、支持外国人在未获许可证情形下经营受限业务，或作为名义股东（Nominee）代外国人持有股份以规避外资持股 49% 上限管辖的，处 3 年以下有期徒刑及 10 万至 100 万泰铢刑事罚金；主审法院依法直接判令解散该公司并吊销全部商业执照！【出海攻防启示】：彻底击碎中资在泰通过‘51% 泰籍代持人 + 49% 中资’空壳公司拿总包牌照的违法幻想！在泰国承揽常规工程受 FBA 附表三第 10 项严苛限制，一旦被商业发展厅（DBD）穿透审查或被当地竞争对手举报，中资投入的注册资本金与机械设备将面临司法查封，管理人员面临跨国刑事追责！必须合规申请投资促进委员会（BOI）100% 独资证书或走大额 5 亿泰铢实缴资本豁免通道！",
        "norm_category": "foreign_investment",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_th_fba36_nominee_structure", "text_zh": "要件一：外资投资者通过抽屉代持协议或表决权委托安排由泰籍名义人实质持有公司 51% 以上控制性股权", "status": "condition_precedent"},
            {"eid": "e_th_fba36_evasion_intent", "text_zh": "要件二：该代持架构之客观目的旨在实质规避《外商经营法》附表三关于禁止外资控股施工服务业之限制", "status": "mandatory"},
            {"eid": "e_th_fba36_criminal_dissolution", "text_zh": "法律后果：代持协议自始绝对无效，涉案人员承担 3 年监禁刑事责任，法院强制下令解散公司并清算资产", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "TH:Land_Code:Sec86_96",
        "law": "TH:Land_Code",
        "enbez": "Sec 86-96",
        "title": "泰国土地法典第86-96条：外资永久土地产权严格禁止与BOI投资促进工业用地特批例外",
        "heading_path": "泰国土地法典 (Land Code B.E. 2497) > 第八章 外国人土地权利 > 外资持有土地禁令与BOI特批",
        "language_mode": "bilingual",
        "lang_original": "th",
        "text_original": "คนต่างด้าวจะได้มาซึ่งที่ดินก็โดยอาศัยบทแห่งสนธิสัญญาซึ่งให้มีกรรมสิทธิ์ในอสังหาริมทรัพย์ได้. ผู้ประกอบธุรกิจที่ได้รับการส่งเสริมการลงทุน (BOI) ได้รับอนุญาตให้ถือกรรมสิทธิ์ในที่ดินสำหรับใช้ประกอบกิจการตามที่คณะกรรมการกำหนดได้ แม้จะเกินกำหนดที่กฎหมายอื่นบัญญัติไว้",
        "text_en": "Foreigners are strictly prohibited from owning land in Thailand, except under international treaties or where granted special statutory permission by Board of Investment (BOI) for approved projects.",
        "text_zh": "【外资持有土地永久产权强制禁令与BOI特批例外】：外国人及外资持股超过 49% 的泰国注册法人，严禁在泰国境内受让或持有任何土地的永久所有权（Freehold）；违规购地的，内政部有权责令在 1 年内强制变卖出让，逾期未卖收归国有！唯一法定的重大例外是：根据《投资促进法》取得投资促进委员会（BOI）投资促进证书的企业，依法特批享有持有项目合理所需工业用地的所有权！【出海攻防启示】：中资海外工业园区与重资产制造基地投资的核心土地路径！中资央企赴泰投资大型光伏电池、汽车零配件及装备制造基地，切忌通过非法名义代持买地；必须在投前以独资申请 BOI 投资优惠，依法取得内政部与 BOI 联合批准的合法永久土地产权证（Chanote），享有 100% 坚固的土地资产产权保障！",
        "norm_category": "property_security",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_th_land86_foreign_entity", "text_zh": "要件一：主体属于外国自然人、外国公司或外资持股比例达到 50% 以上之泰国注册法人实体", "status": "condition_precedent"},
            {"eid": "e_th_land96_boi_promotion_cert", "text_zh": "要件二：正式取得泰国投资促进委员会（BOI）签发的重大制造业或高科技基础设施投资促进核准证书", "status": "mandatory"},
            {"eid": "e_th_land96_ownership_exemption", "text_zh": "法律后果：依法特许受让并持有项目工业用地土地所有权地契（Chanote）；未获特批买地者强制没收变卖", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "TH:Labor_Protection_BE_2541:Sec118",
        "law": "TH:Labor_Protection_BE_2541",
        "enbez": "Sec 118",
        "title": "泰国劳动保护法第118条：工程竣工解雇遣散费法定阶梯补偿标准与免责例外",
        "heading_path": "泰国劳动保护法 (Labor Protection Act B.E. 2541) > 劳动合同终止 > 第118条 法定遣散补偿金标准",
        "language_mode": "bilingual",
        "lang_original": "th",
        "text_original": "นายจ้างต้องจ่ายค่าชดเชยให้แก่ลูกจ้างซึ่งเลิกจ้าง ตามระยะเวลาการทำงาน: ทำงานครบ 120 วันแต่ไม่ครบ 1 ปี ได้รับค่าชดเชย 30 วัน; ทำงานครบ 20 ปีขึ้นไป ได้รับค่าชดเชย 400 วัน. ข้อยกเว้น: การจ้างงานที่มีกำหนดระยะเวลาแน่นอนสำหรับงานโครงการก่อสร้างที่ต้องทำงานให้แล้วเสร็จภายใน 2 ปี",
        "text_en": "Employers terminating employees must pay severance pay ranging from 30 days to 400 days wages based on seniority; fixed-term contracts for construction projects completing within 2 years are exempt.",
        "text_zh": "【施工用工遣散费阶梯补偿与2年期确定性工程合同免责例外】：用人单位解除劳动合同必须依法支付阶梯遣散补偿金（工龄满 120 天补偿 30 天工资，满 20 年最高补偿 400 天工资）；但法律设立了工程行业特别豁免例外：若用人单位在招募本土建筑工人时，订立了期限明确且预期工程在 2 年内竣工完成的‘确定期限项目劳动合同（Fixed-term Project Contract）’，工程完工解约时用人单位依法全额免于支付遣散补偿金！【出海攻防启示】：削减数百万泰铢用工遣散成本的合同设计玄机！中资建筑企业招录泰国当地劳工时，绝不可采用无固定期限常规格式合同（否则竣工退场将面临天价劳资维权罢工）；必须严格按照 Sec 118 款项要求，在用工第一天签署注明‘本项目为 2 年内完工的特定工程节点合同’，确保工完人退、零遣散费平稳收尾！",
        "norm_category": "labor_compliance",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_th_lpa118_fixed_term_contract", "text_zh": "要件一：劳资双方在入职时订立了书面劳动协议且明确约定为特定单项工程建设服务之固定期限", "status": "condition_precedent"},
            {"eid": "e_th_lpa118_within_2years_completion", "text_zh": "要件二：工程规划施工周期在客观技术上能在自签约当日起严格 2 年内竣工交付完毕", "status": "mandatory"},
            {"eid": "e_th_lpa118_severance_exemption", "text_zh": "法律后果：工程完工自然终止用工时依法全额免除支付第 118 条法定遣散补偿金（Severance Pay）", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "TH:CCC:Sec222_223",
        "law": "TH:CCC",
        "enbez": "Sec 222-223",
        "title": "泰国民商法典第222-223条：违约通常损害与特别损害可预见性及与有过失相抵",
        "heading_path": "泰国民商法典 (Civil and Commercial Code) > 债编 > 违约赔偿范围与过失相抵",
        "language_mode": "bilingual",
        "lang_original": "th",
        "text_original": "การเรียกร้องค่าเสียหายย่อมครอบคลุมถึงความเสียหายตามปกติอันเกิดจากการไม่ชำระหนี้ และความเสียหายอันเกิดแต่พฤติการณ์พิเศษ หากคู่กรณีฝ่ายที่ต้องรับผิดได้คาดเห็นหรือควรจะได้คาดเห็นพฤติการณ์นั้น. ถ้าความเสียหายเกิดขึ้นเพราะความผิดของฝ่ายผู้เสียหายร่วมด้วย (Contributory Negligence) ศาลย่อมมีอำนาจลดหย่อนค่าเสียหาย",
        "text_en": "Damages cover ordinary losses and foreseeable special damages; where creditor's fault contributed to damage (Contributory Negligence), court reduces damages accordingly.",
        "text_zh": "【通常损害与特别损害可预见性及与有过失相抵】：违约损害赔偿仅涵盖债务不履行通常发生的直接损害；对于由特殊情况引起的间接或特别损害，唯有在违约方于缔约时预见到或应当预见到该特殊情况时方负赔偿责任；若损害的发生或扩大因债权人自身的过失所促成（与有过失 Contributory Negligence），法院依法强制扣减或免除违约方的赔偿数额！【出海攻防启示】：普通法 Hadley v Baxendale 规则在泰国的成文法对应！业主起诉承包商主张巨额连带商业损失时，中资法务两步拆解：第一步，援引 Sec 222 剔除一切缔约时无法预见的间接营业利润损失；第二步，举证证明业主本身存在审批迟延等与有过失，依法强制按过错比例打折，大幅化解赔偿敞口！",
        "norm_category": "breach_remedy",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_th222_special_damages_foreseeability", "text_zh": "要件一：定作人所主张的间接营业利润损失在双方签署合同时是否属于承包商能够合理预见之范畴", "status": "condition_precedent"},
            {"eid": "e_th223_employer_contributory_fault", "text_zh": "要件二：发包人在工程实施过程中是否存在迟延签发指令、设计交底错误等促成延误损害之过错行为", "status": "mandatory"},
            {"eid": "e_th223_apportionment_reduction", "text_zh": "法律后果：法庭依法行使过错相抵裁量权，按发包人自身过错比例直接同等抵扣核减承包商赔偿责任", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "TH:CCC:Sec224_2021",
        "law": "TH:CCC",
        "enbez": "Sec 224",
        "title": "泰国民商法典第224条：2021年紧急法令修订后金钱债务迟延法定年利率5%计算标准",
        "heading_path": "泰国民商法典 (Civil and Commercial Code as amended by Emergency Decree B.E. 2564) > 金钱之债迟延利息",
        "language_mode": "bilingual",
        "lang_original": "th",
        "text_original": "หนี้เงินนั้น ให้คิดดอกเบี้ยในระหว่างผิดนัดในอัตราที่กำหนดตามมาตรา 7 (ร้อยละ 3 ต่อปี) บวกด้วยอัตราเพิ่มร้อยละ 2 ต่อปี (รวมเป็นร้อยละ 5 ต่อปี) เว้นแต่เจ้าหนี้จะชอบที่จะเรียกร้องดอกเบี้ยได้สูงกว่านั้นโดยอาศัยเหตุอย่างอื่นอันชอบด้วยกฎหมาย",
        "text_en": "Monetary debts in default bear statutory interest at the base rate under Section 7 (3% per annum) plus 2% default surcharge, totaling 5% per annum, amended by 2021 Emergency Decree.",
        "text_zh": "【金钱债务逾期法定年利率5%与严禁复利新规】：依据泰国 2021 年第 2564 号紧急法令重大修法，金钱债务迟延履行的法定违约利息被彻底压低重塑：基准利率为每年 3%，加上迟延履行附加利息 2%，法定迟延年利率统一固定为 5%！且法律严格禁止对违约迟延利息计取利滚利复利（Compound Interest）！【出海攻防启示】：重大涉泰工程审理利息计算标准！过去泰国判例常机械适用 7.5% 旧利率，中资承包商在应对业主反索赔时，必须指出旧利率已被 2021 新法废止，强制锁定按 5% 计息；而在主张自身工程款欠款时，若合同未约定更高利率，同样严格按 5% 计算，防范因提出过高利息主张被仲裁庭认定为恶意索赔而驳回部分仲裁费！",
        "norm_category": "breach_remedy",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_th224_default_monetary_obligation", "text_zh": "要件一：发包人逾期未支付经双方核定或裁决确认的工程款或垫资利息之金钱债务", "status": "condition_precedent"},
            {"eid": "e_th224_2021_amended_rate", "text_zh": "要件二：未在合同中设立更高的合法商业约定利率且违约期间发生于 2021 年新法施行后", "status": "mandatory"},
            {"eid": "e_th224_statutory_5pct_rate", "text_zh": "法律后果：强制适用年化 5% 单利标准裁决利息，严厉排除一切利滚利复利与 7.5% 历史旧法利率", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "TH:CCC:Sec369",
        "law": "TH:CCC",
        "enbez": "Sec 369",
        "title": "泰国民商法典第369条：双务合同同时履行抗辩权与定作人未付款前承包商停工权",
        "heading_path": "泰国民商法典 (Civil and Commercial Code) > 合同履行 > 双务合同同时履行抗辩权",
        "language_mode": "bilingual",
        "lang_original": "th",
        "text_original": "คู่สัญญาฝ่ายหนึ่งจะไม่ยอมชำระหนี้จนกว่าอีกฝ่ายหนึ่งจะชำระหนี้ หรือขอปฏิบัติการชำระหนี้ก็ได้ แต่ความข้อนี้ท่านมิให้ใช้บังคับ ถ้าหนี้ของอีกฝ่ายหนึ่งนั้นยังไม่ถึงกำหนด",
        "text_en": "A party to a bilateral contract may refuse to perform its obligation until the other party performs or tenders performance of its reciprocal obligation, unless the other party's obligation is not yet due.",
        "text_zh": "【双务合同同时履行抗辩权与未获付款合法拒绝施工】：双务合同的一方当事人，在相对方未履行其对待给付义务或未提出对待给付之前，依法有权拒绝履行自身的合同债务（同时履行抗辩权 Exceptio Non Adimpleti Contractus）；但在相对方对待给付债务尚未届清偿期时，不适用本条。【出海攻防启示】：中资总包在泰对抗业主拖欠工程款的盾牌！当发包人逾期拒不支付到期工程进度款时，总承包商援引 Sec 369 发出正式通知并暂停现场施工，阻断业主以‘工期严重迟延’为由单方解除合同并索兑履约保函！",
        "norm_category": "contract_performance",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_th369_bilateral_contract", "text_zh": "要件一：双方受合法有效之建设工程施工或设备安装双务承揽合同拘束", "status": "condition_precedent"},
            {"eid": "e_th369_reciprocal_due_debt", "text_zh": "要件二：定作人所负有的对应期中进度款或进场开工预付款已届清偿期且未实际全额支付", "status": "mandatory"},
            {"eid": "e_th369_lawful_refusal", "text_zh": "法律后果：承包商合法行使拒绝继续作业抗辩权，工期自动依法顺延且不构成任何违约迟延责任", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "TH:CCC:Sec590_591",
        "law": "TH:CCC",
        "enbez": "Sec 590-591",
        "title": "泰国民商法典第590-591条：定作人提供材料瑕疵或不当指令致工程缺陷承包商免责",
        "heading_path": "泰国民商法典 (Civil and Commercial Code) > 承揽编 (Hire of Work) > 定作人原因致瑕疵免责",
        "language_mode": "bilingual",
        "lang_original": "th",
        "text_original": "ถ้าความชำรุดบกพร่องหรือความชักช้าในการที่ทำนั้นเกิดขึ้นเพราะสภาพแห่งสัมภาระซึ่งผู้ว่าจ้างส่งให้ก็ดี หรือเกิดขึ้นเพราะคำสั่งซึ่งผู้ว่าจ้างสั่งให้ทำก็ดี ผู้รับจ้างไม่ต้องรับผิด เว้นแต่ผู้รับจ้างรู้อยู่แล้วว่าสัมภาระนั้นไม่เหมาะหรือคำสั่งนั้นไม่สมควรและมิได้บอกกล่าวเตือน",
        "text_en": "Contractor is not liable for defect or delay caused by materials supplied by employer or by employer's instructions, unless contractor knew of defect/impropriety and failed to warn employer.",
        "text_zh": "【发包人材料缺陷或错误指令致工程瑕疵免责及通知异议要件】：如果工程出现的缺陷瑕疵或工期延误，系由于发包人自行提供的建筑材料设备性质缺陷所致，或系由于发包人签发的错误工程技术指令所致，承包商依法完全免除违约赔偿责任！但存在重大除外规定：若承包商明知该材料设备不适用或明知发包人指令不合理，却未及时书面告知并警告发包人的，承包商仍须承担违约责任！【出海攻防启示】：中资施工企业现场技术沟通第一铁律！业主常指定本地材料商供货或现场强令变更混凝土配比；中资技术团队一旦察觉其材料达不到标号或指令存在安全隐患，必须在 24 小时内发出正式书面警告函（Notice of Defect/Warning），方能牢牢锁定 Sec 591 法律免责金牌！",
        "norm_category": "construction_regulatory",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_th590_employer_cause", "text_zh": "要件一：工程瑕疵或裂缝直接因发包人采购甲供材料不达标或监理工程师错误技术图纸指令所致", "status": "condition_precedent"},
            {"eid": "e_th591_written_warning_served", "text_zh": "要件二：承包商在知晓或应当知晓该材料/指令不当后已及时向发包人签发正式书面书面预警函件", "status": "mandatory"},
            {"eid": "e_th591_liability_exemption", "text_zh": "法律后果：承包商法定免于承担瑕疵返工修补费用与损害赔偿责任，发包人自负全部技术风险后果", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "TH:Arbitration_Act_2545:Sec40",
        "law": "TH:Arbitration_Act_2545",
        "enbez": "Sec 40",
        "title": "泰国2002年仲裁法第40条：法院撤销仲裁裁决法定排他性事由与公共秩序实质审查",
        "heading_path": "泰国仲裁法 (Arbitration Act B.E. 2545) > 仲裁裁决司法审查 > 第40条 撤销裁决法定事由",
        "language_mode": "bilingual",
        "lang_original": "th",
        "text_original": "การเพิกถอนคำชี้ขาด: ศาลมีอำนาจเพิกถอนคำชี้ขาดได้เฉพาะเมื่อผู้ร้องพิสูจน์ได้ว่า: สัญญาอนุญาโตตุลาการไม่สมบูรณ์, ไม่ได้รับคำบอกกล่าวการแต่งตั้ง, คำชี้ขาดเกินขอบเขต, หรือศาลเห็นว่าข้อพิพาทนั้นไม่อาจระงับโดยอนุญาโตตุลาการได้หรือขัดต่อความสงบเรียบร้อยหรือศีลธรรมอันดีของประชาชน (Public Policy). คำร้องต้องยื่นภายใน 90 วัน",
        "text_en": "Courts may set aside arbitral awards exclusively on limited grounds (invalid agreement, lack of notice, excess of jurisdiction) or where award violates Public Policy; petition within 90 days.",
        "text_zh": "【撤销仲裁裁决排他性事由与公共秩序审查及90天除斥期】：泰国法院唯有在申请人举证证明存在仲裁协议无效、未获指定通知未能申辩、裁决超裁等法定情形，或法院依职权认定裁决涉及不可仲裁事项、或执行裁决‘违背泰国公共秩序或公共道德（Public Policy）’时，方有权判决撤销仲裁裁决；撤销申请必须在收到裁决书之日起严格 90 天内提出！【出海攻防启示】：在泰涉外仲裁司法审查的最高风险源！泰国法院对涉及国家重大特许经营、公路交通等公共基础设施案件，常以‘违背公共秩序’为由实质介入推翻仲裁裁决（如著名的 Hopewell 特许权案）；中资企业在泰订立仲裁协议时，应极力争取选择中立仲裁地（如新加坡 SIAC 或吉隆坡 AIAC），避开泰国属地司法撤裁干预！",
        "norm_category": "crossborder_litigation",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_th_arb40_timely_petition_90d", "text_zh": "要件一：撤销仲裁裁决申请必须自申请人收到正式仲裁裁决书之日起严格 90 个日历天内提出", "status": "condition_precedent"},
            {"eid": "e_th_arb40_public_policy_test", "text_zh": "要件二：审查裁决事项是否涉及行政特许权主权垄断或其实体结果严重践踏泰国核心国家公共利益", "status": "mandatory"},
            {"eid": "e_th_arb40_exclusive_grounds", "text_zh": "法律后果：恪守法定排他事由审理；除违背公共秩序或正当程序瑕疵外，法院严禁对裁决进行实体改判", "status": "prohibition"}
        ], ensure_ascii=False)
    }
]


PHASE10_L1_NORMS_BATCH4 = [
    # ==========================================
    # 5. 菲律宾 (asean_ph) - 10 条 L1 强行法
    # ==========================================
    {
        "table": "norms",
        "norm_id": "PH:Civil_Code:Art1723",
        "law": "PH:Civil_Code",
        "enbez": "Art 1723",
        "title": "菲律宾民法典第1723条：工程师与总承包商15年建筑物坍塌隐蔽瑕疵法定连带侵权责任",
        "heading_path": "菲律宾民法典 (Republic Act No. 386) > 第四编 承揽合同 (Contract for a Piece of Work) > 第1723条 结构坍塌15年连带责任",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "The engineer or architect who drew up the plans and specifications for a building is liable for damages if within fifteen years from the completion of the structure, the same should collapse by reason of a defect in those plans and specifications, or due to the defects in the ground. The contractor is likewise responsible for damages if the edifice falls, within the same period, on account of defects in the construction or the use of materials of inferior quality furnished by him, or due to any violation of the terms of the contract. If the engineer or architect supervises the construction, he shall be solidarily liable with the contractor. Acceptance of the building does not imply waiver of the cause of action.",
        "text_en": "Engineer/architect and contractor are solidarily liable for 15 years from completion if building collapses due to defective plans, construction defects, or inferior materials; acceptance does not waive action.",
        "text_zh": "【15年工程倒塌连带法定侵权保证责任与隐蔽瑕疵追索】：菲律宾民法典第1723条确立了全球建筑领域最严苛的法定保修期之一：自建筑物竣工之日起 15 年内，若建筑物因设计规范缺陷、地基基础缺陷发生倒塌坍塌，设计工程师须承担损害赔偿责任；若倒塌系因施工缺陷、使用了劣质材料或违反合同约定所致，总承包商同样须承担赔偿责任；若工程师负责现场监理施工，工程师与承包商依法承担无过错连带责任（Solidarily Liable）！即使业主已签署完工验收证书（TOC），亦绝不构成对该侵权赔偿请求权的放弃！受损业主在倒塌发生之日起享有长达 10 年诉讼时效！【出海攻防启示】：中资央企出海在菲建设高层楼宇、大型桥梁等公建项目，合同约定的通常 1~2 年缺陷责任期（DLP）绝不能免除民法典第1723条规定的 15 年法定连带保证责任！中资企业在竣工交工时必须完成详尽的地质勘察报告归档、隐蔽工程监理终验会签与永久性技术沉降监测记录，并在再分包合同中强制背靠背转嫁 15 年连带责任与不可撤销质量保函！",
        "norm_category": "construction_regulatory",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_ph1723_collapse_within_15y", "text_zh": "要件一：建筑物或工程结构在自交工之日起严格 15 年法定周期内发生倒塌或严重结构性破损", "status": "condition_precedent"},
            {"eid": "e_ph1723_defect_causation", "text_zh": "要件二：倒塌直接系由于设计图纸缺陷、地质未妥善处理、施工工艺瑕疵或使用劣质材料所导致", "status": "mandatory"},
            {"eid": "e_ph1723_solidary_liability", "text_zh": "法律后果：承包商与设计监理工程师承担法定无过错连带损害赔偿责任，发包人签收工程不免除责任", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "PH:Civil_Code:Art1169",
        "law": "PH:Civil_Code",
        "enbez": "Art 1169",
        "title": "菲律宾民法典第1169条：债务人履行迟延法定通知催告要件与催告免除法定例外",
        "heading_path": "菲律宾民法典 (Civil Code of the Philippines) > 债与合同 > 履行迟延 (Delay / Mora)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Those obliged to deliver or to do something incur in delay from the time the obligee judicially or extrajudicially demands from them the fulfillment of their obligation. However, the demand by the creditor shall not be necessary in order that delay may exist: (1) When the obligation or the law expressly so declares; or (2) When from the nature and the circumstances of the obligation it appears that the designation of the time when the thing is to be delivered or the service is to be rendered was a controlling motive for the establishment of the contract; or (3) When demand would be useless, as when the obligor has rendered it beyond his power to perform.",
        "text_en": "Obligor incurs in delay only from judicial or extrajudicial demand by obligee, unless contract/law expressly dispenses with demand, time is of the essence, or demand would be useless.",
        "text_zh": "【债务人迟延Mora Solvendi前置催告通知原则与工期索赔】：在菲律宾民法体系中，单纯到达合同约定的完工截止日期并不当然构成法律意义上的履行迟延（Legal Delay / Mora）；债权人（业主）必须依法向债务人发出正式的司法诉讼（Judicial）或庭外书面催告（Extrajudicial Demand），债务人方自收到催告之时起正式陷于迟延！但在合同或法律明确声明无需催告、时间为合同实质关键要素（Time is of the essence）或催告已属徒劳的情形下除外。【出海攻防启示】：中资承包商工期抗辩之盾！若菲方业主在原定工期届满后并未立即签发正式的违约迟延催告函（Formal Extrajudicial Demand），而仅作非正式口头或邮件催问，则承包商在法律上尚未构成法定迟延；中资企业可利用此法条时间窗口迅速提交工期顺延（EOT）与现场阻碍索赔报告，阻断业主直接扣除误期违约金（Liquidated Damages）！",
        "norm_category": "breach_remedy",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_ph1169_due_obligation", "text_zh": "要件一：合同约定的工程完工或节点交工义务履行期限已经届满", "status": "condition_precedent"},
            {"eid": "e_ph1169_formal_demand_served", "text_zh": "要件二：权利人已向债务人发出正式司法诉讼或庭外书面催告履约通知且被有效送达", "status": "mandatory"},
            {"eid": "e_ph1169_legal_mora_effect", "text_zh": "法律后果：债务人自送达之日起正式构成法律迟延，债权人方享有违约损害赔偿与没收违约金之请求权", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "PH:Civil_Code:Art1229",
        "law": "PH:Civil_Code",
        "enbez": "Art 1229",
        "title": "菲律宾民法典第1229条：司法裁判衡减过高或显失公平违约金惩罚条款强制裁量权",
        "heading_path": "菲律宾民法典 (Civil Code of the Philippines) > 违约罚则条款 (Obligations with a Penal Clause) > 司法衡减违约金",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "The judge shall equitably reduce the penalty when the principal obligation has been partly or irregularly complied with by the debtor. Even if there has been no performance, the penalty may also be reduced by the courts if it is iniquitous or unconscionable.",
        "text_en": "The judge shall equitably reduce the penalty when obligation is partly/irregularly complied with, or where penalty is iniquitous or unconscionable even without performance.",
        "text_zh": "【司法衡减违约金与排除惩罚性赔偿强制法理】：当债务人已部分履行或不完全履行主要债务时，主审法官或仲裁庭应当依法依职权公平衡减合同约定的违约金（Liquidated Damages / Penalty）；即使债务人完全尚未开始履行，若约定的违约金数额畸高、显失公平或具有恶意压榨惩罚性质（Iniquitous or Unconscionable），法院同样有权强制予以核减！【出海攻防启示】：中资承包商对抗业主高额误期罚款的核心利器！FIDIC 合同往往约定每日千分之一或累计高达合同总额 10%~15% 的 LD。在项目已实质竣工投入部分使用，或业主自身存在部分延误指令时，中资企业可坚决援引 Art 1229 请求 CIAC 仲裁庭或菲律宾法院按已完工工程比例大幅核减误期违约金，打破‘照章全额扣罚’的霸王条款！",
        "norm_category": "breach_remedy",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_ph1229_partial_performance", "text_zh": "要件一：承包商已完成主体工程施工并由发包人实际接收投入部分商业运营使用", "status": "condition_precedent"},
            {"eid": "e_ph1229_iniquitous_penalty", "text_zh": "要件二：原合同约定的全额违约罚则数额明显超过发包人实际因工期延误所蒙受的经济损失", "status": "mandatory"},
            {"eid": "e_ph1229_equitable_mitigation", "text_zh": "法律后果：法庭或仲裁庭依据公平正义原则强制同比例削减违约金数额，排他性保护债务人", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "PH:Civil_Code:Art1267",
        "law": "PH:Civil_Code",
        "enbez": "Art 1267",
        "title": "菲律宾民法典第1267条：履行极度困难情势变更原则与债务免除履约调整",
        "heading_path": "菲律宾民法典 (Civil Code of the Philippines) > 债之消灭 > 履行极度困难 (Difficulty of Performance)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "When the service has become so difficult as to be manifestly beyond the contemplation of the parties, the obligor may also be released therefrom, in whole or in part.",
        "text_en": "When service has become so difficult as to be manifestly beyond contemplation of parties, the obligor may be released therefrom, in whole or in part.",
        "text_zh": "【履行极度困难情势变更原则与免除债务或变更合同】：当合同约定的作为劳务义务或工程施工变得极其困难，且该困难明显完全超出了当事人在订立合同时的合理预见范畴时，履行义务人（承包商）有权依法请求完全免除或部分免除履行义务，并促成合同按公平原则重新调整！【出海攻防启示】：菲律宾合同法吸收大陆法‘情势变更’（Rebus Sic Stantibus）的重要法定条款！遭遇超级台风、地缘冲突物资海运禁运、或属地重大环保法律突发突变导致施工成本暴涨数倍时，若继续机械履行将导致中资承包商陷入灭顶之灾，中资企业应依 Art 1267 发函声明义务显失公平，主张调整工期与造价或免除履约责任，有效抗辩业主的违约终止指控！",
        "norm_category": "contract_performance",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_ph1267_extreme_difficulty", "text_zh": "要件一：履约过程中因不可抗力或外部客观宏观情势剧变导致施工成本与难度暴增", "status": "condition_precedent"},
            {"eid": "e_ph1267_beyond_contemplation", "text_zh": "要件二：该重大情势剧变在双方订立合同时完全不属于理性商业人士所能预见的风险范畴", "status": "mandatory"},
            {"eid": "e_ph1267_release_or_adjustment", "text_zh": "法律后果：法庭有权部分或全部免除承包商未完工履约义务，或强制双方重新平抑结算价款", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "PH:Civil_Code:Art1724",
        "law": "PH:Civil_Code",
        "enbez": "Art 1724",
        "title": "菲律宾民法典第1724条：承揽工程增资变更价款必须具备书面授权与金额确认要件",
        "heading_path": "菲律宾民法典 (Civil Code of the Philippines) > 承揽合同 > 第1724条 工程变更书面形式与调价门槛",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "The contractor who undertakes to build a structure or any other work for a stipulated price, in conformity with plans and specifications agreed upon with the land-owner, can neither withdraw from the contract nor demand an increase in the price on account of the higher cost of labor or materials, save when there has been a change in the plans and specifications, provided: (1) Such change has been authorized by the proprietor in writing; and (2) The additional price to be paid to the contractor has been agreed upon in writing by both parties.",
        "text_en": "Contractor under stipulated price cannot claim price increase due to labor/materials cost rise, save upon change in plans provided: (1) authorized in writing by employer; and (2) additional price agreed upon in writing.",
        "text_zh": "【工程变更调价双重书面要件法定强制门槛】：以约定固定总价承揽工程的承包商，既不得单方退出合同，亦不得以人工或材料成本上涨为由要求增加价款；唯有在图纸规范发生变更时方可请求调价，但必须严格同时满足两大双重书面要件：（1）该工程变更已由业主以书面形式正式授权；并且（2）双方已就该变更应向承包商追加支付的价款数额达成书面协议！【出海攻防启示】：菲律宾出海施工索赔最高风险警示线！工程现场常有菲方项目代表或工程师口头指令变更施工，中资现场团队若未按 Art 1724 取得业主有权代表的书面签字并就变更金额锁定书面协议，无论实际施工花费多大，菲律宾最高法院（SC）历来判例一律认定承包商无权主张变更工程款！严守‘先签书面单价，再行动工变更’铁律！",
        "norm_category": "construction_regulatory",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_ph1724_written_authorization", "text_zh": "要件一：发包人或其授权代表出具了明确要求修改原设计图纸规范之正式书面变更指令", "status": "condition_precedent"},
            {"eid": "e_ph1724_written_price_agreement", "text_zh": "要件二：承包商与发包人在实施变更工程前已就追加之调价款项数额达成明确书面协议", "status": "mandatory"},
            {"eid": "e_ph1724_statutory_claim_bar", "text_zh": "法律后果：欠缺任一书面要件的，承包商法定调价请求权被排他性驳回，自负增量工程施工成本", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "PH:Civil_Code:Art1409",
        "law": "PH:Civil_Code",
        "enbez": "Art 1409",
        "title": "菲律宾民法典第1409条：违反强行法与公共政策合同自始绝对无效且不得追认追索",
        "heading_path": "菲律宾民法典 (Civil Code of the Philippines) > 无效合同 (Defective Contracts) > 第1409条 自始无效合同",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "The following contracts are inexistent and void from the beginning: (1) Those whose cause, object or purpose is contrary to law, morals, good customs, public order or public policy; (2) Those which are absolutely simulated or fictitious; (3) Those whose cause or object did not exist at the time of the transaction; (4) Those whose object is outside the commerce of men; (5) Those which contemplate an impossible service; (6) Those where the intention of the parties relative to the principal object cannot be ascertained; (7) Those expressly prohibited or declared void by law. These contracts cannot be ratified. Neither can the right to set up the defense of illegality be waived.",
        "text_en": "Contracts whose cause/object is contrary to law, morals, public policy, or simulated, or prohibited by law are inexistent and void from the beginning, cannot be ratified, and illegality defense cannot be waived.",
        "text_zh": "【绝对无效合同法定排他范畴与不可追认放弃原则】：具有以下情形的合同自始绝对不存在且无效（Void Ab Initio）：（1）其原因、客体或目的违反法律、公序良俗或公共政策；（2）完全虚假伪造或恶意串通假唱的合同；（7）法律明文禁止或宣布无效的合同！此类自始无效合同绝不能通过事后追认使其合法化，当事人亦绝无权事先或事后放弃违法无效的抗辩权！【出海攻防启示】：菲律宾外资并购与重组底线法律保障！凡是通过阴阳合同规避菲律宾宪法或反挂名法（Anti-Dummy Law）的外资控股协议、或无资质出借借牌挂靠合同，一律落入 Art 1409 绝对无效深渊，中资企业投入的资金无法作为合同债权追偿，务必从股权架构根源确保合规！",
        "norm_category": "corporate_governance",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_ph1409_contrary_to_law", "text_zh": "要件一：合同原因、标的或履行目的直接抵触菲律宾宪法外资比例红线、强行法或公共政策", "status": "condition_precedent"},
            {"eid": "e_ph1409_void_ab_initio", "text_zh": "要件二：协议在法律上自始属于虚假拟制或完全欠缺合法合同成立之有效民事客体", "status": "mandatory"},
            {"eid": "e_ph1409_unratifiable_legal_effect", "text_zh": "法律后果：合同确认为自始绝对无效，任何一方均不得主张缔约追认，且违法抗辩权永不消灭", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "PH:RA_11659_PSA_2022:Sec2_4",
        "law": "PH:RA_11659_PSA_2022",
        "enbez": "Sec 2-4",
        "title": "菲律宾2022年公共服务法修正案第2-4条：公用事业界定与电信运输外资100%控股开放",
        "heading_path": "菲律宾共和国法案第11659号 (RA 11659 amending Public Service Act) > 公用事业界定与外资准入",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Public Service Act Amendment (RA 11659): Sec 2-4 reclassifies 'Public Utility' strictly to: (1) distribution of electricity; (2) transmission of electricity; (3) petroleum pipeline transmission; (4) water pipeline distribution and wastewater systems; (5) seaports; (6) public utility vehicles. All other public services not classified as public utilities (including telecommunications, railways, expressways, shipping, airports) are fully open to 100% foreign equity ownership, abolishing the 40% foreign ceiling.",
        "text_en": "RA 11659 narrows 'Public Utility' to 6 key sectors; telecom, railways, shipping, expressways and airports are opened to 100% foreign ownership, repealing the historical 40% cap.",
        "text_zh": "【公用事业外资40%红线大幅收缩与重大基础设施100%外资准入开放】：菲律宾 2022 年第 11659 号共和国法案（RA 11659）彻底重构了菲律宾投资法版图：将受宪法 40% 外资股权上限限制的‘公用事业（Public Utility）’严格收窄限定为输配电、水务管网、海港、客运车辆等 6 类；而将电信、民航、铁路、高速公路、新能源物流等非公用基础设施全面向外资开放 100% 独资控股！【出海攻防启示】：中资央企赴菲投建特许经营 BOT/PPP 项目的里程碑红利！中资企业在菲投资轨道交通、收费公路、通信基站等领域，无需再像过去那样被迫寻找菲籍代持人组建 60/40 合资公司，可合法合规设立 100% 中资控股项目公司（SPV），消除被本地代理人绑架侵吞股权的重大资产安全隐患！",
        "norm_category": "corporate_governance",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_ph_psa_sector_classification", "text_zh": "要件一：外商投资之目标行业属于电信、轨道交通、收费公路或物流基础设施非公用事业领域", "status": "condition_precedent"},
            {"eid": "e_ph_psa_reciprocity_requirement", "text_zh": "要件二：关键基础设施领域投资需满足外国投资者母国提供对等待遇审查合规标准", "status": "mandatory"},
            {"eid": "e_ph_psa_100pct_foreign_equity", "text_zh": "法律后果：外资依法享有设立 100% 独资子公司权利，彻底免受菲律宾宪法 40% 本土持股红线掣肘", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "PH:EO_1008_CIAC:Sec4",
        "law": "PH:EO_1008_CIAC",
        "enbez": "Sec 4",
        "title": "菲律宾第1008号行政令第4条：建筑业仲裁委员会CIAC法定专属与排除法院管辖权",
        "heading_path": "菲律宾第1008号行政令 (Executive Order No. 1008) > 建筑业仲裁委员会 > 第4条 原始专属管辖权",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "The Construction Industry Arbitration Commission (CIAC) shall have original and exclusive jurisdiction over disputes arising from, or in connection with, contracts entered into by parties involved in construction in the Philippines, whether the dispute arises before or after the completion of the contract, or after the abandonment or breach thereof. As long as the parties agree to submit to voluntary arbitration, CIAC jurisdiction is acquired to the exclusion of regular courts.",
        "text_en": "CIAC holds original and exclusive jurisdiction over Philippine construction disputes where parties agreed to voluntary arbitration, excluding regular courts.",
        "text_zh": "【菲律宾建筑业仲裁委员会CIAC法定专属管辖与自动排除普通法院】：菲律宾建筑业仲裁委员会（CIAC）对发生在菲律宾境内的所有涉建筑施工、安装承包合同争议享有原始且排他的专属管辖权！只要当事人在合同中存在任何提及将争议提交自愿仲裁的条款，菲律宾普通法院即彻底丧失初审管辖权，必须依职权立即将案件移送 CIAC 审理；即使仲裁条款约定由其他仲裁机构管辖，只要工程在菲，CIAC 亦依据最高法院判例享有排他管辖权！【出海攻防启示】：在菲建设工程争议解决最高优先级程序规则！中资承包商在菲遭遇工程款拖欠或保函纠纷，切勿浪费数年时间在菲律宾低效拖沓的普通地方法院（RTC）缠诉，直接向 CIAC 提请仲裁，其仲裁规则实行严格 6 个月内结案制度，是迅速冻结业主资产并取得执行裁决的最强法律武器！",
        "norm_category": "crossborder_litigation",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_ph_ciac_construction_nexus", "text_zh": "要件一：合同争议属于在菲律宾境内实施的建筑、安装、设计或工程承揽法律关系范畴", "status": "condition_precedent"},
            {"eid": "e_ph_ciac_arbitration_agreement", "text_zh": "要件二：承揽合同中包含自愿仲裁意向条款或双方书面达成了提交仲裁解决争议之合意", "status": "mandatory"},
            {"eid": "e_ph_ciac_exclusive_jurisdiction", "text_zh": "法律后果：CIAC 依法取得排他性专属管辖权，民事法院应当驳回起诉或裁定移送仲裁程序", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "PH:Labor_Code:Art106_109",
        "law": "PH:Labor_Code",
        "enbez": "Art 106-109",
        "title": "菲律宾劳工法典第106-109条：严禁违法劳务派遣与总承包商对分包工人连带清偿责任",
        "heading_path": "菲律宾劳工法典 (Labor Code of the Philippines, Presidential Decree No. 442) > 承包与转包用工 > 工资连带清偿与纯劳务派遣禁止",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Contractor or Subcontractor: In the event that contractor/subcontractor fails to pay wages of employees, employer shall be jointly and severally liable with contractor to such employees. 'Labor-only contracting' is prohibited where contractor lacks substantial capital or tools/equipment and workers perform activities directly related to principal business; contractor is deemed merely an agent of employer who becomes direct employer.",
        "text_en": "Labor-only contracting is strictly prohibited; principal employer is jointly and severally liable with subcontractor for wages and benefits of contracted workers.",
        "text_zh": "【严禁纯劳务中介派遣Labor-Only与总承包商工资法定连带清偿责任】：如果独立劳务提供方不具备与其劳务作业相称的实质性资本、工具设备或工作场所，且招募的劳工从事与发包人主营业务直接相关的核心工种，即构成法律严厉禁止的‘纯劳务派遣（Labor-only Contracting）’！其法律后果为：劳务提供方仅被视为发包人的雇佣代理人，发包人（中资总包）依法直接被穿透推定为所有工人的法定雇主，须与分包商向全体劳工承担无过错的连带工资清偿与社保福利兜底责任！【出海攻防启示】：中资承包商在菲现场劳务用工最大的合规雷区！严禁中资企业在菲从街头或非持牌劳务贩子处‘买人工’；必须严格核验劳务分包商的 DOLE 劳工部 DO-174 资质证书及其注册资本（实缴资本不低于 500 万比索），并在分包合同中设立专款专用工人工资保证金账户，杜绝因劳务头子卷款潜逃导致中资项目现场被菲劳工部查封停工！",
        "norm_category": "labor_employment",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_ph_labor_wage_nonpayment", "text_zh": "要件一：劳务分包商拖欠参与该总包工程施工现场工人的法定最低工资、加班费或法定福利", "status": "condition_precedent"},
            {"eid": "e_ph_labor_lack_substantial_capital", "text_zh": "要件二：劳务分包商缺乏独立注册资本或施工机械设备工具，构成纯劳务中介（Labor-Only）", "status": "mandatory"},
            {"eid": "e_ph_labor_joint_solidary_liability", "text_zh": "法律后果：总承包商依法承担无过错连带清偿责任，劳工有权直接申请查封总包工程结算账户", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "PH:RA_12009_GPRA_2024:Sec19",
        "law": "PH:RA_12009_GPRA_2024",
        "enbez": "Sec 19",
        "title": "菲律宾2024年新政府采办改革法第19条：公共工程绿色透明招标与外国承包商资质特别许可",
        "heading_path": "菲律宾2024年新政府采办改革法 (Republic Act No. 12009, 2024) > 采购模式与资格预审 > 第19条 外国承包商参标门槛",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "New Government Procurement Act (RA 12009, 2024): Sec 19 standardizes procurement modalities, promoting Fit-for-Purpose procurement and Value for Money. Foreign contractors may participate in public bidding for infrastructure projects involving international funding or bilateral government assistance, subject to obtaining a Special License from PCAB under RA 4566, and compliance with anti-corruption transparency and environmental integrity standards.",
        "text_en": "RA 12009 modernizes public procurement; foreign contractors may bid on foreign-assisted infrastructure projects provided they obtain PCAB Special License and meet anti-corruption criteria.",
        "text_zh": "【2024新政府采办改革法公共工程招标与外资持牌准入门槛】：菲律宾 2024 年颁布实施的全新《政府采办改革法》（RA 12009）对公共基础设施项目招标制度进行全面革新：确立‘按用途定制（Fit-for-Purpose）’采购模式与生命周期成本评估标准；对于国际多边金融机构贷款（如世行、亚投行 AIIB）或双边政府援助的重大公共工程，明确允许外国承包商依法参与竞标，但前提是必须取得菲律宾承包商认可委员会（PCAB）核发的特别许可证（Special License），并严格遵守反腐败信息透明与环境保护硬性指标！【出海攻防启示】：中资企业竞标菲国主权公共工程的最新法律准绳！RA 12009 加大了对围标、串标及提供虚假履历业绩的刑事与行政连带处罚；中资央企在参与菲大型桥梁、港口等政府标段前，必须提前 3 个月在 PCAB 办理完成针对该特定标段的 Special License 批文，杜绝‘中标后因缺执照被菲廉政公署（Ombudsman）追责废标’！",
        "norm_category": "construction_regulatory",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_ph_gpra_foreign_assisted_project", "text_zh": "要件一：公共基础设施工程属于外国政府贷款、双边援助或多边开发银行资助之标段", "status": "condition_precedent"},
            {"eid": "e_ph_gpra_pcab_special_license", "text_zh": "要件二：外国总承包商已按 RA 4566 法定程序取得 PCAB 颁发之有效项目特别许可证", "status": "mandatory"},
            {"eid": "e_ph_gpra_valid_bidding_capacity", "text_zh": "法律后果：取得合法参标与缔约资格，排他性阻断以国籍为由的恶意流标与资格撤销投诉", "status": "legal_consequence"}
        ], ensure_ascii=False)
    }
]

PHASE10_L1_NORMS_BATCH5 = [
    # ==========================================
    # 6. 中国出海监管母法 (china_outbound) - 5 条 L1 强行法
    # ==========================================
    {
        "table": "norms",
        "norm_id": "CN:SPC_Foreign_Law_Ascertainment_2023:Art1_3",
        "law": "CN:SPC_Foreign_Law_Ascertainment_2023",
        "enbez": "Art 1-3",
        "title": "最高人民法院关于涉外民商事案件域外法查明若干规定第1-3条：当事人查明责任与法院穷尽合理途径协助义务",
        "heading_path": "最高人民法院司法解释 > 涉外民商事审判 > 域外法查明若干规定 (法释〔2023〕12号) > 第1-3条 查明责任与途径",
        "language_mode": "original_only",
        "lang_original": "zh",
        "text_original": "《最高人民法院关于涉外民商事案件适用国际条约和国际惯例若干问题的解释》及域外法查明规定：当事人协议选择适用域外法的，应当由当事人提供该域外法律内容并证明其真实有效性；当事人在合理期限内无正当理由未提供，或者各方当事人虽尽合理努力仍无法查明的，人民法院应当通过涉外法律专家库、最高法域外法查明机构、司法协助等法定合理途径协助查明；只有在穷尽合理途径仍无法查明时，方可依法适用中华人民共和国法律裁决案件。",
        "text_en": "PRC Supreme People's Court Rules on Foreign Law Ascertainment: Parties choosing foreign law must provide foreign law contents; court shall assist through expert repositories; PRC law applies only after exhausting all reasonable ascertainment channels.",
        "text_zh": "【最高法域外法查明司法解释当事人举证责任与法院协助职责】：2024年1月1日施行的《最高人民法院关于涉外民商事案件适用国际条约和国际惯例若干问题的解释》及域外法查明规定明确：当事人协议选择适用域外法的，应当由当事人提供该域外法律内容并证明其真实有效性；当事人在合理期限内无正当理由未提供，或者各方当事人虽尽合理努力仍无法查明的，人民法院应当通过涉外法律专家库、最高法域外法查明机构、司法协助等法定合理途径协助查明；只有在穷尽合理途径仍无法查明时，方可依法适用中华人民共和国法律裁决案件！【出海攻防启示】：出海央企涉诉涉仲司法查明基石规范！央企在境外涉诉或在国内涉外庭审理涉东盟合同纠纷时，当事人负有第一位的域外法律查明与翻译公证责任。通过‘东盟域外法查明助手’输出包含 elements_json 结构化要素、官方原文及权威判例先例的系统性查明报告，能够直接满足中国法院涉外庭或国际仲裁院对域外法专业证据的审查标准，有效防止因查明不力被法院强行转而适用内国法而丧失属地合同利益！",
        "norm_category": "crossborder_litigation",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_cn_ascertainment_party_choice", "text_zh": "要件一：当事人在涉外民商事合同中依法协议选择东盟国家实体法作为合同准据法", "status": "condition_precedent"},
            {"eid": "e_cn_ascertainment_proof_burden", "text_zh": "要件二：主张适用域外法的一方当事人提交了经过认证或公信机构出具的域外成文法与判例法文本", "status": "mandatory"},
            {"eid": "e_cn_ascertainment_application_effect", "text_zh": "法律后果：人民法院依法依职权审查并准确适用该东盟域外实体法作为案件定案依据", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "CN:SASAC_Order_35:Art7_8",
        "law": "CN:SASAC_Order_35",
        "enbez": "Art 7-8",
        "title": "国务院国资委第35号令中央企业合规管理办法第7-8条：涉外投资重大决策法律合规审查法定前置与首席合规官签字一票否决",
        "heading_path": "国务院国有资产监督管理委员会令 (第35号) > 中央企业合规管理办法 > 第二章 合规管理职责 > 第7-8条 重大涉外决策法律审核",
        "language_mode": "original_only",
        "lang_original": "zh",
        "text_original": "国资委第35号令《中央企业合规管理办法》第7-8条：中央企业应当将涉外投资并购、境外重大工程承包、大额涉外担保及重大涉外合同谈判纳入法律合规审核必经程序；重大涉外经营决策事项未经合规审查，不得提交党委（党组）前置研究或董事会、总经理办公会审议决定；首席合规官出具的合规审查意见具有实质法定前置地位，合规审查不通过的，依法享有一票否决权。",
        "text_en": "SASAC Order 35 (Compliance Management Measures for Central SOEs): Mandatory legal and compliance review for outbound investments, EPC projects and guarantees; Chief Compliance Officer veto right.",
        "text_zh": "【中央企业涉外投资重大决策法律合规审核法定前置与一票否决权】：国资委第35号令严格规定：中央企业应当将涉外投资并购、境外重大工程承包、大额涉外担保及重大涉外合同谈判纳入法律合规审核必经程序；重大涉外经营决策事项未经合规审查，不得提交党委（党组）前置研究或董事会、总经理办公会审议决定；首席合规官出具的合规审查意见具有实质法定前置地位，合规审查不通过的，依法享有一票否决权！【出海攻防启示】：央企出海风控第一道红线！中资央企各二级、三级海外子公司签署东盟重大 EPC 合同或进行合资股权交割前，必须形成包含域外法尽职调查、制裁审查、外汇合规、税务穿透的系统性合规评估备忘录；无合法合规意见书擅自海外签约交割者，将直接触发国资委重大违规经营投资责任追究与终身追责！",
        "norm_category": "corporate_governance",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_cn_sasac_major_outbound_project", "text_zh": "要件一：境外项目涉及重大境外工程EPC合同签约、跨国股权收购或大额境外融资担保", "status": "condition_precedent"},
            {"eid": "e_cn_sasac_compliance_review_gateway", "text_zh": "要件二：企业法律合规部门与首席合规官已出具正式书面合规审查通过意见书", "status": "mandatory"},
            {"eid": "e_cn_sasac_decision_validity", "text_zh": "法律后果：具备上报党委会及董事会审议之合法前置资格，未经合规审查之海外决议自始违规无效", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "CN:NDRC_Order_11:Art13_15",
        "law": "CN:NDRC_Order_11",
        "enbez": "Art 13-15",
        "title": "国家发展改革委第11号令企业境外投资管理办法第13-15条：敏感类项目国家发改委核准与非敏感项目网上备案时限",
        "heading_path": "国家发展和改革委员会令 (第11号) > 企业境外投资管理办法 > 第二章 境外投资的核准和备案 > 第13-15条 敏感与非敏感项目监管",
        "language_mode": "original_only",
        "lang_original": "zh",
        "text_original": "国家发改委第11号令规定：投资主体开展涉及敏感国家和地区、涉及武器装备/跨境水资源利用/涉外新闻传媒等敏感行业的境外投资项目，必须经国家发改委报国务院或由国家发改委核准；其他非敏感类境外投资项目，中管央企直接投资或地方企业投资金额 3 亿美元及以上的，向国家发改委申请备案；投资金额 3 亿美元以下的，向省级发改委申请备案；在获得发改委核准文件或备案通知书前，投资主体不得实施实质性资金出境与项目签约交割。",
        "text_en": "NDRC Order 11 (Outbound Investment Management Measures): Mandatory NDRC approval for sensitive countries/industries; online filing for non-sensitive projects before closing.",
        "text_zh": "【境外投资项目敏感类核准与非敏感类大额备案前置程序】：发改委第11号令规定：投资主体开展涉及敏感国家和地区、涉及武器装备/跨境水资源利用/涉外新闻传媒等敏感行业的境外投资项目，必须经国家发改委报国务院或由国家发改委核准；其他非敏感类境外投资项目，中管央企直接投资或地方企业投资金额 3 亿美元及以上的，向国家发改委申请备案；投资金额 3 亿美元以下的，向省级发改委申请备案；在获得发改委核准文件或备案通知书前，投资主体不得实施实质性资金出境与项目签约交割！【出海攻防启示】：对外直接投资 ODI 监管合规源头！中资企业在东盟投建水电站（涉及跨境水资源属于敏感类）、矿山冶炼、高科技园区等项目，必须精准定性项目敏感属性并提前 3~6 个月锁定发改委备案核准凭证，在境外商务谈判中必须设置以‘中国发改、商务、外汇部门前置审批完成’作为合同先决条件（Conditions Precedent），防范因国内批文未下被迫毁约承担巨额违约金！",
        "norm_category": "corporate_governance",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_cn_ndrc_sensitive_or_large_project", "text_zh": "要件一：中资境内主体在境外实施直接投资、并购或通过其控制的境外企业进行再投资", "status": "condition_precedent"},
            {"eid": "e_cn_ndrc_approval_or_filing_certificate", "text_zh": "要件二：依法取得国家发改委出具的项目核准批文或《境外投资项目备案通知书》", "status": "mandatory"},
            {"eid": "e_cn_ndrc_closing_authorization", "text_zh": "法律后果：取得外汇资金合法出境交割民事权利能力，未获批文不得进行任何实质资产转移", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "CN:SAFE_Notice_29:Art12_13",
        "law": "CN:SAFE_Notice_29",
        "enbez": "Art 12-13",
        "title": "国家外汇管理局汇发2014-29号文跨境担保外汇管理规定第12-13条：内保外贷外汇登记与担保履约境外资产清收合规",
        "heading_path": "国家外汇管理局规范性文件 (汇发〔2014〕29号) > 跨境担保外汇管理规定 > 第二章 内保外贷 > 第12-13条 登记与履约清收",
        "language_mode": "original_only",
        "lang_original": "zh",
        "text_original": "国家外汇管理局《跨境担保外汇管理规定》第12-13条：境内银行或非银行机构提供‘内保外贷’（境内提供担保、境外申请贷款）的，担保人必须在担保合同签订之日起 15 个工作日内向注册地外汇局办理跨境担保签约登记手续；当境外债务人发生违约导致担保履约时，境内担保人可凭外汇登记凭证直接在银行办理担保履约资金购付汇出境；担保履约后，担保人依法享有代位求偿权，并必须在规定期限内向境外债务人展开实质性资产追偿与资金调回。",
        "text_en": "SAFE Circular 29 (Cross-border Guarantee Foreign Exchange Regulations): Inbound guarantee for outbound loan (Neibaowaidai) requires SAFE registration within 15 days; debt recovery upon default.",
        "text_zh": "【内保外贷外汇登记与对外担保履约资金划转合规要件】：境内银行或非银行机构提供‘内保外贷’（境内提供担保、境外申请贷款）的，担保人必须在担保合同签订之日起 15 个工作日内向注册地外汇局办理跨境担保签约登记手续；当境外债务人发生违约导致担保履约时，境内担保人可凭外汇登记凭证直接在银行办理担保履约资金购付汇出境；担保履约后，担保人依法享有代位求偿权，并必须在规定期限内向境外债务人展开实质性资产追偿与资金调回！【出海攻防启示】：中资海外项目融资生命线！出海央企常采用‘母公司境内提供保函或质押、境外子公司在东盟当地开户银行放贷’的内保外贷模式；必须严格在 15 个工作日内完成外管局登记，严防因登记瑕疵导致保函索赔资金无法合法购汇出境引发跨境信誉危机与主权信用降级！",
        "norm_category": "foreign_exchange",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_cn_safe_guarantee_execution", "text_zh": "要件一：境内母公司或中资银行向境外债权人签署有效之涉外担保、备用信用证或独立保函", "status": "condition_precedent"},
            {"eid": "e_cn_safe_registration_15d", "text_zh": "要件二：自合同签订之日起严格 15 个工作日内在外管局资本项目信息系统完成内保外贷签约登记", "status": "mandatory"},
            {"eid": "e_cn_safe_lawful_remittance", "text_zh": "法律后果：开通银行购付汇履约通道，确保资金合法合规出境偿债并启动境外资产代位追偿", "status": "legal_consequence"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "CN:Anti_Foreign_Sanctions_Law:Art12_15",
        "law": "CN:Anti_Foreign_Sanctions_Law",
        "enbez": "Art 12-15",
        "title": "中华人民共和国反外国制裁法第12-15条：组织和个人不得执行歧视性限制措施与中资企业诉讼索赔阻断",
        "heading_path": "中华人民共和国法律 > 反外国制裁法 (主席令第90号) > 第12-15条 阻断措施与民事赔偿责任",
        "language_mode": "original_only",
        "lang_original": "zh",
        "text_original": "中华人民共和国反外国制裁法第12条明文规定：任何组织和个人均不得执行或者协助执行外国国家对我国公民、组织采取的歧视性限制措施；侵害我国公民、组织合法权益的，我国公民、组织依法可以向人民法院提起民事诉讼，要求其停止侵害、恢复名誉、消除影响、赔偿损失；有关部门可以依法对实施、协助执行歧视性措施的外国实体采取对等反制措施。",
        "text_en": "PRC Anti-Foreign Sanctions Law: Organizations/individuals prohibited from executing discriminatory restrictive foreign sanctions; Chinese parties entitled to sue for compensation in PRC courts.",
        "text_zh": "【反外国制裁法阻断长臂管辖与执行歧视性措施民事赔偿责任】：中华人民共和国反外国制裁法第12条明文规定：任何组织和个人均不得执行或者协助执行外国国家对我国公民、组织采取的歧视性限制措施；侵害我国公民、组织合法权益的，我国公民、组织依法可以向人民法院提起民事诉讼，要求其停止侵害、恢复名誉、消除影响、赔偿损失！【出海攻防启示】：出海央企对抗美欧二级制裁与长臂管辖的法律重器！在东盟多国大型基建与能源项目中，外资金融机构或西方分包商常以遵循第三方国制裁清单为由单方拒付款项、冻结资产或毁约停工；中资企业依法可向中国法院提起侵害民事权益诉讼，并保全该外资实体在华资产，以此为对等制衡筹码迫使外方回到谈判桌！",
        "norm_category": "corporate_governance",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_cn_sanctions_discriminatory_measure", "text_zh": "要件一：外国实体或其代理人在境内外依据外国不当制裁对中国央企实施冻结或歧视性违约", "status": "condition_precedent"},
            {"eid": "e_cn_sanctions_infringement_damages", "text_zh": "要件二：歧视性措施造成中资企业海外工程停工、货物滞港或资金冻结之实质财产损失", "status": "mandatory"},
            {"eid": "e_cn_sanctions_prc_court_remedy", "text_zh": "法律后果：中国法院享有管辖权并判决侵权方停止侵害并全额赔偿损失，可保全其在华财产", "status": "legal_consequence"}
        ], ensure_ascii=False)
    }
]

ALL_PHASE10_L1_NORMS = (
    PHASE10_L1_NORMS +
    PHASE10_L1_NORMS_BATCH2 +
    PHASE10_L1_NORMS_BATCH3 +
    PHASE10_L1_NORMS_BATCH4 +
    PHASE10_L1_NORMS_BATCH5
)
