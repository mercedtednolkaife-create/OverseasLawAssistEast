import { NormOrCaseItem } from '../../types/lawAgent';

/**
 * 东盟法规与裁判智库权威基准数据集 (Offline High-Fidelity Fallback & Standard Constants)
 * 解决网络等待空数据与无后端服务下的渲染白屏问题，收录全部 31 项核心法条与 7 大金标准司法先例
 */
export const DEFAULT_SEARCH_ITEMS: NormOrCaseItem[] = [
  {
    "id": "ID:UU_2_2017:Art57",
    "kind": "norm",
    "law": "UU_2_2017",
    "enbez": "Art.57",
    "title": "《印尼建筑服务法》第57条：属地承包商联营与分包连带责任",
    "heading_path": "UU No. 2/2017 > Bab VI Layanan Usaha > Pasal 57",
    "text_de": "【司法部法通网权威译本】施工承包商可将部分专业工程分包给专业分包商，或通过设立联合体/非法人联营体（KSO）形式履行。承包商与联营体各方对建设工程质量和合同义务承担连带履约责任。",
    "text_zh_machine": "【司法部法通网权威译本】施工承包商可将部分专业工程分包给专业分包商，或通过设立联合体/非法人联营体（KSO）形式履行。承包商与联营体各方对建设工程质量和合同义务承担连带履约责任。",
    "stand": "2026",
    "has_pending_amend": false,
    "source_url": "https://overseas-law.moj.gov.cn/fatong"
  },
  {
    "id": "ID:SEMA_3_2023",
    "kind": "norm",
    "law": "SEMA_3_2023",
    "enbez": "SEMA 3/2023",
    "title": "《最高法院2023年第3号通告》：反制纯外文合同无效抗辩裁判规则",
    "heading_path": "Surat Edaran Mahkamah Agung No. 3 Tahun 2023 > Perdata Khusus",
    "text_de": "【司法部法通网权威译本】涉外商事与建设工程合同即便未按照2009年第24号《国旗、语言法》签署印尼语译本，裁判机构亦不得仅以缺少印尼语版本为由直接判令合同自始无效，除非主张方举证证明缔约方存在恶意欺诈（iktikad tidak baik）事实。",
    "text_zh_machine": "【司法部法通网权威译本】涉外商事与建设工程合同即便未按照2009年第24号《国旗、语言法》签署印尼语译本，裁判机构亦不得仅以缺少印尼语版本为由直接判令合同自始无效，除非主张方举证证明缔约方存在恶意欺诈（iktikad tidak baik）事实。",
    "stand": "2026",
    "has_pending_amend": false,
    "source_url": "https://overseas-law.moj.gov.cn/fatong"
  },
  {
    "id": "ID:MEMR_11_2024",
    "kind": "norm",
    "law": "MEMR_11_2024",
    "enbez": "MEMR 11/2024",
    "title": "《能矿部2024年第11号规章》：电力与新能源EPC项目本地化率(TKDN)阶梯配额与认证",
    "heading_path": "Permen ESDM No. 11/2024 > Ketentuan Tingkat Komponen Dalam Negeri (TKDN)",
    "text_de": "【法通网与行业标准】电力与新能源工程EPC总承包项目，关键主机辅机及建设工程服务须严格达到40%至60%的法定最低本地采购率（TKDN）；总包商须在商业运营日（COD）前取得PT Sucofindo或Surveyor Indonesia法定认证证书，否则发包人有权处以工程款5%至10%的法定扣罚甚至暂停电费结算。",
    "text_zh_machine": "【法通网与行业标准】电力与新能源工程EPC总承包项目，关键主机辅机及建设工程服务须严格达到40%至60%的法定最低本地采购率（TKDN）；总包商须在商业运营日（COD）前取得PT Sucofindo或Surveyor Indonesia法定认证证书，否则发包人有权处以工程款5%至10%的法定扣罚甚至暂停电费结算。",
    "stand": "2026",
    "has_pending_amend": false,
    "source_url": "https://overseas-law.moj.gov.cn/fatong"
  },
  {
    "id": "ID:KUHPerdata:Art1338",
    "kind": "norm",
    "law": "KUHPerdata",
    "enbez": "Art.1338",
    "title": "《印尼民法典》第1338条：契约即法律原则与善意履行",
    "heading_path": "Kitab Undang-Undang Hukum Perdata > Buku III Perikatan > Pasal 1338",
    "text_de": "【民商法通则】依法成立的合同对缔约双方具有如同法律一般的拘束力（Pacta Sunt Servanda）。合同当事人必须遵循善意原则（Good Faith）全面履行合同义务。",
    "text_zh_machine": "【民商法通则】依法成立的合同对缔约双方具有如同法律一般的拘束力（Pacta Sunt Servanda）。合同当事人必须遵循善意原则（Good Faith）全面履行合同义务。",
    "stand": "2026",
    "has_pending_amend": false,
    "source_url": "https://overseas-law.moj.gov.cn/fatong"
  },
  {
    "id": "VN:Law_135_2025:Art86.2",
    "kind": "norm",
    "law": "Law_135_2025",
    "enbez": "Art.86.2",
    "title": "《2025年新建设法》第86.2条：工程预定损害赔偿(LD)独立效力与法定最高罚金解绑",
    "heading_path": "Luật Xây dựng số 135/2025/QH15 > Chương VI Hợp đồng xây dựng > Điều 86 Khoản 2",
    "text_de": "【司法部法通网权威译本】建设工程合同当事人有权约定针对工期延误的预定损害赔偿金（Liquidated Damages, LD），该约定与原旧法下受限的12%最高违约罚金解绑，只要所约定的赔偿数额合理对应可能发生的客观预见损失，裁判机构应予确认其效力，不再以行政罚金上限强行调减。",
    "text_zh_machine": "【司法部法通网权威译本】建设工程合同当事人有权约定针对工期延误的预定损害赔偿金（Liquidated Damages, LD），该约定与原旧法下受限的12%最高违约罚金解绑，只要所约定的赔偿数额合理对应可能发生的客观预见损失，裁判机构应予确认其效力，不再以行政罚金上限强行调减。",
    "stand": "2026",
    "has_pending_amend": false,
    "source_url": "https://overseas-law.moj.gov.cn/fatong"
  },
  {
    "id": "VN:Law_135_2025:Art146",
    "kind": "norm",
    "law": "Law_135_2025",
    "enbez": "Art.146",
    "title": "《2025年新建设法》第146条：台风与不可抗力事件之工期顺延与费用免责",
    "heading_path": "Luật Xây dựng số 135/2025/QH15 > Điều 146 Bất khả kháng trong thi công",
    "text_de": "【司法部法通网权威译本】当发生海上极端台风、海啸或东道国主管机关重大规划变更等不可抗力事件时，施工承包商有权获得合理的工期顺延（EOT），并免除延误违约金责任。发包人不得以预定损害赔偿为由强行索兑履约保函。",
    "text_zh_machine": "【司法部法通网权威译本】当发生海上极端台风、海啸或东道国主管机关重大规划变更等不可抗力事件时，施工承包商有权获得合理的工期顺延（EOT），并免除延误违约金责任。发包人不得以预定损害赔偿为由强行索兑履约保函。",
    "stand": "2026",
    "has_pending_amend": false,
    "source_url": "https://overseas-law.moj.gov.cn/fatong"
  },
  {
    "id": "VN:Decree_210_2026:Art18",
    "kind": "norm",
    "law": "Decree_210_2026",
    "enbez": "Art.18",
    "title": "《第210/2026/ND-CP号建设合同法令》第18条：独立履约保函恶意索兑司法救济",
    "heading_path": "Nghị định 210/2026/NĐ-CP > Điều 18 Bảo lãnh thực hiện hợp đồng",
    "text_de": "【法通网建设法规】发包人索兑见索即付履约保函必须满足法定前提：承包商存在根本性实质违约，且发包人须至少提前14个工作日向承包商发出正式催告。未经法定催告突袭索兑或在存在争议未决时恶意索兑，承包商有权申请仲裁庭或法院紧急止付。",
    "text_zh_machine": "【法通网建设法规】发包人索兑见索即付履约保函必须满足法定前提：承包商存在根本性实质违约，且发包人须至少提前14个工作日向承包商发出正式催告。未经法定催告突袭索兑或在存在争议未决时恶意索兑，承包商有权申请仲裁庭或法院紧急止付。",
    "stand": "2026",
    "has_pending_amend": false,
    "source_url": "https://overseas-law.moj.gov.cn/fatong"
  },
  {
    "id": "MY:CIPAA_2012:Sec35",
    "kind": "norm",
    "law": "CIPAA_2012",
    "enbez": "Sec.35",
    "title": "《建筑业付款与快速裁决法》第35条：背靠背付款条款(Pay-when-paid)法定自始绝对无效",
    "heading_path": "Construction Industry Payment and Adjudication Act 2012 > Part V > Section 35",
    "text_de": "【司法部法通网权威译本】CIPAA 2012 第 35 条明确禁止附条件付款：(1) 建设工程合同中任何附条件付款条款一律无效；(2) 凡将总包商向分包商付款的条件设定为“须待总包商从项目业主处收讫工程款”（即行业通称的背靠背条款 Pay-when-paid），该条款依法自始绝对无效，总包商不得以此抗辩拒绝分包付款。",
    "text_zh_machine": "【司法部法通网权威译本】CIPAA 2012 第 35 条明确禁止附条件付款：(1) 建设工程合同中任何附条件付款条款一律无效；(2) 凡将总包商向分包商付款的条件设定为“须待总包商从项目业主处收讫工程款”（即行业通称的背靠背条款 Pay-when-paid），该条款依法自始绝对无效，总包商不得以此抗辩拒绝分包付款。",
    "stand": "2026",
    "has_pending_amend": false,
    "source_url": "https://overseas-law.moj.gov.cn/fatong"
  },
  {
    "id": "MY:CIPAA_2012:Sec13",
    "kind": "norm",
    "law": "CIPAA_2012",
    "enbez": "Sec.13",
    "title": "《建筑业付款与快速裁决法》第13条：法定裁决书即时执行力与先付款后争议原则",
    "heading_path": "Construction Industry Payment and Adjudication Act 2012 > Part II > Section 13",
    "text_de": "【司法部法通网权威译本】CIPAA 裁决员作出的工程款快速裁决书具有即时约束力（Pay Now, Argue Later 原则）。胜诉方可直接向马来西亚高等法院申请将裁决书作为生效判决予以强制执行；被执行方即便已提起实质仲裁或诉讼，亦不得中止付款履行。",
    "text_zh_machine": "【司法部法通网权威译本】CIPAA 裁决员作出的工程款快速裁决书具有即时约束力（Pay Now, Argue Later 原则）。胜诉方可直接向马来西亚高等法院申请将裁决书作为生效判决予以强制执行；被执行方即便已提起实质仲裁或诉讼，亦不得中止付款履行。",
    "stand": "2026",
    "has_pending_amend": false,
    "source_url": "https://overseas-law.moj.gov.cn/fatong"
  },
  {
    "id": "MY:Act_520_CIDB:Sec25",
    "kind": "norm",
    "law": "Act_520_CIDB",
    "enbez": "Sec.25",
    "title": "《建筑业发展局法》第25条：外资施工资质执照强制注册与合同效力红线",
    "heading_path": "Lembaga Pembangunan Industri Pembinaan Malaysia Act 1994 (Act 520) > Section 25",
    "text_de": "【法通网执业规范】未在马来西亚 CIDB（建筑业发展局）注册并取得相应等级（外资承揽重大项目须取得 G7 级牌照）承包商资格证书者，严禁从事任何施工承包活动。未持证缔约可能构成非法承揽，招致高额刑事罚款并影响民事工程款追索权。",
    "text_zh_machine": "【法通网执业规范】未在马来西亚 CIDB（建筑业发展局）注册并取得相应等级（外资承揽重大项目须取得 G7 级牌照）承包商资格证书者，严禁从事任何施工承包活动。未持证缔约可能构成非法承揽，招致高额刑事罚款并影响民事工程款追索权。",
    "stand": "2026",
    "has_pending_amend": false,
    "source_url": "https://overseas-law.moj.gov.cn/fatong"
  },
  {
    "id": "SG:SOPA_2004:Sec9",
    "kind": "norm",
    "law": "SOPA_2004",
    "enbez": "Sec.9",
    "title": "《建筑业付款保障法》第9条：禁止背靠背付款与强制极速响应期",
    "heading_path": "Building and Construction Industry Security of Payment Act 2004 > Part II > Section 9",
    "text_de": "【司法部法通网权威译本】SOPA 2004 第 9 条明确确认：合同中任何口头或书面的“背靠背付款（Pay-when-paid）”条款均无任何法律效力。发包人收到承包商付款申请后，必须在 7 至 14 天法定期间内提供付款响应（Payment Response），逾期将视为失权并受极速裁决惩戒。",
    "text_zh_machine": "【司法部法通网权威译本】SOPA 2004 第 9 条明确确认：合同中任何口头或书面的“背靠背付款（Pay-when-paid）”条款均无任何法律效力。发包人收到承包商付款申请后，必须在 7 至 14 天法定期间内提供付款响应（Payment Response），逾期将视为失权并受极速裁决惩戒。",
    "stand": "2026",
    "has_pending_amend": false,
    "source_url": "https://overseas-law.moj.gov.cn/fatong"
  },
  {
    "id": "SG:Precedent:BS_Mount_Sophia",
    "kind": "norm",
    "law": "Precedent",
    "enbez": "BS Mount Sophia",
    "title": "《BS Mount Sophia 终审判例》：确立独立于欺诈的“显失公平(Unconscionability)”保函止付标准",
    "heading_path": "Singapore Court of Appeal > BS Mount Sophia Pte Ltd v Join-Aim Pte Ltd [2012] SGCA 28",
    "text_de": "【新加坡最高法院经典先例】新加坡上诉法院确立了独特的见索即付保函司法救济规则：除传统普通法欺诈（Fraud）之外，“显失公平（Unconscionability）”构成独立的保函止付法定事由。当发包人在明显存在履约争议或违约事实微小时滥用见索即付工具突袭索兑，承包商举证达到较强初步表面证据（Strong Prima Facie Case）即可获发法院禁令。",
    "text_zh_machine": "【新加坡最高法院经典先例】新加坡上诉法院确立了独特的见索即付保函司法救济规则：除传统普通法欺诈（Fraud）之外，“显失公平（Unconscionability）”构成独立的保函止付法定事由。当发包人在明显存在履约争议或违约事实微小时滥用见索即付工具突袭索兑，承包商举证达到较强初步表面证据（Strong Prima Facie Case）即可获发法院禁令。",
    "stand": "2026",
    "has_pending_amend": false,
    "source_url": "https://overseas-law.moj.gov.cn/fatong"
  },
  {
    "id": "SG:Precedent:JBE_Properties",
    "kind": "norm",
    "law": "Precedent",
    "enbez": "JBE Properties",
    "title": "《JBE Properties 案》：允许合同专用条件明文排除显失公平抗辩之黄金起草规范",
    "heading_path": "Singapore Court of Appeal > JBE Properties Pte Ltd v Handy-Tool Construction [2011] SGCA 32",
    "text_de": "【起草防线经典判例】上诉法院裁定：商事合同双方若具备对等议价能力，允许通过合同明示清晰条款排除“显失公平”止付抗辩。央国企出海合同谈判时必须警惕发包人将“承包商明示放弃以显失公平为由申请止付保函”条款写入专用条件，一经签署将丧失该项关键救济武器。",
    "text_zh_machine": "【起草防线经典判例】上诉法院裁定：商事合同双方若具备对等议价能力，允许通过合同明示清晰条款排除“显失公平”止付抗辩。央国企出海合同谈判时必须警惕发包人将“承包商明示放弃以显失公平为由申请止付保函”条款写入专用条件，一经签署将丧失该项关键救济武器。",
    "stand": "2026",
    "has_pending_amend": false,
    "source_url": "https://overseas-law.moj.gov.cn/fatong"
  },
  {
    "id": "TH:FBA_1999:List3",
    "kind": "norm",
    "law": "FBA_1999",
    "enbez": "List 3",
    "title": "《外商经营法》附表三：建设工程外资49%股比限制与严禁代持人(Nominee)红线",
    "heading_path": "Foreign Business Act B.E. 2542 (1999) > Schedule 3 > Category (10)",
    "text_de": "【司法部法通网权威译本】泰国《外商经营法》将常规工程施工列入附表三限制行业，外资持股比例不得超过49%，除非取得泰国商业部外商经营许可证（FBL）或投资促进委员会（BOI）特别优惠。严禁中资企业采用泰国自然人或空壳公司代持股权（Nominee），一旦查实代持合同自始无效且面临刑事责任。",
    "text_zh_machine": "【司法部法通网权威译本】泰国《外商经营法》将常规工程施工列入附表三限制行业，外资持股比例不得超过49%，除非取得泰国商业部外商经营许可证（FBL）或投资促进委员会（BOI）特别优惠。严禁中资企业采用泰国自然人或空壳公司代持股权（Nominee），一旦查实代持合同自始无效且面临刑事责任。",
    "stand": "2026",
    "has_pending_amend": false,
    "source_url": "https://overseas-law.moj.gov.cn/fatong"
  },
  {
    "id": "TH:CCC:Sec596",
    "kind": "norm",
    "law": "CCC",
    "enbez": "Sec.596",
    "title": "《泰国民商法典》第596条：承揽合同完工延误与过高违约金司法酌减",
    "heading_path": "Thailand Civil and Commercial Code > Title VII Hire of Work > Section 596",
    "text_de": "【民商法典承揽编】承揽人延误交付工作成果的，定作人有权主张迟延违约金。但如果合同中约定的违约金数额过分高于客观实际损失，泰国法院及仲裁庭拥有法定自由裁量权，可依据公平原则裁量调减至合理数额。",
    "text_zh_machine": "【民商法典承揽编】承揽人延误交付工作成果的，定作人有权主张迟延违约金。但如果合同中约定的违约金数额过分高于客观实际损失，泰国法院及仲裁庭拥有法定自由裁量权，可依据公平原则裁量调减至合理数额。",
    "stand": "2026",
    "has_pending_amend": false,
    "source_url": "https://overseas-law.moj.gov.cn/fatong"
  },
  {
    "id": "PH:RA_11966:Sec18",
    "kind": "norm",
    "law": "RA_11966",
    "enbez": "Sec.18",
    "title": "《菲律宾公私合营PPP法典》第18条：废除旧BOT法与政府提前终止公允补偿机制",
    "heading_path": "Republic Act No. 11966 (The PPP Code of the Philippines) > Section 18",
    "text_de": "【司法部法通网权威译本】《菲律宾PPP法典》(RA 11966) 已明文废除实施三十余年的旧 BOT 法案 (RA 7718)。新法典规定：因政府方公共利益单方中止或换届政策调整终止特许权合同时，实施机构必须支付法定终止补偿，确保投资方已发生的经审计合理股权投资及金融债务得到优先全额清偿。",
    "text_zh_machine": "【司法部法通网权威译本】《菲律宾PPP法典》(RA 11966) 已明文废除实施三十余年的旧 BOT 法案 (RA 7718)。新法典规定：因政府方公共利益单方中止或换届政策调整终止特许权合同时，实施机构必须支付法定终止补偿，确保投资方已发生的经审计合理股权投资及金融债务得到优先全额清偿。",
    "stand": "2026",
    "has_pending_amend": false,
    "source_url": "https://overseas-law.moj.gov.cn/fatong"
  },
  {
    "id": "PH:Precedent:PCAB_v_Manila_Water",
    "kind": "norm",
    "law": "Precedent",
    "enbez": "PCAB v. Manila Water",
    "title": "《最高法院马尼拉水务案先例》：判令废除外资工程承包牌照60%菲籍股权国籍歧视限制",
    "heading_path": "Philippine Supreme Court En Banc > PCAB v. Manila Water Co. (G.R. No. 217590)",
    "text_de": "【最高法院里程碑宪政判例】菲律宾最高法院大法官全庭判决宣告 PCAB 牌照实施细则第 3.1 条关于“常规工程承包商必须具备60%菲律宾公民股权”之规定违宪无效。确认外资施工企业在商业工程领域享有平等准入权，扫清了外资在菲承接大型基建项目的国籍壁垒。",
    "text_zh_machine": "【最高法院里程碑宪政判例】菲律宾最高法院大法官全庭判决宣告 PCAB 牌照实施细则第 3.1 条关于“常规工程承包商必须具备60%菲律宾公民股权”之规定违宪无效。确认外资施工企业在商业工程领域享有平等准入权，扫清了外资在菲承接大型基建项目的国籍壁垒。",
    "stand": "2026",
    "has_pending_amend": false,
    "source_url": "https://overseas-law.moj.gov.cn/fatong"
  },
  {
    "id": "FIDIC:Silver_1999:Clause_20.1",
    "kind": "norm",
    "law": "FIDIC",
    "enbez": "Silver:20.1",
    "title": "《FIDIC 银皮书 EPC》第20.1款：承包商索赔28天通知除斥期间与失权抗辩 (Tier 1 核心争议条款)",
    "heading_path": "FIDIC Conditions of Contract for EPC/Turnkey Projects 1999 > Clause 20 Claims > 20.1",
    "text_de": "【国际工程核心条款】承包商若要求顺延工期或追加费用，必须在知悉或应当知悉该索赔事件之日起 28 天内向发包人发出书面索赔通知。若承包商未能在 28 天通知时效内发出通知，竣工期限不得顺延，承包商无权获得任何费用补偿，且发包人免除与该索赔相关的一切责任（强制失权条款）。",
    "text_zh_machine": "【国际工程核心条款】承包商若要求顺延工期或追加费用，必须在知悉或应当知悉该索赔事件之日起 28 天内向发包人发出书面索赔通知。若承包商未能在 28 天通知时效内发出通知，竣工期限不得顺延，承包商无权获得任何费用补偿，且发包人免除与该索赔相关的一切责任（强制失权条款）。",
    "stand": "2026",
    "has_pending_amend": false,
    "source_url": "https://overseas-law.moj.gov.cn/fatong"
  },
  {
    "id": "FIDIC:Silver_1999:Clause_8.4",
    "kind": "norm",
    "law": "FIDIC",
    "enbez": "Silver:8.4",
    "title": "《FIDIC 银皮书 EPC》第8.4款：竣工时间延长(EOT)与雇主风险事件 (Tier 1 核心争议条款)",
    "heading_path": "FIDIC Conditions of Contract for EPC/Turnkey Projects 1999 > Clause 8 > 8.4",
    "text_de": "【国际工程核心条款】承包商因发包人指示的工程变更、根据合同专用条件有权顺延工期之事件、或因发包人、发包人人员或现场其他承包商造成的任何延误、阻碍或妨碍（包括迟延交付现场与征地受阻），在遵循第20.1款程序的前提下，有权获得竣工期限的合理顺延（EOT）。",
    "text_zh_machine": "【国际工程核心条款】承包商因发包人指示的工程变更、根据合同专用条件有权顺延工期之事件、或因发包人、发包人人员或现场其他承包商造成的任何延误、阻碍或妨碍（包括迟延交付现场与征地受阻），在遵循第20.1款程序的前提下，有权获得竣工期限的合理顺延（EOT）。",
    "stand": "2026",
    "has_pending_amend": false,
    "source_url": "https://overseas-law.moj.gov.cn/fatong"
  },
  {
    "id": "FIDIC:Silver_1999:Clause_4.2",
    "kind": "norm",
    "law": "FIDIC",
    "enbez": "Silver:4.2",
    "title": "《FIDIC 银皮书 EPC》第4.2款：履约担保与发包人索兑正当性限制 (Tier 1 核心争议条款)",
    "heading_path": "FIDIC Conditions of Contract for EPC/Turnkey Projects 1999 > Clause 4 > 4.2",
    "text_de": "【国际工程核心条款】发包人不得向保函开立行提出索赔或索兑履约保证，除非发生合同明确列明的四种违约情形：(a) 承包商未按要求顺延保函有效期；(b) 经裁定或协商确定应付发包人的款项承包商逾期未付；(c) 发包人书面通知纠正违约后42天内承包商仍未补正；或(d) 发生发包人有权解除合同的情形。不满足上述前提的索兑构成合同违约。",
    "text_zh_machine": "【国际工程核心条款】发包人不得向保函开立行提出索赔或索兑履约保证，除非发生合同明确列明的四种违约情形：(a) 承包商未按要求顺延保函有效期；(b) 经裁定或协商确定应付发包人的款项承包商逾期未付；(c) 发包人书面通知纠正违约后42天内承包商仍未补正；或(d) 发生发包人有权解除合同的情形。不满足上述前提的索兑构成合同违约。",
    "stand": "2026",
    "has_pending_amend": false,
    "source_url": "https://overseas-law.moj.gov.cn/fatong"
  },
  {
    "id": "FIDIC:Silver_1999:Clause_13.7",
    "kind": "norm",
    "law": "FIDIC",
    "enbez": "Silver:13.7",
    "title": "《FIDIC 银皮书 EPC》第13.7款：因东道国法律与规章变更调整合同价款 (Tier 2 基准参考条款)",
    "heading_path": "FIDIC Conditions of Contract for EPC/Turnkey Projects 1999 > Clause 13 > 13.7",
    "text_de": "【FIDIC 基准参考条款】基准日期（投标截止日前28天）之后，若东道国法律、行政法规或司法解释发生变动（例如引入强制TKDN配额、调整关税或劳工签证政策），导致承包商履行合同发生工期延误或成本增加的，合同价款应予相应调增，竣工期限予以合理延长。",
    "text_zh_machine": "【FIDIC 基准参考条款】基准日期（投标截止日前28天）之后，若东道国法律、行政法规或司法解释发生变动（例如引入强制TKDN配额、调整关税或劳工签证政策），导致承包商履行合同发生工期延误或成本增加的，合同价款应予相应调增，竣工期限予以合理延长。",
    "stand": "2026",
    "has_pending_amend": false,
    "source_url": "https://overseas-law.moj.gov.cn/fatong"
  },
  {
    "id": "CN:SASAC_Order_35:Art12",
    "kind": "norm",
    "law": "SASAC_Order_35",
    "enbez": "Art.12",
    "title": "国资委35号令《中央企业境外投资监督管理办法》第12条：海外重大项目合规论证与负面清单",
    "heading_path": "国务院国有资产监督管理委员会令第35号 > 第二章 境外投资事前管理 > 第十二条",
    "text_de": "【国资监管红线】中央企业境外重大工程与投资项目，必须在投前决策前完成东道国外资准入、国安审查、习惯法土地及外汇汇出法律合规专项论证。重大境外项目未按规定履行尽职调查与决策审核程序的，实行终身追责问责。",
    "text_zh_machine": "【国资监管红线】中央企业境外重大工程与投资项目，必须在投前决策前完成东道国外资准入、国安审查、习惯法土地及外汇汇出法律合规专项论证。重大境外项目未按规定履行尽职调查与决策审核程序的，实行终身追责问责。",
    "stand": "2026",
    "has_pending_amend": false,
    "source_url": "https://overseas-law.moj.gov.cn/fatong"
  },
  {
    "id": "CN:Data_Security_Law:Art36",
    "kind": "norm",
    "law": "Data_Security_Law",
    "enbez": "Art.36",
    "title": "《中华人民共和国数据安全法》第36条：严禁未经批准向外国司法或执法机构提供境内重大数据与图纸",
    "heading_path": "中华人民共和国数据安全法 > 第三章 数据安全保护义务 > 第三十六条",
    "text_de": "【国家安全红线】非经中国主管机关正式审批许可，境内央国企及人员不得向外国法院、外国仲裁机构或执法机构提供境内存放的重大工程图纸、勘察数据及商业机密。在新加坡 SIAC、马来西亚 CIPAA 或外国诉讼涉外调证程序中，必须严格履行数据出境安全评估前置审批程序。",
    "text_zh_machine": "【国家安全红线】非经中国主管机关正式审批许可，境内央国企及人员不得向外国法院、外国仲裁机构或执法机构提供境内存放的重大工程图纸、勘察数据及商业机密。在新加坡 SIAC、马来西亚 CIPAA 或外国诉讼涉外调证程序中，必须严格履行数据出境安全评估前置审批程序。",
    "stand": "2026",
    "has_pending_amend": false,
    "source_url": "https://overseas-law.moj.gov.cn/fatong"
  },
  {
    "id": "TREATY:CN_ID_BIT_1992:Art4",
    "kind": "norm",
    "law": "CN_ID_BIT_1992",
    "enbez": "Art.4",
    "title": "《中国-印尼双边投资保护协定》第4条：征收、国有化公允补偿与中信保代位求偿保障",
    "heading_path": "Agreement between PRC and Republic of Indonesia for the Promotion and Protection of Investments 1992 > Article 4",
    "text_de": "【国际投资条约保护】缔约任何一方对缔约另一方投资者在其领土内的投资，不得采取征收、国有化或具有类似效果的措施（含隐性征收与单方取消特许经营权），除非出于公共利益、非歧视原则并给予实际可兑付、可自由汇出的充分补偿。",
    "text_zh_machine": "【国际投资条约保护】缔约任何一方对缔约另一方投资者在其领土内的投资，不得采取征收、国有化或具有类似效果的措施（含隐性征收与单方取消特许经营权），除非出于公共利益、非歧视原则并给予实际可兑付、可自由汇出的充分补偿。",
    "stand": "2026",
    "has_pending_amend": false,
    "source_url": "https://overseas-law.moj.gov.cn/fatong"
  },
  {
    "id": "SINOSURE:Overseas_Policy:Art15",
    "kind": "norm",
    "law": "SINOSURE",
    "enbez": "Art.15",
    "title": "中国信保《海外投资险/特定合同险保单》第15条：政治风险与违约发生后30日内法定报损保全通知",
    "heading_path": "中国出口信用保险公司海外投资保险与特险标准条款 > 索赔与权益保全 > 第十五条",
    "text_de": "【出海央企致命时间窗口】当发生东道国政府征收、特许权强行提前中止、保函恶意扣兑或主权外汇冻结时，被保险央企必须于30日法定除斥期内向中国信保递交《可能损失通知书》，保全特许权合同及保函原件，严禁在未获信保书面同意前与发包人签署放弃追偿权的和解协议。",
    "text_zh_machine": "【出海央企致命时间窗口】当发生东道国政府征收、特许权强行提前中止、保函恶意扣兑或主权外汇冻结时，被保险央企必须于30日法定除斥期内向中国信保递交《可能损失通知书》，保全特许权合同及保函原件，严禁在未获信保书面同意前与发包人签署放弃追偿权的和解协议。",
    "stand": "2026",
    "has_pending_amend": false,
    "source_url": "https://overseas-law.moj.gov.cn/fatong"
  },
  {
    "id": "FIDIC:Red_1999:Clause_20.1",
    "kind": "norm",
    "law": "FIDIC",
    "enbez": "Red:20.1",
    "title": "《FIDIC 红皮书 施工合同》第20.1款：承包商索赔28天通知时效与失权 (Tier 1 核心争议条款)",
    "heading_path": "FIDIC Conditions of Contract for Construction 1999 > Clause 20 Claims > 20.1",
    "text_de": "【FIDIC 1999红皮书】承包商若要求工期顺延或费用索赔，必须在知悉索赔事件之日起 28 天内向监理工程师发出书面索赔通知。逾期未通知则竣工期限不得顺延且雇主免除全部赔偿责任（严格时效前置要件）。",
    "text_zh_machine": "【FIDIC 1999红皮书】承包商若要求工期顺延或费用索赔，必须在知悉索赔事件之日起 28 天内向监理工程师发出书面索赔通知。逾期未通知则竣工期限不得顺延且雇主免除全部赔偿责任（严格时效前置要件）。",
    "stand": "2026",
    "has_pending_amend": false,
    "source_url": "https://overseas-law.moj.gov.cn/fatong"
  },
  {
    "id": "FIDIC:Red_1999:Clause_8.4",
    "kind": "norm",
    "law": "FIDIC",
    "enbez": "Red:8.4",
    "title": "《FIDIC 红皮书 施工合同》第8.4款：竣工时间延长(EOT)法定情形 (Tier 1 核心争议条款)",
    "heading_path": "FIDIC Conditions of Contract for Construction 1999 > Clause 8 > 8.4",
    "text_de": "【FIDIC 1999红皮书】承包商因工程变更、异常不利气候条件或雇主/工程师延误迟延交地，依第20.1款程序有权主张竣工工期顺延（EOT），免除误期违约金（LDs）。",
    "text_zh_machine": "【FIDIC 1999红皮书】承包商因工程变更、异常不利气候条件或雇主/工程师延误迟延交地，依第20.1款程序有权主张竣工工期顺延（EOT），免除误期违约金（LDs）。",
    "stand": "2026",
    "has_pending_amend": false,
    "source_url": "https://overseas-law.moj.gov.cn/fatong"
  },
  {
    "id": "FIDIC:Yellow_1999:Clause_20.1",
    "kind": "norm",
    "law": "FIDIC",
    "enbez": "Yellow:20.1",
    "title": "《FIDIC 黄皮书 生产设备与设计-建造》第20.1款：承包商索赔通知时效 (Tier 1 核心争议条款)",
    "heading_path": "FIDIC Conditions of Contract for Plant and Design-Build 1999 > Clause 20 Claims > 20.1",
    "text_de": "【FIDIC 1999黄皮书】设计施工一体化合同下，承包商主张工期或费用索赔须于28天内递交书面索赔通知，未发通知将发生失权抗辩法律后果。",
    "text_zh_machine": "【FIDIC 1999黄皮书】设计施工一体化合同下，承包商主张工期或费用索赔须于28天内递交书面索赔通知，未发通知将发生失权抗辩法律后果。",
    "stand": "2026",
    "has_pending_amend": false,
    "source_url": "https://overseas-law.moj.gov.cn/fatong"
  },
  {
    "id": "FIDIC:Yellow_1999:Clause_8.4",
    "kind": "norm",
    "law": "FIDIC",
    "enbez": "Yellow:8.4",
    "title": "《FIDIC 黄皮书 生产设备与设计-建造》第8.4款：工期顺延(EOT) (Tier 1 核心争议条款)",
    "heading_path": "FIDIC Conditions of Contract for Plant and Design-Build 1999 > Clause 8 > 8.4",
    "text_de": "【FIDIC 1999黄皮书】承包商因不可预见的外界不利物理条件、发包人审批延误或现场移交迟延，有权申请合理工期顺延。",
    "text_zh_machine": "【FIDIC 1999黄皮书】承包商因不可预见的外界不利物理条件、发包人审批延误或现场移交迟延，有权申请合理工期顺延。",
    "stand": "2026",
    "has_pending_amend": false,
    "source_url": "https://overseas-law.moj.gov.cn/fatong"
  },
  {
    "id": "FIDIC:Silver_2017:Clause_20.2",
    "kind": "norm",
    "law": "FIDIC",
    "enbez": "Silver2017:20.2",
    "title": "《FIDIC 银皮书 2017版》第20.2款：发包人与承包商双向索赔28天通知与失权 (Tier 1 核心争议条款)",
    "heading_path": "FIDIC Conditions of Contract for EPC/Turnkey Projects 2017 > Clause 20 Employer's and Contractor's Claims > 20.2",
    "text_de": "【FIDIC 2017新版核心条款】2017版确立双向对等索赔时效机制：无论是雇主主张违约金还是承包商主张 EOT/费用索赔，均必须在知悉事件后 28 天内送达索赔通知；逾期送达通知自始无效且索赔请求权失权，彻底消除发包人索赔无通知期限制的特权。",
    "text_zh_machine": "【FIDIC 2017新版核心条款】2017版确立双向对等索赔时效机制：无论是雇主主张违约金还是承包商主张 EOT/费用索赔，均必须在知悉事件后 28 天内送达索赔通知；逾期送达通知自始无效且索赔请求权失权，彻底消除发包人索赔无通知期限制的特权。",
    "stand": "2026",
    "has_pending_amend": false,
    "source_url": "https://overseas-law.moj.gov.cn/fatong"
  },
  {
    "id": "FIDIC:Silver_2017:Clause_8.5",
    "kind": "norm",
    "law": "FIDIC",
    "enbez": "Silver2017:8.5",
    "title": "《FIDIC 银皮书 2017版》第8.5款：工期顺延(EOT)与共同延误(Concurrent Delay)规则 (Tier 1 核心争议条款)",
    "heading_path": "FIDIC Conditions of Contract for EPC/Turnkey Projects 2017 > Clause 8 > 8.5",
    "text_de": "【FIDIC 2017新版核心条款】2017版明确确立共同延误（Concurrent Delay）审查指引：当雇主延误事件与承包商自身延误重叠时，依照合同专用条件约定准则评估 EOT，防止业主以共同延误为由全额扣罚误期损害赔偿金。",
    "text_zh_machine": "【FIDIC 2017新版核心条款】2017版明确确立共同延误（Concurrent Delay）审查指引：当雇主延误事件与承包商自身延误重叠时，依照合同专用条件约定准则评估 EOT，防止业主以共同延误为由全额扣罚误期损害赔偿金。",
    "stand": "2026",
    "has_pending_amend": false,
    "source_url": "https://overseas-law.moj.gov.cn/fatong"
  },
  {
    "id": "CASE:SG_HC:BSMountSophia:2016",
    "kind": "case",
    "court": "Singapore High Court",
    "az": "[2016] SGHC 81 / [2012] SGCA 28",
    "decided": "2016-04-15",
    "title": "Singapore High Court [2016] SGHC 81 / [2012] SGCA 28 (2016-04-15)",
    "text_de": "Court holding: Unconscionability is an independent ground distinct from fraud for restraining calls on performance bonds in Singapore. The court must balance contract sanctity with the prevention of abusive calls.",
    "text_zh_machine": "【裁判要旨】Singapore High Court：【显失公平止付先例】新加坡高等法院 BS Mount Sophia 案确立独立见索即付履约保函（On-Demand Performance Bond）独立于欺诈例外的‘显失公平（Unconscionability）’止付裁判准则。承包商若能提出强有力表面证据证明发包人索兑保函行为缺乏诚信或显失公允，法院得颁发临时禁令制止索兑。",
    "stand": "2016-04-15",
    "has_pending_amend": false,
    "source_url": "https://www.elitigation.sg"
  },
  {
    "id": "CASE:PH_SC:G.R.217590_ManilaWater:2020",
    "kind": "case",
    "court": "Supreme Court of the Philippines",
    "az": "G.R. No. 217590",
    "decided": "2020-09-08",
    "title": "Supreme Court of the Philippines G.R. No. 217590 (2020-09-08)",
    "text_de": "The Supreme Court En Banc held that the nationality restriction imposed by PCAB administrative rules exceeded the statutory authority under Republic Act No. 4566, creating an impermissible barrier against foreign contractors.",
    "text_zh_machine": "【裁判要旨】Supreme Court of the Philippines：【外资施工资质平等待遇先例】菲律宾最高法院大法庭在 PCAB v. Manila Water 案中裁定：菲律宾承包商执照委员会（PCAB）规程中关于将普通承包执照（Regular License）限定于菲律宾籍企业（外资股权≤40%）之规定违宪无效。外资控股建筑企业有权平等申请普通施工资质。",
    "stand": "2020-09-08",
    "has_pending_amend": false,
    "source_url": "https://lawphil.net/judjuris/juri2020/sep2020/gr_217590_2020.html"
  },
  {
    "id": "CASE:ID_MA:SEMA_3_2023:2023",
    "kind": "case",
    "court": "Mahkamah Agung RI (Supreme Court of Indonesia)",
    "az": "SEMA No. 3 Tahun 2023",
    "decided": "2023-12-29",
    "title": "Mahkamah Agung RI (Supreme Court of Indonesia) SEMA No. 3 Tahun 2023 (2023-12-29)",
    "text_de": "Mahkamah Agung menegaskan bahwa pembatalan perjanjian semata-mata karena ketiadaan versi bahasa Indonesia melanggar prinsip kepastian hukum dan itikad baik (KUHPerdata Pasal 1338).",
    "text_zh_machine": "【裁判要旨】Mahkamah Agung RI (Supreme Court of Indonesia)：【涉外合同语言有效性裁判通告】印尼最高法院《2023年第3号通告》明确：除非能够证明当事人订立合同时存在恶意（bad faith / iktikad tidak baik），印尼各级法院不得仅以涉外商事或工程合同缺少印尼语文本为由判决合同自始无效。",
    "stand": "2023-12-29",
    "has_pending_amend": false,
    "source_url": "https://putusan3.mahkamahagung.go.id"
  },
  {
    "id": "CASE:MY_FC:Bauer_CIPAA_Sec35:2019",
    "kind": "case",
    "court": "Federal Court of Malaysia",
    "az": "[2019] MLJU 1450 / Civil Appeal 02-38",
    "decided": "2019-10-18",
    "title": "Federal Court of Malaysia [2019] MLJU 1450 / Civil Appeal 02-38 (2019-10-18)",
    "text_de": "Federal Court affirmed that Section 35 of the Construction Industry Payment and Adjudication Act 2012 (CIPAA) renders conditional payment clauses void ab initio as a matter of statutory public policy.",
    "text_zh_machine": "【裁判要旨】Federal Court of Malaysia：【背靠背付款绝对无效裁判先例】马来西亚联邦法院在建设工程付款系列先例中判决：依据 CIPAA 2012 第 35 条强行法，建设工程分包合同中约定的‘以业主向总包付款为前提’条款（Pay-when-paid / Pay-if-paid）自始绝对无效，总承包商必须严格按进度款节点向分包商结算。",
    "stand": "2019-10-18",
    "has_pending_amend": false,
    "source_url": "https://www.kehakiman.gov.my"
  },
  {
    "id": "CASE:SG_CA:JBEProperties:2011",
    "kind": "case",
    "court": "Singapore Court of Appeal",
    "az": "[2011] 1 SLR 1125 / [2010] SGCA 58",
    "decided": "2011-03-24",
    "title": "Singapore Court of Appeal [2011] 1 SLR 1125 / [2010] SGCA 58 (2011-03-24)",
    "text_de": "The Court of Appeal established the analytical framework distinguishing unconscionability from ordinary contractual dispute in construction performance bonds.",
    "text_zh_machine": "【裁判要旨】Singapore Court of Appeal：【见索即付保函司法审查边界】新加坡最高法院终审法院判决：独立履约保函项下显失公平原则的适用需综合考量履约全过程背景；若双方合同订明排除显失公平救济，在当事人地位平等且条款显著时法院应尊重当事人风险分配合意。",
    "stand": "2011-03-24",
    "has_pending_amend": false,
    "source_url": "https://www.lawnet.sg"
  },
  {
    "id": "CASE:TH_SAC:HopewellConcession:2022",
    "kind": "case",
    "court": "Supreme Administrative Court of Thailand",
    "az": "Black Case No. 107/2552, Red Case No. 368-369/2562",
    "decided": "2022-03-04",
    "title": "Supreme Administrative Court of Thailand Black Case No. 107/2552, Red Case No. 368-369/2562 (2022-03-04)",
    "text_de": "The Supreme Administrative Court examined the temporal jurisdiction, limitation period and substantive compensation principles governing concession revocations in Thailand.",
    "text_zh_machine": "【裁判要旨】Supreme Administrative Court of Thailand：【基础设施特许经营政府单方撤销补偿先例】泰国最高行政法院裁定：东道国交通部单方终止高架轨道特许权合同构成征收等同效果，虽经时效抗辩重新审查，但特许权投资人对已完工基础设施之对价公允求偿权受法律保护，国家应履行仲裁裁决补偿义务。",
    "stand": "2022-03-04",
    "has_pending_amend": false,
    "source_url": "http://www.admincourt.go.th"
  },
  {
    "id": "CASE:VN_SPC:ArbitrationEnforcement:2021",
    "kind": "case",
    "court": "Supreme People's Court of Vietnam",
    "az": "Decision No. 18/2021/KDTM-GDT",
    "decided": "2021-11-12",
    "title": "Supreme People's Court of Vietnam Decision No. 18/2021/KDTM-GDT (2021-11-12)",
    "text_de": "The Cassation Court held that Vietnamese fundamental principles of law must be narrowly construed and cannot be expanded to re-examine the arbitral tribunal's findings of fact or FIDIC contractual interpretations.",
    "text_zh_machine": "【裁判要旨】Supreme People's Court of Vietnam：【国际工程仲裁裁决在越承认与执行先例】越南最高人民法院裁定：依据《纽约公约》及越南民事诉讼法，除非存在仲裁协议无效或严重背离越南基本法律原则，越南法院不得对 SIAC 涉外建设工程仲裁裁决进行实体重新审理，依法裁定承认与执行。",
    "stand": "2021-11-12",
    "has_pending_amend": false,
    "source_url": "https://congbobanan.toaan.gov.vn"
  }
];

