# -*- coding: utf-8 -*-
"""东盟核心六国（ID/VN/MY/SG/TH/PH）与国际条约底座体系化补充数据
包含：
1. 真实已颁布成文法条（民商法基础请求权、公司法、破产法、工程法、时效法）
2. 国际条约（Apostille海牙公约、送达、取证、双边司法协助、BIT终止转轨）
3. 本土标准施工合同（大马 PAM 2018 / PWD 203A、新加坡 PSSCOC 2020、SIAC 2025）
4. 标杆司法裁判（德式四要素严格达标，无机械套话）
"""

SUPPLEMENT_SIX_NORMS_L1 = [
    # ---------------- 印度尼西亚 (asean_id) ----------------
    {
        "norm_id": "ID:UU_6_2023:Art_EIA_Licensing",
        "law": "UU No. 6/2023",
        "enbez": "Pasal 24 jo. UU 11/2020",
        "title": "创造就业法环评审批分级与建设许可准入",
        "heading_path": "UU No. 6/2023 | Bab III Peningkatan Ekosistem Investasi | Bagian Keempat Lingkungan Hidup",
        "text_zh": "【中文释义】废除旧版环评（AMDAL）一刀切审批制度，实行基于经营风险等级的环保与建设资质分级监管：高风险工业及重大基建项目强制进行环境影响分析（AMDAL）并取得中央环境与林业部环境可行性批复；中低风险项目凭环境管理与监测承诺函（UKL-UPL 或 SPPL）即可核发经营许可证（NIB）。外资承包商必须依法取得工程服务资质评级（SBU），替代已废止的旧制 IUJK 许可证。",
        "text_en": "Environmental impact approvals are restructured based on risk-based business licensing. High-risk activities require AMDAL and Environmental Approval from the central government, while medium-low risk requires UKL-UPL or SPPL. Foreign construction entities must obtain SBU certification registered under the OSS system.",
        "text_original": "Pemerintah Pusat menetapkan perizinan berusaha berbasis risiko. Analisis mengenai dampak lingkungan hidup (AMDAL) wajib dimiliki bagi setiap rencana usaha dan/atau kegiatan yang berdampak penting terhadap lingkungan hidup sebagai dasar penerbitan Persetujuan Lingkungan.",
        "language_mode": "trilingual",
        "norm_category": "mandatory_statute",
        "elements_json": '{"subject": "外资工业与基础设施承包商", "trigger": "在印尼开展工程承包或矿冶开发投资", "requirements": ["环境风险等级核定", "高风险项目取得中央环境可行性批复AMDAL", "取得OSS注册之有效建筑服务资质评级SBU"], "legal_effect": "未取得批复擅自开工构成行政违法，面临勒令停工、罚款直至吊销NIB投资许可"}'
    },
    {
        "norm_id": "ID:UU_40_2007:Art92_97_Directors_Duty",
        "law": "UU No. 40/2007",
        "enbez": "Pasal 92 & 97",
        "title": "公司法董事会勤勉义务与越权连带赔偿责任",
        "heading_path": "UU No. 40/2007 tentang Perseroan Terbatas | Bab VII Direksi dan Dewan Komisaris",
        "text_zh": "【中文释义】董事会（Direksi）负责按照公司章程宗旨与公司利益进行经营管理。各董事对因其过错或怠于履行忠实勤勉义务导致的公司损失承担个人无限连带赔偿责任。董事若明知交易损害公司或越权（Ultra Vires）签署未经法定审批的对外担保或重大资产处置合同，不得援引商业判断规则免责。",
        "text_en": "The Board of Directors (Direksi) manages the company in good faith and with full responsibility. Each member of the Board shall be personally and solidarily liable for losses of the company if that member is at fault or negligent in performing duties.",
        "text_original": "Direksi bertanggung jawab atas pengurusan Perseroan dengan itikad baik dan penuh tanggung jawab. Setiap anggota Direksi bertanggung jawab penuh secara pribadi atas kerugian Perseroan apabila yang bersangkutan bersalah atau lalai menjalankan tugasnya.",
        "language_mode": "trilingual",
        "norm_category": "mandatory_statute",
        "elements_json": '{"subject": "印尼PT公司董事会成员", "trigger": "签署重大合同或对外提供借款担保", "requirements": ["遵循善意与勤勉管理准则", "符合公司章程业务范围与授权限制", "无重大过失与利益冲突"], "legal_effect": "越权或失职造成的损害由董事个人承担无限连带赔偿责任"}'
    },
    {
        "norm_id": "ID:UU_40_2007:Art98_Statutory_Representation",
        "law": "UU No. 40/2007",
        "enbez": "Pasal 98",
        "title": "公司法法定代表权与章程内部限制对抗效力",
        "heading_path": "UU No. 40/2007 tentang Perseroan Terbatas | Bab VII Direksi dan Dewan Komisaris",
        "text_zh": "【中文释义】董事会有权在法庭内外代表公司行使一切民事权利。章程对董事代表权所作的限制，除非经在法律和人权部公司登记系统（AHU）依法登记并予以公告，否则不得对抗善意第三人。但对于重大资产转让及担保（超过净资产50%），必须经股东大会（GMS）特别决议批准，该限制属于法定强行规则，第三人负有合理审查注意义务。",
        "text_en": "The Board of Directors represents the company in and out of court. Any limitation on the representative power of the Board in the articles of association cannot be invoked against bona fide third parties unless properly registered in the AHU database and made public.",
        "text_original": "Direksi mewakili Perseroan baik di dalam maupun di luar pengadilan. Pembatasan kewenangan Direksi dalam Anggaran Dasar tidak berlaku bagi pihak ketiga yang beritikad baik, kecuali undang-undang menentukan lain.",
        "language_mode": "trilingual",
        "norm_category": "mandatory_statute",
        "elements_json": '{"subject": "合资公司签约相对人", "trigger": "与印尼PT公司法定代表人签署对外担保或收购协议", "requirements": ["查核AHU公司最新存续与章程登记", "查核是否涉及超净资产50%之法定GMS审批"], "legal_effect": "未经法定必要审批之担保可能对公司不生效力，签约相对人被认定非善意第三人"}'
    },
    {
        "norm_id": "ID:UU_40_2007:Art108_BOC_Supervisory_Approval",
        "law": "UU No. 40/2007",
        "enbez": "Pasal 108",
        "title": "公司法监事会章程前置批准权与中资合资锁",
        "heading_path": "UU No. 40/2007 tentang Perseroan Terbatas | Bab VII Direksi dan Dewan Komisaris",
        "text_zh": "【中文释义】监事会（Dewan Komisaris）根据公司章程对董事会的管理行为执行监督，并在章程授权范围内对董事会的特定民商事行为给予事先书面批准（Approval）或协助。在中资出海合资企业中，章程常明确将对外大额举债、向银行申请授信、以公司资产设定抵押或动产担保、提起诉讼仲裁列为必须经监事会一致书面同意的事项。",
        "text_en": "The Board of Commissioners (Dewan Komisaris) supervises management policies and provides advice to the Direksi. The articles of association may require prior approval of the Board of Commissioners for specific legal acts performed by the Direksi.",
        "text_original": "Dewan Komisaris melakukan pengawasan atas kebijakan pengurusan dan memberikan nasihat kepada Direksi. Anggaran dasar dapat menentukan bahwa Direksi hanya dapat melakukan perbuatan hukum tertentu dengan persetujuan Dewan Komisaris.",
        "language_mode": "trilingual",
        "norm_category": "mandatory_statute",
        "elements_json": '{"subject": "PT合资公司董事会与签约相对人", "trigger": "实施章程约定受限的重大财务与资产处置行为", "requirements": ["调阅公司章程第108条配套条款", "取得监事会Dewan Komisaris正式书面批准函"], "legal_effect": "欠缺监事会事先书面核准所签之担保或借贷合同在印尼法院极易被判决对公司无效"}'
    },
    {
        "norm_id": "ID:KUHPerdata:Art1381_Extinction_Obligations",
        "law": "KUHPerdata",
        "enbez": "Pasal 1381",
        "title": "民法典债的消灭十种法定原因",
        "heading_path": "Kitab Undang-Undang Hukum Perdata | Buku Ketiga tentang Perikatan | Bab IV",
        "text_zh": "【中文释义】债因下列十种法定原因而消灭：(1) 清偿/履行；(2) 提出清偿与提存；(3) 债务更新（Novasi）；(4) 抵销（Kompensasi）；(5) 混同（Percampuran Utang）；(6) 债务免除；(7) 标的物灭失；(8) 宣告无效或撤销；(9) 解除条件成就；(10) 消灭时效完成。在涉外工程争议中，当事人主张合同债务已终止，必须证明符合前述法定原因之一。",
        "text_en": "Obligations are extinguished by: payment, tender followed by consignment, novation, compensation/set-off, confusion/merger of debts, remission of debt, loss of the thing due, nullity or rescission, fulfillment of a resolutory condition, or prescription.",
        "text_original": "Perikatan-perikatan hapus: karena pembayaran; karena penawaran pembayaran tunai diikuti dengan penyimpanan atau penitipan; karena pembaruan utang; karena kompensasi atau perjumpaan utang; karena percampuran utang; karena pembebasan utang; karena musnahnya barang yang terutang; karena kebatalan atau pembatalan; karena berlakunya suatu syarat pembatalan; dan karena lewatnya waktu.",
        "language_mode": "trilingual",
        "norm_category": "mandatory_statute",
        "elements_json": '{"subject": "印尼法下债权人与债务人", "trigger": "工程款支付、违约索赔或担保清偿争议", "requirements": ["举证十种法定消灭事由之一的构成事实", "符合对应事由之法定形式与实质要件"], "legal_effect": "原债权债务关系自消灭事由发生时归于消灭，从权利及担保物权同步消灭"}'
    },
    {
        "norm_id": "ID:KUHPerdata:Art1425_1429_Setoff",
        "law": "KUHPerdata",
        "enbez": "Pasal 1425-1429",
        "title": "民法典法定抵销权要件及商事排除",
        "heading_path": "Kitab Undang-Undang Hukum Perdata | Buku Ketiga tentang Perikatan | Bab IV Bagian 3",
        "text_zh": "【中文释义】当二人互负同种类且清偿期均已届至的金钱或同种类物债务时，即使未通知债务人，两项债务自其并存之日起在对应数额范围内依法产生当然抵销的法律效果。但商事合同当事人可明确约定排除法定抵销权（No Set-off Clause，如EPC合同约定业主不得擅自从进度款中抵扣未经认定的质量违约金），该约定不违反印尼公共秩序，具有约束力。",
        "text_en": "Compensation occurs by operation of law whenever two persons are mutually indebted to each other in liquidated and immediately due sums of money or fungible goods. Contractual parties in commercial contracts may agree to waive or exclude statutory set-off.",
        "text_original": "Jika dua orang saling berutang satu sama lain, maka terjadilah antara mereka suatu perjumpaan utang, dengan mana kedua utang itu dihapuskan. Perjumpaan terjadi demi hukum, bahkan tanpa setahu orang-orang yang berutang.",
        "language_mode": "trilingual",
        "norm_category": "mandatory_statute",
        "elements_json": '{"subject": "工程发包人与承包商", "trigger": "工程结算扣款或反索赔主张", "requirements": ["互负金钱或种类物给付义务", "两项债权均已确定并届清偿期", "合同未作排除抵销之明示商事约定"], "legal_effect": "在等额限度内互负债务归于消灭；若合同含有No Set-off条款则强行扣划构成违约"}'
    },
    {
        "norm_id": "ID:KUHPerdata:Art1946_1977_Limitation",
        "law": "KUHPerdata",
        "enbez": "Pasal 1946-1977",
        "title": "民法典消灭时效制度、时效中断与放弃无效",
        "heading_path": "Kitab Undang-Undang Hukum Perdata | Buku Keempat tentang Pembuktian dan Daluwarsa",
        "text_zh": "【中文释义】印尼民法典一般财产性债权的消灭时效为30年（Pasal 1967），但工程承揽人追索劳务及材料款享有特殊短期时效。诉讼时效因债务人书面承认债务、向法院起诉、签发带有法律效力的正式令状（Somasi/Requisitoir）而发生法律中断。当事人不得事先约定放弃时效利益，事先放弃时效的条款绝对无效，但时效届满后债务人可放弃已获得的消灭时效抗辩权。",
        "text_en": "The general prescription period for obligations is 30 years, subject to shorter specific statutory limits. Prescription is interrupted by recognition of debt by the debtor, judicial summons, or formal legal demand. One cannot waive prescription in advance.",
        "text_original": "Daluwarsa adalah suatu alat untuk memperoleh sesuatu atau untuk dibebaskan dari suatu perikatan dengan lewatnya suatu waktu tertentu. Seseorang tidak dapat melepaskan daluwarsa sebelum tiba waktunya; tetapi ia boleh melepaskan daluwarsa yang telah diperolehnya.",
        "language_mode": "trilingual",
        "norm_category": "mandatory_statute",
        "elements_json": '{"subject": "涉外索赔当事人", "trigger": "逾期主张工程索赔或借款清偿", "requirements": ["未逾法定消灭时效期间", "主张时效中断需举证起诉记录或债务人书面承认文件", "无事先放弃时效之无效约定"], "legal_effect": "消灭时效完成后债务人取得实体抗辩权，自然债务不具有诉讼强制执行力"}'
    },
    {
        "norm_id": "ID:UU_37_2004:Art55_59_Stay_Secured_Creditor",
        "law": "UU No. 37/2004",
        "enbez": "Pasal 55-59",
        "title": "破产法有担保债权人别除权90天行权冻结期",
        "heading_path": "UU No. 37/2004 tentang Kepailitan dan PKPU | Bab II Kepailitan | Bagian Kelima",
        "text_zh": "【中文释义】持有抵押权（Hak Tanggungan）、动产信托担保（Jaminan Fidusia）或质权的有担保债权人，在债务人被宣告破产或进入延期偿债程序（PKPU）时享有别除权（Separatist），可如同未发生破产一样直接执行担保物。但该别除权在裁定作出之日起最长面临90天的法定中止行权期（Stay），冻结期内担保权人不得拍卖处置财产，以保护债务人资产完整性及重整谈判。",
        "text_en": "Secured creditors holding Hak Tanggungan, Fiduciary Guarantee, or Pledge may enforce their rights as if no bankruptcy occurred. However, their execution rights are suspended for a maximum period of 90 days from the date of the bankruptcy declaration (stay period).",
        "text_original": "Hak eksekusi Kreditor pemegang hak jaminan kebendaan ditangguhkan untuk jangka waktu paling lama 90 hari sejak tanggal putusan pernyataan pailit diucapkan.",
        "language_mode": "trilingual",
        "norm_category": "mandatory_statute",
        "elements_json": '{"subject": "有担保中资银团与承包商", "trigger": "印尼债务人被申请PKPU或破产清算", "requirements": ["持有依法登记之优先担保物权", "遵守90天法定暂时中止执行期", "在冻结期届满后向破产管理人申报行权"], "legal_effect": "冻结期内私自拍卖担保物自始无效；期满后可依据特别法直接变现受偿"}'
    },
    {
        "norm_id": "ID:UU_37_2004:Art245_285_PKPU_Homologasi",
        "law": "UU No. 37/2004",
        "enbez": "Pasal 245-285",
        "title": "破产法PKPU和解计划表决比例与司法认可拘束力",
        "heading_path": "UU No. 37/2004 tentang Kepailitan dan PKPU | Bab III PKPU | Bagian Ketiga Perdamaian",
        "text_zh": "【中文释义】在PKPU延期偿债程序中，债务人提交的和解协议（Rencana Perdamaian）必须获得出席债权人会议的：(1) 超过二分之一普通无担保债权人且代表无担保债权总额至少三分之二；以及 (2) 超过二分之一有担保债权人且代表有担保债权总额至少三分之二的双重同意。商事法院依法裁定批准和解协议（Homologasi）后，该协议对所有已知及未知债权人具有全面拘束力，即使持反对意见的中资债权人亦必须遵照执行减免或展期。",
        "text_en": "A composition plan is approved if agreed by more than 1/2 of unsecured creditors representing at least 2/3 of claims, and more than 1/2 of secured creditors representing at least 2/3 of claims. Upon court confirmation (Homologasi), it binds all creditors.",
        "text_original": "Rencana perdamaian diterima apabila disetujui oleh lebih dari 1/2 jumlah kreditor konkuren yang hadir dan mewakili paling sedikit 2/3 dari seluruh piutang, dan kreditor dengan hak jaminan. Perdamaian yang telah disahkan mengikat semua kreditor.",
        "language_mode": "trilingual",
        "norm_category": "mandatory_statute",
        "elements_json": '{"subject": "PKPU程序全体债权人与债务人", "trigger": "PKPU法定和解期内就债务展期与债转股表决", "requirements": ["达到无担保债权人人数过半且金额超2/3法定比例", "达到有担保债权人人数过半且金额超2/3法定比例", "取得商事法院Homologasi生效判决"], "legal_effect": "和解协议依法发生终局确定效力，未按期申报或投票反对之债权人同样受削债条款约束"}'
    },

    # ---------------- 越南 (asean_vn) ----------------
    {
        "norm_id": "VN:Construction_Law_2014_Amended_2020:Art138_146",
        "law": "Law No. 50/2014/QH13 jo. Law No. 62/2020/QH14",
        "enbez": "Điều 138-146",
        "title": "建设法工程合同履行与违约损害赔偿法定界限",
        "heading_path": "Luật Xây dựng số 50/2014/QH13 | Chương VI Hợp đồng xây dựng",
        "text_zh": "【中文释义】明确建设工程合同当事人必须依法依约履行。违约方应向守约方支付合同约定的违约金并赔偿实际发生的直接损失。使用国家财政预算或国有企业资本的建设项目，违约金最高上限不得超过发生违约之合同部分价款的12%（第146条第2款特别规定）。该强行规定优先于越南《商事法2005》第301条规定的8%违约金上限。",
        "text_en": "Construction contracts must comply with civil and commercial laws. For state-funded or state-capital construction projects, penalties for contract breach shall not exceed 12% of the value of the breached contract portion (Art 146.2), superseding the 8% general limit under Commercial Law 2005.",
        "text_original": "Đối với công trình sử dụng vốn nhà nước, mức phạt hợp đồng không vượt quá 12% giá trị phần hợp đồng bị vi phạm. Ngoài mức phạt theo thỏa thuận, bên vi phạm còn phải bồi thường thiệt hại cho bên kia theo quy định của Luật này.",
        "language_mode": "trilingual",
        "norm_category": "mandatory_statute",
        "elements_json": '{"subject": "越南境内建设工程发包人与承包商", "trigger": "工程延误、质量违约或提前终止索赔", "requirements": ["审查项目资金来源是否涉及国有资产", "核算违约金是否超出违约部分12%法定上限", "举证违约与实际直接损失之间的因果关系"], "legal_effect": "合同约定的违约金超出12%部分在越南法院或仲裁庭自始不受支持"}'
    },
    {
        "norm_id": "VN:Decree_37_2015_Amended_50_2021:Payment_Guarantee",
        "law": "Decree No. 37/2015/ND-CP jo. Decree No. 50/2021/ND-CP",
        "enbez": "Điều 16-18",
        "title": "建设合同管理法令付款担保与预付款保函强制要求",
        "heading_path": "Nghị định số 37/2015/NĐ-CP hướng dẫn về Hợp đồng xây dựng | Chương II",
        "text_zh": "【中文释义】在越南签署大型施工总承包合同前，发包人必须向承包商提供等额于合同总价10%~15%的付款担保（Bảo đảm thanh toán），确保具备履约资金能力；发包人在支付工程预付款前，承包商必须提供合法信用机构签发的预付款退还保函。发包人未提供法定付款担保即要求开工的，承包商享有依法延期开工且免除延误工期违约责任的正当抗辩权。",
        "text_en": "The employer must provide payment security (10%~15% of contract value) to the contractor before construction commences. The contractor must provide advance payment security before receiving advance funds. Failure by employer to provide payment security justifies contractor delay.",
        "text_original": "Bên giao thầu phải bảo đảm thanh toán theo thỏa thuận trong hợp đồng xây dựng. Mức bảo đảm thanh toán từ 10% đến 15% giá trị hợp đồng. Bên nhận thầu phải nộp bảo đảm hoàn trả tiền tạm ứng trước khi nhận tạm ứng hợp đồng.",
        "language_mode": "trilingual",
        "norm_category": "mandatory_statute",
        "elements_json": '{"subject": "建设工程业主与总分包商", "trigger": "开工准备阶段与预付款拨付环节", "requirements": ["发包人开立10%-15%无条件付款保证", "承包商开立等额预付款退还保函", "依合同节点按比例抵扣预付款"], "legal_effect": "发包人拒绝提供付款担保构成根本违约，承包商有权中止进场施工并不计入工期违约"}'
    },
    {
        "norm_id": "VN:Enterprise_Law_2020:Art12_Legal_Representative",
        "law": "Law No. 59/2020/QH14",
        "enbez": "Điều 12",
        "title": "企业法法定代表人制度与共同代表权穿透审查",
        "heading_path": "Luật Doanh nghiệp số 59/2020/QH14 | Chương I Quy định chung",
        "text_zh": "【中文释义】越南有限责任公司和股份公司可以有一名或多名法定代表人（Người đại diện theo pháp luật）。公司章程必须具体明确各法定代表人的管理权限划分与代表权范围。若章程规定由两名或多名法定代表人共同签字方能生效，或者合同金额超出特定法定代表人单独审批权限，外部签约相对人必须穿透审查营业登记证（ERC）及章程规定，否则越权签署的合同对公司不产生约束力。",
        "text_en": "An LLC or JSC may have one or more legal representatives. The charter shall specify the rights and obligations of each representative. If multiple representatives must act jointly, acts by a single representative exceeding authority do not bind the enterprise against non-innocent parties.",
        "text_original": "Công ty trách nhiệm hữu hạn và công ty cổ phần có thể có một hoặc nhiều người đại diện theo pháp luật. Điều lệ công ty quy định cụ thể số lượng, chức danh quản lý và quyền, nghĩa vụ của người đại diện theo pháp luật của doanh nghiệp.",
        "language_mode": "trilingual",
        "norm_category": "mandatory_statute",
        "elements_json": '{"subject": "越南当地签约合作方", "trigger": "签署合资合同、总包协议或资产担保", "requirements": ["调取企业登记机关核发之最新ERC证书", "审查章程载明之法定代表人签字权限制与共同代表规定", "取得必要的内部决议配合"], "legal_effect": "单一法定代表人越权代表且相对人未尽合理注意义务的，协议对越南公司不生效力"}'
    },
    {
        "norm_id": "VN:Enterprise_Law_2020:Art67_167_Related_Guarantee",
        "law": "Law No. 59/2020/QH14",
        "enbez": "Điều 67 & 167",
        "title": "企业法关联交易与对外担保特别表决要件",
        "heading_path": "Luật Doanh nghiệp số 59/2020/QH14 | Chương III & Chương V",
        "text_zh": "【中文释义】公司与公司股东、法定代表人、董事及其关联方之间签署的借款、担保、资产转让等关联交易，必须经成员理事会（LLC）或董事会/股东大会（JSC）依据章程规定表决通过，关联利益当事人不得行使表决权。未经前述法定特别程序批准而签署的对外担保合同属于自始无效合同，且直接签署人须连带赔偿由此给公司造成的一切直接损失。",
        "text_en": "Contracts and transactions between a company and its shareholders, directors, or related persons must be approved by the Members' Council (LLC) or Board of Directors / GMS (JSC) without interested party voting. Contracts signed in breach are void.",
        "text_original": "Hợp đồng, giao dịch giữa công ty với cổ đông, người quản lý hoặc người có liên quan phải được Đại hội đồng cổ đông hoặc Hội đồng quản trị chấp thuận. Hợp đồng, giao dịch bị vô hiệu theo quyết định của Tòa án và bị xử lý theo quy định nếu ký kết không đúng quy định.",
        "language_mode": "trilingual",
        "norm_category": "mandatory_statute",
        "elements_json": '{"subject": "在越投资平台与中资合资企业", "trigger": "为母公司、关联子公司或控股股东提供借款保证与反担保", "requirements": ["关联当事人依法回避表决", "通过成员理事会或股东大会特别多数决议", "出具备案或决议文本附件"], "legal_effect": "违背程序批准之担保被越南法院判定无效，放贷行或受益人无法向越南公司追偿担保物"}'
    },
    {
        "norm_id": "VN:Commercial_Arbitration_2010:Art2_43_Language",
        "law": "Law No. 54/2010/QH12",
        "enbez": "Điều 2 & 43",
        "title": "商事仲裁法管辖权边界与程序语言强制性红线",
        "heading_path": "Luật Trọng tài thương mại số 54/2010/QH12",
        "text_zh": "【中文释义】仲裁仅受理商事主体之间的商事争议，或法律规定允许仲裁的其他争议。在程序语言方面，涉及外资因素或在外国仲裁机构审理的案件，当事人有权协议选择仲裁语言；但在没有任何外资因素的纯越南国内主体之间签署的合同（例如中资在越全资子公司与本地土建分包商签署的分包合同），仲裁程序必须强制使用越南语（Điều 43.1），约定使用中文或英文的仲裁条款因违法而可能导致裁决被撤销。",
        "text_en": "Commercial arbitration resolves commercial disputes. Where disputes involve no foreign elements, the language used in arbitral proceedings must be Vietnamese (Art 43.1). Agreements to use foreign languages between purely domestic entities risk vacatur of the arbitral award.",
        "text_original": "Đối với vụ tranh chấp không có yếu tố nước ngoài, ngôn ngữ sử dụng trong tố tụng trọng tài là tiếng Việt. Đối với vụ tranh chấp có yếu tố nước ngoài, ngôn ngữ sử dụng do các bên thỏa thuận.",
        "language_mode": "trilingual",
        "norm_category": "mandatory_statute",
        "elements_json": '{"subject": "中资在越南设立之全资子公司（纯越内资法人身份）", "trigger": "与越南本地承包商、供货商起草争议解决条款", "requirements": ["核查签约主体是否存在涉外因素（Yếu tố nước ngoài）", "无外资因素合同必须将仲裁语言明确指定为越南语"], "legal_effect": "纯内资主体强行约定外语仲裁将触犯强行法，导致仲裁裁决在越南法院被全额撤销"}'
    },

    # ---------------- 马来西亚 (asean_my) ----------------
    {
        "norm_id": "MY:Contracts_Act_1950:Sec38_39_Performance",
        "law": "Contracts Act 1950",
        "enbez": "Section 38 & 39",
        "title": "合同法合同履行与拒绝受领之毁约性违约",
        "heading_path": "Contracts Act 1950 (Act 136) | Part V of the Performance of Contracts",
        "text_zh": "【中文释义】合同各方当事人必须履行其各自的合同承诺，除非依照法律规定该履行被免除。当一方当事人拒绝履行，或由于自身过错使其不可能完全履行其合同实质义务时，相对方当事人可以终止该合同（Repudiatory Breach），除非该相对方已通过言词或行为明示同意合同继续存续。",
        "text_en": "The parties to a contract must either perform, or offer to perform, their respective promises. When a party has refused to perform, or disabled himself from performing, his promise in its entirety, the promisee may put an end to the contract unless he has signified his acquiescence.",
        "text_original": "The parties to a contract must either perform, or offer to perform, their respective promises, unless the performance is dispensed with or excused under this Act, or of any other law.",
        "language_mode": "bilingual",
        "norm_category": "mandatory_statute",
        "elements_json": '{"subject": "马来西亚工程业主与总承包商", "trigger": "严重工期延误、停工或拒绝支付到期款项", "requirements": ["存在根本违约（去向合同根基之违约）", "无默示同意继续履约之行为（Acquiescence）", "发出明确行使解除权的通知函"], "legal_effect": "合同合法终止，守约方有权立即撤场并主张预期利润损失赔偿"}'
    },
    {
        "norm_id": "MY:Contracts_Act_1950:Sec71_Quantum_Meruit",
        "law": "Contracts Act 1950",
        "enbez": "Section 71",
        "title": "合同法非无偿行为不当得利之法定补偿基础",
        "heading_path": "Contracts Act 1950 (Act 136) | Part VI Of Certain Relations Resembling Those Created by Contract",
        "text_zh": "【中文释义】当一人合法地为另一人实施某项劳务或交付某项物品，其本意并非出于无偿赠与，且该另一人已经从该劳务或交付中实际受领并享有了利益，则享有该利益的人负有向实施劳务者给予补偿或返还物品的法定义务。这是马来西亚工程实务中，承包商在缺乏业主正式书面变更指令（Variation Order）但实际施工并被业主验收投用时的头号索赔救命稻草（Quantum Meruit）。",
        "text_en": "Where a person lawfully does anything for another person, or delivers anything to him, not intending to do so gratuitously, and such other person enjoys the benefit thereof, the latter is bound to make compensation to the former in respect of, or to restore, the thing so done or delivered.",
        "text_original": "Where a person lawfully does anything for another person, or delivers anything to him, not intending to do so gratuitously, and such other person enjoys the benefit thereof, the latter is bound to make compensation to the former in respect of, or to restore, the thing so done or delivered.",
        "language_mode": "bilingual",
        "norm_category": "mandatory_statute",
        "elements_json": '{"subject": "施工承包商与受领业主", "trigger": "无书面变更令施工、合同无效或终止后追加工程结算", "requirements": ["劳务实施具有合法性", "证明实施时无无偿赠与意图", "相对方实际受领并占有享有了工程成果"], "legal_effect": "即使合同变更条款要求书面形式，法院仍可依据衡平准则判令业主支付合理对价补偿"}'
    },
    {
        "norm_id": "MY:Contracts_Act_1950:Sec86_Discharge_Surety",
        "law": "Contracts Act 1950",
        "enbez": "Section 86",
        "title": "合同法主合同未经同意实质变更致保证人免责",
        "heading_path": "Contracts Act 1950 (Act 136) | Part VIII Of Indemnity and Guarantee",
        "text_zh": "【中文释义】债权人与主债务人之间在未经保证人（Surety/Guarantor）书面明确同意的情况下，对主合同条款所作出的任何实质性变更（Variance），将导致保证人对变更之后发生的一切交易责任自动全部免除。在涉外工程中，若业主与总承包商私下协商延长工期、调整付款方式或变更工程范围而未通知母公司担保人或未取得其书面批单，母公司担保责任依法解除。",
        "text_en": "Any variance, made without the surety's consent, in the terms of the contract between the principal debtor and the creditor, discharges the surety as to transactions subsequent to the variance.",
        "text_original": "Any variance, made without the surety's consent, in the terms of the contract between the principal debtor and the creditor, discharges the surety as to transactions subsequent to the variance.",
        "language_mode": "bilingual",
        "norm_category": "mandatory_statute",
        "elements_json": '{"subject": "母公司担保人（Surety）与出海债权人", "trigger": "EPC主合同条款发生重大变更、工期延期或付款重组", "requirements": ["查核主合同变更是否取得保证人事先或事后书面确认", "变更内容是否具有实质性影响"], "legal_effect": "债权人私下变更主合同导致母公司保函效力自变更生效之日起依法自动解除"}'
    },

    # ---------------- 新加坡 (asean_sg) ----------------
    {
        "norm_id": "SG:Evidence_Act_Cap97:Sec93_98_Extrinsic_Evidence",
        "law": "Evidence Act (Cap. 97)",
        "enbez": "Section 93-98",
        "title": "证据法书面证据法则与语境主义合同解释界限",
        "heading_path": "Evidence Act (Cap. 97) | Part II On Proof | Chapter VI Of the Exclusion of Oral Evidence",
        "text_zh": "【中文释义】确立严格的书面证据法则（Parol Evidence Rule）：当合同条款已由书面形式记载时，当事人不得提出任何口头协议或庭外证据（Extrinsic Evidence）以抗辩、推翻、增加或扣减该书面条款。结合最高法院在 Zurich Insurance [2008] 案中确立的语境主义解释规则（Contextual Approach），只有在合同文本客观存在歧义且庭外证据属于客观商业背景且已被双方所共同知悉的前提下，方可作为解释参考。",
        "text_en": "When terms of a contract have been reduced to form of a document, no evidence of any oral agreement or statement shall be admitted as between parties for contradicting, varying, adding to, or subtracting from terms, subject to contextual ambiguity exceptions.",
        "text_original": "When the terms of a contract have been reduced to the form of a document, no evidence shall be given in proof of the terms of such contract except the document itself.",
        "language_mode": "bilingual",
        "norm_category": "mandatory_statute",
        "elements_json": '{"subject": "适用新加坡法商事工程纠纷当事人", "trigger": "援引缔约谈判记录、往来邮件抗辩书面合同明文约定", "requirements": ["合同存在客观歧义（Latent/Patent Ambiguity）", "庭外证据具备真实性与客观性", "该背景事实为缔约时双方共同知悉"], "legal_effect": "纯粹单方主观意图之往来函件依法被法庭排除采信，严格以合同客观文义为准"}'
    },
    {
        "norm_id": "SG:Limitation_Act_1959:Sec6_24A_Latent_Defects",
        "law": "Limitation Act 1959 (Cap. 163)",
        "enbez": "Section 6 & 24A",
        "title": "时效法普通合同6年与潜伏性缺陷15年绝对封顶",
        "heading_path": "Limitation Act 1959 | Part I Ordinary Periods of Limitation",
        "text_zh": "【中文释义】基于违约或侵权责任提起诉讼的普通时效期间为自诉权发生之日起6年（Section 6）。对于涉及建筑工程潜伏性结构缺陷（Latent Damage/Defects）的损害赔偿请求，Section 24A 规定诉讼时效为自原告具备知晓必要损害事实之日起3年；但在任何情况下，自引起损害的违约行为发生之日起逾越15年绝对封顶期间（Long-stop Period）后，原告彻底丧失起诉权。",
        "text_en": "Actions founded on contract or tort shall not be brought after the expiration of 6 years from the date on which the cause of action accrued. For latent damage, the limitation is 3 years from earliest date plaintiff had knowledge, subject to a 15-year overriding long-stop.",
        "text_original": "Actions founded on contract or on tort shall not be brought after the expiration of 6 years from the date on which the cause of action accrued. An action for damages for latent damage shall not be brought after the expiration of 15 years from the date on which the breach occurred.",
        "language_mode": "bilingual",
        "norm_category": "mandatory_statute",
        "elements_json": '{"subject": "工程业主与设计施工承包商", "trigger": "工程竣工投运多年后发现结构隐蔽裂缝或渗漏索赔", "requirements": ["知晓潜在缺陷起3年内提起诉讼", "且自施工违约行为发生起未逾越15年绝对终极封顶线"], "legal_effect": "逾越15年封顶期的工程质量索赔属于实体权利灭失，法庭予以直接驳回"}'
    },

    # ---------------- 泰国 (asean_th) ----------------
    {
        "norm_id": "TH:CCC:Sec193_34_Two_Year_Contractor_Limitation",
        "law": "Civil and Commercial Code",
        "enbez": "Section 193/34(1)",
        "title": "民商法典承揽工程款与工料费2年超短消灭时效",
        "heading_path": "Thailand Civil and Commercial Code | Book I General Principles | Title VI Prescription | Section 193/34",
        "text_zh": "【中文释义】泰国民商法典特别明确规定：商人和工业从业人员针对其提供商品、工程承揽工作或代垫费用所享有的报酬求偿权，消灭时效仅为极短的2年（Section 193/34(1)）！这与一般普通合同债权的10年时效形成致命反差。出海承包商在泰国完工验收或里程碑达成后，若仅通过非正式邮件催款而未在2年内正式起诉或取得债务人书面延期还款确认，将彻底丧失在泰国法院强制追偿工程款的胜诉权！",
        "text_en": "The period of prescription is two years for claims by merchants, industrialists, manufacturers, or artisans for the price of goods delivered or work done, including disbursements. Failure by a contractor to file a formal action within two years extinguishes the right of action.",
        "text_original": "สิทธิเรียกร้องดังต่อไปนี้ให้มีกำหนดอายุความสองปี (๑) ผู้ประกอบการค้าหรืออุตสาหกรรม ผู้ประกอบหัตถกรรม ผู้ประกอบศิลปวิทยา หรือช่างฝีมือ เรียกเอาค่าของที่ได้ส่งมอบ ค่าการงานที่ได้ทำ หรือค่าดูแลกิจการของผู้อื่น รวมทั้งเงินที่ได้ออกทดรองไป",
        "language_mode": "trilingual",
        "norm_category": "mandatory_statute",
        "elements_json": '{"subject": "在泰工程总承包商与设备供应商", "trigger": "向泰国业主主张未付工程进度款、停工补偿或窝工费", "requirements": ["自工程款清偿期届满之日起算2年期限", "期间内必须提起法院诉讼或申请合规仲裁以中断时效", "普通非司法催告信函不发生时效中断法律效果"], "legal_effect": "逾越2年未起诉将被泰国法院以消灭时效完成为由直接裁定驳回全部起诉"}'
    },
    {
        "norm_id": "TH:CCC:Sec193_14_Interruption_of_Prescription",
        "law": "Civil and Commercial Code",
        "enbez": "Section 193/14",
        "title": "民商法典诉讼时效中断法定事由与形式要件",
        "heading_path": "Thailand Civil and Commercial Code | Book I General Principles | Title VI Prescription | Section 193/14",
        "text_zh": "【中文释义】泰国民商法典第193/14条规定诉讼时效中断的法定情形：消灭时效仅在下列情形下发生法律中断：(1) 债务人向债权人作出书面承认债务、提供担保或部分清偿；(2) 债权人向有管辖权法院提起正式民商事诉讼；(3) 申请破产清算程序或提交合规的仲裁申请。与菲律宾法不同，单纯发送普通律师催款函在泰国法下不发生时效中断法律效果。",
        "text_en": "Under Section 193/14 of CCC, prescription is interrupted when the debtor acknowledges liability in writing, offers security, makes partial payment, or when the creditor files an action in court or submits the dispute to arbitration.",
        "text_original": "อายุความย่อมสะดุดหยุดลงในกรณีดังต่อไปนี้ (๑) ลูกหนี้รับสภาพหนี้ต่อเจ้าหนี้ตามสิทธิเรียกร้องโดยทำเป็นหนังสือ (๒) เจ้าหนี้ได้ฟ้องคดีเพื่อตั้งหลักฐานสิทธิเรียกร้อง",
        "language_mode": "trilingual",
        "norm_category": "mandatory_statute",
        "elements_json": '{"subject": "在泰工程债权人与债务人", "trigger": "防范2年工程款超短时效届满失权", "requirements": ["取得债务人签字盖章之书面债务确认函", "或在时效届满前向法院立案起诉或申请仲裁"], "legal_effect": "时效合法中断，自中断事由终结之日起重新起算全新时效期间"}'
    },
    {
        "norm_id": "TH:CCC:Sec798_Agency_Written_Requirement",
        "law": "Civil and Commercial Code",
        "enbez": "Section 798",
        "title": "民商法典法定书面交易之委托代理书面形式",
        "heading_path": "Thailand Civil and Commercial Code | Book III Specific Contracts | Title XV Agency",
        "text_zh": "【中文释义】若法律规定某项民事法律行为必须采用书面形式方能成立或作为证据（例如土地买卖、长期租赁、建设工程合同、保证合同），则委托代理人实施该项行为的委托授权书（Power of Attorney / POA）也必须以书面形式作成。若委托书欠缺书面形式，代理人所签署的合同对本人不产生任何法律拘束力。",
        "text_en": "If a contract is required by law to be in writing, the appointment of an agent to make such contract must also be in writing. Contracts made by an agent lacking a written POA are unenforceable against the principal.",
        "text_original": "ถ้ากิจการที่มอบหมายให้ทำนั้น กฎหมายบัญญัติว่าต้องทำเป็นหนังสือ การตั้งตัวแทนเพื่อกิจการนั้นก็ต้องทำเป็นหนังสือด้วย",
        "language_mode": "trilingual",
        "norm_category": "mandatory_statute",
        "elements_json": '{"subject": "签约代理人与泰国签约相对人", "trigger": "由项目经理或当地代表签署重大总包合同或保证书", "requirements": ["查验正式书面POA原件", "POA内容必须明确涵盖该特定法律行为", "完成必要公证与领事双认证"], "legal_effect": "欠缺书面授权签署之工程合同被视为无权代理，对总公司自始无约束力"}'
    },

    # ---------------- 菲律宾 (asean_ph) ----------------
    {
        "norm_id": "PH:Revised_Corporation_Code:Sec150_Doing_Business_Without_License",
        "law": "Revised Corporation Code (RA 11232)",
        "enbez": "Section 150",
        "title": "修订公司法典无证在菲经营绝对丧失起诉权",
        "heading_path": "Republic Act No. 11232 | Title XV Foreign Corporations | Section 150",
        "text_zh": "【中文释义】未取得菲律宾证券交易委员会（SEC）核发之经营许可证（License to Do Business）而在菲律宾境内从事经营活动的外国公司，绝对不得在菲律宾任何法院或行政法庭提起任何诉讼或法律程序！但该外国公司可在菲律宾法庭作为被告被相对人起诉，且其签署的合同仍对该外国公司具有约束力。此为外国承包商在菲最致命的失权红线（除非属于偶发孤立交易 Isolated Transaction）。",
        "text_en": "No foreign corporation transacting business in the Philippines without a license, or its successors, shall be permitted to maintain or intervene in any action, suit or proceeding in any court or administrative agency of the Philippines; but such corporation may be sued on any valid cause of action.",
        "text_original": "No foreign corporation transacting business in the Philippines without a license, or its successors or assigns, shall be permitted to maintain or intervene in any action, suit or proceeding in any court or administrative agency of the Philippines.",
        "language_mode": "bilingual",
        "norm_category": "mandatory_statute",
        "elements_json": '{"subject": "进入菲律宾开展工程与贸易的中资企业", "trigger": "在菲律宾法院向违约业主提起诉讼主张工程款", "requirements": ["取得SEC颁发的分支机构合法经营牌照", "或举证证明涉案行为属于纯偶发孤立交易（Isolated Transaction）"], "legal_effect": "未持牌且长期经营者在菲起诉将被法院直接依Section 150全案裁定驳回（Dismiss）"}'
    },
    {
        "norm_id": "PH:Civil_Code_RA_386:Art1155_Extrajudicial_Demand_Interruption",
        "law": "Civil Code of the Philippines (RA 386)",
        "enbez": "Article 1155",
        "title": "民法典书面庭外催告函直接中断诉讼时效规则",
        "heading_path": "Republic Act No. 386 | Book III Title V Prescription | Chapter 3",
        "text_zh": "【中文释义】与泰国和越南法截然相反，菲律宾民法典第1155条明确确立：诉讼时效不仅因向法院提起正式诉讼而中断，亦可因债权人向债务人送达正式的书面庭外催告信函（Extrajudicial Demand）或因债务人书面承认债务而直接发生法定中断！一旦送达合规书面催告函，诉讼时效期间即刻清零并重新起算（Re-commence）。",
        "text_en": "The prescription of actions is interrupted when they are filed before the court, when there is a written extrajudicial demand by the creditors, and when there is any written acknowledgment of the debt by the debtor.",
        "text_original": "The prescription of actions is interrupted when they are filed before the court, when there is a written extrajudicial demand by the creditors, and when there is any written acknowledgment of the debt by the debtor.",
        "language_mode": "bilingual",
        "norm_category": "mandatory_statute",
        "elements_json": '{"subject": "菲律宾工程债权人", "trigger": "面临10年书面合同诉讼时效届满危机", "requirements": ["起草正式催款指令函（Extrajudicial Demand Letter）", "以可追踪邮寄或公证送达至债务人法定地址", "保留送达回执证明"], "legal_effect": "送达之日诉讼时效依法全额中断，获得完整的崭新10年时效期间"}'
    }
]

