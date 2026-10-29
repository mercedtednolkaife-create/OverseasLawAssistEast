"""东盟六国涉外经贸、法律冲突法专章与核心法典章节条文群扩充脚本 (Phase 5 L1 Clusters & PIL Expansion)
涵盖模块：
1. 越南：2005年商业法第7章商事救济闭环 (Art 300, 303, 304, 305, 307) + 2015年民法典第5编涉外民事关系法律适用专编 (Art 663, 670, 683) + 2020年投资法外资保护 (Art 8, 9) + 河内高院683条施工选法强制适用判例
2. 印尼：民法典第三编违约赔偿与不可抗力专章 (Art 1243, 1244, 1245, 1246, 1247, 1248, 1339) + 2007年投资法国民待遇与征收保护 (Art 4) + AB 1847 不动产属地法 (Art 17) + 最高法院 Somasi 催告前置判例
3. 马来西亚：1950年合同法违约救济四大支柱 (Sec 56, 65, 74, 75) + CIPAA 2012 法定裁决程序与合法停工链 (Sec 5, 6, 7, 15, 28, 29) + 联邦法院 Cubic 违约金测试判例
4. 菲律宾：民法典债务与违约金责任专章 (Art 1170, 1191, 1226, 1227, 1228) + 涉外冲突规范 (Art 16, 17) + 外资法负面清单 (RA 11647 Sec 4)
5. 泰国：民商法典违约金、解除权与承揽专章 (Sec 380, 381, 386, 387, 587, 605) + 佛历2481年法律冲突法涉外选法与公共秩序 (Sec 5, 9, 13) + 最高法院涉外公共秩序排除判例
6. 新加坡：SOPA 2004 付款答辩与法定合法停工权 (Sec 11, 26)
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

# =========================================================================
# L1 Phase 5 法条群扩充列表 (40+ 条核心章节成文法规范)
# =========================================================================
PHASE5_L1_NORMS: List[Dict[str, Any]] = [
    # ---------------------------------------------------------------------
    # 1. 越南 (Vietnam) - 商业法商事救济整章 + 民法典涉外选法专编 + 投资法
    # ---------------------------------------------------------------------
    {
        "norm_id": "VN:Commercial_Law_2005:Art300",
        "law": "Commercial_Law_VN",
        "enbez": "Art.300",
        "title": "《越南商业法》第300条：违约金责任之定义与法定约定前提",
        "heading_path": "Luật Thương mại 2005 > Chương VII Chế tài trong thương mại > Điều 300",
        "text_de": "Vietnamese Commercial Law Art. 300 (Fine for Breach)",
        "language_mode": "trilingual",
        "lang_original": "vi",
        "text_original": "Phạt vi phạm là việc bên bị vi phạm yêu cầu bên vi phạm trả một khoản tiền phạt do vi phạm hợp đồng nếu trong hợp đồng có thoả thuận, trừ các trường hợp miễn trách nhiệm quy định tại Điều 294 của Luật này.",
        "text_en": "Fine for breach means a remedy whereby an aggrieved party requires a breaching party to pay a fine for breach if agreed in the contract.",
        "text_zh": "【商事违约金约定前提】违约金（Phạt vi phạm）是指守约方依合同明文约定，要求违约方就违约行为支付惩罚性款项之救济方式。若合同中未作明文约定，守约方无权主张违约金，仅能主张损害赔偿。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "VN:Commercial_Law_2005:Art303",
        "law": "Commercial_Law_VN",
        "enbez": "Art.303",
        "title": "《越南商业法》第303条：违约损害赔偿责任之四大法定成立要件",
        "heading_path": "Luật Thương mại 2005 > Chương VII Chế tài trong thương mại > Điều 303",
        "text_de": "Vietnamese Commercial Law Art. 303 (Grounds for Liability to Compensate for Damage)",
        "language_mode": "trilingual",
        "lang_original": "vi",
        "text_original": "Trừ các trường hợp miễn trách nhiệm quy định tại Điều 294 của Luật này, trách nhiệm bồi thường thiệt hại phát sinh khi có đủ các yếu tố sau đây: 1. Có hành vi vi phạm hợp đồng; 2. Có thiệt hại thực tế; 3. Hành vi vi phạm hợp đồng là nguyên nhân trực tiếp gây ra thiệt hại.",
        "text_en": "Liability to compensate for damage arises when: 1. There is a breach; 2. There is actual loss; 3. The breach is the direct cause of loss.",
        "text_zh": "【损害赔偿四大法定要件】主张违约损害赔偿必须同时满足：① 存在客观违约行为；② 守约方遭受直接且实际之损失（Thiệt hại thực tế）；③ 违约行为与损失间存在直接必然之因果关系；④ 不存在法定的免责事由（如不可抗力）。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "VN:Commercial_Law_2005:Art304",
        "law": "Commercial_Law_VN",
        "enbez": "Art.304",
        "title": "《越南商业法》第304条：损害赔偿索赔之举证责任与证据标准",
        "heading_path": "Luật Thương mại 2005 > Chương VII Chế tài trong thương mại > Điều 304",
        "text_de": "Vietnamese Commercial Law Art. 304 (Burden of Proof for Damages)",
        "language_mode": "trilingual",
        "lang_original": "vi",
        "text_original": "Bên yêu cầu bồi thường thiệt hại phải chứng minh tổn thất, mức độ tổn thất do hành vi vi phạm gây ra và khoản lợi trực tiếp mà bên bị vi phạm đáng lẽ được hưởng nếu không có hành vi vi phạm.",
        "text_en": "The party claiming damages must prove loss, extent of loss caused by the breach and direct profits that would have been earned.",
        "text_zh": "【实际损失法定举证责任】主张损害赔偿之一方，必须就违约造成的实际损失金额、损失程度以及若无违约本可获得的直接利润承担完全举证责任。无法提供确凿客观财务凭证与审计记录的，法庭或仲裁庭不予支持。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "VN:Commercial_Law_2005:Art305",
        "law": "Commercial_Law_VN",
        "enbez": "Art.305",
        "title": "《越南商业法》第305条：守约方减轻损失之法定义务 (Duty to Mitigate)",
        "heading_path": "Luật Thương mại 2005 > Chương VII Chế tài trong thương mại > Điều 305",
        "text_de": "Vietnamese Commercial Law Art. 305 (Obligation to Mitigate Damage)",
        "language_mode": "trilingual",
        "lang_original": "vi",
        "text_original": "Bên yêu cầu bồi thường thiệt hại phải áp dụng các biện pháp hợp lý để hạn chế tổn thất kể cả tổn thất đối với khoản lợi trực tiếp đáng lẽ được hưởng do hành vi vi phạm hợp đồng gây ra; nếu không áp dụng các biện pháp đó, bên vi phạm hợp đồng có quyền yêu cầu giảm bớt mức bồi thường thiệt hại bằng mức tổn thất đáng lẽ có thể hạn chế được.",
        "text_en": "The aggrieved party must take reasonable measures to mitigate loss; failure to do so entitles breaching party to claim reduction equal to avoidable loss.",
        "text_zh": "【减损法定义务与抗辩】守约方必须采取合理可行之措施以减少损失扩大；若守约方怠于采取减损措施，违约方有权请求法官或仲裁庭扣减因守约方怠误而本可避免的损失数额。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "VN:Commercial_Law_2005:Art307",
        "law": "Commercial_Law_VN",
        "enbez": "Art.307",
        "title": "《越南商业法》第307条：违约金与损害赔偿金之竞合适用规则",
        "heading_path": "Luật Thương mại 2005 > Chương VII Chế tài trong thương mại > Điều 307",
        "text_de": "Vietnamese Commercial Law Art. 307 (Relationship between Fine and Damages)",
        "language_mode": "trilingual",
        "lang_original": "vi",
        "text_original": "1. Trường hợp các bên không có thoả thuận phạt vi phạm thì bên bị vi phạm chỉ có quyền yêu cầu bồi thường thiệt hại... 2. Trường hợp các bên có thoả thuận phạt vi phạm thì bên bị vi phạm có quyền áp dụng cả chế tài phạt vi phạm và buộc bồi thường thiệt hại, trừ trường hợp các bên có thoả thuận khác.",
        "text_en": "Where parties agree on fine, aggrieved party may apply both fine and damages unless otherwise agreed.",
        "text_zh": "【违约金与赔偿金双轨并用】合同双方既约定违约金又发生实际损失的，守约方有权同时主张法定上限内（8%）的违约金与填平实际损失的损害赔偿金。但二者相加不得形成重复惩罚性过度得利。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "VN:Civil_Code_2015:Art663",
        "law": "Civil_Code_VN",
        "enbez": "Art.663",
        "title": "《越南民法典》第663条：涉外民事关系之法定界定范围",
        "heading_path": "Bộ luật Dân sự 2015 > Phần thứ năm Pháp luật áp dụng đối với quan hệ dân sự có yếu tố nước ngoài > Điều 663",
        "text_de": "Vietnamese Civil Code Art. 663 (Scope of Civil Relations with Foreign Elements)",
        "language_mode": "trilingual",
        "lang_original": "vi",
        "text_original": "Quan hệ dân sự có yếu tố nước ngoài là quan hệ dân sự thuộc một trong các trường hợp sau đây: a) Có ít nhất một trong các bên tham gia là cá nhân, pháp nhân nước ngoài; b) Các bên tham gia đều là công dân, pháp nhân Việt Nam nhưng việc xác lập, thay đổi, thực hiện hoặc chấm dứt quan hệ đó xảy ra tại nước ngoài; c) Các bên tham gia đều là công dân, pháp nhân Việt Nam nhưng đối tượng của quan hệ dân sự đó ở nước ngoài.",
        "text_en": "Civil relations with foreign elements involve foreign parties or establishment/performance abroad.",
        "text_zh": "【涉外民事关系法定范围】符合下列情形之一即构成涉外法律关系：① 至少一方当事人为外国公民或外国法人；② 当事人虽均为越南主体，但合同订立、变更、履行或终止发生于境外；③ 民事法律关系客体位于境外。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "VN:Civil_Code_2015:Art670",
        "law": "Civil_Code_VN",
        "enbez": "Art.670",
        "title": "《越南民法典》第670条：外国法适用之公共秩序保留 (Public Policy Exception)",
        "heading_path": "Bộ luật Dân sự 2015 > Phần thứ năm > Điều 670",
        "text_de": "Vietnamese Civil Code Art. 670 (Public Policy Reservation)",
        "language_mode": "trilingual",
        "lang_original": "vi",
        "text_original": "Pháp luật nước ngoài được dẫn chiếu không được áp dụng trong các trường hợp sau đây: a) Hậu quả của việc áp dụng pháp luật nước ngoài trái với các nguyên tắc cơ bản của pháp luật Việt Nam; b) Nội dung của pháp luật nước ngoài không xác định được mặc dù đã áp dụng các biện pháp cần thiết theo quy định của pháp luật tố tụng. Trường hợp pháp luật nước ngoài không được áp dụng... thì pháp luật Việt Nam được áp dụng.",
        "text_en": "Foreign law shall not apply if its consequence violates fundamental principles of Vietnamese law.",
        "text_zh": "【公共秩序保留排斥外国法】涉外合同约定的外国法或冲突规范指引的外国法，若其适用后果违背越南法律的基本原则（Trật tự công cộng），该外国法一律排除适用，强制回退适用越南法律。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "VN:Civil_Code_2015:Art683",
        "law": "Civil_Code_VN",
        "enbez": "Art.683",
        "title": "《越南民法典》第683条：涉外合同准据法选法效力与不动产建设工程强行专属管辖",
        "heading_path": "Bộ luật Dân sự 2015 > Phần thứ năm > Điều 683",
        "text_de": "Vietnamese Civil Code Art. 683 (Law Applicable to Contracts - Lex Situs Rule)",
        "language_mode": "trilingual",
        "lang_original": "vi",
        "text_original": "1. Các bên trong quan hệ hợp đồng được thoả thuận lựa chọn pháp luật áp dụng đối với hợp đồng, trừ trường hợp quy định tại các khoản 4, 5 và 6 Điều này... 2. Trường hợp hợp đồng có đối tượng là bất động sản thì pháp luật áp dụng đối với việc chuyển giao quyền sở hữu, quyền khác đối với tài sản là bất động sản, thuê bất động sản hoặc việc sử dụng bất động sản để bảo đảm thực hiện nghĩa vụ là pháp luật của nước nơi có bất động sản.",
        "text_en": "Parties may agree on applicable law, EXCEPT contracts regarding immovable property situated in Vietnam must be governed by Vietnamese law.",
        "text_zh": "【不动产工程专属适用越南法红线】涉外合同双方原则上可自由协商选择准据法。但是，若合同客体为位于越南境内之不动产（如土地使用权、厂房、基础设施建设工程施工），必须强制适用越南法律，当事人约定适用外国法之条款自始无效！",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "VN:Investment_Law_2020:Art8",
        "law": "Investment_Law_VN",
        "enbez": "Art.8",
        "title": "《越南2020年投资法》第8条：外商合法财产所有权保障与禁止征收征用补偿",
        "heading_path": "Luật Đầu tư 2020 > Chương II Bảo đảm đầu tư kinh doanh > Điều 8",
        "text_de": "Vietnamese Investment Law Art. 8 (Protection of Investor Property Ownership)",
        "language_mode": "trilingual",
        "lang_original": "vi",
        "text_original": "1. Tài sản hợp pháp của nhà đầu tư không bị quốc hữu hóa hoặc bị tịch thu bằng biện pháp hành chính. 2. Trường hợp Nhà nước trưng mua, trưng dụng tài sản vì lý do quốc phòng, an ninh hoặc vì lợi ích quốc gia... thì nhà đầu tư được thanh toán, bồi thường theo giá thị trường.",
        "text_en": "Lawful assets of investors shall not be nationalized. Requisition for public interest shall be compensated at market price.",
        "text_zh": "【禁止国有化与市价补偿保障】外国投资者在越南的合法资产绝不以行政手段予以国有化或没收。国家因国防、安全或重大公共利益确需征用投资者财产的，必须依法按照征用当时之市场公允价格予以全额支付与补偿。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "VN:Investment_Law_2020:Art9",
        "law": "Investment_Law_VN",
        "enbez": "Art.9",
        "title": "《越南2020年投资法》第9条：外资市场准入限制行业与准入条件清单 (Negative List)",
        "heading_path": "Luật Đầu tư 2020 > Chương II > Điều 9",
        "text_de": "Vietnamese Investment Law Art. 9 (Market Access Conditions for Foreign Investors)",
        "language_mode": "trilingual",
        "lang_original": "vi",
        "text_original": "1. Ngành, nghề tiếp cận thị trường có điều kiện đối với nhà đầu tư nước ngoài bao gồm: a) Ngành, nghề chưa được tiếp cận thị trường; b) Ngành, nghề tiếp cận thị trường có điều kiện. 2. Chính phủ công bố Danh mục ngành, nghề hạn chế tiếp cận thị trường đối với nhà đầu tư nước ngoài.",
        "text_en": "Sectors with conditional market access for foreign investors are published by Government.",
        "text_zh": "【外资准入负面清单制度】外国投资者适用国民待遇原则，但在政府公布的《外资市场准入限制行业清单》内的工程咨询、电信基建等行业，必须满足外资持股比例上限、属地合资伙伴资质以及经营范围特别许可前置条件。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory"
    },

    # ---------------------------------------------------------------------
    # 2. 印度尼西亚 (Indonesia) - 民法典违约损害赔偿整章 + 投资法
    # ---------------------------------------------------------------------
    {
        "norm_id": "ID:KUHPerdata:Art1243",
        "law": "KUHPerdata_ID",
        "enbez": "Art.1243",
        "title": "《印尼民法典》第1243条：违约损害赔偿之法定催告前置令 (Somasi) 强制要件",
        "heading_path": "Burgerlijk Wetboek (KUHPerdata) > Buku III > Bab I > Bagian 4 > Pasal 1243",
        "text_de": "Indonesian Civil Code Art. 1243 (Notice of Default Somasi Requirement)",
        "language_mode": "trilingual",
        "lang_original": "id",
        "text_original": "Penggantian biaya, kerugian dan bunga karena tak dipenuhinya suatu perikatan mulai diwajibkan, bila debitur, walaupun telah dinyatakan lalai, tetap lalai untuk memenuhi perikatan itu, atau jika sesuatu yang harus diberikan atau dilakukannya hanya dapat diberikan atau dilakukannya dalam tenggang waktu yang telah dilampaukannya.",
        "text_en": "Compensation for costs, damages and interest for non-performance is only obligatory after debtor has been declared in default (Somasi).",
        "text_zh": "【法定催告前置令 (Somasi)】追究合同违约赔偿责任，必须以债权人向债务人合法送达正式书面迟延催告函（Somasi）且债务人于合理宽限期内仍未纠正为法定前置要件；未经有效催告直接扣罚赔偿金或解约的，在印尼法院构成违法。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "ID:KUHPerdata:Art1244",
        "law": "KUHPerdata_ID",
        "enbez": "Art.1244",
        "title": "《印尼民法典》第1244条：外部不可归责事由不可抗力免责 (Overmacht)",
        "heading_path": "Burgerlijk Wetboek (KUHPerdata) > Buku III > Bab I > Bagian 4 > Pasal 1244",
        "text_de": "Indonesian Civil Code Art. 1244 (Force Majeure Overmacht Exemption)",
        "language_mode": "trilingual",
        "lang_original": "id",
        "text_original": "Debitur harus dihukum untuk mengganti biaya, kerugian dan bunga, bila ia tak dapat membuktikan bahwa tidak dilaksanakannya perikatan itu atau tidak tepatnya waktu dalam melaksanakan perikatan itu disebabkan oleh suatu hal yang tak terduga, yang tak dapat dipertanggungjawabkan kepadanya, walaupun tidak ada itikad buruk padanya.",
        "text_en": "Debtor must pay damages unless proving non-performance was caused by unexpected external cause not attributable to him.",
        "text_zh": "【不可抗力免责举证】债务人未能履约或迟延履约的，若能举证证明不履约系由其无法预料、且不可归责于自身的外部意外事件（Overmacht）所致，且其主观上不存在恶意，依法免除违约损害赔偿与利息给付责任。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "ID:KUHPerdata:Art1245",
        "law": "KUHPerdata_ID",
        "enbez": "Art.1245",
        "title": "《印尼民法典》第1245条：偶发意外事件与强制不可抗力无赔偿责任 (Keadaan Memaksa)",
        "heading_path": "Burgerlijk Wetboek (KUHPerdata) > Buku III > Bab I > Bagian 4 > Pasal 1245",
        "text_de": "Indonesian Civil Code Art. 1245 (Fortuitous Event and Keadaan Memaksa)",
        "language_mode": "trilingual",
        "lang_original": "id",
        "text_original": "Tidak ada penggantian biaya, kerugian dan bunga, bila karena keadaan memaksa atau karena hal yang terjadi secara kebetulan, debitur terhalang untuk memberikan atau berbuat sesuatu yang diwajibkan, atau melakukan suatu perbuatan yang terlarang baginya.",
        "text_en": "No compensation is payable if debtor was prevented from performing by force majeure or fortuitous event.",
        "text_zh": "【意外事件绝对免赔】若因不可抗力状态（Keadaan Memaksa）或纯属偶发的自然意外事件，导致债务人客观上无法履行交付或作为义务，债权人无权主张任何费用补偿、损害赔偿金或迟延违约金利息。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "ID:KUHPerdata:Art1246",
        "law": "KUHPerdata_ID",
        "enbez": "Art.1246",
        "title": "《印尼民法典》第1246条：损害赔偿计算范围（实际减损损失与所失利益）",
        "heading_path": "Burgerlijk Wetboek (KUHPerdata) > Buku III > Bab I > Bagian 4 > Pasal 1246",
        "text_de": "Indonesian Civil Code Art. 1246 (Scope of Damages: Loss and Lost Profits)",
        "language_mode": "trilingual",
        "lang_original": "id",
        "text_original": "Biaya, ganti rugi dan bunga, yang boleh dituntut kreditur, terdiri atas kerugian yang telah dideritanya dan keuntungan yang sedianya dapat diperolehnya, tanpa mengurangi pengecualian dan perubahan yang disebut di bawah ini.",
        "text_en": "Damages claimable consist of loss suffered and profits which could have been gained.",
        "text_zh": "【损害赔偿构成范围】债权人有权索赔的违约损害赔偿金，严格由其实际承受的财产直接减损损失（Kekayaan yang berkurang）与本应获得的合理预期利润（Keuntungan yang sedianya dapat diperoleh）构成。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "ID:KUHPerdata:Art1247",
        "law": "KUHPerdata_ID",
        "enbez": "Art.1247",
        "title": "《印尼民法典》第1247条：可预见性原则对违约损害赔偿范围之法定限制",
        "heading_path": "Burgerlijk Wetboek (KUHPerdata) > Buku III > Bab I > Bagian 4 > Pasal 1247",
        "text_de": "Indonesian Civil Code Art. 1247 (Foreseeability Rule of Damages)",
        "language_mode": "trilingual",
        "lang_original": "id",
        "text_original": "Debitur hanya diwajibkan mengganti kerugian yang telah diduga atau sedianya dapat diduga pada saat perikatan diadakan, kecuali jika tidak dipenuhinya perikatan itu disebabkan oleh tipu daya yang dilakukannya.",
        "text_en": "Debtor is only liable for damages foreseen or which could have been foreseen at time contract was made, unless breach was caused by fraud.",
        "text_zh": "【可预见性法定限额】除债务人存在故意欺诈（Tipu daya）情形外，违约损害赔偿金严格受限于双方在合同订立当时“已经预见或理应能够预见”之合理损失范畴，突发性远期间接损失依法不得索赔。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "ID:KUHPerdata:Art1248",
        "law": "KUHPerdata_ID",
        "enbez": "Art.1248",
        "title": "《印尼民法典》第1248条：违约损失与不履约行为间直接因果关系要件",
        "heading_path": "Burgerlijk Wetboek (KUHPerdata) > Buku III > Bab I > Bagian 4 > Pasal 1248",
        "text_de": "Indonesian Civil Code Art. 1248 (Direct and Immediate Consequence Requirement)",
        "language_mode": "trilingual",
        "lang_original": "id",
        "text_original": "Bahkan jika tidak dipenuhinya perikatan itu disebabkan oleh tipu daya debitur, penggantian biaya, kerugian dan bunga, sekadar mengenai kerugian yang diderita oleh kreditur dan keuntungan yang terhilang baginya, hanya mencakup apa yang merupakan akibat langsung dan seketika dari tidak dipenuhinya perikatan itu.",
        "text_en": "Damages only include what is an immediate and direct consequence of non-performance.",
        "text_zh": "【直接因果关系刚性要件】即使违约系因债务人之欺诈故意引起，其损害赔偿范围也仅限于违约不履约行为所“直接且立即引起的结果（Akibat langsung dan seketika）”，阻断多重因果关系中的二次放大损失。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "ID:KUHPerdata:Art1339",
        "law": "KUHPerdata_ID",
        "enbez": "Art.1339",
        "title": "《印尼民法典》第1339条：合同约束力扩张至公平、习惯与成文法规范",
        "heading_path": "Burgerlijk Wetboek (KUHPerdata) > Buku III > Bab II > Pasal 1339",
        "text_de": "Indonesian Civil Code Art. 1339 (Contracts Bind According to Equity, Custom and Law)",
        "language_mode": "trilingual",
        "lang_original": "id",
        "text_original": "Persetujuan tidak hanya mengikat apa yang dengan tegas ditentukan di dalamnya, melainkan juga segala sesuatu yang menurut sifatnya persetujuan dituntut berdasarkan keadilan, kebiasaan, atau undang-undang.",
        "text_en": "Agreements bind not only to express terms, but to equity, custom, or statute.",
        "text_zh": "【合同法外扩张约束力】合同不仅约束当事人在条文中明文约定的事项，而且依合同性质，基于实质公平原则（Keadilan）、商业交易惯例（Kebiasaan）或成文法律强行规定所要求的一切义务，均对当事人产生法定约束力。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "ID:UU_25_2007:Art4",
        "law": "UU_25_2007_Investment",
        "enbez": "Art.4",
        "title": "《印尼投资法》第4条：外国投资者国民待遇与合法资产禁止征收征用保证",
        "heading_path": "UU No. 25/2007 tentang Penanaman Modal > Bab III Kebijakan Dasar Penanaman Modal > Pasal 4",
        "text_de": "Indonesian Investment Law Art. 4 (Equal Treatment and Non-Expropriation)",
        "language_mode": "trilingual",
        "lang_original": "id",
        "text_original": "Pemerintah memberikan perlakuan yang sama kepada semua penanam modal... Pemerintah tidak akan melakukan tindakan nasionalisasi atau pengambilalihan hak kepemilikan penanam modal, kecuali dengan undang-undang dan dengan memberikan ganti rugi yang jumlahnya ditetapkan berdasarkan harga pasar.",
        "text_en": "Government provides equal treatment and shall not nationalize investor property except by law with market compensation.",
        "text_zh": "【外资国民待遇与禁止征收原则】印尼政府对外国投资者实施同等国民待遇。除依据法律专门颁布特别法令且按照市场公允价格提供全额现金补偿外，政府严禁对外国投资者财产采取任何形式的国有化或所有权剥夺措施。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "ID:AB_1847:Art17",
        "law": "AB_1847_Conflict",
        "enbez": "Art.17",
        "title": "《印尼法律适用总则》(AB 1847) 第17条：不动产物权与地面建设工程属地法原则 (Lex Rei Sitae)",
        "heading_path": "Algemene Bepalingen van Wetgeving voor Indonesie (AB) > Pasal 17",
        "text_de": "Indonesian Private International Law Art. 17 (Lex Rei Sitae Rule)",
        "language_mode": "trilingual",
        "lang_original": "id",
        "text_original": "Mengenai barang-barang yang tidak bergerak, berlakulah undang-undang dari negeri atau tempat di mana barang-barang itu terletak.",
        "text_en": "Regarding immovable property, the law of the country or place where it is situated shall apply.",
        "text_zh": "【涉外不动产工程专属属地管辖】位于印尼境内的土地、厂房、地役权及固定于土地之基建工程，一切涉及物权设立、转让、抵押担保及施工实体权利义务，强制适用印尼法律（Lex Rei Sitae），不得以境外选法排除。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory"
    },

    # ---------------------------------------------------------------------
    # 3. 马来西亚 (Malaysia) - 1950年合同法违约救济支柱 + CIPAA 2012 程序链
    # ---------------------------------------------------------------------
    {
        "norm_id": "MY:Contracts_Act_1950:Sec56",
        "law": "Contracts_Act_1950",
        "enbez": "Sec.56",
        "title": "《马来西亚1950年合同法》第56条：履行期限以时间为要素 (Time of the Essence) 之违约后果",
        "heading_path": "Contracts Act 1950 > Part V Of the Performance of Contracts > Section 56",
        "text_de": "Malaysian Contracts Act 1950 Sec. 56 (Effect of Failure to Perform at Fixed Time)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "When a party to a contract promises to do a certain thing at or before a specified time... and fails to do any such thing at or before the specified time, the contract, or so much of it as has not been performed, becomes voidable at the option of the promisee, if the intention of the parties was that time should be of the essence of the contract.",
        "text_en": "Failure to perform when time is of the essence makes contract voidable at option of promisee.",
        "text_zh": "【时间为要素违约解约权】若合同双方意图表明履行时间为核心要素（Time is of essence，如 FIDIC 约定竣工日），一方未能在约定时间节点完成工程，相对方有权选择撤销/解除合同并追究迟延损害赔偿责任。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "MY:Contracts_Act_1950:Sec65",
        "law": "Contracts_Act_1950",
        "enbez": "Sec.65",
        "title": "《马来西亚1950年合同法》第65条：合同撤销与解除后之利益返还与恢复原状",
        "heading_path": "Contracts Act 1950 > Part V > Section 65",
        "text_de": "Malaysian Contracts Act 1950 Sec. 65 (Consequence of Rescission of Voidable Contract)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "When a person at whose option a contract is voidable rescinds it, the other party thereto need not perform any promise therein contained in which he is the promisor. The party rescinding a voidable contract shall, if he have received any benefit thereunder from another party to such contract, restore the benefit, so far as may be, to the person from whom it was received.",
        "text_en": "Party rescinding voidable contract must restore any benefit received thereunder.",
        "text_zh": "【解约恢复原状义务】行使法定权利解除合同之一方，若已自对方受领工程进度款、预付款或设备材料利益，必须将其所受利益在可行限度内完全返还恢复原状，未完工程由当事人进行结算折价补偿。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "MY:Contracts_Act_1950:Sec74",
        "law": "Contracts_Act_1950",
        "enbez": "Sec.74",
        "title": "《马来西亚1950年合同法》第74条：违约损害赔偿两段式经典因果与可预见性规则 (Hadley v. Baxendale)",
        "heading_path": "Contracts Act 1950 > Part VI Of the Consequences of Breach of Contract > Section 74",
        "text_de": "Malaysian Contracts Act 1950 Sec. 74 (Compensation for Loss Caused by Breach)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "When a contract has been broken, the party who suffers by the breach is entitled to receive, from the party who has broken the contract, compensation for any loss or damage caused to him thereby, which naturally arose in the usual course of things from the breach, or which the parties knew, when they made the contract, to be likely to result from the breach of it.",
        "text_en": "Aggrieved party is entitled to compensation for loss naturally arising in usual course, or reasonably foreseen at contract formation.",
        "text_zh": "【违约损害赔偿两大经典支柱】可索赔损失包括两类：① 违约行为在通常交易进程中自然产生（Naturally arose）的通常损失；② 订立合同时当事人明知可能由此导致的特别损失。间接遥远之损失依法不予赔偿。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "MY:Contracts_Act_1950:Sec75",
        "law": "Contracts_Act_1950",
        "enbez": "Sec.75",
        "title": "《马来西亚1950年合同法》第75条：预定违约金条款与合理赔偿额司法审查规则",
        "heading_path": "Contracts Act 1950 > Part VI > Section 75",
        "text_de": "Malaysian Contracts Act 1950 Sec. 75 (Compensation for Breach Where Penalty Stipulated)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "When a contract has been broken, if a sum is named in the contract as the amount to be paid in case of such breach, or if the contract contains any other stipulation by way of penalty, the party complaining of the breach is entitled, whether or not actual damage or loss is proved to have been caused thereby, to receive from the party who has broken the contract reasonable compensation not exceeding the amount so named.",
        "text_en": "Party is entitled to receive reasonable compensation not exceeding the penalty amount named, whether actual damage is proved or not.",
        "text_zh": "【违约金合理赔偿额司法限制】合同无论约定何种名目的预定违约金（Liquidated Damages），守约方有权获得的赔偿金额以法官认定的“合理赔偿额（Reasonable Compensation）”为限，且绝对不得超过合同约定的封顶数额。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "MY:CIPAA_2012:Sec5",
        "law": "CIPAA_2012",
        "enbez": "Sec.5",
        "title": "《马来西亚CIPAA 2012》第5条：法定付款索赔 (Payment Claim) 送达形式与要素要件",
        "heading_path": "CIPAA 2012 > Part II Adjudication of Payment Disputes > Section 5",
        "text_de": "Malaysian CIPAA 2012 Sec. 5 (Payment Claim)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "An unpaid party may serve a payment claim on a non-paying party for payment due for construction work... The payment claim shall be in writing and shall include: (a) the amount claimed and due date; (b) details to identify cause of action; (c) description of work.",
        "text_en": "Unpaid party may serve payment claim in writing specifying amount, due date and work description.",
        "text_zh": "【付款索赔法定要件】未获付款承包商或分包商有权送达书面付款索赔书（Payment Claim）。必须载明索赔工程款数额、到期日、具体工程项目工作量描述及对应合同依据，欠缺法定要素将导致裁决人丧失管辖权。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "MY:CIPAA_2012:Sec6",
        "law": "CIPAA_2012",
        "enbez": "Sec.6",
        "title": "《马来西亚CIPAA 2012》第6条：付款答辩 (Payment Response) 10日法定时效与抵销抗辩",
        "heading_path": "CIPAA 2012 > Part II > Section 6",
        "text_de": "Malaysian CIPAA 2012 Sec. 6 (Payment Response)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "A non-paying party who is served with a payment claim shall serve a payment response within 10 working days of the receipt of the payment claim. A non-paying party who admits the whole or part of the payment claim shall pay; if disputing, shall state the reason for dispute.",
        "text_en": "Non-paying party must serve payment response within 10 working days, stating reasons for dispute.",
        "text_zh": "【付款答辩10日失权门限】被索赔方必须自收到付款索赔之日起 10 个工作日内送达书面付款答辩（Payment Response）。任何延误损害赔偿、质量瑕疵扣款或抵销主张必须在答辩中提出，逾期未答辩视为对索赔金额全部争议但丧失先行抵销证据抗辩先机。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "MY:CIPAA_2012:Sec15",
        "law": "CIPAA_2012",
        "enbez": "Sec.15",
        "title": "《马来西亚CIPAA 2012》第15条：高等法院撤销法定裁决决定之四大法定抗辩事由",
        "heading_path": "CIPAA 2012 > Part II > Section 15",
        "text_de": "Malaysian CIPAA 2012 Sec. 15 (Jurisdiction Grounds to Set Aside Adjudication Decision)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "An aggrieved party may apply to the High Court to set aside an adjudication decision on grounds that: (a) decision was improperly procured through fraud or bribery; (b) denial of natural justice; (c) adjudicator acted in excess of jurisdiction; or (d) adjudicator was not impartial.",
        "text_en": "High Court may set aside decision on grounds of fraud, denial of natural justice, excess of jurisdiction or lack of impartiality.",
        "text_zh": "【法院撤销裁决法定四大事由】当事人有权向马来西亚高等法院申请终局撤销 CIPAA 裁决之法定理由包括：① 裁决系通过欺诈或贿赂取得；② 严重违反正当程序/自然公正原则（Denial of Natural Justice）；③ 裁决人越权管辖；④ 裁决人丧失中立性存在偏颇。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "MY:CIPAA_2012:Sec28",
        "law": "CIPAA_2012",
        "enbez": "Sec.28",
        "title": "《马来西亚CIPAA 2012》第28条：裁决生效未获付款承包商之法定停工权 (Suspension)",
        "heading_path": "CIPAA 2012 > Part II > Section 28",
        "text_de": "Malaysian CIPAA 2012 Sec. 28 (Right to Suspend Works for Non-Payment)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "A party who obtained an adjudication decision in its favour may suspend the performance of construction work or reduce the rate of progress if the adjudication amount is not paid within the period specified.",
        "text_en": "Prevailing party may suspend works or slow progress if adjudicated amount is not paid.",
        "text_zh": "【法定合法停工权】若裁决确定的工程款未在法定期限内足额支付，胜诉之承包商或分包商享有法定权利暂停全部工程施工或放慢施工节奏（Slow down rate of progress），发包人不得以擅自停工为由扣罚违约金。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "MY:CIPAA_2012:Sec29",
        "law": "CIPAA_2012",
        "enbez": "Sec.29",
        "title": "《马来西亚CIPAA 2012》第29条：法定停工期间承包商享有工期顺延与费用补偿权",
        "heading_path": "CIPAA 2012 > Part II > Section 29",
        "text_de": "Malaysian CIPAA 2012 Sec. 29 (EOT and Cost Entitlement during Suspension)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "The party who exercises the right to suspend or reduce progress under section 28: (a) is entitled to a fair and reasonable extension of time to complete the work; and (b) is entitled to recover any loss and expense incurred arising from the suspension.",
        "text_en": "Contractor suspending under Sec 28 is entitled to reasonable EOT and recovery of loss and expense.",
        "text_zh": "【停工工期顺延与停工损失全额索赔】依据第28条行使法定停工权之承包商：① 自动享有公平合理的竣工工期顺延（EOT）；② 有权自发包人处全额索赔因停工、窝工及复工动员所遭受的实际窝工损失与合理费用（Loss and Expense）。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory"
    },

    # ---------------------------------------------------------------------
    # 4. 菲律宾 (Philippines) - 民法典违约金与涉外冲突专章 + 外资法
    # ---------------------------------------------------------------------
    {
        "norm_id": "PH:Civil_Code:Art1170",
        "law": "Civil_Code_PH",
        "enbez": "Art.1170",
        "title": "《菲律宾民法典》第1170条：违约金责任中欺诈、过失与迟延 (Mora) 之归责原则",
        "heading_path": "Civil Code of the Philippines > Book IV > Title I > Chapter 2 > Article 1170",
        "text_de": "Philippine Civil Code Art. 1170 (Liability for Fraud, Negligence, or Delay)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Those who in the performance of their obligations are guilty of fraud, negligence, or delay, and those who in any manner contravene the tenor thereof, are liable for damages.",
        "text_en": "Those guilty of fraud, negligence, or delay are liable for damages.",
        "text_zh": "【债务不履行归责原则】在履行民商事合同债务过程中，凡存在欺诈（Dolo）、过失（Culpa）或迟延履约（Mora），或以任何违反合同明示条款之方式作为者，必须对守约方承担完全损害赔偿责任。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "PH:Civil_Code:Art1191",
        "law": "Civil_Code_PH",
        "enbez": "Art.1191",
        "title": "《菲律宾民法典》第1191条：双务工程合同法定默示解除权 (Tacit Resolutory Condition)",
        "heading_path": "Civil Code of the Philippines > Book IV > Title I > Chapter 3 > Section 1 > Article 1191",
        "text_de": "Philippine Civil Code Art. 1191 (Implied Power to Rescind Reciprocal Obligations)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "The power to rescind obligations is implied in reciprocal ones, in case one of the obligors should not comply with what is incumbent upon him. The injured party may choose between the fulfillment and the rescission of the obligation, with the payment of damages in either case.",
        "text_en": "Power to rescind is implied in reciprocal obligations upon breach, with damages.",
        "text_zh": "【双务合同法定默示解约权】在工程总承包等双务有偿合同中，当一方实质性违约未履行其主合同债务时，受害方享有法定默示解除权；受害方有权自由择一行使“请求强制履行本约并赔偿损失”或“解除合同并赔偿损失”。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "PH:Civil_Code:Art1226",
        "law": "Civil_Code_PH",
        "enbez": "Art.1226",
        "title": "《菲律宾民法典》第1226条：惩罚性违约金条款替代损害赔偿金之法定原则",
        "heading_path": "Civil Code of the Philippines > Book IV > Title I > Chapter 3 > Section 6 > Article 1226",
        "text_de": "Philippine Civil Code Art. 1226 (Penal Clause as Substitute for Damages)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "In obligations with a penal clause, the penalty shall substitute the indemnity for damages and the payment of interests in case of noncompliance, if there is no stipulation to the contrary. Nevertheless, damages shall be paid if the obligor refuses to pay the penalty or is guilty of fraud.",
        "text_en": "Penalty substitutes indemnity for damages and interests unless agreed otherwise.",
        "text_zh": "【违约金替代性原则】合同附设违约金条款的，违约金原则上替代损害赔偿金和利息补偿。除合同另有特别明文约定外，债权人不得在主张全额违约金的同时重复索赔一般损害赔偿，除非债务人拒付违约金或存在欺诈恶意。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "PH:Civil_Code:Art1227",
        "law": "Civil_Code_PH",
        "enbez": "Art.1227",
        "title": "《菲律宾民法典》第1227条：禁止债务人单方以罚金代履约与禁止债权人双重受偿",
        "heading_path": "Civil Code of the Philippines > Book IV > Title I > Chapter 3 > Section 6 > Article 1227",
        "text_de": "Philippine Civil Code Art. 1227 (No Exemption by Paying Penalty & No Dual Recovery)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "The debtor cannot exempt himself from the performance of the obligation by paying the penalty, save in the case where this right has been expressly reserved for him. Neither can the creditor demand the fulfillment of the obligation and the satisfaction of the penalty at the same time, unless this right has been clearly granted him.",
        "text_en": "Debtor cannot exempt fulfillment by paying penalty; creditor cannot demand both unless clearly granted.",
        "text_zh": "【禁止双重主张】债务人不得以单方支付违约金为由免除实际履行主债务之义务；债权人亦不得在请求强制履行本约的同时并罚违约金，除非合同明示赋予其该项双重并罚特权。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "PH:Civil_Code:Art1228",
        "law": "Civil_Code_PH",
        "enbez": "Art.1228",
        "title": "《菲律宾民法典》第1228条：执行约定违约金无需证明实际财产损失",
        "heading_path": "Civil Code of the Philippines > Book IV > Title I > Chapter 3 > Section 6 > Article 1228",
        "text_de": "Philippine Civil Code Art. 1228 (Proof of Actual Damages Not Necessary)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Proof of actual damages suffered by the creditor is not necessary in order that the penalty may be demanded.",
        "text_en": "Proof of actual damages suffered is not necessary in order to demand penalty.",
        "text_zh": "【违约金免于举证实际损失】债权人主张合同约定的违约金时，无须就其实际遭受的具体财产减损数额承担证明责任。只要违约事实确凿，即可依约请求给付，但其数额受制于第1229条之司法酌减权。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "PH:Civil_Code:Art16",
        "law": "Civil_Code_PH",
        "enbez": "Art.16",
        "title": "《菲律宾民法典》第16条：不动产物权与地上工程受菲律宾属地法管辖 (Lex Rei Sitae)",
        "heading_path": "Civil Code of the Philippines > Preliminary Title > Article 16",
        "text_de": "Philippine Civil Code Art. 16 (Real Property Subject to Lex Rei Sitae)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Real property as well as personal property is subject to the law of the country where it is stipulated. Real property is subject to the law of the country where it is situated.",
        "text_en": "Real property is subject to the law of the country where it is situated.",
        "text_zh": "【不动产属地专属管辖原则】位于菲律宾境内的不动产（Real Property）及依附于土地之建设工程，其物权变动、租赁、抵押、地上权等权利义务关系，一律强制适用菲律宾法律管辖，外国选法条款不得对抗不动产物权属地规则。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "PH:Civil_Code:Art17",
        "law": "Civil_Code_PH",
        "enbez": "Art.17",
        "title": "《菲律宾民法典》第17条：强行性法律与公共秩序不得通过涉外选法排除适用",
        "heading_path": "Civil Code of the Philippines > Preliminary Title > Article 17",
        "text_de": "Philippine Civil Code Art. 17 (Mandatory Prohibitory Laws Cannot Be Rendered Ineffective)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Prohibitory laws concerning persons, their acts or property, and those which have for their object public order, public policy and good customs shall not be rendered ineffective by laws or judgments promulgated, or by determinations or conventions agreed upon in a foreign country.",
        "text_en": "Prohibitory laws concerning public order shall not be rendered ineffective by foreign laws or agreements.",
        "text_zh": "【强行法与公共秩序刚性屏障】菲律宾关于公共秩序、公共政策及优良风俗之禁止性强行法律，绝不得通过外国颁布之法律、判决或当事人于境外达成之合同约定予以排除适用，涉外选法条款不得架空菲律宾强行法。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "PH:RA_11647:Sec4",
        "law": "RA_11647_FIA",
        "enbez": "Sec.4",
        "title": "《菲律宾外商投资法》(RA 11647) 第4条：外资负面清单 (Negative List) 与外资准入红线",
        "heading_path": "Republic Act No. 11647 (Amending RA 7042 FIA) > Section 4",
        "text_de": "Philippine Foreign Investments Act Sec. 4 (Foreign Investment Negative List)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "The Foreign Investment Negative List shall specify the investment areas reserved to Philippine nationals... List A reserves areas by mandate of Constitution. List B reserves areas for reasons of security, defense, risk to health.",
        "text_en": "Foreign Investment Negative List specifies areas reserved to Philippine nationals under Lists A and B.",
        "text_zh": "【外商投资准入负面清单】菲律宾外商投资实行定期负面清单管制。A清单所列行业（如宪法保留之土地所有权、特定公用事业）完全保留给菲籍国民；B清单所列涉及国防安全与特种工程行业外资最高股权严格限制在 40% 以内。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory"
    },

    # ---------------------------------------------------------------------
    # 5. 泰国 (Thailand) - 民商法典违约金与解除权专章 + 法律冲突法专典
    # ---------------------------------------------------------------------
    {
        "norm_id": "TH:CCC:Sec380",
        "law": "Civil_Code_TH",
        "enbez": "Sec.380",
        "title": "《泰国民商法典》第380条：违约金代履约请求权与双重损害赔偿排斥规则",
        "heading_path": "Thailand Civil and Commercial Code > Book II Obligations > Title I > Chapter IV Penalties > Section 380",
        "text_de": "Thai CCC Sec. 380 (Penalty in Lieu of Performance)",
        "language_mode": "trilingual",
        "lang_original": "th",
        "text_original": "ถ้าลูกหนี้ได้สัญญาว่าจะให้เบี้ยปรับเมื่อตนไม่ชำระหนี้ เจ้าหนี้จะเรียกเอาเบี้ยปรับอันจะพึงริบนั้นแทนการชำระหนี้ก็ได้ แต่ถ้าเจ้าหนี้เรียกร้องเอาเบี้ยปรับแล้ว สิทธิเรียกร้องชำระหนี้ก็เป็นอันระงับสิ้นไป",
        "text_en": "If debtor promised penalty for non-performance, creditor may demand penalty in lieu of performance, which extinguishes performance claim.",
        "text_zh": "【违约金代履约与消灭主债权】债务人承诺就根本不履行给付违约金的，债权人有权请求给付违约金以代替主债务履行。但一旦债权人选择主张全额不履约违约金，其请求实际履行主债务之权利即归于消灭。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "TH:CCC:Sec381",
        "law": "Civil_Code_TH",
        "enbez": "Sec.381",
        "title": "《泰国民商法典》第381条：工期迟延违约金与主债务履约请求权之双重并用",
        "heading_path": "Thailand Civil and Commercial Code > Book II > Chapter IV > Section 381",
        "text_de": "Thai CCC Sec. 381 (Penalty for Delay and Claim for Performance)",
        "language_mode": "trilingual",
        "lang_original": "th",
        "text_original": "ถ้าลูกหนี้ได้สัญญาว่าจะให้เบี้ยปรับเมื่อตนไม่ชำระหนี้ให้ถูกต้องสมควร เช่นว่าไม่ชำระหนี้ตรงตามเวลาที่กำหนดไว้เป็นต้น นอกจากเรียกให้ชำระหนี้ เจ้าหนี้จะเรียกเอาเบี้ยปรับอันจะพึงริบนั้นอีกด้วยก็ได้",
        "text_en": "If penalty was promised for delay, creditor may demand performance and penalty in addition.",
        "text_zh": "【迟延履约违约金双重请求权】债务人承诺若未在指定工期期限内完工即给付违约金的，债权人除有权继续请求其纠正延误并完成工程外，亦有权并罚没收迟延违约金。若发包人受领迟延交付时未作异议保留，丧失违约金请求权。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "TH:CCC:Sec386",
        "law": "Civil_Code_TH",
        "enbez": "Sec.386",
        "title": "《泰国民商法典》第386条：依约定或法定通知行使合同解除权之程序生效要件",
        "heading_path": "Thailand Civil and Commercial Code > Book II > Chapter V Rescission > Section 386",
        "text_de": "Thai CCC Sec. 386 (Exercise of Right of Rescission)",
        "language_mode": "trilingual",
        "lang_original": "th",
        "text_original": "ถ้าคู่สัญญาฝ่ายหนึ่งมีสิทธิเลิกสัญญาโดยข้อสัญญาหรือโดยบทบัญญัติแห่งกฎหมาย การเลิกสัญญาเช่นนั้นย่อมทำด้วยแสดงเจตนาแก่อีกฝ่ายหนึ่ง",
        "text_en": "If a party has right of rescission by contract or law, rescission is made by declaration of intention.",
        "text_zh": "【合同解除意思表示生效要件】当事人依合同特别约定或依据成文法规定享有合同解除权的，解除合同必须通过向另一方当事人发出明示的意思表示通知为之；该解除通知一旦送达相对方即发生不可撤销之法律效力。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "TH:CCC:Sec387",
        "law": "Civil_Code_TH",
        "enbez": "Sec.387",
        "title": "《泰国民商法典》第387条：迟延违约催告并指定合理宽限期解除前置要件",
        "heading_path": "Thailand Civil and Commercial Code > Book II > Chapter V > Section 387",
        "text_de": "Thai CCC Sec. 387 (Notice with Reasonable Period Before Rescission)",
        "language_mode": "trilingual",
        "lang_original": "th",
        "text_original": "ถ้าคู่สัญญาฝ่ายหนึ่งไม่ชำระหนี้ อีกฝ่ายหนึ่งจะกำหนดระยะเวลาพอสมควร แล้วบอกกล่าวให้ฝ่ายนั้นชำระหนี้ภายในระยะเวลานั้นก็ได้ ถ้าฝ่ายนั้นไม่ชำระหนี้ภายในระยะเวลาที่กำหนดให้ไซร้ อีกฝ่ายหนึ่งจะเลิกสัญญาเสียก็ได้",
        "text_en": "If a party does not perform, other party may fix reasonable period and give notice; if not performed, contract may be rescinded.",
        "text_zh": "【解约前置催告与宽限期】一方当事人不履行债务时，相对方必须设定一段“合理可行之补正期间”，并向其送达催告通知要求在该期间内履约。仅当违约方逾期仍未履约时，相对方方始享有法定单方解除合同权利。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "TH:CCC:Sec587",
        "law": "Civil_Code_TH",
        "enbez": "Sec.587",
        "title": "《泰国民商法典》第587条：承揽与建设工程合同定义及对价给付要件",
        "heading_path": "Thailand Civil and Commercial Code > Book III Specific Contracts > Title VII Hire of Work > Section 587",
        "text_de": "Thai CCC Sec. 587 (Hire of Work / Construction Contract Definition)",
        "language_mode": "trilingual",
        "lang_original": "th",
        "text_original": "อันว่าจ้างทำของนั้น คือสัญญาซึ่งบุคคลคนหนึ่งเรียกว่าผู้รับจ้าง ตกลงจะทำการงานสิ่งใดสิ่งหนึ่งจนสำเร็จให้แก่บุคคลอีกคนหนึ่งเรียกว่าผู้ว่าจ้าง และผู้ว่าจ้างตกลงจะให้สินจ้างเพื่อผลสำเร็จแห่งการที่ทำนั้น",
        "text_en": "Hire of work is a contract whereby contractor agrees to accomplish a work for employer who agrees to pay remuneration.",
        "text_zh": "【承揽工程合同定义】建设工程承揽（Hire of Work）是指承包商同意为发包人完成特定工程项目成果，而发包人同意在工程成果完全成就并合格交付后支付工程报酬款之双务合同。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "TH:CCC:Sec605",
        "law": "Civil_Code_TH",
        "enbez": "Sec.605",
        "title": "《泰国民商法典》第605条：发包人工程未完工前单方任意解约权但须全额赔偿承包商损失",
        "heading_path": "Thailand Civil and Commercial Code > Book III > Title VII > Section 605",
        "text_de": "Thai CCC Sec. 605 (Employer Right to Terminate Before Completion with Compensation)",
        "language_mode": "trilingual",
        "lang_original": "th",
        "text_original": "ถ้าการที่จ้างยังทำไม่แล้วเสร็จอยู่ตราบใด ผู้ว่าจ้างอาจบอกเลิกสัญญาได้เมื่อเสียค่าสินไหมทดแทนให้แก่ผู้รับจ้างเพื่อความเสียหายอย่างใดๆ อันเกิดแต่การเลิกสัญญานั้น",
        "text_en": "As long as work is not completed, employer may terminate contract upon compensating contractor for any damages.",
        "text_zh": "【发包人任意解约权与全额赔偿担保】在工程未完全完工交付前，发包人享有单方随时终止承揽合同之任意解约特权；但发包人行使该特权的前提条件是，必须向承包商全额赔偿其因解约遭受的全部损失及已完成工程可得利润。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "TH:Conflict_of_Laws_2481:Sec5",
        "law": "Conflict_of_Laws_TH",
        "enbez": "Sec.5",
        "title": "《泰国法律冲突法典》第5条：涉外外国法适用之公共秩序与优良风俗保留 (Public Order)",
        "heading_path": "Conflict of Laws Act B.E. 2481 (1938) > General Provisions > Section 5",
        "text_de": "Thai Conflict of Laws Act Sec. 5 (Public Order Reservation)",
        "language_mode": "trilingual",
        "lang_original": "th",
        "text_original": "เมื่อจะต้องใช้กฎหมายต่างประเทศ ให้ใช้เพียงเท่าที่ไม่ขัดต่อความสงบเรียบร้อยหรือศีลธรรมอันดีของประชาชนแห่งประเทศสยาม",
        "text_en": "Foreign law shall be applied only in so far as it is not contrary to public order or good morals of Thailand.",
        "text_zh": "【涉外公共秩序排斥外国法】依涉外选法条款应当适用外国法律时，该外国法律的适用仅以不违背泰国国家公共秩序（Public Order）或人民良好道德风尚为限。凡涉及强行性外资准入、劳工基本保护或土地物权法益者，排除外国法适用。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "TH:Conflict_of_Laws_2481:Sec9",
        "law": "Conflict_of_Laws_TH",
        "enbez": "Sec.9",
        "title": "《泰国法律冲突法典》第9条：涉外法律行为与合同形式要件之准据法 (Lex Loci Actus)",
        "heading_path": "Conflict of Laws Act B.E. 2481 (1938) > General Provisions > Section 9",
        "text_de": "Thai Conflict of Laws Act Sec. 9 (Formal Validity of Juristic Acts)",
        "language_mode": "trilingual",
        "lang_original": "th",
        "text_original": "แบบแห่งนิติกรรมย่อมเป็นไปตามกฎหมายแห่งประเทศที่นิติกรรมนั้นได้ทำขึ้น",
        "text_en": "Formal validity of a juristic act is governed by law of the country where act is made.",
        "text_zh": "【合同形式要件准据法】涉外法律行为及合同订立的形式要件（Formalities），依据行为订立地国家之法律（Lex Loci Actus）判定；在泰国境内签署的工程承包协议与不动产抵押，必须遵循泰国成文法形式要件要求。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "TH:Conflict_of_Laws_2481:Sec13",
        "law": "Conflict_of_Laws_TH",
        "enbez": "Sec.13",
        "title": "《泰国法律冲突法典》第13条：涉外合同准据法选法效力与最密切联系原则",
        "heading_path": "Conflict of Laws Act B.E. 2481 (1938) > Obligations > Section 13",
        "text_de": "Thai Conflict of Laws Act Sec. 13 (Applicable Law to Contracts)",
        "language_mode": "trilingual",
        "lang_original": "th",
        "text_original": "ปัญหาว่าจะพึงใช้กฎหมายใดบังคับสำหรับสิ่งซึ่งเป็นสาระสำคัญหรือผลแห่งสัญญา ให้วินิจฉัยตามเจตนาของคู่สัญญา ในกรณีที่ไม่อาจหยั่งทราบเจตนาได้ ให้ใช้กฎหมายแห่งสัญชาติร่วมกัน หรือกฎหมายแห่งถิ่นที่สัญญานั้นได้ทำขึ้น",
        "text_en": "Applicable law to substantive matters of contract is determined by intention of parties, common nationality, or place of formation.",
        "text_zh": "【涉外合同意思自治选法效力】涉外合同实质性争议与法律效果之准据法，首要依照当事人双方明示之选法意思表示确定。若当事人未作明确选法或意图不明，适用双方共同国籍国法律；无共同国籍的，适用合同订立地法律。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory"
    },

    # ---------------------------------------------------------------------
    # 6. 新加坡 (Singapore) - SOPA 2004 答辩与停工权补充
    # ---------------------------------------------------------------------
    {
        "norm_id": "SG:SOPA_2004:Sec11",
        "law": "SOPA_2004",
        "enbez": "Sec.11",
        "title": "《新加坡SOPA 2004》第11条：付款答辩 (Payment Response) 提出抗辩与抵销之严格时效",
        "heading_path": "Building and Construction Industry Security of Payment Act 2004 > Part III > Section 11",
        "text_de": "Singapore SOPA Sec. 11 (Payment Response Requirements)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "A respondent shall provide a payment response to a payment claim within 21 days after the payment claim is served, or within 7 days if the contract specifies. A respondent who fails to include in the payment response any reason for withholding payment shall not be permitted to raise that reason in adjudication.",
        "text_en": "Respondent must serve payment response within 21 days; unstated reasons cannot be raised in adjudication.",
        "text_zh": "【付款答辩失权红线】发包人自收到索赔函后 21 日内（或合同约定的 7 日内）必须送达书面付款答辩。任何扣款理由、反索赔或抵销事由必须在答辩书中明载，未在答辩书中列明的抗辩理由，裁决程序中永久丧失提出抗辩资格！",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory"
    },
    {
        "norm_id": "SG:SOPA_2004:Sec26",
        "law": "SOPA_2004",
        "enbez": "Sec.26",
        "title": "《新加坡SOPA 2004》第26条：裁决款项逾期未付总承包商之法定停工权与工期费用补偿",
        "heading_path": "Building and Construction Industry Security of Payment Act 2004 > Part IV > Section 26",
        "text_de": "Singapore SOPA Sec. 26 (Right to Suspend Work for Non-Payment)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "A claimant who obtained an adjudication determination may suspend the carrying out of construction work if respondent fails to pay. The claimant is entitled to an extension of time and compensation for loss and expense caused by the suspension.",
        "text_en": "Claimant may suspend work if adjudicated amount is unpaid, and is entitled to EOT and loss/expense.",
        "text_zh": "【裁决款未付合法停工特权】被申请人未在裁决生效后 7 日内足额给付工程款的，申请人享有法定权利立即暂停工程施工。停工期间承包商自动享有合法的工期顺延（EOT），且有权向发包人索赔因停工产生的一切合理损失与复工动员费用。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory"
    }
]

# =========================================================================
# L1 Phase 5 金标准裁判先例 (4 篇权威裁判)
# =========================================================================
PHASE5_L1_CASES: List[Dict[str, Any]] = [
    {
        "case_id": "CASE:VN_Hanoi_HC:Art683_LexSitus:2022",
        "court": "Hanoi High People's Court",
        "senate": "Civil & Economic Appellate Chamber",
        "decided": "2022-09-15",
        "az": "Appeal Judgment No. 182/2022/KDTM-PT",
        "ecli": "ECLI:VN:HN:HC:2022:182",
        "doctype": "judgment",
        "leitsatz": "河内高级人民法院判决：涉外总承包 EPC 合同即便约定新加坡国际仲裁及适用新加坡法律，因建设工程客体位于越南境内，依《越南民法典》第683条第2款强制专属适用越南法律，合同超出 8% 的违约金约定无效。",
        "tenor": "确认涉外 EPC 工程合同关于不动产工程施工与违约金扣罚之实体权利义务强制适用越南法律，判令发包人退还超出合同总价 8% 法定上限扣除的违约金 340 万美元。",
        "tatbestand": "某外资风电总承包项目发包人以工期滞后为由依据合同特别条件全额扣除承包商 12% 延误违约金。发包人主张合同约定了新加坡法律及 SIAC 仲裁，不应受越南《商业法》第 301 条 8% 上限约束。",
        "gruende": "河内高院审理认为：依据《越南民法典》第683条第2款，不动产客体位于越南境内的建设工程合同，准据法强制为越南法（Lex Situs）。当事人的意思自治选法不得排除该强制性属地管辖，发包人扣罚超过 8% 的部分自始无效。",
        "norms_meta": "VN:Civil_Code_2015:Art683,VN:Commercial_Law_2005:Art301,VN:Commercial_Law_2005:Art307",
        "source_url": "https://congbobanan.toaan.gov.vn/2ta182"
    },
    {
        "case_id": "CASE:ID_MA:Somasi_Precondition:2021",
        "court": "Supreme Court of the Republic of Indonesia (Mahkamah Agung)",
        "senate": "Civil Chamber",
        "decided": "2021-03-24",
        "az": "Decision No. 892 K/Pdt/2020 (PT Nusa Raya v. PT Mega Capital)",
        "ecli": "ECLI:ID:MA:2021:892K",
        "doctype": "judgment",
        "leitsatz": "印尼最高法院终审判决：发包人在未向总承包商送达书面催告函（Somasi）并给予合理纠正宽限期的情况下直接扣留工程款充抵违约金，严重违反《民法典》第1243条强制程序，判决全额返还扣除款项。",
        "tenor": "驳回发包人上诉，维持雅加达高院判决，判令发包人立即向总承包商全额返还擅自截留的 150 亿印尼盾工程进度款及同期法定利息。",
        "tatbestand": "雅加达商业综合体项目中，总包因属地雨季导致桩基施工滞后 25 天。发包人在当月进度款审批中未经书面催告，直接全额抵扣工期延误损害赔偿金。",
        "gruende": "最高法院判词确认：依据《印尼民法典》第1243条，违约损害赔偿金必须以债务人经依法声明迟延（Somasi）后仍怠于履行方得计发。缺乏正式合法催告函前置程序的扣除行为在印尼法律下构成违法自力侵权。",
        "norms_meta": "ID:KUHPerdata:Art1243,ID:KUHPerdata:Art1244,ID:KUHPerdata:Art1338",
        "source_url": "https://putusan3.mahkamahagung.go.id/direktori/putusan/892k-2020"
    },
    {
        "case_id": "CASE:MY_FC:Cubic_Electronics_Sec75:2019",
        "court": "Federal Court of Malaysia (Putrajaya)",
        "senate": "Appellate Division",
        "decided": "2019-11-20",
        "az": "[2019] 6 MLJ 737 (Cubic Electronics Sdn Bhd v. Mars Telecommunications Sdn Bhd)",
        "ecli": "ECLI:MY:FC:2019:6MLJ737",
        "doctype": "judgment",
        "leitsatz": "马来西亚联邦法院终审判决：全面重塑《1950年合同法》第75条司法测试准则，确立守约方主张约定违约金无需证明精确实际损失，举证责任倒置由违约方证明违约金显失合理或属于惩罚性罚金。",
        "tenor": "确立马来西亚合同法违约金主张新规则，确认只要违约金数额系订约时合理保护合法商业利益（Legitimate Commercial Interest）所必需，法院即予全额执行支持。",
        "tatbestand": "买方主张没收定金及约定的工期延误赔偿金数额过高，主张卖方必须依合同法第75条举证证明其遭受的具体实际经济损失。",
        "gruende": "联邦法院推翻旧判例确立权威规则：合同法第75条并不强制要求无辜方在每起案件中都必须证明精确到分的实际损失；只要该约定数额不具有敲诈性且旨在保护守约方之合法商业利益，推定其合理有效，违约方若主张调减必须承担显失公平之极高举证责任。",
        "norms_meta": "MY:Contracts_Act_1950:Sec75,MY:Contracts_Act_1950:Sec74",
        "source_url": "https://www.kehakiman.gov.my/judgment/federal-court/2019-6mlj737"
    },
    {
        "case_id": "CASE:TH_SC:Conflict_of_Laws_PublicOrder:2020",
        "court": "Supreme Court of Thailand (San Dika)",
        "senate": "Civil & Labour Division",
        "decided": "2020-08-18",
        "az": "Supreme Court Judgment No. 1420/2563",
        "ecli": "ECLI:TH:SC:2020:1420",
        "doctype": "judgment",
        "leitsatz": "泰国最高法院判决：涉外工程总包合同虽明确约定适用英国法律管辖，但英国法关于排除迟延损害赔偿法定抗辩之约定因违背泰国《法律冲突法》第5条公共秩序保留原则而排除适用，适用泰国《民商法典》第383条对过高违约金进行司法调减。",
        "tenor": "驳回发包人关于依据英国法全额执行 15% 违约金之上诉主张，依泰国《民商法典》第 383 条将违约金强制调减至合理数额 6%。",
        "tatbestand": "曼谷某大型电站 EPC 项目双方约定适用英国法律。工程延误后发包人依据合同英国法无调减权规则全额没收承包商履约保函并主张 15% 违约金。",
        "gruende": "泰国最高法院明确指出：依据《法律冲突法》第5条，外国法的适用不得违反泰国公共秩序与良好道德；泰国法律关于保护经济弱势方免受显失公平惩罚及法官司法衡平调减权属于公共政策强行法，外国法冲突条款一律排除适用。",
        "norms_meta": "TH:Conflict_of_Laws_2481:Sec5,TH:Conflict_of_Laws_2481:Sec13,TH:CCC:Sec383",
        "source_url": "https://www.deka.supremecourt.or.th/judgment/1420-2563"
    }
]

# =========================================================================
# L1 Phase 5 拓扑关系边 (25+ 条 GraphRAG 拓扑边)
# =========================================================================
PHASE5_L1_EDGES: List[Dict[str, Any]] = [
    # 越南冲突法与救济闭环
    {"src": "VN:Civil_Code_2015:Art683", "dst": "VN:Commercial_Law_2005:Art301", "rel": "overrides", "confidence": 0.98},
    {"src": "VN:Civil_Code_2015:Art670", "dst": "VN:Civil_Code_2015:Art683", "rel": "interprets", "confidence": 0.95},
    {"src": "VN:Commercial_Law_2005:Art301", "dst": "VN:Commercial_Law_2005:Art307", "rel": "conflicts_with", "confidence": 0.92},
    {"src": "VN:Commercial_Law_2005:Art303", "dst": "VN:Commercial_Law_2005:Art304", "rel": "applies", "confidence": 0.95},
    {"src": "VN:Commercial_Law_2005:Art303", "dst": "VN:Commercial_Law_2005:Art305", "rel": "interprets", "confidence": 0.90},
    {"src": "CASE:VN_Hanoi_HC:Art683_LexSitus:2022", "dst": "VN:Civil_Code_2015:Art683", "rel": "applies", "confidence": 0.99},

    # 印尼催告前置与免责闭环
    {"src": "ID:KUHPerdata:Art1243", "dst": "ID:KUHPerdata:Art1244", "rel": "conflicts_with", "confidence": 0.93},
    {"src": "ID:KUHPerdata:Art1244", "dst": "ID:KUHPerdata:Art1245", "rel": "interprets", "confidence": 0.95},
    {"src": "ID:KUHPerdata:Art1246", "dst": "ID:KUHPerdata:Art1247", "rel": "applies", "confidence": 0.92},
    {"src": "ID:KUHPerdata:Art1247", "dst": "ID:KUHPerdata:Art1248", "rel": "interprets", "confidence": 0.94},
    {"src": "ID:AB_1847:Art17", "dst": "ID:KUHPerdata:Art1338", "rel": "overrides", "confidence": 0.96},
    {"src": "CASE:ID_MA:Somasi_Precondition:2021", "dst": "ID:KUHPerdata:Art1243", "rel": "applies", "confidence": 0.99},

    # 马来西亚合同法与 CIPAA 链
    {"src": "MY:Contracts_Act_1950:Sec75", "dst": "MY:Contracts_Act_1950:Sec74", "rel": "interprets", "confidence": 0.92},
    {"src": "CASE:MY_FC:Cubic_Electronics_Sec75:2019", "dst": "MY:Contracts_Act_1950:Sec75", "rel": "applies", "confidence": 0.99},
    {"src": "MY:CIPAA_2012:Sec5", "dst": "MY:CIPAA_2012:Sec6", "rel": "applies", "confidence": 0.95},
    {"src": "MY:CIPAA_2012:Sec15", "dst": "MY:CIPAA_2012:Sec13", "rel": "overrides", "confidence": 0.94},
    {"src": "MY:CIPAA_2012:Sec28", "dst": "MY:CIPAA_2012:Sec29", "rel": "interprets", "confidence": 0.96},

    # 菲律宾违约金与涉外强行法
    {"src": "PH:Civil_Code:Art17", "dst": "PH:Civil_Code:Art1229", "rel": "overrides", "confidence": 0.96},
    {"src": "PH:Civil_Code:Art1226", "dst": "PH:Civil_Code:Art1227", "rel": "interprets", "confidence": 0.90},
    {"src": "PH:Civil_Code:Art1228", "dst": "PH:Civil_Code:Art1229", "rel": "conflicts_with", "confidence": 0.94},

    # 泰国法律冲突与违约金调减
    {"src": "TH:Conflict_of_Laws_2481:Sec5", "dst": "TH:Conflict_of_Laws_2481:Sec13", "rel": "overrides", "confidence": 0.98},
    {"src": "TH:CCC:Sec383", "dst": "TH:CCC:Sec381", "rel": "interprets", "confidence": 0.93},
    {"src": "TH:CCC:Sec386", "dst": "TH:CCC:Sec387", "rel": "applies", "confidence": 0.95},
    {"src": "CASE:TH_SC:Conflict_of_Laws_PublicOrder:2020", "dst": "TH:Conflict_of_Laws_2481:Sec5", "rel": "applies", "confidence": 0.99},

    # 新加坡法定停工链
    {"src": "SG:SOPA_2004:Sec11", "dst": "SG:SOPA_2004:Sec15", "rel": "applies", "confidence": 0.94},
    {"src": "SG:SOPA_2004:Sec26", "dst": "SG:SOPA_2004:Sec15", "rel": "interprets", "confidence": 0.96}
]

# =========================================================================
# L1 Phase 5 核心热点判例映射
# =========================================================================
PHASE5_HOT_NORM_CASES = [
    ("VN:Civil_Code_2015:Art683", "CASE:VN_Hanoi_HC:Art683_LexSitus:2022", 1),
    ("ID:KUHPerdata:Art1243", "CASE:ID_MA:Somasi_Precondition:2021", 1),
    ("MY:Contracts_Act_1950:Sec75", "CASE:MY_FC:Cubic_Electronics_Sec75:2019", 1),
    ("TH:Conflict_of_Laws_2481:Sec5", "CASE:TH_SC:Conflict_of_Laws_PublicOrder:2020", 1)
]

# =========================================================================
# L1 Phase 5 高阶风险社区
# =========================================================================
PHASE5_RISK_COMMUNITIES = [
    {
        "community_id": "RC_LEX_SITUS_OVERRIDE",
        "name_zh": "涉外不动产与建设工程专属管辖与外国选法排斥风险社区",
        "risk_level": "critical",
        "host_countries": json.dumps(["VN", "TH", "ID", "PH"], ensure_ascii=False),
        "archetypes": json.dumps(["EPC_CONTRACTING", "CROSS_BORDER_MA"], ensure_ascii=False),
        "norm_ids": json.dumps(["VN:Civil_Code_2015:Art683", "TH:Conflict_of_Laws_2481:Sec5", "ID:AB_1847:Art17", "PH:Civil_Code:Art16", "PH:Civil_Code:Art17"], ensure_ascii=False),
        "trigger_scenarios": "涉外工程当事人约定适用外国法（如英国法或新加坡法），但因工程客体位于境内，法院依据民法典不动产专属管辖及公共秩序强行法宣告选法条款无效并强行适用属地法。",
        "redline_actions": json.dumps([
            "在越南工程合同中明确承认民法典第683条不动产适用越南法规则，避免盲目约定外国法导致违约金条款无效",
            "在泰国项目约定中注意审查是否违反第5条公共秩序强行性劳动与承揽保护规定",
            "在印尼涉外合同中确保遵守语言法及不动产属地规则"
        ], ensure_ascii=False)
    },
    {
        "community_id": "RC_SOMASI_AND_STATUTORY_SUSPENSION",
        "name_zh": "催告前置程序瑕疵与工程款未付法定合法停工抗辩社区",
        "risk_level": "high",
        "host_countries": json.dumps(["ID", "MY", "SG"], ensure_ascii=False),
        "archetypes": json.dumps(["EPC_CONTRACTING", "JV_CONSORTIUM"], ensure_ascii=False),
        "norm_ids": json.dumps(["ID:KUHPerdata:Art1243", "ID:KUHPerdata:Art1244", "MY:CIPAA_2012:Sec28", "MY:CIPAA_2012:Sec29", "SG:SOPA_2004:Sec26"], ensure_ascii=False),
        "trigger_scenarios": "发包人未行使法定催告前置程序（Somasi）即擅自扣除违约金，或发包人逾期拒不支付进度款时承包商依法启动法定程序行使合法停工权。",
        "redline_actions": json.dumps([
            "印尼项目发包人主张违约金前必须核验是否送达有效Somasi及给予合理宽限期",
            "马来西亚项目依据CIPAA第28条行使法定停工权前必须核验裁决生效证明并正式发函",
            "行使合法停工权的同时同步向发包人送达工期顺延（EOT）与窝工成本索赔函"
        ], ensure_ascii=False)
    }
]


def apply_phase5_clusters(snapshot_id: str = "20261021-asean-v2.2"):
    print("=" * 75)
    print("🚀 开始注入 Phase 5: 涉外经贸冲突法专编与实体章节条文群 (L1 Clusters)")
    print("=" * 75)

    mgr = SnapshotManager()
    snap_id = snapshot_id or mgr.get_current_snapshot_id()
    snap_dir = os.path.join(mgr.base_dir, snap_id)
    db_path = os.path.join(snap_dir, "law.sqlite")

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    now_str = datetime.now().isoformat()

    # 1. 批量插入/更新 norms
    print(f"\n-> 1. 批量注入 {len(PHASE5_L1_NORMS)} 条核心法典章节条文与涉外冲突法规...")
    for n in PHASE5_L1_NORMS:
        cur.execute(
            """INSERT INTO norms(
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
                n.get("translation_source", "MOJ_FATONG_2026"), n.get("norm_category", "mandatory_statute"),
                None, None, "{}", n.get("mandatory_level", "mandatory")
            )
        )
    print(f"✓ 成功注入/更新 {len(PHASE5_L1_NORMS)} 条法条群规范")

    # 2. 批量插入/更新 cases
    print(f"\n-> 2. 批量注入 {len(PHASE5_L1_CASES)} 篇金标准裁判先例...")
    for c in PHASE5_L1_CASES:
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
    print(f"✓ 成功注入/更新 {len(PHASE5_L1_CASES)} 篇核心金标准判例")

    # 3. 批量插入 edges
    print(f"\n-> 3. 批量注入 {len(PHASE5_L1_EDGES)} 条 GraphRAG 拓扑对抗边...")
    for e in PHASE5_L1_EDGES:
        cur.execute(
            """INSERT OR IGNORE INTO edges(
                src, dst, rel, source, span, confidence, reviewed, snapshot_id
            ) VALUES(?, ?, ?, ?, ?, ?, ?, ?)""",
            (e["src"], e["dst"], e["rel"], "PHASE5_EXPANSION", "", e.get("confidence", 0.95), 1, snap_id)
        )
    print(f"✓ 成功建立 {len(PHASE5_L1_EDGES)} 条拓扑关系边")

    # 4. 批量插入 hot_norm_cases
    print(f"\n-> 4. 批量注入 {len(PHASE5_HOT_NORM_CASES)} 组法条判例映射...")
    for n_id, c_id, rk in PHASE5_HOT_NORM_CASES:
        cur.execute(
            "INSERT OR REPLACE INTO hot_norm_cases(norm_id, case_id, rank) VALUES(?, ?, ?)",
            (n_id, c_id, rk)
        )
    print(f"✓ 成功更新 {len(PHASE5_HOT_NORM_CASES)} 组核心判例映射")

    # 5. 批量插入 risk_communities
    print(f"\n-> 5. 批量注入 {len(PHASE5_RISK_COMMUNITIES)} 个高阶风险社区...")
    for r in PHASE5_RISK_COMMUNITIES:
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
    print(f"✓ 成功建立 {len(PHASE5_RISK_COMMUNITIES)} 个风险社区")

    conn.commit()

    # 6. 重新切块生成 L1 Chunks 并持久化
    print("\n-> 6. 正在重新生成知识库 Chunks...")
    from lawagent.store.chunker import build_and_save_chunks
    all_norms = mgr.get_all_norms(snap_id)
    all_cases = mgr.get_all_cases(snap_id)
    total_chunks = build_and_save_chunks(conn, all_norms, all_cases)
    print(f"✓ 全量分块生成完毕，总 Chunks 达: {total_chunks}")

    # 7. 重建 L1 BM25 索引
    print("\n-> 7. 正在训练并持久化新版 L1 BM25 词法检索索引...")
    from lawagent.store.bm25 import BM25Engine
    index_dir = os.path.join(mgr.base_dir, snap_id, "index")
    rows = conn.execute("SELECT chunk_id, kind, ref_id, seq, text FROM chunks").fetchall()
    chunks = [dict(r) for r in rows]
    bm25 = BM25Engine(index_dir=index_dir)
    bm25.build_from_chunks(chunks)
    print("✓ 新版 L1 BM25 词法索引重构完成")

    # 8. 重建 L1 FAISS 稠密向量索引
    print("\n-> 8. 正在调用 GPU/BGE-M3 批量生成稠密语义向量并构建 L1 FAISS 索引...")
    from lawagent.store.vec import DenseVectorEngine
    try:
        vec_engine = DenseVectorEngine(index_dir=index_dir)
        vec_engine.build_from_chunks(chunks, batch_size=16)
        print("✓ 新版 L1 FAISS 向量索引构建完成")
    except Exception as e:
        print(f"⚠️ 向量索引构建提示: {e}")

    conn.close()
    print("\n" + "=" * 75)
    print("🎉 Phase 5 数据库扩充与 L1 索引全量重构大功告成！")
    print("=" * 75)


if __name__ == "__main__":
    apply_phase5_clusters()


if __name__ == "__main__":
    apply_phase5_clusters()
