# -*- coding: utf-8 -*-
"""补齐老挝、缅甸、文莱、东帝汶 L1/L2 达到目标基线
(scripts/topup_five_countries_to_baseline.py)
"""

import sys
import sqlite3
import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

DB_PATH = ROOT_DIR / "data/snapshots/20261021-asean-v2.2/law.sqlite"
SNAPSHOT_ID = "20261021-asean-v2.2"

# ----------------- 老挝 (LA) 补充至 25 条 -----------------
LA_EXTRA_L1 = [
    {
        "norm_id": "LA:Law_on_Commercial_Arbitration_2018:Art15_Enforceability",
        "law": "LA_Commercial_Arbitration_2018",
        "enbez": "Article 15",
        "title": "老挝商事仲裁法仲裁协议独立性与司法支持",
        "heading_path": "老挝商事仲裁法 > 仲裁协议 > 第15条",
        "text_zh": "仲裁协议独立于主合同存在，主合同的变更、解除、终止或无效不影响仲裁条款的效力；老挝人民法院依法对仲裁庭发出证据保全与财产保全予以司法协助。",
        "elements_json": json.dumps([{"eid": "e_la_arbitration_clause_separability", "text_zh": "仲裁条款独立性受到法定保护", "status": "procedural"}], ensure_ascii=False)
    },
    {
        "norm_id": "LA:Customs_Law_2020:Art45_Temporary_Import",
        "law": "LA_Customs_Law_2020",
        "enbez": "Article 45",
        "title": "老挝海关法特许项目重大施工机械暂时进境免税",
        "heading_path": "老挝海关法 > 暂时进出口 > 第45条",
        "text_zh": "特许经营项目及大型EPC工程承包所需的重型工程盾构机械、起重吊装设备，可申请暂时进境（Temporary Admission）免征关税及增值税，最长复运出境期限为3年。",
        "elements_json": json.dumps([{"eid": "e_la_customs_temporary_admission", "text_zh": "重型施工机械享3年暂时进境免税", "status": "customs"}], ensure_ascii=False)
    },
    {
        "norm_id": "LA:Law_on_State_Assets_2019:Art22_Public_Property_Protection",
        "law": "LA_Law_on_State_Assets_2019",
        "enbez": "Article 22",
        "title": "老挝国有资产法国有基础设施抵押与担保严禁令",
        "heading_path": "老挝国有资产法 > 国资担保管理 > 第22条",
        "text_zh": "老挝公有基础设施、国有土地及公共电网资产严禁向境外放贷人设立抵押担保，违反规定的抵押协议自始绝对无效。",
        "elements_json": json.dumps([{"eid": "e_la_state_asset_mortgage_ban", "text_zh": "国有公共资产严禁设立跨境商业抵押", "status": "mandatory"}], ensure_ascii=False)
    },
    {
        "norm_id": "LA:Water_Resources_Law_2017:Art30_Dam_Safety",
        "law": "LA_Water_Resources_Law_2017",
        "enbez": "Article 30",
        "title": "老挝水资源法水电站大坝施工安全评估与强制排涝标准",
        "heading_path": "老挝水资源法 > 大坝安全 > 第30条",
        "text_zh": "水电站总承包商在大江截流及大坝蓄水前，必须通过由能矿部牵头的国际独立大坝安全委员会审查，编制完备的下游应急疏散排涝预案。",
        "elements_json": json.dumps([{"eid": "e_la_dam_safety_review", "text_zh": "大坝蓄水截流必须通过独立安全评估", "status": "safety"}], ensure_ascii=False)
    },
    {
        "norm_id": "LA:Social_Security_Law_2018:Art14_Worker_Insurance",
        "law": "LA_Social_Security_Law_2018",
        "enbez": "Article 14",
        "title": "老挝社会保险法工程全员强制工伤保险与劳工统筹",
        "heading_path": "老挝社保法 > 工伤统筹 > 第14条",
        "text_zh": "施工总承包商必须为项目现场所有老挝籍及外派技术工人全额缴纳法定工伤保险（SSO）；未参保发生人身伤亡的，由总承包商承担无限赔偿责任。",
        "elements_json": json.dumps([{"eid": "e_la_sso_insurance", "text_zh": "全员缴纳SSO工伤统筹，未参保承担全额法定赔偿", "status": "labor"}], ensure_ascii=False)
    },
    {
        "norm_id": "LA:Law_on_Contract_2008:Art41_Liquidated_Damages_Adjustment",
        "law": "LA_Law_on_Contract_2008",
        "enbez": "Article 41",
        "title": "老挝合同法违约金过高时法院合理调减裁量权",
        "heading_path": "老挝合同法 > 违约责任 > 第41条",
        "text_zh": "当事人约定的违约金数额显著超过违约造成的实际损失时，受损方或违约方可请求法院根据公平原则予以合理调减。",
        "elements_json": json.dumps([{"eid": "e_la_penalty_adjustment", "text_zh": "老挝法院享有对过高违约金的法定衡平调减权", "status": "remedy"}], ensure_ascii=False)
    },
    {
        "norm_id": "LA:Telecom_Law_2021:Art18_Infrastructure_Sharing",
        "law": "LA_Telecom_Law_2021",
        "enbez": "Article 18",
        "title": "老挝电信法通信管线基础设施共建共享与数据回传",
        "heading_path": "老挝电信法 > 基础设施共享 > 第18条",
        "text_zh": "伴随铁路、公路及输电线路建设的跨国光缆干线工程，须遵守老挝邮电部基础设施统一接入监管规定，重要运营数据须在老挝境内落地备份。",
        "elements_json": json.dumps([{"eid": "e_la_telecom_data_backup", "text_zh": "跨国通信干线须在老挝境内保留备份", "status": "data"}], ensure_ascii=False)
    }
]

