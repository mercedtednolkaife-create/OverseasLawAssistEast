"""扩充 kb/asean 静态文件脚本:
- commentary.json: 60+ 条核心法条权威实务评注
- timepoints.yaml: 18+ 个东盟关键修法/生效时点与红黄预警规则
- glossary.csv: 120+ 组涉外工程法律三语专业术语字典
"""

import json
import yaml
import csv
import os

os.makedirs("kb/asean", exist_ok=True)

# 1. 扩充 commentary.json (60+ 核心法条深度评注)
commentary_data = {
    # 🇮🇩 印尼核心评注
    "ID:KUHPerdata:Art1243": {
        "title": "迟延违约损害赔偿请求权与法定催告前置",
        "jurisdiction": "asean_id",
        "core_doctrine": "债务人自收到书面催告令 (Somasi) 且在合理宽限期内仍未履约起，方正式构成迟延责任。未履行 Somasi 前置催告程序直接起诉或索赔，将被法院以诉请不成熟 (Premature Claim) 驳回。",
        "practical_tip": "工程款催收或违约追责时，必须由当地持牌律师发出正式双语 Somasi，设定至少 7~14 天合理履约期限并留存正式签收回执。"
    },
    "ID:KUHPerdata:Art1266": {
        "title": "双务合同法定解除必须通过法院判决原则",
        "jurisdiction": "asean_id",
        "core_doctrine": "双务合同一方违约时，守约方解除合同必须向地方法院提起诉讼并取得生效判决，方发生解约效力。商业实务中当事人可依 Art 1266(2) 明文约定放弃适用第 1266 条以实现单方通知解约。",
        "practical_tip": "在印尼 EPC 合同终止条款中，必须载明：'The Parties hereby expressly waive the provisions of Article 1266 and 1267 of the Indonesian Civil Code to the extent that court intervention is required to effectuate termination.'"
    },
    "ID:KUHPerdata:Art1320": {
        "title": "合同有效四大实质要件与瑕疵后果",
        "jurisdiction": "asean_id",
        "core_doctrine": "有效合同必备四大要件：① 缔约各方自由同意 (Kesepakatan)；② 具有完全民事行为能力 (Kecakapan)；③ 确定之标的 (Objek Tertentu)；④ 合法之原因 (Kausa yang Halal)。前两项为主观要件，缺失致合同可撤销；后两项为客观要件，缺失致合同自始绝对无效。",
        "practical_tip": "审查签约代表是否持有印尼公司章程授权或董事会决议，标的物是否规避印尼外资负面清单或强行法禁令。"
    },
    "ID:KUHPerdata:Art1328": {
        "title": "欺诈撤销权与故意伪造要件举证",
        "jurisdiction": "asean_id",
        "core_doctrine": "欺诈行为不能由法官推定，必须由主张方举证证明存在故意弄虚作假、隐瞒真相或伪造文件等积极诡计，导致受害方在受蒙蔽情况下签署合同。",
        "practical_tip": "在招投标或并购尽调阶段，若发现对方提供伪造的环保许可或财务报表，应固定书面证据并在 5 年撤销时效内向法院起诉撤销合同。"
    },
    "ID:KUHPerdata:Art1338": {
        "title": "契约即法律与客观诚实信用原则",
        "jurisdiction": "asean_id",
        "core_doctrine": "所有依法成立的协议对当事人而言具有法律效力 (Pacta Sunt Servanda)；且协议必须本着善意 (Itikad Baik / Good Faith) 履行。法官有权依据善意原则纠正显失公平的合同条款。",
        "practical_tip": "在面对业主恶意扣款或纯外文合同无效抗辩时，应重点援引 SEMA 3/2023 及 Art 1338 善意原则予以强力抗辩。"
    },
    "ID:KUHPerdata:Art1610": {
        "title": "固定总价工程未经业主书面同意禁止因涨价追加价款",
        "jurisdiction": "asean_id",
        "core_doctrine": "按固定总价方案承包建筑物建设的建筑师或承包商，不得以工人工资或建筑材料价格上涨为由，向定作人索赔增加建筑造价，除非该项工程增减系经定作人书面同意且书面商定价格。",
        "practical_tip": "若适用印尼法总价包干，合同中必须增设 FIDIC 13.7 款法律变更调差或 13.8 款物价通胀调差公式，明文排除 Art 1610 的适用限制。"
    },
    "ID:UU_2_2017:Art30": {
        "title": "外国建筑代表处 (BUJKA) 与本土企业组建 KSO 联营体强制令",
        "jurisdiction": "asean_id",
        "core_doctrine": "外国建筑服务企业在印尼承揽工程，必须设立 BUJKA 并在投标实施前与具备大级资质 (Kualifikasi Besar) 的 100% 纯内资印尼建筑企业组建 KSO 联合体，牵头方资质与技术转让比例受严格监管。",
        "practical_tip": "严禁挂靠借牌，KSO 联合体协议必须明确双方权责、资金账户联签机制与税务 PE 隔离方案。"
    },
    "ID:UU_2_2017:Art47": {
        "title": "建设工程工作合同法定必备 16 项条款与印尼语文本强制令",
        "jurisdiction": "asean_id",
        "core_doctrine": "印尼建设服务合同必须使用印尼语（可双语对照但必须含印尼语），且必须穷尽包含法定 16 项必备条款（包括建筑物失败责任、分包限制、替代争议阶梯等），违者合同面临行政整改与效力瑕疵。",
        "practical_tip": "在合同末尾明确约定以印尼语与英语同时签署，若两者存在冲突以英文为准（须结合 SEMA 3/2023 善意规避无效抗辩）。"
    },
    "ID:UU_2_2017:Art60": {
        "title": "建筑物倒塌失败 (Kegagalan Bangunan) 10 年法定质量安全责任",
        "jurisdiction": "asean_id",
        "core_doctrine": "自工程竣工最终移交之日起最长 10 年内，若发生建筑物倒塌或结构性破坏，承包商与设计院依法承担连带修复与全额损害赔偿责任，由独立注册评估专家评定过错责任。",
        "practical_tip": "移交前必须取得独立工程师签署的移交证书与验收合格批文，并投保 10 年期工程潜在缺陷险 (IDI)。"
    },
    "ID:UU_25_2007:Art33": {
        "title": "严禁股权代持 (Nominee Arrangement) 绝对无效重锤",
        "jurisdiction": "asean_id",
        "core_doctrine": "印尼《投资法》第 33 条明文规定，严禁国内外投资者订立任何借用印尼自然人或企业名义代持公司股份的协议，代持协议自始绝对无效，投资款不受司法保护，法院一律驳回确权诉请。",
        "practical_tip": "切勿通过印尼当地律师或保姆签代持协议投资受限行业，应通过外商独资 PT PMA 或合法 KSO 联营体路径合规落地。"
    },
    "ID:UU_2_2012:Art42": {
        "title": "国家公共利益征地补偿款提存法院 (Konsinyasi) 强制清场机制",
        "jurisdiction": "asean_id",
        "core_doctrine": "在国家公共利益基础设施工程征地中，当个别土地权利人拒绝接受法定评估机构确定的补偿金额时，征地机构可将补偿款依法提存至地方法院 (Konsinyasi)，提存完毕后即产生合法占有效力，有权强制清场交地。",
        "practical_tip": "电站或铁路中资总包商在遭遇村民阻工时，应敦促业主依据 UU 2/2012 第 42 条向法院办理 Konsinyasi 手续，切勿私力武力强拆。"
    },
    "ID:PBI_17_3_2015:Art2": {
        "title": "印尼境内交易强制使用印尼盾与战略基建外币结算豁免",
        "jurisdiction": "asean_id",
        "core_doctrine": "在印尼境内的现金与非现金交易必须强制使用印尼盾计价与结算。但依据第 4 条与第 8 条，国际贸易进出口、离岸贷款及经财政部/能矿部特批的国家战略基建工程，可合法豁免使用美元结算。",
        "practical_tip": "对于战略电站或收费公路 EPC 合同，签约前必须取得能矿部或印尼央行出具的书面外币结算豁免批准函。"
    },

    # 🇻🇳 越南核心评注
    "VN:Civil_Code_2015:Art3": {
        "title": "越南民法基本原则与仲裁司法审查撤裁防线",
        "jurisdiction": "asean_vn",
        "core_doctrine": "确立民事法律关系主体平等、意思自治、诚实信用、自负其责与不违反国家利益和公共利益基本原则。越南法院在依据《民事诉讼法》第 439 条撤销或不予执行涉外仲裁裁决时，超 80% 援引违反 Art 3 基本原则为由。",
        "practical_tip": "起草涉越合同与仲裁抗辩时，必须防范程序剥夺抗辩，确保在越送达与听证程序 100% 严谨留痕。"
    },
    "VN:Civil_Code_2015:Art124": {
        "title": "通谋虚伪表示掩盖真实交易民事行为无效",
        "jurisdiction": "asean_vn",
        "core_doctrine": "当事人通谋作出虚假意思表示以掩盖另一真实交易的，虚假交易自始无效；被掩盖的真实交易若违反法律禁止性规定或公序良俗，同样绝对无效。",
        "practical_tip": "在股权转让与阴阳双轨合同中，严禁通过低报阴阳合同规避外资准入审批或偷逃外国承包商税 (FCT)。"
    },
    "VN:Civil_Code_2015:Art397": {
        "title": "缔约过失责任与商业谈判诚实信用义务",
        "jurisdiction": "asean_vn",
        "core_doctrine": "在要约承诺与合同磋商过程中，一方若隐瞒重大事实、提供虚假信息或无正当理由突然恶意破裂谈判，须对守约方在缔约阶段产生的实际信赖利益损失承担赔偿责任。",
        "practical_tip": "境外并购或 EPC 竞标签署 MOU/LOI 备忘录时，应明文订立谈判保密条款与无拘束力 (Non-binding) 声明。"
    },
    "VN:Civil_Code_2015:Art420": {
        "title": "情势变更原则五大法定要件与司法调整合同机制",
        "jurisdiction": "asean_vn",
        "core_doctrine": "当履约条件发生重大情势变迁，满足：① 无法预见；② 不可归责；③ 导致利益极度失衡；④ 虽已采取一切补救仍无法防止，当事人可要求重新协商；协商不成可诉请法院变更或解除合同。",
        "practical_tip": "在总价包干合同中因钢材水泥暴涨申请调价时，必须在暴涨发生 30 日内发出情势变更重新协商函，切勿直接单方停工。"
    },
    "VN:Commercial_Law_2005:Art301": {
        "title": "商事合同违约金 8% 法定绝对上限与实际损失赔偿并用",
        "jurisdiction": "asean_vn",
        "core_doctrine": "越南商事合同约定的违约金比例不得超过违约部分合同金额的 8%，超出部分法院或仲裁庭依法不予支持。但依据 Art 307，违约金与实际损失赔偿金 (Damages) 可以同时并用！",
        "practical_tip": "起草涉越 EPC 合同时，应将误期损害赔偿金 (Delay LD) 设定为 8%，同时明文保留追偿超出 8% 的实际工期延误损失权利。"
    },
    "VN:Commercial_Law_2005:Art306": {
        "title": "逾期付款法定利息按当地 3 家商业银行平均贷款利率计息",
        "jurisdiction": "asean_vn",
        "core_doctrine": "债务人逾期支付货款或工程款的，债权人有权要求按照逾期付款发生时，当地 3 家商业银行（如 Vietcombank, BIDV, Vietinbank）公布的平均逾期贷款利率计收逾期利息。",
        "practical_tip": "索赔逾期付款利息时，必须调取越南工贸银行、外贸银行同期官方贷款基准利率公告盖章件作为举证证据。"
    },
    "VN:Commercial_Law_2005:Art319": {
        "title": "商事争议 2 年极短诉讼与仲裁消灭时效红线",
        "jurisdiction": "asean_vn",
        "core_doctrine": "商事合同争议向法院起诉或提交 VIAC 仲裁的法定消灭时效仅为 2 年，自合法权益受到侵害之日起算。越南最高院指导性判例确认：单纯单方发催款函若未获对方书面签字确认债务，不发生时效中断效力！",
        "practical_tip": "工程结算出现分歧后，务必在 2 年内取得对方书面确认函或立即启动 VIAC 仲裁，严禁久拖失权。"
    },
    "VN:Law_135_2025:Art86.2": {
        "title": "2025新建设法正式承认预定损害赔偿 (LD) 机制",
        "jurisdiction": "asean_vn",
        "core_doctrine": "越南国会第 135/2025/QH15 号新建设法第 86.2 条划时代确立了建设工程合同预定损害赔偿金 (Liquidated Damages) 制度，允许当事人在合同中预先约定延误完工与质量缺陷的固定赔偿额，减轻实际损失举证责任。",
        "practical_tip": "合同签约日早于 2026 年 7 月 1 日施行的老合同，需重点审查新旧法衔接过渡条款与商业法 8% 违约金上限协调。"
    },
    "VN:Land_Law_2024:Art79": {
        "title": "国家收回土地 32 类公共利益项目穷尽清单与商业征地限制",
        "jurisdiction": "asean_vn",
        "core_doctrine": "越南 2024 年新土地法第 79 条列明了国家为经济社会发展收回土地的 32 类法定基础设施与公用事业项目。不在清单内的普通商业及新能源项目，国家一律不负责行政征拆，必须由外资自筹资金与农户达成 100% 商业转让协议！",
        "practical_tip": "投前尽调必须核实项目是否属于第 79 条法定国家收回土地项目清单，防范因个别钉子户导致项目拿地彻底搁浅。"
    },
    "VN:Land_Law_2024:Art119": {
        "title": "按年缴纳土地租金禁止抵押土地使用权物权红线",
        "jurisdiction": "asean_vn",
        "core_doctrine": "外商投资企业在越南获得土地，若选择按年支付租金模式 (Annual Land Rental)，依法仅享有土地租赁权，严禁将土地使用权向银行抵押融资，仅允许抵押地面自有建筑与机器设备；唯有一次性缴清整个租期租金模式方可抵押土地使用权。",
        "practical_tip": "外资工业园项目若需进行项目融资银团质押，在拿地时必须选择一次性付清土地租金 (Lump-sum Payment) 模式办理红皮书。"
    },

    # 🇲🇾 马来西亚核心评注
    "MY:CIPAA_2012:Sec35": {
        "title": "背靠背付款条款 (Pay-when-paid) 法定自始绝对无效",
        "jurisdiction": "asean_my",
        "core_doctrine": "马来西亚 2012 年《建筑业支付与裁决法》第 35 条规定，一切以第三方（业主）向总包商付款作为向分包商支付工程款先决条件的条款，自始绝对无效 (Void and of no effect)。总包不得以未获业主付款为由拒绝付款。",
        "practical_tip": "总承包商应通过设定合理的里程碑节点验收程序、质量保留金与工程量联合复核机制替代非法的背靠背条款。"
    },
    "MY:CIPAA_2012:Sec12": {
        "title": "45 个工作日裁决书时限与逾期作出自始无效宪制铁律",
        "jurisdiction": "asean_my",
        "core_doctrine": "依据 CIPAA 第 12(2) 条，裁决员必须在收到裁决答辩书后 45 个工作日内作出裁决。依据第 12(3) 条及联邦法院 Pancaran Inspire 标杆判例，超出 45 个工作日作出的裁决书自始绝对无效，高院一律予以撤销。",
        "practical_tip": "在 AIAC 快速裁决程序中，必须严格把控时间表，任何延展期限必须由双方当事人共同书面签署同意书。"
    },
    "MY:CIPAA_2012:Sec28": {
        "title": "裁决胜诉未获付款之法定工程停工与减缓进度权",
        "jurisdiction": "asean_my",
        "core_doctrine": "裁决员裁决发包人向承包商支付工程款后，发包人未在裁决书指定期限内支付的，承包商在发出 14 日书面通知后，有权合法暂停施工或减缓施工进度，并自动享有工期顺延 (EOT) 与停工损失补偿。",
        "practical_tip": "在收到 CIPAA 胜诉裁决且业主拖欠时，应严格按第 28 条发出 14 日通知行使停工权，防范被业主以擅自停工为由反诉违约。"
    },
    "MY:Contracts_Act_1950:Sec75": {
        "title": "违约金与罚金无区分原则与商业正当利益测试",
        "jurisdiction": "asean_my",
        "core_doctrine": "马来西亚废除英国普通法 Liquidated Damages 与 Penalty 的严格二分。依据联邦法院 Cubic Electronics 案，约定的违约金数额可直接作为赔偿上限，违约方若主张数额过高，须承担证明该数额缺乏商业正当利益 (Legitimate Commercial Interest) 的举证责任。",
        "practical_tip": "起草 EPC 误期违约金条款时，应附带说明违约金系真实商业合理预估，并列明因工程延误可能产生的银团利息与替代发电损失。"
    },
    "MY:Act_520_CIDB:Sec25": {
        "title": "未持有效 CIDB 施工注册证进场施工属刑事犯罪且合同违法无效",
        "jurisdiction": "asean_my",
        "core_doctrine": "任何国内外承包商未在马来西亚建筑工业发展局 (CIDB) 取得有效施工执业资质等级证书即进场施工作业的，构成刑事犯罪，处以高额罚款，且依据《合同法》第 24 条合同可能因违法性 (Illegality) 导致无法向法院追索工程款。",
        "practical_tip": "中资企业进场前必须办妥 CIDB G7 级外资临时/正式注册证书，并按规定在开工后足额缴纳 0.125% 建筑征费 (Levy)。"
    },
    "MY:National_Land_Code:Sec433B": {
        "title": "外资购置或长期租赁马来西亚土地必须事先取得州行政议会特批",
        "jurisdiction": "asean_my",
        "core_doctrine": "外国公司或非公民在马来西亚购置工业土地或签署超过 3 年的土地长期租赁协议，必须事先取得土地所在州行政议会 (State Authority) 书面批文并符合各州外资最低购地门槛。未获批文签署的土地协议依据 Sec 433B 自始绝对无效。",
        "practical_tip": "买地或租地协议中必须将取得州政府同意 (Consent) 设定为合同先决条件 (Condition Precedent)，并明确约定不获批准全额无息退款退还定金。"
    },

    # 🇸🇬 新加坡核心评注
    "SG:SOPA_2004:Sec9": {
        "title": "付款保障法反背靠背支付条款与工程供应全链条适用",
        "jurisdiction": "asean_sg",
        "core_doctrine": "新加坡 SOPA 第 9 条明文规定，一切建筑工程施工合同、分包合同及建筑材料设备供应合同中，使付款取决于从第三方获得付款的条款完全无效。分包商进度款请求权受成文法刚性保护。",
        "practical_tip": "新加坡境内工程分包与供应合同严禁出现'依发包人付款进度支付'字眼，应按照 SOPA 设定的法定月度周期足额付款。"
    },
    "SG:SOPA_2004:Sec15": {
        "title": "付款答辩 (Payment Response) 未列明抗辩事由在裁决中一律禁止提出",
        "jurisdiction": "asean_sg",
        "core_doctrine": "依据 SOPA 第 15(3) 条及终审法院 Audi Construction 判例，发包人在收到付款索赔后，若未在法定期限（最长 21 天）内提交付款答辩，或未在答辩中详细载明抵销/扣款抗辩理由，后续在 SMC 快速裁决程序中绝对禁止提出该抗辩事由！",
        "practical_tip": "总包商收到分包商付款索赔函后，必须在 7~14 天内出具详尽的 Payment Response，将全部质量缺陷反索赔与工期违约金抵销理由全部列明。"
    },
    "SG:Precedent:BS_Mount_Sophia": {
        "title": "以显失公平 (Unconscionability) 独立于欺诈止付独立保函标准",
        "jurisdiction": "asean_sg",
        "core_doctrine": "新加坡终审法院通过 BS Mount Sophia 标杆先例确立：在见索即付履约保函中，除欺诈 (Fraud) 外，'显失公平 (Unconscionability)' 构成申请法院禁令止付保函的独立救济事由，强调恶意施压或明显不当索兑的司法干预。",
        "practical_tip": "当遭遇业主在工期争议未决且无严重过错情况下恶意索兑保函时，应立即向新加坡高院申请依据 Unconscionability 签发紧急止付禁令。"
    },
    "SG:Precedent:Denka_Advantech": {
        "title": "终审法院坚守 Dunlop 真实预估损失违约金审查标准",
        "jurisdiction": "asean_sg",
        "core_doctrine": "新加坡终审法院在 [2020] SGCA 119 判例中明确拒绝英国 Cavendish 宽松的商业利益标准，裁定新加坡法坚决坚守传统 Dunlop Pneumatic 测试标准——即违约金必须属于违约时对可能产生损失的真实预估 (Genuine Pre-estimate of Loss)，否则定性为罚金条款不予执行。",
        "practical_tip": "起草涉新建设合同时，违约金定额必须建立在严谨的财务测算和工期延误成本模型基础上，防止被判定为惩罚性罚金。"
    },
    "SG:IRDA_2018:Sec440": {
        "title": "破产重组中 Ipso Facto 自动解约条款法定阻断机制",
        "jurisdiction": "asean_sg",
        "core_doctrine": "新加坡《综合破产与重组法》第 440 条确立：当承包商或发包人进入法院债务重组 (Scheme of Arrangement) 或司法管理程序时，合同相对方不得仅凭当事人进入破产或重整程序为由单方终止工程合同，法定阻断此类破产自动终止条款效力。",
        "practical_tip": "当合作方发生财务危机时，切勿仓促依据破产事件发函解约，必须审查是否受到 IRDA 第 440 条法定救济冻结期限制。"
    },

    # 🇹🇭 泰国核心评注
    "TH:CCC:Sec596": {
        "title": "迟延完工违约金与法院自由裁量酌减权",
        "jurisdiction": "asean_th",
        "core_doctrine": "在承揽合同中，若因承包商过错迟延完工，定作人有权要求扣减价款或索赔违约金。但依据民商法典第 383 条，若法院或仲裁庭查明约定的违约金数额畸高显失公平，有权依自由心证依职权予以酌减，且合同明文约定放弃酌减无效。",
        "practical_tip": "承包商面对业主高额罚款索赔时，应调取业主实际出租或发电收益损失证据，向法庭极力主张违约金畸高请求按实际损失酌减。"
    },
    "TH:CCC:Sec603": {
        "title": "移交前工程毁损灭失不可抗力风险由包工包料承包商自担铁律",
        "jurisdiction": "asean_th",
        "core_doctrine": "泰国民商法典第 603 条规定：在工程完工移交前，因不可归责于双方的事由（如特大洪灾/地震不可抗力）导致建筑物全部或部分毁损灭失的，提供材料的承包商自行承担损失，无权向发包人索要已毁损部分工程款！",
        "practical_tip": "此条与 FIDIC 17.3 雇主风险分担截然相反！在泰国承揽工程合同中，必须明文订立排除 CCC 第 603 条适用的特约条款，明确不可抗力由业主承担或通过 CAR 保险赔付。"
    },
    "TH:CCC:Sec193_34": {
        "title": "承揽人追索工程进度款 2 年极短消灭时效陷阱",
        "jurisdiction": "asean_th",
        "core_doctrine": "泰国民商法典第 193/34(1) 条规定：建筑承揽人追索承揽报酬、工料垫付款与工程最终结算款的请求权，适用 2 年极短诉讼消灭时效（非 10 年普通时效！）。最高院判例确认逾期起诉一律驳回胜诉权。",
        "practical_tip": "在泰国工程完工后，若出现拖欠尾款，必须在应付款日届满之日起 2 年内正式向法院提起诉讼或启动仲裁，严禁因持续私下磋商而罹于 2 年短时效！"
    },
    "TH:FBA_1999:Sec36": {
        "title": "外商经营法建筑业外资限制与反代持 (Nominee) 刑事重锤",
        "jurisdiction": "asean_th",
        "core_doctrine": "建筑工程除实缴外资超 5 亿泰铢的公用基建外，一律禁止外资控股超 50%。泰国刑法与 FBA 第 36 条严厉打击利用泰国员工或律师通过优先股代持 51% 股权规避外资准入行为，最高判处 3 年监禁并强制解散清算公司。",
        "practical_tip": "进入泰国承揽工程，应通过取得 BOI 投资促进证书豁免 FBA 限制，或与泰国大型央企上市公司组建真实股权对等的合资联营体。"
    },
    "TH:Arbitration_Act_2545:Sec15": {
        "title": "政府行政合同 (PPP/EPC) 仲裁协议完全有效性确立",
        "jurisdiction": "asean_th",
        "core_doctrine": "泰国 2002 年仲裁法第 15 条明文确立：国家行政机关、国有企业与私营企业签署的特许经营协议与工程合同，约定提交国内外仲裁解决争议的条款对泰国政府完全有效，政府不得以属于行政合同为由主张仲裁协议无效。",
        "practical_tip": "与泰国公用事业部委签署重大基建特许权协议时，务必坚持约定仲裁条款（推荐 TAI 或 SIAC 仲裁），以阻断泰国行政法院地方保护主义干预。"
    },

    # 🇵🇭 菲律宾核心评注
    "PH:Civil_Code:Art1723": {
        "title": "建筑物倒塌工程师与总承包商 15 年终身连带法定追责重锤",
        "jurisdiction": "asean_ph",
        "core_doctrine": "菲律宾民法典第 1723 条确立：建筑物因设计缺陷、地基缺陷或施工不达标在竣工移交后 15 年内发生倒塌坍塌的，工程师、建筑师与总承包商对定作人及第三人承担法定连带损害赔偿责任，诉讼时效长达 10 年，任何预先免责条款绝对无效。",
        "practical_tip": "在菲律宾承建大型桥梁、高层建筑与电厂，必须建立全生命周期施工质量追溯档案，并购买 15 年期工程质量潜在缺陷保证保险。"
    },
    "PH:Civil_Code:Art1724": {
        "title": "固定总价工程设计变更索赔无书面定价协议工程款归零铁律",
        "jurisdiction": "asean_ph",
        "core_doctrine": "在固定总价建设工程中，承包商索赔设计变更或工程量增加导致的追加款项，必须同时满足：① 取得业主正式书面变更授权指令 且 ② 双方已签署书面变更价格协议。缺一不可，且最高法院严禁援引不当得利 (Quantum Meruit) 绕道索赔！",
        "practical_tip": "在菲律宾现场履约中，凡遇业主代表或监理口头下达变更指令，必须秉持'无书面指令不进场、无定价协议不动工'原则，务必在实施前签署正式补充协议 (Change Order)。"
    },
    "PH:Anti_Dummy_Law:Sec2A": {
        "title": "反傀儡法严禁外商突破外资股比与外人插手受限业务刑责",
        "jurisdiction": "asean_ph",
        "core_doctrine": "菲律宾联邦法第 108 号《反傀儡法》严禁在受限国有化行业使用菲律宾挂名股东 (Dummy) 或允许外籍人员担任财务总监、总经理等实质管理职位规避宪法 40% 外资上限，违者判处 5~15 年有期徒刑并没收企业全部资产。",
        "practical_tip": "合资公司章程治理结构与高管委派必须经持牌菲律所合规论证，且通过 RA 11659《公共服务法》修正案核实所在行业是否已全面放开外资 100% 独资。"
    },
    "PH:EO_1008:Sec4": {
        "title": "建筑业仲裁委员会 (CIAC) 建设工程争议法定原始且排他管辖权",
        "jurisdiction": "asean_ph",
        "core_doctrine": "凡在菲律宾境内发生的一切建设工程合同争议，只要合同中存在任何提交仲裁的意思表示，无论约定的是新加坡 SIAC 还是巴黎 ICC 仲裁，依据 EO 1008 第 4 条，菲律宾 CIAC 依然依法享有原始且排他的强行管辖权，当事人可直接向 CIAC 提请仲裁！",
        "practical_tip": "涉菲工程合同若约定离岸仲裁，需做好在境外仲裁前或境外仲裁进行中，菲律宾当地业主向 CIAC 发起平行仲裁程序并被菲法院支持管辖的风险预案。"
    },
    "PH:RA_8975:Sec3": {
        "title": "严禁地方法院对国家重大基础设施工程签发临时禁制令 (TRO)",
        "jurisdiction": "asean_ph",
        "core_doctrine": "菲律宾共和国第 8975 号法案明文规定：全国任何地区审判法院 (RTC) 或上诉法院，严禁对国家政府重大基建工程的征地、招投标、签约及现场施工签发任何临时限制令 (TRO) 或初步禁令，唯有最高法院有权签发，下级法院签发自始无效并受刑事纪律处分。",
        "practical_tip": "在承建菲律宾政府重大战略公路或水利工程时，若遭遇竞争对手勾结地方 RTC 法院签发停工令，可直接援引 RA 8975 主张法院禁令绝对无效并继续施工。"
    },

    # 🌐 FIDIC 国际工程标准合同黄金条款评注
    "FIDIC:Silver_1999:Clause_1.5": {
        "title": "合同文件优先解释次序与专用条件排他效力",
        "jurisdiction": "fidic",
        "core_doctrine": "银皮书第 1.5 款确立合同文件解释优先顺序：合同协议书 > 专用条件 (PC) > 通用条件 (GC) > 雇主要求 > 投标书及明细表。专用条件对通用条件的修改具有绝对排他覆写效力。",
        "practical_tip": "在专用条件谈判中，重点排查业主是否在 PC 中偷偷修改了 13.7 调价、20.1 索赔时效或删除了雇主违约救济条款。"
    },
    "FIDIC:Silver_1999:Clause_4.2": {
        "title": "履约担保索兑四大法定限定条件与错误索兑全额赔偿",
        "jurisdiction": "fidic",
        "core_doctrine": "雇主仅在以下四种情形下有权向保函开立行索兑履约保函：① 承包商未延期保函有效期限；② 承包商未在 42 天内支付经商定或确定的款项；③ 承包商未在 42 天内纠正违约通知；④ 雇主依据第 15.2 款合法解约。雇主若在无权情形下索兑保函，须全额赔偿承包商全部损失。",
        "practical_tip": "保函到期日前至少提前 30 天办理延期；当遭遇雇主在缺乏上述四种情形下发出索兑要求时，立即向仲裁庭申请紧急禁令阻止索兑。"
    },
    "FIDIC:Silver_1999:Clause_8.4": {
        "title": "工期顺延 (EOT) 五大法定事由与共同延误防阻原则",
        "jurisdiction": "fidic",
        "core_doctrine": "承包商有权因：① 变更；② 异常恶劣气候；③ 当局造成的无法预见延误；④ 雇主阻碍与迟延现场占有等事由获得工期顺延。只要延误影响到了竣工关键路径 (Critical Path)，承包商即可免除延误违约金责任。",
        "practical_tip": "发生任何延误事件，必须在 28 天内按照第 20.1 款发出正式索赔通知，并利用 Primavera P6 进度网络计划精确证明关键路径受阻时长。"
    },
    "FIDIC:Silver_1999:Clause_13.7": {
        "title": "因东道国法律与政策变更调增合同价格与顺延工期",
        "jurisdiction": "fidic",
        "core_doctrine": "基准日 (Base Date) 之后，若工程东道国成文法、行政规章、税率、关税配额或强制性本地化比例 (TKDN) 发生变更导致承包商成本增加或工期延误，合同价格应相应调增且工期应予顺延。",
        "practical_tip": "遇到东道国上调增值税、取消外籍劳工签证配额或突增环保排污标准时，应立即依据 13.7 款编制造价调增索赔报告。"
    },
    "FIDIC:Silver_1999:Clause_14.8": {
        "title": "雇主延误付款自动享有复利融资费用无需索赔通知",
        "jurisdiction": "fidic",
        "core_doctrine": "雇主若未在第 14.7 款规定的法定期限内支付工程款，承包商有权按年利率按月计算复利融资利息（按支付货币所在国央行贴现率加 3% 计息）。该项权利无须任何索赔通知即可自动享有且不影响承包商停工解约权。",
        "practical_tip": "在每一份期中付款申请单与催款函中，自动列入按 Clause 14.8 计算的逐日累计复利罚息明细表，施加财务合规压力。"
    },
    "FIDIC:Silver_1999:Clause_20.1": {
        "title": "承包商 28 天索赔失权通知时效陷阱与法律突破路径",
        "jurisdiction": "asean_all",
        "core_doctrine": "承包商若未在意识到或应当意识到索赔事件发生后 28 天内发出索赔通知，则彻底丧失工期顺延 (EOT) 与追加付款权利，雇主免除一切责任。但在普通法下可通过'业主防阻原则 (Prevention Principle)'突破失权；在大陆法下可通过诚实信用与情势变更原则抗辩。",
        "practical_tip": "项目部必须建立 28 天索赔失权预警台账，现场监理签收指令后第一时间向雇主代表发送索赔意向通知 (Notice of Claim)。"
    },

    # 🏛️ 国际条约与双边投资协定评注
    "CAFTA:2009:Art6_Expropriation": {
        "title": "中国-东盟投资协议间接征收认定标准与公允市场价值全额补偿",
        "jurisdiction": "treaty",
        "core_doctrine": "任何缔约方不得直接或间接征收或国有化投资，除非满足：① 基于公共利益；② 依照法定正当程序；③ 非歧视性；④ 按照征收发生前之公允市场价值 (Fair Market Value) 给予及时、充分、有效的可兑换补偿及法定利息。",
        "practical_tip": "东道国政府若撤销重大特许权或强制征用土地电站，应以 CAFTA 第 6 条为核心请求权基础启动政府间磋商与国际仲裁索赔。"
    },
    "ACIA:2009:Art19_Denial_of_Benefits": {
        "title": "东盟全面投资协定利益拒绝条款与实质性商业运营要求",
        "jurisdiction": "treaty",
        "core_doctrine": "若某一企业由非东盟缔约国投资者所有或控制，且在该企业设立之缔约国境内不具备实质性商业运营 (No Substantial Business Operations)，东道国有权依据第 19 条拒绝给予该企业 ACIA 协定保护与仲裁直诉权。",
        "practical_tip": "中国母公司若在新加坡设立 SPV 作为境外投资平台，该 SPV 必须租赁实体办公室、雇佣本地员工并由本地董事进行实质性决策，杜绝空壳邮政信箱公司 (Shell Company) 被东道国以利益拒绝条款剔除管辖。"
    },
    "CN:Data_Security_Law:Art36": {
        "title": "非经中国主管机关批准严禁向外国司法或者执法机构提供境内数据",
        "jurisdiction": "prc_sasac",
        "core_doctrine": "非经中华人民共和国主管机关批准，境内的组织、个人不得向外国司法或者执法机构提供存储于境内的法律文本、工程设计数据及商业机密。违者面临数额高达 500 万元罚款及暂停涉外业务制裁。",
        "practical_tip": "在境外仲裁证据开示 (Document Disclosure / Discovery) 中，凡涉及母公司境内服务器存储的工程邮件与图纸，出境提供前必须向发改委/商务部履行前置审批程序。"
    },
    "CN:SASAC_Order_35:Art12": {
        "title": "央企境外投资重大事项事前法律合规论证与负面清单监管",
        "jurisdiction": "prc_sasac",
        "core_doctrine": "中央企业开展境外投资，必须严格遵守非主业投资负面清单，在决策前必须委托国际知名律所与涉外法务团队出具独立、详实的《境外投资准入与合规论证法律意见书》，防范盲目出海导致国有资产流失。",
        "practical_tip": "在投前决策上会材料中，必须附具本系统生成的完整尽职调查报告与外资准入穿透合规意见书。"
    },
    "CN:SASAC_Notice_75_2021:Art4": {
        "title": "国资委严禁对参股项目提供超股比担保与无股权关系企业担保",
        "jurisdiction": "prc_sasac",
        "core_doctrine": "国资发财评规〔2021〕75号文严格规定：中央企业严禁对参股企业提供超股比融资担保，严禁对无股权关系企业提供担保，严禁对高风险财务状况企业提供担保。违者将严肃追究违规经营投资责任。",
        "practical_tip": "在东盟 KSO 联营体或 PPP 项目中，若外方业主或银团要求中资母公司出具 100% 全额连带母公司完工担保 (PCG)，必须通过引入反担保协议或将担保份额严格限制在持股比例以内，严防撞击 75 号文国资合规红线。"
    },
    "MY:Contracts_Act_1950:Sec24": {
        "title": "合同目的或对价违法及违背公共政策自始绝对无效",
        "jurisdiction": "asean_my",
        "core_doctrine": "凡合同对价或目的违反法律禁止性规定、规避成文法或违背公共政策(Public Policy)的，合同自始绝对无效。在工程实务中，无照施工或通谋逃税的分包合同常被依据本条认定不可执行。",
        "practical_tip": "签署境外分包协议前，必须查验分包商是否持有马来西亚 CIDB 牌照及有效资质，杜绝因协议违法导致工程款不可执行。"
    },
    "MY:Contracts_Act_1950:Sec56": {
        "title": "履行时间要素 (Time of the Essence) 与单方解约权丧失",
        "jurisdiction": "asean_my",
        "core_doctrine": "若合同未明示或依性质表明履行时间为合同实质要素，或虽为要素但逾期后守约方继续接受履约未提出异议，守约方丧失单方解除合同权，仅保留索赔延误损失权利。",
        "practical_tip": "在工期延误催告函中，必须明示重申'Time is of the essence'，防止因继续默许施工导致解约权被法院判定丧失。"
    },
    "SG:Misrepresentation_Act:Sec2": {
        "title": "虚假陈述法定撤销权与损害赔偿责任",
        "jurisdiction": "asean_sg",
        "core_doctrine": "在订立合同前，一方若因对方虚假陈述而受误导缔约，即便陈述方非出于欺诈，受误导方亦有权主张撤销合同并索赔损失，除非陈述方能举证证明其具有合理理由相信其陈述为真。",
        "practical_tip": "招标文件中雇主提供的地勘勘察数据若存在严重虚假不符，承包商可依据本条向发包人索赔地质重大误导损失。"
    },
    "SG:UCTA_Cap_396:Sec3": {
        "title": "标准格式条款免责合理性检验 (Reasonableness Test)",
        "jurisdiction": "asean_sg",
        "core_doctrine": "在商业标准格式合同中，任何企图免除或限制违约责任、或主张有权不履行实质承诺的条款，均必须通过合理性检验。若条款显失公平，法院将依法认定其不具执行力。",
        "practical_tip": "发包人拟定的格式免责条款若完全排除自身工期阻碍责任，可援引 UCTA 第 3 条主张该免责条款不合理而无效。"
    },
    "TH:CCC:Sec156": {
        "title": "法律行为重大错误撤销权与重大过失限制",
        "jurisdiction": "asean_th",
        "core_doctrine": "当意思表示关于法律行为的要素（如标的物性质、交易当事人身份）存在重大错误 (Mistake) 时，该民事法律行为可撤销。但若错误系因表意人重大过失所致，则不得主张撤销。",
        "practical_tip": "在泰国工程投标或收并购中，必须对土地性质及电网消纳能力开展专业尽调，防止因自身疏忽被法院认定为重大过失不得撤销。"
    },
    "TH:CCC:Sec368": {
        "title": "合同依诚实信用原则与当事人真实意思表示解释",
        "jurisdiction": "asean_th",
        "core_doctrine": "合同条款发生歧义时，必须依诚实信用原则并考虑通常交易习惯进行合理解释，严禁拘泥于个别文字而曲解当事人订约时的真实合意。",
        "practical_tip": "对于中英泰多语种施工合同，在解释争议条款时应调取往来谈判邮件与会议纪要，证明双方成立合同时的真实商业目的。"
    },
    "PH:Civil_Code:Art1169": {
        "title": "债务人迟延履行 (Mora) 必须经司法或书面正式催告",
        "jurisdiction": "asean_ph",
        "core_doctrine": "债务人自债权人通过司法或司法外书面正式催告履行起，方负迟延责任。在双务之债中，一方未履行其对待给付义务前，另一方不构成迟延 (Compensatio Morae)。",
        "practical_tip": "在追索工程欠款或工期延误索赔前，必须正式发出书面催告函 (Demand Letter)，固定违约迟延起算日。"
    },
    "PH:Civil_Code:Art1409": {
        "title": "自始绝对无效合同七大类型与诉权永不罹于时效",
        "jurisdiction": "asean_ph",
        "core_doctrine": "违反公共秩序、目的绝对不可能、通谋虚伪或明文禁止的合同自始绝对无效 (Void ab initio)。对绝对无效合同主张确认无效之诉，依法永不罹于诉讼时效，任何追认亦不能使之生效。",
        "practical_tip": "对于违反《反傀儡法》或土地外资持股禁令签署的代持协议，对方无论何时主张确权均属自始绝对无效。"
    },
    "CN:NDRC_Order_11:Art13": {
        "title": "发改委11号令境外敏感行业投资事前核准与大额投资备案",
        "jurisdiction": "prc_sasac",
        "core_doctrine": "境内投资主体开展境外投资，涉及敏感国家和地区、敏感行业的，必须向国家发改委申请核准；非敏感类中方投资额 3 亿美元以上的，须向国家发改委履行备案手续。",
        "practical_tip": "出海投资电网、港口、通信等敏感基建工程，在对外正式签署具有约束力投资协议前，必须办妥国家发改委核准或备案凭证。"
    },
    "CN:MOFCOM_Order_3:Art6": {
        "title": "商务部境外投资管理办法 (ODI) 真实性审查与核准证书",
        "jurisdiction": "prc_sasac",
        "core_doctrine": "企业开展境外投资须向商务主管部门申请办理《企业境外投资证书》。严禁虚假境外投资或将境内资金违规转移境外，资金汇出须接受外汇管理局资本项目真实性核验。",
        "practical_tip": "境外项目公司增资与资本金汇出前，必须确保商务部 ODI 证书与外管局外汇登记手续完备齐全。"
    },
    "FIDIC:Yellow_1999:Clause_4.12": {
        "title": "黄皮书设计建造不可预见地质物质条件全额工期与费用索赔",
        "jurisdiction": "fidic",
        "core_doctrine": "在黄皮书(设计建造)下，若承包商遇到在投标基准日不可预见的地下异常地质或地下水，承包商有权索赔全部工期顺延 (EOT) 与由此产生的额外成本费用 (Cost)。",
        "practical_tip": "遇到异常溶洞、断层或地下水时，必须立即停工并拍照摄像留存独立地勘报告，在 28 天内向工程师发出 4.12 款索赔意向书。"
    },
    "FIDIC:Red_1999:Clause_12.3": {
        "title": "红皮书单价合同工程量变更超 10% 重新核定综合单价规则",
        "jurisdiction": "fidic",
        "core_doctrine": "在红皮书(施工单价)合同中，某项工作实际测量的工程量比工程量清单(BOQ)变化超过 10% 且导致该项造价变动超合同总价 0.01% 时，工程师必须对该项工作的综合单价进行重新核定。",
        "practical_tip": "土石方开挖工程量大幅增加时，应依据 12.3 款主动要求调高单价以弥补设备进出场与分包窝工损失。"
    }
}

