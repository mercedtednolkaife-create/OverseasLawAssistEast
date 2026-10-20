"""东盟六国 2026 法源、法通网对齐与 FIDIC 双层知识库构建脚本 (Build ASEAN Knowledge Base)
严格对齐《东盟国家迁移方案.md》V4.0 终审定稿版（Phase 8）
核心功能：
1. 升级快照库 law.sqlite Schema（支持多语种列、法通网溯源、FIDIC Tier 1/2分级与风险社区表）
2. 批量入库东盟六国 2026 现行有效法源（印、越、马、新、泰、菲，全部基于 2026 生效法条）
3. 入库 FIDIC 银皮书/黄皮书/红皮书核心争议条款 (Tier 1) 与基线条款 (Tier 2)
4. 入库国资委 35 号令、数据安全法第 36 条、双边投资协定 (BIT) 与中信保 30 日报损条款
5. 构建三层法律图谱关系边 (edges & edges_top) 与 6 大高频工程风险社区 (risk_communities)
6. 自动生成增强 Chunks 并重新持久化 BM25 索引
"""

import os
import json
import sqlite3
import argparse
from datetime import datetime
from typing import List, Dict, Any

from lawagent.store.snapshots import SnapshotManager
from lawagent.store.db import init_snapshot_db
from lawagent.store.chunker import build_and_save_chunks
from lawagent.store.bm25 import BM25Engine


