/**
 * 东盟属地法律顾问与专家咨询库 - 高保真实务数据
 * 严格覆盖印度尼西亚、新加坡、马来西亚、越南、泰国、菲律宾六国工程法执业律师与权威裁决专家
 */

import { Expert, ConsultRecord } from '../../types/lawAgent';

export interface ExtendedExpert extends Expert {
  country_code: string;
  country_name: string;
  country_flag: string;
  city: string;
  experience_years: number;
  contact_channel: string;
  featured_cases: string[];
}

export interface ExtendedConsultRecord extends ConsultRecord {
  country_code?: string;
  country_flag?: string;
  topic?: string;
  legal_references?: string[];
  key_findings?: string[];
}

export const ASEAN_JURISDICTIONS = [
  { code: 'all', name: '全部法域', flag: '🌏' },
  { code: 'asean_id', name: '印度尼西亚', flag: '🇮🇩' },
  { code: 'asean_sg', name: '新加坡', flag: '🇸🇬' },
  { code: 'asean_my', name: '马来西亚', flag: '🇲🇾' },
  { code: 'asean_vn', name: '越南', flag: '🇻🇳' },
  { code: 'asean_th', name: '泰国', flag: '🇹🇭' },
  { code: 'asean_ph', name: '菲律宾', flag: '🇵🇭' },
];

export const INQUIRY_TEMPLATES = [
  {
    id: 'id_lang',
    country_code: 'asean_id',
    title: '印尼双语合同效力与 SEMA 3/2023 审查',
    text: '针对印尼中资 EPC 总承包项目，依据印尼 2017 年第 2 号《建筑法》第 30 条及最高法院 SEMA 3/2023 号通告，咨询双语合同签署中印尼语版本主导效力约定、未附印尼文签署之法律撤销风险与最新司法裁判尺度。',
  },
  {
    id: 'sg_sopa',
    country_code: 'asean_sg',
    title: '新加坡 SOPA 付款响应与保函止付',
    text: '针对新加坡工程项目，依据新加坡《建筑与施工行业付款保障法》(SOPA) 第 15 条，咨询业主对付款申请未在法定 7 日内书面响应的失权后果，以及依据 BS Mount Sophia 案先例申请见索即付保函止付的显失公平（Unconscionability）抗辩要件。',
  },
  {
    id: 'my_cipaa',
    country_code: 'asean_my',
    title: '马来西亚 CIPAA 35 条背靠背支付无效',
    text: '针对马来西亚工程分包与采购合同，依据 2012 年《施工行业付款及裁决法》(CIPAA) 第 35 条，咨询分包合同中“业主付款后方支付分包商（Pay-when-paid）”条款的法定无效效力及向 AIAC 提起法定快速裁决的管辖抗辩。',
  },
  {
    id: 'vn_eot',
    country_code: 'asean_vn',
    title: '越南新建设法工期顺延与违约金上限',
    text: '针对越南基础设施 EPC 项目，依据 2025 年新《建设法》及第 37/2015/ND-CP 号法令，咨询承包商因业主原因申请工期顺延（EOT）逾期未批复的视为认可效力，以及主合同违约金条款能否突破合同总额 12% 法定上限的实务裁判标准。',
  },
  {
    id: 'th_fba',
    country_code: 'asean_th',
    title: '泰国外资准入限制与联合体股权合规',
    text: '针对泰国工程投资与施工联合体，依据《外商经营法》(FBA 1999) 附表三第 10 项，咨询外资持股突破 49% 的合规限制、BOI 投资委员会工程类投资优惠资格，以及中泰联合体（Joint Venture）内部控制权与利润分配机制合规性。',
  },
  {
    id: 'ph_pcab',
    country_code: 'asean_ph',
    title: '菲律宾 PCAB 外资资质与 CIAC 专属仲裁',
    text: '针对菲律宾基建特许经营项目，依据菲律宾共和国法典 RA 4566 及菲律宾最高法院最新 PCAB 违宪判决，咨询外国总承包商申请特别施工许可的准入条件，以及合同争议依据 EO 1008 条直通建筑行业仲裁委员会 (CIAC) 的管辖排他性效力。',
  },
];

