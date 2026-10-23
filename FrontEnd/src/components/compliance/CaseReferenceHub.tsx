import React, { useState } from 'react';
import { useApp } from '../../context/AppContext';
import {
  Search,
  Filter,
  ArrowRight,
  ExternalLink,
  Copy,
  Check,
  Play,
  FileText,
  AlertTriangle,
  Shield,
  Layers,
  ChevronRight,
  Building2,
  Globe2,
} from 'lucide-react';

interface Case5DItem {
  id: string;
  code: string;
  title: string;
  jurisdiction: string;
  countryName: string;
  countryFlag: string;
  stage: string;
  archetypes: string[];
  summary: string;
  // 5D Review Card Data
  dimension1_structure: {
    parties: { role: string; name: string }[];
    dealSummary: string;
  };
  dimension2_rootCause: {
    coreDiagnosis: string;
    contractPitfall: string;
    triggerFactors: string[];
  };
  dimension3_legalAnchors: {
    normId: string;
    nameZh: string;
    statuteSnippet: string;
    keyRule: string;
  }[];
  dimension4_modelClauses: {
    title: string;
    enClause: string;
    zhExplanation: string;
  }[];
  dimension5_simulation: {
    initialFacts: string;
    initialClaims: string;
  };
}

const BENCHMARK_CASES_5D: Case5DItem[] = [
  {
    id: 'C101',
    code: 'C101',
    title: '爪哇 2×660MW 电站 EPC 习惯法土地征拆迟延、纯英文合同效力抗辩与 TKDN 处罚案',
    jurisdiction: 'asean_id',
    countryName: '印度尼西亚',
    countryFlag: '🇮🇩',
    stage: '履约索赔与争议解决',
    archetypes: ['EPC_CONTRACTING', 'JV_CONSORTIUM'],
    summary: '业主因原住民习惯法土地 (Hak Ulayat) 征拆阻碍迟延交地 180 天；承包商索赔工期与费用，业主以“28天逾期失权”、“补充协议未签印尼语故无效”及“逆变器未达 TKDN”拒付并威胁索兑保函。',
    dimension1_structure: {
      parties: [
        { role: '项目业主 (Employer)', name: '印尼国家电力公司 PLN 控股项目特许权公司 (PT Cons)' },
        { role: 'EPC总承包商 (Contractor)', name: '中资能源建设央企海外工程局' },
        { role: '属地联营伙伴 (KSO Partner)', name: '印尼本土一类施工企业 (PT Karya)' },
        { role: '保函开立行 (Guarantor Bank)', name: '中国银行雅加达分行' },
      ],
      dealSummary: '中资央企作为联合体牵头方签署 FIDIC 银皮书 EPC 总包合同，通过联合运营体 (KSO) 形式与本土企业实施属地施工。',
    },
    dimension2_rootCause: {
      coreDiagnosis: '未在合同专用条件中将原住民习惯法土地 (Hak Ulayat) 征拆明确列为业主风险，且误以为签署英文补充协议即可生效，未留痕 TKDN 供应链豁免批文。',
      contractPitfall: '盲目接受删除 FIDIC 14.8 延误付款利息，且未针对印尼《语言法》(UU 24/2009) 建立双语即时签署机制。',
      triggerFactors: [
        '地方习惯法首领阻工导致关键路径停工 180 天',
        '业主法务援引 UU 24/2009 第 31 条主张纯英文工期顺延备忘录自始无效',
        '工业部突击审查认定逆变器本地化率仅 28%（法定 40%），按日计提行政滞纳金',
      ],
    },
    dimension3_legalAnchors: [
      {
        normId: 'ID_SEMA:3_2023',
        nameZh: '印尼最高法院《2023年第3号通告》(SEMA 3/2023)',
        statuteSnippet: '除非证明存在恶意 (itikad tidak baik)，法院不得仅因涉外商事合同缺少印尼语版本而直接宣告合同无效。',
        keyRule: '成功推翻业主所谓“未签印尼语版则工期补偿协议绝对无效”之恶意抗辩，确立善意履约推定。',
      },
      {
        normId: 'ID_UU:2_2017:Art57',
        nameZh: '印尼《建筑服务法》(UU 2/2017) 第 57 条',
        statuteSnippet: 'BUJKA 必须与本土资质企业组建联合运营体 (KSO)，总包连带责任按约定分担。',
        keyRule: '保障联营体总包施工资质合法性，阻断业主关于无资质非法承揽之指控。',
      },
      {
        normId: 'ID_MEMR:Reg11_2024',
        nameZh: '印尼能矿部《2024年第11号电力本地化率规程》',
        statuteSnippet: '电力基础设施建设本土供应链无法满足技术规范的，可依法申请特别技术豁免许可。',
        keyRule: '为光伏逆变器本土产能不足提供法定免罚抗辩通道。',
      },
    ],
    dimension4_modelClauses: [
      {
        title: '反原住民习惯法土地征拆迟延专用条款 (Hak Ulayat Clause)',
        enClause: 'The Employer warrants that the Site shall be delivered free from any traditional or customary land claims (Hak Ulayat). Any failure or delay in delivering site possession due to local community protests shall constitute an Employer Risk under Clause 17.3, entitling the Contractor to an Extension of Time (EOT) and direct reimbursement of prolongation costs without deduction.',
        zhExplanation: '在 FIDIC 银皮书专用条件中明确将习惯法争议划归业主绝对风险，发生社区阻工时承包商自动享有工期顺延与费用补偿。',
      },
      {
        title: '涉外双语协议同等法律效力及善意履约保障条款',
        enClause: 'This Agreement is executed simultaneously in both the Indonesian and English languages. In case of any dispute or discrepancy between the two versions, the English version shall govern to the extent permitted by Law, and neither party shall raise any defense of contract invalidity based on Law No. 24 of 2009 pursuant to Supreme Court Circular SEMA No. 3/2023.',
        zhExplanation: '直接锁定以英文版为解释准据，并由双方在合同中共同签署“承诺不援引语言法瑕疵否定合同效力”的禁反言条款。',
      },
    ],
    dimension5_simulation: {
      initialFacts: '中资联合体总包印尼西爪哇光伏电站项目，业主迟延移交习惯法土地 180 天导致工期严重拖延，总包商依 FIDIC 8.4 发函索赔工期与费用，业主以补充协议仅有英文版且逆变器未达 TKDN 40% 为由扣留进度款并威胁索兑保函。',
      initialClaims: '1. 请求裁定工期顺延 180 天并免除逾期违约金；2. 依据印尼最高法院 SEMA 3/2023 确认英文顺延协议合法有效；3. 申请紧急仲裁禁令阻断业主滥用履约保函索兑。',
    },
  },
  {
    id: 'C102',
    code: 'C102',
    title: '沿海 350MW 海上风电并购 (M&A) 关联 EPC 保函恶意索兑与 2025 新建设法违约金案',
    jurisdiction: 'asean_vn',
    countryName: '越南',
    countryFlag: '🇻🇳',
    stage: '投前准入与签约审查',
    archetypes: ['CROSS_BORDER_MA', 'EPC_CONTRACTING'],
    summary: '中资央企拟收购越南风电项目公司股权并实施 EPC 总包；因越南工贸部 (MOIT) FIT 电价过渡期调整，业主收益受损，恶意发起 10% 履约保函索兑并按旧法主张高额工期罚金。',
    dimension1_structure: {
      parties: [
        { role: '原项目公司股东 (Seller/Sponsor)', name: '越南本土新能源民营投资财团' },
        { role: '并购方兼EPC总包商 (Buyer/EPC)', name: '中资跨国基建投资集团' },
        { role: '东道国购电方 (Offtaker)', name: '越南国家电力公司 (EVN)' },
        { role: '独立见索即付保函开证行', name: '渣打银行河内分行' },
      ],
      dealSummary: '褐地跨境股权收购 (SPA) 与关联 EPC 施工合同捆绑实施，以投资拉动工程出海。',
    },
    dimension2_rootCause: {
      coreDiagnosis: '在股权收购协议 (SPA) 中未对政府 FIT 电价下调设立交割前置条件调整机制，且未在 EPC 合同中对越南新旧建设法违约金封顶机制进行锁死。',
      contractPitfall: '保函未约定适用新加坡国际仲裁中心 (SIAC) 紧急仲裁员 (EA) 止付特别程序，缺乏快速司法阻断救济渠道。',
      triggerFactors: [
        '越南工贸部追溯取消风电优惠上网电价，项目预期 IRR 骤降',
        '业主商运日前夕向银行发出 10% 履约保函全额索兑通知',
        '业主按旧建设法主张累计按日罚金高达合同总额 15%，突破法定上限',
      ],
    },
    dimension3_legalAnchors: [
      {
        normId: 'VN_Law135_2025:Art86_2',
        nameZh: '越南《2025年新建设法》(Law 135/2025/QH15) 第 86.2 条',
        statuteSnippet: '建设工程合同当事人可依法约定预定损害赔偿 (Liquidated Damages)，但因业主原因或不可抗力导致延误的，承包商享有法定免责与顺延权。',
        keyRule: '新法打破旧法 12% 惩罚性违约金机械限制，同时确立情势变更法定免除违约金机制。',
      },
      {
        normId: 'VN_Decree210_2026:Art146',
        nameZh: '越南《第210/2026/ND-CP号建设合同法令》第 146 条',
        statuteSnippet: '因东道国法律政策重大调整导致工程无法继续履约的，各方应协商分担额外成本与工期影响。',
        keyRule: '为应对 FIT 电价政策变动提供东道国强行法层面的调价与顺延依据。',
      },
      {
        normId: 'BIT_CHINA_ASEAN:Art6',
        nameZh: '《中国-东盟投资协议》(BIT) 第 6 条',
        statuteSnippet: '缔约方不得对投资采取直接或间接征收措施，违反者须给予迅速、充分、有效的公允补偿。',
        keyRule: '构筑防范东道国以电价追溯下调进行隐性征收的国际投资仲裁后盾。',
      },
    ],
    dimension4_modelClauses: [
      {
        title: 'FIT 电价政策变动与并购对价联动调整条款 (Tariff Adjustment in SPA)',
        enClause: 'If prior to Closing or during commercial operation, MOIT or EVN reduces the approved Feed-in Tariff (FIT), the Purchase Price shall be downward adjusted dollar-for-dollar based on the revised financial model, or Buyer shall have the option to terminate this SPA without penalty.',
        zhExplanation: '在股权收购合同中设立电价滑脱保护机制，确保政策下调时直接冲减收购溢价或无损退出。',
      },
      {
        title: '履约保函滥用索兑紧急仲裁救济专用条款',
        enClause: 'The Employer expressly covenants that it shall not encash the Performance Security unless a final and binding arbitral award has been rendered by SIAC confirming material contractor default. Any call in breach of this covenant shall entitle Contractor to immediate mandatory injunction from an Emergency Arbitrator.',
        zhExplanation: '将保函索兑与仲裁实体结果挂钩，并授权紧急仲裁员直接签发止付禁令，阻断恶意欺诈索兑。',
      },
    ],
    dimension5_simulation: {
      initialFacts: '中资央企收购越南沿海海上风电项目公司 70% 股权并总承包施工，工程因台风及海事审批延期，商运日前夕越南国家电力公司调低 FIT 补贴，业主突击向开证行索兑 10% 履约保函并索赔高额误期赔偿。',
      initialClaims: '1. 向新加坡国际仲裁中心 (SIAC) 申请紧急仲裁员 (EA) 禁令止付履约保函；2. 依据越南《2025新建设法》第86.2条主张台风属不可抗力并顺延工期；3. 保留依据中越 BIT 协定提起国际投资仲裁权利。',
    },
  },
  {
    id: 'C103',
    code: 'C103',
    title: '吉隆坡轨道交通枢纽 CIPAA 快速裁决、背靠背付款无效与新加坡保函止付案',
    jurisdiction: 'asean_my',
    countryName: '马来西亚 & 新加坡',
    countryFlag: '🇲🇾',
    stage: '履约索赔与争议解决',
    archetypes: ['EPC_CONTRACTING'],
    summary: '业主拖欠中资总承包商 4,500 万令吉工程款；总包商援引“背靠背付款 (Pay-when-paid)”拒付本地土著分包商被提起 CIPAA 极速法定裁决；同时业主向新加坡母公司索兑履约保函。',
    dimension1_structure: {
      parties: [
        { role: '项目业主 (Owner)', name: '马来西亚交通部特许经营开发公司 (MRT Corp SPV)' },
        { role: '工程总承包商 (Main Contractor)', name: '中资基建集团马来西亚分公司' },
        { role: '土著机电分包商 (Subcontractor)', name: '马来西亚本土土著持股工程公司' },
        { role: '保函开立行 (Issuing Bank)', name: '星展银行新加坡总行 (DBS Bank SG)' },
      ],
      dealSummary: 'EPC 总承包合同准据法约定为马来西亚法，母公司履约保函开立地为新加坡。',
    },
    dimension2_rootCause: {
      coreDiagnosis: '严重低估马来西亚 CIPAA 2012 强行法效力，机械在分包合同中照搬“见业主付款后再向分包商付款”条款，导致触发极速裁决穿透。',
      contractPitfall: '未能预先在新加坡高等法院确立的 BS Mount Sophia“显失公平 (Unconscionability)”保函止付门槛下固定业主恶意违约证据。',
      triggerFactors: [
        '业主以内部审计为由冻结支付总包商 4,500 万令吉进度款',
        '土著分包商依据 CIPAA 2012 提起法定裁决，裁决员在 45 天内责令总承包商即刻付款',
        '业主反向发起新加坡母公司履约保函索兑',
      ],
    },
    dimension3_legalAnchors: [
      {
        normId: 'MY_CIPAA:Sec35',
        nameZh: '马来西亚《CIPAA 2012》第 35 条',
        statuteSnippet: '建设工程合同中任何以第三方付款为条件的背靠背付款条款 (Conditional Payment / Pay-when-paid) 均属绝对无效。',
        keyRule: '强行法直接粉碎总承包商以“业主未付款”为由抗辩分包商工程款的法律依据。',
      },
      {
        normId: 'MY_CIPAA:Sec13',
        nameZh: '马来西亚《CIPAA 2012》第 13 条',
        statuteSnippet: '快速裁决员的付款裁决具有法定强制执行力，债务人未遵期付款的总承包商可合法暂停施工。',
        keyRule: '赋予总承包商反向向业主启动 CIPAA 极速裁决并合法停工索赔的法律利器。',
      },
      {
        normId: 'SG_BSMountSophia:2016',
        nameZh: '新加坡高等法院 BS Mount Sophia 先例',
        statuteSnippet: '确立“显失公平 (Unconscionability)”作为见索即付独立保函独立止付裁判标准。',
        keyRule: '无需达到严苛的刑事诈欺证明标准，只要证明业主滥用保函、缺乏正当性即可向新加坡法院成功申请临时禁令。',
      },
    ],
    dimension4_modelClauses: [
      {
        title: '马来西亚分包合同受控付款节点条款 (替代无效的背靠背)',
        enClause: 'Payments to Subcontractor shall become due strictly upon the Independent Engineer certifying the milestone completion and quality compliance, regardless of receipt of funds by Main Contractor from Owner, provided that the certification cycle shall strictly adhere to Section 36 of CIPAA 2012.',
        zhExplanation: '用“独立监理工程师完工核验”替代非法的“见业主付款后付款”，在合规前提下锁定验收抗辩权。',
      },
      {
        title: '保函止付管辖与显失公平救济特别约定条款',
        enClause: 'The parties agree that this Performance Guarantee shall be subject to the exclusive jurisdiction of the High Court of Singapore, and that the Contractor shall be entitled to interlocutory injunctive relief upon demonstrating a prima facie case of unconscionability pursuant to BS Mount Sophia principles.',
        zhExplanation: '明文约定新加坡法院专属管辖，将 BS Mount Sophia 裁判规则直接吸纳为合同约定止付指引。',
      },
    ],
    dimension5_simulation: {
      initialFacts: '吉隆坡轨道交通总包项目中，马来西亚业主拖欠中资总包商 4,500 万令吉进度款，总包商以此为由暂缓向土著分包商付款；分包商依据 CIPAA 2012 第 35 条提起极速裁决，同时业主向新加坡开证行索兑履约保函。',
      initialClaims: '1. 依据马来西亚 CIPAA 2012 第 13 条反向向业主发起法定快速裁决并申请合法停工；2. 依据新加坡高等法院 BS Mount Sophia“显失公平”判例向新加坡法院申请保函止付禁令。',
    },
  },
  {
    id: 'C104',
    code: 'C104',
    title: '菲律宾跨海大桥 PPP 特许经营政府换届单方停工 (隐性征收) 与 PCAB 牌照合规案',
    jurisdiction: 'asean_ph',
    countryName: '菲律宾',
    countryFlag: '🇵🇭',
    stage: '投前准入与履约索赔双阶段',
    archetypes: ['PPP_CONCESSION', 'EPC_CONTRACTING'],
    summary: '菲律宾地方政府换届后以环保审查与国家安全审查为由单方暂停跨海大桥特许经营协议并不予公允补偿；当地工会举报中资联营体 PCAB 施工资质违规。',
    dimension1_structure: {
      parties: [
        { role: '特许权授予方 (Grantor)', name: '菲律宾公私合营管理中心与地方省政府 (LGU)' },
        { role: '特许经营项目公司 (Concessionaire)', name: '中资联合体投资控股项目公司 (SPC)' },
        { role: 'EPC总承包商 (Contractor)', name: '中国交通建设某工程局' },
        { role: '海外投资政治险承保人', name: '中国出口信用保险公司 (Sinosure)' },
      ],
      dealSummary: '采用 BOT 投建营一体化架构，特许经营期 30 年，含政府可行性缺口补贴 (VGF)。',
    },
    dimension2_rootCause: {
      coreDiagnosis: '特许权协议中仍援引已被废止的旧 BOT 法案 (RA 7718)，未对齐 2024 年生效的《菲律宾 PPP 法典》(RA 11966) 关于终止补偿的法定标准；未在 30 日内启动信保报损。',
      contractPitfall: '未能提前落实菲律宾最高院 PCAB v. Manila Water 案对外资普通施工许可证的最新准入备案。',
      triggerFactors: [
        '新换届地方政府借环保规划单方通知暂停特许权协议',
        '政府拒绝按公允市场价值对沉没资产及未来合理收益进行补偿',
        '当地行会试图以 40% 外资股权红线吊销联合体 PCAB 执照',
      ],
    },
    dimension3_legalAnchors: [
      {
        normId: 'PH_RA11966:PPP_Code',
        nameZh: '《菲律宾公私合营法典》(The PPP Code, RA 11966)',
        statuteSnippet: '明文废止旧 BOT 法案 (RA 7718/RA 6957)，确立特许经营终止时政府必须依据重置成本与已投入资产进行公允补偿。',
        keyRule: '杜绝引用已废止法律，锁定政府违约导致特许权终止时的刚性赔偿公式。',
      },
      {
        normId: 'PH_SC:G.R.217590_ManilaWater',
        nameZh: '菲律宾最高法院 PCAB v. Manila Water 里程碑判例',
        statuteSnippet: '最高法院裁定废除 PCAB 规则中关于常规施工牌照 60% 菲籍股权门槛，外资可合法取得普通承包执照。',
        keyRule: '直接粉碎当地行会关于“外资控股施工非法”的行政举报与资质吊销威胁。',
      },
      {
        normId: 'PRC_SASAC:Order35',
        nameZh: '国务院国资委 35 号令与中信保海外投资险保全',
        statuteSnippet: '央企境外重大投资遭遇东道国主权违约或间接征收的，必须在 30 日内完成出险报损留痕。',
        keyRule: '确保中信保政治风险险保全代位求偿权完整，筑牢国资监管安全底线。',
      },
    ],
    dimension4_modelClauses: [
      {
        title: '政府换届单方停工与特许权终止公允补偿条款 (RA 11966 对齐版)',
        enClause: 'In the event of unilateral suspension or termination by the Grantor due to policy review or national security considerations, the Grantor shall pay the Concessionaire Termination Compensation equal to all outstanding Project Debt plus the audited Historical Equity Invested compounded at the Contract WACC, strictly adhering to Section 22 of RA No. 11966.',
        zhExplanation: '将换届违约明确列为政府原因终止，并锁定“全部已投入权益资金+合理加权资金成本”刚性退出补偿公式。',
      },
      {
        title: 'PCAB 资质合规与 Manila Water 判例准用保障条款',
        enClause: 'The Grantor acknowledges and agrees that the Contractor holds a valid regular PCAB license in full compliance with the landmark ruling of the Supreme Court of the Philippines in PCAB v. Manila Water (G.R. No. 217590), and shall not challenge the validity thereof.',
        zhExplanation: '在合同中由政府方明示确认承包商执照合规性，阻断下属监管部门的事后行政阻挠。',
      },
    ],
    dimension5_simulation: {
      initialFacts: '菲律宾跨海大桥 BOT 特许经营项目中，地方政府换届后单方停工并拒付可行性缺口补贴 (VGF)，行会指控中资承包商 PCAB 执照违规，项目面临隐性征收与资产沉没风险。',
      initialClaims: '1. 依据《菲律宾 PPP 法典》(RA 11966) 主张政府违约并索赔已投入资产全额补偿；2. 依据菲律宾最高院 PCAB v. Manila Water 判例驳回资质违法指控；3. 正式启动中信保 30 日出险报损保全程序。',
    },
  },
];

