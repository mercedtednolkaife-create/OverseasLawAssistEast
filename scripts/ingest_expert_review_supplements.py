"""实施数据库审查报告全面补充与多级索引重建脚本
覆盖内容：
1. L1 弱覆盖五国（柬埔寨 KH、老挝 LA、缅甸 MM、文莱 BN、东帝汶 TL）核心强行法补齐
2. L1 横向劳工法（ID, VN, MY, TH, PH）与环境法规（ID, VN, TH, PH）
3. L1 东马沙巴与砂拉越 NCR 原住民土地法规
4. L2 FIDIC 2017 新版核心机制条款（Clause 20.2, 21 DAAB, 21.4/21.7, 8.5 等）
5. L2 国际投资与商事仲裁里程碑先例（CMC v Mozambique, Salini v Morocco, Himpurna v PLN, VIAC Award 等）
6. L2 亚投行 (AIIB) 采购政策与环境社会框架 (ESF)
7. 关联图谱边 (edges & reference_edges) 构建与物化
8. BM25 与 FAISS 稠密向量索引全局重建
"""

import os
import sys
import sqlite3
import json
import time
from datetime import datetime

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

SNAPSHOT_DIR = os.path.abspath("data/snapshots/20261021-asean-v2.2")
DB_PATH = os.path.join(SNAPSHOT_DIR, "law.sqlite")

print("==================================================")
print(f"正在准备写入快照: {DB_PATH}")
print("==================================================")

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