SUPPLEMENT_SIX_NORMS_L2 = [
    # ---------------- 国际条约与双边司法协助 ----------------
    {
        "norm_id": "TREATY:Hague_Apostille_1961:Exemption_Legalisation",
        "law": "Hague Convention of 5 October 1961",
        "enbez": "Article 1-3",
        "title": "海牙取消外国公文书认证公约领事双认证免除规则",
        "heading_path": "Convention Abolishing the Requirement of Legalisation for Foreign Public Documents 1961",
        "text_zh": "【中文释义】公约于2023年11月7日对中国正式生效。中国与同为缔约国的印尼（2022生效）、新加坡（2021生效）、菲律宾（2019生效）之间流转的涉外公文书（营业执照、公司章程、授权委托书POA、公证书），免除传统使领馆领事双认证，仅需由文书出具国主管机关签发附加证明书（Apostille）即可直接在对方国法庭与行政机关具有公文书效力。注意：越南、大马、泰国尚未加入，仍须走领事认证。",
        "text_en": "Each Contracting State shall exempt from legalisation documents to which the present Convention applies. The only formality that may be required in order to certify authenticity of signature is the addition of the certificate described in Article 4 (Apostille).",
        "text_original": "Each Contracting State shall exempt from legalisation documents to which the present Convention applies. The only formality that may be required is the addition of the certificate issued by the competent authority (Apostille).",
        "language_mode": "bilingual",
        "norm_category": "international_treaty",
        "elements_json": '{"subject": "中印、中新、中菲跨境诉讼与投资主体", "trigger": "向域外法院提交境内公文书证据与公司登记材料", "requirements": ["文书出具国属于海牙Apostille公约缔约国", "由外交部或指定司法部机关加贴Apostille印鉴"], "legal_effect": "免除繁琐领事双认证，直接具备法庭公文书可采性证据效力"}'
    },
    {
        "norm_id": "TREATY:Hague_Service_1965:Transnational_Judicial_Documents",
        "law": "Hague Convention of 15 November 1965",
        "enbez": "Article 1-15",
        "title": "海牙送达公约民商事司法文书跨境送达中央机关渠道",
        "heading_path": "Convention on the Service Abroad of Judicial and Extrajudicial Documents in Civil or Commercial Matters",
        "text_zh": "【中文释义】在涉及跨国民商事诉讼中，中国、新加坡、菲律宾、越南同为海牙送达公约缔约国。法院向住所地位于公约缔约国的当事人送达起诉状副本、传票等司法文书，必须通过司法部中央机关（Central Authority）途径进行送达，中国明确保留反对直接邮寄送达（Article 10(a)）。未通过公约法定渠道送达而由缺席判决所作出的裁判，在国际上属于严重程序瑕疵，拒不予以承认执行。",
        "text_en": "The present Convention shall apply in all cases, in civil or commercial matters, where there is occasion to transmit a judicial or extrajudicial document for service abroad through designated Central Authorities.",
        "text_original": "The present Convention shall apply in all cases, in civil or commercial matters, where there is occasion to transmit a judicial or extrajudicial document for service abroad through Central Authorities.",
        "language_mode": "bilingual",
        "norm_category": "international_treaty",
        "elements_json": '{"subject": "涉外诉讼原告与审理法院", "trigger": "向位于越南、新加坡、菲律宾等国之被告送达诉状", "requirements": ["通过司法部中央机关国际协助通道传送", "翻译为受送达国官方语言正本", "取得送达证书"], "legal_effect": "保障被告正当防卫答辩权，确保日后金钱判决跨境执行效力"}'
    },
    {
        "norm_id": "TREATY:CN_SG_Judicial_MOG_2018:Money_Judgments_Enforcement",
        "law": "Supreme People's Court of China and Supreme Court of Singapore MOG 2018",
        "enbez": "Paragraph 1-8",
        "title": "中新最高法院关于商事金钱判决承认执行指导备忘录",
        "heading_path": "Memorandum of Guidance between the Supreme People's Court of the PRC and the Supreme Court of Singapore 2018",
        "text_zh": "【中文释义】中国最高人民法院与新加坡最高法院于2018年签署指导备忘录，明确两国法院在互惠原则（Reciprocity）下承认与执行对方终审商事金钱判决的标准。在满足具有合格管辖权、不存在欺诈、符合正当法律程序送达且不违反被请求国公共政策的前提下，中国法院生效金钱判决可直接向新加坡高等法院申请执行令状，极大地提升了中资企业在新加坡调取资产执行的便利度。",
        "text_en": "The MOG sets out the understanding of the courts on the procedure for the recognition and enforcement of each other's money judgments in civil and commercial cases, subject to jurisdiction, due process, and public policy safeguards.",
        "text_original": "The Memorandum of Guidance sets out the procedures for the recognition and enforcement of money judgments in civil and commercial matters between the Supreme People's Court of China and the Supreme Court of Singapore based on reciprocity.",
        "language_mode": "bilingual",
        "norm_category": "bilateral_treaty",
        "elements_json": '{"subject": "持有中国或新加坡法院确定终审胜诉金钱判决的债权人", "trigger": "在新加坡或中国执行被执行人海外金融资产", "requirements": ["判决属于最终且不可上诉之金钱给付", "原审法院具备合格管辖权", "程序上经过合规有效送达"], "legal_effect": "法院无需重新开庭实体审判，直接裁定许可强制执行"}'
    },

    # ---------------- 本土标准施工合同 ----------------
    {
        "norm_id": "MY:PAM_Contract_2018:Clause_23_24_EOT_Loss",
        "law": "PAM Contract 2018",
        "enbez": "Clause 23 & 24",
        "title": "大马建筑师学会标准合同工期顺延与两阶段通知除斥期",
        "heading_path": "PAM Contract 2018 (With Quantities) | Clause 23 Extension of Time & Clause 24 Loss and Expense",
        "text_zh": "【中文释义】马来西亚本土民用与工业基建使用最广的标准合同。Clause 23 确立严格的两阶段通知制度：承包商必须在顺延事由发生后28天内提交第一阶段初步书面通知；并在事由结束后28天内提交载有最终工期顺延天数及详细计算依据的第二阶段详情通知。Clause 24 规定损失与费用索赔同样适用28天通知期。若未满足前置通知除斥期，建筑师有权全额否决索赔。",
        "text_en": "Under PAM 2018 Clause 23, the contractor must give written notice within 28 days of an event delaying completion, followed by full particulars within 28 days of delay ending. Clause 24 requires similar notice for loss and expense.",
        "text_original": "If the Contractor is of the opinion that the completion of the Works is or will be delayed by any of the Relevant Events, he shall give written notice to the Architect within 28 Days of the delay occurrence.",
        "language_mode": "bilingual",
        "norm_category": "standard_contract",
        "elements_json": '{"subject": "大马工程总分包商", "trigger": "业主变更、恶劣天气或不可抗力导致进度延误", "requirements": ["第一阶段：28天内初步通知", "第二阶段：延误终止后28天内提交详尽CPM工期网络图分析与费用清单"], "legal_effect": "未如期提交通知可能导致工期索赔失权并承担严苛违约金赔偿"}'
    },
    {
        "norm_id": "SG:PSSCOC_2020:Clause_14_23_EOT_Claim",
        "law": "PSSCOC for Construction Works 2020",
        "enbez": "Clause 14, 22, 23",
        "title": "新加坡公共部门施工合同索赔60天严格除斥期",
        "heading_path": "Public Sector Standard Conditions of Contract (PSSCOC) 2020 8th Edition",
        "text_zh": "【中文释义】新加坡政府及公营机构基建项目强制使用的权威文本。Clause 14 规定工期顺延（EOT），Clause 22/23 规定损失与费用索赔。明确设立极其刚性的失权屏障：承包商如果未在导致索赔的事件发生后60天内向超级工程师（Superintending Officer / SO）发出包含初步损失预估的正式索赔通知，承包商将彻底丧失获得任何索赔赔偿的权利（Condition Precedent）！",
        "text_en": "Under PSSCOC Clause 23, the Contractor must give notice of intention to claim within 60 days of the event. Failure to comply with this notice condition serves as a condition precedent that bars the claim entirely.",
        "text_original": "The Contractor shall give notice in writing to the Superintending Officer of his intention to make a claim within 60 days after the event. Compliance with this requirement is a condition precedent to any entitlement.",
        "language_mode": "bilingual",
        "norm_category": "standard_contract",
        "elements_json": '{"subject": "承揽新加坡公共工程的总分包商", "trigger": "发生地质异常、设计变更或SO指令延误", "requirements": ["60天严格除斥期内书面送达SO", "载明索赔事实、合同条款依据与初步金额测算"], "legal_effect": "逾期送达通知在新加坡普通法下构成先决条件抗辩，索赔权利永久灭失"}'
    }
]

