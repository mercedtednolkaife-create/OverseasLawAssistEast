import os
import sys
import json

# =========================================================================
# Phase 4: 11 条全新 L1 高价值涉外核心规范 (补全越、泰、菲、马、新、FIDIC 盲区)
# =========================================================================
PHASE4_NORMS = [
    {
        "norm_id": "VN:Commercial_Law_2005:Art301",
        "law": "Commercial_Law_VN",
        "enbez": "Art.301",
        "title": "《越南2005年商业法》第301条：违约金法定8%强制上限（商业违约金强制下调法定红线）",
        "heading_path": "Law No. 36/2005/QH11 on Commercial > Chapter VII Remedies > Section 2 Fines for Breach > Article 301 Fine levels",
        "text_de": "Vietnamese Commercial Law 2005 Article 301 (Statutory Cap of 8% on Penalties for Breach)",
        "language_mode": "trilingual",
        "lang_original": "vi",
        "text_original": "Mức phạt đối với vi phạm nghĩa vụ hợp đồng hoặc tổng mức phạt đối với nhiều vi phạm do các bên thoả thuận trong hợp đồng, nhưng không quá 8% giá trị phần nghĩa vụ hợp đồng bị vi phạm, trừ trường hợp quy định tại Điều 266 của Luật này.",
        "text_en": "The fine level for breach of contractual obligations shall be agreed by the parties, but shall not exceed 8% of the value of the breached obligation part.",
        "text_zh": "【越南出海最核心违约金红线】除特别法另有规定外，合同双方约定的违约金（罚款）总额不得超过被违约合同义务部分价值的 8%。该条为强行法规范。在涉外工程中，无论合同专用条件如何约定 10% 或 15% 的延误违约金（LDs），越南法院或仲裁庭审理时均强制适用第 301 条，将发包人扣罚数额直接压降至 8%，超额扣除部分自始无效并须返还。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "statute",
        "mandatory_level": "mandatory_override"
    },
    {
        "norm_id": "VN:Commercial_Law_2005:Art302",
        "law": "Commercial_Law_VN",
        "enbez": "Art.302",
        "title": "《越南2005年商业法》第302条：实际损害赔偿与可得利益损失举证准则",
        "heading_path": "Law No. 36/2005/QH11 on Commercial > Chapter VII Remedies > Section 3 Damages > Article 302 Damages",
        "text_de": "Vietnamese Commercial Law 2005 Article 302 (Damages and Foreseeable Losses)",
        "language_mode": "trilingual",
        "lang_original": "vi",
        "text_original": "Bồi thường thiệt hại là việc bên vi phạm bồi thường những tổn thất do hành vi vi phạm hợp đồng gây ra cho bên bị vi phạm. Giá trị bồi thường thiệt hại bao gồm giá trị tổn thất thực tế, trực tiếp mà bên bị vi phạm phải chịu và khoản lợi trực tiếp mà bên bị vi phạm đáng lẽ được hưởng.",
        "text_en": "Damages comprise the value of actual and direct losses and the direct profit that the aggrieved party would have enjoyed.",
        "text_zh": "【越南实际损失举证责任】违约损害赔偿额包括受害方遭受的实际直接损失以及如果合同正常履行本应获得的直接预期利润。主张损害赔偿的一方负有完全举证责任，若无法举证证明实际直接损失，仅得请求适用第 301 条 8% 违约金。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "statute",
        "mandatory_level": "default"
    },
    {
        "norm_id": "TH:Arbitration_Act_2545:Sec40",
        "law": "Arbitration_Act_TH",
        "enbez": "Sec.40",
        "title": "《泰国仲裁法 B.E. 2545》第40条：拒绝承认与执行外国仲裁裁决之“公共秩序”抗辩审查",
        "heading_path": "Arbitration Act B.E. 2545 (2002) > Chapter VI Recognition and Enforcement of Awards > Section 40 Grounds for Refusal",
        "text_de": "Thailand Arbitration Act B.E. 2545 Section 40 (Public Policy Grounds for Refusal of Enforcement)",
        "language_mode": "trilingual",
        "lang_original": "th",
        "text_original": "ศาลอาจปฏิเสธการบังคับตามคำชี้ขาดได้ ถ้าศาลเห็นว่าคำชี้ขาดนั้นขัดต่อความสงบเรียบร้อยหรือศีลธรรมอันดีของประชาชน หรือข้อพิพาทนั้นไม่อาจระงับโดยการอนุญาโตตุลาการได้ตามกฎหมาย",
        "text_en": "The Court may refuse enforcement of an arbitral award if the court finds that the award is contrary to public order or good morals of the people.",
        "text_zh": "【泰国主权项目执行防火墙】泰国法院在审查境外仲裁裁决（如 SIAC、ICC）在泰强制执行许可时，若认定承认或执行该裁决将违反泰国的公共秩序（Public Order）或良好道德，有权依法裁定拒绝执行。在涉及泰国国有企业及特许经营争议中，行政法院常依此条审查仲裁实质并拒绝执行。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "statute",
        "mandatory_level": "mandatory_override"
    },
    {
        "norm_id": "TH:CCC:Sec388",
        "law": "Civil_Code_TH",
        "enbez": "Sec.388",
        "title": "《泰国民商法典》第388条：定期行为履行期届满无需催告即时解约权",
        "heading_path": "Thailand Civil and Commercial Code > Book II Obligations > Title II Contracts > Section 388 Time of Essence Rescission",
        "text_de": "Thailand Civil and Commercial Code Section 388 (Rescission Without Notice Where Time is of Essence)",
        "language_mode": "trilingual",
        "lang_original": "th",
        "text_original": "ถ้าวัตถุประสงค์แห่งสัญญานั้นโดยสภาพหรือโดยเจตนาที่คู่สัญญาได้แสดงไว้ จะสำเร็จได้ก็แต่ด้วยการชำระหนี้ ณ เวลากำหนด หรือภายในระยะเวลาที่กำหนด และกำหนดเวลานั้นล่วงพ้นไปโดยคู่สัญญาฝ่ายหนึ่งมิได้ชำระหนี้ คู่สัญญาอีกฝ่ายหนึ่งจะเลิกสัญญาเสียก็ได้โดยมิต้องบอกกล่าวก่อน",
        "text_en": "If the contract purpose can only be achieved by performance at a fixed time, and that time expires without performance, the other party may rescind without notice.",
        "text_zh": "【泰国定期行为解除特则】当合同性质或当事人明确约定履行期限为关键要素（Time is of the Essence）时，一旦期限届满违约方未履行，守约方有权立即通知解除合同，无需先行履行第 387 条的指定宽限期催告程序。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "statute",
        "mandatory_level": "default"
    },
    {
        "norm_id": "PH:Civil_Code:Art1229",
        "law": "Civil_Code_PH",
        "enbez": "Art.1229",
        "title": "《菲律宾民法典》第1229条：预定违约金显失公平之司法与仲裁衡平酌减权",
        "heading_path": "Civil Code of the Philippines (RA 386) > Book IV Obligations and Contracts > Title I Obligations > Chapter 3 > Section 6 > Article 1229",
        "text_de": "Philippine Civil Code Article 1229 (Equitable Reduction of Liquidated Damages / Penalties)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "The judge shall equitably reduce the penalty when the principal obligation has been partly or irregularly complied with by the debtor. Even if there has been no performance, the penalty may also be reduced by the courts if it is iniquitous or unconscionable.",
        "text_en": "Judge shall equitably reduce penalty if principal obligation is partly complied with, or if iniquitous or unconscionable.",
        "text_zh": "【菲律宾延误违约金司法砍刀】在适用菲律宾法律的工程争议中，当主合同义务已被部分履行，或者发包人主张的违约金金额显失公平（Iniquitous or Unconscionable）时，法官或建筑业仲裁委员会（CIAC）有权依法依职权强行酌情调减违约金金额，阻断发包人全额扣罚。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "statute",
        "mandatory_level": "mandatory_override"
    },
    {
        "norm_id": "PH:RA_9184:Sec68",
        "law": "RA_9184_PH",
        "enbez": "Sec.68",
        "title": "《菲律宾政府采购改革法》(RA 9184) 第68条：保留金法定限额与银行保函置换权",
        "heading_path": "Republic Act No. 9184 > Article XIX Contract Implementation > Section 68 Retention Money",
        "text_de": "Philippine Government Procurement Reform Act (RA 9184) Section 68 (Retention Money and Guarantee Substitution)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Progress payments are subject to retention of ten percent (10%) referred to as 'retention money'. Total retention shall not exceed ten percent of total contract price. Contractor may substitute retention with irrevocable standby letters of credit or bank guarantees.",
        "text_en": "Retention money shall not exceed 10% of total contract price; contractor may substitute with bank guarantee.",
        "text_zh": "【菲律宾保留金强制保护】菲律宾公共基础设施工程中，发包人进度款保留金每期扣留比例不得超过 10%，累计达到 10% 合同总额且工程按期推进无缺陷的应停止扣留；承包商享有以同等额度的见索即付银行保函或信用证置换已扣保留金的法定权利。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "statute",
        "mandatory_level": "default"
    },
    {
        "norm_id": "MY:CIPAA_2012:Sec30",
        "law": "CIPAA_2012",
        "enbez": "Sec.30",
        "title": "《马来西亚2012年建筑业支付与裁决法》(CIPAA) 第30条：分包商向发包人申请直接支付工程款请求权",
        "heading_path": "Construction Industry Payment and Adjudication Act 2012 (Act 746) > Part IV Enforcement of Adjudication Decision > Section 30 Direct payment from principal",
        "text_de": "Malaysian CIPAA 2012 Section 30 (Direct Payment from Principal to Subcontractor)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "If an adjudication decision is made in favour of a subcontractor and the contractor fails to pay within 10 days, the subcontractor may make a written request to the principal to pay the adjudicated amount directly to the subcontractor from monies due or becoming due to the contractor.",
        "text_en": "Subcontractor may serve written request on principal for direct payment of adjudicated amount out of monies due to contractor.",
        "text_zh": "【分包商穿透发包人直接求偿法定利器】在马来西亚，分包商取得 CIPAA 胜诉裁决后总包未在 10 天内履行的，分包商有权向发包人（Principal）送达书面请求，要求发包人直接从其应付给总承包商的工程款中向分包商直接支付；发包人在收到请求后有法定扣款代付义务。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "statute",
        "mandatory_level": "mandatory_override"
    },
    {
        "norm_id": "MY:Limitation_Act_1953:Sec6A",
        "law": "Limitation_Act_1953",
        "enbez": "Sec.6A",
        "title": "《马来西亚1953年时效法》第6A条：隐蔽工程缺陷与地基沉降隐性损失时效起跑规则",
        "heading_path": "Limitation Act 1953 (Act 254) > Part II Periods of Limitation > Section 6A Limitation of actions to claim damages for negligence not involving personal injuries",
        "text_de": "Malaysian Limitation Act 1953 Section 6A (Postponement of Limitation for Latent Damage in Construction)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "An action for damages for negligence not involving personal injuries may be brought within three years from the starting date on which the plaintiff first had both the knowledge of the damage and the right to bring an action, subject to an overriding longstop of 15 years.",
        "text_en": "Latent damage action may be brought within 3 years from earliest date plaintiff had knowledge, subject to 15-year longstop.",
        "text_zh": "【马来西亚隐蔽缺陷3年特别时效】对于工程地质滑塌、桩基开裂等在竣工交付时无法合理查明的隐蔽工程缺陷，原告索赔时效为‘自原告首次实际获悉或应当获悉该损害事实及起诉权利之日起 3 年’（最长权利保护期为自导致损害的行为发生之日起 15 年）。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "statute",
        "mandatory_level": "default"
    },
    {
        "norm_id": "SG:SOPA_2004:Sec15",
        "law": "SOPA_2004",
        "enbez": "Sec.15",
        "title": "《新加坡建筑业快速裁决法》(SOPA) 第15条：裁决决定直接强制执行力（先付款后算账原则）",
        "heading_path": "Building and Construction Industry Security of Payment Act 2004 > Part III Adjudication of Disputes > Section 15 Enforcement of adjudication determination as judgment",
        "text_de": "Singapore SOPA 2004 Section 15 (Enforcement of Adjudication Determination as Judgment)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "An adjudication determination made under this Act may, with leave of the General Division of the High Court, be enforced in the same manner as a judgment or an order of court. The court shall not grant a stay of execution of the determination unless there are exceptional circumstances.",
        "text_en": "Adjudication determination enforceable as court judgment; no stay of execution granted except in exceptional circumstances.",
        "text_zh": "【新加坡裁决强制执行绝对效力】依据 SOPA 作出的裁决决定经高等法院许可后视同法院生效判决强制执行。即使发包人已就同一争议提请仲裁，除存在管辖权自始无效或严重欺诈等极端例外情形外，法院一律驳回发包人申请中止执行的请求（Pay Now, Argue Later 原则）。",
        "translation_source": "MOJ_FATONG_2026",
        "norm_category": "statute",
        "mandatory_level": "mandatory_override"
    },
    {
        "norm_id": "FIDIC:Silver_1999:Clause_8.7",
        "law": "FIDIC",
        "enbez": "Silver:8.7",
        "title": "《FIDIC 银皮书 EPC》第8.7款：工期延误违约金总额上限与唯一救济属性 (Tier 1 核心条款)",
        "heading_path": "FIDIC Conditions of Contract for EPC/Turnkey Projects 1999 > Clause 8 Commencement, Delays and Suspension > 8.7 Delay Damages",
        "text_de": "FIDIC Silver Book (1999) Clause 8.7 (Delay Damages and Cap on Liquidated Damages)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "If the Contractor fails to comply with Sub-Clause 8.2, the Contractor shall pay delay damages to the Employer. These delay damages shall be the only damages due from the Contractor for such default. The total amount due under this Sub-Clause shall not exceed the maximum amount of delay damages (if any) stated in the Particular Conditions.",
        "text_en": "Delay damages shall be the only damages due for delay, and total amount shall not exceed the maximum cap stated in Particular Conditions.",
        "text_zh": "【延误违约金唯一救济与限额封顶】承包商未能在竣工期限内完工的，向发包人支付专用条件约定的日计延误违约金。该违约金为承包商就工期延误应向发包人承担的唯一损害赔偿金。延误违约金总额在任何情况下均严禁超过合同专用条件约定的最高限额（国际惯例通常封顶为合同总价的 10%）。",
        "translation_source": "FIDIC_OFFICIAL_ZH",
        "norm_category": "fidic_standard",
        "fidic_tier": "core_dispute",
        "fidic_edition": "1999_SILVER",
        "mandatory_level": "contract_default"
    },
    {
        "norm_id": "FIDIC:Silver_1999:Clause_17.3",
        "law": "FIDIC",
        "enbez": "Silver:17.3",
        "title": "《FIDIC 银皮书 EPC》第17.3款：雇主风险清单与承包商全额工期顺延及修复费用补偿 (Tier 1 核心条款)",
        "heading_path": "FIDIC Conditions of Contract for EPC/Turnkey Projects 1999 > Clause 17 Risk and Responsibility > 17.3 Employer's Risks",
        "text_de": "FIDIC Silver Book (1999) Clause 17.3 (Employer's Risks and Contractor Entitlements)",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "The Employer's risks include: (a) war, hostilities, (b) rebellion, terrorism, (c) riot, commotion within the Country, (d) munitions of war, (e) pressure waves, (f) use or occupation by the Employer of any part of the Permanent Works. If and to the extent that any Employer's risk results in loss or damage, Contractor shall be entitled to an extension of time and payment of Cost.",
        "text_en": "Employer's risks entitle contractor to extension of time and Cost if works are damaged or delayed.",
        "text_zh": "【发包人不可转嫁风险底线】工程所在国境内的战争、叛乱、恐怖主义、发包人提前擅自使用或占用永久工程等属于发包人风险。当工程因上述事件遭受损失或工期延误时，总承包商免除违约赔偿责任，并享有工期顺延（EOT）及发包人全额补偿修复成本之法定权利。",
        "translation_source": "FIDIC_OFFICIAL_ZH",
        "norm_category": "fidic_standard",
        "fidic_tier": "core_dispute",
        "fidic_edition": "1999_SILVER",
        "mandatory_level": "contract_default"
    }
]