export const CaseReferenceHub: React.FC = () => {
  const { openCaseEntryModal, showToast, openRightDock, setPrefillIntakeParams } = useApp();
  const [selectedCase, setSelectedCase] = useState<Case5DItem>(BENCHMARK_CASES_5D[0]);
  const [filterJur, setFilterJur] = useState<string>('all');
  const [copiedId, setCopiedId] = useState<string | null>(null);

  const filteredCases = BENCHMARK_CASES_5D.filter((c) => {
    if (filterJur !== 'all' && c.jurisdiction !== filterJur) return false;
    return true;
  });

  const handleCopyClause = (text: string, id: string) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    showToast('示范反制条款已复制到剪贴板', 'success');
    setTimeout(() => setCopiedId(null), 2000);
  };

  const handleOpenPlaybook = (item: Case5DItem) => {
    setSelectedCase(item);
    openRightDock('country_playbook');
    showToast(`已在右侧副驾坞展开【${item.countryName}】属地排雷与 5D 复盘手册`, 'info');
  };

  const handleSimulateCase = (item: Case5DItem) => {
    if (setPrefillIntakeParams) {
      setPrefillIntakeParams({
        title: item.title,
        jurisdiction: item.jurisdiction,
        raw_text: `${item.dimension5_simulation.initialFacts}\n\n【诉求】${item.dimension5_simulation.initialClaims}`,
        facts: item.dimension5_simulation.initialFacts,
        claims: item.dimension5_simulation.initialClaims,
      });
    }
    openCaseEntryModal({
      facts_zh: item.dimension5_simulation.initialFacts,
      claims_zh: item.dimension5_simulation.initialClaims,
      meta: {
        jurisdiction: item.jurisdiction,
        contract_type: item.archetypes.join('+'),
        choice_of_law: `${item.countryName}法律及 FIDIC 国际工程标准合同`,
      },
    });
  };

  return (
    <div className="space-y-6">
      {/* 顶部标题与筛选 */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-white p-5 rounded-2xl border border-zinc-200/80 shadow-xs">
        <div>
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-blue-600" />
            <h2 className="text-base font-bold text-zinc-900">
              中资出海基建典型参考案例库 (5D Case Review Cards)
            </h2>
          </div>
          <p className="text-xs text-zinc-500 mt-1">
            独创五维合规复盘卡：交易架构 ➔ 暴雷根因 ➔ 核心法源 ➔ 示范反制条款 ➔ 一键沙盘推演
          </p>
        </div>

        {/* 国别快速过滤 */}
        <div className="flex items-center gap-1.5 overflow-x-auto pb-1 text-xs">
          <button
            onClick={() => setFilterJur('all')}
            className={`px-3 py-1.5 rounded-lg font-medium transition-colors cursor-pointer ${
              filterJur === 'all'
                ? 'bg-zinc-900 text-white shadow-xs'
                : 'bg-zinc-100 text-zinc-600 hover:bg-zinc-200/70'
            }`}
          >
            全部标杆案
          </button>
          {[
            { id: 'asean_id', name: '印尼' },
            { id: 'asean_vn', name: '越南' },
            { id: 'asean_my', name: '大马/新' },
            { id: 'asean_ph', name: '菲律宾' },
          ].map((item) => (
            <button
              key={item.id}
              onClick={() => setFilterJur(item.id)}
              className={`px-3 py-1.5 rounded-lg font-medium transition-colors cursor-pointer ${
                filterJur === item.id
                  ? 'bg-zinc-900 text-white shadow-xs'
                  : 'bg-zinc-100 text-zinc-600 hover:bg-zinc-200/70'
              }`}
            >
              {item.name}
            </button>
          ))}
        </div>
      </div>

      {/* 案例列表与 5D 复盘卡展示区 */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* 左侧：4大标杆案例选择卡 (4 cols) */}
        <div className="lg:col-span-4 space-y-3">
          {filteredCases.map((item) => {
            const isSelected = selectedCase.id === item.id;
            return (
              <div
                key={item.id}
                onClick={() => setSelectedCase(item)}
                className={`p-4 rounded-xl border transition-all cursor-pointer ${
                  isSelected
                    ? 'bg-white border-blue-600 ring-1 ring-blue-600 shadow-sm'
                    : 'bg-white border-zinc-200/80 hover:border-zinc-300 hover:shadow-xs'
                }`}
              >
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-1.5">
                    <span className="text-base">{item.countryFlag}</span>
                    <span className="text-xs font-bold text-zinc-900">{item.countryName}</span>
                    <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-zinc-100 text-zinc-600 font-semibold">
                      {item.code}
                    </span>
                  </div>
                  <span className="text-[11px] text-zinc-400 font-medium">
                    {item.stage}
                  </span>
                </div>

                <h3 className="text-xs font-bold text-zinc-800 line-clamp-2 leading-relaxed mb-2">
                  {item.title}
                </h3>

                <p className="text-[11px] text-zinc-500 line-clamp-2 leading-normal">
                  {item.summary}
                </p>

                <div className="flex flex-wrap gap-1 mt-3">
                  {item.archetypes.map((arch) => (
                    <span
                      key={arch}
                      className="text-[10px] px-2 py-0.5 rounded-full bg-zinc-50 border border-zinc-200/60 text-zinc-600 font-mono"
                    >
                      {arch}
                    </span>
                  ))}
                </div>

                <div className="flex items-center justify-between gap-2 pt-2.5 border-t border-slate-100 mt-3">
                  <button
                    type="button"
                    onClick={(e) => {
                      e.stopPropagation();
                      handleOpenPlaybook(item);
                    }}
                    className="text-[11px] font-semibold text-blue-600 hover:text-blue-800 flex items-center gap-1 cursor-pointer"
                  >
                    <span>右侧副驾 5D 复盘</span>
                    <ArrowRight className="w-3 h-3" />
                  </button>
                  <button
                    type="button"
                    onClick={(e) => {
                      e.stopPropagation();
                      handleSimulateCase(item);
                    }}
                    className="text-[11px] font-semibold text-slate-700 hover:text-slate-900 bg-slate-100 hover:bg-slate-200 px-2.5 py-1 rounded-lg flex items-center gap-1 cursor-pointer"
                  >
                    <Play className="w-2.5 h-2.5 fill-current text-slate-800" />
                    <span>以此建案</span>
                  </button>
                </div>
              </div>
            );
          })}
        </div>

        {/* 右侧：五维合规复盘卡详情 (8 cols) */}
        <div className="lg:col-span-8 bg-white rounded-2xl border border-zinc-200/80 p-6 shadow-xs space-y-6">
          {/* 复盘卡头 */}
          <div className="border-b border-zinc-100 pb-4 flex flex-col md:flex-row md:items-center justify-between gap-3">
            <div>
              <div className="flex items-center gap-2">
                <span className="text-lg">{selectedCase.countryFlag}</span>
                <h3 className="text-sm font-bold text-zinc-900">
                  {selectedCase.code} · {selectedCase.title}
                </h3>
              </div>
              <p className="text-xs text-zinc-500 mt-1">
                适用法域：{selectedCase.countryName} ({selectedCase.jurisdiction}) · 阶段：{selectedCase.stage}
              </p>
            </div>

            <div className="flex items-center gap-2 shrink-0">
              <button
                onClick={() => handleOpenPlaybook(selectedCase)}
                className="px-3 py-2 bg-slate-100 hover:bg-slate-200 text-slate-800 rounded-xl text-xs font-semibold transition-colors flex items-center gap-1.5 cursor-pointer"
              >
                <Layers className="w-3.5 h-3.5 text-blue-600" />
                <span>副驾精读</span>
              </button>
              <button
                onClick={() => handleSimulateCase(selectedCase)}
                className="btn-space-titanium px-4 py-2 rounded-xl text-xs font-semibold flex items-center gap-1.5 cursor-pointer shadow-xs"
              >
                <Play className="w-3.5 h-3.5 fill-current text-emerald-400" />
                <span>以此案为蓝本沙盘推演</span>
              </button>
            </div>
          </div>

          {/* 维度 1: 交易架构与案情还原 */}
          <div className="space-y-3">
            <div className="flex items-center gap-2">
              <span className="w-1.5 h-1.5 rounded-full bg-zinc-400" />
              <h4 className="text-xs font-bold text-zinc-900 uppercase tracking-wider">
                维度 1【交易架构与案情还原】
              </h4>
            </div>
            <div className="p-4 rounded-xl bg-zinc-50/70 border border-zinc-200/60 space-y-3">
              <p className="text-xs text-zinc-700 leading-relaxed font-medium">
                {selectedCase.dimension1_structure.dealSummary}
              </p>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-2 text-xs">
                {selectedCase.dimension1_structure.parties.map((p, idx) => (
                  <div key={idx} className="p-2.5 rounded-lg bg-white border border-zinc-200/60">
                    <span className="text-[10px] text-zinc-400 block font-medium">{p.role}</span>
                    <span className="text-xs font-bold text-zinc-800 line-clamp-2 mt-0.5">{p.name}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* 维度 2: 暴雷根因诊断 (Root Cause) */}
          <div className="space-y-3">
            <div className="flex items-center gap-2">
              <span className="w-1.5 h-1.5 rounded-full bg-red-500" />
              <h4 className="text-xs font-bold text-zinc-900 uppercase tracking-wider">
                维度 2【暴雷根因诊断 (Root Cause)】
              </h4>
            </div>
            <div className="p-4 rounded-xl bg-red-50/30 border border-red-200/60 space-y-2">
              <div className="text-xs font-bold text-red-900">
                核心业务漏洞：{selectedCase.dimension2_rootCause.coreDiagnosis}
              </div>
              <div className="text-xs text-zinc-600">
                合同条款缺陷：{selectedCase.dimension2_rootCause.contractPitfall}
              </div>
              <div className="mt-2 space-y-1">
                {selectedCase.dimension2_rootCause.triggerFactors.map((f, idx) => (
                  <div key={idx} className="text-xs text-zinc-700 flex items-start gap-1.5">
                    <AlertTriangle className="w-3.5 h-3.5 text-amber-500 shrink-0 mt-0.5" />
                    <span>{f}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* 维度 3: 核心裁判规则与法源锚点 */}
          <div className="space-y-3">
            <div className="flex items-center gap-2">
              <span className="w-1.5 h-1.5 rounded-full bg-blue-600" />
              <h4 className="text-xs font-bold text-zinc-900 uppercase tracking-wider">
                维度 3【核心裁判规则与法源锚点】
              </h4>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
              {selectedCase.dimension3_legalAnchors.map((anchor, idx) => (
                <div key={idx} className="p-3 rounded-xl bg-zinc-50 border border-zinc-200/70 space-y-1.5">
                  <span className="text-[10px] font-mono font-bold text-blue-700 bg-blue-50 px-1.5 py-0.5 rounded">
                    {anchor.normId}
                  </span>
                  <div className="text-xs font-bold text-zinc-900 mt-1">{anchor.nameZh}</div>
                  <p className="text-[11px] text-zinc-500 line-clamp-2 italic">
                    "{anchor.statuteSnippet}"
                  </p>
                  <p className="text-[11px] text-zinc-700 font-medium">
                    {anchor.keyRule}
                  </p>
                </div>
              ))}
            </div>
          </div>

          {/* 维度 4: 央国企合规启示与示范反制条款 */}
          <div className="space-y-3">
            <div className="flex items-center gap-2">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-600" />
              <h4 className="text-xs font-bold text-zinc-900 uppercase tracking-wider">
                维度 4【央国企合规启示与示范反制条款 (Model Counter-Clause)】
              </h4>
            </div>
            <div className="space-y-3">
              {selectedCase.dimension4_modelClauses.map((clause, idx) => (
                <div key={idx} className="p-4 rounded-xl bg-zinc-50 border border-zinc-200/80 space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-bold text-zinc-900">{clause.title}</span>
                    <button
                      onClick={() => handleCopyClause(clause.enClause, `${selectedCase.id}-${idx}`)}
                      className="px-2 py-1 rounded text-[11px] bg-white border border-zinc-200 hover:bg-zinc-100 transition-colors flex items-center gap-1 cursor-pointer font-medium"
                    >
                      {copiedId === `${selectedCase.id}-${idx}` ? (
                        <>
                          <Check className="w-3 h-3 text-emerald-600" />
                          <span className="text-emerald-600">已复制</span>
                        </>
                      ) : (
                        <>
                          <Copy className="w-3 h-3 text-zinc-500" />
                          <span>复制英文条文</span>
                        </>
                      )}
                    </button>
                  </div>
                  <div className="p-2.5 rounded-lg bg-white border border-zinc-200/60 font-mono text-[11px] text-zinc-700 leading-relaxed select-all">
                    {clause.enClause}
                  </div>
                  <p className="text-xs text-zinc-600 font-medium leading-relaxed">
                    【实务要旨】{clause.zhExplanation}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
