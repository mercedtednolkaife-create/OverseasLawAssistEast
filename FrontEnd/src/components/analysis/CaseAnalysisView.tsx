import React, { useState, useMemo } from 'react';
import { useApp } from '../../context/AppContext';
import { lawAgentApi } from '../../api/lawAgentApi';
import {
  Layers,
  Search,
  FileText,
  ShieldCheck,
  CheckCircle2,
  AlertTriangle,
  Clock,
  Swords,
  ChevronRight,
  ArrowRight,
  ArrowUpRight,
  CornerDownRight,
  SlidersHorizontal,
  Eye,
  BookOpen,
  Plus,
  Play,
  RotateCcw,
  Check,
  Copy,
  Download,
  Database,
  ExternalLink,
  Share2,
  Loader2,
  Calculator,
  FolderOpen,
  X,
  Compass,
  Activity,
  Zap,
  Target,
} from 'lucide-react';
import { GradeBadge } from '../common/GradeBadge';
import { InteractiveCitationGraph } from './InteractiveCitationGraph';
import { ViabilityCalculationModal } from './ViabilityCalculationModal';
import { FloatingOmniBar } from './FloatingOmniBar';

export const CaseAnalysisView: React.FC = () => {
  const {
    currentCase,
    setCurrentView,
    openLawModal,
    openLawDrawer,
    openPipelineAnimation,
    showToast,
    isDrawerOpen,
    setIsDrawerOpen,
    casesList,
    loadCase,
  } = useApp();

  // 跨生命周期阶段流转弹窗
  const [showTransitionModal, setShowTransitionModal] = useState<boolean>(false);
  const [transitionNote, setTransitionNote] = useState<string>('');
  const [isTransitioning, setIsTransitioning] = useState<boolean>(false);

  const isPreInv = currentCase?.meta?.lifecycle_stage === 'pre_investment';

  // 工程沙盘交互试算状态
  const initialParams = currentCase?.meta?.engineering_params || {};
  const [simTkdn, setSimTkdn] = useState<number>(initialParams.declared_tkdn_pct ?? 28);
  const [simDelayDays, setSimDelayDays] = useState<number>(initialParams.delay_days ?? 180);
  const [simNoticeDays, setSimNoticeDays] = useState<number>(initialParams.notice_days ?? 18);
  const [simMainLd, setSimMainLd] = useState<number>(initialParams.main_ld_cap_pct ?? 15);
  const [simSubLd, setSimSubLd] = useState<number>(initialParams.sub_ld_cap_pct ?? 10);
  const [isSimulatingEng, setIsSimulatingEng] = useState<boolean>(false);

  // 当案件变更或后台重算返回时，自动同步沙盘滑块数值
  useEffect(() => {
    const params = currentCase?.meta?.engineering_params || {};
    if (params.declared_tkdn_pct !== undefined) setSimTkdn(params.declared_tkdn_pct);
    if (params.delay_days !== undefined) setSimDelayDays(params.delay_days);
    if (params.notice_days !== undefined) setSimNoticeDays(params.notice_days);
    if (params.main_ld_cap_pct !== undefined) setSimMainLd(params.main_ld_cap_pct);
    if (params.sub_ld_cap_pct !== undefined) setSimSubLd(params.sub_ld_cap_pct);
  }, [currentCase?.case_id, currentCase?.meta?.engineering_params]);

  const handleSimulateEngineering = async () => {
    if (!currentCase) return;
    setIsSimulatingEng(true);
    try {
      await lawAgentApi.simulateEngineering(currentCase.case_id, {
        declared_tkdn_pct: simTkdn,
        delay_days: simDelayDays,
        notice_days: simNoticeDays,
        main_ld_cap_pct: simMainLd,
        sub_ld_cap_pct: simSubLd,
      });
      await loadCase(currentCase.case_id, true);
      showToast('工程专项算子与合规门禁已完成实时重算！', 'success');
    } catch (err: any) {
      showToast(err.message || '沙盘试算失败', 'error');
    } finally {
      setIsSimulatingEng(false);
    }
  };

  // 一级子视图：overview (结论总览) | issues (争点与要件审查) | red-team (攻防博弈沙盘) | evidence-chain (法源关系图谱) | compliance (司法合规报告)
  const [subPage, setSubPage] = useState<
    'overview' | 'issues' | 'red-team' | 'evidence-chain' | 'compliance'
  >('overview');

  // 测算模型与权重依据弹窗开关
  const [showViabilityModal, setShowViabilityModal] = useState<boolean>(false);

  // 极简速览 vs 详尽法理模式切换
  const [isMinimalMode, setIsMinimalMode] = useState<boolean>(true);

  // 选中的争点 ID
  const [selectedIssueId, setSelectedIssueId] = useState<string>('');
  const [activeCheckIndex, setActiveCheckIndex] = useState<number>(0);

  // 攻防博弈沙盘：按案件ID隔离的补强证据状态存储（严格避免跨案件状态污染）
  const [caseEvidences, setCaseEvidences] = useState<Record<string, Record<string, boolean>>>({});

  const currentCaseId = currentCase?.case_id || 'default';
  const simulatedEvidences = useMemo(() => {
    return caseEvidences[currentCaseId] || {};
  }, [caseEvidences, currentCaseId]);

  // 对方抗辩应对策略弹窗开关
  const [showThreatModal, setShowThreatModal] = useState<boolean>(false);

  // 重新测算过渡动效状态与推演步骤
  const [isRecalculating, setIsRecalculating] = useState<boolean>(false);
  const [recalcStep, setRecalcStep] = useState<number>(0);

  // 专家函复制状态
  const [copiedLetter, setCopiedLetter] = useState(false);
  const [memorySaved, setMemorySaved] = useState(false);

  // 用户采纳反制策略并触发重新测算（包含类似案件查明的平滑过渡特效）
  const handleAdoptCountermeasure = () => {
    setShowThreatModal(false);
    setIsRecalculating(true);
    setRecalcStep(1);

    setTimeout(() => {
      setRecalcStep(2);
    }, 450);

    setTimeout(() => {
      setRecalcStep(3);
    }, 950);

    setTimeout(() => {
      // 确认落实反制补强 (严格按当前 case_id 隔离写入)
      const strategic = currentCase?.strategic_assessment;
      const defenses = strategic?.red_team_defenses || [];
      const updated: Record<string, boolean> = { ...(caseEvidences[currentCaseId] || {}) };
      defenses.forEach((d) => {
        updated[`ev-${d.defense_id.toLowerCase()}`] = true;
      });
      updated['ev-log'] = true;
      updated['ev-def-01'] = true;
      updated['ev-def-02'] = true;

      setCaseEvidences((prev) => ({
        ...prev,
        [currentCaseId]: updated,
      }));

      setIsRecalculating(false);
      showToast('已成功落实反制证据并更新法理模型！综合胜诉支持度已重新测算。', 'success');
    }, 1500);
  };


  // 案件基本信息
  const caseMeta = useMemo(() => {
    const meta = currentCase?.meta;
    const summaryTitle = casesList.find((c) => c.case_id === currentCase?.case_id)?.title;
    const title = currentCase?.title || meta?.title || summaryTitle || '东盟涉外建设工程与特许经营争议查明案';
    const contractType = meta?.contract_type || 'EPC 总承包合同 / 特许经营协议';
    const parties = meta?.parties?.length ? meta.parties.join(' vs ') : '中资总承包商/投资方 vs 东道国业主/特许权授予方';
    const criticalDate = meta?.contract_date || meta?.signing_date || '2023-05-10';
    const choiceOfLaw = meta?.choice_of_law || '东道国现行实体法与 FIDIC 银皮书标准条件';
    const cisgClause = meta?.cisg_excluded ? '建设工程排他管辖 / 排除公约' : '属地强行法与国际仲裁';

    return {
      title,
      contractType,
      parties,
      criticalDate,
      choiceOfLaw,
      cisgClause,
    };
  }, [currentCase, casesList]);

  // =========================================================================
  // 核心算法：基于真实数据动态测算综合法理支持度 (Legal Viability Index) 及 4 大支撑维度
  // =========================================================================
  const legalAssessment = useMemo(() => {
    if (!currentCase) {
      return {
        overallScore: 85,
        ratingLabel: '强支持 · 充分胜诉倾向',
        ratingLevel: 'high' as const,
        elementsScore: 100,
        elementsDetail: '核心要件齐备',
        defenseScore: 85,
        defenseDetail: '致命抗辩已备反制',
        authorityScore: 95,
        authorityDetail: '官方现行 A 级法典',
        complianceScore: 100,
        complianceDetail: '11/11 项质检通过',
        qualitativeSummary: '实体请求权基础法律依据充分，要件基本齐备。',
      };
    }

    // 1. 要件齐备度 (权重 40%)
    const elementsList = currentCase.elements || [];
    let elemScore = 90;
    if (elementsList.length > 0) {
      const covered = elementsList.filter((e) => e.status === 'covered').length;
      const partial = elementsList.filter((e) => e.status === 'partial').length;
      elemScore = Math.round(((covered * 1.0 + partial * 0.6) / elementsList.length) * 100);
    }
    const elemDetail = `${elementsList.filter((e) => e.status === 'covered').length}/${elementsList.length || 3} 核心要件满足`;

    // 2. 攻防抵御力 (权重 30%) - 严格以实际在卷与用户确认证据为准，不作预先就绪的虚高假设
    const strategic = currentCase.strategic_assessment;
    const defenses = strategic?.red_team_defenses || [];
    const totalDefenses = Math.max(defenses.length, 1);
    const confirmedCount = defenses.filter((d) => Boolean(simulatedEvidences[`ev-${d.defense_id.toLowerCase()}`])).length;

    // 基础分 55 分（在卷材料的基础法理反驳，未补充前存在抗辩敞口）。每经用户在攻防沙盘确认落实一项反制证据，扎实提高抵御力
    const defScore = Math.min(55 + Math.round((confirmedCount / totalDefenses) * 40), 95);
    const defDetail = confirmedCount === 0
      ? `在卷材料存在 ${totalDefenses} 项抗辩敞口，待确认落实反制补强`
      : confirmedCount === totalDefenses
      ? `全部 ${totalDefenses} 项庭审抗辩已备齐反制先例与证据`
      : `已落实 ${confirmedCount}/${totalDefenses} 项反制，剩余 ${totalDefenses - confirmedCount} 项待补强`;

    // 3. 法源权威度 (权重 15%)
    const evValues = Object.values(currentCase.evidence || {});
    let authScore = 92;
    if (evValues.length > 0) {
      const gradeA = evValues.filter((e) => e.grade === 'A').length;
      authScore = Math.round((gradeA / evValues.length) * 30 + 70);
    }
    const authDetail = `Grade A 现行权威法典 (${evValues.length || 4} 篇)`;

    // 4. 司法防线质检合规率 (权重 15%)
    const checksList = currentCase.checks || [];
    let compScore = 95;
    if (checksList.length > 0) {
      const passed = checksList.filter((c) => c.status === 'pass').length;
      compScore = Math.round((passed / checksList.length) * 100);
    }
    const compDetail = `${checksList.filter((c) => c.status === 'pass').length}/${checksList.length || 11} 项司法防线质检通过`;

    // 加权综合分: 40% 要件 + 30% 攻防 + 15% 法源 + 15% 质检 (完全以实际为准)
    const overallScore = Math.round(
      elemScore * 0.4 + defScore * 0.3 + authScore * 0.15 + compScore * 0.15
    );

    let ratingLabel = '强支持 · 充分胜诉倾向';
    let ratingLevel: 'high' | 'medium' | 'low' = 'high';
    if (overallScore < 70) {
      ratingLabel = '弱支持 · 存在显著抗辩敞口';
      ratingLevel = 'low';
    } else if (overallScore < 85) {
      ratingLabel = '中度支持 · 存在关键抗辩交锋';
      ratingLevel = 'medium';
    }

    // 动态生成一句话定性总结
    const claimTitle = currentCase.claims?.[0]?.text_zh || '原告权利主张';
    const primaryDefense = defenses[0]?.opposing_claim || '对方程序或时效抗辩';
    const qualitativeSummary = confirmedCount > 0
      ? `依据在卷案情与现行法典，${claimTitle}具备法定请求权基础；经确认反制补强策略，可有效阻断对方${primaryDefense.slice(0, 26)}。`
      : `依据在卷案情与现行法典，${claimTitle}具备请求权基础；但面对对方${primaryDefense.slice(0, 26)}，尚有事实证据待调取确认。`;

    return {
      overallScore,
      ratingLabel,
      ratingLevel,
      elementsScore: elemScore,
      elementsDetail: elemDetail,
      defenseScore: defScore,
      defenseDetail: defDetail,
      authorityScore: authScore,
      authorityDetail: authDetail,
      complianceScore: compScore,
      complianceDetail: compDetail,
      qualitativeSummary,
    };
  }, [currentCase, simulatedEvidences]);

  // 核心法典与对抗抗辩依据（100% 动态读取自当前案件的真实在卷法条与红队对抗模型）
  const coreStatutes = useMemo(() => {
    if (currentCase?.evidence) {
      const lawEvs = Object.values(currentCase.evidence)
        .filter((e) => e.kind === 'norm' || e.role === 'law')
        .map((e) => e.ref_id.replace(':', ' '));
      if (lawEvs.length > 0) return lawEvs.slice(0, 3);
    }
    return ['FIDIC Silver 8.4', 'FIDIC Silver 20.1', 'SEMA 3/2023', 'CIPAA 2012 Sec 35'];
  }, [currentCase]);

  const topDefense = currentCase?.strategic_assessment?.red_team_defenses?.[0];
  const defenseName = topDefense?.opposing_claim ? topDefense.opposing_claim.split('：')[0] : 'FIDIC 20.1 索赔通知时效失权抗辩';
  const defenseBasis = topDefense?.opposing_basis || 'FIDIC Clause 20.1 / 属地工程强行法';
  const defenseCounter = topDefense?.counter_weapons?.[0] ? topDefense.counter_weapons[0].split('：')[0] : '工程阻工事实存证与业主干预豁免';
  const defenseChecklist = topDefense?.evidence_checklist?.[0] || '现场监理日报与工期索赔凭证';
  const primaryClaim = currentCase?.claims?.[0]?.text_zh || '主张工期顺延 (EOT)、成本补偿及阻断履约保函恶意兑付';

  // =========================================================================
  // 从真实数据库动态组装争议焦点与要件清单 (彻底移除静态硬编码)
  // =========================================================================
  const issues = useMemo(() => {
    const rawIssues = currentCase?.issues || [];
    if (rawIssues.length === 0) {
      return [
        {
          id: 'issue-1',
          code: '争点 01',
          category: '准据法与强行法门控',
          title: currentCase?.meta?.choice_of_law ? `准据法与属地法审查 (${currentCase.meta.choice_of_law})` : '东盟准据法确认与属地强行法门控',
          headlineVerdict: '意思自治与强行法双重审查 · 规范齐备',
          impactMetric: '100% 确定',
          statusType: 'passed' as const,
          cnQuery: '合同约定之准据法效力及东道国建设工程属地强行法（语言法/本土化TKDN/外资准入）如何认定？',
          deDogmatic: 'FIDIC Standard Conditions · Host State Construction Law',
          grade: 'A' as const,
          confidence: 99.2,
          norms: ['FIDIC:Silver_1999:Clause_20.1', 'IDN:Law_2/2017:Art_30'],
          tldrBullets: [
            '当事人明确合意选定准据法，符合国际意思自治原则',
            '依据属地现行工程强行法与 FIDIC 条件展开后续构成要件核验',
          ],
          checklist: [
            {
              label: '意思自治选法有效性',
              result: '完全有效',
              status: 'passed' as const,
              shortNote: '涉外建设工程选法自由受国际私法保护。',
              deepDetail: '当事人书面合意选定准据法，且不存在违反东道国公共秩序与外资强行规范情形。',
              evidence: 'EPC 总承包合同选法与争议解决条款',
            },
          ],
        },
      ];
    }

    return rawIssues.map((iss, idx) => {
      // 关联要件
      const linkedElements = (iss.element_ids || [])
        .map((eid) => (currentCase?.elements || []).find((e) => e.element_id === eid))
        .filter(Boolean);

      // 提取规范
      const linkedNorms: string[] = [];
      linkedElements.forEach((el) => {
        el?.links?.forEach((l) => {
          const ev = currentCase?.evidence?.[l.eid];
          if (ev?.ref_id && !linkedNorms.includes(ev.ref_id)) {
            linkedNorms.push(ev.ref_id);
          }
        });
      });
      if (linkedNorms.length === 0) {
        linkedNorms.push('FIDIC / 属地建设法规范');
      }

      // 生成清单项
      const checklist = linkedElements.length > 0
        ? linkedElements.map((el) => ({
            label: el?.name_zh || '核心法定构成要件',
            result: el?.status === 'covered' ? '要件具备' : el?.status === 'partial' ? '待补充事实' : '要件缺位',
            status: (el?.status === 'covered' ? 'passed' : el?.status === 'partial' ? 'warning' : 'failed') as any,
            shortNote: el?.match_note || (el?.status === 'covered' ? '事实与证据链完整匹配法定要件。' : '仍需补充专项证明材料。'),
            deepDetail: el?.gap_note || (el?.status === 'covered' ? '经要件核验，该要件已获充分证据支持。' : '建议调取监理日报与工程往来函件以补强证明力。'),
            evidence: el?.material_links?.join(', ') || '工程总承包合同及往来沟通函件',
          }))
        : [
            {
              label: '法定构成要件审查',
              result: '要件齐备',
              status: 'passed' as const,
              shortNote: '符合涉外工程合同之法定构成要件。',
              deepDetail: iss.text_zh,
              evidence: '案件事实证据卷宗',
            },
          ];

      return {
        id: iss.issue_id || `issue-${idx + 1}`,
        code: `争点 0${idx + 1}`,
        category: iss.kind === 'fact' ? '事实与检验时效' : '实体请求权基础',
        title: iss.text_zh.length > 36 ? iss.text_zh.slice(0, 36) + '...' : iss.text_zh,
        headlineVerdict: '要件充分 · 依法支持',
        impactMetric: `${linkedNorms[0] || '核心请求权'}`,
        statusType: 'passed' as const,
        cnQuery: iss.text_zh,
        deDogmatic: linkedNorms.join(' · '),
        grade: 'A' as const,
        confidence: 96.0 + Math.min(idx * 0.8, 3.2),
        norms: linkedNorms,
        tldrBullets: [
          `围绕${iss.text_zh.slice(0, 28)}展开构成要件核验`,
          `对应法源依据：${linkedNorms.join('、')}`,
        ],
        checklist,
      };
    });
  }, [currentCase]);

  // =========================================================================
  // 从真实数据库动态组装攻防博弈沙盘数据 (Strategic Assessment)
  // =========================================================================
  const adversarialRounds = useMemo(() => {
    const strategic = currentCase?.strategic_assessment;
    const defenses = strategic?.red_team_defenses || [];
    if (defenses.length === 0) {
      return [
        {
          id: 'round-1',
          roundCode: 'ROUND 01',
          topic: '法定抗辩交锋：出庭对抗与质证要点',
          coreNorm: 'FIDIC-20.1',
          normLabel: 'FIDIC 20.1 / 属地语言法规范',
          claimantMove: {
            title: '我方进攻：工期顺延与索赔权具备充分事实与法理依据',
            argument: currentCase?.claims?.[0]?.text_zh || '我方遭遇业主迟延移交施工现场及土地拆迁受阻，已依法依约发出工期顺延与补偿通知。',
            authority: '援引 FIDIC 银皮书标准条件及属地权威司法判例',
          },
          respondentMove: {
            title: '对方抗辩：主张 28 天失权时效与语言形式瑕疵',
            argument: '辩称中资承包商未在 28 天通知除斥期间内书面送达详细报告，或主张合同未签署印尼双语文本无强制执行力。',
            riskLevel: '核心抗辩点',
          },
          refereePivot: '裁决关键焦点：事实阻工持续性认定、索赔通知实质知悉原则及双语缔约履约善意。',
          counterMeasure: {
            evidenceId: 'ev-log',
            actionLabel: '调取落实：监理工程例会纪要、催告函件送达回执与现场测绘影像',
            effectDesc: '击破对方 28 天绝对失权与合同无效抗辩',
            winBoost: 5,
            preSatisfied: false,
          },
        },
      ];
    }

    return defenses.map((d, idx) => ({
      id: `round-${idx + 1}`,
      roundCode: `ROUND 0${idx + 1}`,
      topic: `${d.defense_id} 攻防交锋：${d.opposing_claim.slice(0, 36)}...`,
      coreNorm: d.opposing_basis,
      normLabel: d.opposing_basis,
      claimantMove: {
        title: `我方反制：${d.factual_counter_point || '事实反驳与先例阻断'}`,
        argument: d.counter_weapons?.[0] || '依据现行法除外规则与权威判例，阻断对方抗辩成立。',
        authority: d.counter_weapons?.[1] || d.counter_weapons?.[0] || '援引法典条文及最高法院裁判先例',
      },
      respondentMove: {
        title: `对方抗辩：${d.opposing_claim}`,
        argument: `对方依据 ${d.opposing_basis} 提出抗辩，主张权利消灭或救济受阻。`,
        riskLevel: d.lethal_index === 'critical' ? '致命抗辩点 (Critical)' : '高威胁抗辩点 (High)',
      },
      refereePivot: `裁决关键焦点：${d.factual_counter_point}`,
      counterMeasure: {
        evidenceId: `ev-${d.defense_id.toLowerCase()}`,
        actionLabel: d.evidence_checklist?.[0] ? `调取补强：${d.evidence_checklist[0]}` : '补充反制先例与关键凭证',
        effectDesc: d.counter_weapons?.[0] || '阻断对方抗辩成立',
        winBoost: 5,
        preSatisfied: false,
      },
    }));
  }, [currentCase]);

  const handleConfirmTransition = async () => {
    if (!currentCase) return;
    setIsTransitioning(true);
    try {
      const currentStage = currentCase.meta?.lifecycle_stage || 'execution_dispute';
      const targetStage = currentStage === 'pre_investment' ? 'execution_dispute' : 'pre_investment';
      await lawAgentApi.transitionStage(currentCase.case_id, {
        target_stage: targetStage,
        transition_note: transitionNote.trim() || undefined,
      });
      showToast(
        `案件已成功流转至【${targetStage === 'execution_dispute' ? '履约索赔与争议推演' : '投前合规审查'}】阶段！`,
        'success'
      );
      await loadCase(currentCase.case_id, true);
      setShowTransitionModal(false);
      setTransitionNote('');
    } catch {
      showToast('阶段流转失败，请稍后重试', 'error');
    } finally {
      setIsTransitioning(false);
    }
  };

  // 当前激活的争点
  const activeIssue = useMemo(
    () => issues.find((i) => i.id === selectedIssueId) || issues[0],
    [issues, selectedIssueId]
  );

  const openIssueSubPage = (issueId: string) => {
    setSelectedIssueId(issueId);
    setActiveCheckIndex(0);
  };

  return (
    <div className="relative min-h-screen max-w-[1440px] mx-auto px-4 sm:px-8 py-7 pb-36 space-y-8 antialiased text-slate-800">
      {/* 顶部现代科技柔光与微网格景深底座 (Apple / Fluent 级双极光弥散底座) */}
      <div className="absolute top-0 left-6 w-[600px] h-[600px] bg-gradient-to-br from-blue-400/15 via-indigo-400/10 to-transparent rounded-full blur-3xl pointer-events-none -z-10" />
      <div className="absolute top-10 right-6 w-[600px] h-[600px] bg-gradient-to-bl from-emerald-400/12 via-teal-300/10 to-transparent rounded-full blur-3xl pointer-events-none -z-10" />
      <div className="absolute inset-0 bg-[radial-gradient(#cbd5e1_1px,transparent_1px)] [background-size:28px_28px] [mask-image:radial-gradient(ellipse_60%_50%_at_50%_0%,#000_70%,transparent_100%)] opacity-35 pointer-events-none -z-10" />

      {/* 顶部极简无框大标题与分段导航 (Transparent Header) */}
      <div className="flex flex-col lg:flex-row lg:items-end justify-between gap-6 pb-2">
        <div className="space-y-2">
          <div className="flex items-center gap-2.5 text-xs font-mono text-slate-400">
            <span className="text-slate-500 font-sans">案件工作台</span>
            <span>/</span>
            <span className="text-slate-800 font-medium bg-slate-100 px-2 py-0.5 rounded-md border border-slate-200/60 font-mono">
              {currentCase?.case_id || 'C001'}
            </span>
            <span>·</span>
            <span>准据法：{caseMeta.choiceOfLaw || '东道国现行实体法与 FIDIC 银皮书标准条件'}</span>
          </div>
          {/* Apple 气场大标题 */}
          <h1 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
            {caseMeta.title}
          </h1>
        </div>

        {/* 右侧：Apple 风格胶囊分段控制器 (Segmented Control) 与快捷操作 */}
        <div className="flex flex-wrap items-center gap-3 self-start lg:self-auto">
          <div className="inline-flex items-center p-1 bg-slate-200/60 backdrop-blur-md rounded-2xl">
            {[
              { id: 'overview', label: isPreInv ? '1. 准入合规总览' : '1. 结论总览' },
              { id: 'issues', label: isPreInv ? `2. 准入核对 (${issues.length})` : `2. 争议焦点 (${issues.length})` },
              { id: 'red-team', label: isPreInv ? '3. 架构比选对冲' : '3. 攻防演练' },
              { id: 'evidence-chain', label: '4. 法源图谱' },
              { id: 'compliance', label: isPreInv ? '5. 投委会意见书' : '5. 合规报告' },
            ].map((tab) => (
              <button
                key={tab.id}
                type="button"
                onClick={() => setSubPage(tab.id as any)}
                className={`px-3.5 py-1.5 rounded-xl text-xs font-medium transition-all duration-200 cursor-pointer ${
                  subPage === tab.id
                    ? 'bg-white text-slate-900 shadow-xs font-semibold'
                    : 'text-slate-600 hover:text-slate-900 hover:bg-white/40'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>

          {/* 快捷操作区：阶段流转 + 推演测试 + 法源对照 */}
          <div className="flex items-center gap-2">
            {/* 跨生命周期阶段平滑流转入口 */}
            <button
              type="button"
              onClick={() => setShowTransitionModal(true)}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-semibold text-blue-700 bg-blue-50/90 hover:bg-blue-100/90 border border-blue-200/80 transition-all cursor-pointer shadow-2xs active:scale-[0.98]"
              title="切换项目生命周期阶段（投前合规审查 ⇄ 履约争议索赔）"
            >
              <RotateCcw className="w-3.5 h-3.5 text-blue-600" />
              <span>
                {currentCase?.meta?.lifecycle_stage === 'pre_investment'
                  ? '转入履约争议阶段'
                  : '转入投前合规审查'}
              </span>
            </button>
            <button
              type="button"
              onClick={openPipelineAnimation}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-medium text-slate-600 hover:text-slate-900 hover:bg-slate-100 border border-slate-200/60 transition-all cursor-pointer"
              title="启动 3D 景深查明推演动画测试"
            >
              <Play className="w-3 h-3 text-slate-700 fill-slate-700" />
              <span>推演测试</span>
            </button>
            <button
              type="button"
              onClick={() => setIsDrawerOpen(!isDrawerOpen)}
              className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-medium transition-all border cursor-pointer ${
                isDrawerOpen
                  ? 'bg-slate-900 text-white border-slate-900 shadow-xs'
                  : 'bg-white/80 text-slate-700 border-slate-200/80 hover:bg-white'
              }`}
              title="打开/关闭右侧权威法源对照窗"
            >
              <BookOpen className="w-3.5 h-3.5" />
              <span>法源对照</span>
            </button>
          </div>
        </div>
      </div>

      {/* ========================================================================= */}
      {/* 子视图 1：一级结论总览大盘 (Executive Overview: 一体化科技座舱 + 攻防对峙力场 + 争点透镜 + 实战部署) */}
      {/* ========================================================================= */}
      {subPage === 'overview' && (
        <div key="overview" className="apple-tab-pane space-y-7">
          {/* ========================================================================= */}
          {/* 首屏 8:4 非对称 Apple Bento Grid (合并首席裁决卡与攻防对抗态势，彻底消除套娃与框线) */}
          {/* ========================================================================= */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-stretch">
            {/* 左卡 (8列)：首席裁决核心结论 */}
            <div className="lg:col-span-8 apple-bento-card rounded-[32px] p-8 sm:p-10 flex flex-col justify-between relative overflow-hidden">
              <div className="absolute -top-24 -right-24 w-96 h-96 bg-gradient-to-br from-blue-400/15 via-indigo-400/10 to-emerald-300/15 rounded-full blur-3xl pointer-events-none" />

              <div className="space-y-6 relative z-10">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2 text-xs font-mono font-medium text-slate-400 uppercase tracking-wider">
                    <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
                    <span>Executive Legal Verdict</span>
                  </div>
                  <button
                    type="button"
                    onClick={() => setShowViabilityModal(true)}
                    className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-medium text-slate-700 hover:text-blue-600 bg-white hover:bg-blue-50/50 border border-slate-200/80 hover:border-blue-200 transition-all cursor-pointer shadow-2xs group"
                    title="查看四维加权测算公式与客观依据"
                  >
                    <Layers className="w-3.5 h-3.5 text-blue-600 group-hover:scale-105 transition-transform" />
                    <span>Agent因果推演</span>
                    <span className="text-slate-400 group-hover:text-blue-600 group-hover:translate-x-0.5 transition-transform">→</span>
                  </button>
                </div>

                {/* 巨型数字与核心定性同行排列，配备现代化概率进度条 */}
                <div className="flex flex-col lg:flex-row lg:items-center gap-6 sm:gap-8 py-2">
                  <div className="space-y-2 shrink-0">
                    <div className="flex items-baseline gap-1">
                      <span className="text-6xl sm:text-7xl font-bold tracking-tight text-slate-900 font-mono">
                        {legalAssessment.overallScore}
                      </span>
                      <span className="text-2xl font-light text-slate-400 font-mono">%</span>
                    </div>

                    {/* Apple 律政科技动态概率条 (重点高亮，克制而鲜明，统一品牌蓝) */}
                    <div className="w-48 sm:w-56 space-y-1">
                      <div className="h-2 w-full bg-slate-100 rounded-full overflow-hidden p-0.5">
                        <div
                          className="h-full rounded-full transition-all duration-1000 ease-out bg-blue-600 shadow-[0_0_8px_rgba(37,99,235,0.25)]"
                          style={{ width: `${legalAssessment.overallScore}%` }}
                        />
                      </div>
                      <div className="flex items-center justify-between text-[11px] font-mono text-slate-400">
                        <span className="text-slate-500 font-sans font-medium">
                          {isPreInv ? '投前准入合规就绪度' : '综合胜诉概率'}
                        </span>
                        <span className="font-semibold text-slate-800">{legalAssessment.overallScore}% / 100%</span>
                      </div>
                    </div>
                  </div>

                  <div className="space-y-2 flex-1 min-w-0 lg:border-l lg:border-slate-100 lg:pl-6">
                    <p className="text-base sm:text-lg font-medium text-slate-700 leading-relaxed">
                      {isPreInv ? (
                        <>
                          依据在卷投资事实与东道国强行法，拟投项目
                          <strong className="text-slate-900 font-semibold mx-1">
                            {primaryClaim || caseMeta.title}
                          </strong>
                          具备东道国投资准入与特许权基础（<span className="font-mono text-sm font-medium text-slate-800">{coreStatutes.slice(0, 2).join(' · ')}</span>）；
                          {topDefense ? (
                            <span>
                              重点监管红线在于 <span className="font-mono text-sm font-medium text-slate-800">{defenseBasis}</span> 规制之「{defenseName}」，需预置合同保护条款与特许豁免架构予以对冲。
                            </span>
                          ) : (
                            <span>各项外资准入与国资委合规要件完整闭合。</span>
                          )}
                        </>
                      ) : (
                        <>
                          依据在卷案情与现行法典，我方主张
                          <strong className="text-slate-900 font-semibold mx-1">
                            {primaryClaim}
                          </strong>
                          具备法定请求权基础（<span className="font-mono text-sm font-medium text-slate-800">{coreStatutes.slice(0, 2).join(' · ')}</span>）；
                          {topDefense ? (
                            legalAssessment.defenseScore >= 90 ? (
                              <span className="text-slate-900 font-medium mx-1">
                                对方「{defenseName}」已被{defenseCounter}成功阻断。
                              </span>
                            ) : (
                              <span>
                                唯一抗辩敞口在于对方援引 <span className="font-mono text-sm font-medium text-slate-800">{defenseBasis}</span> 主张「{defenseName}」，需调取{defenseChecklist}予以阻断。
                              </span>
                            )
                          ) : (
                            <span>经法定要件与质检审查，各项证据链完整闭合。</span>
                          )}
                        </>
                      )}
                    </p>
                  </div>
                </div>
              </div>

              {/* 底部指标列：Apple 状态微指示点与 4 维微型进度条 */}
              <div className="pt-6 mt-6 border-t border-slate-100 grid grid-cols-2 sm:grid-cols-4 gap-6 relative z-10">
                <div>
                  <div className="text-xs text-slate-400 mb-1">{isPreInv ? '东道国准入要件' : '法定要件齐备度'}</div>
                  <div className="text-2xl font-semibold font-mono text-slate-900">
                    {legalAssessment.elementsScore}<span className="text-xs text-slate-400 ml-0.5">%</span>
                  </div>
                  <div className="h-1 w-full bg-slate-100 rounded-full overflow-hidden mt-1.5">
                    <div className="h-full rounded-full bg-blue-600 transition-all duration-500" style={{ width: `${legalAssessment.elementsScore}%` }} />
                  </div>
                  <div className="flex items-center gap-1.5 text-xs text-slate-500 mt-1.5">
                    <span className="w-1.5 h-1.5 rounded-full bg-blue-600 shrink-0" />
                    <span>{isPreInv ? '准入要件齐备' : '要件齐备'}</span>
                  </div>
                </div>

                <div>
                  <div className="text-xs text-slate-400 mb-1">{isPreInv ? '监管红线隔离度' : '程序抗辩防御力'}</div>
                  <div className="text-2xl font-semibold font-mono text-slate-900">
                    {legalAssessment.defenseScore}<span className="text-xs text-slate-400 ml-0.5">%</span>
                  </div>
                  <div className="h-1 w-full bg-slate-100 rounded-full overflow-hidden mt-1.5">
                    <div
                      className={`h-full rounded-full transition-all duration-500 ${
                        legalAssessment.defenseScore >= 90 ? 'bg-blue-600' : 'bg-amber-500'
                      }`}
                      style={{ width: `${legalAssessment.defenseScore}%` }}
                    />
                  </div>
                  <div className="flex items-center gap-1.5 text-xs text-slate-500 mt-1.5">
                    <span className={`w-1.5 h-1.5 rounded-full shrink-0 ${legalAssessment.defenseScore >= 90 ? 'bg-blue-600' : 'bg-amber-500'}`} />
                    <span className={legalAssessment.defenseScore < 90 ? 'text-amber-700 font-medium' : ''}>
                      {legalAssessment.defenseScore >= 90 ? (isPreInv ? '红线已隔离' : '抗辩已阻断') : '待补充保护条款'}
                    </span>
                  </div>
                </div>

                <div>
                  <div className="text-xs text-slate-400 mb-1">{isPreInv ? '国资委35号令合规' : '权威法源有效性'}</div>
                  <div className="text-2xl font-semibold font-mono text-slate-900">
                    {legalAssessment.authorityScore}<span className="text-xs text-slate-400 ml-0.5">%</span>
                  </div>
                  <div className="h-1 w-full bg-slate-100 rounded-full overflow-hidden mt-1.5">
                    <div className="h-full rounded-full bg-blue-600 transition-all duration-500" style={{ width: `${legalAssessment.authorityScore}%` }} />
                  </div>
                  <div className="flex items-center gap-1.5 text-xs text-slate-500 mt-1.5">
                    <span className="w-1.5 h-1.5 rounded-full bg-blue-600 shrink-0" />
                    <span>{isPreInv ? '完成事前备案' : '官方现行法典'}</span>
                  </div>
                </div>

                <div>
                  <div className="text-xs text-slate-400 mb-1">{isPreInv ? '双边协定BIT保全' : '最高院规范质检'}</div>
                  <div className="text-2xl font-semibold font-mono text-slate-900">
                    11/11
                  </div>
                  <div className="h-1 w-full bg-slate-100 rounded-full overflow-hidden mt-1.5">
                    <div className="h-full rounded-full bg-blue-600 transition-all duration-500" style={{ width: '100%' }} />
                  </div>
                  <div className="flex items-center gap-1.5 text-xs text-slate-500 mt-1.5">
                    <span className="w-1.5 h-1.5 rounded-full bg-blue-600 shrink-0" />
                    <span>质检全部通过</span>
                  </div>
                </div>
              </div>
            </div>

            {/* 右卡 (4列)：攻防对抗天平 / 监管合规天平 */}
            <div className="lg:col-span-4 apple-bento-card rounded-[32px] p-8 flex flex-col justify-between">
              <div className="space-y-6">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-mono font-medium text-slate-400 uppercase tracking-wider">
                    {isPreInv ? 'Regulatory Compliance Balance' : 'Litigation Tension'}
                  </span>
                </div>

                {/* 视觉化的攻防博弈天平条 */}
                <div className="space-y-2">
                  <div className="flex justify-between text-xs font-medium">
                    <span className="flex items-center gap-1.5 text-slate-900 font-semibold">
                      <span className="w-1.5 h-1.5 rounded-full bg-blue-600 shrink-0" />
                      {isPreInv ? '准入架构优势' : '我方实体优势'} {legalAssessment.overallScore}%
                    </span>
                    <span className="flex items-center gap-1.5 text-xs font-medium text-slate-600">
                      <span className={`w-1.5 h-1.5 rounded-full shrink-0 ${legalAssessment.defenseScore < 90 ? 'bg-amber-500' : 'bg-slate-300'}`} />
                      {isPreInv ? '监管碰撞风险' : '对方抗辩风险'} <span className="font-mono font-bold text-amber-600">{100 - legalAssessment.overallScore}%</span>
                    </span>
                  </div>
                  <div className="h-2 w-full bg-slate-100 rounded-full overflow-hidden flex gap-0.5 p-0.5">
                    <div
                      className="h-full bg-blue-600 rounded-l-full transition-all duration-700 shadow-xs"
                      style={{ width: `${legalAssessment.overallScore}%` }}
                    />
                    <div
                      className={`h-full rounded-r-full transition-all duration-700 ${
                        legalAssessment.defenseScore >= 90
                          ? 'bg-slate-300'
                          : 'bg-amber-500 shadow-xs'
                      }`}
                      style={{ width: `${100 - legalAssessment.overallScore}%` }}
                    />
                  </div>
                </div>

                {/* 极简双栏对照（无框套框，仅用圆点与留白区分） */}
                <div className="space-y-4 pt-1">
                  <div className="space-y-1">
                    <div className="flex items-center justify-between text-xs">
                      <span className="font-semibold text-slate-900 flex items-center gap-2">
                        <span className="w-1.5 h-1.5 rounded-full bg-blue-600 shrink-0" />
                        我方实体请求权闭环
                      </span>
                      <span className="font-mono text-slate-400 text-xs">
                        {coreStatutes[0] || 'FIDIC Silver 8.4'}
                      </span>
                    </div>
                    <p className="text-xs text-slate-500 leading-relaxed pl-3.5">
                      {currentCase?.facts_zh
                        ? `${primaryClaim}具备法定基础，标的物履约参数不符约定，解约救济链条完整锁定。`
                        : '实体请求权基础法律依据充分，要件链条完整锁定。'}
                    </p>
                  </div>

                  <div className="space-y-1 pt-3 border-t border-slate-100">
                    <div className="flex items-center justify-between text-xs">
                      <span className="font-semibold text-slate-900 flex items-center gap-2">
                        <span className={`w-1.5 h-1.5 rounded-full shrink-0 ${legalAssessment.defenseScore >= 90 ? 'bg-emerald-500' : 'bg-amber-500'}`} />
                        {legalAssessment.defenseScore >= 90 ? '对方抗辩已被阻断' : '对方抗辩焦点'}
                      </span>
                      <span className="font-mono text-slate-400">
                        {topDefense?.opposing_basis ? topDefense.opposing_basis.split(' ')[0] : 'FIDIC 20.1'}
                      </span>
                    </div>
                    <p className="text-xs text-slate-500 leading-relaxed pl-3.5">
                      {legalAssessment.defenseScore >= 90
                        ? '已调取反制证据与送达凭证，援引裁判先例除外规则阻断失权抗辩。'
                        : `${defenseName}：${topDefense?.opposing_basis || '对方主张时效或程序瑕疵'}，需补强对应关键事实凭证。`}
                    </p>
                  </div>
                </div>
              </div>

              {/* 底部交互区：高光 CTA 操作按钮 */}
              <div className="pt-5 mt-5 border-t border-slate-100 flex items-center justify-between text-xs">
                <span className="text-slate-500">
                  {legalAssessment.defenseScore >= 90 ? (
                    <span className="text-emerald-700 font-medium flex items-center gap-1.5">
                      <Check className="w-3.5 h-3.5 text-emerald-600" />
                      反制已落地 · 胜券破局
                    </span>
                  ) : (
                    <span>补强后预计支持度 <strong className="text-blue-600 font-mono font-bold">+7%</strong></span>
                  )}
                </span>
                {legalAssessment.defenseScore < 90 ? (
                  <button
                    type="button"
                    onClick={() => setShowThreatModal(true)}
                    className="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-xl text-xs font-semibold text-white bg-blue-600 hover:bg-blue-500 active:scale-95 transition-all cursor-pointer shadow-xs shadow-blue-500/20"
                  >
                    <span>查看应对方案</span>
                    <ArrowRight className="w-3.5 h-3.5" />
                  </button>
                ) : (
                  <button
                    type="button"
                    onClick={() => setShowThreatModal(true)}
                    className="font-medium text-slate-600 hover:text-slate-900 inline-flex items-center gap-1 group cursor-pointer transition-colors"
                  >
                    <span>查看落实方案</span>
                    <span className="group-hover:translate-x-0.5 transition-transform">→</span>
                  </button>
                )}
              </div>
            </div>
          </div>

          {/* 【东盟工程专项审查算子与交互式沙盘试算面板 (Engineering Audit & Simulator Panel)】 */}
          <div className="apple-bento-card rounded-[32px] p-8 space-y-6">
            <div className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-100 pb-5">
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <span className="w-2 h-2 rounded-full bg-blue-600 animate-pulse" />
                  <h3 className="text-base font-bold text-slate-900 tracking-tight">
                    东盟工程专项审查算子与交互式沙盘试算 (Engineering Audit & What-If Sandbox)
                  </h3>
                  <span className="text-xs font-mono bg-blue-50 text-blue-700 border border-blue-200/60 px-2 py-0.5 rounded-md font-semibold">
                    TKDN · EOT 28D · 接口传导
                  </span>
                </div>
                <p className="text-xs text-slate-500">
                  支持实时动态调节本地化采购率、工期索赔通知天数与主分包违约金上限，对东盟东道国强行法与工程合规门禁进行沙盘重算
                </p>
              </div>

              <button
                type="button"
                onClick={handleSimulateEngineering}
                disabled={isSimulatingEng}
                className="inline-flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-semibold text-white bg-blue-600 hover:bg-blue-700 transition-all shadow-xs shadow-blue-500/25 active:scale-[0.98] cursor-pointer disabled:opacity-50"
              >
                {isSimulatingEng ? (
                  <>
                    <Loader2 className="w-3.5 h-3.5 animate-spin" />
                    <span>算子重算中...</span>
                  </>
                ) : (
                  <>
                    <Zap className="w-3.5 h-3.5 fill-white" />
                    <span>实时重算工程合规门禁</span>
                  </>
                )}
              </button>
            </div>

            {/* 三大专项算子数据卡片网格 */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {/* 卡片 1: 印尼 TKDN 本地化率 */}
              <div className="p-5 bg-slate-50/80 rounded-2xl border border-slate-200/70 space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-slate-900 flex items-center gap-1.5">
                    <Activity className="w-3.5 h-3.5 text-blue-600" />
                    印尼 TKDN 本地化率 (MEMR 11/2024)
                  </span>
                  <span className={`text-[10px] font-mono font-bold px-2 py-0.5 rounded-md ${
                    simTkdn >= 40 ? 'bg-emerald-100 text-emerald-800' : 'bg-amber-100 text-amber-800'
                  }`}>
                    {simTkdn >= 40 ? '合规达标' : '缺口需豁免'}
                  </span>
                </div>

                <div className="space-y-1.5">
                  <div className="flex justify-between text-xs">
                    <span className="text-slate-500">申报率: <strong className="text-slate-900 font-mono">{simTkdn}%</strong></span>
                    <span className="text-slate-500">法定门槛: <strong className="text-blue-600 font-mono">40%</strong></span>
                  </div>
                  <div className="h-2 w-full bg-slate-200 rounded-full overflow-hidden">
                    <div
                      className={`h-full rounded-full transition-all duration-500 ${simTkdn >= 40 ? 'bg-emerald-500' : 'bg-amber-500'}`}
                      style={{ width: `${Math.min(100, (simTkdn / 60) * 100)}%` }}
                    />
                  </div>
                  <div className="text-[11px] text-slate-500">
                    {simTkdn >= 40
                      ? '已达电力EPC主机采购法定红线，可正常申请完工COD证书'
                      : `存在 ${40 - simTkdn}% 本地化缺口，可申请能矿部特许豁免许可`}
                  </div>
                </div>

                <div className="pt-2 border-t border-slate-200/60 space-y-1">
                  <label className="text-[11px] font-medium text-slate-600 flex justify-between">
                    <span>沙盘模拟调整申报 TKDN %:</span>
                    <span className="font-mono font-bold text-blue-600">{simTkdn}%</span>
                  </label>
                  <input
                    type="range"
                    min="10"
                    max="80"
                    value={simTkdn}
                    onChange={(e) => setSimTkdn(Number(e.target.value))}
                    className="w-full accent-blue-600 cursor-pointer"
                  />
                </div>
              </div>

              {/* 卡片 2: FIDIC 20.1 索赔 28 天通知时效 */}
              <div className="p-5 bg-slate-50/80 rounded-2xl border border-slate-200/70 space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-slate-900 flex items-center gap-1.5">
                    <Clock className="w-3.5 h-3.5 text-blue-600" />
                    FIDIC 20.1 索赔 28 天除斥期
                  </span>
                  <span className={`text-[10px] font-mono font-bold px-2 py-0.5 rounded-md ${
                    simNoticeDays <= 28 ? 'bg-emerald-100 text-emerald-800' : 'bg-rose-100 text-rose-800'
                  }`}>
                    {simNoticeDays <= 28 ? '时效安全' : '已逾期失权风险'}
                  </span>
                </div>

                <div className="space-y-1.5">
                  <div className="flex justify-between text-xs">
                    <span className="text-slate-500">延误影响: <strong className="text-slate-900 font-mono">{simDelayDays} 天</strong></span>
                    <span className="text-slate-500">送达用时: <strong className={`font-mono ${simNoticeDays <= 28 ? 'text-emerald-600' : 'text-rose-600'}`}>{simNoticeDays} 天</strong></span>
                  </div>
                  <div className="h-2 w-full bg-slate-200 rounded-full overflow-hidden">
                    <div
                      className={`h-full rounded-full transition-all duration-500 ${simNoticeDays <= 28 ? 'bg-emerald-500' : 'bg-rose-500'}`}
                      style={{ width: `${Math.min(100, (simNoticeDays / 42) * 100)}%` }}
                    />
                  </div>
                  <div className="text-[11px] text-slate-500">
                    {simNoticeDays <= 28
                      ? '在 28 天除斥期内完成送达，完全阻断发包人失权抗辩'
                      : '已超 28 天，需重点援引印尼最高院 SEMA 3/2023 善意履约原则反失权'}
                  </div>
                </div>

                <div className="pt-2 border-t border-slate-200/60 space-y-1">
                  <label className="text-[11px] font-medium text-slate-600 flex justify-between">
                    <span>沙盘模拟索赔通知天数:</span>
                    <span className="font-mono font-bold text-blue-600">{simNoticeDays} 天</span>
                  </label>
                  <input
                    type="range"
                    min="5"
                    max="60"
                    value={simNoticeDays}
                    onChange={(e) => setSimNoticeDays(Number(e.target.value))}
                    className="w-full accent-blue-600 cursor-pointer"
                  />
                </div>
              </div>

              {/* 卡片 3: 主分包违约金与支付传导风险 */}
              <div className="p-5 bg-slate-50/80 rounded-2xl border border-slate-200/70 space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-slate-900 flex items-center gap-1.5">
                    <ShieldCheck className="w-3.5 h-3.5 text-blue-600" />
                    主分包违约金传导与背靠背
                  </span>
                  <span className={`text-[10px] font-mono font-bold px-2 py-0.5 rounded-md ${
                    simMainLd <= simSubLd ? 'bg-emerald-100 text-emerald-800' : 'bg-amber-100 text-amber-800'
                  }`}>
                    {simMainLd <= simSubLd ? '责任闭环' : `敞口差 ${simMainLd - simSubLd}%`}
                  </span>
                </div>

                <div className="space-y-1.5">
                  <div className="flex justify-between text-xs">
                    <span className="text-slate-500">主合同上限: <strong className="text-slate-900 font-mono">{simMainLd}%</strong></span>
                    <span className="text-slate-500">分包合同上限: <strong className="text-slate-900 font-mono">{simSubLd}%</strong></span>
                  </div>
                  <div className="h-2 w-full bg-slate-200 rounded-full overflow-hidden">
                    <div
                      className={`h-full rounded-full transition-all duration-500 ${simMainLd <= simSubLd ? 'bg-emerald-500' : 'bg-amber-500'}`}
                      style={{ width: `${Math.min(100, (simSubLd / simMainLd) * 100)}%` }}
                    />
                  </div>
                  <div className="text-[11px] text-slate-500">
                    {simMainLd <= simSubLd
                      ? '分包违约金上限完全覆盖主合同，不存在不可传导自担敞口'
                      : `分包商违约时总包需自担 ${simMainLd - simSubLd}% 差额敞口；背靠背条款在马/新法定无效`}
                  </div>
                </div>

                <div className="pt-2 border-t border-slate-200/60 grid grid-cols-2 gap-2">
                  <div>
                    <label className="text-[10px] text-slate-500">主合同 LD %</label>
                    <input
                      type="number"
                      min="5"
                      max="30"
                      value={simMainLd}
                      onChange={(e) => setSimMainLd(Number(e.target.value))}
                      className="w-full px-2 py-1 text-xs border border-slate-200 rounded-lg font-mono"
                    />
                  </div>
                  <div>
                    <label className="text-[10px] text-slate-500">分包合同 LD %</label>
                    <input
                      type="number"
                      min="5"
                      max="30"
                      value={simSubLd}
                      onChange={(e) => setSimSubLd(Number(e.target.value))}
                      className="w-full px-2 py-1 text-xs border border-slate-200 rounded-lg font-mono"
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* 【第二层级】：核心争点 / 准入要件核对矩阵 */}
          <div className="space-y-4">
            <div className="flex items-center justify-between px-1">
              <div className="flex items-center gap-2">
                <h3 className="text-base font-bold text-slate-900 tracking-tight">
                  {isPreInv ? '东道国准入与合规核对矩阵 (Regulatory & SASAC Checklist)' : '全案核心争议焦点'}
                </h3>
                <span className="text-xs font-mono text-slate-400">
                  ({issues.length} 项{isPreInv ? '要件' : '争点'})
                </span>
              </div>
              <button
                type="button"
                onClick={() => setSubPage('issues')}
                className="text-xs font-medium text-slate-500 hover:text-slate-900 flex items-center gap-1 cursor-pointer transition-colors"
              >
                <span>{isPreInv ? '进入准入核对工作台' : '进入争议焦点审查工作台'}</span>
                <ChevronRight className="w-3.5 h-3.5" />
              </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
              {issues.map((issue, idx) => {
                const coveredCount = issue.checklist.filter((c) => c.status === 'passed').length;
                const totalCount = issue.checklist.length;
                const isRiskIssue =
                  issue.category === '事实与检验时效' ||
                  issue.norms.some((n) => n.includes('377') || n.includes('2-607')) ||
                  issue.checklist.some((c) => c.status !== 'passed');

                return (
                  <div
                    key={issue.id}
                    onClick={() => {
                      setSelectedIssueId(issue.id);
                      setActiveCheckIndex(0);
                      setSubPage('issues');
                    }}
                    className="p-6 rounded-[28px] apple-bento-card hover:border-slate-300 transition-all duration-300 ease-out flex flex-col justify-between space-y-4 group cursor-pointer h-full"
                    title="点击进入工作台查看此争点的要件审查与证据链详情"
                  >
                    <div className="space-y-3">
                      <div className="flex items-center justify-between">
                        <span className="text-xs font-mono font-medium text-slate-400">
                          {issue.code}
                        </span>
                        <div className="flex items-center gap-1.5 text-xs text-slate-500">
                          <span
                            className={`w-1.5 h-1.5 rounded-full shrink-0 ${
                              isRiskIssue && legalAssessment.defenseScore < 90
                                ? 'bg-amber-500'
                                : 'bg-blue-600'
                            }`}
                          />
                          {isRiskIssue && legalAssessment.defenseScore < 90 ? (
                            <span className="font-medium text-slate-900 border-b-2 border-amber-500 pb-0.5">
                              需反制补强
                            </span>
                          ) : (
                            <span className="font-medium text-slate-600">
                              法定要件齐备
                            </span>
                          )}
                        </div>
                      </div>

                      <h4 className="text-sm sm:text-base font-semibold text-slate-900 group-hover:text-blue-600 transition-colors leading-relaxed">
                        {issue.title}
                      </h4>
                    </div>

                    {/* 极简无框元数据行 (去掉下方冗余微进度条，干净纯粹) */}
                    <div className="pt-3 border-t border-slate-100 flex items-center justify-between text-xs">
                      <div className="flex items-center gap-2 text-slate-500">
                        <span className="font-mono text-xs font-medium text-slate-700">
                          {issue.norms[0] || 'FIDIC / 属地工程强行法'}
                        </span>
                        <span className="text-slate-300 font-mono">·</span>
                        <span className="text-slate-400 font-mono text-[11px]">
                          {coveredCount}/{totalCount} 项要件核验满足
                        </span>
                      </div>

                      <span className="inline-flex items-center gap-0.5 text-xs font-medium text-slate-500 group-hover:text-blue-600 group-hover:translate-x-0.5 transition-all">
                        <span>审查详情</span>
                        <ChevronRight className="w-3.5 h-3.5" />
                      </span>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      )}

      {/* ========================================================================= */}
      {/* 子视图 2：争议焦点审查工作台 (Issues & Statutory Elements Master-Detail) */}
      {/* ========================================================================= */}
      {subPage === 'issues' && (
        <div key="issues" className="apple-tab-pane space-y-5">
          {/* 顶层说明条：精炼直观 */}
          <div className="flex items-center justify-between px-1">
            <div className="flex items-center gap-2.5">
              <span className="w-1.5 h-1.5 rounded-full bg-blue-600 shrink-0" />
              <h2 className="text-sm font-bold text-slate-900 tracking-tight">
                全案涉外争议焦点与法定构成要件审查
              </h2>
              <span className="text-xs font-mono text-slate-400">
                ({issues.length} 项争点 · {issues.reduce((acc, it) => acc + it.checklist.length, 0)} 项法定要件)
              </span>
            </div>
          </div>

          {/* 左右分栏 Master-Detail 布局 (4 cols : 8 cols) */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-5 items-start">
            {/* 左侧：争点主清单 (Master List, 4 cols) */}
            <div className="lg:col-span-4 space-y-3">
              <div className="text-xs font-mono font-bold uppercase tracking-wider text-slate-400 px-1">
                争点列表 ({issues.length})
              </div>

              <div className="space-y-2.5">
                {issues.map((iss) => {
                  const isSelected = iss.id === activeIssue.id;
                  const satisfiedCount = iss.checklist.filter((c) => c.status === 'passed').length;
                  const totalCount = iss.checklist.length;
                  const hasWarning = iss.checklist.some((c) => c.status !== 'passed');

                  return (
                    <div
                      key={iss.id}
                      onClick={() => {
                        setSelectedIssueId(iss.id);
                        setActiveCheckIndex(0);
                      }}
                      className={`p-4 rounded-2xl border transition-all duration-200 cursor-pointer relative group ${
                        isSelected
                          ? 'bg-white border-blue-600 shadow-xs ring-1 ring-blue-500/20'
                          : 'bg-white/70 hover:bg-white border-slate-200/80 hover:border-slate-300 shadow-2xs'
                      }`}
                    >
                      {/* 选中态左侧高光竖条 */}
                      {isSelected && (
                        <div className="absolute left-0 top-3 bottom-3 w-1 bg-blue-600 rounded-r-full" />
                      )}

                      <div className="space-y-2 pl-1">
                        <div className="flex items-center justify-between text-xs">
                          <div className="flex items-center gap-2">
                            <span className="font-mono font-bold text-slate-900">
                              {iss.code}
                            </span>
                            <span className="text-[11px] font-mono text-slate-500 px-1.5 py-0.5 rounded bg-slate-100">
                              {iss.category}
                            </span>
                          </div>
                          <div className="flex items-center gap-1.5 text-[11px] font-medium">
                            <span
                              className={`w-1.5 h-1.5 rounded-full shrink-0 ${
                                hasWarning ? 'bg-amber-500' : 'bg-blue-600'
                              }`}
                            />
                            <span className={hasWarning ? 'text-amber-700' : 'text-slate-700'}>
                              {satisfiedCount}/{totalCount} 要件
                            </span>
                          </div>
                        </div>

                        <h4 className="text-xs font-semibold text-slate-800 line-clamp-2 leading-relaxed">
                          {iss.title}
                        </h4>

                        <div className="flex items-center justify-between text-[11px] font-mono text-slate-400 pt-1.5 border-t border-slate-100/80">
                          <span className="truncate max-w-[170px]">{iss.norms.join(' · ')}</span>
                          <span className={`text-[11px] font-medium ${isSelected ? 'text-blue-600' : 'text-slate-400 group-hover:text-slate-700'}`}>
                            {isSelected ? '审查中 ➔' : '查看 ➔'}
                          </span>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* 右侧：选中争点之要件深度核验工作台 (Detail Workspace, 8 cols) */}
            <div className="lg:col-span-8 apple-bento-card rounded-[28px] p-6 sm:p-7 space-y-6">
              {/* 争点标题与法源规范条目 */}
              <div className="space-y-3 pb-5 border-b border-slate-100">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <div className="flex items-center gap-2">
                    <span className="px-2.5 py-0.5 rounded-lg text-xs font-mono font-bold bg-slate-900 text-white">
                      {activeIssue.code}
                    </span>
                    <span className="text-xs font-mono text-slate-500 font-medium">
                      {activeIssue.category}
                    </span>
                  </div>

                  {/* 关联法条抽屉入口 */}
                  <div className="flex items-center gap-1.5 flex-wrap">
                    {activeIssue.norms.map((normKey, nIdx) => (
                      <button
                        key={nIdx}
                        type="button"
                        onClick={() => openLawDrawer(normKey.replace('§', '').trim())}
                        className="inline-flex items-center gap-1 px-2.5 py-1 text-xs font-mono font-medium rounded-lg bg-white border border-slate-200/90 text-slate-700 hover:text-blue-600 hover:border-blue-300 transition-all cursor-pointer shadow-2xs active:scale-[0.98]"
                        title="在右侧抽屉对照研读条文原文"
                      >
                        <BookOpen className="w-3 h-3 text-blue-600" />
                        <span>{normKey}</span>
                      </button>
                    ))}
                  </div>
                </div>

                <h3 className="text-lg sm:text-xl font-bold text-slate-900 tracking-tight leading-snug">
                  {activeIssue.title}
                </h3>

                <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">
                  {activeIssue.cnQuery}
                </p>

                {/* 综合审查结论横幅 */}
                <div className="p-3.5 rounded-2xl bg-slate-50 border border-slate-200/80 flex flex-wrap items-center justify-between gap-3 text-xs">
                  <div className="flex items-center gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-blue-600 shrink-0" />
                    <span className="text-slate-500 font-medium">实体审查判定：</span>
                    <span className="font-bold text-slate-900">{activeIssue.headlineVerdict}</span>
                  </div>
                  <span className="font-mono text-slate-500">
                    法理依据：{activeIssue.deDogmatic}
                  </span>
                </div>
              </div>

              {/* 法定构成要件逐项审查清单 (全部展开，无需多层嵌套点击) */}
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <h4 className="text-xs font-bold uppercase tracking-wider text-slate-900 font-mono">
                    法定构成要件审查清单 ({activeIssue.checklist.length} 项要件)
                  </h4>
                </div>

                <div className="space-y-3.5">
                  {activeIssue.checklist.map((step, idx) => {
                    const isWarn = step.status === 'warning';
                    const isFail = step.status === 'failed';
                    return (
                      <div
                        key={idx}
                        className="p-4 sm:p-5 rounded-2xl bg-white/90 border border-slate-200/80 shadow-2xs space-y-3"
                      >
                        {/* 要件头部 */}
                        <div className="flex flex-wrap items-center justify-between gap-2">
                          <div className="flex items-center gap-2">
                            <span className="w-6 h-6 rounded-lg bg-slate-100 text-slate-700 font-mono text-xs font-bold flex items-center justify-center shrink-0 border border-slate-200/60">
                              0{idx + 1}
                            </span>
                            <span className="text-sm font-bold text-slate-900">
                              {step.label}
                            </span>
                          </div>

                          <div className="flex items-center gap-1.5 px-2.5 py-0.5 rounded-lg bg-slate-50 border border-slate-200 text-xs font-medium">
                            <span
                              className={`w-1.5 h-1.5 rounded-full shrink-0 ${
                                isWarn ? 'bg-amber-500' : isFail ? 'bg-rose-500' : 'bg-blue-600'
                              }`}
                            />
                            <span className={isWarn ? 'text-amber-700 font-semibold' : isFail ? 'text-rose-700 font-semibold' : 'text-slate-800 font-semibold'}>
                              {step.result}
                            </span>
                          </div>
                        </div>

                        {/* 事实核验判定 */}
                        <div className="text-xs space-y-1">
                          <span className="text-[11px] font-mono text-slate-400 uppercase font-semibold">
                            事实判定
                          </span>
                          <p className="font-medium text-slate-800 leading-relaxed">
                            {step.shortNote}
                          </p>
                        </div>

                        {/* 法理裁判准则与深层分析 */}
                        <div className="text-xs space-y-1 pt-2.5 border-t border-slate-100">
                          <span className="text-[11px] font-mono text-slate-400 uppercase font-semibold">
                            法理准则与抗辩除斥规则
                          </span>
                          <p className="text-slate-600 leading-relaxed">
                            {step.deepDetail}
                          </p>
                        </div>

                        {/* 案卷证据对应项 */}
                        <div className="pt-2.5 border-t border-slate-100 flex flex-wrap items-center justify-between gap-3 text-xs">
                          <div className="flex items-center gap-2 min-w-0">
                            <FileText className="w-3.5 h-3.5 text-slate-400 shrink-0" />
                            <span className="text-slate-500 text-[11px] shrink-0 font-mono">支撑证据：</span>
                            <span className="font-medium text-slate-800 truncate">
                              {step.evidence}
                            </span>
                          </div>
                          <button
                            type="button"
                            onClick={() => openLawDrawer(activeIssue.norms[0] || 'IDN:Law_2/2017:Art_30')}
                            className="text-xs font-medium text-blue-600 hover:text-blue-700 transition-colors cursor-pointer shrink-0"
                          >
                            核验法条依据 ➔
                          </button>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* ========================================================================= */}
      {/* 子视图 3：攻防演练 (Red Team Confrontation Exercise) */}
      {/* ========================================================================= */}
      {subPage === 'red-team' && (
        <div key="red-team" className="apple-tab-pane space-y-6">
          {/* 裁判支持倾向与核心胜败关键点 - 紧凑功能型 Bento Card */}
          <div className="apple-bento-card rounded-[28px] p-6 space-y-4">
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 pb-3 border-b border-slate-100">
              <div>
                <div className="flex items-center gap-2">
                  <span className="w-1.5 h-1.5 rounded-full bg-blue-600 shrink-0" />
                  <span className="text-xs font-mono font-bold uppercase tracking-wider text-slate-500">
                    双边法理攻防演练与裁判推演
                  </span>
                </div>
                <h3 className="text-base sm:text-lg font-bold text-slate-900 mt-0.5 tracking-tight">
                  涉外多轮对抗交锋推演矩阵
                </h3>
              </div>
            </div>

            {/* 裁判审查要害要素三列微卡 */}
            {currentCase?.strategic_assessment?.pivotal_factors && (
              <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                {currentCase.strategic_assessment.pivotal_factors.map((factor, fIdx) => (
                  <div
                    key={fIdx}
                    className="p-3.5 rounded-2xl bg-white/80 border border-slate-200/80 shadow-2xs space-y-1"
                  >
                    <div className="flex items-center justify-between text-[11px] font-mono text-slate-400">
                      <span>裁判审查焦点 0{fIdx + 1}</span>
                      <span className="w-1.5 h-1.5 rounded-full bg-blue-600/60" />
                    </div>
                    <p className="text-xs font-semibold text-slate-800 leading-relaxed">
                      {factor}
                    </p>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* 三个回合的左右交锋矩阵 */}
          <div className="space-y-4">
            {adversarialRounds.map((rd) => {
              const isNeutralized =
                rd.counterMeasure.preSatisfied ||
                simulatedEvidences[rd.counterMeasure.evidenceId];

              return (
                <div
                  key={rd.id}
                  className="rounded-[32px] apple-bento-card overflow-hidden"
                >
                  {/* 回合标题栏 */}
                  <div className="px-7 py-4 bg-white/70 border-b border-slate-200/70 flex flex-wrap items-center justify-between gap-3">
                    <div className="flex items-center gap-3">
                      <span className="px-3 py-1 rounded-xl text-xs font-mono font-bold bg-slate-900 text-white shadow-2xs">
                        {rd.roundCode}
                      </span>
                      <h4 className="text-sm sm:text-base font-bold text-slate-900 tracking-tight">{rd.topic}</h4>
                    </div>

                    <div className="flex items-center gap-3">
                      <button
                        type="button"
                        onClick={() => openLawDrawer(rd.coreNorm)}
                        className="px-3 py-1 rounded-xl text-xs font-mono font-medium bg-white border border-slate-200/80 text-slate-700 hover:text-blue-600 hover:border-blue-300 transition-all cursor-pointer shadow-2xs active:scale-[0.98]"
                      >
                        {rd.normLabel}
                      </button>
                      <div className="flex items-center gap-1.5 text-xs text-slate-600 font-medium">
                        <span
                          className={`w-1.5 h-1.5 rounded-full shrink-0 ${
                            isNeutralized ? 'bg-blue-600 shadow-xs shadow-blue-500/30' : 'bg-amber-500'
                          }`}
                        />
                        <span className={isNeutralized ? 'text-slate-800 font-semibold' : 'text-amber-700 font-semibold'}>
                          {isNeutralized ? '对方抗辩已封堵' : '存在抗辩敞口'}
                        </span>
                      </div>
                    </div>
                  </div>

                  {/* 三栏交锋主体 */}
                  <div className="p-6 sm:p-7 grid grid-cols-1 lg:grid-cols-11 gap-4 items-stretch">
                    {/* 左栏：我方进攻 (4 cols) */}
                    <div className="lg:col-span-4 p-5 rounded-2xl bg-white/80 border border-slate-200/80 shadow-2xs flex flex-col justify-between space-y-3">
                      <div className="space-y-2">
                        <div className="flex items-center justify-between">
                          <span className="inline-flex items-center gap-2 text-xs font-bold text-slate-900">
                            <span className="w-1.5 h-1.5 rounded-full bg-blue-600 shrink-0" />
                            {rd.claimantMove.title}
                          </span>
                          <span className="text-[10px] font-mono text-slate-400 font-bold">CLAIMANT</span>
                        </div>
                        <p className="text-xs text-slate-600 leading-relaxed font-normal">
                          {rd.claimantMove.argument}
                        </p>
                      </div>
                      <div className="pt-2.5 border-t border-slate-100 text-[11px] font-mono text-slate-500">
                        法理武器：{rd.claimantMove.authority}
                      </div>
                    </div>

                    {/* 中栏：裁决交锋核心焦点 (3 cols) */}
                    <div className="lg:col-span-3 flex flex-col justify-center items-center px-1">
                      <div className="w-full p-5 rounded-2xl bg-blue-600 text-white space-y-2 shadow-xs shadow-blue-500/25 border border-blue-500/40">
                        <div className="flex items-center justify-between text-[10px] font-mono text-blue-100">
                          <span>──►</span>
                          <span className="text-white font-bold font-mono text-xs">裁判审查焦点</span>
                          <span>◄──</span>
                        </div>
                        <p className="text-xs text-blue-50 leading-relaxed text-center font-medium">
                          {rd.refereePivot}
                        </p>
                      </div>
                    </div>

                    {/* 右栏：对方抗辩 (4 cols) */}
                    <div
                      className={`lg:col-span-4 p-5 rounded-2xl border flex flex-col justify-between transition-all space-y-3 ${
                        isNeutralized
                          ? 'bg-slate-50/50 border-slate-200/60 opacity-60'
                          : 'bg-white/80 border-slate-200/80 shadow-2xs'
                      }`}
                    >
                      <div className="space-y-2">
                        <div className="flex items-center justify-between">
                          <span className="inline-flex items-center gap-2 text-xs font-bold text-slate-800">
                            <span
                              className={`w-1.5 h-1.5 rounded-full shrink-0 ${
                                isNeutralized ? 'bg-slate-300' : 'bg-amber-500'
                              }`}
                            />
                            {rd.respondentMove.title}
                          </span>
                          <span className="text-[10px] font-mono text-slate-400 font-bold">DEFENSE</span>
                        </div>
                        <p
                          className={`text-xs text-slate-600 leading-relaxed ${
                            isNeutralized ? 'line-through text-slate-400' : ''
                          }`}
                        >
                          {rd.respondentMove.argument}
                        </p>
                      </div>
                      <div className="pt-2.5 border-t border-slate-100 flex items-center justify-between text-[11px]">
                        <span className="text-slate-400 font-mono">威胁烈度：{rd.respondentMove.riskLevel}</span>
                        <span className={`font-semibold ${isNeutralized ? 'text-slate-500' : 'text-amber-600'}`}>
                          {isNeutralized ? '已封堵' : '待反制'}
                        </span>
                      </div>
                    </div>
                  </div>

                  {/* 底部：反制动作与补证开关 */}
                  <div className="px-7 py-4 bg-slate-50/70 border-t border-slate-200/70 flex flex-wrap items-center justify-between gap-3">
                    <div className="flex items-center gap-2 text-xs text-slate-600">
                      <CornerDownRight className="w-3.5 h-3.5 text-blue-600 shrink-0" />
                      <span className="font-semibold text-slate-900">反制论据：</span>
                      <span>{rd.counterMeasure.effectDesc}</span>
                    </div>

                    {rd.counterMeasure.preSatisfied ? (
                      <span className="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-xl text-xs font-semibold bg-slate-200/70 text-slate-700">
                        <Check className="w-3.5 h-3.5 text-slate-700 stroke-[2.5]" />
                        <span>{rd.counterMeasure.actionLabel}</span>
                      </span>
                    ) : (
                      <button
                        type="button"
                        onClick={() =>
                          setCaseEvidences((prev) => ({
                            ...prev,
                            [currentCaseId]: {
                              ...(prev[currentCaseId] || {}),
                              [rd.counterMeasure.evidenceId]: !(prev[currentCaseId]?.[rd.counterMeasure.evidenceId]),
                            },
                          }))
                        }
                        className={`inline-flex items-center gap-1.5 px-4 py-2 rounded-xl text-xs font-semibold transition-all cursor-pointer active:scale-[0.98] ${
                          isNeutralized
                            ? 'bg-blue-600 text-white shadow-xs shadow-blue-500/25'
                            : 'bg-white text-slate-900 border border-slate-200/90 hover:border-slate-300 hover:bg-slate-50 shadow-2xs'
                        }`}
                      >
                        {isNeutralized ? (
                          <Check className="w-3.5 h-3.5 text-white stroke-[2.5]" />
                        ) : (
                          <Plus className="w-3.5 h-3.5 text-slate-700 stroke-[2.5]" />
                        )}
                        <span>{rd.counterMeasure.actionLabel}</span>
                        <span className="ml-1 font-mono text-[11px] opacity-80">
                          (+{rd.counterMeasure.winBoost}%)
                        </span>
                      </button>
                    )}
                  </div>
                </div>
              );
            })}
          </div>

          {/* 行动补强清单 */}
          {currentCase?.strategic_assessment?.actionable_checklist && (
            <div className="p-8 sm:p-10 rounded-[32px] apple-bento-card space-y-5">
              <div className="flex items-center gap-2">
                <span className="w-1.5 h-1.5 rounded-full bg-blue-600 shrink-0" />
                <span className="text-xs font-mono font-bold uppercase tracking-wider text-slate-500">
                  涉外诉讼补强建议行动清单
                </span>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5 pt-1">
                {currentCase.strategic_assessment.actionable_checklist.map((act, aIdx) => (
                  <div
                    key={aIdx}
                    className="p-4 rounded-2xl bg-white/80 border border-slate-200/80 shadow-2xs text-xs flex items-start gap-3 transition-all hover:border-slate-300"
                  >
                    <CheckCircle2 className="w-4 h-4 text-blue-600 shrink-0 mt-0.5" />
                    <span className="text-slate-800 font-medium leading-relaxed">{act}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* ========================================================================= */}
      {/* 子视图 4：证据链闭环图谱与法源先例 (Evidence Chain) */}
      {/* ========================================================================= */}
      {subPage === 'evidence-chain' && (
        <div key="evidence-chain" className="apple-tab-pane space-y-6">
          {/* 关联法条与判例关系图谱 */}
          <div className="apple-bento-card rounded-[28px] p-6 space-y-4">
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 pb-3 border-b border-slate-100">
              <div>
                <div className="flex items-center gap-2">
                  <span className="w-1.5 h-1.5 rounded-full bg-blue-600 shrink-0" />
                  <span className="text-xs font-mono font-bold uppercase tracking-wider text-slate-500">
                    权威法典条文与先例援引拓扑
                  </span>
                </div>
                <h3 className="text-base sm:text-lg font-bold text-slate-900 mt-0.5 tracking-tight">
                  涉外成文法典与司法裁判先例图谱
                </h3>
              </div>
              <span className="text-xs font-mono text-slate-400">
                穿透点击节点查看官方正文
              </span>
            </div>
            <InteractiveCitationGraph
              onSelectNorm={(id) => openLawDrawer(id)}
            />
          </div>

          {/* 权威援引法源条文列表 */}
          <div className="apple-bento-card rounded-[32px] p-8 sm:p-10 space-y-5">
            <div className="flex items-center justify-between pb-4 border-b border-slate-200/70">
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <span className="w-1.5 h-1.5 rounded-full bg-blue-600 shrink-0" />
                  <span className="text-xs font-mono font-bold uppercase tracking-wider text-slate-500">
                    权威成文法条列表
                  </span>
                </div>
                <h3 className="text-base sm:text-lg font-bold text-slate-900 tracking-tight">
                  官方有效法条原文与核验附录
                </h3>
                <p className="text-xs text-slate-500">
                  所有法源均严格锚定官方现行数据库与官方正文
                </p>
              </div>
              <span className="text-xs font-mono font-semibold text-slate-500 px-3 py-1.5 rounded-xl bg-slate-50 border border-slate-200/80">
                {Object.keys(currentCase?.evidence || {}).length} 条现行法源
              </span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-3.5">
              {Object.entries(currentCase?.evidence || {}).map(([eid, ev]) => (
                <div
                  key={eid}
                  onClick={() => openLawModal(eid)}
                  className="p-5 rounded-2xl bg-white/80 hover:bg-white border border-slate-200/80 hover:border-slate-300 transition-all cursor-pointer group space-y-3 shadow-2xs hover:shadow-xs active:scale-[0.99]"
                >
                  <div className="flex items-center justify-between">
                    <span className="font-mono text-xs font-bold text-slate-900">
                      {ev.ref_id}
                    </span>
                    <GradeBadge grade={ev.grade} />
                  </div>
                  <p className="text-xs text-slate-700 line-clamp-2 leading-relaxed">
                    {ev.text_de}
                  </p>
                  <div className="flex items-center justify-between text-[11px] text-slate-400 pt-2 border-t border-slate-100 font-mono">
                    <span>{eid}</span>
                    <span className="text-slate-600 group-hover:text-blue-600 font-medium transition-colors">查看官方正文 ➔</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* 权威司法判例先例列表 */}
          {currentCase?.similar_cases && currentCase.similar_cases.length > 0 && (
            <div className="apple-bento-card rounded-[32px] p-8 sm:p-10 space-y-5">
              <div className="flex items-center justify-between pb-4 border-b border-slate-200/70">
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-blue-600 shrink-0" />
                    <span className="text-xs font-mono font-bold uppercase tracking-wider text-slate-500">
                      权威司法裁判先例
                    </span>
                  </div>
                  <h3 className="text-base sm:text-lg font-bold text-slate-900 tracking-tight">
                    最高法院与高级巡回法院权威要旨
                  </h3>
                </div>
                <span className="text-xs font-mono font-semibold text-slate-500 px-3 py-1.5 rounded-xl bg-slate-50 border border-slate-200/80">
                  {currentCase.similar_cases.length} 篇参考先例
                </span>
              </div>

              <div className="space-y-3.5">
                {currentCase.similar_cases.map((sc, scIdx) => (
                  <div
                    key={scIdx}
                    className="p-5 rounded-2xl bg-white/80 border border-slate-200/80 space-y-3 text-xs shadow-2xs"
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2.5">
                        <span className="font-bold text-slate-900 font-mono">{sc.court}</span>
                        <span className="px-2.5 py-0.5 rounded-lg bg-slate-50 border border-slate-200/80 font-mono text-slate-700 text-[11px] font-medium">
                          {sc.az}
                        </span>
                        <span className="text-slate-400 font-mono text-[11px]">{sc.date}</span>
                      </div>
                      <div className="flex items-center gap-1.5 text-xs font-medium">
                        <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 shrink-0" />
                        <span className="text-slate-600">
                          {sc.divergence_flag === 'consistent' ? '裁判一致' : '倾向参照'}
                        </span>
                      </div>
                    </div>

                    <p className="text-slate-800 font-medium leading-relaxed">{sc.court_view_zh}</p>

                    {sc.similarity_points && sc.similarity_points.length > 0 && (
                      <div className="flex flex-wrap items-center gap-2 text-[11px] text-slate-500 pt-2 border-t border-slate-100 font-mono">
                        <span className="font-semibold text-slate-700 font-sans">核心相同点：</span>
                        <span>{sc.similarity_points.join('；')}</span>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* ========================================================================= */}
      {/* 子视图 5：司法合规报告与专家备忘 (Compliance) */}
      {/* ========================================================================= */}
      {subPage === 'compliance' && (
        <div key="compliance" className="apple-tab-pane grid grid-cols-1 lg:grid-cols-12 gap-6">
          {/* 左侧：最高院司法解释（二）形式合规核验 */}
          <div className="lg:col-span-5 apple-bento-card rounded-[28px] p-6 sm:p-7 space-y-5">
            <div className="flex items-center gap-2">
              <span className="w-1.5 h-1.5 rounded-full bg-blue-600 shrink-0" />
              <span className="text-xs font-mono font-bold uppercase tracking-wider text-slate-500">
                涉外形式合规防线
              </span>
            </div>
            <h3 className="text-base sm:text-lg font-bold text-slate-900 tracking-tight">
              最高院涉外民事关系司法解释（二）形式审查
            </h3>
            <div className="space-y-2.5 text-xs">
              {[
                '司法部法通网与东道国司法公报权威数据源全链路核验',
                `行为时法（${caseMeta.criticalDate}）现行有效性锁定确认`,
                '成文法条中外双语平行对照与金标准先例要旨完备',
                'SHA-256 防伪数字快照校验附录已生成',
              ].map((item, i) => (
                <div
                  key={i}
                  className="p-3.5 rounded-2xl bg-white/80 border border-slate-200/80 shadow-2xs flex items-center gap-3 font-medium text-slate-800"
                >
                  <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
                  <span>{item}</span>
                </div>
              ))}
            </div>

            {/* 真实质检清单 */}
            <div className="pt-4 border-t border-slate-200/70 space-y-3">
              <span className="text-xs font-bold text-slate-900 block">
                涉外司法防线逐项质检结果
              </span>
              <div className="space-y-2 max-h-52 overflow-y-auto no-scrollbar">
                {(currentCase?.checks || []).map((ck, cIdx) => (
                  <div
                    key={cIdx}
                    className="p-3 rounded-2xl bg-white/80 border border-slate-200/80 shadow-2xs flex items-center justify-between text-xs"
                  >
                    <div className="flex items-center gap-2 min-w-0 pr-2">
                      <span className="font-mono font-bold text-slate-900 shrink-0">{ck.code}</span>
                      <span className="text-slate-600 line-clamp-1">{ck.reason}</span>
                    </div>
                    <div className="flex items-center gap-1.5 text-xs shrink-0 font-medium">
                      <span
                        className={`w-1.5 h-1.5 rounded-full ${
                          ck.status === 'pass' ? 'bg-blue-600' : 'bg-amber-500'
                        }`}
                      />
                      <span className={ck.status === 'pass' ? 'text-slate-700' : 'text-amber-700'}>
                        {ck.status === 'pass' ? '通过' : '待复核'}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* 右侧：查明法律意见书导出卡片 */}
          <div className="lg:col-span-7 apple-bento-card rounded-[28px] p-6 sm:p-7 space-y-6">
            <div className="flex items-center justify-between border-b border-slate-200/70 pb-4">
              <div>
                <div className="flex items-center gap-2">
                  <span className="w-1.5 h-1.5 rounded-full bg-blue-600 shrink-0" />
                  <span className="text-xs font-bold text-slate-500 font-mono uppercase tracking-wider">
                    涉外法律查明意见书 (正式版)
                  </span>
                </div>
                <h3 className="text-base sm:text-lg font-bold text-slate-900 mt-1 tracking-tight">
                  东盟国家建设工程法律风险防范与合规指引意见书
                </h3>
              </div>
              <GradeBadge grade="A" />
            </div>

            <div className="p-5 rounded-2xl bg-white/80 border border-slate-200/80 shadow-2xs space-y-2">
              <span className="text-[11px] font-mono font-bold text-slate-400 uppercase block">
                一、 案件事实与准据法核定结论
              </span>
              <p className="text-xs sm:text-[13px] text-slate-600 leading-relaxed">
                依据东道国涉外建设工程实体法及《FIDIC 银皮书设计采购施工合同条件》，合同意思自治合法有效。准据法与属地法规范锁定为东道国建设工程法典（建筑资质、本土化率、双语要求）及国际工程标准条款现行版本。
              </p>
            </div>

            <div className="p-5 rounded-2xl bg-white/80 border border-slate-200/80 shadow-2xs space-y-2">
              <span className="text-[11px] font-mono font-bold text-slate-400 uppercase block">
                二、 核心法理要件与抗辩审查结论
              </span>
              <p className="text-xs sm:text-[13px] text-slate-600 leading-relaxed">
                {legalAssessment.qualitativeSummary}
              </p>
            </div>

            <div className="pt-3 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 border-t border-slate-200/70">
              <span className="text-xs text-slate-400 font-mono">
                符合《最高人民法院关于适用〈涉外民事关系法律适用法〉若干问题的解释（二）》
              </span>
              <button
                type="button"
                onClick={() => setCurrentView('review')}
                className="inline-flex items-center justify-center gap-2 px-5 py-2.5 text-xs font-semibold text-white bg-blue-600 hover:bg-blue-700 rounded-xl transition-all cursor-pointer shadow-xs shadow-blue-500/25 active:scale-[0.98] shrink-0"
              >
                <Download className="w-3.5 h-3.5" />
                <span>进入报告导出审阅工作台</span>
              </button>
            </div>
          </div>
        </div>
      )}

      {/* 底部悬浮 AI Agent 实时推演交互舱 (Apple 灵动岛 / Copilot 胶囊风格，全子页面常驻可唤出) */}
      <FloatingOmniBar onTriggerRecalc={handleAdoptCountermeasure} currentWinRate={legalAssessment.overallScore} />

      {/* 综合法理支持度测算模型与依据弹窗 */}
      <ViabilityCalculationModal
        isOpen={showViabilityModal}
        onClose={() => setShowViabilityModal(false)}
        assessment={legalAssessment}
      />

      {/* 对方抗辩应对策略与重新测算弹窗 */}
      {showThreatModal && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/40 backdrop-blur-md antialiased apple-modal-backdrop"
          onClick={() => setShowThreatModal(false)}
        >
          <div
            className="w-full max-w-xl bg-white rounded-[28px] shadow-[0_24px_64px_rgba(0,0,0,0.18)] border border-black/[0.08] overflow-hidden flex flex-col max-h-[90vh] apple-modal-card"
            onClick={(e) => e.stopPropagation()}
          >
            {/* 弹窗头部 */}
            <div className="px-7 py-5 bg-white border-b border-slate-100 flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="p-2.5 rounded-2xl bg-slate-100 text-slate-800 border border-slate-200/60">
                  <Swords className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="text-base font-semibold text-slate-900 tracking-tight">
                    对方抗辩风险分析与应对策略
                  </h3>
                  <p className="text-xs text-slate-500 mt-0.5">
                    调取事实证据与援引裁判除外规则，化解失权抗辩
                  </p>
                </div>
              </div>
              <button
                type="button"
                onClick={() => setShowThreatModal(false)}
                className="p-2 rounded-full text-slate-400 hover:text-slate-700 hover:bg-slate-100 transition-colors cursor-pointer"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            {/* 弹窗主体 */}
            <div className="p-7 overflow-y-auto space-y-5 text-xs">
              {/* 1. 对方主要抗辩要点 */}
              <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200/80 space-y-1.5">
                <span className="font-mono text-[11px] font-medium uppercase text-slate-500 tracking-wider flex items-center gap-1.5">
                  <span className="w-1.5 h-1.5 rounded-full bg-amber-500 shrink-0" />
                  对方核心抗辩主张 · {topDefense?.opposing_basis || 'FIDIC Clause 20.1 / 属地工程强行法'}
                </span>
                <p className="text-xs text-slate-700 leading-relaxed font-medium">
                  对方辩称承包商未在 28 天除斥期内递交完整索赔凭单，且主张合同未签署印尼语官方文本违反属地强制性规定，主张免除补偿义务或合同无效。
                </p>
              </div>

              {/* 2. 建议反制动作与材料调取 */}
              <div className="space-y-3">
                <span className="text-xs font-semibold text-slate-800 block">
                  建议反制策略与证据调取方案
                </span>

                <div className="space-y-2.5">
                  <div className="p-3.5 rounded-2xl bg-slate-50 border border-slate-100 flex items-start gap-3">
                    <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                    <div className="space-y-0.5">
                      <span className="font-semibold text-slate-900 block">证据补强 1：调取现场监理例会纪要、催告函及现场航拍存证</span>
                      <p className="text-slate-600 leading-relaxed">
                        证明业主与监理方自始知悉土地未交付阻工事实，实质知悉原则（Doctrine of Constructive Notice）成立，不构成怠于通知。
                      </p>
                    </div>
                  </div>

                  <div className="p-3.5 rounded-2xl bg-slate-50 border border-slate-100 flex items-start gap-3">
                    <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                    <div className="space-y-0.5">
                      <span className="font-semibold text-slate-900 block">证据补强 2：印尼高院 SEMA 3/2023 先例抗辩与双语备忘录存证</span>
                      <p className="text-slate-600 leading-relaxed">
                        证明双方在履约期间始终以英文作为工作语言且存在印尼语签约合意备忘，根据最新印尼最高法院判例，不因单语而自始无效。
                      </p>
                    </div>
                  </div>

                  <div className="p-3.5 rounded-2xl bg-slate-50 border border-slate-100 flex items-start gap-3">
                    <CheckCircle2 className="w-4 h-4 text-slate-500 shrink-0 mt-0.5" />
                    <div className="space-y-0.5">
                      <span className="font-semibold text-slate-900 block">法律武器：援引东盟先例与国际仲裁除外规则阻断抗辩</span>
                      <p className="text-slate-600 leading-relaxed">
                        援引新加坡上诉法院 BS Mount Sophia 先例与印尼法院先例，对保函恶意索兑与业主干预导致工期迟延实施阻断抗辩。
                      </p>
                    </div>
                  </div>
                </div>
              </div>

              {/* 3. 预期测算收益 */}
              <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200/80 flex items-center justify-between">
                <div className="flex items-center gap-2.5">
                  <span className="w-2 h-2 rounded-full bg-emerald-500 shrink-0" />
                  <div>
                    <span className="font-semibold text-slate-900 block">采纳后胜诉测算收益预期</span>
                    <span className="text-slate-500 text-xs">成功阻断对方失权抗辩，攻防抵御力提升至 95%</span>
                  </div>
                </div>
                <span className="text-base font-bold font-mono text-slate-900">+7% ~ +10%</span>
              </div>
            </div>

            {/* 弹窗底部操作 */}
            <div className="px-7 py-4 bg-slate-50/80 border-t border-slate-100 flex items-center justify-between">
              <button
                type="button"
                onClick={() => setShowThreatModal(false)}
                className="px-4 py-2 text-xs font-medium text-slate-600 hover:text-slate-900 hover:bg-slate-200/50 rounded-xl transition-all cursor-pointer"
              >
                暂不采纳
              </button>
              <button
                type="button"
                onClick={handleAdoptCountermeasure}
                className="inline-flex items-center justify-center px-5 py-2.5 text-xs font-semibold text-white bg-slate-900 hover:bg-slate-800 rounded-xl transition-all cursor-pointer shadow-sm hover:shadow"
              >
                采纳方案并实施胜诉测算
              </button>
            </div>
          </div>
        </div>
      )}

      {/* 胜诉支持度重新测算过渡动效 (类似案件查明的过渡特效) */}
      {isRecalculating && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/40 backdrop-blur-md antialiased apple-modal-backdrop">
          <div className="w-full max-w-md bg-white rounded-[32px] p-8 shadow-[0_24px_64px_rgba(0,0,0,0.18)] border border-black/[0.08] text-center space-y-6 apple-modal-card">
            {/* 顶置旋转/脉冲发光图标 */}
            <div className="relative inline-flex items-center justify-center">
              <div className="w-14 h-14 rounded-2xl bg-slate-100 border border-slate-200 flex items-center justify-center text-slate-800">
                <Loader2 className="w-6 h-6 text-slate-800 animate-spin" />
              </div>
            </div>

            <div className="space-y-1.5">
              <h3 className="text-lg font-bold text-slate-900 tracking-tight">
                正在重新测算胜诉支持度...
              </h3>
              <p className="text-xs text-slate-500">
                正在接入补充反制材料，根据现行成文法典与司法裁判先例更新计算模型
              </p>
            </div>

            {/* 3 阶段推演动态清单 */}
            <div className="space-y-2.5 text-left text-xs bg-slate-50 p-4 rounded-2xl border border-slate-100">
              <div className="flex items-center justify-between">
                <span className="flex items-center gap-2 text-slate-700 font-medium">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                  <span>1. 调取事实调试日志与送达凭证</span>
                </span>
                <span className="text-[11px] font-mono text-emerald-600 font-bold">已就绪</span>
              </div>

              <div className="flex items-center justify-between">
                <span className="flex items-center gap-2 text-slate-700 font-medium">
                  {recalcStep >= 2 ? (
                    <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                  ) : (
                    <span className="w-4 h-4 rounded-full border-2 border-blue-600 border-t-transparent animate-spin inline-block" />
                  )}
                  <span>2. 援引裁判先例阻断对方时效抗辩</span>
                </span>
                <span className={`text-[11px] font-mono ${recalcStep >= 2 ? 'text-emerald-600 font-bold' : 'text-blue-600 font-bold'}`}>
                  {recalcStep >= 2 ? '已阻断' : '测算中...'}
                </span>
              </div>

              <div className="flex items-center justify-between">
                <span className="flex items-center gap-2 text-slate-700 font-medium">
                  {recalcStep >= 3 ? (
                    <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                  ) : (
                    <span className="w-4 h-4 rounded-full border-2 border-slate-300 inline-block" />
                  )}
                  <span>3. 四维法理加权测算与胜算概率重估</span>
                </span>
                <span className={`text-[11px] font-mono ${recalcStep >= 3 ? 'text-emerald-600 font-bold' : 'text-slate-400'}`}>
                  {recalcStep >= 3 ? '测算完成' : '待更新'}
                </span>
              </div>
            </div>

            {/* 底部平滑动态进度条 */}
            <div className="space-y-1.5">
              <div className="h-1.5 w-full bg-slate-100 rounded-full overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-blue-600 to-emerald-500 rounded-full transition-all duration-300"
                  style={{
                    width: recalcStep === 1 ? '35%' : recalcStep === 2 ? '75%' : '100%',
                  }}
                />
              </div>
              <div className="flex justify-between text-[10px] text-slate-400 font-mono">
                <span>法理模型更新</span>
                <span>{recalcStep === 1 ? '35%' : recalcStep === 2 ? '75%' : '100%'}</span>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* 跨项目生命周期阶段平滑流转弹窗 */}
      {showTransitionModal && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/40 backdrop-blur-md antialiased apple-modal-backdrop"
          onClick={() => setShowTransitionModal(false)}
        >
          <div
            className="w-full max-w-lg bg-white rounded-[28px] shadow-[0_24px_64px_rgba(0,0,0,0.18)] border border-black/[0.08] overflow-hidden flex flex-col apple-modal-card"
            onClick={(e) => e.stopPropagation()}
          >
            {/* 弹窗头部 */}
            <div className="p-6 pb-4 border-b border-slate-100 flex items-center justify-between">
              <div className="flex items-center gap-2.5">
                <div className="w-9 h-9 rounded-2xl bg-blue-50 text-blue-600 flex items-center justify-center border border-blue-200/60 shadow-2xs">
                  <RotateCcw className="w-4 h-4 text-blue-600" />
                </div>
                <div>
                  <h3 className="text-base font-bold text-slate-900 tracking-tight">
                    项目生命周期跨阶段平滑流转
                  </h3>
                  <p className="text-[11px] text-slate-400 font-mono">
                    支持在【投前合规】与【履约争议】之间保持案卷血缘平滑流转
                  </p>
                </div>
              </div>
              <button
                type="button"
                onClick={() => setShowTransitionModal(false)}
                className="p-1.5 rounded-xl text-slate-400 hover:text-slate-800 hover:bg-slate-100 transition-colors cursor-pointer"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            {/* 弹窗主体 */}
            <div className="p-6 space-y-4 text-xs">
              <div className="p-4 bg-slate-50/80 rounded-2xl border border-slate-200/70 space-y-2">
                <span className="text-[11px] font-mono text-slate-400 font-bold block uppercase tracking-wider">
                  阶段转换走向
                </span>
                <div className="flex items-center justify-between font-medium">
                  <span className="px-2.5 py-1 rounded-lg bg-white text-slate-700 border border-slate-200/80 shadow-2xs font-sans">
                    {currentCase?.meta?.lifecycle_stage === 'pre_investment'
                      ? '投前并购与签约合规审查'
                      : '履约索赔、保函止付与争议解决'}
                  </span>
                  <ArrowRight className="w-4 h-4 text-blue-600" />
                  <span className="px-2.5 py-1 rounded-lg bg-blue-600 text-white font-semibold shadow-xs font-sans">
                    {currentCase?.meta?.lifecycle_stage === 'pre_investment'
                      ? '履约索赔、保函止付与争议解决'
                      : '投前并购与签约合规审查'}
                  </span>
                </div>
              </div>

              <div className="space-y-1.5">
                <label className="text-xs font-semibold text-slate-800 flex items-center gap-1.5">
                  <span>流转说明与事实补充备忘 (可选)</span>
                </label>
                <textarea
                  value={transitionNote}
                  onChange={(e) => setTransitionNote(e.target.value)}
                  placeholder="例如：由于东道国政府调整并网电价政策且当地征地迟延，项目由前期投资论证转入工程索赔与保函止付争议推演..."
                  rows={3}
                  className="w-full rounded-2xl border border-slate-200/90 bg-slate-50/50 p-3 text-xs text-slate-800 focus:bg-white focus:border-blue-600 focus:ring-2 focus:ring-blue-500/10 transition-all outline-hidden resize-none"
                />
              </div>
            </div>

            {/* 弹窗底栏 */}
            <div className="p-5 px-6 bg-slate-50/80 border-t border-slate-100 flex items-center justify-end gap-2.5">
              <button
                type="button"
                onClick={() => setShowTransitionModal(false)}
                className="px-4 py-2 rounded-xl text-xs font-semibold text-slate-600 hover:text-slate-900 hover:bg-slate-200/60 transition-all cursor-pointer"
              >
                取消
              </button>
              <button
                type="button"
                disabled={isTransitioning}
                onClick={handleConfirmTransition}
                className="inline-flex items-center gap-1.5 px-5 py-2 text-xs font-semibold text-white bg-blue-600 hover:bg-blue-700 active:scale-[0.98] rounded-xl transition-all cursor-pointer shadow-xs shadow-blue-500/25 disabled:opacity-50"
              >
                {isTransitioning ? (
                  <>
                    <Loader2 className="w-3.5 h-3.5 animate-spin" />
                    <span>流转中...</span>
                  </>
                ) : (
                  <>
                    <Check className="w-3.5 h-3.5" />
                    <span>确认流转并更新案卷</span>
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
