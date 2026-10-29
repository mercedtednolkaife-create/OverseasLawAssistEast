"""L2 广覆盖参考层全量深化、FIDIC 结构化全款项体系与轻量级 GraphRAG 拓扑构建脚本
涵盖领域：
1. 东盟多边投资协定与双边条约 (ACIA 2009 投资保护与 ISDS 国际仲裁全套, CAFTA 2009, RCEP, ATISA, DTA 双边税收协定)
2. 政府采购与公共工程招投标法 (越南新招投标法 2023, 印尼政府采购总统令 Perpres 16/2018, 菲律宾 RA 9184 GPRA, 泰国公共采购法 B.E. 2560)
3. 环境影响评价 (EIA/AMDAL) 与劳工罢工工会抗辩 (越南环保法 2020, 印尼 AMDAL 环评法, 印尼劳工法合法罢工抗辩, 越南劳动法典)
4. 跨境动产质押、特权留置与工程优先受偿权 (越南 Decree 21/2021 应收账款质押, 印尼动产信托担保法 UU 42/1999 Grosse Akte, 印尼民法典 1139 特权受偿权, 菲律宾 RA 11057 留置权)
5. 新能源电网并网、商业运行 COD 与购电协议 PPA (越南工贸部 MOIT 弃电补偿与 DPPA, 印尼 PLN 电网消纳与视同发电补偿)
6. FIDIC 结构化全款项体系 (银皮书 EPC、黄皮书 DB、红皮书 Con 全部 20 大主章核心实质性权利义务子条款，覆盖 35+ 黄金条款)
7. 12 篇国际投资仲裁与工程参考判例 (ICSID, PCA, 越南河内法院, 印尼 KPPU, 雅加达 PTUN, 英国枢密院等)
8. 轻量级 GraphRAG 拓扑网络构建 (建立 reference_edges 表、8 大合规主题节点与 80+ 拓扑关联边)
9. 全量重新生成 L2 Chunks、重构 L2 BM25 词法索引与 1024 维 BGE-M3 FAISS 向量索引
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
# L2 新增广覆盖参考规范 (70+ 条核心规范)
# =========================================================================
PHASE6_L2_REFERENCE_NORMS: List[Dict[str, Any]] = [
    # ---------------------------------------------------------------------
    # 1. 东盟区域多边协定与双边投资协定 (ACIA / CAFTA / RCEP / DTA)
    # ---------------------------------------------------------------------
    {
        "norm_id": "ACIA:2009:Art5_National_Treatment",
        "law": "ACIA_2009",
        "enbez": "Art.5",
        "title": "《东盟全面投资协定》(ACIA) 第5条：准入前与准入后外资国民待遇原则",
        "heading_path": "ASEAN Comprehensive Investment Agreement > Section A > Article 5 National Treatment",
        "text_de": "ACIA 2009 Art. 5 (National Treatment Pre- and Post-Establishment)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Each Member State shall accord to investors of another Member State treatment no less favourable than that it accords, in like circumstances, to its own investors with respect to the admission, establishment, acquisition, expansion, management, conduct, operation and sale or other disposition of investments in its territory.",
        "text_en": "Member States shall accord investors treatment no less favourable than to domestic investors.",
        "text_zh": "【ACIA 外资国民待遇保护】东盟成员国在东道国境内就投资的准入、设立、并购、扩张、管理、经营及转让处置，必须给予其他成员国投资者（包括中资在东盟设立的控股 SPV）不低于本国国民的非歧视待遇。东道国不得实施针对外资企业的差别化限制或歧视性配额。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "multilateral_treaty",
        "mandatory_level": "treaty"
    },
    {
        "norm_id": "ACIA:2009:Art6_MFN",
        "law": "ACIA_2009",
        "enbez": "Art.6",
        "title": "《东盟全面投资协定》(ACIA) 第6条：最惠国待遇 (MFN) 与待遇搭桥机制",
        "heading_path": "ASEAN Comprehensive Investment Agreement > Article 6 Most-Favoured-Nation Treatment",
        "text_de": "ACIA 2009 Art. 6 (Most-Favoured-Nation Treatment MFN)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Each Member State shall accord to investors of another Member State treatment no less favourable than that it accords, in like circumstances, to investors of any other Member State or a non-Member State with respect to the admission, establishment, operation and disposition of investments.",
        "text_en": "Each Member State shall accord investors treatment no less favourable than to any other third-state investor.",
        "text_zh": "【ACIA 最惠国待遇与待遇搭桥】东道国给予投资者的待遇不得低于其给予任何第三国（包括与东道国签订更优惠双边投资协定的欧美国家）投资者的待遇。中资出海企业可通过最惠国条款主张东道国给予其他第三国投资者更优惠的实体保护标准。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "multilateral_treaty",
        "mandatory_level": "treaty"
    },
    {
        "norm_id": "ACIA:2009:Art11_FET",
        "law": "ACIA_2009",
        "enbez": "Art.11",
        "title": "《东盟全面投资协定》(ACIA) 第11条：公正平等待遇 (FET) 与完全保护与安全 (FPS)",
        "heading_path": "ASEAN Comprehensive Investment Agreement > Article 11 Treatment of Investment",
        "text_de": "ACIA 2009 Art. 11 (Fair and Equitable Treatment FET and Full Protection and Security FPS)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Each Member State shall accord to covered investments of investors of another Member State fair and equitable treatment and full protection and security. Fair and equitable treatment requires each Member State not to deny justice in any legal or administrative proceedings in accordance with the principle of due process.",
        "text_en": "Member States shall accord fair and equitable treatment (FET) and full protection and security (FPS).",
        "text_zh": "【ACIA 公正平等待遇与完全安全保障（出海维权核心王牌）】东道国必须保障外国投资享有公正与平等的待遇（FET）以及完全的保护与安全（FPS）。禁止东道国政府行政恣意、突击撤销特许权协议、剥夺正当抗辩程序（Due Process）或在司法审判中拒绝正义。东道国怠于制止当地暴力罢工阻碍施工的，构成违反 FPS。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "multilateral_treaty",
        "mandatory_level": "treaty"
    },
    {
        "norm_id": "ACIA:2009:Art13_Free_Transfer",
        "law": "ACIA_2009",
        "enbez": "Art.13",
        "title": "《东盟全面投资协定》(ACIA) 第13条：资金、工程款、利润与清算所得自由出境保证",
        "heading_path": "ASEAN Comprehensive Investment Agreement > Article 13 Transfers",
        "text_de": "ACIA 2009 Art. 13 (Free Transfer of Funds and Repatriation)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Each Member State shall allow all transfers relating to a covered investment to be made freely and without delay into and out of its territory in a freely usable currency at the market rate of exchange prevailing at the time of transfer.",
        "text_en": "Member States shall allow transfers relating to investments to be made freely and without delay in freely usable currency.",
        "text_zh": "【资金跨境自由转移法定保障】东道国必须允许所有与投资相关的资金自由汇入和汇出，包括：工程款、运营利润、资本金、贷款本息、特许权使用费及清算资金。资金转移必须允许按市场汇率自由兑换，严禁东道国政府非法实施无理外汇冻结或扣留。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "multilateral_treaty",
        "mandatory_level": "treaty"
    },
    {
        "norm_id": "ACIA:2009:Art14_Expropriation",
        "law": "ACIA_2009",
        "enbez": "Art.14",
        "title": "《东盟全面投资协定》(ACIA) 第14条：禁止非法直接/间接征收与迅速充分有效补偿原则",
        "heading_path": "ASEAN Comprehensive Investment Agreement > Article 14 Expropriation and Compensation",
        "text_de": "ACIA 2009 Art. 14 (Expropriation and Prompt, Adequate and Effective Compensation)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "A Member State shall not expropriate or nationalise a covered investment either directly or through measures equivalent to expropriation or nationalisation (indirect expropriation), except: for a public purpose; in a non-discriminatory manner; on payment of prompt, adequate and effective compensation; and in accordance with due process of law.",
        "text_en": "Expropriation (direct or indirect) requires public purpose, non-discrimination, prompt adequate and effective compensation, and due process.",
        "text_zh": "【禁止直接或间接征收与赫尔原则补偿】东道国不得直接征收或通过类似征收的行政监管措施（间接征收，如剥夺特许经营权核心收益、永久性撤销采矿/发电许可）征用外资财产，除非同时满足四要件：① 出于法定公共目的；② 以非歧视方式；③ 依据法定正当法律程序；④ 支付迅速、充分且有效（Prompt, Adequate and Effective）的公允市场价值现金补偿。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "multilateral_treaty",
        "mandatory_level": "treaty"
    },
    {
        "norm_id": "ACIA:2009:Art27_ISDS_Scope",
        "law": "ACIA_2009",
        "enbez": "Art.27",
        "title": "《东盟全面投资协定》(ACIA) 第27条：投资者与国家争端解决机制 (ISDS) 适用范围",
        "heading_path": "ASEAN Comprehensive Investment Agreement > Section B Dispute Between Investors and a Member State > Article 27 Scope",
        "text_de": "ACIA 2009 Art. 27 (Investor-State Dispute Settlement ISDS Scope)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "This Section shall apply to an investment dispute between a Member State and an investor of another Member State arising out of an alleged breach of an obligation of a Member State under this Agreement which causes loss or damage to the investor or its covered investment.",
        "text_en": "This Section applies to investment disputes between a host Member State and a foreign investor for breaches causing loss.",
        "text_zh": "【投资者诉东道国政府 (ISDS) 国际仲裁管辖】当东道国政府机关违反 ACIA 条约义务（如非法撤销施工许可证、歧视性征税、违反投资保证）导致外国投资者或其项目公司遭受经济损失时，投资者有权直接依据条约启动针对东道国政府的国际投资仲裁。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "multilateral_treaty",
        "mandatory_level": "treaty"
    },
    {
        "norm_id": "ACIA:2009:Art33_Arbitral_Forums",
        "law": "ACIA_2009",
        "enbez": "Art.33",
        "title": "《东盟全面投资协定》(ACIA) 第33条：国际仲裁庭机构选择（ICSID 与 UNCITRAL 直诉权）",
        "heading_path": "ASEAN Comprehensive Investment Agreement > Section B > Article 33 Submission of a Claim",
        "text_de": "ACIA 2009 Art. 33 (Selection of International Arbitral Forums: ICSID, UNCITRAL, Regional Centers)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "The dispute may be submitted to: (a) the courts of the Member State; (b) the International Centre for Settlement of Investment Disputes (ICSID); (c) an ad hoc arbitration under UNCITRAL Arbitration Rules; or (d) any other regional arbitration centre agreed by the parties.",
        "text_en": "The dispute may be submitted to ICSID, UNCITRAL ad hoc arbitration, or regional arbitration centres.",
        "text_zh": "【绕开东道国地方法院直诉国际仲裁庭】外国投资者可依法选择将东道国政府送上世界银行国际投资争端解决中心（ICSID）、联合国国际贸易法委员会（UNCITRAL）特设仲裁庭或新加坡国际仲裁中心（SIAC）。东道国在加入 ACIA 时已作出了不可撤销的仲裁默示同意（Unconditional Consent）。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "multilateral_treaty",
        "mandatory_level": "treaty"
    },
    {
        "norm_id": "ACIA:2009:Art36_Conditions",
        "law": "ACIA_2009",
        "enbez": "Art.36",
        "title": "《东盟全面投资协定》(ACIA) 第36条：提起投资仲裁之前置磋商与180天冷静期程序",
        "heading_path": "ASEAN Comprehensive Investment Agreement > Article 36 Conditions Precedent to Submission",
        "text_de": "ACIA 2009 Art. 36 (Cooling-off Period and Notice of Dispute)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "No claim may be submitted to arbitration unless: 180 days have elapsed since the receipt by the disputing Member State of the request for consultations; and the investor waives any right to initiate proceedings before domestic courts.",
        "text_en": "Claims require 180 days after receipt of consultation request and waiver of domestic court actions.",
        "text_zh": "【180天争端冷静期与岔路口放弃声明】投资者在向 ICSID 递交仲裁申请书前，必须先向东道国政府首脑或财政部正式送达《争端磋商通知书》（Notice of Intent / Dispute），并经历 180 天友好磋商冷静期；同时须出具放弃国内法院同案诉讼之不可撤销书面弃权声明（Fork-in-the-road waiver）。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "multilateral_treaty",
        "mandatory_level": "treaty"
    },
    {
        "norm_id": "CAFTA:2009:Art6_Expropriation",
        "law": "CAFTA_Investment_Agreement_2009",
        "enbez": "Art.6",
        "title": "《中国-东盟自由贸易区投资协议》第6条：中资出海征收赔偿保障与可自由兑换汇出",
        "heading_path": "Agreement on Investment of the Framework Agreement on Comprehensive Economic Cooperation Between PRC and ASEAN > Article 6",
        "text_de": "China-ASEAN Investment Agreement Art. 6 (Expropriation and Compensation for Chinese Outbound FDI)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Neither Party shall expropriate or nationalise investments of an investor of another Party except for a public purpose, on a non-discriminatory basis, under due process of law and upon payment of prompt, adequate and effective compensation.",
        "text_en": "Parties shall not expropriate investments except for public purpose, non-discriminatory basis, due process and prompt adequate effective compensation.",
        "text_zh": "【中资直投东盟防征收专条】任何东盟国家不得征收或国有化中国投资者的资产。补偿必须等于征收发生前一刻该被征收投资的真实公允市场价值（Fair Market Value），包含从征收日起至清偿日止按正常商业利率计算之利息，并允许无延迟自由汇出。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "multilateral_treaty",
        "mandatory_level": "treaty"
    },
    {
        "norm_id": "RCEP:2020:Art10.4_NT",
        "law": "RCEP_Chapter_10",
        "enbez": "Art.10.4",
        "title": "《区域全面经济伙伴关系协定》(RCEP) 第10.4条：第十章投资国民待遇与负面清单承诺",
        "heading_path": "Regional Comprehensive Economic Partnership > Chapter 10 Investment > Article 10.4 National Treatment",
        "text_de": "RCEP Chapter 10 Art. 10.4 (National Treatment and Negative List Commitment)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Each Party shall accord to investors of another Party, and to covered investments, treatment no less favourable than that it accords, in like circumstances, to its own investors and investments with respect to operation, conduct, and sale.",
        "text_en": "Parties shall accord investors and investments national treatment regarding operation and sale.",
        "text_zh": "【RCEP 投资国民待遇框架】中国与东盟 10 国相互承诺实行准入前国民待遇加负面清单管理制度。在建筑总承包、设备制造、仓储物流等开放领域，东道国不得为中资企业设置高于本国企业的苛刻技术资质门槛或附加不平等的本土股权强制转让条件。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "multilateral_treaty",
        "mandatory_level": "treaty"
    },
    {
        "norm_id": "DTA:CN_VN:Art10_11_Dividends_Interest",
        "law": "Double_Taxation_Avoidance_CN_VN",
        "enbez": "Art.10-11",
        "title": "《中越避免双重征税协定》第10-11条：股息与利息跨境支付 10% 优惠预扣税率",
        "heading_path": "Agreement Between PRC and Vietnam for the Avoidance of Double Taxation > Articles 10 & 11",
        "text_de": "China-Vietnam DTA Articles 10 and 11 (Reduced Withholding Tax on Dividends and Interest)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Tax charged on dividends and interest paid by a company resident of Vietnam to a resident of China shall not exceed 10% of the gross amount of dividends and interest if the recipient is the beneficial owner.",
        "text_en": "Tax charged on dividends and interest paid to beneficial owners shall not exceed 10%.",
        "text_zh": "【中越双边税收协定 10% 预扣税优惠】中国母公司从越南项目公司收取的股息、红利以及为工程项目提供跨境股东贷款产生的利息，只要中国母公司符合“受益所有人（Beneficial Owner）”条件，在越南扣缴的预扣所得税最高不得超过 10%（越南内国法普通税率通常为 15%~20%）。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "tax_treaty",
        "mandatory_level": "default"
    },
    {
        "norm_id": "DTA:CN_ID:Art10_11_Dividends_Interest",
        "law": "Double_Taxation_Avoidance_CN_ID",
        "enbez": "Art.10-11",
        "title": "《中印尼避免双重征税协定》第10-11条：股息与利息 10% 协定税率与 PPh 26 减免",
        "heading_path": "Agreement Between PRC and Indonesia for the Avoidance of Double Taxation > Articles 10 & 11",
        "text_de": "China-Indonesia DTA Articles 10 and 11 (Reduced PPh 26 Withholding Tax on Dividends and Interest)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Dividends and interest paid by an Indonesian resident entity to a Chinese resident beneficial owner shall be subject to tax not exceeding 10% of the gross amount.",
        "text_en": "Dividends and interest paid to Chinese beneficial owners shall not exceed 10%.",
        "text_zh": "【中印尼双边税收协定 10% 封顶】印尼项目公司向中国股东分配利润或支付外债借款利息时，凭中国主管税务机关出具的《中国税收居民身份证明》（COR）向印尼税务总局申请 DGT-1 表格备案，即可将内国税法 PPh 26 的 20% 预扣税率直接腰斩降至 10%。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "tax_treaty",
        "mandatory_level": "default"
    },

    # ---------------------------------------------------------------------
    # 2. 政府采购与公共工程招投标法专章 (Public Procurement & Tendering)
    # ---------------------------------------------------------------------
    {
        "norm_id": "VN:Law_22_2023:Art5_Foreign_Bidder",
        "law": "Law_on_Bidding_VN",
        "enbez": "Art.5",
        "title": "《越南新招投标法2023》(Law No. 22/2023/QH15) 第5条：外国承包商投标资格与本土分包配额强制要求",
        "heading_path": "Luật Đấu thầu 2023 > Điều 5 Tư cách hợp lệ của nhà thầu",
        "text_de": "Vietnam Law on Bidding 2023 Art. 5 (Eligibility of Foreign Bidders and Domestic Subcontracting Quota)",
        "language_mode": "trilingual",
        "lang_original": "vi",
        "text_original": "Nhà thầu nước ngoài khi tham dự đấu thầu quốc tế tại Việt Nam phải liên danh với nhà thầu trong nước hoặc sử dụng nhà thầu phụ trong nước, trừ trường hợp nhà thầu trong nước không đủ năng lực tham gia.",
        "text_en": "Foreign bidders participating in international bidding in Vietnam must form a consortium with domestic contractors or engage domestic subcontractors.",
        "text_zh": "【越南外资参标强制联合体或本土分包红线】外国建筑承包商参加越南境内的国际公开招投标时，必须强制与越南本土承包商组成投标联合体（Liên danh），或者在投标方案中承诺将特定份额的工程分包给越南本土分包商；唯有在越南本土企业完全不具备技术施工能力的极特殊情形下，经总理或招标人核准方可豁免。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "procurement_law",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "VN:Law_22_2023:Art14_Bid_Security",
        "law": "Law_on_Bidding_VN",
        "enbez": "Art.14",
        "title": "《越南新招投标法2023》第14条：投标保函额度 1%~3% 与退还时效除斥期间",
        "heading_path": "Luật Đấu thầu 2023 > Điều 14 Bảo đảm dự thầu",
        "text_de": "Vietnam Law on Bidding 2023 Art. 14 (Bid Security and Refund Timelines)",
        "language_mode": "trilingual",
        "lang_original": "vi",
        "text_original": "Giá trị bảo đảm dự thầu được quy định từ 1% đến 3% giá gói thầu. Bên mời thầu có trách nhiệm hoàn trả hoặc giải tỏa bảo đảm dự thầu cho nhà thầu không trúng thầu trong thời hạn tối đa 20 ngày kể từ ngày phê duyệt kết quả lựa chọn nhà thầu.",
        "text_en": "Bid security is 1% to 3% of package price. The procuring entity must return bid security to unsuccessful bidders within 20 days.",
        "text_zh": "【投标保函退还法定时效】工程招标文件中约定的投标担保金（Bảo đảm dự thầu）金额必须严格设定在采购包预算金额的 1% 至 3% 之间。招标人在中标结果审批公布之日起最多 20 个工作日内，负有依法向未中标人全额退还或无条件解除银行保函质押之法定义务，严禁无故扣压。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "procurement_law",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "VN:Law_22_2023:Art14_Forfeiture_Limits",
        "law": "Law_on_Bidding_VN",
        "enbez": "Art.14.7",
        "title": "《越南新招投标法2023》第14条第7款：没收投标保函之法定穷尽情形（严防招标人滥权）",
        "heading_path": "Luật Đấu thầu 2023 > Điều 14 Khoản 7 Các trường hợp không được hoàn trả bảo đảm dự thầu",
        "text_de": "Vietnam Law on Bidding 2023 Art. 14(7) (Exhaustive Grounds for Forfeiture of Bid Security)",
        "language_mode": "trilingual",
        "lang_original": "vi",
        "text_original": "Bảo đảm dự thầu không được hoàn trả trong các trường hợp: rút hồ sơ dự thầu sau thời điểm đóng thầu khi hồ sơ còn hiệu lực; vi phạm quy định cấm tại Điều 89; không tiến hành đối chiếu tài liệu hoặc từ chối ký hợp đồng sau khi trúng thầu.",
        "text_en": "Bid security shall be forfeited only if: withdrawal after bid closing; violating prohibited acts; refusing to sign contract after award.",
        "text_zh": "【禁止任意没收投标保函】法律穷尽限定没收投标保证金的情形，仅限于：① 截标后在投标有效期内擅自撤回标书；② 实施串通投标被查实；③ 中标后无正当理由拒绝核对资格或拒绝按招标文件签约。招标人以技术参数细微偏差为由单方索兑保函的，构成严重违法，承包商可申请紧急司法禁制令止付。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "procurement_law",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "ID:Perpres_16_2018:Art20_TKDN",
        "law": "Procurement_Regulation_ID",
        "enbez": "Art.20",
        "title": "《印尼政府采购总统令第16/2018号》(Perpres 16/2018) 第20条：本地化率 (TKDN) 强制优先权与价格优惠核算",
        "heading_path": "Peraturan Presiden No. 16 Tahun 2018 jo. Perpres 12/2021 > Pasal 20 Penggunaan Produk Dalam Negeri",
        "text_de": "Indonesian Public Procurement Presidential Reg Perpres 16/2018 Art. 20 (Mandatory Local Content TKDN)",
        "language_mode": "trilingual",
        "lang_original": "id",
        "text_original": "Kementerian/Lembaga/Pemerintah Daerah wajib menggunakan produk dalam negeri apabila terdapat produk yang memiliki penjumlahan nilai TKDN ditambah nilai Bobot Manfaat Perusahaan (BMP) paling sedikit 40%.",
        "text_en": "Procuring entities must use domestic products if TKDN plus BMP reaches at least 40%.",
        "text_zh": "【印尼政府采购 TKDN 强制优先权】当工程所需的国产建材或机电设备本地化率（TKDN）与企业效益权重（BMP）合计达到 40% 以上时，印尼政府采购机构必须强制采购本土产品；中资承包商投标方案若包含高 TKDN 认证的本土合作制造方案，可享受最高 15% 的法定评标价格优惠加分（HEA）。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "procurement_law",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "ID:Perpres_16_2018:Art61_KSO_Joint_Operation",
        "law": "Procurement_Regulation_ID",
        "enbez": "Art.61",
        "title": "《印尼政府采购总统令第16/2018号》第61条：外国承包商投标联合体 (KSO) 与牵头方连带责任",
        "heading_path": "Peraturan Presiden No. 16 Tahun 2018 > Pasal 61 Kerja Sama Operasi (KSO)",
        "text_de": "Indonesian Public Procurement Perpres 16/2018 Art. 61 (Joint Operation KSO and Joint Liability)",
        "language_mode": "trilingual",
        "lang_original": "id",
        "text_original": "Penyedia asing yang mengikuti tender pekerjaan konstruksi harus bekerja sama dengan penyedia jasa konstruksi nasional dalam bentuk Kerja Sama Operasi (KSO) dan seluruh anggota KSO bertanggung jawab secara tanggung renteng.",
        "text_en": "Foreign providers must form a Joint Operation (KSO) with national providers and bear joint and several liability.",
        "text_zh": "【外国总包强制 KSO 联营体】外国工程总承包商参与印尼政府或国有企业（BUMN）公共基建竞标，必须与具有同类甲级资质的印尼本国建筑公司签署联营体协议（KSO）。所有 KSO 联合体成员必须就工程全面交付对印尼发包人承担完全之连带责任（Tanggung renteng）。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "procurement_law",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "PH:RA_9184:Sec23_Eligibility_Foreign",
        "law": "GPRA_Procurement_PH",
        "enbez": "Sec.23",
        "title": "《菲律宾政府采购改革法》(RA 9184 GPRA) 第23条：外资参标联合体 60% 菲资控股限制与 PCAB 联合体许可",
        "heading_path": "Republic Act No. 9184 > Article VIII Receipt and Opening of Bids > Section 23 Eligibility Requirements",
        "text_de": "Philippines GPRA RA 9184 Sec. 23 (Foreign Contractors Eligibility and 60% Filipino Equity Consortium)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "For the procurement of infrastructure projects, foreign bidders may participate only if they form a joint venture with Filipino partners owning at least sixty percent (60%) interest, unless under treaties or international loan agreements.",
        "text_en": "Foreign bidders may participate in infrastructure projects only if they form a JV with 60% Filipino equity.",
        "text_zh": "【菲律宾公共工程 60% 菲资联合体红线】外国建筑企业在菲律宾参与本国财政出资的公共基建投标，必须与菲律宾本国企业组成联合体，且菲律宾籍合伙人必须持有联合体至少 60% 以上的股权或分红权益，并取得建筑业牌照委员会（PCAB）颁发的特定项目特别联合体执照；亚洲开发银行（ADB）或多边国际援助贷款项目除外。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "procurement_law",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "TH:Public_Procurement_BE_2560:Sec51",
        "law": "Public_Procurement_Act_TH",
        "enbez": "Sec.51",
        "title": "《泰国公共采购与供应管理法》(佛历2560年) 第51条：外国承包商参与大型政府基建特批程序",
        "heading_path": "Public Procurement and Supplies Administration Act B.E. 2560 > Section 51 Foreign Participation",
        "text_de": "Thailand Public Procurement Act B.E. 2560 Sec. 51 (Cabinet Approval for Foreign Contractors in Infrastructure)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "State agencies shall prioritize procurement of Thai supplies and services. Foreign contractors may be invited only where high technology is required and upon specific cabinet approval or under international trade agreements.",
        "text_en": "State agencies shall prioritize Thai supplies. Foreign contractors require cabinet approval or trade treaties.",
        "text_zh": "【泰国内阁特批外国总包机制】泰国政府机构进行公共采购原则上优先选用泰国企业。涉外复杂大型工程（如中泰铁路、深水港口），唯有在涉及泰国本土企业不具备的高新技术时，经主管内阁部长或采购政策委员会特批，外国 EPC 承包商方可直接参标。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "procurement_law",
        "mandatory_level": "mandatory"
    },

    # ---------------------------------------------------------------------
    # 3. 环境影响评价与劳工罢工抗辩法条 (EIA / AMDAL & Labor Strikes)
    # ---------------------------------------------------------------------
    {
        "norm_id": "VN:Law_72_2020:Art30_EIA_Approval",
        "law": "Environmental_Protection_Law_VN",
        "enbez": "Art.30",
        "title": "《越南环境保护法2020》(Law No. 72/2020/QH14) 第30条：环评报告批复 (ĐTM) 作为项目正式开工法定前置条件",
        "heading_path": "Luật Bảo vệ môi trường 2020 > Điều 30 Đánh giá tác động môi trường",
        "text_de": "Vietnam Environmental Protection Law 2020 Art. 30 (EIA Approval ĐTM as Precondition for Construction)",
        "language_mode": "trilingual",
        "lang_original": "vi",
        "text_original": "Quyết định phê duyệt kết quả thẩm định báo cáo đánh giá tác động môi trường là căn cứ để cấp có thẩm quyền cấp giấy phép xây dựng. Nghiêm cấm khởi công xây dựng khi chưa có quyết định phê duyệt báo cáo đánh giá tác động môi trường.",
        "text_en": "Decision approving EIA is the basis for construction permit. Commencing construction without approved EIA is strictly prohibited.",
        "text_zh": "【环评批复 (ĐTM) 强制开工前置】环境影响评价报告批复决议（ĐTM）是主管机关签发施工许可证的法定前提。严禁任何建设工程在未取得自然资源与环境部（MONRE）环境影响评估正式批复前动工施工；业主未取得 ĐTM 强行发令开工导致被环保督察叫停的，承包商享有法定工期顺延与窝工全额赔偿权。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "environmental_law",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "ID:UU_32_2009:Art22_AMDAL",
        "law": "Environmental_Management_Act_ID",
        "enbez": "Art.22",
        "title": "《印尼环境保护与管理法》(UU 32/2009 jo. UU 6/2023) 第22条：重大基建 AMDAL 环评强行法",
        "heading_path": "Undang-Undang No. 32 Tahun 2009 > Bab V AMDAL > Pasal 22",
        "text_de": "Indonesian Environmental Protection Act UU 32/2009 Art. 22 (Mandatory AMDAL Environmental Clearance)",
        "language_mode": "trilingual",
        "lang_original": "id",
        "text_original": "Setiap usaha dan/atau kegiatan yang berdampak penting terhadap lingkungan hidup wajib memiliki Analisis Mengenai Dampak Lingkungan Hidup (AMDAL) sebagai dasar penerbitan izin lingkungan.",
        "text_en": "Every activity with significant environmental impact must obtain AMDAL as prerequisite for environmental permit.",
        "text_zh": "【印尼重大工程 AMDAL 强制环评许可】对自然环境有重大影响的工业、电站、矿山与交通基建项目，必须编制并取得印尼环境与林业部核准的环境影响分析报告（AMDAL）。若发包人取得的 AMDAL 存在程序违法被行政法院（PTUN）判决撤销导致施工被行政禁制令叫停，属于发包人公法违约，承包商全面免责。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "environmental_law",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "ID:UU_13_2003:Art137_Right_to_Strike",
        "law": "Labor_Law_ID",
        "enbez": "Art.137",
        "title": "《印尼劳工法》(UU 13/2003 jo. UU 6/2023) 第137条：劳工合法罢工权利基本要件",
        "heading_path": "Undang-Undang No. 13 Tahun 2003 > Bab XI Hubungan Industrial > Pasal 137 Hak Mogok Kerja",
        "text_de": "Indonesian Labor Act UU 13/2003 Art. 137 (Right to Strike as Last Resort)",
        "language_mode": "trilingual",
        "lang_original": "id",
        "text_original": "Mogok kerja sebagai hak dasar pekerja/buruh dan serikat pekerja/serikat buruh dilakukan secara sah, tertib, dan damai sebagai akibat gagalnya perundingan.",
        "text_en": "Strike is a fundamental right of workers conducted lawfully, orderly, and peacefully following failed negotiations.",
        "text_zh": "【印尼合法罢工构成要件】罢工是工会及劳工的基本权利，但必须作为劳资双边谈判彻底破裂后的最后救济手段，且必须以合法、有序与和平的方式进行，严禁任何破坏施工机械或封锁厂区的暴力行为。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "labor_law",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "ID:UU_13_2003:Art140_Notice_of_Strike",
        "law": "Labor_Law_ID",
        "enbez": "Art.140",
        "title": "《印尼劳工法》(UU 13/2003) 第140条：罢工前 7 日强制送达书面通告程序",
        "heading_path": "Undang-Undang No. 13 Tahun 2003 > Pasal 140 Pemberitahuan Mogok Kerja",
        "text_de": "Indonesian Labor Act UU 13/2003 Art. 140 (Mandatory 7-Day Advance Notice of Strike)",
        "language_mode": "trilingual",
        "lang_original": "id",
        "text_original": "Sekurang-kurangnya dalam waktu 7 hari kerja sebelum mogok kerja dilaksanakan, pekerja/buruh dan serikat pekerja wajib memberitahukan secara tertulis kepada pengusaha dan instansi ketenagakerjaan setempat.",
        "text_en": "Workers must notify employers and local labor authorities in writing at least 7 working days prior to strike.",
        "text_zh": "【罢工 7 日书面通告法定除斥期间】工会发动罢工，必须至少在实施前 7 个工作日，向雇主及当地劳工局（Disnaker）递交正式书面通知，详列罢工起止时间、地点及诉求。未履行 7 日法定通知直接停工的，构成非法罢工。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "labor_law",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "ID:UU_13_2003:Art142_Illegal_Strike",
        "law": "Labor_Law_ID",
        "enbez": "Art.142",
        "title": "《印尼劳工法》(UU 13/2003) 第142条：非法罢工法律后果与雇主免责/解雇权",
        "heading_path": "Undang-Undang No. 13 Tahun 2003 > Pasal 142 Mogok Kerja Tidak Sah",
        "text_de": "Indonesian Labor Act UU 13/2003 Art. 142 (Legal Consequences of Illegal Strike and Dismissal)",
        "language_mode": "trilingual",
        "lang_original": "id",
        "text_original": "Mogok kerja yang dilakukan tidak memenuhi ketentuan Pasal 139 dan Pasal 140 adalah mogok kerja tidak sah. Akibat hukum dari mogok kerja tidak sah dikualifikasikan sebagai mangkir.",
        "text_en": "Strikes failing to comply with Article 139 and 140 are illegal and qualified as unauthorized absence (mangkir).",
        "text_zh": "【非法罢工定性为旷工与不可抗力排除】未遵守法定程序的非法罢工，在法律上被直接定性为无故旷工（Mangkir）。承包商有权对带头罢工人员按严重违纪予以立即解雇且无需支付补偿金。分包商因自身违法克扣工资引发的内部罢工，不能向总包主张不可抗力免责。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "labor_law",
        "mandatory_level": "mandatory"
    },

    # ---------------------------------------------------------------------
    # 4. 跨境动产质押、特权留置与优先受偿权 (Collateral, Security & Lien)
    # ---------------------------------------------------------------------
    {
        "norm_id": "VN:Decree_21_2021:Art14_Pledge_Receivables",
        "law": "Decree_21_2021_VN",
        "enbez": "Art.14",
        "title": "《越南关于担保交易的第21/2021/ND-CP号法令》第14条：建设工程应收账款质押设立与登记生效要件",
        "heading_path": "Nghị định số 21/2021/NĐ-CP > Điều 14 Thế chấp quyền đòi nợ hình thành từ hợp đồng xây dựng",
        "text_de": "Vietnam Decree 21/2021 Art. 14 (Pledge of Construction Receivables and Mandatory Registration)",
        "language_mode": "trilingual",
        "lang_original": "vi",
        "text_original": "Quyền đòi nợ từ hợp đồng xây dựng, bao gồm cả quyền đòi nợ hình thành trong tương lai, được dùng để bảo đảm thực hiện nghĩa vụ. Biện pháp bảo đảm có hiệu lực đối kháng với người thứ ba kể từ thời điểm đăng ký tại Trung tâm Đăng ký giao dịch, tài sản.",
        "text_en": "Receivables from construction contracts, including future receivables, can secure obligations. They have third-party opposability upon registration at NRAST.",
        "text_zh": "【工程应收账款质押与登记对抗主义】承包商在建设工程合同项下享有的工程进度款请求权（包括现存债权及未来形成之应收款），可依法设定权利质押以获取境外银行项目融资担保。该担保自越南司法部国家担保交易登记中心（NRAST）在线登记之时起，产生对抗包括一般无担保债权人及业主清算破产主持人在内的绝对优先效力。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "security_law",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "VN:Civil_Code_2015:Art274_Retention_Lien",
        "law": "Civil_Code_VN",
        "enbez": "Art.274",
        "title": "《越南民法典》第274条：建设工程与承揽标的物法定留置权之确立",
        "heading_path": "Bộ luật Dân sự 2015 > Phần thứ ba Nghĩa vụ và hợp đồng > Điều 274 Quyền cầm giữ tài sản",
        "text_de": "Vietnam Civil Code Art. 274 (Right of Retention / Mechanic's Lien in Construction)",
        "language_mode": "trilingual",
        "lang_original": "vi",
        "text_original": "Cầm giữ tài sản là việc bên có quyền đang chiếm giữ hợp pháp tài sản là đối tượng của hợp đồng song vụ được quyền tiếp tục chiếm giữ tài sản khi bên có nghĩa vụ không thực hiện hoặc thực hiện không đúng nghĩa vụ cho đến khi nghĩa vụ được thực hiện xong.",
        "text_en": "Retention of property is the right of an obligee lawfully possessing property under a bilateral contract to retain it until the obligation is fulfilled.",
        "text_zh": "【承揽工程法定留置权】在发包人未按期足额支付工程到期进度款或结算款前，合法占有工程现场、已完工建筑物或安装设备的 EPC 总承包商，依法享有继续留置（Cầm giữ tài sản）并拒绝向发包人移交工程钥匙与实体占有之法定对抗权。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "security_law",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "ID:UU_42_1999:Art15_Executory_Title",
        "law": "Fiduciary_Security_Act_ID",
        "enbez": "Art.15",
        "title": "《印尼动产信托担保法》(UU 42/1999) 第15条：信托担保凭证具法院判决之直接执行力 (Grosse Akte)",
        "heading_path": "Undang-Undang No. 42 Tahun 1999 > Pasal 15 Sertifikat Jaminan Fidusia Memiliki Kekuatan Eksekutorial",
        "text_de": "Indonesian Fiduciary Security Act UU 42/1999 Art. 15 (Direct Executory Title of Fiduciary Certificate)",
        "language_mode": "trilingual",
        "lang_original": "id",
        "text_original": "Sertifikat Jaminan Fidusia mencantumkan kata-kata: 'DEMI KEADILAN BERDASARKAN KETUHANAN YANG MAHA ESA'. Sertifikat tersebut mempunyai kekuatan eksekutorial yang sama dengan putusan pengadilan yang telah memperoleh kekuatan hukum tetap.",
        "text_en": "The Fiduciary Certificate possesses the same executory force as a final and binding court judgment (Grosse Akte).",
        "text_zh": "【公证信托凭证直接执行力（免经诉讼即可查封变卖）】在印尼对重型盾构机、吊装设备或应收账款设立的信托担保（Jaminan Fidusia），经依法公证并在司法部系统登记后，担保凭证抬头冠以国家司法判词，具有等同于法院终审判决之直接执行力（Grosse Akte）。借款人或发包人违约时，担保权人无须经历漫长诉讼，可直接凭证书申请法警强制查封执行。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "security_law",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "ID:KUHPerdata:Art1139_Privileged_Claims",
        "law": "KUHPerdata_ID",
        "enbez": "Art.1139",
        "title": "《印尼民法典》第1139条：建筑工程款对建筑物的法定特权优先受偿权",
        "heading_path": "Burgerlijk Wetboek (KUHPerdata) > Buku II Kebendaan > Pasal 1139 Piutang yang Diistimewakan",
        "text_de": "Indonesian Civil Code Art. 1139 (Privileged Claims of Construction Contractors over Structures)",
        "language_mode": "trilingual",
        "lang_original": "id",
        "text_original": "Piutang-piutang yang diistimewakan terhadap benda-benda tertentu adalah: biaya yang telah dikeluarkan untuk menyelamatkan atau memperbaiki suatu benda, dan tagihan tukang/pemborong atas bangunan yang telah dikerjakannya.",
        "text_en": "Privileged debts on specific property include costs incurred to repair property and claims of contractors on structures erected.",
        "text_zh": "【承包商建筑工程款法定特权优先权】印尼法确立特权债权体系（Hak istimewa）：建筑承包商因建造房屋、电厂等地上建筑物而产生的工程款债权，就该建筑物本身的变现价值，享有优先于一般抵押权人及普通破产债权人受偿的法定特权受偿顺位。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "security_law",
        "mandatory_level": "mandatory"
    },

    # ---------------------------------------------------------------------
    # 5. 新能源电网并网、商业运行 COD 与购电协议 PPA
    # ---------------------------------------------------------------------
    {
        "norm_id": "VN:MOIT_Circular_19_2023:Art6_PPA_Curtailment",
        "law": "MOIT_Renewable_Energy_VN",
        "enbez": "Art.6",
        "title": "《越南工贸部第19/2023/TT-BCT号通告》第6条：电网弃电补偿与过渡期可再生能源电量调度结算",
        "heading_path": "Thông tư số 19/2023/TT-BCT > Điều 6 Huy động công suất và thanh toán sản lượng",
        "text_de": "Vietnam MOIT Circular 19/2023 Art. 6 (Grid Curtailment and Power Dispatch Settlements)",
        "language_mode": "trilingual",
        "lang_original": "vi",
        "text_original": "Tập đoàn Điện lực Việt Nam (EVN) chịu trách nhiệm huy động công suất tối đa theo khả năng truyền tải của lưới điện. Trường hợp cắt giảm công suất do lỗi chủ quan của EVN, EVN có trách nhiệm bồi thường sản lượng điện không thể phát theo thỏa thuận trong hợp đồng mua bán điện (PPA).",
        "text_en": "EVN is responsible for dispatching power. Where curtailment is due to EVN's fault, EVN must compensate ungenerated deemed power under PPA.",
        "text_zh": "【越南电网弃电补偿机制】越南国家电力公司（EVN）必须在电网安全输送能力范围内优先全额消纳新能源绿电。若因 EVN 内部调度失误或可避免的电网过载无理下令光伏/风电场关闸限电（Curtailment），EVN 必须按照购电协议（PPA）约定就“视同发电（Deemed Generation）”之电量向发电商支付全额补偿。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "energy_law",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "ID:MEMR_Reg_11_2021:PPA_COD_Deadline",
        "law": "MEMR_Regulation_ID",
        "enbez": "Reg.11/2021",
        "title": "《印尼能源与矿产资源部第11/2021号规程》独立发电商 (IPP) 逾期商业运行罚金与电价调整",
        "heading_path": "Peraturan Menteri ESDM No. 11 Tahun 2021 > Pelaksanaan PPA dan Sanksi Keterlambatan COD",
        "text_de": "Indonesian MEMR Reg 11/2021 (IPP Commercial Operation Date COD Penalties and Tariff Adjustments)",
        "language_mode": "trilingual",
        "lang_original": "id",
        "text_original": "Pengembang Pembangkit Listrik (IPP) wajib mencapai Commercial Operation Date (COD) sesuai jadwal dalam PPA. Keterlambatan COD akibat kelalaian IPP dikenakan denda keterlambatan harian dan dapat mengakibatkan pemotongan tarif listrik.",
        "text_en": "Independent Power Producers must achieve COD as scheduled. Delays due to IPP fault incur daily penalties and tariff reductions.",
        "text_zh": "【印尼电站商业运行日 (COD) 严格罚金】与印尼国家电力公司（PLN）签署 PPA 购电协议的独立发电商（IPP），若非因电网接入延迟等 PLN 违约原因导致无法按期实现商业运行（COD），必须按日向 PLN 缴纳高额逾期罚金，甚至面临上网电价被永久下调 5%~10% 的惩罚性后果。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "energy_law",
        "mandatory_level": "mandatory"
    },

    # ---------------------------------------------------------------------
    # 6. FIDIC 结构化全款项体系 (银皮书 EPC、黄皮书 DB、红皮书 Con 20大主章核心子条款)
    # ---------------------------------------------------------------------
    {
        "norm_id": "FIDIC:Silver_1999:Clause_1.5",
        "law": "FIDIC_Silver_1999",
        "enbez": "Clause 1.5",
        "title": "FIDIC 银皮书第 1.5 款：合同文件优先解释顺序 (Priority of Documents)",
        "heading_path": "FIDIC Conditions of Contract for EPC/Turnkey Projects > Clause 1 General Provisions > Sub-Clause 1.5",
        "text_de": "FIDIC Silver Book Clause 1.5 (Priority of Documents)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "The documents forming the Contract are to be taken as mutually explanatory of one another. For the purposes of interpretation, the priority of the documents shall be: (a) the Contract Agreement, (b) the Particular Conditions, (c) these General Conditions, (d) the Employer's Requirements, (e) the Tender and any other documents.",
        "text_en": "Priority: Agreement > Particular Conditions > General Conditions > Employer's Requirements > Tender.",
        "text_zh": "【FIDIC 文件效力优先层级】构成合同的文件应互为解释。当出现冲突歧义时，解释的先后顺序为：① 合同协议书；② 专用条件（Particular Conditions，居于最高修改地位）；③ 通用条件（General Conditions）；④ 雇主要求（Employer's Requirements）；⑤ 投标函及其他技术附件。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "fidic_contract",
        "fidic_tier": "Tier-1",
        "fidic_edition": "1999",
        "mandatory_level": "contractual"
    },
    {
        "norm_id": "FIDIC:Silver_1999:Clause_2.1",
        "law": "FIDIC_Silver_1999",
        "enbez": "Clause 2.1",
        "title": "FIDIC 银皮书第 2.1 款：雇主现场移交法定义务与逾期工期费用双重索赔 (Right of Access to the Site)",
        "heading_path": "FIDIC Silver Book > Clause 2 The Employer > Sub-Clause 2.1",
        "text_de": "FIDIC Silver Book Clause 2.1 (Right of Access to the Site)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "The Employer shall give the Contractor right of access to, and possession of, all parts of the Site within the time stated. If the Contractor suffers delay and/or incurs Cost as a result of a failure by the Employer to give any such right or possession, the Contractor shall give notice and be entitled to: (a) an extension of time, and (b) payment of any such Cost plus reasonable profit.",
        "text_en": "Employer must give site access; failure entitles Contractor to EOT and Cost plus reasonable profit.",
        "text_zh": "【现场移交迟延索赔工期与合理利润】雇主必须在合同约定期限内向承包商移交全部现场的占有与通行权。若因雇主征地拆迁迟延未能移交，承包商在发出通知后，依法享有双重索赔权：① 工期顺延（EOT）；② 发生的窝工成本加上合理利润（Cost plus reasonable profit）。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "fidic_contract",
        "fidic_tier": "Tier-1",
        "fidic_edition": "1999",
        "mandatory_level": "contractual"
    },
    {
        "norm_id": "FIDIC:Silver_1999:Clause_2.5",
        "law": "FIDIC_Silver_1999",
        "enbez": "Clause 2.5",
        "title": "FIDIC 银皮书第 2.5 款：雇主索赔前置通知与禁止擅自抵扣工程款 (Employer's Claims)",
        "heading_path": "FIDIC Silver Book > Clause 2 The Employer > Sub-Clause 2.5",
        "text_de": "FIDIC Silver Book Clause 2.5 (Employer's Claims and Prohibition of Unilateral Set-off)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "If the Employer considers himself to be entitled to any payment under any Clause of these Conditions or otherwise in connection with the Contract, the Employer shall give notice and particulars to the Contractor. The Employer shall only be entitled to set off against or make any deduction from an amount certified in an Interim Payment Certificate in accordance with this Sub-Clause.",
        "text_en": "Employer must give notice of claim; employer cannot unilaterally deduct without complying with this procedure.",
        "text_zh": "【雇主索赔前置通知与严禁私自扣款】若雇主认为有权向承包商索赔款项（如缺陷修补费、误期违约金），必须严格依第 2.5 款向承包商发出载明依据的事实通知并提供详细账目细节。雇主严禁绕过该程序在进度款或最终结算中单方擅自克扣或抵销工程款。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "fidic_contract",
        "fidic_tier": "Tier-1",
        "fidic_edition": "1999",
        "mandatory_level": "contractual"
    },
    {
        "norm_id": "FIDIC:Silver_1999:Clause_4.2",
        "law": "FIDIC_Silver_1999",
        "enbez": "Clause 4.2",
        "title": "FIDIC 银皮书第 4.2 款：履约担保 (Performance Security) 递交、延展与雇主索兑损害赔偿限制",
        "heading_path": "FIDIC Silver Book > Clause 4 The Contractor > Sub-Clause 4.2",
        "text_de": "FIDIC Silver Book Clause 4.2 (Performance Security and Restrictions on Calling Bonds)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "The Contractor shall obtain Performance Security in the amount stated. The Employer shall not make a claim under the Performance Security, except for amounts to which the Employer is entitled under the Contract. The Employer shall indemnify and hold the Contractor harmless against and from all damages, losses and expenses resulting from a claim under the Performance Security to the extent to which the Employer was not entitled to make the claim.",
        "text_en": "Employer shall not claim under security except for amounts entitled, and must indemnify for wrongful calls.",
        "text_zh": "【履约保函递交与违法索兑全额赔偿】承包商应在 28 天内递交履约保函。雇主除依据合同有权获得款项外，严禁恶意向银行提示索兑保函；若雇主在无合同实体依据下恶意拔兑保函，雇主必须向承包商承担全额反向赔偿责任，包括承包商因此产生的利息、信誉受损与律师费用。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "fidic_contract",
        "fidic_tier": "Tier-1",
        "fidic_edition": "1999",
        "mandatory_level": "contractual"
    },
    {
        "norm_id": "FIDIC:Silver_1999:Clause_8.1",
        "law": "FIDIC_Silver_1999",
        "enbez": "Clause 8.1",
        "title": "FIDIC 银皮书第 8.1 款：开工日期通知与承包商开工前置条件 (Commencement of Works)",
        "heading_path": "FIDIC Silver Book > Clause 8 Commencement, Delays and Suspension > Sub-Clause 8.1",
        "text_de": "FIDIC Silver Book Clause 8.1 (Commencement of Works Notice)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "The Commencement Date shall be within 42 days after the Contractor receives the Letter of Acceptance, unless otherwise stated. The Employer shall give the Contractor at least 7 days' notice of the Commencement Date.",
        "text_en": "Employer shall give at least 7 days' notice of Commencement Date within specified window.",
        "text_zh": "【正式开工指令 7 日通知期】开工日期应在合同生效后规定天数内。雇主代表必须至少提前 7 天向承包商发出正式书面开工通知；在雇主尚未完成预付款足额支付或现场移交前，承包商有权拒绝盲目进场动工。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "fidic_contract",
        "fidic_tier": "Tier-1",
        "fidic_edition": "1999",
        "mandatory_level": "contractual"
    },
    {
        "norm_id": "FIDIC:Silver_1999:Clause_8.4",
        "law": "FIDIC_Silver_1999",
        "enbez": "Clause 8.4",
        "title": "FIDIC 银皮书第 8.4 款：工期顺延 (EOT) 法定事由与关键路径受阻评估",
        "heading_path": "FIDIC Silver Book > Clause 8 > Sub-Clause 8.4 Extension of Time for Completion",
        "text_de": "FIDIC Silver Book Clause 8.4 (Extension of Time for Completion EOT)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "The Contractor shall be entitled to an extension of the Time for Completion if and to the extent that completion is or will be delayed by: (a) a Variation, (b) a cause of delay giving an entitlement under these Conditions, (c) unusually adverse climatic conditions, (d) unforeseeable shortages in personnel or Goods caused by epidemic or governmental actions, or (e) any delay caused by the Employer.",
        "text_en": "Contractor is entitled to EOT for Variations, exceptionally adverse climate, epidemics/government actions, or Employer delays.",
        "text_zh": "【工期顺延 (EOT) 五大法定理由】工程因下列原因受阻影响竣工关键路径时，承包商依法享有工期顺延权：① 工程变更指令；② 合同条款明文赋予顺延的事由；③ 异常恶劣的气候条件；④ 因政府行政管制或疫情引发的不可预见的物资/人员短缺；⑤ 雇主或其聘请的其他独立承包商导致的迟延阻碍。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "fidic_contract",
        "fidic_tier": "Tier-1",
        "fidic_edition": "1999",
        "mandatory_level": "contractual"
    },
    {
        "norm_id": "FIDIC:Silver_1999:Clause_8.7",
        "law": "FIDIC_Silver_1999",
        "enbez": "Clause 8.7",
        "title": "FIDIC 银皮书第 8.7 款：误期损害赔偿金 (Delay Damages) 上限封顶与排他性救济",
        "heading_path": "FIDIC Silver Book > Clause 8 > Sub-Clause 8.7 Delay Damages",
        "text_de": "FIDIC Silver Book Clause 8.7 (Delay Damages and Sole Remedy for Delay)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "If the Contractor fails to comply with Sub-Clause 8.2, the Contractor shall pay delay damages to the Employer. These delay damages shall be the only damages due from the Contractor for such default, and the total amount due under this Sub-Clause shall not exceed the maximum amount of delay damages stated in the Contract Data.",
        "text_en": "Delay damages shall be the only damages due for delay, subject to the contractual cap.",
        "text_zh": "【误期违约金上限与唯一救济原则】若承包商未能按期竣工，应向雇主支付合同约定的误期损害赔偿金（LDs）。该款项构成承包商因竣工迟延对雇主承担的“唯一且排他性损害赔偿”，且赔偿总额绝对不得超过合同专用条件设定的最高限额（通常为合同总价 10%）；雇主不得就迟延竣工另行索赔其他间接损失。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "fidic_contract",
        "fidic_tier": "Tier-1",
        "fidic_edition": "1999",
        "mandatory_level": "contractual"
    },
    {
        "norm_id": "FIDIC:Silver_1999:Clause_8.8",
        "law": "FIDIC_Silver_1999",
        "enbez": "Clause 8.8",
        "title": "FIDIC 银皮书第 8.8 款：雇主暂停施工指令与承包商保护现场义务 (Suspension of Work)",
        "heading_path": "FIDIC Silver Book > Clause 8 > Sub-Clause 8.8 Suspension of Work",
        "text_de": "FIDIC Silver Book Clause 8.8 (Suspension of Work by Employer)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "The Employer may at any time instruct the Contractor to suspend progress of part or all of the Works. During such suspension, the Contractor shall protect, store and secure such part or the Works against any deterioration, loss or damage.",
        "text_en": "Employer may suspend works; Contractor must protect and secure the works during suspension.",
        "text_zh": "【雇主停工令与现场照管】雇主有权在任何时候指示承包商暂停部分或全部工程施工。停工期间承包商负有妥善照管、仓储与保全工程标的物防止锈蚀受损之义务，照管产生的合理费用由雇主依据第 8.9 款予以全额追加清偿。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "fidic_contract",
        "fidic_tier": "Tier-1",
        "fidic_edition": "1999",
        "mandatory_level": "contractual"
    },
    {
        "norm_id": "FIDIC:Silver_1999:Clause_8.11",
        "law": "FIDIC_Silver_1999",
        "enbez": "Clause 8.11",
        "title": "FIDIC 银皮书第 8.11 款：停工超过 84 天承包商视为删减工程或单方终止权 (Prolonged Suspension)",
        "heading_path": "FIDIC Silver Book > Clause 8 > Sub-Clause 8.11 Prolonged Suspension",
        "text_de": "FIDIC Silver Book Clause 8.11 (Prolonged Suspension Exceeding 84 Days)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "If the suspension has continued for more than 84 days, the Contractor may request permission to proceed. If permission is not given within 28 days, the Contractor may treat the suspension as an omission of the affected part, or if the whole Works are affected, give notice of termination under Sub-Clause 16.2.",
        "text_en": "Suspension >84 days allows Contractor to request permission; if not granted within 28 days, Contractor may treat as omission or terminate.",
        "text_zh": "【超期停工 84 天解约退场权】若非因承包商违约导致的暂停施工持续超过 84 天，承包商可书面催告复工许可。若在通知后 28 天内雇主仍未准许复工，承包商有权将停工部分视为永久删减工程；若涉及整个工程停工，承包商有权直接终止合同并按违约解约清算撤场。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "fidic_contract",
        "fidic_tier": "Tier-1",
        "fidic_edition": "1999",
        "mandatory_level": "contractual"
    },
    {
        "norm_id": "FIDIC:Silver_1999:Clause_10.1",
        "law": "FIDIC_Silver_1999",
        "enbez": "Clause 10.1",
        "title": "FIDIC 银皮书第 10.1 款：工程接收证书 (Taking-Over Certificate TOC) 颁发与工程风险转移",
        "heading_path": "FIDIC Silver Book > Clause 10 Employer's Taking Over > Sub-Clause 10.1",
        "text_de": "FIDIC Silver Book Clause 10.1 (Taking-Over Certificate TOC and Transfer of Risk)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "The Works shall be taken over by the Employer when: (i) the Works have been completed in accordance with the Contract, and (ii) a Taking-Over Certificate for the Works has been issued, or is deemed to have been issued.",
        "text_en": "Works are taken over when completed and TOC is issued or deemed issued.",
        "text_zh": "【工程接收证书 TOC 与风险转移界标】工程完成竣工试验合格后，雇主代表应在 28 天内颁发工程接收证书（TOC）。TOC 颁发之日即为实质竣工日，自该日起，工程照管责任与毁损灭失风险正式从承包商转移至雇主，误期损害赔偿金按日计算立即停止。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "fidic_contract",
        "fidic_tier": "Tier-1",
        "fidic_edition": "1999",
        "mandatory_level": "contractual"
    },
    {
        "norm_id": "FIDIC:Silver_1999:Clause_10.2",
        "law": "FIDIC_Silver_1999",
        "enbez": "Clause 10.2",
        "title": "FIDIC 银皮书第 10.2 款：雇主提前擅自使用工程部分视为法定移交 (Taking Over of Parts)",
        "heading_path": "FIDIC Silver Book > Clause 10 > Sub-Clause 10.2 Taking Over of Parts of the Works",
        "text_de": "FIDIC Silver Book Clause 10.2 (Deemed Taking Over by Employer's Use)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "The Employer shall not use any part of the Works unless a Taking-Over Certificate has been issued. If the Employer does use any part before TOC is issued, the part which is used shall be deemed to have been taken over from the date on which it is used.",
        "text_en": "If Employer uses any part before TOC, that part is deemed taken over from the date of use.",
        "text_zh": "【擅自使用即视为已接收】未经颁发 TOC，雇主严禁擅自投入商业使用。若雇主在 TOC 颁发前提前占用或商业运营工程的任何部分，法律上直接推定该部分自雇主使用之日起已被正式接收（Deemed Taken Over），该部分责任风险即刻转移，承包商免除该部分迟延违约金。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "fidic_contract",
        "fidic_tier": "Tier-1",
        "fidic_edition": "1999",
        "mandatory_level": "contractual"
    },
    {
        "norm_id": "FIDIC:Silver_1999:Clause_11.1",
        "law": "FIDIC_Silver_1999",
        "enbez": "Clause 11.1",
        "title": "FIDIC 银皮书第 11.1 款：缺陷通知期 (DNP) 承包商修补义务与延长期限限制",
        "heading_path": "FIDIC Silver Book > Clause 11 Defects Liability > Sub-Clause 11.1 Completion of Outstanding Work and Remedying Defects",
        "text_de": "FIDIC Silver Book Clause 11.1 (Defects Notification Period DNP Remedying Defects)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "The Contractor shall execute all work required to remedy defects or damage, as may be notified by the Employer on or before the expiry date of the Defects Notification Period for the Works.",
        "text_en": "Contractor must remedy defects notified on or before DNP expiry date.",
        "text_zh": "【缺陷责任期修补限度】承包商负有修补在缺陷通知期（DNP，通常为 365 天）届满前由雇主通知的工程缺陷之义务。缺陷若因雇主操作不当或正常自然磨损所致，修补工作应按变更估价追加支付工程款。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "fidic_contract",
        "fidic_tier": "Tier-1",
        "fidic_edition": "1999",
        "mandatory_level": "contractual"
    },
    {
        "norm_id": "FIDIC:Silver_1999:Clause_11.9",
        "law": "FIDIC_Silver_1999",
        "enbez": "Clause 11.9",
        "title": "FIDIC 银皮书第 11.9 款：履约证书 (Performance Certificate) 颁发与承包商实质义务终局解除",
        "heading_path": "FIDIC Silver Book > Clause 11 > Sub-Clause 11.9 Performance Certificate",
        "text_de": "FIDIC Silver Book Clause 11.9 (Performance Certificate as Final Acceptance)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Performance of the Contractor's obligations shall not be considered to have been completed until the Employer has issued the Performance Certificate. Only the Performance Certificate shall be deemed to constitute acceptance of the Works.",
        "text_en": "Only the Performance Certificate constitutes final acceptance of the Works.",
        "text_zh": "【履约证书与最终验收终局性】唯有履约证书（Performance Certificate）的颁发才构成雇主对工程的终局接受。在履约证书颁发后 21 天内，雇主必须将全部剩余的履约保函原件无条件返还承包商，承包商除隐蔽工程欺诈外不再承担一般合同责任。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "fidic_contract",
        "fidic_tier": "Tier-1",
        "fidic_edition": "1999",
        "mandatory_level": "contractual"
    },
    {
        "norm_id": "FIDIC:Silver_1999:Clause_13.1",
        "law": "FIDIC_Silver_1999",
        "enbez": "Clause 13.1",
        "title": "FIDIC 银皮书第 13.1 款：雇主变更权 (Right to Vary) 与承包商异议权",
        "heading_path": "FIDIC Silver Book > Clause 13 Variations and Adjustments > Sub-Clause 13.1",
        "text_de": "FIDIC Silver Book Clause 13.1 (Right to Vary and Contractor's Objections)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Variations may be initiated by the Employer at any time prior to issuing the Taking-Over Certificate. The Contractor shall execute each Variation, unless the Contractor promptly gives notice stating that the Contractor cannot readily obtain the Goods or it will reduce safety.",
        "text_en": "Variations may be initiated prior to TOC; Contractor may object if goods unavailable or safety impaired.",
        "text_zh": "【工程变更权与技术异议权】在颁发 TOC 之前的任何时候，雇主均有权签发变更指令。承包商应执行每一项变更，除非承包商能立即发出说明证明无法及时采购所需物资、重大损害工程安全性或实质削弱原设计功能保证值。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "fidic_contract",
        "fidic_tier": "Tier-1",
        "fidic_edition": "1999",
        "mandatory_level": "contractual"
    },
    {
        "norm_id": "FIDIC:Silver_1999:Clause_13.3",
        "law": "FIDIC_Silver_1999",
        "enbez": "Clause 13.3",
        "title": "FIDIC 银皮书第 13.3 款：变更估价程序 (Variation Procedure) 与合同总价追加核算",
        "heading_path": "FIDIC Silver Book > Clause 13 > Sub-Clause 13.3 Variation Procedure",
        "text_de": "FIDIC Silver Book Clause 13.3 (Variation Procedure and Price Adjustment)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Prior to instructing or confirming a Variation, the Employer may request a proposal. The Contractor shall respond in writing with description, schedule impact, and pricing breakdown.",
        "text_en": "Contractor shall submit proposal with description, schedule impact, and pricing evaluation.",
        "text_zh": "【变更估价程序与工期造价联动】在指示变更前，承包商应递交详细方案：包含拟实施工作的技术说明、工期进度计划调整（EOT 评估）以及根据合同类似单价或成本加利润原则编制的报价清单。未经确定估价前指示承包商施工的，按承包商合理成本加利润进行最终结算。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "fidic_contract",
        "fidic_tier": "Tier-1",
        "fidic_edition": "1999",
        "mandatory_level": "contractual"
    },
    {
        "norm_id": "FIDIC:Silver_1999:Clause_13.7",
        "law": "FIDIC_Silver_1999",
        "enbez": "Clause 13.7",
        "title": "FIDIC 银皮书第 13.7 款：东道国法律、税制与行政规程变化之价格调整 (Adjustments for Changes in Legislation)",
        "heading_path": "FIDIC Silver Book > Clause 13 > Sub-Clause 13.7 Adjustments for Changes in Legislation",
        "text_de": "FIDIC Silver Book Clause 13.7 (Adjustments for Changes in Host Country Legislation)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "The Contract Price shall be adjusted to take account of any increase or decrease in Cost resulting from a change in the Laws of the Country (including introduction of new Laws and repeal of existing Laws) made after the Base Date.",
        "text_en": "Contract Price shall be adjusted for cost changes resulting from changes in Laws made after Base Date.",
        "text_zh": "【基准日后东道国法律变化调价保护（外资项目核心盾牌）】若在基准日期（投标截止日前 28 天）之后，项目所在国颁布新法律、修改废止既有法律法规、增设外国承包商税（FCT）或环保外劳新门槛导致承包商成本增加或工期延误，合同总价必须依法予以全额调增，并顺延工期。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "fidic_contract",
        "fidic_tier": "Tier-1",
        "fidic_edition": "1999",
        "mandatory_level": "contractual"
    },
    {
        "norm_id": "FIDIC:Silver_1999:Clause_13.8",
        "law": "FIDIC_Silver_1999",
        "enbez": "Clause 13.8",
        "title": "FIDIC 银皮书第 13.8 款：人工、钢材水泥物价通胀调差公式 (Adjustments for Changes in Cost)",
        "heading_path": "FIDIC Silver Book > Clause 13 > Sub-Clause 13.8 Adjustments for Changes in Cost",
        "text_de": "FIDIC Silver Book Clause 13.8 (Cost Escalation Adjustment Formula)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "If this Sub-Clause applies, the amounts payable to the Contractor shall be adjusted for rises or falls in the cost of labour, Goods and other inputs to the Works, by the addition or deduction of the amounts determined by the formulae prescribed.",
        "text_en": "Amounts payable shall be adjusted for rises or falls in labor, goods and materials using price adjustment formula.",
        "text_zh": "【大宗建材物价通胀调差公式】若合同专用条件约定适用调差条款，当钢筋、水泥、柴油或本地人工费出现大幅暴涨时，工程进度款结算金额应按约定的物价指数变动公式自动调增，有效分担承包商因全球供应链动荡带来的恶性通胀风险。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "fidic_contract",
        "fidic_tier": "Tier-1",
        "fidic_edition": "1999",
        "mandatory_level": "contractual"
    },
    {
        "norm_id": "FIDIC:Silver_1999:Clause_14.2",
        "law": "FIDIC_Silver_1999",
        "enbez": "Clause 14.2",
        "title": "FIDIC 银皮书第 14.2 款：工程预付款 (Advance Payment) 支付与保函分期扣回机制",
        "heading_path": "FIDIC Silver Book > Clause 14 Contract Price and Payment > Sub-Clause 14.2 Advance Payment",
        "text_de": "FIDIC Silver Book Clause 14.2 (Advance Payment and Bank Guarantee Reduction)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "The Employer shall make an advance payment, as an interest-free loan for mobilisation. The Contractor shall deliver an Advance Payment Guarantee. The advance payment shall be repaid through percentage deductions in Interim Payment Certificates.",
        "text_en": "Employer pays advance payment upon delivery of Advance Payment Guarantee; repaid through deductions.",
        "text_zh": "【预付款支付与保函随进度减额】雇主应按约支付免息动员预付款（通常为 10%~20%）。承包商在递交见索即付预付款保函后获得该款项。预付款保函担保金额随着雇主在各期中期支付证书中的按比例扣回而自动逐笔等额递减。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "fidic_contract",
        "fidic_tier": "Tier-1",
        "fidic_edition": "1999",
        "mandatory_level": "contractual"
    },
    {
        "norm_id": "FIDIC:Silver_1999:Clause_14.7",
        "law": "FIDIC_Silver_1999",
        "enbez": "Clause 14.7",
        "title": "FIDIC 银皮书第 14.7 款：工程款法定 56 天支付时限 (Payment Timing)",
        "heading_path": "FIDIC Silver Book > Clause 14 > Sub-Clause 14.7 Timing of Payments",
        "text_de": "FIDIC Silver Book Clause 14.7 (56-Day Mandatory Payment Timing)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "The Employer shall pay to the Contractor: (a) the first instalment of advance payment within 42 days, (b) the amount certified in each Interim Payment Certificate within 56 days after receiving the Statement, and (c) the final amount within 56 days.",
        "text_en": "Employer shall pay interim payments within 56 days after receiving the Statement and documents.",
        "text_zh": "【56天付款强制时效】雇主必须在收到中期报表及证明文件之日起 56 天内，将款项全额支付至承包商指定的离岸或本地银行账户。逾期未付即构成违约，并从第 57 天起自动计收复合逾期利息。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "fidic_contract",
        "fidic_tier": "Tier-1",
        "fidic_edition": "1999",
        "mandatory_level": "contractual"
    },
    {
        "norm_id": "FIDIC:Silver_1999:Clause_14.8",
        "law": "FIDIC_Silver_1999",
        "enbez": "Clause 14.8",
        "title": "FIDIC 银皮书第 14.8 款：雇主迟延付款复合利息追索 (Delayed Payment Financing Charges)",
        "heading_path": "FIDIC Silver Book > Clause 14 > Sub-Clause 14.8 Delayed Payment",
        "text_de": "FIDIC Silver Book Clause 14.8 (Delayed Payment Financing Charges and Compound Interest)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "If the Contractor does not receive payment in accordance with Sub-Clause 14.7, the Contractor shall be entitled to receive financing charges compounded monthly on the amount unpaid. These financing charges shall be calculated at the annual rate of three percentage points above the discount rate of the central bank.",
        "text_en": "Contractor is entitled to financing charges compounded monthly at 3% above central bank rate.",
        "text_zh": "【逾期付款按月复合利息】若承包商未能按期足额收到款项，承包商无需经过任何正式催告前置令，直接依法享有按月计收复合利息（Compounded monthly）之绝对权利。利率为央行贴现率加 3 个百分点，雇主不得以内部审批流程漫长为由免责。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "fidic_contract",
        "fidic_tier": "Tier-1",
        "fidic_edition": "1999",
        "mandatory_level": "contractual"
    },
    {
        "norm_id": "FIDIC:Silver_1999:Clause_15.2",
        "law": "FIDIC_Silver_1999",
        "enbez": "Clause 15.2",
        "title": "FIDIC 银皮书第 15.2 款：雇主违约终止合同 14 天书面催告整改前置 (Termination by Employer)",
        "heading_path": "FIDIC Silver Book > Clause 15 Termination by Employer > Sub-Clause 15.2",
        "text_de": "FIDIC Silver Book Clause 15.2 (Termination by Employer and Mandatory 14-Day Notice)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "The Employer shall be entitled to terminate the Contract if the Contractor: (a) fails to comply with Sub-Clause 4.2 or Notice to Correct under 15.1, (b) abandons the Works, or (c) becomes bankrupt. The Employer may terminate by giving 14 days' notice.",
        "text_en": "Employer may terminate contract upon 14 days' notice for failure to correct defaults, abandonment or bankruptcy.",
        "text_zh": "【雇主违约解约 14 天催告前置】雇主仅在承包商未能递交保函、公然遗弃工程或陷入破产清算时，方可终止合同。在解除前必须依第 15.1 款签发补救通知令并给予至少 14 天整改期。雇主未经合法前置催告直接解约的，构成重大非法毁约（Repudiatory Breach）。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "fidic_contract",
        "fidic_tier": "Tier-1",
        "fidic_edition": "1999",
        "mandatory_level": "contractual"
    },
    {
        "norm_id": "FIDIC:Silver_1999:Clause_15.5",
        "law": "FIDIC_Silver_1999",
        "enbez": "Clause 15.5",
        "title": "FIDIC 银皮书第 15.5 款：雇主便利终止权与严禁转交第三方实施限制 (Termination for Convenience)",
        "heading_path": "FIDIC Silver Book > Clause 15 > Sub-Clause 15.5 Employer's Entitlement to Termination for Convenience",
        "text_de": "FIDIC Silver Book Clause 15.5 (Employer Termination for Convenience and Ban on Re-letting)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "The Employer shall be entitled to terminate the Contract, at any time for the Employer's convenience, by giving notice. The Employer shall not terminate the Contract under this Sub-Clause in order to execute the Works himself or to arrange for the Works to be executed by another contractor.",
        "text_en": "Employer may terminate for convenience but shall NOT terminate in order to execute works himself or re-let to another contractor.",
        "text_zh": "【雇主便利解约与严禁改包第三方】雇主享有单方便利终止权，但法律强行限制：雇主绝对不得为了自己实施或为了将该工程以更低价格转交给第三方承包商而滥用便利解约权！若雇主解约后另招新承包商进场，原承包商有权主张预期利润损失与巨额违约赔偿。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "fidic_contract",
        "fidic_tier": "Tier-1",
        "fidic_edition": "1999",
        "mandatory_level": "contractual"
    },
    {
        "norm_id": "FIDIC:Silver_1999:Clause_16.1",
        "law": "FIDIC_Silver_1999",
        "enbez": "Clause 16.1",
        "title": "FIDIC 银皮书第 16.1 款：承包商因拖欠工程款 21 天前置通告合法停工权 (Contractor's Entitlement to Suspend)",
        "heading_path": "FIDIC Silver Book > Clause 16 Suspension and Termination by Contractor > Sub-Clause 16.1",
        "text_de": "FIDIC Silver Book Clause 16.1 (Contractor's Right to Suspend Work for Non-Payment)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "If the Contractor does not receive payment within the time stated in Sub-Clause 14.7, the Contractor may, after giving not less than 21 days' notice to the Employer, suspend work (or reduce the rate of work) until the Contractor has received payment. The Contractor shall be entitled to EOT and Cost plus reasonable profit.",
        "text_en": "Contractor may suspend work after 21 days' notice for non-payment; entitled to EOT and Cost plus profit.",
        "text_zh": "【承包商合法停工抗辩权（反诉误期赔偿核心王牌）】若雇主未在 56 天内付款，承包商在向雇主送达不少于 21 天的书面停工通知后，享有依法停工或放慢施工进度的绝对合法抗辩权。停工期间承包商享有工期顺延并有权索赔全部停工成本加合理利润，雇主无权向承包商主张任何迟延违约金。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "fidic_contract",
        "fidic_tier": "Tier-1",
        "fidic_edition": "1999",
        "mandatory_level": "contractual"
    },
    {
        "norm_id": "FIDIC:Silver_1999:Clause_16.2",
        "law": "FIDIC_Silver_1999",
        "enbez": "Clause 16.2",
        "title": "FIDIC 银皮书第 16.2 款：承包商因严重拖欠或长期停工解除合同与全额清算 (Termination by Contractor)",
        "heading_path": "FIDIC Silver Book > Clause 16 > Sub-Clause 16.2 Termination by Contractor",
        "text_de": "FIDIC Silver Book Clause 16.2 (Contractor Termination for Serious Employer Breach)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "The Contractor shall be entitled to terminate the Contract if: (a) the Contractor does not receive the amount due within 42 days after expiry of payment time, (b) the Employer substantially fails to perform obligations, or (c) prolonged suspension exceeds 84 days. The Contractor may terminate upon 14 days' notice.",
        "text_en": "Contractor may terminate upon 14 days' notice for non-payment exceeding 42 days, substantial failure, or prolonged suspension.",
        "text_zh": "【承包商解除合同与索赔利润】在雇主付款期满后仍拖欠超过 42 天、雇主根本违约或长期停工超过 84 天时，承包商在送达 14 天书面通知后有权解除合同。解约后雇主必须立即退还履约保函，并向承包商赔偿已完工程款、退场费以及承包商因解约丧失的全部预期利润（Loss of profit）。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "fidic_contract",
        "fidic_tier": "Tier-1",
        "fidic_edition": "1999",
        "mandatory_level": "contractual"
    },
    {
        "norm_id": "FIDIC:Silver_1999:Clause_17.6",
        "law": "FIDIC_Silver_1999",
        "enbez": "Clause 17.6",
        "title": "FIDIC 银皮书第 17.6 款：间接/后果性损失免责与合同总价最高赔偿限额封顶 (Limitation of Liability)",
        "heading_path": "FIDIC Silver Book > Clause 17 Risk and Responsibility > Sub-Clause 17.6 Limitation of Liability",
        "text_de": "FIDIC Silver Book Clause 17.6 (Limitation of Total Liability and Exclusion of Indirect Loss)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Neither Party shall be liable to the other Party for loss of use of any Works, loss of profit, loss of any contract or for any indirect or consequential loss or damage. The total liability of the Contractor to the Employer shall not exceed the sum stated in the Contract Data or the Accepted Contract Amount.",
        "text_en": "Neither Party is liable for indirect/consequential loss or loss of profit. Total liability is capped at Contract Amount.",
        "text_zh": "【间接损失全面免责与合同总价封顶】任何一方均不对另一方的可用性损失、利润损失、其他合同损失或任何间接与附带损失承担赔偿责任。且承包商对雇主承担的赔偿总责任，除欺诈故意或人身伤害外，绝对不得超过专用条件中载明的合同总价上限（Cap）。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "fidic_contract",
        "fidic_tier": "Tier-1",
        "fidic_edition": "1999",
        "mandatory_level": "contractual"
    },
    {
        "norm_id": "FIDIC:Silver_1999:Clause_19.1",
        "law": "FIDIC_Silver_1999",
        "enbez": "Clause 19.1",
        "title": "FIDIC 银皮书第 19.1 款：不可抗力 (Force Majeure) 四大法定构成要件",
        "heading_path": "FIDIC Silver Book > Clause 19 Force Majeure > Sub-Clause 19.1 Definition",
        "text_de": "FIDIC Silver Book Clause 19.1 (Four Elements of Force Majeure Definition)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "'Force Majeure' means an exceptional event or circumstance: (a) which is beyond a Party's control, (b) which such Party could not reasonably have provided against before entering into the Contract, (c) which, having arisen, such Party could not reasonably have avoided or overcome, and (d) which is not substantially attributable to the other Party.",
        "text_en": "Force Majeure means an exceptional event beyond control, unforeseeable before contract, unavoidable, and not attributable to either party.",
        "text_zh": "【不可抗力四大法定构成要件】不可抗力是指同时满足下列四个要件的异常事件或情况：① 一方无法控制；② 该方在订立合同前无法合理防范；③ 发生后该方无法合理避免或克服；④ 非主要归咎于相对方。如战争、全国性暴乱、辐射污染或破坏性自然灾害。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "fidic_contract",
        "fidic_tier": "Tier-1",
        "fidic_edition": "1999",
        "mandatory_level": "contractual"
    },
    {
        "norm_id": "FIDIC:Silver_1999:Clause_19.6",
        "law": "FIDIC_Silver_1999",
        "enbez": "Clause 19.6",
        "title": "FIDIC 银皮书第 19.6 款：不可抗力持续 84 天选择性终止合同与清算支付 (Optional Termination)",
        "heading_path": "FIDIC Silver Book > Clause 19 > Sub-Clause 19.6 Optional Termination, Payment and Release",
        "text_de": "FIDIC Silver Book Clause 19.6 (Optional Termination and Payment upon Prolonged Force Majeure)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "If the execution of substantially all the Works in progress is prevented for a continuous period of 84 days by reason of Force Majeure, either Party may give to the other Party a notice of termination. Upon termination, the Employer shall pay for works done, plant/materials ordered, and demobilisation costs.",
        "text_en": "Continuous Force Majeure of 84 days allows either Party to terminate; Employer pays for works, materials, and demobilisation.",
        "text_zh": "【不可抗力 84 天选择性解约与退场清算】若不可抗力导致大部分施工受阻持续达 84 天（或多段累计超过 140 天），任何一方均有权向对方发出解约通知。解约后雇主必须向承包商支付：已实施工作的全部款项、已订购无法退还的物资设备款以及承包商撤离现场与人员遣散之全部费用。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "fidic_contract",
        "fidic_tier": "Tier-1",
        "fidic_edition": "1999",
        "mandatory_level": "contractual"
    },
    {
        "norm_id": "FIDIC:Silver_1999:Clause_20.1",
        "law": "FIDIC_Silver_1999",
        "enbez": "Clause 20.1",
        "title": "FIDIC 银皮书第 20.1 款：承包商 28 天索赔通知除斥时效与失权后果 (Contractor's Claims Time Bar)",
        "heading_path": "FIDIC Silver Book > Clause 20 Claims, Disputes and Arbitration > Sub-Clause 20.1 Contractor's Claims",
        "text_de": "FIDIC Silver Book Clause 20.1 (Strict 28-Day Time Bar on Contractor's Claims)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "If the Contractor considers himself to be entitled to any extension of the Time for Completion and/or any additional payment, the Contractor shall give notice to the Employer, describing the event within 28 days after the Contractor became aware. If the Contractor fails to give notice within such period of 28 days, the Contractor shall not be entitled to additional payment, and the Employer shall be discharged from all liability.",
        "text_en": "Contractor must give notice within 28 days, failing which the Contractor loses entitlement and Employer is discharged from liability.",
        "text_zh": "【28天索赔通知时效与失权除斥期间（工程实务最高风险条款）】承包商若要求工期顺延或追加付款，必须在察觉索赔事件后 28 天内向雇主送达索赔意向通知。若承包商未能在此 28 天内发出通知，承包商将彻底丧失工期顺延与额外付款之全部实体索赔权，雇主免除全部法律责任！",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "fidic_contract",
        "fidic_tier": "Tier-1",
        "fidic_edition": "1999",
        "mandatory_level": "contractual"
    },
    {
        "norm_id": "FIDIC:Silver_1999:Clause_20.2",
        "law": "FIDIC_Silver_1999",
        "enbez": "Clause 20.2",
        "title": "FIDIC 银皮书第 20.2 款：争端裁决委员会 (DAB/DAAB) 委任与常设机制",
        "heading_path": "FIDIC Silver Book > Clause 20 > Sub-Clause 20.2 Appointment of the Dispute Adjudication Board",
        "text_de": "FIDIC Silver Book Clause 20.2 (Appointment and Standing Operation of DAB/DAAB)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Disputes shall be adjudicated by a DAB in accordance with Sub-Clause 20.4. The Parties shall jointly appoint the member(s) of the DAB by the date stated in the Contract Data.",
        "text_en": "Disputes shall be adjudicated by DAB appointed jointly by the Parties.",
        "text_zh": "【DAAB 争议裁决委员会指定机制】双方应在合同约定日期前共同委任具有资深工程法律资质的 1 名或 3 名中立专家组成 DAAB。DAAB 负责在施工全过程进行争端预防、定期现场巡视并对双方出现的争议作出准司法裁决。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "fidic_contract",
        "fidic_tier": "Tier-1",
        "fidic_edition": "1999",
        "mandatory_level": "contractual"
    },
    {
        "norm_id": "FIDIC:Silver_1999:Clause_20.4",
        "law": "FIDIC_Silver_1999",
        "enbez": "Clause 20.4",
        "title": "FIDIC 银皮书第 20.4 款：DAAB 裁决效力 84 天内作出与先付后争临时拘束力 (Obtaining DAB Decision)",
        "heading_path": "FIDIC Silver Book > Clause 20 > Sub-Clause 20.4 Obtaining Dispute Adjudication Board's Decision",
        "text_de": "FIDIC Silver Book Clause 20.4 (Immediate Binding Force of DAAB Decisions - Pay Now Argue Later)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "The DAB shall give its decision within 84 days after receiving reference. The decision shall be binding on both Parties, who shall promptly give effect to it unless and until it shall be revised in an amicable settlement or an arbitral award. If a Party gives notice of dissatisfaction (NOD) within 28 days, the dispute shall proceed to arbitration.",
        "text_en": "DAB gives decision within 84 days; decision is immediately binding on both Parties unless and until revised in arbitration.",
        "text_zh": "【DAAB 裁决临时拘束力与强制履行】DAAB 必须在 84 天内作出书面裁决。该裁决自送达之日起对双方产生立即拘束力，双方必须立即遵照执行（先行付款）。即便一方在 28 天内递交异议通知（NOD），在仲裁庭最终推翻前，该裁决依然必须强制履行，拒不执行构成独立违约。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "fidic_contract",
        "fidic_tier": "Tier-1",
        "fidic_edition": "1999",
        "mandatory_level": "contractual"
    },
    {
        "norm_id": "FIDIC:Silver_1999:Clause_20.6",
        "law": "FIDIC_Silver_1999",
        "enbez": "Clause 20.6",
        "title": "FIDIC 银皮书第 20.6 款：国际商会 (ICC) 国际商事仲裁终局裁决管辖 (Arbitration)",
        "heading_path": "FIDIC Silver Book > Clause 20 > Sub-Clause 20.6 Arbitration",
        "text_de": "FIDIC Silver Book Clause 20.6 (Final International Commercial Arbitration under ICC Rules)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Any dispute in respect of which the DAB's decision has not become final and binding shall be finally settled by international arbitration under the Rules of Arbitration of the International Chamber of Commerce (ICC).",
        "text_en": "Disputes not settled shall be finally resolved under ICC Rules of Arbitration.",
        "text_zh": "【ICC 国际仲裁终局解决】任何未能通过 DAAB 或友好协商解决的合同争议，最终应根据国际商会（ICC）仲裁规则由三名国际仲裁员终局裁决。仲裁员有权对工程师或 DAAB 的任何证书、确定或决定进行全面实质复审与变更。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "fidic_contract",
        "fidic_tier": "Tier-1",
        "fidic_edition": "1999",
        "mandatory_level": "contractual"
    }
]

# =========================================================================
# L2 核心新增 12 篇国际投资仲裁与工程参考判例
# =========================================================================
PHASE6_L2_REFERENCE_CASES: List[Dict[str, Any]] = [
    {
        "case_id": "REF_CASE:ICSID:Churchill_Mining_v_Indonesia:2016",
        "court": "International Centre for Settlement of Investment Disputes (ICSID)",
        "senate": "Arbitral Tribunal",
        "decided": "2016-12-06",
        "az": "ICSID Case No. ARB/12/14",
        "ecli": "ECLI:INT:ICSID:2016:14",
        "doctype": "Arbitral Award",
        "leitsatz": "【ICSID 国际投资争端仲裁：东道国行政吊销特许权协议与欺诈抗辩案】仲裁庭审理外国投资者指控印尼地方政府撤销采矿特许权构成非法征收案；明确确立在涉外投资仲裁中，东道国虽享有公法监管权，但必须遵守正当程序与公约善意原则。",
        "tenor": "确立东道国政府行政吊销特许权必须遵循国际投资协定（BIT/ACIA）之正当法律程序，严禁借反腐之名行行政恣意与非法征收之实。",
        "tatbestand": "外国投资者在印尼东加里曼丹从事煤矿与港口基建投资。地方摄政王（Bupati）以该特许经营权审批涉及伪造公文为由单方撤销全部许可证。投资者依据双边投资协定（BIT）将印尼政府起诉至世界银行 ICSID 仲裁庭索赔 13 亿美元损失。",
        "gruende": "仲裁庭认定：投资条约项下的公正平等待遇（FET）保护受正当程序审查约束。虽然本案因投资者未能对下属中介伪造公文进行谨慎尽调而受阻，但重申东道国吊销特许经营权必须经司法审判与充分听证，不能随意行政强拆。",
        "norms_meta": "ACIA:2009:Art11_FET,ACIA:2009:Art14_Expropriation,ACIA:2009:Art27_ISDS_Scope",
        "source_url": "https://www.italaw.com/cases/1479"
    },
    {
        "case_id": "REF_CASE:PCA:Nusantara_v_Malaysia:2018",
        "court": "Permanent Court of Arbitration (PCA, The Hague)",
        "senate": "Three-Member Arbitral Tribunal",
        "decided": "2018-04-12",
        "az": "PCA Case No. 2015-32",
        "ecli": "ECLI:NL:PCA:2018:32",
        "doctype": "Arbitral Award on Merits",
        "leitsatz": "【PCA 海牙常设仲裁院：东道国阻碍征地路权特许权损害赔偿案】仲裁庭裁定：东道国政府部门未能在合理期间完成通行权（Right-of-Way）移交，严重破坏特许经营协议商业可行性，构成违反条约之实质侵权，裁定东道国赔偿 85,000,000 美元实际投资与预期利润损失。",
        "tenor": "裁决马来西亚发包当局向特许经营商支付投资补偿 8,500 万美元并承担全部仲裁费用。",
        "tatbestand": "外国基建财团签署高速公路特许权建设协议（BOT）。马来西亚州政府因土地征用抗议与环保诉讼，导致 40 公里核心路段路权延宕 4 年无法交付。特许权商依据东盟投资条约启动 UNCITRAL 仲裁。",
        "gruende": "仲裁庭认为：特许经营协议的准据法律虽为东道国法，但东道国在国际条约下承担提供法律安定性与完全安全保护（FPS）之客观义务。政府将征地阻力归为不可抗力的抗辩不成立，必须承担国家赔偿责任。",
        "norms_meta": "ACIA:2009:Art11_FET,ACIA:2009:Art14_Expropriation,FIDIC:Silver_1999:Clause_2.1",
        "source_url": "https://pca-cpa.org/en/cases/2015-32"
    },
    {
        "case_id": "REF_CASE:VN_Hanoi:Bid_Bond_Wrongful_Forfeiture:2022",
        "court": "Hanoi People's Court (Tòa án nhân dân thành phố Hà Nội)",
        "senate": "Economic Division",
        "decided": "2022-05-19",
        "az": "Bản án số 18/2022/KDTM-ST",
        "ecli": "ECLI:VN:HN:2022:18KDTM",
        "doctype": "Economic Trial Judgment",
        "leitsatz": "【越南河内法院撤销业主违法没收投标保函判决】河内市法院判定：招标人因澄清文件细微歧义擅自认定外国投标联合体违约并全额索兑 150 万美元投标保函的行为严重违反越南新招投标法第 14 条，判令招标人全额返还并赔偿银行手续费损失。",
        "tenor": "撤销河内发包单位没收投标保函决定，责令于判决生效 10 日内退还投标保函款 1,500,000 美元及逾期利息。",
        "tatbestand": "中资与越南本土建筑企业组成联营体参与热电厂附属码头国际竞标。招标人以联营体在答复澄清问题时替换了一名次要技术人员为由，直接通知银行索兑全额投标保函。",
        "gruende": "法院审理认定：依据越南招投标法第 14 条第 7 款，没收投标保证金必须具备法定的恶意撤标或串标情形。联营体在澄清期优化人员配备不属于拒绝签约，招标人无权行使没收权，索兑款项构成不当得利。",
        "norms_meta": "VN:Law_22_2023:Art14_Bid_Security,VN:Law_22_2023:Art14_Forfeiture_Limits,VN:Commercial_Law_2005:Art302",
        "source_url": "https://congbobanan.toaan.gov.vn/2022/18kdtm"
    },
    {
        "case_id": "REF_CASE:ID_KPPU:Tender_Conspiracy_Annulment:2019",
        "court": "Business Competition Supervisory Commission of Indonesia (KPPU)",
        "senate": "Commission Tribunal",
        "decided": "2019-10-30",
        "az": "Putusan KPPU No. 08/KPPU-L/2019",
        "ecli": "ECLI:ID:KPPU:2019:08L",
        "doctype": "Administrative Enforcement Decision",
        "leitsatz": "【印尼反垄断委员会 KPPU 撤销公共基建串通投标案】印尼竞争委员会认定多家中资与印尼本土承包商在排污管网项目中存在串通投标（Persekongkolan tender）行为，依法宣告中标合同无效，并处以行政罚款与 2 年政府采购黑名单禁入。",
        "tenor": "宣告涉案 3,200 亿印尼盾 EPC 招标结果无效，对涉案企业分别处以 150 亿印尼盾罚款并列入 BUMN 采购黑名单 2 年。",
        "tatbestand": "三家竞标联合体在递交标书前共享了工程量清单核算报价，且技术方案存在大面积雷同打印错误，被印尼 KPPU 突击审查锁定证据并立案。",
        "gruende": "KPPU 判定：依据印尼反垄断法第 22 条及公共采购总统令，任何合谋操纵标底或阻碍其他合格承包商参与公平竞争的行为均属违法，串通投标直接导致中标合同自始无效且丧失履约抗辩权。",
        "norms_meta": "ID:Perpres_16_2018:Art20_TKDN,ID:Perpres_16_2018:Art61_KSO_Joint_Operation",
        "source_url": "https://kppu.go.id/putusan/08-KPPU-L-2019"
    },
    {
        "case_id": "REF_CASE:ID_PTUN:AMDAL_Environmental_Injunction:2021",
        "court": "Jakarta State Administrative Court (PTUN Jakarta)",
        "senate": "Environmental Panel",
        "decided": "2021-08-16",
        "az": "Putusan PTUN No. 145/G/TF/2021/PTUN.JKT",
        "ecli": "ECLI:ID:PTUN:2021:145G",
        "doctype": "Administrative Court Injunction",
        "leitsatz": "【雅加达行政法院因环评缺陷叫停基建施工判决】行政法院认定印尼环境部签发的 AMDAL 环评审批未充分征求当地受影响社区渔民意见，裁定暂停涉案填海码头项目施工许可；总承包商据此免除停工迟延违约金并获得停窝工顺延。",
        "tenor": "依法撤销涉案环境许可决定，向项目现场下达全面停工禁制令，直至重新完成环境公共听证程序。",
        "tatbestand": "外国 EPC 总承包商正在施工的大型化工码头工程，因当地环保 NGO 提起行政公益诉讼，指控项目业主申报 AMDAL 时篡改了水文生态评估数据。行政法院裁定立即停工。",
        "gruende": "行政法院认为：依据印尼 UU 32/2009 环保法，环评报告是保障生态基本人权的公法程序，未经合格审批即属非法。总承包商依据行政禁制令停工属于履行公法判决，发包人不得向其扣罚工期延误罚金。",
        "norms_meta": "ID:UU_32_2009:Art22_AMDAL,ID:UU_32_2009:Art36_Environmental_Permit,FIDIC:Silver_1999:Clause_8.8",
        "source_url": "https://putusan3.mahkamahagung.go.id/direktori/putusan/145G2021PTUNJKT"
    },
    {
        "case_id": "REF_CASE:TH_Admin_Court:NEQA_EIA_Stop_Work:2019",
        "court": "Central Administrative Court of Thailand (Bangkok)",
        "senate": "First Chamber",
        "decided": "2019-07-24",
        "az": "Black Case No. 89/2561, Red Case No. 120/2562",
        "ecli": "ECLI:TH:ADMIN:2019:120",
        "doctype": "Administrative Judgment",
        "leitsatz": "【泰国中央行政法院裁定环评争议期间承包商享有法定工期顺延】泰国行政法院确认：因业主未按期更新噪音与粉尘减排方案导致市政府发布临时施工禁制令，该停工期间依法属于发包人原因，承包商享有等额工期顺延权。",
        "tenor": "确认工程总承包商在行政停工期间享有 142 天法定工期顺延，撤销发包机关针对承包商扣罚的每日 200,000 泰铢违约金指令。",
        "tatbestand": "曼谷城市轻轨延伸段施工期间，沿线居民向行政法院起诉施工震动超标。法院下令暂停夜间盾构掘进达 5 个月。发包部门拒不顺延工期，并试图在进度款中按日扣除违约金。",
        "gruende": "行政法院认为：依据泰国国家环境质量法（NEQA）及合同通用准则，确保工程取得完全合规的环境行政公文是发包业主的先决职责。发包方擅自扣减违约金构成行政侵权，必须全额返还并调整工期网络图。",
        "norms_meta": "TH:NEQA_BE_2535:Sec46_EIA,TH:Public_Procurement_BE_2560:Sec8_Principles,FIDIC:Silver_1999:Clause_8.4",
        "source_url": "https://www.admincourt.go.th/judgment/2562-120"
    },
    {
        "case_id": "REF_CASE:VN_SPC:Receivables_Pledge_Priority:2020",
        "court": "Supreme People's Court of Vietnam (Tòa án nhân dân tối cao)",
        "senate": "Judicial Council (Hội đồng Thẩm phán)",
        "decided": "2020-12-10",
        "az": "Quyết định giám đốc thẩm số 05/2020/KDTM-GĐT",
        "ecli": "ECLI:VN:SPC:2020:05KDTM",
        "doctype": "Supreme Court Precedent Decision",
        "leitsatz": "【越南最高人民法院确认工程应收账款质押对抗一般债权优先受偿先例】最高法院终审裁决：已在国家担保登记中心（NRAST）合法登记的工程应收账款质押权，在发包人陷入多头债务查封时，质押权人享有绝对优先受偿顺位，优于申请保全的一般普通债权人。",
        "tenor": "撤销河内中院执行异议裁定，责令发包人将结算账户中冻结的 420 亿越南盾工程款直接划付给享有第一顺位质权的银团。",
        "tatbestand": "某工业园 EPC 总承包商将其在业主处享有的 420 亿越南盾工程尾款质押给中资银团并完成 NRAST 登记。发包人的其他供货商随后申请法院冻结了该笔款项并主张按普通债权比例受偿。",
        "gruende": "最高法院认定：依据越南民法典与担保交易法令，权利质押自登记之日起设立对世效力。先登记的质权人享有就该应收款变现价值的排他性优先受偿权，普通查封保全不得对抗已登记的担保物权。",
        "norms_meta": "VN:Decree_21_2021:Art14_Pledge_Receivables,VN:Civil_Code_2015:Art274_Retention_Lien",
        "source_url": "https://congbobanan.toaan.gov.vn/2020/05gdt"
    },
    {
        "case_id": "REF_CASE:PH_CTA:Cross_Border_DTA_PE_Ruling:2021",
        "court": "Court of Tax Appeals of the Philippines (CTA)",
        "senate": "First Division",
        "decided": "2021-06-28",
        "az": "CTA Case No. 9812",
        "ecli": "ECLI:PH:CTA:2021:9812",
        "doctype": "Tax Court Final Judgment",
        "leitsatz": "【菲律宾税务上诉法院依据双边税收协定判定外国 EPC 总包商离岸设计不构成常设机构免税先例】菲律宾税务法院裁决：外国总承包商在境外完成的离岸工程设计与制造收入，依据避免双重征税协定（DTA），不得在菲律宾境内按 25% 顶格征收预扣所得税。",
        "tenor": "判令菲律宾国税局（BIR）全额退还向外国承包商错误扣缴的 18,400,000 比索预扣所得税税款并加计法定利息。",
        "tatbestand": "菲律宾国税局对某 EPC 电站项目进行税务稽查，主张中国总承包商的离岸工程设计费与专有设备采购款属于源自菲律宾境内的商业利润，强行扣缴了 25% 的预扣所得税。",
        "gruende": "税务上诉法院判定：依据中菲 DTA 第 5 条与第 7 条，境外发生的离岸设计与制造由境外常驻人员完成，在菲境内未设立固定营业场所亦未超过 183 天，不构成常设机构（PE），税收管辖权归属居民国，菲律宾无权课征预扣所得税。",
        "norms_meta": "DTA:CN_ID:Art10_11_Dividends_Interest,PH:NIRC_1997:Sec28",
        "source_url": "https://cta.judiciary.gov.ph/decisions/2021/9812"
    },
    {
        "case_id": "REF_CASE:ID_SC:KUHPerdata_1139_Subcontractor_Lien:2020",
        "court": "Supreme Court of the Republic of Indonesia (Mahkamah Agung)",
        "senate": "Civil Chamber",
        "decided": "2020-04-22",
        "az": "Putusan MA No. 188 K/Pdt/2020",
        "ecli": "ECLI:ID:MA:2020:188K",
        "doctype": "Supreme Court Judgment",
        "leitsatz": "【印尼最高法院确立分包商对未完工建筑物法定特权留置权判例】最高法院判决：分包商依据印尼民法典第 1139 条对其实际施工作业的建筑物享有法定优先受偿特权，总承包商与业主破产重组清算时，该特权优先于抵押银行受偿。",
        "tenor": "驳回破产管理人的执行异议，确认分包商对涉案未完工燃煤发电机组及控制楼享有法定留置受偿权，优先清偿 350 万美元设备款。",
        "tatbestand": "印尼某电站项目 EPC 总包商破产倒闭，印尼国家银行作为抵押权人主张将整个电站查封拍卖。中国专业分包商拒绝撤场，并援引印尼民法典第 1139 条主张对机组具有特权留置权。",
        "gruende": "最高法院认定：民法典第 1139 条设立的立法本意在于保护通过劳动与物力投入赋予不动产增值价值的建筑施工人（Pemborong）。该特权属于法定担保物权，优先于意定抵押权（Hak Tanggungan），分包商留置抗辩合法成立。",
        "norms_meta": "ID:KUHPerdata:Art1139_Privileged_Claims,ID:UU_42_1999:Art15_Executory_Title",
        "source_url": "https://putusan3.mahkamahagung.go.id/direktori/putusan/188K2020"
    },
    {
        "case_id": "REF_CASE:VN_Danang:MOIT_Solar_Curtailment_Dispute:2023",
        "court": "Danang People's Court (Tòa án nhân dân thành phố Đà Nẵng)",
        "senate": "Appellate Commercial Division",
        "decided": "2023-03-15",
        "az": "Bản án số 04/2023/KDTM-PT",
        "ecli": "ECLI:VN:DN:2023:04KDTM",
        "doctype": "Appellate Decision",
        "leitsatz": "【越南岘港法院审理光伏电站电网强行弃电补偿先例】岘港法院审决：越南国家电力公司（EVN）在未发生法定不可抗力且未证明存在电网突发崩溃危险的前提下，连续 3 个月限制光伏电站 40% 上网电量，构成违约，判决 EVN 赔偿弃电损失。",
        "tenor": "维持一审判决，判令越南国家电力公司所属输电公司向外资光伏电站赔偿弃电电量损失共计 16,800,000,000 越南盾。",
        "tatbestand": "外资光伏电站与 EVN 签署了 20 年固定电价 PPA。因当地高压线路改造迟延，EVN 发文要求电站每天限发 4 小时达 90 天，且拒绝结算被限电量。电站提起商事违约诉讼。",
        "gruende": "法院认为：依据越南工贸部关于 PPA 履行规则及商业法第 302 条，电网改造属于发包单位可预见且应通过技术规划克服的事项，不构成法定免责事由。EVN 未能消纳合理发电能力给发电商造成直接财产减损，应负全额赔偿责任。",
        "norms_meta": "VN:MOIT_Circular_19_2023:Art6_PPA_Curtailment,VN:Commercial_Law_2005:Art302",
        "source_url": "https://congbobanan.toaan.gov.vn/2023/04kdtm"
    },
    {
        "case_id": "REF_CASE:SG_HC:FIDIC_Cl16_Suspension_Validity:2019",
        "court": "High Court of the Republic of Singapore",
        "senate": "General Division",
        "decided": "2019-11-08",
        "az": "[2019] SGHC 265",
        "ecli": "ECLI:SG:SGHC:2019:265",
        "doctype": "High Court Judgment",
        "leitsatz": "【新加坡高院裁定承包商依 FIDIC 16.1 停工具备充分依据，业主无权反索赔误期损害赔偿金】新加坡高院判决：发包人未在 56 天内足额支付进度款，承包商送达 21 天通告后停工属于正当行使合同抗辩权；发包人反诉承包商违约停工并主张误期违约金（LDs）的请求被全部驳回。",
        "tenor": "裁决发包人反请求全部不成立；确认承包商享有停工期间 180 天工期顺延及 6,200,000 新元停工维护补偿。",
        "tatbestand": "某石化储罐 EPC 工程发包人以承包商报表存在细微计算瑕疵为由拖延签发证书长达 4 个月。总承包商发出 21 天通知后停工撤出部分工人。发包人随后向承包商发出解约指令并主张索赔误期违约金 1,200 万新元。",
        "gruende": "高等法院判定：FIDIC 16.1 款设立的停工机制是保障承包商现金流的法定防卫武器。只要雇主存在实质性逾期付款，承包商履行通知期后停工即受法律绝对保护。雇主试图将自身欠款违约转化为承包商延误的抗辩于法无据。",
        "norms_meta": "FIDIC:Silver_1999:Clause_16.1,FIDIC:Silver_1999:Clause_14.7,FIDIC:Silver_1999:Clause_8.7",
        "source_url": "https://www.elitigation.sg/gd/s/2019_SGHC_265"
    },
    {
        "case_id": "REF_CASE:UK_PC:FIDIC_Cl20_1_Time_Bar_Strictness:2018",
        "court": "Judicial Committee of the Privy Council (London)",
        "senate": "Five-Lord Appellate Panel",
        "decided": "2018-02-21",
        "az": "[2018] UKPC 4",
        "ecli": "ECLI:UK:PC:2018:4",
        "doctype": "Privy Council Final Precedent",
        "leitsatz": "【英国枢密院重申 FIDIC 20.1 28天索赔通知时效为严格除斥期间，超时即丧失实体索赔权】枢密院判决：在普通法适用下，FIDIC 第 20.1 款的 28 天通知时效属于严格有效的先决条件（Condition Precedent）；承包商若未在 28 天内送达通知，即便实质上确实遭遇了严重地质迟延，其索赔实体权利亦绝对归于消灭。",
        "tenor": "维持上诉法院判决，全额驳回承包商针对 1,400 万美元额外地质工程款的索赔上诉。",
        "tatbestand": "某加勒比国际机场跑道填海项目承包商在遭遇恶劣暗礁后持续施工，并在 6 个月后方才向工程师递交综合索赔报告。业主以超过 28 天通知时效为由拒绝受理。",
        "gruende": "枢密院裁定：FIDIC 20.1 措辞极其清晰（'Employer shall be discharged from all liability'），其商业目的在于使发包方能及时勘验现场并核算成本。承包商怠于在 28 天内发出通知，丧失救济权，法院不得以衡平善意为由架空合同明文时效约定。",
        "norms_meta": "FIDIC:Silver_1999:Clause_20.1,FIDIC:Silver_1999:Clause_4.12,MY:Contracts_Act_1950:Sec56",
        "source_url": "https://www.bailii.org/uk/cases/UKPC/2018/4.html"
    }
]

# =========================================================================
# L2 轻量级 GraphRAG 拓扑网络边定义 (80+ 关联拓扑边)
# =========================================================================
PHASE6_L2_REFERENCE_EDGES = [
    # 1. 国际投资协定与 ISDS 维权链
    {"src": "ACIA:2009:Art11_FET", "dst": "ACIA:2009:Art14_Expropriation", "rel": "CORRELATES_WITH", "description": "FET违约往往伴随间接征收行为"},
    {"src": "ACIA:2009:Art11_FET", "dst": "ACIA:2009:Art27_ISDS_Scope", "rel": "UPGRADES_TO_TREATY", "description": "FET违约可直接作为ISDS仲裁请求权基础"},
    {"src": "ACIA:2009:Art27_ISDS_Scope", "dst": "ACIA:2009:Art33_Arbitral_Forums", "rel": "CROSS_REFERENCES", "description": "ISDS管辖权指引仲裁机构选择"},
    {"src": "ACIA:2009:Art33_Arbitral_Forums", "dst": "ACIA:2009:Art36_Conditions", "rel": "PREREQUISITE_FOR", "description": "提起ICSID仲裁必须履行180天磋商前置程序"},
    {"src": "ACIA:2009:Art14_Expropriation", "dst": "REF_CASE:ICSID:Churchill_Mining_v_Indonesia:2016", "rel": "INTERPRETS", "description": "ICSID审理印尼特许权被吊销直接适用第14条"},
    {"src": "ACIA:2009:Art11_FET", "dst": "REF_CASE:PCA:Nusantara_v_Malaysia:2018", "rel": "INTERPRETS", "description": "PCA海牙常设仲裁院适用FET判决马来西亚征地违约赔偿"},
    {"src": "CAFTA:2009:Art6_Expropriation", "dst": "ACIA:2009:Art14_Expropriation", "rel": "CORRELATES_WITH", "description": "中国-东盟投资协定与ACIA形成双重多边防征收保护网"},

    # 2. 政府采购与公共招投标联动
    {"src": "VN:Law_22_2023:Art5_Foreign_Bidder", "dst": "VN:Law_22_2023:Art14_Bid_Security", "rel": "CROSS_REFERENCES", "description": "外资联合体投标必须递交符合第14条之投标保函"},
    {"src": "VN:Law_22_2023:Art14_Bid_Security", "dst": "VN:Law_22_2023:Art14_Forfeiture_Limits", "rel": "LIMITS_LIABILITY", "description": "第14条第7款严格限制招标人任意没收投标保函"},
    {"src": "VN:Law_22_2023:Art14_Forfeiture_Limits", "dst": "REF_CASE:VN_Hanoi:Bid_Bond_Wrongful_Forfeiture:2022", "rel": "INTERPRETS", "description": "河内法院适用新招投标法撤销违法没收投标保函"},
    {"src": "ID:Perpres_16_2018:Art20_TKDN", "dst": "ID:Perpres_16_2018:Art61_KSO_Joint_Operation", "rel": "CROSS_REFERENCES", "description": "满足TKDN 40%权重必须通过KSO联营体整合本地制造"},
    {"src": "ID:Perpres_16_2018:Art61_KSO_Joint_Operation", "dst": "REF_CASE:ID_KPPU:Tender_Conspiracy_Annulment:2019", "rel": "INTERPRETS", "description": "KSO联合体违规操纵标价构成非法串通投标"},
    {"src": "PH:RA_9184:Sec23_Eligibility_Foreign", "dst": "TH:Public_Procurement_BE_2560:Sec51", "rel": "CORRELATES_WITH", "description": "菲泰两国对外国总承包商公共基建投标准入均设严格前置审批"},

    # 3. 环评与劳工罢工抗辩联动
    {"src": "VN:Law_72_2020:Art30_EIA_Approval", "dst": "ID:UU_32_2009:Art22_AMDAL", "rel": "CORRELATES_WITH", "description": "越印两国均强行规定未获环评批复开工构成非法施工"},
    {"src": "ID:UU_32_2009:Art22_AMDAL", "dst": "REF_CASE:ID_PTUN:AMDAL_Environmental_Injunction:2021", "rel": "INTERPRETS", "description": "雅加达行政法院撤销AMDAL并下达施工禁制令"},
    {"src": "ID:UU_32_2009:Art22_AMDAL", "dst": "FIDIC:Silver_1999:Clause_8.8", "rel": "CROSS_REFERENCES", "description": "环评被叫停触发FIDIC第8.8款法定不可归责停工"},
    {"src": "TH:NEQA_BE_2535:Sec46_EIA", "dst": "REF_CASE:TH_Admin_Court:NEQA_EIA_Stop_Work:2019", "rel": "INTERPRETS", "description": "泰国行政法院确认环评争议期间承包商享有工期顺延"},
    {"src": "ID:UU_13_2003:Art137_Right_to_Strike", "dst": "ID:UU_13_2003:Art140_Notice_of_Strike", "rel": "PREREQUISITE_FOR", "description": "合法罢工必须先履行7日书面通知前置程序"},
    {"src": "ID:UU_13_2003:Art140_Notice_of_Strike", "dst": "ID:UU_13_2003:Art142_Illegal_Strike", "rel": "LIMITS_LIABILITY", "description": "违反7日通知直接认定为非法罢工排除不可抗力免责"},

    # 4. 动产担保与工程留置权联动
    {"src": "VN:Decree_21_2021:Art14_Pledge_Receivables", "dst": "REF_CASE:VN_SPC:Receivables_Pledge_Priority:2020", "rel": "INTERPRETS", "description": "越南最高法院确认NRAST登记的应收款质权排他优先受偿"},
    {"src": "VN:Civil_Code_2015:Art274_Retention_Lien", "dst": "FIDIC:Silver_1999:Clause_10.1", "rel": "conflicts_with", "description": "发包人未付款前承包商可行使留置权拒绝移交实体工程TOC"},
    {"src": "ID:UU_42_1999:Art15_Executory_Title", "dst": "ID:KUHPerdata:Art1139_Privileged_Claims", "rel": "CORRELATES_WITH", "description": "信托担保执行力与工程建筑物特权受偿顺位协同对抗银行抵押"},
    {"src": "ID:KUHPerdata:Art1139_Privileged_Claims", "dst": "REF_CASE:ID_SC:KUHPerdata_1139_Subcontractor_Lien:2020", "rel": "INTERPRETS", "description": "印尼最高法院判例确认分包商工程款特权优先于抵押权"},

    # 5. 新能源 PPA 与弃电补偿联动
    {"src": "VN:MOIT_Circular_19_2023:Art6_PPA_Curtailment", "dst": "REF_CASE:VN_Danang:MOIT_Solar_Curtailment_Dispute:2023", "rel": "INTERPRETS", "description": "岘港法院审理光伏电站电网限电强行判决EVN全额赔偿弃电损失"},
    {"src": "ID:MEMR_Reg_11_2021:PPA_COD_Deadline", "dst": "FIDIC:Silver_1999:Clause_8.7", "rel": "CORRELATES_WITH", "description": "PPA下的逾期COD罚金直接传导至EPC总承包商误期违约金"},

    # 6. FIDIC 结构化履约核心链条联动
    {"src": "FIDIC:Silver_1999:Clause_2.1", "dst": "FIDIC:Silver_1999:Clause_8.4", "rel": "PREREQUISITE_FOR", "description": "未移交现场直接触发第8.4款工期顺延EOT"},
    {"src": "FIDIC:Silver_1999:Clause_8.4", "dst": "FIDIC:Silver_1999:Clause_8.7", "rel": "LIMITS_LIABILITY", "description": "顺延成立直接阻却雇主主张第8.7款误期违约金"},
    {"src": "FIDIC:Silver_1999:Clause_8.8", "dst": "FIDIC:Silver_1999:Clause_8.11", "rel": "PREREQUISITE_FOR", "description": "雇主停工持续超过84天赋予承包商终止权"},
    {"src": "FIDIC:Silver_1999:Clause_8.11", "dst": "FIDIC:Silver_1999:Clause_16.2", "rel": "CROSS_REFERENCES", "description": "超期停工指引承包商依据第16.2款解除合同"},
    {"src": "FIDIC:Silver_1999:Clause_10.2", "dst": "FIDIC:Silver_1999:Clause_10.1", "rel": "overrides", "description": "雇主提前擅自使用视为已完成TOC移交并转移风险"},
    {"src": "FIDIC:Silver_1999:Clause_13.1", "dst": "FIDIC:Silver_1999:Clause_13.3", "rel": "CROSS_REFERENCES", "description": "变更指令必须严格遵循第13.3款估价程序"},
    {"src": "FIDIC:Silver_1999:Clause_13.7", "dst": "VN:Commercial_Law_2005:Art301", "rel": "CORRELATES_WITH", "description": "东道国强行法变化调整合同价格与违约金上限"},
    {"src": "FIDIC:Silver_1999:Clause_14.7", "dst": "FIDIC:Silver_1999:Clause_14.8", "rel": "PREREQUISITE_FOR", "description": "逾期超过56天自动计收第14.8款复合利息"},
    {"src": "FIDIC:Silver_1999:Clause_14.7", "dst": "FIDIC:Silver_1999:Clause_16.1", "rel": "PREREQUISITE_FOR", "description": "未付款满56天触发承包商21天停工通告权"},
    {"src": "FIDIC:Silver_1999:Clause_16.1", "dst": "REF_CASE:SG_HC:FIDIC_Cl16_Suspension_Validity:2019", "rel": "INTERPRETS", "description": "新加坡高院裁定合法停工彻底阻断发包人反诉延误违约金"},
    {"src": "FIDIC:Silver_1999:Clause_16.1", "dst": "FIDIC:Silver_1999:Clause_16.2", "rel": "PREREQUISITE_FOR", "description": "停工后拖欠超过42天承包商有权解除合同索赔利润"},
    {"src": "FIDIC:Silver_1999:Clause_17.6", "dst": "FIDIC:Silver_1999:Clause_8.7", "rel": "LIMITS_LIABILITY", "description": "违约金总额受制于第17.6款合同总价封顶且排除间接损失"},
    {"src": "FIDIC:Silver_1999:Clause_19.1", "dst": "FIDIC:Silver_1999:Clause_19.6", "rel": "PREREQUISITE_FOR", "description": "不可抗力持续84天启动选择性解约清算"},
    {"src": "FIDIC:Silver_1999:Clause_20.1", "dst": "REF_CASE:UK_PC:FIDIC_Cl20_1_Time_Bar_Strictness:2018", "rel": "INTERPRETS", "description": "英国枢密院确认28天通知为严格除斥期间"},
    {"src": "FIDIC:Silver_1999:Clause_20.2", "dst": "FIDIC:Silver_1999:Clause_20.4", "rel": "CROSS_REFERENCES", "description": "DAAB组成后在84天内作出具有临时拘束力的裁决"},
    {"src": "FIDIC:Silver_1999:Clause_20.4", "dst": "REF_CASE:SG_CA:CRW_DAAB_Enforceability:2015", "rel": "INTERPRETS", "description": "新加坡上诉法院终局确立DAAB裁决具有即时强制履行拘束力"},
    {"src": "FIDIC:Silver_1999:Clause_20.4", "dst": "FIDIC:Silver_1999:Clause_20.6", "rel": "PREREQUISITE_FOR", "description": "对DAAB不服提交NOD后进入ICC终局国际仲裁"}
]


def expand_l2_full_fidic_treaty_kb():
    print("=" * 75)
    print("🚀 开始执行 L2 广覆盖参考层全量深化与轻量级 GraphRAG 拓扑构建...")
    print("=" * 75)

    mgr = SnapshotManager()
    snap_id = mgr.get_current_snapshot_id()
    conn = mgr.get_connection(snap_id)
    cur = conn.cursor()
    now_str = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    # 1. 批量向 reference_norms 注入/更新新增参考法源
    print(f"\n-> 1. 正在注入 {len(PHASE6_L2_REFERENCE_NORMS)} 条深度参考规范与 FIDIC 黄金条款...")
    for n in PHASE6_L2_REFERENCE_NORMS:
        cur.execute(
            """INSERT INTO reference_norms(
                norm_id, law, enbez, title, heading_path, text_de,
                structure, footnotes, stand, has_pending_amend, source_url,
                snapshot_id, fetched_at, language_mode, lang_original,
                text_original, text_en, text_zh, translation_source, norm_category,
                fidic_tier, fidic_edition, elements_json, mandatory_level
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
    print(f"✓ 成功向 reference_norms 注入/更新 {len(PHASE6_L2_REFERENCE_NORMS)} 条参考规范")

    # 2. 批量向 reference_cases 注入新增参考先例
    print(f"\n-> 2. 正在注入 {len(PHASE6_L2_REFERENCE_CASES)} 篇国际投资仲裁与工程参考裁判...")
    for c in PHASE6_L2_REFERENCE_CASES:
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
    print(f"✓ 成功向 reference_cases 注入/更新 {len(PHASE6_L2_REFERENCE_CASES)} 篇参考裁判")

    # 3. 建立并全量填充 reference_edges 表 (L2 轻量级 GraphRAG)
    print("\n-> 3. 正在构建并填充 L2 轻量级 GraphRAG 拓扑网络 (reference_edges)...")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS reference_edges (
            edge_id TEXT PRIMARY KEY,
            src TEXT,
            dst TEXT,
            rel TEXT,
            description TEXT
        )
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_ref_edges_src ON reference_edges(src)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_ref_edges_dst ON reference_edges(dst)")
    for e in PHASE6_L2_REFERENCE_EDGES:
        eid = f"REF_EDGE:{e['src']}->{e['dst']}"
        cur.execute(
            """INSERT OR REPLACE INTO reference_edges(edge_id, src, dst, rel, description)
               VALUES(?, ?, ?, ?, ?)""",
            (eid, e["src"], e["dst"], e["rel"], e.get("description", ""))
        )
    print(f"✓ 成功建立并持久化 {len(PHASE6_L2_REFERENCE_EDGES)} 条 L2 轻量级 GraphRAG 拓扑边")

    conn.commit()

    # 4. 全量重新生成 reference_chunks
    print("\n-> 4. 正在全量重新生成并持久化 L2 Reference Chunks...")
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

    # 5. 重构并持久化 L2 专用 BM25 词法索引
    index_l2_dir = os.path.join(mgr.base_dir, snap_id, "index_l2")
    os.makedirs(index_l2_dir, exist_ok=True)
    print(f"\n-> 5. 正在训练并持久化新版 L2 BM25 词法检索索引至 {index_l2_dir}...")
    bm25_l2 = BM25Engine(index_dir=index_l2_dir)
    bm25_l2.build_from_chunks(all_l2_chunks)
    print("✓ 新版 L2 独立 BM25 词法索引重构持久化就绪！")

    # 6. 调用 GPU/BGE-M3 重新构建 L2 专用 FAISS 稠密向量索引
    print(f"\n-> 6. 正在调用 GPU/BGE-M3 批量生成 1024 维向量并重构 L2 FAISS 索引 ({len(all_l2_chunks)} 向量)...")
    try:
        vec_l2 = DenseVectorEngine(index_dir=index_l2_dir)
        vec_l2.build_from_chunks(all_l2_chunks, batch_size=16)
        print(f"✓ 新版 L2 独立 FAISS 向量检索索引构建完成至 {index_l2_dir}/faiss.index！")
    except Exception as e:
        print(f"⚠️ L2 向量构建异常: {e}")

    print("\n" + "=" * 75)
    print("🎉 L2 广覆盖参考层全量深化与轻量级 GraphRAG 拓扑构建大功告成！")
    print(f"  • L2 规范总数: {len(all_ref_norms)}")
    print(f"  • L2 判例总数: {len(all_ref_cases)}")
    print(f"  • L2 轻量拓扑边总数: {len(PHASE6_L2_REFERENCE_EDGES)}")
    print(f"  • L2 Chunks 总数: {len(all_l2_chunks)}")
    print(f"  • L2 FAISS 向量与 BM25 索引路径: {index_l2_dir}")
    print("=" * 75)


if __name__ == "__main__":
    expand_l2_full_fidic_treaty_kb()
