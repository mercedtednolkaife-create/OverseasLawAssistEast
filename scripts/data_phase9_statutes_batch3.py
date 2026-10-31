# -*- coding: utf-8 -*-
"""Phase 9 阶梯式长尾法条扩充 - Batch 3 (实务域 07、08、09)
实务域 07: 物权担保、工程优先权/留置权、独立保函与项目融资
实务域 08: 跨境税务筹划、双边税收协定(DTA)、EPC拆分与外汇管制
实务域 09: 属地用工、外劳签证配额、欠薪连带责任与安全生产(HSE)
严格遵循《数据库审查.md》第五部分字段规范与 elements_json 结构化标准。
"""

import json

BATCH3_STATUTES = [
    # =========================================================================
    # 实务域 07: 物权担保、工程优先权/留置权与独立保函 (L1+L2)
    # =========================================================================
    {
        "table": "reference_norms",
        "norm_id": "ICC:URDG_758:Art15_Breach",
        "law": "ICC:URDG_758",
        "enbez": "Art 15",
        "title": "见索即付保函统一规则第15条：违约声明（Statement of Breach）必备要件",
        "heading_path": "国际商会《见索即付保函统一规则》(ICC URDG 758) > 索赔要件",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Requirements for Demand: A demand under the guarantee shall be accompanied by such other documents as the guarantee specifies, and in any event by a statement by the beneficiary indicating in what respect the applicant is in breach of its obligations under the underlying relationship. This statement may be in the demand itself or in a separate signed document.",
        "text_en": "URDG 758 Art 15 requires a demand to be accompanied by a statement by the beneficiary indicating in what respect the applicant is in breach of underlying obligations.",
        "text_zh": "【保函索兑必备违约声明要件】：根据 URDG 758 规则开立的独立保函，受益人（业主）发起索赔请求时，必须随附保函约定的其他单据，且在任何情况下，必须附具受益人出具的‘违约声明（Statement of Breach）’，具体指明被保证人（承包商）在基础法律关系中究竟在何种方面违反了何项具体合同义务；该声明可载于索赔函正文中，亦可为独立签署的文件。【实务攻防】：若业主向开立银行发起的索赔仅简短声称‘请立即支付全额保函款项’，而未具体陈述承包商何项违约或陈述前后自相矛盾，承包商可立即通知银行以‘单据表面不符（Discrepant Demand）’为由依法拒付！",
        "norm_category": "multilateral_treaty",
        "mandatory_level": "contract_default",
        "elements_json": json.dumps([
            {"eid": "e_urdg15_formal_demand", "text_zh": "要件一：受益人向开立银行提交正式书面索赔申请书并在保函有效期内送达", "status": "condition_precedent"},
            {"eid": "e_urdg15_statement_of_breach", "text_zh": "要件二：必须载明或附具指明被申请人具体基础违约事实的正式违约声明", "status": "mandatory"},
            {"eid": "e_urdg15_discrepant_refusal", "text_zh": "法律后果：缺失具体违约声明构成单据不符，银行有权在5个营业日内正式拒付", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "CN:SASAC_Notice_75_2021:Art4",
        "law": "CN:SASAC_Notice_75_2021",
        "enbez": "第4条",
        "title": "国资委75号文第4条：央企境外融资担保严禁超股比连带及无股权担保",
        "heading_path": "国务院国资委《关于加强中央企业融资担保管理工作的通知》(国资发财评规〔2021〕75号) > 担保范围与限额",
        "language_mode": "bilingual",
        "lang_original": "zh",
        "text_original": "中央企业应当严格控制融资担保规模，规范融资担保行为：严格限制对参股企业提供担保，确需提供的，应当按照持股比例提供担保，严禁超出持股比例提供担保；严禁对集团外无股权关系的企业提供任何形式的担保；严禁为控股股东、实际控制人及其关联方提供担保。",
        "text_en": "SASAC Notice 75 (2021) Art 4 strictly limits SOE financing guarantees: Guarantees for equity-participating enterprises must NOT exceed equity proportion; Guarantees for non-equity entities are STRICTLY PROHIBITED.",
        "text_zh": "【央企境外担保三大合规死线】：① 严禁对集团外无股权关系的企业提供任何形式的担保；② 对参股企业确需提供担保的，必须严格按‘持股比例’提供担保，严禁超出持股比例提供超额连带担保；③ 严禁为无实质产权控制关系的合资合作方提供兜底担保。【出海实务攻防】：在东盟承建 EPC+F 融资项目或合资建厂，外方业主和银团几乎 100% 习惯要求中方出具 100% 连带母公司担保（PCG）；中资央国企必须坚定援引国资委 75 号令作为不可退让的国资法定监管红线，坚决将母公司担保责任上限限定在中方股权比例以内，杜绝盲目签署全额连带担保！",
        "norm_category": "prc_sasac_reg",
        "mandatory_level": "mandatory_override",
        "elements_json": json.dumps([
            {"eid": "e_sasac75_guarantee_subject", "text_zh": "要件一：担保提供方属于中国国务院国资委直接监管的中央企业及所属各级子企业", "status": "condition_precedent"},
            {"eid": "e_sasac75_equity_proportion_cap", "text_zh": "要件二：审查被担保对象股权关系，对参股企业担保责任不得超出中方实缴股比", "status": "mandatory"},
            {"eid": "e_sasac75_compliance_veto", "text_zh": "法律后果：超股比担保或对无股权企业担保直接构成国资违规追责事项，具有合规否决权", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "ID:KUHPerdata:Art1139_8",
        "law": "ID:KUHPerdata",
        "enbez": "Art 1139(8)",
        "title": "印尼民法典第1139条第8款：承揽人建筑物优先特权（Hak Istimewa）",
        "heading_path": "印尼民法典 > 第三编 债权法 > 第十九章 特权 > 不动产特权优先受偿",
        "language_mode": "trilingual",
        "lang_original": "id",
        "text_original": "Piutang-piutang yang diistimewakan atas benda-benda tertentu adalah: (8) Tagihan-tagihan seorang tukang batu, tukang kayu dan buruh lainnya mengenai pembangunan atau perbaikan sebuah barang tak bergerak, namun hanya sampai seharga pertambahan harga benda tersebut.",
        "text_en": "Privileged claims on specific assets include claims of masons, carpenters, and contractors for construction or repair of immovables, limited to the increased value created.",
        "text_zh": "【承揽人建筑物法定特权优先受偿权】：对特定不动产享有法定优先特权（Hak Istimewa）的债权包括：建筑师、承包商、石匠、木匠及其他工程工人，因建造、修缮该不动产所产生的工程款债权；但该特权的行使，以该项工程活动所实际增加的不动产价值增值为限，且其预算与工程证明须依法登记。【出海实务攻防】：印尼法律下存在大陆法系典型的建设工程法定优先特权！当印尼业主资不抵债或被其他债权人查封土地时，总承包商可依据第1139条第8款向商事法院主张其施工使该宗土地厂房产生增值，从而在该增值范围内优先于普通债权人甚至受偿抵押权余额！",
        "norm_category": "statute",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_id1139_construction_claim", "text_zh": "要件一：债权系因合规承揽建造、修缮该特定不动产所产生之工程欠款", "status": "condition_precedent"},
            {"eid": "e_id1139_added_value_limit", "text_zh": "要件二：优先受偿数额严格以施工活动使该不动产所实际产生之评估增值额为限", "status": "mandatory"},
            {"eid": "e_id1139_privileged_rank", "text_zh": "法律后果：在不动产拍卖分配中依法享有优先特权受偿顺位，阻断普通破产查封", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "MY:Common_Law:No_Mechanic_Lien",
        "law": "MY:Common_Law",
        "enbez": "Common Law Principle",
        "title": "马来西亚普通法：不存在不动产法定建设工程优先受偿权判例规则",
        "heading_path": "马来西亚普通法司法先例与国家土地法典 > 建设工程物权救济边界",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Under Malaysian law and the National Land Code (Act 828), there is NO statutory mechanic's lien or construction contractor's preferential right over real property. Once unfixed building materials are fixed to the soil/structure, title automatically passes to the landowner under the maxim 'quicquid plantatur solo, solo cedit'.",
        "text_en": "Malaysian law does NOT recognize any statutory contractor's lien over land. Unfixed materials affixed to land automatically become the property of the landowner.",
        "text_zh": "【普通法系无建设工程法定优先受偿权（重大认知盲区防范）】：在马来西亚普通法与《国家土地法典》(NLC) 体系下，根本不存在类似于中国《民法典》第807条或印尼民法典第1139条那种针对业主土地或建筑物的‘法定建设工程优先受偿权（No Statutory Mechanic's Lien）’！一旦工程材料安装砌入建筑物并附着于土地，根据普通法‘附着于土地者即归土地所有’原则（Quicquid plantatur solo, solo cedit），其所有权即刻自动归于土地所有权人。【出海实务攻防】：中资法务与律师严禁产生‘停工并留置、拍卖业主土地厂房优先受偿’的母法投射幻觉；在马来西亚遭受欠款，唯一合法的快速追款通道是依据 CIPAA 2012 发起快速裁决并向高院申请强制执行，或在材料未安装固定前行使动产留置！",
        "norm_category": "golden_principle",
        "mandatory_level": "mandatory_override",
        "elements_json": json.dumps([
            {"eid": "e_my_no_lien_jurisdiction", "text_zh": "规则要旨：明确马来西亚法律不赋予承包商对土地及建筑物的法定优先受偿物权", "status": "condition_precedent"},
            {"eid": "e_my_affixation_rule", "text_zh": "法律效果：工程设备与材料一旦安装固定即自动丧失所有权归土地所有人", "status": "mandatory"},
            {"eid": "e_my_correct_remedy_cipaa", "text_zh": "实操指引：严禁非法擅自查封占有工地，必须走CIPAA快速裁决并申请法院执行令", "status": "prohibition"}
        ], ensure_ascii=False)
    },

    # =========================================================================
    # 实务域 08: 跨境税务筹划、双边税收协定(DTA)与外汇管制 (L2)
    # =========================================================================
    {
        "table": "reference_norms",
        "norm_id": "DTA:CN_ID:Art5_3_PE",
        "law": "DTA:CN_ID",
        "enbez": "Art 5(3)",
        "title": "中印尼双边税收协定第5条第3款：建筑安装工程常设机构6个月门槛",
        "heading_path": "中华人民共和国政府和印度尼西亚共和国政府避免双重征税协定 > 第5条 常设机构",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "The term 'permanent establishment' also encompasses: a building site, a construction, assembly or installation project or supervisory activities in connection therewith, but only where such site, project or activities continue for a period of more than 6 (six) months.",
        "text_en": "DTA CN-ID Art 5(3): A building site, construction or installation project constitutes a PE only if it continues for more than 6 months.",
        "text_zh": "【建筑安装工程常设机构（PE）6个月时间红线】：建筑工地、建筑、装配或安装工程，或者与此相关的监督管理活动，仅在‘该工地、工程或活动存续超过 6 个月’的情形下，方构成税收常设机构（Permanent Establishment, PE）。【实务攻防】：工期小于等于6个月的纯设备指导安装或保修技术服务，中资企业可依第5条第3款向印尼税务局（DGT）提交中国税务机关开具的《中国税收居民身份证明》，申请完全免除印尼企业所得税（PE所得税）；工期超6个月的，必须按在岸建筑PE申报最终预扣税。",
        "norm_category": "tax_treaty",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_dta_cn_id_5_pe_nature", "text_zh": "要件一：在印尼境内设立的建筑工地、设备安装、调试或工程监理咨询活动", "status": "condition_precedent"},
            {"eid": "e_dta_cn_id_5_six_month_test", "text_zh": "要件二：施工现场自开工起算持续时间严格判定是否跨越连续或累计6个月红线", "status": "mandatory"},
            {"eid": "e_dta_cn_id_5_tax_exemption_right", "text_zh": "法律后果：未满6个月依法豁免常设机构税负；跨越6个月触发东道国在岸征税权", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "DTA:CN_VN:Art7_Business_Profits",
        "law": "DTA:CN_VN",
        "enbez": "Art 7",
        "title": "中越双边税收协定第7条：营业利润归属与禁止引力原则（EPC拆分母法）",
        "heading_path": "中国-越南避免双重征税协定 > 第7条 营业利润",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "The profits of an enterprise of a Contracting State shall be taxable only in that State unless the enterprise carries on business in the other Contracting State through a permanent establishment situated therein. If the enterprise carries on business as aforesaid, the profits of the enterprise may be taxed in the other State but only so much of them as is attributable to that permanent establishment.",
        "text_en": "Profits taxable only in home state unless carrying on business via PE in the other state, and only to the extent attributable to that PE (No Force of Attraction).",
        "text_zh": "【营业利润归属与禁止引力原则（EPC总承包合同拆分国际法依据）】：缔约国一方企业的利润应仅在该国征税，除非该企业通过设在缔约国另一方的常设机构（PE）在另一方进行营业；若该企业通过常设机构进行营业，另一方仅得对‘实际归属于该常设机构的利润部分’征税！【出海实务攻防】：国际工程 EPC 拆分为《离岸供货合同（Offshore Supply）》与《在岸施工合同（Onshore Construction）》的核心法理依据！根据禁止引力原则，中国母公司在境外制造、以 CIF/FOB 交付给越南的机电设备，其利润完全归属于中国境内制造环节，越南税务局无权对离岸设备供货款按在岸PE利润强征所得税！",
        "norm_category": "tax_treaty",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_dta_cn_vn_7_pe_existence", "text_zh": "要件一：缔约国企业在东道国境内依法设有从事施工安装业务的建筑常设机构", "status": "condition_precedent"},
            {"eid": "e_dta_cn_vn_7_attributable_profits", "text_zh": "要件二：精确区分实际归属于东道国常设机构现场实施的劳务与安装工程利润", "status": "mandatory"},
            {"eid": "e_dta_cn_vn_7_offshore_exemption", "text_zh": "法律后果：离岸设备制造供货款完全归属于中国母国征税，严禁东道国强行引力征税", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "ID:PBI_17_3_2015:Art4_8_Exemption",
        "law": "ID:PBI_17_3_2015",
        "enbez": "Art 4 & 8",
        "title": "印尼央行本币令第4条与第8条：战略基础设施项目外币结算豁免后门",
        "heading_path": "印尼央行2015年第17/3/PBI/2015号规程及实施细则 > 外币使用特许豁免",
        "language_mode": "trilingual",
        "lang_original": "id",
        "text_original": "Kewajiban penggunaan Rupiah dikecualikan untuk: (a) transaksi tertentu dalam rangka pelaksanaan anggaran pendapatan dan belanja negara; (b) pembiayaan internasional; dan (c) proyek infrastruktur strategis yang dibiayai oleh pinjaman atau hibah luar negeri setelah memperoleh persetujuan Bank Indonesia.",
        "text_en": "Mandatory Rupiah use is EXEMPTED for: international financing, and strategic infrastructure projects funded by foreign loans with Bank Indonesia approval.",
        "text_zh": "【强制使用印尼盾令的重大基建豁免后门（防范误判违法关键条文）】：印尼央行第2条虽规定印尼境内交易强制使用印尼盾结算，但第4条与第8条设定了重大除外豁免机制：凡属于① 国际贸易进出口结算；② 国际银团境外贷款融资；③ 经印尼对口部委（如能矿部、公共工程部）出具立项证明、由外国贷款资助且经印尼央行（Bank Indonesia）正式批复同意的‘国家战略基础设施项目（Proyek Infrastruktur Strategis）’，可以合法使用美元或人民币计价并结算！【出海实务攻防】：若系统仅审查第2条本币令，会错误将所有中资涉外美元计价 EPC 合同判定为违法；必须结合第4条和第8条协助企业向印尼央行申请战略基建外币结算豁免批文，锁定合同外汇合法性！",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_id_pbi_strategic_project", "text_zh": "要件一：项目属于列入国家战略基建目录（PSN）或由国际银团提供跨境融资", "status": "condition_precedent"},
            {"eid": "e_id_pbi_bi_approval", "text_zh": "要件二：向印尼中央银行（Bank Indonesia）提交外币计价结算专项申请并取得批文", "status": "mandatory"},
            {"eid": "e_id_pbi_legal_forex_use", "text_zh": "法律后果：合同合法使用美元/人民币等外币计价与跨境收付，完全豁免违法制裁", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "VN:Circular_103_2014:Art11_FCT_Split",
        "law": "VN:Circular_103_2014",
        "enbez": "Art 11",
        "title": "越南外国承包商税通告第11条：合同拆分独立核定税率生死线",
        "heading_path": "越南财政部第103/2014/TT-BTC号通告 (外国承包商税规程) > 税率计算与拆分",
        "language_mode": "trilingual",
        "lang_original": "vi",
        "text_original": "Trường hợp hợp đồng nhà thầu bao gồm nhiều hoạt động kinh doanh khác nhau và xác định được giá trị từng hoạt động kinh doanh thì áp dụng tỷ lệ % để tính thuế TNDN và GTGT tương ứng cho từng hoạt động. Nếu không bóc tách được giá trị từng hoạt động thì áp dụng mức tỷ lệ cao nhất cho toàn bộ giá trị hợp đồng.",
        "text_en": "If a contract separates values of different activities (supply vs installation), specific FCT rates apply to each. If NOT separated, the highest rate applies to the ENTIRE contract value.",
        "text_zh": "【越南外国承包商税（FCT）拆分合同税率生死线】：外国总包商签署的 EPC 合同若明确将‘机械设备供货价值’与‘建筑、安装、调试劳务价值’在合同中独立列明各自金额的，税务局分别适用对应核定税率（纯离岸设备供货免增值税且仅征 1% 企业所得税 CIT；现场安装劳务征 5% VAT + 2% CIT；设计与管理咨询征 5% VAT + 5% CIT）；反之，若合同签为‘一揽子总价包干而未明确拆分各项金额’，税务局将对整份合同总金额（包含数亿美元的高价值重型设备款）统一按最高的 3%~5% VAT + 2% CIT 强行全额征税！【出海实务攻防】：总承包合同签约前必须实施《离岸供货》与《在岸施工》双合同结构或在主合同清单中进行具有审计效力的明细拆分，避免遭受千万美元级冤枉税负！",
        "norm_category": "tax_treaty",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_vn_fct_separated_values", "text_zh": "要件一：EPC合同正文及清单中将设备供货价款与在岸安装调试技术劳务费清晰拆分", "status": "condition_precedent"},
            {"eid": "e_vn_fct_itemized_invoicing", "text_zh": "要件二：开具的离岸商业发票、海关报关单与在岸增值税发票与拆分金额完全吻合", "status": "mandatory"},
            {"eid": "e_vn_fct_lower_effective_tax", "text_zh": "法律后果：纯设备供货享受1%超低核定税率，阻断税务局全额按高税率核定征税", "status": "prohibition"}
        ], ensure_ascii=False)
    },

    # =========================================================================
    # 实务域 09: 属地用工、外劳签证配额、欠薪连带与安全生产 (L1+L2)
    # =========================================================================
    {
        "table": "norms",
        "norm_id": "ID:UU_6_2011:Art122_Visa_Crime",
        "law": "ID:UU_6_2011",
        "enbez": "Art 122",
        "title": "印尼移民法第122条：持商务签证从事现场施工属刑事犯罪监禁五年",
        "heading_path": "印尼2011年第6号移民法 > 第十一章 刑事罚则 > 非法务工刑事责任",
        "language_mode": "trilingual",
        "lang_original": "id",
        "text_original": "Dipidana dengan pidana penjara paling lama 5 (lima) tahun dan pidana denda paling banyak Rp 500.000.000,00 (lima ratus juta rupiah): (a) setiap orang asing yang dengan sengaja menyalahgunakan atau melakukan kegiatan yang tidak sesuai dengan maksud dan tujuan pemberian Izin Tinggal yang diberikan kepadanya; (b) setiap orang yang menyuruh atau memberikan kesempatan kepada orang asing menyalahgunakan atau melakukan kegiatan yang tidak sesuai.",
        "text_en": "Misuse of stay permit (e.g. working on business visa) punishable by up to 5 years imprisonment and fine up to Rp 500,000,000 for both foreign national and the employer.",
        "text_zh": "【签证用途不符刑事罪责（监禁五年重罚）】：外国公民故意滥用居留许可，或从事与其所持居留许可签发目的不符的活动者，处最高 5 年有期徒刑，并处最高 5 亿印尼盾罚金；指使或为外国人提供机会实施前款违法活动的企业负责人与雇主，处以同等刑事处罚并强制驱逐出境！【出海实务攻防】：中企出海高危刑事地雷！为赶工期，部分项目部让中方工程师持商务签证（Visa Kunjungan 211A/B）甚至免签入境直接在工地爬塔吊、调试机组；一旦被印尼移民局（Imigrasi）联合突击执法，直接定性为刑事现行犯抓捕入狱并查封项目部！外派人员必须依法取得劳工部批复的 RPTKA 并申办工作签证（KITAS/C312）方可进场！",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory_override",
        "elements_json": json.dumps([
            {"eid": "e_id122_visa_misuse_act", "text_zh": "要件一：持旅游、商务访客或非工作类签证在工地现场从事技术操作与管理工作", "status": "condition_precedent"},
            {"eid": "e_id122_intentional_employment", "text_zh": "要件二：雇主或项目负责人明知外籍人员缺乏合法工作许可（KITAS）而安排上岗", "status": "mandatory"},
            {"eid": "e_id122_five_year_imprisonment", "text_zh": "法律后果：雇员与雇主面临最高5年监禁+5亿盾刑事罚款，当事人被驱逐出境并拉黑", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "MY:Employment_Act_1955:Sec33",
        "law": "MY:Employment_Act_1955",
        "enbez": "Sec 33",
        "title": "马来西亚雇佣法第33条：业主与总承包商对分包商欠薪承担法定连带垫付责任",
        "heading_path": "马来西亚1955年雇佣法 (Employment Act 1955) > 第VI部 工资给付优先与连带清偿",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Where a principal contracts with a contractor, and that contractor contracts with a subcontractor for execution of work, the principal and the contractor shall be liable jointly and severally with the subcontractor to pay any wages due to any employee employed by the subcontractor, limited to not more than 3 months wages.",
        "text_en": "Under Sec 33, the principal and main contractor are JOINTLY AND SEVERALLY LIABLE with the subcontractor for wages due to subcontractor's employees, up to 3 months wages.",
        "text_zh": "【业主与总包商对下层劳务欠薪法定连带清偿责任】：在发包人与总承包商、总承包商与各级分包商的工程承揽链条中，发包人与总承包商对任何下级分包商所雇佣工人拖欠的工资，与该分包商承担法定连带给付责任（Joint and Several Liability）；该连带责任上限为该等雇员不超过 3 个月的到期工资总额。【出海实务攻防】：在马来西亚承建项目，若本地土建分包商卷款跑路或破产，其属地劳工直接围堵工地并向劳工局投诉，劳工法官将依据第33条直接向中资总包商签发具有强制执行力的限期垫付令，总包商不得以‘工程款已超额付给分包商’为由对抗工人的连带欠薪请求权！",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory_override",
        "elements_json": json.dumps([
            {"eid": "e_my33_cascading_contract", "text_zh": "要件一：存在发包人-总承包商-专业分包商的层级工程承揽链条关系", "status": "condition_precedent"},
            {"eid": "e_my33_subcontractor_wage_default", "text_zh": "要件二：分包商拖欠其现场受雇工人的合法法定劳动报酬事实成立", "status": "mandatory"},
            {"eid": "e_my33_three_month_joint_liability", "text_zh": "法律后果：总包商必须无条件连带全额代垫最长达3个月的欠薪，事后再向下游追偿", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "TH:Labor_Protection_Act:Sec12",
        "law": "TH:Labor_Protection_Act",
        "enbez": "Sec 12",
        "title": "泰国劳动保护法第12条：分包链条各级总包商对劳工欠薪承担无限连带责任",
        "heading_path": "泰国1998年劳动保护法 (LPA B.E. 2541) > 第一章 总则 > 分包连带责任",
        "language_mode": "trilingual",
        "lang_original": "th",
        "text_original": "ในกรณีที่นายจ้างเป็นผู้รับเหมาช่วง ให้ผู้รับเหมาช่วงชั้นเหนือขึ้นไปจนถึงผู้รับเหมาขั้นต้น ร่วมรับผิดกับผู้รับเหมาช่วงซึ่งเป็นนายจ้าง ในค่าจ้าง ค่าล่วงเวลา ค่าทำงานในวันหยุด และค่าชดเชย",
        "text_en": "Where an employer is a subcontractor, all superior contractors up to the primary contractor shall be jointly liable with the subcontractor for wages, overtime, holiday pay, and severance pay.",
        "text_zh": "【分包链条层层穿透无限连带欠薪铁律】：若劳工的直接雇主属于工程分包商，则其上层的所有各级分包商乃至最顶层的首级总承包商（Primary Contractor），均必须与作为直接雇主的分包商共同承担连带给付责任；连带给付范围涵盖：法定基本工资、加班费、假日津贴及法定期满解雇遣散补偿金！【出海实务攻防】：泰国劳动保护法采取最严格的劳工倾斜保护！即便中资总包商与分包商在分包协议中约定‘分包商自行负责工人全部劳工纠纷与欠薪’，该免责约定在泰国劳动法院完全被判定为无效，劳动监察官可直接查封总承包商在泰商业银行账户用于划扣工人工资！",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory_override",
        "elements_json": json.dumps([
            {"eid": "e_th12_subcontractor_employer", "text_zh": "要件一：直接用人单位属于在建设工程现场实施具体施工任务的分包商", "status": "condition_precedent"},
            {"eid": "e_th12_unpaid_remuneration", "text_zh": "要件二：分包商拖欠工人的劳动报酬、加班费或法定法定解雇遣散费事实确凿", "status": "mandatory"},
            {"eid": "e_th12_primary_contractor_liability", "text_zh": "法律后果：链条所有上级承包商乃至首级总包商依法承担不可约定免除的连带垫付责任", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "PH:Labor_Code:Art106_Solidary",
        "law": "PH:Labor_Code",
        "enbez": "Art 106",
        "title": "菲律宾劳动法典第106条：严禁纯劳务分包及总包商直接连带雇主责任",
        "heading_path": "菲律宾劳动法典 (PD 442) > 第三编 劳动报酬条件 > 承包与分包专章",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Contractor or subcontractor: There is 'labor-only contracting' where the person supplying workers does not have substantial capital or investment in tools and equipment, and the workers recruited perform activities directly related to the principal business. Labor-only contracting is PROHIBITED. In such cases, the person or company contracting with the labor supplier shall be responsible to the workers in the same manner as if the workers were DIRECTLY EMPLOYED by such company.",
        "text_en": "Labor-only contracting is PROHIBITED. The principal contractor shall be considered the DIRECT EMPLOYER of the workers, solidarily liable for all wages and benefits.",
        "text_zh": "【严禁‘纯劳务分包’与总承包商穿透直接雇主责任】：凡提供工人的劳务承包商若缺乏‘实质性实缴资本’或未拥有施工机械工具设备，且所提供工人从事的业务与发包人的核心主营业务直接相关，法律强制判定该行为构成‘纯劳务挂靠分包（Labor-Only Contracting）’；纯劳务分包自始被公法严厉禁止！一旦被劳工部（DOLE）认定为纯劳务分包，法律直接穿透劳务公司，将该等工人直接拟制为总承包商的‘正式直接雇佣员工（Direct Regular Employees）’，总承包商必须补发全额法定社保福利并承担稳定就业解雇赔偿责任！【出海实务攻防】：在菲律宾严禁使用无施工机具的皮包劳务队，分包合同必须附具分包商合法工程施工牌照与设备清单，避免数千名劳务工人被菲劳工部穿透认定为中企直接正式员工！",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory_override",
        "elements_json": json.dumps([
            {"eid": "e_ph106_labor_only_nature", "text_zh": "要件一：劳务分包商缺乏实质性资本实力或施工设备，仅作为纯劳力提供中介", "status": "condition_precedent"},
            {"eid": "e_ph106_prohibited_arrangement", "text_zh": "要件二：工人从事之土建施工活动直接融入总承包商主要工程建造业务范畴", "status": "mandatory"},
            {"eid": "e_ph106_direct_employer_status", "text_zh": "法律后果：纯劳务分包绝对无效，总包商被法定穿透拟制为直接雇主承担无限福利责任", "status": "prohibition"}
        ], ensure_ascii=False)
    }
]