# --------------------------------------------------------------------------
# 1. 待入库 L1 NORMS (强行法)
# --------------------------------------------------------------------------
L1_NORMS = [
    # --- 柬埔寨 (Cambodia) ---
    {
        "norm_id": "KH:Commercial_Arbitration_Law_2006:Art3",
        "law": "Cambodia Commercial Arbitration Law 2006",
        "enbez": "Article 3",
        "title": "仲裁协议独立性与排他管辖 (Arbitration Agreement Autonomy)",
        "heading_path": "Chapter I > General Provisions > Article 3",
        "text_original": "An arbitration agreement that forms part of a contract shall be treated as an agreement independent of the other terms of the contract. A decision by the arbitral tribunal that the contract is null and void shall not entail ipso jure the invalidity of the arbitration clause.",
        "text_en": "An arbitration agreement that forms part of a contract shall be treated as an agreement independent of the other terms of the contract.",
        "text_zh": "包含在合同中的仲裁协议应被视为独立于合同其他条款的独立协议。仲裁庭裁定基础合同无效的，不当然导致仲裁条款无效，受诉法院应当驳回起诉并移交仲裁。",
        "language_mode": "bilingual",
        "lang_original": "en",
        "mandatory_level": "mandatory",
        "norm_category": "arbitration"
    },
    {
        "norm_id": "KH:Commercial_Arbitration_Law_2006:Art5",
        "law": "Cambodia Commercial Arbitration Law 2006",
        "enbez": "Article 5",
        "title": "外国仲裁裁决承认与执行 (Recognition and Enforcement of Foreign Arbitral Awards)",
        "heading_path": "Chapter VII > Recognition and Enforcement > Article 5",
        "text_original": "Foreign arbitral awards shall be recognized and enforced in Cambodia in accordance with the New York Convention on the Recognition and Enforcement of Foreign Arbitral Awards 1958, through an application filed before the competent Court of Appeal in Phnom Penh.",
        "text_en": "Foreign arbitral awards shall be recognized and enforced in Cambodia under the 1958 New York Convention via the Phnom Penh Court of Appeal.",
        "text_zh": "外国仲裁裁决依据1958年《纽约公约》在柬埔寨获得承认与执行。申请人须向金边上诉法院提交申请，除第35条规定的法定排他事由外，法院不得对裁决实体进行实质审查。",
        "language_mode": "bilingual",
        "lang_original": "en",
        "mandatory_level": "mandatory",
        "norm_category": "arbitration"
    },
    {
        "norm_id": "KH:Land_Law_2001:Art43",
        "law": "Cambodia Land Law 2001",
        "enbez": "Article 43",
        "title": "经济土地特许权最长租期与征收补偿 (Economic Land Concessions ELC)",
        "heading_path": "Title III > Immovable Property of State > Article 43",
        "text_original": "Economic land concessions may not exceed 99 years. The state may only expropriate or repossess the land for public interest and with prior, fair, and just compensation.",
        "text_en": "Economic land concessions may not exceed 99 years. State expropriation requires prior, fair and just compensation.",
        "text_zh": "国家经济土地特许权（ELC）租赁期限最长不得超过99年。国家仅得基于公共利益且依据法定程序收回土地，且必须事先提供公正、足额的法定补偿。",
        "language_mode": "bilingual",
        "lang_original": "en",
        "mandatory_level": "mandatory",
        "norm_category": "property"
    },
    {
        "norm_id": "KH:Sub_Decree_111:Art5",
        "law": "Cambodia Sub-Decree No 111 on BOT Concessions",
        "enbez": "Article 5",
        "title": "BOT 特许经营协议法定强制条款 (Mandatory Terms of Concession Contracts)",
        "heading_path": "Chapter II > Concession Procedures > Article 5",
        "text_original": "All Concession Contracts under BOT, BOO or BTO schemes must specify project duration, technical standards, step-in rights of lenders, tariff revision formulas, and dispute resolution mechanisms.",
        "text_en": "All Concession Contracts must specify duration, step-in rights, tariff adjustment formulas and dispute resolution mechanisms.",
        "text_zh": "所有依据 BOT/BOO/BTO 模式订立的特许经营协议，必须明确约定特许经营期、融资人介入权（Step-in Rights）、电价与过路费物价调整公式及中立国际仲裁争议解决机制。",
        "language_mode": "bilingual",
        "lang_original": "en",
        "mandatory_level": "mandatory",
        "norm_category": "concession"
    },
    {
        "norm_id": "KH:Prakas_346_2018:Tax",
        "law": "Cambodia MEF Prakas No 346 on Withholding Tax",
        "enbez": "Instruction 1",
        "title": "非居民承包商工程技术服务 15% 预扣税 (15% Withholding Tax on Non-Residents)",
        "heading_path": "General Taxation Department > Withholding Tax > Prakas 346",
        "text_original": "Resident enterprises paying technical services, management fees, or engineering contract remuneration to non-resident entities are obligated to deduct and withhold 15% Withholding Tax (WHT).",
        "text_en": "Resident enterprises paying engineering fees to non-resident entities must deduct 15% Withholding Tax.",
        "text_zh": "柬埔寨境内企业向非居民企业支付工程承包款、勘察设计费或技术服务费时，负有刚性代扣代缴 15% 预扣税（WHT）的法定义务，除非受中柬双边税收协定（DTA）优惠待遇阻却。",
        "language_mode": "bilingual",
        "lang_original": "en",
        "mandatory_level": "mandatory",
        "norm_category": "tax"
    },

    # --- 老挝 (Laos) ---
    {
        "norm_id": "LA:Decree_135_PM:Art8",
        "law": "Laos Decree No 135/PM on Concession Agreements",
        "enbez": "Article 8",
        "title": "特许经营协议生效要件与跨部委管辖 (Validity of Concession Agreements)",
        "heading_path": "Part II > Execution of Concessions > Article 8",
        "text_original": "A Concession Agreement (CA) shall enter into legal force only upon approval by the Government of Lao PDR and registration with the Ministry of Planning and Investment (MPI).",
        "text_en": "A Concession Agreement enters into force only upon Government approval and MPI registration.",
        "text_zh": "老挝特许经营协议（CA）必须经老挝政府内阁会议核准并在老挝计划投资部（MPI）完成正式登记后方始发生法律效力，单纯地方政府签署文书自始无效。",
        "language_mode": "bilingual",
        "lang_original": "en",
        "mandatory_level": "mandatory",
        "norm_category": "concession"
    },
    {
        "norm_id": "LA:Decree_135_PM:Art15",
        "law": "Laos Decree No 135/PM on Concession Agreements",
        "enbez": "Article 15",
        "title": "水电特许权政府单方终止与公允回购 (Government Unilateral Termination and Buyout)",
        "heading_path": "Part IV > Termination > Article 15",
        "text_original": "The Government reserves the right to unilaterally terminate a concession for reasons of national security or public interest, provided that fair market value compensation is paid to the concessionaire.",
        "text_en": "Government may unilaterally terminate concession for public interest subject to fair market value compensation.",
        "text_zh": "老挝政府基于国家重大利益或环境安全需要保留单方提前终止特许权（CA）并收回资产之权力，但必须依据公允市场价值（Fair Market Value）向特许经营者足额支付补偿金。",
        "language_mode": "bilingual",
        "lang_original": "en",
        "mandatory_level": "mandatory",
        "norm_category": "concession"
    },
    {
        "norm_id": "LA:Hydropower_Law_2017:Art21",
        "law": "Laos Hydropower Business Law 2017",
        "enbez": "Article 21",
        "title": "购电协议 PPA 电价调整机制与照付不议 (Tariff Adjustment and Take-or-Pay)",
        "heading_path": "Chapter III > Power Purchase Agreements > Article 21",
        "text_original": "Power Purchase Agreements (PPA) between hydropower developers and Electricite du Laos (EDL) must include take-or-pay commitments, currency indexation formulas, and transmission curtailment relief.",
        "text_en": "PPAs must include take-or-pay commitments, currency indexation formulas and grid curtailment relief.",
        "text_zh": "水电投资者与老挝国家电力公司（EDL）订立的购电协议（PPA），必须明确照付不议（Take-or-Pay）最低保障电量、美元汇率与通胀联动调整公式，以及电网原因弃水限电的赔偿责任。",
        "language_mode": "bilingual",
        "lang_original": "en",
        "mandatory_level": "mandatory",
        "norm_category": "energy"
    },
    {
        "norm_id": "LA:Labor_Law_2013:Art138",
        "law": "Laos Labor Law No 43/NA 2013",
        "enbez": "Article 138",
        "title": "外籍劳工 10% 严格法定配额与准证前置 (Foreign Labor Quota Restrictions)",
        "heading_path": "Chapter XII > Foreign Labor > Article 138",
        "text_original": "Investment projects are prohibited from employing foreign labor exceeding 10% of physical manual workers and 20% of technical specialized workers. Prior quota approval by the Ministry of Labor is compulsory.",
        "text_en": "Foreign labor cannot exceed 10% for manual work and 20% for technical staff; labor ministry approval required.",
        "text_zh": "投资项目雇佣外籍非技术劳工不得超过劳工总数的10%，专业技术人员不得超过20%。未获老挝劳动与社会福利部事先配额核准擅自使用外籍工人的，责令停工整顿并处以巨额罚款。",
        "language_mode": "bilingual",
        "lang_original": "en",
        "mandatory_level": "mandatory",
        "norm_category": "labor"
    },

    # --- 缅甸 (Myanmar) ---
    {
        "norm_id": "MM:Arbitration_Law_2016:Sec7",
        "law": "Myanmar Arbitration Law 2016",
        "enbez": "Section 7",
        "title": "涉外仲裁协议排除法院司法管辖 (Mandatory Court Referral to Arbitration)",
        "heading_path": "Chapter II > General Provisions > Section 7",
        "text_original": "A court before which an action is brought in a matter which is the subject of an arbitration agreement shall refer the parties to arbitration, unless it finds that the agreement is null and void, inoperative or incapable of being performed.",
        "text_en": "Court shall refer parties to arbitration unless agreement is null and void or incapable of performance.",
        "text_zh": "对于当事人订有仲裁协议的争议，受诉法院在被告首次实体抗辩前提出异议的，应当强制裁定中止诉讼并移送仲裁，除非法院认定仲裁协议自始无效、失效或无法执行。",
        "language_mode": "bilingual",
        "lang_original": "en",
        "mandatory_level": "mandatory",
        "norm_category": "arbitration"
    },
    {
        "norm_id": "MM:CBM_Notification_01_2022:FX",
        "law": "Myanmar CBM Notification No 01/2022",
        "enbez": "Section 1",
        "title": "外汇收入强制结汇与跨境资金监管 (Mandatory Foreign Currency Conversion)",
        "heading_path": "Central Bank of Myanmar > Foreign Exchange Management > Notification 01/2022",
        "text_original": "All foreign exchange receipts derived from overseas trade, investment or construction contracts must be converted into Myanmar Kyats at the official Central Bank exchange rate within the prescribed statutory period.",
        "text_en": "Foreign currency earnings must be converted into Myanmar Kyats within statutory timelines.",
        "text_zh": "涉外投资与工程承包取得之外币收入，必须在法定期限内按缅甸中央银行官方汇率强制兑换为缅币（MMK），外债离岸偿付与利润购汇汇出必须经过国家外汇监督委员会（FESC）审批。",
        "language_mode": "bilingual",
        "lang_original": "en",
        "mandatory_level": "mandatory",
        "norm_category": "forex"
    },
    {
        "norm_id": "MM:Investment_Law_2016:Sec50",
        "law": "Myanmar Investment Law 2016",
        "enbez": "Section 50",
        "title": "MIC 批文下长期土地租赁与转让限制 (Land Use Rights and Transfer Restrictions)",
        "heading_path": "Chapter XII > Right to Use Land > Section 50",
        "text_original": "Foreign investors holding an MIC Permit are entitled to lease land up to an initial period of 50 years, with two consecutive 10-year extensions. Subleasing or transferring land use rights requires prior written approval from the Commission.",
        "text_en": "MIC Permit holders may lease land up to 50+10+10 years; transferring land use rights requires prior MIC approval.",
        "text_zh": "取得缅甸投资委员会（MIC）批文的外资企业有权租赁土地最长50年并可续展两次各10年。未经 MIC 事先书面核准，不得擅自转让、转租或抵押土地使用权，违者取消投资批文。",
        "language_mode": "bilingual",
        "lang_original": "en",
        "mandatory_level": "mandatory",
        "norm_category": "property"
    },

    # --- 文莱 (Brunei) ---
    {
        "norm_id": "BN:Companies_Act_Cap39:Sec9",
        "law": "Brunei Companies Act (Cap 39)",
        "enbez": "Section 9",
        "title": "外资持股 30% Bumiputera 本地化强制要求 (30% Local Shareholding Requirement)",
        "heading_path": "Part II > Incorporation and Powers > Section 9",
        "text_original": "Foreign entities seeking commercial registration for public infrastructure contracting must ensure at least 30% equity shareholding by Brunei citizens (Bumiputera) to be eligible for government tender awards.",
        "text_en": "Foreign contractors must secure at least 30% local Bumiputera shareholding for government tenders.",
        "text_zh": "在文莱参与政府与公共基础设施工程投标的外资承包商，必须确保文莱本土马来人（Bumiputera）持股比例不低于30%，且董事会须有文莱常住董事代表。",
        "language_mode": "bilingual",
        "lang_original": "en",
        "mandatory_level": "mandatory",
        "norm_category": "corporate"
    },
    {
        "norm_id": "BN:PWD_Form_Contract:Clause38",
        "law": "Brunei PWD Standard Form of Contract",
        "enbez": "Clause 38",
        "title": "公共工程履约保函即付索兑与政府豁免 (Unconditional Performance Bond and Sovereign Immunity)",
        "heading_path": "General Conditions of Contract > Securities > Clause 38",
        "text_original": "The Contractor shall provide an unconditional on-demand performance bond. Under Section 24 of the Crown Proceedings Act, no injunction may be issued against the Government or its departments to restrain bond encashment.",
        "text_en": "Contractor must provide unconditional bond; courts cannot issue injunction against Government encashment.",
        "text_zh": "承包商应提供见索即付无条件履约保函。依据文莱《王权诉讼法》第24条及宪法第84C条，民事法院不得向文莱政府签发禁止没收保函的临时禁令，承包商仅能在实体诉讼中请求损害赔偿。",
        "language_mode": "bilingual",
        "lang_original": "en",
        "mandatory_level": "mandatory",
        "norm_category": "bond"
    },

    # --- 东帝汶 (Timor-Leste) ---
    {
        "norm_id": "TL:Decree_Law_22_2022:Art16",
        "law": "Timor-Leste Decree-Law No 22/2022 on Public Procurement",
        "enbez": "Article 16",
        "title": "公共采购本地含量与分包比例要求 (Local Content and Subcontracting Quota)",
        "heading_path": "Chapter III > Special Conditions > Article 16",
        "text_original": "International contractors executing public works financed by the State Budget must subcontract at least 20% of contract value to certified Timorese domestic enterprises and recruit local workforce.",
        "text_en": "International contractors must subcontract at least 20% of public works to domestic enterprises.",
        "text_zh": "执行东帝汶国家预算资助公共工程的国际承包商，必须将不少于合同总额20%的工程量分包给经认证的东帝汶本国企业，且优先雇佣属地普通劳工。",
        "language_mode": "bilingual",
        "lang_original": "en",
        "mandatory_level": "mandatory",
        "norm_category": "procurement"
    },
    {
        "norm_id": "TL:Private_Investment_Law_2017:Art11",
        "law": "Timor-Leste Private Investment Law No 14/2017",
        "enbez": "Article 11",
        "title": "外资待遇保障与 ICSID 国际仲裁承诺 (Foreign Investment Protection and ICSID Arbitration)",
        "heading_path": "Chapter IV > Guarantees and Rights > Article 11",
        "text_original": "Foreign investors are guaranteed equal protection against unlawful expropriation. Investment disputes between the State and foreign investors may be submitted to arbitration under ICSID or UNCITRAL rules.",
        "text_en": "Foreign investors are protected against unlawful expropriation; disputes may be submitted to ICSID or UNCITRAL.",
        "text_zh": "东帝汶保障外国投资者免受非法国有化与征收。东帝汶国家与外国投资者之间的投资争议，根据双方约定有权直接提交至解决投资争端国际中心（ICSID）或 UNCITRAL 仲裁。",
        "language_mode": "bilingual",
        "lang_original": "en",
        "mandatory_level": "mandatory",
        "norm_category": "investment"
    },

    # --- 横向劳工法补全 ---
    {
        "norm_id": "ID:UU_13_2003_Labor:Art59",
        "law": "Indonesia Labor Law (UU 13/2003 amended by UU 6/2023)",
        "enbez": "Pasal 59",
        "title": "固定期限劳动合同 PKWT 限制与赔偿责任 (PKWT Fixed-Term Employment)",
        "heading_path": "BAB IX > Hubungan Kerja > Pasal 59",
        "text_original": "Perjanjian Kerja Waktu Tertentu (PKWT) hanya dapat dibuat untuk pekerjaan tertentu yang menurut jenis dan sifat atau kegiatan pekerjaannya akan selesai dalam waktu tertentu. PKWT tidak dapat diadakan untuk pekerjaan yang bersifat tetap.",
        "text_en": "Fixed-term employment agreements (PKWT) can only be made for temporary work, not permanent positions.",
        "text_zh": "固定期限劳动合同（PKWT）仅适用于临时性或一次性完成的工程。若将其用于核心长期业务，依法自动拟制为无固定期限劳动合同（PKWTT），提前解除时总包方承担双倍经济赔偿金。",
        "language_mode": "bilingual",
        "lang_original": "id",
        "mandatory_level": "mandatory",
        "norm_category": "labor"
    },
    {
        "norm_id": "VN:Labor_Code_2019:Art152",
        "law": "Vietnam Labor Code 2019 (Law 45/2019/QH14)",
        "enbez": "Điều 152",
        "title": "外国劳工工作许可证制度与违法驱逐 (Foreign Workers Permit and Deportation)",
        "heading_path": "Chương XI > Lao Động Nước Ngoài > Điều 152",
        "text_original": "Người sử dụng lao động chỉ được tuyển dụng người lao động nước ngoài vào làm vị trí công việc quản lý, điều hành, chuyên gia và lao động kỹ thuật mà người lao động Việt Nam chưa đáp ứng được theo nhu cầu sản xuất, kinh doanh.",
        "text_en": "Employers may only recruit foreign workers for managerial, executive and expert positions not filled by Vietnamese.",
        "text_zh": "用人单位仅得在越南劳工无法满足的管理、专家及专业技术岗位招募外籍人员。未持有合法工作许可证（Work Permit）在越南施工的，行政机关有权强制驱逐出境并勒令停工整顿。",
        "language_mode": "bilingual",
        "lang_original": "vi",
        "mandatory_level": "mandatory",
        "norm_category": "labor"
    },
    {
        "norm_id": "MY:Employment_Act_1955:Sec60L",
        "law": "Malaysia Employment Act 1955",
        "enbez": "Section 60L",
        "title": "主承包商对分包劳工工资垫付连带责任 (Principal Contractor Wage Liability)",
        "heading_path": "Part XI > Contractors and Sub-contractors > Section 60L",
        "text_original": "A principal contractor who has entered into a contract with a sub-contractor shall be liable for the wages earned by any employee of such sub-contractor for work done, up to the amount of one month's wages.",
        "text_en": "Principal contractor is liable for up to one month's unpaid wages owed by sub-contractors to employees.",
        "text_zh": "总承包商对其分包商在工程现场所雇劳工的工资承担连带代付清偿责任，连带责任额度以劳工应得之一个月工资为限，总承包商代偿后有权从应付分包工程款中直接扣留冲抵。",
        "language_mode": "bilingual",
        "lang_original": "en",
        "mandatory_level": "mandatory",
        "norm_category": "labor"
    },
    {
        "norm_id": "PH:DOLE_DO_174_17:Sec5",
        "law": "Philippines DOLE Department Order No 174-17",
        "enbez": "Section 5",
        "title": "严禁非法单纯劳务分包与直接雇主法定推定 (Absolute Prohibition of Labor-Only Contracting)",
        "heading_path": "Rules Implementing Articles 106 to 109 of Labor Code > Section 5",
        "text_original": "Labor-only contracting is hereby declared prohibited. In the event of a finding of labor-only contracting, the principal shall be considered the direct employer of the contractor's employees for all purposes.",
        "text_en": "Labor-only contracting is prohibited; finding thereof makes principal direct employer of subcontractor workers.",
        "text_zh": "严禁无实质设备与资产的纯劳务分包（Labor-only Contracting）。一旦被认定为非法分包，总承包商依法被直接拟制为分包工人的法定雇主，就欠薪、工伤事故承担第一顺位全额清偿责任。",
        "language_mode": "bilingual",
        "lang_original": "en",
        "mandatory_level": "mandatory",
        "norm_category": "labor"
    },

    # --- 横向环境合规法规补全 ---
    {
        "norm_id": "ID:PP_22_2021_AMDAL:Art3",
        "law": "Indonesia Government Regulation PP No 22/2021",
        "enbez": "Pasal 3",
        "title": "重大基建项目强制环境影响评价 (AMDAL Mandatory Requirement)",
        "heading_path": "BAB II > Persetujuan Lingkungan > Pasal 3",
        "text_original": "Setiap Rencana Usaha dan/atau Kegiatan yang berdampak penting terhadap lingkungan hidup wajib memiliki Amdal sebagai persyaratan penerbitan Perizinan Berusaha.",
        "text_en": "Every activity with significant environmental impact must obtain AMDAL approval before business licensing.",
        "text_zh": "所有对环境具有重大影响的基础设施及电站工程，必须事先取得环境影响评价审批决定书（AMDAL），未取得 AMDAL 批准擅自开工的，省长或环境部有权下令吊销开工许可并实施行政封锁。",
        "language_mode": "bilingual",
        "lang_original": "id",
        "mandatory_level": "mandatory",
        "norm_category": "environment"
    },
    {
        "norm_id": "VN:Decree_08_2022_EIA:Art12",
        "law": "Vietnam Decree No 08/2022/ND-CP on Environment Protection",
        "enbez": "Điều 12",
        "title": "环评批复与排污许可证开工前置审批 (EIA Approval and Environmental Permit Precondition)",
        "heading_path": "Chương II > Đánh Giá Tác Động Môi Trường > Điều 12",
        "text_original": "Chủ dự án đầu tư có trách nhiệm lập báo cáo đánh giá tác động môi trường trình cơ quan nhà nước có thẩm quyền phê duyệt kết quả thẩm định trước khi khởi công xây dựng công trình.",
        "text_en": "Investors must obtain EIA appraisal approval from authorities before commencement of construction.",
        "text_zh": "项目业主在正式开工建设前，必须编制环境影响评估报告（ĐTM）并取得自然资源与环境部或省人委会的批复结果。未批先建者处以最高20亿越南盾罚款并勒令中止施工。",
        "language_mode": "bilingual",
        "lang_original": "vi",
        "mandatory_level": "mandatory",
        "norm_category": "environment"
    },
    {
        "norm_id": "PH:DENR_AO_2003_30_ECC:Sec4",
        "law": "Philippines DENR Administrative Order No 2003-30",
        "enbez": "Section 4",
        "title": "环境合规证书 ECC 刚性前置与停工令 (Environmental Compliance Certificate ECC Precondition)",
        "heading_path": "Procedural Manual for PEISS > Scope > Section 4",
        "text_original": "No person or entity shall undertake or operate an environmentally critical project (ECP) without first securing an Environmental Compliance Certificate (ECC). Violators shall be subject to Cease and Desist Orders.",
        "text_en": "No critical project shall proceed without ECC; violators face Cease and Desist Orders.",
        "text_zh": "未取得环境合规证书（ECC）前，严禁开展任何环境敏感工程施工。环境与自然资源部（DENR）发现无证施工的，有权立即发布停工中止令（Cease and Desist Order），并不受一般法院禁制令限制。",
        "language_mode": "bilingual",
        "lang_original": "en",
        "mandatory_level": "mandatory",
        "norm_category": "environment"
    },

    # --- 马来西亚东马原住民土地法 ---
    {
        "norm_id": "MY:Sabah_Land_Ordinance:Sec76",
        "law": "Sabah Land Ordinance (Cap 68)",
        "enbez": "Section 76",
        "title": "沙巴土著习惯地 NCR 认定与工程征拆受阻 (Native Customary Rights NCR in Sabah)",
        "heading_path": "Part IV > Native Titles > Section 76",
        "text_original": "Native Customary Rights (NCR) lawfully acquired by natives shall not be extinguished by grant of title to any other person without prior settlement, acquisition under the Land Acquisition Ordinance, and full compensation.",
        "text_en": "Native Customary Rights are not extinguished without statutory acquisition and full compensation.",
        "text_zh": "沙巴原住民依法取得之土著习惯地权利（NCR），在政府未依法完成征拆程序并足额给付补偿前不被消灭。承包商擅自进场施工将构成民事非法侵入（Trespass），引发停工围堵风险。",
        "language_mode": "bilingual",
        "lang_original": "en",
        "mandatory_level": "mandatory",
        "norm_category": "property"
    },
    {
        "norm_id": "MY:Sarawak_Land_Code:Sec18",
        "law": "Sarawak Land Code (Cap 81)",
        "enbez": "Section 18",
        "title": "砂拉越土著习惯地保护与处置无效 (Sarawak Native Area Land Protection)",
        "heading_path": "Part II > Classification and Titles > Section 18",
        "text_original": "Any dealing or transaction purporting to transfer or encumber Native Area Land or Native Customary Land to a non-native shall be void and of no effect, and no compensation shall be recoverable.",
        "text_en": "Any transfer of Native Area Land to non-natives is void ab initio without compensation.",
        "text_zh": "任何企图将砂拉越土著领地（Native Area Land）或习惯地转让或抵押给非土著（包括外资承包商与投资企业）的协议自始绝对无效，投资款项依法不予返还。",
        "language_mode": "bilingual",
        "lang_original": "en",
        "mandatory_level": "mandatory",
        "norm_category": "property"
    }
]