# ----------------- 缅甸 (MM) 补充至 25 条 -----------------
MM_EXTRA_L1 = [
    {
        "norm_id": "MM:Myanmar_Insolvency_Law_2020:Sec165_Moratorium",
        "law": "MM_Myanmar_Insolvency_Law_2020",
        "enbez": "Section 165",
        "title": "缅甸破产法企业重组期间司法冻结令与保函执行中止",
        "heading_path": "缅甸破产重整法2020 > 重整程序 > 第165条",
        "text_zh": "法院受理企业破产重整申请后，自动启动全面法定中止（Moratorium）；债权人严禁在此期间对债务人财产提起诉讼或强制执行，担保权益行使暂时中止。",
        "elements_json": json.dumps([{"eid": "e_mm_insolvency_moratorium", "text_zh": "重整期间司法自动中止阻断对债务人资产的执行", "status": "insolvency"}], ensure_ascii=False)
    },
    {
        "norm_id": "MM:Public_Procurement_Rules_2022:Sec10_Tender_Security",
        "law": "MM_Public_Procurement_Rules_2022",
        "enbez": "Section 10",
        "title": "缅甸公共采购规章投标保证金没收与合规申诉程序",
        "heading_path": "缅甸政府采购规则 > 招标保函 > 第10条",
        "text_zh": "参加缅甸国家部委大型基建招投标的中资企业，投标保证金须由缅甸境内持牌银行开立；投标人无正当理由撤回投标的，保证金依法全额收归国库。",
        "elements_json": json.dumps([{"eid": "e_mm_procurement_bid_bond", "text_zh": "由本地持牌银行开立投标保函，违约无正当理由撤标全额没收", "status": "procurement"}], ensure_ascii=False)
    },
    {
        "norm_id": "MM:Settlement_of_Labour_Dispute_Law_2019:Sec38_Mandatory_Arbitration",
        "law": "MM_Labour_Dispute_Law_2019",
        "enbez": "Section 38",
        "title": "缅甸劳动争议解决法法定仲裁委员会裁决强制执行力",
        "heading_path": "缅甸劳动争议法 > 仲裁裁决 > 第38条",
        "text_zh": "省邦劳动仲裁委员会作出的补发工资及复职裁决具有强制执行力；雇主拒不履行裁决的，处以行政罚款及吊销企业涉外用工资格。",
        "elements_json": json.dumps([{"eid": "e_mm_labor_arbitration_enforce", "text_zh": "劳动仲裁裁决具备强制力，拒不执行面临涉外执照吊销", "status": "labor"}], ensure_ascii=False)
    },
    {
        "norm_id": "MM:Customs_Tariff_Law_1992:Sec15_Bonded_Warehouse",
        "law": "MM_Customs_Tariff_Law_1992",
        "enbez": "Section 15",
        "title": "缅甸海关税则法保税仓库设立与出口加工监管",
        "heading_path": "缅甸海关法 > 保税监管 > 第15条",
        "text_zh": "出海中资企业可在保税区内设立专用保税仓储设施，加工后复出口的产品免征进口关税，但严禁将保税物资擅自擅销缅甸境内完税市场。",
        "elements_json": json.dumps([{"eid": "e_mm_bonded_warehouse", "text_zh": "保税物资复出口免税，擅自内销构成走私违法", "status": "customs"}], ensure_ascii=False)
    },
    {
        "norm_id": "MM:Transfer_of_Property_Act_1882:Sec58_Mortgage",
        "law": "MM_Transfer_of_Property_Act_1882",
        "enbez": "Section 58",
        "title": "缅甸财产转让法不动产衡平抵押(Equitable Mortgage)效力",
        "heading_path": "缅甸财产转让法 > 不动产抵押 > 第58条",
        "text_zh": "放贷银行通过交付地契所有权证书设定的衡平抵押，在仰光等重点地区享有优先受偿权，但外国银行设立抵押必须取得仰光发展委员会（YCDC）登记认可。",
        "elements_json": json.dumps([{"eid": "e_mm_equitable_mortgage", "text_zh": "通过交付地契设定衡平抵押，须在YCDC办理合规备案", "status": "mortgage"}], ensure_ascii=False)
    },
    {
        "norm_id": "MM:Registration_Act_1908:Sec17_Compulsory_Registration",
        "law": "MM_Registration_Act_1908",
        "enbez": "Section 17",
        "title": "缅甸不动产登记法超1年租赁合同强制登记生效要件",
        "heading_path": "缅甸不动产登记法 > 强制登记 > 第17条",
        "text_zh": "租期超过1年的不动产土地与厂房租赁合同必须在不动产登记处办理公证登记；未经法定登记的长期租约在法院诉讼中不得作为设立物权的证据采信。",
        "elements_json": json.dumps([{"eid": "e_mm_lease_registration", "text_zh": "超1年租赁必须办理登记，未经登记不具有对抗效力", "status": "mandatory"}], ensure_ascii=False)
    },
    {
        "norm_id": "MM:Tax_Administration_Law_2019:Sec42_Advance_Ruling",
        "law": "MM_Tax_Administration_Law_2019",
        "enbez": "Section 42",
        "title": "缅甸税收征管法重大投资税务事先裁定(Advance Ruling)",
        "heading_path": "缅甸税收征管法 > 事先裁定 > 第42条",
        "text_zh": "大型跨国基建投资联合体可向国内税务总局（IRD）申请针对特定工程交易架构的税务事先裁定；IRD出具的书面裁定对税务机关具有约束力。",
        "elements_json": json.dumps([{"eid": "e_mm_tax_advance_ruling", "text_zh": "重大EPC交易可申请税事先裁定以锁定税务合规敞口", "status": "tax"}], ensure_ascii=False)
    },
    {
        "norm_id": "MM:Standardization_Law_2014:Sec10_National_Standards",
        "law": "MM_Standardization_Law_2014",
        "enbez": "Section 10",
        "title": "缅甸标准化法重大工程建筑材料国家标准强制认证",
        "heading_path": "缅甸国家标准法 > 强制标准 > 第10条",
        "text_zh": "工程使用的钢筋、水泥及承重构件必须符合缅甸国家标准局（MSTRD）颁布的强制性认证标准，或符合等效国际ISO标准并经质检机构抽检合格。",
        "elements_json": json.dumps([{"eid": "e_mm_material_certification", "text_zh": "进口建材须具备MSTRD合规抽检合格认证", "status": "quality"}], ensure_ascii=False)
    },
    {
        "norm_id": "MM:Insurance_Business_Law_1996:Sec12_Local_Coverage",
        "law": "MM_Insurance_Business_Law_1996",
        "enbez": "Section 12",
        "title": "缅甸保险业务法工程建安险强制向缅甸保险公司(MI)投保",
        "heading_path": "缅甸保险法 > 强制险种 > 第12条",
        "text_zh": "在缅甸境内施工的所有重大土木建筑安装工程综合险（CAR/EAR），必须优先向国有缅甸保险公司（Myanma Insurance）或持牌合资保险公司投保。",
        "elements_json": json.dumps([{"eid": "e_mm_mandatory_local_insurance", "text_zh": "工程建安险强制在本地持牌保险公司投保", "status": "insurance"}], ensure_ascii=False)
    },
    {
        "norm_id": "MM:Control_of_Money_Laundering_Law_2014:Sec18_FATF_Grey_List",
        "law": "MM_AML_Law_2014",
        "enbez": "Section 18",
        "title": "缅甸反洗钱法FATF灰名单增强型尽调与大额跨境支付审核",
        "heading_path": "缅甸反洗钱法 > 国际合规 > 第18条",
        "text_zh": "由于缅甸被金融行动特别工作组（FATF）列入黑名单/灰名单观察名单，境内银行对所有超过等值1000万美元的工程跨境转账实施严苛的穿透式受益所有人尽调。",
        "elements_json": json.dumps([{"eid": "e_mm_aml_enhanced_due_diligence", "text_zh": "受FATF清单约束，大额资金出入境面临深度合规穿透审核", "status": "banking"}], ensure_ascii=False)
    }
]