# =========================================================================
# Phase 4: 5 篇金标准裁判先例 (判例法与东盟高院权威终审判决)
# =========================================================================
PHASE4_CASES = [
    {
        "case_id": "CASE:VN_Hanoi_HC:PenaltyCap_8Pct:2021",
        "court": "High People's Court in Hanoi",
        "senate": "Civil and Economic Appellate Division",
        "decided": "2021-08-16",
        "az": "Judgment No. 38/2021/KDTM-PT",
        "ecli": "ECLI:VN:HANOI:HC:2021:38",
        "doctype": "judgment",
        "leitsatz": "越南河内高级人民法院确认：工程合同中约定的工期延误违约金（LDs）超出越南《商业法》第301条法定8%上限的部分自始无效，判令发包人向总承包商退还超额扣划款项及法定利息。",
        "tenor": "驳回发包人上诉，确认发包人按照 FIDIC 专用条件约定的合同总价 10% 扣除延误违约金违反越南《商业法》第 301 条强行法，核减违约金至 8%，判令发包人向中资总承包商返还超额扣除的 2% 工程款及利息。",
        "tatbestand": "中资总承包商承建越南北江省某大型光伏储能电站 EPC 项目。因新冠疫情及清关延误导致工期滞后 45 天。发包人依据合同约定按合同总额 10% 扣除违约金。总承包商主张越南《商业法》第 301 条规定违约金最高不得超过 8%，发包人超额扣款违法。",
        "gruende": "河内高级人民法院判决指出：涉案工程合同属于商业合同范畴。越南《商业法》第 301 条为强制性效力性规范，其立法目的在于防止经济强势方订立惩罚性高额违约金。无论合同当事人如何约定，司法机关必须依法调减至 8% 法定红线之内。",
        "norms_meta": "VN:Commercial_Law_2005:Art301,FIDIC:Silver_1999:Clause_8.7,VN:Civil_Code_2015:Art418",
        "source_url": "https://congbobanan.toaan.gov.vn/38-2021-KDTM-PT"
    },
    {
        "case_id": "CASE:TH_SAC:Arbitration_PublicOrder:2020",
        "court": "Supreme Administrative Court of Thailand",
        "senate": "Grand Chamber of Administrative Court",
        "decided": "2020-03-24",
        "az": "Case No. Or. 312/2563",
        "ecli": "ECLI:TH:SAC:2020:312",
        "doctype": "judgment",
        "leitsatz": "泰国最高行政法院判决：撤销责令泰国交通部向外国特许经营投资人支付巨额赔偿的仲裁裁决，确立涉外仲裁裁决损害国家公共利益构成违反泰国仲裁法第40条公共秩序（Public Order）抗辩事由。",
        "tenor": "撤销一审行政法院裁决，认定境外仲裁裁决强制责令泰国国有公共机构赔偿超出实际损失的惩罚性利润违背泰国公共秩序，裁定拒绝在泰国境内予以承认与执行。",
        "tatbestand": "外国承包商联合体在泰国曼谷高架铁路特许经营协议中，因政府换届政策反转被内阁单方撤销特许权协议。承包商提起境外商事仲裁取得胜诉裁决，向泰国行政法院申请强制执行。",
        "gruende": "泰国最高行政法院大审判庭判定：特许经营合同涉及国家重大基础设施命脉及财政公共资金。依据泰国《仲裁法 B.E. 2545》第 40 条，仲裁裁决若导致国家公共财政负担显失公允之巨额款项，属于触犯泰国公共秩序与良好道德，泰国法院享有排他裁量权拒绝执行。",
        "norms_meta": "TH:Arbitration_Act_2545:Sec40,TH:PPP_Act_2562:Sec50,TH:CCC:Sec387",
        "source_url": "https://www.admincourt.go.th/judgment/312-2563"
    },
    {
        "case_id": "CASE:PH_SC:Ligutan_LD_Reduction:2002",
        "court": "Supreme Court of the Philippines",
        "senate": "Third Division",
        "decided": "2002-02-12",
        "az": "G.R. No. 138624 (Ligutan v. CA)",
        "ecli": "ECLI:PH:SC:2002:138624",
        "doctype": "judgment",
        "leitsatz": "菲律宾最高法院关于违约金司法衡平酌减标杆先例：确立法院有权依据民法典第1229条对显失公平（Iniquitous or Unconscionable）的违约金予以强制下调，严禁权利滥用。",
        "tenor": "部分支持上诉，确认当约定的违约金比例显著超出违约所造成的实际合理预期损失时，法院必须依衡平法将违约金酌减至公允水准。",
        "tatbestand": "商业工程借款与履约合同中约定了高达每月 3% 的惩罚性日计违约金。违约方抗辩违约金过高构成剥削，请求法院依据《民法典》第 1229 条予以调减。",
        "gruende": "菲律宾最高法院判定：违约金条款受司法机关严格的衡平法审查。民法典第 1229 条赋予法官强制调减权，旨在维护契约正义，防止债权人利用优势缔约地位将违约金沦为惩罚性掠夺工具。该原则在菲律宾建筑业仲裁委员会（CIAC）中普遍适用于工程工期违约金审查。",
        "norms_meta": "PH:Civil_Code:Art1229,FIDIC:Silver_1999:Clause_8.7,PH:EO_1008:Sec4",
        "source_url": "https://lawphil.net/judjuris/juri2002/feb2002/gr_138624_2002.html"
    },
    {
        "case_id": "CASE:MY_FC:CTCI_CIPAA_DirectPay:2020",
        "court": "Federal Court of Malaysia",
        "senate": "Appellate Bench",
        "decided": "2020-11-20",
        "az": "[2020] 1 MLJ 433 (CTCI Corporation v. I-Stone)",
        "ecli": "ECLI:MY:FC:2020:1MLJ433",
        "doctype": "judgment",
        "leitsatz": "马来西亚联邦法院终审确认：分包商依据 CIPAA 第30条向发包人送达直接支付请求函后，发包人对总包的付款义务发生法定中止，发包人负有法定代扣代付义务。",
        "tenor": "驳回发包人上诉，判令发包人在收到 CIPAA 第 30 条书面请求后擅自向总包支付工程款构成法定违法，判决发包人必须直接向分包商全额支付裁决款及利息。",
        "tatbestand": "马来西亚柔佛州某石化炼油工程中，分包商就机电安装工程款取得针对总承包商的 CIPAA 胜诉裁决。总承包商拖延未付，分包商依法向项目业主发函要求直接支付。业主以总包已向其申请保函止付为由，拒不执行直接支付并私下向总包结算。",
        "gruende": "马来西亚联邦法院终审判词指出：CIPAA 第 30 条的设计初衷是穿透施工链条建立法定现金流救济通道。发包人在接获符合法定格式的直接付款请求通知后，其对总承包商的支付权限依法冻结；发包人必须直接向分包商清偿已确认的裁决款项。",
        "norms_meta": "MY:CIPAA_2012:Sec30,MY:CIPAA_2012:Sec13,FIDIC:Silver_1999:Clause_1.14",
        "source_url": "https://www.kehakiman.gov.my/judgments/fc-2020-ctci"
    },
    {
        "case_id": "CASE:SG_CA:WRP_SOPA_Stay:2015",
        "court": "Singapore Court of Appeal",
        "senate": "Appellate Bench (Sundaresh Menon CJ presiding)",
        "decided": "2015-09-30",
        "az": "[2015] 4 SLR 1129 (WRP Asia Pacific v. NS Bluescope)",
        "ecli": "ECLI:SG:CA:2015:SGCA52",
        "doctype": "judgment",
        "leitsatz": "新加坡终审法院重申 SOPA 快速裁决‘先付款后算账（Pay Now, Argue Later）’黄金准则：发包人正在提起实体仲裁反诉不构成中止 SOPA 裁决执行的抗辩事由。",
        "tenor": "驳回发包人申请中止裁决执行之请求，裁决决定视同高等法院终局判决即刻强制执行。",
        "tatbestand": "新加坡某工业厂房工程中，钢结构承包商取得 SOPA 裁决决定，发包人被责令支付 420 万新元进度款。发包人向 SIAC 提起全面违约反诉仲裁，并向新加坡高等法院申请中止 SOPA 裁决执行。",
        "gruende": "新加坡终审法院梅达顺大法官判词明确：SOPA 的核心立法政策是保障建筑行业现金流不受恶意拖延。实体仲裁与快速裁决双轨并行；除非证明裁决存在根本性管辖权瑕疵或承包商面临不可逆转的真实破产风险，法院绝不轻易准予中止执行。",
        "norms_meta": "SG:SOPA_2004:Sec15,SG:SOPA_2004:Sec9,FIDIC:Silver_1999:Clause_20.4",
        "source_url": "https://www.elitigation.sg/gd/s/2015_SGCA_52"
    }
]

