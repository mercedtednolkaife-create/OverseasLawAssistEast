import React, { useState } from 'react';
import { useApp } from '../../context/AppContext';
import { lawAgentApi } from '../../api/lawAgentApi';
import { MaterialVerificationResult } from '../../types/lawAgent';
import { ShieldCheck, FileText, CheckCircle2, AlertTriangle, XCircle, ArrowRight, BookOpen, Layers } from 'lucide-react';

export const MaterialVerificationView: React.FC = () => {
  const { currentCase, openLawModal, showToast } = useApp();

  const aseanDefaultText = `对方当事人（外方业主）在来函中提出了以下法律依据与抗辩理由：
1. 引用 FIDIC 银皮书第 20.1 款：“承包商必须在知悉事件后 28 天内发出索赔通知，否则丧失一切工期顺延与费用补偿救济权利”。
2. 引用印度尼西亚 2009 年第 24 号《语言法》主张合同未签署印尼语版本自始绝对无效，但忽视印尼最高院 SEMA 3/2023 善意有效裁判规则。
3. 引用马来西亚 CIPAA 2012 第 35 条，主张总包与分包合同中约定的背靠背付款条款自始绝对无效。`;

  const [inputText, setInputText] = useState(aseanDefaultText);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<MaterialVerificationResult | null>(null);

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
      showToast('请先输入需要核验的外国法条文或抗辩文本', 'warning');
      return;
    }
    setLoading(true);
    try {
      const res = await lawAgentApi.verifyForeignMaterials(inputText);
      setResult(res);
      showToast('材料核验比对已完成', 'success');
    } catch (err: any) {
      showToast(err.message || '核验请求失败，请稍后重试', 'error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="apple-page-pane max-w-[1600px] mx-auto px-4 sm:px-6 py-6 space-y-6">
      {/* 头部标题卡片 */}
      <div className="apple-bento-card rounded-[28px] p-6 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="space-y-1">
          <div className="flex items-center gap-2.5">
            <div className="w-9 h-9 rounded-2xl bg-blue-50 border border-blue-200/60 text-blue-600 flex items-center justify-center shrink-0 shadow-2xs">
              <ShieldCheck className="w-4 h-4 text-blue-600" />
            </div>
            <h1 className="text-lg font-bold text-slate-900 tracking-tight">
              外国法材料真实性与有效性核验
            </h1>
          </div>
          <p className="text-xs text-slate-500 pl-11.5">
            对当事人主张或提交的东盟六国成文法典、司法通告、FIDIC 标准条款及裁判先例进行真实性比对与现行效力核验
          </p>
        </div>
      </div>

      {/* 文本输入框 */}
      <div className="apple-bento-card rounded-[28px] p-6 space-y-4">
        <div>
          <label className="block text-xs font-semibold text-slate-700 mb-2">
            粘贴对方当事人提交的东盟属地法抗辩意见或建设工程涉外法查明材料文本
          </label>
          <textarea
            rows={5}
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="粘贴含东盟成文法条文（如 SEMA 3/2023、CIPAA Sec 35）、FIDIC 标准条款或司法仲裁先例引证文本..."
            className="w-full px-4 py-3 text-xs border border-slate-200/90 rounded-2xl focus:outline-none focus:ring-2 focus:ring-blue-500/10 focus:border-blue-600/80 font-mono text-slate-800 leading-relaxed bg-slate-50/50 focus:bg-white transition-all shadow-2xs"
          />
        </div>

        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <span className="text-[11px] text-slate-400 font-mono">
            支持自动识别东盟现行法条、FIDIC 条款及 SIAC/属地裁判案号并核验文字一致率
          </span>
          <button
            onClick={handleVerify}
            disabled={loading}
            className="flex items-center justify-center gap-2 px-5 py-2.5 text-xs font-semibold text-white bg-blue-600 hover:bg-blue-700 rounded-xl transition-all shadow-xs shadow-blue-500/25 disabled:opacity-50 cursor-pointer shrink-0 active:scale-[0.98]"
          >
            <span>{loading ? '正在比对官方库源...' : '执行智能核验'}</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>

      {/* 核验报告结果 */}
      {result && (
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
                  {result.summary.risk_count} 处提示修订过渡
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
                    </td>

                    <td className="px-5 py-4">
                      {it.has_full_text ? (
                        <span className="text-slate-700 font-mono text-[11px] bg-slate-100 px-2 py-0.5 rounded-lg border border-slate-200/80">
                          具备全文
                        </span>
                      ) : (
                        <span className="text-rose-600 font-mono text-[11px]">缺判例全文</span>
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
