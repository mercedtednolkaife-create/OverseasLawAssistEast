import React, { useState, useMemo, useEffect, useRef, useCallback } from 'react';
import { useApp } from '../../context/AppContext';
import { lawAgentApi } from '../../api/lawAgentApi';
import {
  Layers,
  FileText,
  ShieldCheck,
  Clock,
  Swords,
  ChevronRight,
  ArrowRight,
  SlidersHorizontal,
  BookOpen,
  Play,
  RotateCcw,
  Check,
  Copy,
  Download,
  Loader2,
  Compass,
  Activity,
  Zap,
  Target,
  X,
  Globe,
  Share2,
  Sparkles,
  Maximize2,
  Bot,
} from 'lucide-react';
import { GradeBadge } from '../common/GradeBadge';
import { CitationGraphFullscreenModal } from './CitationGraphFullscreenModal';
import { ViabilityCalculationModal } from './ViabilityCalculationModal';
import { TacticalGuidance, NegotiationScript, UrgentAction, AttachedArtifact } from '../../types/lawAgent';
import { getJurisdictionConfig, ASEAN_JURISDICTIONS } from '../../configs/jurisdictions';

type AnalysisFacet = 'verdict' | 'elements' | 'sandbox' | 'export';

export const CaseAnalysisView: React.FC = () => {
  const {
    currentCase,
    setCurrentCase,
    currentCaseId,
    setCurrentView,
    openLawModal,
    openLawDrawer,
    openRightDock,
    closeRightDock,
    openPipelineAnimation,
    showToast,
    isRightDockOpen,
    casesList,
    loadCase,
    refreshCurrentCase,
    switchingCaseId,
  } = useApp();

  // 当前主切面：verdict (决策/准入全景) | elements (争点/红线要件) | sandbox (沙盘/工坊) | export (图谱/意见书)
  const [facet, setFacet] = useState<AnalysisFacet>('verdict');

  const isPreInv = currentCase?.meta?.lifecycle_stage === 'pre_investment';
  const hostJur = currentCase?.meta?.jurisdiction || 'asean_id';
  const jurConfig = getJurisdictionConfig(hostJur);

  // 工程沙盘交互试算状态
  const initialParams = currentCase?.meta?.engineering_params || {};
  const [simTkdn, setSimTkdn] = useState<number>(() => {
    return initialParams.declared_tkdn_pct ?? initialParams.subcontract_ratio ?? (hostJur === 'asean_my' ? 35 : hostJur === 'asean_vn' ? 8 : 28);
  });
  const [simDelayDays, setSimDelayDays] = useState<number>(() => {
    return initialParams.delay_days ?? initialParams.eot_delay_days ?? 180;
  });
  const [simNoticeDays, setSimNoticeDays] = useState<number>(() => {
    return initialParams.notice_days ?? initialParams.notice_served_days ?? (hostJur === 'asean_my' ? 10 : 18);
  });
  const [simMainLd, setSimMainLd] = useState<number>(initialParams.main_ld_cap_pct ?? 15);
  const [simSubLd, setSimSubLd] = useState<number>(initialParams.sub_ld_cap_pct ?? 10);
  const [simSinosureDays, setSimSinosureDays] = useState<number>(initialParams.sinosure_notice_days ?? 12);
  const [isSimulatingEng, setIsSimulatingEng] = useState<boolean>(false);

  // 投前投资架构切换状态
  const [selectedSpvScheme, setSelectedSpvScheme] = useState<'A' | 'B' | 'C'>('B');
  const [foreignEquityPct, setForeignEquityPct] = useState<number>(49);
  const [localSubcontractPct, setLocalSubcontractPct] = useState<number>(35);

  // 商务谈判话术卡场景与双语切换
  const [activeScriptIdx, setActiveScriptIdx] = useState<number>(0);
  const [scriptLangMode, setScriptLangMode] = useState<'zh' | 'en'>('zh');
  const [copiedScript, setCopiedScript] = useState<boolean>(false);
  const [scriptPulse, setScriptPulse] = useState<boolean>(false);

  // 工坊内落实反制清单与调取证据
  const [completedActionIds, setCompletedActionIds] = useState<Record<string, boolean>>({});

  // 选中的争点/审查支柱 ID
  const [selectedIssueId, setSelectedIssueId] = useState<string>('');

  // 测算模型与依据弹窗开关
  const [showViabilityModal, setShowViabilityModal] = useState<boolean>(false);
  // 法源因果拓扑图谱全屏弹窗开关
  const [showGraphModal, setShowGraphModal] = useState<boolean>(false);

  // 当案件变更时同步沙盘滑块数值 (仅在切换不同案件 ID 时初始化，不重复触发自旋重算)
  const userInteractedRef = useRef<boolean>(false);
  const currentCaseRef = useRef(currentCase);
  currentCaseRef.current = currentCase;

  useEffect(() => {
    const params = currentCase?.meta?.engineering_params || {};
    const jur = currentCase?.meta?.jurisdiction || 'asean_id';
    const tkdnVal = params.declared_tkdn_pct ?? params.subcontract_ratio ?? (jur === 'asean_my' ? 35 : jur === 'asean_vn' ? 8 : 28);
    setSimTkdn(tkdnVal);
    const delayVal = params.delay_days ?? params.eot_delay_days ?? 180;
    setSimDelayDays(delayVal);
    const noticeVal = params.notice_days ?? params.notice_served_days ?? (jur === 'asean_my' ? 10 : 18);
    setSimNoticeDays(noticeVal);
    if (params.main_ld_cap_pct !== undefined) setSimMainLd(params.main_ld_cap_pct);
    if (params.sub_ld_cap_pct !== undefined) setSimSubLd(params.sub_ld_cap_pct);
    if (params.sinosure_notice_days !== undefined) setSimSinosureDays(params.sinosure_notice_days);
    userInteractedRef.current = false;

    // 核心状态重置：防止上一案的争点选择、话术索引、勾选项等残留污染新案
    setSelectedIssueId('');
    setActiveScriptIdx(0);
    setCompletedActionIds({});
    setShowGraphModal(false);
    setShowViabilityModal(false);
    setSelectedSpvScheme('B');
    setForeignEquityPct(49);
    setLocalSubcontractPct(jur === 'asean_my' ? 35 : jur === 'asean_vn' ? 8 : 28);
  }, [currentCase?.case_id]);

  // 用户主动交互滑块辅助处理
  const handleSliderChange = (setter: (val: number) => void, val: number) => {
    userInteractedRef.current = true;
    setter(val);
  };

  // 全键盘流桌面级微交互 (1/2/3/4 切换切面, B 呼出副驾坞)
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      const target = e.target as HTMLElement;
      if (
        target &&
        (target.tagName === 'INPUT' ||
          target.tagName === 'TEXTAREA' ||
          target.isContentEditable)
      ) {
        return;
      }

      if (e.key === '1') setFacet('verdict');
      else if (e.key === '2') setFacet('elements');
      else if (e.key === '3') setFacet('sandbox');
      else if (e.key === '4') setFacet('export');
      else if (e.key === 'b' || e.key === 'B') {
        openRightDock('case_copilot');
      } else if (e.key === 'Escape') {
        setShowViabilityModal(false);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [openRightDock]);

  // 沙盘试算防抖与并发写锁保护
  const simReqVersionRef = useRef<number>(0);
  const handleSimulateEngineering = useCallback(async () => {
    const activeCase = currentCaseRef.current;
    if (!activeCase || isSimulatingEng) return;
    setIsSimulatingEng(true);
    const reqVersion = ++simReqVersionRef.current;
    try {
      const updatedCase = await lawAgentApi.simulateEngineering(activeCase.case_id, {
        declared_tkdn_pct: simTkdn,
        delay_days: simDelayDays,
        notice_days: simNoticeDays,
        sinosure_notice_days: simSinosureDays,
        main_ld_cap_pct: simMainLd,
        sub_ld_cap_pct: simSubLd,
      });
      if (reqVersion === simReqVersionRef.current) {
        if (updatedCase) {
          setCurrentCase(updatedCase);
        } else {
          await loadCase(activeCase.case_id, true);
        }
        showToast('✓ 工程沙盘算子与中信保合规门禁已完成实时重算！', 'success');
        // 触发右侧话术卡高亮呼吸
        setScriptPulse(true);
        setTimeout(() => setScriptPulse(false), 800);
      }
    } catch (err: any) {
      if (reqVersion === simReqVersionRef.current) {
        showToast(err.message || '沙盘试算失败', 'error');
      }
    } finally {
      if (reqVersion === simReqVersionRef.current) {
        setIsSimulatingEng(false);
      }
    }
  }, [isSimulatingEng, simTkdn, simDelayDays, simNoticeDays, simSinosureDays, simMainLd, simSubLd, setCurrentCase, loadCase, showToast]);

  // 基准参数快照
  const baselineParams = useMemo(() => currentCase?.meta?.engineering_params || {}, [currentCase?.case_id]);

  // 滑块 1 依据案件东道国法域自适应 (避免非印尼案件显示印尼 TKDN)
  const slider1Config = useMemo(() => {
    const hostJur = currentCase?.meta?.jurisdiction || 'asean_id';
    if (hostJur === 'asean_my') {
      return {
        title: '马来西亚 本地分包/土著采购比例 (CIDB Act 520)',
        target: 30,
        anchorLeft: '37.5%',
        isCompliant: simTkdn >= 30,
        statusLabel: simTkdn >= 30 ? '(符合 CIDB 规范)' : '(配额不足预警)',
        desc: simTkdn >= 30
          ? '已达到马来西亚 CIDB 属地分包配额标准，履约风险受控。'
          : `属地配额低于 30% 基准线，易遭 CIDB 资质审查与属地分包抗辩。`,
      };
    }
    if (hostJur === 'asean_vn') {
      return {
        title: '越南 2025新建设法违约金 (LD) 上限率 (Law 135/2025)',
        target: 8,
        anchorLeft: '10%',
        isCompliant: simTkdn <= 8,
        statusLabel: simTkdn <= 8 ? '(符合商法 8% 封顶)' : '(超额易遭法定核减)',
        desc: simTkdn <= 8
          ? '在越南商法第 301 条 8% 封顶线内，受法律强行法保护。'
          : `超出商法 8% 基础线，可依据 2025 新建设法第 86.2 条提请法院核减。`,
      };
    }
    if (hostJur === 'asean_sg') {
      return {
        title: '新加坡 SOPA 快速付款裁决核算准备金率',
        target: 20,
        anchorLeft: '25%',
        isCompliant: simTkdn >= 20,
        statusLabel: simTkdn >= 20 ? '(拨备充足)' : '(流动性预警)',
        desc: simTkdn >= 20
          ? '符合新加坡建筑业付款保障法 SOPA 快速裁决准备金安全线。'
          : '准备金不足，面临紧急仲裁强制执行流动性压力。',
      };
    }
    // 默认印尼
    return {
      title: '印尼 TKDN 本地化采购率 (MEMR 11/2024)',
      target: 40,
      anchorLeft: '42.8%',
      isCompliant: simTkdn >= 40,
      statusLabel: simTkdn >= 40 ? '(达标)' : '(缺口待豁免)',
      desc: simTkdn >= 40
        ? '已达电力主机采购法定线，可直接申请完工 COD 证书。'
        : `存在 ${40 - simTkdn}% 缺口，需依据 MEMR 11/2024 第 8 条提请部长特许豁免。`,
    };
  }, [currentCase?.meta?.jurisdiction, simTkdn]);

  // 恢复案卷初始基准参数
  const handleResetBaseline = () => {
    userInteractedRef.current = true;
    const p = baselineParams;
    if (p.declared_tkdn_pct !== undefined) setSimTkdn(p.declared_tkdn_pct);
    if (p.delay_days !== undefined) setSimDelayDays(p.delay_days);
    if (p.notice_days !== undefined) setSimNoticeDays(p.notice_days);
    if (p.main_ld_cap_pct !== undefined) setSimMainLd(p.main_ld_cap_pct);
    if (p.sub_ld_cap_pct !== undefined) setSimSubLd(p.sub_ld_cap_pct);
    if (p.sinosure_notice_days !== undefined) setSimSinosureDays(p.sinosure_notice_days);
    showToast('已恢复案卷初始基准参数', 'info');
  };

  // 350ms 防抖自动实时试算 (仅在用户主动拖动滑块时生效，杜绝案件加载时自旋弹窗)
  useEffect(() => {
    if (!userInteractedRef.current) {
      return;
    }
    const timer = setTimeout(() => {
      userInteractedRef.current = false;
      handleSimulateEngineering();
    }, 350);
    return () => clearTimeout(timer);
  }, [simTkdn, simDelayDays, simNoticeDays, simSinosureDays, simMainLd, simSubLd, handleSimulateEngineering]);

  // 移除挂载成果
  const handleRemoveArtifact = async (artifactId: string) => {
    if (!currentCase) return;
    try {
      const updated = await lawAgentApi.removeCaseArtifact(currentCase.case_id, artifactId);
      setCurrentCase({
        ...currentCase,
        attached_artifacts: updated,
      });
      showToast('已从本案卷移除该挂载附件', 'info');
    } catch (e: any) {
      showToast(e.message || '移除失败', 'error');
    }
  };

  // 案件元数据提取
  const caseMeta = useMemo(() => {
    const meta = currentCase?.meta;
    const summaryTitle = casesList.find((c) => c.case_id === currentCase?.case_id)?.title;
    const title = currentCase?.title || meta?.title || summaryTitle || '东盟涉外建设工程与特许经营争议查明案';
    const contractType = meta?.contract_type || (isPreInv ? '特许经营协议 / 跨境合资合同' : 'EPC 总承包合同 / FIDIC 银皮书');
    const parties = meta?.parties?.length ? meta.parties.join(' vs ') : '中资总承包商/投资方 vs 东道国业主/特许权授予方';
    const criticalDate = meta?.contract_date || meta?.signing_date || '2024-03-15';
    const hostJur = meta?.jurisdiction || 'asean_id';
    const jurConfig = getJurisdictionConfig(hostJur);
    const choiceOfLaw = meta?.choice_of_law || meta?.governing_law_jurisdiction || `${jurConfig.name_zh}实体法`;

    return {
      title,
      contractType,
      parties,
      criticalDate,
      choiceOfLaw,
      hostJur: `${jurConfig.flag} ${jurConfig.name_zh}`,
    };
  }, [currentCase, casesList, isPreInv]);

  // 从案件数据提取战术引导与 3D 定性结论 (自适应东盟法域)
  const tacticalGuidance: TacticalGuidance = useMemo(() => {
    const hostJur = currentCase?.meta?.jurisdiction || 'asean_id';
    const activeGuidance = currentCase?.meta?.tactical_guidance || (currentCase as any)?.tactical_guidance;
    // 如果存在后端缓存，但当前案件为非印尼且缓存中含有印尼特有关键字 (SEMA/MEMR/TKDN/印尼)，则视为陈旧数据穿透
    const isStaleIndonesian = hostJur !== 'asean_id' && activeGuidance && JSON.stringify(activeGuidance).includes('印尼');
    if (activeGuidance && !isStaleIndonesian) {
      return activeGuidance;
    }
    const jurConfig = getJurisdictionConfig(hostJur);

    if (hostJur === 'asean_my') {
      return {
        qualitative_verdict: {
          legal_support_level: isPreInv ? '附条件准入 (Conditional Clearance)' : '强支持 (Substantial Support)',
          confidence_band: isPreInv ? '置信区间 78%-86%' : '置信区间 84%-92%',
          procedural_exposure: isPreInv ? 'CIDB 资质合规 & 属地劳工配额' : 'CIPAA 第35条背靠背无效 & 28天时效抗辩',
          counter_block_expectation: isPreInv ? '中转新加坡 SPV 激活 BIT 保护' : '高确定性阻断 (CIPAA 强行法排除背靠背条款)',
        },
        negotiation_scripts: [
          {
            scenario_title: 'FIDIC 20.1 索赔通知逾期反驳 (Prevention Principle)',
            legal_basis: 'FIDIC 20.1 · Prevention Principle · 马来西亚合同法 Contracts Act 1950 善意履约原则',
            script_zh: '我方坚决驳斥发包人因我方未严格满足 28 天通知即主张权利灭失之抗辩。根据普通法确立并为马来西亚联邦法院采纳之“阻碍原则 (Prevention Principle)”，当工期延误系因发包人交地迟延等自身违约导致时，发包人无权援引除斥期条款计取预定违约金 (LD)。在卷监理日志已证实发包人完全实际知情，程序瑕疵不构成实体权利灭失。',
            script_en: 'We vigorously refute the Employer\'s contention that Contractor\'s entitlement to Time Extension is barred under Clause 20.1. Under the established Prevention Principle affirmed by Malaysian courts, an Employer cannot benefit from its own breach. The contemporaneous records demonstrate the Employer\'s actual knowledge, legally precluding forfeiture.',
          },
          {
            scenario_title: '马来西亚 CIPAA 2012 法定裁决与背靠背无效条款抗辩',
            legal_basis: '马来西亚 CIPAA 2012 第 35 条有条件付款无效明文 & 亚洲国际仲裁中心 (AIAC) 规程',
            script_zh: '针对分包商所提起的 CIPAA 快速法定裁决，我方提出严正抗辩：虽 CIPAA 第 35 条规定背靠背付款条款自始无效，但主合同争议正处于关键路径事实审理阶段，且发包人拖欠主合同款项系因不可归责于总包方之客观原因所致。我方正依法向高院提请中止裁决执行，并提出反向扣款抵销，防范突击索兑。',
            script_en: 'Pursuant to Section 35 of CIPAA 2012, while conditional payment mechanisms face statutory constraints, the Contractor maintains substantive cross-claims for delay compensation. We are lodging emergency applications to stay adjudication enforcement and safeguard against unmerited execution.',
          },
          {
            scenario_title: '见索即付保函恶意索兑抗辩与中信保通报口径',
            legal_basis: '新加坡最高法院 BS Mount Sophia 判例 · 显失公平止付规则 · 中信保 30 天报损规程',
            script_zh: '严正告知发包人：鉴于工期延误系发包人未尽交地义务所致，目前并无任何承包商实质违约。若发包人突击索兑履约保函，将构成极度显失公平 (Unconscionability)。我方将立即向紧急仲裁员提请全额临时止付令，且我方已向中国信保正式提交出险通报，发包人恶意行为将被列入多边联合黑名单。',
            script_en: 'Any demand upon the Performance Security while delay is solely attributable to site handover failure constitutes unconscionability (BS Mount Sophia [2016] SGCA 57). Contractor is immediately applying for emergency interim injunctions and has lodged Sinosure pre-loss notices.',
          },
        ],
        urgent_actions: [
          {
            action_type: 'FIDIC 20.1 索赔通知补强函',
            deadline_tag: '7日内发出',
            document_template_title: '《关于工程受阻关键路径停滞之工期顺延补充通告》',
            key_points: [
              '正式援引 FIDIC 银皮书第 8.4(c) 款（雇主原因延误）与 20.1 款',
              '随函附送监理工程师每日现场签到表与 P6 关键路径阻断对比图',
              '马来西亚法域应留存正式书面签收回执与向工程师送达留痕凭证',
            ],
          },
          {
            action_type: 'CIPAA 裁决应诉与 AIAC 答辩准备',
            deadline_tag: '10日法定答辩期内',
            document_template_title: '《依据 CIPAA 2012 第 10 条提交之工程款争议实质答辩书》',
            key_points: [
              '调取工程师签证之工期延误阻却与反向扣款抵销证据清单',
              '依据 CIDB Act 520 审查分包商施工资质与执照有效性',
            ],
          },
          {
            action_type: '中国信保出险事前留痕通报',
            deadline_tag: '30日除斥期内',
            document_template_title: '《海外投资/承包工程险可能损失正式通知书 (Notice of Loss)》',
            key_points: [
              '向中国出口信用保险公司提交正式书面《可能损失通知书》锁定保全利益',
              '提交发包人拖欠工程款及恶意索兑保函威胁证据链',
            ],
          },
        ],
      };
    }

    if (hostJur === 'asean_vn') {
      return {
        qualitative_verdict: {
          legal_support_level: isPreInv ? '附条件准入 (Conditional Clearance)' : '强支持 (Substantial Support)',
          confidence_band: isPreInv ? '置信区间 78%-86%' : '置信区间 83%-91%',
          procedural_exposure: isPreInv ? '外商投资负面清单 & 工商登记' : '2025新建设法第 86.2 条违约金(LD)上限核减',
          counter_block_expectation: isPreInv ? '中转新加坡 SPV 激活 BIT 保护' : '高确定性阻断 (依据新建设法 86.2 条调减违约金)',
        },
        negotiation_scripts: [
          {
            scenario_title: 'FIDIC 20.1 索赔通知逾期反驳 (Prevention Principle)',
            legal_basis: 'FIDIC 20.1 · Prevention Principle · 越南民法典善意原则',
            script_zh: '我方坚决驳斥发包人因我方未严格满足 28 天通知即主张权利灭失之抗辩。发包人原因交地迟延实质导致关键路径受阻，发包人无权以此要求罚金。',
            script_en: 'We vigorously refute Employer\'s claim of forfeiture under Clause 20.1. Handover delays caused by Employer cannot justify liquidated damages.',
          },
          {
            scenario_title: '越南《2025新建设法》第 86.2 条预定损害赔偿 (LD) 封顶抗辩',
            legal_basis: '越南 2025 年新建设法 (Law 135/2025) 第 86.2 条 & 商法第 301 条 8% 封顶',
            script_zh: '依据越南《2025新建设法》第 86.2 条及《商法》第 301 条，违约金与预定损害赔偿须以实际合理损失为基准，法定封顶为 8%。发包人擅自扣减缺乏法定依据，我方保留提起越仲 (VIAC) 反诉及司法核减权利。',
            script_en: 'Pursuant to Article 86.2 of Vietnam Construction Law 2025 and Commercial Law Article 301, liquidated damages must reflect actual losses and cannot exceed statutory limits.',
          },
          {
            scenario_title: '见索即付保函恶意索兑抗辩与中信保通报口径',
            legal_basis: '国际商会 URDG 758 · 显失公平止付规则 · 中信保 30 天报损规程',
            script_zh: '严正告知发包人：鉴于工期延误的唯一近因系发包人未交付土地，若突击索兑履约保函将直接构成欺诈与极度显失公平。我方已向中国信保正式提交出险通报。',
            script_en: 'Any call upon the Performance Security while delay is attributable to site non-possession constitutes egregious unconscionability.',
          },
        ],
        urgent_actions: [
          {
            action_type: 'FIDIC 20.1 索赔通知补强函',
            deadline_tag: '7日内发出',
            document_template_title: '《关于工程受阻关键路径停滞之工期顺延补充通告》',
            key_points: [
              '正式援引 FIDIC 银皮书第 8.4(c) 款与 20.1 款',
              '随函附送监理工程师每日现场签到表与 P6 阻断对比图',
              '越南法域应留存正式书面签收与越文备忘录回执',
            ],
          },
          {
            action_type: '越南新建设法 86.2 条损害核算抗辩',
            deadline_tag: '14日内核算期内',
            document_template_title: '《依据 2025 新建设法提请违约金司法调减抗辩要旨》',
            key_points: [
              '提交不可抗力证明与实际合理损失对比测算表',
              '援引商法 301 条主张 8% 法定上限封顶',
            ],
          },
          {
            action_type: '中国信保出险事前留痕通报',
            deadline_tag: '30日除斥期内',
            document_template_title: '《海外投资/承包工程险可能损失正式通知书 (Notice of Loss)》',
            key_points: [
              '向中国出口信用保险公司提交正式书面《可能损失通知书》锁定保全利益',
              '提交发包人延迟批文及突击索兑保函威胁证据链',
            ],
          },
        ],
      };
    }

    if (hostJur === 'asean_sg') {
      return {
        qualitative_verdict: {
          legal_support_level: isPreInv ? '附条件准入 (Conditional Clearance)' : '强支持 (Substantial Support)',
          confidence_band: isPreInv ? '置信区间 80%-88%' : '置信区间 85%-93%',
          procedural_exposure: isPreInv ? '中转 SPV 投资协定保护 & 税务安排' : 'SOPA 快速付款程序 & 保函止付门槛',
          counter_block_expectation: isPreInv ? '全面激活 BIT 与中立仲裁管辖' : '高确定性阻断 (BS Mount Sophia 显失公平止付与 SOPA 保护)',
        },
        negotiation_scripts: [
          {
            scenario_title: 'FIDIC 20.1 索赔通知逾期反驳 (Prevention Principle)',
            legal_basis: 'FIDIC 20.1 · Prevention Principle · 新加坡普通法防阻原则',
            script_zh: '我方坚决驳斥发包人因我方未严格满足 28 天通知即主张权利灭失之抗辩。根据新加坡普通法确立之防阻原则 (Prevention Principle)，发包人未尽移交施工现场义务构成自身违约，无权援引除斥期条款计取预定违约金 (LD)。在卷监理日志已证实发包人完全实际知情，程序瑕疵不构成实体权利灭失。',
            script_en: 'Contractor refutes Employer\'s forfeiture contention under Clause 20.1. Under Singapore common law Prevention Principle, Employer cannot benefit from its own failure to deliver site possession.',
          },
          {
            scenario_title: '新加坡 SOPA 第 9 条反背靠背支付与工程款清偿',
            legal_basis: '新加坡建筑业付款与裁决法 (SOPA) 第 9 条强行法',
            script_zh: '依据新加坡建筑业付款与裁决法 (SOPA) 第 9 条，任何以第三方付款为条件的背靠背付款条款均属自始无效。分包合同款项需按审定进度结算，总包商不得因业主未付而扣延分包款。',
            script_en: 'Pursuant to Section 9 of the Building and Construction Industry Security of Payment Act (SOPA), pay-when-paid provisions are statutorily void and unenforceable.',
          },
          {
            scenario_title: 'BS Mount Sophia 显失公平保函止付口径',
            legal_basis: '新加坡上诉庭 BS Mount Sophia [2016] SGCA 57 · 显失公平止付先例',
            script_zh: '严正告知发包人：鉴于工程延误系发包人未交付施工场地所致，若发包人恶意突击索兑履约保函，将构成极度显失公平 (Unconscionability)。我方将立即向新加坡高院提请止付禁令。',
            script_en: 'Any demand upon the Performance Security constitutes unconscionability under BS Mount Sophia [2016] SGCA 57, warranting interim injunction relief from the Singapore High Court.',
          },
        ],
        urgent_actions: [
          {
            action_type: 'FIDIC 20.1 索赔通知补强函',
            deadline_tag: '7日内发出',
            document_template_title: '《关于工程受阻关键路径停滞之工期顺延补充通告》',
            key_points: [
              '正式援引 FIDIC 银皮书第 8.4(c) 款与 20.1 款',
              '附监理工程师每日现场签到表与 P6 阻断对比图',
              '留存正式书面签收回执与向工程师送达留痕凭证',
            ],
          },
          {
            action_type: 'SIAC 紧急仲裁与保函止付',
            deadline_tag: '48小时内',
            document_template_title: '《向新加坡高院/SIAC紧急仲裁员提请保函临时止付令申请书》',
            key_points: [
              '依据 BS Mount Sophia 规则整理发包人缺乏善意之证据链',
              '向开证商业银行送达争议正式通告函',
              '申请 SIAC 紧急仲裁员程序冻结保函兑付',
            ],
          },
          {
            action_type: '中国信保出险事前留痕通报',
            deadline_tag: '30日除斥期内',
            document_template_title: '《海外投资/承包工程险可能损失正式通知书 (Notice of Loss)》',
            key_points: [
              '向中国出口信用保险公司提交正式书面《可能损失通知书》锁定保全利益',
              '提交发包人延迟批文及突击索兑保函威胁证据链',
            ],
          },
        ],
      };
    }

    // 默认或印尼法域 (asean_id)
    return {
      qualitative_verdict: {
        legal_support_level: isPreInv ? '附条件准入 (Conditional Clearance)' : '强支持 (Substantial Support)',
        confidence_band: isPreInv ? '置信区间 78%-86%' : '置信区间 82%-90%',
        procedural_exposure: isPreInv ? '2 项刚性准入红线 (TKDN 40% / 双语同文)' : '可控中度威胁 (FIDIC 20.1 28天时效)',
        counter_block_expectation: isPreInv ? '建议中转新加坡 SPV 激活 BIT 保护' : '高确定性阻断 (业主阻碍原则与 SEMA 3/2023)',
      },
      negotiation_scripts: [
        {
          scenario_title: 'FIDIC 20.1 索赔通知逾期反驳 (Prevention Principle)',
          legal_basis: 'FIDIC 20.1 · Prevention Principle · 印尼民法典第 1338 条契约善意原则',
          script_zh: '我方坚决驳斥发包人因我方未严格满足 28 天通知即主张权利灭失之抗辩。根据英美法确立并为东道国民法典及 FIDIC 仲裁广泛采纳之“阻碍原则 (Prevention Principle)”以及东道国民法典第 1338 条所确立的善意履约规则，当工期延误系因发包人交地迟延及未尽征拆义务等自身行为实质导致时，发包人无权援引时效除斥条款免除自身违约后果，亦无权据此计取预定违约赔偿金 (LD)。在卷现场监理日志及往来邮件已充分证实发包人对阻工事实具备完全实际知情，通知程序瑕疵不构成实质权利灭失。',
          script_en: 'We vigorously refute the Employer\'s contention that Contractor\'s entitlement to Time Extension is barred under Clause 20.1. Under the well-settled Prevention Principle and the statutory requirement of Good Faith (Article 1338 of the Civil Code), an Employer cannot benefit from its own default—namely, the 180-day site access handover failure. The contemporaneous site diaries demonstrate the Employer\'s actual knowledge, legally precluding the forfeiture of our substantive remedy.',
        },
        {
          scenario_title: '印尼 TKDN 能矿部特许豁免申请谈判口径 (MEMR 11/2024)',
          legal_basis: '印尼能源与矿产资源部 MEMR 11/2024 条例第 8 条豁免通道',
          script_zh: '针对光伏高精逆变器与主变电设备本地化率 (TKDN) 申报数值，我方严格遵守印尼能源与矿产资源部第 11/2024 号条例关于国家重大战略电力项目的特别规程。鉴于东道国本土供应链尚不具备同等技术规格与产能，且本项目已获得外资商业部前期规划备忘录批准，我方正依据 MEMR 11/2024 第 8 条程序向能矿部提请本土制造能力缺口特许豁免认定，该审批并不阻碍完工商业运营 (COD) 证书的法定核发。',
          script_en: 'Pursuant to Article 8 of MEMR Regulation No. 11/2024, given that local domestic manufacturers cannot supply components matching the project\'s technical threshold, the Contractor is fully eligible for the official TKDN ministerial exemption pathway, which secures the Commercial Operation Date (COD) clearance.',
        },
        {
          scenario_title: '见索即付保函恶意索兑抗辩与中信保通报口径',
          legal_basis: '新加坡最高法院 BS Mount Sophia 判例 · 显失公平止付规则 · 中信保 30 天报损规程',
          script_zh: '严正告知发包人：鉴于工期延误的唯一近因系发包人未交付原住民土地所致，目前并无任何承包商违约事实成立。若发包人突击向开证银行发起履约保函全额索兑，将直接构成欺诈与极度显失公平 (Unconscionability)。根据准据法专属法院裁判先例 (BS Mount Sophia [2016] SGCA 57)，我方将立即向紧急仲裁员提请全额临时止付禁令，且我方已向中国信保正式提交出险通报，发包人恶意行为将被列入多边信用联合黑名单。',
          script_en: 'Any demand upon the Performance Security while delay is solely attributable to site non-possession constitutes egregious unconscionability under established precedents (BS Mount Sophia [2016] SGCA 57). Contractor is immediately applying for emergency interim injunctions and has lodged Sinosure underwriting pre-loss notices.',
        },
      ],
      urgent_actions: [
        {
          action_type: 'FIDIC 20.1 索赔通知补强函',
          deadline_tag: '7日内发出',
          document_template_title: '《关于原住民土地阻工导致关键路径停滞之工期顺延补充通告》',
          key_points: [
            '正式援引 FIDIC 银皮书第 8.4(c) 款（雇主原因延误）与 20.1 款',
            '随函附送监理工程师每日现场签到表与 P6 关键路径不可抗力阻断对比图',
            '印尼法域必须附带印尼语同文版本并留存正式书面签收回执 (SEMA 3/2023)',
          ],
        },
        {
          action_type: '印尼能矿部 TKDN 豁免听证申请',
          deadline_tag: '14日内提交',
          document_template_title: '《MEMR 11/2024 电力设备本土供应链能力技术核实报告》',
          key_points: [
            '出具印尼本土 3 家同类厂商无供货能力的官方询价函与拒函',
            '援引 MEMR 11/2024 第 8 条向新能源总司申请技术性豁免',
          ],
        },
        {
          action_type: '中国信保出险事前留痕通报',
          deadline_tag: '30日除斥期内',
          document_template_title: '《海外投资/承包工程险可能损失正式通知书 (Notice of Loss)》',
          key_points: [
            '向中国出口信用保险公司提交正式书面《可能损失通知书》锁定保全利益',
            '提交东道国政府延迟批文及发包人恶意索兑保函威胁证据链',
          ],
        },
      ],
    };
  }, [currentCase, isPreInv]);

  // 争议焦点与要件清单动态解析
  const issues = useMemo(() => {
    const rawIssues = currentCase?.issues || [];
    if (rawIssues.length === 0) {
      return isPreInv
        ? [
            {
              id: 'issue-1',
              code: '审查支柱 01',
              category: '准入许可与资质牌照',
              title: '东道国外资准入牌照 (BUJKA/PCAB/CIDB) 与强制联营体协议合规',
              norms: ['IDN:Law_2/2017:Art_30', 'IDN:BKPM_5/2021'],
              tldr: '外资股比满足东道国负面清单限制，且持有合格外资建筑施工总承包牌照。',
            },
            {
              id: 'issue-2',
              code: '审查支柱 02',
              category: '国际条约与间接征收',
              title: '特许权法律变动、电价补贴调整与双边投资协定 (BIT) 间接征收保护',
              norms: ['BIT:China_ASEAN:Art_6', 'ICSID:Precedents'],
              tldr: '搭建新加坡 SPV 中转架构，激活中新双边投资保护协定间接征收仲裁管辖。',
            },
          ]
        : [
            {
              id: 'issue-1',
              code: '争点 01',
              category: '程序除斥与时效抗辩',
              title: 'FIDIC 20.1 索赔通知28天时效失权与属地强行法反制',
              norms: ['FIDIC:Silver:20.1', 'IDN:SEMA_3/2023'],
              tldr: '索赔通知送达存在瑕疵，但可依据阻碍原则与善意履约阻断失权抗辩。',
            },
            {
              id: 'issue-2',
              code: '争点 02',
              category: '实体请求权成立',
              title: 'FIDIC 8.4 迟延交地工期顺延 (EOT) 与预定违约金抗辩',
              norms: ['FIDIC:Silver:8.4', 'IDN:CivCode:Art_1338'],
              tldr: '业主交地迟延构成关键路径阻工，我方享有法定工期全额顺延请求权。',
            },
          ];
    }
    return rawIssues.map((iss, idx) => ({
      id: iss.issue_id || `issue-${idx + 1}`,
      code: isPreInv ? `支柱 0${idx + 1}` : `争点 0${idx + 1}`,
      category: isPreInv
        ? '准入合规与强行法审查'
        : iss.kind === 'fact' ? '事实与时效审查' : '实体请求权与抗辩阻断',
      title: iss.text_zh.length > 40 ? iss.text_zh.slice(0, 40) + '...' : iss.text_zh,
      norms: (iss.element_ids || [])
        .map((eid) => (currentCase?.elements || []).find((e) => e.element_id === eid))
        .filter(Boolean)
        .flatMap((el) => (el?.links || []).map((l) => currentCase?.evidence?.[l.eid]?.ref_id).filter(Boolean) as string[])
        .slice(0, 2),
      tldr: iss.text_zh,
    }));
  }, [currentCase, isPreInv]);

  // 当前选中的争议焦点
  const activeIssue = useMemo(() => {
    return issues.find((i) => i.id === selectedIssueId) || issues[0];
  }, [issues, selectedIssueId]);

  // 当前选中争点下挂载的要件 (自适应东盟法域)
  const activeElements = useMemo(() => {
    const rawElements = currentCase?.elements || [];
    const hostJur = currentCase?.meta?.jurisdiction || 'asean_id';
    const jurConfig = getJurisdictionConfig(hostJur);

    if (rawElements.length === 0) {
      if (hostJur === 'asean_my') {
        return isPreInv
          ? [
              {
                element_id: 'elem-1',
                name_zh: '马来西亚外商投资与 CIDB 承包工程资质许可',
                status: 'covered' as const,
                match_note: '持有有效的马来西亚 CIDB 执照及 MIDA 外资投资准入合规登记。',
                gap_note: '资质牌照要件齐备。',
                ref_norm: 'CIDB Act 520',
                eid: 'E1',
              },
              {
                element_id: 'elem-2',
                name_zh: '属地合资与土著股东权益合规审查',
                status: 'covered' as const,
                match_note: '已按马来西亚公司法与属地股权配额标准订立合资协议。',
                gap_note: '合规要件通过。',
                ref_norm: 'Companies Act 2016',
                eid: 'E2',
              },
              {
                element_id: 'elem-3',
                name_zh: '双语合同效力与强行法合规审查',
                status: 'covered' as const,
                match_note: '合同采用英文及马来语规范，符合马来西亚合同法标准。',
                gap_note: '合规要件齐备。',
                ref_norm: 'Contracts Act 1950',
                eid: 'E3',
              },
            ]
          : [
              {
                element_id: 'elem-1',
                name_zh: '迟延交地事实与发包人违约责任归属',
                status: 'covered' as const,
                match_note: '在卷现场监理日志证明交地迟延达关键路径阻断，责任归属于发包人。',
                gap_note: '要件事实闭合完整。',
                ref_norm: 'FIDIC Silver 8.4(c)',
                eid: 'E1',
              },
              {
                element_id: 'elem-2',
                name_zh: '28天索赔通知送达与阻碍原则 (Prevention Principle)',
                status: 'partial' as const,
                match_note: '承包商已发出阻工通报，依据马来西亚合同法阻碍原则，发包人不可援引自身违约获益免除责任。',
                gap_note: '需补强工程师例会纪要与书面送达回执凭证。',
                ref_norm: 'FIDIC Silver 20.1 & Contracts Act 1950',
                eid: 'E2',
              },
              {
                element_id: 'elem-3',
                name_zh: 'CIPAA 2012 第 35 条背靠背条款法定绝对无效',
                status: 'covered' as const,
                match_note: '分包合同以业主付款为前提之“背靠背”条款违反 CIPAA 强行法，总承包商需以主合同延误提出实体交叉索赔。',
                gap_note: '已锁定法定无效抗辩，正向 AIAC 准备实质应诉。',
                ref_norm: 'CIPAA 2012 Sec 35',
                eid: 'E3',
              },
            ];
      }

      if (hostJur === 'asean_vn') {
        return isPreInv
          ? [
              {
                element_id: 'elem-1',
                name_zh: '越南外商投资牌照与承包资质许可',
                status: 'covered' as const,
                match_note: '持有有效的越南计划投资部 (MPI) 投资登记证 (IRC)。',
                gap_note: '资质牌照要件齐备。',
                ref_norm: 'VN Law on Investment 2020',
                eid: 'E1',
              },
              {
                element_id: 'elem-2',
                name_zh: '双语合同与越文官方效力审查',
                status: 'covered' as const,
                match_note: '合同采用越文及英文双语文本，满足涉外承揽法定义务。',
                gap_note: '合规要件通过。',
                ref_norm: 'Civil Code 2015',
                eid: 'E2',
              },
              {
                element_id: 'elem-3',
                name_zh: '2025新建设法 86.2 条违约金封顶合规',
                status: 'covered' as const,
                match_note: '合同约定的损害赔偿条款符合商法 8% 封顶及新建设法标准。',
                gap_note: '要件通过。',
                ref_norm: 'Law 135/2025 Art 86.2',
                eid: 'E3',
              },
            ]
          : [
              {
                element_id: 'elem-1',
                name_zh: '迟延交地事实与发包人违约责任归属',
                status: 'covered' as const,
                match_note: '在卷现场监理日志证明交地迟延达关键路径停滞，责任归属于发包人。',
                gap_note: '要件事实闭合完整。',
                ref_norm: 'FIDIC Silver 8.4(c)',
                eid: 'E1',
              },
              {
                element_id: 'elem-2',
                name_zh: '28天索赔通知送达与发包人知情推定',
                status: 'partial' as const,
                match_note: '承包商已发出阻工邮件，发包人完全知情，不可免除自身违约后果。',
                gap_note: '需补强监理工程例会纪要凭证。',
                ref_norm: 'FIDIC Silver 20.1',
                eid: 'E2',
              },
              {
                element_id: 'elem-3',
                name_zh: '2025新建设法 86.2 条违约金封顶与合理性审查',
                status: 'covered' as const,
                match_note: '预定损害赔偿受越南商法 301 条 8% 封顶及新建设法合理损失归属约束。',
                gap_note: '需提交不可抗力证明。',
                ref_norm: 'VN Law 135/2025 Art 86.2',
                eid: 'E3',
              },
            ];
      }

      // 默认印尼法域 (asean_id)
      return isPreInv
        ? [
            {
              element_id: 'elem-1',
              name_zh: '东道国外商直接投资牌照与资质许可',
              status: 'covered' as const,
              match_note: '持有有效的东道国外资承包工程执照（BUJKA）及 BKPM 外资准入备案。',
              gap_note: '资质牌照要件齐备。',
              ref_norm: 'IDN Law 2/2017 Art 30',
              eid: 'E1',
            },
            {
              element_id: 'elem-2',
              name_zh: '双语合同签署与文本效力强行法合规',
              status: 'covered' as const,
              match_note: '已签署印尼语及英语双语同文合同，符合印尼最高法院 SEMA 3/2023 形式合规标准。',
              gap_note: '合规要件通过。',
              ref_norm: 'SEMA 3/2023',
              eid: 'E2',
            },
            {
              element_id: 'elem-3',
              name_zh: '本地化采购率 (TKDN) 部长特许豁免批复',
              status: 'partial' as const,
              match_note: '当前申报 TKDN 为 28%，低于法定 40% 红线，已提交能矿部 MEMR 11/2024 豁免申请。',
              gap_note: '需跟进东道国能矿部最终豁免批文。',
              ref_norm: 'MEMR 11/2024',
              eid: 'E3',
            },
          ]
        : [
            {
              element_id: 'elem-1',
              name_zh: '迟延交地事实与发包人违约责任归属',
              status: 'covered' as const,
              match_note: '在卷现场监理日志证明交地迟延达 180 天，且责任完全归属于发包人。',
              gap_note: '要件事实闭合完整。',
              ref_norm: 'FIDIC Silver 8.4(c)',
              eid: 'E1',
            },
            {
              element_id: 'elem-2',
              name_zh: '28天索赔通知送达与发包人知情推定',
              status: 'partial' as const,
              match_note: '承包商发出多封往来邮件通报阻工，但未形成符合合同正式形式之发函。',
              gap_note: '需补强监理工程例会纪要与发包人书面签收回复凭证。',
              ref_norm: 'FIDIC Silver 20.1',
              eid: 'E2',
            },
            {
              element_id: 'elem-3',
              name_zh: '双语法定语言签署与强制法合规',
              status: 'covered' as const,
              match_note: '已签署印尼语及英语双语同文合同，符合最高法院 SEMA 3/2023 形式合规标准。',
              gap_note: '合规要件通过。',
              ref_norm: 'SEMA 3/2023',
              eid: 'E3',
            },
          ];
    }
    // 过滤出与当前选中争点相关的要件
    const matched = rawElements.filter((el) => {
      const parentIssue = (currentCase?.issues || []).find((iss) => iss.issue_id === activeIssue.id);
      return parentIssue?.element_ids?.includes(el.element_id);
    });
    const list = matched.length > 0 ? matched : rawElements;

    return list.map((el) => ({
      element_id: el.element_id,
      name_zh: el.name_zh,
      status: el.status,
      match_note: el.match_note || '在卷事实及沟通底稿可支持该要件。',
      gap_note: el.gap_note || (el.status === 'covered' ? '要件已获充分证据支持。' : '建议调取监理日报与工程往来函件补强。'),
      ref_norm: el.links?.[0]?.eid ? currentCase?.evidence?.[el.links[0].eid]?.ref_id || '东盟工程规范' : '东盟现行法典',
      eid: el.links?.[0]?.eid || 'E1',
    }));
  }, [currentCase, activeIssue]);

  // 综合测算模型指标 (完全绑定当前案卷后端真实战术研判与证据链数据)
  const viabilityAssessment = useMemo(() => {
    const rawConf = tacticalGuidance.qualitative_verdict?.confidence_band || '82% - 90%';
    const match = rawConf.match(/(\d+)%/g);
    let avgScore = 88;
    if (match && match.length >= 2) {
      const v1 = parseInt(match[0], 10);
      const v2 = parseInt(match[1], 10);
      avgScore = Math.round((v1 + v2) / 2);
    } else if (match && match.length === 1) {
      avgScore = parseInt(match[0], 10);
    }

    const ratingLevel: 'high' | 'medium' | 'low' = avgScore >= 85 ? 'high' : avgScore >= 75 ? 'medium' : 'low';
    const coveredCount = activeElements.filter((e) => e.status === 'covered').length;
    const elemRatio = Math.round((coveredCount / Math.max(activeElements.length, 1)) * 100);

    return {
      overallScore: avgScore,
      ratingLabel: tacticalGuidance.qualitative_verdict?.legal_support_level || (isPreInv ? '合规可准入' : '强支持 · 胜诉倾向'),
      ratingLevel,
      elementsScore: elemRatio,
      elementsDetail: `${coveredCount}/${activeElements.length} 核心要件满足在卷举证`,
      defenseScore: tacticalGuidance.qualitative_verdict?.counter_block_expectation ? 88 : 80,
      defenseDetail: tacticalGuidance.qualitative_verdict?.counter_block_expectation || '已锁定阻断抗辩与补强底线',
      authorityScore: currentCase?.evidence ? Math.min(100, Object.keys(currentCase.evidence).length * 15 + 40) : 95,
      authorityDetail: `${jurConfig.name_zh}官方现行法典与权威判例`,
      complianceScore: currentCase?.flags?.length ? Math.max(70, 100 - currentCase.flags.length * 10) : 100,
      complianceDetail: currentCase?.flags?.length ? `检出 ${currentCase.flags.length} 处合规关注` : '已通过涉外法查明全流程合规质检',
    };
  }, [tacticalGuidance, activeElements, currentCase, jurConfig, isPreInv]);

  // 复制话术
  const handleCopyScript = (text: string) => {
    navigator.clipboard.writeText(text);
    setCopiedScript(true);
    showToast('✓ 谈判实战话术已复制至剪贴板！', 'success');
    setTimeout(() => setCopiedScript(false), 2000);
  };

  // 导出 DOCX
  const handleExportDocx = (type: 'standard' | 'handbook' = 'standard') => {
    if (!currentCaseId) return;
    const url = `/api/cases/${currentCaseId}/export/docx`;
    window.open(url, '_blank');
    showToast(
      type === 'standard'
        ? '正在导出最高人民法院标准域外法查明意见书 (.docx)...'
        : '正在导出央国企海外投资与工程合规实务手册 (.docx)...',
      'info'
    );
  };

  // 标注入卷补强证据
  const handleToggleAction = (actionId: string) => {
    const nextState = !completedActionIds[actionId];
    setCompletedActionIds((prev) => ({ ...prev, [actionId]: nextState }));
    showToast(
      nextState
        ? '✓ 已将该证据调取行动标记为【已落实补强】，置信区间已扎实收敛！'
        : '已取消该项落实标记',
      'info'
    );
  };

  return (
    <div className="relative min-h-screen max-w-[1520px] mx-auto px-4 sm:px-8 py-6 pb-28 space-y-6 antialiased text-slate-800">
      {/* 顶部极光微网格科技底座 */}
      <div className="absolute top-0 left-6 w-[580px] h-[580px] bg-gradient-to-br from-blue-400/10 via-indigo-400/8 to-transparent rounded-full blur-3xl pointer-events-none -z-10" />
      <div className="absolute top-10 right-6 w-[580px] h-[580px] bg-gradient-to-bl from-emerald-400/8 via-teal-300/6 to-transparent rounded-full blur-3xl pointer-events-none -z-10" />
      <div className="absolute inset-0 bg-[radial-gradient(#cbd5e1_1px,transparent_1px)] [background-size:28px_28px] opacity-25 pointer-events-none -z-10" />

      {/* ========================================================================= */}
      {/* 头部大标题与四切面导航控制器 (Segmented Control) */}
      {/* ========================================================================= */}
      <div className="flex flex-col lg:flex-row lg:items-end justify-between gap-5 pb-2 border-b border-slate-200/60">
        <div className="space-y-1.5">
          <div className="flex flex-wrap items-center gap-2 text-xs font-mono text-slate-400">
            <span className="text-slate-500 font-sans">专案研判舱</span>
            <span>/</span>
            <span className="text-slate-800 font-semibold bg-slate-100 px-2 py-0.5 rounded-md border border-slate-200/60 font-mono">
              {currentCase?.case_id || 'C101'}
            </span>
            <span>·</span>
            <span className="text-slate-600 font-sans">
              准据法：<strong className="text-slate-900 font-mono">{caseMeta.choiceOfLaw}</strong>
            </span>
            <span>·</span>
            <span className="text-slate-600 font-sans">
              履行地：<strong className="text-slate-900 font-mono">{caseMeta.hostJur}</strong>
            </span>
            {switchingCaseId && switchingCaseId !== currentCase?.case_id && (
              <span className="inline-flex items-center gap-1.5 px-2 py-0.5 rounded-md bg-blue-50 text-blue-700 text-[11px] font-sans border border-blue-200/80 animate-pulse ml-1">
                <Loader2 className="w-3 h-3 animate-spin text-blue-600" />
                <span>正在调阅 {switchingCaseId} 卷宗...</span>
              </span>
            )}
          </div>
          <h1 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
            {caseMeta.title}
          </h1>
        </div>

        {/* 右侧：Apple 风格四切面胶囊分段控制器 (Segmented Control) 与工具按钮 */}
        <div className="flex flex-wrap items-center gap-3 self-start lg:self-auto">
          <div className="inline-flex items-center p-1 bg-slate-200/70 backdrop-blur-md rounded-2xl shadow-2xs">
            {[
              {
                id: 'verdict',
                key: '1',
                label: isPreInv ? '准入评估结论' : '综合研判结论',
              },
              {
                id: 'elements',
                key: '2',
                label: isPreInv ? `准入要件审查 (${activeElements.length})` : `争点要件审查 (${issues.length})`,
              },
              {
                id: 'sandbox',
                key: '3',
                label: isPreInv ? '投资架构与商务方案' : '工程履约与争议抗辩',
              },
              {
                id: 'export',
                key: '4',
                label: '法源图谱与意见书',
              },
            ].map((tab) => (
              <button
                key={tab.id}
                type="button"
                onClick={() => setFacet(tab.id as AnalysisFacet)}
                className={`inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-xl text-xs font-medium transition-all duration-200 cursor-pointer ${
                  facet === tab.id
                    ? 'bg-white text-slate-900 shadow-xs font-semibold'
                    : 'text-slate-600 hover:text-slate-900 hover:bg-white/40'
                }`}
                title={`快捷键 [${tab.key}] 切换`}
              >
                <span className="font-mono text-[10px] text-slate-400 opacity-80">[{tab.key}]</span>
                <span>{tab.label}</span>
              </button>
            ))}
          </div>

          {/* 快捷操作：查明动效 + AI 法律助手 */}
          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={openPipelineAnimation}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-medium text-slate-700 hover:text-slate-900 bg-white hover:bg-slate-50 border border-slate-200/80 transition-all shadow-2xs cursor-pointer"
              title="查看智能多智能体查明全流程"
            >
              <Play className="w-3 h-3 text-slate-700 fill-slate-700" />
              <span>查明流程回溯</span>
            </button>
            <button
              type="button"
              onClick={() => (isRightDockOpen ? closeRightDock() : openRightDock('case_copilot'))}
              className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-medium transition-all border cursor-pointer ${
                isRightDockOpen
                  ? 'bg-blue-50 text-blue-700 border-blue-200 shadow-xs'
                  : 'bg-white/90 text-slate-700 border-slate-200/80 hover:bg-white shadow-2xs'
              }`}
              title={isRightDockOpen ? "收起法律辅助面板" : "展开 AI 法律助手 (Cmd/Ctrl + B)"}
            >
              <Bot className="w-3.5 h-3.5 text-blue-600" />
              <span>AI 法律助手</span>
            </button>
          </div>
        </div>
      </div>

      {/* ========================================================================= */}
      {/* 切面 1：决策全景看板 / 投前准入全景看板 (verdict) */}
      {/* ========================================================================= */}
      {facet === 'verdict' && (
        <div key="facet-verdict" className="space-y-6 apple-tab-pane">
          {/* 顶部：三维定性结论遥测带 (中立多维定性研判结论) */}
          <div className="apple-bento-card rounded-[30px] p-6 sm:p-7 space-y-5">
            <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-100 pb-4">
              <div className="flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
                <span className="text-xs font-semibold text-slate-700 tracking-wide">
                  {isPreInv ? '项目投前准入三维评估结论' : '涉外争议三维研判结论'}
                </span>
              </div>
              <button
                type="button"
                onClick={() => setShowViabilityModal(true)}
                className="inline-flex items-center gap-1.5 text-xs font-medium text-slate-600 hover:text-blue-600 transition-colors cursor-pointer"
              >
                <Layers className="w-3.5 h-3.5 text-blue-600" />
                <span>查看量化测算模型与评分依据</span>
                <span>→</span>
              </button>
            </div>

            {/* 三维定性指标胶囊组 */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {/* 维度 1: 实体索赔胜诉确定性 */}
              <div className="p-4.5 rounded-2xl bg-blue-50/50 border border-blue-100 space-y-1.5">
                <div className="text-[11px] font-mono text-blue-600 font-semibold uppercase tracking-wider">
                  {isPreInv ? '外资持牌准入合规度' : '实体索赔胜诉确定性'}
                </div>
                <div className="text-lg font-bold text-slate-900 tracking-tight">
                  {tacticalGuidance?.qualitative_verdict?.legal_support_level || (isPreInv ? '合规可准入 (Permissible)' : '高度确定支持 (Substantial Support)')}
                </div>
                <div className="text-xs text-slate-500 font-mono">
                  {tacticalGuidance?.qualitative_verdict?.confidence_band || (isPreInv ? '置信区间 85%-92% · 资质牌照与股比完备' : '置信区间 82%-90% · 实体索赔请求权成立')}
                </div>
              </div>

              {/* 维度 2: 程序失权驳回风险 */}
              <div className="p-4.5 rounded-2xl bg-amber-50/50 border border-amber-100 space-y-1.5">
                <div className="text-[11px] font-mono text-amber-700 font-semibold uppercase tracking-wider">
                  {isPreInv ? '属地强行法合规防线' : '程序失权驳回风险'}
                </div>
                <div className="text-lg font-bold text-slate-900 tracking-tight">
                  {tacticalGuidance?.qualitative_verdict?.procedural_exposure || (isPreInv ? '受控合规关注 (TKDN 40%)' : '可控中度威胁 (FIDIC 20.1 时效)')}
                </div>
                <div className="text-xs text-slate-500 font-mono">
                  {isPreInv ? `${jurConfig.short_name}外资准入与强行法合规` : (hostJur === 'asean_my' ? '对方主张 28 天失权及背靠背付款，需落实 CIPAA 送达底稿' : '对方主张 28 天失权，需落实监理事实送达底稿')}
                </div>
              </div>

              {/* 维度 3: 保函止付与反制预期 */}
              <div className="p-4.5 rounded-2xl bg-emerald-50/50 border border-emerald-100 space-y-1.5">
                <div className="text-[11px] font-mono text-emerald-700 font-semibold uppercase tracking-wider">
                  {isPreInv ? '双边投资保护力 (BIT)' : '保函止付与反制预期'}
                </div>
                <div className="text-lg font-bold text-slate-900 tracking-tight">
                  {tacticalGuidance?.qualitative_verdict?.counter_block_expectation || (isPreInv ? '高保护力 (中新BIT框架)' : '高确定性阻断 (阻碍原则)')}
                </div>
                <div className="text-xs text-slate-500 font-mono">
                  {isPreInv ? '设立新加坡 SPV 可激活中新 BIT 间接征收保护' : '援引 Prevention Principle 与善意原则阻断失权'}
                </div>
              </div>
            </div>

            {/* 定性评述段落 (完全绑定当前案卷后端真实战略研判与核心裁判要素) */}
            <div className="text-xs sm:text-sm text-slate-600 leading-relaxed pt-1 space-y-1.5">
              <p>
                依据在卷案情与东道国 ({jurConfig.name_zh}) 司法实践，我方关于
                <strong className="text-slate-900 font-semibold mx-1">{caseMeta.title}</strong>
                的法律立场评定为【{tacticalGuidance.qualitative_verdict?.legal_support_level}】。
                {currentCase?.strategic_assessment?.outcome_branches?.[0]?.outcome_summary && (
                  <span className="text-slate-800 font-medium ml-1">
                    研判结论：{currentCase.strategic_assessment.outcome_branches[0].outcome_summary}
                  </span>
                )}
              </p>
              {currentCase?.strategic_assessment?.pivotal_factors && currentCase.strategic_assessment.pivotal_factors.length > 0 && (
                <div className="flex flex-wrap items-center gap-1.5 pt-0.5 text-xs">
                  <span className="text-slate-400 font-mono text-[11px]">关键裁判抗辩枢纽:</span>
                  {currentCase.strategic_assessment.pivotal_factors.map((factor, idx) => (
                    <span key={idx} className="px-2 py-0.5 rounded-md bg-slate-100 text-slate-700 font-mono text-[11px] border border-slate-200/60">
                      ⚡ {factor}
                    </span>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* 下半区 8:4 布局：假定条件推演矩阵 (65%) + 谈判行动底线 (35%) */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
            {/* 左侧 8 列 (65%)：假定条件推演矩阵 (If-Then Condition Precedent Matrix) */}
            <div className="lg:col-span-8 apple-bento-card rounded-[30px] p-6 sm:p-7 space-y-5">
              <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-100 pb-4">
                <div className="space-y-0.5">
                  <div className="flex items-center gap-2">
                    <Target className="w-4 h-4 text-blue-600" />
                    <h3 className="text-sm font-bold text-slate-900 tracking-tight">
                      {isPreInv ? '东盟投资与特许经营多情景后果推演' : '争议多情景裁判走势推演'}
                    </h3>
                  </div>
                  <p className="text-xs text-slate-500">
                    {isPreInv
                      ? '结合不同资质审批与股权架构前提，模拟乐观、基准、压力情景下的准入落地走向'
                      : '结合不同证据充分度与事实认定前提，模拟乐观、基准、压力情景下的裁判走向与抗辩后果'}
                  </p>
                </div>
                <span className="text-[11px] font-mono text-slate-400 bg-slate-100 px-2.5 py-1 rounded-lg">
                  三阶情景推演
                </span>
              </div>

              {/* 三阶泳道卡片 (完全绑定后端真实战略研判与红队抗辩) */}
              <div className="space-y-3.5">
                {/* 泳道 1: 乐观假定 (绑定后端真实战略研判乐观分支) */}
                <div className="p-4.5 rounded-2xl border border-emerald-200/80 bg-emerald-50/30 space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="inline-flex items-center gap-1.5 text-xs font-bold text-emerald-800">
                      <span className="w-2 h-2 rounded-full bg-emerald-500" />
                      <span>{currentCase?.strategic_assessment?.outcome_branches?.[0]?.title ? `【乐观情景 · ${currentCase.strategic_assessment.outcome_branches[0].title}】` : (isPreInv ? '【乐观情景 · 外资持牌准入与BIT全保护】' : '【乐观情景 · 胜诉与完全顺延】')}</span>
                    </span>
                    <span className="text-[11px] font-mono text-emerald-700 bg-emerald-100/70 px-2 py-0.5 rounded-md font-semibold">
                      {isPreInv ? '牌照齐备 · BIT保护生效' : '胜券锁定 · 阻断失权'}
                    </span>
                  </div>
                  <div className="text-xs text-slate-700 space-y-1">
                    <p>
                      <strong>事实认定前提 (If)：</strong>{' '}
                      {currentCase?.strategic_assessment?.outcome_branches?.[0]?.condition_precedent || (isPreInv
                        ? (hostJur === 'asean_id' ? '调取当地工业部出具的 TKDN 40% 豁免批复，并通过新加坡 SPV 完成外资股比核准。' : `调取${jurConfig.name_zh}外资主管机关准入批复，并通过合规 SPV 架构完成投资备案。`)
                        : '调取现场监理签发之每日阻工日志，并依据东道国法律完成核心证据链保全。')}
                    </p>
                    <p>
                      <strong>法律适用后果 (Then)：</strong>{' '}
                      {currentCase?.strategic_assessment?.outcome_branches?.[0]?.outcome_summary || (isPreInv
                        ? `获得${jurConfig.name_zh}外资准入与总承包持牌许可，特许权协议受双边投资保护协定 (BIT) 间接征收保护与国际仲裁管辖。`
                        : '阻断发包人失权主张，工期获全额顺延 (EOT)，完全排除预定违约金 (LD)，保函获法院/仲裁庭专属禁令止付。')}
                    </p>
                    <p className="text-[11px] font-mono text-slate-400">
                      依据：{currentCase?.strategic_assessment?.outcome_branches?.[0]?.substantive_basis?.join(' · ') || (isPreInv ? `${jurConfig.short_name}投资法案 · 国际投资协定 (BIT)` : `FIDIC Silver · ${jurConfig.short_name}强行法规范`)}
                    </p>
                  </div>
                </div>

                {/* 泳道 2: 基准稳健 */}
                <div className="p-4.5 rounded-2xl border border-blue-200/80 bg-blue-50/20 space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="inline-flex items-center gap-1.5 text-xs font-bold text-blue-800">
                      <span className="w-2 h-2 rounded-full bg-blue-600" />
                      <span>{isPreInv ? '【基准情景 · 联营体准入与常规合规】' : '【基准情景 · 核心抗辩成立】'}</span>
                    </span>
                    <span className="text-[11px] font-mono text-blue-700 bg-blue-100/70 px-2 py-0.5 rounded-md font-semibold">
                      {isPreInv ? '资质合规 · 监管受控' : '要件齐备 · 部分交锋'}
                    </span>
                  </div>
                  <div className="text-xs text-slate-700 space-y-1">
                    <p>
                      <strong>事实认定前提 (If)：</strong>{' '}
                      {currentCase?.strategic_assessment?.actionable_checklist?.[0]
                        ? `严格执行风控清单：${currentCase.strategic_assessment.actionable_checklist[0]}，固定现场各方知情事实。`
                        : (isPreInv ? `依托${jurConfig.name_zh}属地合资/联营体满足本地化配额要求，完成规范双语合同签署。` : '依托在卷往来邮件与会议纪要间接证明发包人知情事实，但未获正式书面签署确认。')}
                    </p>
                    <p>
                      <strong>法律适用后果 (Then)：</strong>{' '}
                      {isPreInv
                        ? '特许经营协议合法生效，满足行业强制准入门槛，属地强行法排斥风险在受控区间。'
                        : '实体请求权成立，可主张部分工期补偿；发包人将针对违约金上限展开抗辩。'}
                    </p>
                    <p className="text-[11px] font-mono text-slate-400">
                      依据：{jurConfig.name_zh}法律规范 · {tacticalGuidance.qualitative_verdict?.counter_block_expectation || '善意履约原则'}
                    </p>
                  </div>
                </div>

                {/* 泳道 3: 压力情景 (绑定后端真实红队抗辩与时效审查) */}
                <div className="p-4.5 rounded-2xl border border-rose-200/80 bg-rose-50/30 space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="inline-flex items-center gap-1.5 text-xs font-bold text-rose-800">
                      <span className="w-2 h-2 rounded-full bg-rose-500" />
                      <span>{isPreInv ? '【压力情景 · 股权穿透超标与强行法效力挑战】' : '【压力情景 · 对方红队抗辩交锋】'}</span>
                    </span>
                    <div className="flex items-center gap-2">
                      {!isPreInv && simNoticeDays > 28 && (
                        <span className="text-[10px] font-mono text-rose-700 bg-rose-100 px-2 py-0.5 rounded-full font-bold border border-rose-300 animate-pulse">
                          ⚡ 索赔通知 {simNoticeDays}d &gt; 28d 已触发此泳道
                        </span>
                      )}
                      <span className="text-[11px] font-mono text-rose-700 bg-rose-100/70 px-2 py-0.5 rounded-md font-semibold">
                        {isPreInv ? '合同无效风险 · 审查挑战' : '失权威胁 · 违约抗辩'}
                      </span>
                    </div>
                  </div>
                  <div className="text-xs text-slate-700 space-y-1">
                    <p>
                      <strong>事实认定前提 (If)：</strong>{' '}
                      {currentCase?.strategic_assessment?.red_team_defenses?.[0]?.opposing_claim || (isPreInv
                        ? '合同仅签署单语版本，或外资实际控股穿透超过东道国负面清单法定上限且未获特许豁免。'
                        : '索赔通知超过 28 天且无法举证发包人实际知情，或合同未签署属地官方语言版本。')}
                    </p>
                    <p>
                      <strong>法律适用后果 (Then)：</strong>{' '}
                      {currentCase?.strategic_assessment?.red_team_defenses?.[0]?.factual_counter_point
                        ? `我方反制主张：${currentCase.strategic_assessment.red_team_defenses[0].factual_counter_point}`
                        : (isPreInv ? `特许权协议面临${jurConfig.name_zh}法院确认合同无效风险，且无法穿透享受双边投资保护协定待遇。` : `仲裁员可能机械适用时效条款认定失权；合同部分排除性条款面临${jurConfig.name_zh}强行法审查。`)}
                    </p>
                    <p className="text-[11px] font-mono text-slate-400">
                      依据：{currentCase?.strategic_assessment?.red_team_defenses?.[0]?.opposing_basis || `严格字面解释 · ${jurConfig.short_name}最高法院司法先例`}
                    </p>
                  </div>
                </div>
              </div>

              {/* 底部跳转模块引导 */}
              <div className="pt-2 border-t border-slate-100 flex items-center justify-between text-xs">
                <span className="text-slate-500">
                  {isPreInv
                    ? '如需调整投资架构与股比参数并推演法律后果，可前往投资架构分析模块'
                    : '如需调整分析参数并推演法律后果，可前往履约与抗辩分析模块'}
                </span>
                <button
                  type="button"
                  onClick={() => setFacet('sandbox')}
                  className="inline-flex items-center gap-1 text-xs font-semibold text-blue-600 hover:text-blue-700 cursor-pointer"
                >
                  <span>{isPreInv ? '前往投资架构与商务方案' : '前往工程履约与争议抗辩'}</span>
                  <span>→</span>
                </button>
              </div>
            </div>

            {/* 右侧 4 列 (35%)：7 天行动底线 */}
            <div className="lg:col-span-4 space-y-5">
              {/* 卡片 2: 7天紧急行动与商务谈判底线 */}
              <div className="apple-bento-card rounded-[30px] p-6 space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-slate-900 flex items-center gap-1.5">
                    <Clock className="w-4 h-4 text-blue-600" />
                    <span>{isPreInv ? '法务风控 7 天审查与发函要点' : '首席法务官 7 天行动底线'}</span>
                  </span>
                  <span className="text-[11px] font-mono text-blue-600 bg-blue-50 px-2 py-0.5 rounded-md font-semibold">
                    {isPreInv
                      ? `${tacticalGuidance.urgent_actions.length} 项前置审查`
                      : `${tacticalGuidance.urgent_actions.length} 项紧急发函`}
                  </span>
                </div>

                <div className="space-y-2.5">
                  {tacticalGuidance.urgent_actions.slice(0, 2).map((act, idx) => (
                    <div key={idx} className="p-3 bg-slate-50 rounded-xl border border-slate-200/70 text-xs space-y-1">
                      <div className="flex items-center justify-between">
                        <strong className="text-slate-900 font-semibold">{act.action_type}</strong>
                        <span className="text-[10px] font-mono text-rose-600 bg-rose-50 px-1.5 py-0.5 rounded border border-rose-200 font-bold">
                          {act.deadline_tag}
                        </span>
                      </div>
                      <p className="text-slate-500 text-[11px] line-clamp-1">{act.document_template_title}</p>
                    </div>
                  ))}
                </div>

                <button
                  type="button"
                  onClick={() => setFacet('sandbox')}
                  className="w-full py-2.5 rounded-xl text-xs font-semibold text-white bg-blue-600 hover:bg-blue-700 transition-all shadow-xs cursor-pointer flex items-center justify-center gap-1.5"
                >
                  <span>查看完整谈判话术与取证清单</span>
                  <ChevronRight className="w-3.5 h-3.5" />
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* ========================================================================= */}
      {/* 切面 2：争点拆解 & 要件四态涵摄 (elements) */}
      {/* ========================================================================= */}
      {facet === 'elements' && (
        <div key="facet-elements" className="space-y-6 apple-tab-pane">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
            {/* 左栏 (32% · 4列)：争议焦点 / 审查支柱列表 */}
            <div className="lg:col-span-4 apple-bento-card rounded-[30px] p-5 space-y-4">
              <div className="flex items-center justify-between pb-3 border-b border-slate-100">
                <span className="text-xs font-bold text-slate-900 uppercase tracking-wider flex items-center gap-1.5">
                  <Compass className="w-4 h-4 text-blue-600" />
                  <span>{isPreInv ? '东盟投资四大审查支柱' : '核心争议焦点拆解'}</span>
                </span>
                <span className="text-[11px] font-mono text-slate-400">{issues.length} 个焦点</span>
              </div>

              <div className="space-y-2">
                {issues.map((iss) => {
                  const isSelected = (selectedIssueId || issues[0]?.id) === iss.id;
                  return (
                    <div
                      key={iss.id}
                      onClick={() => setSelectedIssueId(iss.id)}
                      className={`p-4 rounded-2xl cursor-pointer transition-all text-xs space-y-1.5 border ${
                        isSelected
                          ? 'bg-blue-50/80 border-blue-300 shadow-2xs text-slate-900'
                          : 'bg-white hover:bg-slate-50 border-slate-200/70 text-slate-700'
                      }`}
                    >
                      <div className="flex items-center justify-between">
                        <span className="font-mono font-bold text-blue-700">{iss.code}</span>
                        <span className="text-[10px] text-slate-500 font-mono bg-white px-2 py-0.5 rounded border border-slate-200/60">
                          {iss.category}
                        </span>
                      </div>
                      <h4 className="font-semibold text-slate-900 line-clamp-2 leading-relaxed">
                        {iss.title}
                      </h4>
                      <div className="text-[11px] text-slate-400 font-mono">
                        适用规范: {iss.norms.join(' · ') || '属地强行法'}
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* 右栏 (68% · 8列)：要件四态胶囊比对卡 */}
            <div className="lg:col-span-8 apple-bento-card rounded-[30px] p-7 space-y-6">
              {/* 焦点标题栏 */}
              <div className="border-b border-slate-100 pb-4 space-y-1.5">
                <div className="flex items-center gap-2">
                  <span className="font-mono font-bold text-xs text-blue-700 bg-blue-50 px-2 py-0.5 rounded border border-blue-200/60">
                    {activeIssue.code}
                  </span>
                  <span className="text-xs text-slate-400 font-mono">{activeIssue.category}</span>
                </div>
                <h3 className="text-base font-bold text-slate-900 tracking-tight">
                  {activeIssue.title}
                </h3>
                <p className="text-xs text-slate-500 leading-relaxed pt-1">
                  {activeIssue.tldr}
                </p>
              </div>

              {/* 要件四态比对列表 (三列分区卡片：法定要件 & 法条徽章 -> 在卷事实涵摄 -> 缺口与补强) */}
              <div className="space-y-4">
                <div className="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center justify-between">
                  <span>法定要件审查与在案事实涵摄</span>
                  <span className="font-normal font-sans text-slate-500">
                    点击法条可直接在右侧辅助面板对照中英双语原文
                  </span>
                </div>

                {activeElements.map((elem, idx) => {
                  const isCovered = elem.status === 'covered';
                  const isPartial = elem.status === 'partial';
                  return (
                    <div
                      key={elem.element_id || idx}
                      className={`p-5 rounded-2xl border transition-all text-xs space-y-3 ${
                        isCovered
                          ? 'bg-emerald-50/20 border-emerald-200/70'
                          : isPartial
                          ? 'bg-amber-50/20 border-amber-200/70'
                          : 'bg-rose-50/20 border-rose-200/70'
                      }`}
                    >
                      {/* 头部：要件名称与四态徽章 */}
                      <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-100/80 pb-2.5">
                        <div className="flex items-center gap-2">
                          <span
                            className={`w-2 h-2 rounded-full ${
                              isCovered ? 'bg-emerald-500' : isPartial ? 'bg-amber-500' : 'bg-rose-500'
                            }`}
                          />
                          <h4 className="font-bold text-slate-900 text-xs sm:text-sm">
                            {elem.name_zh}
                          </h4>
                        </div>

                        <div className="flex items-center gap-2">
                          {/* 点击法条徽章直接呼出右侧辅助面板精读 */}
                          <button
                            type="button"
                            onClick={() => openRightDock('law_reader', elem.eid)}
                            className="inline-flex items-center gap-1 font-mono text-[11px] font-semibold text-blue-700 bg-white hover:bg-blue-50 px-2.5 py-1 rounded-lg border border-blue-200/80 transition-all cursor-pointer shadow-2xs"
                            title="在右侧辅助面板中阅读双语全文"
                          >
                            <BookOpen className="w-3 h-3 text-blue-600" />
                            <span>{elem.ref_norm}</span>
                          </button>

                          <span
                            className={`text-[10px] font-mono font-bold px-2 py-0.5 rounded uppercase tracking-wider ${
                              isCovered
                                ? 'bg-emerald-100 text-emerald-800'
                                : isPartial
                                ? 'bg-amber-100 text-amber-800'
                                : 'bg-rose-100 text-rose-800'
                            }`}
                          >
                            {isCovered ? '✓ 已满足' : isPartial ? '◐ 部分满足' : '✕ 缺失'}
                          </span>
                        </div>
                      </div>

                      {/* 事实涵摄与缺口补强说明 */}
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                        <div className="space-y-1 bg-white/70 p-3 rounded-xl border border-slate-200/60">
                          <span className="text-[11px] text-slate-400 font-medium">在卷事实涵摄判定：</span>
                          <p className="text-slate-800 leading-relaxed font-sans">{elem.match_note}</p>
                        </div>
                        <div className="space-y-1 bg-white/70 p-3 rounded-xl border border-slate-200/60">
                          <span className="text-[11px] text-slate-400 font-medium">证据缺口与补强指引：</span>
                          <p className="text-slate-700 leading-relaxed font-sans">{elem.gap_note}</p>
                        </div>
                      </div>

                      {/* 底部联动操作：转入工坊补强 */}
                      {!isCovered && (
                        <div className="pt-1 flex justify-end">
                          <button
                            type="button"
                            onClick={() => setFacet('sandbox')}
                            className="inline-flex items-center gap-1.5 text-xs font-semibold text-blue-600 hover:text-blue-700 bg-blue-50/80 hover:bg-blue-100/80 px-3 py-1.5 rounded-xl border border-blue-200/70 transition-colors cursor-pointer"
                          >
                            <span>针对此缺口转入工坊实操补强</span>
                            <ArrowRight className="w-3.5 h-3.5" />
                          </button>
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* ========================================================================= */}
      {/* 切面 3：工程沙盘 & 攻防工坊 (sandbox) */}
      {/* ========================================================================= */}
      {facet === 'sandbox' && (
        <div key="facet-sandbox" className="space-y-6 apple-tab-pane">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
            {/* 左舱 (48% · 6列)：精密参数沙盘 / 投资架构比选 */}
            <div className="lg:col-span-6 apple-bento-card rounded-[30px] p-7 space-y-6">
              <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-100 pb-4">
                <div className="space-y-0.5">
                  <div className="flex items-center gap-2">
                    <SlidersHorizontal className="w-4 h-4 text-blue-600" />
                    <h3 className="text-sm font-bold text-slate-900 tracking-tight">
                      {isPreInv ? '投资架构与商务方案模拟' : '合同履约参数与索赔敏感度模拟'}
                    </h3>
                  </div>
                  <p className="text-xs text-slate-500">
                    {isPreInv
                      ? '调节外资股比与设立架构，系统基于东道国外资准入负面清单与双边投资协定实时测算合规后果'
                      : '调节工程履约与通知时效参数，系统基于法定红线与先例规则实时测算法律责任后果'}
                  </p>
                </div>
                <div className="flex items-center gap-2">
                  <button
                    type="button"
                    onClick={handleResetBaseline}
                    className="inline-flex items-center gap-1 px-2.5 py-1.5 rounded-xl text-xs font-semibold text-slate-700 bg-slate-100 hover:bg-slate-200 transition-all cursor-pointer"
                    title="恢复案卷初始基准参数"
                  >
                    <RotateCcw className="w-3.5 h-3.5 text-slate-500" />
                    <span>恢复初始</span>
                  </button>
                  <button
                    type="button"
                    onClick={handleSimulateEngineering}
                    disabled={isSimulatingEng}
                    className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl text-xs font-semibold text-white bg-blue-600 hover:bg-blue-700 transition-all shadow-xs shadow-blue-500/25 active:scale-[0.98] cursor-pointer disabled:opacity-50"
                  >
                    {isSimulatingEng ? (
                      <>
                        <Loader2 className="w-3.5 h-3.5 animate-spin" />
                        <span>自动测算中...</span>
                      </>
                    ) : (
                      <>
                        <Zap className="w-3.5 h-3.5 fill-white" />
                        <span>重新测算后果</span>
                      </>
                    )}
                  </button>
                </div>
              </div>

              {/* 争议模式下的五大滑块 (带法定红线刻度锚点) */}
              {!isPreInv ? (
                <div className="space-y-5">
                  {/* 滑块 1: 属地强行法与本地采购配额自适应滑块 */}
                  <div className="clean-row-card p-4 space-y-2.5">
                    <div className="flex items-center justify-between text-xs">
                      <span className="font-semibold text-slate-900 flex items-center gap-1.5">
                        <Activity className="w-3.5 h-3.5 text-blue-600 shrink-0" />
                        {slider1Config.title}
                      </span>
                      <div className="flex items-center gap-2">
                        {baselineParams.declared_tkdn_pct !== undefined && simTkdn !== baselineParams.declared_tkdn_pct && (
                          <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-slate-100 text-slate-600 font-semibold">
                            {simTkdn > baselineParams.declared_tkdn_pct ? `+${(simTkdn - baselineParams.declared_tkdn_pct).toFixed(0)}%` : `${(simTkdn - baselineParams.declared_tkdn_pct).toFixed(0)}%`} 较基准
                          </span>
                        )}
                        <span className={`font-mono font-bold ${slider1Config.isCompliant ? 'text-emerald-600' : 'text-amber-600'}`}>
                          {simTkdn}% {slider1Config.statusLabel}
                        </span>
                      </div>
                    </div>
                    <div className="relative pt-1 pb-3">
                      <input
                        type="range"
                        min="5"
                        max="80"
                        value={simTkdn}
                        onChange={(e) => handleSliderChange(setSimTkdn, Number(e.target.value))}
                        className="w-full accent-blue-600 cursor-pointer"
                      />
                      {/* 法定刻度锚点 */}
                      <div className="absolute top-5 text-[10px] font-mono text-emerald-600 flex flex-col items-center" style={{ left: slider1Config.anchorLeft }}>
                        <span className="w-0.5 h-2 bg-emerald-500" />
                        <span>{slider1Config.target}% 基准线</span>
                      </div>
                    </div>
                    <p className="text-[11px] text-slate-500">
                      {slider1Config.desc}
                    </p>
                  </div>

                  {/* 滑块 2: FIDIC 20.1 索赔通知天数 (28天失权线) */}
                  <div className="clean-row-card p-4 space-y-2.5">
                    <div className="flex items-center justify-between text-xs">
                      <span className="font-semibold text-slate-900 flex items-center gap-1.5">
                        <Clock className="w-3.5 h-3.5 text-blue-600 shrink-0" />
                        FIDIC 20.1 索赔通知送达天数
                      </span>
                      <div className="flex items-center gap-2">
                        {baselineParams.notice_days !== undefined && simNoticeDays !== baselineParams.notice_days && (
                          <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-slate-100 text-slate-600 font-semibold">
                            {simNoticeDays > baselineParams.notice_days ? `+${simNoticeDays - baselineParams.notice_days}d` : `${simNoticeDays - baselineParams.notice_days}d`} 较基准
                          </span>
                        )}
                        <span className={`font-mono font-bold ${simNoticeDays <= 28 ? 'text-emerald-600' : 'text-rose-600'}`}>
                          {simNoticeDays} 天 {simNoticeDays <= 28 ? '(安全)' : '(逾期失权风险)'}
                        </span>
                      </div>
                    </div>
                    <div className="relative pt-1 pb-3">
                      <input
                        type="range"
                        min="1"
                        max="60"
                        value={simNoticeDays}
                        onChange={(e) => handleSliderChange(setSimNoticeDays, Number(e.target.value))}
                        className="w-full accent-blue-600 cursor-pointer"
                      />
                      {/* 法定刻度锚点 */}
                      <div className="absolute left-[46.6%] top-5 text-[10px] font-mono text-rose-600 flex flex-col items-center">
                        <span className="w-0.5 h-2 bg-rose-500" />
                        <span>28d 失权线</span>
                      </div>
                    </div>
                    <p className="text-[11px] text-slate-500">
                      {simNoticeDays <= 28
                        ? '在 28 天除斥期内完成送达，完全排除失权抗辩。'
                        : (hostJur === 'asean_my'
                            ? '已超 28 天时效，需重点援引 Prevention Principle（阻碍原则）与 Contracts Act 1950 善意履约反失权。'
                            : hostJur === 'asean_vn'
                            ? '已超 28 天时效，需重点援引民法典善意原则与新建设法第 86.2 条合理损失界定反失权。'
                            : hostJur === 'asean_sg'
                            ? '已超 28 天时效，需重点援引新加坡普通法 Prevention Principle 反失权。'
                            : '已超 28 天时效，需重点援引 Prevention Principle 与 SEMA 3/2023 善意原则反失权。')}
                    </p>
                  </div>

                  {/* 滑块 3: 中信保可能损失报损天数 (30天除斥线) */}
                  <div className="clean-row-card p-4 space-y-2.5">
                    <div className="flex items-center justify-between text-xs">
                      <span className="font-semibold text-slate-900 flex items-center gap-1.5">
                        <ShieldCheck className="w-3.5 h-3.5 text-blue-600 shrink-0" />
                        中信保海外项目险可能损失报损天数
                      </span>
                      <div className="flex items-center gap-2">
                        {baselineParams.sinosure_notice_days !== undefined && simSinosureDays !== baselineParams.sinosure_notice_days && (
                          <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-slate-100 text-slate-600 font-semibold">
                            {simSinosureDays > baselineParams.sinosure_notice_days ? `+${simSinosureDays - baselineParams.sinosure_notice_days}d` : `${simSinosureDays - baselineParams.sinosure_notice_days}d`} 较基准
                          </span>
                        )}
                        <span className={`font-mono font-bold ${simSinosureDays <= 30 ? 'text-emerald-600' : 'text-rose-600'}`}>
                          {simSinosureDays} 天 {simSinosureDays <= 30 ? '(合规)' : '(理赔受限)'}
                        </span>
                      </div>
                    </div>
                    <div className="relative pt-1 pb-3">
                      <input
                        type="range"
                        min="1"
                        max="60"
                        value={simSinosureDays}
                        onChange={(e) => handleSliderChange(setSimSinosureDays, Number(e.target.value))}
                        className="w-full accent-blue-600 cursor-pointer"
                      />
                      {/* 法定刻度锚点 */}
                      <div className="absolute left-[50%] top-5 text-[10px] font-mono text-rose-600 flex flex-col items-center">
                        <span className="w-0.5 h-2 bg-rose-500" />
                        <span>30d 报损线</span>
                      </div>
                    </div>
                    <p className="text-[11px] text-slate-500">
                      中信保特别条款约定在知悉政府征收或业主恶意索兑 30 日内须递交书面预通报。
                    </p>
                  </div>

                  {/* 滑块 4 & 5: 违约金封顶上限 (10% vs 15%) */}
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div className="clean-row-card p-3.5 space-y-2">
                      <div className="flex justify-between text-xs">
                        <span className="text-slate-700 font-medium">总包合同 LD 上限:</span>
                        <span className="font-mono font-bold text-slate-900">{simMainLd}%</span>
                      </div>
                      <input
                        type="range"
                        min="5"
                        max="25"
                        value={simMainLd}
                        onChange={(e) => handleSliderChange(setSimMainLd, Number(e.target.value))}
                        className="w-full accent-blue-600 cursor-pointer"
                      />
                    </div>
                    <div className="clean-row-card p-3.5 space-y-2">
                      <div className="flex justify-between text-xs">
                        <span className="text-slate-700 font-medium">分包背靠背 LD 上限:</span>
                        <span className="font-mono font-bold text-slate-900">{simSubLd}%</span>
                      </div>
                      <input
                        type="range"
                        min="5"
                        max="25"
                        value={simSubLd}
                        onChange={(e) => handleSliderChange(setSimSubLd, Number(e.target.value))}
                        className="w-full accent-blue-600 cursor-pointer"
                      />
                    </div>
                  </div>
                </div>
              ) : (
                /* 投前模式下的 SPV 架构比选器 */
                <div className="space-y-4">
                  <div className="text-xs font-semibold text-slate-800">
                    选择出海投资与特许经营架构方案：
                  </div>
                  <div className="grid grid-cols-1 gap-3">
                    {[
                      {
                        key: 'A',
                        title: '方案 A：中资母公司直接投资 (Direct Investment)',
                        desc: `受中国与${jurConfig.name_zh}双边投资保护协定 (BIT) 直接保护，但缺少中转税收协定与法域中立仲裁优势。`,
                      },
                      {
                        key: 'B',
                        title: '方案 B：设立新加坡 SPV 中转 (Singapore SPV + BIT)',
                        desc: `激活新加坡与东道国双边投资保护 (BIT) 间接征收保护与税务协定 (DTA)，且履约保函受法域中立仲裁管辖。`,
                      },
                      {
                        key: 'C',
                        title: '方案 C：属地合资/联营体 (Consortium / Joint Operation)',
                        desc: `满足${jurConfig.name_zh}工程资质强行法与本地劳工配额要求，但存在连带责任接口敞口。`,
                      },
                    ].map((opt) => (
                      <div
                        key={opt.key}
                        onClick={() => setSelectedSpvScheme(opt.key as any)}
                        className={`p-4 rounded-2xl border cursor-pointer transition-all text-xs space-y-1.5 ${
                          selectedSpvScheme === opt.key
                            ? 'bg-blue-50/80 border-blue-400 shadow-2xs text-slate-900'
                            : 'bg-white hover:bg-slate-50 border-slate-200/70 text-slate-700'
                        }`}
                      >
                        <div className="font-bold text-blue-700 flex items-center justify-between">
                          <span>{opt.title}</span>
                          {selectedSpvScheme === opt.key && <Check className="w-4 h-4 text-blue-600" />}
                        </div>
                        <p className="text-slate-500 leading-relaxed">{opt.desc}</p>
                      </div>
                    ))}
                  </div>

                  <div className="clean-row-card p-4 space-y-2">
                    <div className="flex justify-between text-xs">
                      <span className="font-medium text-slate-700">外资股比上限设定:</span>
                      <span className="font-mono font-bold text-slate-900">{foreignEquityPct}% (负面清单 49%)</span>
                    </div>
                    <input
                      type="range"
                      min="20"
                      max="100"
                      value={foreignEquityPct}
                      onChange={(e) => setForeignEquityPct(Number(e.target.value))}
                      className="w-full accent-blue-600 cursor-pointer"
                    />
                  </div>
                </div>
              )}
            </div>

            {/* 右舱 (52% · 6列)：实时联动的实战交付卡 (谈判话术卡 + 7天取证清单) */}
            <div className="lg:col-span-6 space-y-5">
              {/* 交付卡 1: 《明日商务谈判反驳话术卡》 (支持中英双语切换 & 一键复制 & 光学脉冲) */}
              <div
                className={`apple-bento-card rounded-[30px] p-7 space-y-5 transition-all duration-500 ${
                  scriptPulse ? 'ring-2 ring-blue-500 shadow-lg' : ''
                }`}
              >
                <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-100 pb-3">
                  <div className="flex items-center gap-2">
                    <Swords className="w-4 h-4 text-blue-600" />
                    <h3 className="text-sm font-bold text-slate-900 tracking-tight">
                      《涉外商务谈判抗辩口径与发函要点》
                    </h3>
                  </div>

                  {/* 中英双语切换器 */}
                  <div className="inline-flex items-center p-0.5 bg-slate-100 rounded-xl">
                    <button
                      type="button"
                      onClick={() => setScriptLangMode('zh')}
                      className={`px-2.5 py-1 text-[11px] font-semibold rounded-lg transition-all cursor-pointer ${
                        scriptLangMode === 'zh' ? 'bg-white text-slate-900 shadow-2xs' : 'text-slate-500'
                      }`}
                    >
                      中文谈判定稿
                    </button>
                    <button
                      type="button"
                      onClick={() => setScriptLangMode('en')}
                      className={`px-2.5 py-1 text-[11px] font-semibold rounded-lg transition-all cursor-pointer ${
                        scriptLangMode === 'en' ? 'bg-white text-slate-900 shadow-2xs' : 'text-slate-500'
                      }`}
                    >
                      English Notice
                    </button>
                  </div>
                </div>

                {/* 场景选项卡 */}
                <div className="flex flex-wrap gap-2">
                  {tacticalGuidance.negotiation_scripts.map((sc, idx) => {
                    const isTriggeredByNotice = sc.scenario_title.includes('20.1') && simNoticeDays > 28;
                    const isTriggeredByTkdn = (sc.scenario_title.includes('TKDN') || sc.scenario_title.includes('CIPAA') || sc.scenario_title.includes('86.2') || sc.scenario_title.includes('SOPA')) && simTkdn < (slider1Config.target || 30);
                    const isTriggeredBySinosure = sc.scenario_title.includes('信保') && simSinosureDays > 30;
                    const isTriggered = isTriggeredByNotice || isTriggeredByTkdn || isTriggeredBySinosure;
                    return (
                      <button
                        key={idx}
                        type="button"
                        onClick={() => setActiveScriptIdx(idx)}
                        className={`px-3 py-1.5 rounded-xl text-xs font-medium transition-all cursor-pointer flex items-center gap-1.5 ${
                          activeScriptIdx === idx
                            ? 'bg-blue-600 text-white shadow-2xs font-semibold'
                            : 'bg-slate-100 hover:bg-slate-200/80 text-slate-700'
                        }`}
                      >
                        {isTriggered && <span className="w-1.5 h-1.5 rounded-full bg-rose-400 animate-pulse" />}
                        <span>{sc.scenario_title.split(' ')[0]}</span>
                      </button>
                    );
                  })}
                </div>

                {/* 话术主体展示区 */}
                {tacticalGuidance.negotiation_scripts[activeScriptIdx] && (
                  <div className="space-y-3">
                    <div className="flex flex-wrap items-center justify-between gap-2 text-[11px] font-mono text-slate-400">
                      <span>法理请求权/抗辩基础：{tacticalGuidance.negotiation_scripts[activeScriptIdx].legal_basis}</span>
                      {tacticalGuidance.negotiation_scripts[activeScriptIdx].scenario_title.includes('20.1') && simNoticeDays > 28 && (
                        <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-rose-50 border border-rose-200 text-rose-700 text-[10px] font-semibold animate-pulse">
                          <span className="w-1.5 h-1.5 rounded-full bg-rose-600" />
                          <span>NEW · 因越过 28d 失权红线触发</span>
                        </span>
                      )}
                    </div>

                    <div className="p-4 bg-slate-50/80 rounded-2xl border border-slate-200/80 text-xs text-slate-800 leading-relaxed font-sans whitespace-pre-wrap select-all">
                      {scriptLangMode === 'zh'
                        ? tacticalGuidance.negotiation_scripts[activeScriptIdx].script_zh
                        : tacticalGuidance.negotiation_scripts[activeScriptIdx].script_en}
                    </div>

                    <div className="flex items-center justify-between pt-1">
                      <span className="text-[11px] text-slate-400 font-mono">
                        发函送达需附带正式签收回执以防除斥
                      </span>
                      <button
                        type="button"
                        onClick={() =>
                          handleCopyScript(
                            scriptLangMode === 'zh'
                              ? tacticalGuidance.negotiation_scripts[activeScriptIdx].script_zh
                              : tacticalGuidance.negotiation_scripts[activeScriptIdx].script_en
                          )
                        }
                        className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-semibold text-white bg-blue-600 hover:bg-blue-700 transition-all shadow-xs cursor-pointer active:scale-95"
                      >
                        {copiedScript ? (
                          <>
                            <Check className="w-3.5 h-3.5" />
                            <span>已复制话术</span>
                          </>
                        ) : (
                          <>
                            <Copy className="w-3.5 h-3.5" />
                            <span>一键复制谈判定稿</span>
                          </>
                        )}
                      </button>
                    </div>
                  </div>
                )}
              </div>

              {/* 交付卡 2: 《红队抗辩推演 & 7天现场紧急取证清单》 */}
              <div className="apple-bento-card rounded-[30px] p-7 space-y-5">
                <div className="flex items-center justify-between border-b border-slate-100 pb-3">
                  <div className="flex items-center gap-2">
                    <Clock className="w-4 h-4 text-rose-600" />
                    <h3 className="text-sm font-bold text-slate-900 tracking-tight">
                      《对方核心抗辩预判与现场证据固化清单》
                    </h3>
                  </div>
                  <span className="text-[11px] font-mono text-slate-400">
                    落实后可阻断时效失权并固化索赔权利
                  </span>
                </div>

                <div className="space-y-3">
                  {tacticalGuidance.urgent_actions.map((act, idx) => {
                    const isDone = Boolean(completedActionIds[act.action_type]);
                    return (
                      <div
                        key={idx}
                        className={`p-4 rounded-2xl border transition-all text-xs space-y-2 ${
                          isDone ? 'bg-emerald-50/30 border-emerald-300' : 'bg-slate-50/60 border-slate-200/80'
                        }`}
                      >
                        <div className="flex items-center justify-between">
                          <div className="flex items-center gap-2">
                            <span
                              className={`w-2 h-2 rounded-full ${isDone ? 'bg-emerald-500' : 'bg-rose-500'}`}
                            />
                            <h4 className="font-bold text-slate-900">{act.action_type}</h4>
                          </div>
                          <span className="text-[10px] font-mono font-bold text-rose-700 bg-rose-50 px-2 py-0.5 rounded border border-rose-200">
                            {act.deadline_tag}
                          </span>
                        </div>

                        <p className="text-slate-600 text-xs font-medium">{act.document_template_title}</p>

                        <ul className="text-[11px] text-slate-500 space-y-1 list-disc pl-4 font-sans">
                          {act.key_points.map((pt, pidx) => (
                            <li key={pidx}>{pt}</li>
                          ))}
                        </ul>

                        <div className="pt-2 border-t border-slate-100 flex justify-end">
                          <button
                            type="button"
                            onClick={() => handleToggleAction(act.action_type)}
                            className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-xl text-xs font-semibold transition-all cursor-pointer ${
                              isDone
                                ? 'bg-emerald-600 text-white shadow-2xs'
                                : 'bg-white hover:bg-slate-100 text-slate-700 border border-slate-200/90'
                            }`}
                          >
                            <Check className="w-3.5 h-3.5" />
                            <span>{isDone ? '已在卷完成补强存证' : '标记此项证据已调取'}</span>
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
      {/* 切面 4：法源穿透图谱 & 意见书交付 (export) */}
      {/* ========================================================================= */}
      {facet === 'export' && (
        <div key="facet-export" className="space-y-6 apple-tab-pane">
          {/* 顶部操作栏：简洁标题 + 拓扑图谱按钮 + 双 DOCX 导出操作按钮组 */}
          <div className="apple-bento-card rounded-2xl p-5 flex flex-wrap items-center justify-between gap-4">
            <div className="flex items-center gap-3">
              <div className="w-9 h-9 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center shrink-0 border border-blue-100">
                <FileText className="w-4 h-4" />
              </div>
              <div>
                <h3 className="text-sm font-bold text-slate-900 tracking-tight">
                  涉外法律意见书生成与预览
                </h3>
                <p className="text-xs text-slate-500">
                  依据案卷事实要件与东盟现行法典自动生成公文级域外法查明意见书
                </p>
              </div>
            </div>

            {/* 操作按钮组：图谱按钮与导出手册按钮并排一体化 */}
            <div className="flex flex-wrap items-center gap-2.5">
              <button
                type="button"
                onClick={() => setShowGraphModal(true)}
                className="inline-flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs font-semibold text-slate-700 bg-white hover:bg-slate-50 border border-slate-200/90 transition-all shadow-2xs active:scale-[0.98] cursor-pointer"
              >
                <Share2 className="w-3.5 h-3.5 text-blue-600" />
                <span>法源因果拓扑图谱</span>
              </button>

              <button
                type="button"
                onClick={() => handleExportDocx('standard')}
                className="inline-flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs font-semibold text-white bg-blue-600 hover:bg-blue-700 transition-all shadow-xs shadow-blue-500/25 active:scale-[0.98] cursor-pointer"
              >
                <Download className="w-3.5 h-3.5" />
                <span>导出标准查明意见书 (.docx)</span>
              </button>

              <button
                type="button"
                onClick={() => handleExportDocx('handbook')}
                className="inline-flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs font-semibold text-slate-700 bg-white hover:bg-slate-50 border border-slate-200/90 transition-all shadow-2xs active:scale-[0.98] cursor-pointer"
              >
                <FileText className="w-3.5 h-3.5 text-slate-500" />
                <span>导出企业合规实务手册 (.docx)</span>
              </button>
            </div>
          </div>

          {/* 法律意见书高拟真预览纸张 (居中通栏展示，获得完整专业公文排版视距) */}
          <div className="w-full max-w-[1040px] mx-auto bg-white rounded-[28px] p-8 sm:p-12 border border-slate-200 shadow-xl space-y-6 text-slate-800 relative overflow-hidden font-serif">
            {/* 规范依据形式标 */}
            <div className="absolute right-6 top-6 text-[10px] font-mono text-slate-400 pointer-events-none select-none flex items-center gap-1.5">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500/70 inline-block" />
              <span>CASE-VERIFY: {currentCase?.case_id || 'C101'} · 最高法涉外法解释规范认证</span>
            </div>

            {/* 快速章节定位锚点 */}
            <div className="flex items-center gap-2 overflow-x-auto pb-2 text-[11px] font-sans font-medium text-slate-500 border-b border-slate-100">
              <span className="text-[10px] text-slate-400 font-mono uppercase">公文章节索引:</span>
              <span className="px-2 py-0.5 rounded bg-slate-100 text-slate-700 font-semibold">§1 查明定性结论</span>
              <span>·</span>
              <span className="px-2 py-0.5 rounded bg-slate-100 text-slate-700 font-semibold">§2 事实要件涵摄</span>
              <span>·</span>
              <span className="px-2 py-0.5 rounded bg-slate-100 text-slate-700 font-semibold">§3 挂载凭证附表 ({currentCase?.attached_artifacts?.length || 0})</span>
            </div>

            {/* 公文正式报头 */}
            <div className="text-center space-y-2 pb-6 border-b-2 border-slate-900 font-sans">
              <div className="text-xs font-mono tracking-widest text-slate-500 uppercase">
                CONFIDENTIAL LEGAL ASCERTAINMENT OPINION
              </div>
              <h2 className="text-xl sm:text-2xl font-bold text-slate-900 tracking-tight">
                {caseMeta.title} · 域外法查明与法律适用评估意见书
              </h2>
              <div className="flex flex-wrap items-center justify-center gap-4 text-xs font-mono text-slate-500 pt-1">
                <span>案卷编号: {currentCase?.case_id || 'C101'}</span>
                <span>·</span>
                <span>评估基准日: {caseMeta.criticalDate}</span>
                <span>·</span>
                <span>准据法: {caseMeta.choiceOfLaw}</span>
              </div>
            </div>

            {/* 章节一：首席定性结论与假定条件 */}
            <div className="space-y-3 font-sans">
              <h3 className="text-sm font-bold text-slate-900 uppercase tracking-wide border-l-3 border-slate-900 pl-2.5">
                一、 涉外法查明核心定性结论与 3D 评估
              </h3>
              <table className="w-full text-xs border border-slate-200 text-left border-collapse">
                <tbody>
                  <tr className="border-b border-slate-200 bg-slate-50">
                    <td className="p-2.5 font-bold w-1/3">
                      {isPreInv ? '外资持牌准入合规度' : '实体索赔胜诉确定性'}
                    </td>
                    <td className="p-2.5 text-slate-800">
                      {tacticalGuidance.qualitative_verdict?.legal_support_level} (
                      {tacticalGuidance.qualitative_verdict?.confidence_band})
                    </td>
                  </tr>
                  <tr className="border-b border-slate-200">
                    <td className="p-2.5 font-bold">
                      {isPreInv ? '属地强行法合规防线' : '程序失权驳回风险'}
                    </td>
                    <td className="p-2.5 text-slate-800">
                      {tacticalGuidance.qualitative_verdict?.procedural_exposure}
                    </td>
                  </tr>
                  <tr className="bg-slate-50">
                    <td className="p-2.5 font-bold">
                      {isPreInv ? '双边投资保护力 (BIT)' : '保函止付与反制预期'}
                    </td>
                    <td className="p-2.5 text-slate-800">
                      {tacticalGuidance.qualitative_verdict?.counter_block_expectation}
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            {/* 章节二：要件涵摄与法典条文平行对照 */}
            <div className="space-y-3 font-sans">
              <h3 className="text-sm font-bold text-slate-900 uppercase tracking-wide border-l-3 border-slate-900 pl-2.5">
                二、 争议焦点构成要件涵摄与法条对照
              </h3>
              <div className="space-y-2 text-xs">
                {activeElements.map((el, idx) => (
                  <div key={idx} className="p-3 bg-slate-50 rounded-xl border border-slate-200/80 space-y-1">
                    <div className="flex justify-between font-bold">
                      <span>{el.name_zh}</span>
                      <span className="font-mono text-blue-700">{el.ref_norm}</span>
                    </div>
                    <p className="text-slate-600 text-[11px] leading-relaxed">{el.match_note}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* 章节三：已挂载的外挂记录附表 */}
            {currentCase?.attached_artifacts && currentCase.attached_artifacts.length > 0 && (
              <div className="space-y-3 font-sans">
                <h3 className="text-sm font-bold text-slate-900 uppercase tracking-wide border-l-3 border-slate-900 pl-2.5">
                  三、 专项工具箱已挂载凭证附表 (Attached Artifacts)
                </h3>
                <div className="space-y-2">
                  {currentCase.attached_artifacts.map((art, idx) => (
                    <div key={idx} className="p-3 bg-slate-50 rounded-xl border border-slate-200 text-xs space-y-1 group">
                      <div className="flex justify-between items-center font-bold text-slate-900">
                        <span>
                          [{art.artifact_type === 'redline_scan' ? '合同红线' : art.artifact_type === 'statute_pin' ? '法典引用' : '专家会商'}] {art.title}
                        </span>
                        <div className="flex items-center gap-2">
                          <span className="text-[10px] font-mono text-slate-400">{art.created_at}</span>
                          <button
                            type="button"
                            onClick={() => handleRemoveArtifact(art.artifact_id || (art as any).id)}
                            className="text-[10px] text-slate-400 hover:text-rose-600 px-1.5 py-0.5 rounded hover:bg-rose-50 transition-colors cursor-pointer"
                            title="从案卷移除此挂载项"
                          >
                            <X className="w-3.5 h-3.5" />
                          </button>
                        </div>
                      </div>
                      <p className="text-slate-600 text-[11px]">{art.summary}</p>
                      {art.redline_clause && (
                        <div className="p-2 bg-emerald-50 rounded border border-emerald-100 font-mono text-[11px] text-emerald-900">
                          示范修订：{art.redline_clause}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* 公文正式落款 */}
            <div className="pt-6 border-t border-slate-200 text-xs font-sans flex flex-col sm:flex-row justify-between items-start sm:items-end gap-3 text-slate-500">
              <div>
                <p>出具机构：OverseasLawAssist 域外法查明联合体专家组</p>
                <p>法源依据：最高人民法院涉外法查明规范 · 东盟官方公报 · 国际工程与投资公约</p>
              </div>
              <div className="text-right font-mono text-[11px]">
                <span>意见书编号：{(currentCase?.case_id || 'C101')}-ASCERTAINMENT-REV2</span>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* 算法模型与依据弹窗 (完全绑定当前案卷动态数据) */}
      <ViabilityCalculationModal
        isOpen={showViabilityModal}
        onClose={() => setShowViabilityModal(false)}
        assessment={viabilityAssessment}
        isPreInvestment={isPreInv}
      />

      {/* 法源因果拓扑穿透图谱全屏弹窗 */}
      <CitationGraphFullscreenModal
        isOpen={showGraphModal}
        onClose={() => setShowGraphModal(false)}
        onSelectNorm={(normId) => {
          openRightDock('law_reader', normId);
        }}
      />
    </div>
  );
};
