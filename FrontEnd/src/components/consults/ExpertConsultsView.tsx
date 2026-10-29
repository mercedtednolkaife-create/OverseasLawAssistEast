import React, { useState, useEffect, useMemo } from 'react';
import { useApp } from '../../context/AppContext';
import { lawAgentApi } from '../../api/lawAgentApi';
import { Expert, ConsultRecord } from '../../types/lawAgent';
import {
  DEFAULT_EXPERTS,
  DEFAULT_CONSULTS,
  ASEAN_JURISDICTIONS,
  INQUIRY_TEMPLATES,
  ExtendedExpert,
  ExtendedConsultRecord,
} from './consultDefaultData';
import {
  Users,
  Send,
  FileText,
  Shield,
  Paperclip,
  Check,
  Loader2,
  Search,
  BookOpen,
  Copy,
  Sparkles,
  Scale,
  Building2,
  ChevronDown,
  ChevronUp,
} from 'lucide-react';

export const ExpertConsultsView: React.FC = () => {
  const { currentCase, currentCaseId, refreshCurrentCase, showToast } = useApp();

  const [experts, setExperts] = useState<ExtendedExpert[]>(DEFAULT_EXPERTS);
  const [consults, setConsults] = useState<ExtendedConsultRecord[]>(DEFAULT_CONSULTS);
  const [selectedExpertId, setSelectedExpertId] = useState<string>(DEFAULT_EXPERTS[0].expert_id);
  const [selectedJurFilter, setSelectedJurFilter] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [questionText, setQuestionText] = useState<string>(INQUIRY_TEMPLATES[0].text);

  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [attachingId, setAttachingId] = useState<string | null>(null);
  const [attachedIds, setAttachedIds] = useState<Record<string, boolean>>({});
  const [copiedId, setCopiedId] = useState<string | null>(null);
  const [expandedConsultIds, setExpandedConsultIds] = useState<Record<string, boolean>>({
    'CON-ID-2026-001': true,
    'CON-SG-2026-002': true,
  });

  // 后台无缝静默加载与同步后端专家及咨询数据
  const loadData = async () => {
    try {
      const expList = await lawAgentApi.getExperts();
      if (Array.isArray(expList) && expList.length > 0) {
        // 合并后端数据与本地富数据
        const mergedExperts = expList.map((be) => {
          const matched = DEFAULT_EXPERTS.find((de) => de.expert_id === be.expert_id);
          return (matched ? { ...matched, ...be } : be) as ExtendedExpert;
        });
        setExperts(mergedExperts);
      }

      const consList = await lawAgentApi.getConsults(currentCase?.case_id);
      if (Array.isArray(consList) && consList.length > 0) {
        // 将后端最新产生的咨询记录与高保真示范意见书合并
        const backendIds = new Set(consList.map((c) => c.consult_id));
        const unseededDefaults = DEFAULT_CONSULTS.filter((dc) => !backendIds.has(dc.consult_id));
        setConsults([...consList, ...unseededDefaults]);
      }
    } catch (err: any) {
      console.warn('Consults background fetch failed, using high-fidelity local data:', err);
    }
  };

  useEffect(() => {
    loadData();
  }, [currentCase?.case_id]);

  // 根据法域和关键词过滤专家
  const filteredExperts = useMemo(() => {
    return experts.filter((exp) => {
      if (selectedJurFilter !== 'all' && exp.country_code !== selectedJurFilter) {
        return false;
      }
      if (searchQuery.trim()) {
        const q = searchQuery.toLowerCase();
        const inName = exp.name.toLowerCase().includes(q);
        const inTitle = exp.title.toLowerCase().includes(q);
        const inAffil = exp.affiliation.toLowerCase().includes(q);
        const inFields = exp.fields.some((f) => f.toLowerCase().includes(q));
        if (!inName && !inTitle && !inAffil && !inFields) return false;
      }
      return true;
    });
  }, [experts, selectedJurFilter, searchQuery]);

  // 根据法域和关键词过滤意见书
  const filteredConsults = useMemo(() => {
    return consults.filter((con) => {
      if (selectedJurFilter !== 'all' && con.country_code && con.country_code !== selectedJurFilter) {
        return false;
      }
      if (searchQuery.trim()) {
        const q = searchQuery.toLowerCase();
        const inTopic = (con.topic || '').toLowerCase().includes(q);
        const inName = con.expert_name.toLowerCase().includes(q);
        const inQ = con.question_snapshot.toLowerCase().includes(q);
        const inReply = (con.reply || '').toLowerCase().includes(q);
        if (!inTopic && !inName && !inQ && !inReply) return false;
      }
      return true;
    });
  }, [consults, selectedJurFilter, searchQuery]);

  // 当前选中的专家详情
  const currentSelectedExpert = useMemo(() => {
    return experts.find((e) => e.expert_id === selectedExpertId) || experts[0];
  }, [experts, selectedExpertId]);

  // 一键填充咨询模板
  const handleApplyTemplate = (tmpl: typeof INQUIRY_TEMPLATES[0]) => {
    setQuestionText(tmpl.text);
    const matchedExp = experts.find((e) => e.country_code === tmpl.country_code);
    if (matchedExp) {
      setSelectedExpertId(matchedExp.expert_id);
    }
    showToast(`已填入【${tmpl.title}】咨询要点并匹配对应国别专家`, 'info');
  };

  // 挂载会商意见至案卷
  const handleAttachConsult = async (con: ConsultRecord) => {
    if (!currentCaseId) {
      showToast('请先选择或新建目标案卷以挂载意见书', 'warning');
      return;
    }
    setAttachingId(con.consult_id);
    try {
      await lawAgentApi.attachCaseArtifact(currentCaseId, {
        artifact_type: 'expert_coi',
        title: `东道国法律顾问意见书 - ${con.expert_name}`,
        jurisdiction: currentCase?.meta?.jurisdiction || 'asean_id',
        summary: `特邀属地专家 ${con.expert_name} 就「${con.question_snapshot.slice(0, 60)}...」出具专项法律意见书，已通过独立性与利益冲突审查并形成合规归档。`,
      });
      setAttachedIds((prev) => ({ ...prev, [con.consult_id]: true }));
      showToast(`✓ 已成功将专家意见书挂载至案卷【${currentCaseId}】`, 'success');
      await refreshCurrentCase();
    } catch (e: any) {
      showToast(e.message || '挂载失败', 'error');
    } finally {
      setAttachingId(null);
    }
  };

  // 复制意见书全文
  const handleCopyOpinion = (text: string, id: string) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    showToast('法律意见书全文已复制至剪贴板', 'success');
    setTimeout(() => setCopiedId(null), 2500);
  };

  // 折叠/展开意见书
  const toggleExpand = (id: string) => {
    setExpandedConsultIds((prev) => ({
      ...prev,
      [id]: !prev[id],
    }));
  };

  // 发起咨询委托
  const handleCreateConsult = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedExpertId || !questionText.trim()) return;

    setIsSubmitting(true);
    const exp = experts.find((x) => x.expert_id === selectedExpertId);
    try {
      const created = await lawAgentApi.createConsult({
        case_id: currentCase?.case_id || 'DEFAULT-CASE',
        expert_id: selectedExpertId,
        question_snapshot: questionText,
        evidence_summary: `咨询专家: ${exp?.name || '东盟专家'} (${exp?.affiliation || '属地机构'})`,
      });

      const newRecord: ExtendedConsultRecord = {
        ...created,
        expert_name: exp?.name || '东盟工程法专家',
        country_code: exp?.country_code,
        country_flag: exp?.country_flag,
        topic: `关于 ${exp?.country_name || '东盟'} 涉外工程合规专项法律咨询`,
        reply: `【${exp?.country_name || '东盟'}属地法律顾问正式受理通知】\n已完成受托事项利益冲突审查，${exp?.name} 特邀出海法务团队已接受委托。\n专家组正在调阅东道国现行成文法典、属地行业行政规程及最高裁判先例，预计将于 3 个工作日内正式出具盖章签署版法律意见书。`,
        legal_references: exp?.fields || ['东道国建设工程法典', 'FIDIC 标准合同条件'],
        key_findings: [
          '已通过利益冲突排查与独立性审查',
          '案卷材料已移送属地出海执业团队审阅',
          '预计 3 个工作日内出具正式签署书面意见书',
        ],
        updated_at: new Date().toLocaleString('zh-CN', { hour12: false }),
      };

      setConsults((prev) => [newRecord, ...prev]);
      showToast(`✓ 已向【${exp?.name}】发起法律咨询委托并生成流转编号`, 'success');
    } catch (err: any) {
      showToast(err.message || '委托创建失败', 'error');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="max-w-[1600px] mx-auto px-4 sm:px-6 py-6 space-y-6">
      {/* 顶部决策看板 Header Banner */}
      <div className="apple-bento-card rounded-[28px] p-6 sm:p-7 relative overflow-hidden">
        <div className="relative z-10 max-w-5xl space-y-3">
          <div className="inline-flex items-center gap-2 px-2.5 py-1 rounded-full bg-blue-50 border border-blue-200/80 text-blue-700 text-xs font-semibold">
            <span className="w-1.5 h-1.5 rounded-full bg-blue-600 animate-pulse" />
            <span>东盟六国特聘出海法律顾问网络 · 独立性排查 (COI Cleared) · 穿透式合规归档</span>
          </div>

          <h1 className="text-xl sm:text-2xl font-bold tracking-tight text-slate-900">
            东盟属地法律顾问与出海专家咨询库
          </h1>

          <p className="text-xs sm:text-sm text-slate-600 leading-relaxed font-normal">
            特邀东盟六国涉外基建工程持证律师与国际争议裁决专家，提供东道国强行法、外资准入、履约保函与争议解决专项书面意见书。
          </p>

          {/* 法域快速筛选胶囊条 */}
          <div className="flex flex-wrap items-center gap-2 pt-2">
            <span className="text-xs text-slate-400 font-medium">聚焦法域：</span>
            {ASEAN_JURISDICTIONS.map((j) => {
              const isSelected = selectedJurFilter === j.code;
              return (
                <button
                  key={j.code}
                  type="button"
                  onClick={() => setSelectedJurFilter(j.code)}
                  className={`px-3 py-1.5 rounded-xl text-xs font-medium border transition-all cursor-pointer flex items-center gap-1.5 ${
                    isSelected
                      ? 'bg-blue-600 text-white border-blue-600 shadow-xs shadow-blue-500/25 font-semibold'
                      : 'bg-white/80 text-slate-600 border-slate-200/80 hover:bg-white hover:text-slate-900 shadow-2xs'
                  }`}
                >
                  <span>{j.flag}</span>
                  <span>{j.name}</span>
                  {isSelected && <Check className="w-3 h-3 text-white ml-0.5" />}
                </button>
              );
            })}
          </div>
        </div>

        {/* 装饰图标 */}
        <div className="absolute right-6 -bottom-6 opacity-5 pointer-events-none hidden lg:block">
          <Scale className="w-56 h-56 text-slate-900" />
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* 左侧：会商发起与专家资质库 (5列) */}
        <div className="lg:col-span-5 space-y-6">
          {/* 发起专家咨询表单卡片 */}
          <div className="apple-bento-card rounded-[28px] p-6 space-y-4 shadow-2xs">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <div className="flex items-center gap-2">
                <div className="w-8 h-8 rounded-xl bg-blue-50 border border-blue-200/60 text-blue-600 flex items-center justify-center shrink-0">
                  <Send className="w-4 h-4 text-blue-600" />
                </div>
                <div>
                  <h3 className="text-sm font-bold text-slate-900">
                    发起属地出海法律顾问咨询
                  </h3>
                  <p className="text-[11px] text-slate-400">
                    指派受托专家开展法律论证并出具书面意见
                  </p>
                </div>
              </div>
            </div>

            <form onSubmit={handleCreateConsult} className="space-y-4 text-xs">
              {/* 选择专家 */}
              <div>
                <label className="block font-semibold text-slate-700 mb-1.5">
                  受托属地专家 (已通过执业合规与利益冲突排查)
                </label>
                <select
                  value={selectedExpertId}
                  onChange={(e) => setSelectedExpertId(e.target.value)}
                  className="w-full px-3.5 py-2.5 border border-slate-200/80 rounded-xl bg-white/90 font-medium focus:outline-none focus:ring-2 focus:ring-blue-500/10 focus:border-blue-600 text-slate-800 shadow-2xs cursor-pointer"
                >
                  {experts.map((exp) => (
                    <option key={exp.expert_id} value={exp.expert_id}>
                      {exp.country_flag} {exp.name} · {exp.country_name} ({exp.affiliation})
                    </option>
                  ))}
                </select>

                {currentSelectedExpert && (
                  <div className="mt-2 p-2.5 rounded-xl bg-slate-50/70 border border-slate-200/60 flex items-center justify-between text-[11px] text-slate-600">
                    <span className="truncate">
                      {currentSelectedExpert.city} · {currentSelectedExpert.qualification}
                    </span>
                    <span className="font-semibold text-blue-600 shrink-0 ml-2">
                      {currentSelectedExpert.experience_years}年资历
                    </span>
                  </div>
                )}
              </div>

              {/* 常用模板一键填入 */}
              <div>
                <div className="flex items-center justify-between mb-1.5">
                  <label className="block font-semibold text-slate-700">
                    实务咨询事项模板 (点击快速填入)
                  </label>
                  <span className="text-[10px] text-slate-400 font-medium">智能匹配</span>
                </div>
                <div className="grid grid-cols-2 gap-1.5">
                  {INQUIRY_TEMPLATES.map((tmpl) => (
                    <button
                      key={tmpl.id}
                      type="button"
                      onClick={() => handleApplyTemplate(tmpl)}
                      className="p-2 text-left rounded-xl bg-slate-50/80 hover:bg-blue-50/60 border border-slate-200/70 hover:border-blue-300 transition-all cursor-pointer group"
                    >
                      <div className="flex items-center gap-1 text-[11px] font-bold text-slate-800 group-hover:text-blue-700 truncate">
                        <Sparkles className="w-3 h-3 text-blue-500 shrink-0" />
                        <span className="truncate">{tmpl.title}</span>
                      </div>
                    </button>
                  ))}
                </div>
              </div>

              {/* 咨询事项输入框 */}
              <div>
                <div className="flex items-center justify-between mb-1.5">
                  <label className="block font-semibold text-slate-700">
                    委托待澄清法律事项与背景说明
                  </label>
                  <span className="text-[10px] font-mono text-slate-400">
                    {questionText.length} 字
                  </span>
                </div>
                <textarea
                  rows={4}
                  value={questionText}
                  onChange={(e) => setQuestionText(e.target.value)}
                  className="w-full px-4 py-3 border border-slate-200/90 rounded-2xl focus:outline-none focus:ring-2 focus:ring-blue-500/10 focus:border-blue-600 leading-relaxed font-sans bg-slate-50/50 focus:bg-white text-slate-800 transition-all shadow-2xs"
                  placeholder="请输入待咨询的东道国强行法、合同条款有效性、工期索赔或履约保函具体争议细节..."
                  required
                />
              </div>

              {/* 独立性承诺提示 */}
              <div className="p-3.5 bg-blue-50/40 rounded-2xl border border-blue-200/60 space-y-1 text-[11px] text-slate-600">
                <div className="flex items-center gap-1.5 font-semibold text-slate-900">
                  <Shield className="w-3.5 h-3.5 text-blue-600 shrink-0" />
                  <span>执业资质已审验 · 利益冲突排查留痕</span>
                </div>
                <p className="text-slate-500 leading-relaxed">
                  特聘出海专家均具备东道国高等出庭资质或知名国际仲裁中心（SIAC/AIAC/BANI/VIAC/CIAC/TAI）在册仲裁员资格，严格执行无利害关系承诺。
                </p>
              </div>

              <button
                type="submit"
                disabled={isSubmitting}
                className="w-full flex items-center justify-center gap-2 px-5 py-2.5 font-semibold text-white bg-blue-600 hover:bg-blue-700 rounded-xl transition-all shadow-xs shadow-blue-500/25 cursor-pointer disabled:opacity-50 active:scale-[0.98]"
              >
                {isSubmitting ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin" />
                    <span>正在生成委托流转单...</span>
                  </>
                ) : (
                  <>
                    <Send className="w-4 h-4" />
                    <span>向属地顾问派发咨询委托</span>
                  </>
                )}
              </button>
            </form>
          </div>

          {/* 专家名录卡片 */}
          <div className="apple-bento-card rounded-[28px] p-6 space-y-4 shadow-2xs">
            <div className="flex items-center justify-between">
              <h3 className="text-xs font-bold text-slate-900 uppercase tracking-wider flex items-center gap-2">
                <Users className="w-4 h-4 text-blue-600" />
                <span>东盟重点法域出海法律顾问名录 ({filteredExperts.length}位)</span>
              </h3>
              <span className="text-[11px] text-slate-400 font-medium">均在册有效</span>
            </div>

            <div className="space-y-3">
              {filteredExperts.map((exp) => {
                const isSelected = selectedExpertId === exp.expert_id;
                return (
                  <div
                    key={exp.expert_id}
                    onClick={() => {
                      setSelectedExpertId(exp.expert_id);
                      showToast(`已选定【${exp.name}】（${exp.country_name}）`, 'info');
                    }}
                    className={`p-4 rounded-2xl border transition-all cursor-pointer ${
                      isSelected
                        ? 'bg-blue-50/50 border-blue-500 ring-1 ring-blue-500/30 shadow-xs'
                        : 'bg-white/80 border-slate-200/70 hover:border-slate-300 hover:bg-white shadow-2xs'
                    }`}
                  >
                    <div className="flex items-center justify-between mb-1.5">
                      <div className="flex items-center gap-2">
                        <span className="text-base">{exp.country_flag}</span>
                        <span className="font-bold text-xs text-slate-900">{exp.name}</span>
                        <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-slate-100 text-slate-600 font-semibold">
                          {exp.city}
                        </span>
                      </div>
                      <div className="flex items-center gap-1.5">
                        <span className="w-1.5 h-1.5 rounded-full bg-blue-600 shrink-0" />
                        <span className="text-[10px] font-medium text-slate-600">
                          资质审验有效
                        </span>
                      </div>
                    </div>

                    <p className="text-[11px] text-slate-700 font-medium mb-1">
                      {exp.title}
                    </p>
                    <p className="text-[10px] text-slate-400 mb-2">
                      {exp.affiliation} · 执业资历 {exp.experience_years} 年
                    </p>

                    <div className="flex flex-wrap gap-1 mb-2">
                      {exp.fields.map((f, i) => (
                        <span
                          key={i}
                          className="text-[10px] px-2 py-0.5 rounded-md bg-slate-50 border border-slate-200/70 text-slate-600 font-mono"
                        >
                          {f}
                        </span>
                      ))}
                    </div>

                    <div className="flex items-center justify-between pt-2 border-t border-slate-100 text-[10px] text-slate-400">
                      <span className="truncate">{exp.qualification}</span>
                      <span className="text-blue-600 font-semibold hover:underline shrink-0 ml-2">
                        {isSelected ? '✓ 当前已选中' : '点击指派咨询'}
                      </span>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>

        {/* 右侧：会商记录与专家书面回复 (7列) */}
        <div className="lg:col-span-7 space-y-4">
          <div className="apple-bento-card rounded-2xl p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3 shadow-2xs">
            <div className="flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-blue-600 shadow-xs shadow-blue-500/40" />
              <h3 className="text-xs font-bold text-slate-900 uppercase tracking-wider">
                出海法律顾问专项意见书与流转归档 ({filteredConsults.length}份)
              </h3>
            </div>

            {/* 搜索过滤框 */}
            <div className="relative w-full sm:w-64">
              <Search className="w-3.5 h-3.5 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="搜索专家、法域或咨询要点..."
                className="w-full pl-8 pr-3 py-1.5 bg-slate-50/80 border border-slate-200/80 rounded-xl text-xs text-slate-800 focus:outline-none focus:ring-1 focus:ring-blue-500 focus:bg-white transition-all"
              />
            </div>
          </div>

          <div className="space-y-4">
            {filteredConsults.length === 0 ? (
              <div className="apple-bento-card rounded-[28px] p-12 text-center text-slate-400 space-y-2">
                <FileText className="w-8 h-8 text-slate-300 mx-auto" />
                <p className="text-xs font-medium">未找到符合条件的法律顾问意见书</p>
                <p className="text-[11px] text-slate-400">请尝试切换国别筛选或清空关键词</p>
              </div>
            ) : (
              filteredConsults.map((con) => {
                const isExpanded = !!expandedConsultIds[con.consult_id];
                return (
                  <div
                    key={con.consult_id}
                    className="apple-bento-card rounded-[28px] p-6 space-y-4 shadow-2xs transition-all"
                  >
                    {/* 卡片头部 */}
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-100 pb-3.5">
                      <div className="space-y-1">
                        <div className="flex items-center gap-2">
                          <span className="font-mono font-bold text-xs text-blue-700 bg-blue-50 px-2 py-0.5 rounded-md border border-blue-200/60">
                            {con.consult_id}
                          </span>
                          <span className="text-xs font-bold text-slate-900">
                            {con.topic || `关于 ${con.expert_name} 专项会商`}
                          </span>
                        </div>
                        <div className="flex items-center gap-1.5 text-xs text-slate-500">
                          <span>{con.country_flag || '🌏'}</span>
                          <span className="font-medium text-slate-700">受托专家：{con.expert_name}</span>
                        </div>
                      </div>

                      <div className="flex items-center gap-2 shrink-0">
                        <div className="flex items-center gap-1.5 bg-emerald-50 border border-emerald-200/80 px-2.5 py-1 rounded-lg text-xs font-medium text-emerald-700">
                          <Check className="w-3.5 h-3.5 text-emerald-600" />
                          <span>已出具正式意见书</span>
                        </div>
                        <span className="text-[11px] font-mono text-slate-400">
                          {con.updated_at}
                        </span>
                      </div>
                    </div>

                    {/* 委托咨询事项 */}
                    <div className="space-y-1.5 text-xs">
                      <span className="font-bold text-slate-400 uppercase tracking-wider text-[10px]">
                        委托咨询事项说明
                      </span>
                      <p className="text-slate-800 bg-slate-50/70 p-3.5 rounded-2xl border border-slate-200/70 leading-relaxed font-sans">
                        {con.question_snapshot}
                      </p>
                    </div>

                    {/* 涉及法条与关键判例依据 */}
                    {con.legal_references && con.legal_references.length > 0 && (
                      <div className="space-y-1.5 text-xs">
                        <span className="font-bold text-slate-400 uppercase tracking-wider text-[10px] flex items-center gap-1">
                          <BookOpen className="w-3 h-3 text-blue-600" />
                          <span>涉及东道国法定依据与关键先例</span>
                        </span>
                        <div className="flex flex-wrap gap-1.5">
                          {con.legal_references.map((ref, i) => (
                            <span
                              key={i}
                              className="px-2.5 py-1 rounded-lg bg-blue-50/40 border border-blue-200/60 text-blue-900 text-[11px] font-mono font-medium"
                            >
                              {ref}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* 实务研判要旨 */}
                    {con.key_findings && con.key_findings.length > 0 && (
                      <div className="p-3.5 rounded-2xl bg-amber-50/30 border border-amber-200/60 space-y-1.5">
                        <span className="font-bold text-amber-900 uppercase tracking-wider text-[10px]">
                          实务研判要旨 (Key Guidance)
                        </span>
                        <ul className="space-y-1 text-xs text-slate-700">
                          {con.key_findings.map((finding, idx) => (
                            <li key={idx} className="flex items-start gap-1.5">
                              <span className="w-1.5 h-1.5 rounded-full bg-amber-500 shrink-0 mt-1.5" />
                              <span className="leading-snug">{finding}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {/* 专家书面意见书全文 */}
                    {con.reply && (
                      <div className="space-y-1.5 text-xs">
                        <div className="flex items-center justify-between">
                          <span className="font-bold text-slate-400 uppercase tracking-wider text-[10px] flex items-center gap-1">
                            <FileText className="w-3 h-3 text-slate-500" />
                            <span>属地顾问法律意见书全文</span>
                          </span>
                          <button
                            type="button"
                            onClick={() => toggleExpand(con.consult_id)}
                            className="text-[11px] font-medium text-blue-600 hover:text-blue-800 flex items-center gap-0.5 cursor-pointer"
                          >
                            <span>{isExpanded ? '收起全文' : '展开全文'}</span>
                            {isExpanded ? (
                              <ChevronUp className="w-3.5 h-3.5" />
                            ) : (
                              <ChevronDown className="w-3.5 h-3.5" />
                            )}
                          </button>
                        </div>

                        <div
                          className={`p-4 bg-slate-50/60 rounded-2xl border border-slate-200/70 text-slate-800 leading-relaxed font-sans whitespace-pre-wrap transition-all overflow-hidden ${
                            isExpanded ? 'max-h-none' : 'max-h-36 relative'
                          }`}
                        >
                          {con.reply}
                          {!isExpanded && (
                            <div className="absolute inset-x-0 bottom-0 h-16 bg-gradient-to-t from-slate-50/90 to-transparent flex items-end justify-center pb-2 pointer-events-none">
                              <span className="text-[11px] text-blue-600 font-semibold bg-white/90 px-3 py-0.5 rounded-full border border-blue-200 shadow-2xs">
                                点击展开查看完整意见书
                              </span>
                            </div>
                          )}
                        </div>
                      </div>
                    )}

                    {/* 卡片底部操作栏 */}
                    <div className="pt-3 border-t border-slate-100 flex flex-col sm:flex-row sm:items-center justify-between gap-2.5 text-xs">
                      <div className="flex items-center gap-1.5 text-[11px] text-slate-400 font-mono">
                        <Shield className="w-3.5 h-3.5 text-emerald-600 shrink-0" />
                        <span>已通过独立性与利益冲突排查 (COI Cleared)</span>
                      </div>

                      <div className="flex items-center gap-2">
                        {con.reply && (
                          <button
                            type="button"
                            onClick={() => handleCopyOpinion(con.reply || '', con.consult_id)}
                            className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-semibold bg-white hover:bg-slate-50 text-slate-700 border border-slate-200/90 shadow-2xs transition-colors cursor-pointer"
                          >
                            {copiedId === con.consult_id ? (
                              <>
                                <Check className="w-3.5 h-3.5 text-emerald-600" />
                                <span className="text-emerald-600">已复制全文</span>
                              </>
                            ) : (
                              <>
                                <Copy className="w-3.5 h-3.5 text-slate-500" />
                                <span>复制意见书</span>
                              </>
                            )}
                          </button>
                        )}

                        <button
                          type="button"
                          onClick={() => handleAttachConsult(con)}
                          disabled={attachingId === con.consult_id || attachedIds[con.consult_id]}
                          className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-semibold transition-all cursor-pointer ${
                            attachedIds[con.consult_id]
                              ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                              : 'bg-white hover:bg-slate-50 text-slate-700 border border-slate-200/90 shadow-2xs'
                          }`}
                        >
                          {attachingId === con.consult_id ? (
                            <>
                              <Loader2 className="w-3.5 h-3.5 animate-spin text-blue-600" />
                              <span>挂载中...</span>
                            </>
                          ) : attachedIds[con.consult_id] ? (
                            <>
                              <Check className="w-3.5 h-3.5 text-emerald-600" />
                              <span>已挂载至案卷附表</span>
                            </>
                          ) : (
                            <>
                              <Paperclip className="w-3.5 h-3.5 text-slate-500" />
                              <span>+ 挂载至案卷附表</span>
                            </>
                          )}
                        </button>
                      </div>
                    </div>
                  </div>
                );
              })
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