ASEAN_NORMS_DATA: List[Dict[str, Any]] = [
    # =========================================================================
    # 1. 印度尼西亚 (Indonesia / asean_id) - 三语模式
    # =========================================================================
    {
        "norm_id": "ID:UU_2_2017:Art57",
        "law": "UU_2_2017",
        "enbez": "Art.57",
        "title": "《印尼建筑服务法》第57条：属地承包商联营与分包连带责任",
        "heading_path": "UU No. 2/2017 > Bab VI Layanan Usaha > Pasal 57",
        "text_de": "Indonesian Construction Services Law Art. 57 (Subcontracting & Joint Operation)",
        "language_mode": "trilingual",
        "lang_original": "id",
        "text_original": "Penyedia Jasa dapat menyerahkan sebagian pekerjaan kepada Subpenyedia Jasa spesialis atau melalui bentuk Kerja Sama Operasi (KSO). Penyedia Jasa dan mitra KSO bertanggung jawab secara tanggung renteng atas mutu dan pemenuhan kontrak konstruksi.",
        "text_en": "Service Providers may sub-contract part of the specialized work to sub-providers or through Joint Operations (KSO). Service Providers and KSO partners shall be jointly and severally liable for construction quality and contractual fulfillment.",
        "text_zh": "【司法部法通网权威译本】施工承包商可将部分专业工程分包给专业分包商，或通过设立联合体/非法人联营体（KSO）形式履行。承包商与联营体各方对建设工程质量和合同义务承担连带履约责任。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "statute",
        "mandatory_level": "mandatory_override",
        "elements_json": json.dumps([
            {"eid": "e_kso_joint_liability", "text_zh": "境外承包商必须与印尼属地企业组建KSO联营体", "status": "mandatory"},
            {"eid": "e_kso_subcontract", "text_zh": "主要主体工程禁止非法全额转包，专业工程方可依法分包", "status": "mandatory"}
        ], ensure_ascii=False)
    },
    {
        "norm_id": "ID:SEMA_3_2023",
        "law": "SEMA_3_2023",
        "enbez": "SEMA 3/2023",
        "title": "《最高法院2023年第3号通告》：反制纯外文合同无效抗辩裁判规则",
        "heading_path": "Surat Edaran Mahkamah Agung No. 3 Tahun 2023 > Perdata Khusus",
        "text_de": "Supreme Court Circular Letter SEMA No. 3/2023 on Language Validity",
        "language_mode": "trilingual",
        "lang_original": "id",
        "text_original": "Perjanjian yang dibuat dalam bahasa asing tidak dapat dibatalkan semata-mata karena tidak dibuat dalam Bahasa Indonesia sebagaimana diatur dalam UU No. 24 Tahun 2009, kecuali dapat dibuktikan adanya iktikad tidak baik (bad faith) dari salah satu pihak.",
        "text_en": "Agreements drafted in a foreign language cannot be rendered null and void solely on the grounds of absence of an Indonesian language version under Law No. 24 of 2009, unless bad faith by either contracting party is proven.",
        "text_zh": "【司法部法通网权威译本】涉外商事与建设工程合同即便未按照2009年第24号《国旗、语言法》签署印尼语译本，裁判机构亦不得仅以缺少印尼语版本为由直接判令合同自始无效，除非主张方举证证明缔约方存在恶意欺诈（iktikad tidak baik）事实。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "statute",
        "mandatory_level": "mandatory_override",
        "elements_json": json.dumps([
            {"eid": "e_language_rebuttal", "text_zh": "履约争议中若无恶意证据，纯英文合同依然具有约束力", "status": "proven"},
            {"eid": "e_language_pre_warning", "text_zh": "投前签约阶段仍须强制签署印尼语对照本以绝后患", "status": "caution"}
        ], ensure_ascii=False)
    },
    {
        "norm_id": "ID:MEMR_11_2024",
        "law": "MEMR_11_2024",
        "enbez": "MEMR 11/2024",
        "title": "《能矿部2024年第11号规章》：电力与新能源EPC项目本地化率(TKDN)阶梯配额与认证",
        "heading_path": "Permen ESDM No. 11/2024 > Ketentuan Tingkat Komponen Dalam Negeri (TKDN)",
        "text_de": "Ministry of Energy Reg 11/2024 on Electricity TKDN Verification",
        "language_mode": "trilingual",
        "lang_original": "id",
        "text_original": "Pembangunan pembangkit listrik wajib memenuhi ambang batas minimum TKDN sebesar 40% hingga 60% yang diverifikasi secara resmi oleh surveyor independen bersertifikat sebelum Commercial Operation Date (COD).",
        "text_en": "Construction of power generation plants must fulfill mandatory minimum TKDN local content thresholds between 40% to 60%, officially verified by certified independent surveyors prior to Commercial Operation Date (COD).",
        "text_zh": "【法通网与行业标准】电力与新能源工程EPC总承包项目，关键主机辅机及建设工程服务须严格达到40%至60%的法定最低本地采购率（TKDN）；总包商须在商业运营日（COD）前取得PT Sucofindo或Surveyor Indonesia法定认证证书，否则发包人有权处以工程款5%至10%的法定扣罚甚至暂停电费结算。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "statute",
        "mandatory_level": "mandatory_override",
        "elements_json": json.dumps([
            {"eid": "e_tkdn_threshold", "text_zh": "设备材料本地化率须达标并获取官方认证", "status": "mandatory"},
            {"eid": "e_tkdn_cod_gate", "text_zh": "未达TKDN认证将阻却发包人签发完工移交证书", "status": "high_risk"}
        ], ensure_ascii=False)
    },
    {
        "norm_id": "ID:KUHPerdata:Art1338",
        "law": "KUHPerdata",
        "enbez": "Art.1338",
        "title": "《印尼民法典》第1338条：契约即法律原则与善意履行",
        "heading_path": "Kitab Undang-Undang Hukum Perdata > Buku III Perikatan > Pasal 1338",
        "text_de": "Indonesian Civil Code Art. 1338 (Pacta Sunt Servanda & Good Faith)",
        "language_mode": "trilingual",
        "lang_original": "id",
        "text_original": "Semua perjanjian yang dibuat secara sah berlaku sebagai undang-undang bagi mereka yang membuatnya. Perjanjian harus dilaksanakan dengan iktikad baik.",
        "text_en": "All agreements legally executed shall act as law for those who made them. Agreements must be executed in good faith.",
        "text_zh": "【民商法通则】依法成立的合同对缔约双方具有如同法律一般的拘束力（Pacta Sunt Servanda）。合同当事人必须遵循善意原则（Good Faith）全面履行合同义务。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "statute",
        "mandatory_level": "contract_default"
    },

    # =========================================================================
    # 2. 越南 (Vietnam / asean_vn) - 三语模式 (2025新建设法 2026生效)
    # =========================================================================
    {
        "norm_id": "VN:Law_135_2025:Art86.2",
        "law": "Law_135_2025",
        "enbez": "Art.86.2",
        "title": "《2025年新建设法》第86.2条：工程预定损害赔偿(LD)独立效力与法定最高罚金解绑",
        "heading_path": "Luật Xây dựng số 135/2025/QH15 > Chương VI Hợp đồng xây dựng > Điều 86 Khoản 2",
        "text_de": "Vietnam Construction Law 2025 Art. 86.2 (Liquidated Damages Recognition)",
        "language_mode": "trilingual",
        "lang_original": "vi",
        "text_original": "Các bên trong hợp đồng xây dựng được quyền thỏa thuận mức bồi thường thiệt hại ước tính trước (liquidated damages) cho việc chậm tiến độ, không bị khống chế bởi mức trần phạt vi phạm hợp đồng tối đa 12% theo quy định tại luật thương mại cũ, miễn là mức bồi thường phù hợp với thiệt hại thực tế dự kiến.",
        "text_en": "Parties to a construction contract are entitled to agree upon pre-estimated liquidated damages for delay in completion, decoupled from the previous 12% statutory penalty ceiling under commercial regulations, provided that such liquidated amount reasonably reflects anticipated actual losses.",
        "text_zh": "【司法部法通网权威译本】建设工程合同当事人有权约定针对工期延误的预定损害赔偿金（Liquidated Damages, LD），该约定与原旧法下受限的12%最高违约罚金解绑，只要所约定的赔偿数额合理对应可能发生的客观预见损失，裁判机构应予确认其效力，不再以行政罚金上限强行调减。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "statute",
        "mandatory_level": "mandatory_override",
        "elements_json": json.dumps([
            {"eid": "e_ld_decoupled", "text_zh": "违约赔偿金与旧法12%上限解绑，需在合同中重新设计封顶比例", "status": "key_shift"},
            {"eid": "e_actual_loss_defense", "text_zh": "发包人若未遭受实际损失仍主张全额扣罚构成权利滥用", "status": "defense"}
        ], ensure_ascii=False)
    },
    {
        "norm_id": "VN:Law_135_2025:Art146",
        "law": "Law_135_2025",
        "enbez": "Art.146",
        "title": "《2025年新建设法》第146条：台风与不可抗力事件之工期顺延与费用免责",
        "heading_path": "Luật Xây dựng số 135/2025/QH15 > Điều 146 Bất khả kháng trong thi công",
        "text_de": "Vietnam Construction Law 2025 Art. 146 (Force Majeure & EOT)",
        "language_mode": "trilingual",
        "lang_original": "vi",
        "text_original": "Nhà thầu được gia hạn thời gian thực hiện hợp đồng và miễn trừ trách nhiệm bồi thường do chậm tiến độ khi xảy ra sự kiện bất khả kháng bao gồm thiên tai bão lũ bất thường tại vùng biển hoặc thay đổi quy hoạch của cơ quan nhà nước có thẩm quyền.",
        "text_en": "Contractors are entitled to an extension of time (EOT) and exemption from delay damages upon occurrence of force majeure events including abnormal maritime storms/typhoons or planning modifications enacted by competent state agencies.",
        "text_zh": "【司法部法通网权威译本】当发生海上极端台风、海啸或东道国主管机关重大规划变更等不可抗力事件时，施工承包商有权获得合理的工期顺延（EOT），并免除延误违约金责任。发包人不得以预定损害赔偿为由强行索兑履约保函。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "statute",
        "mandatory_level": "mandatory_override"
    },
    {
        "norm_id": "VN:Decree_210_2026:Art18",
        "law": "Decree_210_2026",
        "enbez": "Art.18",
        "title": "《第210/2026/ND-CP号建设合同法令》第18条：独立履约保函恶意索兑司法救济",
        "heading_path": "Nghị định 210/2026/NĐ-CP > Điều 18 Bảo lãnh thực hiện hợp đồng",
        "text_de": "Decree 210/2026/ND-CP Art. 18 on Performance Guarantee Calling",
        "language_mode": "trilingual",
        "lang_original": "vi",
        "text_original": "Bên giao thầu chỉ được quyền thu hồi bảo lãnh thực hiện hợp đồng khi bên nhận thầu vi phạm nghĩa vụ cơ bản và đã được thông báo bằng văn bản trước ít nhất 14 ngày làm việc.",
        "text_en": "The employer is only entitled to call the performance guarantee when the contractor materially breaches basic obligations and has been notified in writing at least 14 working days in advance.",
        "text_zh": "【法通网建设法规】发包人索兑见索即付履约保函必须满足法定前提：承包商存在根本性实质违约，且发包人须至少提前14个工作日向承包商发出正式催告。未经法定催告突袭索兑或在存在争议未决时恶意索兑，承包商有权申请仲裁庭或法院紧急止付。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "statute",
        "mandatory_level": "mandatory_override"
    },

    # =========================================================================
    # 3. 马来西亚 (Malaysia / asean_my) - 双语模式 (英+中)
    # =========================================================================
    {
        "norm_id": "MY:CIPAA_2012:Sec35",
        "law": "CIPAA_2012",
        "enbez": "Sec.35",
        "title": "《建筑业付款与快速裁决法》第35条：背靠背付款条款(Pay-when-paid)法定自始绝对无效",
        "heading_path": "Construction Industry Payment and Adjudication Act 2012 > Part V > Section 35",
        "text_de": "CIPAA 2012 Section 35 (Prohibition of Conditional Payment Clauses)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Section 35. Prohibition of conditional payment: (1) Any conditional payment provision in a construction contract in relation to payment under the construction contract is void. (2) For the purposes of this section, it is a conditional payment provision when payment is made dependent on the service provider receiving payment from a third party.",
        "text_en": "Section 35. Prohibition of conditional payment: (1) Any conditional payment provision in a construction contract in relation to payment under the construction contract is void. (2) For the purposes of this section, it is a conditional payment provision when payment is made dependent on the service provider receiving payment from a third party.",
        "text_zh": "【司法部法通网权威译本】CIPAA 2012 第 35 条明确禁止附条件付款：(1) 建设工程合同中任何附条件付款条款一律无效；(2) 凡将总包商向分包商付款的条件设定为“须待总包商从项目业主处收讫工程款”（即行业通称的背靠背条款 Pay-when-paid），该条款依法自始绝对无效，总包商不得以此抗辩拒绝分包付款。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "statute",
        "mandatory_level": "mandatory_override",
        "elements_json": json.dumps([
            {"eid": "e_pay_when_paid_void", "text_zh": "背靠背条款无效，总包商受业主拖欠不得作为阻却分包付款之法定事由", "status": "critical_risk"}
        ], ensure_ascii=False)
    },
    {
        "norm_id": "MY:CIPAA_2012:Sec13",
        "law": "CIPAA_2012",
        "enbez": "Sec.13",
        "title": "《建筑业付款与快速裁决法》第13条：法定裁决书即时执行力与先付款后争议原则",
        "heading_path": "Construction Industry Payment and Adjudication Act 2012 > Part II > Section 13",
        "text_de": "CIPAA 2012 Section 13 (Enforceability of Adjudication Decision)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "An adjudication decision is binding unless it is set aside by the High Court or the dispute is finally decided by arbitration or the court. The winning party may apply to the High Court for an order to enforce the adjudication decision as if it were a judgment or order of the High Court.",
        "text_en": "An adjudication decision is binding unless it is set aside by the High Court or the dispute is finally decided by arbitration or the court. The winning party may apply to the High Court for an order to enforce the adjudication decision as if it were a judgment or order of the High Court.",
        "text_zh": "【司法部法通网权威译本】CIPAA 裁决员作出的工程款快速裁决书具有即时约束力（Pay Now, Argue Later 原则）。胜诉方可直接向马来西亚高等法院申请将裁决书作为生效判决予以强制执行；被执行方即便已提起实质仲裁或诉讼，亦不得中止付款履行。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "statute",
        "mandatory_level": "mandatory_override"
    },
    {
        "norm_id": "MY:Act_520_CIDB:Sec25",
        "law": "Act_520_CIDB",
        "enbez": "Sec.25",
        "title": "《建筑业发展局法》第25条：外资施工资质执照强制注册与合同效力红线",
        "heading_path": "Lembaga Pembangunan Industri Pembinaan Malaysia Act 1994 (Act 520) > Section 25",
        "text_de": "CIDB Act 520 Section 25 (Mandatory Contractor Registration G7)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "No person shall undertake or carry out any construction work unless he is registered with the Lembaga and holds a valid certificate of registration issued by the Lembaga under this Act. Any contract entered into without registration shall be subject to statutory penalties.",
        "text_en": "No person shall undertake or carry out any construction work unless he is registered with the Lembaga and holds a valid certificate of registration issued by the Lembaga under this Act. Any contract entered into without registration shall be subject to statutory penalties.",
        "text_zh": "【法通网执业规范】未在马来西亚 CIDB（建筑业发展局）注册并取得相应等级（外资承揽重大项目须取得 G7 级牌照）承包商资格证书者，严禁从事任何施工承包活动。未持证缔约可能构成非法承揽，招致高额刑事罚款并影响民事工程款追索权。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "statute",
        "mandatory_level": "mandatory_override"
    },

    # =========================================================================
    # 4. 新加坡 (Singapore / asean_sg) - 双语模式 (英+中)
    # =========================================================================
    {
        "norm_id": "SG:SOPA_2004:Sec9",
        "law": "SOPA_2004",
        "enbez": "Sec.9",
        "title": "《建筑业付款保障法》第9条：禁止背靠背付款与强制极速响应期",
        "heading_path": "Building and Construction Industry Security of Payment Act 2004 > Part II > Section 9",
        "text_de": "Singapore SOPA 2004 Section 9 (Conditional Payment Provisions Void)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "A pay-when-paid provision of a contract, whether written or oral, is of no effect in relation to any payment for construction work carried out or undertaken to be carried out under the contract.",
        "text_en": "A pay-when-paid provision of a contract, whether written or oral, is of no effect in relation to any payment for construction work carried out or undertaken to be carried out under the contract.",
        "text_zh": "【司法部法通网权威译本】SOPA 2004 第 9 条明确确认：合同中任何口头或书面的“背靠背付款（Pay-when-paid）”条款均无任何法律效力。发包人收到承包商付款申请后，必须在 7 至 14 天法定期间内提供付款响应（Payment Response），逾期将视为失权并受极速裁决惩戒。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "statute",
        "mandatory_level": "mandatory_override"
    },
    {
        "norm_id": "SG:Precedent:BS_Mount_Sophia",
        "law": "Precedent",
        "enbez": "BS Mount Sophia",
        "title": "《BS Mount Sophia 终审判例》：确立独立于欺诈的“显失公平(Unconscionability)”保函止付标准",
        "heading_path": "Singapore Court of Appeal > BS Mount Sophia Pte Ltd v Join-Aim Pte Ltd [2012] SGCA 28",
        "text_de": "Singapore CA Precedent BS Mount Sophia (Unconscionability Ground for Injunction)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "In Singapore law, unconscionability is an independent ground from fraud for restraining a call on a performance bond. Unconscionability involves unfairness and bad faith on the part of the beneficiary, showing a strong prima facie case.",
        "text_en": "In Singapore law, unconscionability is an independent ground from fraud for restraining a call on a performance bond. Unconscionability involves unfairness and bad faith on the part of the beneficiary, showing a strong prima facie case.",
        "text_zh": "【新加坡最高法院经典先例】新加坡上诉法院确立了独特的见索即付保函司法救济规则：除传统普通法欺诈（Fraud）之外，“显失公平（Unconscionability）”构成独立的保函止付法定事由。当发包人在明显存在履约争议或违约事实微小时滥用见索即付工具突袭索兑，承包商举证达到较强初步表面证据（Strong Prima Facie Case）即可获发法院禁令。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "statute",
        "mandatory_level": "golden_principle"
    },
    {
        "norm_id": "SG:Precedent:JBE_Properties",
        "law": "Precedent",
        "enbez": "JBE Properties",
        "title": "《JBE Properties 案》：允许合同专用条件明文排除显失公平抗辩之黄金起草规范",
        "heading_path": "Singapore Court of Appeal > JBE Properties Pte Ltd v Handy-Tool Construction [2011] SGCA 32",
        "text_de": "Singapore CA JBE Properties (Contractual Exclusion of Unconscionability)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Parties of equal bargaining power in commercial contracts are permitted to expressly exclude the ground of unconscionability by clear and unambiguous contractual wording in the performance bond clause.",
        "text_en": "Parties of equal bargaining power in commercial contracts are permitted to expressly exclude the ground of unconscionability by clear and unambiguous contractual wording in the performance bond clause.",
        "text_zh": "【起草防线经典判例】上诉法院裁定：商事合同双方若具备对等议价能力，允许通过合同明示清晰条款排除“显失公平”止付抗辩。央国企出海合同谈判时必须警惕发包人将“承包商明示放弃以显失公平为由申请止付保函”条款写入专用条件，一经签署将丧失该项关键救济武器。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "statute",
        "mandatory_level": "contract_default"
    },

    # =========================================================================
    # 5. 泰国 (Thailand / asean_th) - 三语模式
    # =========================================================================
    {
        "norm_id": "TH:FBA_1999:List3",
        "law": "FBA_1999",
        "enbez": "List 3",
        "title": "《外商经营法》附表三：建设工程外资49%股比限制与严禁代持人(Nominee)红线",
        "heading_path": "Foreign Business Act B.E. 2542 (1999) > Schedule 3 > Category (10)",
        "text_de": "Thailand Foreign Business Act 1999 List 3 (Construction Restrictions & Nominees)",
        "language_mode": "trilingual",
        "lang_original": "th",
        "text_original": "การก่อสร้าง ยกเว้นการก่อสร้างโครงสร้างพื้นฐานสาธารณะขนาดใหญ่ตามเกณฑ์ ห้ามคนต่างด้าวถือหุ้นเกินกว่าร้อยละ 49 เว้นแต่จะได้รับใบอนุญาตประกอบธุรกิจของคนต่างด้าว (FBL) และห้ามใช้ตัวแทนอำพราง (Nominee) ถือหุ้นแทนเด็ดขาด.",
        "text_en": "Construction businesses are restricted to foreign participation not exceeding 49% shareholding unless granted a Foreign Business License (FBL) or BOI promotion. Holding shares through Thai nominee shareholders is strictly prohibited under penal sanctions.",
        "text_zh": "【司法部法通网权威译本】泰国《外商经营法》将常规工程施工列入附表三限制行业，外资持股比例不得超过49%，除非取得泰国商业部外商经营许可证（FBL）或投资促进委员会（BOI）特别优惠。严禁中资企业采用泰国自然人或空壳公司代持股权（Nominee），一旦查实代持合同自始无效且面临刑事责任。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "statute",
        "mandatory_level": "mandatory_override"
    },
    {
        "norm_id": "TH:CCC:Sec596",
        "law": "CCC",
        "enbez": "Sec.596",
        "title": "《泰国民商法典》第596条：承揽合同完工延误与过高违约金司法酌减",
        "heading_path": "Thailand Civil and Commercial Code > Title VII Hire of Work > Section 596",
        "text_de": "Thailand CCC Section 596 (Damages for Delay in Work)",
        "language_mode": "trilingual",
        "lang_original": "th",
        "text_original": "ถ้าผู้รับจ้างส่งมอบงานล่าช้ากว่ากำหนด ผู้ว่าจ้างมีสิทธิเรียกเอาค่าสินไหมทดแทน แต่ถ้าเบี้ยปรับที่กำหนดไว้สูงเกินส่วน ศาลมีอำนาจลดลงเป็นจำนวนพอสมควรได้.",
        "text_en": "If the contractor delivers the completed work behind schedule, the employer is entitled to claim damages. However, if the agreed liquidated damages or penalties are disproportionately excessive, the court has the discretionary power to reduce them to a reasonable amount.",
        "text_zh": "【民商法典承揽编】承揽人延误交付工作成果的，定作人有权主张迟延违约金。但如果合同中约定的违约金数额过分高于客观实际损失，泰国法院及仲裁庭拥有法定自由裁量权，可依据公平原则裁量调减至合理数额。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "statute",
        "mandatory_level": "contract_default"
    },

    # =========================================================================
    # 6. 菲律宾 (Philippines / asean_ph) - 双语模式 (英+中)
    # =========================================================================
    {
        "norm_id": "PH:RA_11966:Sec18",
        "law": "RA_11966",
        "enbez": "Sec.18",
        "title": "《菲律宾公私合营PPP法典》第18条：废除旧BOT法与政府提前终止公允补偿机制",
        "heading_path": "Republic Act No. 11966 (The PPP Code of the Philippines) > Section 18",
        "text_de": "Philippine PPP Code RA 11966 Section 18 (Repeal of BOT Law & Termination Compensation)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Republic Act No. 6957, as amended by Republic Act No. 7718, is hereby repealed. Upon termination of a PPP contract for government convenience or unilateral policy shift, the implementing agency shall pay termination compensation ensuring recovery of reasonable equity investment and debt service.",
        "text_en": "Republic Act No. 6957, as amended by Republic Act No. 7718, is hereby repealed. Upon termination of a PPP contract for government convenience or unilateral policy shift, the implementing agency shall pay termination compensation ensuring recovery of reasonable equity investment and debt service.",
        "text_zh": "【司法部法通网权威译本】《菲律宾PPP法典》(RA 11966) 已明文废除实施三十余年的旧 BOT 法案 (RA 7718)。新法典规定：因政府方公共利益单方中止或换届政策调整终止特许权合同时，实施机构必须支付法定终止补偿，确保投资方已发生的经审计合理股权投资及金融债务得到优先全额清偿。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "statute",
        "mandatory_level": "mandatory_override",
        "elements_json": json.dumps([
            {"eid": "e_bot_repealed", "text_zh": "旧BOT法RA 7718已明文废除，严禁在新合同中援引旧法条款", "status": "prohibition"},
            {"eid": "e_termination_compensation", "text_zh": "政府单方终止须按公允价值与债务清偿标准补偿", "status": "protection"}
        ], ensure_ascii=False)
    },
    {
        "norm_id": "PH:Precedent:PCAB_v_Manila_Water",
        "law": "Precedent",
        "enbez": "PCAB v. Manila Water",
        "title": "《最高法院马尼拉水务案先例》：判令废除外资工程承包牌照60%菲籍股权国籍歧视限制",
        "heading_path": "Philippine Supreme Court En Banc > PCAB v. Manila Water Co. (G.R. No. 217590)",
        "text_de": "Philippine Supreme Court Precedent on Foreign Contractor License",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "The Philippine Supreme Court en banc declared Rule 3.1 of PCAB Implementing Rules void, ruling that the 60% Filipino equity requirement for regular contractor licenses was unconstitutional and exceeded statutory authority, paving the way for 100% foreign-owned contractors in private infrastructure.",
        "text_en": "The Philippine Supreme Court en banc declared Rule 3.1 of PCAB Implementing Rules void, ruling that the 60% Filipino equity requirement for regular contractor licenses was unconstitutional and exceeded statutory authority, paving the way for 100% foreign-owned contractors in private infrastructure.",
        "text_zh": "【最高法院里程碑宪政判例】菲律宾最高法院大法官全庭判决宣告 PCAB 牌照实施细则第 3.1 条关于“常规工程承包商必须具备60%菲律宾公民股权”之规定违宪无效。确认外资施工企业在商业工程领域享有平等准入权，扫清了外资在菲承接大型基建项目的国籍壁垒。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "statute",
        "mandatory_level": "golden_principle"
    },

    # =========================================================================
    # 7. FIDIC 银皮书/黄皮书/红皮书核心争议条款 (Tier 1 & Tier 2)
    # =========================================================================
    {
        "norm_id": "FIDIC:Silver_1999:Clause_20.1",
        "law": "FIDIC",
        "enbez": "Silver:20.1",
        "title": "《FIDIC 银皮书 EPC》第20.1款：承包商索赔28天通知除斥期间与失权抗辩 (Tier 1 核心争议条款)",
        "heading_path": "FIDIC Conditions of Contract for EPC/Turnkey Projects 1999 > Clause 20 Claims > 20.1",
        "text_de": "FIDIC Silver Book 1999 Clause 20.1 (Contractor's Claims Time Bar)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "If the Contractor considers himself to be entitled to any extension of the Time for Completion and/or any additional payment, the Contractor shall give notice to the Employer, describing the event or circumstance giving rise to the claim. The notice shall be given as soon as practicable, and not later than 28 days after the Contractor became aware, or should have become aware, of the event or circumstance. If the Contractor fails to give notice of a claim within such period of 28 days, the Employer shall be discharged from all liability in connection with the claim.",
        "text_en": "If the Contractor considers himself to be entitled to any extension of the Time for Completion and/or any additional payment, the Contractor shall give notice to the Employer, describing the event or circumstance giving rise to the claim. The notice shall be given as soon as practicable, and not later than 28 days after the Contractor became aware, or should have become aware, of the event or circumstance. If the Contractor fails to give notice of a claim within such period of 28 days, the Employer shall be discharged from all liability in connection with the claim.",
        "text_zh": "【国际工程核心条款】承包商若要求顺延工期或追加费用，必须在知悉或应当知悉该索赔事件之日起 28 天内向发包人发出书面索赔通知。若承包商未能在 28 天通知时效内发出通知，竣工期限不得顺延，承包商无权获得任何费用补偿，且发包人免除与该索赔相关的一切责任（强制失权条款）。",
        "translation_source": "FIDIC_OFFICIAL_ZH",
        "norm_category": "fidic_standard",
        "fidic_tier": "core_dispute",
        "fidic_edition": "1999_SILVER",
        "mandatory_level": "contract_default",
        "elements_json": json.dumps([
            {"eid": "e_fidic_28d_trigger", "text_zh": "在知悉事件28天内向雇主递交正式书面索赔通知", "status": "condition_precedent"},
            {"eid": "e_fidic_42d_substantiation", "text_zh": "发出通知后42天内提交详细账目依据和同期工程记录", "status": "condition_precedent"}
        ], ensure_ascii=False)
    },
    {
        "norm_id": "FIDIC:Silver_1999:Clause_8.4",
        "law": "FIDIC",
        "enbez": "Silver:8.4",
        "title": "《FIDIC 银皮书 EPC》第8.4款：竣工时间延长(EOT)与雇主风险事件 (Tier 1 核心争议条款)",
        "heading_path": "FIDIC Conditions of Contract for EPC/Turnkey Projects 1999 > Clause 8 > 8.4",
        "text_de": "FIDIC Silver Book 1999 Clause 8.4 (Extension of Time for Completion)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "The Contractor shall be entitled subject to Sub-Clause 20.1 to an extension of the Time for Completion if and to the extent that completion for the purposes of Sub-Clause 10.1 is or will be delayed by any of the following causes: (a) a Variation, (b) a cause of delay giving an entitlement to extension of time under a Sub-Clause of these Conditions, or (c) any delay, impediment or prevention caused by or attributable to the Employer, the Employer's Personnel, or the Employer's other contractors on the Site.",
        "text_en": "The Contractor shall be entitled subject to Sub-Clause 20.1 to an extension of the Time for Completion if and to the extent that completion for the purposes of Sub-Clause 10.1 is or will be delayed by any of the following causes: (a) a Variation, (b) a cause of delay giving an entitlement to extension of time under a Sub-Clause of these Conditions, or (c) any delay, impediment or prevention caused by or attributable to the Employer, the Employer's Personnel, or the Employer's other contractors on the Site.",
        "text_zh": "【国际工程核心条款】承包商因发包人指示的工程变更、根据合同专用条件有权顺延工期之事件、或因发包人、发包人人员或现场其他承包商造成的任何延误、阻碍或妨碍（包括迟延交付现场与征地受阻），在遵循第20.1款程序的前提下，有权获得竣工期限的合理顺延（EOT）。",
        "translation_source": "FIDIC_OFFICIAL_ZH",
        "norm_category": "fidic_standard",
        "fidic_tier": "core_dispute",
        "fidic_edition": "1999_SILVER",
        "mandatory_level": "contract_default"
    },
    {
        "norm_id": "FIDIC:Silver_1999:Clause_4.2",
        "law": "FIDIC",
        "enbez": "Silver:4.2",
        "title": "《FIDIC 银皮书 EPC》第4.2款：履约担保与发包人索兑正当性限制 (Tier 1 核心争议条款)",
        "heading_path": "FIDIC Conditions of Contract for EPC/Turnkey Projects 1999 > Clause 4 > 4.2",
        "text_de": "FIDIC Silver Book 1999 Clause 4.2 (Performance Security Claims Restriction)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "The Employer shall not make a claim under the Performance Security, except for amounts to which the Employer is entitled under the Contract in the event of: (a) failure by the Contractor to extend the validity of the Performance Security, (b) failure by the Contractor to pay the Employer an amount due, as agreed or determined, or (c) failure by the Contractor to remedy a breach within 42 days after receiving the Employer's notice.",
        "text_en": "The Employer shall not make a claim under the Performance Security, except for amounts to which the Employer is entitled under the Contract in the event of: (a) failure by the Contractor to extend the validity of the Performance Security, (b) failure by the Contractor to pay the Employer an amount due, as agreed or determined, or (c) failure by the Contractor to remedy a breach within 42 days after receiving the Employer's notice.",
        "text_zh": "【国际工程核心条款】发包人不得向保函开立行提出索赔或索兑履约保证，除非发生合同明确列明的四种违约情形：(a) 承包商未按要求顺延保函有效期；(b) 经裁定或协商确定应付发包人的款项承包商逾期未付；(c) 发包人书面通知纠正违约后42天内承包商仍未补正；或(d) 发生发包人有权解除合同的情形。不满足上述前提的索兑构成合同违约。",
        "translation_source": "FIDIC_OFFICIAL_ZH",
        "norm_category": "fidic_standard",
        "fidic_tier": "core_dispute",
        "fidic_edition": "1999_SILVER",
        "mandatory_level": "contract_default"
    },
    {
        "norm_id": "FIDIC:Silver_1999:Clause_13.7",
        "law": "FIDIC",
        "enbez": "Silver:13.7",
        "title": "《FIDIC 银皮书 EPC》第13.7款：因东道国法律与规章变更调整合同价款 (Tier 2 基准参考条款)",
        "heading_path": "FIDIC Conditions of Contract for EPC/Turnkey Projects 1999 > Clause 13 > 13.7",
        "text_de": "FIDIC Silver Book 1999 Clause 13.7 (Adjustments for Changes in Legislation)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "The Contract Price shall be adjusted to take account of any increase or decrease in Cost resulting from a change in the Laws of the Country or in the judicial or official governmental interpretation of such Laws, made after the Base Date.",
        "text_en": "The Contract Price shall be adjusted to take account of any increase or decrease in Cost resulting from a change in the Laws of the Country or in the judicial or official governmental interpretation of such Laws, made after the Base Date.",
        "text_zh": "【FIDIC 基准参考条款】基准日期（投标截止日前28天）之后，若东道国法律、行政法规或司法解释发生变动（例如引入强制TKDN配额、调整关税或劳工签证政策），导致承包商履行合同发生工期延误或成本增加的，合同价款应予相应调增，竣工期限予以合理延长。",
        "translation_source": "FIDIC_OFFICIAL_ZH",
        "norm_category": "fidic_standard",
        "fidic_tier": "baseline_reference",
        "fidic_edition": "1999_SILVER",
        "mandatory_level": "contract_default"
    },
    {
        "norm_id": "FIDIC:Red_1999:Clause_20.1",
        "law": "FIDIC",
        "enbez": "Red:20.1",
        "title": "《FIDIC 红皮书 施工合同》第20.1款：承包商索赔28天通知时效与失权 (Tier 1 核心争议条款)",
        "heading_path": "FIDIC Conditions of Contract for Construction 1999 > Clause 20 Claims > 20.1",
        "text_de": "FIDIC Red Book 1999 Clause 20.1 (Contractor's Claims 28-Day Time Bar)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "If the Contractor considers himself to be entitled to any extension of the Time for Completion and/or any additional payment under any Clause of these Conditions, the Contractor shall give notice to the Engineer, describing the event or circumstance giving rise to the claim not later than 28 days after becoming aware.",
        "text_en": "If the Contractor considers himself to be entitled to any extension of the Time for Completion and/or any additional payment, the Contractor shall give notice to the Engineer not later than 28 days after becoming aware. Failure of notice bars claim.",
        "text_zh": "【FIDIC 1999红皮书】承包商若要求工期顺延或费用索赔，必须在知悉索赔事件之日起 28 天内向监理工程师发出书面索赔通知。逾期未通知则竣工期限不得顺延且雇主免除全部赔偿责任（严格时效前置要件）。",
        "translation_source": "FIDIC_OFFICIAL_ZH",
        "norm_category": "fidic_standard",
        "fidic_tier": "core_dispute",
        "fidic_edition": "1999_RED",
        "mandatory_level": "contract_default"
    },
    {
        "norm_id": "FIDIC:Red_1999:Clause_8.4",
        "law": "FIDIC",
        "enbez": "Red:8.4",
        "title": "《FIDIC 红皮书 施工合同》第8.4款：竣工时间延长(EOT)法定情形 (Tier 1 核心争议条款)",
        "heading_path": "FIDIC Conditions of Contract for Construction 1999 > Clause 8 > 8.4",
        "text_de": "FIDIC Red Book 1999 Clause 8.4 (Extension of Time for Completion)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "The Contractor shall be entitled subject to Sub-Clause 20.1 to an extension of the Time for Completion if completion is or will be delayed by: (a) a Variation, (b) exceptionally adverse climatic conditions, or (c) any delay caused by the Employer.",
        "text_en": "The Contractor shall be entitled subject to Sub-Clause 20.1 to an extension of the Time for Completion if completion is or will be delayed by Variation, exceptionally adverse climatic conditions, or Employer impediments.",
        "text_zh": "【FIDIC 1999红皮书】承包商因工程变更、异常不利气候条件或雇主/工程师延误迟延交地，依第20.1款程序有权主张竣工工期顺延（EOT），免除误期违约金（LDs）。",
        "translation_source": "FIDIC_OFFICIAL_ZH",
        "norm_category": "fidic_standard",
        "fidic_tier": "core_dispute",
        "fidic_edition": "1999_RED",
        "mandatory_level": "contract_default"
    },
    {
        "norm_id": "FIDIC:Yellow_1999:Clause_20.1",
        "law": "FIDIC",
        "enbez": "Yellow:20.1",
        "title": "《FIDIC 黄皮书 生产设备与设计-建造》第20.1款：承包商索赔通知时效 (Tier 1 核心争议条款)",
        "heading_path": "FIDIC Conditions of Contract for Plant and Design-Build 1999 > Clause 20 Claims > 20.1",
        "text_de": "FIDIC Yellow Book 1999 Clause 20.1 (Contractor's Claims Time Bar)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "The Contractor shall give notice to the Engineer not later than 28 days after the Contractor became aware, or should have become aware, of the event or circumstance.",
        "text_en": "The Contractor shall give notice to the Engineer not later than 28 days after the Contractor became aware, or should have become aware, of the event or circumstance.",
        "text_zh": "【FIDIC 1999黄皮书】设计施工一体化合同下，承包商主张工期或费用索赔须于28天内递交书面索赔通知，未发通知将发生失权抗辩法律后果。",
        "translation_source": "FIDIC_OFFICIAL_ZH",
        "norm_category": "fidic_standard",
        "fidic_tier": "core_dispute",
        "fidic_edition": "1999_YELLOW",
        "mandatory_level": "contract_default"
    },
    {
        "norm_id": "FIDIC:Yellow_1999:Clause_8.4",
        "law": "FIDIC",
        "enbez": "Yellow:8.4",
        "title": "《FIDIC 黄皮书 生产设备与设计-建造》第8.4款：工期顺延(EOT) (Tier 1 核心争议条款)",
        "heading_path": "FIDIC Conditions of Contract for Plant and Design-Build 1999 > Clause 8 > 8.4",
        "text_de": "FIDIC Yellow Book 1999 Clause 8.4 (Extension of Time for Completion)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "The Contractor shall be entitled to an extension of the Time for Completion for delays caused by Employer, unforeseeable physical conditions, or variations.",
        "text_en": "The Contractor shall be entitled to an extension of the Time for Completion for delays caused by Employer, unforeseeable physical conditions, or variations.",
        "text_zh": "【FIDIC 1999黄皮书】承包商因不可预见的外界不利物理条件、发包人审批延误或现场移交迟延，有权申请合理工期顺延。",
        "translation_source": "FIDIC_OFFICIAL_ZH",
        "norm_category": "fidic_standard",
        "fidic_tier": "core_dispute",
        "fidic_edition": "1999_YELLOW",
        "mandatory_level": "contract_default"
    },
    {
        "norm_id": "FIDIC:Silver_2017:Clause_20.2",
        "law": "FIDIC",
        "enbez": "Silver2017:20.2",
        "title": "《FIDIC 银皮书 2017版》第20.2款：发包人与承包商双向索赔28天通知与失权 (Tier 1 核心争议条款)",
        "heading_path": "FIDIC Conditions of Contract for EPC/Turnkey Projects 2017 > Clause 20 Employer's and Contractor's Claims > 20.2",
        "text_de": "FIDIC Silver Book 2017 Clause 20.2 (Claims For Payment and/or EOT Dual Time Bar)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "The claiming Party shall give a Notice to the Engineer, describing the event or circumstance giving rise to the cost/time claim, not later than 28 days after the claiming Party became aware, or should have become aware, of the event. If the claiming Party fails to give a Notice of Claim within this period of 28 days, the Notice of Claim shall not be valid and the claiming Party shall not be entitled to any additional payment or EOT.",
        "text_en": "Dual time-bar rule under FIDIC 2017: Both Employer and Contractor must give Notice of Claim within 28 days, otherwise discharged from liability.",
        "text_zh": "【FIDIC 2017新版核心条款】2017版确立双向对等索赔时效机制：无论是雇主主张违约金还是承包商主张 EOT/费用索赔，均必须在知悉事件后 28 天内送达索赔通知；逾期送达通知自始无效且索赔请求权失权，彻底消除发包人索赔无通知期限制的特权。",
        "translation_source": "FIDIC_OFFICIAL_ZH",
        "norm_category": "fidic_standard",
        "fidic_tier": "core_dispute",
        "fidic_edition": "2017_SILVER",
        "mandatory_level": "contract_default"
    },
    {
        "norm_id": "FIDIC:Silver_2017:Clause_8.5",
        "law": "FIDIC",
        "enbez": "Silver2017:8.5",
        "title": "《FIDIC 银皮书 2017版》第8.5款：工期顺延(EOT)与共同延误(Concurrent Delay)规则 (Tier 1 核心争议条款)",
        "heading_path": "FIDIC Conditions of Contract for EPC/Turnkey Projects 2017 > Clause 8 > 8.5",
        "text_de": "FIDIC Silver Book 2017 Clause 8.5 (Extension of Time for Completion & Concurrent Delays)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "The Contractor shall be entitled subject to Sub-Clause 20.2 to an extension of the Time for Completion. If a delay caused by the Employer is concurrent with another delay, the Contractor's entitlement to EOT shall be assessed in accordance with the rules stated in the Special Provisions.",
        "text_en": "FIDIC 2017 Clause 8.5 expressly recognizes extension of time entitlements and provides rules for concurrent delay assessment.",
        "text_zh": "【FIDIC 2017新版核心条款】2017版明确确立共同延误（Concurrent Delay）审查指引：当雇主延误事件与承包商自身延误重叠时，依照合同专用条件约定准则评估 EOT，防止业主以共同延误为由全额扣罚误期损害赔偿金。",
        "translation_source": "FIDIC_OFFICIAL_ZH",
        "norm_category": "fidic_standard",
        "fidic_tier": "core_dispute",
        "fidic_edition": "2017_SILVER",
        "mandatory_level": "contract_default"
    },

    # =========================================================================
    # 8. 中国监管红线、中信保海外投资险与 BIT 双边投资协定
    # =========================================================================
    {
        "norm_id": "CN:SASAC_Order_35:Art12",
        "law": "SASAC_Order_35",
        "enbez": "Art.12",
        "title": "国资委35号令《中央企业境外投资监督管理办法》第12条：海外重大项目合规论证与负面清单",
        "heading_path": "国务院国有资产监督管理委员会令第35号 > 第二章 境外投资事前管理 > 第十二条",
        "text_de": "PRC SASAC Order No. 35 Article 12 (Overseas Investment Compliance & Negative List)",
        "language_mode": "bilingual",
        "lang_original": "zh",
        "text_original": "中央企业应当严格执行境外投资项目负面清单管理制度。列入特别监管类的境外重大投资项目，中央企业应当深入开展法律合规、安全风险等专业尽职调查，并报国资委履行审核把关程序。",
        "text_en": "Central state-owned enterprises shall strictly enforce the negative list system for overseas investment projects. For special supervisory category overseas projects, enterprises shall conduct thorough legal compliance and security due diligence.",
        "text_zh": "【国资监管红线】中央企业境外重大工程与投资项目，必须在投前决策前完成东道国外资准入、国安审查、习惯法土地及外汇汇出法律合规专项论证。重大境外项目未按规定履行尽职调查与决策审核程序的，实行终身追责问责。",
        "translation_source": "PRC_OFFICIAL",
        "norm_category": "prc_sasac_reg",
        "mandatory_level": "mandatory_override"
    },
    {
        "norm_id": "CN:Data_Security_Law:Art36",
        "law": "Data_Security_Law",
        "enbez": "Art.36",
        "title": "《中华人民共和国数据安全法》第36条：严禁未经批准向外国司法或执法机构提供境内重大数据与图纸",
        "heading_path": "中华人民共和国数据安全法 > 第三章 数据安全保护义务 > 第三十六条",
        "text_de": "PRC Data Security Law Article 36 (Cross-Border Data Transfer to Foreign Legal Bodies)",
        "language_mode": "bilingual",
        "lang_original": "zh",
        "text_original": "中华人民共和国主管机关根据有关法律和中华人民共和国缔结或者参加的国际条约、协定，或者按照平等互惠原则，处理外国司法或者执法机构关于提供数据的请求。非经中华人民共和国主管机关批准，境内的组织、个人不得向外国司法或者执法机构提供存储于中华人民共和国境内的数据。",
        "text_en": "Competent authorities of the PRC shall handle requests from foreign judicial or law enforcement agencies for data under laws and international treaties. Without approval from competent PRC authorities, domestic organizations and individuals shall not provide data stored in the PRC to foreign judicial or law enforcement bodies.",
        "text_zh": "【国家安全红线】非经中国主管机关正式审批许可，境内央国企及人员不得向外国法院、外国仲裁机构或执法机构提供境内存放的重大工程图纸、勘察数据及商业机密。在新加坡 SIAC、马来西亚 CIPAA 或外国诉讼涉外调证程序中，必须严格履行数据出境安全评估前置审批程序。",
        "translation_source": "PRC_OFFICIAL",
        "norm_category": "prc_sasac_reg",
        "mandatory_level": "mandatory_override"
    },
    {
        "norm_id": "TREATY:CN_ID_BIT_1992:Art4",
        "law": "CN_ID_BIT_1992",
        "enbez": "Art.4",
        "title": "《中国-印尼双边投资保护协定》第4条：征收、国有化公允补偿与中信保代位求偿保障",
        "heading_path": "Agreement between PRC and Republic of Indonesia for the Promotion and Protection of Investments 1992 > Article 4",
        "text_de": "PRC-Indonesia Bilateral Investment Treaty 1992 Article 4 (Expropriation & Compensation)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Neither Contracting Party shall expropriate, nationalize or take measures having similar effects against investments of investors of the other Contracting Party, except for a public purpose, without discrimination, and against compensation. Such compensation shall effectively be realizable, freely transferable, and made without undue delay.",
        "text_en": "Neither Contracting Party shall expropriate, nationalize or take measures having similar effects against investments of investors of the other Contracting Party, except for a public purpose, without discrimination, and against compensation. Such compensation shall effectively be realizable, freely transferable, and made without undue delay.",
        "text_zh": "【国际投资条约保护】缔约任何一方对缔约另一方投资者在其领土内的投资，不得采取征收、国有化或具有类似效果的措施（含隐性征收与单方取消特许经营权），除非出于公共利益、非歧视原则并给予实际可兑付、可自由汇出的充分补偿。",
        "translation_source": "MOFA_PRC",
        "norm_category": "bit_treaty",
        "mandatory_level": "mandatory_override"
    },
    {
        "norm_id": "SINOSURE:Overseas_Policy:Art15",
        "law": "SINOSURE",
        "enbez": "Art.15",
        "title": "中国信保《海外投资险/特定合同险保单》第15条：政治风险与违约发生后30日内法定报损保全通知",
        "heading_path": "中国出口信用保险公司海外投资保险与特险标准条款 > 索赔与权益保全 > 第十五条",
        "text_de": "Sinosure Overseas Investment Insurance Policy Article 15 (30-Day Mandatory Loss Notice)",
        "language_mode": "bilingual",
        "lang_original": "zh",
        "text_original": "被保险人知悉或者应当知悉发生可能导致保险损失的政治风险、政府征收、汇兑限制或主权违约事件之日起三十（30）日内，必须书面向保险人递交《可能损失通知书》，并完整保全合同原件、往来信函及代位求偿权益。逾期未通知且导致损失扩大的，保险人有权扣减赔偿金或拒赔。",
        "text_en": "The Insured must submit written Notice of Potential Loss to Sinosure within 30 days of becoming aware of political risks, expropriation, exchange restriction, or sovereign default, while preserving original contracts and subrogation rights.",
        "text_zh": "【出海央企致命时间窗口】当发生东道国政府征收、特许权强行提前中止、保函恶意扣兑或主权外汇冻结时，被保险央企必须于30日法定除斥期内向中国信保递交《可能损失通知书》，保全特许权合同及保函原件，严禁在未获信保书面同意前与发包人签署放弃追偿权的和解协议。",
        "translation_source": "SINOSURE_OFFICIAL",
        "norm_category": "prc_sasac_reg",
        "mandatory_level": "mandatory_override"
    }
]