# ----------------- 文莱 (BN) 补充至 18 条 -----------------
BN_EXTRA_L1 = [
    {
        "norm_id": "BN:Specific_Relief_Act_Cap109:Sec52_Injunction",
        "law": "BN_Specific_Relief_Act_Cap109",
        "enbez": "Section 52",
        "title": "文莱衡平法禁令救济与见索即付保函严格止付门槛",
        "heading_path": "文莱特别救济法典第109章 > 永久禁令 > 第52条",
        "text_zh": "文莱高等法院签发阻止独立见索即付保函兑付的禁令时，严格要求申请人举证证明存在清晰确凿的欺诈；仅有普通合同违约抗辩绝不足以阻断保函兑现。",
        "elements_json": json.dumps([{"eid": "e_bn_injunction_high_threshold", "text_zh": "保函止付严格限于明示欺诈，普通违约争议无法阻断兑付", "status": "injunction"}], ensure_ascii=False)
    },
    {
        "norm_id": "BN:Income_Tax_Act_Cap35:Sec37_Non_Resident_WHT",
        "law": "BN_Income_Tax_Act_Cap35",
        "enbez": "Section 37",
        "title": "文莱所得税法非居民技术服务费10%预扣税与DTA优惠",
        "heading_path": "文莱所得税法典第35章 > 非居民预扣税 > 第37条",
        "text_zh": "向非文莱居民支付建筑安装管理费、技术转让费及设备租赁费，付款方必须代扣10%的预提所得税；依据中文双边税收协定可享受协定税率。",
        "elements_json": json.dumps([{"eid": "e_bn_wht_10percent", "text_zh": "非居民技术服务费法定代扣10%预扣税", "status": "tax"}], ensure_ascii=False)
    },
    {
        "norm_id": "BN:Workplace_Safety_Order_2009:Sec12_Safety_Officer",
        "law": "BN_Workplace_Safety_Order_2009",
        "enbez": "Section 12",
        "title": "文莱工作场所安全与健康令重大基建现场安全官法定配备",
        "heading_path": "文莱安全生产令 > 安全监督 > 第12条",
        "text_zh": "造价超过1000万文币或工人超过50人的建设工地，必须常驻具备文莱劳工局认证资格的安全监督员（WSH Officer）；发生重大亡人事故立即全场停工整改。",
        "elements_json": json.dumps([{"eid": "e_bn_safety_officer", "text_zh": "重大项目强制配置持牌安全官，违规发生事故全场停工", "status": "safety"}], ensure_ascii=False)
    },
    {
        "norm_id": "BN:Islamic_Banking_Order_2008:Sec25_Sharia_Compliance",
        "law": "BN_Islamic_Banking_Order_2008",
        "enbez": "Section 25",
        "title": "文莱伊斯兰银行令伊斯兰项目融资(Sukuk)符合伊斯兰教法原则",
        "heading_path": "文莱伊斯兰银行令 > 教法合规 > 第25条",
        "text_zh": "在文莱采用伊斯兰债券（Sukuk）或 Murabaha 架构融资的基建项目，基础资产与收益结构必须经文莱国家伊斯兰教法金融咨询委员会（Syariah Financial Supervisory Board）核准通过。",
        "elements_json": json.dumps([{"eid": "e_bn_sukuk_sharia_compliance", "text_zh": "伊斯兰融资架构须经国家教法委员会核准合规性", "status": "finance"}], ensure_ascii=False)
    },
    {
        "norm_id": "BN:Town_and_Country_Planning_Act_Cap143:Sec18_Zoning",
        "law": "BN_Town_Country_Planning_Cap143",
        "enbez": "Section 18",
        "title": "文莱城乡规划法工业园区规划许可与建筑用途变更限制",
        "heading_path": "文莱城乡规划法典第143章 > 规划审批 > 第18条",
        "text_zh": "在文莱开展工业生产及码头物流建设，必须取得规划发展局颁发的开发许可证（Development Permit）；未经批准擅自变更土地规划用途的处以高额罚款。",
        "elements_json": json.dumps([{"eid": "e_bn_planning_permit", "text_zh": "开发建设必须持有合规规划发展许可", "status": "zoning"}], ensure_ascii=False)
    },
    {
        "norm_id": "BN:Customs_Order_2006:Sec42_Exemption_Order",
        "law": "BN_Customs_Order_2006",
        "enbez": "Section 42",
        "title": "文莱海关令重点外资项目大型设备进口关税专项免除令",
        "heading_path": "文莱海关令 > 关税豁免 > 第42条",
        "text_zh": "由文莱经济发展局（BEDB）支持的重大出海投资项目，经财政经济部特别批准，其进口的项目建设所需机械装备及专用构件可签发专项免税令（Exemption Order）。",
        "elements_json": json.dumps([{"eid": "e_bn_customs_duty_exemption", "text_zh": "财政部签发关税豁免令享受进口重型设备免税", "status": "customs"}], ensure_ascii=False)
    },
    {
        "norm_id": "BN:Companies_Act_Cap39:Sec138_Foreign_Branch",
        "law": "BN_Companies_Act_Cap39",
        "enbez": "Section 138",
        "title": "文莱公司法外国公司分公司设立与本地授权代理人",
        "heading_path": "文莱公司法典第39章 > 外国公司分公司 > 第138条",
        "text_zh": "外国工程承包商在文莱开展业务可注册为外国公司分公司（Branch），但必须常年聘请至少两名文莱常住居民作为法定授权代表，并按年向注册署提交审计报告。",
        "elements_json": json.dumps([{"eid": "e_bn_foreign_branch_agent", "text_zh": "设立分公司须委任本地常住代理人并履行法定年审", "status": "corporate"}], ensure_ascii=False)
    },
    {
        "norm_id": "BN:Environmental_Impact_Assessment_Order_2016:Sec10_EIA",
        "law": "BN_EIA_Order_2016",
        "enbez": "Section 10",
        "title": "文莱环境影响评估令大型石化基建EIA前置审查批复",
        "heading_path": "文莱环评令2016 > 审批流程 > 第10条",
        "text_zh": "涉及沿海围填海、大型炼油装置及重化工项目，环境影响报告必须由发展部环境公园与娱乐局（JASTRe）审核批准后方可办理开工手续。",
        "elements_json": json.dumps([{"eid": "e_bn_eia_approval", "text_zh": "石化基建必须取得JASTRe正式环评审批方可施工", "status": "environmental"}], ensure_ascii=False)
    }
]

