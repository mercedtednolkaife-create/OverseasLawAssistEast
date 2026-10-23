import React, { useState, useEffect } from 'react';
import { useApp } from '../../context/AppContext';
import { lawAgentApi } from '../../api/lawAgentApi';
import { Expert, ConsultRecord } from '../../types/lawAgent';
import { Users, Send, CheckCircle2, FileText, Download, UserCheck, Shield, Paperclip, Check, Loader2 } from 'lucide-react';

export const ExpertConsultsView: React.FC = () => {
  const { currentCase, currentCaseId, refreshCurrentCase, showToast } = useApp();
  const [experts, setExperts] = useState<Expert[]>([]);
  const [consults, setConsults] = useState<ConsultRecord[]>([]);
  const [selectedExpertId, setSelectedExpertId] = useState<string>('');
  const [questionText, setQuestionText] = useState(
    '针对东盟东道国基建工程与跨境投资项目，请就东道国强行法（如印尼 SEMA 3/2023 语言合规、大马 CIPAA 35 背靠背无效、泰 FBA 外资限制、菲 PCAB 施工资质与 FIDIC 8.4/20.1 时效）出具权威专家法律意见。'
  );
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [attachingId, setAttachingId] = useState<string | null>(null);
  const [attachedIds, setAttachedIds] = useState<Record<string, boolean>>({});

  const loadData = async () => {
    try {
      const expList = await lawAgentApi.getExperts();
      const safeExp = Array.isArray(expList) ? expList : [];
      setExperts(safeExp);
      if (safeExp.length > 0 && !selectedExpertId) {
        setSelectedExpertId(safeExp[0].expert_id);
      }
      const consList = await lawAgentApi.getConsults(currentCase?.case_id);
      setConsults(Array.isArray(consList) ? consList : []);
    } catch (err: any) {
      showToast(err.message || '加载专家与会商数据失败', 'error');
    }
  };

  useEffect(() => {
    loadData();
  }, [currentCase?.case_id]);

  const handleAttachConsult = async (con: ConsultRecord) => {
    if (!currentCaseId) {
      showToast('请先选择或创建一个目标案卷以挂载会商意见', 'warning');
      return;
    }
    setAttachingId(con.consult_id);
    try {
      await lawAgentApi.attachCaseArtifact(currentCaseId, {
        artifact_type: 'expert_coi',
        title: `Local Counsel 专家会商意见 - ${con.expert_name}`,
        jurisdiction: currentCase?.meta?.jurisdiction || 'asean_id',
        summary: `特邀属地专家 ${con.expert_name} 就「${con.question_snapshot.slice(0, 60)}...」出具专项法律意见，已通过利益冲突审查并形成合规归档。`,
      });
      setAttachedIds((prev) => ({ ...prev, [con.consult_id]: true }));
      showToast(`✓ 已成功将专家会商记录挂载至案卷【${currentCaseId}】`, 'success');
      await refreshCurrentCase();
    } catch (e: any) {
      showToast(e.message || '挂载失败', 'error');
    } finally {
      setAttachingId(null);
    }
  };

  const handleCreateConsult = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!currentCase || !selectedExpertId) return;

    setIsSubmitting(true);
    try {
      await lawAgentApi.createConsult({
        case_id: currentCase.case_id,
        expert_id: selectedExpertId,
        question_snapshot: questionText,
        evidence_summary: `涉及法条: FIDIC 银皮书 Clause 20.1, 印尼 2017 年第 2 号建筑法第 30 条, 最高法院通告 SEMA 3/2023`,
      });
      await loadData();
      showToast('专家查明会商委托单已生成并进入流转', 'success');
    } catch (err: any) {
      showToast(err.message || '委托创建失败', 'error');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="apple-page-pane max-w-[1600px] mx-auto px-4 sm:px-6 py-6 space-y-6">
      {/* 头部标题卡片 */}
      <div className="apple-bento-card rounded-[28px] p-6 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="space-y-1">
          <div className="flex items-center gap-2.5">
            <div className="w-9 h-9 rounded-2xl bg-blue-50 border border-blue-200/60 text-blue-600 flex items-center justify-center shrink-0 shadow-2xs">
              <Users className="w-4 h-4 text-blue-600" />
            </div>
            <h1 className="text-lg font-bold text-slate-900 tracking-tight">
              东盟 Local Counsel 与 FIDIC DAAB 专家会商管理
            </h1>
          </div>
          <p className="text-xs text-slate-500 pl-11.5">
            特邀印尼、新加坡、大马、越南、泰国、菲律宾六国属地执业大律师与 FIDIC DAAB 裁决人，开展利益冲突排除与专家意见留痕
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* 左侧：会商发起与专家资质库 (5列) */}
        <div className="lg:col-span-5 space-y-6">
          {/* 发起专家咨询表单 */}
          <div className="apple-bento-card rounded-[28px] p-6 space-y-4 shadow-2xs">
            <h3 className="text-xs font-bold text-slate-900 uppercase tracking-wider flex items-center gap-2">
              <FileText className="w-4 h-4 text-blue-600" />
              发起东盟属地大律师 / DAAB 专家会商委托单
            </h3>

            <form onSubmit={handleCreateConsult} className="space-y-4 text-xs">
              <div>
                <label className="block font-semibold text-slate-700 mb-1.5">
                  选择咨询专家 (已完成利益冲突审查)
                </label>
                <select
                  value={selectedExpertId}
                  onChange={(e) => setSelectedExpertId(e.target.value)}
                  className="w-full px-3.5 py-2.5 border border-slate-200/80 rounded-xl bg-white font-medium focus:outline-none focus:ring-2 focus:ring-blue-500/10 focus:border-blue-600/80 text-slate-800 shadow-2xs cursor-pointer"
                >
                  {experts.map((exp) => (
                    <option key={exp.expert_id} value={exp.expert_id}>
                      {exp.name} · {exp.affiliation}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block font-semibold text-slate-700 mb-1.5">
                  委托咨询待澄清事项说明
                </label>
                <textarea
                  rows={4}
                  value={questionText}
                  onChange={(e) => setQuestionText(e.target.value)}
                  className="w-full px-4 py-3 border border-slate-200/90 rounded-2xl focus:outline-none focus:ring-2 focus:ring-blue-500/10 focus:border-blue-600/80 leading-relaxed font-sans bg-slate-50/50 focus:bg-white text-slate-800 transition-all shadow-2xs"
                  required
                />
              </div>

              <div className="p-4 bg-slate-50/80 rounded-2xl border border-slate-200/70 space-y-1 text-[11px] text-slate-600">
                <div className="flex items-center gap-1.5 font-semibold text-slate-900">
                  <Shield className="w-3.5 h-3.5 text-blue-600" />
                  独立性与无利害关系承诺
                </div>
                <p>入库特聘专家均已提交无利害关系声明，严格排除当事人利益冲突。</p>
              </div>

              <button
                type="submit"
                disabled={isSubmitting}
                className="w-full flex items-center justify-center gap-2 px-5 py-2.5 font-semibold text-white bg-blue-600 hover:bg-blue-700 rounded-xl transition-all shadow-xs shadow-blue-500/25 cursor-pointer disabled:opacity-50 active:scale-[0.98]"
              >
                <Send className="w-3.5 h-3.5" />
                <span>{isSubmitting ? '正在生成委托单...' : '生成会商委托单并派发'}</span>
              </button>
            </form>
          </div>

          {/* 专家名录卡片 */}
          <div className="apple-bento-card rounded-[28px] p-6 space-y-4">
            <h3 className="text-xs font-bold text-slate-900 uppercase tracking-wider">
              东盟六国特聘 Local Counsel 与 DAAB 专家名录 (6位权威专家)
            </h3>
            <div className="space-y-3">
              {experts.map((exp) => (
                <div
                  key={exp.expert_id}
                  className="p-4 bg-white/70 rounded-2xl border border-slate-200/70 text-xs space-y-1 hover:border-slate-300 transition-colors"
                >
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-slate-900">{exp.name}</span>
                    <div className="flex items-center gap-1.5">
                      <span className="w-1.5 h-1.5 rounded-full bg-blue-600 shrink-0" />
                      <span className="text-[11px] font-mono font-medium text-slate-700">
                        资质已审验
                      </span>
                    </div>
                  </div>
                  <p className="text-slate-700 font-medium">{exp.title}</p>
                  <p className="text-[11px] text-slate-400">{exp.affiliation}</p>
                  <div className="text-[10px] text-slate-500 pt-1 font-mono">
                    专业领域: {exp.fields.join(' · ')}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* 右侧：会商记录与专家书面回复 (7列) */}
        <div className="lg:col-span-7 space-y-4">
          <div className="flex items-center justify-between px-1">
            <h3 className="text-xs font-bold text-slate-900 uppercase tracking-wider">
              会商流转状态与专家书面意见 ({consults.length}份)
            </h3>
            <span className="text-xs text-slate-400 font-medium">独立归档存卷</span>
          </div>

          <div className="space-y-4">
            {consults.map((con) => (
              <div
                key={con.consult_id}
                className="apple-bento-card rounded-[28px] p-6 space-y-4"
              >
                <div className="flex items-center justify-between border-b border-slate-100 pb-3">
                  <div>
                    <span className="font-mono font-bold text-xs text-slate-900">
                      {con.consult_id}
                    </span>
                    <h4 className="text-xs font-medium text-slate-700 mt-0.5">
                      特邀专家: {con.expert_name}
                    </h4>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="flex items-center gap-1.5 bg-white/80 border border-slate-200/80 px-2.5 py-1 rounded-lg text-xs font-medium text-slate-700">
                      <span className="w-1.5 h-1.5 rounded-full bg-blue-600 shrink-0" />
                      <span>已出具意见书</span>
                    </div>
                    <span className="text-[11px] font-mono text-slate-400">
                      {con.updated_at}
                    </span>
                  </div>
                </div>

                {/* 咨询事项快照 */}
                <div className="text-xs space-y-1.5">
                  <span className="font-bold text-slate-400 uppercase tracking-wider text-[10px]">
                    委托咨询事项
                  </span>
                  <p className="text-slate-800 bg-slate-50/70 p-3 rounded-2xl border border-slate-200/70 leading-relaxed">
                    {con.question_snapshot}
                  </p>
                </div>

                {/* 专家回复全文 */}
                {con.reply && (
                  <div className="space-y-1.5 text-xs">
                    <span className="font-bold text-slate-400 uppercase tracking-wider text-[10px]">
                      专家书面意见书
                    </span>
                    <div className="p-4 bg-slate-50/60 rounded-2xl border border-slate-200/70 text-slate-900 leading-relaxed font-sans whitespace-pre-wrap">
                      {con.reply}
                    </div>
                  </div>
                )}

                {/* 挂载至案卷附表操作 */}
                <div className="pt-2 border-t border-slate-100 flex items-center justify-between text-xs">
                  <span className="text-[11px] text-slate-400 font-mono">
                    已通过 SIAC/Local Bar 利益冲突 (COI) 合规认证
                  </span>
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
                        <span>+ 挂载会商记录至当前案卷</span>
                      </>
                    )}
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
