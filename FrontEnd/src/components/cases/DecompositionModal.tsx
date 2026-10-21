import React, { useState } from 'react';
import { useApp } from '../../context/AppContext';
import { lawAgentApi } from '../../api/lawAgentApi';
import { Issue, LegalQuestion, Fact } from '../../types/lawAgent';
import { CheckCircle2, Plus, Trash2, ListChecks, ArrowRight, ShieldCheck } from 'lucide-react';

interface DecompositionModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const DecompositionModal: React.FC<DecompositionModalProps> = ({ isOpen, onClose }) => {
  const { currentCase, refreshCurrentCase, showToast } = useApp();
  const [issues, setIssues] = useState<Issue[]>(currentCase?.issues || []);
  const [questions, setQuestions] = useState<LegalQuestion[]>(currentCase?.questions || []);
  const [facts, setFacts] = useState<Fact[]>(currentCase?.facts || []);
  const [loading, setLoading] = useState(false);

  if (!isOpen || !currentCase) return null;

  const isPreInvestment =
    currentCase.meta?.stage === 'pre_investment' ||
    currentCase.meta?.lifecycle_stage === 'pre_investment' ||
    currentCase.meta?.lifecycle_stage === ('bidding_investment' as any);

  const handleToggleFactDispute = (fid: string) => {
    setFacts(
      facts.map((f) => (f.fid === fid ? { ...f, disputed: !f.disputed } : f))
    );
  };

  const handleAddIssue = () => {
    const newId = `ISSUE-${issues.length + 1}`;
    setIssues([
      ...issues,
      {
        issue_id: newId,
        kind: 'law',
        text_zh: '',
        claim_ids: ['C1'],
        element_ids: ['e1'],
      },
    ]);
  };

  const handleRemoveIssue = (index: number) => {
    setIssues(issues.filter((_, idx) => idx !== index));
  };

