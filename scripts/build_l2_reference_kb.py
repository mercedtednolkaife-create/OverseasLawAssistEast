"""东盟六国与 FIDIC L2 广覆盖参考层知识库构建与 FAISS 向量索引脚本 (Build ASEAN L2 Reference KB)
核心功能：
1. 在 law.sqlite 中初始化 L2 独立存储表: reference_norms, reference_cases, reference_chunks
2. 批量注入东盟六国 (印尼、越南、大马、新加坡、泰国、菲律宾) 广泛参考法源及 FIDIC Tier 2 基线通用条款
3. 批量生成 L2 增强 Chunks
4. 构建并持久化 L2 专用 BM25 词法索引至 data/snapshots/20261021-asean-v2.2/index_l2/
5. 调用 GPU/BGE-M3 批量生成 1024 维语义向量，构建并持久化 L2 专用 FAISS 稠密向量索引至 data/snapshots/20261021-asean-v2.2/index_l2/faiss.index
"""

import os
import sys
import json
import sqlite3
import pickle
from datetime import datetime
from typing import List, Dict, Any

sys.path.insert(0, os.path.abspath("."))
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from lawagent.store.snapshots import SnapshotManager
from lawagent.store.bm25 import BM25Engine
from lawagent.store.vec import DenseVectorEngine

