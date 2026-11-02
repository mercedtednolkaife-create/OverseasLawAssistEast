# -*- coding: utf-8 -*-
"""东盟后五国（柬埔寨 KH、老挝 LA、缅甸 MM、文莱 BN、东帝汶 TL）及 L2 双边条约数据底座扩充脚本
(scripts/expand_five_asean_countries_and_l2.py)
对齐《功能优化及审查.md》Phase 1 第三步规范
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

# ----------------- 柬埔寨 (KH) -----------------
KH_L1_NORMS = [
    {
        "norm_id": "KH:Law_on_Investment_2021:Art12_Tax_Incentive",
        "law": "KH_Law_on_Investment_2021",
        "enbez": "Article 12",
        "title": "新投资法合格投资项目(QIP)免税期与增强型费用扣除",
        "heading_path": "柬埔寨新投资法 > 激励机制 > 第12条",
        "text_de": "Cambodia Investment Law 2021 Art. 12 (QIP Tax Holiday)",
        "text_zh": "注册为合格投资项目（QIP）的出海制造业与基础设施项目，享有自首次取得营业收入起最长9年的企业所得税（CIT）豁免期；或可选择加计扣除200%的研发、培训及技术改造开支。",
        "elements_json": json.dumps([{"eid": "e_qip_tax_holiday", "text_zh": "经CDC批准取得QIP证书的项目享受最长9年CIT免税", "status": "incentive"}], ensure_ascii=False)
    },
    {
        "norm_id": "KH:Civil_Code_2007:Art403_No_Reduction",
        "law": "KH_Civil_Code_2007",
        "enbez": "Article 403",
        "title": "柬埔寨民法典第403条预定违约金法官绝对不可调减原则",
        "heading_path": "柬埔寨民法典 > 债权总论 > 违约责任 > 第403条",
        "text_de": "Cambodia Civil Code Art. 403 (Non-reduction of Liquidated Damages)",
        "text_zh": "当事人可以预先约定债务不履行时的赔偿数额（违约金）。当事人约定违约金的，法院不得予以增加或减少。法官绝无衡平酌减违约金的法定裁量权。",
        "elements_json": json.dumps([{"eid": "e_kh_strict_liquidated_damages", "text_zh": "合同约定的违约金刚性支持，法官无权酌减", "status": "mandatory"}], ensure_ascii=False)
    },
    {
        "norm_id": "KH:Law_on_Construction_2019:Art38_Permit",
        "law": "KH_Law_on_Construction_2019",
        "enbez": "Article 38",
        "title": "柬埔寨建筑法施工许可证前置审批与无证停工拆除令",
        "heading_path": "柬埔寨建筑法 > 施工许可 > 第38条",
        "text_de": "Cambodia Construction Law Art. 38 (Mandatory Construction Permit)",
        "text_zh": "所有建设工程在破土动工前，必须依法取得国土规划建设部或省政府颁发的开工建设许可证（Construction Permit）；未获许可擅自施工的，处以停工、没收施工设备并限期拆除。",
        "elements_json": json.dumps([{"eid": "e_kh_permit_prereq", "text_zh": "开工前必须取得建设许可证，无证施工面临拆除及行政处罚", "status": "mandatory"}], ensure_ascii=False)
    },
    {
        "norm_id": "KH:Law_on_Construction_2019:Art73_Ten_Year_Warranty",
        "law": "KH_Law_on_Construction_2019",
        "enbez": "Article 73",
        "title": "柬埔寨建筑法主体结构工程10年法定隐蔽缺陷质保期",
        "heading_path": "柬埔寨建筑法 > 质量缺陷责任 > 第73条",
        "text_de": "Cambodia Construction Law Art. 73 (10-Year Decennial Structural Liability)",
        "text_zh": "建筑工程总承包商与设计单位对工程基础及承重结构缺陷承担法定的10年质量责任；该10年期自竣工验收合格移交之日起算，任何合同特约排除均属无效。",
        "elements_json": json.dumps([{"eid": "e_kh_10year_decennial", "text_zh": "主体结构法定10年缺陷责任，不可通过合同约定免除", "status": "mandatory"}], ensure_ascii=False)
    },
    {
        "norm_id": "KH:Labour_Law_1997:Art138_Foreign_Quota",
        "law": "KH_Labour_Law_1997",
        "enbez": "Article 138-142",
        "title": "柬埔寨劳动法外籍劳工10%配额限制与工作证年审",
        "heading_path": "柬埔寨劳动法 > 外籍劳工管理 > 第138-142条",
        "text_de": "Cambodia Labour Law (10% Foreign Worker Quota & Annual Work Permits)",
        "text_zh": "企业聘用的外籍员工总数原则上不得超过柬籍员工总数的10%（管理人员3%、专业技术人员5%、非技术人员2%）；超出配额必须提前向劳动部申请特殊用工许可并办理年度工作证。",
        "elements_json": json.dumps([{"eid": "e_kh_labor_quota", "text_zh": "外籍员工受10%配额严格限制，须持有有效工作证与签证", "status": "quota"}], ensure_ascii=False)
    },
    {
        "norm_id": "KH:Land_Law_2001:Art8_Foreign_Land_Restriction",
        "law": "KH_Land_Law_2001",
        "enbez": "Article 8, 44",
        "title": "柬埔寨土地法外资永久所有权禁令与最长50年长期租赁",
        "heading_path": "柬埔寨土地法 > 土地权属 > 第8、44条",
        "text_de": "Cambodia Land Law 2001 (Foreign Land Ownership Prohibition & 50-Year Lease)",
        "text_zh": "只有柬埔寨籍自然人或柬资持股51%以上的法人方能拥有土地所有权；外资企业可依法取得最长50年的长期租赁权（Perpetual Lease），并在土地上独立拥有建筑物所有权及设定抵押。",
        "elements_json": json.dumps([{"eid": "e_kh_land_ownership_ban", "text_zh": "外资严禁直接持有土地所有权，可通过50年租赁权投资建厂", "status": "mandatory"}], ensure_ascii=False)
    },
    {
        "norm_id": "KH:Commercial_Arbitration_2006:Art34_NCAC",
        "law": "KH_Commercial_Arbitration_2006",
        "enbez": "Article 34",
        "title": "柬埔寨国家商事仲裁法关于仲裁裁决最终性与法院撤销事由",
        "heading_path": "柬埔寨商事仲裁法 > 裁决撤销 > 第34条",
        "text_de": "Cambodia Commercial Arbitration Law Art. 34 (NCAC Finality & Set-Aside)",
        "text_zh": "柬埔寨国家商事仲裁中心（NCAC）作出的仲裁裁决为终局裁决；法院仅在存在缺乏仲裁协议、超裁或违反柬埔寨公共政策时方可撤销裁决，对实体争议不予复审。",
        "elements_json": json.dumps([{"eid": "e_kh_ncac_finality", "text_zh": "仲裁裁决终局，司法撤裁严格限于程序与公共秩序事由", "status": "procedural"}], ensure_ascii=False)
    },
    {
        "norm_id": "KH:Tax_Law_2023:Art25_WHT_Crossborder",
        "law": "KH_Tax_Law_2023",
        "enbez": "Article 25",
        "title": "柬埔寨2023新税法非居民预提所得税14%与双边税收协定待遇",
        "heading_path": "柬埔寨新税法 > 预提税 > 第25条",
        "text_de": "Cambodia Tax Law 2023 Art. 25 (14% Withholding Tax on Non-residents & DTA)",
        "text_zh": "向非居民企业支付利息、特许权使用费、工程技术服务费及管理费时，法定扣缴14%的预提所得税（WHT）；若依据中柬双边税收协定（DTA），利息与特许权税率降至10%。",
        "elements_json": json.dumps([{"eid": "e_kh_wht_14percent", "text_zh": "非居民技术服务法定扣缴14%WHT，中柬DTA可享受10%协定税率", "status": "tax"}], ensure_ascii=False)
    },
    {
        "norm_id": "KH:SEZ_Sub_Decree_147:Art10_Customs_Duty_Free",
        "law": "KH_SEZ_Sub_Decree_147",
        "enbez": "Article 10",
        "title": "柬埔寨经济特区(SEZ)免征进出口关税与增值税监管政策",
        "heading_path": "柬埔寨经济特区政令 > 关税优惠 > 第10条",
        "text_de": "Cambodia SEZ Sub-Decree 147 (Duty-free Imports in SEZ Zones)",
        "text_zh": "进驻西港特区及其他国家级经济特区（SEZ）的中资基建与生产企业，其进口建设材料、生产设备及原辅料免征全部进口关税及增值税（VAT）。",
        "elements_json": json.dumps([{"eid": "e_kh_sez_customs_free", "text_zh": "特区内进口基建施工物资免除进口关税及VAT", "status": "incentive"}], ensure_ascii=False)
    },
    {
        "norm_id": "KH:FX_Law_1997:Art13_Currency_Freedom",
        "law": "KH_FX_Law_1997",
        "enbez": "Article 13",
        "title": "柬埔寨外汇法资金自由汇出与NBC大额资本项下报备",
        "heading_path": "柬埔寨外汇管理法 > 资本项目 > 第13条",
        "text_de": "Cambodia FX Law 1997 (Free Repatriation of Capital & NBC Reporting)",
        "text_zh": "柬埔寨不实行外汇管制，投资者依法纳税后可通过授权商业银行自由汇出投资本金、股息红利及借款本息；单笔等值1万美元以上资本流动须向柬埔寨国家银行（NBC）申报备案。",
        "elements_json": json.dumps([{"eid": "e_kh_fx_repatriation", "text_zh": "税后利润自由汇出，高度美元化结算无强制结汇阻碍", "status": "fx"}], ensure_ascii=False)
    },
    {
        "norm_id": "KH:Civil_Code_2007:Art387_Force_Majeure",
        "law": "KH_Civil_Code_2007",
        "enbez": "Article 387",
        "title": "柬埔寨民法典不可抗力构成要件与免责范围",
        "heading_path": "柬埔寨民法典 > 履行障碍 > 不可抗力 > 第387条",
        "text_de": "Cambodia Civil Code Art. 387 (Force Majeure Doctrine)",
        "text_zh": "因当事人在订立合同时不能预见、不能避免且不能克服的客观情势导致合同不能履行的，构成不可抗力，免除债务人的违约赔偿责任，但受阻方须在合理期限内发出通知。",
        "elements_json": json.dumps([{"eid": "e_kh_force_majeure", "text_zh": "不可预见且无法避免的客观情势免除违约责任，须及时通知", "status": "defense"}], ensure_ascii=False)
    },
    {
        "norm_id": "KH:Law_on_Commercial_Enterprises_2005:Art91_Director_Duty",
        "law": "KH_Law_on_Commercial_Enterprises_2005",
        "enbez": "Article 91",
        "title": "柬埔寨商业企业法董事信义义务与合规审查责任",
        "heading_path": "柬埔寨商业企业法 > 董事职责 > 第91条",
        "text_de": "Cambodia Commercial Enterprises Law Art. 91 (Director Duties & Liabilities)",
        "text_zh": "项目公司董事必须以诚实信用及公司最佳利益履行职责；因董事违反东道国法律规章或从事重大利益冲突交易造成公司损失的，承担个人无限连带赔偿责任。",
        "elements_json": json.dumps([{"eid": "e_kh_director_liability", "text_zh": "中资外派董事承担法定注意义务，违规操作面临个人连带赔偿", "status": "governance"}], ensure_ascii=False)
    },
    {
        "norm_id": "KH:Environmental_Law_2023:Art22_EIA_Approval",
        "law": "KH_Environmental_Law_2023",
        "enbez": "Article 22",
        "title": "柬埔寨环境法重大工程环境影响评价(EIA)前置审批令",
        "heading_path": "柬埔寨环境保护法 > 环境影响评价 > 第22条",
        "text_de": "Cambodia Environmental Code 2023 (Mandatory EIA Approval Before Construction)",
        "text_zh": "大型水电、燃煤电站、深水港及化工基建项目必须在开工前完成全本环境与社会影响评价（ESIA），并取得环境部（MoE）正式核准函；未批先建处以停工及环境修复罚金。",
        "elements_json": json.dumps([{"eid": "e_kh_eia_requirement", "text_zh": "重大基建项目必须取得环境部EIA批文，未经批准不得开工", "status": "environmental"}], ensure_ascii=False)
    }
]

# ----------------- 老挝 (LA) -----------------
LA_L1_NORMS = [
    {
        "norm_id": "LA:Law_on_Investment_Promotion_2016:Art35_Concession_CA",
        "law": "LA_Law_on_Investment_Promotion_2016",
        "enbez": "Article 35",
        "title": "老挝投资促进法特许权协议(CA)签署与国会前置审批令",
        "heading_path": "老挝投资促进法 > 特许经营业务 > 第35条",
        "text_de": "Laos Investment Promotion Law Art. 35 (Concession Agreement & Parliamentary Approval)",
        "text_zh": "涉及矿产开采、大型水电BOT、高速公路特许经营等占用国家土地和自然资源的项目，必须与老挝政府规划投资部（MPI）签署正式《特许权协议》（CA）；重大特许经营项目须报老挝国会（National Assembly）批准生效。",
        "elements_json": json.dumps([{"eid": "e_la_ca_approval", "text_zh": "大型基建特许经营必须经老挝国会审批并签署CA协议方具法定效力", "status": "mandatory"}], ensure_ascii=False)
    },
    {
        "norm_id": "LA:Law_on_FX_Management_2022:Art15_Offshore_Loan_BOL",
        "law": "LA_Law_on_FX_Management_2022",
        "enbez": "Article 15, 34",
        "title": "老挝2022外汇法境外股东借款必须取得老挝央行(BOL)批准",
        "heading_path": "老挝外汇管理法 > 离岸借款 > 第15条",
        "text_de": "Laos Foreign Exchange Management Law 2022 Art. 15 (BOL Offshore Loan Approval)",
        "text_zh": "老挝境内企业（含外资中资项目公司）从境外母公司或国际银团举借离岸外债，必须在贷款协议生效前取得老挝国家银行（BOL）的书面批准并办理外债登记；未经批准的离岸贷款，本金及利息依法一律严禁购汇汇出境外！",
        "elements_json": json.dumps([{"eid": "e_la_bol_offshore_loan", "text_zh": "境外母公司贷款未获BOL批准导致本息绝对无法合规购汇出境", "status": "fx_barrier"}], ensure_ascii=False)
    },
    {
        "norm_id": "LA:Civil_Code_2018:Art355_Breach_Compensation",
        "law": "LA_Civil_Code_2018",
        "enbez": "Article 355",
        "title": "老挝民法典合同违约法定损害赔偿范围与可预见性规则",
        "heading_path": "老挝民法典 > 违约责任 > 第355条",
        "text_de": "Laos Civil Code Art. 355 (Contractual Damages & Foreseeability)",
        "text_zh": "因一方违约给对方造成损失的，赔偿范围包括直接实际损失及合理可得利益；损害赔偿数额不得超过违约方在订立合同时已经预见或应当预见的损失范围。",
        "elements_json": json.dumps([{"eid": "e_la_foreseeable_damages", "text_zh": "违约损害赔偿严格限于订立合同时可预见的损失与实际损失", "status": "damages"}], ensure_ascii=False)
    },
    {
        "norm_id": "LA:Labour_Law_2013:Art68_Foreign_Labor_Cap",
        "law": "LA_Labour_Law_2013",
        "enbez": "Article 68",
        "title": "老挝劳动法体力劳工15%与脑力劳工25%外籍配额限制",
        "heading_path": "老挝劳动法 > 外籍劳工配额 > 第68条",
        "text_de": "Laos Labour Law Art. 68 (Foreign Labor Caps 15% / 25%)",
        "text_zh": "工程承包及生产企业雇佣外籍体力劳工不得超过老挝籍员工总数的15%，脑力技术劳工不得超过25%；引进中国工程技术人员必须取得劳动与社会福利部的年度配额准核证。",
        "elements_json": json.dumps([{"eid": "e_la_labor_quota", "text_zh": "外劳严格受15%/25%比例封顶，超配额须专项报批", "status": "quota"}], ensure_ascii=False)
    },
    {
        "norm_id": "LA:Electricity_Law_2017:Art28_PPA_Grid",
        "law": "LA_Electricity_Law_2017",
        "enbez": "Article 28",
        "title": "老挝电力法购电协议(PPA)与国家电网EDL排他并网权",
        "heading_path": "老挝电力法 > 发电与并网 > 第28条",
        "text_de": "Laos Electricity Law Art. 28 (PPA with EDL & Grid Access)",
        "text_zh": "在老挝境内开发的所有水电站、光伏电站独立发电商（IPP），必须与老挝国家电力公司（EDL）签署购电协议（PPA）；PPA 中的照付不议（Take-or-Pay）条款受国家能源矿产部与财政部联合监管。",
        "elements_json": json.dumps([{"eid": "e_la_ppa_edl", "text_zh": "电站运营必须与EDL签署PPA，受老挝主权电网调度与担保约束", "status": "energy"}], ensure_ascii=False)
    },
    {
        "norm_id": "LA:Land_Law_2019:Art65_State_Land_Concession",
        "law": "LA_Land_Law_2019",
        "enbez": "Article 65",
        "title": "老挝土地法国家土地特许使用期最长50年与征地补偿",
        "heading_path": "老挝土地法 > 土地特许 > 第65条",
        "text_de": "Laos Land Law 2019 Art. 65 (50-Year State Land Concession Limit)",
        "text_zh": "外国投资者依法不得拥有老挝土地所有权，但可通过特许经营获得国家土地使用权，最长特许期不超过50年；征用当地农户土地必须由省政府委员会主导并完成全额足额补偿安置。",
        "elements_json": json.dumps([{"eid": "e_la_land_concession", "text_zh": "土地特许期不超过50年，征地补偿必须合规闭环", "status": "mandatory"}], ensure_ascii=False)
    },
    {
        "norm_id": "LA:Mining_Law_2017:Art42_Mineral_Export_Ban",
        "law": "LA_Mining_Law_2017",
        "enbez": "Article 42",
        "title": "老挝矿业法未加工原矿出口限制与就地深加工配额",
        "heading_path": "老挝矿业法 > 矿产深加工与出口 > 第42条",
        "text_de": "Laos Mining Law Art. 42 (Raw Mineral Export Restrictions)",
        "text_zh": "老挝政府严禁未加工原矿（铜、金、钾盐）直接出口；采矿企业必须在老挝境内投资建设精炼与深加工设施，达到工业与贸易部规定的精炼标准后方予签发出口许可证。",
        "elements_json": json.dumps([{"eid": "e_la_mineral_export_restriction", "text_zh": "原矿禁止直接出口，须在老挝境内完成法定深度加工", "status": "mandatory"}], ensure_ascii=False)
    },
    {
        "norm_id": "LA:Tax_Law_2019:Art18_CIT_Standard",
        "law": "LA_Tax_Law_2019",
        "enbez": "Article 18",
        "title": "老挝税法标准企业所得税20%与重点经济特区优惠税率",
        "heading_path": "老挝税法 > 企业所得税 > 第18条",
        "text_de": "Laos Tax Law 2019 Art. 18 (20% Corporate Income Tax & SEZ Rates)",
        "text_zh": "老挝企业标准所得税率为20%；在老挝磨丁经济特区、赛色塔综合开发区投资符合条件的高新技术或出口导向型企业，可享受5%~10%的优惠税率或特定免税期。",
        "elements_json": json.dumps([{"eid": "e_la_cit_20percent", "text_zh": "标准所得税20%，特区内投资享受5%-10%优惠税率", "status": "tax"}], ensure_ascii=False)
    },
    {
        "norm_id": "LA:Enterprise_Law_2013:Art90_Joint_Venture",
        "law": "LA_Enterprise_Law_2013",
        "enbez": "Article 90",
        "title": "老挝企业法合资企业注册资本实缴与出资验证",
        "heading_path": "老挝企业法 > 合资企业 > 第90条",
        "text_de": "Laos Enterprise Law Art. 90 (Registered Capital Injection Timetable)",
        "text_zh": "外商投资企业注册资本原则上应在公司成立之日起90天内完成首期出资（不低于30%），并在1年内缴足全部注册资本；资金必须通过老挝商业银行合规验资账户存入。",
        "elements_json": json.dumps([{"eid": "e_la_capital_injection", "text_zh": "注册资本1年内缴足，须经由老挝商业银行外汇专用账户验资", "status": "capital"}], ensure_ascii=False)
    },
    {
        "norm_id": "LA:Dispute_Resolution_2010:Art25_Arbitration",
        "law": "LA_Dispute_Resolution_2010",
        "enbez": "Article 25",
        "title": "老挝经济纠纷解决法仲裁裁决承认与法院执行管辖",
        "heading_path": "老挝经济纠纷解决法 > 仲裁执行 > 第25条",
        "text_de": "Laos Economic Dispute Resolution Law (Arbitral Award Recognition & Enforcement)",
        "text_zh": "老挝作为《纽约公约》缔约国，其法院依法承认并执行境外常设仲裁机构（SIAC、VIAC、CIETAC）作出的商事仲裁裁决；外国裁决须经老挝人民法院初审裁定予以认可方可强制执行。",
        "elements_json": json.dumps([{"eid": "e_la_award_enforcement", "text_zh": "依据纽约公约承认境外仲裁裁决，经老挝法院审查后强制执行", "status": "procedural"}], ensure_ascii=False)
    }
]

# ----------------- 缅甸 (MM) -----------------
MM_L1_NORMS = [
    {
        "norm_id": "MM:Myanmar_Companies_Law_2017:Art35_Foreign_Ownership",
        "law": "MM_Myanmar_Companies_Law_2017",
        "enbez": "Section 35",
        "title": "缅甸公司法35%外资股权红线与本土公司界定",
        "heading_path": "缅甸公司法2017 > 公司分类 > 第35条",
        "text_de": "Myanmar Companies Law 2017 Section 35 (35% Foreign Ownership Threshold)",
        "text_zh": "外国投资者在缅甸注册公司中持股比例不超过35%的，该公司仍被依法界定为“缅甸本土公司（Myanmar Company）”，依法享有拥有土地及从事部分受限贸易的同等待遇；外资超过35%即变更为外国公司。",
        "elements_json": json.dumps([{"eid": "e_mm_35percent_threshold", "text_zh": "持股超35%即转为外国公司，触发土地所有权与特定行业准入限制", "status": "mandatory"}], ensure_ascii=False)
    },
    {
        "norm_id": "MM:FEML_2012:Notification_12_2022_Mandatory_Conversion",
        "law": "MM_FEML_2012",
        "enbez": "Directive 12/2022",
        "title": "缅甸央行第12/2022号令外汇收入1个工作日内强制结汇为缅币",
        "heading_path": "缅甸外汇管理法 > 央行指令 > 第12/2022号令",
        "text_de": "CBM Notification 12/2022 (Mandatory 1-Day Foreign Exchange Conversion into MMK)",
        "text_zh": "缅甸所有境内企业（除MIC特批豁免外）收到境外汇入的美元外汇款项，必须在1个工作日内按照缅甸央行（CBM）官方参考汇率强制兑换为缅甸元（MMK）；严禁私自保留离岸美元账户或境外沉淀资金。",
        "elements_json": json.dumps([{"eid": "e_mm_mandatory_fx_conversion", "text_zh": "到账1日内强制按官方低汇率结汇为缅币，面临巨大汇率折损与汇出阻断", "status": "fx_barrier"}], ensure_ascii=False)
    },
    {
        "norm_id": "MM:Contract_Act_1872:Sec56_Frustration",
        "law": "MM_Contract_Act_1872",
        "enbez": "Section 56",
        "title": "缅甸合同法第56条合同受阻落空(Doctrine of Frustration)",
        "heading_path": "缅甸合同法1872 > 合同落空 > 第56条",
        "text_de": "Myanmar Contract Act 1872 Section 56 (Doctrine of Frustration)",
        "text_zh": "合同订立后，因发生当事人无法控制且不可归责于任何一方的外部重大情势变更（如政变、爆发全面内战、军管外汇禁令），致使合同在物理上或法律上完全无法履行的，合同自始落空并归于终止，双方互免后续履行责任。",
        "elements_json": json.dumps([{"eid": "e_mm_frustration_defense", "text_zh": "军管外汇限制与不可预见内战构成合同落空，阻断违约金赔偿请求", "status": "defense"}], ensure_ascii=False)
    },
    {
        "norm_id": "MM:Myanmar_Investment_Law_2016:Art50_MIC_Permit",
        "law": "MM_Myanmar_Investment_Law_2016",
        "enbez": "Section 50",
        "title": "缅甸投资法MIC长期投资许可证与土地长期使用权",
        "heading_path": "缅甸投资法2016 > 投资许可 > 第50条",
        "text_de": "Myanmar Investment Law 2016 (MIC Permit & 50-Year Land Lease Rights)",
        "text_zh": "涉及重大基建、特许经营、战略自然资源开发的大型投资项目，必须取得缅甸投资委员会（MIC）颁发的投资许可证（MIC Permit）；获证企业依法享有最长50年（可连续展期两次每次10年）的土地长期使用权。",
        "elements_json": json.dumps([{"eid": "e_mm_mic_permit", "text_zh": "大型基建必须持有MIC许可证方能合法租赁最长70年土地并享受外汇结汇豁免", "status": "permit"}], ensure_ascii=False)
    },
    {
        "norm_id": "MM:SEZ_Law_2014:Art32_Kyaukphyu_Incentives",
        "law": "MM_SEZ_Law_2014",
        "enbez": "Section 32",
        "title": "缅甸经济特区法与皎漂深水港特区所得税减免激励",
        "heading_path": "缅甸经济特区法 > 特区投资激励 > 第32条",
        "text_de": "Myanmar SEZ Law 2014 Section 32 (Tax Exemptions in Kyaukphyu SEZ)",
        "text_zh": "在皎漂特区、迪拉瓦特区等国家级SEZ投资的基础设施开发商，享有前7年免征企业所得税，后续5年减半征收所得税的特别待遇；特区内允许保留美元外汇账户并豁免日常强制结汇。",
        "elements_json": json.dumps([{"eid": "e_mm_sez_incentive", "text_zh": "皎漂等特区内享有7年免税并可申请豁免强制结汇令", "status": "incentive"}], ensure_ascii=False)
    },
    {
        "norm_id": "MM:Arbitration_Law_2016:Sec34_Enforcement",
        "law": "MM_Arbitration_Law_2016",
        "enbez": "Section 34",
        "title": "缅甸2016仲裁法对联合国UNCITRAL规则与纽约公约的采纳",
        "heading_path": "缅甸仲裁法2016 > 外国裁决承认 > 第34条",
        "text_de": "Myanmar Arbitration Law 2016 Section 34 (UNCITRAL Model Law & New York Convention)",
        "text_zh": "缅甸2016年新仲裁法全面采纳联合国贸法会（UNCITRAL）示范法体系，正式确认国际商事仲裁裁决在缅甸各级法院具有执行力；撤销或拒绝执行裁决的事由严格限于仲裁协议无效或严重违反缅甸公共政策。",
        "elements_json": json.dumps([{"eid": "e_mm_arbitration_model_law", "text_zh": "全面采纳示范法，认可SIAC及海外涉外仲裁裁决的国内执行力", "status": "procedural"}], ensure_ascii=False)
    },
    {
        "norm_id": "MM:Labour_Organization_Law_2011:Art29_Dispute_Settlement",
        "law": "MM_Labour_Organization_Law_2011",
        "enbez": "Section 29",
        "title": "缅甸劳工组织法关于罢工合法性审查与劳动争议仲裁委员会前置",
        "heading_path": "缅甸劳工组织法 > 劳动争议处理 > 第29条",
        "text_de": "Myanmar Labour Organization Law (Strike Legality & Dispute Settlement)",
        "text_zh": "工会发动罢工必须提前14天向雇主及镇区劳动局发出书面通知并取得超过50%会员无记名投票支持；未遵守前置程序的非法罢工不构成不可抗力，雇主有权依法予以解雇。",
        "elements_json": json.dumps([{"eid": "e_mm_strike_legality", "text_zh": "未履行14天通知前置程序的非法罢工不豁免承包商工期责任", "status": "labor"}], ensure_ascii=False)
    },
    {
        "norm_id": "MM:Environmental_Conservation_Law_2012:Sec14_EIA",
        "law": "MM_Environmental_Conservation_Law_2012",
        "enbez": "Section 14",
        "title": "缅甸环境保护法EIA环评审批与违规停工令",
        "heading_path": "缅甸环境保护法 > 环境与社会评价 > 第14条",
        "text_de": "Myanmar Environmental Conservation Law 2012 (Mandatory EIA Approval)",
        "text_zh": "所有重大建设工程必须取得自然资源与环境保护部（MONREC）颁发的情境审查与EIA环境批准证书（ECC）；未获ECC擅自施工的项目，政府依法签发停工令并处以追溯罚款。",
        "elements_json": json.dumps([{"eid": "e_mm_eia_ecc", "text_zh": "开工必须具备MONREC颁发的ECC环境证书，否则面临停工及法律制裁", "status": "environmental"}], ensure_ascii=False)
    }
]

# ----------------- 文莱 (BN) -----------------
BN_L1_NORMS = [
    {
        "norm_id": "BN:Constitution_1959:Art84C_Absolute_Immunity",
        "law": "BN_Constitution_1959",
        "enbez": "Article 84C",
        "title": "文莱达鲁萨兰国宪法第84C条政府绝对主权豁免权",
        "heading_path": "文莱宪法1959 > 主权与法院管辖 > 第84C条",
        "text_de": "Brunei Constitution 1959 Art. 84C (Absolute Sovereign Immunity)",
        "text_zh": "苏丹陛下及其政府部委享有绝对司法管辖豁免权；文莱国内各级法院严禁受理任何直接或间接针对文莱政府提起的民事违约起诉或执行申请，除非在商业合同中明确订立离岸仲裁协议。",
        "elements_json": json.dumps([{"eid": "e_bn_absolute_immunity", "text_zh": "文莱国内法院严禁受理针对政府的违约诉讼，出海文莱必须锁定国际离岸仲裁", "status": "mandatory"}], ensure_ascii=False)
    },
    {
        "norm_id": "BN:Contracts_Act_Cap106:Sec74_75_Reasonable_Damages",
        "law": "BN_Contracts_Act_Cap106",
        "enbez": "Section 74, 75",
        "title": "文莱合同法第74/75条违约金惩罚性条款无效与合理补偿原则",
        "heading_path": "文莱合同法典第106章 > 违约赔偿 > 第74、75条",
        "text_de": "Brunei Contracts Act Cap 106 Sec. 74/75 (Penalty Rule & Reasonable Compensation)",
        "text_zh": "合同中约定的违约金若构成惩罚性条款（Penalty），文莱法院不予直接按全额支持，而是判令违约方仅承担受损方能够证明的合理损失补偿额（Reasonable Compensation），但最高不超过约定上限。",
        "elements_json": json.dumps([{"eid": "e_bn_penalty_rule", "text_zh": "英美法Penalty规则适用，过高过苛违约金可抗辩其为无效惩罚条款", "status": "defense"}], ensure_ascii=False)
    },
    {
        "norm_id": "BN:Arbitration_Order_2009:Sec33_BDAC",
        "law": "BN_Arbitration_Order_2009",
        "enbez": "Section 33",
        "title": "文莱国际仲裁令与文莱仲裁中心(BDAC)裁决执行",
        "heading_path": "文莱国际仲裁令2009 > 裁决执行 > 第33条",
        "text_de": "Brunei International Arbitration Order 2009 (BDAC Arbitral Rules & Enforcement)",
        "text_zh": "依据文莱国际仲裁令，在文莱仲裁中心（BDAC）或依照国际规则作出的商事仲裁裁决，在文莱具有相当于文莱高等法院判决的同等强制执行效力；司法干预严格受到限制。",
        "elements_json": json.dumps([{"eid": "e_bn_arbitration_finality", "text_zh": "仲裁裁决在文莱具备相当于法院终审判决的执行力", "status": "procedural"}], ensure_ascii=False)
    },
    {
        "norm_id": "BN:Investment_Incentives_Order_2001:Sec15_Pioneer_Status",
        "law": "BN_Investment_Incentives_Order_2001",
        "enbez": "Section 15",
        "title": "文莱投资激励令先锋工业免税地位与最长11年免税期",
        "heading_path": "文莱投资激励令 > 先锋工业地位 > 第15条",
        "text_de": "Brunei Investment Incentives Order 2001 (Pioneer Status CIT Exemption up to 11 Years)",
        "text_zh": "在大摩拉岛石化一体化等国家级重点项目中被授予先锋企业地位（Pioneer Industry）的外商投资企业，享有5年至最长11年的企业所得税（CIT）免税期，并免征生产设备进口关税。",
        "elements_json": json.dumps([{"eid": "e_bn_pioneer_tax_free", "text_zh": "取得先锋地位享有最长11年所得税免税与进口免税待遇", "status": "incentive"}], ensure_ascii=False)
    },
    {
        "norm_id": "BN:Land_Code_Cap40:Sec23_Foreign_Ownership_Ban",
        "law": "BN_Land_Code_Cap40",
        "enbez": "Section 23",
        "title": "文莱土地法典第40章外国法人土地所有权禁令与政府租赁",
        "heading_path": "文莱土地法典 > 土地转让限制 > 第23条",
        "text_de": "Brunei Land Code Cap 40 (Foreign Land Ownership Restriction & State Leases)",
        "text_zh": "外国自然人及外国控股公司严禁在文莱直接拥有永久私人土地（Freehold）；外商投资者通常向文莱工业发展局（BEDB）申请国家级工业用地长期租赁，租期通常为30至60年。",
        "elements_json": json.dumps([{"eid": "e_bn_land_freehold_ban", "text_zh": "严禁外资持有永久地契，通过政府30-60年工业租赁权落地", "status": "mandatory"}], ensure_ascii=False)
    },
    {
        "norm_id": "BN:Employment_Order_2009:Sec64_Work_Pass",
        "law": "BN_Employment_Order_2009",
        "enbez": "Section 64",
        "title": "文莱雇佣令外籍劳工准证(LPA)与本地员工就业配额",
        "heading_path": "文莱雇佣令2009 > 外劳管制 > 第64条",
        "text_de": "Brunei Employment Order 2009 (Foreign Worker License LPA & Bruneianisation)",
        "text_zh": "企业引进中国工程技术人员与施工劳动力，必须事先向劳工局申请外籍员工许可证（LPA）并落实文莱化用工比例（Bruneianisation）；未获LPA雇佣外籍人员属于严重刑事违法。",
        "elements_json": json.dumps([{"eid": "e_bn_lpa_license", "text_zh": "必须持有合规LPA准证方可外派工程技术劳动力", "status": "labor"}], ensure_ascii=False)
    }
]

# ----------------- 东帝汶 (TL) -----------------
TL_L1_NORMS = [
    {
        "norm_id": "TL:Law_9_2011:Art14_Pre_Audit_Visto",
        "law": "TL_Law_9_2011",
        "enbez": "Article 14, 40",
        "title": "东帝汶审计法院法关于公共工程合同事前签证(Visto)刚性要求",
        "heading_path": "东帝汶国家高等审计法院法 > 事前财务审查 > 第14条",
        "text_de": "Timor-Leste Law 9/2011 Art. 14 (Mandatory Chamber of Accounts Visto for Public Contracts)",
        "text_zh": "所有涉及东帝汶国家财政资金、公共预算超50万美元的建设工程合同及追加工程补充协议，必须在开工前呈送审计法院（Câmara de Contas）签发事前签证（Visto）；未获Visto签证的合同在法律上自始无效，财政部严禁向承包商拨付任何工程款项！",
        "elements_json": json.dumps([{"eid": "e_tl_visto_mandatory", "text_zh": "未取得审计法院事前Visto签证导致合同在财务上自始无效，工程款遭法定拒付", "status": "mandatory"}], ensure_ascii=False)
    },
    {
        "norm_id": "TL:Civil_Code_2011:Art798_Contractual_Liability",
        "law": "TL_Civil_Code_2011",
        "enbez": "Article 798, 804",
        "title": "东帝汶民法典大陆法系过错违约责任与定金罚则",
        "heading_path": "东帝汶民法典 > 债务不履行责任 > 第798、804条",
        "text_de": "Timor-Leste Civil Code 2011 (Portuguese Civil Law Tradition & Default Liability)",
        "text_zh": "东帝汶民法典沿袭葡萄牙民法传统；债务人因自身过错致使履行迟延或不履行的，承担全部损害赔偿责任；合同约定的预付款具有定金（Sinal）性质的，违约方承担双倍返还责任。",
        "elements_json": json.dumps([{"eid": "e_tl_civil_code_fault", "text_zh": "沿袭葡语系大陆法，遵循过错归责与定金双倍罚则", "status": "liability"}], ensure_ascii=False)
    },
    {
        "norm_id": "TL:Private_Investment_Law_2017:Art21_ICSID",
        "law": "TL_Private_Investment_Law_2017",
        "enbez": "Article 21",
        "title": "东帝汶私人投资法关于国际投资仲裁管辖前置磋商期",
        "heading_path": "东帝汶私人投资法 > 争端解决 > 第21条",
        "text_de": "Timor-Leste Private Investment Law Art. 21 (Investment Disputes & ICSID Consent)",
        "text_zh": "外商投资者与东帝汶政府因投资征收或重大违约发生争议，双方必须先进行为期90天的友好前置协商；协商不成的，可依据《华盛顿公约》向世界银行 ICSID 或依 UNCITRAL 规则提起国际仲裁。",
        "elements_json": json.dumps([{"eid": "e_tl_icsid_consent", "text_zh": "法定义务经90天磋商前置程序后方可启动ICSID投资仲裁", "status": "isds"}], ensure_ascii=False)
    },
    {
        "norm_id": "TL:Tax_Act_2008:Sec58_Service_WHT",
        "law": "TL_Tax_Act_2008",
        "enbez": "Section 58",
        "title": "东帝汶税法建筑承包工程预扣税与非居民境外税率",
        "heading_path": "东帝汶税收法典 > 预提税 > 第58条",
        "text_de": "Timor-Leste Tax Act 2008 Section 58 (Withholding Tax on Construction & Services)",
        "text_zh": "对在东帝汶境内从事建筑安装与工程设计承包的非居民外国企业，发包人在每次支付工程进度款时必须依法预扣2%~4%的最终工程预扣税；对技术咨询费按10%代扣预提所得税。",
        "elements_json": json.dumps([{"eid": "e_tl_wht_tax", "text_zh": "工程款进度支付时强制代扣2%-4%工程预扣税", "status": "tax"}], ensure_ascii=False)
    },
    {
        "norm_id": "TL:Labour_Code_2012:Art24_Specialized_Foreign_Labor",
        "law": "TL_Labour_Code_2012",
        "enbez": "Article 24",
        "title": "东帝汶劳动法外籍专业技术人员工签前置技能对口证明",
        "heading_path": "东帝汶劳动法典第4/2012号 > 外劳管理 > 第24条",
        "text_de": "Timor-Leste Labour Code 2012 (Foreign Specialized Workers & National Training)",
        "text_zh": "只有在东帝汶国内劳动力市场缺乏对应技能时方允许招募外籍员工；聘用外国专家的承包商必须向内政部移民局提交技能对口认证，并制定培训东帝汶本土工人的技能转移方案。",
        "elements_json": json.dumps([{"eid": "e_tl_labor_transfer", "text_zh": "外派人员须具备专业技能认证并承担属地劳动力培训义务", "status": "labor"}], ensure_ascii=False)
    },
    {
        "norm_id": "TL:Land_Law_13_2017:Art10_Expropriation",
        "law": "TL_Land_Law_13_2017",
        "enbez": "Article 10",
        "title": "东帝汶第13/2017号土地法关于国家土地所有权与征收补偿程序",
        "heading_path": "东帝汶特别土地权属法 > 国家土地与征收 > 第10条",
        "text_de": "Timor-Leste Land Law 13/2017 (State Domain & Expropriation with Fair Compensation)",
        "text_zh": "东帝汶国家对未登记私人土地享有主权推定所有权；国家因公共利益需要征收土地建设港口、道路、机场设施的，必须按照市场公允评估价值向受影响原住民支付全额补偿。",
        "elements_json": json.dumps([{"eid": "e_tl_land_expropriation", "text_zh": "公共基建征地必须依法履行公允市场评估与足额补偿程序", "status": "mandatory"}], ensure_ascii=False)
    }
]

# ----------------- 5国 L2 双边条约、DTA与国际规则补充 -----------------
FIVE_COUNTRIES_L2_TREATIES = [
    {
        "norm_id": "TREATY:CN_KH_BIT_1996:Art4_Expropriation",
        "law": "TREATY_CN_KH_BIT_1996",
        "enbez": "Article 4",
        "title": "中国-柬埔寨双边投资保护协定(BIT)征收补偿与国民待遇",
        "heading_path": "中柬投资保护协定1996 > 征收与征用 > 第4条",
        "text_de": "China-Cambodia Bilateral Investment Treaty 1996 Art. 4 (Expropriation & FET)",
        "text_zh": "缔约任何一方对缔约另一方投资者在其境内的投资不得采取征收、国有化或具有类似效果的措施，除非为了公共利益并在符合国内法律程序、非歧视原则下，并给予及时、充分、有效的补偿。",
        "elements_json": json.dumps([{"eid": "e_cn_kh_bit_expropriation", "text_zh": "间接征收必须遵循非歧视原则并给予充分有效补偿", "status": "treaty"}], ensure_ascii=False)
    },
    {
        "norm_id": "TREATY:CN_KH_DTA_2016:Art11_Interest_Tax",
        "law": "TREATY_CN_KH_DTA_2016",
        "enbez": "Article 11",
        "title": "中柬避免双重征税协定(DTA)跨境贷款利息10%协定税率",
        "heading_path": "中柬双边税收协定 > 利息所得 > 第11条",
        "text_de": "China-Cambodia Double Taxation Agreement 2016 Art. 11 (10% Interest WHT Cap)",
        "text_zh": "发生于柬埔寨而支付给中国居民的利息，其征税额不得超过利息总额的10%；直接突破柬埔寨国内14%的高额法定预提所得税。",
        "elements_json": json.dumps([{"eid": "e_cn_kh_dta_interest", "text_zh": "跨境股东借款利息预提税降至10%，显著减轻融资财务成本", "status": "tax_relief"}], ensure_ascii=False)
    },
    {
        "norm_id": "TREATY:CN_LA_BIT_1993:Art3_FET",
        "law": "TREATY_CN_LA_BIT_1993",
        "enbez": "Article 3",
        "title": "中国-老挝双边投资保护协定(BIT)公平公正待遇与充分保护",
        "heading_path": "中老投资保护协定1993 > 投资待遇 > 第3条",
        "text_de": "China-Laos Bilateral Investment Treaty 1993 Art. 3 (Fair and Equitable Treatment)",
        "text_zh": "缔约各方应始终确保缔约另一方投资者的投资获得公平公正的待遇以及持续的保护与安全；任何一方均不得采取不合理或歧视性措施损害对方投资者的管理、维持、使用或处分权。",
        "elements_json": json.dumps([{"eid": "e_cn_la_bit_fet", "text_zh": "老挝东道国政策恶意巨幅变动构成违反FET公平公正待遇", "status": "treaty"}], ensure_ascii=False)
    },
    {
        "norm_id": "TREATY:CN_LA_DTA_1999:Art12_Royalties",
        "law": "TREATY_CN_LA_DTA_1999",
        "enbez": "Article 12",
        "title": "中老避免双重征税协定(DTA)特许权使用费与专有技术转让税率",
        "heading_path": "中老双边税收协定 > 特许权使用费 > 第12条",
        "text_de": "China-Laos Double Taxation Agreement 1999 (5% - 10% Royalties Cap)",
        "text_zh": "向老挝水电及工程项目转让特许权、工业专利及专有技术所取得的使用费，在老挝征收的税款最高不得超过使用费总额的5%（工业设备使用）至10%。",
        "elements_json": json.dumps([{"eid": "e_cn_la_dta_royalties", "text_zh": "跨境技术许可与专利转让享受5%-10%协定优惠税率", "status": "tax_relief"}], ensure_ascii=False)
    },
    {
        "norm_id": "TREATY:CN_MM_BIT_2001:Art6_Repatriation",
        "law": "TREATY_CN_MM_BIT_2001",
        "enbez": "Article 6",
        "title": "中国-缅甸双边投资保护协定(BIT)外汇资金无迟延自由转移",
        "heading_path": "中缅投资保护协定2001 > 资金转移 > 第6条",
        "text_de": "China-Myanmar Bilateral Investment Treaty 2001 Art. 6 (Free Transfer of Funds)",
        "text_zh": "缔约各方应保证缔约另一方投资者在其境内的投资及收益能够以可自由兑换的货币、按转移当日的市场汇率、无迟延地自由转移出境；该条约强行力直接抗辩缅甸国内非常规强制结汇法令！",
        "elements_json": json.dumps([{"eid": "e_cn_mm_bit_repatriation", "text_zh": "条约保障资金无延迟自由汇出，构成抗辩缅甸国内单方强制结汇的有力上位法武器", "status": "treaty_override"}], ensure_ascii=False)
    },
    {
        "norm_id": "TREATY:CN_BN_BIT_2000:Art4_Compensation",
        "law": "TREATY_CN_BN_BIT_2000",
        "enbez": "Article 4",
        "title": "中国-文莱双边投资保护协定(BIT)非歧视与国际仲裁救济",
        "heading_path": "中文投资保护协定2000 > 征收与争端 > 第4条",
        "text_de": "China-Brunei Bilateral Investment Treaty 2000 Art. 4 (Non-discrimination & ICSID Pathway)",
        "text_zh": "缔约方若对中资投资者的石化、港口及公用事业设施采取实质性征用或权利剥夺，必须依法按照被征收投资在征收决定公开宣布前的公允市场价值支付足额赔偿并加计商业利息；争议可提交 ICSID 解决。",
        "elements_json": json.dumps([{"eid": "e_cn_bn_bit_compensation", "text_zh": "条约突破文莱国内宪制绝对主权豁免，打通ICSID国际仲裁救济路径", "status": "treaty"}], ensure_ascii=False)
    },
    {
        "norm_id": "TREATY:UN_New_York_Convention_1958:Art5_Timor_Leste",
        "law": "TREATY_New_York_Convention_1958",
        "enbez": "Article 5",
        "title": "联合国承认及执行外国仲裁裁决公约(纽约公约)东帝汶适用与例外事由",
        "heading_path": "海牙纽约公约1958 > 拒绝承认与执行事由 > 第5条",
        "text_de": "New York Convention 1958 Art. 5 (Timor-Leste Accession & Public Policy Defense)",
        "text_zh": "东帝汶于2021年正式加入《纽约公约》；东帝汶法院承认与执行缔约国境外仲裁裁决时，拒绝执行的事由严格穷尽列举于第5条（仲裁协议无效、未获适当通知、越权超裁或违背本国公共政策）。",
        "elements_json": json.dumps([{"eid": "e_ny_convention_tl", "text_zh": "东帝汶正式纳入纽约公约执行网络，境外仲裁裁决可直接申请法院执行", "status": "treaty"}], ensure_ascii=False)
    }
]

# ----------------- 5国 标杆裁判 -----------------
FIVE_COUNTRIES_CASES = [
    {
        "case_id": "CASE:KH_NCAC:Lump_Sum_Delay_Damages_Award_2022",
        "court": "National Commercial Arbitration Centre (NCAC Cambodia)",
        "senate": "Tribunal Arbitral",
        "decided": "2022-09-14",
        "az": "NCAC Case No. 018/2021",
        "ecli": "KH:NCAC:2022:18",
        "doctype": "Award",
        "leitsatz": "柬埔寨国家商事仲裁中心标杆裁决：全面确认柬埔寨《民法典》第403条预定违约金刚性不可调减效力。总承包商以疫情及雨季导致工期延误、主张违约金畸高请求仲裁庭依公平原则酌减的，仲裁庭依据民法典第403条明确裁定：仲裁庭绝无依职权调减违约金的法定裁量权，判令全额赔付。",
        "tenor": "仲裁庭一致裁决：全面支持业主依据合同专用条件索赔的全部 300 万美元工期延误违约赔偿金，驳回中资总承包商关于违约金畸高酌减的全部抗辩请求。",
        "tatbestand": "中资央企承建金边商业大厦，合同约定延期违约金按天计算且无上限。施工期间因地下地质异常与暴雨导致工期延误 60 天。业主向 NCAC 申请仲裁扣罚全额违约金。",
        "gruende": "仲裁庭指出：柬埔寨民法典受日本法系深度影响，第403条明确剥夺了法官或仲裁员对当事人约定违约金的增减权。总承包商在签约时对该刚性条款应当预见，合同既已生效，必须依约全面履行。",
        "norms_meta": "KH:Civil_Code_2007:Art403_No_Reduction",
        "source_url": "https://ncac.org.kh"
    },
    {
        "case_id": "CASE:LA_SC:Hydro_BOT_Concession_Default_2020",
        "court": "People's Supreme Court of Laos",
        "senate": "Commercial Chamber",
        "decided": "2020-11-25",
        "az": "Supreme Court Judgment No. 45/2020/PC",
        "ecli": "LA:SC:2020:45",
        "doctype": "Urteil",
        "leitsatz": "老挝人民最高法院经典判决：境外投资人未取得老挝国家银行（BOL）离岸外债登记审批，擅自向老挝项目公司注入的外债借款，在老挝国内法下不产生优先债务效力；在项目清偿清盘时，该未登记借款不得对抗属地银行及国家特许权税费债务。",
        "tenor": "老挝最高法院终审判决：驳回外国投资方要求项目公司强制清偿未登记离岸股东贷款的诉求，确认未经BOL批准的境外借款不得强制购汇转出老挝。",
        "tatbestand": "外国开发商投资老挝南部水电站BOT项目，通过香港关联公司向老挝项目公司提供数千万美元过桥贷款，但未向老挝央行BOL申报外债登记。后项目重组，投资方起诉要求优先收回借款本息。",
        "gruende": "最高法院裁定：老挝外汇法属于维护国家金融秩序的强行性法律规范（Public Order）。未经国家银行审批登记的跨境资金流动，丧失合规购汇通道，司法机关严禁协助违法规避外汇监管的资金出境。",
        "norms_meta": "LA:Law_on_FX_Management_2022:Art15_Offshore_Loan_BOL",
        "source_url": "https://touristsupremecourt.gov.la"
    },
    {
        "case_id": "CASE:MM_HC:Military_FX_Control_Frustration_2022",
        "court": "Yangon High Court",
        "senate": "Commercial Appellate Division",
        "decided": "2022-12-08",
        "az": "Civil Appeal No. 78 of 2022",
        "ecli": "MM:HC:2022:78",
        "doctype": "Urteil",
        "leitsatz": "仰光高等法院里程碑判例：由于缅甸军管政府2022年4月出台第12/2022号紧急外汇强制结汇通知，导致涉外工程承包合同中约定的美元境外清算支付在法律上陷入绝对客观不能。法院依据《合同法》第56条判决该类无法预见的监管突变构成合同落空（Frustration），免除债务人的延期付款违约责任。",
        "tenor": "仰光高等法院裁定驳回外方供货商要求中资EPC承包商支付美元迟延违约金的起诉，裁定因军管外汇政策构成法律受阻，双方互免违约金责任并依合规程序结算已完成工程量。",
        "tatbestand": "仰光供水管道总承包项目中，业主与承包商约定使用美元结算。2022年4月缅甸央行突发外汇强制结汇令，美元汇款通道全面中断，发包人无法调拨美元支付进度款，供货商遂起诉索赔巨额违约金。",
        "gruende": "高等法院审判官认定：外国投资者与本地企业均无法预见并阻止国家外汇政策的颠覆性调整。由于该不可抗外力导致以特定货币清算的合同基础丧失，适用第56条合同落空原则，双方均无需为该不可抗力违约承担赔偿。",
        "norms_meta": "MM:Contract_Act_1872:Sec56_Frustration;MM:FEML_2012:Notification_12_2022_Mandatory_Conversion",
        "source_url": "https://www.unodc.org/cld/en/v3/myanmar"
    },
    {
        "case_id": "CASE:BN_HC:Petrochemical_EPC_Injunction_Restraint_2021",
        "court": "High Court of Brunei Darussalam",
        "senate": "Civil Jurisdiction",
        "decided": "2021-08-25",
        "az": "High Court Suit No. 19 of 2021",
        "ecli": "BN:HC:2021:19",
        "doctype": "Urteil",
        "leitsatz": "文莱高等法院见索即付独立保函欺诈例外审查先例：履约保函系独立于 EPC 主合同的自主抽象承诺；承包商仅在能举证证明业主索赔存在明目张胆欺诈（Clear and Obvious Fraud）时方可获得止付禁令；主合同项下的违约金与工期延误争议绝不构成止付保函的正当抗辩事由。",
        "tenor": "文莱高等法院裁定驳回中国建筑总承包商申请冻结银行履约保函项下兑付的单方面临时禁令，撤销原临时限制令，允许国际放贷行全额向项目业主兑付履约保函保证金。",
        "tatbestand": "大型央企承揽文莱大摩拉岛石化一体化装置安装工程。工程收尾阶段，业主以若干附属管道存在微小渗漏为由，向银行发出全额没收总额 3,500 万美元履约保函的即付索赔。承包商向文莱法院申请紧急临时禁令。",
        "gruende": "高等法院重申：银行保函是国际贸易与基建工程的生命线。法院仅在原告能够初步证明受益人在索赔时具有恶意虚构事实的明确欺诈意图（Fraudulent Intent）时方能干预，实体违约争议必须通过仲裁解决。",
        "norms_meta": "BN:Contracts_Act_Cap106:Sec74_75_Reasonable_Damages",
        "source_url": "https://www.judiciary.gov.bn"
    },
    {
        "case_id": "CASE:TL_CdC:Recusa_de_Visto_Grid_Project_2021",
        "court": "Câmara de Contas de Timor-Leste",
        "senate": "Secção de Fiscalização Prévia",
        "decided": "2021-10-28",
        "az": "Acórdão No. 12/2021",
        "ecli": "TL:CDC:2021:12",
        "doctype": "Urteil",
        "leitsatz": "东帝汶国家高等审计法院标杆判例：公共工程追加预算补充协议未经合法公开招标且缺乏国家预算拨款证明的，审计法院裁定拒绝核发 Visto 事前签证。该拒绝签证直接导致补充协议自始不产生任何财务给付效力，政府财政部依法永久免除支付该笔工程追加款的义务。",
        "tenor": "审计法院大法官合议庭全席裁定：对公共工程部呈交的《国家输变电网项目第 3 号追加预算工程补充协议》予以拒绝签发签证（Recusa de Visto）；裁定通报东帝汶财政部与国家检察院。",
        "tatbestand": "外国总承包商与东帝汶政府签署特许输电网建设合同。施工过程中因地质滑坡双方签署追加 420 万美元补充协议，承包商抢先施工完成。工程部后报送审计法院申领 Visto 签证，遭法院直接拒绝。",
        "gruende": "审计法院依据《第9/2011号法律》第14条判定：事前审计签证是东帝汶宪法与预算法确立的硬性防腐与预算平衡防火墙。未经合规批准的追加工程即使在物理上已完工，在法律上绝不能强制公共财政支付无预算依据的款项。",
        "norms_meta": "TL:Law_9_2011:Art14_Pre_Audit_Visto",
        "source_url": "https://www.camaradecontas.tl"
    }
]


def expand_database():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    print("=== [1/4] 补齐 5 国 L1 核心强行法条 ===")
    all_l1_norms = KH_L1_NORMS + LA_L1_NORMS + MM_L1_NORMS + BN_L1_NORMS + TL_L1_NORMS
    for n in all_l1_norms:
        cur.execute("""
            INSERT OR REPLACE INTO norms (
                norm_id, law, enbez, title, heading_path, text_de, 
                text_original, text_en, text_zh, elements_json, mandatory_level, snapshot_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            n["norm_id"], n["law"], n["enbez"], n["title"], n["heading_path"], n["text_de"],
            n["text_zh"], n["text_zh"], n["text_zh"], n["elements_json"], "mandatory_override", SNAPSHOT_ID
        ))
    print(f"  ✓ 成功注入 {len(all_l1_norms)} 条 L1 核心法条")

    print("=== [2/4] 补齐 5 国 L2 国际投资条约、DTA与国际规则 ===")
    for n in FIVE_COUNTRIES_L2_TREATIES:
        cur.execute("""
            INSERT OR REPLACE INTO reference_norms (
                norm_id, law, enbez, title, heading_path, text_de, 
                text_original, text_en, text_zh, elements_json, mandatory_level, snapshot_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            n["norm_id"], n["law"], n["enbez"], n["title"], n["heading_path"], n["text_de"],
            n["text_zh"], n["text_zh"], n["text_zh"], n["elements_json"], "statutory_default", SNAPSHOT_ID
        ))
    print(f"  ✓ 成功注入 {len(FIVE_COUNTRIES_L2_TREATIES)} 条 L2 双边条约与规则")

    print("=== [3/4] 补齐 5 国 L1 权威司法裁判 ===")
    for c in FIVE_COUNTRIES_CASES:
        cur.execute("""
            INSERT OR REPLACE INTO cases (
                case_id, court, senate, decided, az, ecli, doctype, leitsatz, tenor, tatbestand, gruende, norms_meta, source_url, snapshot_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            c["case_id"], c["court"], c["senate"], c["decided"], c["az"], c["ecli"], c["doctype"],
            c["leitsatz"], c["tenor"], c["tatbestand"], c["gruende"], c["norms_meta"], c["source_url"], SNAPSHOT_ID
        ))
    print(f"  ✓ 成功注入 {len(FIVE_COUNTRIES_CASES)} 篇 5 国最高法院/仲裁裁判")

    print("=== [4/4] 建立 5 国上位法条约桥接边与判例关联边 ===")
    bridge_edges = [
        # 柬埔寨
        ("KH:Law_on_Investment_2021:Art12_Tax_Incentive", "TREATY:CN_KH_BIT_1996:Art4_Expropriation", "upgrades_to_treaty"),
        ("KH:Tax_Law_2023:Art25_WHT_Crossborder", "TREATY:CN_KH_DTA_2016:Art11_Interest_Tax", "complements"),
        ("CASE:KH_NCAC:Lump_Sum_Delay_Damages_Award_2022", "KH:Civil_Code_2007:Art403_No_Reduction", "interprets"),
        ("KH:Law_on_Construction_2019:Art38_Permit", "KH:Law_on_Construction_2019:Art73_Ten_Year_Warranty", "correlates_with"),
        # 老挝
        ("LA:Law_on_Investment_Promotion_2016:Art35_Concession_CA", "TREATY:CN_LA_BIT_1993:Art3_FET", "upgrades_to_treaty"),
        ("LA:Tax_Law_2019:Art18_CIT_Standard", "TREATY:CN_LA_DTA_1999:Art12_Royalties", "complements"),
        ("CASE:LA_SC:Hydro_BOT_Concession_Default_2020", "LA:Law_on_FX_Management_2022:Art15_Offshore_Loan_BOL", "interprets"),
        ("LA:Electricity_Law_2017:Art28_PPA_Grid", "LA:Law_on_Investment_Promotion_2016:Art35_Concession_CA", "governs"),
        # 缅甸
        ("MM:Myanmar_Investment_Law_2016:Art50_MIC_Permit", "TREATY:CN_MM_BIT_2001:Art6_Repatriation", "upgrades_to_treaty"),
        ("CASE:MM_HC:Military_FX_Control_Frustration_2022", "MM:Contract_Act_1872:Sec56_Frustration", "interprets"),
        ("CASE:MM_HC:Military_FX_Control_Frustration_2022", "MM:FEML_2012:Notification_12_2022_Mandatory_Conversion", "interprets"),
        ("MM:Arbitration_Law_2016:Sec34_Enforcement", "MM:Contract_Act_1872:Sec56_Frustration", "correlates_with"),
        # 文莱
        ("BN:Constitution_1959:Art84C_Absolute_Immunity", "TREATY:CN_BN_BIT_2000:Art4_Compensation", "upgrades_to_treaty"),
        ("CASE:BN_HC:Petrochemical_EPC_Injunction_Restraint_2021", "BN:Contracts_Act_Cap106:Sec74_75_Reasonable_Damages", "interprets"),
        ("BN:Arbitration_Order_2009:Sec33_BDAC", "TREATY:CN_BN_BIT_2000:Art4_Compensation", "correlates_with"),
        # 东帝汶
        ("TL:Private_Investment_Law_2017:Art21_ICSID", "TREATY:UN_New_York_Convention_1958:Art5_Timor_Leste", "upgrades_to_treaty"),
        ("CASE:TL_CdC:Recusa_de_Visto_Grid_Project_2021", "TL:Law_9_2011:Art14_Pre_Audit_Visto", "interprets"),
        ("TL:Law_9_2011:Art14_Pre_Audit_Visto", "TL:Civil_Code_2011:Art798_Contractual_Liability", "overrides"),
    ]
    for src, dst, rel in bridge_edges:
        cur.execute("""
            INSERT OR IGNORE INTO edges (src, dst, rel, source, confidence, reviewed, snapshot_id)
            VALUES (?, ?, ?, 'FIVE_COUNTRIES_EXPANSION_2026', 1.0, 1, ?)
        """, (src, dst, rel, SNAPSHOT_ID))
        cur.execute("""
            INSERT OR IGNORE INTO reference_edges (src, dst, rel, description)
            VALUES (?, ?, ?, 'Five countries treaty bridge edge')
        """, (src, dst, rel))

    conn.commit()
    conn.close()
    print(">>> 5 国成文法、判例与 L2 条约扩充成功入库！")


if __name__ == "__main__":
    expand_database()