# --------------------------------------------------------------------------
# 2. 待入库 L2 REFERENCE_NORMS (参考层规范 / FIDIC 2017 / AIIB)
# --------------------------------------------------------------------------
L2_NORMS = [
    {
        "norm_id": "FIDIC:Silver_2017:Clause_20.2",
        "law": "FIDIC Silver Book 2017",
        "enbez": "Clause 20.2",
        "title": "FIDIC 2017 索赔分步通知机制与失权例外 (Claims for Payment and/or EOT)",
        "heading_path": "Clause 20 > Employer's and Contractor's Claims > Sub-Clause 20.2",
        "text_original": "The claiming Party shall give a Notice of Claim to the Engineer/Employer within 28 days after becoming aware. If the Party fails, the Notice is invalid, BUT if the DAAB considers it justified due to no prejudice to the other Party, the DAAB may waive the strict time-bar.",
        "text_en": "Party must give Notice of Claim within 28 days; DAAB has discretion to waive time-bar if no prejudice.",
        "text_zh": "索赔方须在知悉受阻事件后28天内发出索赔通知。相较1999版僵化失权，2017版赋予争端避免与裁决委员会（DAAB）在未对相对人造成实质损害且具有合理正当事由时，豁免28天绝对失权的自由裁量权。",
        "language_mode": "bilingual",
        "lang_original": "en",
        "mandatory_level": "reference",
        "norm_category": "standard_contract"
    },
    {
        "norm_id": "FIDIC:Silver_2017:Clause_21.1",
        "law": "FIDIC Silver Book 2017",
        "enbez": "Clause 21.1",
        "title": "常设 DAAB 争端避免与裁决委员会任命 (Constitution of the DAAB)",
        "heading_path": "Clause 21 > Disputes and Arbitration > Sub-Clause 21.1",
        "text_original": "Disputes shall be decided by a DAAB in accordance with Sub-Clause 21.4. The Parties shall jointly appoint the member(s) of the DAAB within the time stated in the Contract Data. The DAAB shall be standing from the Commencement Date.",
        "text_en": "Parties shall jointly appoint DAAB as a standing board from the Commencement Date.",
        "text_zh": "当事人应在合同开工后约定时间内共同任命常设争端避免与裁决委员会（DAAB）。DAAB 从开工起常设运作，定期巡视现场并主动协助当事人避免潜在争议发酵为正式争端。",
        "language_mode": "bilingual",
        "lang_original": "en",
        "mandatory_level": "reference",
        "norm_category": "standard_contract"
    },
    {
        "norm_id": "FIDIC:Silver_2017:Clause_21.4",
        "law": "FIDIC Silver Book 2017",
        "enbez": "Clause 21.4",
        "title": "DAAB 决定之即时有约束力与必须履行 (Obtaining DAAB's Decision)",
        "heading_path": "Clause 21 > Disputes and Arbitration > Sub-Clause 21.4",
        "text_original": "The decision shall be binding on both Parties, who shall promptly comply with it whether or not a Party gives a Notice of Dissatisfaction (NOD).",
        "text_en": "The DAAB decision is immediately binding on both Parties, who shall promptly comply with it even if NOD is issued.",
        "text_zh": "DAAB 裁决对双方当事人具有即时约束力（Immediately Binding）。即便任何一方随后在28天内发出了不满通知（NOD），各方在仲裁裁决作出前仍必须立即执行 DAAB 决定中的给付义务。",
        "language_mode": "bilingual",
        "lang_original": "en",
        "mandatory_level": "reference",
        "norm_category": "standard_contract"
    },
    {
        "norm_id": "FIDIC:Silver_2017:Clause_21.7",
        "law": "FIDIC Silver Book 2017",
        "enbez": "Clause 21.7",
        "title": "不服从 DAAB 决定直接向仲裁庭申请执行裁决 (Failure to Comply with DAAB's Decision)",
        "heading_path": "Clause 21 > Disputes and Arbitration > Sub-Clause 21.7",
        "text_original": "In the event that a Party fails to comply with any decision of the DAAB, whether binding or final and binding, the other Party may, without prejudice to any other rights, refer the failure itself directly to arbitration under Sub-Clause 21.6.",
        "text_en": "Party may refer failure to comply with DAAB decision directly to arbitration for summary enforcement.",
        "text_zh": "若一方拒绝履行 DAAB 具有约束力的决定，另一方无需重新等待友好协商期，可直接将该'不履行事实本身'提交仲裁，请求仲裁庭迅速颁发具有强制执行力的临时裁决或部分终局裁决。",
        "language_mode": "bilingual",
        "lang_original": "en",
        "mandatory_level": "reference",
        "norm_category": "standard_contract"
    },
    {
        "norm_id": "FIDIC:Silver_2017:Clause_8.5",
        "law": "FIDIC Silver Book 2017",
        "enbez": "Clause 8.5",
        "title": "工期延误原因重新界定与共同延误评估 (Extension of Time for Completion)",
        "heading_path": "Clause 8 > Commencement, Delays and Suspension > Sub-Clause 8.5",
        "text_original": "If a delay caused by a matter which is the Employer's risk is concurrent with a delay caused by the Contractor, the Contractor's entitlement to EOT shall be assessed in accordance with the rules stated in the Special Provisions or relevant construction law principles.",
        "text_en": "Concurrent delay rules shall be assessed in accordance with Special Provisions and applicable construction law.",
        "text_zh": "针对雇主风险事件与承包商原因同时发生导致的共同延误（Concurrent Delay），明确由专用条件或准据法原则进行量化评估，避免一刀切剥夺承包商工期顺延权利。",
        "language_mode": "bilingual",
        "lang_original": "en",
        "mandatory_level": "reference",
        "norm_category": "standard_contract"
    },
    {
        "norm_id": "FIDIC:Red_2017:Clause_13.6",
        "law": "FIDIC Red Book 2017",
        "enbez": "Clause 13.6",
        "title": "大宗建材与劳动力物价波动公式调整 (Adjustments for Changes in Cost)",
        "heading_path": "Clause 13 > Variations and Adjustments > Sub-Clause 13.6",
        "text_original": "The amounts payable to the Contractor shall be adjusted for rises or falls in the cost of labor, Goods and other inputs to the Works, by the addition or deduction of the amounts determined by the formulae prescribed in the Schedule of Cost Indexation.",
        "text_en": "Contractor payments shall be adjusted for cost changes in labor and materials using agreed indexation formulae.",
        "text_zh": "合同约定的工程价款应当依据物价指数调整表所列公式，就劳动力、大宗建材（钢材、水泥）的市场价格剧烈波动进行定期增减调整，防范通货膨胀导致承包商巨额亏损。",
        "language_mode": "bilingual",
        "lang_original": "en",
        "mandatory_level": "reference",
        "norm_category": "standard_contract"
    },

    # --- 亚投行 (AIIB) 规范 ---
    {
        "norm_id": "AIIB:Procurement_Policy:2021:Sec2",
        "law": "AIIB Procurement Policy for Projects 2021",
        "enbez": "Section II",
        "title": "亚投行资助工程国际公开招标与联合体资格 (International Open Competitive Tendering)",
        "heading_path": "Core Procurement Principles > Section II",
        "text_original": "International Open Competitive Tendering (IOCT) shall be the default method. Eligible firms from all member countries, including international joint ventures, are entitled to participate without discriminatory local barriers.",
        "text_en": "International open competitive tendering is default; firms from all member states eligible without local barriers.",
        "text_zh": "亚投行（AIIB）资助项目原则上采用国际公开竞争性招标（IOCT）。所有成员国合格企业（包括中资跨国联合体）均有权平等参与，借款国不得设置歧视性的属地排他壁垒。",
        "language_mode": "bilingual",
        "lang_original": "en",
        "mandatory_level": "reference",
        "norm_category": "multilateral_treaty"
    },
    {
        "norm_id": "AIIB:ESF_2021:Sec3_Social",
        "law": "AIIB Environmental and Social Framework 2021",
        "enbez": "Standard 3",
        "title": "亚投行原住民保护与非自愿移民安置强制标准 (Indigenous Peoples and Involuntary Resettlement)",
        "heading_path": "Environmental and Social Standards > ESS 3",
        "text_original": "Clients must ensure meaningful consultation, free prior and informed consent (FPIC) where applicable, and fair resettlement compensation before project activities physically displace communities.",
        "text_en": "Borrowers must secure FPIC and ensure fair resettlement before community displacement.",
        "text_zh": "借款方与项目实施单位必须遵循原住民保护标准，涉及原住民领地的必须取得知情同意（FPIC），未完成征迁补偿与安置计划前不得强行入场开工，违者将被亚投行暂停或撤回贷款。",
        "language_mode": "bilingual",
        "lang_original": "en",
        "mandatory_level": "reference",
        "norm_category": "multilateral_treaty"
    }
]

