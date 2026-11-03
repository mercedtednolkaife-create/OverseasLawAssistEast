/**
 * 东盟法域配置字典 (ASEAN Jurisdictions)
 */

export interface JurisdictionConfig {
  code: string;
  name_zh: string;
  short_name: string;
  flag: string;
  primary_language: 'id' | 'vi' | 'en' | 'th' | 'zh' | 'km' | 'lo' | 'my' | 'ms' | 'pt' | string;
  language_mode?: 'bilingual' | 'trilingual';
  is_active: boolean;
  citation_standard: string;
  default_laws: string[];
  description_zh: string;
  practice_focus: string;
  high_risk_alerts: string[];
}

export const ASEAN_JURISDICTIONS: JurisdictionConfig[] = [
  {
    code: 'asean_id',
    name_zh: '印度尼西亚共和国',
    short_name: '印尼法域',
    flag: '🇮🇩',
    primary_language: 'id',
    is_active: true,
    citation_standard: 'indonesia_statute',
    default_laws: ['UU_2_2017', 'UU_6_2023', 'SEMA_3_2023', 'KUHPerdata', 'MEMR_11_2024'],
    description_zh: '建筑服务法、新能源本地化率(TKDN)与涉外合同印尼语双语令',
    practice_focus: '习惯法土地征拆延误、电力TKDN配额处罚、强制KSO非法人联营体与合同双语有效性',
    high_risk_alerts: [
      '《语言法》与 SEMA 3/2023：纯英文涉外合同易遭无效抗辩，须严格签署印尼语对照本',
      '能矿部 MEMR 11/2024：电力EPC须取得第三方机构法定TKDN认证证书',
      '习惯法土地征拆周期不可控，专用条件(PC)必须明确将征地受阻约定为业主风险与顺延事由',
    ],
  },
  {
    code: 'asean_vn',
    name_zh: '越南社会主义共和国',
    short_name: '越南法域',
    flag: '🇻🇳',
    primary_language: 'vi',
    is_active: true,
    citation_standard: 'vietnam_statute',
    default_laws: ['Law_135_2025', 'Decree_210_2026', 'Civil_Code_2015', 'Commercial_Law_2005'],
    description_zh: '《2025年新建设法》第86.2条工期预定损害赔偿(LD)与违约金封顶',
    practice_focus: '2025新法预定损害赔偿(LD)约定及核减抗辩、工程违约金法定比例封顶、政府投资资金拨付门禁',
    high_risk_alerts: [
      '新旧法衔接：2025建设法正式承认工期延误预定损害赔偿(LD)，但过高时法院享有自由核减权',
      '商法第301条违约金8%硬性封顶与新法LD的竞合适用边界',
      '涉及越方国企/公权力投资项目，工程结算审计常出现强制调减合同价风险',
    ],
  },
  {
    code: 'asean_my',
    name_zh: '马来西亚',
    short_name: '马来西亚法域',
    flag: '🇲🇾',
    primary_language: 'en',
    is_active: true,
    citation_standard: 'malaysia_statute',
    default_laws: ['CIPAA_2012', 'Act_520_CIDB', 'Contracts_Act_1950', 'Arbitration_Act_2005'],
    description_zh: 'CIPAA 2012工程款极速法定裁决、第35条背靠背绝对无效与CIDB资质管辖',
    practice_focus: 'CIPAA 2012 临时快速裁决追索进度款、分包背靠背支付条款无效抗辩、保函无条件见索即付反制',
    high_risk_alerts: [
      'CIPAA 第35条：有条件付款(背靠背 Pay-when-paid)条款法律明文绝对无效',
      'CIPAA裁决虽为暂定效力(Provisional)，但在仲裁前具有可直接向高等法院申请强制执行效力',
      'Act 520：未持有效CIDB执照从事建筑施工作业属刑事违法且合同价款主张可能受阻',
    ],
  },
  {
    code: 'asean_sg',
    name_zh: '新加坡共和国',
    short_name: '新加坡法域',
    flag: '🇸🇬',
    primary_language: 'en',
    is_active: true,
    citation_standard: 'singapore_statute',
    default_laws: ['SOPA_2004', 'Building_Control_Act', 'Civil_Law_Act', 'SIAC_Rules_2024'],
    description_zh: 'SOPA 2004付款保障法、BS Mount Sophia保函显失公平(Unconscionability)止付标准',
    practice_focus: '国际仲裁中心选法与管辖、履约保函显失公平止付禁令、普通法惩罚性违约金与真实损失预估',
    high_risk_alerts: [
      '保函止付普通法双支柱：欺诈(Fraud)与显失公平(Unconscionability)，后者举证门槛极高',
      'SOPA 第9条：反背靠背支付保护，支付通知书(Payment Response)必须在规定期限内核实答复',
      'SIAC 仲裁地监督法院对仲裁协议独立性与紧急仲裁员(Emergency Arbitrator)救济的高效执行',
    ],
  },
  {
    code: 'asean_th',
    name_zh: '泰王国',
    short_name: '泰国法域',
    flag: '🇹🇭',
    primary_language: 'th',
    is_active: true,
    citation_standard: 'thailand_statute',
    default_laws: ['CCC_Contract', 'FBA_1999', 'Public_Procurement_Act_2017', 'TAI_Rules'],
    description_zh: '《外商经营法》(FBA 1999)建设特许准入、民商法典承揽工程风险分担',
    practice_focus: '外资建筑承包持股比例红线、隐名代持(Nominee)合规排雷、政府特许经营协议纠纷行政法院管辖',
    high_risk_alerts: [
      'FBA List 3：工程建设通常禁止外资控股(外资股权上限49%)，除非取得外商经营许可证(FBL)或BOI投资委特批',
      '严禁通过泰国籍人头(Nominee)代持规避外资审查，面临没收股权与刑事合规重罚',
      '涉政府项目(Hopewell案先例)受行政法院管辖，仲裁裁决在泰国承认执行面临公共利益强行审查',
    ],
  },
  {
    code: 'asean_ph',
    name_zh: '菲律宾共和国',
    short_name: '菲律宾法域',
    flag: '🇵🇭',
    primary_language: 'en',
    is_active: true,
    citation_standard: 'philippines_statute',
    default_laws: ['RA_11966_PPP', 'CIAC_Rules', 'Civil_Code_PH', 'RA_9184_Procurement'],
    description_zh: '《2023年新公私合营法典》(RA 11966 PPP Code)、CIAC 建设仲裁委专属管辖',
    practice_focus: 'PPP项目特许经营协议公允终止补偿清算、PCAB特殊外资施工执照审查、CIAC法定专属管辖权',
    high_risk_alerts: [
      'RA 11966：全面废止实施三十年的旧BOT法(RA 7718)，设立全新公私合营法治体系与换届终止补偿机制',
      'CIAC 专属管辖权：合同只要约定仲裁且涉及菲律宾建筑争议，CIAC通常主张法定先决仲裁管辖',
      'PCAB执照：外资承包商必须依法取得专案特殊许可(Special License)，否则面临工程款追索受阻',
    ],
  },
  {
    code: 'asean_kh',
    name_zh: '柬埔寨王国',
    short_name: '柬埔寨法域',
    flag: '🇰🇭',
    primary_language: 'km',
    language_mode: 'trilingual',
    is_active: true,
    citation_standard: 'cambodia_law',
    default_laws: ['Law_on_Investment_2021', 'Civil_Code_2007', 'Law_on_Construction_2019', 'Commercial_Arbitration_2006'],
    description_zh: '《2021新投资法》QIP激励、《2007民法典》违约金不可调减原则及建筑法许可制度',
    practice_focus: '民法典第403条预定赔偿金排除法官衡平酌减、合格投资项目(QIP)税务优惠与外资施工资质',
    high_risk_alerts: [
      '民法典第403条：违约金属于约定清算赔偿金，法官无权依据公平原则进行调减，严禁以违约金过高为抗辩',
      '2019建筑法：未取得施工许可证擅自开工属严重违法，面临工程强制停工拆除及刑事责任',
      '土地所有权宪法限制：外国企业与个人不得拥有土地所有权，仅可设立长期租赁(Perpetual Lease)',
    ],
  },
  {
    code: 'asean_la',
    name_zh: '老挝人民民主共和国',
    short_name: '老挝法域',
    flag: '🇱🇦',
    primary_language: 'lo',
    language_mode: 'trilingual',
    is_active: true,
    citation_standard: 'laos_law',
    default_laws: ['Investment_Promotion_2016', 'Civil_Code_2020', 'Amended_Land_Law_2019', 'Foreign_Currency_2022'],
    description_zh: '水电与矿业特许经营(CA)、民法典承揽编、2022外汇法强制结汇与离岸外债审批红线',
    practice_focus: '特许经营协议(CA)与购电协议(PPA)背靠背责任、央行离岸借款事前审批、跨境资金汇出清税证明',
    high_risk_alerts: [
      '2022外汇法第15条：离岸外债须经老挝央行(BOL)事前审核登记，未登记者利息与本金汇出严重受阻',
      '强制结汇令：出口与工程收汇必须通过老挝商业银行系统结汇，离岸收汇面临外汇违规重罚',
      '土地特许使用权抵押：特许权土地向境外银团抵押必须取得老挝自然资源与环境部(MONRE)前置批文',
    ],
  },
  {
    code: 'asean_mm',
    name_zh: '缅甸联邦共和国',
    short_name: '缅甸法域',
    flag: '🇲🇲',
    primary_language: 'my',
    language_mode: 'bilingual',
    is_active: true,
    citation_standard: 'myanmar_act',
    default_laws: ['Myanmar_Investment_Law_2016', 'Contract_Act_1872', 'Arbitration_Law_2016', 'FEML_2012'],
    description_zh: '《2016缅甸投资法》(MIL)、1872合同法落空原则(Frustration)及央行外汇管制红线',
    practice_focus: '投资委员会(MIC)土地租赁许可上限、合同受阻落空免责抗辩、央行强制结汇与离岸仲裁执行',
    high_risk_alerts: [
      '外汇管理局(CBM)1日强制结汇与离岸支付严格配额审批，外汇进出必须保留全套进出口与履约凭证',
      '合同法第56条落空原则：情势变迁与政治动荡免责门槛极高，非不可抗力不可轻易主张免除履约',
      '不动产转移限制法(TRIPA 1987)：外国实体租期超过1年必须取得MIC特别批文',
    ],
  },
  {
    code: 'asean_bn',
    name_zh: '文莱达鲁萨兰国',
    short_name: '文莱法域',
    flag: '🇧🇳',
    primary_language: 'en',
    language_mode: 'bilingual',
    is_active: true,
    citation_standard: 'brunei_act',
    default_laws: ['Contracts_Act_Cap106', 'Brunei_Constitution_Art84C', 'International_Arbitration_2009', 'Building_Control_2014'],
    description_zh: '宪法第84C条政府绝对主权豁免红线、普通法合同制度与国际仲裁令',
    practice_focus: '政府工程绝对主权豁免与排他管辖、本地马来化就业配额、离岸商事仲裁地选择',
    high_risk_alerts: [
      '宪法第84C条：苏丹陛下及文莱政府享有绝对主权豁免，国内法院不得对政府签发强制令，必须在合同中明确放弃豁免',
      '建筑业从业人员注册令(BOEPDRA)：工程设计与技术负责人必须在文莱工务局(PWD)在册注册',
      '司法救济终审通道：文莱民商事上诉终审保留向英国枢密院司法委员会(JCPC)上诉机制',
    ],
  },
  {
    code: 'asean_tl',
    name_zh: '东帝汶民主共和国',
    short_name: '东帝汶法域',
    flag: '🇹🇱',
    primary_language: 'pt',
    language_mode: 'trilingual',
    is_active: true,
    citation_standard: 'timor_leste_law',
    default_laws: ['Law_9_2011_Budget', 'Civil_Code_2011', 'Private_Investment_2023', 'Decree_Law_22_2022_Procurement'],
    description_zh: '国家审计院事前合法性签证(Visto)生死线、2011民法典承揽工程及私人投资保护法',
    practice_focus: '审计院事前合法性核准(Visto)生效要件、公共采购法典合规、葡萄牙语官方签署要求',
    high_risk_alerts: [
      '第9/2011号预算框架法第40条：超过50万美元公共工程合同必须经最高上诉法院审计庭事前取得Visto签证，否则自始无效且不得付款',
      '公共采购法典(Decree-Law 10/2005)：严格限制分包比例，重大变更有赖国库事前资金匹配证明',
      '语言强制令：政府招投标及合同正式正本强制使用葡萄牙语，英文仅具辅助参考效力',
    ],
  },
];

export function getJurisdictionConfig(code?: string): JurisdictionConfig {
  const found = ASEAN_JURISDICTIONS.find((j) => j.code === code);
  return found || ASEAN_JURISDICTIONS[0];
}
