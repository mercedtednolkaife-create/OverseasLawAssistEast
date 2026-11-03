import React, { useState, useMemo, useEffect } from 'react';
import {
  ShieldCheck,
  AlertTriangle,
  Scale,
  ArrowRight,
  CheckCircle2,
  Copy,
  Check,
  Send,
  FileText,
  RefreshCw,
  Building2,
  Globe,
  Lock,
  ShieldAlert,
  ChevronDown,
  ChevronUp,
} from 'lucide-react';
import { CaseState, DualComplianceAudit, DualComplianceItem } from '../../types/lawAgent';
import { lawAgentApi } from '../../api/lawAgentApi';
import { getJurisdictionConfig } from '../../configs/jurisdictions';

interface DualComplianceCompassProps {
  caseState: CaseState;
  onRefreshCase?: () => void;
  showToast?: (type: 'success' | 'error' | 'info' | 'warning', message: string) => void;
}

export const DualComplianceCompass: React.FC<DualComplianceCompassProps> = ({
  caseState,
  onRefreshCase,
  showToast,
}) => {
  const hostJur = caseState?.meta?.jurisdiction || 'asean_id';
  const jurConfig = getJurisdictionConfig(hostJur);

  // 本地动态审查数据状态 (优先使用案卷内数据，支持在线动态重跑)
  const [dynamicAudit, setDynamicAudit] = useState<DualComplianceAudit | null>(null);
  const [isChecking, setIsChecking] = useState<boolean>(false);
  const [copiedCode, setCopiedCode] = useState<string | null>(null);
  const [expandedCollisions, setExpandedCollisions] = useState<Record<string, boolean>>({});

  // 反馈规则弹窗状态
  const [isFeedbackOpen, setIsFeedbackOpen] = useState<boolean>(false);
  const [feedbackRuleCode, setFeedbackRuleCode] = useState<string>('RULE_PRC_ODI_01');
  const [feedbackType, setFeedbackType] = useState<'corroboration' | 'amendment' | 'exception'>('corroboration');
  const [feedbackComment, setFeedbackComment] = useState<string>('');
  const [feedbackStatute, setFeedbackStatute] = useState<string>('');
  const [isSubmittingFeedback, setIsSubmittingFeedback] = useState<boolean>(false);

  // 最终生效的 audit 对象 (100% 真实后端数据，零 Mock)
  const audit: DualComplianceAudit | null = useMemo(() => {
    if (dynamicAudit) return dynamicAudit;
    if (caseState?.dual_compliance_audit) return caseState.dual_compliance_audit;
    return null;
  }, [dynamicAudit, caseState?.dual_compliance_audit]);

  // 动态重新测算
  const handleRunCheck = async () => {
    setIsChecking(true);
    try {
      const engParams = caseState?.meta?.engineering_params || {};
      const fullText = `${caseState?.facts_zh || ''} ${caseState?.claims_zh || ''} ${caseState?.title || ''}`;
      const hasOverseasTransfer = engParams.has_overseas_transfer ?? /境外放款|外债|资本汇出|担保|保函|资金出境/i.test(fullText);
      const dataOutboundSensitive = engParams.data_outbound_sensitive ?? /调证|数据|测绘|图纸|源码|发现程序|Discovery|出口管制|两用物项|EAR/i.test(fullText);
      const hasSanctionsClause = engParams.has_sanctions_clause ?? /制裁|OFAC|SDN|长臂|实体清单|阻断/i.test(fullText);

      const res = await lawAgentApi.runDualComplianceCheck({
        jurisdiction: hostJur,
        facts_zh: caseState?.facts_zh || '',
        claims_zh: caseState?.claims_zh || '',
        title: caseState?.title || '',
        lifecycle_stage: typeof caseState?.meta?.lifecycle_stage === 'string'
          ? caseState.meta.lifecycle_stage
          : (caseState?.meta?.lifecycle_stage as any)?.value || 'execution_dispute',
        declared_equity_pct: engParams.declared_equity_pct,
        declared_tkdn_pct: engParams.declared_tkdn_pct,
        has_overseas_transfer: hasOverseasTransfer,
        data_outbound_sensitive: dataOutboundSensitive,
        has_sanctions_clause: hasSanctionsClause,
        engineering_params: engParams,
      });
      if (res && res.items) {
        setDynamicAudit(res);
        showToast?.('success', '中-东盟双向合规审查测算完成！');
      }
    } catch (err: any) {
      showToast?.('warning', '实时合规检测返回默认审查结论');
    } finally {
      setIsChecking(false);
    }
  };

  // 若案卷尚未具备双向合规审查结论，自动触发动态核验计算
  useEffect(() => {
    if (!audit && !isChecking && caseState?.case_id) {
      handleRunCheck();
    }
  }, [audit, isChecking, caseState?.case_id]);

  // 区分三方条目
  const prcItems = useMemo(() => audit?.items.filter((i) => i.side === 'prc_outbound') || [], [audit?.items]);
  const hostItems = useMemo(() => audit?.items.filter((i) => i.side === 'host_country') || [], [audit?.items]);
  const collisionItems = useMemo(() => audit?.items.filter((i) => i.side === 'bidirectional_conflict') || [], [audit?.items]);

  // 复制对冲条款
  const handleCopyClause = (code: string, clause: string) => {
    navigator.clipboard.writeText(clause);
    setCopiedCode(code);
    showToast?.('success', '合规避冲示范条款已复制至剪贴板');
    setTimeout(() => setCopiedCode(null), 2500);
  };

  // 提交合规实务反馈
  const handleSubmitFeedback = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!caseState?.case_id) {
      showToast?.('error', '未加载有效案卷');
      return;
    }
    if (!feedbackComment.trim()) {
      showToast?.('warning', '请填写具体实务反馈意见');
      return;
    }

    setIsSubmittingFeedback(true);
    try {
      const res = await lawAgentApi.feedbackToCompliance(caseState.case_id, {
        rule_code: feedbackRuleCode,
        feedback_type: feedbackType,
        comment: feedbackComment.trim(),
        suggested_statute: feedbackStatute.trim() || undefined,
      });
      showToast?.('success', res.message || '实务经验已成功反馈并沉淀至合规规则库！');
      setIsFeedbackOpen(false);
      setFeedbackComment('');
      setFeedbackStatute('');
      onRefreshCase?.();
    } catch (err: any) {
      showToast?.('error', '反馈提交失败: ' + (err.message || '网络异常'));
    } finally {
      setIsSubmittingFeedback(false);
    }
  };

  const toggleCollision = (ruleCode: string) => {
    setExpandedCollisions((prev) => ({
      ...prev,
      [ruleCode]: !prev[ruleCode],
    }));
  };

  if (!audit) {
    return (
      <div className="apple-bento-card rounded-[30px] p-8 text-center space-y-4 border border-slate-200/80 shadow-xs bg-white">
        <div className="w-12 h-12 rounded-2xl bg-indigo-50 border border-indigo-100 text-indigo-600 flex items-center justify-center mx-auto">
          <Scale className="w-6 h-6 animate-pulse" />
        </div>
        <div className="space-y-1">
          <h3 className="text-base font-bold text-slate-900">中-东盟双向合规与法律冲突审查</h3>
          <p className="text-xs text-slate-500 max-w-md mx-auto">
            {isChecking
              ? '正在对标中国企业出海监管红线与东道国属地强行法，排查潜在法域冲突...'
              : '当前案卷暂未生成合规审查数据，点击下方按钮立即开展双向强行法对标'}
          </p>
        </div>
        <button
          type="button"
          onClick={handleRunCheck}
          disabled={isChecking}
          className="inline-flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-semibold text-white bg-indigo-600 hover:bg-indigo-700 transition-all shadow-xs cursor-pointer disabled:opacity-50"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${isChecking ? 'animate-spin' : ''}`} />
          <span>{isChecking ? '正在核算审查结论...' : '立即开展双向合规对标'}</span>
        </button>
      </div>
    );
  }

  return (
    <div className="apple-bento-card rounded-[30px] p-6 sm:p-7 space-y-6 border border-slate-200/80 shadow-xs bg-white">
      {/* 顶部标题与评分指标栏 */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-100 pb-5">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-2xl bg-indigo-50 border border-indigo-200/70 flex items-center justify-center text-indigo-700 shadow-2xs">
            <Scale className="w-5 h-5 text-indigo-600" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h3 className="text-base font-bold text-slate-900 tracking-tight">
                中-东盟双向合规与法律冲突审查规程 (Dual Compliance Review)
              </h3>
              <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-indigo-50 text-indigo-700 border border-indigo-200/60 font-mono">
                法定强行法对标 · 避冲条款
              </span>
            </div>
            <p className="text-xs text-slate-500 mt-0.5">
              严格对标中国企业境外投资监管规定与东道国（{jurConfig.name_zh}）属地强行法，排查法域冲突并提供避冲示范条款
            </p>
          </div>
        </div>

        {/* 顶部按钮组 */}
        <div className="flex items-center gap-2.5">
          <button
            type="button"
            onClick={handleRunCheck}
            disabled={isChecking}
            className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-semibold text-slate-700 bg-slate-100 hover:bg-slate-200 transition-all cursor-pointer disabled:opacity-50"
            title="依据最新案情动态重跑双向合规审查"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${isChecking ? 'animate-spin text-blue-600' : 'text-slate-600'}`} />
            <span>{isChecking ? '核算中...' : '重新对标核算'}</span>
          </button>
          <button
            type="button"
            onClick={() => setIsFeedbackOpen(true)}
            className="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-xl text-xs font-semibold text-white bg-indigo-600 hover:bg-indigo-700 transition-all shadow-xs cursor-pointer"
            title="将本次案卷实务经验向合规规则库反馈沉淀"
          >
            <Send className="w-3.5 h-3.5" />
            <span>实务反馈沉淀</span>
          </button>
        </div>
      </div>

      {/* 核心双轨评分与冲突数量卡片 */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* 中国出海合规指数 */}
        <div className="p-4.5 rounded-2xl bg-gradient-to-br from-rose-50/50 to-orange-50/40 border border-rose-100 space-y-1.5">
          <div className="flex items-center justify-between">
            <span className="text-[11px] font-mono text-rose-700 font-bold uppercase tracking-wider flex items-center gap-1">
              <Building2 className="w-3.5 h-3.5 text-rose-600" />
              <span>中国企业出海合规指数</span>
            </span>
            <span className="text-[10px] font-mono font-semibold px-2 py-0.5 rounded-md bg-rose-100/70 text-rose-800">
              PRC OUTBOUND
            </span>
          </div>
          <div className="flex items-baseline gap-2">
            <span className="text-2xl font-black text-slate-900 tracking-tight font-mono">
              {audit.prc_score.toFixed(1)}
            </span>
            <span className="text-xs text-slate-400 font-mono">/ 100</span>
          </div>
          <p className="text-[11px] text-slate-600 leading-tight">
            国资委 35/43 号令、发改委 11 号令及跨境数据安全法要件全面扫描
          </p>
        </div>

        {/* 东道国强行法指数 */}
        <div className="p-4.5 rounded-2xl bg-gradient-to-br from-blue-50/50 to-indigo-50/40 border border-blue-100 space-y-1.5">
          <div className="flex items-center justify-between">
            <span className="text-[11px] font-mono text-blue-700 font-bold uppercase tracking-wider flex items-center gap-1">
              <Globe className="w-3.5 h-3.5 text-blue-600" />
              <span>{jurConfig.short_name} 属地强行法对标指数</span>
            </span>
            <span className="text-[10px] font-mono font-semibold px-2 py-0.5 rounded-md bg-blue-100/70 text-blue-800">
              HOST MANDATORY
            </span>
          </div>
          <div className="flex items-baseline gap-2">
            <span className="text-2xl font-black text-slate-900 tracking-tight font-mono">
              {audit.host_score.toFixed(1)}
            </span>
            <span className="text-xs text-slate-400 font-mono">/ 100</span>
          </div>
          <p className="text-[11px] text-slate-600 leading-tight">
            外资施工准入、TKDN 配额、背靠背付款效力与独立保函止付门槛
          </p>
        </div>

        {/* 双向法域冲突碰撞点 */}
        <div className="p-4.5 rounded-2xl bg-gradient-to-br from-amber-50/50 to-yellow-50/40 border border-amber-200 space-y-1.5">
          <div className="flex items-center justify-between">
            <span className="text-[11px] font-mono text-amber-800 font-bold uppercase tracking-wider flex items-center gap-1">
              <AlertTriangle className="w-3.5 h-3.5 text-amber-600" />
              <span>双向法域冲突碰撞点</span>
            </span>
            <span className="text-[10px] font-mono font-semibold px-2 py-0.5 rounded-md bg-amber-100 text-amber-800">
              CONFLICT IDENTIFIED
            </span>
          </div>
          <div className="flex items-baseline gap-2">
            <span className="text-2xl font-black text-amber-900 tracking-tight font-mono">
              {audit.collision_count}
            </span>
            <span className="text-xs text-amber-700 font-medium">项潜在法律抵触已识别</span>
          </div>
          <p className="text-[11px] text-slate-600 leading-tight">
            已生成防冲突合同特别条款与中国信保/商务部阻断避险方案
          </p>
        </div>
      </div>

      {/* 冲突消解专栏 (Collision Resolution Cards) */}
      {collisionItems.length > 0 && (
        <div className="space-y-3.5">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Scale className="w-4 h-4 text-amber-600" />
              <h4 className="text-sm font-bold text-slate-900">
                法域冲突重点对标与消解方案 ({collisionItems.length})
              </h4>
            </div>
            <span className="text-[11px] text-slate-400 font-mono">
              点击卡片展开合同防冲突条款与落地动作
            </span>
          </div>

          <div className="space-y-3">
            {collisionItems.map((item) => {
              const isExp = expandedCollisions[item.rule_code] !== false; // 默认展开
              return (
                <div
                  key={item.rule_code}
                  className="rounded-2xl border border-amber-200/90 bg-amber-50/25 overflow-hidden transition-all shadow-2xs"
                >
                  <button
                    type="button"
                    onClick={() => toggleCollision(item.rule_code)}
                    className="w-full p-4.5 flex items-start justify-between text-left cursor-pointer hover:bg-amber-50/50 transition-colors"
                  >
                    <div className="space-y-1 pr-4">
                      <div className="flex items-center gap-2">
                        <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-amber-500 text-white">
                          冲突碰撞
                        </span>
                        <span className="text-xs font-mono text-slate-400">[{item.rule_code}]</span>
                        <h5 className="text-sm font-bold text-slate-900">{item.title_zh}</h5>
                      </div>
                      <p className="text-xs text-slate-600 leading-relaxed mt-1">{item.collision_desc}</p>
                    </div>
                    <div className="flex items-center gap-2 text-slate-400 pt-0.5">
                      <span className="text-xs font-medium">{isExp ? '收起' : '展开'}</span>
                      {isExp ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                    </div>
                  </button>

                  {isExp && (
                    <div className="px-4.5 pb-4.5 pt-1 border-t border-amber-100/80 space-y-3">
                      {/* 规范比对栏 */}
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
                        <div className="p-3 rounded-xl bg-white border border-slate-200/70 space-y-1">
                          <span className="text-[10px] font-mono text-rose-600 font-bold uppercase">
                            🇨🇳 中国企业出海强行法要件
                          </span>
                          <p className="font-semibold text-slate-800">{item.prc_statute}</p>
                        </div>
                        <div className="p-3 rounded-xl bg-white border border-slate-200/70 space-y-1">
                          <span className="text-[10px] font-mono text-blue-600 font-bold uppercase">
                            🌐 东道国法律或合同规制
                          </span>
                          <p className="font-semibold text-slate-800">{item.host_statute}</p>
                        </div>
                      </div>

                      {/* 推荐合同对冲条款 */}
                      {item.mitigation_clause_zh && (
                        <div className="p-3.5 rounded-xl bg-white border border-amber-200 space-y-2">
                          <div className="flex items-center justify-between">
                            <span className="text-xs font-bold text-amber-900 flex items-center gap-1.5">
                              <FileText className="w-3.5 h-3.5 text-amber-600" />
                              <span>推荐合同特别避冲示范条款 (Mitigation Clause)</span>
                            </span>
                            <button
                              type="button"
                              onClick={() => handleCopyClause(item.rule_code, item.mitigation_clause_zh!)}
                              className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg text-[11px] font-semibold text-amber-900 bg-amber-100/70 hover:bg-amber-200 transition-colors cursor-pointer"
                            >
                              {copiedCode === item.rule_code ? (
                                <>
                                  <Check className="w-3 h-3 text-emerald-600" />
                                  <span className="text-emerald-700">已复制</span>
                                </>
                              ) : (
                                <>
                                  <Copy className="w-3 h-3" />
                                  <span>复制示范条款</span>
                                </>
                              )}
                            </button>
                          </div>
                          <p className="text-xs text-slate-700 bg-slate-50 p-2.5 rounded-lg border border-slate-200/60 font-serif leading-relaxed">
                            {item.mitigation_clause_zh}
                          </p>
                        </div>
                      )}

                      {/* 实务行动指引 */}
                      {item.action_guidance && (
                        <div className="flex items-start gap-2 text-xs text-slate-600 bg-emerald-50/60 p-2.5 rounded-xl border border-emerald-100">
                          <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                          <span>
                            <strong>合规落地动作：</strong>
                            {item.action_guidance}
                          </span>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* 左右分栏：中国出海合规红线 vs 东道国属地强行法要件 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
        {/* 左栏：🇨🇳 中国企业出海强行法要件 (国资委/发改委/外管/数安) */}
        <div className="p-5 rounded-2xl bg-slate-50/80 border border-slate-200/80 space-y-3.5">
          <div className="flex items-center justify-between pb-2 border-b border-slate-200/60">
            <span className="text-xs font-bold text-slate-900 flex items-center gap-1.5">
              <ShieldAlert className="w-4 h-4 text-rose-600" />
              <span>中国企业出海强行法基准 ({prcItems.length})</span>
            </span>
            <span className="text-[10px] font-mono text-slate-400">母国法定合规前哨</span>
          </div>

          <div className="space-y-2.5">
            {prcItems.map((item) => (
              <div
                key={item.rule_code}
                className="p-3 bg-white rounded-xl border border-slate-200/70 shadow-2xs text-xs space-y-1.5"
              >
                <div className="flex items-center justify-between">
                  <span className="font-semibold text-slate-900">{item.title_zh}</span>
                  <span
                    className={`text-[10px] font-mono px-2 py-0.5 rounded font-bold ${
                      item.status === 'pass'
                        ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                        : item.status === 'warning'
                        ? 'bg-amber-50 text-amber-700 border border-amber-200'
                        : 'bg-rose-50 text-rose-700 border border-rose-200'
                    }`}
                  >
                    {item.status.toUpperCase()}
                  </span>
                </div>
                {item.prc_statute && (
                  <p className="text-[11px] font-mono text-slate-500">法定依据：{item.prc_statute}</p>
                )}
                {item.action_guidance && (
                  <p className="text-slate-600 leading-relaxed text-[11px]">{item.action_guidance}</p>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* 右栏：🌐 东道国属地强行法要件 (外资/资质/背靠背/保函) */}
        <div className="p-5 rounded-2xl bg-slate-50/80 border border-slate-200/80 space-y-3.5">
          <div className="flex items-center justify-between pb-2 border-b border-slate-200/60">
            <span className="text-xs font-bold text-slate-900 flex items-center gap-1.5">
              <Globe className="w-4 h-4 text-blue-600" />
              <span>东道国 ({jurConfig.name_zh}) 强行法基准 ({hostItems.length})</span>
            </span>
            <span className="text-[10px] font-mono text-slate-400">属地履约刚性红线</span>
          </div>

          <div className="space-y-2.5">
            {hostItems.map((item) => (
              <div
                key={item.rule_code}
                className="p-3 bg-white rounded-xl border border-slate-200/70 shadow-2xs text-xs space-y-1.5"
              >
                <div className="flex items-center justify-between">
                  <span className="font-semibold text-slate-900">{item.title_zh}</span>
                  <span
                    className={`text-[10px] font-mono px-2 py-0.5 rounded font-bold ${
                      item.status === 'pass'
                        ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                        : item.status === 'warning'
                        ? 'bg-amber-50 text-amber-700 border border-amber-200'
                        : 'bg-rose-50 text-rose-700 border border-rose-200'
                    }`}
                  >
                    {item.status.toUpperCase()}
                  </span>
                </div>
                {item.host_statute && (
                  <p className="text-[11px] font-mono text-slate-500">属地依据：{item.host_statute}</p>
                )}
                {item.action_guidance && (
                  <p className="text-slate-600 leading-relaxed text-[11px]">{item.action_guidance}</p>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* 集团合规审批链条 (Corporate Approval Chain) */}
      {audit.approval_chain && audit.approval_chain.length > 0 && (
        <div className="p-5 rounded-2xl bg-gradient-to-r from-slate-50 to-blue-50/30 border border-slate-200/80 space-y-3.5">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Building2 className="w-4 h-4 text-indigo-600" />
              <h4 className="text-sm font-bold text-slate-900">
                出海集团合规前置审批与时间节点链条
              </h4>
            </div>
            <span className="text-[11px] font-mono text-indigo-700 bg-indigo-50 px-2 py-0.5 rounded border border-indigo-200/60 font-semibold">
              {audit.approval_chain.length} 阶法定流程
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-5 gap-3 pt-1">
            {audit.approval_chain.map((step, idx) => (
              <div
                key={idx}
                className="p-3 bg-white rounded-xl border border-slate-200/80 shadow-2xs space-y-1.5 relative group hover:border-indigo-300 transition-all flex flex-col justify-between"
              >
                <div className="space-y-1.5">
                  <div className="flex items-center justify-between gap-1">
                    <div className="flex items-center gap-1.5 min-w-0">
                      <span className="w-4 h-4 rounded-full bg-indigo-600 text-white text-[10px] font-mono font-bold flex items-center justify-center shrink-0">
                        {idx + 1}
                      </span>
                      <span className="text-[11px] font-bold text-slate-900 truncate" title={step.step}>
                        {step.step.includes('·') ? step.step.split('·')[1]?.trim() : step.step}
                      </span>
                    </div>
                    {step.status && (
                      <span className="px-1.5 py-0.5 rounded text-[9px] font-medium bg-indigo-50 text-indigo-700 shrink-0">
                        {step.status.length > 8 ? step.status.slice(0, 8) + '...' : step.status}
                      </span>
                    )}
                  </div>
                  <div className="text-[10px] font-semibold text-indigo-700 line-clamp-1" title={step.authority}>
                    🏛️ {step.authority}
                  </div>
                  {step.item && (
                    <div className="text-[10px] text-slate-700 line-clamp-2 leading-snug" title={step.item}>
                      📋 {step.item}
                    </div>
                  )}
                  <div className="text-[10px] font-mono text-slate-500 flex items-center gap-1" title={step.timing}>
                    ⏳ {step.timing}
                  </div>
                </div>
                <div className="text-[10px] text-rose-600/90 pt-1 border-t border-slate-100 line-clamp-2 leading-snug mt-1" title={step.risk_consequence}>
                  ⚠️ {step.risk_consequence}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 实务经验反馈弹窗 (Feedback Modal) */}
      {isFeedbackOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 backdrop-blur-xs p-4 animate-in fade-in duration-200">
          <div className="w-full max-w-lg bg-white rounded-3xl p-6 shadow-2xl border border-slate-200 space-y-4">
            <div className="flex items-center justify-between pb-3 border-b border-slate-100">
              <div className="flex items-center gap-2">
                <Send className="w-4 h-4 text-indigo-600" />
                <h4 className="text-sm font-bold text-slate-900">案卷实务经验向合规规则库反馈</h4>
              </div>
              <button
                type="button"
                onClick={() => setIsFeedbackOpen(false)}
                className="p-1 rounded-lg text-slate-400 hover:text-slate-600 hover:bg-slate-100 cursor-pointer"
              >
                ✕
              </button>
            </div>

            <form onSubmit={handleSubmitFeedback} className="space-y-3.5 text-xs">
              <div>
                <label className="block font-semibold text-slate-700 mb-1">
                  对应合规规则 / 碰撞点
                </label>
                <select
                  value={feedbackRuleCode}
                  onChange={(e) => setFeedbackRuleCode(e.target.value)}
                  className="w-full px-3 py-2 rounded-xl border border-slate-200 bg-slate-50 font-mono text-xs focus:bg-white focus:outline-hidden focus:ring-2 focus:ring-indigo-500"
                >
                  <option value="RULE_PRC_ODI_01">RULE_PRC_ODI_01 · 发改委11号令敏感行业备案</option>
                  <option value="RULE_PRC_SASAC_01">RULE_PRC_SASAC_01 · 国资委35号令境外代持禁止</option>
                  <option value="COLL_DATA_TRANSFER">COLL_DATA_TRANSFER · 跨境工程地质数据流动冲突</option>
                  <option value="COLL_SANCTIONS">COLL_SANCTIONS · 单边制裁长臂管辖与反制裁法冲突</option>
                  <option value="RULE_HOST_PERMIT_01">RULE_HOST_PERMIT_01 · 东道国外国承包商执照</option>
                  <option value="RULE_HOST_PAY_01">RULE_HOST_PAY_01 · 属地背靠背付款绝对无效令</option>
                </select>
              </div>

              <div>
                <label className="block font-semibold text-slate-700 mb-1">
                  反馈类型
                </label>
                <div className="grid grid-cols-3 gap-2">
                  {[
                    { id: 'corroboration', label: '实务佐证支持' },
                    { id: 'amendment', label: '条文或阈值修正' },
                    { id: 'exception', label: '司法裁判例外' },
                  ].map((t) => (
                    <button
                      key={t.id}
                      type="button"
                      onClick={() => setFeedbackType(t.id as any)}
                      className={`p-2 rounded-xl border text-center font-medium transition-all cursor-pointer ${
                        feedbackType === t.id
                          ? 'bg-indigo-50 border-indigo-300 text-indigo-700 font-bold'
                          : 'bg-white border-slate-200 text-slate-600 hover:bg-slate-50'
                      }`}
                    >
                      {t.label}
                    </button>
                  ))}
                </div>
              </div>

              <div>
                <label className="block font-semibold text-slate-700 mb-1">
                  实务经验总结 / 裁决实操意见 <span className="text-rose-500">*</span>
                </label>
                <textarea
                  rows={3}
                  value={feedbackComment}
                  onChange={(e) => setFeedbackComment(e.target.value)}
                  placeholder="例如：在马来西亚吉隆坡高院最新判例中，即使总包合同约定适用英国法，属地 CIPAA 快速裁决仍属不可剥夺的法定管辖权..."
                  className="w-full px-3 py-2 rounded-xl border border-slate-200 bg-slate-50 text-xs focus:bg-white focus:outline-hidden focus:ring-2 focus:ring-indigo-500 resize-none"
                  required
                />
              </div>

              <div>
                <label className="block font-semibold text-slate-700 mb-1">
                  建议补充/修正的法规条文或判例编号 (可选)
                </label>
                <input
                  type="text"
                  value={feedbackStatute}
                  onChange={(e) => setFeedbackStatute(e.target.value)}
                  placeholder="例如：High Court of Malaya [2025] 3 MLJ 412"
                  className="w-full px-3 py-2 rounded-xl border border-slate-200 bg-slate-50 text-xs focus:bg-white focus:outline-hidden focus:ring-2 focus:ring-indigo-500"
                />
              </div>

              <div className="flex items-center justify-end gap-2 pt-2 border-t border-slate-100">
                <button
                  type="button"
                  onClick={() => setIsFeedbackOpen(false)}
                  className="px-4 py-2 rounded-xl text-xs font-medium text-slate-600 hover:bg-slate-100 transition-all cursor-pointer"
                >
                  取消
                </button>
                <button
                  type="submit"
                  disabled={isSubmittingFeedback}
                  className="px-4 py-2 rounded-xl text-xs font-semibold text-white bg-indigo-600 hover:bg-indigo-700 transition-all shadow-xs cursor-pointer disabled:opacity-50"
                >
                  {isSubmittingFeedback ? '提交中...' : '确认沉淀至合规库'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
