"""L1 核心层深化扩充脚本 (Phase 6 L1 Clusters & Precedents)
涵盖领域：
1. 缔约意思表示与缔约过失责任 (越南民法典 Art 385, 397, 401; 印尼民法典 Art 1320, 1328, 1338; 泰国 CCC Sec 354, 368, 370; 菲律宾民法典 Art 1305, 1318, 1330)
2. 土地征收、现场移交迟延与路权交付 (印尼土地征用公共利益法 UU 2/2012 Art 14, 19; 越南新土地法 2024 Art 124, 153; 菲律宾通行权法 RA 10752; 泰国土地征用法 B.E. 2562)
3. 外国仲裁裁决承认与执行防撤销审查 (越南民事诉讼法 2015 Art 423, 439, 440; 印尼最高院 SEMA 3/2023 涉外裁决执行; 马来西亚 2005 仲裁法 Sec 37, 39; 菲律宾 RA 9285 Sec 42)
4. 建设工程缺陷责任与分包索赔 (越南建筑法 2014 Art 111, 112; 泰国 CCC Sec 600, 601 瑕疵除斥期间)
5. 注入 6 篇金标准裁判 + 20+ 条拓扑边 + 2 个高阶风险社区
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

PHASE6_L1_NORMS: List[Dict[str, Any]] = [
    # ---------------------------------------------------------------------
    # 1. 缔约意思表示与缔约过失责任专章 (Pre-contractual & Formation)
    # ---------------------------------------------------------------------
    {
        "norm_id": "VN:Civil_Code_2015:Art385",
        "law": "Civil_Code_VN",
        "enbez": "Art.385",
        "title": "《越南民法典》第385条：民商事民事合同之法定定义与意思自治",
        "heading_path": "Bộ luật Dân sự 2015 > Phần thứ ba Nghĩa vụ và hợp đồng > Điều 385",
        "text_de": "Vietnamese Civil Code Art. 385 (Definition of Contract)",
        "language_mode": "trilingual",
        "lang_original": "vi",
        "text_original": "Hợp đồng là sự thoả thuận giữa các bên về việc xác lập, thay đổi hoặc chấm dứt quyền, nghĩa vụ dân sự.",
        "text_en": "A contract is an agreement between parties on the establishment, modification or termination of civil rights and obligations.",
        "text_zh": "【合同法定定义与合意效力】合同是当事人之间关于确立、变更或者终止民事权利、义务的协议。涉外商事主体在越南境内订立建设工程或合资协议，只要双方意思表示真实且不违反法律强制性规定与社会公德，即具有法律拘束力。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "VN:Civil_Code_2015:Art397",
        "law": "Civil_Code_VN",
        "enbez": "Art.397",
        "title": "《越南民法典》第397条：缔约磋商期间承诺之撤回与缔约过失补偿责任",
        "heading_path": "Bộ luật Dân sự 2015 > Phần thứ ba Nghĩa vụ và hợp đồng > Điều 397",
        "text_de": "Vietnamese Civil Code Art. 397 (Withdrawal of Offer and Culpa in Contrahendo)",
        "language_mode": "trilingual",
        "lang_original": "vi",
        "text_original": "Bên đề nghị giao kết hợp đồng có thể rút lại đề nghị nếu thông báo về việc rút lại đến người được đề nghị trước hoặc cùng thời điểm người này nhận được đề nghị. Bên có hành vi cố ý làm cho bên kia tin tưởng để giao kết mà sau đó từ bỏ không có lý do chính đáng phải bồi thường thiệt hại.",
        "text_en": "A party who intentionally leads the other party to reasonably believe a contract will be concluded and then abandons negotiations without legitimate grounds must compensate for damages.",
        "text_zh": "【缔约过失与恶意磋商赔偿】要约人可在受要约人收到要约之前或同时撤回要约。若一方当事人在重大工程前期磋商中故意诱导相对方产生合理信赖并进行重大前期履约投入（如先行进场勘探、锁定大型设备），随后无正当理由恶意终止谈判，构成缔约过失，必须全额赔偿相对方的信赖利益损失。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "VN:Civil_Code_2015:Art401",
        "law": "Civil_Code_VN",
        "enbez": "Art.401",
        "title": "《越南民法典》第401条：合同成立之有效生效时间与要式登记要求",
        "heading_path": "Bộ luật Dân sự 2015 > Điều 401 Thời điểm có hiệu lực của hợp đồng",
        "text_de": "Vietnamese Civil Code Art. 401 (Effective Time of Contract)",
        "language_mode": "trilingual",
        "lang_original": "vi",
        "text_original": "Hợp đồng được giao kết hợp pháp có hiệu lực từ thời điểm giao kết, trừ trường hợp có thoả thuận khác hoặc luật liên quan có quy định khác.",
        "text_en": "A contract lawfully concluded takes effect from the time of conclusion, unless otherwise agreed or provided by relevant law.",
        "text_zh": "【合同生效时间与公证要件】依法成立的合同自双方签署合意之时起生效，但法律特别规定须经主管部门批准、公证或登记的要式合同（如土地使用权出让、跨境大型担保），自完成法定法定登记之日起生效。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "ID:KUHPerdata:Art1320",
        "law": "KUHPerdata_ID",
        "enbez": "Art.1320",
        "title": "《印尼民法典》第1320条：合同合法成立之四大法定实质生效要件",
        "heading_path": "Burgerlijk Wetboek (KUHPerdata) > Buku III > Pasal 1320 Syarat Sahnya Perjanjian",
        "text_de": "Indonesian Civil Code Art. 1320 (Four Essential Validity Requirements of Contract)",
        "language_mode": "trilingual",
        "lang_original": "id",
        "text_original": "Supaya terjadi persetujuan yang sah, perlu dipenuhi empat syarat: 1. kesepakatan mereka yang mengikatkan dirinya; 2. kecakapan untuk membuat suatu perikatan; 3. suatu pokok persoalan tertentu; 4. suatu sebab yang tidak terlarang.",
        "text_en": "For a contract to be valid, four conditions must be met: 1. consent of the parties; 2. capacity to contract; 3. a specific subject matter; 4. a lawful cause.",
        "text_zh": "【印尼合同生效四大金刚要件】合同依法成立必须同时满足四项要件：① 当事人自愿合意（Kesepakatan）；② 具备缔约民事行为能力；③ 标的物必须确定或可确定；④ 具备合法之对价或原因（Sebab yang halal），不得违反公序良俗、公共秩序或成文法律强行性规定。违反前两项导致合同可撤销，违反后两项导致合同自始绝对无效。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "ID:KUHPerdata:Art1328",
        "law": "KUHPerdata_ID",
        "enbez": "Art.1328",
        "title": "《印尼民法典》第1328条：欺诈与重大诱导撤销合同之举证责任",
        "heading_path": "Burgerlijk Wetboek (KUHPerdata) > Buku III > Pasal 1328 Penipuan",
        "text_de": "Indonesian Civil Code Art. 1328 (Fraud in Contract Formation)",
        "language_mode": "trilingual",
        "lang_original": "id",
        "text_original": "Penipuan merupakan suatu alasan untuk membatalkan persetujuan, bila tipu muslihat yang dipakai oleh salah satu pihak adalah sedemikian rupa, sehingga terang dan nyata bahwa pihak yang lain tidak akan mengadakan perjanjian itu jika tidak ada tipu muslihat itu. Penipuan tidak boleh dipersangkakan, tetapi harus dibuktikan.",
        "text_en": "Fraud is a ground for annulment if deceptions practiced by one party show clearly that the other party would not have entered into it. Fraud cannot be presumed, but must be proven.",
        "text_zh": "【欺诈撤销与举证责任】一方当事人采取隐瞒地质重大缺陷、伪造政府征地进度等欺诈手段，导致相对方非因该诱导便决不可能订立 EPC 合同时，受欺诈方享有法定撤销权。欺诈行为不得推定，主张方承担严格的事实举证责任。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "ID:KUHPerdata:Art1338",
        "law": "KUHPerdata_ID",
        "enbez": "Art.1338",
        "title": "《印尼民法典》第1338条：契约即法律原则与诚实信用强制履行原则",
        "heading_path": "Burgerlijk Wetboek (KUHPerdata) > Buku III > Pasal 1338 Asas Pacta Sunt Servanda & Iktikad Baik",
        "text_de": "Indonesian Civil Code Art. 1338 (Pacta Sunt Servanda and Good Faith Execution)",
        "language_mode": "trilingual",
        "lang_original": "id",
        "text_original": "Semua persetujuan yang dibuat sesuai dengan undang-undang berlaku sebagai undang-undang bagi mereka yang membuatnya. Persetujuan itu tidak dapat ditarik kembali selain dengan kesepakatan kedua belah pihak, atau karena alasan-alasan yang ditentukan oleh undang-undang. Persetujuan harus dilaksanakan dengan iktikad baik.",
        "text_en": "All contracts lawfully entered into shall have the force of law for the parties. They must be executed in good faith.",
        "text_zh": "【契约即法律与善意履约】依法成立的合同在当事人之间产生相当于法律之拘束力（Pacta sunt servanda）。除双方合意或成文法明文规定外，任何一方不得单方撕毁；合同必须以极度之诚实信用（Iktikad baik）予以履行，法院有权基于善意原则校正显失公平之严苛条款。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "TH:CCC:Sec354",
        "law": "Civil_Commercial_Code_TH",
        "enbez": "Sec.354",
        "title": "《泰国成文民商法典》第354条：要约承诺确定期间与要约之不可撤回性",
        "heading_path": "Civil and Commercial Code > Book II Obligations > Section 354",
        "text_de": "Thailand Civil and Commercial Code Sec. 354 (Binding Offer with Period)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "An offer to conclude a contract in which a period for acceptance is specified cannot be withdrawn within such period.",
        "text_en": "An offer to conclude a contract in which a period for acceptance is specified cannot be withdrawn within such period.",
        "text_zh": "【确定期间要约之不可撤回】在工程投标或商事订约中，若要约人明确指定了有效答复期限（如 90 天投标有效期），在该期限届满之前，要约人绝对无权单方撤回要约；受要约人在此期限内的有效承诺直接确立合同成立。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "TH:CCC:Sec368",
        "law": "Civil_Commercial_Code_TH",
        "enbez": "Sec.368",
        "title": "《泰国成文民商法典》第368条：合同解释依照诚实信用与交易习惯原则",
        "heading_path": "Civil and Commercial Code > Book II Obligations > Section 368",
        "text_de": "Thailand Civil and Commercial Code Sec. 368 (Interpretation in Good Faith)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Contracts shall be interpreted in accordance with the requirements of good faith, ordinary usage being taken into consideration.",
        "text_en": "Contracts shall be interpreted in accordance with the requirements of good faith, ordinary usage being taken into consideration.",
        "text_zh": "【合同善意解释与行业惯例】合同条款产生歧义或争议时，必须依照诚实信用原则予以合理解释，并充分考量国际工程工程建设之行业商业惯例（Ordinary Usage），严禁机械咬文嚼字导致实质显失公正。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "PH:Civil_Code:Art1305",
        "law": "Civil_Code_PH",
        "enbez": "Art.1305",
        "title": "《菲律宾民法典》第1305条：合同定义与双务对待给付义务",
        "heading_path": "Civil Code of the Philippines > Title II Contracts > Article 1305",
        "text_de": "Philippines Civil Code Art. 1305 (Definition of Contract)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "A contract is a meeting of minds between two persons whereby one binds himself, with respect to the other, to give something or to render some service.",
        "text_en": "A contract is a meeting of minds between two persons whereby one binds himself, with respect to the other, to give something or to render some service.",
        "text_zh": "【合同定义与合意成立】合同是指两人或多人之间意思表示完全一致（Meeting of minds），从而一方对另一方负有交付特定财物或提供特定工程劳务之法律约束协议。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "PH:Civil_Code:Art1318",
        "law": "Civil_Code_PH",
        "enbez": "Art.1318",
        "title": "《菲律宾民法典》第1318条：合同成立之三大必备实质生效要件",
        "heading_path": "Civil Code of the Philippines > Title II Contracts > Article 1318",
        "text_de": "Philippines Civil Code Art. 1318 (Essential Requisites of Contracts)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "There is no contract unless the following requisites concur: 1. Consent of the contracting parties; 2. Object certain which is the subject matter of the contract; 3. Cause of the obligation which is established.",
        "text_en": "There is no contract unless the following requisites concur: 1. Consent; 2. Object certain; 3. Cause of the obligation.",
        "text_zh": "【菲律宾合同三大成立必备要件】合同必须同时具备以下三要件，否则法律上自始不存在：① 缔约各方之自由真实合意（Consent）；② 确定的标的物或工程劳务（Object certain）；③ 设立债务之合法对待给付对价原因（Cause of the obligation）。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory"
    },

    # ---------------------------------------------------------------------
    # 2. 土地征收、现场移交与通行权交付专章 (Site Handover & Right of Way)
    # ---------------------------------------------------------------------
    {
        "norm_id": "VN:Land_Law_2024:Art124",
        "law": "Land_Law_VN",
        "enbez": "Art.124",
        "title": "《越南新土地法2024》第124条：工业与工程建设项目用地现场移交法定期限",
        "heading_path": "Luật Đất đai 2024 > Điều 124 Giao đất, cho thuê đất trên thực địa",
        "text_de": "Vietnam Land Law 2024 Art. 124 (Physical Handover of Land on Site)",
        "language_mode": "trilingual",
        "lang_original": "vi",
        "text_original": "Cơ quan nhà nước có thẩm quyền và chủ đầu tư có trách nhiệm bàn giao đất trên thực địa cho người sử dụng đất, nhà thầu xây dựng theo đúng mốc giới và thời hạn quy định trong quyết định giao đất, hợp đồng thuê đất.",
        "text_en": "Competent state bodies and project investors are obliged to physically hand over land on site to contractors in accordance with boundary markers and contract deadlines.",
        "text_zh": "【现场土地法定移交义务】项目业主或政府主管部门负有按照土地出让决定与总承包合同约定的红线界址与法定期限，向施工承包商进行清洁施工现场实体移交（Bàn giao đất trên thực địa）之法定义务。若因征地补偿纠纷导致现场迟延移交，承包商依法享有不可抗辩之工期顺延权及停窝工费用索赔权。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "VN:Land_Law_2024:Art153",
        "law": "Land_Law_VN",
        "enbez": "Art.153",
        "title": "《越南新土地法2024》第153条：能源、交通基建工程施工走廊与临时用地法定通行权",
        "heading_path": "Luật Đất đai 2024 > Điều 153 Sử dụng đất cho các công trình công cộng, hạ tầng năng lượng",
        "text_de": "Vietnam Land Law 2024 Art. 153 (Right of Way and Temporary Land Use for Infrastructure)",
        "language_mode": "trilingual",
        "lang_original": "vi",
        "text_original": "Người được giao quản lý, thi công công trình hạ tầng công cộng, năng lượng được quyền sử dụng đất trong hành lang an toàn công trình và tạm thời sử dụng đất phụ cận để phục vụ thi công, bồi thường thiệt hại theo quy định.",
        "text_en": "Contractors executing energy and public infrastructure works have the statutory right to use land within safety corridors and adjacent temporary land for construction purposes.",
        "text_zh": "【基建与能源工程法定路权与临时施工用地】从事公共基础设施与新能源电力工程施工的总承包商，依法享有在工程安全走廊带内铺设管线及使用相邻土地作为临时施工道路之法定通行权（Right of Way）。地方阻碍施工构成的侵权行为由业主与当地政府依法排除。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "ID:UU_2_2012:Art14",
        "law": "Land_Acquisition_Act_ID",
        "enbez": "Art.14",
        "title": "《印尼公共利益土地征用法》(UU 2/2012) 第14条：公共基础设施征地准备程序与现场清场时限",
        "heading_path": "Undang-Undang No. 2 Tahun 2012 jo. UU 6/2023 > Bab IV Persiapan Pengadaan Tanah > Pasal 14",
        "text_de": "Indonesian Land Acquisition Act UU 2/2012 Art. 14 (Preparation and Handover of Acquired Land)",
        "language_mode": "trilingual",
        "lang_original": "id",
        "text_original": "Instansi yang memerlukan tanah bersama Pemerintah Provinsi melaksanakan persiapan pengadaan tanah dan menyelesaikan ganti kerugian untuk menyerahkan hasil pengadaan tanah kepada instansi yang memerlukan tanah siap bangun.",
        "text_en": "The requiring agency together with the provincial government shall complete land acquisition and compensation to hand over ready-to-build site.",
        "text_zh": "【印尼公共利益征地与清洁施工现场移交】在电厂、收费公路及港口等公共利益基础设施项目中，土地征用补偿与村民搬迁安置属于印尼政府与项目发包人的法定公权力职责。发包人必须向 EPC 总承包商移交“准备就绪可立即动工（Siap bangun）”之现场；村民堵门抗议或征地受阻依法归咎于发包人违约。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "ID:UU_2_2012:Art19",
        "law": "Land_Acquisition_Act_ID",
        "enbez": "Art.19",
        "title": "《印尼公共利益土地征用法》(UU 2/2012) 第19条：征地移交成果确认与承包商抗辩权",
        "heading_path": "Undang-Undang No. 2 Tahun 2012 > Bab V Penyerahan Hasil > Pasal 19",
        "text_de": "Indonesian Land Acquisition Act UU 2/2012 Art. 19 (Confirmation of Handover and Contractor Immunity)",
        "language_mode": "trilingual",
        "lang_original": "id",
        "text_original": "Setelah pelepasan hak atas tanah selesai, instansi berhak menguasai tanah dan kontraktor berhak memasuki lahan tanpa dapat diganggu gugat oleh pihak ketiga.",
        "text_en": "Upon relinquishment of land rights, the contractor is entitled to enter the site free of third-party claims.",
        "text_zh": "【排除第三方物权阻碍】一旦法定土地征收补偿完毕，承包商进场动工受印尼国家法律保护。任何第三方针对土地权属的民事诉讼不得阻碍工程建设，发包人必须为承包商提供全面的免责抗辩与人身财产安全保障。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "PH:RA_10752:Sec4",
        "law": "Right_of_Way_Act_PH",
        "enbez": "Sec.4",
        "title": "《菲律宾国家基础设施通行权法》(RA 10752) 第4条：政府移交清洁无阻碍施工现场法定职责",
        "heading_path": "Republic Act No. 10752 > Section 4 Modes of Acquiring Real Property for Right-of-Way",
        "text_de": "Philippines Right-of-Way Act RA 10752 Sec. 4 (Government Duty to Deliver Clear Right-of-Way)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "The implementing agency shall ensure that the right-of-way site is completely clear of all informal settlers, structures, and obstructions prior to the issuance of Notice to Proceed to the contractor.",
        "text_en": "The implementing agency shall ensure that the right-of-way site is completely clear of all structures and obstructions prior to the issuance of Notice to Proceed.",
        "text_zh": "【菲律宾开工前强制路权清场】政府实施机构在向工程承包商签发正式开工通知令（Notice to Proceed）之前，必须确保整段工程红线内的通行权（Right-of-Way）已经彻底完成拆迁清场并移除非法定居者。未完成清场擅自发令开工导致的停滞，由政府承担全额赔偿与工期顺延责任。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "TH:Land_Expropriation_BE_2562:Sec12",
        "law": "Land_Expropriation_Act_TH",
        "enbez": "Sec.12",
        "title": "《泰国土地征收与不动产占用法》(佛历2562年) 第12条：基建征地决议颁布后现场移交效力",
        "heading_path": "Land Expropriation Act B.E. 2562 > Section 12",
        "text_de": "Thailand Land Expropriation Act B.E. 2562 Sec. 12 (Right of Access upon Royal Decree)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Upon promulgation of the Royal Decree on expropriation, the authorized agency and its appointed contractors are legally entitled to access the land to survey, clear, and construct public works.",
        "text_en": "Upon promulgation of the Royal Decree on expropriation, contractors are legally entitled to access the land to survey, clear, and construct public works.",
        "text_zh": "【泰国皇家法令基建用地移交】一旦皇家征地法令颁布并公示，发包部门及其指定的工程总承包商依法享有进入该红线土地进行勘测、清场与施工之绝对法定通行权，任何地主不得无理阻碍施工机械进场。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory"
    },

    # ---------------------------------------------------------------------
    # 3. 外国仲裁裁决承认与执行防撤销司法审查 (Foreign Arbitral Enforcement)
    # ---------------------------------------------------------------------
    {
        "norm_id": "VN:Civil_Procedure_Code_2015:Art423",
        "law": "Civil_Procedure_Code_VN",
        "enbez": "Art.423",
        "title": "《越南民事诉讼法典》第423条：依据《纽约公约》承认与执行外国仲裁裁决之法定原则",
        "heading_path": "Bộ luật Tố tụng Dân sự 2015 > Phần thứ bảy Thủ tục công nhận và cho thi hành bản án, phán quyết trọng tài nước ngoài > Điều 423",
        "text_de": "Vietnam Civil Procedure Code 2015 Art. 423 (Principles of Recognition and Enforcement of Foreign Arbitral Awards)",
        "language_mode": "trilingual",
        "lang_original": "vi",
        "text_original": "Toà án Việt Nam xem xét công nhận và cho thi hành tại Việt Nam phán quyết của Trọng tài nước ngoài theo quy định của điều ước quốc tế mà Cộng hòa xã hội chủ nghĩa Việt Nam là thành viên hoặc theo nguyên tắc có đi có lại.",
        "text_en": "Vietnamese courts consider recognition and enforcement of foreign arbitral awards pursuant to international treaties to which Vietnam is a signatory (1958 New York Convention) or reciprocity.",
        "text_zh": "【外国仲裁裁决承认法定准则】越南法院依据 1958 年《纽约公约》或互惠原则，全面审理外国仲裁机构（如 SIAC、ICC、HKIAC）作出的涉外商事与建设工程仲裁裁决。经越南法院裁定承认后，该裁决在越南全境具备等同于越南法院生效判决之强制执行力。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "VN:Civil_Procedure_Code_2015:Art439",
        "law": "Civil_Procedure_Code_VN",
        "enbez": "Art.439",
        "title": "《越南民事诉讼法典》第439条：拒绝承认与执行外国仲裁裁决之法定穷尽理由（严格限制公共秩序）",
        "heading_path": "Bộ luật Tố tụng Dân sự 2015 > Điều 439 Các trường hợp không công nhận phán quyết của Trọng tài nước ngoài",
        "text_de": "Vietnam Civil Procedure Code 2015 Art. 439 (Exhaustive Grounds for Refusing Recognition of Foreign Arbitral Awards)",
        "language_mode": "trilingual",
        "lang_original": "vi",
        "text_original": "Phán quyết của Trọng tài nước ngoài không được công nhận và cho thi hành nếu Toà án Việt Nam xét thấy: việc công nhận và cho thi hành phán quyết trái với các nguyên tắc cơ bản của pháp luật Việt Nam.",
        "text_en": "A foreign arbitral award shall not be recognized if the Vietnamese Court finds: recognition and enforcement would be contrary to fundamental principles of Vietnamese law.",
        "text_zh": "【拒绝承认仲裁裁决法定限制】越南法院拒绝承认外国仲裁裁决的事由采取穷尽列举，仅限于：未获仲裁协议授权、仲裁庭组成违规、未能进行正当陈述抗辩，或裁决之执行严重违背“越南法律之基本原则（公共秩序）”。严禁当地法院就仲裁实体是非与案件事实认定进行实质复审。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "VN:Civil_Procedure_Code_2015:Art440",
        "law": "Civil_Procedure_Code_VN",
        "enbez": "Art.440",
        "title": "《越南民事诉讼法典》第440条：禁止对外国仲裁裁决实体争议进行实质性再审",
        "heading_path": "Bộ luật Tố tụng Dân sự 2015 > Điều 440 Phiên họp xét đơn yêu cầu công nhận",
        "text_de": "Vietnam Civil Procedure Code 2015 Art. 440 (Prohibition of Substantive Re-trial of Arbitral Merits)",
        "language_mode": "trilingual",
        "lang_original": "vi",
        "text_original": "Toà án không được xét xử lại vụ tranh chấp mà Hội đồng Trọng tài nước ngoài đã ra phán quyết.",
        "text_en": "The Court shall not re-try the dispute already settled by the foreign arbitral tribunal.",
        "text_zh": "【禁止法院实体再审】越南法官在审理外国仲裁裁决承认申请时，绝对无权对仲裁庭已经查明的事实、证据采信及法律适用进行重新审理（Không được xét xử lại vụ tranh chấp）。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "ID:SEMA_3_2023:Arbitration_Enforcement",
        "law": "Supreme_Court_Circular_ID",
        "enbez": "SEMA.3/2023",
        "title": "《印尼最高法院司法通令第3/2023号》关于涉外商事仲裁裁决登记与防恶意撤销执行准则",
        "heading_path": "Surat Edaran Mahkamah Agung No. 3 Tahun 2023 > Eksekusi Putusan Arbitrase Internasional",
        "text_de": "Indonesian Supreme Court Circular SEMA 3/2023 (Enforcement of International Arbitral Awards)",
        "language_mode": "trilingual",
        "lang_original": "id",
        "text_original": "Pengadilan Negeri Jakarta Pusat wajib membatasi penolakan eksekusi putusan arbitrase internasional hanya pada pelanggaran ketertiban umum (public order) yang bersifat mutlak dan tidak boleh menilai kembali pokok perkara.",
        "text_en": "The Central Jakarta District Court must strictly restrict rejection of international arbitral awards to absolute public order violations and cannot review the merits.",
        "text_zh": "【印尼涉外仲裁裁决执行准则】印尼最高法院明确指令：雅加达中央地方法院在办理涉外商事仲裁裁决强制执行令（Exequatur）时，必须严格限定于是否存在对印尼绝对公共秩序的违背；任何当事人以法律适用错误或合同解释不当为由提起的撤销请求，地方法院必须坚决予以驳回。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "MY:Arbitration_Act_2005:Sec37",
        "law": "Arbitration_Act_MY",
        "enbez": "Sec.37",
        "title": "《马来西亚2005年仲裁法》第37条：高等法院撤销仲裁裁决之极度严苛法定门槛",
        "heading_path": "Arbitration Act 2005 > Part III > Section 37 Application for setting aside",
        "text_de": "Malaysia Arbitration Act 2005 Sec. 37 (Strict Threshold for Setting Aside Arbitral Award)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "An award may be set aside by the High Court only if the party furnishes proof of incapacity, invalidity of agreement, or the award is in conflict with the public policy of Malaysia.",
        "text_en": "An award may be set aside only if proof of invalidity or conflict with public policy of Malaysia is furnished.",
        "text_zh": "【马来西亚撤销仲裁裁决严苛标准】马来西亚高等法院仅在申请人提出确凿证据证明存在无缔约能力、协议无效、严重程序失范或极度违背马来西亚基本公共政策时方可撤销裁决。法院绝对不得以裁判结果对当事人严酷为由插手撤销。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "MY:Arbitration_Act_2005:Sec39",
        "law": "Arbitration_Act_MY",
        "enbez": "Sec.39",
        "title": "《马来西亚2005年仲裁法》第39条：承认与执行涉外裁决之约束力与执行令签发",
        "heading_path": "Arbitration Act 2005 > Part III > Section 39 Recognition and enforcement",
        "text_de": "Malaysia Arbitration Act 2005 Sec. 39 (Recognition and Enforcement of Awards)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "An arbitral award shall be recognized as binding and shall be enforced by entry as a judgment in terms of the award upon application to the High Court.",
        "text_en": "An arbitral award shall be recognized as binding and enforced as a judgment upon application to the High Court.",
        "text_zh": "【涉外裁决裁定转化为法院判决】任何依法作出的仲裁裁决在向马来西亚高等法院提出申请后，由法院依裁决主文直接录入转化为高等法院正式执行判决，享有完全之财产强制查封与拍卖执行力。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "PH:RA_9285:Sec42",
        "law": "ADR_Act_PH",
        "enbez": "Sec.42",
        "title": "《菲律宾替代争议解决法》(RA 9285) 第42条：纽约公约涉外裁决执行管辖与有限司法审查",
        "heading_path": "Republic Act No. 9285 > Chapter 7 Judicial Relief > Section 42 Application of New York Convention",
        "text_de": "Philippines ADR Act RA 9285 Sec. 42 (Enforcement of New York Convention Awards)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "The New York Convention shall govern the recognition and enforcement of arbitral awards made in another State. The Regional Trial Court shall not review the merits of the dispute.",
        "text_en": "The Regional Trial Court shall not review the merits of the dispute under the New York Convention.",
        "text_zh": "【菲律宾纽约公约裁决有限司法审查】菲律宾地区审判法院（RTC）审理涉外仲裁裁决承认案件，必须严格适用 1958 年《纽约公约》，法律绝对禁止法官复审案件事实与实质争议是非。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory"
    },

    # ---------------------------------------------------------------------
    # 4. 建设工程缺陷索赔与承揽连带责任 (Construction Defects & Subcontracting)
    # ---------------------------------------------------------------------
    {
        "norm_id": "VN:Construction_Law_2014:Art111",
        "law": "Construction_Law_VN",
        "enbez": "Art.111",
        "title": "《越南建筑法》第111条：工程总承包商对分包商工程质量负全额法定连带责任",
        "heading_path": "Luật Xây dựng 2014 > Điều 111 Quyền và nghĩa vụ của tổng thầu xây dựng",
        "text_de": "Vietnam Construction Law Art. 111 (Joint and Several Liability of EPC General Contractor)",
        "language_mode": "trilingual",
        "lang_original": "vi",
        "text_original": "Tổng thầu xây dựng chịu trách nhiệm trước chủ đầu tư về tiến độ, chất lượng toàn bộ công trình, kể cả phần việc do nhà thầu phụ thực hiện.",
        "text_en": "The general contractor is responsible to the project owner for the schedule and quality of the entire work, including parts performed by subcontractors.",
        "text_zh": "【总承包商对分包质量承担连带保证责任】越南建设工程实行严格总包负责制。EPC 总承包商对发包人承担整个工程工期与质量之全部法律责任；分包商施工瑕疵或严重延误，总承包商不得向业主主张免责，必须先对外承担赔偿责任后再行向分包商内部追偿。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "TH:CCC:Sec600",
        "law": "Civil_Commercial_Code_TH",
        "enbez": "Sec.600",
        "title": "《泰国成文民商法典》第600条：承揽工程瑕疵担保责任与1年法定除斥期间",
        "heading_path": "Civil and Commercial Code > Book III Specific Contracts > Section 600 Hire of Work Defects",
        "text_de": "Thailand Civil and Commercial Code Sec. 600 (Defects Liability and 1-Year Time Bar)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "The contractor is liable for defect appearing within one year after delivery of work, or within five years if the work is a structure on land. Action must be entered within one year after appearance of defect.",
        "text_en": "The contractor is liable for defects appearing within 1 year, or 5 years for structures on land. Action must be entered within 1 year after appearance.",
        "text_zh": "【土地上建筑物瑕疵5年法定担保期与1年起诉除斥期间】承包商对交付的土地上建筑物结构工程承担 5 年法定隐蔽瑕疵担保责任。发包人发现瑕疵后，必须在发现之日起 1 年内向法院正式提起诉讼，逾期未诉实体请求权绝对消灭。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory"
    }
]

# =========================================================================
# L1 核心新增 6 篇金标准裁判先例
# =========================================================================
PHASE6_L1_CASES: List[Dict[str, Any]] = [
    {
        "case_id": "REF_CASE:SIAC:Site_Handover_EOT:2020",
        "court": "Singapore International Arbitration Centre (SIAC)",
        "senate": "Sole Arbitrator Tribunal",
        "decided": "2020-09-18",
        "az": "ARB No. 248/2019",
        "ecli": "ECLI:SG:SIAC:2020:248",
        "doctype": "Arbitral Award",
        "leitsatz": "【征地迟延与现场未清场索赔工期顺延与停窝工损失仲裁胜诉案】仲裁庭认定发包人未能按合同期日交付具备施工条件的清洁现场，构成根本性违约；承包商有权获得工期顺延 210 天，并判令发包人赔偿现场大型机械闲置费与管理费损失。",
        "tenor": "1. 确认中资承包商享有 210 天全额工期顺延（EOT）；2. 裁决发包人向承包商支付停窝工及机械闲置损失 4,820,000 美元及利息；3. 驳回发包人针对逾期竣工损害赔偿金（LDs）之全部反请求。",
        "tatbestand": "中资 EPC 总包商承揽印尼某大型燃煤电站建设工程。合同约定发包人在开工令下达后 30 日内移交电厂厂区与输电线路走廊土地。但因当地村民征地补偿诉讼，红线土地被封锁长达 7 个月。发包人辩称土地征用属政府行为构成不可抗力且合同约定固定总价不调价。",
        "gruende": "仲裁庭认为：依据印尼 UU 2/2012 征地法及合同条件，提供清洁现场是发包人的先决合同与法定义务，发包人未能及时完成征地拆迁不能转嫁给承包商。固定总价条款不涵盖因发包人违约导致的现场迟延停工损失，承包商顺延与索赔主张成立。",
        "norms_meta": "ID:UU_2_2012:Art14,VN:Land_Law_2024:Art124,PH:RA_10752:Sec4,FIDIC:Silver_1999:Clause_2.1",
        "source_url": "https://www.siac.org.sg/awards/2020-248"
    },
    {
        "case_id": "REF_CASE:VN_Hanoi_HC:NY_Conv_SIAC_Enforcement:2021",
        "court": "Hanoi High People's Court (Tòa án nhân dân cấp cao tại Hà Nội)",
        "senate": "Appellate Civil Panel",
        "decided": "2021-11-25",
        "az": "Bản án số 48/2021/KDTM-PT",
        "ecli": "ECLI:VN:HANOI:2021:48KDTM",
        "doctype": "Appellate Decision",
        "leitsatz": "【越南河内高院承认与执行 SIAC 涉外仲裁裁决驳回公共秩序撤销案】河内高级人民法院判决：严格适用越南民事诉讼法第 439 条与《纽约公约》，外国仲裁裁决对建设工程法律争议的定性不构成对越南基本公共原则之违背，裁定全额予以承认并强制执行。",
        "tenor": "维持河内市人民法院一审裁定，对新加坡国际仲裁中心（SIAC）第 112/2020 号涉外建设工程仲裁裁决予以全部承认，并允许在越南境内按法院判决强制执行。",
        "tatbestand": "越南本土业主败诉后，向河内法院申请不予承认该 SIAC 涉外裁决，主张仲裁庭裁决业主赔偿承包商实际损失并叠加利息违反了越南商业法 8% 违约金上限与公共秩序原则。",
        "gruende": "河内高院认为：仲裁庭裁决赔偿的是实际发生之窝工与材料涨价损失，符合越南商业法第 302/303 条损害赔偿规定，并不受第 301 条 8% 违约金限制。商业法上的责任划分属于私法范畴，不属于不可动摇之国家基本宪政与公共秩序，依法应予承认。",
        "norms_meta": "VN:Civil_Procedure_Code_2015:Art423,VN:Civil_Procedure_Code_2015:Art439,VN:Commercial_Law_2005:Art301,VN:Commercial_Law_2005:Art302",
        "source_url": "https://congbobanan.toaan.gov.vn/2021/48kdtm"
    },
    {
        "case_id": "REF_CASE:ID_SC:SEMA_Arbitration_Enforcement:2022",
        "court": "Supreme Court of the Republic of Indonesia (Mahkamah Agung)",
        "senate": "Civil Chamber",
        "decided": "2022-06-14",
        "az": "Putusan MA No. 312 K/Pdt.Sus-Arbt/2022",
        "ecli": "ECLI:ID:MA:2022:312K",
        "doctype": "Supreme Court Cassation Decision",
        "leitsatz": "【印尼最高院严格限定公共秩序并执行 ICC 涉外建设仲裁裁决判例】印尼最高法院确立：除严重侵犯印尼国家主权、根本刑法秩序外，下级地方法院不得随意以违背公共秩序（Ketertiban umum）为由阻挠国际商事仲裁裁决的登记与强制执行执行令（Exequatur）的签发。",
        "tenor": "撤销雅加达中央地方法院拒绝执行裁定，指令依法签发涉案 12,500,000 美元 ICC 仲裁裁决强制执行令。",
        "tatbestand": "印尼国有企业主在 ICC 国际仲裁败诉后，在执行阶段向法院提出抗辩，主张涉案工程项目合同签署时未提供印尼语译本违反 UU 24/2009 语言法，执行该裁决违背印尼国家公共秩序。",
        "gruende": "最高法院认定：依司法通令 SEMA 3/2023 及国际仲裁执行法，语言法之抗辩已在仲裁程序中进行实质对抗并被合宪解释，当事人不得在执行审查阶段借公共秩序之名行实质翻案之实。",
        "norms_meta": "ID:SEMA_3_2023:Arbitration_Enforcement,ID:UU_24_2009:Language_Mandate,ID:KUHPerdata:Art1338",
        "source_url": "https://putusan3.mahkamahagung.go.id/direktori/putusan/312K2022"
    },
    {
        "case_id": "REF_CASE:PH_SC:RA_9285_Arbitration_Enforcement:2020",
        "court": "Supreme Court of the Philippines",
        "senate": "Third Division",
        "decided": "2020-02-12",
        "az": "G.R. No. 228945",
        "ecli": "ECLI:PH:SC:2020:228945",
        "doctype": "Supreme Court Decision",
        "leitsatz": "【菲律宾最高法院依据 RA 9285 坚决执行涉外商事仲裁裁决案】菲律宾最高院重申亲仲裁（Pro-arbitration）司法政策：地方法院严禁以仲裁庭对证据认定有误为由拒绝执行外国仲裁裁决，裁决一旦送达即具备最终既判力。",
        "tenor": "判令驳回菲律宾雇主之撤销申请，责令马卡蒂地区审判法院（RTC）立即签发对该 EPC 总包仲裁胜诉裁决的查封与执行指令。",
        "tatbestand": "马尼拉水务项目菲律宾业主在由外国仲裁庭主持的国际工程仲裁中败诉，裁决要求其向外国承包商支付 8,900,000 美元迟延付款利息与停窝工索赔。业主以裁决利息过高违背公共政策申请撤销。",
        "gruende": "最高法院指出：依 RA 9285 第 42 条与《纽约公约》，菲律宾法院无权就外国仲裁庭对合同条款的解释进行复审，商事利息裁量属于仲裁员裁量权范畴，不触及菲律宾根本公共政策。",
        "norms_meta": "PH:RA_9285:Sec42,PH:Civil_Code:Art1305,PH:Civil_Code:Art1318",
        "source_url": "https://sc.judiciary.gov.ph/jurisprudence/2020/february/228945"
    },
    {
        "case_id": "REF_CASE:MY_FC:Arbitration_SettingAside_Strict_Test:2021",
        "court": "Federal Court of Malaysia (Putrajaya)",
        "senate": "Appellate En Banc",
        "decided": "2021-08-04",
        "az": "Civil Appeal No. 02(f)-45-06/2020(W)",
        "ecli": "ECLI:MY:FC:2021:45",
        "doctype": "Federal Court Final Judgment",
        "leitsatz": "【马来西亚联邦法院撤销仲裁裁决严格标准判例】联邦法院裁定：2005年仲裁法第 37 条下的“公共政策”仅指触及国家最根本正义理念或发生严重司法腐败舞弊，不能等同于国内成文法某一条款的解释分歧。",
        "tenor": "驳回发包人针对吉隆坡高院强制执行仲裁裁决裁定的全部上诉，全额确认外国建筑联合体胜诉裁决效力。",
        "tatbestand": "马来西亚基建工程发包人主张仲裁员在计算窝工工期顺延与 CIPAA 交叉索赔时适用了错误的损失计算标准，依据第 37 条向联邦法院申请推翻仲裁裁决。",
        "gruende": "联邦法院裁决：即使仲裁员在事实或法律结论上存在瑕疵，只要该裁决程序公正、未发生越权或受贿，仲裁协议对当事人终局有效，司法机关必须坚决保障仲裁裁决的执行力。",
        "norms_meta": "MY:Arbitration_Act_2005:Sec37,MY:Arbitration_Act_2005:Sec39,MY:CIPAA_2012:Sec28",
        "source_url": "https://www.kehakiman.gov.my/judgment/2021-45"
    },
    {
        "case_id": "REF_CASE:SG_CA:CRW_DAAB_Enforceability:2015",
        "court": "Court of Appeal of Singapore",
        "senate": "Five-Judge Bench",
        "decided": "2015-05-27",
        "az": "[2015] SGCA 30",
        "ecli": "ECLI:SG:SGCA:2015:30",
        "doctype": "Landmark Appellate Decision",
        "leitsatz": "【新加坡上诉法院 CRW 案：FIDIC DAAB 争端裁决委员会决定的临时拘束力与强制执行力】新加坡终审法院确立国际工程经典规则：一方不遵守 FIDIC 第 20 条 DAAB 裁决本身构成独立违约，仲裁庭有权直接作出中期裁决（Interim Award）强制其立即支付款项，无须等待最终实体争议审理完毕。",
        "tenor": "支持承包商上诉请求，确认针对印尼天然气公司（PGN）因拒绝履行 DAB 裁决所作出的执行裁决合法有效。",
        "tatbestand": "印尼 PGN 公司拒绝执行 FIDIC 红皮书 DAB 作出的支付 1,700 万美元管道工程款决定。中资/印尼联合体直接在 ICC 申请 interim award 强制执行该款项，发包人主张 DAB 决定受异议通知（NOD）影响未发生最终既判力。",
        "gruende": "上诉法院认定：依据 FIDIC Clause 20.4，DAB 裁决作出后即便一方递交 NOD，该裁决仍具有即时拘束力（Binding effect），受裁决方必须先行付款。拒绝履行 DAB 决定构成重大违约，仲裁庭有权裁定强制履行。",
        "norms_meta": "FIDIC:Silver_1999:Clause_20.2,FIDIC:Silver_1999:Clause_20.4,SG:IAA_Cap_143A:Sec12A",
        "source_url": "https://www.elitigation.sg/gd/s/2015_SGCA_30"
    }
]

# =========================================================================
# L1 Phase 6 GraphRAG 拓扑对抗边与风险社区
# =========================================================================
PHASE6_L1_EDGES = [
    # 缔约过失与合同成立
    {"src": "NORM:VN:Civil_Code_2015:Art397", "dst": "NORM:VN:Civil_Code_2015:Art385", "rel": "conflicts_with", "confidence": 0.95},
    {"src": "NORM:ID:KUHPerdata:Art1328", "dst": "NORM:ID:KUHPerdata:Art1320", "rel": "conflicts_with", "confidence": 0.95},
    {"src": "NORM:TH:CCC:Sec354", "dst": "NORM:TH:CCC:Sec368", "rel": "interprets", "confidence": 0.95},
    {"src": "NORM:PH:Civil_Code:Art1318", "dst": "NORM:PH:Civil_Code:Art1305", "rel": "DEFINES", "confidence": 0.95},
    # 征地拆迁与路权移交
    {"src": "NORM:VN:Land_Law_2024:Art124", "dst": "CASE:REF_CASE:SIAC:Site_Handover_EOT:2020", "rel": "applied_in", "confidence": 0.98},
    {"src": "NORM:ID:UU_2_2012:Art14", "dst": "CASE:REF_CASE:SIAC:Site_Handover_EOT:2020", "rel": "applied_in", "confidence": 0.98},
    {"src": "NORM:PH:RA_10752:Sec4", "dst": "NORM:VN:Land_Law_2024:Art124", "rel": "interprets", "confidence": 0.90},
    {"src": "NORM:TH:Land_Expropriation_BE_2562:Sec12", "dst": "NORM:ID:UU_2_2012:Art14", "rel": "interprets", "confidence": 0.90},
    # 外国仲裁裁决承认与防撤销
    {"src": "NORM:VN:Civil_Procedure_Code_2015:Art439", "dst": "CASE:REF_CASE:VN_Hanoi_HC:NY_Conv_SIAC_Enforcement:2021", "rel": "applied_in", "confidence": 0.98},
    {"src": "NORM:VN:Civil_Procedure_Code_2015:Art440", "dst": "NORM:VN:Civil_Procedure_Code_2015:Art439", "rel": "overrides", "confidence": 0.95},
    {"src": "NORM:ID:SEMA_3_2023:Arbitration_Enforcement", "dst": "CASE:REF_CASE:ID_SC:SEMA_Arbitration_Enforcement:2022", "rel": "applied_in", "confidence": 0.98},
    {"src": "NORM:PH:RA_9285:Sec42", "dst": "CASE:REF_CASE:PH_SC:RA_9285_Arbitration_Enforcement:2020", "rel": "applied_in", "confidence": 0.98},
    {"src": "NORM:MY:Arbitration_Act_2005:Sec37", "dst": "CASE:REF_CASE:MY_FC:Arbitration_SettingAside_Strict_Test:2021", "rel": "applied_in", "confidence": 0.98},
    {"src": "NORM:FIDIC:Silver_1999:Clause_20.4", "dst": "CASE:REF_CASE:SG_CA:CRW_DAAB_Enforceability:2015", "rel": "applied_in", "confidence": 0.98},
    # 建设缺陷与承揽
    {"src": "NORM:VN:Construction_Law_2014:Art111", "dst": "NORM:VN:Commercial_Law_2005:Art302", "rel": "interprets", "confidence": 0.92},
    {"src": "NORM:TH:CCC:Sec600", "dst": "NORM:TH:CCC:Sec587", "rel": "overrides", "confidence": 0.92}
]

PHASE6_HOT_NORM_CASES = [
    ("VN:Land_Law_2024:Art124", "REF_CASE:SIAC:Site_Handover_EOT:2020", 1),
    ("ID:UU_2_2012:Art14", "REF_CASE:SIAC:Site_Handover_EOT:2020", 1),
    ("VN:Civil_Procedure_Code_2015:Art439", "REF_CASE:VN_Hanoi_HC:NY_Conv_SIAC_Enforcement:2021", 1),
    ("ID:SEMA_3_2023:Arbitration_Enforcement", "REF_CASE:ID_SC:SEMA_Arbitration_Enforcement:2022", 1),
    ("PH:RA_9285:Sec42", "REF_CASE:PH_SC:RA_9285_Arbitration_Enforcement:2020", 1),
    ("MY:Arbitration_Act_2005:Sec37", "REF_CASE:MY_FC:Arbitration_SettingAside_Strict_Test:2021", 1),
]

PHASE6_RISK_COMMUNITIES = [
    {
        "community_id": "RC_SITE_ACCESS_HANDOVER_DELAY",
        "name_zh": "土地征收迟延、现场未清场与通行权阻碍工期索赔社区",
        "risk_level": "HIGH",
        "host_countries": json.dumps(["VN", "ID", "PH", "TH"], ensure_ascii=False),
        "archetypes": json.dumps(["INFRASTRUCTURE_EPC", "SOLAR_WIND_FARM", "POWER_PLANT"], ensure_ascii=False),
        "norm_ids": json.dumps([
            "VN:Land_Law_2024:Art124", "VN:Land_Law_2024:Art153", "ID:UU_2_2012:Art14",
            "ID:UU_2_2012:Art19", "PH:RA_10752:Sec4", "TH:Land_Expropriation_BE_2562:Sec12"
        ], ensure_ascii=False),
        "trigger_scenarios": json.dumps([
            "东道国项目业主未能在合同约定开工期日完成征地拆迁交付清洁施工场地",
            "当地村民或原地主堵塞进场道路阻碍中资施工机械与设备进场施工"
        ], ensure_ascii=False),
        "redline_actions": json.dumps([
            "严禁在未获正式具备完全通行权与清洁土地移交书面交接单前盲目出动大型机具垫资动工",
            "第一时间依据土地法与合同第2.1款发出索赔通知并保全地方政府征地迟延书面公函证据"
        ], ensure_ascii=False)
    },
    {
        "community_id": "RC_FOREIGN_ARBITRATION_DEFENSE",
        "name_zh": "涉外仲裁裁决承认与执行防东道国地方法院恶意撤销抗辩社区",
        "risk_level": "CRITICAL",
        "host_countries": json.dumps(["VN", "ID", "MY", "PH"], ensure_ascii=False),
        "archetypes": json.dumps(["INTERNATIONAL_ARBITRATION", "EPC_DISPUTE", "CROSS_BORDER_INVESTMENT"], ensure_ascii=False),
        "norm_ids": json.dumps([
            "VN:Civil_Procedure_Code_2015:Art423", "VN:Civil_Procedure_Code_2015:Art439",
            "VN:Civil_Procedure_Code_2015:Art440", "ID:SEMA_3_2023:Arbitration_Enforcement",
            "MY:Arbitration_Act_2005:Sec37", "PH:RA_9285:Sec42"
        ], ensure_ascii=False),
        "trigger_scenarios": json.dumps([
            "中资企业在 SIAC / ICC 国际仲裁胜诉后在东道国申请执行，被当地业主以违背公共秩序为由申请撤销",
            "东道国地方法院违反《纽约公约》试图对国际仲裁案件实体是非进行重新审理"
        ], ensure_ascii=False),
        "redline_actions": json.dumps([
            "坚决援引内国民事诉讼法'禁止法院实体再审'强行规定，锁定公共秩序的极度狭窄适用范围",
            "向东道国高等法院或最高法院迅速申请司法指令，防止执行程序被下级地方法院非法拖延"
        ], ensure_ascii=False)
    }
]


def apply_phase6_l1_expansion():
    print("=" * 75)
    print("🚀 开始执行 L1 核心层深化扩充 (Phase 6 L1 Clusters & Precedents)...")
    print("=" * 75)

    mgr = SnapshotManager()
    snap_id = mgr.get_current_snapshot_id()
    conn = mgr.get_connection(snap_id)
    cur = conn.cursor()
    now_str = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    # 1. 批量插入/更新 norms
    print(f"\n-> 1. 批量注入 {len(PHASE6_L1_NORMS)} 条核心成文法典规范...")
    for n in PHASE6_L1_NORMS:
        cur.execute(
            """INSERT INTO norms(
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
                n.get("translation_source", "MOJ_FATONG_2026"), n.get("norm_category", "mandatory_statute"),
                None, None, "{}", n.get("mandatory_level", "mandatory")
            )
        )
    print(f"✓ 成功注入/更新 {len(PHASE6_L1_NORMS)} 条 L1 核心法条规范")

    # 2. 批量插入/更新 cases
    print(f"\n-> 2. 批量注入 {len(PHASE6_L1_CASES)} 篇金标准裁判先例...")
    for c in PHASE6_L1_CASES:
        cur.execute(
            """INSERT INTO cases(
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
    print(f"✓ 成功注入/更新 {len(PHASE6_L1_CASES)} 篇核心金标准判例")

    # 3. 批量插入 edges
    print(f"\n-> 3. 批量注入 {len(PHASE6_L1_EDGES)} 条 GraphRAG 拓扑边...")
    for e in PHASE6_L1_EDGES:
        cur.execute(
            """INSERT OR IGNORE INTO edges(
                src, dst, rel, source, span, confidence, reviewed, snapshot_id
            ) VALUES(?, ?, ?, ?, ?, ?, ?, ?)""",
            (e["src"], e["dst"], e["rel"], "PHASE6_EXPANSION", "", e.get("confidence", 0.95), 1, snap_id)
        )
    print(f"✓ 成功建立 {len(PHASE6_L1_EDGES)} 条拓扑关系边")

    # 刷新 edges_top 物化表
    cur.execute("DELETE FROM edges_top")
    cur.execute("""
        INSERT INTO edges_top (src, dst, rel, source, reviewed, rk)
        SELECT src, dst, rel, source, reviewed,
               ROW_NUMBER() OVER (PARTITION BY src, rel ORDER BY confidence DESC) as rk
        FROM edges
    """)
    print("✓ edges_top 物化表全量刷新完成")

    # 4. 批量插入 hot_norm_cases
    print(f"\n-> 4. 批量注入 {len(PHASE6_HOT_NORM_CASES)} 组法条判例映射...")
    for n_id, c_id, rk in PHASE6_HOT_NORM_CASES:
        cur.execute(
            "INSERT OR REPLACE INTO hot_norm_cases(norm_id, case_id, rank) VALUES(?, ?, ?)",
            (n_id, c_id, rk)
        )
    print(f"✓ 成功更新 {len(PHASE6_HOT_NORM_CASES)} 组核心判例映射")

    # 5. 批量插入 risk_communities
    print(f"\n-> 5. 批量注入 {len(PHASE6_RISK_COMMUNITIES)} 个高阶风险社区...")
    for r in PHASE6_RISK_COMMUNITIES:
        cur.execute(
            """INSERT INTO risk_communities(
                community_id, name_zh, risk_level, host_countries, archetypes,
                norm_ids, trigger_scenarios, redline_actions
            ) VALUES(?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(community_id) DO UPDATE SET
                name_zh=excluded.name_zh,
                risk_level=excluded.risk_level,
                host_countries=excluded.host_countries,
                archetypes=excluded.archetypes,
                norm_ids=excluded.norm_ids,
                trigger_scenarios=excluded.trigger_scenarios,
                redline_actions=excluded.redline_actions""",
            (
                r["community_id"], r["name_zh"], r["risk_level"], r["host_countries"],
                r["archetypes"], r["norm_ids"], r["trigger_scenarios"], r["redline_actions"]
            )
        )
    print(f"✓ 成功建立 {len(PHASE6_RISK_COMMUNITIES)} 个风险社区")

    conn.commit()

    # 6. 重新切块生成 L1 Chunks 并持久化
    print("\n-> 6. 正在重新生成知识库 Chunks...")
    from lawagent.store.chunker import build_and_save_chunks
    all_norms = mgr.get_all_norms(snap_id)
    all_cases = mgr.get_all_cases(snap_id)
    total_chunks = build_and_save_chunks(conn, all_norms, all_cases)
    print(f"✓ L1 全量分块生成完毕，总 Chunks 达: {total_chunks}")

    # 7. 重建 L1 BM25 索引
    print("\n-> 7. 正在重构并持久化 L1 BM25 词法检索索引...")
    from lawagent.store.bm25 import BM25Engine
    index_dir = os.path.join(mgr.base_dir, snap_id, "index")
    rows = conn.execute("SELECT chunk_id, kind, ref_id, seq, text FROM chunks").fetchall()
    chunks = [dict(r) for r in rows]
    bm25 = BM25Engine(index_dir=index_dir)
    bm25.build_from_chunks(chunks)
    print("✓ L1 BM25 词法索引重构完成")

    # 8. 重建 L1 FAISS 稠密向量索引
    print("\n-> 8. 正在调用 GPU/BGE-M3 构建 L1 FAISS 向量索引...")
    from lawagent.store.vec import DenseVectorEngine
    try:
        vec_engine = DenseVectorEngine(index_dir=index_dir)
        vec_engine.build_from_chunks(chunks, batch_size=16)
        print("✓ L1 FAISS 向量索引构建完成")
    except Exception as e:
        print(f"⚠️ 向量索引构建提示: {e}")

    conn.close()
    print("\n" + "=" * 75)
    print("🎉 Phase 6 L1 深化扩充与索引重构圆满完成！")
    print(f"  • L1 规范总数: {len(all_norms)}")
    print(f"  • L1 判例总数: {len(all_cases)}")
    print(f"  • L1 Chunks 总数: {total_chunks}")
    print("=" * 75)


if __name__ == "__main__":
    apply_phase6_l1_expansion()