  const handleConfirm = async () => {
    setLoading(true);
    try {
      await lawAgentApi.confirmGate(currentCase.case_id, 's3', {
        issues: issues.filter((i) => i.text_zh.trim()),
        questions,
      });
      await refreshCurrentCase();
      showToast(isPreInvestment ? 'S3 投前合规要项清单已确认，工作流继续执行' : 'S3 争点需求单已确认，工作流继续执行', 'success');
      onClose();
    } catch (err: any) {
      showToast(err.message || '确认失败', 'error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/40 backdrop-blur-md p-4 apple-modal-backdrop">
      <div className="bg-white rounded-[24px] border border-black/[0.08] max-w-3xl w-full p-6 shadow-[0_24px_64px_rgba(0,0,0,0.18)] space-y-5 max-h-[90vh] overflow-y-auto apple-modal-card">
        <div className="flex items-start gap-3 border-b border-slate-100 pb-4">
          <div className="w-8 h-8 rounded-xl bg-slate-900 text-white flex items-center justify-center shrink-0">
            <ListChecks className="w-4 h-4 text-slate-100" />
          </div>
          <div>
            <h3 className="text-sm font-semibold text-slate-900">
              {isPreInvestment
                ? 'S3 投前合规审查要项拆解与核查清单人工确认 (Interrupt Gate)'
                : 'S3 查明事项拆解与争点需求单人工确认 (Interrupt Gate)'}
            </h3>
            <p className="text-xs text-slate-500 mt-0.5">
              {isPreInvestment
                ? '区分东道国外资准入要件与合规事实核查；人工标记待核实前置要项；锁定投前检索与政策调查查询式'
                : '区分工程事实争点与法律争点；人工标记双方争议事实；锁定进入东道国与 FIDIC 检索的双语查询式'}
            </p>
          </div>
        </div>

        {/* 事实争议标记区 (F29: 人工确认哪些事实有争议/待核实) */}
        <div className="space-y-2">
          <label className="block text-xs font-semibold text-slate-800 uppercase tracking-wider">
            {isPreInvestment
              ? '1. 投资背景事实 F# 待核查标记 (影响要件评估中待补充/存疑状态)'
              : '1. 案情事实 F# 争议标记 (影响 Matcher 四态中 disputed 判定)'}
          </label>
          <div className="space-y-1.5 bg-slate-50/80 p-3.5 rounded-xl border border-slate-100 text-xs">
            {facts.map((fact) => (
              <div
                key={fact.fid}
                className="flex items-center justify-between gap-3 py-1.5 border-b border-slate-200/50 last:border-0"
              >
                <div className="flex items-start gap-2">
                  <span className="font-mono font-semibold text-slate-900 shrink-0">
                    [{fact.fid}]
                  </span>
                  <span className="text-slate-700 leading-normal">{fact.text_zh}</span>
                </div>
                <button
                  type="button"
                  onClick={() => handleToggleFactDispute(fact.fid)}
                  className={`px-3 py-1 rounded-lg text-[11px] font-medium shrink-0 transition-colors duration-150 cursor-pointer ${
                    fact.disputed
                      ? 'bg-slate-900 text-white border border-slate-900'
                      : 'bg-slate-200/70 text-slate-700 hover:bg-slate-300/80'
                  }`}
                >
                  {isPreInvestment
                    ? fact.disputed
                      ? '待穿透核验 (Disputed / Pending)'
                      : '基本核实 (Verified)'
                    : fact.disputed
                    ? '双方存在争议 (Disputed)'
                    : '客观无争议事实'}
                </button>
              </div>
            ))}
          </div>
        </div>

        {/* 争点清单编辑 */}
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <label className="text-xs font-semibold text-slate-800 uppercase tracking-wider">
              {isPreInvestment
                ? '2. 提炼之投前合规审查要项 (法律强行法 / 商业与技术资质)'
                : '2. 提炼之争议焦点 (事实争点 / 法律争点)'}
            </label>
            <button
              type="button"
              onClick={handleAddIssue}
              className="flex items-center gap-1 text-xs text-slate-700 hover:text-slate-900 font-medium cursor-pointer"
            >
              <Plus className="w-3.5 h-3.5" />
              <span>{isPreInvestment ? '添加合规要项' : '添加争点'}</span>
            </button>
          </div>

          <div className="space-y-2">
            {issues.map((issue, idx) => (
              <div
                key={issue.issue_id}
                className="p-3 bg-slate-50/80 rounded-xl border border-slate-100 grid grid-cols-12 gap-3 items-center text-xs"
              >
                <div className="col-span-3">
                  <select
                    value={issue.kind}
                    onChange={(e) => {
                      const copy = [...issues];
                      copy[idx].kind = e.target.value as 'fact' | 'law';
                      setIssues(copy);
                    }}
                    className="w-full px-2.5 py-1.5 text-xs border border-slate-200 rounded-lg bg-white font-medium"
                  >
                    <option value="law">{isPreInvestment ? '东道国强行法审查要项' : '法律规范争点'}</option>
                    <option value="fact">{isPreInvestment ? '外资准入与资质核验' : '案情事实争点'}</option>
                  </select>
                </div>
                <div className="col-span-8">
                  <input
                    type="text"
                    value={issue.text_zh}
                    onChange={(e) => {
                      const copy = [...issues];
                      copy[idx].text_zh = e.target.value;
                      setIssues(copy);
                    }}
                    placeholder={isPreInvestment ? '输入投前准入审查要项表述...' : '输入争点表述...'}
                    className="w-full px-3 py-1.5 text-xs border border-slate-200 rounded-lg bg-white"
                  />
                </div>
                <div className="col-span-1 text-right">
                  <button
                    type="button"
                    onClick={() => handleRemoveIssue(idx)}
                    className="text-slate-400 hover:text-rose-600 p-1 cursor-pointer"
                  >
                    <Trash2 className="w-3.5 h-3.5" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* 底部确认操作 */}
        <div className="flex items-center justify-between pt-4 border-t border-slate-100">
          <span className="text-[11px] text-slate-400 font-mono">
            {isPreInvestment
              ? '人工确认后将锁定合规要项并启动东道国投资法典与外资准入先例检索'
              : '人工确认后将锁定争点并启动东盟法源与工程先例混合检索'}
          </span>
          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-xs text-slate-600 hover:text-slate-900 font-medium rounded-xl hover:bg-slate-100 transition-colors cursor-pointer"
            >
              稍后确认
            </button>
            <button
              type="button"
              disabled={loading}
              onClick={handleConfirm}
              className="flex items-center gap-1.5 px-4.5 py-2 text-xs font-medium text-white bg-slate-900 hover:bg-slate-800 rounded-xl transition-all cursor-pointer shadow-sm disabled:opacity-50"
            >
              <CheckCircle2 className="w-3.5 h-3.5" />
              <span>{loading ? '确认中...' : isPreInvestment ? '确认要项并启动检索' : '确认需求单并执行检索'}</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