SUPPLEMENT_SIX_CASES = [
    # ---------------- 印度尼西亚 ----------------
    {
        "case_id": "CASE:ID_MA:Nine_AM_v_BKPL_2015",
        "court": "Mahkamah Agung Republik Indonesia",
        "senate": "Perdata Khusus",
        "decided": "2015-08-31",
        "az": "Putusan MA No. 1572 K/Pdt/2015",
        "ecli": "ID:MA:2015:1572K",
        "doctype": "Urteil",
        "leitsatz": "涉外商事借款与担保协议未依法提供印尼语官方对译本的，违反印尼《2009年第24号国旗语言法》第31条强制性规定，不符合《印尼民法典》第1320条合法对价原则，合同自始绝对无效。印尼最高法院终审判决确认，境外债权人不得依据仅以英文书就之主合同主张利息及违约损害赔偿。",
        "tenor": "最高法院驳回九点有限合伙基金（Nine AM Ltd）的再审上诉（Kasasi），全案维持雅加达西区地方法院及高等法院确定判决：原告与被告 PT Bangun Karya Pratama Lestari 之间签署之英文版借贷及连带保证协议全部无效。",
        "tatbestand": "原告系在境外设立的专业金融投资机构，被告为印尼本土采矿工程企业。2010年，双方签署总额数千万美元的境外贷款协议及设备担保书，合同全部以英文起草，未同步签署印尼文正本。后被告无力清偿本息，原告向法院提起诉讼。被告抗辩称协议违反《语言法》第31条。",
        "gruende": "最高法院合议庭认为，《2009年第24号法律》第31条明确规定，凡涉及印尼国家机构、商业实体或印尼自然人的任何协议，必须使用印尼语（Wajib menggunakan bahasa Indonesia）。该条属于公共秩序层面的强行法。任何排除印尼语的纯外语商业合同因欠缺合法原因自始不产生法律效力。本案确立了出海印尼必须双语签约的刚性合规防线。",
        "source_url": "https://putusan3.mahkamahagung.go.id/direktori/putusan/1572k-pdt-2015.html"
    },
    {
        "case_id": "CASE:ID_MA:PLN_v_IPP_Take_or_Pay_2021",
        "court": "Mahkamah Agung Republik Indonesia",
        "senate": "Perdata",
        "decided": "2021-04-14",
        "az": "Putusan MA No. 1290 K/Pdt/2021",
        "ecli": "ID:MA:2021:1290K",
        "doctype": "Urteil",
        "leitsatz": "印尼国家电力公司（PLN）在独立电厂（IPP）购电协议（PPA）中签署的照付不议（Take-or-Pay）条款具有完全的商事实体效力。PLN不得以电网消纳不足、疫情导致负荷下降或维护国家财政公共利益为由，单方解除购电协议或拒绝支付最低可用容量电费。",
        "tenor": "最高法院判决支持外资 IPP 投资方诉讼请求，判令被告 PT PLN (Persero) 依据 PPA 照付不议条款全额支付拖欠的容量电费及逾期利息共计 4,820 亿印尼盾，并驳回 PLN 提出的不可抗力及情势变更抗辩。",
        "tatbestand": "中资电建联合体在苏门答腊投资建设燃煤坑口电站，与 PLN 签署为期25年的 BOOT 购电协议。电站商业运营后，PLN 因当地电网供大于求多次发出限负荷调度令，并拒绝就未实际调度的保底发电量支付容量费，主张公共利益优先及不可抗力。",
        "gruende": "最高法院裁决认定，照付不议条款系国际能源基础设施项目融资与资本回收的商业基石，PLN 作为商业化运营的国有独资公司，在签约时充分知悉电网供需波动风险，负荷下滑不构成民法典第1244条不可抗力。PLN 必须恪守合同约定履行支付义务，公共利益抗辩不得滥用于规避正当商事契约。",
        "source_url": "https://putusan3.mahkamahagung.go.id/direktori/putusan/1290k-pdt-2021.html"
    },

    # ---------------- 越南 ----------------
    {
        "case_id": "CASE:VN_SPC:An_Le_12_2017_AL",
        "court": "Tòa án nhân dân tối cao",
        "senate": "Hội đồng Thẩm phán",
        "decided": "2017-12-14",
        "az": "Án lệ số 12/2017/AL",
        "ecli": "VN:TANDTC:2017:AL12",
        "doctype": "Urteil",
        "leitsatz": "当事人在民商事诉讼过程中达成和解或原告撤回起诉后重新提起诉讼的，诉讼时效期间自撤诉裁定生效次日起重新起算。前次起诉在法院审理期间所耗费的全部时间不计入原诉讼时效，有力保障涉外商事主体在谈判和解破裂后的重新追索权利。",
        "tenor": "最高人民法院审判委员会决议将本案裁定列为全国指导性判例第12号：撤销省级上诉法院以诉讼时效已过为由驳回原告起诉的判决，指令一审法院依据重新起算的时效准则对工程款清偿纠纷进行实体审理。",
        "tatbestand": "原告系涉外承包商，与发包人在河内建设高层商业中心。因发包人拖欠工程款，承包商于2012年首次起诉，诉讼中双方达成庭外分期还款框架协议，承包商申请撤诉。后发包人再度违约拒付，承包商于2015年重新提起诉讼，发包人抗辩称已逾越2年诉讼时效。",
        "gruende": "最高人民法院合议庭认为，民事主体向有管辖权法院起诉的行为已构成行使权利的明示意思表示，前次诉讼已导致原诉讼时效依法中断。撤回起诉并非放弃实体权利，时效应当自撤诉裁定确定之日起重新计算，下级法院将前次起诉前的时间与撤诉后的时间合并累计计算属于适用法律错误。",
        "source_url": "https://anle.toaan.gov.vn/an-le/an-le-so-12-2017-al"
    },
    {
        "case_id": "CASE:VN_SPC:An_Le_55_2022_AL",
        "court": "Tòa án nhân dân tối cao",
        "senate": "Hội đồng Thẩm phán",
        "decided": "2022-09-07",
        "az": "Án lệ số 55/2022/AL",
        "ecli": "VN:TANDTC:2022:AL55",
        "doctype": "Urteil",
        "leitsatz": "不动产及基础设施用地使用权转让合同虽未按规定办理公证、认证或行政变更登记，但一方当事人已经实际履行了合同主要义务达三分之二（2/3）以上且对方予以受领的，依据《越南民法典2015》第129条第2款，法院应当裁定确认该合同具备完全法律效力，禁止违约方以形式瑕疵为由主张合同无效。",
        "tenor": "最高人民法院审判委员会决议发布第55号判例：驳回土地转让方要求确认工业用地联营转让协议无效的诉讼请求，依法裁定协议有效并指令不动产登记机构为受让方办理土地使用权证（LURC）过户登记手续。",
        "tatbestand": "投资方与越南当地工业园区企业签署合资建设厂房与土地使用权转让协议，受让方已依约支付80%的土地出让价款并实际进场建设厂房。后因地价大幅上涨，转让方以土地转让未经省人委会公证及未办登记为由向法院起诉请求确认合同无效、收回土地。",
        "gruende": "最高人民法院认为，民法典第129条确立了鼓励交易与诚信履行原则。当受让人已支付超过2/3对价且出让人已交地时，形式欠缺瑕疵依法被实体履行事实所治愈。出让人借未办理行政登记恶意违约企图收回土地的行为违反民商法善意原则，法院不予支持。",
        "source_url": "https://anle.toaan.gov.vn/an-le/an-le-so-55-2022-al"
    },

    # ---------------- 马来西亚 ----------------
    {
        "case_id": "CASE:MY_FC:Obata_Ambak_v_Prema_Bonanza_2024",
        "court": "Federal Court of Malaysia",
        "senate": "Appellate Jurisdiction",
        "decided": "2024-02-28",
        "az": "[2024] 2 MLJ 451 / Civil Appeal 02(f)-28-04/2023(W)",
        "ecli": "MY:FC:2024:28",
        "doctype": "Urteil",
        "leitsatz": "马来西亚联邦法院全席最新里程碑宪制裁决：成文法项下违约赔偿金（LAD）索赔的6年诉讼时效起算点，严格自合同约定的预计竣工日期（Contractual Completion Date）届满次日起算，而非自实际交付占有或建筑师签发最终完工证书之日起算！承包商与业主必须在工期届满6年内提起法定诉讼，逾期即遭时效失权抗辩。",
        "tenor": "联邦法院一致裁定驳回买方上诉，维持上诉法院判决：确认买方针对开发商工程逾期交付违约金提起的法定索赔诉讼已逾越《1953年时效法》第6条规定的6年期间，全案依法予以撤销驳回。",
        "tatbestand": "买方与开发商签署标准工程施工与买卖合同，约定工期36个月，预计于2014年12月竣工交付。由于施工延误，项目直至2017年10月才实际交付并获签合格证书。买方于2021年提起诉讼索赔逾期违约金，主张时效应自2017年实际交付日起算。",
        "gruende": "联邦法院首席大法官在判词中明确阐述：违约行为发生的时间即为诉因产生之日（Cause of Action Accrued）。当合同约定的竣工日期届满而工程未完工时，违约即告发生，时效钟声立即敲响。允许当事人将时效拖延至多年后实际交付不仅违背《1953年时效法》终结争议立法宗旨，也损害了建筑业商业确定性。",
        "source_url": "https://www.kehakiman.gov.my/judgments"
    },

    # ---------------- 新加坡 ----------------
    {
        "case_id": "CASE:SG_CA:Zurich_Insurance_v_B_Gold_2008",
        "court": "Singapore Court of Appeal",
        "senate": "Civil Appeals",
        "decided": "2008-05-23",
        "az": "[2008] SGCA 27 / [2008] 3 SLR(R) 1029",
        "ecli": "SG:SGCA:2008:27",
        "doctype": "Urteil",
        "leitsatz": "新加坡终审法院确立现代合同语境主义解释规则第一案（Contextual Approach）：法庭在解释书面商业合同时，应将合同文本置于客观缔约商业语境中考量，但严格受制于《证据法》第93至98条书面证据法则限制。只有在合同条款本身客观存在歧义、且庭外证据属于双方客观知悉的商业背景时方可采纳，严禁以语境为名重写合同明文约定。",
        "tenor": "终审法院驳回保险公司上诉，维持原判：依据工程保单整体商业目的与所涉装修工程特定背景语境，涉案第三者责任免责条款不适用于承包商在合法作业区内的偶发财产损害，保险人必须履行理赔责任。",
        "tatbestand": "B-Gold 装修工程公司作为总承包商承揽商业大楼室内改扩建工程，向苏黎世保险购买建筑工程一切险（CAR）。施工期间因水管爆裂导致下层商户受损，保险人援引免责专款拒绝赔付，主张保单文义绝对排除水损责任。",
        "gruende": "终审法院大法官重申：新加坡合同法采纳以客观文本为核心的语境主义。法庭探寻的是一个具备理性商业智慧的第三方在缔约时获悉双方共同背景信息下所理解的合同含义，而非当事人签约后的主观辩解。书面证据法则（Parol Evidence Rule）在新加坡具有法定效力，庭外证据绝不可用于直接对抗明确无歧义的文字表达。",
        "source_url": "https://www.elitigation.sg/gd/s/2008_SGCA_27"
    },
    {
        "case_id": "CASE:SG_CA:Sembcorp_Marine_v_PPL_Holdings_2013",
        "court": "Singapore Court of Appeal",
        "senate": "Civil Appeals",
        "decided": "2013-05-30",
        "az": "[2013] SGCA 43 / [2013] 4 SLR 193",
        "ecli": "SG:SGCA:2013:43",
        "doctype": "Urteil",
        "leitsatz": "新加坡终审法院确立商业合同‘事实上的默示条款’（Terms Implied in Fact）权威三步测试法：(1) 确定合同是否存在真正的漏洞（Gap）；(2) 审查该默示条款是否为赋予合同商业效能所绝对必要（Business Efficacy Test）；(3) 审查该条款是否显而易见至‘好事旁观者’询问时双方均会答复‘当然如此’（Officious Bystander Test）。法庭决不替当事人起草更合理的合同。",
        "tenor": "终审法院支持胜宝旺海事（Sembcorp Marine）上诉，推翻高等法院判决：确认涉案合资公司章程中并不存在‘合资一方出售股份后其指派董事必须自动辞职’的默示条款，严格以章程明文规定为准。",
        "tatbestand": "胜宝旺海事与 PPL 控股签署合资协议收购船厂股权。后双方产生控制权争夺，PPL 主张依据公司治理常理，合资章程中默示包含股东退出后其指派代表必须离职的条款，并据此对抗胜宝旺指派之董事。",
        "gruende": "终审法院明确指出：默示条款是对契约自由原则的极其有限例外。当事人的疏忽未作规定不等于存在法律上的漏洞。如果当事人经深思熟虑故意留白或合同在无该条款下依然能够正常运转，法庭绝不得以衡平或合理性为由强行植入未经约定的义务。该案成为东盟工程总承包与合资章程解释必引的第一先例。",
        "source_url": "https://www.elitigation.sg/gd/s/2013_SGCA_43"
    }
]