export const DEFAULT_EXPERTS: ExtendedExpert[] = [
  {
    expert_id: 'EXP-001',
    name: 'Dr. Arief Wijaya, S.H., LL.M.',
    title: '资深东盟工程法律顾问 / 印度尼西亚最高法院出庭律师',
    affiliation: '雅加达工程仲裁委员会 (BANI) / 印尼大学法学院',
    languages: ['印尼语', '英语', '中文'],
    fields: ['印尼第2号建筑法', 'TKDN 本土化审查', 'SEMA 3/2023 语言合规', 'BANI 国际工程仲裁'],
    qualification: '印尼最高法院出庭资格、BANI 注册资深仲裁员 (执业注册号: PERADI-08421)',
    conflict_declared: true,
    country_code: 'asean_id',
    country_name: '印度尼西亚',
    country_flag: '🇮🇩',
    city: '雅加达 (Jakarta)',
    experience_years: 22,
    contact_channel: '雅加达涉外律师公会独立会商加密专线',
    featured_cases: ['雅万高铁附属标段合同争议', '西爪哇电站 EPC 双语合同效力抗辩'],
  },
  {
    expert_id: 'EXP-002',
    name: 'Prof. Kevin Tan, FCIArb',
    title: '新加坡国际仲裁中心 (SIAC) 资深仲裁员 / 法学教授',
    affiliation: '新加坡国立大学法学院 / 新加坡建设工程学会 (SCL)',
    languages: ['英语', '中文', '马来语'],
    fields: ['FIDIC 标准合同条件', '新加坡 SOPA 付款保障', '见索即付保函止付', 'SIAC 国际仲裁'],
    qualification: '英国特许仲裁员协会院士 (FCIArb)、SIAC 专家组仲裁员 (注册号: SIAC-ARB-2012)',
    conflict_declared: true,
    country_code: 'asean_sg',
    country_name: '新加坡',
    country_flag: '🇸🇬',
    city: '新加坡城 (Singapore)',
    experience_years: 26,
    contact_channel: '新加坡麦士威国际仲裁大厦 (Maxwell Chambers) 会商席位',
    featured_cases: ['滨海湾金沙扩建工程索赔', '某大型港口保函止付 (BS Mount Sophia 先例)'],
  },
  {
    expert_id: 'EXP-003',
    name: 'Dato\' Lim Chong Beng, KMN',
    title: '马来西亚资深大律师 / CIPAA 裁决人',
    affiliation: '吉隆坡亚洲国际仲裁中心 (AIAC) / 马来西亚律师公会',
    languages: ['英语', '马来语', '粤语', '中文'],
    fields: ['马来西亚 CIPAA 快速裁决', '背靠背支付无效 (Sec 35)', '吉隆坡轻轨与港口争议'],
    qualification: '马来西亚联邦法院出庭大律师、AIAC 主任认证高级裁决员 (注册号: AIAC-ADJ-0441)',
    conflict_declared: true,
    country_code: 'asean_my',
    country_name: '马来西亚',
    country_flag: '🇲🇾',
    city: '吉隆坡 (Kuala Lumpur)',
    experience_years: 24,
    contact_channel: 'AIAC 苏莱曼大厦专业意见流转平台',
    featured_cases: ['东海岸铁路工程分包支付纠纷', '槟城填海工程工期索赔快速裁决'],
  },
  {
    expert_id: 'EXP-004',
    name: 'Nguyen Van Minh, Senior Counsel',
    title: '越南资深建设工程法务专家 / VIAC 仲裁员',
    affiliation: '越南国际仲裁中心 (VIAC) / 河内律师协会',
    languages: ['越南语', '英语', '中文'],
    fields: ['越南2025新建设法', '工期顺延 (EOT) 索赔', '违约赔偿 12% 上限', 'VIAC 仲裁裁决执行'],
    qualification: '越南司法部注册出庭律师、VIAC 建设工程专属调解仲裁员 (注册号: VIAC-ARB-309)',
    conflict_declared: true,
    country_code: 'asean_vn',
    country_name: '越南',
    country_flag: '🇻🇳',
    city: '河内 / 胡志明市 (Hanoi/HCMC)',
    experience_years: 19,
    contact_channel: '河内市国际法务协作中心会商通道',
    featured_cases: ['河内轻轨二号线总承包工程索赔', '平顺省光伏电站 EPC 履约抗辩'],
  },
  {
    expert_id: 'EXP-005',
    name: 'Somchai Prasert, FCIArb',
    title: '泰国皇家执业大律师 / TAI 注册仲裁员',
    affiliation: '泰国仲裁学会 (TAI) / 朱拉隆功大学法学院',
    languages: ['泰语', '英语', '中文'],
    fields: ['泰国外资商业法 (FBA 1999)', 'BOI 投资优惠政策', '中泰 EPC 联合体架构', '曼谷中央法院出庭'],
    qualification: '泰国大律师公会资深会员、TAI 注册仲裁员 (注册号: TAI-ARB-115)',
    conflict_declared: true,
    country_code: 'asean_th',
    country_name: '泰国',
    country_flag: '🇹🇭',
    city: '曼谷 (Bangkok)',
    experience_years: 23,
    contact_channel: '曼谷拉差达披色路司法法务中心专家会商通道',
    featured_cases: ['中泰铁路合作项目一期联合体合同核查', '罗勇工业园外资股权代持穿透审查'],
  },
  {
    expert_id: 'EXP-006',
    name: 'Atty. Maria Santos, LL.M.',
    title: '菲律宾基建公私合营 (PPP) 资深法律顾问',
    affiliation: '菲律宾建筑行业仲裁委员会 (CIAC) / 雅典耀大学法学院',
    languages: ['英语', '他加禄语', '中文'],
    fields: ['菲律宾 PCAB 资质准入 (RA 4566)', 'CIAC 建设工程专属仲裁', 'RA 11966 PPP 特许经营'],
    qualification: '菲律宾最高法院出庭资格、CIAC 资深工程仲裁员 (注册号: CIAC-ARB-088)',
    conflict_declared: true,
    country_code: 'asean_ph',
    country_name: '菲律宾',
    country_flag: '🇵🇭',
    city: '马尼拉 (Manila)',
    experience_years: 21,
    contact_channel: '马尼拉博尼法乔高街 (BGC) 涉外争端调解处',
    featured_cases: ['马尼拉地铁项目外资特别许可准入', '苏比克湾港口 BOT 特许经营合同争议'],
  },
];

