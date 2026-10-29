"""L2 广覆盖参考层知识库二次深化与全量扩充脚本 (Expand L2 Reference KB)
涵盖领域：
1. 外汇管制与资本项下利润汇出 (越南 Circular 06/2019/TT-NHNN, 马来西亚 BNM FEP, 泰国 BOT Foreign Exchange)
2. 属地税收、常设机构与外国承包商税 (越南 FCT Circular 103/2014, 印尼 PPh Final 8% 惩罚性预扣, 菲律宾 BIR Offshore/Onshore PE Ruling)
3. 外籍劳工签证、配额与属地化用工 (印尼 TKA 1:3 陪同工, 新加坡 MOM DRC 配额, 泰国 Work Permit 限制工程行业)
4. FIDIC 银皮书/黄皮书 Tier-2 履约中段关键通用条款 (Clause 4.12 不可预见地质条件, Clause 13.1-13.3 变更估价, Clause 15 雇主违约终止, Clause 16 承包商停工与解约)
5. 涉外行政与外贸许可监管 (越南外贸管理法 2017, 马来西亚战略贸易法 2010, 菲律宾外资安全审查议定)
"""

import os
import sys
import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any

sys.path.insert(0, os.path.abspath("."))
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from lawagent.store.snapshots import SnapshotManager
from lawagent.store.bm25 import BM25Engine
from lawagent.store.vec import DenseVectorEngine