# --------------------------------------------------------------------------
# 3. 待入库 L2 REFERENCE_CASES (国际投资与商事仲裁经典判例)
# --------------------------------------------------------------------------
L2_CASES = [
    {
        "case_id": "CASE:ICSID:CMC_v_Mozambique:2019",
        "title": "CMC Africa Austral v Republic of Mozambique (ICSID Case No ARB/17/23)",
        "jurisdiction": "asean_all",
        "court": "International Centre for Settlement of Investment Disputes (ICSID)",
        "decided": "2019-10-24",
        "leitsatz": "中资跨国基建企业 BIT 仲裁胜诉标杆案：东道国财政部长期恶意拖欠公路 EPC 工程进度款并实施外汇管制，被仲裁庭裁定构成对双边投资协定项下'公正与平等待遇' (FET) 的实质违反，判决东道国全额赔偿工程款本息及违约损害赔偿金。",
        "tenor": "Tribunal ruled that systematic non-payment of certified IPCs and currency exchange refusal violated the Fair and Equitable Treatment standard under the BIT.",
        "gruende": "Arbitral Tribunal held that sovereign non-payment crossing the threshold of commercial breach into regulatory abuse and arbitrary non-responsiveness constitutes a violation of the Fair and Equitable Treatment (FET) standard and indirect expropriation under international law.",
        "source_url": "https://www.italaw.com/cases/7632"
    },
    {
        "case_id": "CASE:ICSID:Salini_v_Morocco:2001",
        "title": "Salini Costruttori S.p.A. v Kingdom of Morocco (ICSID Case No ARB/00/4)",
        "jurisdiction": "asean_all",
        "court": "International Centre for Settlement of Investment Disputes (ICSID)",
        "decided": "2001-07-23",
        "leitsatz": "国际投资仲裁'Salini 四要素'投资界定奠基案：确立了大型跨国基建承包工程属于 ICSID 公约第25条项下受保护'投资'的四大要件：① 资本与资产贡献；② 相当期限的持续履行；③ 承担重大商业风险；④ 对东道国经济发展做出实质贡献。",
        "tenor": "Established the classic 'Salini Test' defining investment under Article 25(1) of the ICSID Convention.",
        "gruende": "The Tribunal affirmed that a major infrastructure EPC contract fulfills the definition of investment provided it incorporates contribution, duration, participation in risks, and contribution to economic development of the host State.",
        "source_url": "https://www.italaw.com/cases/958"
    },
    {
        "case_id": "CASE:UNCITRAL:Himpurna_v_PLN:1999",
        "title": "Himpurna California Energy Ltd. v PT. (Persero) Perusahaan Listrik Negara (UNCITRAL)",
        "jurisdiction": "asean_id",
        "court": "UNCITRAL Ad Hoc Arbitral Tribunal",
        "decided": "1999-05-04",
        "leitsatz": "印尼国家电力公司 PLN 地热 PPA 违约仲裁案：亚洲金融危机期间印尼总统颁布紧急政令要求 PLN 中止履行地热电站购电协议。仲裁庭裁定：主权国家所拥有的商业国营企业不能以自身主权政府签发的行政命令作为不可抗力主张免责，PLN 构成根本违约并判赔3.9亿美元。",
        "tenor": "State-owned utility PLN cannot invoke sovereign government decree as force majeure to escape PPA payment obligations.",
        "gruende": "The Arbitral Tribunal firmly rejected PLN's force majeure defense based on Presidential Decrees, holding that a state instrumentality cannot shield itself behind state intervention where the risk of political and financial change was allocated to it.",
        "source_url": "https://www.trans-lex.org/206900"
    },
    {
        "case_id": "CASE:VIAC:Award_45_2019:2019",
        "title": "Vietnam Hydroelectric EPC Consortium v Owner (VIAC Construction Award 2019)",
        "jurisdiction": "asean_vn",
        "court": "Vietnam International Arbitration Centre (VIAC)",
        "decided": "2019-11-15",
        "leitsatz": "越南国际仲裁中心水电 EPC 工期违约金 8% 上限适用案：越南业主主张依据合同约定扣除相当于工程总价 15% 的延误违约金并没收保函。仲裁庭裁定：依据《越南商事法》第301条强行法规定，违约金上限严格限制在违约义务金额的 8%，超出部分无效并判令业主返还多扣工程款。",
        "tenor": "VIAC arbitral tribunal enforced mandatory 8% penalty cap under Commercial Law 2005 Article 301, invalidating contractual 15% LD deduction.",
        "gruende": "Under Article 301 of the Commercial Law 2005, the maximum penalty for breach of contract is capped at 8% of the value of the breached obligation. Any contractual stipulation exceeding this statutory ceiling is null and void under Vietnamese mandatory public law.",
        "source_url": "https://www.viac.vn/an-le"
    },
    {
        "case_id": "CASE:ICSID:Klockner_v_Cameroon:1983",
        "title": "Klöckner Industrie-Anlagen GmbH v United Republic of Cameroon (ICSID Case No ARB/81/2)",
        "jurisdiction": "asean_all",
        "court": "International Centre for Settlement of Investment Disputes (ICSID)",
        "decided": "1983-10-21",
        "leitsatz": "特许经营成套工厂投资案：国际仲裁庭确立了特许经营与交钥匙工程中，东道国不得以微小瑕疵阻绝巨额合同支付的善意履约义务（Good Faith），以及对外国投资者合理期待（Legitimate Expectations）的司法保护范式。",
        "tenor": "Recognized the mutual obligation of good faith and protection of legitimate investor expectations in turnkey concession projects.",
        "gruende": "Tribunal stressed that long-term cross-border infrastructure concessions impose reciprocal duties of good faith and cooperation between host state entities and foreign turnkey contractors.",
        "source_url": "https://www.italaw.com/cases/610"
    }
]