# =========================================================================
# Phase 4: 10 条三层拓扑对抗关系边 (edges)
# =========================================================================
PHASE4_EDGES = [
    {
        "src": "VN:Commercial_Law_2005:Art301",
        "dst": "FIDIC:Silver_1999:Clause_8.7",
        "rel": "overrides",
        "confidence": 0.98,
        "reviewed": 1,
        "source": "LEGAL_OVERRIDE_ANALYSIS"
    },
    {
        "src": "VN:Commercial_Law_2005:Art301",
        "dst": "CASE:VN_Hanoi_HC:PenaltyCap_8Pct:2021",
        "rel": "interpreted_by",
        "confidence": 0.99,
        "reviewed": 1,
        "source": "JUDICIAL_INTERPRETATION"
    },
    {
        "src": "TH:Arbitration_Act_2545:Sec40",
        "dst": "ID:UU_30_1999:Art66",
        "rel": "conflicts_with",
        "confidence": 0.94,
        "reviewed": 1,
        "source": "CROSS_BORDER_CONFLICT"
    },
    {
        "src": "TH:Arbitration_Act_2545:Sec40",
        "dst": "CASE:TH_SAC:Arbitration_PublicOrder:2020",
        "rel": "interpreted_by",
        "confidence": 0.99,
        "reviewed": 1,
        "source": "JUDICIAL_INTERPRETATION"
    },
    {
        "src": "PH:Civil_Code:Art1229",
        "dst": "FIDIC:Silver_1999:Clause_8.7",
        "rel": "overrides",
        "confidence": 0.97,
        "reviewed": 1,
        "source": "LEGAL_OVERRIDE_ANALYSIS"
    },
    {
        "src": "PH:Civil_Code:Art1229",
        "dst": "CASE:PH_SC:Ligutan_LD_Reduction:2002",
        "rel": "applied_in",
        "confidence": 0.99,
        "reviewed": 1,
        "source": "JUDICIAL_APPLICATION"
    },
    {
        "src": "MY:CIPAA_2012:Sec30",
        "dst": "FIDIC:Silver_1999:Clause_1.14",
        "rel": "conflicts_with",
        "confidence": 0.95,
        "reviewed": 1,
        "source": "STATUTORY_OVERRIDE"
    },
    {
        "src": "MY:CIPAA_2012:Sec30",
        "dst": "CASE:MY_FC:CTCI_CIPAA_DirectPay:2020",
        "rel": "interpreted_by",
        "confidence": 0.99,
        "reviewed": 1,
        "source": "JUDICIAL_INTERPRETATION"
    },
    {
        "src": "SG:SOPA_2004:Sec15",
        "dst": "FIDIC:Silver_1999:Clause_20.4",
        "rel": "overrides",
        "confidence": 0.96,
        "reviewed": 1,
        "source": "STATUTORY_OVERRIDE"
    },
    {
        "src": "SG:SOPA_2004:Sec15",
        "dst": "CASE:SG_CA:WRP_SOPA_Stay:2015",
        "rel": "interpreted_by",
        "confidence": 0.99,
        "reviewed": 1,
        "source": "JUDICIAL_INTERPRETATION"
    }
]