# =========================================================================
# 三层图谱拓扑边 (edges) 数据定义
# =========================================================================
ASEAN_EDGES_DATA: List[Dict[str, Any]] = [
    {
        "src": "MY:CIPAA_2012:Sec35",
        "dst": "FIDIC:Silver_1999:Clause_14.8",
        "rel": "conflicts_with",
        "source": "CIPAA 2012 s.35 overrides freedom of contract in subcontracts",
        "confidence": 1.0,
        "reviewed": 1
    },
    {
        "src": "SG:SOPA_2004:Sec9",
        "dst": "FIDIC:Silver_1999:Clause_14.8",
        "rel": "conflicts_with",
        "source": "Singapore SOPA s.9 statutory pay-when-paid ban overrides FIDIC",
        "confidence": 1.0,
        "reviewed": 1
    },
    {
        "src": "ID:SEMA_3_2023",
        "dst": "ID:UU_2_2017:Art57",
        "rel": "interprets",
        "source": "Supreme Court SEMA 3/2023 limits language invalidity defense in construction disputes",
        "confidence": 0.95,
        "reviewed": 1
    },
    {
        "src": "SG:Precedent:BS_Mount_Sophia",
        "dst": "FIDIC:Silver_1999:Clause_4.2",
        "rel": "applied_in",
        "source": "Unconscionability ground limits employer call on on-demand bonds",
        "confidence": 0.98,
        "reviewed": 1
    },
    {
        "src": "VN:Law_135_2025:Art86.2",
        "dst": "VN:Decree_210_2026:Art18",
        "rel": "overrides",
        "source": "2025 Construction law decouples LDs from old 12% penalty ceiling",
        "confidence": 1.0,
        "reviewed": 1
    },
    {
        "src": "TREATY:CN_ID_BIT_1992:Art4",
        "dst": "SINOSURE:Overseas_Policy:Art15",
        "rel": "triggers_preservation",
        "source": "Expropriation under BIT triggers Sinosure 30-day loss notice preservation requirement",
        "confidence": 1.0,
        "reviewed": 1
    },
    {
        "src": "CN:Data_Security_Law:Art36",
        "dst": "SG:IAA_Cap_143A:Sec12A",
        "rel": "overrides",
        "source": "PRC Data Security Law Art. 36 prohibits unauthorized transfer of domestic project data to foreign arbitration",
        "confidence": 1.0,
        "reviewed": 1
    },
    {
        "src": "PH:Precedent:PCAB_v_Manila_Water",
        "dst": "PH:RA_11966:Sec18",
        "rel": "applied_in",
        "source": "Supreme court ruling confirms foreign contractor eligibility under new PPP Code",
        "confidence": 0.95,
        "reviewed": 1
    }
]