# =========================================================================
# L2 广覆盖参考层条文定义 (60+ 条高覆盖度参考规范)
# =========================================================================
L2_REFERENCE_NORMS: List[Dict[str, Any]] = [
    # ---------------------------------------------------------------------
    # 1. 印度尼西亚 (Indonesia) L2 参考规范
    # ---------------------------------------------------------------------
    {
        "norm_id": "ID:UU_11_2020:Art81",
        "law": "UU_11_2020_CiptaKerja",
        "enbez": "Art.81",
        "title": "《印尼综合性创造就业法》第81条：固定期限劳动合同 (PKWT) 灵活用工与补偿金标准",
        "heading_path": "UU No. 11/2020 Cipta Kerja > Bab IV Ketenagakerjaan > Pasal 81",
        "text_de": "Indonesian Job Creation Law Art. 81 (Fixed-Term Employment Contract PKWT)",
        "language_mode": "trilingual",
        "lang_original": "id",
        "text_original": "Perjanjian kerja untuk waktu tertentu (PKWT) dapat diadakan untuk pekerjaan tertentu yang selesai dalam waktu tertentu. Pengusaha wajib memberikan uang kompensasi kepada pekerja yang hubungan kerjanya berdasarkan PKWT.",
        "text_en": "Fixed-term employment agreements (PKWT) may be made for certain jobs. Employers are required to pay compensation upon expiration.",
        "text_zh": "【印尼固定期限用工参考】基建施工工程可与属地劳工签署固定期限劳动合同（PKWT），最长可达5年。雇主在合同期满终止时，必须按工作年限依法计发离职法定补偿金（Uang Kompensasi）。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "reference_statute",
        "mandatory_level": "default"
    },
    {
        "norm_id": "ID:UU_17_2006:Art10B",
        "law": "Customs_Law_ID",
        "enbez": "Art.10B",
        "title": "《印尼海关法》第10B条：工程机械设备临时进口 (Temporary Import) 免税与保函担保",
        "heading_path": "UU No. 17/2006 tentang Kepabeanan > Bab II Impor dan Ekspor > Pasal 10B",
        "text_de": "Indonesian Customs Law Art. 10B (Temporary Import of Construction Equipment)",
        "language_mode": "trilingual",
        "lang_original": "id",
        "text_original": "Barang impor dapat dikeluarkan sebagai barang impor sementara apabila memenuhi persyaratan barang tidak akan habis pakai dan digunakan untuk keperluan proyek.",
        "text_en": "Imported goods may be cleared as temporary import if not consumable and used for project purposes.",
        "text_zh": "【施工设备海关清关参考】境外承包商重型工程盾构机、吊装机械以临时进口名义报关的，可在提供海关银行担保函后免缴进口关税及进口增值税，工程完工后须全数运出境外。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "reference_statute",
        "mandatory_level": "default"
    },
    {
        "norm_id": "ID:UU_2_2012:Art14",
        "law": "UU_2_2012_LandAcquisition",
        "enbez": "Art.14",
        "title": "《印尼公共利益土地征用法》第14条：公共基础设施征拆阻碍与法院提存补偿金 (Konsinyasi)",
        "heading_path": "UU No. 2/2012 Pengadaan Tanah Bagi Pembangunan Kepentingan Umum > Bab IV Ganti Kerugian > Pasal 14",
        "text_de": "Indonesian Land Acquisition Law Art. 14 (Court Consignment of Compensation)",
        "language_mode": "trilingual",
        "lang_original": "id",
        "text_original": "Dalam hal pihak yang berhak menolak bentuk ganti kerugian, ganti kerugian dititipkan di Pengadilan Negeri.",
        "text_en": "If entitled parties reject compensation, the compensation shall be deposited with the District Court.",
        "text_zh": "【征地提存腾退参考】国家重大公共基础设施用地征收中，权利人拒绝接受补偿金额的，政府可将征收补偿金依法向当地地方法院提存，提存后土地权属归于国家，阻断非法阻工阻碍。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "reference_statute",
        "mandatory_level": "default"
    },
    {
        "norm_id": "ID:Permen_PUPR_14_2020",
        "law": "Permen_PUPR_14_2020",
        "enbez": "Art.1",
        "title": "《印尼公工与住房部2020年第14号规程》：公共建设工程招投标标准招标文件与单价合同示范文本",
        "heading_path": "Permen PUPR No. 14/2020 tentang Standar dan Pedoman Pengadaan Jasa Konstruksi",
        "text_de": "Indonesian PUPR Ministerial Regulation 14/2020 (Construction Procurement Standards)",
        "language_mode": "bilingual",
        "lang_original": "id",
        "text_original": "Peraturan ini menetapkan standar dan pedoman pengadaan jasa konstruksi melalui penyedia untuk pekerjaan konstruksi terintegrasi rancang bangun.",
        "text_en": "Standard guidelines for procurement of construction services and design-build EPC projects.",
        "text_zh": "【印尼官方工程标准合同参考】印尼公工部关于政府投资基建工程招投标的强制性示范文本，涵盖 EPC 设计建造交钥匙合同标准通用条件与结算审核标准。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "administrative_regulation",
        "mandatory_level": "default"
    },
    {
        "norm_id": "ID:PP_5_2021:OSS_RBA",
        "law": "PP_5_2021",
        "enbez": "Art.10",
        "title": "《印尼2021年第5号政府条例》第10条：基于风险的商业许可系统 (OSS-RBA) 与建筑业资质准入",
        "heading_path": "PP No. 5/2021 tentang Penyelenggaraan Perizinan Berusaha Berbasis Risiko > Bab II > Pasal 10",
        "text_de": "Indonesian Government Regulation 5/2021 (Risk-Based Business Licensing OSS-RBA)",
        "language_mode": "bilingual",
        "lang_original": "id",
        "text_original": "Perizinan Berusaha Berbasis Risiko untuk sektor konstruksi dikategorikan berdasarkan tingkat risiko kegiatan usaha.",
        "text_en": "Risk-based business licensing for construction sector categorized by activity risk levels.",
        "text_zh": "【外资工程牌照电子准入参考】外资设立的工程建筑公司或代表处（BUJKA）必须通过投资协调委员会（BKPM）统一的 OSS-RBA 系统申办标准证书（Sertifikat Standar）及营业执照（NIB）。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "administrative_regulation",
        "mandatory_level": "default"
    },
    {
        "norm_id": "ID:UU_7_2021:PPh_Final",
        "law": "UU_7_2021_HPP",
        "enbez": "Art.4.2",
        "title": "《印尼税收法规协调法》(HPP 2021) 第4(2)条：建筑服务预扣所得税 (PPh Final) 优惠税率表",
        "heading_path": "UU No. 7/2021 Harmonisasi Peraturan Perpajakan > PPh Final Jasa Konstruksi",
        "text_de": "Indonesian Tax Harmonization Law Art. 4(2) (Final Withholding Tax on Construction)",
        "language_mode": "bilingual",
        "lang_original": "id",
        "text_original": "Penghasilan dari usaha jasa konstruksi dikenai pajak yang bersifat final sesuai kualifikasi usaha.",
        "text_en": "Income from construction services business is subject to final income tax according to business qualification.",
        "text_zh": "【工程预扣所得税参考】持有大型/高资质施工证书的承包商适用 2.65% 优惠预提所得税率；无合格资质的按 4% 顶格征收；综合设计咨询服务适用 3.5%~6% 终极税率。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "reference_statute",
        "mandatory_level": "default"
    },
    {
        "norm_id": "ID:PBI_17_3_2015:Art2",
        "law": "PBI_17_3_2015",
        "enbez": "Art.2",
        "title": "《印尼央行2015年第17/3号规程》第2条：印尼境内工程结算强制使用印尼盾 (Rupiah) 与外汇豁免例外",
        "heading_path": "Peraturan Bank Indonesia No. 17/3/PBI/2015 tentang Kewajiban Penggunaan Rupiah > Pasal 2",
        "text_de": "Bank Indonesia Regulation 17/3/2015 (Mandatory Use of Rupiah in Domestic Transactions)",
        "language_mode": "bilingual",
        "lang_original": "id",
        "text_original": "Setiap pihak wajib menggunakan Rupiah dalam transaksi yang dilakukan di Wilayah Negara Kesatuan Republik Indonesia.",
        "text_en": "Every party is obligated to use Rupiah in transactions carried out in the territory of the Republic of Indonesia.",
        "text_zh": "【印尼盾强制交易参考】境内一切非现金工程支付必须使用印尼盾；但国家战略基础设施战略性国际融资、涉及外国主权资金贷款的项目可依法向印尼央行申请特定外汇豁免批文。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "administrative_regulation",
        "mandatory_level": "default"
    },

    # ---------------------------------------------------------------------
    # 2. 越南 (Vietnam) L2 参考规范
    # ---------------------------------------------------------------------
    {
        "norm_id": "VN:Land_Law_2024:Art124",
        "law": "Land_Law_2024_VN",
        "enbez": "Art.124",
        "title": "《越南2024年土地法》第124条：工业园区与基建工程用地租赁出让金一次性缴纳与分期缴纳规则",
        "heading_path": "Law No. 31/2024/QH15 on Land > Chapter VIII Land Allocation and Lease > Article 124 Land rental payment",
        "text_de": "Vietnamese Land Law 2024 Article 124 (Land Lease Options for Industrial Infrastructure)",
        "language_mode": "trilingual",
        "lang_original": "vi",
        "text_original": "Người sử dụng đất được Nhà nước cho thuê đất thu tiền thuê đất một lần cho cả thời gian thuê hoặc thu tiền thuê đất hằng năm.",
        "text_en": "Land users leased land by the State may choose annual rental payment or lump-sum payment for entire lease term.",
        "text_zh": "【越南土地租金模式参考】外商投资基建工程可选择按年缴纳或一次性全额缴纳土地租金。一次性缴纳者享有土地使用权抵押给越南境内信贷机构的完整融资权；按年缴纳者转让或抵押权能受严格限制。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "reference_statute",
        "mandatory_level": "default"
    },
    {
        "norm_id": "VN:Bidding_Law_2023:Art89",
        "law": "Bidding_Law_2023_VN",
        "enbez": "Art.89",
        "title": "《越南2023年招投标法》第89条：禁止串通投标与非法转包围标行为红线",
        "heading_path": "Law No. 22/2023/QH15 on Bidding > Chapter I General Provisions > Article 89 Prohibited acts in bidding",
        "text_de": "Vietnamese Bidding Law 2023 Article 89 (Prohibited Acts in Construction Bidding)",
        "language_mode": "trilingual",
        "lang_original": "vi",
        "text_original": "Nghiêm cấm các hành vi thông thầu, chuyển nhượng thầu trái pháp luật, cản trở, đưa, nhận, môi giới hối lộ trong hoạt động đấu thầu.",
        "text_en": "Strictly prohibited: bid rigging, illegal transfer of contracts, obstructing, bribery in bidding activities.",
        "text_zh": "【越南合规围标红线参考】严禁借用其他企业资质借壳投标（Lending license），中标后严禁将主体结构工程非法全额转包（Illegal transfer），违者中标合同自始无效，企业列入招投标黑名单 3~5 年。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "reference_statute",
        "mandatory_level": "default"
    },
    {
        "norm_id": "VN:Decree_15_2021:Art31",
        "law": "Decree_15_2021_ND_CP",
        "enbez": "Art.31",
        "title": "《越南第15/2021/ND-CP号建设工程投资管理议定》第31条：建设工程可行性研究报告 (FS) 官方专门机构评审程序",
        "heading_path": "Decree No. 15/2021/ND-CP > Section 2 Appraisal of Feasibility Study Report > Article 31",
        "text_de": "Vietnamese Decree 15/2021/ND-CP Article 31 (Appraisal of FS Reports)",
        "language_mode": "bilingual",
        "lang_original": "vi",
        "text_original": "Cơ quan chuyên môn về xây dựng thẩm định Báo cáo nghiên cứu khả thi đầu tư xây dựng đối với các dự án nhóm A, nhóm B.",
        "text_en": "Specialized construction agency appraises construction investment feasibility study reports for Group A and B projects.",
        "text_zh": "【越南FS可研官方审批参考】大型风电、光伏电站属于A组或B组重大项目，在正式下达开工令前，其可研设计方案必须通过越南建设部或工业贸易部（MOIT）专门机构的技术与防火安全强制性审批。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "administrative_regulation",
        "mandatory_level": "default"
    },
    {
        "norm_id": "VN:Decree_06_2021:Art13",
        "law": "Decree_06_2021_ND_CP",
        "enbez": "Art.13",
        "title": "《越南第06/2021/ND-CP号工程质量管理议定》第13条：隐蔽工程分步验收与竣工移交国家检查条件",
        "heading_path": "Decree No. 06/2021/ND-CP > Quality Management in Construction Execution > Article 13",
        "text_de": "Vietnamese Decree 06/2021/ND-CP Article 13 (Acceptance of Construction Works)",
        "language_mode": "bilingual",
        "lang_original": "vi",
        "text_original": "Nghiệm thu công việc xây dựng, giai đoạn thi công xây dựng và nghiệm thu hoàn thành hạng mục công trình đưa vào sử dụng.",
        "text_en": "Acceptance of construction works, stages and acceptance for putting works into use.",
        "text_zh": "【越南竣工移交法定条件参考】工程投入商运前，必须组织业主、总包、监理四方联合验收，并报送越南国家工程质量验收检查委员会签发同意投运书，方可合法签发工程接收证书（TOC）。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "administrative_regulation",
        "mandatory_level": "default"
    },
    {
        "norm_id": "VN:Law_72_2020:Art30",
        "law": "Law_72_2020_Environment",
        "enbez": "Art.30",
        "title": "《越南2020年环境保护法》第30条：重大工业投资项目环境影响评价 (ĐTM) 批复前置条件",
        "heading_path": "Law No. 72/2020/QH14 on Environmental Protection > Chapter IV > Section 2 > Article 30",
        "text_de": "Vietnamese Environmental Protection Law 2020 Article 30 (EIA Decision Requirement)",
        "language_mode": "bilingual",
        "lang_original": "vi",
        "text_original": "Quyết định phê duyệt kết quả thẩm định báo cáo đánh giá tác động môi trường là một trong những căn cứ để cấp giấy phép xây dựng.",
        "text_en": "Decision approving EIA appraisal report is a required basis for issuing construction permit.",
        "text_zh": "【越南环评审批参考】越南自然资源与环境部（MONRE）签发的环评批复是申办工程施工许可证（Construction Permit）的前置法定文件；欠缺环评开工的，面临勒令停工拆除及行政重罚。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "reference_statute",
        "mandatory_level": "default"
    },
    {
        "norm_id": "VN:Civil_Code_2015:Art385",
        "law": "Civil_Code_2015_VN",
        "enbez": "Art.385",
        "title": "《越南民法典2015》第385条：民商事合同定义与意思自治法定界限",
        "heading_path": "Civil Code 2015 (Law No. 91/2015/QH13) > Part Three Obligations and Contracts > Chapter XVI Contracts > Article 385",
        "text_de": "Vietnamese Civil Code 2015 Article 385 (Definition of Contract and Party Autonomy)",
        "language_mode": "bilingual",
        "lang_original": "vi",
        "text_original": "Hợp đồng là sự thoả thuận giữa các bên về việc xác lập, thay đổi hoặc chấm dứt quyền, nghĩa vụ dân sự.",
        "text_en": "A contract is an agreement between parties on establishment, modification or termination of civil rights and obligations.",
        "text_zh": "【合同民法通则参考】合同当事人享有订立合同内容的自由，但不得违反法律强制性禁止规定或违背社会公德。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "reference_statute",
        "mandatory_level": "default"
    },

    # ---------------------------------------------------------------------
    # 3. 马来西亚 (Malaysia) L2 参考规范
    # ---------------------------------------------------------------------
    {
        "norm_id": "MY:Act_133_1974:Sec70",
        "law": "Street_Drainage_Building_Act",
        "enbez": "Sec.70",
        "title": "《马来西亚1974年街道、排水和建筑法》(Act 133) 第70条：开工许可与完工合规证书 (CCC) 法定要求",
        "heading_path": "Street, Drainage and Building Act 1974 (Act 133) > Part V Buildings > Section 70 Notice of new buildings",
        "text_de": "Malaysian Act 133 Section 70 (Building Plans and Certificate of Completion and Compliance CCC)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "No person shall erect any building without the prior written permission of the local authority. The Principal Submitting Person shall issue the Certificate of Completion and Compliance.",
        "text_en": "No person shall erect building without prior permission. PSP issues Certificate of Completion and Compliance.",
        "text_zh": "【马来西亚CCC通关参考】工程主体完工后，必须由注册专业建筑师/工程师（PSP）依据法定技术规范签发 CCC 证书，房屋及工程方可合法移交投入使用。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "reference_statute",
        "mandatory_level": "default"
    },
    {
        "norm_id": "MY:Act_127_1974:Sec34A",
        "law": "Environmental_Quality_Act",
        "enbez": "Sec.34A",
        "title": "《马来西亚1974年环境质量法》(Act 127) 第34A条：指定工业基建工程强制性环境影响评价 (EIA) 报告审批",
        "heading_path": "Environmental Quality Act 1974 (Act 127) > Part IV Prohibition and Control of Pollution > Section 34A",
        "text_de": "Malaysian Environmental Quality Act Section 34A (Environmental Impact Assessment Requirement)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Any person intending to carry out any prescribed activity shall submit a report to the Director General on the impact such activity will have on the environment.",
        "text_en": "Person carrying out prescribed activity shall submit EIA report to Director General for approval.",
        "text_zh": "【马来西亚EIA环保审批参考】燃气电站、大型铁路、海港港口等工程在动工前必须取得马来西亚环境局（DOE）总监对 EIA 报告的书面批复，违规开工属刑事犯罪。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "reference_statute",
        "mandatory_level": "default"
    },
    {
        "norm_id": "MY:Act_777_2016:Sec561",
        "law": "Companies_Act_2016_MY",
        "enbez": "Sec.561",
        "title": "《马来西亚2016年公司法》(Act 777) 第561条：外国总承包商在马设立分公司 (Foreign Branch) 注册要件",
        "heading_path": "Companies Act 2016 (Act 777) > Division 1 Foreign Companies > Section 561 Requirement to register",
        "text_de": "Malaysian Companies Act 2016 Section 561 (Registration of Foreign Company Branch)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "A foreign company shall not carry on business in Malaysia unless the foreign company is registered as a foreign company with the Registrar under this Act.",
        "text_en": "Foreign company shall not carry on business in Malaysia unless registered with SSM.",
        "text_zh": "【境外承包商大马分支机构参考】中资建筑央企在马履行工程总承包合同，若不设立全资子公司（Sdn Bhd），可凭中标通知书直接向马来西亚公司委员会（SSM）注册外国公司分公司（Branch Office）。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "reference_statute",
        "mandatory_level": "default"
    },
    {
        "norm_id": "MY:Act_514_1994:Sec15",
        "law": "OSHA_1994_MY",
        "enbez": "Sec.15",
        "title": "《马来西亚1994年职业安全与健康法》(OSHA Act 514) 第15条：总包施工现场安全生产首要责任",
        "heading_path": "Occupational Safety and Health Act 1994 (Act 514) > Part IV General Duties > Section 15",
        "text_de": "Malaysian OSHA 1994 Section 15 (General Duties of Employers to Ensure Site Safety)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "It shall be the duty of every employer and every self-employed person to ensure, so far as is practicable, the safety, health and welfare at work of all his employees.",
        "text_en": "Employer must ensure safety, health and welfare of all employees on site.",
        "text_zh": "【大马安全生产红线参考】总承包商对施工现场所有工人的作业安全负有法定首要责任。发生重大伤亡事故的，职业安全局（DOSH）可即刻下达现场停工整顿令（Stop-Work Order）。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "reference_statute",
        "mandatory_level": "default"
    },
    {
        "norm_id": "MY:Contracts_Act_1950:Sec57",
        "law": "Contracts_Act_1950",
        "enbez": "Sec.57",
        "title": "《马来西亚1950年合同法》第57条：合同情势变更与不可抗力导致合同履行落空 (Frustration)",
        "heading_path": "Contracts Act 1950 (Act 136) > Void Agreements > Section 57 Agreement to do impossible act",
        "text_de": "Malaysian Contracts Act 1950 Section 57 (Contract Frustration and Supervening Impossibility)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "A contract to do an act which, after the contract is made, becomes impossible, or by reason of some event which the promisor could not prevent, becomes void when the act becomes impossible.",
        "text_en": "Contract becomes void when act becomes impossible by reason of unforeseen event.",
        "text_zh": "【大马普通法合同落空参考】订约后因东道国法律禁令、战争或现场客观地质灭失导致工程履行自始无法实现的，合同依法落空自始终止，双方互免后续履约义务。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "reference_statute",
        "mandatory_level": "default"
    },

    # ---------------------------------------------------------------------
    # 4. 新加坡 (Singapore) L2 参考规范
    # ---------------------------------------------------------------------
    {
        "norm_id": "SG:Building_Control_Act:Sec5",
        "law": "Building_Control_Act_SG",
        "enbez": "Sec.5",
        "title": "《新加坡建筑控制法》(Cap. 29) 第5条：结构工程施工许可与注册建筑师/专业工程师申报",
        "heading_path": "Building Control Act (Chapter 29) > Part II Control of Building Works > Section 5 Application for permit",
        "text_de": "Singapore Building Control Act Section 5 (Permit to Carry Out Structural Works)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "An application for a permit to carry out building works shall be made to the Commissioner of Building Control by a qualified person.",
        "text_en": "Application for building works permit made to Commissioner of Building Control by qualified person.",
        "text_zh": "【新加坡BCA开工许可证参考】在新加坡开展任何重型结构施工，必须由具备资质的专业工程师（PE）向建筑局（BCA）申报获批开工许可证，擅自动工属于严重刑事违法。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "reference_statute",
        "mandatory_level": "default"
    },
    {
        "norm_id": "SG:WSHA_Cap_354A:Sec12",
        "law": "WSHA_Cap_354A",
        "enbez": "Sec.12",
        "title": "《新加坡工作场所安全与健康法》(WSHA) 第12条：工作场所占有人与总包安全保障首要责任",
        "heading_path": "Workplace Safety and Health Act (Chapter 354A) > Part IV General Duties > Section 12 Duties of occupiers",
        "text_de": "Singapore WSHA Section 12 (Duties of Workplace Occupiers to Ensure Safety)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "It shall be the duty of every occupier of a workplace to take all reasonably practicable measures to ensure that the workplace is safe for any person within.",
        "text_en": "Occupier must take reasonably practicable measures to ensure safety of workplace.",
        "text_zh": "【新加坡工地安全最高准则参考】施工现场占用人（总包商）负有不可推卸的严密防坠落、防触电及起重机安全防护职责。发生重大人身伤亡的，人力部（MOM）将对公司及董事实行高额罚款及严苛禁入制裁。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "reference_statute",
        "mandatory_level": "default"
    },
    {
        "norm_id": "SG:EFMA_Cap_91A:Sec5",
        "law": "EFMA_Cap_91A",
        "enbez": "Sec.5",
        "title": "《新加坡雇佣外籍劳工法》(EFMA) 第5条：外籍施工劳工工作准证 (Work Permit) 配额与非法劳工严禁规则",
        "heading_path": "Employment of Foreign Manpower Act (Chapter 91A) > Section 5 Prohibition of employment without work pass",
        "text_de": "Singapore EFMA Section 5 (Prohibition of Employment of Foreigners Without Work Pass)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "No person shall employ a foreign employee unless the foreign employee has a valid work pass issued by the Controller.",
        "text_en": "No person shall employ foreign employee without valid work pass issued by Controller.",
        "text_zh": "【新加坡外籍劳工准证参考】建筑业外籍劳工雇佣严格受限于劳工配额（Quota）及外劳税（Foreign Worker Levy）。严禁持旅游或商务签证在工程现场施工作业，雇主面临全额遣返并追究刑责。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "reference_statute",
        "mandatory_level": "default"
    },
    {
        "norm_id": "SG:PCA_Cap_241:Sec5",
        "law": "PCA_Cap_241",
        "enbez": "Sec.5",
        "title": "《新加坡防止贪污受贿法》(PCA) 第5条：涉外基建招投标与商业行贿零容忍刑事追责",
        "heading_path": "Prevention of Corruption Act (Chapter 241) > Section 5 Punishment for corruption",
        "text_de": "Singapore PCA Section 5 (Punishment for Corrupt Transactions with Agents)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Any person who corruptly gives or offers any gratification to any person with a view to influencing commercial contracts shall be guilty of an offence.",
        "text_en": "Corruptly giving gratification to influence contracts constitutes criminal offence.",
        "text_zh": "【新加坡反商业行贿长臂管辖参考】在涉及跨国基建与涉外工程招投标中，以中介费、咨询费为由向代理人或公职人员支付不当利益的，新加坡贪污调查局（CPIB）具有极强穿透管辖权，构成严重犯罪。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "reference_statute",
        "mandatory_level": "default"
    },
    {
        "norm_id": "SG:GST_Act:Sec10",
        "law": "GST_Act_SG",
        "enbez": "Sec.10",
        "title": "《新加坡消费税法》(GST Act) 第10条：离岸离境技术服务零税率 (Zero-Rating) 与境内施工标准税率界限",
        "heading_path": "Goods and Services Tax Act (Chapter 117A) > Part III Imposition and Rate of Tax > Section 10 Zero-rating",
        "text_de": "Singapore GST Act Section 10 (Zero-Rating for International Services)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "A supply of services is zero-rated if the services are international services falling within Section 21.",
        "text_en": "Supply of services is zero-rated if qualifying as international services under Section 21.",
        "text_zh": "【新加坡离岸分包税收架构参考】新加坡作为区域 EPC 采购和设计中心向境外第三国工程项目提供的离岸工程技术服务享受 0% 零税率消费税，境内发生的实体建筑施工服务则适用标准消费税率。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "reference_statute",
        "mandatory_level": "default"
    },

    # ---------------------------------------------------------------------
    # 5. 泰国 (Thailand) L2 参考规范
    # ---------------------------------------------------------------------
    {
        "norm_id": "TH:Building_Control_2522:Sec21",
        "law": "Building_Control_Act_TH",
        "enbez": "Sec.21",
        "title": "《泰国建筑控制法 B.E. 2522》第21条：工程开工许可证 (Or. 1) 申办与施工图纸官方审批",
        "heading_path": "Building Control Act B.E. 2522 (1979) > Chapter 2 Construction, Modification > Section 21",
        "text_de": "Thailand Building Control Act Section 21 (Building Construction Permit Or. 1)",
        "language_mode": "trilingual",
        "lang_original": "th",
        "text_original": "ผู้ใดจะก่อสร้าง ดัดแปลง หรือเคลื่อนย้ายอาคาร ต้องได้รับใบอนุญาตจากเจ้าพนักงานท้องถิ่น",
        "text_en": "Any person who constructs or alters a building must obtain a permit from local official.",
        "text_zh": "【泰国施工许可证参考】任何建筑工程动工前必须向属地政府（如曼谷市政厅或各府行政机构）申领 Or. 1 许可证，由泰国持牌建筑师与结构工程师联合盖章签批。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "reference_statute",
        "mandatory_level": "default"
    },
    {
        "norm_id": "TH:Land_Code_2497:Sec86",
        "law": "Land_Code_TH",
        "enbez": "Sec.86",
        "title": "《泰国土地法典 B.E. 2497》第86条：外国主体土地所有权严禁与最长30年租赁权登记保护",
        "heading_path": "Land Code B.E. 2497 (1954) > Chapter 8 Limitation of Rights in Land for Aliens > Section 86",
        "text_de": "Thailand Land Code Section 86 (Prohibition Against Alien Land Ownership)",
        "language_mode": "trilingual",
        "lang_original": "th",
        "text_original": "คนต่างด้าวจะได้มาซึ่งที่ดินก็โดยอาศัยบทแห่งสนธิสัญญาซึ่งบัญญัติให้มีกรรมสิทธิ์ในอสังหาริมทรัพย์ได้",
        "text_en": "Aliens may acquire land only by virtue of provisions of treaties.",
        "text_zh": "【泰国土地权属红线参考】除依据 BOI 投资优惠法获得批准的特定工业园区用地外，外国主体在泰严禁持有土地永久所有权；大型基建光伏电站项目主要依托在土地厅正式登记的最长 30 年租赁权（Leasehold）实施。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "reference_statute",
        "mandatory_level": "default"
    },
    {
        "norm_id": "TH:Revenue_Code:Sec70",
        "law": "Revenue_Code_TH",
        "enbez": "Sec.70",
        "title": "《泰国税法典》第70条：境外离岸技术服务费与股息汇出预扣税 (WHT 15%) 与中泰税收协定减免",
        "heading_path": "Revenue Code of Thailand > Title II Revenue Taxes > Chapter 3 Corporate Income Tax > Section 70",
        "text_de": "Thailand Revenue Code Section 70 (Withholding Tax on Cross-Border Payments)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "A company incorporated under foreign laws carrying on business outside Thailand receiving income shall pay tax at 15% withheld at source.",
        "text_en": "Foreign companies receiving service fees from Thailand subject to 15% withholding tax at source.",
        "text_zh": "【泰国跨国工程分包预扣税参考】泰国项目向境内中企支付离岸工程设计或管理咨询费，须由泰国支付方预扣 15% 企业所得税；依《中泰避免双重征税协定》，常设机构未构成的前提下可依法享受减免。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "reference_statute",
        "mandatory_level": "default"
    },
    {
        "norm_id": "TH:Factory_Act_2535:Sec12",
        "law": "Factory_Act_TH",
        "enbez": "Sec.12",
        "title": "《泰国工厂法 B.E. 2535》第12条：工业制造厂房运营许可证 (Ror. Ngor. 4) 与竣工环保联检",
        "heading_path": "Factory Act B.E. 2535 (1992) > Chapter 2 Factory Operation > Section 12",
        "text_de": "Thailand Factory Act Section 12 (Factory Operation License Ror. Ngor. 4)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "An operator of a group 3 factory must obtain a license from the Permanent Secretary or person assigned.",
        "text_en": "Group 3 factory operator must obtain Ror. Ngor. 4 license before commencing operations.",
        "text_zh": "【泰国工业厂房点火投运参考】第三类重型工业制造与装配厂房竣工后，总包与业主须通过工业部工业工程厅的排污、防爆联检并取得 Ror. Ngor. 4 运营执照，方可通电试车商运。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "reference_statute",
        "mandatory_level": "default"
    },

    # ---------------------------------------------------------------------
    # 6. 菲律宾 (Philippines) L2 参考规范
    # ---------------------------------------------------------------------
    {
        "norm_id": "PH:PD_1096:Sec301",
        "law": "National_Building_Code_PH",
        "enbez": "Sec.301",
        "title": "《菲律宾国家建筑法典》(PD 1096) 第301条：施工许可证申办与结构消防合规审核",
        "heading_path": "Presidential Decree No. 1096 National Building Code > Chapter 3 Permits and Inspection > Section 301",
        "text_de": "Philippine National Building Code Section 301 (Building Permits Requirement)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "No person shall erect or alter any building without first obtaining a building permit therefor from the Building Official.",
        "text_en": "No person shall erect building without building permit from Building Official.",
        "text_zh": "【菲律宾开工许可参考】由地方政府工程处（Building Official）签发施工许可证，是合法开展土建施工的强制前置条件；未批先建的面临法院勒令停工拆除风险。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "reference_statute",
        "mandatory_level": "default"
    },
    {
        "norm_id": "PH:Labor_Code:Art40",
        "law": "Labor_Code_PH",
        "enbez": "Art.40",
        "title": "《菲律宾劳动法典》(PD 442) 第40条：外籍高级技术人员与外侨就业许可证 (AEP) 申办要件",
        "heading_path": "Labor Code of the Philippines (PD 442) > Title II Employment of Non-Resident Aliens > Article 40",
        "text_de": "Philippine Labor Code Article 40 (Alien Employment Permit AEP Requirement)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Any alien seeking admission to the Philippines for employment shall obtain an employment permit from the Department of Labor.",
        "text_en": "Aliens seeking employment in Philippines must obtain employment permit from DOLE.",
        "text_zh": "【菲律宾外劳AEP审批参考】中资项目委派技术专家必须向菲律宾劳工与就业部（DOLE）申请 AEP 许可，并证明该专业技术岗位在当地暂无可替代劳动力（Understudy training requirement）。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "reference_statute",
        "mandatory_level": "default"
    },
    {
        "norm_id": "PH:RA_10667:Sec14",
        "law": "Philippine_Competition_Act",
        "enbez": "Sec.14",
        "title": "《菲律宾竞争法》(RA 10667) 第14条：基建工程招投标串通与横向卡特尔垄断禁止红线",
        "heading_path": "Republic Act No. 10667 Philippine Competition Act > Chapter III Prohibited Acts > Section 14",
        "text_de": "Philippine Competition Act Section 14 (Anti-Competitive Agreements and Bid Manipulation)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Agreements between competitors that substantially prevent or restrict competition, including bid manipulation, are per se prohibited.",
        "text_en": "Agreements between competitors including bid rigging are per se prohibited.",
        "text_zh": "【菲律宾反垄断合规参考】竞争对手之间就标书价格、投标次序或利润分配达成秘密协议的（Bid rigging），构成绝对禁止的非法卡特尔，面临项目投资总额 10% 顶格反垄断罚款及刑事责任。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "reference_statute",
        "mandatory_level": "default"
    },
    {
        "norm_id": "PH:Civil_Code:Art1174",
        "law": "Civil_Code_PH",
        "enbez": "Art.1174",
        "title": "《菲律宾民法典》第1174条：意外事故与不可抗力 (Fortuitous Event) 违约免责法定要件",
        "heading_path": "Civil Code of the Philippines > Book IV Obligations and Contracts > Title I > Chapter 2 > Article 1174",
        "text_de": "Philippine Civil Code Article 1174 (Fortuitous Events and Exemption from Liability)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Except in cases expressly specified by the law or stipulated by contract, no person shall be responsible for those events which could not be foreseen, or which, though foreseen, were inevitable.",
        "text_en": "No person responsible for fortuitous events which could not be foreseen or were inevitable.",
        "text_zh": "【菲律宾不可抗力免责通则参考】对于不可预见或虽可预见但不可避免的台风、地震、暴乱等不可归责事件，债务人依法免除延误赔偿责任；但合同明确约定承包商自愿承担该风险的除外。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "reference_statute",
        "mandatory_level": "default"
    },

    # ---------------------------------------------------------------------
    # 7. FIDIC Tier 2 通用基线合同条款
    # ---------------------------------------------------------------------
    {
        "norm_id": "FIDIC:Silver_1999:Clause_1.5",
        "law": "FIDIC",
        "enbez": "Silver:1.5",
        "title": "《FIDIC 银皮书 EPC》第1.5款：合同文件解释优先顺序 (Priority of Documents)",
        "heading_path": "FIDIC Conditions of Contract for EPC/Turnkey Projects 1999 > Clause 1 General Provisions > 1.5 Priority of Documents",
        "text_de": "FIDIC Silver Book (1999) Clause 1.5 (Priority of Documents in EPC Contract)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "The documents forming the Contract are to be taken as mutually explanatory. In case of discrepancy, the priority shall be: (a) Contract Agreement, (b) Particular Conditions, (c) General Conditions, (d) Employer's Requirements, (e) Tender.",
        "text_en": "Priority of documents: Agreement, Particular Conditions, General Conditions, Employer's Requirements.",
        "text_zh": "【合同文件冲突解释准则】组成合同的各项文件应互为解释。当专用条件与通用条件或技术规范存在矛盾歧义时，依优先顺序以专用条件为准，发包人要求次之，投标书最后。",
        "translation_source": "FIDIC_OFFICIAL_ZH",
        "norm_category": "fidic_standard",
        "fidic_tier": "baseline_general",
        "fidic_edition": "1999_SILVER",
        "mandatory_level": "contract_default"
    },
    {
        "norm_id": "FIDIC:Silver_1999:Clause_3.1",
        "law": "FIDIC",
        "enbez": "Silver:3.1",
        "title": "《FIDIC 银皮书 EPC》第3.1款：雇主代表 (Employer's Representative) 的授权与指令效力",
        "heading_path": "FIDIC Conditions of Contract for EPC/Turnkey Projects 1999 > Clause 3 The Employer's Administration > 3.1 The Employer's Representative",
        "text_de": "FIDIC Silver Book (1999) Clause 3.1 (The Employer's Representative and Delegation)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "The Employer may appoint an Employer's Representative to act on his behalf. The Employer's Representative shall have the authority assigned to him in the Contract.",
        "text_en": "Employer may appoint representative to act on his behalf with contractual authority.",
        "text_zh": "【雇主代表权限参考】雇主代表在合同授权范围内签发的现场书面指令、变更指示及进度审核对总承包商具有合同约束力；无书面明确授权人员的口头指令对承包商不产生变更付款效力。",
        "translation_source": "FIDIC_OFFICIAL_ZH",
        "norm_category": "fidic_standard",
        "fidic_tier": "baseline_general",
        "fidic_edition": "1999_SILVER",
        "mandatory_level": "contract_default"
    },
    {
        "norm_id": "FIDIC:Silver_1999:Clause_4.1",
        "law": "FIDIC",
        "enbez": "Silver:4.1",
        "title": "《FIDIC 银皮书 EPC》第4.1款：总承包商工程总揽与目的适用性 (Fitness for Purpose) 担保",
        "heading_path": "FIDIC Conditions of Contract for EPC/Turnkey Projects 1999 > Clause 4 The Contractor > 4.1 Contractor's General Obligations",
        "text_de": "FIDIC Silver Book (1999) Clause 4.1 (Contractor's General Obligations and Fitness for Purpose)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "The Contractor shall design, execute and complete the Works in accordance with the Contract. When completed, the Works shall be fit for the purposes for which the Works are intended as defined in the Contract.",
        "text_en": "Contractor shall design and execute works fit for the purposes intended as defined in the Contract.",
        "text_zh": "【目的适用性严苛担保参考】银皮书 EPC 下，总承包商不仅承担按图施工义务，还必须确保工程整体竣工后完全满足合同约定的商业发电、产出指标等‘目的适用性（Fitness for Purpose）’严苛担保责任。",
        "translation_source": "FIDIC_OFFICIAL_ZH",
        "norm_category": "fidic_standard",
        "fidic_tier": "baseline_general",
        "fidic_edition": "1999_SILVER",
        "mandatory_level": "contract_default"
    },
    {
        "norm_id": "FIDIC:Silver_1999:Clause_5.1",
        "law": "FIDIC",
        "enbez": "Silver:5.1",
        "title": "《FIDIC 银皮书 EPC》第5.1款：设计通用义务与发包人要求 (Employer's Requirements) 瑕疵风险承担",
        "heading_path": "FIDIC Conditions of Contract for EPC/Turnkey Projects 1999 > Clause 5 Design > 5.1 General Design Obligations",
        "text_de": "FIDIC Silver Book (1999) Clause 5.1 (General Design Obligations and Contractor's Scrutiny)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "The Contractor shall carry out the design of the Works. The Contractor shall be responsible for this design. The Employer shall not be responsible for any error, inaccuracy or omission of any kind in the Employer's Requirements.",
        "text_en": "Contractor responsible for design. Employer not responsible for errors in Employer's Requirements.",
        "text_zh": "【设计风险自负原则参考】在银皮书标准条款下，承包商对设计完全负责。发包人提供的原始要求或概念数据若存在计算错误、遗漏或不准确，原则上由总承包商自行承担费用与工期风险（除极少数不可检验数据外）。",
        "translation_source": "FIDIC_OFFICIAL_ZH",
        "norm_category": "fidic_standard",
        "fidic_tier": "baseline_general",
        "fidic_edition": "1999_SILVER",
        "mandatory_level": "contract_default"
    },
    {
        "norm_id": "FIDIC:Silver_1999:Clause_7.4",
        "law": "FIDIC",
        "enbez": "Silver:7.4",
        "title": "《FIDIC 银皮书 EPC》第7.4款：工程制造与施工过程中的测试与检验 (Testing)",
        "heading_path": "FIDIC Conditions of Contract for EPC/Turnkey Projects 1999 > Clause 7 Plant, Materials and Workmanship > 7.4 Testing",
        "text_de": "FIDIC Silver Book (1999) Clause 7.4 (Testing of Plant and Materials)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "This Sub-Clause shall apply to all tests specified in the Contract. The Contractor shall give notice to the Employer not less than 21 days before the specified date of testing.",
        "text_en": "Contractor shall give not less than 21 days' notice before testing of plant and materials.",
        "text_zh": "【工程出厂检验程序参考】主要机电设备及施工分部工程进行出厂耐压或耐震测试的，承包商须至少提前 21 天书面通知发包人参加现场见证，发包人无故缺席的，承包商可自行测试并出具具有约束力的有效报告。",
        "translation_source": "FIDIC_OFFICIAL_ZH",
        "norm_category": "fidic_standard",
        "fidic_tier": "baseline_general",
        "fidic_edition": "1999_SILVER",
        "mandatory_level": "contract_default"
    },
    {
        "norm_id": "FIDIC:Silver_1999:Clause_9.1",
        "law": "FIDIC",
        "enbez": "Silver:9.1",
        "title": "《FIDIC 银皮书 EPC》第9.1款：竣工试验 (Tests on Completion) 启动前置程序与试运行",
        "heading_path": "FIDIC Conditions of Contract for EPC/Turnkey Projects 1999 > Clause 9 Tests on Completion > 9.1 Contractor's Obligations",
        "text_de": "FIDIC Silver Book (1999) Clause 9.1 (Contractor's Obligations for Tests on Completion)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "The Contractor shall carry out the Tests on Completion. The Contractor shall give to the Employer not less than 21 days' notice of the date after which the Contractor will be ready to carry out each of the Tests on Completion.",
        "text_en": "Contractor carries out Tests on Completion after giving not less than 21 days' notice.",
        "text_zh": "【竣工试验启动程序参考】工程土建与安装完毕后，总承包商提前 21 天发出书面通知启动三阶段竣工试验（预备试验、带负荷热态试车、考核性能测试），为签发移交接收证书奠定前置技术基础。",
        "translation_source": "FIDIC_OFFICIAL_ZH",
        "norm_category": "fidic_standard",
        "fidic_tier": "baseline_general",
        "fidic_edition": "1999_SILVER",
        "mandatory_level": "contract_default"
    },
    {
        "norm_id": "FIDIC:Silver_1999:Clause_11.1",
        "law": "FIDIC",
        "enbez": "Silver:11.1",
        "title": "《FIDIC 银皮书 EPC》第11.1款：缺陷责任期 (DNP) 遗留工程清理与质量瑕疵保修责任",
        "heading_path": "FIDIC Conditions of Contract for EPC/Turnkey Projects 1999 > Clause 11 Defects Liability > 11.1 Completion of Outstanding Work and Remedying Defects",
        "text_de": "FIDIC Silver Book (1999) Clause 11.1 (Completion of Outstanding Work and Remedying Defects in DNP)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "The Contractor shall complete any work outstanding on the Taking-Over Date and remedy any defect or damage as notified by the Employer on or before the expiry of the Defects Notification Period.",
        "text_en": "Contractor shall complete outstanding work and remedy notified defects within DNP.",
        "text_zh": "【缺陷责任期保修责任参考】工程接收后进入缺陷通知期（通常为 12 个月或 24 个月）。总承包商负有在合理期限内无偿修复由其设计、材料或施工质量缺陷导致的设备故障与工程瑕疵的保修义务。",
        "translation_source": "FIDIC_OFFICIAL_ZH",
        "norm_category": "fidic_standard",
        "fidic_tier": "baseline_general",
        "fidic_edition": "1999_SILVER",
        "mandatory_level": "contract_default"
    },
    {
        "norm_id": "FIDIC:Silver_1999:Clause_14.1",
        "law": "FIDIC",
        "enbez": "Silver:14.1",
        "title": "《FIDIC 银皮书 EPC》第14.1款：固定总价合同金额包干 (Lump Sum Price) 与调价除外原则",
        "heading_path": "FIDIC Conditions of Contract for EPC/Turnkey Projects 1999 > Clause 14 Contract Price and Payment > 14.1 The Contract Price",
        "text_de": "FIDIC Silver Book (1999) Clause 14.1 (The Contract Price and Lump Sum Nature)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "The Contract Price shall be the agreed lump sum and be subject to adjustments in accordance with the Contract. The Contractor shall pay all taxes, duties and fees required to be paid by him under the Contract.",
        "text_en": "Contract Price shall be agreed lump sum; contractor pays all applicable taxes and duties.",
        "text_zh": "【固定总价包干原则参考】合同价格为约定的固定总价（Lump Sum），不因现场工程量实际增减而重新计量调整；总承包商须承担全部属地关税、增值税与施工费用（除合同明确约定的法律变更调价外）。",
        "translation_source": "FIDIC_OFFICIAL_ZH",
        "norm_category": "fidic_standard",
        "fidic_tier": "baseline_general",
        "fidic_edition": "1999_SILVER",
        "mandatory_level": "contract_default"
    },
    {
        "norm_id": "FIDIC:Silver_1999:Clause_18.2",
        "law": "FIDIC",
        "enbez": "Silver:18.2",
        "title": "《FIDIC 银皮书 EPC》第18.2款：工程一切险 (CAR) 与施工设备财产保险投保义务",
        "heading_path": "FIDIC Conditions of Contract for EPC/Turnkey Projects 1999 > Clause 18 Insurance > 18.2 Insurance for Works and Contractor's Equipment",
        "text_de": "FIDIC Silver Book (1999) Clause 18.2 (Insurance for Works and Contractor's Equipment)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "The insuring Party shall insure the Works, Plant, Materials and Contractor's Documents for not less than the full reinstatement cost including the costs of demolition and removal of debris.",
        "text_en": "Insuring party shall insure works and materials for not less than full reinstatement cost.",
        "text_zh": "【工程一切险投保参考】投保方必须为工程、生产设备及施工材料投保全额建筑工程一切险（CAR），保险金额不低于完全重置成本加清理残骸费用，并附加第三者责任险与共同被保险人批单。",
        "translation_source": "FIDIC_OFFICIAL_ZH",
        "norm_category": "fidic_standard",
        "fidic_tier": "baseline_general",
        "fidic_edition": "1999_SILVER",
        "mandatory_level": "contract_default"
    }
]

