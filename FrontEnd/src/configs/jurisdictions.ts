/**
 * 东盟法域配置字典 (ASEAN Jurisdictions)
 */

export interface JurisdictionConfig {
  code: string;
  name_zh: string;
  short_name: string;
  flag: string;
  primary_language: 'id' | 'vi' | 'en' | 'th' | 'zh';
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
];

export function getJurisdictionConfig(code?: string): JurisdictionConfig {
  const found = ASEAN_JURISDICTIONS.find((j) => j.code === code);
  return found || ASEAN_JURISDICTIONS[0];
}