export const DEFAULT_CONSULTS: ExtendedConsultRecord[] = [
  {
    consult_id: 'CON-ID-2026-001',
    case_id: 'CASE-ASEAN-01',
    expert_id: 'EXP-001',
    expert_name: 'Dr. Arief Wijaya, S.H., LL.M.',
    status: 'replied',
    country_code: 'asean_id',
    country_flag: '🇮🇩',
    topic: '印尼双语合同效力与最高法院 SEMA 3/2023 裁判对策',
    question_snapshot:
      '请就印尼 2017 年第 2 号建筑法第 30 条及最高法院通告 SEMA 3/2023，针对中资总包与印尼业主签署的 FIDIC 银皮书双语合同，明确文本效力冲突时印尼法院与 BANI 仲裁庭的实体裁判倾向，以及如何有效防范合同被判定无效或被撤销。',
    evidence_summary:
      '涉案依据：印尼《国语、国旗与国徽法》(Law No. 24/2009) 第 31 条；2017 年第 2 号《建筑法》第 30 条；最高法院第 3/2023 号通告 (SEMA 3/2023)；印尼最高法院 PT Bangun Karya Pratama Lestari 案 (No. 1572 K/Pdt/2015)。',
    reply: `【印度尼西亚属地出海法律顾问意见书】
致：涉外工程项目管理团队与涉外法务组
就贵司委托关于印尼双语建设工程合同效力及 SEMA 3/2023 通告实务适用，经全面检索印尼最高法院最新判例与印尼民法典，出具如下专项法律意见：

一、法定强制要件与核心法律风险
1. 印尼 2009 年第 24 号法律第 31 条与 2017 年第 2 号《建筑法》第 30 条明确规定：凡在印尼境内订立、且包含印尼主体或在印尼实施的工程承包合同，必须以印尼文（Bahasa Indonesia）订立。若涉及外国当事人，允许同时使用外语订立双语版本。
2. 历史司法风险：在印尼最高法院第 1572 K/Pdt/2015 号判例中，法院曾认定一份未附印尼语译本的跨境贷款协议违反法律强行法（UU 24/2009），判决协议自始无效（Batal demi hukum）。印尼本土业主在工程款索赔争议中常借此恶意主张主合同无效。

二、最高法院 SEMA 3/2023 最新司法转向与防范对策
1. 2023 年底，印尼最高法院颁布第 3/2023 号司法通告（SEMA 3/2023），民事庭就该问题明确确立裁判标准：如果当事人已经订立双语版本并约定以外文（如英文）为主导语言，印尼法院不得仅因文本解释分歧而认定合同无效。
2. 关键合规红线：必须确保“印尼语与英语版本在签字时同步形成并由双方同时签署盖章”。若仅签署英文版，事后单方补充公证翻译件，仍面临极高被印尼法院推翻的诉讼风险。

三、建议合同修改与实务操作要领
1. 补充订立《双语合同一致性确认备忘录》，由双方授权代表签署并经印尼当地公证人（Notaris）公证。
2. 条款示范推荐：“This Agreement is executed in both the English and Indonesian languages. Both texts are equally authentic; provided that in the event of any divergence, ambiguity, or conflict in interpretation, the English version shall govern and prevail to the fullest extent permitted under Indonesian Supreme Court Circular SEMA No. 3 of 2023.”
3. 争议解决条款建议明确排除印尼各地区初级法院（Pengadilan Negeri）管辖，约定提交至新加坡国际仲裁中心 (SIAC) 或雅加达仲裁院 (BANI)，仲裁语言明确指定为英语。`,
    legal_references: [
      '印尼 2017 年第 2 号建筑工程法第 30 条',
      '印尼最高法院司法通告 SEMA No. 3/2023',
      '印尼 2019 年第 63 号总统令关于印尼语强制使用的规定',
    ],
    key_findings: [
      '双语合同必须同步签署，不得事后单方补充印尼语译本',
      'SEMA 3/2023 支持在双语齐备前提下约定英文为最终解释主导语',
      '建议经印尼公证人 (Notaris) 公证并约定 SIAC 或 BANI 仲裁',
    ],
    conflict_affirmed: true,
    updated_at: '2026-03-28 14:30',
  },
  {
    consult_id: 'CON-SG-2026-002',
    case_id: 'CASE-ASEAN-02',
    expert_id: 'EXP-002',
    expert_name: 'Prof. Kevin Tan, FCIArb',
    status: 'replied',
    country_code: 'asean_sg',
    country_flag: '🇸🇬',
    topic: '新加坡 SOPA 付款保障失权与保函止付抗辩',
    question_snapshot:
      '请就新加坡《建筑与施工行业付款保障法》(SOPA) 项下进度款支付响应（Payment Response）法定 7 天失权规则，以及承包商面临业主不当索兑独立保函时，依据 BS Mount Sophia 先例申请法院禁令止付的举证要件出具权威法律意见。',
    evidence_summary:
      '涉案依据：新加坡《建筑与施工行业付款保障法》(Cap 30B, SOPA) 第 12、15 条；新加坡上诉法院里程碑先例 BS Mount Sophia Pte Ltd v Joint Venture (2012 SGCA 57)；新加坡高等法院 JBE Holdings Ltd v Premas Construction Pte Ltd (2012 SGHC 139)。',
    reply: `【新加坡国际仲裁与建设工程法专项法律意见书】
致：新加坡项目工程管理部与涉外法务团队
本席审阅案卷涉及的付款申请及保函争议材料，依据新加坡现行立法及最高法院上诉庭（SGCA）既有判例规则，出具本法律意见：

一、新加坡 SOPA 法定付款响应失权规则 (Section 15 SOPA)
1. 依据 SOPA 第 15 条第 (3) 款之强制性规定，业主在收到总承包商递交的付款申请（Payment Claim）后，如未在合同约定或法定期限（最长不超过 7 天或 21 天，视合同约定）内出具付款响应（Payment Response），则丧失在后续法定裁决程序（Adjudication）中提出抵销、扣款或违约赔偿抗辩的实体权利。
2. 司法后果：新加坡最高法院在上诉案件中严格坚持“先付款后争议（Pay now, argue later）”立法原则。若业主逾期出具付款响应，裁决员（Adjudicator）依法必须全额支持承包商申请款额，业主不得补提逾期索赔抗辩。

二、见索即付保函止付与 BS Mount Sophia 裁判规则
1. 新加坡法律在传统普通法“欺诈（Fraud）”例外之外，确立了独特的第二项止付事由——“显失公平（Unconscionability）”（BS Mount Sophia 先例）。
2. 举证门槛与裁判心证标准：
   - 证明标准高于“表面证据（Prima Facie）”，需达到“极高盖然性（High Degree of Probability）”或“强烈真实案件（Strong Prima Facie Case）”。
   - 仅存在工程合同违约或工期争议不足以认定显失公平；承包商必须证明：业主索兑保函缺乏实质善意、存在滥用强势地位恶意挤压承包商资金链、或索兑款额与实际受损之间存在极端不成比例的悬殊。
3. 紧急救济程序：若业主拟恶意索兑，承包商应在 24-48 小时内向新加坡高院主审法官申请单方面临时禁令（Ex-parte Injunction），并准备足额反担保保函。`,
    legal_references: [
      'Singapore Building and Construction Industry Security of Payment Act (Cap 30B)',
      'BS Mount Sophia Pte Ltd v Joint Venture [2012] SGCA 57',
      'JBE Holdings Ltd v Premas Construction Pte Ltd [2012] SGHC 139',
    ],
    key_findings: [
      'SOPA 法定响应逾期将导致实体抗辩权绝对丧失',
      '新加坡允许以“显失公平 (Unconscionability)”为由申请保函止付',
      '需证明业主索兑缺乏善意或属于恶意施压，门槛高但救济迅速',
    ],
    conflict_affirmed: true,
    updated_at: '2026-03-25 16:45',
  },
  {
    consult_id: 'CON-MY-2026-003',
    case_id: 'CASE-ASEAN-03',
    expert_id: 'EXP-003',
    expert_name: 'Dato\' Lim Chong Beng, KMN',
    status: 'replied',
    country_code: 'asean_my',
    country_flag: '🇲🇾',
    topic: '马来西亚 CIPAA 第 35 条背靠背支付无效与 AIAC 裁决实务',
    question_snapshot:
      '请就马来西亚 2012 年《施工行业付款及裁决法》(CIPAA) 第 35 条，分析总承包合同与专业分包合同中“若业主未付则总包无需支付（Pay when paid / Pay if paid）”条款的法律效力，以及分包商绕过诉讼直接向 AIAC 申请法定裁决的风险与抗辩策略。',
    evidence_summary:
      '涉案依据：马来西亚《施工行业付款及裁决法 2012》(CIPAA 2012) 第 35 条；马来西亚联邦法院里程碑判例 Jack-In Pile (M) Sdn Bhd v Bauer (M) Sdn Bhd (2020)；亚洲国际仲裁中心 (AIAC) CIPAA 裁决规程。',
    reply: `【马来西亚联邦出庭大律师法律意见书】
致：马来西亚涉外工程项目管理团队
就贵司关切的专业分包款项支付纠纷及 CIPAA 第 35 条强行法适用，出具如下书面意见：

一、CIPAA 第 35 条强制宣告背靠背条款无效
1. CIPAA 2012 第 35 条明文规定：施工合同中任何将“付款义务”与“第三方支付（如业主向上游支付）”相挂钩的有条件支付条款（Conditional Payment Provision）自始绝对无效，且该规定不可通过合同任何约定予以排除。
2. 即使分包合同在抬头明确标明“各方自愿放弃适用 CIPAA”，在马来西亚法院与 AIAC 裁决中均被认定为违反公共政策而归于无效。总承包商不得以“业主尚未计量支付”为由拒绝支付合格分包款项。

二、AIAC CIPAA 快速裁决程序特点与总包应对策略
1. 时间极其紧迫：裁决人从受指定起至出具具有法定执行力的裁决书仅需 45 个工作日；被申请人（总包商）在收到裁决申请（Adjudication Claim）后仅有 10 个工作日提交裁决答辩（Adjudication Response）。
2. 答辩核心防线：
   - 聚焦于“工程质量缺陷”、“现场未完工签证缺失”或“分包商自身延误导致的逾期违约赔偿金 (LAD) 抵销”，上述抗辩不受第 35 条背靠背限制；
   - 确保在答辩中同步递交工程检验报告与工程师不合格备忘录，形成严密的抵销数额计算。`,
    legal_references: [
      'Construction Industry Payment and Adjudication Act 2012 (CIPAA 2012) Section 35',
      'Jack-In Pile (M) Sdn Bhd v Bauer (M) Sdn Bhd [2020] 1 CLJ 562 FC',
      'AIAC Standard CIPAA Rules and Practice Directions',
    ],
    key_findings: [
      '背靠背条款在马来西亚属法定绝对无效，不可抗辩分包款项',
      '应对重点应转移至“工程质量缺陷”与“违约赔偿金 (LAD) 合法抵销”',
      'AIAC 裁决程序答辩期仅 10 个工作日，必须在立案阶段备齐证据',
    ],
    conflict_affirmed: true,
    updated_at: '2026-03-22 10:15',
  },
  {
    consult_id: 'CON-VN-2026-004',
    case_id: 'CASE-ASEAN-04',
    expert_id: 'EXP-004',
    expert_name: 'Nguyen Van Minh, Senior Counsel',
    status: 'replied',
    country_code: 'asean_vn',
    country_flag: '🇻🇳',
    topic: '越南新建设法工期顺延 (EOT) 默示认可与违约金 12% 限制',
    question_snapshot:
      '请就越南 2025 年新《建设法》及第 37/2015/ND-CP 号法令，针对中资 EPC 总包商在越南执行火电与基建项目，就业主逾期答复工期顺延（EOT）的视为认可效力、以及合同约定的超额延误赔偿金能否突破越南民法典与商法典法定违约金上限出具专业意见。',
    evidence_summary:
      '涉案依据：越南《建设法》(Law No. 50/2014/QH13 及 2025 年修正案)；越南政府第 37/2015/ND-CP 号法令关于建设工程合同第 16、23 条；越南 2005 年《商法典》第 301 条（违约金 8% 上限）与建设法专属 12% 上限。',
    reply: `【越南建设工程资深法律顾问专业意见书】
致：在越重大基建总承包项目组
结合越南建设部（BXD）最新监管通令及越南国际仲裁中心（VIAC）近三年裁决趋势，就涉案 EOT 及违约金争议出具意见如下：

一、工期顺延 (EOT) 申请之业主逾期“视为认可”规则
1. 依据越南政府第 37/2015/ND-CP 号法令第 16 条第 3 款：承包商因不可抗力、设计变更或业主交付场地延误提交工期顺延书面申请后，发包人（业主）必须在合同约定期限内或自收到申请之日起 14 个工作日内作出书面决定。
2. 若发包人逾期未提出书面反对意见，且承包商已按期提交进度影响关键路径（Critical Path）分析，在 VIAC 仲裁中仲裁庭倾向于裁定发包人默示认可（Deemed Approval）工期顺延，发包人事后主张工期延误违约金的诉求将被驳回。

二、法定违约赔偿金上限之强行法适用
1. 越南法律对违约赔偿金（Penalty）设有严格的法定上限：
   - 一般商事合同依据《商法典》第 301 条上限为违约义务部分金额的 8%；
   - 建设工程合同依据《建设法》专属法令，双方约定的违约赔偿金总额不得超过合同签约价值的 12%。
2. 若 EPC 合同约定每日 0.1% 且无封顶，超出合同总额 12% 的部分在越南法院及 VIAC 仲裁中将被依法强制削减至 12%。承包商可据此提出合法限额抗辩。`,
    legal_references: [
      '越南《建设法》2025 修订案第 141 条',
      '越南政府第 37/2015/ND-CP 号法令第 16、23 条',
      '越南 2005 年《商法典》第 301 条',
    ],
    key_findings: [
      '业主在 14 个工作日内未答复 EOT 申请构成默示认可',
      '建设工程违约赔偿金法定上限为合同签约价值的 12%',
      '合同中约定超出 12% 的部分依法属于绝对无效并被强制剔除',
    ],
    conflict_affirmed: true,
    updated_at: '2026-03-19 11:20',
  },
  {
    consult_id: 'CON-TH-2026-005',
    case_id: 'CASE-ASEAN-05',
    expert_id: 'EXP-005',
    expert_name: 'Somchai Prasert, FCIArb',
    status: 'replied',
    country_code: 'asean_th',
    country_flag: '🇹🇭',
    topic: '泰国外资商业法 FBA 准入限制与联合体 (JV) 控制权合规',
    question_snapshot:
      '请就泰国《外商经营法》(FBA 1999) 附表三第 10 项关于建筑工程的外资股比限制，分析中泰企业组建非法人联营体（Unincorporated Joint Venture）或法人型合资公司执行大型工业 EPC 项目的合规风险，重点针对名义代持（Nominee Shareholding）的刑民责任及 BOI 优惠政策出具意见。',
    evidence_summary:
      '涉案依据：泰国《外商经营法 B.E. 2542》(FBA 1999) 第 8 条、附表三第 10 项；泰国刑法典及商业部商业发展厅 (DBD) 第 205/2565 号稽查通令；泰国投资促进委员会 (BOI) 招商优惠目录。',
    reply: `【泰国皇家执业大律师法律意见书】
致：中泰出海工程联营体决策委员会
就贵司在泰开展 EPC 工业工程及联合体合规设计，结合商业部商业发展厅（DBD）严监管现状，出具如下专项意见：

一、外商经营法 (FBA) 准入红线与名义代持刑事风险
1. 依据 FBA 1999 附表三第 10 项：普通建筑工程属于限制外资经营业务，外资持股比例不得达到或超过 50%。
2. DBD 严打“名义代持（Nominee）”：泰国商业部自 2022 年起对中资背景合资公司实施严格银行流水穿透审查。若泰方股东的资金来自中方借款、垫资或无实际分红权，将被认定为非法代持。中泰双方高管均面临最高 3 年监禁及最高 100 万泰铢罚金，合资公司营业执照将被强制吊销。

二、合法破局路径：非法人联合体或申请 BOI / FBL 许可
1. 若为大型复杂基础设施，可向泰国商业部申请外商经营许可证（Foreign Business License, FBL），或通过 BOI 申请投资促进优惠（获批后允许外资 100% 控股）。
2. 在工程招投标中，推荐采用“非法人联合体（Unincorporated Joint Venture）”架构：中方总包企业与泰国本地持证承包商共同签署《联营体协议》，明确约定双方连带责任，同时由泰方负责属地施工许可，中方负责技术与海外采购，此模式在泰国现行税法及商业法下成熟合规。`,
    legal_references: [
      'Thailand Foreign Business Act B.E. 2542 (1999) List 3 (10)',
      'DBD Inspection Guideline on Nominee Shareholding No. 205/2565',
      'Board of Investment (BOI) Investment Promotion Act B.E. 2520',
    ],
    key_findings: [
      '严禁使用名义代持突破 49% 股比，面临商业部穿透与刑事责任',
      '推荐采用“非法人联合体 (Unincorporated JV)”合法联合竞标',
      '重大基建应优先申请 BOI 或商业部 FBL 许可证实现外资合规',
    ],
    conflict_affirmed: true,
    updated_at: '2026-03-15 09:40',
  },
  {
    consult_id: 'CON-PH-2026-006',
    case_id: 'CASE-ASEAN-06',
    expert_id: 'EXP-006',
    expert_name: 'Atty. Maria Santos, LL.M.',
    status: 'replied',
    country_code: 'asean_ph',
    country_flag: '🇵🇭',
    topic: '菲律宾外国承包商 PCAB 特别许可与 CIAC 专属仲裁',
    question_snapshot:
      '请就菲律宾承包商认可委员会（PCAB）针对外国总承包商的特别许可（Special License）制度、以及菲律宾第 1008 号总统令项下建筑行业仲裁委员会（CIAC）对建设工程合同争议的法定专属管辖权出具专家法律意见。',
    evidence_summary:
      '涉案依据：菲律宾共和国法典 RA 4566；菲律宾最高法院里程碑判决 Philippine Contractors Accreditation Board v. Manila Water Company (G.R. No. 175622)；第 1008 号行政令 (Executive Order No. 1008, CIAC 组织法)。',
    reply: `【菲律宾资深基建工程法律顾问专业意见书】
致：菲律宾重大基建特许经营项目部
就外国承包商在菲资质准入与争议解决专属管辖权问题，依据菲律宾最高法院最新判例，出具意见如下：

一、PCAB 资质准入最新裁判转向与特别许可办理
1. 历史背景：菲律宾原规定外国承包商只能按单个项目申请特别许可（Special License），不得获得正规普通营业执照。
2. 最高法院里程碑突破：在 PCAB v. Manila Water 案中，菲律宾最高法院大法官全体席位判决 PCAB 规则第 3 条第 3.1 款违宪，认定其非法剥夺外国承包商的平等竞争权。外国承包商现已具备平等待遇基础，但目前实务中办理大中型基建项目仍必须在开工前向 PCAB 申请取得 AAA 级特别承包资质，未获许可开工构成行政违法并导致合同执行受阻。

二、CIAC 仲裁专属管辖权之不可撤销性 (EO 1008)
1. 依据菲律宾 EO 1008 第 4 条：凡涉及菲律宾境内建设工程合同，只要合同中包含任何形式的仲裁条款，菲律宾建筑行业仲裁委员会（CIAC）即依法享有初审原创专属管辖权（Original and Exclusive Jurisdiction）。
2. 即使合同中约定由“新加坡 SIAC 或香港 HKIAC”仲裁，若任何一方先向菲律宾 CIAC 提起仲裁，菲律宾法院依法将强制支持 CIAC 的排他管辖权。因此，在合同争议解决条款设计中，必须周密统筹 CIAC 与境外国际仲裁的管辖权协调。`,
    legal_references: [
      'Philippine Republic Act No. 4566 (Contractors License Law)',
      'Supreme Court Ruling: PCAB v. Manila Water Co. [G.R. No. 175622]',
      'Executive Order No. 1008 Creating the Construction Industry Arbitration Commission',
    ],
    key_findings: [
      '外国承包商必须在开工前办理 PCAB 特别施工资质许可',
      '建设工程争议只要有仲裁约定，CIAC 即依法享有法定专属管辖',
      '涉菲工程合同需审慎设计国际仲裁与 CIAC 的管辖衔接条款',
    ],
    conflict_affirmed: true,
    updated_at: '2026-03-12 15:10',
  },
];
