# -*- coding: utf-8 -*-
"""
最新数据库审查方案：全面补全成文法簇 (L1 核心强行法 + L2 广覆盖参考规程)
包含印尼、越南、马来西亚、新加坡、泰国、菲律宾、中国涉外法及国际条约/本土合同范本。
"""

import json

L1_STATUTES = [
    # ---------------- 1. 印度尼西亚 (ID) ----------------
    {
        "norm_id": "ID:KUHPerdata:Art1604_1616",
        "law": "KUHPerdata",
        "enbez": "Art 1604-1616",
        "title": "承揽工程专节（Aanneming van Werk）风险分配、固定总价加价限制与10年工程法定责任",
        "country": "ID",
        "heading_path": "KUHPerdata >> Buku III Van Verbintenissen >> Bab VIIA Aanneming van Werk",
        "text_zh": "【承揽工程法定风险与固定总价调差限制】《印尼民法典》第三编第七A章承揽工程专节：承揽人包工包料的，在工程交付验收前发生毁损灭失的，损失由承揽人承担（Art 1605）；承揽合同约定固定总价（Borongan）的，承揽人不得以建材或人工成本上涨为由要求增加工程款，除非增项工程系经定作人书面同意并明确约定单价（Art 1610）；建筑物承揽人与建筑师对因地基缺陷或施工瑕疵导致的建筑物全部或部分倒塌毁损承担为期10年的法定连带保证责任（Art 1609）；定作人有权单方任意终止承揽合同，但必须赔偿承揽人因终止遭受的已发生实际支出及合理预期利润（Art 1611）。",
        "text_en": "Indonesian Civil Code (KUHPerdata) Articles 1604-1616 (Aanneming van Werk): If contractor supplies materials, loss before handover rests on contractor; in lump-sum contracts (Borongan), contractor cannot demand price escalation due to increased materials/labor costs unless additional works are approved in writing with agreed price (Art 1610); 10-year statutory liability for structural collapse (Art 1609); employer right to unilaterally terminate subject to indemnifying contractor for all incurred costs and lost profits (Art 1611).",
        "text_original": "Kitab Undang-Undang Hukum Perdata Pasal 1604-1616: Pemborongan Pekerjaan. Jika pemborong menyediakan bahan, kehancuran sebelum penyerahan ditanggungnya (Pasal 1605); Tidak boleh menuntut kenaikan harga borongan kecuali disetujui tertulis (Pasal 1610); Tanggung jawab 10 tahun atas robohnya bangunan (Pasal 1609); Pemberi kerja berhak membatalkan sepihak dengan ganti rugi biaya dan keuntungan (Pasal 1611).",
        "source_url": "https://peraturan.go.id/id/kuhperdata",
        "elements_json": json.dumps([
            {"eid": "e_borongan_lump_sum_bar", "text_zh": "固定总价合同建材人工涨价法定禁止调价抗辩及书面批准要件", "status": "mandatory"},
            {"eid": "e_ten_year_defect_liability", "text_zh": "建筑物地基与结构倒塌毁损之10年法定无过错保证责任", "status": "mandatory"},
            {"eid": "e_unilateral_termination_indemnity", "text_zh": "定作人单方任意终止合同之全额已发生成本及所失预期利润全额赔偿义务", "status": "remedy"}
        ], ensure_ascii=False)
    },
    {
        "norm_id": "ID:KUHPerdata:Art1967",
        "law": "KUHPerdata",
        "enbez": "Art 1967",
        "title": "一般债权30年法定诉讼时效与商事特别时效规则",
        "country": "ID",
        "heading_path": "KUHPerdata >> Buku IV Van Bewijs en Verjaring >> Bab VII Verjaring",
        "text_zh": "【一般民事债权30年诉讼时效】一切物权与人身债权之民事诉求，除法律另有特别短期时效规定外，均适用自权利可行使之日起算为期30年的一般诉讼时效消灭规则；期间届满后，债务人享有诉讼时效消灭抗辩权，法官不得依职权主动审查诉讼时效。",
        "text_en": "Indonesian Civil Code Article 1967: All legal claims, both in rem and in personam, are extinguished by prescription after thirty years, without the party claiming prescription being obliged to produce any title or good faith; judges shall not apply prescription ex officio.",
        "text_original": "KUHPerdata Pasal 1967: Semua tuntutan hukum, baik yang bersifat kebendaan maupun perseorangan, hapus karena lewat waktu dengan lewatnya waktu tiga puluh tahun.",
        "source_url": "https://peraturan.go.id/id/kuhperdata",
        "elements_json": json.dumps([
            {"eid": "e_general_prescription_30yr", "text_zh": "一般民事与商事债权30年最长诉讼时效要件", "status": "statutory"},
            {"eid": "e_prescription_party_assertion", "text_zh": "诉讼时效须由债务人主动抗辩且法庭不得依职权主动适用", "status": "procedural"}
        ], ensure_ascii=False)
    },
    {
        "norm_id": "ID:PP_22_2020:Art14_21",
        "law": "PP 22/2020",
        "enbez": "Art 14-21",
        "title": "建筑服务法实施细则KSO本土联合体工作量分配与SBU/SKK资质强制核验",
        "country": "ID",
        "heading_path": "Peraturan Pemerintah No. 22 Tahun 2020 jo. PP No. 14/2021",
        "text_zh": "【KSO联营体本土工作量分配与外资施工资质红线】境外建筑承包商在印尼设立代表处（BUJKA）承揽重大工程，必须与印尼本土高等级施工企业（B1/B2）组建联合运营体（KSO）；印尼本土成员在联合体中承担的实质施工技术工作量不得低于30%；承包商及其关键技术人员必须具备由 LPJK 颁发且在 OSS-RBA 系统认证的 SBU 资质证书与 SKK 执业证书；未履行对印尼籍工程师技术转让与培训义务的，面临行政警告乃至吊销执照行政处罚。",
        "text_en": "Government Regulation No. 22/2020 jo. PP 14/2021 Articles 14-21: Foreign Construction Representative Offices (BUJKA) must form Joint Operations (KSO) with Indonesian national construction companies with minimum 30% local technical participation; mandatory SBU and SKK licenses via OSS-RBA system; administrative sanctions for failure to perform mandatory technology transfer.",
        "text_original": "PP No. 22/2020 jo. PP No. 14/2021 Pasal 14-21: Kewajiban KSO bagi BUJKA dengan badan usaha jasa konstruksi nasional kualifikasi besar, porsi pekerjaan dan kewajiban sertifikasi SBU/SKK melalui OSS-RBA serta alih teknologi.",
        "source_url": "https://jdih.pu.go.id/detail-dokumen/pp/22-2020",
        "elements_json": json.dumps([
            {"eid": "e_kso_local_quota", "text_zh": "外商独资与BUJKA必须与本土企业组建KSO且本土工作量不低于法定比例", "status": "mandatory"},
            {"eid": "e_sbu_skk_verification", "text_zh": "SBU企业资质与SKK关键工程师执业证书在OSS-RBA系统强制准入", "status": "mandatory"}
        ], ensure_ascii=False)
    },
    {
        "norm_id": "ID:PP_19_2021:PSN_Land",
        "law": "PP 19/2021",
        "enbez": "Art 19-35",
        "title": "国家战略项目（PSN）加速土地征收、地点确定书与法院提存清场程序",
        "country": "ID",
        "heading_path": "Peraturan Pemerintah No. 19 Tahun 2021 jo. PP No. 39/2023",
        "text_zh": "【国家战略项目土地征收提存清场强行法】针对印尼列入国家战略项目（PSN）的交通、能源及工业园区基建，土地征收地点确定书（Penetapan Lokasi）自公布之日起具备排他物权锁定效力；土地所有权人或习惯法社区（Masyarakat Hukum Adat）对征收补偿金有异议的，必须在14日内向地方法院起诉；逾期不起诉或法院判决后仍拒不交地的，征地机构有权将补偿款向地方法院提存（Konsinyasi），提存生效之日土地权利依法归于消灭，政府有权启动强制清场与移交工程场地。",
        "text_en": "Government Regulation No. 19/2021 jo. PP 39/2023 (Land Acquisition for PSN): Penetapan Lokasi locks site rights; objections to compensation must be filed within 14 days; upon deposit of compensation into district court (Konsinyasi), ownership terminates and mandatory physical site clearance proceeds.",
        "text_original": "PP No. 19/2021 jo. PP No. 39/2023: Pengadaan Tanah bagi Pembangunan Proyek Strategis Nasional (PSN), Penetapan Lokasi, Konsinyasi ganti kerugian di Pengadilan Negeri dan pengosongan lahan.",
        "source_url": "https://peraturan.go.id/id/pp-no-19-tahun-2021",
        "elements_json": json.dumps([
            {"eid": "e_penlok_lock_in", "text_zh": "地点确定书Penetapan Lokasi确立工程用地排他建设使用权", "status": "condition_precedent"},
            {"eid": "e_konsinyasi_handover", "text_zh": "法院提存补偿金Konsinyasi直接消灭原物权并合法强制移交施工场地", "status": "mandatory"}
        ], ensure_ascii=False)
    },
    {
        "norm_id": "ID:UU_21_2023:IKN_Capital",
        "law": "UU 21/2023",
        "enbez": "Art 16A & PP 12/2023",
        "title": "2024新国都法修正案95年HGB建筑权、黄金签证与投资特区特许经营",
        "country": "ID",
        "heading_path": "UU No. 21 Tahun 2023 jo. PP No. 12 Tahun 2023",
        "text_zh": "【印尼新首都投资建设特区土地与准入特权】外国投资者在印尼新首都努山塔拉（IKN）投资关键基础设施与商业配套，可一次性获得最长达95年（首期50年+延长30年+更新15年）的建筑权（HGB）；外籍专业技术人员及高管享受10年期黄金签证（Golden Visa）待遇；对新首都先行绿色能源与公用事业投资项目，依法豁免常规工业本土化含量（TKDN）前置审查，并享有首期30年企业所得税全额豁免。",
        "text_en": "Law No. 21/2023 amending Law 3/2022 on Nusantara Capital City (IKN) & PP 12/2023: Grants up to 95 years HGB building rights, 10-year golden visas for foreign technical staff, fiscal incentives, and specific TKDN regulatory exemptions for pioneer green infrastructure investments.",
        "text_original": "UU No. 21/2023 tentang Perubahan atas UU No. 3/2022 tentang Ibu Kota Negara: Hak Atas Tanah HGB hingga 95 tahun, perizinan berusaha, insentif fiskal dan golden visa di IKN.",
        "source_url": "https://peraturan.go.id/id/uu-no-21-tahun-2023",
        "elements_json": json.dumps([
            {"eid": "e_ikn_95yr_hgb", "text_zh": "新首都特许基础设施最长95年HGB法定物权保障", "status": "statutory"},
            {"eid": "e_ikn_special_exemption", "text_zh": "先行产业外资股比及TKDN本地化含量法定特惠豁免", "status": "privilege"}
        ], ensure_ascii=False)
    },
    {
        "norm_id": "ID:PERMA_3_2023:Art6_10",
        "law": "PERMA 3/2023",
        "enbez": "Art 6-10",
        "title": "国内仲裁裁决30日电子化登记时限与可执行性形式审查",
        "country": "ID",
        "heading_path": "Peraturan Mahkamah Agung No. 3 Tahun 2023 >> Bab II Pendaftaran Putusan Arbitrase Nasional",
        "text_zh": "【印尼国内仲裁裁决电子登记法定时限】依据印尼最高法院2023年第3号规程，仲裁庭（如 BANI）作出的国内仲裁裁决书正本及当事人授权委托文件，必须自裁决公布之日起30日内，通过最高法院电子化司法系统（e-Court）向管辖地方法院完成登记提存；逾期未完成法定登记提存的，仲裁裁决丧失申请强制执行令（Fiat Eksekusi）的法律效力。",
        "text_en": "Supreme Court Regulation (PERMA) No. 3/2023 Articles 6-10: National arbitral awards must be registered electronically via e-Court with the District Court within 30 days from the date of pronouncement; failure to register within the statutory deadline invalidates enforceability.",
        "text_original": "PERMA No. 3/2023 Pasal 6-10: Pendaftaran putusan arbitrase nasional wajib dilakukan dalam jangka waktu paling lama 30 hari terhitung sejak tanggal putusan diucapkan melalui sistem peradilan elektronik.",
        "source_url": "https://peraturan.mahkamahagung.go.id/peraturan/detail/perma-3-2023",
        "elements_json": json.dumps([
            {"eid": "e_national_award_30d_reg", "text_zh": "仲裁裁决公布后30日内向管辖法院电子登记强行时限", "status": "mandatory"},
            {"eid": "e_registration_enforceability", "text_zh": "登记提存系获得执行令Fiat Eksekusi的绝对法定形式前置", "status": "condition_precedent"}
        ], ensure_ascii=False)
    },
    {
        "norm_id": "ID:PERMA_3_2023:Art16_24",
        "law": "PERMA 3/2023",
        "enbez": "Art 16-24",
        "title": "外国仲裁裁决中雅加达地院Exequatur执行许可法定审查时限与救济限制",
        "country": "ID",
        "heading_path": "Peraturan Mahkamah Agung No. 3 Tahun 2023 >> Bab III Pengakuan dan Pelaksanaan Putusan Arbitrase Internasional",
        "text_zh": "【外国仲裁裁决执行许可审查与最高院终审救济】在中雅加达地方法院申请承认与执行外国仲裁裁决（Exequatur），法院首席法官必须在收到完备申请之日起30日内作出准予或不予执行的裁定；地方法院签发执行许可的，任何当事人不得向最高法院提起上诉或抗告；仅在法院裁定驳回执行申请时，申请人才有权在14日内向印尼最高法院提起最终抗告（Kasasi）；执行审查严禁复审仲裁实体法律与事实问题。",
        "text_en": "PERMA No. 3/2023 Articles 16-24: Central Jakarta District Court Chief Judge must decide on Exequatur of international arbitral awards within 30 days; decisions granting Exequatur are final and non-appealable; only decisions refusing Exequatur may be appealed to the Supreme Court (Kasasi) within 14 days; merits of the award shall strictly not be re-examined.",
        "text_original": "PERMA No. 3/2023 Pasal 16-24: Pengakuan dan eksekusi putusan arbitrase internasional di Pengadilan Negeri Jakarta Pusat, jangka waktu 30 hari, pembatasan kasasi, dan larangan memeriksa pokok perkara.",
        "source_url": "https://peraturan.mahkamahagung.go.id/peraturan/detail/perma-3-2023",
        "elements_json": json.dumps([
            {"eid": "e_exequatur_30d_period", "text_zh": "中雅加达地院30日法定出具Exequatur审查时限", "status": "procedural"},
            {"eid": "e_merits_review_prohibition", "text_zh": "司法审查严禁进入仲裁实体与事实错误的绝对禁令", "status": "mandatory"}
        ], ensure_ascii=False)
    },

    # ---------------- 2. 越南 (VN) ----------------
    {
        "norm_id": "VN:Law_61_2024_QH15:Art12_18",
        "law": "Law 61/2024/QH15",
        "enbez": "Art 12-18",
        "title": "2024新电力法海上风电国安审查、PPA最低合约电量Qc与直接购电DPPA机制",
        "country": "VN",
        "heading_path": "Luật Điện lực số 61/2024/QH15 >> Chương II Phát triển năng lượng tái tạo",
        "text_zh": "【2024年越南新电力法新能源重大改革】越南第61/2024/QH15号《新电力法》（2025年2月1日起施行，废止2004年旧法）：海上风电项目必须经国防部、公安部国家安全事前审查与总理投资核准；燃气电站与大型新能源长期购电协议（PPA）正式确立最低合约电量（Qc）比例传导规则，为外国独立发电商（IPP）提供长周期现金流对冲；全面确立大工业用户与可再生能源发电商直接购电机制（DPPA，衔接 Decree 80/2024/ND-CP）；民间资本投资电网配套资产的可经协商有偿或无偿移交给国家电网（EVN）运营。",
        "text_en": "Law on Electricity No. 61/2024/QH15 Articles 12-18 (effective Feb 1, 2025): Mandates national security clearance for offshore wind projects; introduces statutory minimum contractual electricity volume (Qc) framework in PPAs to protect project financing; formalizes Direct Power Purchase Agreements (DPPA) mechanism; rules on transferring privately funded grid assets to EVN.",
        "text_original": "Luật số 61/2024/QH15 Luật Điện lực: Quy định về dự án điện gió ngoài khơi gắn với quốc phòng an ninh, cơ chế sản lượng điện hợp đồng tối thiểu (Qc) trong PPA dài hạn, cơ chế mua bán điện trực tiếp (DPPA) và đầu tư lưới điện.",
        "source_url": "https://thuvienphapluat.vn/van-ban/Xay-dung-Do-thi/Luat-Dien-luc-2024-61-2024-QH15-628892.aspx",
        "elements_json": json.dumps([
            {"eid": "e_offshore_wind_security_clearance", "text_zh": "海上风电与大型能源外资准入国家安全前置审查要件", "status": "mandatory"},
            {"eid": "e_ppa_qc_statutory_framework", "text_zh": "长期购电合同PPA法定最低履约结算电量Qc保障机制", "status": "statutory"}
        ], ensure_ascii=False)
    },
    {
        "norm_id": "VN:Resolution_01_2019_NQ_HDTP:Interest",
        "law": "Resolution 01/2019/NQ-HĐTP",
        "enbez": "Art 2-7",
        "title": "借款与商事工程拖欠工程款利息计算公式、复利禁令及判决执行阶段起算规则",
        "country": "VN",
        "heading_path": "Nghị quyết số 01/2019/NQ-HĐTP của Hội đồng Thẩm phán TANDTC",
        "text_zh": "【工程欠款利息与复利绝对禁止司法解释】越南最高人民法院法官委员会第01/2019号司法解释决议：商事合同当事人未按期支付工程款的，守约方有权依据《商事法》第306条要求按违约时逾期一般借款平均利率主张利息；若合同既约定了违约金又主张逾期利息，法庭在法定上限内予以合并支持；但严厉禁止在逾期利息之上重复计收复利（Compound Interest）；在民事诉讼判决生效后进入执行程序阶段，债务人未清偿的，自申请执行日起按年利率10%（或民法典第468条第2款规定标准）持续计收执行迟延履行利息。",
        "text_en": "Resolution No. 01/2019/NQ-HĐTP: Governs statutory interest computation for overdue commercial construction payments; applies Commercial Law Art 306 average overdue lending rate; strictly prohibits compound interest on unpaid interest; defines statutory late judgment execution interest under Civil Code Art 468.",
        "text_original": "Nghị quyết số 01/2019/NQ-HĐTP: Hướng dẫn áp dụng một số quy định của pháp luật về lãi, lãi suất, phạt vi phạm trong hợp đồng thương mại, cấm tính lãi mẹ đẻ lãi con, và lãi suất chậm thi hành án.",
        "source_url": "https://congbobanan.toaan.gov.vn",
        "elements_json": json.dumps([
            {"eid": "e_commercial_interest_rate_cap", "text_zh": "商业法第306条逾期付款利息参照平均银行借款利率计算", "status": "statutory"},
            {"eid": "e_compound_interest_prohibition", "text_zh": "禁止对利息计收复利的绝对强制法公序良俗规则", "status": "mandatory"}
        ], ensure_ascii=False)
    },
    {
        "norm_id": "VN:Resolution_01_2014_NQ_HDTP:Art14",
        "law": "Resolution 01/2014/NQ-HĐTP",
        "enbez": "Art 14",
        "title": "商事仲裁撤裁审查何谓“违反越南法律基本原则”及保函止付紧急保全规则",
        "country": "VN",
        "heading_path": "Nghị quyết số 01/2014/NQ-HĐTP của Hội đồng Thẩm phán TANDTC",
        "text_zh": "【涉外仲裁撤裁公共秩序与临时保全司法指导】越南最高人民法院法官委员会第01/2014号决议第14条严格限缩撤销商事仲裁裁决的事由：仅当仲裁裁决违背了越南确立和实施法律的基本社会公共准则与宪法性核心原则时，方构成‘违反越南法律基本原则’；地方法院严禁以仲裁庭认定事实不清或适用法律不当为由复审实体；地方法院可依据仲裁庭请求签发针对银行见索即付保函的紧急临时保全令（Biện pháp khẩn cấp tạm thời）。",
        "text_en": "Resolution No. 01/2014/NQ-HĐTP Article 14: Narrowly defines 'breach of fundamental principles of Vietnamese law' as grounds for setting aside arbitral awards; prohibits courts from reviewing substantive merits of arbitral awards; governs court interim measures over performance guarantees upon arbitral request.",
        "text_original": "Nghị quyết số 01/2014/NQ-HĐTP Điều 14: Hướng dẫn thế nào là phán quyết trọng tài trái với các nguyên tắc cơ bản của pháp luật Việt Nam và áp dụng biện pháp khẩn cấp tạm thời.",
        "source_url": "https://congbobanan.toaan.gov.vn",
        "elements_json": json.dumps([
            {"eid": "e_narrow_public_policy_annulment", "text_zh": "撤销商事仲裁裁决公共秩序保留的极度限缩审查标准", "status": "statutory"},
            {"eid": "e_interim_injunction_guarantee", "text_zh": "法院应仲裁庭申请签发独立保函止付临时保全裁定权", "status": "remedy"}
        ], ensure_ascii=False)
    },
    {
        "norm_id": "VN:Law_29_2023_QH15:Art23_25",
        "law": "Law 29/2023/QH15",
        "enbez": "Art 23-25",
        "title": "2023新不动产经营法外资产业园预售款最高50%与银行保函强制担保",
        "country": "VN",
        "heading_path": "Luật Kinh doanh bất động sản số 29/2023/QH15 >> Chương II Kinh doanh nhà ở, công trình xây dựng hình thành trong tương lai",
        "text_zh": "【外资工业地产与综合体期房预售限制】越南第29/2023/QH15号《不动产经营法》（2024年8月1日起施行）：外资房地产与产业园开发商在未向买受人正式交接厂房或房屋前，累计收取预售款总额不得超过合同总金额的50%；开发商销售未来形成的建设工程，必须有具备资格的商业银行出具关于开发商交房履约义务的担保保函（Bảo lãnh nhà ở hình thành trong tương lai）；未取得施工许可与基础工程验收合格证明前严禁以认筹、预订金形式变相违规融资。",
        "text_en": "Law on Real Estate Business No. 29/2023/QH15 Articles 23-25: Foreign-invested real estate developers shall not collect more than 50% of contract value prior to physical handover of off-plan industrial or commercial properties; mandatory bank guarantees to secure completion obligations.",
        "text_original": "Luật số 29/2023/QH15 Điều 23-25: Thu tiền thanh toán trong bán, cho thuê mua nhà ở, công trình xây dựng hình thành trong tương lai (không quá 50% đối với doanh nghiệp có vốn đầu tư nước ngoài) và bảo lãnh bán nhà ở.",
        "source_url": "https://thuvienphapluat.vn/van-ban/Bat-dong-san/Luat-Kinh-doanh-bat-dong-san-2023-29-2023-QH15-589578.aspx",
        "elements_json": json.dumps([
            {"eid": "e_pre_sale_collection_cap", "text_zh": "外商投资企业交付前预售款项累计不得超过50%刚性上限", "status": "mandatory"},
            {"eid": "e_mandatory_bank_guarantee_completion", "text_zh": "商业银行对开发商按期竣工交付承担强制法定履约保函担保", "status": "mandatory"}
        ], ensure_ascii=False)
    },

    # ---------------- 3. 马来西亚 (MY) ----------------
    {
        "norm_id": "MY:Specific_Relief_Act_1950:Sec20_21",
        "law": "Specific Relief Act 1950",
        "enbez": "Sec 20-21",
        "title": "施工合同强制实际履行绝对排除与金钱损害赔偿优先原则",
        "country": "MY",
        "heading_path": "Specific Relief Act 1950 (Act 137) >> Part II >> Chapter II Specific Performance of Contracts",
        "text_zh": "【施工合同禁止判令强制实际履行】马来西亚《1950年特定救济法》第20条第(1)款：对于其履行涉及法院无法进行日常连续监督的工程建设、劳务提供合同，或金钱损害赔偿构成充分救济的商事合同，法庭严禁判令强制实际履行（Specific Performance）；因此在建设工程争议中，承包商无权强行要求留场强行施工，合同终止后承包商仅能提起违约损害赔偿或已完工程价款清算诉求。",
        "text_en": "Malaysia Specific Relief Act 1950 (Act 137) Sections 20-21: Specific performance cannot be enforced for building construction contracts or contracts requiring continuous court supervision, or where monetary damages provide adequate relief; contractor cannot compel employer to allow continued site possession.",
        "text_original": "Specific Relief Act 1950 Section 20(1): Contracts not specifically enforceable, including contracts the performance of which involves the performance of a continuous duty which the court cannot supervise.",
        "source_url": "https://lom.agc.gov.my/act-detail.php?act=137",
        "elements_json": json.dumps([
            {"eid": "e_no_specific_performance_construction", "text_zh": "法院禁止判令工程承包合同强制实际履行的法定抗辩", "status": "mandatory"},
            {"eid": "e_damages_exclusive_remedy", "text_zh": "违约救济优先退化为金钱损害赔偿之法理规则", "status": "statutory"}
        ], ensure_ascii=False)
    },
    {
        "norm_id": "MY:Specific_Relief_Act_1950:Sec50_53",
        "law": "Specific Relief Act 1950",
        "enbez": "Sec 50-53",
        "title": "保函止付禁令与反停工令（Interim Injunction）司法审查要件",
        "country": "MY",
        "heading_path": "Specific Relief Act 1950 (Act 137) >> Part III Preventive Relief >> Chapter IX Injunctions Generally",
        "text_zh": "【临时禁令与保函止付司法准则】马来西亚《1950年特定救济法》第50-53条：法庭享有依据衡平法签发临时禁令（Interim Injunction）的自由裁量权；在建设工程履约保函索兑争议中，申请人若请求法院签发止付禁令，必须达到确凿证明存在欺诈（Fraud）或无良行径（Unconscionability）且存在重大不可逆损害的极高证明标准；否则法庭必须维护见索即付商业保函的独立流通性。",
        "text_en": "Specific Relief Act 1950 Sections 50-53: Regulates temporary and perpetual injunctions; stop-payment injunctions against on-demand performance bonds require proof of clear fraud or established unconscionability pursuant to American Cyanamid and Sumatec principles.",
        "text_original": "Specific Relief Act 1950 Sections 50-53: Preventive relief granted by injunction, temporary or perpetual, discretionary principles and conditions for restraint.",
        "source_url": "https://lom.agc.gov.my/act-detail.php?act=137",
        "elements_json": json.dumps([
            {"eid": "e_injunction_balance_of_convenience", "text_zh": "临时禁令申请之不可弥补损害与便利平衡要件", "status": "procedural"},
            {"eid": "e_bond_injunction_threshold", "text_zh": "独立保函止付禁令欺诈或显失公平之极高司法心证标准", "status": "mandatory"}
        ], ensure_ascii=False)
    },
    {
        "norm_id": "MY:Arbitration_Amendment_Act_2024:Sec4_7",
        "law": "Arbitration Act 2005",
        "enbez": "Amendment Act 2024",
        "title": "2024仲裁法修正案第三方仲裁资助（TPF）合法化披露与AIAC管理重塑",
        "country": "MY",
        "heading_path": "Arbitration (Amendment) Act 2024 (Act A1715) >> Part II Amendments",
        "text_zh": "【马来西亚2024仲裁法重大修正】马来西亚2024年仲裁修正法案（Arbitration (Amendment) Act 2024）：正式废除普通法关于诉讼买卖（Champerty and Maintenance）对仲裁资助的束缚，确立在涉外与工程商事仲裁中引入第三方资助（Third-Party Funding, TPF）的合法性；受资助当事人负有在仲裁开始阶段即向仲裁庭和相对方主动披露资助协议存在及资助人身份的刚性法定义务；确立马来西亚国际仲裁中心（AIAC）全新治理框架。",
        "text_en": "Arbitration (Amendment) Act 2024: Legalizes Third-Party Funding (TPF) in domestic and international arbitrations seated in Malaysia; imposes mandatory disclosure requirements of funding agreements and funder identities to avoid conflicts of interest; restructures AIAC administrative authorities.",
        "text_original": "Arbitration (Amendment) Act 2024: Introduction of third-party funding provisions, mandatory disclosure obligations, and institutional reform of AIAC.",
        "source_url": "https://lom.agc.gov.my/act-detail.php?act=A1715",
        "elements_json": json.dumps([
            {"eid": "e_tpf_statutory_legality", "text_zh": "涉外工程仲裁第三方资助TPF法定合法性确立", "status": "statutory"},
            {"eid": "e_tpf_mandatory_disclosure", "text_zh": "受资助方主动向仲裁庭披露资助人身份与利益冲突之强行义务", "status": "mandatory"}
        ], ensure_ascii=False)
    },
    {
        "norm_id": "MY:National_Land_Code_Act828:Sec221_228",
        "law": "National Land Code",
        "enbez": "Sec 221-228",
        "title": "超过3年长期土地租赁（Lease）法定登记对抗要件与新能源用地保障",
        "country": "MY",
        "heading_path": "National Land Code (Act 828) >> Part Fifteen Leases and Tenancies",
        "text_zh": "【长期土地租赁法定登记对抗效力】马来西亚《1965年国家土地法典》第221-228条：租期超过3年的长期土地租赁（Lease）属于法定物权性权利，必须以标准表格（Form 15A）向土地注册处办理正式物权登记；未办理物权登记的长期租约，在法律上仅产生当事人之间的债权性租赁（Tenancy exempt from registration），不得对抗善意取得土地所有权的后续买受人或银行抵押权人（Chargee）；光伏与基建项目必须办理注册以对抗土地权属变动风险。",
        "text_en": "National Land Code (Act 828) Sections 221-228: Leases exceeding 3 years must be registered via Form 15A to confer an indefeasible legal interest in land; unregistered long-term leases take effect merely as equitable tenancies unenforceable against subsequent registered proprietors or bank chargees.",
        "text_original": "National Land Code Section 221-228: Powers of leasing, requirements for valid registration of leases exceeding three years using Form 15A, and consequences of non-registration.",
        "source_url": "https://lom.agc.gov.my/act-detail.php?act=828",
        "elements_json": json.dumps([
            {"eid": "e_lease_registration_form15a", "text_zh": "超过3年租赁必须通过Form 15A向土地局办理物权登记要件", "status": "mandatory"},
            {"eid": "e_unregistered_lease_vulnerability", "text_zh": "未登记长期租赁仅具债权效力无法对抗第三人抵押与转让", "status": "risk_rule"}
        ], ensure_ascii=False)
    },

    # ---------------- 4. 新加坡 (SG) ----------------
    {
        "norm_id": "SG:SCJA_Cap322:Sec18D_18M",
        "law": "SCJA Cap 322",
        "enbez": "Sec 18D-18M & SICC Rules",
        "title": "新加坡国际商事法院（SICC）专属管辖、不方便法院排除与外国法出庭律师直接查明",
        "country": "SG",
        "heading_path": "Supreme Court of Judicature Act (Cap 322) >> Part IIA Singapore International Commercial Court",
        "text_zh": "【SICC管辖权与外国法出庭律师法律陈词直接查明】新加坡最高法院司法管辖权法第18D-18M条及《SICC Rules 2022》Order 16 Rule 8：凡合同约定由新加坡国际商事法院（SICC）管辖的跨国案件，法庭自动排除传统‘不方便法院（Forum Non Conveniens）’的中止抗辩；在涉外法律查明中，SICC 允许外国法直接由具备资质的外国注册出庭律师（Registered Foreign Lawyers）通过向法庭提交书面法律陈词（Submissions）直接进行查明，彻底免除普通法传统漫长、昂贵的专家证人出庭与交叉质证程序！",
        "text_en": "Supreme Court of Judicature Act (Cap 322) Part IIA & SICC Rules 2022 Order 16 Rule 8: SICC exercises international commercial jurisdiction; contractual submission precludes forum non conveniens; foreign law can be determined on basis of legal submissions from registered foreign lawyers without formal expert witness testimony.",
        "text_original": "Supreme Court of Judicature Act (Cap 322) Section 18D-18M and SICC Rules Order 16 Rule 8: Determination of foreign law on submissions rather than by proof as a matter of fact.",
        "source_url": "https://sso.agc.gov.sg/Act/SCJA1969",
        "elements_json": json.dumps([
            {"eid": "e_sicc_jurisdiction_exclusive", "text_zh": "SICC管辖权协议约定排除普通法不方便法院抗辩", "status": "statutory"},
            {"eid": "e_foreign_law_submission_ascertainment", "text_zh": "外国法免于专家证人质证而由外国出庭律师法律陈词直接查明", "status": "procedural"}
        ], ensure_ascii=False)
    },
    {
        "norm_id": "SG:WSH_Design_for_Safety_2015:Reg4_6",
        "law": "WSH (DFS) Regulations 2015",
        "enbez": "Reg 4-6",
        "title": "工作场所安全与健康（设计安全）发包人、设计师与总包商法定连带责任",
        "country": "SG",
        "heading_path": "Workplace Safety and Health (Design for Safety) Regulations 2015",
        "text_zh": "【新加坡工程设计阶段法定安全连带责任】新加坡《工作场所安全与健康（设计安全）条例》：项目发包人（Developer）、工程设计单位（Designer）及主承包商（Principal Contractor）在工程策划与施工图深化设计阶段，负有消除或最小化全生命周期施工与运维职业安全风险的法定连带义务；发包人必须设立设计安全专业协调员（DFS Coordinator）；违反设计安全评估导致严重安全事故的，依法追究发包人及设计总监个人刑事责任。",
        "text_en": "Workplace Safety and Health (Design for Safety) Regulations 2015 Regulations 4-6: Mandates Developers, Designers, and Contractors to eliminate and mitigate workplace safety and health risks upstream during the design phase; statutory duty to appoint a Design for Safety Coordinator.",
        "text_original": "WSH (Design for Safety) Regulations 2015: Duties of developers, designers, and contractors to conduct safety design risk assessments and appoint DFS coordinators.",
        "source_url": "https://sso.agc.gov.sg/SL/WSHA2006-S440-2015",
        "elements_json": json.dumps([
            {"eid": "e_dfs_joint_duty", "text_zh": "发包人与设计单位在设计源头消除施工运维风险的法定强行法责任", "status": "mandatory"},
            {"eid": "e_dfs_coordinator_mandate", "text_zh": "大型工程项目必须强制任命法定DFS协调员要件", "status": "condition_precedent"}
        ], ensure_ascii=False)
    },

    # ---------------- 5. 泰国 (TH) ----------------
    {
        "norm_id": "TH:Administrative_Court_Act_2542:Sec3_9_51",
        "law": "Administrative Court Act 2542",
        "enbez": "Sec 3, 9, 51",
        "title": "政府工程特许权定性为行政合同、5年特别时效与行政法院专属司法审查",
        "country": "TH",
        "heading_path": "Act on Establishment of Administrative Courts and Administrative Court Procedure B.E. 2542 >> Sections 3, 9, 51",
        "text_zh": "【泰国行政合同特权与5年特别诉讼时效】泰国佛历2542年《行政法院设立与诉讼程序法》第3条、第9条及第51条：凡是私营主体与泰国政府部委、国有独资企业（如 EGAT 泰国国家电力局、SRT 铁路局、PAT 港务局）签署的基础设施特许经营（Concession）及公用事业 EPC 总包合同，在法律上被强制归类为‘行政合同（Administrative Contract）’；行政合同项下索赔起诉时效为自知道或应当知道原因之日起5年（排除民商法典承揽工程款2年时效）；行政机关享有基于重大公共利益单方变更合同特权，且任何仲裁裁决均须受泰国行政法院关于国家重大利益公共秩序（Public Order）的严苛司法撤裁审查！",
        "text_en": "Thailand Administrative Court Act B.E. 2542 (1999) Sections 3, 9, 51: Infrastructure concessions and EPC contracts with Thai government ministries or state enterprises (EGAT, SRT) are statutorily classified as 'Administrative Contracts'; subject to a 5-year limitation period (distinguished from 2-year civil code hire-of-work period) and exclusive supervisory jurisdiction of Administrative Courts.",
        "text_original": "พระราชบัญญัติจัดตั้งศาลปกครองและวิธีพิจารณาคดีปกครอง พ.ศ. 2542 มาตรา 3, 9, 51: สัญญาทางปกครอง อายุความ 5 ปี และอำนาจศาลปกครองในการพิจารณาพิพากษา.",
        "source_url": "https://www.admincourt.go.th",
        "elements_json": json.dumps([
            {"eid": "e_admin_contract_classification", "text_zh": "涉政府与国企基础设施特许经营合同被法定定性为行政合同", "status": "mandatory"},
            {"eid": "e_five_year_admin_limitation", "text_zh": "行政合同特别起诉时效5年排除普通民商事承揽2年时效", "status": "statutory"},
            {"eid": "e_admin_court_public_order_review", "text_zh": "最高行政法院基于国家重大公共利益撤销仲裁裁决专属审查权", "status": "mandatory"}
        ], ensure_ascii=False)
    },
    {
        "norm_id": "TH:CCC:Sec681_1_686_Guarantee",
        "law": "Civil and Commercial Code",
        "enbez": "Sec 681/1, 686",
        "title": "保证编修正案自然人连带保证绝对无效与债权人60天催告时效失权",
        "country": "TH",
        "heading_path": "Thailand Civil and Commercial Code >> Title XI Suretyship >> Sections 681/1, 686",
        "text_zh": "【泰国保证担保强行法修正】《泰国民商法典》保证编第681/1条与第686条（2014/2015重大修法）：任何要求非法人自然人保证人承担连带保证责任（Joint and Several Debtor）或预先放弃先诉抗辩权的条款一律自始绝对无效；主债务人违约后，债权人必须在60日内向保证人发出正式书面催告通知，若债权人未能在此60日法定期间内发出催告，保证人依法免除该60日届满后所产生的一切利息、违约金及附随履约费用！",
        "text_en": "Thailand Civil and Commercial Code Sections 681/1 and 686 (amended 2014/2015): Agreements requiring individual non-corporate guarantors to be held jointly liable with the debtor are strictly void; creditors must give written notice of default to the guarantor within 60 days, failing which the guarantor is released from all interest and penalties accruing thereafter.",
        "text_original": "ประมวลกฎหมายแพ่งและพาณิชย์ มาตรา 681/1 และ มาตรา 686: ข้อตกลงให้ผู้ค้ำประกันรับผิดอย่างลูกหนี้ร่วมเป็นโมฆะ และหน้าที่เจ้าหนี้ต้องมีหนังสือบอกกล่าวผู้ค้ำประกันภายใน 60 วัน.",
        "source_url": "https://www.krisdika.go.th",
        "elements_json": json.dumps([
            {"eid": "e_individual_guarantor_joint_void", "text_zh": "非法人保证人连带责任格式条款绝对无效之强行法抗辩", "status": "mandatory"},
            {"eid": "e_sixty_day_notice_interest_release", "text_zh": "债权人违约后60日未催告保证人导致后续利息违约金法定免除", "status": "mandatory"}
        ], ensure_ascii=False)
    },

    # ---------------- 6. 菲律宾 (PH) ----------------
    {
        "norm_id": "PH:DOE_DC2022_11_0034:Renewable_Energy",
        "law": "DOE Circular DC2022-11-0034",
        "enbez": "Section 1",
        "title": "可再生能源实施细则修正令全面废除40%外资上限允许100%独资持有电站",
        "country": "PH",
        "heading_path": "Department of Energy Department Circular No. DC2022-11-0034",
        "text_zh": "【可再生能源外资准入100%独资重磅新规】菲律宾能源部第DC2022-11-0034号通函（依据司法部第21号宪法解释意见签发）：正式修订《2008年可再生能源法实施细则》第19条第(B)款，废止此前对太阳能、风能、潮汐能、海洋能及地热能电站开发外资股权不得超过40%的限制，明确允许外国投资者100%独资设立项目公司（SPV）在菲律宾全境勘探、开发和利用可再生能源；出海能源央企无需再采用高风险的菲律宾本土代持人架构！",
        "text_en": "Philippine Department of Energy Circular No. DC2022-11-0034: Formally amends Section 19(B) of the Renewable Energy Act IRR pursuant to DOJ Opinion No. 21 (2022), abolishing the 40% foreign equity cap and allowing 100% foreign ownership in solar, wind, and renewable power projects in the Philippines.",
        "text_original": "DOE Department Circular No. DC2022-11-0034: Prescribing Amendments to the Implementing Rules and Regulations of Republic Act No. 9513, permitting 100% foreign ownership of renewable energy projects.",
        "source_url": "https://www.doe.gov.ph",
        "elements_json": json.dumps([
            {"eid": "e_renewable_100pct_foreign_equity", "text_zh": "太阳能风能新能源电站开发外商100%独资合法化", "status": "statutory"},
            {"eid": "e_anti_dummy_risk_elimination", "text_zh": "依法彻底终结代持Nominee违规架构之法律前提", "status": "key_shift"}
        ], ensure_ascii=False)
    },
    {
        "norm_id": "PH:RA_12009:New_Government_Procurement_2024",
        "law": "RA 12009",
        "enbez": "Sec 8, 61-65, 72",
        "title": "2024新政府采购法最具经济优势标MEARB与最终受益所有人穿透审查",
        "country": "PH",
        "heading_path": "Republic Act No. 12009 (New Government Procurement Act 2024)",
        "text_zh": "【2024年菲律宾新政府采购法重构】菲律宾共和国法第12009号（2024年8月起生效，废止旧RA 9184）：废止唯低价中标传统，全面引入全生命周期成本（LCC）与最具经济优势标（MEARB）；确立全流程电子采购透明度机制；投标联合体必须穿透披露实际最终受益所有人（Beneficial Ownership），严打关联企业围标、借用资质与影子投标；发生严重迟延或履约瑕疵的总包商，将被依法列入全国统一黑名单并处以1至5年全行业禁入。",
        "text_en": "Republic Act No. 12009 (New Government Procurement Act 2024): Replaces lowest calculated responsive bid with Most Economically Advantageous and Responsive Bid (MEARB); mandates disclosure of beneficial ownership to combat bid-rigging; establishes unified debarment blacklisting system.",
        "text_original": "Republic Act No. 12009: An Act Providing for the Modernization and Standardization of the Procurement Activities of the Government and for Other Purposes.",
        "source_url": "https://www.officialgazette.gov.ph",
        "elements_json": json.dumps([
            {"eid": "e_mearb_bidding_standard", "text_zh": "最具经济优势标MEARB取代传统唯低价中标机制", "status": "statutory"},
            {"eid": "e_beneficial_ownership_transparency", "text_zh": "联合体实际控制人Beneficial Ownership穿透披露强行法要件", "status": "mandatory"}
        ], ensure_ascii=False)
    },

    # ---------------- 7. 中国 (CN) 涉外法 ----------------
    {
        "norm_id": "CN:Civil_Procedure_Law_2023:Foreign_Related_Sec",
        "law": "PRC Civil Procedure Law 2023",
        "enbez": "Art 276, 277, 280, 284, 300",
        "title": "2023修正民事诉讼法第四编涉外程序适当联系管辖、境外取证与平行诉讼协调",
        "country": "CN",
        "heading_path": "中华人民共和国民事诉讼法（2023修正）第四编 涉外民事诉讼程序的特别规定",
        "text_zh": "【中国民诉法2023涉外编特别规定】《中华人民共和国民事诉讼法》（2023年修正，2024年1月1日施行）第四编：涉外合同或其他财产权益纠纷，合同签订地、履行地、诉讼标的物所在地、代表机构所在地或可供扣押财产所在地在境内的，人民法院享有管辖权（适当联系管辖，第276条）；当事人书面协议排他选择境内法院且与争议有实际联系的，按协议确定（第277条）；针对同一争议在外国法院与中国法院同时起诉的，中国法院享有先行管辖权，但在外国法院裁判更便于审理时可裁定中止诉讼（平行诉讼与不方便法院，第280-281条）；非经中国主管机关许可严禁向外国司法机构提供境内数据材料（第284条，衔接数安法36条）。",
        "text_en": "PRC Civil Procedure Law (2023 Amendment) Part IV (Special Provisions for Foreign-Related Civil Procedures): Expands appropriate connection jurisdiction over foreign defendants (Art 276); recognizes exclusive jurisdiction agreements (Art 277); regulates parallel litigation and forum non conveniens (Arts 280-281); judicial review on cross-border evidence taking (Art 284).",
        "text_original": "《中华人民共和国民事诉讼法》（2023修正）第四编 涉外民事诉讼程序的特别规定：第二百七十六条至第三百零四条。",
        "source_url": "https://flk.npc.gov.cn/detail2.html?ZmY4MDgwODE4YTgxZDBmYTAxOGFlNGY2YWEwMjExNmQ%3D",
        "elements_json": json.dumps([
            {"eid": "e_appropriate_connection_jurisdiction", "text_zh": "出海中资企业财产或合同履行地适当联系境内管辖权", "status": "statutory"},
            {"eid": "e_cross_border_data_judicial_gate", "text_zh": "涉外诉讼境内数据与图纸境外提供前置司法审查许可", "status": "mandatory"}
        ], ensure_ascii=False)
    },
    {
        "norm_id": "CN:SPC_Foreign_Law_Ascertainment_2023:Art6_10",
        "law": "SPC Judicial Interpretation",
        "enbez": "Art 6-10",
        "title": "最高人民法院域外法查明规定庭前会议固定范围、五项完备性审查与无法查明认定",
        "country": "CN",
        "heading_path": "最高人民法院关于适用〈中华人民共和国涉外民事关系法律适用法〉若干问题的解释（二）（法释〔2023〕10号）",
        "text_zh": "【最高法域外法查明五项法定完备性审查标准】最高人民法院法释〔2023〕10号司法解释：涉外商事案件在庭前会议中由法官主持固定应当适用的域外法及各方争议焦点（第6条）；当事人提供域外法材料的，法院必须严格核验五项形式完备性要件：法律公布机关、生效时间、是否现行有效、修改沿革、判例权威层级与遵循先例拘束力（第8条）；出具法律意见书的专家证人应出庭接受质证，无正当理由不出庭的意见书不予采信（第9条）；只有在穷尽了国际司法协助、外国使领馆、法律查明专业机构等所有途径仍无法获得确切法律条文的，方能裁定‘无法查明’并依职权适用中国法（第10条）。",
        "text_en": "Supreme Court Interpretation on Foreign Law Ascertainment (Fa Shi [2023] No. 10) Articles 6-10: Mandates pre-trial conferences to fix applicable foreign laws; sets out 5 formal completeness review criteria (promulgating body, effective date, validity, amendments, precedent authority); expert witnesses must testify in court; strict exhaust-all-remedies threshold before declaring foreign law unascertainable.",
        "text_original": "最高人民法院法释〔2023〕10号第六条至第十条：域外法律查明的程序规程、完备性审查要件、专家证人出庭说明义务及无法查明之严格限制。",
        "source_url": "https://www.court.gov.cn/fabu-xiangqing-425251.html",
        "elements_json": json.dumps([
            {"eid": "e_five_formal_criteria_foreign_law", "text_zh": "域外法材料公布机关、有效性与判例效力五项完备性审查要件", "status": "mandatory"},
            {"eid": "e_expert_cross_examination_obligation", "text_zh": "出具域外法律查明报告之专家证人出庭接受质证强行法义务", "status": "procedural"},
            {"eid": "e_unascertainable_strict_exhaustion", "text_zh": "穷尽途径方可认定无法查明并依职权转回适用中国法", "status": "statutory"}
        ], ensure_ascii=False)
    }
]