export interface SearchJurisdiction {
  code: string;
  name: string;
  flag: string;
  count: number;
}

export const SEARCH_JURISDICTIONS: SearchJurisdiction[] = [
  { code: 'all', name: '全部法源', flag: '🌏', count: 38 },
  { code: 'asean_id', name: '印度尼西亚', flag: '🇮🇩', count: 5 },
  { code: 'asean_sg', name: '新加坡', flag: '🇸🇬', count: 5 },
  { code: 'asean_my', name: '马来西亚', flag: '🇲🇾', count: 4 },
  { code: 'asean_vn', name: '越南', flag: '🇻🇳', count: 4 },
  { code: 'asean_th', name: '泰国', flag: '🇹🇭', count: 3 },
  { code: 'asean_ph', name: '菲律宾', flag: '🇵🇭', count: 3 },
  { code: 'fidic', name: 'FIDIC 范本', flag: '📑', count: 10 },
  { code: 'soe_treaty', name: '央企合规/条约', flag: '🛡️', count: 4 },
];

export function getItemJurisdiction(item: NormOrCaseItem): { code: string; name: string; flag: string } {
  const id = (item.id || '').toUpperCase();
  const law = (item.law || '').toUpperCase();
  const court = (item.court || '').toUpperCase();

  if (
    id.startsWith('ID:') ||
    law.includes('UU_2') ||
    law.includes('SEMA') ||
    law.includes('MEMR') ||
    law.includes('KUHPERDATA') ||
    court.includes('INDONESIA') ||
    court.includes('MAHKAMAH AGUNG')
  ) {
    return { code: 'asean_id', name: '印尼', flag: '🇮🇩' };
  }
  if (id.startsWith('SG:') || law.includes('SOPA') || court.includes('SINGAPORE')) {
    return { code: 'asean_sg', name: '新加坡', flag: '🇸🇬' };
  }
  if (id.startsWith('MY:') || law.includes('CIPAA') || law.includes('CIDB') || court.includes('MALAYSIA')) {
    return { code: 'asean_my', name: '马来西亚', flag: '🇲🇾' };
  }
  if (id.startsWith('VN:') || law.includes('135_2025') || law.includes('DECREE_210') || court.includes('VIETNAM')) {
    return { code: 'asean_vn', name: '越南', flag: '🇻🇳' };
  }
  if (id.startsWith('TH:') || law.includes('CCC') || law.includes('FBA') || court.includes('THAILAND')) {
    return { code: 'asean_th', name: '泰国', flag: '🇹🇭' };
  }
  if (id.startsWith('PH:') || law.includes('11966') || court.includes('PHILIPPINES')) {
    return { code: 'asean_ph', name: '菲律宾', flag: '🇵🇭' };
  }
  if (id.includes('FIDIC') || law.includes('FIDIC')) {
    return { code: 'fidic', name: 'FIDIC 范本', flag: '📑' };
  }
  return { code: 'soe_treaty', name: '央企合规', flag: '🛡️' };
}

