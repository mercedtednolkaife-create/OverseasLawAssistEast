/**
 * 东盟六国与涉外法域全局配置中心
 * 严格对齐《东盟国家迁移方案.md》V4.0 终审定稿版
 * 德美法域已在此无损软屏蔽 (is_active: false)，仅供后台自动化回归测试与历史案件调用
 */

export interface JurisdictionConfig {
  code: string;
  name_zh: string;
  short_name: string;
  flag: string;
  region: 'asean' | 'europe' | 'north_america' | 'legacy';
  primary_language: 'id' | 'vi' | 'en' | 'th' | 'de' | 'zh';
  language_mode: 'bilingual' | 'trilingual';
  is_active: boolean;
  citation_standard: string;
  default_laws: string[];
  description_zh: string;
  practice_focus: string; // 实务焦点
  high_risk_alerts: string[]; // 常见高危合规风险点
}

export const ASEAN_JURISDICTIONS: JurisdictionConfig[] = [
  {
    code: 'asean_id',
    name_zh: '印度尼西亚共和国',
    short_name: '印尼法域',
    flag: '🇮🇩',
    region: 'asean',
    primary_language: 'id',
    language_mode: 'trilingual',
    is_active: true,
    citation_standard: 'indonesia_statute',
    default_laws: ['UU_2_2017', 'UU_6_2023', 'SEMA_3_2023', 'KUHPerdata', 'MEMR_11_2024'],
    description_zh: '涵盖印尼《建筑服务法》、电力与工业TKDN本地化率新规及SEMA 3/2023合同语言效力规则',
    practice_focus: '习惯法土地(Hak Ulayat)征拆延误、电力TKDN配额处罚、强制KSO非法人联营体与印尼语合同效力抗辩',
    high_risk_alerts: [
      '《语言法》(UU 24/2009)与SEMA 3/2023：纯英文涉外合同易遭恶意主张无效，须投前严格签署印尼语对照本',
      '能矿部 MEMR 11/2024：电力EPC须严格取得第三方机构(Sucofindo/Surveyor)法定TKDN认证证书',
      '习惯法土地征拆周期不可控，专用条件(PC)必须明确将征地受阻约定为业主风险与工期顺延事由'
    ],
  },
  {
    code: 'asean_vn',
    name_zh: '越南社会主义共和国',
    short_name: '越南法域',
    flag: '🇻🇳',
    region: 'asean',
    primary_language: 'vi',
    language_mode: 'trilingual',
    is_active: true,
    citation_standard: 'vietnam_law',
    default_laws: ['Law_135_2025_QH15', 'Decree_210_2026_ND_CP', 'Law_64_2020_PPP', 'Civil_Code_2015'],
    description_zh: '涵盖越南《2025新建设法》第86.2条违约金规则、第210/2026/ND-CP号建设合同法令及PPP法典',
    practice_focus: '海上风电/光伏M&A股权交割先决条件(CP)、见索即付保函恶意索兑反制与新建设法违约金封顶重构',
    high_risk_alerts: [
      '《2025新建设法》第86.2条正式承认预定损害赔偿(LD)，改变了原法定12%违约罚金上限，合同违约金条款须重构',
      '外国承包商许可证(Contractor Permit)为法定强制前置，且须与越企联营或指定分包',
      '工贸部(MOIT) FIT补贴电价过渡期下调风险，须在PPA特许协议与EPC合同中做好背靠背无缝传导'
    ],
  },
  {
    code: 'asean_my',
    name_zh: '马来西亚',
    short_name: '马来西亚法域',
    flag: '🇲🇾',
    region: 'asean',
    primary_language: 'en',
    language_mode: 'bilingual',
    is_active: true,
    citation_standard: 'malaysia_act',
    default_laws: ['CIPAA_2012', 'Act_520_CIDB', 'Contracts_Act_1950'],
    description_zh: '涵盖马来西亚CIPAA 2012法定快速裁决、第35条背靠背付款无效及CIDB执照要求',
    practice_focus: '轨道交通与市政基建CIPAA工程款快速追索、土著(Bumiputera)联营配额与保函止付',
    high_risk_alerts: [
      'CIPAA 2012 第35条明文规定“背靠背付款条款(Pay-when-paid)”一律无效，总包不可因业主拖欠而抗辩拒付分包',
      'CIDB G7牌照是外资承接无上限金额工程法定门槛，未取得牌照可能导致承揽合同自始无效',
      '保函止付严格适用普通法欺诈及显失公平先例(Sumatec)'
    ],
  },
  {
    code: 'asean_sg',
    name_zh: '新加坡共和国',
    short_name: '新加坡法域',
    flag: '🇸🇬',
    region: 'asean',
    primary_language: 'en',
    language_mode: 'bilingual',
    is_active: true,
    citation_standard: 'singapore_act',
    default_laws: ['SOPA_2004', 'Building_Control_Act', 'IAA_Cap_143A'],
    description_zh: '涵盖新加坡SOPA付款保障法、SIAC国际仲裁与BS Mount Sophia保函显失公平止付先例',
    practice_focus: '涉外工程争议国际仲裁管辖(SIAC)、紧急仲裁员(EA)保函止付令与SOPA快速裁决应对',
    high_risk_alerts: [
      '确立了独立的“显失公平(Unconscionability)”保函止付法定标准（BS Mount Sophia案），门槛低于传统欺诈',
      'SOPA第9条排斥背靠背条款，提供7~14天极速付款响应机制',
      '国际仲裁法(IAA)对仲裁协议严密保护，属地司法干预门槛极高'
    ],
  },
  {
    code: 'asean_th',
    name_zh: '泰王国',
    short_name: '泰国法域',
    flag: '🇹🇭',
    region: 'asean',
    primary_language: 'th',
    language_mode: 'trilingual',
    is_active: true,
    citation_standard: 'thailand_code',
    default_laws: ['CCC_Hire_of_Work', 'FBA_1999', 'PPP_Act_2019'],
    description_zh: '涵盖泰国民商法典(CCC)承揽编、外商经营法(FBA)限制与公共工程管辖规则',
    practice_focus: '东部经济走廊(EEC)基建特许经营、外商经营许可证(FBL)与公共行政诉讼',
    high_risk_alerts: [
      '外商经营法(FBA)限制外资持股超过49%，严禁使用本地代持人(Nominee)规避监管',
      '政府公共采购强制使用泰语文本，诉讼仲裁管辖高度受最高行政法院影响',
      '独立保函止付依循传统欺诈例外，需向法院交纳高额反担保'
    ],
  },
  {
    code: 'asean_ph',
    name_zh: '菲律宾共和国',
    short_name: '菲律宾法域',
    flag: '🇵🇭',
    region: 'asean',
    primary_language: 'en',
    language_mode: 'bilingual',
    is_active: true,
    citation_standard: 'philippines_ra',
    default_laws: ['RA_11966_PPP_Code', 'RA_12009_Procurement', 'RA_4566_Contractors', 'RA_11659_PSA'],
    description_zh: '涵盖菲律宾新《PPP法典》(RA 11966)、CIAC工程仲裁管辖及Manila Water外资牌照先例',
    practice_focus: '跨海大桥与交通PPP特许权中止补偿、中菲BIT投资协定第4条与中信保30日报损联动',
    high_risk_alerts: [
      '新《PPP法典》(RA 11966)已明文废止旧BOT法(RA 7718)，严禁继续援引失效旧法条款',
      '最高院Manila Water先例已废除普通工程60%菲籍股权限制，但公用事业与政府采购仍具排他性',
      'CIAC对工程争议具备排他性专属管辖权，即便约定其他仲裁机构仍可能被CIAC提级审理'
    ],
  },
];

export const LEGACY_JURISDICTIONS: JurisdictionConfig[] = [];

export const ALL_JURISDICTIONS = ASEAN_JURISDICTIONS;

export function getActiveJurisdictions(): JurisdictionConfig[] {
  return ASEAN_JURISDICTIONS.filter((j) => j.is_active);
}

export function getAllJurisdictions(): JurisdictionConfig[] {
  return ASEAN_JURISDICTIONS;
}

export function getJurisdictionConfig(code?: string): JurisdictionConfig {
  const found = ASEAN_JURISDICTIONS.find((j) => j.code === code);
  return found || ASEAN_JURISDICTIONS[0];
}

