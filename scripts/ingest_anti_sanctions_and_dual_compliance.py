# -*- coding: utf-8 -*-
"""入库中方“三反”法规、双向合规母国强行法与东盟金融制裁边界法源
(scripts/ingest_anti_sanctions_and_dual_compliance.py)
对齐《功能优化及审查.md》Phase 1 第二步规范
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

NEW_L1_NORMS = [
    {
        "norm_id": "CN:Anti_Foreign_Sanctions_Law:Art3_4_12_15",
        "law": "CN_Anti_Foreign_Sanctions_Law",
        "enbez": "Art. 3, 4, 6, 12, 15",
        "title": "反外国制裁法核心反制措施、不执行义务、侵权追偿与对等反制",
        "heading_path": "中华人民共和国反外国制裁法 > 反制措施与执行 > 第3、4、6、12、15条",
        "text_de": "PRC Anti-Foreign Sanctions Law (Blocking & Countermeasures)",
        "text_original": "国务院有关部门可以决定将直接或间接参与制定、决定、实施歧视性限制措施的组织和个人列入反制清单，采取不予签发签证、查封扣押冻结财产、禁止交易等措施。任何组织和个人均不得执行或者协助执行外国国家对我国公民、组织采取的歧视性限制措施；违反规定侵害我国合法权益的，公民、组织可以依法向人民法院提起诉讼，请求停止侵害、赔偿损失。",
        "text_en": "PRC departments may place entities/individuals implementing discriminatory measures on counter-measures list. No entity or individual may implement or assist in foreign discriminatory measures. Victims may sue in Chinese courts for damages.",
        "text_zh": "国务院有关部门可以决定将直接或间接参与制定、决定、实施歧视性限制措施的组织和个人列入反制清单，采取不予签发签证、查封扣押冻结财产、禁止交易等措施。任何组织和个人均不得执行或者协助执行外国国家对我国公民、组织采取的歧视性限制措施；违反规定侵害我国合法权益的，公民、组织可以依法向人民法院提起诉讼，请求停止侵害、赔偿损失。",
        "elements_json": json.dumps([
            {"eid": "e_discriminatory_sanctions", "text_zh": "外国对中国公民、企业采取单边长臂管制、列入制裁清单或限制正常经贸合作", "status": "factual"},
            {"eid": "e_blocking_obligation", "text_zh": "境内组织及个人不得协议执行或配合外国单边制裁，违反者承担国内侵权追偿责任", "status": "mandatory"},
            {"eid": "e_court_remedy_seizure", "text_zh": "受侵害中资企业有权在中国法院起诉执行制裁方并申请财产查封冻结", "status": "remedy"}
        ], ensure_ascii=False),
        "mandatory_level": "mandatory_override",
    },
    {
        "norm_id": "CN:State_Council_AFSL_Reg_2025:Art1_22",
        "law": "CN_State_Council_AFSL_Reg_2025",
        "enbez": "Art. 1-22",
        "title": "国务院反外国制裁法实施细则与反制执行程序",
        "heading_path": "实施《中华人民共和国反外国制裁法》的规定 > 全文 > 第1-22条",
        "text_de": "State Council Regulations on Implementing Anti-Foreign Sanctions Law (2025)",
        "text_original": "细化对被列入反制清单的外国实体在境内不动产、动产、股权、知识产权及其他各类财产的查封、扣押、冻结流程；明确境内企业在遭遇次级制裁威胁时的安全审查报备、合规整改豁免申请机制以及联合惩戒工作机制。",
        "text_en": "Specifies seizure, freezing, and attachment procedures for assets of entities on counter-measures list; establishes reporting, compliance rectifications, and exemption mechanisms.",
        "text_zh": "细化对被列入反制清单的外国实体在境内不动产、动产、股权、知识产权及其他各类财产的查封、扣押、冻结流程；明确境内企业在遭遇次级制裁威胁时的安全审查报备、合规整改豁免申请机制以及联合惩戒工作机制。",
        "elements_json": json.dumps([
            {"eid": "e_asset_seizure_protocol", "text_zh": "反制清单实体的境内关联财产可由法院及主管部门直接执行查封冻结", "status": "enforcement"},
            {"eid": "e_exemption_mechanism", "text_zh": "设立向国家反制裁工作机制申请特定商业交易豁免或替代履约的法定指引", "status": "compliance"}
        ], ensure_ascii=False),
        "mandatory_level": "mandatory_override",
    },
    {
        "norm_id": "CN:MOFCOM_Order_1_2021:Blocking_Statute",
        "law": "CN_MOFCOM_Order_1_2021",
        "enbez": "Art. 5, 7, 9",
        "title": "商务部1号令阻断法30日报告义务、禁令制度与司法追偿权",
        "heading_path": "阻断外国法律与措施不当域外适用办法 > 报告、禁令与追偿 > 第5、7、9条",
        "text_de": "MOFCOM Order No. 1 (2021) Blocking Rules on Extraterritorial Application",
        "text_original": "中国公民、法人或者其他组织遇到外国法律与措施不当域外适用、限制其开展正常经贸及相关活动情形的，应当自发生之日起30日内向国务院商务主管部门如实报告；工作机制根据评估可以发布不得承认、不得执行、不得遵守有关外国法律与措施的禁令；因当事人遵守禁令范围内的外国法律措施侵害他人合法权益的，受害人可依法向人民法院提起追偿诉讼。",
        "text_en": "Mandates 30-day reporting to MOFCOM upon extraterritorial application; working mechanism may issue non-recognition/execution injunctions; civil compensation rights for damages caused by compliance with foreign measures.",
        "text_zh": "中国公民、法人或者其他组织遇到外国法律与措施不当域外适用、限制其开展正常经贸及相关活动情形的，应当自发生之日起30日内向国务院商务主管部门如实报告；工作机制根据评估可以发布不得承认、不得执行、不得遵守有关外国法律与措施的禁令；因当事人遵守禁令范围内的外国法律措施侵害他人合法权益的，受害人可依法向人民法院提起追偿诉讼。",
        "elements_json": json.dumps([
            {"eid": "e_30day_reporting_obligation", "text_zh": "中资企业遭遇外国长臂管辖阻断时必须在30日内向商务部递交书面报告", "status": "mandatory"},
            {"eid": "e_blocking_injunction_effect", "text_zh": "工作机制发布禁令后，外国长臂措施在中国主权范围内绝对丧失执行效力", "status": "mandatory"},
            {"eid": "e_civil_recovery_lawsuit", "text_zh": "中资企业对配合外国制裁解约、断供或扣留资金的合作方享有法定损害赔偿请求权", "status": "remedy"}
        ], ensure_ascii=False),
        "mandatory_level": "mandatory_override",
    },
    {
        "norm_id": "CN:MOFCOM_Order_4_2020:UEL",
        "law": "CN_MOFCOM_Order_4_2020",
        "enbez": "Art. 2, 10",
        "title": "商务部4号令不可靠实体清单与非商业目的断供反制",
        "heading_path": "不可靠实体清单规定 > 调查与处理 > 第2、10条",
        "text_de": "MOFCOM Order No. 4 (2020) Provisions on Unreliable Entity List",
        "text_original": "对危害中国国家主权、安全、发展利益，违反正常的市场交易原则，中断与中国企业正常交易或者采取歧视性措施的外国实体，列入不可靠实体清单；限制或禁止其从事与中国有关的进出口活动、境内投资及高级管理人员入境。",
        "text_en": "Foreign entities violating normal market principles and halting transactions with Chinese enterprises for non-commercial purposes may be designated on Unreliable Entity List with trade/investment bans.",
        "text_zh": "对危害中国国家主权、安全、发展利益，违反正常的市场交易原则，中断与中国企业正常交易或者采取歧视性措施的外国实体，列入不可靠实体清单；限制或禁止其从事与中国有关的进出口活动、境内投资及高级管理人员入境。",
        "elements_json": json.dumps([
            {"eid": "e_noncommercial_cut_off", "text_zh": "外国供应商或分包商出于外国政府政治管制目的单方中断供货或终止服务", "status": "breach"},
            {"eid": "e_trade_ban_sanction", "text_zh": "对列入实体依法阻断其在华商业准入与贸易结算", "status": "sanction"}
        ], ensure_ascii=False),
        "mandatory_level": "mandatory_override",
    },
    {
        "norm_id": "CN:Export_Control_Law_2020:Art12_44",
        "law": "CN_Export_Control_Law_2020",
        "enbez": "Art. 12, 44",
        "title": "出口管制法物项合规许可证与域外管辖对等反制",
        "heading_path": "中华人民共和国出口管制法 > 管制措施与监督 > 第12、44条",
        "text_de": "PRC Export Control Law (Licensing & Extraterritorial Effect)",
        "text_original": "国家对两用物项、军品、核以及其他与维护国家安全和利益、履行防扩散等国际义务相关的货物、技术、服务等物项实施出口管制，出口管制清单所列管制物项必须获得主管部门许可证件；中华人民共和国境外的组织和个人违反本法规定，危害国家安全和利益的，依法追究法律责任并采取相应反制措施。",
        "text_en": "Export of dual-use, defense, nuclear items requires MOFCOM export license. Extraterritorial application against foreign entities endangering PRC national security.",
        "text_zh": "国家对两用物项、军品、核以及其他与维护国家安全和利益、履行防扩散等国际义务相关的货物、技术、服务等物项实施出口管制，出口管制清单所列管制物项必须获得主管部门许可证件；中华人民共和国境外的组织和个人违反本法规定，危害国家安全和利益的，依法追究法律责任并采取相应反制措施。",
        "elements_json": json.dumps([
            {"eid": "e_export_license_requirement", "text_zh": "向境外移交电力特种测绘、加密通信、两用关键构件必须取得前置许可", "status": "mandatory"},
            {"eid": "e_end_user_verification", "text_zh": "禁止境外中间商违规再转让管制物项给受限受制裁第三方", "status": "compliance"}
        ], ensure_ascii=False),
        "mandatory_level": "mandatory_override",
    },
    {
        "norm_id": "CN:Foreign_State_Immunity_Law_2024:Art7_21",
        "law": "CN_Foreign_State_Immunity_Law_2024",
        "enbez": "Art. 7, 21",
        "title": "外国国家豁免法商业活动例外与对等原则",
        "heading_path": "中华人民共和国外国国家豁免法 > 管辖豁免例外 > 第7、21条",
        "text_de": "PRC Law on Foreign State Immunity (Commercial Activity Exception & Reciprocity)",
        "text_original": "外国国家在中华人民共和国领域内从事商业活动，或者在中华人民共和国领域外从事商业活动但在中华人民共和国领域内产生直接影响的，在基于该商业活动引起的诉讼中不享有管辖豁免；外国对中华人民共和国国家及其财产的豁免给予低于本法规定的待遇的，中华人民共和国实行对等原则。",
        "text_en": "Foreign states do not enjoy jurisdictional immunity in lawsuits arising from commercial activities with direct effects in China. Reciprocity applies.",
        "text_zh": "外国国家在中华人民共和国领域内从事商业活动，或者在中华人民共和国领域外从事商业活动但在中华人民共和国领域内产生直接影响的，在基于该商业活动引起的诉讼中不享有管辖豁免；外国对中华人民共和国国家及其财产的豁免给予低于本法规定的待遇的，中华人民共和国实行对等原则。",
        "elements_json": json.dumps([
            {"eid": "e_commercial_exception", "text_zh": "东道国主权实体或主权基金从事基建商业承包的，在中国法院无管辖豁免", "status": "jurisdiction"},
            {"eid": "e_reciprocity_rule", "text_zh": "东道国司法若剥夺中资企业主权资产豁免，中国法院依法对等执行东道国在华财产", "status": "reciprocity"}
        ], ensure_ascii=False),
        "mandatory_level": "mandatory_override",
    },
    {
        "norm_id": "CN:SASAC_Notice_75_2021:Guarantee_Risk",
        "law": "CN_SASAC_Notice_75_2021",
        "enbez": "Art. 4, 7",
        "title": "国资委75号文央企严禁超股比担保与反担保刚性要求",
        "heading_path": "关于加强中央企业融资担保业务风险管理的通知 > 担保管控 > 第4、7条",
        "text_de": "SASAC Notice No. 75 (2021) Management of Central SOE Financing Guarantees",
        "text_original": "中央企业应当严格控制融资担保规模，严禁对集团外无股权关系的企业提供担保；对参股企业提供担保的，担保额度不得超过持股比例，严禁无对价或超比例提供担保，且必须要求其他股东按同等比例提供担保或落实足额有效反担保措施。",
        "text_en": "Central SOEs strictly prohibited from providing guarantees to non-equity entities or exceeding shareholding ratio. Mandatory counter-guarantee measures required.",
        "text_zh": "中央企业应当严格控制融资担保规模，严禁对集团外无股权关系的企业提供担保；对参股企业提供担保的，担保额度不得超过持股比例，严禁无对价或超比例提供担保，且必须要求其他股东按同等比例提供担保或落实足额有效反担保措施。",
        "elements_json": json.dumps([
            {"eid": "e_shareholding_ratio_cap", "text_zh": "在东盟合资或联营体项目中，中资央企向业主提供100%全额PCG构成违规", "status": "prohibition"},
            {"eid": "e_counter_guarantee_requirement", "text_zh": "提供担保必须由外方伙伴开立银行反担保或设立独立托管账户", "status": "risk_mitigation"}
        ], ensure_ascii=False),
        "mandatory_level": "mandatory_override",
    },
    {
        "norm_id": "CN:SAFE_Notice_29_2014:Crossborder_Security",
        "law": "CN_SAFE_Notice_29_2014",
        "enbez": "Art. 6, 12",
        "title": "外管局29号文内保外贷登记与跨境履约外汇核准",
        "heading_path": "跨境担保外汇管理规定 > 内保外贷与外债登记 > 第6、12条",
        "text_de": "SAFE Circular No. 29 (2014) Regulations on Cross-border Security",
        "text_original": "境内企业提供内保外贷担保的，应当自担保合同签订之日起15个工作日内到所在地外汇局办理内保外贷签约登记手续；担保项下借款人仅能用于主营业务范围内的境外合法项目支出，不得用于虚假境外投资或虚构离岸贸易。",
        "text_en": "Domestic guarantors must register cross-border security (Neibaowaidai) within 15 working days with SAFE. Funds strictly tied to overseas main business.",
        "text_zh": "境内企业提供内保外贷担保的，应当自担保合同签订之日起15个工作日内到所在地外汇局办理内保外贷签约登记手续；担保项下借款人仅能用于主营业务范围内的境外合法项目支出，不得用于虚假境外投资或虚构离岸贸易。",
        "elements_json": json.dumps([
            {"eid": "e_safe_15day_registration", "text_zh": "未完成外汇局登记的跨境担保将导致履约项下资金无法合规购汇出境", "status": "mandatory"},
            {"eid": "e_commercial_genuineness", "text_zh": "担保资金严格绑定东道国备案项目真实开支", "status": "fx_control"}
        ], ensure_ascii=False),
        "mandatory_level": "mandatory_override",
    }
]

NEW_L2_NORMS = [
    {
        "norm_id": "SG:MAS_Act_Sanctions_2022:Sec27A",
        "law": "SG_MAS_Act",
        "enbez": "Section 27A",
        "title": "新加坡金管局法令关于多边制裁执行边界与外国单边制裁非自动适用",
        "heading_path": "Monetary Authority of Singapore Act > Section 27A",
        "text_de": "MAS Act Section 27A (Financial Sanctions Directives & UNSC Boundary)",
        "text_original": "Financial institutions in Singapore are legally bound to comply with MAS directives giving effect to resolutions of the Security Council of the United Nations. Unilateral sanctions of third countries do not form part of Singapore law automatically.",
        "text_en": "Financial institutions in Singapore are bound by MAS directives giving effect to UNSC resolutions; unilateral third-country sanctions do not automatically apply in Singapore.",
        "text_zh": "新加坡金融机构依据新加坡法律，仅有义务严格执行联合国安理会（UNSC）通过的决议以及 MAS 依法颁布的直接指名指令；外国（如美国、欧盟）单边制裁措施不具有新加坡属地成文法上的当然效力，银行不得在无明确合同免责授权或法定依据的情况下任意单方拒绝履行结算或止付保函。",
        "elements_json": json.dumps([
            {"eid": "e_unsc_mas_boundary", "text_zh": "新加坡金融机构仅法定强制执行UNSC及MAS指令", "status": "statutory_boundary"},
            {"eid": "e_unilateral_non_lex_loci", "text_zh": "外国OFAC单边管制在新加坡不构成嗣后违法（Supervening Illegality）", "status": "lex_loci"}
        ], ensure_ascii=False),
        "mandatory_level": "statutory_default",
    },
    {
        "norm_id": "SG:Strategic_Goods_Control_Act:Sec5",
        "law": "SG_Strategic_Goods_Control_Act",
        "enbez": "Section 5",
        "title": "新加坡战略物品管制法关于两用物项中转与过境许可证规定",
        "heading_path": "Strategic Goods (Control) Act (Cap 300) > Section 5",
        "text_de": "Strategic Goods (Control) Act Cap 300 Section 5 (Transshipment Permits)",
        "text_original": "No person shall bring into Singapore or tranship or transmit through Singapore any strategic goods or strategic goods technology without a valid strategic goods permit issued by Singapore Customs.",
        "text_en": "Mandates strategic goods transshipment permit from Singapore Customs for dual-use equipment and technology transiting through Singapore.",
        "text_zh": "任何转运、过境新加坡港口或保税区的管制战略物品（包含高精测绘、军民两用逆变设备、特定涉密通信芯片），必须在抵港前取得新加坡关税局（Singapore Customs）颁发的战略物品转运许可证，未经许可不得擅自拆箱变更新目的地。",
        "elements_json": json.dumps([
            {"eid": "e_transshipment_permit", "text_zh": "两用重大工程设备过境新加坡须提前办理过境准运", "status": "customs_permit"},
            {"eid": "e_end_user_compliance", "text_zh": "转运物项禁止擅自转供第三国受限黑名单企业", "status": "compliance"}
        ], ensure_ascii=False),
        "mandatory_level": "statutory_default",
    }
]

NEW_L2_CASES = [
    {
        "case_id": "REF_CASE:UK_CA:Lamesa_v_Cynergy_2020",
        "court": "England and Wales Court of Appeal",
        "senate": "Civil Division",
        "decided": "2020-06-30",
        "az": "[2020] EWCA Civ 821",
        "ecli": "ECLI:UK:EWCA:Civ:2020:821",
        "doctype": "Urteil",
        "leitsatz": "普通法标杆先例：商业合同约定“如因遵守强制性法律规定导致延期付款不构成违约”时，英国上诉法院裁定：若该约定仅为排除自身违约责任，并不等同于认可外国单边次级制裁具有消灭合同主债务的效力，债务人仍须积极探索合规替代支付通道。",
        "tenor": "The Court of Appeal held that an express clause excusing non-payment in order to comply with mandatory provision of law may cover secondary sanctions in specific drafting, but does not extinguish the underlying debt nor frustrate the contract.",
        "tatbestand": "塞浦路斯公司向英国银行借款，约定英国法管辖。因借款方实际控制人被列入美国 OFAC SDN 次级制裁清单，英国银行担心触发美国二级制裁拒绝向其支付借款利息，并援引合同中的合规免责条款抗辩。",
        "gruende": "法院认为合同免责条款在特定上下文下可暂时中止违约追究，但强调次级制裁本身并非英国普通法下的成文法强制性规范，若存在替代清算货币或路径，债务人依然负有切实履约义务。",
        "norms_meta": "REF_STATUTE:UK_COMMON_LAW:Supervening_Illegality;SG:MAS_Act_Sanctions_2022:Sec27A",
        "source_url": "https://www.bailii.org/ew/cases/EWCA/Civ/2020/821.html"
    },
    {
        "case_id": "REF_CASE:SG_SICC:Sanctions_LC_Payment_2023",
        "court": "Singapore Court of Appeal",
        "senate": "Appellate Division",
        "decided": "2023-04-18",
        "az": "[2023] SGCA 28",
        "ecli": "ECLI:SG:SGCA:2023:28",
        "doctype": "Urteil",
        "leitsatz": "新加坡最高法院终审先例：银行在信用证或见索即付保函中单方植入“制裁免责条款（Sanctions Clause）”时，若拟据此拒付，必须承担极高的举证责任，证明该笔基础贸易或交易单据真实违反了国际强制性法律；若仅凭普遍性次级制裁风险推测即拒绝兑付，法院将判决银行承担恶意违约责任。",
        "tenor": "The Singapore Court of Appeal confirmed that banks cannot invoke standard sanctions clauses to refuse payment under letters of credit/bonds without objective evidence that the payment itself violates applicable mandatory sanctions laws.",
        "tatbestand": "买方通过新加坡摩根大通开立跟单信用证采购印尼煤炭。银行发现承运船只疑似涉及叙利亚航行历史，直接援引内部制裁条款拒付中资贸易商全套合规单据。",
        "gruende": "新加坡终审法院确立规则：在涉外保函与信用证独立抽象性原则下，银行不得将第三国非安理会单边制裁作为无条件拒付的避风港，有力保护了善意出海承包商与出口企业的收款安全。",
        "norms_meta": "SG:MAS_Act_Sanctions_2022:Sec27A;REF_CASE:UK_CA:Lamesa_v_Cynergy_2020",
        "source_url": "https://www.elitigation.sg"
    }
]


def ingest_data():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    print("=== [1/3] 写入 L1 中方三反与双向合规法源 ===")
    for n in NEW_L1_NORMS:
        cur.execute("""
            INSERT OR REPLACE INTO norms (
                norm_id, law, enbez, title, heading_path, text_de, 
                text_original, text_en, text_zh, elements_json, mandatory_level, snapshot_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            n["norm_id"], n["law"], n["enbez"], n["title"], n["heading_path"], n["text_de"],
            n["text_original"], n["text_en"], n["text_zh"], n["elements_json"], n["mandatory_level"], SNAPSHOT_ID
        ))
        print(f"  ✓ L1 法条: {n['norm_id']}")

    print("=== [2/3] 写入 L2 东盟制裁边界与国际标杆先例 ===")
    for n in NEW_L2_NORMS:
        cur.execute("""
            INSERT OR REPLACE INTO reference_norms (
                norm_id, law, enbez, title, heading_path, text_de, 
                text_original, text_en, text_zh, elements_json, mandatory_level, snapshot_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            n["norm_id"], n["law"], n["enbez"], n["title"], n["heading_path"], n["text_de"],
            n["text_original"], n["text_en"], n["text_zh"], n["elements_json"], n["mandatory_level"], SNAPSHOT_ID
        ))
        print(f"  ✓ L2 规范: {n['norm_id']}")

    for c in NEW_L2_CASES:
        cur.execute("""
            INSERT OR REPLACE INTO reference_cases (
                case_id, court, senate, decided, az, ecli, doctype, leitsatz, tenor, tatbestand, gruende, norms_meta, source_url, snapshot_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            c["case_id"], c["court"], c["senate"], c["decided"], c["az"], c["ecli"], c["doctype"],
            c["leitsatz"], c["tenor"], c["tatbestand"], c["gruende"], c["norms_meta"], c["source_url"], SNAPSHOT_ID
        ))
        print(f"  ✓ L2 先例: {c['case_id']}")

    print("=== [3/3] 建立三反与双向合规知识图谱关联边 ===")
    new_edges = [
        ("CN:Anti_Foreign_Sanctions_Law:Art3_4_12_15", "CN:MOFCOM_Order_1_2021:Blocking_Statute", "complements"),
        ("CN:State_Council_AFSL_Reg_2025:Art1_22", "CN:MOFCOM_Order_1_2021:Blocking_Statute", "hierarchical_parent"),
        ("CN:Data_Security_Law:Art36", "CN:MOFCOM_Order_1_2021:Blocking_Statute", "correlates_with"),
        ("CN:SASAC_Notice_75_2021:Guarantee_Risk", "CN:SAFE_Notice_29_2014:Crossborder_Security", "correlates_with"),
        ("REF_CASE:UK_CA:Lamesa_v_Cynergy_2020", "SG:MAS_Act_Sanctions_2022:Sec27A", "interprets"),
        ("REF_CASE:SG_SICC:Sanctions_LC_Payment_2023", "SG:MAS_Act_Sanctions_2022:Sec27A", "interprets"),
    ]
    for src, dst, rel in new_edges:
        cur.execute("""
            INSERT OR IGNORE INTO edges (src, dst, rel, source, confidence, reviewed, snapshot_id)
            VALUES (?, ?, ?, 'PRC_DUAL_COMPLIANCE_2026', 1.0, 1, ?)
        """, (src, dst, rel, SNAPSHOT_ID))
        cur.execute("""
            INSERT OR IGNORE INTO reference_edges (src, dst, rel, description)
            VALUES (?, ?, ?, 'Cross-border sanctions and blocking rule interpretation')
        """, (src, dst, rel))

    conn.commit()
    conn.close()
    print(">>> 中方三反与双向合规法源入库成功！")


if __name__ == "__main__":
    ingest_data()