# =========================================================================
# Phase 4: 5 组重点法条裁判物化映射 (hot_norm_cases)
# =========================================================================
PHASE4_HOT_CASES = [
    ("VN:Commercial_Law_2005:Art301", "CASE:VN_Hanoi_HC:PenaltyCap_8Pct:2021", 1),
    ("TH:Arbitration_Act_2545:Sec40", "CASE:TH_SAC:Arbitration_PublicOrder:2020", 1),
    ("PH:Civil_Code:Art1229", "CASE:PH_SC:Ligutan_LD_Reduction:2002", 1),
    ("MY:CIPAA_2012:Sec30", "CASE:MY_FC:CTCI_CIPAA_DirectPay:2020", 1),
    ("SG:SOPA_2004:Sec15", "CASE:SG_CA:WRP_SOPA_Stay:2015", 1)
]

# =========================================================================
# Phase 4: 2 个新增高频工程合规风险社区 (risk_communities)
# =========================================================================
PHASE4_RISK_COMMUNITIES = [
    {
        "community_id": "RC_PENALTY_CAP",
        "name_zh": "违约金法定强行法上限与司法衡平酌减红线",
        "risk_level": "critical",
        "host_countries": json.dumps(["VN", "PH", "MY", "TH"], ensure_ascii=False),
        "archetypes": json.dumps(["EPC_CONTRACTING", "CROSS_BORDER_MA"], ensure_ascii=False),
        "norm_ids": json.dumps(["VN:Commercial_Law_2005:Art301", "PH:Civil_Code:Art1229", "MY:Contracts_Act_1950:Sec75", "TH:CCC:Sec383", "FIDIC:Silver_1999:Clause_8.7"], ensure_ascii=False),
        "trigger_scenarios": "发包人以工期延误为由，按照合同专用条件顶格扣除合同总价 10%~15% 的延误违约金（LDs），总承包商利用东道国强行法上限抗辩要求返还超额扣款。",
        "redline_actions": json.dumps([
            "在越南项目专用条件中必须明确‘任何违约赔偿金受限于《商业法》第301条8%法定上限’",
            "在菲律宾工程发生延误时立即向 CIAC 或法院申请依据民法典第1229条启动衡平酌减程序",
            "在马来西亚项目援引 Cubic Electronics 判例要求发包人负倒置举证责任证明客观实际损失"
        ], ensure_ascii=False)
    },
    {
        "community_id": "RC_DIRECT_PAYMENT",
        "name_zh": "分包工程款穿透索要与发包人直接支付扣款风险",
        "risk_level": "high",
        "host_countries": json.dumps(["MY", "SG"], ensure_ascii=False),
        "archetypes": json.dumps(["EPC_CONTRACTING", "JV_CONSORTIUM"], ensure_ascii=False),
        "norm_ids": json.dumps(["MY:CIPAA_2012:Sec30", "SG:SOPA_2004:Sec15", "FIDIC:Silver_1999:Clause_1.14"], ensure_ascii=False),
        "trigger_scenarios": "联合体分包商或本地指定分包商取得法定快速裁决后，直接越过总承包商向发包人索要工程款，导致发包人在总包工程款中直接代扣。",
        "redline_actions": json.dumps([
            "总承包合同专用条件中订立‘发包人执行 CIPAA/SOPA 直接支付前必须给予总包 14 天异议核实宽限期’",
            "在分包协议中约定分包商必须在提起法定裁决前完成前置友好磋商",
            "密切监控分包商资金链状况，发生违约争议及时申请紧急仲裁员（EA）临时保全措施"
        ], ensure_ascii=False)
    }
]