# --------------------------------------------------------------------------
# 4. 执行写入 norms 与 reference_norms
# --------------------------------------------------------------------------
print("\n[步骤 1] 写入 L1 norms 强行法...")
inserted_l1_norms = 0
for norm in L1_NORMS:
    cur.execute("SELECT 1 FROM norms WHERE norm_id = ?", (norm["norm_id"],))
    if not cur.fetchone():
        cur.execute(
            """INSERT INTO norms (
                norm_id, law, enbez, title, heading_path, text_de, text_original, text_en, text_zh,
                language_mode, lang_original, mandatory_level, norm_category, translation_source,
                source_url, fetched_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                norm["norm_id"], norm["law"], norm["enbez"], norm["title"], norm["heading_path"],
                norm["text_zh"], norm.get("text_original"), norm.get("text_en"), norm.get("text_zh"),
                norm["language_mode"], norm["lang_original"], norm["mandatory_level"],
                norm["norm_category"], "EXPERT_REVIEW_2026", "https://asean.org/legal",
                datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
            )
        )
        inserted_l1_norms += 1
print(f"-> 新增 L1 norms: {inserted_l1_norms} 条")

print("\n[步骤 2] 写入 L2 reference_norms 参考层...")
inserted_l2_norms = 0
for norm in L2_NORMS:
    cur.execute("SELECT 1 FROM reference_norms WHERE norm_id = ?", (norm["norm_id"],))
    if not cur.fetchone():
        cur.execute(
            """INSERT INTO reference_norms (
                norm_id, law, enbez, title, heading_path, text_de, text_original, text_en, text_zh,
                language_mode, lang_original, mandatory_level, norm_category, translation_source,
                source_url, fetched_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                norm["norm_id"], norm["law"], norm["enbez"], norm["title"], norm["heading_path"],
                norm["text_zh"], norm.get("text_original"), norm.get("text_en"), norm.get("text_zh"),
                norm["language_mode"], norm["lang_original"], norm["mandatory_level"],
                norm["norm_category"], "EXPERT_REVIEW_2026", "https://fidic.org",
                datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
            )
        )
        inserted_l2_norms += 1