L2_STATUTES = [
    {
        "norm_id": "TREATY:CAFTA_3.0_Upgrade:2024",
        "law": "CAFTA 3.0",
        "enbez": "Protocol 2024",
        "title": "中国-东盟自贸区3.0升级规则与中新自贸协定进一步升级议定书负面清单制度",
        "country": "ASEAN",
        "heading_path": "China-ASEAN Free Trade Area 3.0 & CSFTA Further Upgrade Protocol 2024",
        "text_zh": "【中国-东盟自贸区3.0与中新升级议定书负面清单】2024年12月31日生效的中新自贸协定进一步升级议定书及中国-东盟自贸区 3.0 版升级谈判成果：全面废止传统的正面清单准入模式，引入高标准的‘外资准入负面清单（Negative List）’及棘轮机制（Ratchet Mechanism）；确立建筑工程、电信及绿色能源领域国民待遇与最惠国待遇承诺；为中资企业投资东盟基础设施提供防止行政征收与资金自由汇兑的高水平条约保护防线。",
        "text_en": "CAFTA 3.0 and CSFTA Further Upgrade Protocol (effective Dec 31, 2024): Replaces positive lists with a comprehensive Negative List approach and Ratchet mechanism for foreign investments; establishes high-standard protection for construction, engineering, telecom, and green energy investments.",
        "text_original": "China-Singapore Free Trade Agreement Further Upgrade Protocol & CAFTA 3.0: Negative list commitments, investment liberalization, and investor-state dispute prevention.",
        "source_url": "http://fta.mofcom.gov.cn",
        "elements_json": json.dumps([
            {"eid": "e_negative_list_ratchet", "text_zh": "外商投资负面清单模式与锁定自主开放成果之棘轮机制", "status": "treaty"},
            {"eid": "e_national_treatment_construction", "text_zh": "涉外工程施工与电信数字基建全周期国民待遇保护", "status": "treaty"}
        ], ensure_ascii=False)
    },
    {
        "norm_id": "TREATY:DTA_BEPS_MLI:Art14_PE_Anti_Split",
        "law": "BEPS MLI",
        "enbez": "Article 14",
        "title": "多边税收公约（MLI）第14条建筑安装工程常设机构（PE）反合同拆分强行规则",
        "country": "ASEAN",
        "heading_path": "Multilateral Convention to Implement Tax Treaty Related Measures to Prevent BEPS (MLI) >> Article 14 Splitting-up of Contracts",
        "text_zh": "【涉外EPC工程工期分拆规避PE彻底失效】经合组织与二十国集团防范税基侵蚀多边公约（BEPS MLI）第14条（中国与东盟各国均已签署适用）：在判定建筑工地、建筑、装配或安装工程是否构成常设机构（PE，通常为6个月门槛）时，一个企业进行的紧密相连的工程活动如果超过30天，且由一个或多个关联企业在不同时期承揽的紧密相关活动合计超过6个月的，各段工期必须累计合并计算！出海央企传统‘将10个月项目分拆为两个关联公司各干5个月’规避东道国企业所得税的架构在此条款下自始穿透并面临巨额偷税追缴及刑事责任！",
        "text_en": "BEPS Multilateral Instrument (MLI) Article 14 (Splitting-up of Contracts): For the purpose of determining whether the PE period (typically 6 months) has been exceeded for building sites or construction projects, activities carried on by associated enterprises during connected periods exceeding 30 days are aggregated.",
        "text_original": "OECD BEPS Multilateral Instrument Article 14: Splitting-up of Contracts for building sites, construction or installation projects; aggregation of associated enterprise periods.",
        "source_url": "https://www.oecd.org/tax/treaties/beps-mli-position-china.pdf",
        "elements_json": json.dumps([
            {"eid": "e_anti_contract_splitting_rule", "text_zh": "关联企业工程分包活动在反拆分规则下强制工期合并计算", "status": "tax_rule"},
            {"eid": "e_pe_threshold_breach", "text_zh": "合并工期超6个月直接穿透触发东道国常设机构纳税义务", "status": "mandatory"}
        ], ensure_ascii=False)
    },
    {
        "norm_id": "STD_CONTRACT:SG_PSSCOC_2020:Clause14_31",
        "law": "PSSCOC 2020",
        "enbez": "Cl 14, 31",
        "title": "新加坡公共部门标准施工合同条件（PSSCOC）工期顺延与60天索赔绝对失权条款",
        "country": "SG",
        "heading_path": "Public Sector Standard Conditions of Contract for Construction Works 2020",
        "text_zh": "【新加坡政府工程PSSCOC严格时效失权】新加坡建设局（BCA）公共部门标准施工合同条件（PSSCOC 2020，新加坡公共交通LTA、供水PUB全部强制采用）：第14条规定因发包人延误场地、图纸迟延或恶劣气候可顺延工期（EOT）；第31条【索赔除斥期】：承包商必须在导致额外支出事件发生之日起28天内提交索赔意向通知，并在60天内提交详细账目与事实清单；若承包商未能在60天内提交详尽凭据，承包商完全丧失索赔权利，发包人彻底免除责任，且审裁员或仲裁庭无权依衡平法放宽该60天刚性除斥期！",
        "text_en": "Singapore PSSCOC 2020 Clauses 14 & 31: Regulates Extension of Time; Clause 31 sets a strict 60-day absolute time-bar for submission of detailed claims accounts, failure of which completely bars contractor's financial remedies with no equitable relief.",
        "text_original": "PSSCOC 2020 Clause 31.1: Condition precedent to claim for loss and expense, notice within 28 days and detailed account within 60 days, absolute time bar.",
        "source_url": "https://www1.bca.gov.sg/procurement/post-tender-stage/public-sector-standard-conditions-of-contract-psscoc",
        "elements_json": json.dumps([
            {"eid": "e_psscoc_60d_absolute_time_bar", "text_zh": "60天内未提交详尽索赔账册事实导致实体权利绝对消灭", "status": "condition_precedent"},
            {"eid": "e_eot_employer_prevention", "text_zh": "因发包人违约妨碍迟延交地构成工期顺延正当抗辩事由", "status": "statutory"}
        ], ensure_ascii=False)
    },
    {
        "norm_id": "STD_CONTRACT:MY_PWD_203A:Clause40_43",
        "law": "PWD Form 203A",
        "enbez": "Clause 40, 43",
        "title": "马来西亚公共工程局标准合同条件违约金核减与建筑师工期顺延裁决",
        "country": "MY",
        "heading_path": "Standard Form of Contract P.W.D. Form 203A (Rev. 1/2010 / 2020)",
        "text_zh": "【马来西亚公共工程局标准合同违约与EOT规则】马来西亚工程部公共工程局标准合同条件（PWD Form 203A）：第40条误期损害赔偿金（LAD）：必须由监督官（Superintending Officer, SO）签发迟延违约证书（CNC）后方可按日扣款；第43条工期延长：承包商遭遇不可归责事由或政府迟延时必须在事件发生后30天内向 SO 发函申请顺延，SO 有权依职权公正评估核定合理的工期延长天数。",
        "text_en": "Malaysia P.W.D. Form 203A Clauses 40 & 43: Governs Liquidated and Ascertained Damages (LAD) triggered only upon issuance of Certificate of Non-Completion (CNC); Clause 43 regulates Extension of Time assessments by the Superintending Officer upon timely written notice.",
        "text_original": "JKR Standard Form 203A Clauses 40 & 43: Liquidated and Ascertained Damages and Extension of Time procedures.",
        "source_url": "https://www.jkr.gov.my",
        "elements_json": json.dumps([
            {"eid": "e_cnc_prerequisite_for_lad", "text_zh": "签发不合格/迟延完成证书CNC系主张工期违约金之绝对前置要件", "status": "condition_precedent"},
            {"eid": "e_so_fair_eot_assessment", "text_zh": "监督官SO依法秉持中立合理核定工期延长天数之义务", "status": "mandatory"}
        ], ensure_ascii=False)
    },
    {
        "norm_id": "REG:VN_Decree_80_2024:DPPA",
        "law": "Decree 80/2024/ND-CP",
        "enbez": "Art 12-22",
        "title": "越南大工业用户与可再生能源发电商直接购电机制（DPPA）实施细则",
        "country": "VN",
        "heading_path": "Nghị định số 80/2024/ND-CP về cơ chế mua bán điện trực tiếp (DPPA)",
        "text_zh": "【越南大工业可再生能源直接购电机制DPPA】越南政府第80/2024/ND-CP号法令：正式落地直连线路（Private Wire）及国家电网转供（Grid-connected DPPA via CfD 差价合约）两种模式；年用电量超过20万千瓦时的大工业用户可直接与光伏、风电发电商签署买卖合同；在网转模式下，发电商向国家电力市场出清并与大用户按照差价合约进行金融结算，彻底打破国家电网单一统购统销垄断，为外资大型工业园绿色电力消纳与绿证（REC）核发提供法理依据。",
        "text_en": "Vietnam Decree No. 80/2024/ND-CP (DPPA Mechanism): Governs physical direct private wire purchase and national grid-connected synthetic purchase via Contracts for Difference (CfD); enables large power consumers to contract directly with renewable energy generators.",
        "text_original": "Nghị định số 80/2024/ND-CP: Quy định về cơ chế mua bán điện trực tiếp giữa đơn vị phát điện năng lượng tái tạo với khách hàng sử dụng điện lớn.",
        "source_url": "https://thuvienphapluat.vn/van-ban/Thuong-mai/Nghi-dinh-80-2024-ND-CP-mua-ban-dien-truc-tiep-giua-don-vi-phat-dien-nang-luong-tai-tao-voi-khach-hang-su-dung-dien-lon-615655.aspx",
        "elements_json": json.dumps([
            {"eid": "e_dppa_cfd_mechanism", "text_zh": "可再生能源发电商与大工业用户签署差价合约CfD进行差价金融结算", "status": "statutory"},
            {"eid": "e_grid_wheeling_regime", "text_zh": "利用国家电网转供电量并按国家统一定价支付过网与系统调度费用", "status": "mandatory"}
        ], ensure_ascii=False)
    },
    {
        "norm_id": "LAW:ID_UU_27_2022_PDP:Cross_Border",
        "law": "UU 27/2022",
        "enbez": "Art 56",
        "title": "印尼个人数据保护法跨境传输同等保护水平与数据主体明示同意要件",
        "country": "ID",
        "heading_path": "Undang-Undang No. 27 Tahun 2022 tentang Pelindungan Data Pribadi >> Bab VIII Transfer Data Pribadi",
        "text_zh": "【印尼数据主权与跨境传输合规要件】印尼第27/2022号个人数据保护法（UU PDP，2024年10月17日正式全面强制执法！）：工程总承包商或跨国企业将印尼境内员工、分包商雇员及业主人员个人数据向中国总部或境外服务器跨境传输的，必须满足三级递进要件：接收国必须具备等同或更高的数据保护法律水平；若无，数据控制者必须与境外接收方订立具备法律约束力的数据保护协议；在上述条件均不具备时，必须取得数据主体的单独明示同意（Explicit Consent）；擅自违规跨境传输的，面临最高相当于年营业额2%的行政罚款及个人刑事监禁！",
        "text_en": "Indonesian Personal Data Protection Law (UU No. 27/2022) Article 56 (effective Oct 17, 2024): Mandates strict tiered conditions for cross-border personal data transfers: adequacy of destination country protection, binding contractual safeguards, or explicit consent; severe administrative and criminal penalties for unlawful transfer.",
        "text_original": "UU No. 27/2022 Pasal 56: Pengendali Data Pribadi wajib memastikan negara tempat kedudukan Pengendali Data Pribadi yang menerima transfer memiliki tingkat pelindungan data yang setara atau lebih tinggi.",
        "source_url": "https://peraturan.go.id/id/uu-no-27-tahun-2022",
        "elements_json": json.dumps([
            {"eid": "e_cross_border_data_adequacy", "text_zh": "数据接收国具备同等保护水平或签署标准合同条款SCC要件", "status": "mandatory"},
            {"eid": "e_explicit_data_subject_consent", "text_zh": "数据跨境流动必须取得自然人数据主体单独明示同意之刚性抗辩", "status": "mandatory"}
        ], ensure_ascii=False)
    },
    {
        "norm_id": "LAW:SG_IRDA_2018:Cross_Border_Insolvency",
        "law": "IRDA 2018",
        "enbez": "Tenth Schedule",
        "title": "新加坡破产重组与解散法采纳联合国跨国破产示范法及其跨境承认效力",
        "country": "SG",
        "heading_path": "Insolvency, Restructuring and Dissolution Act 2018 >> Part 11 & Tenth Schedule",
        "text_zh": "【新加坡跨境破产与跨国资产保全机制】新加坡《破产、重组与解散法》（IRDA 2018）第十附表：正式全额采纳《联合国国际贸易法委员会跨国界破产示范法》；外国主要破产程序（Foreign Main Proceeding）在新加坡高等法院获得承认后，新加坡境内的诉讼、仲裁程序及针对债务人财产的执行措施依法自动产生中止（Stay）效力，破产管理人享有接管境内资产及申请协助调查的法定权力；但对以独立见索即付保函为代表的第三方信贷增信工具，不因基础债务人进入破产程序而自动豁免兑付义务。",
        "text_en": "Singapore Insolvency, Restructuring and Dissolution Act 2018 (IRDA) Tenth Schedule: Enacts the UNCITRAL Model Law on Cross-Border Insolvency; recognition of a foreign main proceeding imposes an automatic stay on local enforcement actions against debtor assets while preserving third-party performance guarantee rights.",
        "text_original": "IRDA 2018 Tenth Schedule: Model Law on Cross-Border Insolvency, recognition of foreign proceedings, automatic relief and cooperation with foreign courts.",
        "source_url": "https://sso.agc.gov.sg/Act/IRDA2018",
        "elements_json": json.dumps([
            {"eid": "e_foreign_main_proceeding_stay", "text_zh": "外国主要破产程序承认后对境内司法执行措施之自动中止效力", "status": "procedural"},
            {"eid": "e_third_party_guarantee_carve_out", "text_zh": "独立见索即付保函等第三方担保工具独立于债务人破产保护清算程序", "status": "statutory"}
        ], ensure_ascii=False)
    }
]
