# -*- coding: utf-8 -*-
"""Phase 9 阶梯式长尾法条扩充 - Batch 1 (实务域 01、02、03)
实务域 01: 民商法典总则、合同成立、代理权限与合同解释
实务域 02: 违约救济、解约程序、违约金、情势变更与抗辩权
实务域 03: 建设工程专门法、施工资质牌照、分包管理与快速裁决
严格遵循《数据库审查.md》第五部分字段规范与 elements_json 结构化标准。
"""

import json

BATCH1_STATUTES = [
    # =========================================================================
    # 实务域 01: 合同成立、代理权限与合同解释 (L1)
    # =========================================================================
    {
        "table": "norms",
        "norm_id": "ID:KUHPerdata:Art1342",
        "law": "ID:KUHPerdata",
        "enbez": "Art 1342",
        "title": "印尼民法典第1342条：合同文字清晰禁止曲解与客观文义解释",
        "heading_path": "印尼民法典 > 第三编 债权法 > 第二章 契约之债 > 合同解释",
        "language_mode": "trilingual",
        "lang_original": "id",
        "text_original": "Jika kata-kata suatu perjanjian adalah jelas, maka tidak diperkenankan untuk menyimpang daripadanya dengan jalan penafsiran.",
        "text_en": "If the words of a contract are clear, it is not permitted to deviate from them by way of interpretation.",
        "text_zh": "【文义清晰禁止曲解原则】：若合同条款文字文义清晰明确，则裁判机构与当事人一律不得借由所谓合同解释曲解或偏离其字面明确含义。【出海实务攻防】：在印尼涉外工程合同中，若合同专用条件明确约定了工期节点、违约金上限或放弃特定抗辩，只要印尼文或双语合同文本无歧义，地方法院与仲裁庭必须优先遵循字面客观约定，阻断业主以所谓‘缔约真实默示背景’架空清晰合同条款。",
        "norm_category": "statute",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_id1342_clear_wording", "text_zh": "要件一：合同条款所采用的法律用语及商业约定在文义上客观清晰且无歧义", "status": "condition_precedent"},
            {"eid": "e_id1342_prohibition_deviate", "text_zh": "要件二：当事人或裁判机构被法定禁止通过扩张或限缩解释偏离字面含义", "status": "mandatory"},
            {"eid": "e_id1342_legal_effect", "text_zh": "法律后果：字面条款直接产生拘束力，任何背离字面的外部主张均不予采信", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "ID:KUHPerdata:Art1792",
        "law": "ID:KUHPerdata",
        "enbez": "Art 1792",
        "title": "印尼民法典第1792条：委托代理之成立与授权要件",
        "heading_path": "印尼民法典 > 第三编 债权法 > 第十六章 委任 > 代理权限",
        "language_mode": "trilingual",
        "lang_original": "id",
        "text_original": "Pemberian kuasa adalah suatu persetujuan dengan mana seorang memberikan kekuasaan kepada seorang lain, yang menerimanya, untuk atas namanya menyelenggarakan suatu urusan.",
        "text_en": "Granting of power of attorney is an agreement whereby a person authorizes another, who accepts it, to perform a business matter in the principal's name.",
        "text_zh": "【委托代理基本原则】：授权委托系一种协议，一人据此授予他人以本人名义办理特定法律事务的权力，受托人接受该授权。【出海实务攻防】：外资公司在印尼签署工程合同或变更纪要，签字人若非印尼公司注册法定代表人（Direktur Utama），必须持有股东会/董事会合法签发的特别授权委托书（Surat Kuasa Khusus），否则相对人有权主张合同处于效力待定或对公司不生效力。",
        "norm_category": "statute",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_id1792_valid_grant", "text_zh": "要件一：本人已依法作出书面或法定明示授权指令", "status": "condition_precedent"},
            {"eid": "e_id1792_acceptance", "text_zh": "要件二：代理人已明确接受授权并在授权范围内行为", "status": "mandatory"},
            {"eid": "e_id1792_scope_binding", "text_zh": "法律后果：在授权范围内的签约与表意直接对本人产生完全拘束力", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "VN:Civil_Code_2015:Art3",
        "law": "VN:Civil_Code_2015",
        "enbez": "Art 3",
        "title": "越南2015民法典第3条：民法基本原则与公共秩序底线",
        "heading_path": "越南2015民法典 > 第一编 总则 > 第一章 基本原则",
        "language_mode": "trilingual",
        "lang_original": "vi",
        "text_original": "Các nguyên tắc cơ bản của pháp luật dân sự: Mọi cá nhân, pháp nhân đều bình đẳng; Các bên tự do cam kết, thỏa thuận không trái pháp luật, đạo đức xã hội; Thiện chí, trung thực; Không xâm phạm lợi ích quốc gia, dân tộc, lợi ích công cộng.",
        "text_en": "Fundamental principles of civil law: Equality of all legal persons; Freedom of contract not violating laws or social morals; Good faith and honesty; No infringement upon national interests, public interests.",
        "text_zh": "【民法基本原则（撤销仲裁裁决母条）】：民事主体法律地位平等；自愿在不违反法律禁止性规定和社会公德前提下达成协议；行使民事权利履行义务必须遵循诚实信用；不得侵犯国家利益、社会公共利益。【出海实务攻防】：越南法院在司法审查外国仲裁裁决（包括 VIAC 或 SIAC 涉越裁决）时，最常引用的撤销事由即为‘违反越南法律基本原则’，其核心实定法源即来源于第3条。合同条款严禁存在损害越南国家能源安全、越权免税或规避法定强行法的违规安排。",
        "norm_category": "statute",
        "mandatory_level": "mandatory_override",
        "elements_json": json.dumps([
            {"eid": "e_vn3_freedom_boundary", "text_zh": "要件一：合同约定不得违反越南强行法律规范及公序良俗", "status": "condition_precedent"},
            {"eid": "e_vn3_good_faith", "text_zh": "要件二：民事权利行使与抗辩必须遵循客观诚实信用原则", "status": "mandatory"},
            {"eid": "e_vn3_national_interest", "text_zh": "法律后果：凡严重违背民法基本原则的行为及裁决，越南法院有权认定无效或撤销", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "VN:Civil_Code_2015:Art122",
        "law": "VN:Civil_Code_2015",
        "enbez": "Art 122",
        "title": "越南2015民法典第122条：民事法律行为无效之法定条件",
        "heading_path": "越南2015民法典 > 第一编 总则 > 第四章 民事法律行为 > 民事行为无效",
        "language_mode": "trilingual",
        "lang_original": "vi",
        "text_original": "Giao dịch dân sự không có một trong các điều kiện được quy định tại Điều 117 của Bộ luật này thì vô hiệu, trừ trường hợp Bộ luật này có quy định khác.",
        "text_en": "A civil transaction lacking any of the conditions provided in Article 117 of this Code shall be invalid, unless otherwise provided by this Code.",
        "text_zh": "【民事行为无效总纲】：民事法律行为欠缺第117条规定的有效要件（主体资格、意思表示真实、内容与形式合法）之一的，自始绝对无效，本法另有规定的除外。【出海实务攻防】：在越南设立项目公司或签署EPC合同，若签字代表越权且未经事后追认，或未取得必须的外国承包商许可证（Contractor Permit），对方当事人或破产管理人可直接依据第122条主张合同整体或涉案条款自始无效。",
        "norm_category": "statute",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_vn122_lack_condition", "text_zh": "要件一：法律行为确属欠缺法定主体资格、意思表示真实或形式合法要件", "status": "condition_precedent"},
            {"eid": "e_vn122_invalidation", "text_zh": "要件二：经法院或仲裁庭依法确认为无效民事行为", "status": "mandatory"},
            {"eid": "e_vn122_null_ab_initio", "text_zh": "法律后果：自成立起不发生民事法律效力，双方负有恢复原状与过错赔偿责任", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "VN:Civil_Code_2015:Art124",
        "law": "VN:Civil_Code_2015",
        "enbez": "Art 124",
        "title": "越南2015民法典第124条：虚伪意思表示与掩盖真实交易之无效",
        "heading_path": "越南2015民法典 > 第一编 总则 > 第四章 民事法律行为 > 虚伪表示",
        "language_mode": "trilingual",
        "lang_original": "vi",
        "text_original": "Khi các bên xác lập giao dịch dân sự một cách giả tạo nhằm che giấu một giao dịch dân sự khác thì giao dịch dân sự giả tạo vô hiệu, còn giao dịch dân sự bị che giấu vẫn có hiệu lực, trừ trường hợp giao dịch đó cũng vô hiệu.",
        "text_en": "Where parties enter into a sham civil transaction to conceal another transaction, the sham transaction is void, while the concealed transaction remains valid, unless it is also void.",
        "text_zh": "【通谋虚伪表示与掩盖交易无效】：当事人通谋设立虚假民事法律行为以掩盖另一真实交易的，虚假行为绝对无效；被掩盖的真实交易仍发生法律效力，除非该真实交易本身亦违反法律强制性规定。【出海实务攻防】：中资企业在越南通过本地自然人‘代持股权（Nominee）’或订立阴阳合同规避外资准入限制的，表面代持协议一律依据第124条被认定为虚假交易而无效，且真实中资控股意图若触犯外资限制亦同样归于绝对无效。",
        "norm_category": "statute",
        "mandatory_level": "mandatory_override",
        "elements_json": json.dumps([
            {"eid": "e_vn124_sham_nature", "text_zh": "要件一：双方当事人通谋作出不符合真实意思的虚假外在行为", "status": "condition_precedent"},
            {"eid": "e_vn124_hidden_transaction", "text_zh": "要件二：虚假行为目的系掩盖背后的真实基础法律关系", "status": "mandatory"},
            {"eid": "e_vn124_sham_void", "text_zh": "法律后果：外在虚伪合同自始无效，被掩盖合同若违反禁止性规定亦绝对无效", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "VN:Civil_Code_2015:Art138",
        "law": "VN:Civil_Code_2015",
        "enbez": "Art 138",
        "title": "越南2015民法典第138条：委托代理权限与特别授权范围",
        "heading_path": "越南2015民法典 > 第一编 总则 > 第七章 代理 > 委托代理",
        "language_mode": "trilingual",
        "lang_original": "vi",
        "text_original": "Cá nhân, pháp nhân có thể ủy quyền cho cá nhân, pháp nhân khác xác lập, thực hiện giao dịch dân sự. Người đại diện chỉ được xác lập, thực hiện giao dịch dân sự trong phạm vi đại diện.",
        "text_en": "An individual or legal person may authorize another to establish and perform civil transactions. The representative may only act within the authorized scope of representation.",
        "text_zh": "【委托代理权限范围】：自然人、法人可以授权其他主体代为设立、变更民事法律关系。代理人仅得在明示授权范围内实施民事法律行为。【出海实务攻防】：在越南总包项目现场，越方项目经理签署的‘现场签证单’或‘工期顺延确认备忘录’，承包商必须事先核验其所持有的公司授权委托书（Giấy ủy quyền）是否包含造价变更确认权，防范越方后续以‘超越代理权限’为由主张对公司不具约束力。",
        "norm_category": "statute",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_vn138_valid_poa", "text_zh": "要件一：持有被代理法人法定代表人签发的有效书面授权委托书", "status": "condition_precedent"},
            {"eid": "e_vn138_within_scope", "text_zh": "要件二：代理签署的工程文件在明确列举的授权权限范围之内", "status": "mandatory"},
            {"eid": "e_vn138_principal_bound", "text_zh": "法律后果：合法授权行为直接约束被代理法人，超出授权范围的行为对本人不生效力", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "MY:Contracts_Act_1950:Sec2",
        "law": "MY:Contracts_Act_1950",
        "enbez": "Sec 2",
        "title": "马来西亚1950年合同法第2条：合同成立、对价与协议定义",
        "heading_path": "马来西亚1950年合同法 > 第I部 契约初步 > 释义与成立要件",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "When one person signifies to another his willingness to do or to abstain from doing anything, with a view to obtaining the assent of that other to the act or abstinence, he is said to make a proposal. An agreement enforceable by law is a contract.",
        "text_en": "When one person signifies to another his willingness to do or to abstain from doing anything, with a view to obtaining the assent of that other to the act or abstinence, he is said to make a proposal. An agreement enforceable by law is a contract.",
        "text_zh": "【要约、承诺与对价法定定义】：一人向他人表示愿意作为或不作为以取得他人同意者，构成要约；要约经接受即为承诺与协议；受法律强制力拘束之协议方构成合同；当事人互负的给付或忍受义务构成法定对价（Consideration）。【出海实务攻防】：在马来西亚普通法与成文法双轨制下，任何工程意向书（LOI）或中标通知书（LOA）若缺乏明确对价或仅构成‘预约谈判’，守约方无法依据合同法主张实质履约请求权，必须审查是否已具备实质性对价与终局性合意。",
        "norm_category": "statute",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_my2_valid_proposal", "text_zh": "要件一：一方发出具有受拘束意思表示的明确要约与对价承诺", "status": "condition_precedent"},
            {"eid": "e_my2_unconditional_acceptance", "text_zh": "要件二：相对方作出实质一致且未实质修改的无条件接受承诺", "status": "mandatory"},
            {"eid": "e_my2_binding_contract", "text_zh": "法律后果：形成具有法定法律强制执行力的正式工程商事合同", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "MY:Contracts_Act_1950:Sec14",
        "law": "MY:Contracts_Act_1950",
        "enbez": "Sec 14",
        "title": "马来西亚1950年合同法第14条：自由合意与意思表示瑕疵分类",
        "heading_path": "马来西亚1950年合同法 > 第II部 合同成立与有效性 > 自由合意",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Consent is said to be free when it is not caused by: (a) coercion; (b) undue influence; (c) fraud; (d) misrepresentation; or (e) mistake. Consent is said to be so caused when it would not have been given but for the existence of such coercion, undue influence, fraud, misrepresentation, or mistake.",
        "text_en": "Consent is said to be free when it is not caused by coercion, undue influence, fraud, misrepresentation, or mistake. Consent is deemed caused when it would not have been given but for such defects.",
        "text_zh": "【自由合意五大排除要件】：合同当事人之合意，若非因胁迫（Coercion）、不当影响（Undue Influence）、欺诈（Fraud）、虚假陈述（Misrepresentation）或重大错误（Mistake）引起，方为自由合意；若无上述瑕疵即不会作出同意表示者，构成意思表示瑕疵。【出海实务攻防】：在工程索赔结案和解中，若业主利用承包商资金链极度断裂或扣留关键设备施加经济胁迫（Economic Duress），承包商可在事后依第14条主张和解免责声明缺乏自由合意而撤销。",
        "norm_category": "statute",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_my14_defect_presence", "text_zh": "要件一：存在法定胁迫、不当影响、欺诈或重大虚假陈述事实", "status": "condition_precedent"},
            {"eid": "e_my14_but_for_causation", "text_zh": "要件二：该瑕疵直接导致相对方作出若无瑕疵决不会给出的合意", "status": "mandatory"},
            {"eid": "e_my14_voidable_right", "text_zh": "法律后果：受害方享有法定的合同解除或撤销撤销权（Voidable）", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "MY:Contracts_Act_1950:Sec28",
        "law": "MY:Contracts_Act_1950",
        "enbez": "Sec 28",
        "title": "马来西亚1950年合同法第28条：限制贸易条款自始绝对无效",
        "heading_path": "马来西亚1950年合同法 > 第II部 合同有效性 > 违法与无效约定",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Every agreement by which anyone is restrained from exercising a lawful profession, trade, or business of any kind, is to that extent void, save for statutory exceptions relating to sale of goodwill and partnership.",
        "text_en": "Every agreement by which anyone is restrained from exercising a lawful profession, trade, or business of any kind, is to that extent void, save for statutory exceptions.",
        "text_zh": "【限制贸易与竞争条款绝对无效】：除出让商誉或合伙解散之法定特许例外情形外，任何限制当事人从事合法职业、贸易或任何类型正当商业活动的协议约定，在该限制范围内自始绝对无效。【出海实务攻防】：在马来西亚分包或工程技术协议中，若业主或总包强加严苛的‘5年内禁止在全马承接任何同类工程’的竞业限制条款，该条款直接触犯第28条强行法而绝对无效，对中企不发生任何阻断效力。",
        "norm_category": "statute",
        "mandatory_level": "mandatory_override",
        "elements_json": json.dumps([
            {"eid": "e_my28_restraint_clause", "text_zh": "要件一：合同条款包含限制相对人开展合法工程业务或竞标的约束", "status": "condition_precedent"},
            {"eid": "e_my28_no_statutory_exception", "text_zh": "要件二：该限制不属于法定商誉买卖或合伙散伙豁免范围", "status": "mandatory"},
            {"eid": "e_my28_void_ab_initio", "text_zh": "法律后果：该限制贸易约定自始绝对无效，当事人不受任何约束", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "TH:CCC:Sec149",
        "law": "TH:CCC",
        "enbez": "Sec 149",
        "title": "泰国民商法典第149条：法律行为成立与合法目的要件",
        "heading_path": "泰国民商法典 > 第一编 总则 > 第四章 法律行为 > 一般规定",
        "language_mode": "trilingual",
        "lang_original": "th",
        "text_original": "นิติกรรม หมายความว่า การใดๆ อันทำลงโดยชอบด้วยกฎหมายและด้วยใจสมัคร มุ่งโดยตรงต่อการผูกนิติสัมพันธ์ขึ้นระหว่างบุคคล เพื่อจะก่อ เปลี่ยนแปลง โอน สงวน หรือระงับซึ่งสิทธิ",
        "text_en": "Juridical acts are voluntary lawful acts, the immediate purpose of which is to establish legal relations between persons, to create, modify, transfer, preserve or extinguish rights.",
        "text_zh": "【法律行为与自愿要件】：法律行为系指依法自愿实施、以在民事主体之间设立法律关系为直接目的，从而产生、变更、转让、保持或消灭权利的行为。【出海实务攻防】：在泰国承揽工程，一切备忘录与技术协议必须出于真实自愿且不违背公共秩序。凡在政府官员不正当干预或无资质非法挂靠情形下签署的协议，泰国法院有权直接否定其具备第149条之法律行为合法性。",
        "norm_category": "statute",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_th149_voluntary_act", "text_zh": "要件一：主体自愿实施产生法律效果之明示意思表示", "status": "condition_precedent"},
            {"eid": "e_th149_lawful_purpose", "text_zh": "要件二：行为目的符合泰国实定法律规范与公共秩序", "status": "mandatory"},
            {"eid": "e_th149_legal_relationship", "text_zh": "法律后果：在当事人之间产生排他性法定权利义务设立与拘束力", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "TH:CCC:Sec155",
        "law": "TH:CCC",
        "enbez": "Sec 155",
        "title": "泰国民商法典第155条：通谋虚伪表示与掩盖隐藏行为效力",
        "heading_path": "泰国民商法典 > 第一编 总则 > 第四章 法律行为 > 意思表示瑕疵",
        "language_mode": "trilingual",
        "lang_original": "th",
        "text_original": "การแสดงเจตนาลวงด้วยสมรู้กับคู่กรณีอีกฝ่ายหนึ่งเป็นโมฆะ แต่จะยกขึ้นเป็นข้อต่อสู้บุคคลภายนอกผู้กระทำการโดยสุจริตและต้องเสียหายมิได้",
        "text_en": "A declaration of intention made with the connivance of the other party in collusion is void; but its invalidity cannot be set up against third persons acting in good faith.",
        "text_zh": "【通谋虚伪与善意第三人保护】：与相对人通谋串通作出的虚伪意思表示绝对无效；但该无效不得用以对抗善意并因而遭受损害的第三人；若虚伪表示旨在掩盖另一真实法律行为，应依该真实行为之法律规定审查效力。【出海实务攻防】：中资在泰通过泰国自然人或‘空壳公司代持股权’以规避 FBA 外商经营法 49% 股比限制的代持协议，直接构成第155条通谋虚伪表示而绝对无效，且无法对抗债权人及善意第三方对代持股权的查封拍卖。",
        "norm_category": "statute",
        "mandatory_level": "mandatory_override",
        "elements_json": json.dumps([
            {"eid": "e_th155_collusion", "text_zh": "要件一：双方当事人明知虚假而恶意通谋实施虚伪行为", "status": "condition_precedent"},
            {"eid": "e_th155_voidness", "text_zh": "要件二：该表面通谋行为依法被裁定为自始绝对无效", "status": "mandatory"},
            {"eid": "e_th155_bona_fide_protection", "text_zh": "法律后果：双方不得向善意相对人主张无效，隐藏规避行为面临追缴与罚没", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "PH:Civil_Code:Art1370",
        "law": "PH:Civil_Code",
        "enbez": "Art 1370",
        "title": "菲律宾民法典第1370条：字面客观意图与文义清晰拘束力",
        "heading_path": "菲律宾民法典 > 第四编 债权与合同 > 第二章 合同 > 合同解释",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "If the terms of a contract are clear and leave no doubt upon the intention of the contracting parties, the literal meaning of its stipulations shall control. If the words appear to be contrary to the evident intention of the parties, the latter shall prevail over the former.",
        "text_en": "If the terms of a contract are clear and leave no doubt upon the intention of the contracting parties, the literal meaning of its stipulations shall control.",
        "text_zh": "【文义解释首要原则】：若合同条款表述清晰且对当事人之意图不留任何怀疑余地，则其条款之字面文义具有绝对支配与控制力；仅当字面措辞与当事人显而易见的真实意图发生明显冲突时，真实意图方优先于字面。【出海实务攻防】：在菲律宾工程纠纷中，菲最高法院一贯严格执行‘四角规则（Four-Corner Rule）’，凡总价包干合同已对地质风险或通胀调差作出了明文约定，承包商严禁以所谓口头谈判背景推翻清晰合同文义。",
        "norm_category": "statute",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_ph1370_clear_terms", "text_zh": "要件一：合同条款文义客观明确，无重大多义或模糊不清", "status": "condition_precedent"},
            {"eid": "e_ph1370_literal_control", "text_zh": "要件二：优先直接依字面通常含义予以涵摄适用", "status": "mandatory"},
            {"eid": "e_ph1370_parol_evidence_rule", "text_zh": "法律后果：字面条款具有终局裁判力，口头证据规则排除外部反证", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "PH:Civil_Code:Art1403",
        "law": "PH:Civil_Code",
        "enbez": "Art 1403",
        "title": "菲律宾民法典第1403条：欺诈防止法与不可强制执行合同",
        "heading_path": "菲律宾民法典 > 第四编 债权与合同 > 第二章 合同 > 不可执行合同",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "The following contracts are unenforceable, unless they are ratified: (1) Those entered into in the name of another without authority; (2) Those that do not comply with the Statute of Frauds, including agreements not to be performed within a year, special promise to answer for debt of another, and agreements for leasing for more than one year or sale of real property.",
        "text_en": "The following contracts are unenforceable unless ratified: unauthorized contracts, and agreements violating the Statute of Frauds requiring written note or memorandum.",
        "text_zh": "【欺诈防止法与书面形式要件】：下列合同若未经被代理人追认或缺乏书面备忘录，在法律上不可强制执行（Unenforceable）：① 无代理权人以他人名义订立的合同；② 违反欺诈防止法（Statute of Frauds）的合同，包括履约期限超过一年的协议、为他人债务提供担保的保证承诺、超过一年的不动产租赁或买卖协议。【出海实务攻防】：在菲律宾开展长期基建工程（工期通常超过1年）或工程母公司担保，一切合同及其修改必须持有经公证（Notarized）的正式书面原件，口头约定在诉讼中直接被法院裁定不可强制执行。",
        "norm_category": "statute",
        "mandatory_level": "mandatory_override",
        "elements_json": json.dumps([
            {"eid": "e_ph1403_covered_category", "text_zh": "要件一：合同性质属于越权代理或属于履约期超1年、担保、不动产交易范畴", "status": "condition_precedent"},
            {"eid": "e_ph1403_lack_written_memo", "text_zh": "要件二：未签署符合法定要件的书面合同文书或载明必要条款之备忘录", "status": "mandatory"},
            {"eid": "e_ph1403_unenforceability", "text_zh": "法律后果：合同在法律上不可被强制执行，相对方无法据此获得判决救济", "status": "prohibition"}
        ], ensure_ascii=False)
    },

    # =========================================================================
    # 实务域 02: 违约救济、解约程序、违约金与情势变更 (L1)
    # =========================================================================
    {
        "table": "norms",
        "norm_id": "ID:KUHPerdata:Art1238",
        "law": "ID:KUHPerdata",
        "enbez": "Art 1238",
        "title": "印尼民法典第1238条：法定催告通知（Somasi）前置要件",
        "heading_path": "印尼民法典 > 第三编 债权法 > 第一章 债法总则 > 债务人迟延违约",
        "language_mode": "trilingual",
        "lang_original": "id",
        "text_original": "Debitur dinyatakan lalai dengan surat perintah, atau dengan akta sejenis itu, atau berdasarkan kekuatan dari perikatan sendiri, yaitu bila perikatan tersebut mengakibatkan debitur harus dianggap lalai dengan lewatnya waktu yang ditentukan.",
        "text_en": "The debtor is declared in default by a warrant or similar instrument, or by virtue of the obligation itself, when the obligation provides that the debtor shall be deemed in default by the mere expiration of the term.",
        "text_zh": "【法定催告令（Somasi）前置程序】：债务人迟延履行，必须经债权人发出法定书面催告令（Somasi）或具有等同效力的正式公文进行催告；或者当合同本身明文约定履行期限届满即自动构成违约且免除催告时，方可直接认定迟延违约。【出海实务攻防】：在印尼工程索赔实务中，业主主张总包迟延或总包主张业主拖欠工程款，除非合同专用条件明文约定‘免除第1238条催告’，否则必须事先发出至少 1~2 次书面催告函（Somasi），并给予合理宽限期；未经催告直接停工或索兑保函，将被法院认定程序违法并判定索赔不成立。",
        "norm_category": "statute",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_id1238_formal_notice", "text_zh": "要件一：债权人已向迟延方发出正式书面催告令并载明违约事实与履行期限", "status": "condition_precedent"},
            {"eid": "e_id1238_grace_period", "text_zh": "要件二：催告令所给予的合理履行宽限期已届满而债务人仍未纠正", "status": "mandatory"},
            {"eid": "e_id1238_default_effect", "text_zh": "法律后果：债务人正式构成法定迟延违约（Wanprestasi），违约责任正式启动", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "ID:KUHPerdata:Art1266",
        "law": "ID:KUHPerdata",
        "enbez": "Art 1266",
        "title": "印尼民法典第1266条：双务合同解除须经法院判决与约定排除",
        "heading_path": "印尼民法典 > 第三编 债权法 > 第一章 债权消灭 > 合同解除",
        "language_mode": "trilingual",
        "lang_original": "id",
        "text_original": "Syarat batal dianggap selalu dicantumkan dalam persetujuan yang bertimbal balik, manakala salah satu pihak tidak memenuhi kewajibannya. Pembatalan harus dimintakan kepada Hakim.",
        "text_en": "A resolutory condition is always implied in bilateral contracts if one party does not perform. Termination must be sought from the Court.",
        "text_zh": "【合同解除必须经法院裁决原则及约定排除】：在双务合同中，一方不履行义务时始终默示包含解除条件；但合同之正式解除必须向法院起诉请求判决准许，不得任意单方私力解除。【出海实务攻防】：印尼法律严格要求合同解除须经司法裁定，但商业实务中允许当事人在合同中明文约定‘双方特此明确放弃印尼民法典第1266条与第1267条要求法院判决解约的规定（Expressly waive Art 1266/1267）’。若涉外EPC合同漏写该放弃条款，单方发函解约将被印尼法院认定为非法解除并被判巨额违约赔偿！",
        "norm_category": "statute",
        "mandatory_level": "mandatory_override",
        "elements_json": json.dumps([
            {"eid": "e_id1266_court_requirement", "text_zh": "要件一：双务合同一方发生根本违约时法定要求向法院申请解约令", "status": "condition_precedent"},
            {"eid": "e_id1266_express_waiver", "text_zh": "要件二：审查合同文本是否已明文约定放弃民法典第1266条之适用", "status": "mandatory"},
            {"eid": "e_id1266_termination_validity", "text_zh": "法律后果：无放弃条款的单方解约不具法律效力，附放弃条款的可依约直接生效", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "VN:Commercial_Law_2005:Art301",
        "law": "VN:Commercial_Law_2005",
        "enbez": "Art 301",
        "title": "越南2005商业法第301条：商事违约金8%法定上限封顶",
        "heading_path": "越南2005商业法 > 第七章 违约救济 > 违约罚金",
        "language_mode": "trilingual",
        "lang_original": "vi",
        "text_original": "Mức phạt đối với vi phạm nghĩa vụ hợp đồng hoặc tổng mức phạt đối với nhiều vi phạm do các bên thoả thuận trong hợp đồng, nhưng không quá 8% giá trị phần nghĩa vụ hợp đồng bị vi phạm, trừ trường hợp quy định tại Điều 266 của Luật này.",
        "text_en": "The fine level for breach of a contractual obligation shall not exceed 8% of the value of the breached contractual obligation, unless otherwise provided by law.",
        "text_zh": "【商事违约金8%法定封顶上限】：合同双方可约定违约罚金，但针对单项或多项违约的罚金总额，最高不得超过该项‘被违反合同义务对应金额’的 8%，本法另有规定的除外。【出海实务攻防】：涉外商事合同（适用《商业法》体系）若约定按合同总额 10%~20% 计扣误期违约金（LDs），超出 8% 的部分越南法院与仲裁庭将依职权强行裁减并认定无效；但注意2025新建设法对纯工程合同预定违约金机制已有最新松绑趋势，需结合具体合同性质进行双法域抗辩。",
        "norm_category": "statute",
        "mandatory_level": "mandatory_override",
        "elements_json": json.dumps([
            {"eid": "e_vn301_commercial_nature", "text_zh": "要件一：争议合同属于越南《商业法》调整的商事买卖或服务合同范畴", "status": "condition_precedent"},
            {"eid": "e_vn301_breached_portion", "text_zh": "要件二：精确核算实际发生违约行为所对应的具体合同价款部分", "status": "mandatory"},
            {"eid": "e_vn301_eight_percent_cap", "text_zh": "法律后果：罚金金额依法以该部分的8%为上限封顶，超出部分绝对无效", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "VN:Civil_Code_2015:Art420",
        "law": "VN:Civil_Code_2015",
        "enbez": "Art 420",
        "title": "越南2015民法典第420条：情势变更原则五大要件与合同调整",
        "heading_path": "越南2015民法典 > 第三编 债权与合同 > 合同修改与解除",
        "language_mode": "trilingual",
        "lang_original": "vi",
        "text_original": "Thực hiện hợp đồng khi hoàn cảnh thay đổi cơ bản: Hoàn cảnh thay đổi do nguyên nhân khách quan xảy ra sau khi giao kết hợp đồng; Các bên không thể lường trước được; Hoàn cảnh thay đổi lớn đến mức nếu biết trước thì hợp đồng đã không được giao kết; Việc tiếp tục thực hiện hợp đồng sẽ gây thiệt hại nghiêm trọng.",
        "text_en": "Performance of contracts upon fundamental change of circumstances: Change occurs after contract conclusion due to objective causes; Unforeseeable; Material impact; Severe prejudice if continued without modification.",
        "text_zh": "【情势变更原则五大构成要件】：因客观事由在缔约后发生重大情势变更；当事人缔约时无法预见；情势发生重大变化致使若预知则决不会签约或条件迥异；继续按原合同履行将导致一方遭受严重损害；受损方已采取一切必要救济措施。满足要件时，双方应重新协商；协商不成可请求法院变更或终止合同。【出海实务攻防】：当越南出现全球性建筑钢材水泥暴涨超50%或重大电价新政调整时，承包商可依第420条向越方业主启动正式调价重签谈判，若业主拒绝可依法请求裁判机构介入调整合同价格。",
        "norm_category": "statute",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_vn420_objective_change", "text_zh": "要件一：缔约后发生不可归责于当事人的客观重大情势剧变", "status": "condition_precedent"},
            {"eid": "e_vn420_unforeseeable", "text_zh": "要件二：该情势变化在缔约当时属于商业上不可合理预见的异常事件", "status": "mandatory"},
            {"eid": "e_vn420_renegotiation_or_court", "text_zh": "法律后果：触发法定重新谈判程序，协商未果有权请求法院依公平原则调整价格或解约", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "MY:Contracts_Act_1950:Sec57",
        "law": "MY:Contracts_Act_1950",
        "enbez": "Sec 57",
        "title": "马来西亚1950年合同法第57条：合同落空（Frustration）与嗣后不能",
        "heading_path": "马来西亚1950年合同法 > 第IV部 合同的履行 > 履行不能",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "An agreement to do an act impossible in itself is void. A contract to do an act which, after the contract is made, becomes impossible, or by reason of some event which the promisor could not prevent, unlawful, becomes void when the act becomes impossible or unlawful.",
        "text_en": "A contract to do an act which, after contract is made, becomes impossible or unlawful becomes void when the act becomes impossible or unlawful.",
        "text_zh": "【合同嗣后履行不能与合同落空】：自始履行不能之协议无效；合同成立后，因发生当事人无法防止的外部事件致使履行在物理上变为不可能或法律上变为非法的，该合同自该事件发生时起自动归于无效（Becomes Void）。【出海实务攻防】：在马来西亚遭遇战争、全国性紧急法令戒严或政府绝对吊销项目主批文时，承包商可援引第57条主张合同落空，阻断业主追索违约金；但注意普通物价暴涨或施工难度增加在马来判例中绝对不构成合同落空！",
        "norm_category": "statute",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_my57_subsequent_event", "text_zh": "要件一：合同订立后发生超越当事人合理控制的外部根本性剧变", "status": "condition_precedent"},
            {"eid": "e_my57_impossibility", "text_zh": "要件二：该事件导致合同履行业已物理上彻底不能或法律上违法", "status": "mandatory"},
            {"eid": "e_my57_automatic_void", "text_zh": "法律后果：合同依法自动终止落空，双方互免后续履约责任并按公允价值结算", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "MY:Contracts_Act_1950:Sec75",
        "law": "MY:Contracts_Act_1950",
        "enbez": "Sec 75",
        "title": "马来西亚1950年合同法第75条：违约金条款与商业正当利益标准",
        "heading_path": "马来西亚1950年合同法 > 第VI部 违约后果 > 违约损害赔偿",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "When a contract has been broken, if a sum is named in the contract as the amount to be paid in case of such breach, the party complaining of the breach is entitled to receive from the party who has broken the contract reasonable compensation not exceeding the amount so named, whether or not actual damage or loss is proved to have been caused thereby.",
        "text_en": "Party complaining of breach is entitled to reasonable compensation not exceeding the amount named, whether or not actual loss is proved.",
        "text_zh": "【违约金合理补偿与比例性测试】：合同约定违约应付金额的，守约方有权获得不超过该金额的‘合理补偿’，无论是否证明发生实际损失。【出海实务攻防】：马来西亚联邦法院在先例 Cubic Electronics 中彻底确立：第75条并不要求业主逐笔证明实际损失，只要业主证明违约金数额保护的是其商业正当利益（Legitimate Commercial Interest）且非不成比例，违约金条款即完全有效，举证证明违约金畸高过度的责任完全转移由违约方承担！",
        "norm_category": "statute",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_my75_stipulated_sum", "text_zh": "要件一：合同明文约定了针对特定违约行为的定额赔偿金或计费公式", "status": "condition_precedent"},
            {"eid": "e_my75_reasonable_cap", "text_zh": "要件二：裁判机构对该金额实施合理性与保护正当商业利益审查", "status": "mandatory"},
            {"eid": "e_my75_compensation_award", "text_zh": "法律后果：支持合理违约金请求，但最高不得超出合同约定的限额上限", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "TH:CCC:Sec383",
        "law": "TH:CCC",
        "enbez": "Sec 383",
        "title": "泰国民商法典第383条：过高违约金法院依职权酌减",
        "heading_path": "泰国民商法典 > 第二编 债权 > 第二章 债之效力 > 违约金",
        "language_mode": "trilingual",
        "lang_original": "th",
        "text_original": "ถ้าเบี้ยปรับที่ตกลงกันไว้นั้นสูงเกินส่วน ศาลจะลดลงเป็นจำนวนพอสมควรก็ได้ ในการที่จะวินิจฉัยว่าสมควรเพียงใดนั้น ท่านให้พิเคราะห์ถึงทางได้เสียของเจ้าหนี้ทุกอย่างอันชอบด้วยกฎหมาย",
        "text_en": "If a forfeited penalty is disproportionately high, it may be reduced to a reasonable amount by the court. In determining reasonableness, every legal interest of the creditor shall be considered.",
        "text_zh": "【过高违约金法院酌减权】：若约定的违约金（เบี้ยปรับ）过高且显失比例，法院有权将其酌减至合理金额；在判断是否合理时，应综合考量债权人依法享有的一切合法利益，而非仅仅是其实际财产损失。【出海实务攻防】：在泰国承揽工程，若业主合同约定高达日千分之二、总额无上限的拖期误期违约金，总包商即使迟延完工，亦可依第383条向泰国中央行政法院或商事法庭诉请依职权酌减违约金至实际合理损失水平，合同中任何‘放弃请求法院酌减违约金’的条款依法无效！",
        "norm_category": "statute",
        "mandatory_level": "mandatory_override",
        "elements_json": json.dumps([
            {"eid": "e_th383_disproportionate_penalty", "text_zh": "要件一：合同约定的违约金数额在客观上畸高并显失比例平衡", "status": "condition_precedent"},
            {"eid": "e_th383_judicial_discretion", "text_zh": "要件二：法院或仲裁庭根据债权人合法利益与实际损害实施衡平审查", "status": "mandatory"},
            {"eid": "e_th383_reduction_to_reasonable", "text_zh": "法律后果：司法裁决将违约金强制下调至合理金额，约定放弃酌减权无效", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "PH:Civil_Code:Art1229",
        "law": "PH:Civil_Code",
        "enbez": "Art 1229",
        "title": "菲律宾民法典第1229条：衡平原则司法酌减显失公平违约罚金",
        "heading_path": "菲律宾民法典 > 第四编 债权与合同 > 第一章 债的类型 > 附惩罚性条款之债",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "The judge shall equitably reduce the penalty when the principal obligation has been partly or irregularly complied with by the debtor. Even if there has been no performance, the penalty may also be reduced by the courts if it is iniquitous or unconscionable.",
        "text_en": "The judge shall equitably reduce the penalty when the principal obligation has been partly or irregularly complied with, or if the penalty is iniquitous or unconscionable.",
        "text_zh": "【部分履行与显失公平罚金司法酌减】：债务人已部分履行或不规则履行主债务的，法官应当基于衡平原则酌减约定的违约罚金（Penalty Clause）；即便债务人完全未履行，若约定的罚金显失公平或显失诚信（Iniquitous or Unconscionable），法院亦有权予以酌减。【出海实务攻防】：在菲律宾工程实务中，若总包商已完成电站工程的 95% 且电站已实际并网商运，业主却依然扣留按 100% 合同额计算的误期罚金，总承包商可直接援引第1229条强制要求主事法官依衡平原则大幅扣减该违约罚金。",
        "norm_category": "statute",
        "mandatory_level": "mandatory_override",
        "elements_json": json.dumps([
            {"eid": "e_ph1229_partial_performance", "text_zh": "要件一：债务人已实施了工程实质性部分履行或该罚金显失公平", "status": "condition_precedent"},
            {"eid": "e_ph1229_equitable_test", "text_zh": "要件二：全额索赔罚金将导致债权人获得与其损失极不相称的不当暴利", "status": "mandatory"},
            {"eid": "e_ph1229_mandatory_reduction", "text_zh": "法律后果：主审法官或CIAC仲裁员负有法定审判职责裁减违约金至公平水准", "status": "prohibition"}
        ], ensure_ascii=False)
    },

    # =========================================================================
    # 实务域 03: 建设工程专门法、资质牌照、分包管理与快速裁决 (L1)
    # =========================================================================
    {
        "table": "norms",
        "norm_id": "ID:UU_2_2017:Art30",
        "law": "ID:UU_2_2017",
        "enbez": "Art 30",
        "title": "印尼建筑服务法第30条：外国建筑企业代表处设立与KSO强制联营",
        "heading_path": "印尼2017年第2号建筑服务法 > 第五章 建筑服务企业 > 外国建筑服务代表处",
        "language_mode": "trilingual",
        "lang_original": "id",
        "text_original": "Kantor Perwakilan Badan Usaha Jasa Konstruksi Asing (BUJKA) hanya dapat menyelenggarakan usaha jasa konstruksi yang berisiko besar, berteknologi tinggi, dan/atau berbiaya besar. BUJKA wajib membentuk kerja sama operasi (KSO) dengan Badan Usaha Jasa Konstruksi Nasional berkualifikasi besar.",
        "text_en": "Foreign Construction Services Representative Office (BUJKA) may only undertake high-risk, high-tech, and/or high-cost projects, and MUST form a joint operation (KSO) with large-qualification national enterprises.",
        "text_zh": "【BUJKA 执业门槛与强制 KSO 联营】：外国建筑服务企业代表处（BUJKA）仅被允许承揽具备重大风险、高新技术和/或高额造价的大型工程；BUJKA 在印尼承揽工程，必须与具备最高资质（Kualifikasi Besar）且 100% 印尼内资的本土建筑企业组建联合运营体（KSO）。【出海实务攻防】：中资工程局若仅在雅加达设立代表处而未与具备对应顶级牌照的印尼本土国企（如 Wijaya Karya、Adhi Karya、PP）组成 KSO 联营体投标，该投标及中标合同依法自始无效，且面临最高按合同额 10% 的行政罚款与驱逐出境令。",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory_override",
        "elements_json": json.dumps([
            {"eid": "e_id30_bujka_license", "text_zh": "要件一：持有公共工程与民房部（PUPR）核发的有效 BUJKA 执业准入牌照", "status": "condition_precedent"},
            {"eid": "e_id30_mandatory_kso", "text_zh": "要件二：与符合法定顶级资质要求的印尼本土 100% 内资建筑商签署真实 KSO 协议", "status": "mandatory"},
            {"eid": "e_id30_high_complexity_scope", "text_zh": "法律后果：满足条件方可在印尼合法施工，违规承揽合同无效且面临刑事罚金与停工", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "ID:UU_2_2017:Art60",
        "law": "ID:UU_2_2017",
        "enbez": "Art 60",
        "title": "印尼建筑服务法第60条：建筑物失败（Kegagalan Bangunan）十年终身法定追责",
        "heading_path": "印尼2017年第2号建筑服务法 > 第六章 建筑工程合同与责任 > 建筑物失败责任",
        "language_mode": "trilingual",
        "lang_original": "id",
        "text_original": "Penyedia Jasa wajib bertanggung jawab atas Kegagalan Bangunan dalam jangka waktu yang ditentukan dalam Kontrak Kerja Konstruksi, paling lama 10 (sepuluh) tahun terhitung sejak tanggal penyerahan akhir layanan jasa konstruksi.",
        "text_en": "Service Providers must be responsible for Building Failure (Kegagalan Bangunan) for a period determined in the contract, up to a maximum of 10 years from final handover.",
        "text_zh": "【建筑物失败最长十年法定赔偿责任】：工程承包商与设计监理方，必须在建设工程合同约定的期限内对‘建筑物失败（Kegagalan Bangunan）’承担法定修复与全额损害赔偿责任；该法定期限自工程最终竣工移交（FHO）之日起计算，最长达 10 年。【出海实务攻防】：印尼法律将建筑物坍塌或重大结构缺陷定性为不可通过普通缺陷责任期（DNP 1~2年）免除的法定特别责任；移交后10年内一旦发生由独立专家评估员认定的工程失败，总包商即使撤场亦仍须负全部赔偿责任与连带清偿责任。",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory_override",
        "elements_json": json.dumps([
            {"eid": "e_id60_building_failure_event", "text_zh": "要件一：移交后发生建筑物坍塌、结构失稳或丧失预定使用功能的建筑物失败事件", "status": "condition_precedent"},
            {"eid": "e_id60_independent_assessor", "text_zh": "要件二：由部委登记备案的独立工程评估专家（Penilai Ahli）依法出具因果归责报告", "status": "mandatory"},
            {"eid": "e_id60_ten_year_liability", "text_zh": "法律后果：竣工后最长10年内总包商承担法定赔偿与修复责任，合同约定免责无效", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "VN:Construction_Law_2025:Art148",
        "law": "VN:Construction_Law_2025",
        "enbez": "Art 148",
        "title": "越南2025新建设法第148条：外国承包商许可证（Contractor Permit）前置红线",
        "heading_path": "越南2025新建设法 (Law 135/2025/QH15) > 涉外工程承包管理",
        "language_mode": "trilingual",
        "lang_original": "vi",
        "text_original": "Nhà thầu nước ngoài chỉ được hoạt động xây dựng tại Việt Nam sau khi được cơ quan nhà nước có thẩm quyền cấp Giấy phép hoạt động xây dựng. Nhà thầu nước ngoài phải liên danh với nhà thầu Việt Nam hoặc sử dụng nhà thầu phụ Việt Nam.",
        "text_en": "Foreign contractors may only operate in Vietnam after being granted a Construction Activity License (Contractor Permit). Foreign contractors must joint-venture or subcontract with Vietnamese contractors.",
        "text_zh": "【外国承包商施工许可证强制前置】：外国承包商唯有在获得越南建设主管部门正式核发《外国承包商施工许可证》（Contractor Permit）后，方可在越南境内开展施工与工程咨询活动；外国承包商必须与越南本土承包商组建联营体，或承诺将特定工程内容分包给越南本土分包商。【出海实务攻防】：中资企业在越南中标后，必须在签约之日起向建设厅（SXD）申领该许可证并在越设立临时执行办公室（Điều hành）；未经办证擅自调动机械进场施工，建设监察总署将下达全场停工令并处以没收违法所得重罚！",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory_override",
        "elements_json": json.dumps([
            {"eid": "e_vn148_contractor_permit", "text_zh": "要件一：在中标签约后、正式开工前取得建设部或省级建设厅核发的许可证", "status": "condition_precedent"},
            {"eid": "e_vn148_local_partnership", "text_zh": "要件二：按法定比例与越南本土承包商订立合法联营或专业分包协议", "status": "mandatory"},
            {"eid": "e_vn148_stop_work_penalty", "text_zh": "法律后果：无证施工直接触发停工取缔令与高额行政处罚，施工合同面临无效风险", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "MY:CIPAA_2012:Sec35",
        "law": "MY:CIPAA_2012",
        "enbez": "Sec 35",
        "title": "马来西亚2012年建筑业付款与裁决法第35条：禁止背靠背付款条款",
        "heading_path": "马来西亚2012年建筑业付款与快速裁决法 (CIPAA Act 746) > 第四部 建筑合同有条件付款禁止",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "Any conditional payment provision in a construction contract in relation to payment is VOID. A conditional payment provision includes terms that make payment contingent on the payer receiving payment from a third party (Pay-when-paid or Pay-if-paid).",
        "text_en": "Any conditional payment provision in a construction contract is void, including pay-when-paid and pay-if-paid terms.",
        "text_zh": "【背靠背付款条款自始绝对无效】：在一切适用于本法的建设工程合同及分包协议中，任何‘有条件付款条款（Conditional Payment Provision）’一律自始绝对无效；本条明文禁止‘以总包收到业主付款为向分包付款前置条件’（Pay-when-paid / Pay-if-paid）的任何表述。【出海实务攻防】：中资总包在马来西亚分包合同中即使明文约定‘待业主款项到账后 14 日内支付分包工程款’，分包商依据 CIPAA 提起快速裁决时，该背靠背约定直接被依法宣告无效，总包商必须无条件向分包商依施工进度履行清偿义务！",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory_override",
        "elements_json": json.dumps([
            {"eid": "e_my35_construction_contract", "text_zh": "要件一：争议协议属于在马来西亚境内实施的书面工程、咨询或供货合同", "status": "condition_precedent"},
            {"eid": "e_my35_conditional_payment_clause", "text_zh": "要件二：合同约定将向下游付款与上游资金到账或第三方审批相挂钩", "status": "mandatory"},
            {"eid": "e_my35_absolute_voidness", "text_zh": "法律后果：该背靠背条款自始绝对无效，付款期限依法回退适用法定30天月结规则", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "MY:CIDB_Act_520:Sec25",
        "law": "MY:CIDB_Act_520",
        "enbez": "Sec 25",
        "title": "马来西亚建筑工业发展局法第25条：未持CIDB注册证施工属刑事犯罪",
        "heading_path": "马来西亚1994年建筑工业发展局法 (CIDB Act 520) > 第VI部 承包商注册",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "No person shall undertake or complete any construction work unless he is registered with the Lembaga (CIDB) and holds a valid certificate of registration issued by the Lembaga. Any person who contravenes subsection (1) commits an offense and shall be liable on conviction to a fine of not less than RM 10,000 but not exceeding RM 100,000.",
        "text_en": "No person shall undertake any construction work unless registered with CIDB and holding a valid certificate. Violation is a criminal offense.",
        "text_zh": "【未持 CIDB 施工注册证进场属于刑事犯罪】：任何人未在 CIDB 获得注册并持有 CIDB 签发的有效资质证书（G1~G7），严禁在马来西亚境内承揽或实施任何建设工程；违者构成刑事犯罪，最高处以 10 万林吉特罚款并按日加处罚金。【出海实务攻防】：外国承包商赴马，即便中标亦不得直接以中国母公司名义开工，必须通过注册成立本地公司或取得 CIDB 外国承包商专项临时注册证书（Temporary Certificate）；无证施工不仅项目负责人面临刑事追责，而且工程合同将因违法而丧失向法院主张支付的司法救济力！",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory_override",
        "elements_json": json.dumps([
            {"eid": "e_my25_undertake_work", "text_zh": "要件一：在马来西亚境内实质性组织施工人员与设备实施工程建造活动", "status": "condition_precedent"},
            {"eid": "e_my25_lack_cidb_reg", "text_zh": "要件二：未持有 CIDB 依 Act 520 核发且处于有效期内的 G1~G7 注册许可", "status": "mandatory"},
            {"eid": "e_my25_criminal_penalty", "text_zh": "法律后果：构成刑事违法并被责令停工，涉案合同面临因违法而不予强制执行抗辩", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "SG:SOPA_2004:Sec9",
        "law": "SG:SOPA_2004",
        "enbez": "Sec 9",
        "title": "新加坡建筑业付款保障法第9条：背靠背付款条款绝对无效",
        "heading_path": "新加坡建筑与施工行业付款保障法 (SOPA Cap 30B) > 第II部 付款权利",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "A pay when paid provision of a construction contract is of no effect, in that any provision of the contract that makes the liability to pay money contingent on the payer receiving payment from a third party shall be unenforceable.",
        "text_en": "A pay when paid provision in a construction contract has no effect and is unenforceable under Singapore law.",
        "text_zh": "【新加坡 SOPA 背靠背条款绝对无效】：建筑工程合同或分包协议中约定任何以‘付款人从第三方收取款项为付款条件’的条款（Pay-when-paid），在法律上一律不发生任何效力且不可执行。【出海实务攻防】：在新加坡工程市场，总包商企图以业主未批复期中付款证书（IPC）或业主拖欠款项为由拒绝向分包商付款的抗辩，直接被第9条法律铁律彻底否定，裁决员在快速裁决程序中将直接剔除该条款并裁决总包按施工进度付款。",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory_override",
        "elements_json": json.dumps([
            {"eid": "e_sg9_sopa_covered", "text_zh": "要件一：属于在新加坡境内实施的工程建造、咨询或材料采购施工合同", "status": "condition_precedent"},
            {"eid": "e_sg9_pay_when_paid", "text_zh": "要件二：合同专用条款载有以第三方付款作为向当事人付款前提条件的约定", "status": "mandatory"},
            {"eid": "e_sg9_no_effect", "text_zh": "法律后果：该背靠背条款自始不发生任何法律效力，裁决员直接剔除该抗辩", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "SG:SOPA_2004:Sec15_3",
        "law": "SG:SOPA_2004",
        "enbez": "Sec 15(3)",
        "title": "新加坡建筑业付款保障法第15条第3款：未在答辩中列明之抗辩理由绝对失权",
        "heading_path": "新加坡建筑与施工行业付款保障法 (SOPA Cap 30B) > 第III部 快速裁决程序",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "The adjudicator shall not consider any reason for withholding payment, or any response to the adjudication application, unless that reason or response was included in the relevant payment response provided by the respondent to the claimant within the prescribed time.",
        "text_en": "The adjudicator SHALL NOT consider any reason for withholding payment unless that reason was included in the payment response within prescribed time.",
        "text_zh": "【付款答辩失权铁律（裁决员法定审查禁区）】：快速裁决员在审理案件时，绝对不得考虑任何未在规定期限内核发的‘付款答辩书（Payment Response）’中明文列明的扣款理由或反驳意见！【出海实务攻防】：新加坡工程法上最致命的程序陷阱！业主若在收到总包的付款索赔（Payment Claim）后，未在合同规定时限（或最长21天）内出具付款答辩，或者答辩中漏写了违约金扣款或瑕疵索赔理由，后续在 SMC 快速裁决程序中绝对被禁止补提该等理由，裁决员依法必须全额支持索赔款！",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory_override",
        "elements_json": json.dumps([
            {"eid": "e_sg15_payment_claim_served", "text_zh": "要件一：索赔方依法定时间窗口与形式向被申请人有效送达了付款索赔书", "status": "condition_precedent"},
            {"eid": "e_sg15_omitted_in_response", "text_zh": "要件二：被申请人在法定期限内提交的付款答辩中未具体阐明该扣款/抵销事由", "status": "mandatory"},
            {"eid": "e_sg15_absolute_time_bar", "text_zh": "法律后果：裁决员依法被强制剥夺审查该新理由的法定管辖权，抗辩绝对失权", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "TH:CCC:Sec600",
        "law": "TH:CCC",
        "enbez": "Sec 600",
        "title": "泰国民商法典第600条：建筑物瑕疵担保法定期限（大型工程5年）",
        "heading_path": "泰国民商法典 > 第三编 特种契约 > 第七章 承揽 > 承揽人责任",
        "language_mode": "trilingual",
        "lang_original": "th",
        "text_original": "ถ้าการที่จ้างทำนั้นเป็นสิ่งปลูกสร้างบนแผ่นดิน นอกจากเรือนไม้ ผู้รับจ้างย่อมต้องรับผิดเพื่อการชำรุดบกพร่องภายในเวลาห้าปี นับแต่วันส่งมอบงาน",
        "text_en": "If the work is a structure on land other than a wooden building, the contractor is liable for defects appearing within 5 years from delivery date.",
        "text_zh": "【土地上非木制永久建筑物五年法定瑕疵担保】：承揽工程标的物若属于建造在土地上的建筑物或构筑物（木屋除外），承揽人必须对自工程竣工交付之日起 5 年内出现的任何工程缺陷与瑕疵承担法定修理及赔偿责任。【出海实务攻防】：在泰国承建电厂、高架路、水厂等大型土木工程，即便合同专用条件约定缺陷通知期（DNP）为 1 年或 2 年，一旦在移交后 5 年内发生非木结构建筑沉降开裂等工程质量缺陷，发包人依据第600条强行法依然享有法定索赔权，合同短于5年的约定不能对抗法条强行追责！",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory",
        "elements_json": json.dumps([
            {"eid": "e_th600_structure_on_land", "text_zh": "要件一：承揽工程标的系附着于土地上的砖石、混凝土或钢结构永久工程", "status": "condition_precedent"},
            {"eid": "e_th600_five_year_window", "text_zh": "要件二：工程质量缺陷在移交之日起5年法定瑕疵责任期内发生并显现", "status": "mandatory"},
            {"eid": "e_th600_statutory_liability", "text_zh": "法律后果：总承包商负有法定返修及全额损害赔偿义务，短于5年的合同约定不免责", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "PH:Civil_Code:Art1723",
        "law": "PH:Civil_Code",
        "enbez": "Art 1723",
        "title": "菲律宾民法典第1723条：建筑物坍塌十五年法定连带终身追责",
        "heading_path": "菲律宾民法典 > 第四编 债权与合同 > 第九章 承揽与建筑工程专章",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "The engineer or architect who drew up the plans and specifications for a building is liable for damages if within 15 years from the completion of the structure, the same should collapse by reason of a defect in those plans and specifications, or due to the defects in the ground. The contractor is likewise responsible for damages if the edifice falls, within the same period, on account of defects in the construction or the violation of the terms of the contract. Any stipulation waiving this liability is VOID.",
        "text_en": "Engineer/architect and contractor are liable for damages if building collapses within 15 years from completion due to design, ground or construction defects. Waiver is void.",
        "text_zh": "【建筑物坍塌十五年终身追责重锤】：若建筑物在竣工后 15 年内因设计图纸缺陷、地基缺陷或施工违规而发生坍塌或毁损，负责设计的工程师/建筑师与施工总承包商承担法定连带损害赔偿责任；诉讼追赔期长达 10 年；合同中任何免除本条责任的约定自始绝对无效！【出海实务攻防】：菲律宾工程法上最严厉的法定强行法！总包商严禁以‘业主已签发最终验收证书（TOC）’或‘地质勘测数据由业主提供’为由免责，一旦在15年内发生坍塌，总承包商与设计院面临法定全额连带赔偿，且合同任何免责声明均被法院裁定无效！",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory_override",
        "elements_json": json.dumps([
            {"eid": "e_ph1723_collapse_within_15yr", "text_zh": "要件一：建筑物在竣工移交之日起15年内发生倒塌、严重倾斜或主体结构毁损", "status": "condition_precedent"},
            {"eid": "e_ph1723_defect_causation", "text_zh": "要件二：毁损原因系由于地基缺陷、设计图纸缺陷、施工质量问题或违反工程规范", "status": "mandatory"},
            {"eid": "e_ph1723_solidary_strict_liability", "text_zh": "法律后果：承包商与设计方依法承担不可约定豁免的连带终身赔偿责任", "status": "prohibition"}
        ], ensure_ascii=False)
    },
    {
        "table": "norms",
        "norm_id": "PH:Civil_Code:Art1724",
        "law": "PH:Civil_Code",
        "enbez": "Art 1724",
        "title": "菲律宾民法典第1724条：固定总价工程变更款法定双重书面要件",
        "heading_path": "菲律宾民法典 > 第四编 债权与合同 > 第九章 承揽与建筑工程专章",
        "language_mode": "bilingual",
        "lang_original": "en",
        "text_original": "The contractor who undertakes to build a larger work for a stipulated price, in accordance with plans agreed upon, cannot bear any increase in price unless there has been a change in the plans which has been AUTHORIZED IN WRITING by the proprietor, AND the additional price to be paid has been AGREED UPON IN WRITING by both parties.",
        "text_en": "Contractor under lump sum cannot claim price increase unless plan change was authorized in writing by owner AND additional price was agreed upon in writing by both parties.",
        "text_zh": "【固定总价变更索赔双重书面法定铁律】：凡按约定包干价格承建工程的承包商，无权就任何设计变更要求增加工程价款，除非同时满足两大硬性法定条件：① 业主已正式出具书面变更授权指令；且 ② 双方已就该项变更应增加支付的工程价款达成书面价格协议！缺一不可！【出海实务攻防】：菲律宾工程变更第一杀手条款！菲最高法院先例反复重申：即便业主现场口头指令要求干了变更，且业主已实际接收并投产该变更工程，只要总承包商拿不出双方签字盖章的‘书面变更价格协议’，一分钱追加款都不能赔，且严禁援引不当得利（Quantum Meruit）绕开本条！",
        "norm_category": "mandatory_statute",
        "mandatory_level": "mandatory_override",
        "elements_json": json.dumps([
            {"eid": "e_ph1724_written_authorization", "text_zh": "要件一：发包人（业主）已就设计图纸变更出具正式书面授权变更通知", "status": "condition_precedent"},
            {"eid": "e_ph1724_written_price_agreement", "text_zh": "要件二：双方已针对该项变更增加的工程价款正式签署了书面变更价格协议", "status": "mandatory"},
            {"eid": "e_ph1724_claim_barred", "text_zh": "法律后果：缺失任一书面要件，工程款索赔绝对不予支持，严禁援引不当得利突破", "status": "prohibition"}
        ], ensure_ascii=False)
    }
]