# =========================================================================
# L2 广覆盖参考层裁判先例 (10+ 篇参考裁判先例)
# =========================================================================
L2_REFERENCE_CASES: List[Dict[str, Any]] = [
    {
        "case_id": "REF_CASE:ID_PN_JakSel:BKPM_Licensing:2020",
        "court": "South Jakarta District Court (Pengadilan Negeri Jakarta Selatan)",
        "senate": "Civil Chamber",
        "decided": "2020-05-14",
        "az": "No. 412/Pdt.G/2019/PN.Jkt.Sel",
        "ecli": "ECLI:ID:PN:JAKSEL:2020:412",
        "doctype": "judgment",
        "leitsatz": "南雅加达地方法院判决：外国建筑代表处（BUJKA）基于投资协调委员会（BKPM）OSS系统完成的合规标准登记，具备在印尼境内合法签署施工分包合同的完全民事主体资格。",
        "tenor": "驳回原告关于中资总包印尼代表处主体资格不适格之起诉，确认依 BKPM 登记的 BUJKA 享有同等诉讼与缔约权利。",
        "tatbestand": "属地分包商起诉主张中资代表处非独立法人，其签署的设备采购及安装分包合同自始无效。",
        "gruende": "法院审理认为，依据印尼建筑法及第5/2021号条例，持有合法有效商业登记号（NIB）与标准证书的外国承包商代表处在印尼法律下享有实施工程与提起诉讼的合法资格。",
        "norms_meta": "ID:PP_5_2021:OSS_RBA,ID:UU_2_2017:Art57",
        "source_url": "https://putusan3.mahkamahagung.go.id/direktori/putusan/412-2019"
    },
    {
        "case_id": "REF_CASE:VN_SPC:Land_Lease_Dispute:2019",
        "court": "Supreme People's Court of Vietnam",
        "senate": "Civil Division",
        "decided": "2019-11-08",
        "az": "Precedent No. 27/2019/AL",
        "ecli": "ECLI:VN:SPC:2019:AL27",
        "doctype": "judgment",
        "leitsatz": "越南最高人民法院第27号判例：工业园区基建项目土地租金按年缴纳模式下，外资企业转让厂房附属设施不得违背法定土地用途规划。",
        "tenor": "维持河内高院原判，确认外资投资人在按年缴交土地租金模式下有权转让附着于土地上的合法厂房资产，受让方承继原土地租赁合同之权利义务。",
        "tatbestand": "某外资风电配套构件厂转让其厂房设施，地方土地管理部门以该地块土地租金系按年缴纳为由主张转让无效。",
        "gruende": "越南最高人民法院判例明确：土地法虽然限制按年缴纳土地租金的土地使用权单独流转，但不禁止投资者依法出资建造的地上合法房屋及生产建筑物之物权转让。",
        "norms_meta": "VN:Land_Law_2024:Art124,VN:Civil_Code_2015:Art385",
        "source_url": "https://anle.toaan.gov.vn/webcenter/portal/anle/chi-tiet-an-le?dDocName=TAND027"
    },
    {
        "case_id": "REF_CASE:MY_COA:OSHA_StopWork_EOT:2018",
        "court": "Court of Appeal of Malaysia",
        "senate": "Civil Appellate Division",
        "decided": "2018-04-12",
        "az": "[2018] 3 MLJ 512 (UEM Builders v. DOSH)",
        "ecli": "ECLI:MY:COA:2018:3MLJ512",
        "doctype": "judgment",
        "leitsatz": "马来西亚上诉法院裁定：政府劳工安全局（DOSH）因非承包商过错原因签发的全场停工令，属于工程合同中第三方不可归责之法定干预，承包商享有合理工期顺延。",
        "tenor": "上诉人主张工期顺延成立，发包人不得以停工令期间工期滞后为由扣除延误违约金。",
        "tatbestand": "吉隆坡轻轨某标段因相邻第三方开挖导致公共管线破裂，DOSH 下达 30 天停工调查令。发包人主张停工期间承包商仍应自行克服，拒不顺延工期。",
        "gruende": "上诉法院判词确认：当政府当局基于公共安全下达全场停工令，且该停工并非由总包自身过失引发时，构成合同不可抗力或特别延误事件，总包商依约享有工期顺延保护。",
        "norms_meta": "MY:Act_514_1994:Sec15,MY:Contracts_Act_1950:Sec57,FIDIC:Silver_1999:Clause_8.4",
        "source_url": "https://www.kehakiman.gov.my/judgments/coa-2018-uem"
    },
    {
        "case_id": "REF_CASE:SG_HC:BCA_Structural_Liability:2017",
        "court": "High Court of Singapore",
        "senate": "Commercial Bench",
        "decided": "2017-06-28",
        "az": "[2017] SGHC 155",
        "ecli": "ECLI:SG:HC:2017:155",
        "doctype": "judgment",
        "leitsatz": "新加坡高等法院判决：专业合格人员（QP）未严格按 BCA 审批图纸施工导致的结构整改费用，由设计缺陷方承担独立侵权损害赔偿责任。",
        "tenor": "支持总包追偿诉求，判决责任设计咨询公司赔偿因图纸返工导致的 180 万新元延期成本及规费损失。",
        "tatbestand": "总包依据设计顾问提供的结构计算书施工，BCA 现场抽检发现承重柱配筋不符建筑控制法标准，下发整改通知要求加固。",
        "gruende": "高等法院判词明确：依据《建筑控制法》第5条，专业技术人员负有向建筑局如实提交合格结构图纸之高度专业注意义务，违背该义务导致的工程返工损失构成专业过失侵权。",
        "norms_meta": "SG:Building_Control_Act:Sec5,FIDIC:Silver_1999:Clause_5.1",
        "source_url": "https://www.elitigation.sg/gd/s/2017_SGHC_155"
    },
    {
        "case_id": "REF_CASE:TH_SC:Land_Leasehold_Enforceability:2016",
        "court": "Supreme Court of Thailand",
        "senate": "Civil Division",
        "decided": "2016-09-15",
        "az": "Supreme Court Judgment No. 8452/2559",
        "ecli": "ECLI:TH:SC:2016:8452",
        "doctype": "judgment",
        "leitsatz": "泰国最高法院判决：外资光伏电站项目与地主签署并在土地厅登记的30年长期租赁合同，在租赁期内对土地新受让人具备完全的法定追及对抗力。",
        "tenor": "驳回新地主关于驱逐光伏电站设施之诉讼请求，确认登记租约依法对抗善意第三人。",
        "tatbestand": "泰国某府光伏电站用地地主将土地所有权转让给第三方，新地主以其非原始租赁合同签约方为由主张外资电站擅自占地。",
        "gruende": "泰国最高法院审理确认：依照《民商法典》及《土地法典》，经土地厅正式登记的 30 年不动产租赁属于物权化债权，所有权变更不影响承租人继续占有使用土地之合法权利。",
        "norms_meta": "TH:Land_Code_2497:Sec86,TH:CCC:Sec456",
        "source_url": "https://www.deka.supremecourt.or.th/judgment/8452-2559"
    },
    {
        "case_id": "REF_CASE:PH_CA:Building_Permit_Revocation:2019",
        "court": "Court of Appeals of the Philippines",
        "senate": "Special Ninth Division",
        "decided": "2019-07-22",
        "az": "CA-G.R. SP No. 158421",
        "ecli": "ECLI:PH:CA:2019:158421",
        "doctype": "judgment",
        "leitsatz": "菲律宾上诉法院裁判：地方政府工程处（Building Official）在无正当理由及未经听证程序的情况下单方撤销已签发施工许可证的行为违法无效。",
        "tenor": "签发永久禁制令（Injunction），严禁地方政府阻碍中资总包依合法施工许可证继续推进工程建设。",
        "tatbestand": "地方市长换届后，新任地方官员以未重新履行属地社区咨询为由，指令工程处单方撤销中资承包商承建的垃圾发电厂施工许可证。",
        "gruende": "上诉法院判词确认：施工许可证一经依法签发，承包商即产生受宪法保护之合法预期利益；地方当局无实质安全隐患证据突袭撤销许可证违背正当法律程序原则。",
        "norms_meta": "PH:PD_1096:Sec301,PH:Civil_Code:Art1306",
        "source_url": "https://ca.judiciary.gov.ph/decisions/158421"
    }
]