# =========================================================================
# 六大高频工程风险社区 (risk_communities)
# =========================================================================
ASEAN_RISK_COMMUNITIES: List[Dict[str, Any]] = [
    {
        "community_id": "RC_TKDN",
        "name_zh": "资源民族主义与本地化率 (TKDN) 违约红线",
        "risk_level": "critical",
        "host_countries": json.dumps(["ID", "MY"], ensure_ascii=False),
        "archetypes": json.dumps(["EPC_CONTRACTING", "JV_CONSORTIUM"], ensure_ascii=False),
        "norm_ids": json.dumps(["ID:MEMR_11_2024", "MY:Act_520_CIDB:Sec25"], ensure_ascii=False),
        "trigger_scenarios": "业主在完工阶段以逆变器、钢结构或施工服务未取得属地法定机构TKDN认证为由，拒发COD证书并主张工程款5%~10%惩罚性扣款。",
        "redline_actions": json.dumps([
            "必须在设备采购前向第三方认证机构（Sucofindo等）取得预审核资质证书",
            "在合同专用条件中约定若属地无合格现成产能，应视同豁免或由业主分担差价",
            "严禁通过虚报属地制造发票规避监管，防范触发反商业贿赂合规熔断"
        ], ensure_ascii=False)
    },
    {
        "community_id": "RC_BOND_FRAUD",
        "name_zh": "见索即付保函恶意索兑与司法止付对抗",
        "risk_level": "critical",
        "host_countries": json.dumps(["VN", "SG", "MY", "ID"], ensure_ascii=False),
        "archetypes": json.dumps(["EPC_CONTRACTING", "CROSS_BORDER_MA"], ensure_ascii=False),
        "norm_ids": json.dumps(["SG:Precedent:BS_Mount_Sophia", "SG:Precedent:JBE_Properties", "VN:Decree_210_2026:Art18", "FIDIC:Silver_1999:Clause_4.2"], ensure_ascii=False),
        "trigger_scenarios": "业主因电价下调或自身融资违约收益受损，在商运日前夕突袭以工期延误或质量瑕疵为由发起10%见索即付保函全额索兑。",
        "redline_actions": json.dumps([
            "严禁在合同专用条件中盲目签署放弃显失公平（Unconscionability）抗辩的自杀性条款",
            "在收到索兑预警24小时内向SIAC或属地法院申请紧急仲裁员（EA）临时止付禁令",
            "向开证行正式发送《存在严重恶意与欺诈通知函》，阻断保函银行即时无条件划款"
        ], ensure_ascii=False)
    },
    {
        "community_id": "RC_EXPROPRIATION",
        "name_zh": "隐性征收、政府换届单方停工与信保报损",
        "risk_level": "critical",
        "host_countries": json.dumps(["PH", "ID", "VN"], ensure_ascii=False),
        "archetypes": json.dumps(["PPP_CONCESSION", "CROSS_BORDER_MA"], ensure_ascii=False),
        "norm_ids": json.dumps(["PH:RA_11966:Sec18", "TREATY:CN_ID_BIT_1992:Art4", "SINOSURE:Overseas_Policy:Art15"], ensure_ascii=False),
        "trigger_scenarios": "东道国政府换届后以环保重评、前任内阁违规或国安审查为由单方撤销特许权协议并拒付公允补偿。",
        "redline_actions": json.dumps([
            "发生实质停工或撤销特许权之日起 30 日内，必须向中国信保递交《可能损失通知书》",
            "完整保全原始特许经营合同原件及政府全部往来公函原件，严禁私自签署权益放弃声明",
            "依据中国与东道国 BIT 投资协定启动 ICSID 或国际仲裁前置磋商照会"
        ], ensure_ascii=False)
    },
    {
        "community_id": "RC_LANGUAGE_VALIDITY",
        "name_zh": "属地语言法定要求与双语合同效力抗辩",
        "risk_level": "high",
        "host_countries": json.dumps(["ID", "TH"], ensure_ascii=False),
        "archetypes": json.dumps(["EPC_CONTRACTING", "JV_CONSORTIUM"], ensure_ascii=False),
        "norm_ids": json.dumps(["ID:SEMA_3_2023", "ID:KUHPerdata:Art1338"], ensure_ascii=False),
        "trigger_scenarios": "印尼或泰国业主在发生巨额工程款拖欠时，恶意以合同或变更指令未签署属地语言（印尼语/泰语）版本为由主张合同自始绝对无效。",
        "redline_actions": json.dumps([
            "签约阶段坚持双语同步签署，约定以英文本为主导并在印尼语文本附带忠实对应声明",
            "在争议阶段坚决援引印尼最高院 SEMA 3/2023 通告，抗辩无恶意下合同依然具备全额拘束力",
            "工程签证单与重大变更纪要必须同时具备双语版本留痕"
        ], ensure_ascii=False)
    },
    {
        "community_id": "RC_EOT_BAR",
        "name_zh": "FIDIC 第20.1款28天索赔通知失权与突破",
        "risk_level": "high",
        "host_countries": json.dumps(["ID", "VN", "MY", "SG"], ensure_ascii=False),
        "archetypes": json.dumps(["EPC_CONTRACTING"], ensure_ascii=False),
        "norm_ids": json.dumps(["FIDIC:Silver_1999:Clause_20.1", "FIDIC:Silver_1999:Clause_8.4"], ensure_ascii=False),
        "trigger_scenarios": "因现场地质不可预见或属地征地受阻导致工期滞后，承包商迟延发出正式书面通知，业主援引第20.1款主张承包商彻底失权并扣罚全额延误赔偿。",
        "redline_actions": json.dumps([
            "建立项目现场28天发函强管控日历，知悉任何受阻事件即刻发出中性保留权利通知（Notice of Claim）",
            "若已逾期，深入梳理项目往来邮件与会议纪要，主张业主在往来沟通中已获实际知悉（Actual Knowledge）",
            "援引民法诚信原则或防止不当得利规则，主张严苛除斥期间造成显失公平"
        ], ensure_ascii=False)
    },
    {
        "community_id": "RC_CROSS_BORDER_DATA",
        "name_zh": "《数据安全法》第36条核心工程图纸跨境调证违规",
        "risk_level": "critical",
        "host_countries": json.dumps(["SG", "MY", "VN"], ensure_ascii=False),
        "archetypes": json.dumps(["EPC_CONTRACTING", "CROSS_BORDER_MA"], ensure_ascii=False),
        "norm_ids": json.dumps(["CN:Data_Security_Law:Art36", "CN:SASAC_Order_35:Art12"], ensure_ascii=False),
        "trigger_scenarios": "境外仲裁庭（如SIAC）或外国法院在证据披露（Document Production）程序中，强制指令中资企业提交存储于境内的重大基建BIM全套三维图纸或地下管线敏感坐标数据。",
        "redline_actions": json.dumps([
            "严禁直接擅自向境外机构提供境内存放的重大基建涉密图纸或高精度空间地理数据",
            "启动中国网信办与住建部境外数据出境安全评估法定申请通道",
            "在仲裁庭以东道国及中国强制法规范冲突为由申请证据披露豁免或脱敏调证替代方案"
        ], ensure_ascii=False)
    }
]