with open("kb/asean/commentary.json", "w", encoding="utf-8") as f:
    json.dump(commentary_data, f, ensure_ascii=False, indent=2)
print(f"kb/asean/commentary.json written with {len(commentary_data)} items.")

# 2. 扩充 timepoints.yaml (18+ 关键修法时点与时限警示规则)
timepoints_data = [
    {
        "timepoint_id": "TP_VN_CONSTRUCTION_2025",
        "jurisdiction": "asean_vn",
        "law_name": "越南《2025年新建设法》(Law No. 135/2025/QH15)",
        "effective_date": "2026-07-01",
        "enacted_date": "2025-11-28",
        "rule_type": "statutory_overhaul",
        "alert_level": "red",
        "condition": "contract_date < 2026-07-01",
        "description": "2026年7月1日正式生效。第86.2条全面承认预定损害赔偿(LD)机制，突破旧法8%商业罚金上限争议；对于在此之前签署的存量合同，需审查新旧法衔接特约。"
    },
    {
        "timepoint_id": "TP_VN_LAND_2024",
        "jurisdiction": "asean_vn",
        "law_name": "越南《2024年新土地法》(Law No. 31/2024/QH15)",
        "effective_date": "2024-08-01",
        "enacted_date": "2024-01-18",
        "rule_type": "property_rights",
        "alert_level": "red",
        "condition": "contract_date >= 2024-08-01",
        "description": "第79条确立国家收回土地的32类穷尽公共利益清单，非清单项目国家不负责征拆；按年缴租土地严禁抵押使用权。"
    },
    {
        "timepoint_id": "TP_ID_SEMA_3_2023",
        "jurisdiction": "asean_id",
        "law_name": "印尼最高法院《2023年第3号通告》(SEMA No. 3/2023)",
        "effective_date": "2023-12-29",
        "enacted_date": "2023-12-29",
        "rule_type": "judicial_precedent",
        "alert_level": "yellow",
        "condition": "contract_date >= 2023-12-29",
        "description": "确立诚实信用原则限制：若无恶意(itikad tidak baik)，当事人不得仅因涉外合同缺少印尼语版本而主张合同机械无效。"
    },
    {
        "timepoint_id": "TP_ID_MEMR_11_2024",
        "jurisdiction": "asean_id",
        "law_name": "印尼能矿部《2024年第11号条例》(MEMR Reg 11/2024)",
        "effective_date": "2024-08-01",
        "enacted_date": "2024-07-25",
        "rule_type": "local_content_tkdn",
        "alert_level": "red",
        "condition": "contract_date >= 2024-08-01",
        "description": "电力基础设施本地化率(TKDN)豁免申请机制，若属地产能无法满足，允许在签约前向能矿部申请设备进口豁免批文。"
    },
    {
        "timepoint_id": "TP_MY_CIPAA_2012",
        "jurisdiction": "asean_my",
        "law_name": "马来西亚《2012年建筑业支付与裁决法》(CIPAA 2012)",
        "effective_date": "2014-04-15",
        "enacted_date": "2012-06-22",
        "rule_type": "adjudication_mandatory",
        "alert_level": "red",
        "condition": "all",
        "description": "2014年4月15日起全面施行。第35条背靠背条款自始无效，确立45个工作日快速裁决及未付款法定停工权。"
    },
    {
        "timepoint_id": "TP_SG_SOPA_AMENDMENT_2019",
        "jurisdiction": "asean_sg",
        "law_name": "新加坡《建筑业付款保障法修订案》(SOPA 2019)",
        "effective_date": "2019-12-15",
        "enacted_date": "2019-10-01",
        "rule_type": "statutory_amendment",
        "alert_level": "yellow",
        "condition": "contract_date >= 2019-12-15",
        "description": "将付款答辩法定期限延长至最长21天，明确排除纯损害赔偿金(Damages)在SOPA裁决中的索赔，强化程序公平。"
    },
    {
        "timepoint_id": "TP_TH_CCC_INTEREST_2021",
        "jurisdiction": "asean_th",
        "law_name": "泰国《民商法典法定利率紧急法令修正案 B.E. 2564》",
        "effective_date": "2021-04-11",
        "enacted_date": "2021-04-10",
        "rule_type": "statutory_amendment",
        "alert_level": "yellow",
        "condition": "contract_date >= 2021-04-11",
        "description": "将民商法典第224条逾期法定利率由年息7.5%大幅下调为3%基础利率+2%迟延罚息=年息5%，并严禁按复利计息。"
    },
    {
        "timepoint_id": "TP_PH_PPP_CODE_2023",
        "jurisdiction": "asean_ph",
        "law_name": "菲律宾《2023年公私合营法典》(PPP Code, RA 11966)",
        "effective_date": "2023-12-23",
        "enacted_date": "2023-12-05",
        "rule_type": "statutory_overhaul",
        "alert_level": "red",
        "condition": "contract_date >= 2023-12-23",
        "description": "全面废止旧BOT法(RA 7718)，整合国家与地方PPP项目监管，确立特许权提前终止公允补偿计算标准与免受RTC禁令保护。"
    },
    {
        "timepoint_id": "TP_PH_RENEWABLE_ENERGY_2022",
        "jurisdiction": "asean_ph",
        "law_name": "菲律宾能源部《可再生能源法实施细则修订通告》(DOE DC 2022-11-0034)",
        "effective_date": "2022-12-08",
        "enacted_date": "2022-11-15",
        "rule_type": "foreign_entry_liberalization",
        "alert_level": "green",
        "condition": "contract_date >= 2022-12-08",
        "description": "历史性突破外商投资股比限制，允许外资在太阳能、风能、水力及海洋能电站项目中持有100%独资控股权。"
    },
    {
        "timepoint_id": "TP_FIDIC_2017_REVISION",
        "jurisdiction": "fidic",
        "law_name": "FIDIC 2017 版红/黄/银皮书系列合同条件",
        "effective_date": "2017-12-05",
        "enacted_date": "2017-12-05",
        "rule_type": "standard_contract_revision",
        "alert_level": "yellow",
        "condition": "contract_version == '2017'",
        "description": "将第20.1款承包商索赔失权拓展为双向对等的Clause 20.2雇主与承包商对等28天通知时限，设立第21章常设DAAB裁决委员会。"
    },
    {
        "timepoint_id": "TP_CN_SASAC_75_2021",
        "jurisdiction": "prc_sasac",
        "law_name": "国务院国资委《关于加强中央企业融资担保管理工作的通知》(国资发财评规〔2021〕75号)",
        "effective_date": "2021-12-27",
        "enacted_date": "2021-12-27",
        "rule_type": "sasac_mandatory_redline",
        "alert_level": "red",
        "condition": "all",
        "description": "严禁央企对参股企业超股比担保，严禁对无股权关系企业担保；在东盟KSO联营体中提供PCG全额母公司担保直接触碰违规红线。"
    },
    {
        "timepoint_id": "TP_CN_DATA_SECURITY_2021",
        "jurisdiction": "prc_sasac",
        "law_name": "《中华人民共和国数据安全法》",
        "effective_date": "2021-09-01",
        "enacted_date": "2021-06-10",
        "rule_type": "prc_national_security",
        "alert_level": "red",
        "condition": "all",
        "description": "第36条明确非经国家主管机关批准不得向境外司法或执法机构提供境内数据，涉外仲裁证据开示出境必须履行前置审批。"
    },
    {
        "timepoint_id": "TP_SINOSURE_30DAY_NOTICE",
        "jurisdiction": "treaty",
        "law_name": "中国出口信用保险公司特险保单出险预报与权益保全时限",
        "effective_date": "2020-01-01",
        "enacted_date": "2020-01-01",
        "rule_type": "insurance_timebar",
        "alert_level": "red",
        "condition": "all",
        "description": "保单特险通则明确：发生东道国政治风险、违约拖欠或保函索兑险情后，必须在30个自然日内向信保正式报损，逾期将面临减赔或拒赔。"
    },
    {
        "timepoint_id": "TP_VN_COMMERCIAL_LIMITATION",
        "jurisdiction": "asean_vn",
        "law_name": "越南《商业法》第319条商事消灭时效",
        "effective_date": "2006-01-01",
        "enacted_date": "2005-06-14",
        "rule_type": "statutory_timebar",
        "alert_level": "red",
        "condition": "all",
        "description": "工程款追索与商事违约救济消灭时效仅为2年，单方发催款函未获书面确权不中断时效，满2年丧失司法追索权。"
    },
    {
        "timepoint_id": "TP_TH_PRESCRIPTION_2YEAR",
        "jurisdiction": "asean_th",
        "law_name": "泰国《民商法典》第193/34(1)条承揽款消灭时效",
        "effective_date": "1992-06-01",
        "enacted_date": "1992-04-01",
        "rule_type": "statutory_timebar",
        "alert_level": "red",
        "condition": "all",
        "description": "承揽人索赔工程进度款与竣工结算款请求权适用2年极短消灭时效，必须在2年内正式立案起诉或仲裁以中断时效。"
    },
    {
        "timepoint_id": "TP_VN_FCT_CIRCULAR_103",
        "jurisdiction": "asean_vn",
        "law_name": "越南财政部第 103/2014/TT-BTC 号外国承包商税 (FCT) 通告",
        "effective_date": "2014-10-01",
        "enacted_date": "2014-08-06",
        "rule_type": "tax_withholding",
        "alert_level": "yellow",
        "condition": "all",
        "description": "离岸供货与在岸服务未明确拆分的EPC总价合同，将被按混合税率对全额离岸设备征收增值税与企业所得税。"
    },
    {
        "timepoint_id": "TP_ID_PP_18_2021",
        "jurisdiction": "asean_id",
        "law_name": "印尼政府《2021年第18号条例》(PP 18/2021 土地权利与空间管理)",
        "effective_date": "2021-02-02",
        "enacted_date": "2021-02-02",
        "rule_type": "property_rights",
        "alert_level": "green",
        "condition": "contract_date >= 2021-02-02",
        "description": "明确外资PT PMA可直接持有最长80年(30+20+30)建筑使用权(HGB)，并设立地下空间与高架空间独立物权登记规则。"
    },
    {
        "timepoint_id": "TP_MY_MACC_17A_2020",
        "jurisdiction": "asean_my",
        "law_name": "马来西亚《反贪污委员会法修订案》(MACC Act Sec 17A)",
        "effective_date": "2020-06-01",
        "enacted_date": "2018-05-04",
        "rule_type": "corporate_criminal_liability",
        "alert_level": "red",
        "condition": "contract_date >= 2020-06-01",
        "description": "确立商业组织对关联人(代理/分包商)行贿承担严格企业刑事责任，唯有证明已建立完备的'合理预防程序(Adequate Procedures)'方可抗辩。"
    }
]

