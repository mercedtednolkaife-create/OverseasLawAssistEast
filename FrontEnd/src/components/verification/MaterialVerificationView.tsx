import React, { useState, useRef } from 'react';
import { useApp } from '../../context/AppContext';
import { lawAgentApi } from '../../api/lawAgentApi';
import { MaterialVerificationResult } from '../../types/lawAgent';
import {
  ShieldCheck,
  FileText,
  CheckCircle2,
  AlertTriangle,
  ArrowRight,
  BookOpen,
  Layers,
  Copy,
  Check,
  FileSearch,
  Paperclip,
  FolderPlus,
  Loader2,
  Scale,
  Sparkles,
  X,
  UploadCloud,
} from 'lucide-react';

export const MaterialVerificationView: React.FC = () => {
  const {
    currentCase,
    currentCaseId,
    openLawModal,
    showToast,
    openCaseEntryWithPrefill,
    refreshCurrentCase,
  } = useApp();

  const [verifyMode, setVerifyMode] = useState<'CONTRACT_REDLINE_AUDIT' | 'CITATION_CHECK'>('CONTRACT_REDLINE_AUDIT');
  const [attachingIdx, setAttachingIdx] = useState<number | null>(null);
  const [attachedIdxs, setAttachedIdxs] = useState<Record<number, boolean>>({});
  const [diffMode, setDiffMode] = useState<Record<number, boolean>>({});

  const fileInputRef = useRef<HTMLInputElement>(null);
  const [isParsingDoc, setIsParsingDoc] = useState<boolean>(false);

  const sampleClauses = [
    {
      label: '印尼单语种英文合同与排除印尼语',
      text: `Clause 28.4 (Governing Law & Language): This Contract is executed solely in the English language. In no event shall any Bahasa Indonesia version be required, executed, or referred to. The parties expressly waive the application of Indonesian Law No. 24 of 2009 regarding the mandatory use of the Indonesian national language in commercial agreements.`
    },
    {
      label: '马新分包背靠背支付 (Pay-When-Paid)',
      text: `Clause 14.8 (Subcontractor Interim Payments): Payment to the Subcontractor shall be strictly conditional upon receipt of payment by the Main Contractor from the Employer (Pay-when-paid). If the Employer withholds or delays progress payments for any reason, the Contractor shall have no obligation to disburse funds to the Subcontractor.`
    },
    {
      label: '见索即付保函放弃止付抗辩与调价排除',
      text: `Clause 4.2 & 13.7 (Performance Security & Law Changes): The Contractor unconditionally and irrevocably waives any right to seek court injunctions or stop payment on the Performance Security, even in cases of alleged unconscionability. Furthermore, Sub-Clause 13.7 of FIDIC is deleted: no adjustment to Contract Price shall be made for changes in laws, taxation or TKDN local content quotas enacted after the Base Date.`
    },
    {
      label: '泰国外商法 49% 外资限制与联合体条款',
      text: `Clause 18.2 (Contractor Nationality & Subcontracting): The Contractor represents that it is 100% foreign owned without a Foreign Business License (FBL) under Thai Foreign Business Act B.E. 2542 (1999) List 3(10), relying on Board of Investment (BOI) Category 7 infrastructure incentives.`
    },
    {
      label: '菲律宾 PCAB 外资承包商执照特别许可',
      text: `Clause 2.4 (Licensing Condition Precedent): Main Contractor shall hold a Regular PCAB Contractor License under RA 4566. Employer reserves the right to terminate if foreign ownership exceeds 40%, unless protected by Supreme Court precedent G.R. No. 217590 (PCAB v. Manila Water).`
    }
  ];

  const [inputText, setInputText] = useState(sampleClauses[0].text);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<MaterialVerificationResult | null>(null);
  const [copiedIndex, setCopiedIndex] = useState<number | null>(null);

  const handleFileUpload = async (file: File) => {
    try {
      setIsParsingDoc(true);
      showToast(`正在解析文件【${file.name}】...`, 'info');
      const res = await lawAgentApi.parseDocument(file);
      setInputText(res.text);
      showToast(`已提取【${file.name}】合同文本（${res.char_count} 字符）！`, 'success');
    } catch (e: any) {
      showToast(e.message || '文档解析失败', 'error');
    } finally {
      setIsParsingDoc(false);
    }
  };

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
      showToast('请先输入需要审查的合同条款或法律引证文本', 'warning');
      return;
    }
    setLoading(true);
    try {
      const res = await lawAgentApi.verifyForeignMaterials(inputText, verifyMode);
      setResult(res);
      showToast(
        verifyMode === 'CONTRACT_REDLINE_AUDIT'
          ? `合同合规审查完成：检出 ${res.redline_items?.length || 0} 处强行法合规风险！`
          : '引证真实性核验比对已完成',
        'success'
      );
    } catch (err: any) {
      showToast(err.message || '审查请求失败，请稍后重试', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleCopyClause = (clause: string, idx: number) => {
    navigator.clipboard.writeText(clause);
    setCopiedIndex(idx);
    showToast('示范条款已复制至剪贴板', 'success');
    setTimeout(() => setCopiedIndex(null), 2000);
  };

  const handleAttachArtifact = async (item: any, idx: number) => {
    if (!currentCaseId) {
      showToast('请先选择或新建目标案卷以挂载审查记录', 'warning');
      return;
    }
    setAttachingIdx(idx);
    try {
      await lawAgentApi.attachCaseArtifact(currentCaseId, {
        artifact_type: 'redline_scan',
        title: item.violated_rule_title || '合同强行法合规风险条款',
        jurisdiction: currentCase?.meta?.jurisdiction || 'asean_id',
        summary: item.mandatory_rule_desc || '强行法违规风险及后果说明',
        redline_clause: item.recommended_revision,
      });
      setAttachedIdxs((prev) => ({ ...prev, [idx]: true }));
      showToast(`✓ 已成功将该条款审查记录挂载至案卷【${currentCaseId}】附表`, 'success');
      await refreshCurrentCase();
    } catch (e: any) {
      showToast(e.message || '挂载失败', 'error');
    } finally {
      setAttachingIdx(null);
    }
  };

  const handleUpgradeToCase = (item: any) => {
    openCaseEntryWithPrefill({
      title: `${item.violated_rule_title || '涉外合同合规审查专案'}`,
      jurisdiction: currentCase?.meta?.jurisdiction || 'asean_id',
      governing_law: currentCase?.meta?.choice_of_law || currentCase?.meta?.jurisdiction || 'asean_sg',
      lifecycle_stage: 'execution_dispute',
      facts: `【涉案合同条款片段】\n"${item.clause_snippet}"\n\n【东道国法律依据】\n${item.mandatory_rule_desc}`,
      claims: `依据 ${item.violated_norm_id || '东道国法律与司法裁判先例'}，主张违规条款自始无效或依法予以合规重构，适用推荐合规替代条款。`,
    });
    showToast('已将该风险条款与法律依据填入立项面板！', 'info');
  };

  return (
    <div className="max-w-[1600px] mx-auto px-4 sm:px-6 py-6 space-y-6">
      {/* 头部标题卡片与工作台模式切换 */}
      <div className="apple-bento-card rounded-[28px] p-6 sm:p-7 relative overflow-hidden flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="relative z-10 max-w-4xl space-y-2">
          <div className="inline-flex items-center gap-2 px-2.5 py-1 rounded-full bg-blue-50 border border-blue-200/80 text-blue-700 text-xs font-semibold">
            <span className="w-1.5 h-1.5 rounded-full bg-blue-600 animate-pulse" />
            <span>东道国法定规范穿透 · FIDIC 黄金原则对齐 · 合规替代条款示范</span>
          </div>

          <h1 className="text-xl sm:text-2xl font-bold tracking-tight text-slate-900">
            {verifyMode === 'CONTRACT_REDLINE_AUDIT'
              ? '涉外工程合同合规审查'
              : '外国法条文引用与真实性核验'}
          </h1>

          <p className="text-xs sm:text-sm text-slate-600 leading-relaxed font-normal">
            {verifyMode === 'CONTRACT_REDLINE_AUDIT'
              ? '针对招标文件、EPC主合同与分包协议，系统审查背靠背付款、语言强制性、违约金法定上限与保函止付等涉外法律合规风险并输出替代建议。'
              : '对法律意见书或证据材料中引用的东盟成文法条、司法通告、FIDIC 标准条款进行现行有效性与引证一致率核验。'}
          </p>
        </div>

        {/* 模式切换 Tab (Apple 分段控制) */}
        <div className="relative z-10 inline-flex items-center p-1 bg-slate-100 rounded-2xl self-start sm:self-auto border border-slate-200/60 shadow-2xs">
          <button
            type="button"
            onClick={() => {
              setVerifyMode('CONTRACT_REDLINE_AUDIT');
              setInputText(sampleClauses[0].text);
              setResult(null);
            }}
            className={`px-3.5 py-2 rounded-xl text-xs font-semibold transition-all cursor-pointer ${
              verifyMode === 'CONTRACT_REDLINE_AUDIT'
                ? 'bg-white text-slate-900 shadow-2xs'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            <span className="flex items-center gap-1.5">
              <FileText className="w-3.5 h-3.5 text-blue-600" />
              <span>合同条款合规审查</span>
            </span>
          </button>

          <button
            type="button"
            onClick={() => {
              setVerifyMode('CITATION_CHECK');
              setInputText(
                `1. FIDIC 银皮书第 20.1 款：承包商28天索赔通知失权抗辩。\n2. 印尼最高院 SEMA 3/2023 善意有效裁判规则。\n3. 马来西亚 CIPAA 2012 第 35 条背靠背付款无效。`
              );
              setResult(null);
            }}
            className={`px-3.5 py-2 rounded-xl text-xs font-semibold transition-all cursor-pointer ${
              verifyMode === 'CITATION_CHECK'
                ? 'bg-white text-slate-900 shadow-2xs'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            <span className="flex items-center gap-1.5">
              <FileSearch className="w-3.5 h-3.5 text-slate-700" />
              <span>法源意见引证核验</span>
            </span>
          </button>
        </div>

        {/* 装饰水印 */}
        <div className="absolute right-6 -bottom-6 opacity-5 pointer-events-none hidden lg:block">
          <Scale className="w-56 h-56 text-slate-900" />
        </div>
      </div>

      {/* 典型风险条款示例快捷填入 */}
      {verifyMode === 'CONTRACT_REDLINE_AUDIT' && (
        <div className="flex flex-wrap items-center gap-2 text-xs">
          <span className="text-slate-400 font-medium flex items-center gap-1">
            <Sparkles className="w-3.5 h-3.5 text-blue-600" />
            <span>高频风险条款示例：</span>
          </span>
          {sampleClauses.map((sc, idx) => (
            <button
              key={idx}
              type="button"
              onClick={() => {
                setInputText(sc.text);
                setResult(null);
              }}
              className="px-3 py-1.5 bg-white/90 hover:bg-white border border-slate-200/80 hover:border-blue-400 rounded-xl text-slate-700 transition-all cursor-pointer shadow-2xs active:scale-[0.98]"
            >
              {sc.label}
            </button>
          ))}
        </div>
      )}

      {/* 文本输入与文件上传卡片 */}
      <div className="apple-bento-card rounded-[28px] p-6 space-y-4 shadow-2xs">
        <div>
          <div className="flex items-center justify-between mb-2">
            <label className="block text-xs font-semibold text-slate-700">
              {verifyMode === 'CONTRACT_REDLINE_AUDIT'
                ? '待审查合同条款草案或招标协议片段：'
                : '待核验法律意见书或证据引述文本：'}
            </label>
            <div className="flex items-center gap-2">
              <input
                ref={fileInputRef}
                type="file"
                accept=".docx,.txt,.md"
                className="hidden"
                onChange={(e) => {
                  const f = e.target.files?.[0];
                  if (f) handleFileUpload(f);
                }}
              />
              <button
                type="button"
                onClick={() => fileInputRef.current?.click()}
                disabled={isParsingDoc}
                className="px-3 py-1.5 text-xs font-semibold bg-white border border-slate-200/90 text-slate-700 hover:bg-slate-50 rounded-xl flex items-center gap-1.5 cursor-pointer shadow-2xs transition-all hover:border-slate-300"
              >
                <UploadCloud className="w-3.5 h-3.5 text-blue-600" />
                <span>{isParsingDoc ? '文档解析中...' : '上传/拖拽 .docx / .txt 合同'}</span>
              </button>
              {inputText && (
                <button
                  type="button"
                  onClick={() => {
                    setInputText('');
                    setResult(null);
                  }}
                  className="px-2.5 py-1.5 text-xs text-slate-400 hover:text-slate-600 cursor-pointer"
                  title="清空内容"
                >
                  <X className="w-3.5 h-3.5" />
                </button>
              )}
            </div>
          </div>

          <textarea
            rows={5}
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onDragOver={(e) => e.preventDefault()}
            onDrop={(e) => {
              e.preventDefault();
              const f = e.dataTransfer.files?.[0];
              if (f) handleFileUpload(f);
            }}
            placeholder={
              verifyMode === 'CONTRACT_REDLINE_AUDIT'
                ? '粘贴待审查的合同条款片段，或直接拖拽 .docx / .txt 文件至此 (如背靠背付款、单语种排他、保函放弃抗辩、无上限违约金)...'
                : '粘贴含东盟成文法条（如 SEMA 3/2023、CIPAA Sec 35）、FIDIC 标准条款或司法判例引证文本...'
            }
            className="w-full px-4 py-3 text-xs border border-slate-200/90 rounded-2xl focus:outline-none focus:ring-2 focus:ring-blue-500/10 focus:border-blue-600/80 font-mono text-slate-800 leading-relaxed bg-slate-50/50 focus:bg-white transition-all shadow-2xs"
          />
        </div>

        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pt-1 border-t border-slate-100">
          <span className="text-[11px] text-slate-400 font-mono">
            {verifyMode === 'CONTRACT_REDLINE_AUDIT'
              ? '比对印尼 SEMA 3/2023、大马 CIPAA 35、越南2025建设法、新加坡保函判例及 FIDIC 黄金原则'
              : '自动核验东盟成文法、FIDIC 规范及国际仲裁裁判引证的一致率与时点'}
          </span>
          <button
            onClick={handleVerify}
            disabled={loading}
            className="flex items-center justify-center gap-2 px-5 py-2.5 text-xs font-semibold text-white bg-blue-600 hover:bg-blue-700 rounded-xl transition-all shadow-xs shadow-blue-500/25 disabled:opacity-50 cursor-pointer shrink-0 active:scale-[0.98]"
          >
            {loading ? (
              <>
                <Loader2 className="w-3.5 h-3.5 animate-spin" />
                <span>正在审查东道国法律与合规规范...</span>
              </>
            ) : (
              <>
                <span>{verifyMode === 'CONTRACT_REDLINE_AUDIT' ? '执行合同合规审查' : '执行引证核验'}</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </>
            )}
          </button>
        </div>
      </div>

      {/* 合同条款合规审查结果展示 */}
      {result && result.redline_items && result.redline_items.length > 0 && (
        <div className="space-y-4">
          <div className="flex items-center justify-between px-1">
            <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
              <AlertTriangle className="w-4 h-4 text-rose-600" />
              <span>检出 {result.redline_items.length} 处涉外合规风险条款</span>
            </h3>
            <span className="text-xs font-mono font-medium text-rose-700 bg-rose-50 px-2.5 py-1 rounded-xl border border-rose-200/70">
              触发东道国法定规范否定性后果
            </span>
          </div>

          <div className="grid grid-cols-1 gap-4">
            {result.redline_items.map((item, idx) => (
              <div
                key={idx}
                className="apple-bento-card rounded-[28px] p-6 space-y-4 border-l-4 border-l-rose-500 shadow-2xs"
              >
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <div className="flex items-center gap-2">
                    <span
                      className={`text-[10px] font-bold font-mono px-2 py-0.5 rounded-lg uppercase tracking-wider ${
                        item.risk_level === 'critical'
                          ? 'bg-rose-100 text-rose-700 border border-rose-200'
                          : 'bg-amber-100 text-amber-800 border border-amber-200'
                      }`}
                    >
                      {item.risk_level === 'critical' ? '自始无效风险 (Void)' : '高危合规风险 (High Risk)'}
                    </span>
                    <h4 className="text-xs font-bold text-slate-900">{item.violated_rule_title}</h4>
                  </div>
                  <span className="text-[11px] font-mono text-slate-600 bg-slate-100 px-2 py-0.5 rounded-md border border-slate-200/70">
                    {item.violated_norm_id}
                  </span>
                </div>

                <div className="space-y-3 text-xs">
                  {/* 原合同条款 */}
                  <div>
                    <span className="text-slate-500 font-semibold block mb-1">
                      触发风险的原合同条款片段：
                    </span>
                    <blockquote className="p-3.5 bg-rose-50/60 rounded-xl border border-rose-200/70 font-mono text-rose-950 text-[11px] leading-relaxed">
                      {item.clause_snippet}
                    </blockquote>
                  </div>

                  {/* 法律依据 */}
                  <div>
                    <span className="text-slate-500 font-semibold block mb-1">
                      东道国法律与司法裁判依据：
                    </span>
                    <p className="p-3 bg-slate-50/80 rounded-xl border border-slate-200/70 text-slate-700 leading-relaxed font-sans">
                      {item.mandatory_rule_desc}
                    </p>
                  </div>

                  {/* 推荐修改方案 */}
                  <div className="pt-2 border-t border-slate-100 space-y-2">
                    <div className="flex flex-wrap items-center justify-between gap-2">
                      <div className="flex items-center gap-2">
                        <span className="font-semibold text-emerald-800 flex items-center gap-1.5 text-xs">
                          <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
                          <span>推荐合规修改替代表述：</span>
                        </span>
                        <div className="inline-flex items-center p-0.5 bg-slate-100 rounded-lg text-[10px] border border-slate-200/70">
                          <button
                            type="button"
                            onClick={() => setDiffMode({ ...diffMode, [idx]: false })}
                            className={`px-2 py-0.5 rounded font-medium cursor-pointer ${
                              !diffMode[idx] ? 'bg-white text-slate-900 shadow-2xs font-semibold' : 'text-slate-600'
                            }`}
                          >
                            完整示范
                          </button>
                          <button
                            type="button"
                            onClick={() => setDiffMode({ ...diffMode, [idx]: true })}
                            className={`px-2 py-0.5 rounded font-medium cursor-pointer ${
                              diffMode[idx] ? 'bg-white text-slate-900 shadow-2xs font-semibold' : 'text-slate-600'
                            }`}
                          >
                            增删对比 (Diff)
                          </button>
                        </div>
                      </div>

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
                            <span>复制示范条款</span>
                          </>
                        )}
                      </button>
                    </div>

                    {/* Diff 对比视图：采用 Apple 质感双色卡片，杜绝生硬大纯黑终端 */}
                    {diffMode[idx] ? (
                      <div className="space-y-2 font-mono text-[11px] leading-relaxed select-all">
                        <div className="p-3 bg-rose-50/70 rounded-xl border border-rose-200/80 text-rose-900 line-through space-y-1">
                          <span className="text-[10px] uppercase font-bold text-rose-600 font-sans block not-italic">
                            [- 建议删除原条款]
                          </span>
                          <span>{item.clause_snippet}</span>
                        </div>
                        <div className="p-3 bg-emerald-50/70 rounded-xl border border-emerald-200/80 text-emerald-950 font-semibold space-y-1">
                          <span className="text-[10px] uppercase font-bold text-emerald-700 font-sans block">
                            [+ 建议修改为合规表述]
                          </span>
                          <span>{item.recommended_revision}</span>
                        </div>
                      </div>
                    ) : (
                      <div className="p-3.5 bg-emerald-50/50 rounded-xl border border-emerald-200/70 font-mono text-emerald-950 text-[11px] leading-relaxed select-all">
                        {item.recommended_revision}
                      </div>
                    )}

                    {/* 动作闭环：挂载至案卷附表 + 以此条款立项 */}
                    <div className="pt-3 border-t border-slate-100 flex flex-wrap items-center justify-between gap-2.5">
                      <div className="flex items-center gap-1.5 text-[11px] text-slate-500">
                        <span className="w-1.5 h-1.5 rounded-full bg-blue-600" />
                        <span>挂载目标案卷：<strong className="text-slate-800 font-mono">{currentCaseId || '未指定'}</strong></span>
                      </div>

                      <div className="flex items-center gap-2">
                        <button
                          type="button"
                          onClick={() => handleAttachArtifact(item, idx)}
                          disabled={attachingIdx === idx || attachedIdxs[idx]}
                          className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-semibold transition-all cursor-pointer ${
                            attachedIdxs[idx]
                              ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                              : 'bg-white hover:bg-slate-50 text-slate-700 border border-slate-200/90 shadow-2xs'
                          }`}
                        >
                          {attachingIdx === idx ? (
                            <>
                              <Loader2 className="w-3.5 h-3.5 animate-spin text-blue-600" />
                              <span>挂载中...</span>
                            </>
                          ) : attachedIdxs[idx] ? (
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

                        <button
                          type="button"
                          onClick={() => handleUpgradeToCase(item)}
                          className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-semibold text-blue-700 bg-blue-50 hover:bg-blue-100/90 border border-blue-200/80 transition-all cursor-pointer shadow-2xs active:scale-[0.98]"
                        >
                          <FolderPlus className="w-3.5 h-3.5 text-blue-600" />
                          <span>以此条款立项研判</span>
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 法源引证核验报告 */}
      {result && result.items && result.items.length > 0 && (
        <div className="apple-bento-card rounded-[28px] overflow-hidden space-y-4 shadow-2xs">
          <div className="p-5 border-b border-slate-100 bg-slate-50/80 flex flex-wrap items-center justify-between gap-4">
            <div>
              <h3 className="text-xs font-bold text-slate-900 uppercase tracking-wider flex items-center gap-2">
                <Layers className="w-4 h-4 text-blue-600" />
                <span>法源引证真实性核验结论</span>
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
                  <th className="px-5 py-3.5">判例全文</th>
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
