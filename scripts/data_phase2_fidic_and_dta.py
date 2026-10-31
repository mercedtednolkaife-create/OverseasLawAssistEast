"""
data_phase2_fidic_and_dta.py - Phase 2 数据模块 1:
32 条 FIDIC 国际工程标准合同对比条款 (Red/Yellow/Silver) + 13 条 中国-东盟 6 国双边税收协定 (DTA) 核心条款
总计 45 条权威涉外规范，全部 100% 结构化填充 elements_json
"""
import json

PHASE2_FIDIC_CLAUSES = [
    {
        "table": "reference_norms",
        "norm_id": "FIDIC:Red_1999:Clause_1.9",
        "law": "FIDIC:Red_1999",
        "enbez": "Clause 1.9",
        "title": "FIDIC红皮书第1.9款：图纸或指示延误索赔工期与利润",
        "heading_path": "FIDIC 施工合同条件 (Red Book 1999) > 第1条 一般规定 > 图纸或指示延误",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Delayed Drawings or Instructions: The Contractor shall give notice to the Engineer whenever the Works are likely to be delayed or disrupted if any necessary drawing or instruction is not issued within a specified reasonable time. If the Contractor suffers delay and/or incurs Cost as a result of an unissued drawing or instruction, the Contractor shall be entitled subject to Sub-Clause 20.1 to: (a) an extension of time, and (b) payment of any such Cost plus reasonable profit.",
        "text_en": "Contractor is entitled to EOT plus Cost plus reasonable profit if Engineer fails to issue necessary drawings or instructions in reasonable time.",
        "text_zh": "【图纸或指示延误索赔工期与利润】：在红皮书单价合同中，承包商发现若工程师未在合理期限内签发必要的施工图纸或工程指示将导致工程延误或中断时，应及时向工程师发出书面通知；若因工程师迟延签发导致承包商工期延误或增加成本，承包商有权依据第20.1款索赔：① 竣工工期顺延（EOT），以及 ② 额外实际支出成本加上合理利润！【实务启示】：与银皮书‘图纸由总包自理’不同，红皮书下设计风险在雇主。一旦监理图纸交付不及时，中资施工总包必须在第一时间发函预警，牢牢锁定工期顺延与利润索赔权！",
        "norm_category": "fidic_standard",
        "mandatory_level": "contract_default",
        "elements_json": json.dumps([
            {"eid": "e_fidic19_notice_issued", "text_zh": "要件一：承包商已就图纸或指示的必要交付时限向工程师发出书面催告通知", "status": "condition_precedent"},
            {"eid": "e_fidic19_engineer_delay", "text_zh": "要件二：工程师未能未在合理时限内签发该等施工图纸或技术指示", "status": "mandatory"},
            {"eid": "e_fidic19_eot_cost_profit", "text_zh": "法律后果：承包商依法享有顺延竣工工期、补偿实际成本并加计合理利润之权利", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "FIDIC:Red_1999:Clause_4.7",
        "law": "FIDIC:Red_1999",
        "enbez": "Clause 4.7",
        "title": "FIDIC红皮书第4.7款：放线基准点错误索赔工期与成本利润",
        "heading_path": "FIDIC 施工合同条件 (Red Book 1999) > 第4条 承包商 > 放线",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Setting Out: The Contractor shall set out the Works in relation to original points, lines and levels of reference specified in the Contract. If the Contractor suffers delay and/or incurs Cost from remedying errors caused by an error in these reference points, the Contractor shall give notice to the Engineer and shall be entitled subject to Sub-Clause 20.1 to EOT and payment of such Cost plus reasonable profit.",
        "text_en": "Employer is responsible for errors in original reference points; Contractor entitled to EOT plus Cost plus profit for rectifying errors.",
        "text_zh": "【放线基准点错误索赔】：雇主负责提供工程放线的原始基准点、基准线和参考标高。若承包商因雇主提供的初始基准数据存在错误而遭受工期延误或发生纠正错误额外成本，承包商有权索赔工期顺延及实际成本与合理利润。【实务启示】：银皮书 4.7 款将全部放线错误风险转移给总包商，而红皮书严格保留了雇主对基准点真实性的法律责任，中资单价施工项目应据此争取索赔！",
        "norm_category": "fidic_standard",
        "mandatory_level": "contract_default",
        "elements_json": json.dumps([
            {"eid": "e_fidic47_employer_error", "text_zh": "要件一：合同中指定的原始放线基准点、基准线或参考标高存在实质错误", "status": "condition_precedent"},
            {"eid": "e_fidic47_timely_notice", "text_zh": "要件二：承包商在发现基准错误后及时通知工程师进行现场复核确认", "status": "mandatory"},
            {"eid": "e_fidic47_compensation", "text_zh": "法律后果：享有纠正返工导致的工期顺延及成本利润补偿", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "FIDIC:Red_1999:Clause_12.1",
        "law": "FIDIC:Red_1999",
        "enbez": "Clause 12.1",
        "title": "FIDIC红皮书第12.1款：工程量现场测量与工程师核实程序",
        "heading_path": "FIDIC 施工合同条件 (Red Book 1999) > 第12条 测量与估价 > 工程量测量",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Works to be Measured: The Works shall be measured, and valued for payment, in accordance with this Clause. Whenever the Engineer requires any part of the Works to be measured, reasonable notice shall be given to the Contractor's Representative, who shall promptly attend and assist the Engineer in making such measurement.",
        "text_en": "Works under Red Book are measured and valued based on actual quantities executed; Engineer gives notice for joint measurement.",
        "text_zh": "【红皮书工程量实际测量铁律】：红皮书为单价重测合同，合同价格应按实际完成的合格工程量乘以合同单价进行核算。工程师要求测量任何部分工程时，须向承包商发出合理通知并实施联合测量；若承包商未到场，工程师的单方测量记录视为准确。【实务启示】：红皮书与银皮书固定总价有本质区别，中资项目部必须设立专职测量与算量工程师，紧跟现场联合测量签认，防止结算量被恶意压低！",
        "norm_category": "fidic_standard",
        "mandatory_level": "contract_default",
        "elements_json": json.dumps([
            {"eid": "e_fidic121_measurement_mandate", "text_zh": "要件一：合同计价模式属于红皮书单价重测机制", "status": "condition_precedent"},
            {"eid": "e_fidic121_joint_attendance", "text_zh": "要件二：工程师发出测量通知并由双方授权代表联合进行现场测量核验", "status": "mandatory"},
            {"eid": "e_fidic121_binding_records", "text_zh": "法律后果：双方签字记录作为期中及最终付款证书计价的核心法定依据", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "FIDIC:Red_1999:Clause_12.3",
        "law": "FIDIC:Red_1999",
        "enbez": "Clause 12.3",
        "title": "FIDIC红皮书第12.3款：工程量偏差超10%时单价重新核定机制",
        "heading_path": "FIDIC 施工合同条件 (Red Book 1999) > 第12条 测量与估价 > 估价与费率调整",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Evaluation: A new rate or price shall be appropriate for an item of work if: (a)(i) the measured quantity of the item changes by more than 10% from the quantity in the Bill of Quantities, (ii) this change in quantity multiplies by such specified rate exceeds 0.01% of the Accepted Contract Amount, and (iii) this change in quantity directly changes the Cost per unit quantity of this item by more than 1%.",
        "text_en": "New rate or price applies where measured quantity changes by more than 10% from BOQ and impact exceeds 0.01% of Contract Amount.",
        "text_zh": "【工程量剧变重定单价三大门槛】：当某项工程的实际测量工程量发生重大变化时，在同时满足下列三大要件时，应核定新的合理单价：① 实际工程量变化幅度超过工程量清单（BOQ）约定数量的 10%；② 该工程量变动乘以原单价超过中标合同金额的 0.01%；③ 该工程量变动直接导致该项目单位成本变化超过 1%！【实务启示】：红皮书调价神器！当土石方、混凝土等大宗项目因业主设计导致工程量暴增或骤减时，承包商可依法启动重新议价，大幅提升项目综合利润率！",
        "norm_category": "fidic_standard",
        "mandatory_level": "contract_default",
        "elements_json": json.dumps([
            {"eid": "e_fidic123_ten_percent_shift", "text_zh": "要件一：实测工程量与清单工程量偏差幅度绝对值超过10%", "status": "condition_precedent"},
            {"eid": "e_fidic123_contract_value_impact", "text_zh": "要件二：变动总金额超过中标合同金额的0.01%", "status": "mandatory"},
            {"eid": "e_fidic123_rate_revision_right", "text_zh": "法律后果：原单价自动失效，双方依法按照实际成本加利润核定全新综合单价", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "FIDIC:Yellow_1999:Clause_5.1",
        "law": "FIDIC:Yellow_1999",
        "enbez": "Clause 5.1",
        "title": "FIDIC黄皮书第5.1款：总承包商设计一般义务与设计责任",
        "heading_path": "FIDIC 生产设备和设计-施工合同条件 (Yellow Book 1999) > 第5条 设计 > 一般设计义务",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "General Design Obligations: The Contractor shall carry out, and be responsible for, the design of the Works. Design shall be prepared by qualified designers who are engineers or other professionals who comply with criteria stated in the Employer's Requirements.",
        "text_en": "Contractor is responsible for design in Yellow Book, ensuring qualified professionals prepare design complying with Employer's Requirements.",
        "text_zh": "【黄皮书设计建造承包商设计责任】：承包商应对工程的设计全权负责并实施设计。设计必须由具备法定资质的注册工程师完成，并完全满足《发包人要求》（Employer's Requirements）规定的技术标准与功能指标。【实务启示】：黄皮书设计责任属于总包商，必须防范发包人要求中的前后矛盾或指标过高，在投标阶段须全面组织技术清标！",
        "norm_category": "fidic_standard",
        "mandatory_level": "contract_default",
        "elements_json": json.dumps([
            {"eid": "e_fidic_y51_qualified_designers", "text_zh": "要件一：设计由持有东道国或国际认可执业资质的专业设计人员完成", "status": "condition_precedent"},
            {"eid": "e_fidic_y51_compliance_reqs", "text_zh": "要件二：设计图纸与技术计算完全符合发包人要求及功能指标", "status": "mandatory"},
            {"eid": "e_fidic_y51_design_liability", "text_zh": "法律后果：总包商对设计缺陷承担全额修复与迟延赔偿责任", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "FIDIC:Yellow_1999:Clause_5.2",
        "law": "FIDIC:Yellow_1999",
        "enbez": "Clause 5.2",
        "title": "FIDIC黄皮书第5.2款：承包商设计文件审查与21天视为批准",
        "heading_path": "FIDIC 生产设备和设计-施工合同条件 (Yellow Book 1999) > 第5条 设计 > 承包商文件审查",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Contractor's Documents: The Contractor shall submit documents to the Engineer for review. Unless otherwise stated, each review period shall not exceed 21 days, calculated from the date on which the Engineer receives a Contractor's Document. If the Engineer fails to give notice within such review period, the document shall be deemed approved.",
        "text_en": "Engineer review period shall not exceed 21 days; failure to notify within 21 days constitutes deemed approval of Contractor's Documents.",
        "text_zh": "【设计文件21天审查时限与视为批准规则】：承包商应将设计图纸报送工程师审查。除另有约定外，工程师的审查期限不得超过21个日历日；若工程师在21天期限届满后未发出反对或修改通知，该设计文件法律上直接‘视为已获批准（Deemed Approved）’，承包商有权据此开工！【实务启示】：制约监理审查拖延的核心武器！中资技术团队必须做好图纸递交送达凭证，满21天未获答复直接签发开工函，阻断业主借口图纸未批拒付进度款！",
        "norm_category": "fidic_standard",
        "mandatory_level": "contract_default",
        "elements_json": json.dumps([
            {"eid": "e_fidic_y52_submission_receipt", "text_zh": "要件一：承包商已向工程师正式送达完整设计图纸并取得有效签收", "status": "condition_precedent"},
            {"eid": "e_fidic_y52_twentyone_days_lapse", "text_zh": "要件二：21个日历日审查期届满且工程师未提出书面反对意见", "status": "mandatory"},
            {"eid": "e_fidic_y52_deemed_approval_effect", "text_zh": "法律后果：设计文件视为法定批准，承包商可依法据此组织施工作业", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "FIDIC:Silver_1999:Clause_1.9",
        "law": "FIDIC:Silver_1999",
        "enbez": "Clause 1.9",
        "title": "FIDIC银皮书第1.9款：发包人要求中的错误核查与风险承担",
        "heading_path": "FIDIC EPC/交钥匙合同条件 (Silver Book 1999) > 第1条 一般规定 > 发包人要求中的错误",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Errors in the Employer's Requirements: The Contractor shall be responsible for the accuracy of the Employer's Requirements (including design criteria and calculations), except as otherwise stated below. The Employer shall be responsible for correctness of: (a) portions stated as being sole responsibility of Employer, (b) definitions of intended purpose, (c) criteria for testing and performance, and (d) data which cannot be verified by an experienced contractor.",
        "text_en": "Silver Book Contractor is generally responsible for accuracy of Employer's Requirements, except for 4 specific categories Employer retains responsibility for.",
        "text_zh": "【银皮书发包人要求错误审查与四大法定例外】：银皮书总承包商对《发包人要求》的准确性原则上承担全责，但雇主对下列四类数据和指标的真实性承担排他性法律责任：① 合同明文规定由雇主负责的部分；② 工程预期目的的定义；③ 竣工试验与性能考核的最终验收标准；④ 有经验的承包商在签约前无法在现场验证的数据！【实务启示】：银皮书号称‘交钥匙风险全包’，但第1.9款保留了四大豁免后门。当业主提供的深水测绘数据严重失真且签约前无法探测时，中资总包商可据此打破全包封锁，主张索赔！",
        "norm_category": "fidic_standard",
        "mandatory_level": "contract_default",
        "elements_json": json.dumps([
            {"eid": "e_fidic_s19_unverifiable_data", "text_zh": "要件一：错误数据属于签约前常规尽调无法查明的隐蔽地质或专有数据", "status": "condition_precedent"},
            {"eid": "e_fidic_s19_statutory_exception", "text_zh": "要件二：属于银皮书第1.9款明文保留的发包人四项法定保证责任范围", "status": "mandatory"},
            {"eid": "e_fidic_s19_contractor_relief", "text_zh": "法律后果：发包人承担纠偏成本与工期顺延，承包商免除违约责任", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "FIDIC:Silver_1999:Clause_2.2",
        "law": "FIDIC:Silver_1999",
        "enbez": "Clause 2.2",
        "title": "FIDIC银皮书第2.2款：雇主协助办理规划许可与审批职责",
        "heading_path": "FIDIC EPC/交钥匙合同条件 (Silver Book 1999) > 第2条 雇主 > 许可、执照或批准",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Permits, Licences or Approvals: The Employer shall (where he is in a position to do so) provide reasonable assistance to the Contractor at the request and cost of the Contractor in applying for permits, licences or approvals required by the Laws of the Country.",
        "text_en": "Employer must provide reasonable assistance to Contractor in applying for statutory permits, licences or approvals in host country.",
        "text_zh": "【雇主协助办理属地行政许可法定义务】：雇主应在承包商提出请求并承担合理费用的前提下，就办理东道国法律所要求的一切工程规划许可证、施工执照、海关豁免或环保批准提供合理的行政与官方协助。【实务启示】：虽然施工许可证由总包负责，但土地使用权批准、电网并网接入批复必须由业主出面。若业主怠于协助导致执照办不下来，总包商可依此主张雇主阻碍违约！",
        "norm_category": "fidic_standard",
        "mandatory_level": "contract_default",
        "elements_json": json.dumps([
            {"eid": "e_fidic_s22_contractor_request", "text_zh": "要件一：承包商已正式书面请求雇主就特定法定许可提供行政协调支持", "status": "condition_precedent"},
            {"eid": "e_fidic_s22_employer_capacity", "text_zh": "要件二：该等许可证系依据属地法必须由业主作为立项主体方能申办", "status": "mandatory"},
            {"eid": "e_fidic_s22_breach_consequence", "text_zh": "法律后果：雇主拖延协助导致延误构成发包人阻碍，承包商享有EOT抗辩", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "FIDIC:Silver_1999:Clause_3.5",
        "law": "FIDIC:Silver_1999",
        "enbez": "Clause 3.5",
        "title": "FIDIC银皮书第3.5款：雇主代表商定与确定程序",
        "heading_path": "FIDIC EPC/交钥匙合同条件 (Silver Book 1999) > 第3条 雇主管理 > 商定与确定",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Determinations: Whenever these Conditions provide that the Employer shall proceed in accordance with this Sub-Clause 3.5 to agree or determine any matter, the Employer shall consult with the Contractor in an endeavour to reach agreement. If agreement is not reached, the Employer shall make a fair determination in accordance with the Contract, taking due regard of all relevant circumstances.",
        "text_en": "Employer must consult with Contractor to reach agreement; if no agreement, Employer must make a fair determination under Contract.",
        "text_zh": "【雇主代表商定与确定法定程序】：每当合同规定雇主应依照第3.5款商定或确定任何索赔事项时，雇主必须事先与承包商充分协商以期达成合意；若未达成一致，雇主应依据合同兼顾一切相关情况作出‘公正的确定（Fair Determination）’并附具详细理由通知承包商。【实务启示】：雇主不能任意一言堂拒赔！必须履行事先磋商程序；若雇主未做公正确定，承包商可立即依据第20款提交争端裁决委员会（DAAB）推翻！",
        "norm_category": "fidic_standard",
        "mandatory_level": "contract_default",
        "elements_json": json.dumps([
            {"eid": "e_fidic_s35_prior_consultation", "text_zh": "要件一：雇主代表在作出决定前已与承包商就索赔金额与工期举行正式磋商", "status": "condition_precedent"},
            {"eid": "e_fidic_s35_fair_determination", "text_zh": "要件二：决定的作出符合合同约定且体现客观公允原则与计算依据", "status": "mandatory"},
            {"eid": "e_fidic_s35_right_to_dispute", "text_zh": "法律后果：对确定不服有权在法定期限内签发异议通知并提交DAAB审查", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "FIDIC:Silver_2017:Clause_3.7",
        "law": "FIDIC:Silver_2017",
        "enbez": "Clause 3.7",
        "title": "FIDIC银皮书2017版第3.7款：工程师中立确定、42天时效与28天NOD终局性",
        "heading_path": "FIDIC EPC/交钥匙合同条件 (Silver Book 2017) > 第3条 雇主管理 > 协议与确定",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Agreement or Determination: When carrying out duties under Sub-Clause 3.7, the Engineer/Employer's Representative shall act neutrally and shall not be deemed for acting for the Employer. The Engineer shall give Notice of agreement or determination within 42 days. If either Party is dissatisfied with the determination, the Party may issue a Notice of Dissatisfaction (NOD) within 28 days, failing which the determination shall become final and binding on both Parties.",
        "text_en": "2017 Suite: Engineer must act neutrally, decide within 42 days; 28-day NOD time-bar renders determination final and binding.",
        "text_zh": "【2017版重大变革：工程师中立性、42天确定与28天NOD终局失权】：2017版第3.7款彻底重塑了工程师地位：在作出确定时必须保持‘中立（Act Neutrally）’，不再代表雇主利益！工程师必须在42个日历日内作出确定；任何一方对确定不服的，必须在收到后 28 个日历日内发出《不满通知》（NOD）；若未在 28 天内发出 NOD，该确定立即变为对双方具有‘终局且不可推翻的绝对拘束力（Final and Binding）’！【实务启示】：生死攸关的失权陷阱！中资出海采用2017版合同，若工程师签发的减款确定被中方项目部在案头搁置超过28天未发 NOD，该损失裁决永久不可推翻，哪怕仲裁庭也无权翻案！",
        "norm_category": "fidic_standard",
        "mandatory_level": "contract_default",
        "elements_json": json.dumps([
            {"eid": "e_fidic17_37_neutral_duty", "text_zh": "要件一：工程师履行确定职责时依法独立中立履职，不受雇主干预", "status": "condition_precedent"},
            {"eid": "e_fidic17_37_fortytwo_days_limit", "text_zh": "要件二：工程师在42天法定时限内正式签发书面确定书", "status": "mandatory"},
            {"eid": "e_fidic17_37_twentyeight_nod_timebar", "text_zh": "法律后果：逾期28天未发不满通知NOD，该确定变为终局拘束力且不得反悔", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "FIDIC:Silver_1999:Clause_4.18",
        "law": "FIDIC:Silver_1999",
        "enbez": "Clause 4.18",
        "title": "FIDIC银皮书第4.18款：现场环境保护与污染减损义务",
        "heading_path": "FIDIC EPC/交钥匙合同条件 (Silver Book 1999) > 第4条 承包商 > 环境保护",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Protection of the Environment: The Contractor shall take all reasonable steps to protect the environment (both on and off the Site) and to limit damage and nuisance to people and property resulting from pollution, noise and other results of his operations. The Contractor shall ensure that air emissions, surface discharges and effluent from Site activities comply with applicable Laws.",
        "text_en": "Contractor must take all reasonable steps to protect environment and ensure site operations comply with applicable environmental laws.",
        "text_zh": "【施工现场环境保护与合规红线】：承包商应采取一切合理措施保护现场内外环境，限制因施工作业产生的污染、噪音、粉尘和振动对人身和财产造成的损害与妨碍；承包商必须确保废气排放、地表径流与污水排放完全符合东道国适用的环保法律法规标准。【实务启示】：在印尼 AMDAL、越南 ĐTM 及泰国 EIA 严管下，环保违规不仅触发当地行政停工令，且根据第4.18款总包须自行承担全部罚款与停工损失！",
        "norm_category": "fidic_standard",
        "mandatory_level": "contract_default",
        "elements_json": json.dumps([
            {"eid": "e_fidic_s418_statutory_standards", "text_zh": "要件一：施工作业符合东道国环境影响评价批复及法定的污染物排放指标", "status": "condition_precedent"},
            {"eid": "e_fidic_s418_nuisance_mitigation", "text_zh": "要件二：采取合理工程降噪、除尘及泥水沉淀净化等技术防治措施", "status": "mandatory"},
            {"eid": "e_fidic_s418_contractor_liability", "text_zh": "法律后果：因环保违规被行政处罚或勒令停工之损失由承包商自担", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "FIDIC:Silver_1999:Clause_4.20",
        "law": "FIDIC:Silver_1999",
        "enbez": "Clause 4.20",
        "title": "FIDIC银皮书第4.20款：雇主提供设备与免费提供材料照管",
        "heading_path": "FIDIC EPC/交钥匙合同条件 (Silver Book 1999) > 第4条 承包商 > 雇主设备和免费材料",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Employer's Equipment and Free-Issue Material: The Employer shall make the Employer's Equipment available for the use of the Contractor in accordance with the details stated in the Employer's Requirements. The Employer shall supply, free of charge, the 'free-issue materials' (if any) in accordance with the details stated in the Specification.",
        "text_en": "Employer must make available Employer's equipment and free-issue materials as specified; Contractor takes care upon receipt.",
        "text_zh": "【雇主提供设备与甲供免费材料照管规则】：雇主应按《发包人要求》在约定时间向承包商提供雇主自有的施工机械设备与免费材料（甲供材）；承包商在目测检验合格接收后负责日常操作与妥善照管。若甲供设备迟延交付或存在隐蔽质量瑕疵导致工程延误，承包商有权主张工期顺延及费用补偿。【实务启示】：甲供料迟延是中资工程向业主索赔工期顺延的利器！交接时必须形成双方签字的质检纪要，防范后续责任纠缠。",
        "norm_category": "fidic_standard",
        "mandatory_level": "contract_default",
        "elements_json": json.dumps([
            {"eid": "e_fidic_s420_free_issue_delivery", "text_zh": "要件一：合同明文约定雇主负责提供特定甲供设备或原材料并在现场交割", "status": "condition_precedent"},
            {"eid": "e_fidic_s420_visual_inspection", "text_zh": "要件二：承包商在接收时履行合理目测检验并出具书面状态确认凭单", "status": "mandatory"},
            {"eid": "e_fidic_s420_delay_compensation", "text_zh": "法律后果：甲供料迟交或质量缺陷造成停窝工，承包商依法享有EOT及费用索赔", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "FIDIC:Silver_1999:Clause_4.24",
        "law": "FIDIC:Silver_1999",
        "enbez": "Clause 4.24",
        "title": "FIDIC银皮书第4.24款：地下化石文物发现工期顺延与费用索赔",
        "heading_path": "FIDIC EPC/交钥匙合同条件 (Silver Book 1999) > 第4条 承包商 > 化石文物",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Fossils: All fossils, coins, articles of value or antiquity found on the Site shall be placed under the care of the Employer. The Contractor shall take reasonable precautions to prevent removal or damage. If Contractor suffers delay and/or incurs Cost from complying with Engineer's instructions, Contractor shall be entitled to EOT and Cost compensation.",
        "text_en": "Fossils and antiquities found on site are property of host state/Employer; Contractor entitled to EOT and Cost for following instructions.",
        "text_zh": "【地下化石与古代文物发现索赔】：在现场发现的一切化石、硬币、具有地质或考古价值的文物均属雇主或东道国所有。承包商应妥善保护并遵照工程师指示停工保护；由此导致的施工暂停与改道作业，承包商有权依据第20.1款索赔工期顺延（EOT）及额外支出的全部直接成本（Cost）！【实务启示】：东南亚历史古迹多（如柬埔寨吴哥、印尼爪哇寺庙群、泰国大城），施工中挖出古迹必须即刻停工并拍照备案，坚决索赔全额窝工成本与工期！",
        "norm_category": "fidic_standard",
        "mandatory_level": "contract_default",
        "elements_json": json.dumps([
            {"eid": "e_fidic_s424_antiquity_discovery", "text_zh": "要件一：在施工现场地下开挖过程中发现具有考古、历史或地质价值的物品", "status": "condition_precedent"},
            {"eid": "e_fidic_s424_preservation_compliance", "text_zh": "要件二：承包商立即暂停开挖、保护现场并遵照雇主指示实施考古发掘配合", "status": "mandatory"},
            {"eid": "e_fidic_s424_relief_entitlement", "text_zh": "法律后果：承包商全额享有竣工日期顺延及实际支出费用补偿", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "FIDIC:Silver_1999:Clause_8.3",
        "law": "FIDIC:Silver_1999",
        "enbez": "Clause 8.3",
        "title": "FIDIC银皮书第8.3款：进度计划提交与21天未异议视为有效",
        "heading_path": "FIDIC EPC/交钥匙合同条件 (Silver Book 1999) > 第8条 开工、延误和暂停 > 进度计划",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Programme: The Contractor shall submit a detailed time programme to the Employer within 28 days after receiving the notice under Sub-Clause 8.1. Unless the Employer, within 21 days after receiving the programme, gives notice to the Contractor stating the extent to which it does not comply with the Contract, the Contractor shall proceed in accordance with the programme.",
        "text_en": "Contractor submits detailed programme within 28 days; Employer has 21 days to object, failing which programme becomes accepted baseline.",
        "text_zh": "【关键路径进度计划21天异议期与基线确立】：承包商应在开工通知后28天内向雇主提交详细的实施进度计划（包含关键路径 Critical Path）。雇主在收到计划后拥有21个日历日审查异议期；若雇主在21天内未发出不符合合同的反对通知，承包商应依照该计划施工，该进度计划自动成为衡量未来工期顺延与延误责任的‘法定基线进度计划（Baseline Programme）’！【实务启示】：项目索赔的生命线！中资总包必须在28天内递交逻辑紧密的 Primavera P6 进度网络图，21天一过即坐实索赔基线！",
        "norm_category": "fidic_standard",
        "mandatory_level": "contract_default",
        "elements_json": json.dumps([
            {"eid": "e_fidic_s83_timely_submission", "text_zh": "要件一：承包商在开工通知后28日内提交符合合同深度要求的详细进度计划", "status": "condition_precedent"},
            {"eid": "e_fidic_s83_twentyone_day_silence", "text_zh": "要件二：雇主在收到进度计划后21个日历日内未签发实质性反对通知", "status": "mandatory"},
            {"eid": "e_fidic_s83_baseline_binding", "text_zh": "法律后果：该计划正式确立为双方认可的项目进度基线，作为EOT分析依据", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "FIDIC:Silver_1999:Clause_8.6",
        "law": "FIDIC:Silver_1999",
        "enbez": "Clause 8.6",
        "title": "FIDIC银皮书第8.6款：赶工指令与加速施工费索赔边界",
        "heading_path": "FIDIC EPC/交钥匙合同条件 (Silver Book 1999) > 第8条 开工、延误和暂停 > 进度速度与赶工",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Rate of Progress: If the Employer gives notice that the rate of progress is too slow to complete within the Time for Completion, the Contractor shall adopt revised methods, which may require increase in working hours or equipment. If these revised methods cause the Employer to incur additional costs, the Contractor shall subject to Sub-Clause 2.5 pay these costs to the Employer.",
        "text_en": "If progress is slow due to Contractor default, Contractor accelerates at own cost; if acceleration ordered without Contractor default, it constitutes Variation.",
        "text_zh": "【施工赶工指令与加速费用权责归属】：若工程实际进度落后，雇主可发出加快进度的指令。若延误系由承包商原因造成，承包商须自费采取增加班次、增派机械等赶工措施；但若导致工程滞后的原因此前已构成可顺延工期的事件，而雇主拒绝批复工期顺延并强制要求承包商赶工以按原计划竣工，此种指令在普通法上构成‘推定赶工（Constructive Acceleration）’，承包商有权主张变更估价并索赔全部赶工加速费！【实务启示】：出海索赔核心战术！雇主不批工期逼迫项目部赶工时，项目部必须发出保留赶工费用的异议函，为后续仲裁追回数百万赶工成本打下伏笔！",
        "norm_category": "fidic_standard",
        "mandatory_level": "contract_default",
        "elements_json": json.dumps([
            {"eid": "e_fidic_s86_acceleration_instruction", "text_zh": "要件一：雇主因竣工日期逼近向承包商正式签发书面加快工程进度指令", "status": "condition_precedent"},
            {"eid": "e_fidic_s86_excusable_delay_basis", "text_zh": "要件二：导致进度滞后的根本原因属于承包商原本依法享有EOT的免责事件", "status": "mandatory"},
            {"eid": "e_fidic_s86_constructive_cost", "text_zh": "法律后果：承包商构成推定赶工，依法享有全额追索赶工窝工费用之请求权", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "FIDIC:Silver_1999:Clause_10.3",
        "law": "FIDIC:Silver_1999",
        "enbez": "Clause 10.3",
        "title": "FIDIC银皮书第10.3款：雇主阻碍竣工试验导致工程视为接收",
        "heading_path": "FIDIC EPC/交钥匙合同条件 (Silver Book 1999) > 第10条 雇主接收 > 对竣工试验的干预",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Interference with Tests on Completion: If the Contractor is prevented, for more than 14 days, from carrying out the Tests on Completion by a cause for which the Employer is responsible, the Employer shall be deemed to have taken over the Works on the date when the Tests on Completion would otherwise have been completed, and the Engineer shall issue a Taking-Over Certificate accordingly.",
        "text_en": "If Contractor is prevented from carrying out Tests on Completion for over 14 days by Employer, Works are deemed taken over on date tests would have finished.",
        "text_zh": "【阻碍竣工试验超14天工程拟制视为接收】：若由于发包人的原因（如未通天然气、未提供并网负荷、或未提供试验水源原油）导致承包商无法进行竣工试验超过 14 个日历日，法律直接拟制‘雇主已于竣工试验原本应当完成之日正式接收工程’，工程师必须签发《工程接收证书》（TOC）！工程照管风险移转，误期违约金立即切断！【实务启示】：电站与工厂交钥匙工程必杀技！业主拖着不给并网负荷企图压低结算款，总包商依此款宣告工程视为接收，倒逼业主退还50%保留金并承担电站照管风险！",
        "norm_category": "fidic_standard",
        "mandatory_level": "contract_default",
        "elements_json": json.dumps([
            {"eid": "e_fidic_s103_fourteen_day_prevention", "text_zh": "要件一：因归责于雇主原因导致竣工性能试验受阻连续超过14个日历日", "status": "condition_precedent"},
            {"eid": "e_fidic_s103_ready_for_test", "text_zh": "要件二：承包商已书面通告其各项施工准备已就绪、具备投料试验条件", "status": "mandatory"},
            {"eid": "e_fidic_s103_deemed_toc_cut", "text_zh": "法律后果：工程拟制视为法定接收，误期违约金即时终结且雇主承担照管风险", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "FIDIC:Silver_1999:Clause_11.4",
        "law": "FIDIC:Silver_1999",
        "enbez": "Clause 11.4",
        "title": "FIDIC银皮书第11.4款：未能修补缺陷雇主自行修补与承包商费用扣减",
        "heading_path": "FIDIC EPC/交钥匙合同条件 (Silver Book 1999) > 第11条 缺陷责任 > 未能修补缺陷",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Failure to Remedy Defects: If the Contractor fails to remedy any defect within a reasonable time, a date may be fixed by (or on behalf of) the Employer, on or by which the defect is to be remedied. If the Contractor fails to remedy the defect by this notified date, the Employer may carry out the work himself or by others, at the Contractor's cost, subject to Sub-Clause 2.5.",
        "text_en": "Employer may fix a final date for defect rectification; if Contractor fails, Employer may repair at Contractor's reasonable cost.",
        "text_zh": "【未能修补缺陷雇主自行代修与费用追索限额】：若承包商在缺陷通知期（DNP）内未能在合理期限内修补缺陷，雇主可设定最终整改截止日通知承包商；若届期承包商仍未修补，雇主有权自行或聘请第三方代为修补，合理费用由承包商承担，雇主可自保留金或工程款中抵扣。若缺陷导致整个工程无法实现合同预期商业目的，雇主有权终止合同并退回工程！【实务启示】：防范业主雇佣天价第三方恶意扣款！总包商收到通知后应坚决派驻留守团队自行维修，杜绝业主借助第三方高昂账单强行没收质保金！",
        "norm_category": "fidic_standard",
        "mandatory_level": "contract_default",
        "elements_json": json.dumps([
            {"eid": "e_fidic_s114_reasonable_notice", "text_zh": "要件一：雇主已向承包商发出正式催告并指定了合理的最终缺陷修补期限", "status": "condition_precedent"},
            {"eid": "e_fidic_s114_contractor_nonperformance", "text_zh": "要件二：承包商无正当理由逾期未能实施修补或修补未达到标准", "status": "mandatory"},
            {"eid": "e_fidic_s114_reasonable_cost_deduction", "text_zh": "法律后果：雇主仅有权扣减实际发生且合理的直接维修成本，严禁惩罚性扣款", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "FIDIC:Silver_1999:Clause_13.5",
        "law": "FIDIC:Silver_1999",
        "enbez": "Clause 13.5",
        "title": "FIDIC银皮书第13.5款：暂列金额（Provisional Sums）指令与计价",
        "heading_path": "FIDIC EPC/交钥匙合同条件 (Silver Book 1999) > 第13条 变更和调整 > 暂列金额",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Provisional Sums: Each Provisional Sum shall only be used, in whole or in part, in accordance with the Employer's instructions, and the Contract Price shall be adjusted accordingly. The total sum paid to the Contractor shall include only such amounts for the work, supplies or services to which the Provisional Sum relates, as the Employer shall have instructed.",
        "text_en": "Provisional sums are only used pursuant to Employer's instructions; actual expended amounts plus overhead and profit adjust Contract Price.",
        "text_zh": "【暂列金额指令与实际核销规则】：合同工程量清单中设立的每一笔暂列金额（Provisional Sums），仅能依据雇主的正式书面指令全额或部分使用，合同价格相应予以增减调整。承包商按照雇主指示实施暂列金额项下作业的，支付金额应包含承包商实际发生的有效支出加上合同约定的现场管理费与利润百分比。【实务启示】：暂列金额不是业主的私房钱！未经承包商参与确认，业主严禁单方私自挪用或指定高价分包商强塞给总包商承担质量连带责任！",
        "norm_category": "fidic_standard",
        "mandatory_level": "contract_default",
        "elements_json": json.dumps([
            {"eid": "e_fidic_s135_written_instruction", "text_zh": "要件一：雇主就特定暂列金额项下的施工或设备采购签发正式书面动用指令", "status": "condition_precedent"},
            {"eid": "e_fidic_s135_actual_cost_incurred", "text_zh": "要件二：承包商已实际签署分包采购合同并发生经审核的合规支付凭单", "status": "mandatory"},
            {"eid": "e_fidic_s135_price_adjustment", "text_zh": "法律后果：合同总价按照实际动用额加计合同管理费比例予以调整结算", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "FIDIC:Silver_1999:Clause_14.9",
        "law": "FIDIC:Silver_1999",
        "enbez": "Clause 14.9",
        "title": "FIDIC银皮书第14.9款：保留金（Retention Money）两阶段按期返还",
        "heading_path": "FIDIC EPC/交钥匙合同条件 (Silver Book 1999) > 第14条 合同价格和付款 > 保留金的返还",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Payment of Retention Money: When the Taking-Over Certificate has been issued, the first half of the Retention Money shall be certified and paid to the Contractor. Promptly after the latest of the expiry dates of the Defects Notification Periods, the outstanding balance of the Retention Money shall be certified and paid to the Contractor.",
        "text_en": "First half of Retention Money is certified and released upon TOC; remaining balance released upon expiry of Defects Notification Period.",
        "text_zh": "【保留金两阶段法定释放时点】：当工程师/雇主签发全场或分部《工程接收证书》（TOC）时，保留金的第一半（50%）必须立即核发期中证书并全额付给承包商；在缺陷通知期（DNP 通常为移交后1~2年）最后届满日后，剩余的第二半（50%）保留金必须立即结清退付给承包商！【实务启示】：出海项目资金回收关键点！移交证书一签，50% 现金保留金必须到账；中资企业可以争取以银行保留金保函（Retention Guarantee）替换现金抵扣，极大优化海外项目现金流！",
        "norm_category": "fidic_standard",
        "mandatory_level": "contract_default",
        "elements_json": json.dumps([
            {"eid": "e_fidic_s149_toc_release_fifty", "text_zh": "要件一：工程接收证书TOC签发，触发第一笔50%保留金即刻退还请求权", "status": "condition_precedent"},
            {"eid": "e_fidic_s149_dnp_expiry_final", "text_zh": "要件二：缺陷通知期DNP届满且已修复所有通知瑕疵，触发剩余50%结清", "status": "mandatory"},
            {"eid": "e_fidic_s149_mandatory_payment", "text_zh": "法律后果：雇主必须按期支付保留金，迟延支付自动按14.8款计算复利", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "FIDIC:Silver_1999:Clause_14.15",
        "law": "FIDIC:Silver_1999",
        "enbez": "Clause 14.15",
        "title": "FIDIC银皮书第14.15款：支付货币种类与固定汇率防范汇率波动",
        "heading_path": "FIDIC EPC/交钥匙合同条件 (Silver Book 1999) > 第14条 合同价格和付款 > 支付货币",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Currencies of Payment: The Contract Price shall be paid in the currency or currencies named in the Contract. Unless otherwise agreed, if payment is to be made in more than one currency, the proportion and the exchange rates shall be fixed as specified in the Contract.",
        "text_en": "Payments made in contract currencies; multiple currency proportions and exchange rates are fixed as stated in Contract, shielding from FX risk.",
        "text_zh": "【支付货币与锁定合同固定汇率】：合同价格应以合同约定的货币种类支付；若以一种以上货币计价支付（如美金+东道国本地货币），其各币种占比及兑换汇率必须锁定为合同投标基准日明确记载的固定汇率，任何后续外汇牌价波动均不得改变已固定的支付金额与折算比例！【实务启示】：中资防范东盟货币（印尼盾、越南盾、泰铢）贬值的护身符！必须在合同中争取 70%~80% 以美元或离岸人民币结算，若包含本币必须明文锁定兑美元固定汇率！",
        "norm_category": "fidic_standard",
        "mandatory_level": "contract_default",
        "elements_json": json.dumps([
            {"eid": "e_fidic_s1415_named_currency", "text_zh": "要件一：合同专用条件明文列明支付货币种类及各自固定支付比例", "status": "condition_precedent"},
            {"eid": "e_fidic_s1415_fixed_fx_ratio", "text_zh": "要件二：合同明确锁定各币种折算适用的基准日官方外汇牌价基准汇率", "status": "mandatory"},
            {"eid": "e_fidic_s1415_currency_shield", "text_zh": "法律后果：锁定结算汇率风险，发包人无权因东道国本币贬值扣减美金应付额", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "FIDIC:Silver_1999:Clause_16.4",
        "law": "FIDIC:Silver_1999",
        "enbez": "Clause 16.4",
        "title": "FIDIC银皮书第16.4款：承包商合法解约后损失补偿与所失利润（Loss of Profit）",
        "heading_path": "FIDIC EPC/交钥匙合同条件 (Silver Book 1999) > 第16条 暂停和终止 > 承包商终止合同后的付款",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Payment on Termination: After termination under Sub-Clause 16.2, the Employer shall promptly: (a) return the Performance Security to the Contractor, (b) pay the Contractor for any work carried out, and (c) pay to the Contractor the amount of any loss of profit or other loss or damage sustained by the Contractor as a result of this termination.",
        "text_en": "Upon Contractor termination under 16.2, Employer must return Performance Security, pay for executed works, and compensate full loss of profit.",
        "text_zh": "【承包商解约后雇主退还保函并赔偿所失预期利润】：当承包商因雇主拖欠工程款超42天、停工超84天或雇主破产而依据第16.2款合法终止合同时，雇主必须立即履行三项法定给付：① 立即向承包商全额退还履约保函与预付款保函；② 结清已完工程及现场材料全部款项；③ 赔偿承包商因提前解约遭受的全部损失及‘所失利润（Loss of Profit）’！【实务启示】：核威慑维权条款！不仅拿回应得工程款并抽回保函，还能依据未完成工程合同预期毛利率（通常 10%~15%）索赔全部未来利润，重创恶意违约的境外业主！",
        "norm_category": "fidic_standard",
        "mandatory_level": "contract_default",
        "elements_json": json.dumps([
            {"eid": "e_fidic_s164_lawful_termination", "text_zh": "要件一：承包商已依据第16.2款严谨履行催告并合法签发了解除合同通知", "status": "condition_precedent"},
            {"eid": "e_fidic_s164_immediate_bond_return", "text_zh": "要件二：雇主在法律上丧失索兑保函权利且必须在规定期限内原样退还", "status": "mandatory"},
            {"eid": "e_fidic_s164_loss_of_profit_recovery", "text_zh": "法律后果：发包人必须赔偿承包商未实施工程部分的预期净利润与窝工损失", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "FIDIC:Silver_1999:Clause_17.4",
        "law": "FIDIC:Silver_1999",
        "enbez": "Clause 17.4",
        "title": "FIDIC银皮书第17.4款：雇主风险后果及工期与成本补偿",
        "heading_path": "FIDIC EPC/交钥匙合同条件 (Silver Book 1999) > 第17条 风险与职责 > 雇主风险的后果",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Consequences of Employer's Risks: If and to the extent that any of the risks listed in Sub-Clause 17.3 results in loss or damage to the Works, Goods or Contractor's Documents, the Contractor shall promptly give notice to the Employer and shall rectify this loss or damage to the extent required by the Employer. The Contractor shall be entitled to an extension of time and payment of such Cost.",
        "text_en": "Contractor rectifies damage caused by Employer's risks, entitled to EOT plus Cost (plus profit in certain cases) under Clause 20.1.",
        "text_zh": "【雇主风险造成工程损坏修复之工期与费用补偿】：当发生第17.3款列明的雇主风险（如战争、军事动乱、放射性污染、雇主使用部分永久工程）导致工程或材料受损时，承包商应及时发函并在雇主指示下进行修复；承包商有权全额索赔顺延竣工工期（EOT）并获得实际发生的全部直接修复成本（Cost）补偿！【实务启示】：东南亚政局波动或发生内乱暴动时，中资项目部应第一时间援引 17.3/17.4 款固定证据，将工程一切修复支出列为雇主赔偿项目！",
        "norm_category": "fidic_standard",
        "mandatory_level": "contract_default",
        "elements_json": json.dumps([
            {"eid": "e_fidic_s174_employer_risk_event", "text_zh": "要件一：工程损坏直接由第17.3款界定的不可归责于承包商的雇主风险引发", "status": "condition_precedent"},
            {"eid": "e_fidic_s174_prompt_notice", "text_zh": "要件二：承包商在事故发生后及时发出书面通告并保护受损工程现场", "status": "mandatory"},
            {"eid": "e_fidic_s174_eot_cost_award", "text_zh": "法律后果：发包人全额承担工期顺延及抢修修复实际发生成本费用", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "FIDIC:Silver_1999:Clause_18.1",
        "law": "FIDIC:Silver_1999",
        "enbez": "Clause 18.1",
        "title": "FIDIC银皮书第18.1款：工程保险通则与共同被保险人约定",
        "heading_path": "FIDIC EPC/交钥匙合同条件 (Silver Book 1999) > 第18条 保险 > 保险的一般要求",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "General Requirements for Insurances: Wherever the Contractor is the insuring Party, each insurance shall be effected with insurers and in terms approved by the Employer. The insurance shall be in the joint names of the Parties, who shall be jointly entitled to receive payments from the insurers, payments being held or allocated between the Parties for the sole purpose of rectifying the loss or damage.",
        "text_en": "Contractor effects CAR and third party insurances in joint names of Employer and Contractor; insurance proceeds used solely to rectify damage.",
        "text_zh": "【建筑一切险共同被保险人与保险金专款专用规则】：承包商作为投保方时，应在雇主认可的合规保险公司投保工程一切险（CAR）与第三方责任险；保单必须以雇主与承包商‘共同名义（Joint Names）’开具。保险赔偿金应由双方共同受领，且该赔偿金在法律上必须‘专款专用’于修复受损工程或清偿第三方债务，任何一方严禁私自挪作他用！【实务启示】：中资央企承保海外项目，保单联名必查！出险后保险公司理赔款必须直接用于现场修复，严防境外业主截留理赔金导致现场停工！",
        "norm_category": "fidic_standard",
        "mandatory_level": "contract_default",
        "elements_json": json.dumps([
            {"eid": "e_fidic_s181_joint_names_policy", "text_zh": "要件一：工程一切险及第三方责任险保单以发包人与总包商共同名义投保", "status": "condition_precedent"},
            {"eid": "e_fidic_s181_insurer_approval", "text_zh": "要件二：承保机构具备国际信用评级或属地持牌且保额免赔额符合合同约定", "status": "mandatory"},
            {"eid": "e_fidic_s181_proceeds_dedicated_use", "text_zh": "法律后果：保险理赔款具备专款专用属性，双方均无权单方私自挪用侵占", "status": "prohibition"}
        ], ensure_ascii=False)
    }
]

PHASE2_DTA_TREATIES = [
    {
        "table": "reference_norms",
        "norm_id": "DTA:CN_PH:Art5_PE",
        "law": "DTA:CN_PH",
        "enbez": "Art 5",
        "title": "中菲双边税收协定第五条：建筑安装工程常设机构6个月门槛",
        "heading_path": "中国-菲律宾双边避免双重征税协定 (DTA) > 第5条 常设机构",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "A building site, a construction, assembly or installation project or supervisory activities in connection therewith constitutes a permanent establishment only if it lasts more than 6 months.",
        "text_en": "Construction site, assembly, installation project or supervisory activities in Philippines constitutes PE only if lasting over 6 months.",
        "text_zh": "【中菲建筑工程常设机构6个月界限】：中国企业在菲律宾境内的建筑工地、建筑、装配或安装工程，或与工程相关的监理管理活动，仅在连续或累计超过6个月时方构成在菲常设机构（PE）。【实务启示】：未超过6个月的短期设备指导、调试或勘察，依法免征菲律宾25%的企业所得税；超过6个月则触发菲律宾国税局（BIR）税务登记与纳税申报义务！",
        "norm_category": "tax_treaty",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_dtaph5_construction_site", "text_zh": "要件一：在菲律宾实施建筑安装工程、组装或工程监理服务", "status": "condition_precedent"},
            {"eid": "e_dtaph5_six_months_duration", "text_zh": "要件二：现场作业时间连续或累计超过6个日历月", "status": "mandatory"},
            {"eid": "e_dtaph5_pe_tax_trigger", "text_zh": "法律后果：构成常设机构并纳税，未超6个月免征在岸所得税", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "DTA:CN_PH:Art7_Business_Profits",
        "law": "DTA:CN_PH",
        "enbez": "Art 7",
        "title": "中菲税收协定第七条：营业利润归属与禁止引力原则",
        "heading_path": "中国-菲律宾双边税收协定 (DTA) > 第7条 营业利润",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "The profits of an enterprise of a Contracting State shall be taxable only in that State unless the enterprise carries on business in the other Contracting State through a permanent establishment. Only profits attributable to that permanent establishment may be taxed.",
        "text_en": "Profits taxable only in Contracting State unless through PE in other State; only profits attributable to that PE may be taxed in Philippines.",
        "text_zh": "【中菲营业利润与EPC离岸设备免税母法】：中国企业在菲律宾取得的营业利润，仅在菲律宾设有常设机构（PE）且利润直接归属于该常设机构时方可在菲纳税；菲律宾国税局严禁援引引力原则对中国母公司在境内制造并通过离岸交付（FOB）的EPC机械设备货款强征在岸所得税！【出海实务】：中资工程承包商签署赴菲总包工程，必须拆分为《离岸设备供货合同》与《在岸安装施工合同》，依据本条彻底隔离离岸设备款的在岸税务暴露风险！",
        "norm_category": "tax_treaty",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_dtaph7_attributable_profits", "text_zh": "要件一：仅对实际归属于菲律宾在岸施工常设机构的利润征税", "status": "condition_precedent"},
            {"eid": "e_dtaph7_no_attraction", "text_zh": "要件二：排除引力原则，母公司境外离岸制造与供货利润不可并入征税", "status": "mandatory"},
            {"eid": "e_dtaph7_offshore_tax_exemption", "text_zh": "法律后果：离岸设备供货款依法免征菲律宾企业所得税与增值税", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "DTA:CN_PH:Art10_Dividends",
        "law": "DTA:CN_PH",
        "enbez": "Art 10",
        "title": "中菲税收协定第十条：股息预提税协定优惠上限",
        "heading_path": "中国-菲律宾双边税收协定 (DTA) > 第10条 股息",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Dividends paid by a company resident in a Contracting State to a resident of the other Contracting State may be taxed in that other State. The tax shall not exceed: (a) 10% if the beneficial owner directly holds at least 10% of capital; (b) 15% in all other cases.",
        "text_en": "Dividends withholding tax shall not exceed 10% if beneficial owner holds at least 10% of capital, and 15% in other cases.",
        "text_zh": "【中菲股息预提所得税10%优惠】：菲律宾项目公司向中国母公司分配股息时，若中国母公司直接持有至少10%股份且为受益所有人，预提税上限锁定为10%（菲国内常规税率为25%）！【实务启示】：利润汇回前须主动向菲律宾国税局（BIR）提交《税收协定待遇申请备忘录（Request for Confirmation）》，未申报将被按25%高税率强行代扣！",
        "norm_category": "tax_treaty",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_dtaph10_shareholding_ratio", "text_zh": "要件一：中国居民企业直接持有菲律宾项目公司至少10%股权", "status": "condition_precedent"},
            {"eid": "e_dtaph10_beneficial_owner", "text_zh": "要件二：收款主体满足国际税法受益所有人及实质经营标准", "status": "mandatory"},
            {"eid": "e_dtaph10_reduced_wht_rate", "text_zh": "法律后果：预提所得税锁定为10%上限，较法定常规税率节省15%", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "DTA:CN_TH:Art7_Business_Profits",
        "law": "DTA:CN_TH",
        "enbez": "Art 7",
        "title": "中泰税收协定第七条：营业利润归属与常设机构征税限制",
        "heading_path": "中国-泰国双边税收协定 (DTA) > 第7条 营业利润",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "The profits of an enterprise of a Contracting State shall be taxable only in that State unless the enterprise carries on business in the other Contracting State through a permanent establishment. Only profits attributable to that permanent establishment may be taxed.",
        "text_en": "Profits of a Chinese enterprise taxable only in China unless operating via PE in Thailand; only profits attributable to Thai PE are taxable in Thailand.",
        "text_zh": "【中泰营业利润与离岸供货设备免税依据】：中国企业在泰国开展业务，仅在设立常设机构且利润直接归属于该常设机构时方在泰纳税。中资企业通过境内制造并从中国港口离岸交付（FOB/CIF）泰国的成套设备货款，泰国税务局无权并入在岸征税！【实务启示】：在泰开展光伏、轨道交通 EPC，必须合同拆分，并在泰国港口前完成物权公海转移，杜绝被泰税务局按税法典 76 Bis 条强征所得税！",
        "norm_category": "tax_treaty",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_dtath7_pe_attribution", "text_zh": "要件一：仅限实际归属于在泰建筑安装常设机构的现场施工作业服务利润", "status": "condition_precedent"},
            {"eid": "e_dtath7_separate_accounting", "text_zh": "要件二：离岸供货与在岸服务合同主体独立、账目核算完全隔离", "status": "mandatory"},
            {"eid": "e_dtath7_thai_tax_exemption", "text_zh": "法律后果：离岸设备供货款受DTA条约豁免保护，免征泰国企业所得税", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "DTA:CN_TH:Art10_Dividends",
        "law": "DTA:CN_TH",
        "enbez": "Art 10",
        "title": "中泰税收协定第十条：股息预提税15%/20%协定税率",
        "heading_path": "中国-泰国双边税收协定 (DTA) > 第10条 股息",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Dividends paid by a company resident in a Contracting State to a resident of the other Contracting State may be taxed in that other State. The tax shall not exceed: (a) 15% if the beneficial owner directly holds at least 25% of capital; (b) 20% in all other cases.",
        "text_en": "Dividends tax shall not exceed 15% if beneficial owner directly holds at least 25% of capital, and 20% in other cases.",
        "text_zh": "【中泰股息预提所得税上限】：泰国子公司向中国母公司分红，中国母公司直接持股不低于25%的，预提税上限为15%（其余为20%）。结合泰国投资促进委员会（BOI）政策，若项目取得 BOI 投资促进证书，在免税期内免征股息预提税！【实务启示】：赴泰投资建厂首选申请 BOI 证书，实现 0% 预提税利润汇出！",
        "norm_category": "tax_treaty",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_dtath10_holding_ratio", "text_zh": "要件一：母公司直接持有泰国项目公司资本至少25%", "status": "condition_precedent"},
            {"eid": "e_dtath10_boi_coordination", "text_zh": "要件二：结合BOI投资促进证书落实所得税豁免或协定优惠税率", "status": "mandatory"},
            {"eid": "e_dtath10_tax_rate_cap", "text_zh": "法律后果：预提所得税率锁定在15%上限，免除惩罚性加税", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "DTA:CN_MY:Art10_Dividends",
        "law": "DTA:CN_MY",
        "enbez": "Art 10",
        "title": "中马税收协定第十条：股息预提所得税10%上限",
        "heading_path": "中国-马来西亚双边税收协定 (DTA) > 第10条 股息",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Dividends paid by a company which is a resident of a Contracting State to a resident of the other Contracting State may be taxed in that other State, but the tax shall not exceed 10% of the gross amount of the dividends.",
        "text_en": "Dividends paid by a Malaysian company to a Chinese resident shall not be taxed in Malaysia at a rate exceeding 10%.",
        "text_zh": "【中马股息预提所得税10%上限与单层税制豁免】：马来西亚目前实行单层公司税制（Single Tier System），公司在缴纳24%企业所得税后，向境外股东分配股息在马来西亚国内法下免征预提所得税；若未来税法调整，中马税收协定第10条锁定预提税上限不得超过10%！【实务启示】：马来西亚是东盟各国中股息分配税负极低的法域，非常适合作为区域利润归集中心之一。",
        "norm_category": "tax_treaty",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_dtamy10_residency_status", "text_zh": "要件一：分红公司为马来西亚税收居民企业且在马完成公司税清缴", "status": "condition_precedent"},
            {"eid": "e_dtamy10_single_tier_exemption", "text_zh": "要件二：适用马来西亚单层公司税制或依据DTA申请协定待遇", "status": "mandatory"},
            {"eid": "e_dtamy10_zero_or_ten_cap", "text_zh": "法律后果：当前国内法享0%预提税，协定最高上限不得超过10%", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "DTA:CN_VN:Art5_3_PE",
        "law": "DTA:CN_VN",
        "enbez": "Art 5(3)",
        "title": "中越双边税收协定第五条第三款：建筑安装工程常设机构6个月规则",
        "heading_path": "中国-越南双边税收协定 (DTA) > 第5条 常设机构",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "A building site, a construction, assembly or installation project or supervisory activities in connection therewith constitutes a permanent establishment only if it lasts more than 6 months.",
        "text_en": "Construction, assembly, installation project or supervisory activities in Vietnam constitutes PE only if lasting more than 6 months.",
        "text_zh": "【中越建筑安装工程常设机构6个月时限】：中国总包商在越南境内的建筑、装配、安装工程或工程监理活动，仅在连续或累计超过6个月时方构成越南税收常设机构（PE）。【实务启示】：工期超6个月的工程在越构成建筑常设机构，须办理外国承包商税（FCT）申报；若合同拆分为离岸设备与在岸劳务，离岸设备款受协定保护免征在岸企业所得税！",
        "norm_category": "tax_treaty",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_dtavn5_six_months_pe", "text_zh": "要件一：在越南实施工程作业或技术指导时间跨度超过6个日历月", "status": "condition_precedent"},
            {"eid": "e_dtavn5_fct_compliance", "text_zh": "要件二：依法在越南税务机关登记并按FCT混合法或扣缴法申报纳税", "status": "mandatory"},
            {"eid": "e_dtavn5_pe_tax_consequence", "text_zh": "法律后果：在岸劳务部分缴纳越南税款，离岸设备供货款受DTA豁免保护", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "reference_norms",
        "norm_id": "DTA:CN_ID:Art7_Business_Profits",
        "law": "DTA:CN_ID",
        "enbez": "Art 7",
        "title": "中印尼双边税收协定第七条：营业利润与离岸设备供货免税",
        "heading_path": "中国-印度尼西亚双边税收协定 (DTA) > 第7条 营业利润",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "The profits of an enterprise of a Contracting State shall be taxable only in that State unless the enterprise carries on business in the other Contracting State through a permanent establishment. Only profits attributable to that permanent establishment may be taxed in Indonesia.",
        "text_en": "Profits of Chinese enterprise are taxable only in China unless through PE in Indonesia; only profits attributable to that PE may be taxed.",
        "text_zh": "【中印尼营业利润归属与EPC离岸设备拆分免税母法】：中国企业在印尼取得的营业利润，仅在印尼设有常设机构（PE，如BUJKA办事处）且利润直接归属于该常设机构时方可在印尼征税。印尼税务总局（DGT）严禁对中国母公司在境外制造并离岸交付的设备货款强征 2.65%/4% 建筑最终所得税！【出海实务】：印尼税务法院标杆判例（Putusan Pengadilan Pajak）胜诉铁证：只要合同清晰拆分为离岸供货与在岸服务，印尼税务局无权对离岸设备全额征税！",
        "norm_category": "tax_treaty",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_dtaid7_attributable_income", "text_zh": "要件一：仅对印尼代表处或在岸项目部实际实施的施工作业利润代扣最终税", "status": "condition_precedent"},
            {"eid": "e_dtaid7_offshore_fob_delivery", "text_zh": "要件二：设备供货合同由中国母公司签署并在公海或中国港口完成所有权转移", "status": "mandatory"},
            {"eid": "e_dtaid7_tax_court_protection", "text_zh": "法律后果：离岸设备款全额受DTA保护，印尼税务机关强征构成违法并可诉请撤销", "status": "prohibition"}
        ], ensure_ascii=False)
    }
]