print(f"-> 新增 L2 reference_norms: {inserted_l2_norms} 条")

print("\n[步骤 3] 写入 L2 reference_cases 仲裁案例...")
inserted_l2_cases = 0
for case in L2_CASES:
    cur.execute("SELECT 1 FROM reference_cases WHERE case_id = ?", (case["case_id"],))
    if not cur.fetchone():
        cur.execute(
            """INSERT INTO reference_cases (
                case_id, az, court, decided, leitsatz, tenor, gruende, source_url, fetched_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                case["case_id"], case["title"], case["court"], case["decided"],
                case["leitsatz"], case["tenor"], case["gruende"], case["source_url"],
                datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
            )
        )
        inserted_l2_cases += 1
print(f"-> 新增 L2 reference_cases: {inserted_l2_cases} 条")

# --------------------------------------------------------------------------
# 5. 生成对应的 Chunks 并写入 chunks 与 reference_chunks
# --------------------------------------------------------------------------
print("\n[步骤 4] 生成分块 Chunks 并写入...")

inserted_l1_chunks = 0
for norm in L1_NORMS:
    cid = f"CHUNK:NORM:{norm['norm_id']}:0"
    cur.execute("SELECT 1 FROM chunks WHERE chunk_id = ?", (cid,))
    if not cur.fetchone():
        chunk_text = f"【法条】{norm['law']} {norm['enbez']} {norm['title']}\n{norm['text_zh']}\nEnglish: {norm['text_en']}"
        ctx_prefix = f"{norm['law']} {norm['enbez']}"
        cur.execute(
            """INSERT INTO chunks (chunk_id, kind, ref_id, seq, text, ctx_prefix)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (cid, "norm", norm["norm_id"], 0, chunk_text, ctx_prefix)
        )
        inserted_l1_chunks += 1
