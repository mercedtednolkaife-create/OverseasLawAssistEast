import React, { useState } from 'react';
import { useApp } from '../../context/AppContext';
import { lawAgentApi } from '../../api/lawAgentApi';
import { MaterialVerificationResult } from '../../types/lawAgent';
import {
  ShieldCheck,
  FileText,
  CheckCircle2,
  AlertTriangle,
  XCircle,
  ArrowRight,
  BookOpen,
  Layers,
  Copy,
  Check,
  Sparkles,
  FileSearch,
  Scale
} from 'lucide-react';

export const MaterialVerificationView: React.FC = () => {
  const { currentCase, openLawModal, showToast } = useApp();

  const [verifyMode, setVerifyMode] = useState<'CONTRACT_REDLINE_AUDIT' | 'CITATION_CHECK'>('CONTRACT_REDLINE_AUDIT');

  const sampleClauses = [
    {
      label: '印尼单语种英文合同与排除印尼语条款',
      text: `Clause 28.4 (Governing Law & Language): This Contract is executed solely in the English language. In no event shall any Bahasa Indonesia version be required, executed, or referred to. The parties expressly waive the application of Indonesian Law No. 24 of 2009 regarding the mandatory use of the Indonesian national language in commercial agreements.`
    },
    {
      label: '马来西亚/新加坡 EPC 分包背靠背 Pay-When-Paid 条款',
      text: `Clause 14.8 (Subcontractor Interim Payments): Payment to the Subcontractor shall be strictly conditional upon receipt of payment by the Main Contractor from the Employer (Pay-when-paid). If the Employer withholds or delays progress payments for any reason, the Contractor shall have no obligation to disburse funds to the Subcontractor.`
    },
    {
      label: '见索即付保函放弃止付禁令与排除法律变更调价条款',
      text: `Clause 4.2 & 13.7 (Performance Security & Law Changes): The Contractor unconditionally and irrevocably waives any right to seek court injunctions or stop payment on the Performance Security, even in cases of alleged unconscionability. Furthermore, Sub-Clause 13.7 of FIDIC is deleted: no adjustment to Contract Price shall be made for changes in laws, taxation or TKDN local content quotas enacted after the Base Date.`
    }
  ];

  const [inputText, setInputText] = useState(sampleClauses[0].text);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<MaterialVerificationResult | null>(null);
  const [copiedIndex, setCopiedIndex] = useState<number | null>(null);

  const getMatchedEid = (refId: string): string => {
    if (!currentCase?.evidence) return 'E1';
    for (const [eid, ev] of Object.entries(currentCase.evidence)) {
      if (ev.ref_id && (refId.includes(ev.ref_id) || ev.ref_id.includes(refId))) {
        return eid;
      }
    }
    if (refId.includes('20.1') || refId.includes('20_1')) return 'E1';
    if (refId.includes('8.4') || refId.includes('8_4')) return 'E2';
    if (refId.includes('SEMA') || refId.includes('2023')) return 'E3';
    if (refId.includes('CIPAA') || refId.includes('35')) return 'E4';
    if (refId.includes('Mount') || refId.includes('Sophia')) return 'E5';
    if (refId.includes('4.2') || refId.includes('4_2')) return 'E6';
    return 'E1';
  };

  const handleVerify = async () => {
    if (!inputText.trim()) {
      showToast('请先输入需要核验的合同条款或外国法条文', 'warning');
      return;
    }
    setLoading(true);
    try {
      const res = await lawAgentApi.verifyForeignMaterials(inputText, verifyMode);
      setResult(res);
      showToast(
        verifyMode === 'CONTRACT_REDLINE_AUDIT'
          ? `合同红线体检完成：共检出 ${res.redline_items?.length || 0} 处强行法合规风险！`
          : '引证真实性核验比对已完成',
        'success'
      );
    } catch (err: any) {
      showToast(err.message || '核验请求失败，请稍后重试', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleCopyClause = (clause: string, idx: number) => {
    navigator.clipboard.writeText(clause);
    setCopiedIndex(idx);
    showToast('合规替代示范条款已复制到剪贴板！', 'success');
    setTimeout(() => setCopiedIndex(null), 2000);
  };

  return (
    <div className="apple-page-pane max-w-[1600px] mx-auto px-4 sm:px-6 py-6 space-y-6">
      {/* 头部标题卡片与工作台模式切换 */}
      <div className="apple-bento-card rounded-[28px] p-6 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="space-y-1">
          <div className="flex items-center gap-2.5">
            <div className="w-9 h-9 rounded-2xl bg-blue-50 border border-blue-200/60 text-blue-600 flex items-center justify-center shrink-0 shadow-2xs">
              <ShieldCheck className="w-4 h-4 text-blue-600" />
            </div>
            <h1 className="text-lg font-bold text-slate-900 tracking-tight">
              {verifyMode === 'CONTRACT_REDLINE_AUDIT'
                ? '出海工程合同条款强行法红线体检工作台'
                : '外国法证据材料与法律意见书真实性核验'}
            </h1>
          </div>
          <p className="text-xs text-slate-500 pl-11.5">
            {verifyMode === 'CONTRACT_REDLINE_AUDIT'
              ? '针对招标文件、EPC主合同与分包协议，扫描背靠背付款、单语种有效性、无上限违约金与保函止付等东盟强行法红线'
              : '对当事人主张或当地律所法律意见书中引用的东盟成文法典、司法通告、FIDIC 标准条款进行真实性比对与现行效力核验'}
          </p>
        </div>

        {/* 模式切换 Tab */}
        <div className="inline-flex items-center p-1 bg-slate-100 rounded-2xl self-start sm:self-auto border border-slate-200/60">
          <button
            type="button"
            onClick={() => {
              setVerifyMode('CONTRACT_REDLINE_AUDIT');
              setInputText(sampleClauses[0].text);
              setResult(null);
            }}
            className={`px-3.5 py-1.5 rounded-xl text-xs font-semibold transition-all cursor-pointer ${
              verifyMode === 'CONTRACT_REDLINE_AUDIT'
                ? 'bg-white text-slate-900 shadow-2xs'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            <span className="flex items-center gap-1.5">
              <Scale className="w-3.5 h-3.5 text-blue-600" />
              <span>合同条款红线体检</span>
            </span>
          </button>
          <button
            type="button"
            onClick={() => {
              setVerifyMode('CITATION_CHECK');
              setInputText(`1. FIDIC 银皮书第 20.1 款：承包商28天索赔通知失权抗辩。\n2. 印尼最高院 SEMA 3/2023 善意有效裁判规则。\n3. 马来西亚 CIPAA 2012 第 35 条背靠背付款无效。`);
              setResult(null);
            }}
            className={`px-3.5 py-1.5 rounded-xl text-xs font-semibold transition-all cursor-pointer ${
              verifyMode === 'CITATION_CHECK'
                ? 'bg-white text-slate-900 shadow-2xs'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            <span className="flex items-center gap-1.5">
              <FileSearch className="w-3.5 h-3.5 text-slate-700" />
              <span>律所意见书引证核验</span>
            </span>
          </button>
        </div>
      </div>

      {/* 典型示例快捷填入区 */}
      {verifyMode === 'CONTRACT_REDLINE_AUDIT' && (
        <div className="flex flex-wrap items-center gap-2 text-xs">
          <span className="text-slate-400 font-medium flex items-center gap-1">
            <Sparkles className="w-3.5 h-3.5 text-blue-500" />
            <span>东盟高频风险条款范本：</span>
          </span>
          {sampleClauses.map((sc, idx) => (
            <button
              key={idx}
              type="button"
              onClick={() => {
                setInputText(sc.text);
                setResult(null);
              }}
              className="px-3 py-1 bg-white hover:bg-slate-50 border border-slate-200/80 hover:border-blue-300 rounded-xl text-slate-700 transition-all cursor-pointer shadow-2xs active:scale-[0.98]"
            >
              {sc.label}
            </button>
          ))}
        </div>
      )}

      {/* 文本输入框 */}
      <div className="apple-bento-card rounded-[28px] p-6 space-y-4">
        <div>
          <label className="block text-xs font-semibold text-slate-700 mb-2">
            {verifyMode === 'CONTRACT_REDLINE_AUDIT'
              ? '粘贴待审查的英文/双语工程合同草案、专用条件变更或招标条款片段'
              : '粘贴对方当事人或当地律所出具的东盟法查明意见文本'}
          </label>
          <textarea
            rows={5}
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder={
              verifyMode === 'CONTRACT_REDLINE_AUDIT'
                ? "粘贴待体检的合同条款，如背靠背付款条款、语言排他条款、保函放弃抗辩条款、无上限违约金或删除法律调价条款..."
                : "粘贴含东盟成文法条文（如 SEMA 3/2023、CIPAA Sec 35）、FIDIC 标准条款或司法仲裁先例引证文本..."
            }
            className="w-full px-4 py-3 text-xs border border-slate-200/90 rounded-2xl focus:outline-none focus:ring-2 focus:ring-blue-500/10 focus:border-blue-600/80 font-mono text-slate-800 leading-relaxed bg-slate-50/50 focus:bg-white transition-all shadow-2xs"
          />
        </div>

        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <span className="text-[11px] text-slate-400 font-mono">
            {verifyMode === 'CONTRACT_REDLINE_AUDIT'
              ? '自动对齐印尼 SEMA 3/2023、大马 CIPAA 35、越南2025建设法、新加坡保函止付先例与 FIDIC 黄金原则'
              : '支持自动识别东盟现行法条、FIDIC 条款及 SIAC/属地裁判案号并核验文字一致率'}
          </span>
          <button
            onClick={handleVerify}
            disabled={loading}
            className="flex items-center justify-center gap-2 px-5 py-2.5 text-xs font-semibold text-white bg-blue-600 hover:bg-blue-700 rounded-xl transition-all shadow-xs shadow-blue-500/25 disabled:opacity-50 cursor-pointer shrink-0 active:scale-[0.98]"
          >
            <span>{loading ? '正在穿透扫描强行法库...' : (verifyMode === 'CONTRACT_REDLINE_AUDIT' ? '启动条款红线体检' : '执行智能核验')}</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>

      {/* 合同条款红线体检扫描结果卡片 */}
      {result && result.redline_items && result.redline_items.length > 0 && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
              <AlertTriangle className="w-4 h-4 text-rose-600" />
              <span>检测到 {result.redline_items.length} 处合同强行法违规风险条款 (Redline Audit Findings)</span>
            </h3>
            <span className="text-xs font-mono font-medium text-rose-600 bg-rose-50 px-2.5 py-1 rounded-xl border border-rose-200/60">
              触发东盟东道国强制法否定性后果
            </span>
          </div>

          <div className="grid grid-cols-1 gap-4">
            {result.redline_items.map((item, idx) => (
              <div
                key={idx}
                className="apple-bento-card rounded-[28px] p-6 space-y-4 border-l-4 border-l-rose-500"
              >
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <div className="flex items-center gap-2">
                    <span
                      className={`text-[10px] font-bold font-mono px-2 py-0.5 rounded-lg uppercase tracking-wider ${
                        item.risk_level === 'critical'
                          ? 'bg-rose-100 text-rose-700 border border-rose-200'
                          : 'bg-amber-100 text-amber-700 border border-amber-200'
                      }`}
                    >
                      {item.risk_level === 'critical' ? '致命红线 (Void Ab Initio)' : '高危违规 (High Risk)'}
                    </span>
                    <h4 className="text-xs font-bold text-slate-900">{item.violated_rule_title}</h4>
                  </div>
                  <span className="text-[11px] font-mono text-slate-500 bg-slate-100 px-2 py-0.5 rounded-md">
                    {item.violated_norm_id}
                  </span>
                </div>

                <div className="space-y-2 text-xs">
                  <div>
                    <span className="text-slate-400 font-medium">触发风险的原合同片段：</span>
                    <blockquote className="mt-1 p-3 bg-rose-50/50 rounded-xl border border-rose-100 font-mono text-slate-800 text-[11px] leading-relaxed">
                      {item.clause_snippet}
                    </blockquote>
                  </div>

                  <div>
                    <span className="text-slate-400 font-medium">东盟强行法与司法裁判依据：</span>
                    <p className="mt-1 text-slate-700 leading-relaxed">{item.mandatory_rule_desc}</p>
                  </div>

                  <div className="pt-2 border-t border-slate-100">
                    <div className="flex items-center justify-between mb-1.5">
                      <span className="font-semibold text-emerald-800 flex items-center gap-1.5">
                        <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
                        <span>推荐合规修改替代表述 (Recommended Clause Revision)：</span>
                      </span>
                      <button
                        type="button"
                        onClick={() => handleCopyClause(item.recommended_revision, idx)}
                        className="inline-flex items-center gap-1 px-2.5 py-1 text-[11px] font-medium text-emerald-700 bg-emerald-50 hover:bg-emerald-100/80 rounded-lg border border-emerald-200/80 transition-all cursor-pointer active:scale-[0.98]"
                      >
                        {copiedIndex === idx ? (
                          <>
                            <Check className="w-3 h-3 text-emerald-600" />
                            <span>已复制</span>
                          </>
                        ) : (
                          <>
                            <Copy className="w-3 h-3 text-emerald-600" />
                            <span>一键复制示范条款</span>
                          </>
                        )}
                      </button>
                    </div>
                    <div className="p-3 bg-emerald-50/40 rounded-xl border border-emerald-100 font-mono text-emerald-950 text-[11px] leading-relaxed select-all">
                      {item.recommended_revision}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 引证核验报告结果 */}
      {result && result.items && result.items.length > 0 && (
        <div className="apple-bento-card rounded-[28px] overflow-hidden space-y-4">
          <div className="p-5 border-b border-slate-100 bg-slate-50/80 flex flex-wrap items-center justify-between gap-4">
            <div>
              <h3 className="text-xs font-bold text-slate-900 uppercase tracking-wider flex items-center gap-2">
                <Layers className="w-4 h-4 text-slate-700" />
                核验结论汇总 (逐项法源比对)
              </h3>
              <p className="text-xs text-slate-500 mt-1">
                检出 {result.summary.total} 处法源引用 ·{' '}
                <span className="text-slate-900 font-mono font-semibold">
                  {result.summary.verified_count} 处完全一致
                </span>{' '}
                ·{' '}
                <span className="text-amber-700 font-mono font-semibold">
                  {result.summary.risk_count} 处提示风险
                </span>
              </p>
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs border-collapse">
              <thead>
                <tr className="border-b border-slate-100 bg-slate-50/50 text-[11px] font-semibold text-slate-500">
                  <th className="px-6 py-3.5">引述法源标的</th>
                  <th className="px-5 py-3.5">在库状态</th>
                  <th className="px-5 py-3.5">一致性判定</th>
                  <th className="px-5 py-3.5">判例全文要求</th>
                  <th className="px-6 py-3.5">核验说明与时点提示</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {result.items.map((it, idx) => (
                  <tr key={idx} className="hover:bg-slate-50/80 transition-colors duration-150">
                    <td className="px-6 py-4">
                      <div className="flex items-center gap-2">
                        <span className="font-mono font-bold text-slate-900">{it.ref_id}</span>
                        {it.in_db && (
                          <button
                            type="button"
                            onClick={() => openLawModal(getMatchedEid(it.ref_id))}
                            className="inline-flex items-center gap-1.5 text-[11px] font-medium text-slate-700 bg-white hover:bg-slate-50 px-2.5 py-1 rounded-xl border border-slate-200/90 transition-all shadow-2xs hover:border-slate-300 active:scale-[0.98] cursor-pointer"
                            title="查阅法源全文"
                          >
                            <BookOpen className="w-3 h-3 text-slate-600" />
                            <span>查阅条文</span>
                          </button>
                        )}
                      </div>
                    </td>

                    <td className="px-5 py-4">
                      {it.in_db ? (
                        <div className="flex items-center gap-1.5">
                          <span className="w-1.5 h-1.5 rounded-full bg-blue-600 shrink-0" />
                          <span className="font-mono text-[11px] font-medium text-slate-700">在库正文</span>
                        </div>
                      ) : (
                        <div className="flex items-center gap-1.5">
                          <span className="w-1.5 h-1.5 rounded-full bg-slate-300 shrink-0" />
                          <span className="font-mono text-[11px] font-medium text-slate-500">库外条目</span>
                        </div>
                      )}
                    </td>

                    <td className="px-5 py-4">
                      {it.consistency_verdict === 'exact' && (
                        <div className="flex items-center gap-1.5 text-xs text-slate-800 font-medium">
                          <span className="w-1.5 h-1.5 rounded-full bg-blue-600 shrink-0" />
                          <span>完全一致</span>
                        </div>
                      )}
                      {it.consistency_verdict === 'partial' && (
                        <div className="flex items-center gap-1.5 text-xs text-amber-700 font-medium">
                          <span className="w-1.5 h-1.5 rounded-full bg-amber-500 shrink-0" />
                          <span>提示过渡</span>
                        </div>
                      )}
                      {it.consistency_verdict === 'inconsistent' && (
                        <div className="flex items-center gap-1.5 text-xs text-rose-600 font-medium">
                          <span className="w-1.5 h-1.5 rounded-full bg-rose-500 shrink-0" />
                          <span>文本偏差</span>
                        </div>
                      )}
                      {it.consistency_verdict === 'unverified' && (
                        <div className="flex items-center gap-1.5 text-xs text-slate-500 font-medium">
                          <span className="w-1.5 h-1.5 rounded-full bg-slate-400 shrink-0" />
                          <span>待核实</span>
                        </div>
                      )}
                    </td>

                    <td className="px-5 py-4">
                      {it.has_full_text ? (
                        <span className="text-slate-700 font-mono text-[11px] bg-slate-100 px-2 py-0.5 rounded-lg border border-slate-200/80">
                          具备全文
                        </span>
                      ) : (
                        <span className="text-slate-400 font-mono text-[11px]">法条条文</span>
                      )}
                    </td>

                    <td className="px-6 py-4 text-slate-700 leading-relaxed text-xs">
                      <p>{it.note}</p>
                      <span className="text-[11px] text-slate-400 font-mono block mt-1">
                        {it.stand_note}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};