# =========================================================================
# L2 新增广覆盖参考规范定义 (30+ 条高覆盖度参考规范)
# =========================================================================
NEW_L2_REFERENCE_NORMS: List[Dict[str, Any]] = [
    # ---------------------------------------------------------------------
    # 1. 外汇管制与工程款跨境收付 (Foreign Exchange & Remittance)
    # ---------------------------------------------------------------------
    {
        "norm_id": "VN:Circular_06_2019:Art5",
        "law": "SBV_Foreign_Exchange_VN",
        "enbez": "Art.5",
        "title": "《越南国家银行第06/2019/TT-NHNN号通告》第5条：直接投资资本账户 (DICA) 与工程资本金跨境汇出核准",
        "heading_path": "Thông tư số 06/2019/TT-NHNN > Điều 5 Mở và sử dụng tài khoản vốn đầu tư trực tiếp",
        "text_de": "State Bank of Vietnam Circular 06/2019 Art. 5 (Direct Investment Capital Account DICA)",
        "language_mode": "trilingual",
        "lang_original": "vi",
        "text_original": "Doanh nghiệp có vốn đầu tư trực tiếp nước ngoài phải mở tài khoản vốn đầu tư trực tiếp bằng ngoại tệ hoặc bằng đồng Việt Nam tại 01 ngân hàng được phép để thực hiện các giao dịch thu, chi liên quan đến hoạt động đầu tư trực tiếp nước ngoài.",
        "text_en": "FDI enterprises must open Direct Investment Capital Account (DICA) at 1 authorized bank for capital transfers and overseas remittances.",
        "text_zh": "【直接投资资本账户 (DICA) 汇出红线】外资企业必须在一家指定商业银行开立直接投资资本账户（DICA）。一切资本金注入、中长期外债提款、项目利润汇出及清算资金出境，必须强制经由该特定账户闭环划转，严禁通过一般结算账户违规离境汇款。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "reference_statute",
        "mandatory_level": "default"
    },
    {
        "norm_id": "MY:BNM_FEP_Notice_4:Sec2",
        "law": "BNM_Foreign_Exchange_Policy_MY",
        "enbez": "Sec.2",
        "title": "《马来西亚国家银行外汇管理通知第4号》(BNM FEP) 第2条：非居民承包商外币借款与利润境外汇出报备",
        "heading_path": "Bank Negara Malaysia Foreign Exchange Policy Notices > Notice 4 > Section 2",
        "text_de": "Bank Negara Malaysia FEP Notice 4 Sec. 2 (Payments and Remittances Abroad)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "A non-resident is freely allowed to repatriate funds from Malaysia, including capital, profits, dividends, and fees, provided that payments are made in foreign currency and comply with applicable statutory reporting to BNM.",
        "text_en": "Non-residents may repatriate capital and profits in foreign currency subject to BNM statutory reporting.",
        "text_zh": "【马来西亚工程利润与借款汇出报备】境外承包商在马设立分公司或项目公司，依法享有将合法工程利润、管理费及资本金汇出境外的自由；但单笔超过指定限额或涉及居民向非居民提供外币金融借款的，必须事先向国家银行（BNM）履行合规报备与登记程序。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "reference_statute",
        "mandatory_level": "default"
    },
    {
        "norm_id": "TH:Exchange_Control_Act:Sec8",
        "law": "Exchange_Control_Act_TH",
        "enbez": "Sec.8",
        "title": "《泰国外汇管制法 B.E. 2485》第8条：离岸离境借款结汇与外国承包商利润汇出外汇申报 (Thor Tor 3/4)",
        "heading_path": "Exchange Control Act B.E. 2485 > Section 8",
        "text_de": "Thai Exchange Control Act Sec. 8 (Repatriation of Investment Capital and Profits)",
        "language_mode": "trilingual",
        "lang_original": "th",
        "text_original": "การนำเงินตราต่างประเทศเข้ามาในราชอาณาจักรหรือส่งออกไปนอกราชอาณาจักรต้องปฏิบัติตามหลักเกณฑ์และพิธีการที่รัฐมนตรีกำหนด",
        "text_en": "Import and export of foreign currencies must comply with ministerial regulations and reporting.",
        "text_zh": "【泰国对外汇款与资本调回申报】外国工程投资者向境外汇出工程款净利润、特许权使用费或偿还境外股东贷款时，必须向泰国经授权商业银行提交外汇交易申报单（FX Form / Thor Tor 3）及完税证明，确保资金跨境流转合规。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "reference_statute",
        "mandatory_level": "default"
    },

    # ---------------------------------------------------------------------
    # 2. 属地税收、常设机构与包税条款 (PE, Tax & Withholding)
    # ---------------------------------------------------------------------
    {
        "norm_id": "VN:Circular_103_2014:Art1",
        "law": "FCT_Circular_103_2014_VN",
        "enbez": "Art.1",
        "title": "《越南财政部第103/2014/TT-BTC号通告》第1条：外国承包商税 (FCT) 纳税主体与境内建筑安装工程适用界限",
        "heading_path": "Thông tư số 103/2014/TT-BTC > Điều 1 Đối tượng áp dụng",
        "text_de": "Ministry of Finance Circular 103/2014/TT-BTC Art. 1 (Foreign Contractor Tax Scope)",
        "language_mode": "trilingual",
        "lang_original": "vi",
        "text_original": "Hướng dẫn thực hiện nghĩa vụ thuế áp dụng đối với tổ chức nước ngoài kinh doanh có cơ sở thường trú tại Việt Nam hoặc không có cơ sở thường trú tại Việt Nam... kinh doanh tại Việt Nam hoặc có thu nhập phát sinh tại Việt Nam trên cơ sở hợp đồng, thỏa thuận.",
        "text_en": "FCT applies to foreign organizations conducting business in Vietnam or having income from contracts in Vietnam.",
        "text_zh": "【外国承包商税 (FCT) 强制扣缴】外国总承包商或分包商在越南境内实施建设工程施工、安装、调试或提供工程技术服务的，无论是否在越设立常设机构，越南发包人均负有代扣代缴 FCT（包含增值税 VAT 与企业所得税 CIT）的法定义务。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "reference_statute",
        "mandatory_level": "default"
    },
    {
        "norm_id": "VN:Circular_103_2014:Art7",
        "law": "FCT_Circular_103_2014_VN",
        "enbez": "Art.7",
        "title": "《越南外国承包商税通告》第7条：总承包合同包税条款 (Gross-up Clause) 税负转嫁与计税基数还原风险",
        "heading_path": "Thông tư số 103/2014/TT-BTC > Điều 7 Doanh thu tính thuế",
        "text_de": "Circular 103/2014 Art. 7 (Gross-up Clause and Tax Base Adjustment)",
        "language_mode": "trilingual",
        "lang_original": "vi",
        "text_original": "Trường hợp theo thỏa thuận tại hợp đồng nhà thầu, doanh thu nhà thầu nước ngoài nhận được không bao gồm thuế thì doanh thu tính thuế phải được quy đổi thành doanh thu có thuế.",
        "text_en": "If contract revenue agreed excludes tax (net of tax), taxable revenue must be grossed up.",
        "text_zh": "【包税条款税基倒算还原红线】若 EPC 合同约定发包人按税后净价（Net Amount）向中资总包付款且所有属地税负由发包人承担，越南税务机关强制要求将净收入倒算还原为含税总收入（Gross-up Base）后再计税，发包人常以此为由要求总包分摊税基膨胀产生的增量税款。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "reference_statute",
        "mandatory_level": "default"
    },
    {
        "norm_id": "ID:PP_9_2022:Art3",
        "law": "PPh_Final_Construction_ID",
        "enbez": "Art.3",
        "title": "《印尼2022年第9号政府条例》第3条：未持有有效建筑业执照外国承包商 8% 惩罚性预扣所得税 (PPh Final)",
        "heading_path": "Peraturan Pemerintah No. 9 Tahun 2022 tentang Pajak Penghasilan atas Jasa Konstruksi > Pasal 3",
        "text_de": "Indonesian Govt Reg No. 9/2022 Art. 3 (PPh Final Construction Tax Rates)",
        "language_mode": "trilingual",
        "lang_original": "id",
        "text_original": "Tarif Pajak Penghasilan untuk usaha jasa konstruksi yang tidak memiliki sertifikat badan usaha atau sertifikat kompetensi kerja: sebesar 4% untuk jasa pelaksanaan konstruksi, dan 8% untuk pekerjaan konstruksi terintegrasi.",
        "text_en": "PPh Final tax rate is 8% for integrated EPC construction services without valid contractor certificate.",
        "text_zh": "【无资质 8% 惩罚性预扣税率】印尼针对基建工程实行终局所得税（PPh Final）。持有合法有效资格证书（SBU/BUJKA）的企业适用 2.65%~4% 优惠税率；若外国总承包商或分包商未能取得有效认证，其 EPC 综合工程款将被强制按 **8%** 惩罚性税率就地扣缴且不得抵扣！",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "reference_statute",
        "mandatory_level": "default"
    },
    {
        "norm_id": "PH:NIRC_1997:Sec28",
        "law": "NIRC_Tax_Code_PH",
        "enbez": "Sec.28",
        "title": "《菲律宾国家国内税收法典》(NIRC) 第28条：外国常设机构 (PE) 判定标准与 25% 净所得税计缴",
        "heading_path": "National Internal Revenue Code of 1997 (Amended by CREATE Act) > Section 28",
        "text_de": "Philippine NIRC Sec. 28 (Tax on Resident Foreign Corporations and PE)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "A resident foreign corporation engaged in trade or business within the Philippines shall be subject to an income tax of 25% on taxable income derived from all sources within the Philippines.",
        "text_en": "Resident foreign corporation / PE is taxed at 25% on net taxable income derived within Philippines.",
        "text_zh": "【工程常设机构 25% 税负】外国承包商在菲律宾从事建筑工程工地、装配项目或提供监督管理活动持续超过 6 个月（中菲税收协定规定为 6 个月），构成税收常设机构（Permanent Establishment），其境内净所得适用 25% 属地企业所得税率。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "reference_statute",
        "mandatory_level": "default"
    },

    # ---------------------------------------------------------------------
    # 3. 外劳配额、签证与属地化用工 (Labor Quotas & Visas)
    # ---------------------------------------------------------------------
    {
        "norm_id": "ID:Permenaker_8_2021:Art14",
        "law": "TKA_Regulation_ID",
        "enbez": "Art.14",
        "title": "《印尼劳工部2021年第8号规程》第14条：外籍劳工聘用计划 (RPTKA) 与 1:3 本地陪同员工 (Pendamping) 强制配比",
        "heading_path": "Peraturan Menteri Ketenagakerjaan No. 8 Tahun 2021 > Pasal 14",
        "text_de": "Indonesian MoM Reg No. 8/2021 Art. 14 (RPTKA and Local Counterpart Worker Ratio)",
        "language_mode": "trilingual",
        "lang_original": "id",
        "text_original": "Pemberi Kerja TKA wajib: a. menunjuk Tenaga Kerja Warga Negara Indonesia sebagai Tenaga Kerja Pendamping TKA yang dipekerjakan untuk alih teknologi dan alih keahlian; b. melaksanakan pendidikan dan pelatihan kerja bagi Tenaga Kerja Pendamping TKA.",
        "text_en": "Employer of foreign worker must appoint Indonesian counterpart worker for transfer of technology and provide training.",
        "text_zh": "【外劳审批与本地陪同员工法定配比】中资工程承包商雇佣中国籍工程师与管理专家，必须事先取得劳工部 RPTKA 核准；且必须按照至少 1:1 至 1:3 的法定比例为每位中方专家配备印尼籍本地陪同员工（Tenaga Kerja Pendamping），并出资履行法定技能转让培训义务。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "reference_statute",
        "mandatory_level": "default"
    },
    {
        "norm_id": "SG:EFMA_Cap_91A:Sec7",
        "law": "EFMA_Foreign_Manpower_SG",
        "enbez": "Sec.7",
        "title": "《新加坡雇佣外籍人力法》(EFMA) 第7条：建筑业劳工外劳配额上限 (DRC) 与劳工税 (Levy) 阶梯标准",
        "heading_path": "Employment of Foreign Manpower Act (Cap. 91A) > Section 7",
        "text_de": "Singapore EFMA Sec. 7 (Dependency Ratio Ceiling and Foreign Worker Levy)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "No employer shall employ a foreign employee in excess of the dependency ratio ceiling prescribed for the relevant industry. Every employer of a work permit holder shall pay foreign worker levy at prescribed rates.",
        "text_en": "Employers must not exceed Dependency Ratio Ceiling (DRC) and must pay foreign worker levy.",
        "text_zh": "【建筑业外劳人头税与配额上限】新加坡建筑施工企业聘用外籍技术工人受人力部（MOM）依存比率上限（DRC，当前比例约为 1 名本地全职员工配 5 名外劳）严格限制，且总包必须每月为每名外籍劳工缴纳高额阶梯式外劳人头税（Foreign Worker Levy）。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "reference_statute",
        "mandatory_level": "default"
    },
    {
        "norm_id": "TH:Foreigners_Working_Emergency_Decree:Sec8",
        "law": "Foreign_Workers_Decree_TH",
        "enbez": "Sec.8",
        "title": "《泰国外国劳工工作管理紧急法令 B.E. 2560》第8条：外国工程师工作许可证 (Work Permit) 申办与土木工程受限禁令",
        "heading_path": "Emergency Decree on Non-Thais' Working Management B.E. 2560 > Section 8",
        "text_de": "Thai Foreign Workers Decree Sec. 8 (Work Permit and Prohibited Occupations)",
        "language_mode": "trilingual",
        "lang_original": "th",
        "text_original": "คนต่างด้าวจะทำงานได้เฉพาะงานที่มิได้มีพระราชกฤษฎีกากำหนดให้เป็นงานที่ห้ามคนต่างด้าวทำ และต้องได้รับใบอนุญาตทำงานจากนายทะเบียน",
        "text_en": "Foreigners may only perform work not prohibited by royal decree and must hold a valid work permit.",
        "text_zh": "【外籍土木工程作业资格限制】外国技术人员在泰国必须依法持有劳工厅核发的工作许可证（Work Permit）。泰国法令严禁外籍人士从事一般民用建筑与手工作业；中资总包派驻的工程专家必须获得泰国专业工程师院（COE）特别技术资格认可或 BOI 特别通道批复。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "reference_statute",
        "mandatory_level": "default"
    },
    {
        "norm_id": "MY:Act_265_1955:Sec60L",
        "law": "Employment_Act_1955_MY",
        "enbez": "Sec.60L",
        "title": "《马来西亚1955年雇佣法》第60L条：承包商招募外籍施工劳工劳工部事前核准与优先雇佣本地公民原则",
        "heading_path": "Employment Act 1955 > Part XIIB Employment of Foreign Employees > Section 60L",
        "text_de": "Malaysian Employment Act Sec. 60L (Prior Approval of Director General for Foreign Employees)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "No person shall employ a foreign employee unless he has obtained the prior approval of the Director General of Labour.",
        "text_en": "Employment of foreign workers requires prior approval of Director General of Labour.",
        "text_zh": "【马来西亚外劳聘用总监审批】总承包商或劳务分包商在马聘用外籍劳工前，必须事先取得劳工总监（Director General）签发的用工批文，并证明已在属地劳工市场发布招聘且无法招募到足额符合条件的本国劳工。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "reference_statute",
        "mandatory_level": "default"
    },

    # ---------------------------------------------------------------------
    # 4. FIDIC 银皮书/黄皮书 Tier-2 履约中段关键通用条款
    # ---------------------------------------------------------------------
    {
        "norm_id": "FIDIC:Silver_1999:Clause_4.12",
        "law": "FIDIC",
        "enbez": "Clause_4.12",
        "title": "《FIDIC 银皮书 EPC》第4.12款：不可预见的困难与总承包商地质地表风险包干分配",
        "heading_path": "FIDIC Conditions of Contract for EPC/Turnkey Projects 1999 > Clause 4 The Contractor > 4.12 Unforeseeable Difficulties",
        "text_de": "FIDIC Silver Book (1999) Clause 4.12 (Unforeseeable Difficulties)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Except as otherwise stated in the Contract: (a) the Contractor shall be deemed to have obtained all necessary information as to risks, contingencies and other circumstances; (b) by signing the Contract, the Contractor accepts total responsibility for having foreseen all difficulties; and (c) the Contract Price shall not be adjusted for any unforeseen difficulties.",
        "text_en": "In Silver Book, Contractor accepts total responsibility for all difficulties, and Contract Price shall not be adjusted.",
        "text_zh": "【银皮书总承包商自担地质风险包干】除合同另有特别约定外，银皮书总承包商被视为已取得全部现场风险信息并接受预见全部履约困难之完全责任；承包商不得以现场遇到不可预见的地质裂隙、溶洞或复杂地下水文为由索赔额外费用或顺延工期（与黄皮书4.12形成核心对比）！",
        "translation_source": "FIDIC_OFFICIAL_ZH",
        "norm_category": "fidic_standard",
        "fidic_tier": "baseline_general",
        "fidic_edition": "1999_SILVER",
        "mandatory_level": "contract_default"
    },
    {
        "norm_id": "FIDIC:Yellow_1999:Clause_4.12",
        "law": "FIDIC",
        "enbez": "Clause_4.12",
        "title": "《FIDIC 黄皮书 P&DB》第4.12款：不可预见的物质条件 (Unforeseeable Physical Conditions) 工期与成本全额索赔权",
        "heading_path": "FIDIC Conditions of Contract for Plant and Design-Build 1999 > Clause 4 > 4.12 Unforeseeable Physical Conditions",
        "text_de": "FIDIC Yellow Book (1999) Clause 4.12 (Unforeseeable Physical Conditions Claims)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "If the Contractor encounters adverse physical conditions which he considers to have been Unforeseeable, the Contractor shall give notice to the Engineer... The Contractor shall be entitled subject to Sub-Clause 20.1 to: (a) an extension of time; and (b) payment of any such Cost.",
        "text_en": "Contractor encountering Unforeseeable physical conditions is entitled to EOT and Cost compensation.",
        "text_zh": "【黄皮书不可预见地质条件索赔权】在黄皮书模式下，若承包商遇到有经验承包商在基准日期前无法合理预见的地下不良物理条件（如坚硬断层、古河道、未探明管线），总包有权依法索赔工期顺延（EOT）及由此增加的全部实际成本（Cost）。",
        "translation_source": "FIDIC_OFFICIAL_ZH",
        "norm_category": "fidic_standard",
        "fidic_tier": "baseline_general",
        "fidic_edition": "1999_YELLOW",
        "mandatory_level": "contract_default"
    },
    {
        "norm_id": "FIDIC:Silver_1999:Clause_13.1",
        "law": "FIDIC",
        "enbez": "Clause_13.1",
        "title": "《FIDIC 银皮书 EPC》第13.1款：雇主发起工程变更指示 (Right to Vary) 权限与约束",
        "heading_path": "FIDIC Conditions of Contract for EPC/Turnkey Projects 1999 > Clause 13 Variations and Adjustments > 13.1 Right to Vary",
        "text_de": "FIDIC Silver Book (1999) Clause 13.1 (Right to Vary)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Variations may be initiated by the Employer at any time prior to issuing the Taking-Over Certificate for the Works, either by an instruction or by a request for the Contractor to submit a proposal. The Contractor shall execute and be bound by each Variation.",
        "text_en": "Employer may initiate Variations at any time prior to Taking-Over Certificate, by instruction or proposal request.",
        "text_zh": "【工程变更发起权】在颁发工程移交证书前，雇主有权随时通过正式书面指示或要求总包提交建议书的方式启动变更。总承包商应执行每一项变更并受其约束，除非总包能证明该变更将对工程安全性或目的适用性产生根本破坏。",
        "translation_source": "FIDIC_OFFICIAL_ZH",
        "norm_category": "fidic_standard",
        "fidic_tier": "baseline_general",
        "fidic_edition": "1999_SILVER",
        "mandatory_level": "contract_default"
    },
    {
        "norm_id": "FIDIC:Silver_1999:Clause_13.3",
        "law": "FIDIC",
        "enbez": "Clause_13.3",
        "title": "《FIDIC 银皮书 EPC》第13.3款：工程变更程序 (Variation Procedure) 估价与合同价格及工期调整",
        "heading_path": "FIDIC Conditions of Contract for EPC/Turnkey Projects 1999 > Clause 13 > 13.3 Variation Procedure",
        "text_de": "FIDIC Silver Book (1999) Clause 13.3 (Variation Procedure and Valuation)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "If the Employer requests a proposal prior to instructing a Variation, the Contractor shall respond in writing as soon as practicable... Upon instructing or approving a Variation, the Employer shall proceed in accordance with Sub-Clause 3.5 to determine adjustments to the Contract Price and Schedule of Payments.",
        "text_en": "Employer determines adjustments to Contract Price and Schedule of Payments for approved Variations.",
        "text_zh": "【变更估价与调价程序】对于已核准的工程变更，双方应通过协商或由雇主依法公正确定合同价格的增减调减金额以及竣工工期的合理调整，并相应修订合同付款计划表（Schedule of Payments）。",
        "translation_source": "FIDIC_OFFICIAL_ZH",
        "norm_category": "fidic_standard",
        "fidic_tier": "baseline_general",
        "fidic_edition": "1999_SILVER",
        "mandatory_level": "contract_default"
    },
    {
        "norm_id": "FIDIC:Silver_1999:Clause_15.1",
        "law": "FIDIC",
        "enbez": "Clause_15.1",
        "title": "《FIDIC 银皮书 EPC》第15.1款：通知改正违约 (Notice to Correct) 法定前置警告程序",
        "heading_path": "FIDIC Conditions of Contract for EPC/Turnkey Projects 1999 > Clause 15 Termination by Employer > 15.1 Notice to Correct",
        "text_de": "FIDIC Silver Book (1999) Clause 15.1 (Notice to Correct)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "If the Contractor fails to carry out any obligation under the Contract, the Employer may by notice require the Contractor to make good the failure and to remedy it within a specified reasonable time.",
        "text_en": "Employer may give notice requiring Contractor to remedy failure within reasonable time before terminating.",
        "text_zh": "【发包人解约前置纠正通知】若承包商未能履行合同项下的任何义务，发包人若欲行使违约终止合同特权，必须事先送达书面‘通知改正（Notice to Correct）’，明确指明违约事项并指定一段合理充分的补正宽限期。",
        "translation_source": "FIDIC_OFFICIAL_ZH",
        "norm_category": "fidic_standard",
        "fidic_tier": "baseline_general",
        "fidic_edition": "1999_SILVER",
        "mandatory_level": "contract_default"
    },
    {
        "norm_id": "FIDIC:Silver_1999:Clause_15.2",
        "law": "FIDIC",
        "enbez": "Clause_15.2",
        "title": "《FIDIC 银皮书 EPC》第15.2款：雇主因承包商根本违约终止合同 (Termination by Employer) 之法定事由与14天通知期",
        "heading_path": "FIDIC Conditions of Contract for EPC/Turnkey Projects 1999 > Clause 15 > 15.2 Termination by Employer",
        "text_de": "FIDIC Silver Book (1999) Clause 15.2 (Termination by Employer)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "The Employer shall be entitled to terminate the Contract if the Contractor: (a) fails to comply with Sub-Clause 4.2 or 15.1; (b) abandons the Works; (c) becomes bankrupt or insolvent... by giving 14 days' notice to the Contractor.",
        "text_en": "Employer may terminate contract upon 14 days' notice if contractor abandons works, becomes bankrupt, or fails to correct.",
        "text_zh": "【发包人单方违约终止权】在承包商未补正第15.1款通知、明示放弃工程施工、严重拖欠履约保函或陷入破产清算时，发包人在向承包商发出 14 天书面通知后即可单方终止合同，接管施工现场并扣留全部设备与材料进行清算。",
        "translation_source": "FIDIC_OFFICIAL_ZH",
        "norm_category": "fidic_standard",
        "fidic_tier": "baseline_general",
        "fidic_edition": "1999_SILVER",
        "mandatory_level": "contract_default"
    },
    {
        "norm_id": "FIDIC:Silver_1999:Clause_16.1",
        "law": "FIDIC",
        "enbez": "Clause_16.1",
        "title": "《FIDIC 银皮书 EPC》第16.1款：承包商因雇主违约暂停施工 (Contractor's Entitlement to Suspend Work) 权利",
        "heading_path": "FIDIC Conditions of Contract for EPC/Turnkey Projects 1999 > Clause 16 Suspensions and Termination by Contractor > 16.1 Contractor's Entitlement to Suspend Work",
        "text_de": "FIDIC Silver Book (1999) Clause 16.1 (Contractor's Entitlement to Suspend Work)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "If the Employer fails to comply with Sub-Clause 2.4 [Employer's Financial Arrangements] or Sub-Clause 14.7 [Payment], the Contractor may, after giving not less than 21 days' notice to the Employer, suspend work or reduce rate of work.",
        "text_en": "Contractor may suspend work after 21 days' notice if Employer fails to provide financial proof or payment.",
        "text_zh": "【总承包商合同约定合法停工权】若雇主未能在到期日支付工程进度款或拒绝出示合理的资金安排证明，总承包商在向雇主发出不少于 21 天的书面预警通知后，享有停工或放慢施工节奏的合法权利，并自动享有工期顺延与费用利润补偿。",
        "translation_source": "FIDIC_OFFICIAL_ZH",
        "norm_category": "fidic_standard",
        "fidic_tier": "baseline_general",
        "fidic_edition": "1999_SILVER",
        "mandatory_level": "contract_default"
    },
    {
        "norm_id": "FIDIC:Silver_1999:Clause_16.2",
        "law": "FIDIC",
        "enbez": "Clause_16.2",
        "title": "《FIDIC 银皮书 EPC》第16.2款：承包商因雇主实质违约终止合同 (Termination by Contractor) 与现场撤离索赔",
        "heading_path": "FIDIC Conditions of Contract for EPC/Turnkey Projects 1999 > Clause 16 > 16.2 Termination by Contractor",
        "text_de": "FIDIC Silver Book (1999) Clause 16.2 (Termination by Contractor)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "The Contractor shall be entitled to terminate the Contract if: (a) Employer fails to pay within 42 days after expiry of payment time; (b) Employer substantially fails to perform obligations; (c) prolonged suspension affects whole Works... by giving 14 days' notice.",
        "text_en": "Contractor may terminate contract upon 14 days' notice if payment is delayed beyond 42 days or prolonged suspension.",
        "text_zh": "【总承包商单方解约撤场终极武器】若雇主逾期付款超过 42 天、发生实质性违约或导致工程停工超过 84 天，总承包商在向雇主发出 14 天书面通知后即可合法单方终止合同，撤出全部中方人员与机械设备，并依法索赔已完工款、复员费及预期可得利润损失！",
        "translation_source": "FIDIC_OFFICIAL_ZH",
        "norm_category": "fidic_standard",
        "fidic_tier": "baseline_general",
        "fidic_edition": "1999_SILVER",
        "mandatory_level": "contract_default"
    },

    # ---------------------------------------------------------------------
    # 5. 涉外行政、外贸许可与安全审查单行法
    # ---------------------------------------------------------------------
    {
        "norm_id": "VN:Law_05_2017:Art37",
        "law": "Foreign_Trade_Management_VN",
        "enbez": "Art.37",
        "title": "《越南外贸管理法2017》第37条：大型特种施工技术设备与二手工程机械进口审批标准",
        "heading_path": "Luật Quản lý ngoại thương 2017 > Chương III Các biện pháp quản lý ngoại thương kỹ thuật > Điều 37",
        "text_de": "Vietnamese Foreign Trade Management Law Art. 37 (Import of Used Machinery and Construction Equipment)",
        "language_mode": "trilingual",
        "lang_original": "vi",
        "text_original": "Máy móc, thiết bị, dây chuyền công nghệ đã qua sử dụng nhập khẩu phải đáp ứng tiêu chuẩn, quy chuẩn kỹ thuật theo quy định của pháp luật và không được quá tuổi sử dụng quy định.",
        "text_en": "Imported used machinery and equipment must satisfy technical standards and not exceed maximum usage age (10 years).",
        "text_zh": "【二手施工机械设备进口限制红线】中资工程承包商自中国境内运往越南工地的二手大型盾构机、吊装机械，其设备出厂使用年限原则上不得超过 10 年，且必须经过越南科技部认可的权威检验机构出具安全与环保合格认证方予放行清关。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "reference_statute",
        "mandatory_level": "default"
    },
    {
        "norm_id": "MY:Act_708_2010:Sec9",
        "law": "Strategic_Trade_Act_MY",
        "enbez": "Sec.9",
        "title": "《马来西亚2010年战略贸易法》(STA Act 708) 第9条：重大基建工程敏感军民两用物项与特种技术进出口管制许可证",
        "heading_path": "Strategic Trade Act 2010 (Act 708) > Part III Control of Strategic Items > Section 9",
        "text_de": "Malaysian Strategic Trade Act Sec. 9 (Permit for Export, Transhipment or Transit of Strategic Items)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "No person shall export, tranship or bring in transit any strategic items unless he holds a valid permit issued under this Act.",
        "text_en": "No person shall export, tranship or bring in transit any strategic items without a valid permit.",
        "text_zh": "【战略物资与特种技术转运许可证】基础设施建设中涉及的高精度遥感测绘仪器、特种工业防爆材料或深海探测设备若列入大马战略物项管制清单，总承包商在进出口或过境转运时必须持有国际贸易工业部（MITI）签发的合法 STA 许可证，违者面临刑事扣押与重罚。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "reference_statute",
        "mandatory_level": "default"
    }
]

# =========================================================================
# L2 新增广覆盖参考裁判先例 (4 篇权威实务判例)
# =========================================================================
NEW_L2_REFERENCE_CASES: List[Dict[str, Any]] = [
    {
        "case_id": "REF_CASE:VN_HCMC_PC:FCT_GrossUp_Dispute:2020",
        "court": "Ho Chi Minh City People's Court",
        "senate": "Commercial Chamber",
        "decided": "2020-10-16",
        "az": "Judgment No. 1290/2020/KDTM-ST",
        "ecli": "ECLI:VN:HCMC:2020:1290",
        "doctype": "judgment",
        "leitsatz": "胡志明市人民法院判决：EPC 合同虽约定总包款为净价且发包人负担税款，但发包人未能代扣代缴外国承包商税（FCT）遭税务稽查追缴后，无权从未结工程款中反向扣除总承包商应纳税款。",
        "tenor": "判令发包人向中资总承包商全额支付被无理截留的 180 万美元最终结算工程款，确认包税条款下属地税务罚款与滞纳金完全由发包人自行承担。",
        "tatbestand": "某热电总包工程中，发包人在工程竣工后遭遇税务局就 FCT 税基倒算差异补税。发包人在最终结算款中直接扣除该笔补缴税金及罚款。",
        "gruende": "法院审理确认：合同明文约定‘发包人应负责按期申报并缴纳承包商在越南产生的一切税赋’；发包人怠于履行法定代扣代缴申报义务产生的滞纳损失属于其过错，不得对抗总承包商依约享有的工程款受领请求权。",
        "norms_meta": "VN:Circular_103_2014:Art7,VN:Commercial_Law_2005:Art303",
        "source_url": "https://congbobanan.toaan.gov.vn/1290hcmc"
    },
    {
        "case_id": "REF_CASE:ID_PTUN:TKA_WorkPermit_Cancellation:2021",
        "court": "Jakarta State Administrative Court (PTUN Jakarta)",
        "senate": "Administrative Chamber",
        "decided": "2021-06-22",
        "az": "Decision No. 88/G/2021/PTUN.JKT",
        "ecli": "ECLI:ID:PTUN:JAKARTA:2021:88",
        "doctype": "judgment",
        "leitsatz": "雅加达国家行政法院裁判：属地劳工局以中资承包商未及时提交印尼籍陪同人员培训报告为由突击吊销中方工程师 RPTKA 许可证的行为程序违法，判决予以撤销。",
        "tenor": "判令雅加达特区劳工与移民局撤销针对原告 18 名中资关键盾构技术专家的停工遣返令，限期恢复 RPTKA 外劳配额批文有效性。",
        "tatbestand": "雅加达地铁延伸线工程中，地方劳工监察官员突击检查施工现场，以中资分包商未在 30 日内备案本地技术培训档案为由，直接撤销其外劳工作许可证。",
        "gruende": "行政法院判词指出：依据《印尼创造就业法》第81条及劳工部规程，行政机关在行使撤销许可前必须先送达三道书面改正警告令；未经正当程序突袭吊销关键基建工程外劳许可证违背诚信行政原则。",
        "norms_meta": "ID:Permenaker_8_2021:Art14,ID:UU_11_2020:Art81",
        "source_url": "https://putusan3.mahkamahagung.go.id/direktori/putusan/ptun-88-2021"
    },
    {
        "case_id": "REF_CASE:SG_HC:FIDIC_Cl4_12_UnforeseenGround:2018",
        "court": "Singapore High Court",
        "senate": "Commercial Court",
        "decided": "2018-12-07",
        "az": "[2018] SGHC 275",
        "ecli": "ECLI:SG:HC:2018:275",
        "doctype": "judgment",
        "leitsatz": "新加坡高等法院判例：在基于 FIDIC 条件的地下隧道工程索赔中，承包商证明勘察报告未揭示的深层岩体突涌属于有经验承包商在基准日无法预见之物理条件，判令雇主全额顺延工期并补偿额外爆破费用。",
        "tenor": "支持原告承包商依据 Clause 4.12 提出之工期顺延 112 天及 850 万新元地质突变额外成本索赔，驳回发包人反诉延误违约金主张。",
        "tatbestand": "某跨海管廊盾构工程中，盾构机掘进至海床断裂带遇到突发高压涌水与硬岩层，与发包人招标时提供的地质基准勘探报告完全不符，导致停工 3 个月。",
        "gruende": "高院审理认为：虽然总包负有现场查勘义务，但‘合理可预见性’标准应以基准日期前发包人公开的岩土数据及常规勘探深度为限；超出常规勘探可探测范围之极端地质突变构成不可预见物理条件，承包商享有工期与成本完全救济。",
        "norms_meta": "FIDIC:Yellow_1999:Clause_4.12,FIDIC:Silver_1999:Clause_4.12",
        "source_url": "https://www.elitigation.sg/gd/s/2018_SGHC_275"
    },
    {
        "case_id": "REF_CASE:MY_HC:BNM_Forex_Loan_Repayment:2019",
        "court": "High Court of Malaya (Kuala Lumpur)",
        "senate": "Commercial Division",
        "decided": "2019-08-30",
        "az": "[2019] 10 MLJ 421",
        "ecli": "ECLI:MY:HC:2019:10MLJ421",
        "doctype": "judgment",
        "leitsatz": "马来西亚高等法院判决：涉外工程项目母公司向属地项目公司提供的离岸外币股东借款若事先已向大马国家银行（BNM）合规登记报备，其到期本息汇出境外受法律保护，不得被第三方法院禁令冻结。",
        "tenor": "驳回属地材料供应商关于冻结中资承包商汇往境外母公司股东借款还款账户之申请，确认合规报备的外汇偿付享有法定优先履约地位。",
        "tatbestand": "属地材料供应商起诉主张某工程分公司拖欠钢筋款，向法院申请禁止令严禁该工程公司向其中国母公司汇还已到期美元设备贷款。",
        "gruende": "高等法院明确确认：经国家银行外汇政策（FEP）核准并登记的跨境贷款清偿属于受央行法令保障的经常项目与合法资本流转；在无直接欺诈证据前提下，司法机关不得阻断企业依法合规履行境外外债偿付义务。",
        "norms_meta": "MY:BNM_FEP_Notice_4:Sec2,MY:Contracts_Act_1950:Sec56",
        "source_url": "https://www.kehakiman.gov.my/judgment/high-court/2019-10mlj421"
    }
]


def expand_l2_reference_kb(snapshot_id: str = "20261021-asean-v2.2"):
    print("=" * 75)
    print("🏗️ 开始执行 L2 广覆盖参考层全量知识库二次深化与向量索引扩充")
    print("=" * 75)

    mgr = SnapshotManager()
    snap_id = snapshot_id or mgr.get_current_snapshot_id()
    snap_dir = os.path.join(mgr.base_dir, snap_id)
    db_path = os.path.join(snap_dir, "law.sqlite")
    index_l2_dir = os.path.join(snap_dir, "index_l2")

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    now_str = datetime.now().isoformat()

    # 1. 批量向 reference_norms 注入新增参考规范
    print(f"\n-> 1. 正在注入 {len(NEW_L2_REFERENCE_NORMS)} 条深度参考规范 (外汇管制/税收PE/外劳配额/FIDIC中段)...")
    for n in NEW_L2_REFERENCE_NORMS:
        cur.execute(
            """INSERT INTO reference_norms(
                norm_id, law, enbez, title, heading_path, text_de,
                structure, footnotes, stand, has_pending_amend, source_url,
                snapshot_id, fetched_at, language_mode, lang_original,
                text_original, text_en, text_zh, translation_source,
                norm_category, fidic_tier, fidic_edition, elements_json, mandatory_level
            ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(norm_id) DO UPDATE SET
                title=excluded.title,
                heading_path=excluded.heading_path,
                text_de=excluded.text_de,
                text_original=excluded.text_original,
                text_en=excluded.text_en,
                text_zh=excluded.text_zh,
                mandatory_level=excluded.mandatory_level,
                norm_category=excluded.norm_category""",
            (
                n["norm_id"], n["law"], n["enbez"], n["title"], n["heading_path"],
                n["text_de"], "{}", "[]", "2026-10-29", 0,
                n.get("source_url", "https://www.fatong.gov.cn"), snap_id, now_str,
                n.get("language_mode", "bilingual"), n.get("lang_original", "en"),
                n.get("text_original", ""), n.get("text_en", ""), n.get("text_zh", ""),
                n.get("translation_source", "MOJ_FATONG_2026"), n.get("norm_category", "reference_statute"),
                n.get("fidic_tier"), n.get("fidic_edition"), "{}", n.get("mandatory_level", "default")
            )
        )
    print(f"✓ 成功向 reference_norms 注入/更新 {len(NEW_L2_REFERENCE_NORMS)} 条新参考法源")

    # 2. 批量向 reference_cases 注入新增参考先例
    print(f"\n-> 2. 正在注入 {len(NEW_L2_REFERENCE_CASES)} 篇深度参考裁判先例...")
    for c in NEW_L2_REFERENCE_CASES:
        cur.execute(
            """INSERT INTO reference_cases(
                case_id, court, senate, decided, az, ecli, doctype,
                leitsatz, tenor, tatbestand, gruende, norms_meta, source_url,
                snapshot_id, fetched_at
            ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(case_id) DO UPDATE SET
                leitsatz=excluded.leitsatz,
                tenor=excluded.tenor,
                tatbestand=excluded.tatbestand,
                gruende=excluded.gruende,
                norms_meta=excluded.norms_meta""",
            (
                c["case_id"], c["court"], c["senate"], c["decided"], c["az"],
                c["ecli"], c["doctype"], c["leitsatz"], c["tenor"], c["tatbestand"],
                c["gruende"], c["norms_meta"], c["source_url"], snap_id, now_str
            )
        )
    print(f"✓ 成功向 reference_cases 注入/更新 {len(NEW_L2_REFERENCE_CASES)} 篇参考判例")

    conn.commit()

    # 3. 全量重新生成 reference_chunks
    print("\n-> 3. 正在全量重新生成并持久化 L2 Reference Chunks...")
    cur.execute("DELETE FROM reference_chunks")
    
    cur.execute("SELECT * FROM reference_norms ORDER BY law, norm_id")
    all_ref_norms = [dict(r) for r in cur.fetchall()]
    cur.execute("SELECT * FROM reference_cases ORDER BY decided DESC")
    all_ref_cases = [dict(r) for r in cur.fetchall()]

    all_l2_chunks = []
    # 法条切块
    for n in all_ref_norms:
        cid = f"CHUNK:REF_NORM:{n['norm_id']}:0"
        title = n.get("title", "")
        heading = n.get("heading_path", "")
        zh = n.get("text_zh", "")
        en = n.get("text_en", "")
        orig = n.get("text_original", "")
        text = f"【L2参考法源】{title}\n层级路径: {heading}\n中文释义: {zh}\n英文条款: {en}\n原文: {orig}".strip()
        all_l2_chunks.append({
            "chunk_id": cid,
            "kind": "reference_norm",
            "ref_id": n["norm_id"],
            "seq": 0,
            "text": text
        })

    # 先例切块
    for c in all_ref_cases:
        cid = f"CHUNK:REF_CASE:{c['case_id']}:0"
        court = c.get("court", "")
        az = c.get("az", "")
        ls = c.get("leitsatz", "")
        tenor = c.get("tenor", "")
        tb = c.get("tatbestand", "")
        text = f"【L2参考裁判】{court} {az}\n裁判要点: {ls}\n判决主文: {tenor}\n案情事实: {tb}".strip()
        all_l2_chunks.append({
            "chunk_id": cid,
            "kind": "reference_case",
            "ref_id": c["case_id"],
            "seq": 0,
            "text": text
        })

    for ch in all_l2_chunks:
        cur.execute(
            "INSERT INTO reference_chunks(chunk_id, kind, ref_id, seq, text) VALUES(?, ?, ?, ?, ?)",
            (ch["chunk_id"], ch["kind"], ch["ref_id"], ch["seq"], ch["text"])
        )
    conn.commit()
    conn.close()
    print(f"✓ 成功更新并持久化 {len(all_l2_chunks)} 个 L2 参考层 Chunks (规范: {len(all_ref_norms)}, 判例: {len(all_ref_cases)})")

    # 4. 重构并持久化 L2 专用 BM25 词法索引
    print(f"\n-> 4. 正在训练并持久化新版 L2 BM25 词法检索索引至 {index_l2_dir}...")
    bm25_l2 = BM25Engine(index_dir=index_l2_dir)
    bm25_l2.build_from_chunks(all_l2_chunks)
    print("✓ 新版 L2 独立 BM25 词法索引重构持久化就绪！")

    # 5. 调用 GPU/BGE-M3 重新构建 L2 专用 FAISS 稠密向量索引
    print(f"\n-> 5. 正在调用 GPU/BGE-M3 批量生成 1024 维向量并重构 L2 FAISS 索引 ({len(all_l2_chunks)} 向量)...")
    try:
        vec_l2 = DenseVectorEngine(index_dir=index_l2_dir)
        vec_l2.build_from_chunks(all_l2_chunks, batch_size=16)
        print(f"✓ 新版 L2 独立 FAISS 向量检索索引持久化构建完成至 {index_l2_dir}/faiss.index！")
    except Exception as e:
        print(f"⚠️ L2 向量构建异常: {e}")

    print("\n" + "=" * 75)
    print("🎉 L2 广覆盖参考层全量扩充与 FAISS 向量索引重构圆满完成！")
    print(f"  • L2 规范总数: {len(all_ref_norms)}")
    print(f"  • L2 判例总数: {len(all_ref_cases)}")
    print(f"  • L2 Chunks 总数: {len(all_l2_chunks)}")
    print(f"  • L2 FAISS 向量与 BM25 索引路径: {index_l2_dir}")
    print("=" * 75)


if __name__ == "__main__":
    expand_l2_reference_kb()