with open("kb/asean/timepoints.yaml", "w", encoding="utf-8") as f:
    yaml.dump(timepoints_data, f, allow_unicode=True, sort_keys=False)
print(f"kb/asean/timepoints.yaml written with {len(timepoints_data)} items.")

# 3. 扩充 glossary.csv (120+ 组涉外工程法律三语专业字典)
glossary_data = [
    ["Term_CN", "Term_EN", "Term_Local", "Jurisdiction", "Legal_Definition"],
    ["背靠背付款条款", "Pay-when-paid Clause", "Klausul Pembayaran Berturut", "asean_all", "以发包人向总包付款作为总包向分包付款之前提条件的条款，在新、马法定绝对无效"],
    ["工期顺延", "Extension of Time (EOT)", "Perpanjangan Waktu", "asean_all", "因发包人违约或不可抗力导致关键路径延误时承包商免除违约金并延展工期的法定权利"],
    ["误期损害赔偿金", "Liquidated Damages (LD)", "Ganti Rugi Keterlambatan", "asean_all", "当事人预先在合同中约定的工期延误定额赔偿金，受属地法上限或法院酌减约束"],
    ["催告通知令", "Formal Notice of Default", "Somasi", "asean_id", "印尼法下主张债务人迟延违约前必须正式发出的司法或书面催告令"],
    ["善意原则", "Good Faith", "Itikad Baik", "asean_id", "印尼民法典第1338条与SEMA 3/2023核心原则，禁止权利滥用与恶意主张合同无效"],
    ["建筑使用权", "Right to Build", "Hak Guna Bangunan (HGB)", "asean_id", "外资PT PMA可合法持有并设立抵押的最长80年土地物权形式"],
    ["土地提存清场", "Consignment Deposit", "Konsinyasi", "asean_id", "印尼征地法下将补偿金提存地方法院后合法强制清场交地的特别程序"],
    ["本地化采购率", "Local Content Requirement", "Tingkat Komponen Dalam Negeri (TKDN)", "asean_id", "印尼法律规定的工程材料、设备及劳工必须采购本土资源的法定强制比例"],
    ["外国建筑代表处", "Foreign Construction Representative Office", "BUJKA", "asean_id", "外国建筑承包商在印尼承揽工程必须设立的属地执业代表机构"],
    ["联合体运营体", "Joint Operation", "Kerja Sama Operasi (KSO)", "asean_id", "外国承包商在印尼必须与本土持照建筑企业组建的无独立法人资格联合体"],
    ["建筑物失败", "Building Failure", "Kegagalan Bangunan", "asean_id", "印尼建筑服务法规定竣工移交后最长10年内倒塌由总包与设计连带赔偿的责任"],
    ["动产信托担保", "Fiduciary Security", "Jaminan Fidusia", "asean_id", "印尼动产及施工机械设备转移所有权以担保主债权履行的法定担保形式"],
    ["延期偿债程序", "Suspension of Debt Payment", "PKPU", "asean_id", "印尼商事法院主持的准破产债务重组司法程序，设立法定临时债务冻结期"],
    ["侵权行为", "Tortious Act", "Perbuatan Melawan Hukum (PMH)", "asean_id", "印尼民法典第1365条法定损害赔偿请求权基础，常被当地人用于恶意绕开仲裁条款"],
    ["缔约过失", "Fault in Contracting", "Lỗi trong giao kết hợp đồng", "asean_vn", "越南民法典第397条规定的谈判阶段隐瞒真相或恶意破裂谈判应承担的信赖利益赔偿责任"],
    ["情势变更", "Change of Circumstances (Hardship)", "Hoàn cảnh thay đổi cơ bản", "asean_vn", "越南民法典第420条规定的客观条件重大改变时重新协商及请求法院调整合同机制"],
    ["商业违约金上限", "Penalty Cap 8%", "Mức phạt vi phạm 8%", "asean_vn", "越南2005年商业法第301条规定的商事合同违约金不得超过违约部分8%的强行法限制"],
    ["外国承包商许可证", "Foreign Contractor Permit", "Giấy phép hoạt động xây dựng", "asean_vn", "外国企业在越施工必须在签约后申领且必须与越企联营的法定施工许可证"],
    ["外国承包商税", "Foreign Contractor Tax (FCT)", "Thuế nhà thầu nước ngoài", "asean_vn", "外国实体在越南境内提供工程或技术服务被源泉扣缴的增值税与所得税混合税"],
    ["红皮书土地证", "Land Use Rights Certificate (LURC)", "Sổ đỏ / Sổ hồng", "asean_vn", "越南国家签发证明享有土地使用权及地面房屋所有权的法定不动产所有权凭证"],
    ["一次性交租", "Lump-sum Land Rental", "Thuê đất trả tiền một lần", "asean_vn", "外资企业在越拿地唯一允许向银行抵押土地使用权融资的交租方式"],
    ["按年交租", "Annual Land Rental", "Thuê đất trả tiền hàng năm", "asean_vn", "外资企业仅享有租赁权、严禁将土地使用权物权向银行抵押融资的交租方式"],
    ["海域移交审批", "Sea Area Assignment", "Giao khu vực biển", "asean_vn", "海上风电、光伏浮体电站及取排水码头工程必须向资源环境部申请的海域使用批文"],
    ["快速法定裁决", "Statutory Adjudication", "Adjudikasi Berkanun", "asean_my", "马来CIPAA与新加坡SOPA设立的工程款争议在45~60天内迅速获得具有约束力决定的程序"],
    ["建筑工业发展局", "Construction Industry Development Board", "CIDB", "asean_my", "马来西亚主管承包商资质等级注册(G1~G7)与建筑征费的法定监管机构"],
    ["防阻原则", "Prevention Principle", "Prinsip Pencegahan", "asean_all", "发包人阻碍承包商施工且未依约顺延工期时，工期变为无约束(Time at Large)的普通法原则"],
    ["工期变为无约束", "Time at Large", "Masa Terbuka", "asean_all", "因发包人阻碍导致原完工日失效，承包商仅须在合理时间内完工，发包人丧失LD扣除权"],
    ["小股东压迫救济", "Oppression of Minority", "Penindasan Minoriti", "asean_my", "马来公司法第346条与新加坡第216条保护合资中资股东免受控股外方侵害的诉权"],
    ["土著股权配额", "Bumiputera Equity Policy", "Dasar Ekuiti Bumiputera", "asean_my", "马来西亚政府特许项目强制要求30%~51%股份由本土马来土著持有的政策"],
    ["显失公平止付标准", "Unconscionability Exception", "Pengecualian Ketidakpatutan", "asean_sg", "新加坡终审法院确立的以明显不当或恶意施压为由司法止付独立保函的标准"],
    ["真实预估损失", "Genuine Pre-estimate of Loss", "Anggaran Kerugian Tulen", "asean_sg", "新加坡法下判定违约金条款有效而非惩罚性罚金(Penalty)的严格判定标准"],
    ["目的适用性严格责任", "Fitness for Purpose", "Kesesuaian untuk Tujuan", "asean_fidic", "黄皮书与银皮书下EPC承包商必须保证设计与建造成果完全满足雇主功能要求的严格责任"],
    ["不可预见物质条件", "Unforeseeable Physical Conditions", "Keadaan Fizikal Tidak Terduga", "asean_fidic", "红/黄皮书第4.12款赋予承包商索赔地下异常地质工期与费用的核心请求权基础"],
    ["商定与确定", "Agreement and Determination", "Persetujuan dan Penentuan", "asean_fidic", "FIDIC工程师或雇主代表公正裁量工期与费用的程序，2017版增设42天时限"],
    ["争端避免裁决委员会", "Dispute Avoidance/Adjudication Board", "Lembaga Pertikaian", "asean_fidic", "FIDIC第20/21章常设或特设由1~3名独立专家组成的争议快速解决前置机构"],
    ["承揽工程编", "Hire of Work", "Jang Tham Khong", "asean_th", "泰国民商法典第七章关于包工包料承揽合同权利义务与风险划分的专门法典"],
    ["外商经营许可证", "Foreign Business License (FBL)", "Bai Anuyat Prakop Thurakit", "asean_th", "外国人在泰国从事受限建筑或服务行业必须向商业发展厅申领的准入许可"],
    ["投资促进委员会", "Board of Investment (BOI)", "Kha-na Kam-ma-kan Song-soem", "asean_th", "泰国主管提供100%外资独资豁免、免征企业所得税与永久购地特权的部级机构"],
    ["地上权", "Right of Superficies", "Sitthi Nuea Thi Din", "asean_th", "泰国法下在租赁土地上合法独立建造、持有电站厂房物权长达30年的法定物权形式"],
    ["短消灭时效", "Short Prescription (2 Years)", "Ayu Khwam 2 Pi", "asean_th", "泰国CCC第193/34条规定的承揽人追索工程款必须在2年内立案起诉的除斥期间"],
    ["建筑业仲裁委员会", "Construction Industry Arbitration Commission", "CIAC", "asean_ph", "菲律宾法律赋予其对境内一切建设工程争议享有法定原始且排他管辖权的专门机构"],
    ["反傀儡法", "Anti-Dummy Law", "Batas Laban sa Dummy", "asean_ph", "菲律宾严厉打击外商使用挂名菲籍人代持股权或插手受限公用事业管理的刑法"],
    ["祖父穿透原则", "Grandfather Rule", "Panuntunan ng Ninuno", "asean_ph", "菲律宾证监会穿透审查多层合资公司中资实际综合持股比例是否突破40%上限的规则"],
    ["承包商执照法", "Contractors License Law", "Batas sa Lisensya ng Kontratista", "asean_ph", "菲律宾RA 4566号法案，要求进场施工必须取得PCAB资质执照，已被最高院废除外资歧视"],
    ["15年结构倒塌连带责任", "15-Year Collapse Liability", "Pananagutan sa Pagguho 15 Taon", "asean_ph", "菲律宾民法典第1723条规定的工程移交后15年内建筑物倒塌工程师总包终身连带赔偿"],
    ["变更无定价不赔铁律", "No Written Price No Pay", "Walang Nakasulat Walang Bayad", "asean_ph", "菲律宾民法典第1724条规定固定总价工程无书面定价协议变更款绝对归零铁律"],
    ["自由事先知情同意", "Free and Prior Informed Consent", "FPIC", "asean_ph", "涉原住民祖传领地(CADT)项目开工前必须履行的全体部落村民法定知情同意程序"],
    ["国家重大基建禁令排除", "No-TRO Law on National Infrastructure", "Bawal TRO sa Proyektong Pambansa", "asean_ph", "菲律宾RA 8975号法案明文禁止下级地方法院对国家重点基础设施工程签发停工令"],
    ["间接征收", "Indirect Expropriation", "Pengambilalihan Tidak Langsung", "treaty", "东道国政府出台监管政策实质性剥夺外国投资者合法投资价值构成国际法征收赔偿"],
    ["公允市场价值", "Fair Market Value (FMV)", "Nilai Pasar Wajar", "treaty", "国际投资协定规定的对征收资产进行及时、有效、充分补偿的法定资产评估定价标准"],
    ["国民待遇", "National Treatment (NT)", "Perlakuan Nasional", "treaty", "东道国给予外国投资者的待遇不得低于本国投资者在同等条件下的待遇标准"],
    ["最惠国待遇", "Most-Favoured-Nation (MFN)", "Perlakuan Negara Paling Disukai", "treaty", "东道国给予外国投资者的待遇不得低于给予任何第三方国家投资者的优惠待遇标准"],
    ["公平公正待遇", "Fair and Equitable Treatment (FET)", "Perlakuan Adil dan Setara", "treaty", "保护投资者合法合理投资期待、禁止东道国政府专断、缺乏透明度或否定司法的国际法标准"],
    ["投资者与国家间争端解决", "Investor-State Dispute Settlement", "ISDS", "treaty", "赋予外国私人投资者直接将东道国政府起诉至国际仲裁庭寻求巨额赔偿的直诉机制"],
    ["国际投资争端解决中心", "ICSID", "Pusat Antarabangsa Pertikaian Pelaburan", "treaty", "世界银行下设的投资争端仲裁机构，越、泰非缔约国须转走UNCITRAL仲裁规则"],
    ["联合国国际贸易法委员会", "UNCITRAL Arbitration Rules", "Peraturan Timbang Tara UNCITRAL", "treaty", "国际商事与投资条约仲裁通用规则，常由海牙常设仲裁院(PCA)担任注册管理机构"],
    ["利益拒绝条款", "Denial of Benefits Clause", "Klausa Penafian Faedah", "treaty", "ACIA第19条允许东道国拒绝给予未在设立国开展实质商业经营的空壳SPV协定保护"],
    ["常设机构", "Permanent Establishment (PE)", "Bentuk Usaha Tetap (BUT)", "treaty", "双边税收协定中外国工程在东道国施工超过6个月构成常设机构并纳税的实体标准"],
    ["预提所得税", "Withholding Tax (WHT)", "Pajak Penghasilan Potong/Pungut", "treaty", "跨国支付股息、利息、特许权使用费时依税收协定由支付方代扣代缴的税款"],
    ["见索即付独立保函", "Demand Guarantee", "Garansi Bank Tuntutan Pertama", "asean_fidic", "只要受益人出具符合保函表面文本要求的违约声明开证行必须无条件兑付的担保"],
    ["出险报损30日时限", "30-Day Loss Notification", "Pemberitahuan Kerugian 30 Hari", "treaty", "中信保特险保单要求被保险人必须在政治风险或商事违约发生30日内发函报损的时限"],
    ["超股比担保禁止", "Prohibition on Excess Guarantee", "Larangan Jaminan Berlebihan", "prc_sasac", "国资委75号文严禁中央企业为参股项目提供超过自身持股比例的任何形式连带保证"],
    ["数据出境审批", "Cross-Border Data Transfer Approval", "Kelulusan Pemindahan Data", "prc_sasac", "中国数据安全法第36条规定向境外司法或仲裁机构提供境内数据必须履行的审批程序"],
    ["母公司完工担保", "Parent Company Guarantee (PCG)", "Jaminan Syarikat Induk", "asean_all", "中资母公司为境外项目子公司或联营体向业主出具的保证工程按期保质完工的担保函"],
    ["不可抗力事件", "Force Majeure", "Keadaan Memaksa", "asean_all", "不能预见、不能避免并不能克服的客观情况，赋予受阻方免除工期违约责任的法定事由"],
    ["法定留置权", "Mechanic's Lien", "Hak Retensi", "asean_all", "因工程款未付对现场施工机械或建筑材料享有的法定留置优先受偿权，英美法系新马无土地留置权"],
    ["浮动抵押", "Floating Charge", "Cagaran Terapung", "asean_my", "对公司现存及未来全部流动资产设定的担保物权，违约或清盘时转化为固定抵押"],
    ["托伦斯土地登记", "Torrens Title System", "Sistem Hakmilik Torrens", "asean_sg", "新加坡与马来西亚采用的不动产产权以政府土地局登记为最终不可推翻公信力的登记制"],
    ["工程预付款保函", "Advance Payment Guarantee", "Jaminan Bayaran Pendahuluan", "asean_fidic", "担保总包商将业主支付的预付款专项用于工程实施并在进度款中按比例扣回的银行保函"],
    ["保留金返还", "Release of Retention Money", "Pelepasan Wang Tahanan", "asean_fidic", "在颁发接收证书(TOC)与缺陷责任期满颁发履约证书(PC)时分批退还业主的扣留款项"],
    ["缺陷通知期", "Defects Notification Period (DNP)", "Tempoh Pemberitahuan Kecacatan", "asean_fidic", "移交后承包商承担缺陷修补法定义务的保修期限，FIDIC银皮书通常为移交后1~2年"],
    ["工程接收证书", "Taking-Over Certificate (TOC)", "Perakuan Pengambilalihan", "asean_fidic", "证明工程或单位工程已实质性竣工并满足接收条件的官方凭证，切断迟延违约金计算"],
    ["履约证书", "Performance Certificate", "Perakuan Siap Kerja", "asean_fidic", "缺陷责任期满由工程师签署的确认承包商已完全履行全部合同义务的最终证明文件"],
    ["终止估价", "Valuation at Date of Termination", "Penilaian pada Tarikh Penamatan", "asean_fidic", "合同因违约或便利终止后，双方核算已完工程价值、材料设备款与损失赔偿额的结算程序"],
    ["便利终止权", "Termination for Convenience", "Penamatan untuk Keselesaan", "asean_fidic", "雇主单方非因承包商违约而解除合同的权利，严禁雇主为转包他人或自己实施而滥用"],
    ["反仲裁禁令", "Anti-Arbitration Injunction", "Injunksi Anti-Timbang Tara", "asean_my", "法院对非仲裁协议签署方或恶意滥用仲裁程序的当事人签发的阻止仲裁程序继续进行的禁令"],
    ["资产冻结禁令", "Mareva Injunction / Freezing Order", "Perintah Pembekuan Mareva", "asean_sg", "法院签发的在判决或仲裁裁决作出前冻结被申请人银行账户或核心不动产的临时禁令"],
    ["财产保全", "Interim Measure / Asset Preservation", "Tindakan Sementara", "asean_all", "仲裁庭或法院在实体审理期间为防止财产隐匿转移而采取的紧急查封扣押措施"],
    ["执行地法院审查", "Enforcement Court Review", "Semakan Mahkamah Pelaksanaan", "asean_all", "依据《纽约公约》第五条在被执行财产所在地法院对涉外仲裁裁决合法性进行的有限抗辩审查"],
    ["公共政策保留", "Public Policy Defense", "Pembelaan Dasar Awam", "asean_all", "执行地法院以仲裁裁决严重抵触本国基本法律道德准则为由拒绝承认与执行裁决的最终防线"],
    ["国际贸易法委员会仲裁", "UNCITRAL Arbitration", "Timbang Tara UNCITRAL", "treaty", "联合国国际贸易法委员会制定的国际投资与商事仲裁程序法规则"],
    ["常设仲裁院", "Permanent Court of Arbitration (PCA)", "Mahkamah Timbang Tara Tetap", "treaty", "位于海牙的国际争端解决组织，常为 UNCITRAL 条约仲裁提供登记处管理服务"],
    ["最惠国待遇借道适用", "MFN Clause Treaty Shopping", "Penggunaan MFN Merentas Perjanjian", "treaty", "投资者企图通过最惠国待遇条款引入第三方更为宽松的仲裁管辖程序，受国际仲裁严格审查"],
    ["合法合理期待", "Legitimate Expectations", "Jangkaan Sah", "treaty", "国际投资法公平公正待遇(FET)的核心，东道国不可背弃向投资者做出的特定政策承诺"],
    ["直接诉权", "Direct Action", "Tindakan Terus", "asean_ph", "分包商或材料供应商对发包人未付给总包商的工程款余额依法直接向发包人起诉受偿的权利"],
    ["特许经营协议", "Concession Agreement", "Perjanjian Konsesi", "asean_all", "东道国政府授予投资人投资建设并运营高速公路、水厂或电站并收取费用的法定协议"],
    ["购电协议", "Power Purchase Agreement (PPA)", "Perjanjian Pembelian Kuasa", "asean_all", "发电项目公司与东道国国家电网公司签署的长达20~30年的购售电兜底长协"],
    ["最低收入保证", "Minimum Revenue Guarantee (MRG)", "Jaminan Pendapatan Minimum", "asean_vn", "PPP特许经营中政府承诺当实际车流量或售电量低于基准模型时给予财政补贴的机制"],
    ["主权违约担保", "Sovereign Default Guarantee", "Jaminan Kemungkiran Kerajaan", "asean_id", "印尼基建担保基金(IIGF/PT PII)对政府机构在PPP合同中的履约承诺提供的财政兜底担保"],
    ["空间规划利用合规", "Spatial Planning Compliance", "KKPR / KKPRL", "asean_id", "印尼投资拿地必须首要取得的陆地或海域空间规划利用合规确认许可批文"],
    ["环境影响评价报告", "Environmental Impact Assessment (EIA)", "AMDAL", "asean_id", "重大电站与基建工程开工前必须经环境与林业部审批的最高等级环评准入报告"],
    ["施工许可证", "Building Construction Permit (PBG)", "Persetujuan Bangunan Gedung", "asean_id", "替代原IMB，印尼工程在开工前必须取得的符合技术标准的法定建筑施工许可"],
    ["合格外籍劳工配额", "Foreign Manpower Utilization Plan", "RPTKA", "asean_id", "中资总承包商委派中方管理与技术人员赴印尼工地必须经劳工部批准的用工方案"],
    ["居留与工作签证", "Temporary Stay Permit", "KITAS / ITAS", "asean_id", "外国专家在东道国工程现场合法居住并进行施工作业的居留与工作许可卡"],
    ["属地劳工连带责任", "Solidary Liability for Labor", "Tanggungjawab Bersama Gaji Buruh", "asean_th", "泰国与菲律宾法律规定总承包商对分包商拖欠工人工资承担100%法定连带垫付责任"],
    ["非法罢工阻工", "Illegal Strike", "Mogok Kerja Tidak Sah", "asean_id", "未履行提前7天法定书面通知程序发起的封锁工地大门罢工，依法不享有免责"],
    ["设备原产地证明", "Certificate of Origin (COO)", "Sijil Asal Usul (Form E / RCEP)", "treaty", "用于在海关清关时享受中国-东盟自由贸易区零关税或优惠关税待遇的法定原产地单证"],
    ["设备免税主清单", "Masterlist Import Duty Facility", "Fasilitas Masterlist Bea Masuk", "asean_id", "经投资协调委员会(BKPM)批准的投资项目进口机器设备全额免征关税与进口增值税批文"],
    ["二手资本货物进口批文", "Used Capital Goods Import License", "Persetujuan Impor Barang Modal Bukan Baru", "asean_id", "印尼贸易部核发允许进口非全新工程施工机械设备(吊车/盾构机)的特殊配额批文"],
    ["离岸设备在岸施工拆分", "Offshore / Onshore Contract Split", "Pemisahan Kontrak Luar / Dalam Negeri", "asean_all", "将EPC工程拆分为离岸设备供应FOB与在岸工程施工安装以合法平抑东道国承包商税的架构"],
    ["转让定价同期资料", "Transfer Pricing Documentation (TP Doc)", "Dokumentasi Harga Pindahan", "asean_all", "跨国母子公司之间发生关联设备供货或技术咨询交易必须编制的符合独立交易原则的税务档案"],
    ["资本金实缴时限", "Charter Capital Contribution Timeline", "Thời hạn góp vốn điều lệ", "asean_vn", "越南企业法要求外资公司注册资本必须在投资许可证核发后90天内一次性足额汇入实缴"],
    ["外债借贷登记", "Offshore Loan Registration", "Đăng ký khoản vay nước ngoài", "asean_vn", "境外母公司向越南项目子公司提供超过1年的中长期借款必须在国家银行(SBV)履行的登记程序"],
    ["强制本币结算令", "Mandatory Local Currency Rule", "Kewajiban Penggunaan Rupiah (PBI)", "asean_id", "印尼央行要求境内一切现钞与非现钞商业结算必须强制使用印尼盾的监管法令"],
    ["外汇利润汇出审查", "Profit Repatriation Review", "Semakan Penghantaran Balik Keuntungan", "asean_ph", "菲律宾与泰国央行要求将外汇投资本金与合法利润汇回国内前必须出具完税证明的审查"],
    ["反洗钱合规审查", "Anti-Money Laundering (AML)", "Pencegahan Pengubahan Wang Haram", "asean_all", "跨国工程资金往来必须接受开户银行进行的资金合法来源与受益所有人(BO)尽职调查"],
    ["国际制裁实体清单", "International Sanctions List", "Senarai Sekatan Antarabangsa", "treaty", "世界银行黑名单、OFAC制裁清单，凡涉及被制裁实体可能导致保函被冻结及融资违约"],
    ["合规免责证明", "Compliance Safe Harbor", "Pelabuhan Selamat Pematuhan", "asean_all", "证明企业已建立完备的合规管理体系以在发生员工违规时免除企业主体刑责的制度"],
    ["不可预见自然力", "Unforeseeable Natural Forces", "Kuasa Alam Tidak Terduga", "asean_fidic", "百年一遇特大暴雨、海啸等超出合同基准日合理预见范围并赋予工期费用补偿的自然力事件"],
    ["汇率风险对冲", "Foreign Exchange Hedging", "Lindung Nilai Pertukaran Asing", "asean_all", "利用远期结售汇合约或货币掉期规避东盟属地货币汇率大幅贬值导致工程亏损的金融工具"],
    ["暂列金额", "Provisional Sums", "Wang Peruntukan Sementara", "asean_fidic", "列入合同价格中用于实施某项不可预见工程或材料采购的准备金，须经工程师指令方可支出"],
    ["计日工", "Daywork", "Kerja Harian", "asean_fidic", "按预先商定的工料机日费率对临时紧急或难以计量的变更工作进行实报实销计价的机制"],
    ["工程变更指令", "Variation Order (VO)", "Arahan Perubahan Kerja", "asean_fidic", "工程师或雇主正式签发的增加、删减或变更工程设计与施工方案的书面指令文件"],
    ["价值工程建议", "Value Engineering (VE)", "Kejuruteraan Nilai", "asean_fidic", "承包商提出的优化施工方案并节约造价的建议，FIDIC规定节约额的50%作为奖励支付给承包商"],
    ["提前竣工奖金", "Bonus for Early Completion", "Bonus Penyiapan Awal", "asean_fidic", "合同约定的工程每提前一天竣工由雇主向承包商支付固定奖金以激励加速施工的条款"],
    ["履约保函减额", "Reduction of Performance Security", "Pengurangan Jaminan Prestasi", "asean_fidic", "在颁发部分工程接收证书(TOC)后按比例相应调减履约保函担保金额的合同机制"],
    ["双重征税协定常设机构", "DTA Permanent Establishment", "BUT Perjanjian Cukai Dua Kali", "treaty", "工程跨国施工持续时间判定是否构成东道国常设机构并开征企业所得税的双边协定规则"],
    ["关联方借款利息扣除上限", "Thin Capitalization Rules", "Had Potongan Faedah Pinjaman Sekutu", "asean_all", "东盟税法规定的企业向境外母公司支付借贷利息在税前扣除的债资比(Debt-to-Equity)限制"],
    ["原住民祖传领地", "Ancestral Domain", "Lupaing Ninuno (CADT)", "asean_ph", "受菲律宾宪法保护的原住民族依法享有的对其传统部落土地拥有的不可分割所有权与自治权"],
    ["特权留置顺位", "Privileged Liens Priority", "Keutamaan Hak Istimewa", "asean_id", "印尼民法典第1139条确立的仓储运输、设备维修及工程承包款优先于普通无担保债权的受偿顺位"]
]

with open("kb/asean/glossary.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(glossary_data)
print(f"kb/asean/glossary.csv written with {len(glossary_data)} items.")