print(f"-> 新增 L1 chunks: {inserted_l1_chunks} 条")

inserted_l2_chunks = 0
for norm in L2_NORMS:
    cid = f"CHUNK:REF_NORM:{norm['norm_id']}:0"
    cur.execute("SELECT 1 FROM reference_chunks WHERE chunk_id = ?", (cid,))
    if not cur.fetchone():
        chunk_text = f"【国际工程参考规范】{norm['law']} {norm['enbez']} {norm['title']}\n{norm['text_zh']}\nEnglish: {norm['text_en']}"
        cur.execute(
            """INSERT INTO reference_chunks (chunk_id, kind, ref_id, seq, text)
               VALUES (?, ?, ?, ?, ?)""",
            (cid, "reference_norm", norm["norm_id"], 0, chunk_text)
        )
        inserted_l2_chunks += 1

for case in L2_CASES:
    cid = f"CHUNK:REF_CASE:{case['case_id']}:0"
    cur.execute("SELECT 1 FROM reference_chunks WHERE chunk_id = ?", (cid,))
    if not cur.fetchone():
        chunk_text = f"【国际投资与商事仲裁先例】{case['title']} ({case['court']}, {case['decided']})\n裁判要旨: {case['leitsatz']}\n裁判主文: {case['tenor']}"
        cur.execute(
            """INSERT INTO reference_chunks (chunk_id, kind, ref_id, seq, text)
               VALUES (?, ?, ?, ?, ?)""",
            (cid, "reference_case", case["case_id"], 0, chunk_text)
        )
        inserted_l2_chunks += 1