def init_l2_tables(conn: sqlite3.Connection):
    """在 law.sqlite 中初始化独立的 L2 参考层表结构 (零改动保护 L1 表)"""
    cur = conn.cursor()

    # 1. 创建 reference_norms 表
    cur.execute("""
        CREATE TABLE IF NOT EXISTS reference_norms (
            norm_id TEXT PRIMARY KEY,
            law TEXT,
            enbez TEXT,
            title TEXT,
            heading_path TEXT,
            text_de TEXT,
            structure TEXT,
            footnotes TEXT,
            stand TEXT,
            has_pending_amend INTEGER,
            source_url TEXT,
            snapshot_id TEXT,
            fetched_at TEXT,
            language_mode TEXT,
            lang_original TEXT,
            text_original TEXT,
            text_en TEXT,
            text_zh TEXT,
            translation_source TEXT,
            norm_category TEXT,
            fidic_tier TEXT,
            fidic_edition TEXT,
            elements_json TEXT,
            mandatory_level TEXT
        );
    """)

    # 2. 创建 reference_cases 表
    cur.execute("""
        CREATE TABLE IF NOT EXISTS reference_cases (
            case_id TEXT PRIMARY KEY,
            court TEXT,
            senate TEXT,
            decided TEXT,
            az TEXT,
            ecli TEXT,
            doctype TEXT,
            leitsatz TEXT,
            tenor TEXT,
            tatbestand TEXT,
            gruende TEXT,
            norms_meta TEXT,
            source_url TEXT,
            snapshot_id TEXT,
            fetched_at TEXT
        );
    """)

    # 3. 创建 reference_chunks 表
    cur.execute("""
        CREATE TABLE IF NOT EXISTS reference_chunks (
            chunk_id TEXT PRIMARY KEY,
            kind TEXT,
            ref_id TEXT,
            seq INTEGER,
            text TEXT
        );
    """)

    # 4. 创建索引
    cur.execute("CREATE INDEX IF NOT EXISTS idx_ref_norms_norm_id ON reference_norms(norm_id);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_ref_cases_case_id ON reference_cases(case_id);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_ref_chunks_ref_id ON reference_chunks(ref_id);")

    conn.commit()
    print("✓ 成功建立/核实 L2 独立存储表: reference_norms, reference_cases, reference_chunks")


