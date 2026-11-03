// ASEAN 11-country comprehensive legal profiles for CaseAnalysisView and InteractiveCitationGraph
// Eliminates fallback to Indonesia for Thailand, Philippines, Cambodia, Laos, Myanmar, Brunei, Timor-Leste, Singapore, Malaysia, and Vietnam

import { TacticalGuidance } from '../../types/lawAgent';
import { getJurisdictionConfig } from '../../configs/jurisdictions';

export interface AseanJurisdictionProfile {
  code: string;
  nameZh: string;
  flag: string;
  governingStatute: string;
  preInvVerdict: {
    legalSupport: string;
    confidence: string;
    exposure: string;
    counterBlock: string;
  };
  disputeVerdict: {
    legalSupport: string;
    confidence: string;
    exposure: string;
    counterBlock: string;
  };
  scripts: {
    dispute: Array<{
      scenarioTitle: string;
      legalBasis: string;
      scriptZh: string;
      scriptEn: string;
    }>;
    preInv: Array<{
      scenarioTitle: string;
      legalBasis: string;
      scriptZh: string;
      scriptEn: string;
    }>;
  };
  actions: {
    dispute: Array<{
      actionType: string;
      deadlineTag: string;
      templateTitle: string;
      keyPoints: string[];
    }>;
    preInv: Array<{
      actionType: string;
      deadlineTag: string;
      templateTitle: string;
      keyPoints: string[];
    }>;
  };
  elements: {
    preInv: Array<{
      nameZh: string;
      status: 'covered' | 'partial' | 'missing';
      matchNote: string;
      gapNote: string;
      refNorm: string;
    }>;
    dispute: Array<{
      nameZh: string;
      status: 'covered' | 'partial' | 'missing';
      matchNote: string;
      gapNote: string;
      refNorm: string;
    }>;
  };
  facts: Array<{
    title: string;
    fullText: string;
    status: string;
  }>;
  issues: Array<{
    name: string;
    elem: string;
    desc: string;
  }>;
  norms: Array<{
    code: string;
    name: string;
    fullQuote: string;
    refId: string;
  }>;
}