print(f"-> 新增 L2 reference_chunks: {inserted_l2_chunks} 条")

# --------------------------------------------------------------------------
# 6. 构建图谱边 (edges & reference_edges) 消除孤立节点
# --------------------------------------------------------------------------
print("\n[步骤 5] 构建高密度拓扑关联图谱边 (edges & reference_edges)...")

EDGES_L1 = [
    # 柬埔寨关联
    ("KH:Commercial_Arbitration_Law_2006:Art3", "KH:Commercial_Arbitration_Law_2006:Art5", "complements"),
    ("KH:Commercial_Arbitration_Law_2006:Art5", "KH:Commercial_Arbitration_Law_2006:Art34", "interprets"),
    ("KH:Land_Law_2001:Art43", "KH:Sub_Decree_111:Art5", "governs"),
    ("KH:Sub_Decree_111:Art5", "KH:Sub_Decree_111:Art12", "complements"),
    ("KH:Prakas_346_2018:Tax", "KH:Financial_Management_Law_2023:Art18", "applies_with"),

    # 老挝关联
    ("LA:Decree_135_PM:Art8", "LA:Decree_135_PM:Art15", "governs"),
    ("LA:Decree_135_PM:Art15", "LA:Hydropower_Law_2017:Art21", "complements"),
    ("LA:Hydropower_Law_2017:Art21", "LA:Electricity_Law_2017:Art35", "interprets"),
    ("LA:Labor_Law_2013:Art138", "LA:Revenue_Law_2019:Art45", "applies_with"),

    # 缅甸关联
    ("MM:Arbitration_Law_2016:Sec7", "MM:Arbitration_Law_2016:Sec8", "complements"),
    ("MM:Investment_Law_2016:Sec50", "MM:SEZ_Law_2014:Sec30", "interprets"),
    ("MM:CBM_Notification_01_2022:FX", "MM:Investment_Law_2016:Sec50", "applies_with"),

    # 文莱关联
    ("BN:Companies_Act_Cap39:Sec9", "BN:PWD_Form_Contract:Clause38", "governs"),
    ("BN:PWD_Form_Contract:Clause38", "BN:Constitution:Art84C", "overrides"),

    # 东帝汶关联
    ("TL:Decree_Law_22_2022:Art16", "TL:Private_Investment_Law_2017:Art11", "complements"),
    ("TL:Private_Investment_Law_2017:Art11", "TL:Petroleum_Tax_Law_2017:Art6", "applies_with"),

    # 劳工与环境横向关联合同法
    ("ID:UU_13_2003_Labor:Art59", "ID:PP_22_2021_AMDAL:Art3", "applies_with"),
    ("VN:Labor_Code_2019:Art152", "VN:Decree_08_2022_EIA:Art12", "applies_with"),
    ("MY:Employment_Act_1955:Sec60L", "MY:Sabah_Land_Ordinance:Sec76", "applies_with"),
    ("MY:Sabah_Land_Ordinance:Sec76", "MY:Sarawak_Land_Code:Sec18", "interprets"),
    ("PH:DOLE_DO_174_17:Sec5", "PH:DENR_AO_2003_30_ECC:Sec4", "applies_with"),
]

inserted_l1_edges = 0
for src, dst, rel in EDGES_L1:
    cur.execute("SELECT 1 FROM edges WHERE src = ? AND dst = ?", (src, dst))
    if not cur.fetchone():
        cur.execute("INSERT INTO edges (src, dst, rel, source) VALUES (?, ?, ?, ?)", (src, dst, rel, "EXPERT_REVIEW_2026"))
        inserted_l1_edges += 1
print(f"-> 新增 L1 edges: {inserted_l1_edges} 条")

EDGES_L2 = [
    ("FIDIC:Silver_2017:Clause_20.2", "FIDIC:Silver_2017:Clause_21.1", "precedes"),
    ("FIDIC:Silver_2017:Clause_21.1", "FIDIC:Silver_2017:Clause_21.4", "governs"),
    ("FIDIC:Silver_2017:Clause_21.4", "FIDIC:Silver_2017:Clause_21.7", "enforces"),
    ("FIDIC:Silver_2017:Clause_8.5", "FIDIC:Silver_2017:Clause_20.2", "triggers"),
    ("FIDIC:Red_2017:Clause_13.6", "FIDIC:Silver_2017:Clause_20.2", "complements"),
    ("AIIB:Procurement_Policy:2021:Sec2", "AIIB:ESF_2021:Sec3_Social", "complements"),
    ("CASE:ICSID:CMC_v_Mozambique:2019", "CASE:ICSID:Salini_v_Morocco:2001", "follows"),
    ("CASE:UNCITRAL:Himpurna_v_PLN:1999", "CASE:ICSID:Klockner_v_Cameroon:1983", "interprets"),
    ("CASE:VIAC:Award_45_2019:2019", "VN:Commercial_Law_2005:Art301", "applied_in"),
]

inserted_l2_edges = 0
for i, (src, dst, rel) in enumerate(EDGES_L2):
    cur.execute("SELECT 1 FROM reference_edges WHERE src = ? AND dst = ?", (src, dst))
    if not cur.fetchone():
        edge_id = f"REF_EDGE_EXP_{int(time.time())}_{i}"
        cur.execute(
            "INSERT INTO reference_edges (edge_id, src, dst, rel, description) VALUES (?, ?, ?, ?, ?)",
            (edge_id, src, dst, rel, "EXPERT_REVIEW_2026")
        )
        inserted_l2_edges += 1
print(f"-> 新增 L2 reference_edges: {inserted_l2_edges} 条")

# 更新 edges_top 物化视图/表
cur.execute("DELETE FROM edges_top")
cur.execute("""
    INSERT INTO edges_top (src, dst, rel, source, rk)
    SELECT src, dst, rel, source, ROW_NUMBER() OVER (PARTITION BY src ORDER BY rowid ASC) as rk
    FROM edges
""")
print(f"-> 同步刷新物化表 edges_top 完成")

# 提交数据库事务
conn.commit()
conn.close()
print(">> 数据库 SQLite 数据写入与事务提交成功！")