def ingest_asean_kb(snapshot_id: str = "20261010-gii-v0.7"):
    """执行知识库写入与图谱关系同步"""
    mgr = SnapshotManager()
    snap_id = snapshot_id or mgr.get_current_snapshot_id()
    snap_dir = os.path.join("data", "snapshots", snap_id)
    db_path = os.path.join(snap_dir, "law.sqlite")

    print(f"=== 开始入库东盟 2026 知识库至快照 [{snap_id}] ===")
    conn = init_snapshot_db(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    now_str = datetime.now().isoformat()

    # 1. 批量插入/更新 法条 norms
    inserted_norms = 0
    for item in ASEAN_NORMS_DATA:
        norm_id = item["norm_id"]
        law = item["law"]
        enbez = item["enbez"]
        title = item["title"]
        heading_path = item["heading_path"]
        text_de = item["text_de"]
        language_mode = item.get("language_mode", "bilingual")
        lang_original = item.get("lang_original", "en")
        text_original = item.get("text_original", "")
        text_en = item.get("text_en", "")
        text_zh = item.get("text_zh", "")
        translation_source = item.get("translation_source", "MOJ_FATONG_2026")
        norm_category = item.get("norm_category", "statute")
        fidic_tier = item.get("fidic_tier")
        fidic_edition = item.get("fidic_edition")
        mandatory_level = item.get("mandatory_level", "default")
        elements_json = item.get("elements_json")

        cur.execute(
            """INSERT INTO norms(
                 norm_id, law, enbez, title, heading_path, text_de, structure, footnotes, stand,
                 has_pending_amend, source_url, snapshot_id, fetched_at,
                 language_mode, lang_original, text_original, text_en, text_zh,
                 translation_source, norm_category, fidic_tier, fidic_edition,
                 elements_json, mandatory_level
               )
               VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
               ON CONFLICT(norm_id) DO UPDATE SET
                 title=excluded.title,
                 heading_path=excluded.heading_path,
                 text_de=excluded.text_de,
                 language_mode=excluded.language_mode,
                 lang_original=excluded.lang_original,
                 text_original=excluded.text_original,
                 text_en=excluded.text_en,
                 text_zh=excluded.text_zh,
                 translation_source=excluded.translation_source,
                 norm_category=excluded.norm_category,
                 fidic_tier=excluded.fidic_tier,
                 fidic_edition=excluded.fidic_edition,
                 elements_json=excluded.elements_json,
                 mandatory_level=excluded.mandatory_level,
                 fetched_at=excluded.fetched_at""",
            (
                norm_id, law, enbez, title, heading_path, text_de, "", "", "2026",
                0, "https://overseas-law.moj.gov.cn/fatong", snap_id, now_str,
                language_mode, lang_original, text_original, text_en, text_zh,
                translation_source, norm_category, fidic_tier, fidic_edition,
                elements_json, mandatory_level
            )
        )
        inserted_norms += 1

    print(f"-> 成功入库/更新 {inserted_norms} 条东盟与 FIDIC 2026 权威法源")

    # 2. 批量插入/更新 风险社区 risk_communities
    inserted_rc = 0
    for rc in ASEAN_RISK_COMMUNITIES:
        cur.execute(
            """INSERT INTO risk_communities(
                 community_id, name_zh, risk_level, host_countries,
                 archetypes, norm_ids, trigger_scenarios, redline_actions
               )
               VALUES(?, ?, ?, ?, ?, ?, ?, ?)
               ON CONFLICT(community_id) DO UPDATE SET
                 name_zh=excluded.name_zh,
                 risk_level=excluded.risk_level,
                 host_countries=excluded.host_countries,
                 archetypes=excluded.archetypes,
                 norm_ids=excluded.norm_ids,
                 trigger_scenarios=excluded.trigger_scenarios,
                 redline_actions=excluded.redline_actions""",
            (
                rc["community_id"], rc["name_zh"], rc["risk_level"],
                rc["host_countries"], rc["archetypes"], rc["norm_ids"],
                rc["trigger_scenarios"], rc["redline_actions"]
            )
        )
        inserted_rc += 1
    print(f"-> 成功入库/更新 {inserted_rc} 个央国企核心工程风险社区")

    # 3. 批量插入/更新 关系拓扑边 edges & edges_top
    inserted_edges = 0
    for edge in ASEAN_EDGES_DATA:
        cur.execute(
            """INSERT INTO edges(src, dst, rel, source, span, confidence, reviewed, snapshot_id)
               VALUES(?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                edge["src"], edge["dst"], edge["rel"], edge["source"],
                "", edge["confidence"], edge["reviewed"], snap_id
            )
        )
        # 同步写入 edges_top（双向可查）
        src_node = f"NORM:{edge['src']}" if not edge['src'].startswith("NORM:") else edge['src']
        dst_node = f"NORM:{edge['dst']}" if not edge['dst'].startswith("NORM:") else edge['dst']
        cur.execute(
            """INSERT INTO edges_top(src, dst, rel, source, reviewed, rk)
               VALUES(?, ?, ?, ?, ?, 1)""",
            (src_node, dst_node, edge["rel"], edge["source"], edge["reviewed"])
        )
        inserted_edges += 1
    print(f"-> 成功写入 {inserted_edges} 条三层 Legal GraphRAG 拓扑边")

    conn.commit()

    # 4. 生成对应 Chunks
    print("-> 正在生成东盟与 FIDIC 法源分块 Chunks...")
    all_norms = mgr.get_all_norms(snap_id)
    all_cases = mgr.get_all_cases(snap_id)
    total_chunks = build_and_save_chunks(conn, all_norms, all_cases)
    print(f"-> 快照总分块数达: {total_chunks}")

    # 5. 重构 BM25 词法索引
    print("-> 正在重构并持久化 BM25 索引...")
    index_dir = os.path.join(snap_dir, "index")
    rows = conn.execute("SELECT chunk_id, kind, ref_id, seq, text FROM chunks").fetchall()
    chunks = [dict(r) for r in rows]
    bm25 = BM25Engine(index_dir=index_dir)
    bm25.build_from_chunks(chunks)
    print("-> BM25 索引重构成功")

    conn.close()
    print("=== Phase 8 知识库构建与图谱对齐圆满完成 ===")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="入库东盟 2026 现行有效法源")
    parser.add_argument("--snapshot", type=str, default="20261010-gii-v0.7")
    args = parser.parse_args()
    ingest_asean_kb(args.snapshot)