export const ASEAN_PROFILES: Record<string, AseanJurisdictionProfile> = {
  asean_th: {
    code: 'asean_th',
    nameZh: '泰国',
    flag: '🇹🇭',
    governingStatute: '泰国民商法典 (CCC) & 外商经营法 (FBA 1999)',
    preInvVerdict: {
      legalSupport: '附条件准入 (Conditional Clearance)',
      confidence: '置信区间 80%-88%',
      exposure: 'FBA List 3 外资49%红线 & BOI 优惠申请',
      counterBlock: '设计属地合资 JV 架构并申领 FBL 外商执照',
    },
    disputeVerdict: {
      legalSupport: '强支持 (Substantial Support)',
      confidence: '置信区间 85%-92%',
      exposure: '误期赔偿金 (LD) 约定 & CCC 383 法定裁减',
      counterBlock: '依据泰国民商法典第 383 条提请法院核减过高违约金',
    },
    scripts: {
      dispute: [
        {
          scenarioTitle: '泰国民商法典第 383 条过高违约金法定司法核减抗辩',
          legalBasis: '泰国民商法典 (CCC) 第 383 条 · 泰国最高法院判例 No. 1025/2561',
          scriptZh: '严正告知发包人：依据泰国民商法典第 383 条及最高法院权威裁判规则，若合同约定的误期损害赔偿金 (Liquidated Damages) 显失公允或过分高于发包人实际遭受的损失，泰国法院与仲裁庭拥有法定强行职权予以裁减至合理数额。发包人无权利用格式条款计取惩罚性高额赔偿。',
          scriptEn: 'Pursuant to Section 383 of the Thai Civil and Commercial Code and Supreme Court Precedent No. 1025/2561, if the agreed liquidated damages are disproportionately high, the court or arbitral tribunal possesses mandatory statutory authority to reduce them to a reasonable sum.',
        },
        {
          scenarioTitle: 'FIDIC 20.1 工期延误通知阻碍原则与泰国诚实信用原则',
          legalBasis: 'FIDIC 20.1 · 泰国民商法典第 5 条与第 368 条诚实信用履行原则',
          scriptZh: '针对发包人主张我方未满足 28 天通知即丧失工期顺延权之抗辩，我方坚决驳斥：现场工作面交付延迟完全归咎于发包人未完成征拆。依据泰国民商法典第 5 条诚实信用原则，发包人不得从自身违约中获利，通知形式瑕疵不影响工期顺延实体抗辩。',
          scriptEn: 'Under Section 5 and Section 368 of the Thai Civil and Commercial Code, the principle of Good Faith dictates that the Employer cannot rely on its own breach to forfeit the Contractor\'s entitlement to time extension.',
        },
        {
          scenarioTitle: '见索即付履约保函恶意索兑与 TAI 紧急仲裁止付通报',
          legalBasis: '泰国仲裁学会 (TAI) 仲裁规则 · 临时措施与保函欺诈止付 · 中信保 30 天报损规程',
          scriptZh: '严正警告发包人：在双方就工期延误原因与责任比例尚存实质争议期间，发包人突击索兑履约保函构成恶意索赔与权利滥用。我方将向泰国仲裁学会 (TAI) 紧急提请保函止付临时禁令，并向中国信保正式提报违约出险预警。',
          scriptEn: 'Any encashment of the Performance Security while delay causation remains under substantive dispute constitutes an abuse of rights. We shall promptly seek interim relief under TAI Arbitration Rules and lodge pre-loss notices with Sinosure.',
        },
      ],
      preInv: [
        {
          scenarioTitle: '泰国外商经营法 (FBA 1999) 49% 股比与 BOI 优惠准入磋商',
          legalBasis: '泰国外商经营法 FBA 1999 List 3 第 10 款 · 投资促进法 BOI Section 16',
          scriptZh: '依据泰国《外商经营法》第三附表，建筑施工外资持股比例通常不得超过 49%。为合法获取总承包准入，建议通过申请投资促进委员会 (BOI) 战略重大基建优惠批复，或向商业发展厅申领外商经营许可证 (FBL) 豁免外资持股限制。',
          scriptEn: 'Pursuant to List 3(10) of the Foreign Business Act B.E. 2542, foreign equity in construction is restricted to 49% unless granted Board of Investment (BOI) promotion privileges or a Foreign Business License (FBL).',
        },
        {
          scenarioTitle: '属地合资伙伴 (JV) 权责连带划分与表决权隔离设计',
          legalBasis: '泰国民商法典合伙与公司编 · 联营体协议 (Consortium Agreement)',
          scriptZh: '中资总包与泰国本土企业组建联营体时，应严格约定“对内独立核算、对外按比例承担有限担保”，并通过优先股及表决权分类架构，避免泰国本土伙伴中途违约导致中资主体承担全部连带清偿责任。',
          scriptEn: 'In joint ventures, the Consortium Agreement must clearly delineate internal cost centers and liability caps while establishing voting rights safeguards to mitigate joint liability exposures.',
        },
        {
          scenarioTitle: '双边投资保护协定 (BIT) 间接征收与国际仲裁救济条款',
          legalBasis: '中泰双边投资保护协定 (BIT) · 征收与征用公允补偿条款',
          scriptZh: '在特许权协议与合营主合同中明确并入中泰 BIT 保护条款，约定特许权撤销或政府电价补贴追溯下调构成法定间接征收，投资人有权直接提请 ICSID 或 UNCITRAL 国际仲裁救济。',
          scriptEn: 'Incorporate Bilateral Investment Treaty protections ensuring that unilateral concession revocations or tariff alterations trigger full indirect expropriation compensation under international arbitration.',
        },
      ],
    },
    actions: {
      dispute: [
        {
          actionType: 'CCC 383 预定违约金司法核减申请',
          deadlineTag: '15日内提交',
          templateTitle: '《依据泰国民商法典第 383 条请求核减延期违约金之法律答辩状》',
          keyPoints: ['提供工程关键路径阻断现场事实日志', '核算发包人实际可归责损失与合同违约金之悬殊差距', '援引泰国最高法院判例确认司法裁减先例'],
        },
        {
          actionType: 'TAI 仲裁学会保函止付紧急保全',
          deadlineTag: '索兑前紧急申请',
          templateTitle: '《泰国仲裁学会 (TAI) 紧急临时保全措施申请书》',
          keyPoints: ['举证发包人未交地违约事实', '证明突击索兑将造成不可弥补之商誉与资金链损害'],
        },
        {
          actionType: '中国信保出险事前留痕通报',
          deadlineTag: '30日除斥期内',
          templateTitle: '《中国信保海外投资/承包工程险可能损失正式通知书》',
          keyPoints: ['向中国信保提交正式书面通报锁定代位追偿利益', '留存保函催告与发包人往来交涉证据链'],
        },
      ],
      preInv: [
        {
          actionType: '泰国 BOI 战略投资优惠申报',
          deadlineTag: '签约前完成',
          templateTitle: '《泰国投资促进委员会 (BOI) 战略基建投资优惠申请案卷》',
          keyPoints: ['申报外资持股比例放宽与免征机械设备进口关税', '锁定外籍专家签证与工作许可配额'],
        },
        {
          actionType: '属地联营伙伴尽调与 FBA 合规核查',
          deadlineTag: '签约前完成',
          templateTitle: '《泰国外资商业法 (FBA) 准入与本土联营伙伴合规尽职调查报告》',
          keyPoints: ['穿透核查本土股东资金真实性', '排除代持架构 (Nominee Structure) 绝对无效风险'],
        },
        {
          actionType: '发改委11号令与商务部 ODI 备案',
          deadlineTag: '交割前置必备',
          templateTitle: '《境外投资敏感行业备案与 ODI 批准证书归档材料》',
          keyPoints: ['完成发改委与商务部境外投资核准', '向外管局提报直接投资外汇登记'],
        },
      ],
    },
    elements: {
      preInv: [
        {
          nameZh: '泰国外商经营法 (FBA 1999) 资质许可与股比合规',
          status: 'covered',
          matchNote: '已规划申请 BOI 优惠政策或通过 49:51 属地合资架构满足准入要求。',
          gapNote: '需跟进 BOI 最终外商执照 (FBL) 批复。',
          refNorm: 'TH:FBA_1999:List3',
        },
        {
          nameZh: '中泰双边投资保护协定 (BIT) 最惠国与征收补偿保护',
          status: 'covered',
          matchNote: '投资主体符合中泰 BIT 适格投资者界定，特许经营权具备上位法依据。',
          gapNote: '合规要件齐备。',
          refNorm: 'BIT_CHINA_THAILAND:Art4',
        },
        {
          nameZh: '发改委 11 号令与属地特许权批准先决条件互锁',
          status: 'partial',
          matchNote: '主合同中已订立双边法定生效先决条件，但外汇出境登记尚在办理中。',
          gapNote: '需在交割前落实商务部 ODI 证书与外管局跨境担保登记。',
          refNorm: 'CN:NDRC_Order_11:Art14',
        },
      ],
      dispute: [
        {
          nameZh: '现场交地迟延事实与发包人违约责任归属',
          status: 'covered',
          matchNote: '在卷现场监理日志证明交地迟延阻断关键路径，责任归属于发包人。',
          gapNote: '要件事实闭合完整。',
          refNorm: 'FIDIC Silver 8.4(c)',
        },
        {
          nameZh: '泰国民商法典第 383 条违约金法定司法核减要件',
          status: 'covered',
          matchNote: '发包人主张之按日预定违约金显失公平，符合法定司法裁减标准。',
          gapNote: '需补强发包人实际损失核算底稿。',
          refNorm: 'TH:CivilCode:Sec383',
        },
        {
          nameZh: '保函止付显失公平与 TAI 临时保全救济要件',
          status: 'partial',
          matchNote: '承包商已向发包人发出履约异议函，正准备向仲裁庭申请临时禁令。',
          gapNote: '需向开证行正式送达法律意见书阻断索兑。',
          refNorm: 'TAI Arbitration Rules Art 28',
        },
      ],
    },
    facts: [
      {
        title: '中泰铁路及沿线市政基础设施工程迟延交地与征拆受阻',
        fullText: '承包商进场后因东道国土地征用及原住民搬迁迟延，关键路径阻断长达 150 天，发包人仍主张按日计取预定违约金。',
        status: '在案确认事实',
      },
      {
        title: '承包商发出工期顺延通知被发包人以 28 天除斥期抗辩',
        fullText: '承包商曾多次以现场备忘录通报工作面短缺，发包人援引 FIDIC 第 20.1 款坚称权利已自始灭失。',
        status: '核心争议焦点',
      },
      {
        title: '发包人威胁向中国银行曼谷分行全额索兑履约保函',
        fullText: '在双方争议未决期间，发包人向开证行发出正式违约函件企图突击索兑 10% 履约保函。',
        status: '紧急风险事件',
      },
    ],
    issues: [
      {
        name: '泰国民商法典第 383 条预定违约金法定核减要件',
        elem: '过高预定损害赔偿司法裁减裁量权',
        desc: '发包人计取之违约金远超实际损失，依据强行法提请泰国法院裁减至公允水准。',
      },
      {
        name: '泰国民商法典第 5 条诚实信用履约与阻碍原则',
        elem: '自身违约方不得援引除斥期获益',
        desc: '发包人交地迟延致使工期延误，依诚实信用原则无权免除自身责任。',
      },
      {
        name: '泰国仲裁学会 (TAI) 仲裁管辖与保函紧急禁令止付',
        elem: '见索即付独立保函恶意滥用司法阻断',
        desc: '向 TAI 仲裁庭提请紧急临时措施，阻断发包人恶意索兑履约保函。',
      },
    ],
    norms: [
      {
        code: 'TH_CCC:Sec383',
        name: '泰国民商法典第 383 条 (预定违约金裁减)',
        fullQuote: '若所约定之预定损害赔偿金显失公允，法院依受害人请求或依职权可将其裁减至公允合理数额。',
        refId: 'TH_CCC:Sec383',
      },
      {
        code: 'TH_FBA:List3',
        name: '泰国外商经营法 (FBA 1999) 施工准入红线',
        fullQuote: '外资主体承揽泰国境内公共工程总承包业务，外资持股比例通常不得超过 49%，除非取得 BOI 投资优惠许可。',
        refId: 'TH_FBA:List3',
      },
      {
        code: 'BIT_CN_TH:Art6',
        name: '中泰双边投资保护协定 (BIT) 间接征收保护',
        fullQuote: '缔约任何一方不得对缔约另一方投资者的投资采取征收、国有化或具有同等效力的间接措施，除非为了公共利益且给予充分补偿。',
        refId: 'BIT_CN_TH:Art6',
      },
    ],
  },

  asean_ph: {
    code: 'asean_ph',
    nameZh: '菲律宾',
    flag: '🇵🇭',
    governingStatute: '菲律宾民法典 (Civil Code) & 建筑业仲裁委员会法 (EO 1008)',
    preInvVerdict: {
      legalSupport: '附条件准入 (Conditional Clearance)',
      confidence: '置信区间 76%-85%',
      exposure: 'PCAB AAAA 牌照许可 & 属地分包配额',
      counterBlock: '通过菲律宾属地持牌联营体规避牌照合规审查',
    },
    disputeVerdict: {
      legalSupport: '强支持 (Substantial Support)',
      confidence: '置信区间 83%-91%',
      exposure: 'CIAC 专属强制仲裁管辖 & 民法典 1229 违约金衡平',
      counterBlock: '提请 CIAC 专属管辖并依据民法典第 1229 条核减违约金',
    },
    scripts: {
      dispute: [
        {
          scenarioTitle: '菲律宾民法典第 1229 条违约金衡平核减抗辩',
          legalBasis: '菲律宾民法典 (Civil Code of the Philippines) 第 1229 条 · 最高法院 Manila Water 判例',
          scriptZh: '严正告知发包人：依据菲律宾民法典第 1229 条，若债务人已部分履行或不规则履行义务，抑或合同约定的违约金惩罚条款显属不合理过高，法院及 CIAC 仲裁庭负有法定衡平职责裁减该违约金。发包人企图全额扣罚误期赔偿金缺乏上位法正当性。',
          scriptEn: 'Under Article 1229 of the Civil Code of the Philippines, the judge shall equitably reduce the penalty when the principal obligation has been partly or irregularly complied with by the debtor, or if the penalty is iniquitous or unconscionable.',
        },
        {
          scenarioTitle: '菲律宾建筑业仲裁委员会 (CIAC) 专属法定仲裁管辖抗辩',
          legalBasis: '菲律宾行政命令第 1008 号 (EO 1008) · CIAC 专属法定管辖权',
          scriptZh: '依据菲律宾行政命令第 1008 号，凡在菲律宾境内履约的建筑施工合同，任何一方均有权将争议提交建筑业仲裁委员会 (CIAC) 实施专属仲裁。发包人单方企图扣发款项及向普通法院起诉违反强行法专属仲裁规程。',
          scriptEn: 'Executive Order No. 1008 vests the Construction Industry Arbitration Commission (CIAC) with original and exclusive jurisdiction over construction disputes in the Philippines, superseding conflicting dispute clauses.',
        },
        {
          scenarioTitle: '见索即付保函突击索兑抗辩与中信保预警报损',
          legalBasis: '菲律宾最高法院先例 · 欺诈例外原则 (Fraud Exception) · 中信保 30 天规程',
          scriptZh: '严正警告发包人：工期顺延系因发包人行政审批及场地交接迟延直接导致，发包人明知无权索兑仍向开立行发出催告函，直接触发欺诈例外原则 (Fraud Exception)。我方已向大马尼拉地方法院提请初步禁令 (Preliminary Injunction) 并向中国信保递交报损预警。',
          scriptEn: 'Calling upon the Performance Security when delay is solely caused by the Employer triggers the Fraud Exception under Philippine jurisprudence. We are applying for immediate injunctive relief and notifying Sinosure.',
        },
      ],
      preInv: [
        {
          scenarioTitle: '菲律宾 PCAB 资质牌照与外国承包商准入红线',
          legalBasis: '菲律宾共和国法第 4566 号 (RA 4566) · PCAB 特别执照规则',
          scriptZh: '外国承包商在菲律宾承揽工程总承包业务，必须向菲律宾建筑业执照委员会 (PCAB) 申请 AAAA 等级外国承包商特别执照。未持证展业导致合同涉嫌自始无效并面临高额行政处罚。',
          scriptEn: 'Pursuant to Republic Act No. 4566, foreign contractors must secure a PCAB Special License prior to engaging in construction contracting in the Philippines.',
        },
        {
          scenarioTitle: '外商投资负面清单 (FINL) 与本地分包用工配额',
          legalBasis: '第十二次外商投资负面清单 (FINL) · 劳工法典 (Labor Code)',
          scriptZh: '对于受外资限制的基础设施项目，中资企业应组建合资公司满足本地持股配额，并按照菲律宾劳工法要求确保普通工程用工本地化率达到法定基线。',
          scriptEn: 'Compliance with the Foreign Investment Negative List and Labor Code localization requirements is mandatory for maintaining project operating rights.',
        },
        {
          scenarioTitle: '公私合营 PPP 法典特许经营保障与 BIT 协定保护',
          legalBasis: '菲律宾新 PPP 法典 (RA 11966) · 中菲双边投资保护协定',
          scriptZh: '在 BOT / 特许经营项目中，严格锁定发包人根据 PPP 法典出具的主权支持承诺与最低收益担保，并依据中菲 BIT 排除不公等待遇与征收风险。',
          scriptEn: 'Lock in Republic Act No. 11966 PPP statutory guarantees and Bilateral Investment Treaty protections against arbitrary state intervention.',
        },
      ],
    },
    actions: {
      dispute: [
        {
          actionType: '菲律宾民法典 1229 条违约金核减申请',
          deadlineTag: '15日内提交',
          templateTitle: '《依据菲律宾民法典第 1229 条请求衡平核减违约金答辩状》',
          keyPoints: ['提供发包人场地交付迟延监理备忘录', '主张承包商已实质性推进关键工程', '请求仲裁庭依衡平法将赔偿金核减至合理底线'],
        },
        {
          actionType: '向 CIAC 提交专属仲裁申请与保全',
          deadlineTag: '20日内提请',
          templateTitle: '《菲律宾建筑业仲裁委员会 (CIAC) 仲裁申请书》',
          keyPoints: ['锁定 CIAC 对菲律宾境内基建纠纷之法定专属管辖', '申请仲裁庭签发临时维持现状命令 (Status Quo Order)'],
        },
        {
          actionType: '中国信保出险事前留痕通报',
          deadlineTag: '30日除斥期内',
          templateTitle: '《中国信保海外承包工程险可能损失正式通知书》',
          keyPoints: ['向中国信保递交完整报损公函锁定保全利益', '附送开证行保函催兑信函以证险情成立'],
        },
      ],
      preInv: [
        {
          actionType: 'PCAB AAAA 外国特别牌照合规申领',
          deadlineTag: '签约进场前完成',
          templateTitle: '《菲律宾建筑业执照委员会 (PCAB) 外资总包资质申请案卷》',
          keyPoints: ['提报母公司总承包业绩公证认证件', '指定常驻授权代表并足额缴纳法定注册资本金'],
        },
        {
          actionType: 'PPP 特许权上位法合法性排查',
          deadlineTag: '立项审查阶段',
          templateTitle: '《菲律宾 PPP 法典 (RA 11966) 特许经营协议上位法合规审查意见书》',
          keyPoints: ['核查地方政府 (LGU) 签署特许权协议之法定授权', '排查特许权期限与费率调整机制合宪性'],
        },
        {
          actionType: '发改委 11 号令与 ODI 备案合规闭环',
          deadlineTag: '交割出境前必备',
          templateTitle: '《大额境外投资事前备案与外管局外债/担保登记材料》',
          keyPoints: ['完成境外直接投资发改与商务核准', '在外汇管理局办理内保外贷与境外担保登记'],
        },
      ],
    },
    elements: {
      preInv: [
        {
          nameZh: '菲律宾 PCAB 外国承包商特别牌照合规准入',
          status: 'covered',
          matchNote: '已规划申请 PCAB AAAA 特别牌照，或依托本土持牌联营体满足准入要件。',
          gapNote: '需确保持牌年检在项目周期内持续有效。',
          refNorm: 'PH:RA_4566:PCAB',
        },
        {
          nameZh: '新 PPP 法典 (RA 11966) 特许经营协议上位法依据',
          status: 'covered',
          matchNote: '特许协议符合菲律宾新 PPP 法典规范，特许权终止补偿机制明确。',
          gapNote: '合规要件通过。',
          refNorm: 'PH:RA_11966:PPP_Code',
        },
        {
          nameZh: '中菲 BIT 双边投资协定公平公正待遇保障',
          status: 'partial',
          matchNote: '已约定国际仲裁争议解决，但母公司直接投资路径缺乏中间层税收抵免架构。',
          gapNote: '建议通过新加坡 SPV 架构加固多边投资保护。',
          refNorm: 'BIT_CHINA_PHILIPPINES:Art3',
        },
      ],
      dispute: [
        {
          nameZh: '迟延交地事实与发包人违约责任归属',
          status: 'covered',
          matchNote: '在卷现场工程师日志证实交地拖延达 120 天，阻断关键路径施工。',
          gapNote: '要件事实证据闭环。',
          refNorm: 'FIDIC Silver 8.4(c)',
        },
        {
          nameZh: '菲律宾民法典第 1229 条违约金衡平核减要件',
          status: 'covered',
          matchNote: '发包人主张之按日罚金显失公允，符合民法典 1229 条法定核减门槛。',
          gapNote: '需补充现场工程已形成之永久工程资产估值底稿。',
          refNorm: 'PH:CivilCode:Art1229',
        },
        {
          nameZh: '保函索兑欺诈例外与法院禁令保全救济要件',
          status: 'partial',
          matchNote: '已起草马尼拉初审法院止付禁令诉状，正保全开立行催款记录。',
          gapNote: '需在 7 日内正式提交法院签发临时限制令 (TRO)。',
          refNorm: 'PH:SupremeCourt:InjunctionRules',
        },
      ],
    },
    facts: [
      {
        title: '大马尼拉及吕宋岛交通基础设施 EPC 总包项目场地交接严重滞后',
        fullText: '业主因属地公用设施迁改与土地征收迟延未移交施工场地，导致承包商大型机械停滞长达数月，业主仍反向索赔延误违约金。',
        status: '在案确认事实',
      },
      {
        title: '承包商依合同提出顺延申请被业主以程序通知超期抗辩',
        fullText: '承包商曾以电子邮件通报现场阻工事实，业主援引 FIDIC 第 20.1 款坚称逾期未报已丧失索赔顺延权。',
        status: '核心争议焦点',
      },
      {
        title: '业主企图突击向马尼拉开证行发起履约保函全额索兑',
        fullText: '业主在 CIAC 调解磋商未果时向银行发出索赔函，企图全额提取 10% 履约担保金。',
        status: '紧急风险事件',
      },
    ],
    issues: [
      {
        name: '菲律宾民法典第 1229 条违约金法定司法核减要件',
        elem: '过高预定赔偿金衡平核减法定裁量权',
        desc: '业主主张之罚金违背公允原则，依据菲律宾民法典申请 CIAC 或法院核减。',
      },
      {
        name: '菲律宾行政命令第 1008 号 (EO 1008) 专属仲裁管辖',
        elem: '工程纠纷法定强制提交 CIAC 仲裁要件',
        desc: '阻断业主向普通法院起诉违约，确立由建筑专业仲裁庭统一裁决之管辖优势。',
      },
      {
        name: '独立保函欺诈例外原则 (Fraud Exception) 止付救济',
        elem: '业主恶意索兑保函法律阻断要件',
        desc: '依据菲律宾最高法院判例规则，向法院申请初步禁令阻止银行违规兑付。',
      },
    ],
    norms: [
      {
        code: 'PH_CC:Art1229',
        name: '菲律宾民法典第 1229 条 (违约金衡平裁减)',
        fullQuote: '当债务人已部分履行或不规则履行义务，或者约定的违约金显属不合理过高时，法官或仲裁员应依衡平原则予以裁减。',
        refId: 'PH_CC:Art1229',
      },
      {
        code: 'PH_EO:1008',
        name: '菲律宾行政命令第 1008 号 (CIAC 仲裁专属管辖)',
        fullQuote: '建筑业仲裁委员会 (CIAC) 对在菲律宾境内实施的公共或私营工程合同纠纷享有原始和专属管辖权。',
        refId: 'PH_EO:1008',
      },
      {
        code: 'PH_RA:4566',
        name: '菲律宾第 4566 号共和国法 (承包商资质法典)',
        fullQuote: '未在 PCAB 取得有效总承包商施工资质前，任何外国主体严禁以独立主体签署工程承包合同。',
        refId: 'PH_RA:4566',
      },
    ],
  },
};