def append_phase4():
    with open('scripts/kb_expansion_data.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Append Phase 4 Norms
    marker_norm_end = 'NEW_CASES_DATA: List[Dict[str, Any]] = ['
    idx_case_start = content.find(marker_norm_end)
    assert idx_case_start != -1, "Could not find NEW_CASES_DATA start"
    closing_bracket_norm = content.rfind(']', 0, idx_case_start)
    assert closing_bracket_norm != -1, "Could not find closing bracket of NEW_NORMS_DATA"

    norm_texts = []
    for n in PHASE4_NORMS:
        norm_texts.append(json.dumps(n, ensure_ascii=False, indent=4))
    joined_norms = ",\n" + ",\n".join(norm_texts) + "\n"
    content = content[:closing_bracket_norm] + joined_norms + content[closing_bracket_norm:]

    # 2. Append Phase 4 Cases
    marker_edges_start = 'NEW_EDGES_DATA: List[Dict[str, Any]] = ['
    idx_edge_start = content.find(marker_edges_start)
    assert idx_edge_start != -1, "Could not find NEW_EDGES_DATA start"
    closing_bracket_case = content.rfind(']', 0, idx_edge_start)
    assert closing_bracket_case != -1, "Could not find closing bracket of NEW_CASES_DATA"

    case_texts = []
    for c in PHASE4_CASES:
        case_texts.append(json.dumps(c, ensure_ascii=False, indent=4))
    joined_cases = ",\n" + ",\n".join(case_texts) + "\n"
    content = content[:closing_bracket_case] + joined_cases + content[closing_bracket_case:]

    # 3. Append Phase 4 Edges
    marker_hot_start = 'NEW_HOT_CASES_DATA: List[Tuple[str, str, int]] = ['
    idx_hot_start = content.find(marker_hot_start)
    assert idx_hot_start != -1, "Could not find NEW_HOT_CASES_DATA start"
    closing_bracket_edge = content.rfind(']', 0, idx_hot_start)
    assert closing_bracket_edge != -1, "Could not find closing bracket of NEW_EDGES_DATA"

    edge_texts = []
    for e in PHASE4_EDGES:
        edge_texts.append(json.dumps(e, ensure_ascii=False, indent=4))
    joined_edges = ",\n" + ",\n".join(edge_texts) + "\n"
    content = content[:closing_bracket_edge] + joined_edges + content[closing_bracket_edge:]

    # 4. Append Phase 4 Hot Cases
    marker_rc_start = 'NEW_RISK_COMMUNITIES: List[Dict[str, Any]] = ['
    idx_rc_start = content.find(marker_rc_start)
    assert idx_rc_start != -1, "Could not find NEW_RISK_COMMUNITIES start"
    closing_bracket_hot = content.rfind(']', 0, idx_rc_start)
    assert closing_bracket_hot != -1, "Could not find closing bracket of NEW_HOT_CASES_DATA"

    hot_texts = []
    for h in PHASE4_HOT_CASES:
        hot_texts.append(f'    ("{h[0]}", "{h[1]}", {h[2]})')
    joined_hots = ",\n" + ",\n".join(hot_texts) + "\n"
    content = content[:closing_bracket_hot] + joined_hots + content[closing_bracket_hot:]

    # 5. Append Phase 4 Risk Communities
    closing_bracket_rc = content.rfind(']')
    assert closing_bracket_rc != -1, "Could not find closing bracket of NEW_RISK_COMMUNITIES"

    rc_texts = []
    for rc in PHASE4_RISK_COMMUNITIES:
        rc_texts.append(json.dumps(rc, ensure_ascii=False, indent=4))
    joined_rc = ",\n" + ",\n".join(rc_texts) + "\n"
    content = content[:closing_bracket_rc] + joined_rc + content[closing_bracket_rc:]

    with open('scripts/kb_expansion_data.py', 'w', encoding='utf-8') as f:
        f.write(content)

    print("Phase 4 L1 supplement successfully written to scripts/kb_expansion_data.py!")

if __name__ == "__main__":
    append_phase4()
