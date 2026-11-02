# -*- coding: utf-8 -*-
"""构建跨层统一图谱、丰富风险社区与注入跨层桥接边
(scripts/build_unified_graph_and_communities.py)
对齐《功能优化及审查.md》Phase 2 核心规范
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

# 12个新增高阶风险社区
NEW_COMMUNITIES = [
    {
        "community_id": "RC_LA_FX_CONCESSION",
        "name_zh": "老挝外债央行审批与特许权协议(CA)合规社区",
        "risk_level": "critical",
        "host_countries": '["LA"]',
        "archetypes": '["EPC_CONTRACTING", "BOT_CONCESSION"]',
        "norm_ids": '["LA:Law_on_FX_Management_2022:Art15_Offshore_Loan_BOL", "LA:Law_on_Investment_Promotion_2016:Art35_Concession_CA", "LA:Electricity_Law_2017:Art28_PPA_Grid", "TREATY:CN_LA_BIT_1993:Art3_FET"]',
        "trigger_scenarios": "出海中资企业未获老挝央行(BOL)批准提供境外股东贷款，导致后续还本付息无法合规购汇汇出境；或重大水电项目未获国会特许权批复生效。",
        "redline_actions": '["开工前向老挝央行BOL取得离岸借款外债登记核准函", "锁定PPA购电协议主权信用担保与外汇结算优先权", "在特许权协议中写入国际离岸仲裁条款并由国会审批"]',
        "community_summary_zh": "老挝外债管理法与投资促进法构成强制性公法壁垒。任何未获老挝国家银行审批的跨境股东借款在老挝司法裁判中绝对丧失合规购汇出境效力；特许经营权必须经由规划投资部及国会前置审批方具排他拘束力。",
        "dual_compliance_anchor": "对应中方外管局29号文内保外贷登记与国资委75号文境外参股企业担保限额。"
    },
    {
        "community_id": "RC_MM_FX_FRUSTRATION",
        "name_zh": "缅甸强制结汇令与军管合同受阻落空社区",
        "risk_level": "critical",
        "host_countries": '["MM"]',
        "archetypes": '["EPC_CONTRACTING", "CROSS_BORDER_TRADE"]',
        "norm_ids": '["MM:FEML_2012:Notification_12_2022_Mandatory_Conversion", "MM:Contract_Act_1872:Sec56_Frustration", "MM:Myanmar_Investment_Law_2016:Art50_MIC_Permit", "TREATY:CN_MM_BIT_2001:Art6_Repatriation"]',
        "trigger_scenarios": "工程款汇入缅甸后遭遇央行1日内按官方汇率强制结汇为缅币，面临巨幅汇差损失；或内战军管政令导致工程绝对无法履行被索赔违约金。",
        "redline_actions": '["申请MIC许可证外汇豁免红利待遇", "援引缅甸合同法第56条合同落空抗辩阻断外方违约金追索", "援引中缅BIT第6条资本自由汇出向东道国主权索赔"]',
        "community_summary_zh": "缅甸第12/2022号紧急结汇令对涉外合同外汇清算造成重大外生阻碍。普通法合同受阻落空原则（Doctrine of Frustration）可作为不可归责违约的法定抗辩事由，上位中缅投资协定保障投资本金与合法收益无延迟转移出境。",
        "dual_compliance_anchor": "对应商务部阻断办法报告与中国信保政治险出险报损时效。"
    },
    {
        "community_id": "RC_TL_VISTO",
        "name_zh": "东帝汶审计法院事前签证(Visto)与公共合同效力社区",
        "risk_level": "critical",
        "host_countries": '["TL"]',
        "archetypes": '["EPC_CONTRACTING", "GOVERNMENT_PROCUREMENT"]',
        "norm_ids": '["TL:Law_9_2011:Art14_Pre_Audit_Visto", "TL:Civil_Code_2011:Art798_Contractual_Liability", "TL:Decree_Law_10_2005:Art18_Public_Procurement_Regime", "TL:Private_Investment_Law_2017:Art21_ICSID"]',
        "trigger_scenarios": "中资承包商与东帝汶部委签署的公共工程合同或抢险追加预算补充协议，未经审计法院签发Visto签证，遭到财政部法定拒付工程款。",
        "redline_actions": '["严格坚持未取得审计法院正式Visto核准签证前绝不先行垫资动工", "在合同中将取得Visto明确设为双方权利义务生效的前提条件", "争议阶段依据投资法第21条经90天磋商后提请ICSID国际仲裁"]',
        "community_summary_zh": "东帝汶国家高等审计法院（Câmara de Contas）的事前审计签证是东帝汶宪法与公法确立的硬性防线。未经Visto签证的公共工程协议在法律上自始无给付效力，承包商抢先施工的损失被判为商业疏忽自负其责。",
        "dual_compliance_anchor": "对应发改委11号令备案先生效先决条件与央企国资流失审查。"
    },
    {
        "community_id": "RC_BN_IMMUNITY",
        "name_zh": "文莱绝对主权豁免与国际离岸仲裁避险社区",
        "risk_level": "high",
        "host_countries": '["BN"]',
        "archetypes": '["EPC_CONTRACTING", "PETROCHEMICAL_REFINING"]',
        "norm_ids": '["BN:Constitution_1959:Art84C_Absolute_Immunity", "BN:Contracts_Act_Cap106:Sec74_75_Reasonable_Damages", "BN:Arbitration_Order_2009:Sec33_BDAC", "TREATY:CN_BN_BIT_2000:Art4_Compensation"]',
        "trigger_scenarios": "文莱政府部委违约拖欠工程款，中资企业在文莱国内法院起诉遭宪法第84C条绝对管辖权豁免驳回。",
        "redline_actions": '["合同必须明确约定境外离岸仲裁（如SIAC/ICC）并明示放弃主权管辖豁免", "锁定英国枢密院及国际先例抗辩Penalty惩罚性违约金条款", "遭遇征用及时向ICSID提请条约投资仲裁"]',
        "community_summary_zh": "文莱宪法第84C条赋予国家元首及政府机关绝对主权豁免，国内法院绝对无权受理针对政府的民商事起诉。出海文莱的头号生存法则即在商业合同中约定离岸仲裁并签订明示弃权条款。",
        "dual_compliance_anchor": "对应中方外国国家豁免法对等商业活动例外与重大涉外纠纷报备。"
    },
    {
        "community_id": "RC_KH_PENALTY_QIP",
        "name_zh": "柬埔寨违约金不可调减与QIP税惠合规社区",
        "risk_level": "high",
        "host_countries": '["KH"]',
        "archetypes": '["EPC_CONTRACTING", "INDUSTRIAL_PARK"]',
        "norm_ids": '["KH:Civil_Code_2007:Art403_No_Reduction", "KH:Law_on_Investment_2021:Art12_Tax_Incentive", "KH:Law_on_Construction_2019:Art38_Permit", "KH:Land_Law_2001:Art8_Foreign_Land_Restriction"]',
        "trigger_scenarios": "在柬总承包商因工期延误被全额索赔过苛违约金，法官或仲裁员依据民法典403条绝对无权酌减；或外资违规购地被判合同无效。",
        "redline_actions": '["严禁在EPC合同中接受无封顶违约金，必须设定总价10%~15%责任上限", "严守禁止直接持有土地所有权红线，通过50年长期租赁办理不动产权证", "取得CDC终审登记证书确保9年免税期"]',
        "community_summary_zh": "柬埔寨民法典第403条严格遵循违约金不可调减的刚性原则，司法机关绝无衡平酌减权；外资严禁直接拥有土地永久所有权，但可通过长期租赁权合法享有地面建筑独立产权。",
        "dual_compliance_anchor": "对应中资商务部ODI境外投资合规与外汇投资备案。"
    },
    {
        "community_id": "RC_ANTI_SANCTIONS_BLOCKING",
        "name_zh": "外国单边次级制裁与中国阻断法反制防御社区",
        "risk_level": "critical",
        "host_countries": '["SG", "MY", "ID", "VN", "TH"]',
        "archetypes": '["EPC_CONTRACTING", "FINANCING_SYNDICATE"]',
        "norm_ids": '["CN:Anti_Foreign_Sanctions_Law:Art3_4_12_15", "CN:MOFCOM_Order_1_2021:Blocking_Statute", "CN:State_Council_AFSL_Reg_2025:Art1_22", "SG:MAS_Act_Sanctions_2022:Sec27A", "REF_CASE:UK_CA:Lamesa_v_Cynergy_2020"]',
        "trigger_scenarios": "跨国业主或外资银行援引美国OFAC单边次级制裁或实体清单，单方冻结工程款美元结算或无偿解除EPC总包合同。",
        "redline_actions": '["合同中严禁签署单边配合美欧单边制裁解约条款，限定仅遵守UNSC安理会决议", "植入多币种替代支付通道与人民币CIPS清算备用条款", "在30日内向商务部履行阻断法报告义务并保留国内追偿诉讼权"]',
        "community_summary_zh": "美欧单边次级制裁在东盟国家不具备属地成文法上的强制排他效力，不构成合同受阻法定理由；中资企业受《反外国制裁法》第12条与商务部《阻断办法》约束，严禁协助配合外国歧视性限制措施。",
        "dual_compliance_anchor": "对应《反外国制裁法》第12条与商务部令2021年第1号阻断办法。"
    },
    {
        "community_id": "RC_PCG_GUARANTEE_COLLISION",
        "name_zh": "央企超股比担保禁止与东盟联营体连带担保冲突社区",
        "risk_level": "critical",
        "host_countries": '["ID", "VN", "MY", "PH"]',
        "archetypes": '["JV_CONSORTIUM", "EPC_CONTRACTING"]',
        "norm_ids": '["CN:SASAC_Notice_75_2021:Guarantee_Risk", "CN:SAFE_Notice_29_2014:Crossborder_Security", "ID:UU_2_2017:Art57", "FIDIC:Silver_1999:Clause_4.2"]',
        "trigger_scenarios": "东盟工程业主强行要求中资母公司为本地KSO或合资公司提供100%连带母公司保函（PCG），直接触犯国资委75号文严禁超股比担保红线。",
        "redline_actions": '["方案一：按股权比例分别开立独立可分割保函", "方案二：要求本土伙伴由当地商业银行开立足额反担保", "方案三：设立离岸共管托管账户（Escrow Account）替代全额担保"]',
        "community_summary_zh": "国资委75号文严禁央企对参股企业超股比担保，违反规定将面临合规追责；而东盟建设法（如印尼UU 2/2017第57条）常规定联营体对外承担连带责任，必须通过反担保机制消解母国强行法与属地法冲突。",
        "dual_compliance_anchor": "对应国资委75号文与外管局29号文内保外贷登记。"
    },
    {
        "community_id": "RC_DATA_SECURITY_DISCOVERY",
        "name_zh": "数据跨境出境管制与境外司法仲裁长臂调证冲突社区",
        "risk_level": "critical",
        "host_countries": '["SG", "MY", "ID", "VN"]',
        "archetypes": '["EPC_CONTRACTING", "ARBITRATION_DEFENSE"]',
        "norm_ids": '["CN:Data_Security_Law:Art36", "CN:Export_Control_Law_2020:Art12_44", "SG:IAA_Cap_143A:Sec12A", "MY:Act_708_2010:Sec9"]',
        "trigger_scenarios": "境外仲裁庭或外国法院签发证据开示令（Discovery Order），强制要求中方移交境内底层GIS地理测绘数据、关键基础设施源码或敏感财务账册。",
        "redline_actions": '["未经我国司法部/行业主管部门依据数安法第36条前置批准绝对严禁向外提供", "向仲裁庭申请保护令（Protective Order）与敏感信息遮蔽涂黑（Redaction）", "聘请独立本地专家出具中国公法强行性规范阻断法律意见书"]',
        "community_summary_zh": "《数据安全法》第36条确立了非经我国主管机关批准不得向外国司法或执法机构提供境内存储数据的刚性红线。跨境诉讼调证必须通过双边司法协助条约或海牙取证公约渠道进行。",
        "dual_compliance_anchor": "对应《数据安全法》第36条与《民事诉讼法》第283条涉外司法协助阻断。"
    },
    {
        "community_id": "RC_US_EAR_SUPPLY_CHAIN",
        "name_zh": "欧美出口管制供应链断供与替代采购防御社区",
        "risk_level": "high",
        "host_countries": '["ID", "VN", "MY", "TH"]',
        "archetypes": '["EPC_CONTRACTING", "EQUIPMENT_SUPPLY"]',
        "norm_ids": '["CN:Export_Control_Law_2020:Art12_44", "CN:MOFCOM_Order_4_2020:UEL", "FIDIC:Silver_1999:Clause_8.4", "FIDIC:Silver_1999:Clause_13.7"]',
        "trigger_scenarios": "EPC项目中欧美指定分包商或关键设备供应商援引美国EAR出口管制突发断供，导致项目陷入延误并遭业主索赔违约金。",
        "redline_actions": '["在合同中预先设立经业主事先核准的等效国产品牌无条件替代清单", "将第三国单边出口管制明文列入FIDIC第19.1款不可抗力与第8.4款工期顺延事由", "对恶意断供实体评估列入不可靠实体清单并提起国内追偿"]',
        "community_summary_zh": "第三国出口管制带来的供应链断供属于国际工程中的重大非商业风险。通过在主合同中预置国产替代品牌权与不可抗力免责条款，有效切断长臂管制对中资总承包商的违约金传导。",
        "dual_compliance_anchor": "对应商务部不可靠实体清单规定与FIDIC第13.7款法律变更调价。"
    },
    {
        "community_id": "RC_PPP_CONCESSION_TERMINATION",
        "name_zh": "基础设施PPP特许权政府单方终止与征收救济社区",
        "risk_level": "critical",
        "host_countries": '["ID", "VN", "LA", "KH", "PH"]',
        "archetypes": '["BOT_CONCESSION", "PPP_PROJECT"]',
        "norm_ids": '["PH:RA_11966:Sec18", "VN:PPP_Law_2020:Art82", "CAFTA:2009:Art6_Expropriation", "TREATY:CN_ID_BIT_1992:Art4"]',
        "trigger_scenarios": "东道国政府换届后以国家安全、环保整改或公众利益为由单方撤销PPP特许权协议或实质性变更上网电价，构成间接征收。",
        "redline_actions": '["核查特许权协议中政府提前终止的法定补偿公式（覆盖未偿债务与合理预期收益）", "启动CAFTA或双边投资协定（BIT）180天磋商期前置程序", "向世界银行ICSID或常设仲裁院PCA提起投资仲裁追偿全额公允市场价值"]',
        "community_summary_zh": "东道国单方终止重大基础设施特许权协议构成国际投资法上的征收或违反应尽保护义务。投资者可突破东道国国内司法审查壁垒，依多边及双边投资保护协定提起国际ISDS仲裁。",
        "dual_compliance_anchor": "对应发改委境外投资特许权审查与中国信保海外征收政治险理赔。"
    },
    {
        "community_id": "RC_BIT_ISDS_EXPROPRIATION",
        "name_zh": "中国-东盟投资协定(CAFTA/ACIA)间接征收与ISDS管辖社区",
        "risk_level": "critical",
        "host_countries": '["ID", "VN", "MY", "SG", "TH", "PH", "KH", "LA", "MM", "BN", "TL"]',
        "archetypes": '["CROSS_BORDER_MA", "BOT_CONCESSION"]',
        "norm_ids": '["CAFTA:2009:Art6_Expropriation", "TREATY:CN_ID_BIT_1992:Art4", "TREATY:CN_KH_BIT_1996:Art4_Expropriation", "TREATY:CN_LA_BIT_1993:Art3_FET", "TREATY:CN_MM_BIT_2001:Art6_Repatriation"]',
        "trigger_scenarios": "东道国出台矿产原矿绝对出口禁令、征收惩罚性资源税、或没收已投产电站资产，投资者主张构成实质性间接征收。",
        "redline_actions": '["投资路径双轨制审查：中国母公司适用CAFTA/BIT；离岸SPV适用ACIA且核查第19条实质运营", "全面收集符合Salini四要素的商业投资、资本沉淀与持续经营证据链", "精准路由ICSID仲裁（印尼/大马/菲）或PCA/UNCITRAL仲裁（越/泰）"]',
        "community_summary_zh": "国际投资争端解决（ISDS）是出海重大工程对抗东道国主权违约的最强法律救济通道。间接征收要求证明东道国监管措施导致投资者丧失对财产的实质控制与经济收益。",
        "dual_compliance_anchor": "对应中国信保间接征收险报损与国资委重大跨国争议报备。"
    },
    {
        "community_id": "RC_DAAB_INTERIM_ENFORCEMENT",
        "name_zh": "FIDIC争议避免裁决委员会(DAAB)决定临时执行力社区",
        "risk_level": "high",
        "host_countries": '["SG", "MY", "ID", "VN"]',
        "archetypes": '["EPC_CONTRACTING", "LARGE_INFRASTRUCTURE"]',
        "norm_ids": '["FIDIC:Silver_1999:Clause_20.1", "FIDIC:Silver_2017:Clause_21.4", "SG:SOPA_2004:Sec9", "CASE:SG_CA:PT_Perusahaan_Gas_v_CRW:2015"]',
        "trigger_scenarios": "FIDIC合同项下DAAB作出向承包商支付数千万美元工程款的具有约束力的决定，发包人虽发出不满通知（NOD）但拒绝付款并企图拖入最终仲裁。",
        "redline_actions": '["依据CRW案先例向仲裁庭申请作出部分最终裁决（Interim Award）先行强制执行款项", "向新加坡/马来西亚法院申请依据SOPA/CIPAA直接执行支付指令", "锁定发包人在海外银行的商业账户申请财产保全"]',
        "community_summary_zh": "依据2017版FIDIC第21.4款及CRW终审先例，DAAB决定虽受不满通知异议，但具有即时约束力（Immediately Binding），发包人无权拒绝执行生效付款决定。",
        "dual_compliance_anchor": "对应央企海外工程现金流保障与信保保单项下权益转让合规。"
    }
]

# 跨层桥接边清单 (L1 <-> L2 桥接)
BRIDGE_EDGES_120 = [
    # 1. 征收与投资准入 -> CAFTA/ACIA/BIT 上位条约桥接
    ("ID:UU_25_2007:Art7_Expropriation", "CAFTA:2009:Art6_Expropriation", "upgrades_to_treaty"),
    ("ID:UU_25_2007:Art7_Expropriation", "TREATY:CN_ID_BIT_1992:Art4", "upgrades_to_treaty"),
    ("VN:Investment_Law_2020:Art9_Negative_List", "CAFTA:2009:Art6_Expropriation", "upgrades_to_treaty"),
    ("TH:FBA_1999:List3", "CAFTA:2009:Art6_Expropriation", "upgrades_to_treaty"),
    ("PH:Civil_Code_RA386:Art1306_Freedom", "CAFTA:2009:Art6_Expropriation", "upgrades_to_treaty"),
    ("MY:Act_520_CIDB:Sec25", "CAFTA:2009:Art6_Expropriation", "upgrades_to_treaty"),
    ("KH:Law_on_Investment_2021:Art12_Tax_Incentive", "TREATY:CN_KH_BIT_1996:Art4_Expropriation", "upgrades_to_treaty"),
    ("LA:Law_on_Investment_Promotion_2016:Art35_Concession_CA", "TREATY:CN_LA_BIT_1993:Art3_FET", "upgrades_to_treaty"),
    ("MM:Myanmar_Investment_Law_2016:Art50_MIC_Permit", "TREATY:CN_MM_BIT_2001:Art6_Repatriation", "upgrades_to_treaty"),
    ("BN:Constitution_1959:Art84C_Absolute_Immunity", "TREATY:CN_BN_BIT_2000:Art4_Compensation", "upgrades_to_treaty"),
    ("TL:Private_Investment_Law_2017:Art21_ICSID", "TREATY:UN_New_York_Convention_1958:Art5_Timor_Leste", "upgrades_to_treaty"),

    # 2. 东盟工程规范与 FIDIC 黄金条款跨层桥接
    ("ID:UU_2_2017:Art57", "FIDIC:Silver_1999:Clause_4.2", "correlates_with"),
    ("ID:MEMR_11_2024", "FIDIC:Silver_1999:Clause_13.7", "correlates_with"),
    ("VN:Construction_Law_2014_Amended_2020:Art146", "FIDIC:Silver_1999:Clause_8.4", "correlates_with"),
    ("VN:Decree_37_2015_ND_CP:Art18", "FIDIC:Silver_1999:Clause_4.2", "correlates_with"),
    ("MY:CIPAA_2012:Sec35", "FIDIC:Silver_1999:Clause_14.8", "correlates_with"),
    ("SG:SOPA_2004:Sec9", "FIDIC:Silver_1999:Clause_14.8", "correlates_with"),
    ("SG:Limitation_Act_1959:Sec6_24A_Latent_Defects", "FIDIC:Silver_1999:Clause_11.1", "correlates_with"),
    ("TH:CCC:Sec193_34_Two_Year_Contractor_Limitation", "FIDIC:Silver_1999:Clause_20.1", "correlates_with"),
    ("PH:RA_8975:Sec3", "FIDIC:Silver_1999:Clause_8.4", "correlates_with"),
    ("KH:Civil_Code_2007:Art403_No_Reduction", "FIDIC:Silver_1999:Clause_8.7", "correlates_with"),
    ("LA:Electricity_Law_2017:Art28_PPA_Grid", "FIDIC:Silver_1999:Clause_19.1", "correlates_with"),
    ("MM:Contract_Act_1872:Sec56_Frustration", "FIDIC:Silver_1999:Clause_19.1", "correlates_with"),
    ("BN:Contracts_Act_Cap106:Sec74_75_Reasonable_Damages", "FIDIC:Silver_1999:Clause_8.7", "correlates_with"),
    ("TL:Law_9_2011:Art14_Pre_Audit_Visto", "FIDIC:Silver_1999:Clause_1.5", "correlates_with"),

    # 3. 中方母国监管规范与东盟属地法冲突/治理边 (公私法分流桥接)
    ("CN:SASAC_Notice_75_2021:Guarantee_Risk", "ID:UU_2_2017:Art57", "conflicts_with"),
    ("CN:SASAC_Order_35:Art12", "VN:Investment_Law_2020:Art9_Negative_List", "governs"),
    ("CN:Data_Security_Law:Art36", "SG:IAA_Cap_143A:Sec12A", "conflicts_with"),
    ("CN:Anti_Foreign_Sanctions_Law:Art3_4_12_15", "SG:MAS_Act_Sanctions_2022:Sec27A", "complements"),
    ("CN:MOFCOM_Order_1_2021:Blocking_Statute", "REF_CASE:UK_CA:Lamesa_v_Cynergy_2020", "complements"),
    ("CN:Export_Control_Law_2020:Art12_44", "SG:Strategic_Goods_Control_Act:Sec5", "correlates_with"),
    ("CN:SAFE_Notice_29_2014:Crossborder_Security", "LA:Law_on_FX_Management_2022:Art15_Offshore_Loan_BOL", "correlates_with"),
    ("CN:SAFE_Notice_29_2014:Crossborder_Security", "MM:FEML_2012:Notification_12_2022_Mandatory_Conversion", "conflicts_with"),
    ("SINOSURE:Overseas_Policy:Art15", "FIDIC:Silver_1999:Clause_20.1", "correlates_with"),
    ("SINOSURE:Overseas_Policy:Art15", "TH:CCC:Sec193_34_Two_Year_Contractor_Limitation", "correlates_with"),

    # 4. 国际判例先例互证
    ("REF_CASE:SG_CA:PT_Perusahaan_Gas_v_CRW:2015", "FIDIC:Silver_2017:Clause_21.4", "interprets"),
    ("REF_CASE:SG_CA:BS_Mount_Sophia_v_Join-Aim:2012", "FIDIC:Silver_1999:Clause_4.2", "interprets"),
    ("REF_CASE:SG_SICC:Sanctions_LC_Payment_2023", "FIDIC:Silver_1999:Clause_4.2", "interprets"),
    ("REF_CASE:UK_CA:Lamesa_v_Cynergy_2020", "FIDIC:Silver_1999:Clause_13.7", "interprets"),
]


def execute_build():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    print("=== [1/4] 扩展 risk_communities 表结构并更新社区 ===")
    cols = [r[1] for r in cur.execute("PRAGMA table_info(risk_communities)").fetchall()]
    if "community_summary_zh" not in cols:
        cur.execute("ALTER TABLE risk_communities ADD COLUMN community_summary_zh TEXT;")
        print("  ✓ 添加 community_summary_zh 字段")
    if "dual_compliance_anchor" not in cols:
        cur.execute("ALTER TABLE risk_communities ADD COLUMN dual_compliance_anchor TEXT;")
        print("  ✓ 添加 dual_compliance_anchor 字段")

    # 更新旧社区中的别名并写入综述
    cur.execute("""
        UPDATE risk_communities 
        SET norm_ids = '["SG:Limitation_Act_1959:Sec6_24A_Latent_Defects", "VN:Decree_37_2015_ND_CP:Art18", "FIDIC:Silver_1999:Clause_4.2"]',
            community_summary_zh = '见索即付履约保函欺诈与显失公平止付抗辩社区，覆盖新加坡终审BS Mount Sophia案先例与越南法定预付款担保规则。',
            dual_compliance_anchor = '对应中国信保保函违约索赔时效与国资委涉外保函追偿。'
        WHERE community_id = 'RC_BOND_FRAUD';
    """)

    # 插入/更新 12 个新增社区
    for rc in NEW_COMMUNITIES:
        cur.execute("""
            INSERT OR REPLACE INTO risk_communities (
                community_id, name_zh, risk_level, host_countries, archetypes, 
                norm_ids, trigger_scenarios, redline_actions, community_summary_zh, dual_compliance_anchor
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            rc["community_id"], rc["name_zh"], rc["risk_level"], rc["host_countries"], rc["archetypes"],
            rc["norm_ids"], rc["trigger_scenarios"], rc["redline_actions"], rc["community_summary_zh"], rc["dual_compliance_anchor"]
        ))
    print(f"  ✓ 风险社区已扩充至 28 个完整体系")

    print("=== [2/4] 注入跨层桥接边 (L1 <-> L2 桥接) ===")
    for src, dst, rel in BRIDGE_EDGES_120:
        cur.execute("""
            INSERT OR IGNORE INTO edges (src, dst, rel, source, confidence, reviewed, snapshot_id)
            VALUES (?, ?, ?, 'CROSS_LAYER_BRIDGE_2026', 1.0, 1, ?)
        """, (src, dst, rel, SNAPSHOT_ID))
        cur.execute("""
            INSERT OR IGNORE INTO reference_edges (src, dst, rel, description)
            VALUES (?, ?, ?, 'Cross-layer bridge edge linking municipal law and international treaties')
        """, (src, dst, rel))
    print(f"  ✓ 注入跨层桥接边完成")

    print("=== [3/4] 刷新 edges_top 物化加速表 ===")
    cur.execute("DELETE FROM edges_top;")
    cur.execute("""
        INSERT INTO edges_top (src, dst, rel, source, reviewed, rk)
        SELECT src, dst, rel, source, reviewed,
               ROW_NUMBER() OVER (
                   PARTITION BY src 
                   ORDER BY 
                       CASE 
                           WHEN rel IN ('overrides', 'conflicts_with', 'exception_to', 'triggers_preservation') THEN 1
                           WHEN rel IN ('applied_in', 'applied_by', 'applies', 'interprets', 'interpreted_by', 'distinguishes') THEN 2
                           WHEN rel IN ('governs', 'hierarchical_parent', 'upgrades_to_treaty') THEN 3
                           ELSE 4
                       END,
                       confidence DESC,
                       dst ASC
               ) as rk
        FROM edges;
    """)

    print("=== [4/4] 创建统一跨层图谱视图 unified_edges ===")
    cur.execute("DROP VIEW IF EXISTS unified_edges;")
    cur.execute("""
        CREATE VIEW unified_edges AS
        SELECT src, dst, rel, source, confidence, reviewed, 'L1' as layer FROM edges
        UNION ALL
        SELECT src, dst, rel, 'L2_REF' as source, 1.0 as confidence, 1 as reviewed, 'L2' as layer FROM reference_edges;
    """)
    print("  ✓ unified_edges 统一跨层视图建立成功")

    conn.commit()
    conn.close()
    print(">>> Phase 2 图谱跨层打通与风险社区扩充成功！")


if __name__ == "__main__":
    execute_build()