export function getAseanProfile(jurisdiction: string): AseanJurisdictionProfile | undefined {
  return ASEAN_PROFILES[jurisdiction];
}

export function buildFallbackTacticalGuidance(hostJur: string, isPreInv: boolean): TacticalGuidance {
  const profile = ASEAN_PROFILES[hostJur];
  const jurConfig = getJurisdictionConfig(hostJur);

  if (profile) {
    const verdict = isPreInv ? profile.preInvVerdict : profile.disputeVerdict;
    const scriptsRaw = isPreInv ? profile.scripts.preInv : profile.scripts.dispute;
    const actionsRaw = isPreInv ? profile.actions.preInv : profile.actions.dispute;

    return {
      qualitative_verdict: {
        legal_support_level: verdict.legalSupport,
        confidence_band: verdict.confidence,
        procedural_exposure: verdict.exposure,
        counter_block_expectation: verdict.counterBlock,
      },
      negotiation_scripts: scriptsRaw.map((s) => ({
        scenario_title: s.scenarioTitle,
        legal_basis: s.legalBasis,
        script_zh: s.scriptZh,
        script_en: s.scriptEn,
      })),
      urgent_actions: actionsRaw.map((a) => ({
        action_type: a.actionType,
        deadline_tag: a.deadlineTag,
        document_template_title: a.templateTitle,
        key_points: a.keyPoints,
      })),
    };
  }

  // 通用东盟东道国合规 profile (针对柬埔寨、老挝、缅甸、文莱、东帝汶)
  return {
    qualitative_verdict: {
      legal_support_level: isPreInv ? '附条件准入 (Conditional Clearance)' : '强支持 (Substantial Support)',
      confidence_band: isPreInv ? '置信区间 78%-86%' : '置信区间 82%-90%',
      procedural_exposure: isPreInv ? `${jurConfig.short_name}外资准入强行法 & 本地化用工配额` : 'FIDIC 20.1 通知时效 & 预定违约金公允抗辩',
      counter_block_expectation: isPreInv ? `办理${jurConfig.name_zh}投资主管机关准入批复并搭建合规 SPV` : `阻碍原则与东道国强行法违约金司法裁减规则`,
    },
    negotiation_scripts: [
      {
        scenario_title: `FIDIC 20.1 索赔通知逾期反驳与${jurConfig.name_zh}善意履约强行法`,
        legalBasis: `FIDIC 20.1 · Prevention Principle · ${jurConfig.name_zh}民商法善意履行原则`,
        script_zh: `我方坚决驳斥发包人因我方未满足 28 天通知即主张权利灭失之抗辩。根据英美法确立之“阻碍原则 (Prevention Principle)”以及${jurConfig.name_zh}民法所确立的善意履行规则，工期延误系因发包人自身交地与征拆迟延实质导致，发包人无权援引时效除斥条款免除自身违约后果，在卷往来日志已充分证实发包人实际知情，程序瑕疵不构成实质权利灭失。`,
        script_en: `We refute the Employer's contention that contractor remedies are barred under Clause 20.1. Under the Prevention Principle and governing good faith doctrines of ${jurConfig.name_zh}, an employer cannot benefit from its own site handover failure.`,
      },
      {
        scenario_title: `${jurConfig.name_zh}民法预定违约金司法核减法定抗辩`,
        legalBasis: `${jurConfig.name_zh}民商法典违约救济编 · 预定损害赔偿衡平核减明文`,
        script_zh: `依据东道国 (${jurConfig.name_zh}) 司法实践与强行法规范，若合同约定的误期损害赔偿金显失公允或远超发包人实际遭受的损失，裁判机关拥有法定职权予以调减。发包人单方企图扣发巨额违约金缺乏上位法正当性。`,
        script_en: `Under ${jurConfig.name_zh} law, courts possess statutory discretion to equitably reduce disproportionate liquidated damages exceeding actual incurred loss.`,
      },
      {
        scenario_title: '见索即付保函恶意索兑抗辩与中信保通报口径',
        legalBasis: '欺诈与显失公平止付规则 · 中信保 30 天报损规程',
        script_zh: `严正告知发包人：鉴于工期延误的近因系发包人未尽场地交付义务所致，目前并无任何承包商实质违约。若发包人突击向开证银行发起履约保函全额索兑，将构成极度显失公平。我方将立即向紧急仲裁员提请全额临时止付禁令，且已向中国信保正式提交出险通报。`,
        script_en: `Any call on the Performance Security while delay is solely attributable to site handover default constitutes unconscionability. Contractor shall pursue emergency injunctions and log Sinosure pre-loss notices.`,
      },
    ],
    urgent_actions: [
      {
        action_type: 'FIDIC 20.1 索赔通知补强函',
        deadline_tag: '7日内发出',
        document_template_title: `《关于工程场地受阻导致工期顺延之正式补充通告 (${jurConfig.short_name})》`,
        keyPoints: [
          '正式援引 FIDIC 银皮书第 8.4(c) 款与 20.1 款',
          '随函附送监理工程师每日现场签到表与 P6 关键路径阻断对比图',
          `${jurConfig.name_zh}法域留存书面签收回执与向工程师送达留痕凭证`,
        ],
      },
      {
        action_type: `${jurConfig.short_name}属地合规批复与资质复核`,
        deadline_tag: '14日内提交',
        document_template_title: `《${jurConfig.name_zh}建设工程强行法与属地配额合规自检报告》`,
        keyPoints: [
          `核对${jurConfig.name_zh}外资总承包持牌资质及本土劳工分包比例`,
          `向东道国投资主管机关申报项目实施合规进展与不可抗力备忘录`,
        ],
      },
      {
        action_type: '中国信保出险事前留痕通报',
        deadlineTag: '30日除斥期内',
        document_template_title: '《海外投资/承包工程险可能损失正式通知书 (Notice of Loss)》',
        keyPoints: [
          '向中国出口信用保险公司提交正式书面《可能损失通知书》锁定保全利益',
          '提交东道国发包人迟延提供工作面与突击索兑保函威胁证据链',
        ],
      },
    ],
  };
}