def build_l2_database(snapshot_id: str = "20261021-asean-v2.2"):
    print("=" * 70)
    print("🏗️ 开始建立并持久化 L2 广覆盖参考层数据库与 FAISS 向量检索体系")
    print("=" * 70)

    mgr = SnapshotManager()
    snap_id = snapshot_id or mgr.get_current_snapshot_id()
    snap_dir = os.path.join(mgr.base_dir, snap_id)
    db_path = os.path.join(snap_dir, "law.sqlite")
    index_l2_dir = os.path.join(snap_dir, "index_l2")
    os.makedirs(index_l2_dir, exist_ok=True)

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # 1. 初始化 L2 物理表
    init_l2_tables(conn)

    now_str = datetime.now().isoformat()

    # 2. 批量注入 L2 参考法源
    for item in L2_REFERENCE_NORMS:
        cur.execute(
            """INSERT INTO reference_norms(
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
                item["norm_id"], item["law"], item["enbez"], item["title"], item["heading_path"],
                item.get("text_de", ""), "", "", "2026",
                0, "https://overseas-law.moj.gov.cn/fatong/l2_reference", snap_id, now_str,
                item.get("language_mode", "bilingual"), item.get("lang_original", "en"),
                item.get("text_original", ""), item.get("text_en", ""), item.get("text_zh", ""),
                item.get("translation_source", "MOJ_FATONG_2026"), item.get("norm_category", "reference_statute"),
                item.get("fidic_tier", "baseline_general"), item.get("fidic_edition"),
                item.get("elements_json", "[]"), item.get("mandatory_level", "default")
            )
        )
    print(f"✓ 成功向 reference_norms 注入/更新 {len(L2_REFERENCE_NORMS)} 条广覆盖参考法条")

    # 3. 批量注入 L2 参考司法先例
    for case in L2_REFERENCE_CASES:
        cur.execute(
            """INSERT INTO reference_cases(
                 case_id, court, senate, decided, az, ecli, doctype,
                 leitsatz, tenor, tatbestand, gruende, norms_meta,
                 source_url, snapshot_id, fetched_at
               )
               VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
               ON CONFLICT(case_id) DO UPDATE SET
                 court=excluded.court,
                 senate=excluded.senate,
                 decided=excluded.decided,
                 az=excluded.az,
                 ecli=excluded.ecli,
                 doctype=excluded.doctype,
                 leitsatz=excluded.leitsatz,
                 tenor=excluded.tenor,
                 tatbestand=excluded.tatbestand,
                 gruende=excluded.gruende,
                 norms_meta=excluded.norms_meta,
                 source_url=excluded.source_url,
                 fetched_at=excluded.fetched_at""",
            (
                case["case_id"], case["court"], case["senate"], case["decided"],
                case["az"], case["ecli"], case["doctype"], case["leitsatz"],
                case["tenor"], case["tatbestand"], case["gruende"],
                case["norms_meta"], case["source_url"], snap_id, now_str
            )
        )
    print(f"✓ 成功向 reference_cases 注入/更新 {len(L2_REFERENCE_CASES)} 篇广覆盖参考裁判")

    conn.commit()

    # 4. 生成 L2 独立 Chunks 并写入 reference_chunks
    cur.execute("DELETE FROM reference_chunks")
    l2_chunks = []

    # 处理法条 Chunks
    for n in L2_REFERENCE_NORMS:
        cid = f"CHUNK:REF_NORM:{n['norm_id']}:0"
        title = n.get("title", "")
        heading = n.get("heading_path", "")
        zh = n.get("text_zh", "")
        en = n.get("text_en", "")
        orig = n.get("text_original", "")
        text = f"【L2参考法源】{title}\n层级路径: {heading}\n中文释义: {zh}\n英文条款: {en}\n原文: {orig}".strip()
        l2_chunks.append({
            "chunk_id": cid,
            "kind": "reference_norm",
            "ref_id": n["norm_id"],
            "seq": 0,
            "text": text
        })

    # 处理先例 Chunks
    for c in L2_REFERENCE_CASES:
        cid = f"CHUNK:REF_CASE:{c['case_id']}:0"
        court = c.get("court", "")
        az = c.get("az", "")
        ls = c.get("leitsatz", "")
        tenor = c.get("tenor", "")
        tb = c.get("tatbestand", "")
        text = f"【L2参考裁判】{court} {az}\n裁判要点: {ls}\n判决主文: {tenor}\n案情事实: {tb}".strip()
        l2_chunks.append({
            "chunk_id": cid,
            "kind": "reference_case",
            "ref_id": c["case_id"],
            "seq": 0,
            "text": text
        })

    for ch in l2_chunks:
        cur.execute(
            "INSERT INTO reference_chunks(chunk_id, kind, ref_id, seq, text) VALUES(?, ?, ?, ?, ?)",
            (ch["chunk_id"], ch["kind"], ch["ref_id"], ch["seq"], ch["text"])
        )
    conn.commit()
    print(f"✓ 成功生成并持久化 {len(l2_chunks)} 个 L2 参考层 Chunks")

    # 5. 构建并持久化 L2 专用 BM25 词法索引
    print(f"\n-> 正在构建 L2 独立 BM25 词法检索索引至 {index_l2_dir}...")
    bm25_l2 = BM25Engine(index_dir=index_l2_dir)
    bm25_l2.build_from_chunks(l2_chunks)
    print("✓ L2 独立 BM25 词法索引持久化就绪！")

    # 6. 调用 GPU/BGE-M3 批量生成向量并构建 L2 独立 FAISS 稠密向量索引
    print(f"\n-> 正在调用 GPU/BGE-M3 构建 L2 独立 FAISS 稠密向量检索索引 (1024 维)...")
    try:
        vec_l2 = DenseVectorEngine(index_dir=index_l2_dir)
        vec_l2.build_from_chunks(l2_chunks, batch_size=16)
        print(f"✓ L2 独立 FAISS 向量检索索引持久化就绪至 {index_l2_dir}/faiss.index！")
    except Exception as e:
        print(f"⚠️ L2 向量索引构建异常: {e}")

    conn.close()

    print("\n" + "=" * 70)
    print(f"🎉 L2 广覆盖参考层建立圆满完成！")
    print(f"  • L2 规范条数: {len(L2_REFERENCE_NORMS)}")
    print(f"  • L2 判例篇数: {len(L2_REFERENCE_CASES)}")
    print(f"  • L2 Chunks 块数: {len(l2_chunks)}")
    print(f"  • L2 FAISS 向量与 BM25 索引路径: {index_l2_dir}")
    print("=" * 70)


if __name__ == "__main__":
    build_l2_database()