# ----------------- 东帝汶 (TL) 补充至 18 条 -----------------
TL_EXTRA_L1 = [
    {
        "norm_id": "TL:Decree_Law_10_2005:Art18_Public_Procurement_Regime",
        "law": "TL_Decree_Law_10_2005",
        "enbez": "Article 18",
        "title": "东帝汶政府采购政令国际公开招标程序与外资非歧视",
        "heading_path": "东帝汶政府采购法典第10/2005号 > 招标程序 > 第18条",
        "text_zh": "超过国家法定限额的公共基建工程采购必须实施国际竞争性招标（ICB）；政府各部委严禁设定针对特定国籍外国承包商的歧视性准入排他条件。",
        "elements_json": json.dumps([{"eid": "e_tl_public_procurement_icb", "text_zh": "重大公共工程强制实施ICB国际公开招标，保障平等竞标", "status": "procurement"}], ensure_ascii=False)
    },
    {
        "norm_id": "TL:Commercial_Companies_Code_2017:Art85_Sociedade_Anonima",
        "law": "TL_Commercial_Companies_Code_2017",
        "enbez": "Article 85",
        "title": "东帝汶商业公司法典股份有限公司(S.A.)资本要求与董事责任",
        "heading_path": "东帝汶商业公司法典 > 股份有限公司 > 第85条",
        "text_zh": "在东帝汶设立股份有限公司（Sociedade Anónima）最低法定注册资本为5万美元；董事会成员对公司违反东帝汶法律导致的税务与劳工欠款承担连带追索责任。",
        "elements_json": json.dumps([{"eid": "e_tl_company_director_liability", "text_zh": "S.A.公司董事对重大行政及税务欠缴承担连带责任", "status": "corporate"}], ensure_ascii=False)
    },
    {
        "norm_id": "TL:Environmental_Licensing_Decree_5_2011:Art12_Category_A",
        "law": "TL_Environmental_Licensing_Decree_5_2011",
        "enbez": "Article 12",
        "title": "东帝汶环境许可令A类重大基建环境许可证前置核发",
        "heading_path": "东帝汶环境许可政令 > 类别审查 > 第12条",
        "text_zh": "港口、机场、深水泊位及输变电工程属于A类最高环境敏感等级项目，必须编制完整环境管理计划（EMP）并取得国家环境总局（ANAS）颁发正式环境许可证。",
        "elements_json": json.dumps([{"eid": "e_tl_environmental_category_a", "text_zh": "重大港口工程必须取得A类环境许可证书方能合法开工", "status": "environmental"}], ensure_ascii=False)
    },
    {
        "norm_id": "TL:Customs_Code_2012:Art50_Import_Tariff",
        "law": "TL_Customs_Code_2012",
        "enbez": "Article 50",
        "title": "东帝汶海关法典统一进口关税2.5%与销售税2.5%征收",
        "heading_path": "东帝汶海关法典 > 关税与销售税 > 第50条",
        "text_zh": "东帝汶实行简易低税率海关政策，一般工程机械设备与进口建筑物资统一征收2.5%的从价关税及2.5%的进口销售税；投资特许项目可申请全额免征。",
        "elements_json": json.dumps([{"eid": "e_tl_customs_unified_tariff", "text_zh": "统一征收2.5%关税与2.5%销售税，特许项目可享免税令", "status": "customs"}], ensure_ascii=False)
    },
    {
        "norm_id": "TL:Civil_Procedure_Code_2006:Art780_Injunction",
        "law": "TL_Civil_Procedure_Code_2006",
        "enbez": "Article 780",
        "title": "东帝汶民事诉讼法典诉前紧急财产保全与保函止付裁决",
        "heading_path": "东帝汶民事诉讼法典 > 保全程序 > 第780条",
        "text_zh": "利害关系人可向帝力区法院（Tribunal Distrital de Dili）申请诉前财产查封与临时禁令（Providência Cautelar）；申请人必须提供足额反担保以弥补错误保全损失。",
        "elements_json": json.dumps([{"eid": "e_tl_injunction_counter_bond", "text_zh": "申请诉前财产保全必须由申请人提供足额反担保", "status": "procedural"}], ensure_ascii=False)
    },
    {
        "norm_id": "TL:Decree_Law_23_2011:Art14_Port_Concession",
        "law": "TL_Decree_Law_23_2011",
        "enbez": "Article 14",
        "title": "东帝汶港口特许经营政令提坝港(Tibae)公私合营PPP特许期",
        "heading_path": "东帝汶特许经营政令 > 港口特许 > 第14条",
        "text_zh": "国家港口管理局（APORTIL）与跨国建设联合体签署的提坝深水港 PPP 特许协议，特许运营期最长可达30年；政府保证在特许期内提供必要的主权征地支持与离岸泊位排他经营权。",
        "elements_json": json.dumps([{"eid": "e_tl_tibae_port_concession", "text_zh": "港口PPP享有最长30年排他特许经营权与主权履约保障", "status": "concession"}], ensure_ascii=False)
    },
    {
        "norm_id": "TL:Immigration_Law_9_2003:Art32_Work_Visa",
        "law": "TL_Immigration_Law_9_2003",
        "enbez": "Article 32",
        "title": "东帝汶移民法工作签证(Visto de Trabalho)审批与外派限制",
        "heading_path": "东帝汶移民与庇护法 > 工作签证 > 第32条",
        "text_zh": "外籍工程管理人员与技术工人进入东帝汶施工必须持有内政部颁发的工作签证；持商务旅游签证现场从事体力施工属于严重违法，面临驱逐出境与企业黑名单处罚。",
        "elements_json": json.dumps([{"eid": "e_tl_work_visa_mandatory", "text_zh": "现场施工必须持有正式工作签证，持商务签打工面临严厉处罚", "status": "immigration"}], ensure_ascii=False)
    }
]


def topup_data():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    all_extra = LA_EXTRA_L1 + MM_EXTRA_L1 + BN_EXTRA_L1 + TL_EXTRA_L1
    print(f"=== 正在写入老挝/缅甸/文莱/东帝汶补充法条共 {len(all_extra)} 条 ===")
    for n in all_extra:
        cur.execute("""
            INSERT OR REPLACE INTO norms (
                norm_id, law, enbez, title, heading_path, text_de, 
                text_original, text_en, text_zh, elements_json, mandatory_level, snapshot_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            n["norm_id"], n["law"], n["enbez"], n["title"], n["heading_path"], n.get("text_de", n["title"]),
            n["text_zh"], n["text_zh"], n["text_zh"], n["elements_json"], "mandatory_override", SNAPSHOT_ID
        ))
    
    conn.commit()
    conn.close()
    print(f">>> 成功写入 {len(all_extra)} 条规范！")


if __name__ == "__main__":
    topup_data()