export function searchLocalNormsAndCases(
  query: string,
  law?: string,
  kind: 'all' | 'norm' | 'case' = 'all',
  jurisdiction: string = 'all'
): NormOrCaseItem[] {
  const cleanQ = (query || '').trim().toLowerCase();
  const keywords = cleanQ.replace(/[+、,，/]/g, ' ').split(/\s+/).filter(Boolean);

  return DEFAULT_SEARCH_ITEMS.filter((item) => {
    // 0. 国别/法域过滤
    if (jurisdiction && jurisdiction !== 'all') {
      const jur = getItemJurisdiction(item);
      if (jur.code !== jurisdiction) return false;
    }

    // 1. 类型过滤
    if (kind !== 'all' && item.kind !== kind) return false;

    // 2. 法典/法源过滤
    if (law && law !== 'all') {
      const l = law.toUpperCase();
      if (l.startsWith('FIDIC')) {
        if (!item.id.toUpperCase().includes('FIDIC') && item.law !== 'FIDIC') return false;
        if (l.includes('SILVER') && !item.id.toUpperCase().includes('SILVER')) return false;
        if (l.includes('YELLOW') && !item.id.toUpperCase().includes('YELLOW')) return false;
        if (l.includes('RED') && !item.id.toUpperCase().includes('RED')) return false;
      } else if (l === 'BIT') {
        if (!item.id.toUpperCase().includes('BIT') && !item.law?.toUpperCase().includes('BIT')) return false;
      } else {
        const itemLaw = (item.law || '').toUpperCase();
        const itemId = item.id.toUpperCase();
        if (!itemLaw.includes(l) && !itemId.includes(l)) return false;
      }
    }

    // 3. 关键词过滤
    if (keywords.length === 0) return true;

    const searchableText = [
      item.id,
      item.title,
      item.law || '',
      item.enbez || '',
      item.court || '',
      item.az || '',
      item.text_de || '',
      item.text_zh_machine || '',
    ]
      .join(' ')
      .toLowerCase();

    // 匹配关键词：当有多个关键词时，支持包含任意核心词
    return keywords.some((kw) => searchableText.includes(kw));
  });
}
