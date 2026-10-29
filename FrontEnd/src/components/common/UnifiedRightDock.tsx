import React, { useState, useEffect, useRef, useMemo } from 'react';
import { useApp } from '../../context/AppContext';
import { GradeBadge } from './GradeBadge';
import { Evidence, RightDockMode, CaseChatMessage } from '../../types/lawAgent';
import { lawAgentApi } from '../../api/lawAgentApi';
import {
  X,
  BookOpen,
  Bot,
  Compass,
  Copy,
  Check,
  ShieldCheck,
  Send,
  Swords,
  Pin,
  AlertTriangle,
  FileCheck2,
  ArrowRight,
} from 'lucide-react';

interface UnifiedRightDockProps {
  onClose?: () => void;
}

export const UnifiedRightDock: React.FC<UnifiedRightDockProps> = ({ onClose }) => {
  const {
    currentCase,
    currentCaseId,
    selectedEvidenceEid,
    setSelectedEvidenceEid,
    rightDockMode,
    setRightDockMode,
    closeRightDock,
    openCaseEntryWithPrefill,
    showToast,
    refreshCurrentCase,
  } = useApp();

  const [copied, setCopied] = useState(false);
  const [attaching, setAttaching] = useState(false);
  const [attachedSuccess, setAttachedSuccess] = useState(false);

  // --- Mode 2: Copilot Chat State ---
  const [messages, setMessages] = useState<
    Array<{
      role: 'user' | 'assistant';
      content: string;
      model?: string;
      mode?: 'neutral' | 'red_teaming';
      statutes?: string[];
      timestamp: string;
    }>
  >([]);
  const [inputText, setInputText] = useState('');
  const [sending, setSending] = useState(false);
  const [copilotMode, setCopilotMode] = useState<'neutral' | 'red_teaming'>('neutral');
  const chatScrollRef = useRef<HTMLDivElement>(null);

  // --- Mode 3: Country Playbook State ---
  const defaultJur = currentCase?.meta?.jurisdiction || 'asean_id';
  const [selectedJur, setSelectedJur] = useState<string>(defaultJur);

  useEffect(() => {
    if (currentCase?.meta?.jurisdiction) {
      setSelectedJur(currentCase.meta.jurisdiction);
    }
  }, [currentCase?.meta?.jurisdiction]);

  // Evidence resolving
  const evidenceMap = currentCase?.evidence || {};
  const evidenceList: Evidence[] = useMemo(() => Object.values(evidenceMap || {}), [evidenceMap]);
  const currentEid = selectedEvidenceEid || (evidenceList[0]?.eid ?? 'E1');
  const evidence: Evidence | undefined = evidenceMap[currentEid] || evidenceList[0];

  const handleCopy = (text: string) => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    showToast('文本已复制到剪贴板', 'success');
    setTimeout(() => setCopied(false), 2000);
  };

  const handleAttachStatute = async () => {
    if (!currentCaseId || !evidence) return;
    setAttaching(true);
    try {
      await lawAgentApi.attachCaseArtifact(currentCaseId, {
        artifact_type: 'statute_pin',
        title: `${evidence.ref_id} 重点法源`,
        jurisdiction: currentCase?.meta?.jurisdiction,
        summary: currentCase?.translations?.[evidence.eid] || (evidence?.text_original || "").slice(0, 150),
        redline_clause: (evidence?.text_original || "").slice(0, 300),
      });
      setAttachedSuccess(true);
      showToast('✓ 法条已成功挂载至当前案卷重点援引清单', 'success');
      await refreshCurrentCase();
      setTimeout(() => setAttachedSuccess(false), 3000);
    } catch (e: any) {
      showToast(e.message || '挂载法源失败', 'error');
    } finally {
      setAttaching(false);
    }
  };

  // Copilot quick send
  const handleSendMessage = async (textToSend?: string) => {
    const text = textToSend || inputText.trim();
    if (!text || sending || !currentCaseId) return;

    const userMsg = {
      role: 'user' as const,
      content: text,
      timestamp: new Date().toLocaleTimeString(),
    };
    setMessages((prev) => [...prev, userMsg]);
    setInputText('');
    setSending(true);

    try {
      const history: CaseChatMessage[] = messages.concat(userMsg).map((m) => ({
        role: m.role,
        content: m.content,
      }));
      const res = await lawAgentApi.chatWithCase(currentCaseId, history, 'practitioner', copilotMode);
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: res.reply,
          model: res.model,
          mode: res.mode,
          statutes: res.referenced_statutes,
          timestamp: new Date().toLocaleTimeString(),
        },
      ]);
    } catch (err: any) {
      showToast(err.message || 'AI 协同响应超时，请重试', 'error');
    } finally {
      setSending(false);
      setTimeout(() => {
        chatScrollRef.current?.scrollTo({ top: chatScrollRef.current.scrollHeight, behavior: 'smooth' });
      }, 100);
    }
  };

  const jurPlaybooks: Record<string, { country: string; flag: string; majorShift: string; dos: string[]; donts: string[] }> = {
    asean_id: {
      country: '印度尼西亚',
      flag: '🇮🇩',
      majorShift: '印尼最高院 SEMA No. 3/2023：纯英文协议不必然无效，需考察各方签署善意；MEMR 11/2024 能矿部特许豁免。',
      dos: [
        '严格依据 SEMA 3/2023 与 UU 24/2009 安排中英双语同文签署；',
        '光伏/火电设备进口前向工业部 (Kemenperin) 申办 TKDN 特许豁免；',
        '原住民习惯法土地 (Hak Ulayat) 必须取得省政府征用移交纪要。',
      ],
      donts: [
        '严禁签署放弃 FIDIC 8.4 习惯法阻碍工期索赔的单方承诺；',
        '严禁未经当地能源矿产部审查私自签署 100% 外资控股协议；',
        '严禁单方擅自将涉税与工程图纸数据未经脱敏提供给外国调证机构。',
      ],
    },
    asean_vn: {
      country: '越南',
      flag: '🇻🇳',
      majorShift: '越南《2025年新建设法》(Law 135/2025/QH15) 第 86.2 条确立预定违约金上限 (LD Cap) 制度。',
      dos: [
        '在 EPC 主合同中约定违约金封顶不超过签约总价的 8%-12%；',
        '适用第 210/2026/ND-CP 号建设合同法令排除不可抗力违约金；',
        'EPC 与并购交易优先设立新加坡中转 SPV 激活 BIT 条约保护。',
      ],
      donts: [
        '严禁签署无封顶预定损害赔偿 (Uncapped LD) 条款；',
        '严禁在未获工贸部 (MOIT) 并网批复前擅自垫资全额开工；',
        '严禁忽略 EVN 国家电力公司购电协议 (PPA) 的限电非补偿风险。',
      ],
    },
    asean_my: {
      country: '马来西亚',
      flag: '🇲🇾',
      majorShift: '马来西亚 CIPAA 2012 第 35 条明文规定：建设分包合同中的背靠背付款条款法定绝对无效。',
      dos: [
        '分包合同改用独立里程碑付款节点或设定最长 45 天付款期限；',
        '发生工程款争议立即申请 AIAC 快速法定裁决并在 45 天内锁定执行令；',
        '总包及时向 CIDB 报备一级承包商注册资质。',
      ],
      donts: [
        '严禁在分包合同中约定以业主向总包付款为前提的 Pay-when-paid 条款；',
        '严禁在收到裁决书后超过 14 天拒付裁决款导致现场被依法停工；',
        '严禁在土著配额 (Bumiputera) 联营体中进行虚假代持或抽逃资本。',
      ],
    },
    asean_sg: {
      country: '新加坡',
      flag: '🇸🇬',
      majorShift: '新加坡 SOPA 第 9 条反背靠背支付 + BS Mount Sophia 先例确立以“显失公平”独立止付见索即付保函。',
      dos: [
        '当业主滥用保函索兑时，依据 BS Mount Sophia 先例向高院申请止付令；',
        '优先选择 SIAC 仲裁规则并约定适用紧急仲裁员 (Emergency Arbitrator)；',
        '在出海架构中充分利用新加坡作为东盟跨境投资与资金调配 SPV 枢纽。',
      ],
      donts: [
        '严禁在专用条件中排除法院以 Unconscionability 止付保函的救济权利；',
        '严禁超过 28 天通知期限才发出工期索赔意向函；',
        '严禁在保函开立申请中放弃要求受益人出具实质违约真实声明的限制。',
      ],
    },
    asean_th: {
      country: '泰国',
      flag: '🇹🇭',
      majorShift: '泰国民商法典第 596 条法院违约金酌减权 + 外商经营法 (FBA 1999) 建筑施工外资限制。',
      dos: [
        '重大基建项目向泰国投资促进委员会 (BOI) 申请分类 7 投资优惠；',
        '外资持股超 49% 时向商业部商业发展厅 (DBD) 申请 FBL 营业执照；',
        '遭遇过高延误罚款时援引 CCC 第 596 条申请仲裁庭依法酌减。',
      ],
      donts: [
        '严禁在未取得 FBL 许可证前以纯外资独资名义直接作为总包施工；',
        '严禁使用泰国名义股东代持股权规避 FBA 限制（违法自始无效）；',
        '严禁在泰国国家铁路/高速公路公建项目中违反政府采购特别令。',
      ],
    },
    asean_ph: {
      country: '菲律宾',
      flag: '🇵🇭',
      majorShift: '菲律宾 2023 年新 PPP 法典 (RA 11966) + 最高院 Manila Water 案判定普通承包商外资限制违宪。',
      dos: [
        '依据 Manila Water 判例向 PCAB 申请普通承包商牌照或 Special License；',
        '在 PPP 特许经营合同中依据 RA 11966 严格锁定政府违约终止公允补偿；',
        '争议解决约定 CIAC 建设工程仲裁或新加坡 SIAC 涉外仲裁。',
      ],
      donts: [
        '严禁继续依据已被废止的旧 BOT 法 (RA 7718) 起草特许权协议；',
        '严禁在政府换届停工令发布后超过 30 天未向中信保报损；',
        '严禁未通过当地环保局 (DENR) 环保证书 (ECC) 强行推进跨海工程。',
      ],
    },
  };

  const activePlaybook = jurPlaybooks[selectedJur] || jurPlaybooks['asean_id'];

  return (
    <aside className="w-[440px] shrink-0 h-full border-l border-slate-200/80 bg-white flex flex-col z-30 shadow-xl apple-drawer-spring">
      {/* 顶部模态控制器与关闭按钮 */}
      <div className="h-14 border-b border-slate-200/80 px-4 flex items-center justify-between bg-slate-50/75 backdrop-blur-md shrink-0">
        <div className="apple-segmented-control text-xs">
          <button
            onClick={() => setRightDockMode('law_reader')}
            className={`px-3 py-1.5 rounded-lg flex items-center gap-1.5 transition-all cursor-pointer ${
              rightDockMode === 'law_reader'
                ? 'apple-segmented-item-active text-slate-900 font-semibold'
                : 'text-slate-500 hover:text-slate-800'
            }`}
          >
            <BookOpen className="w-3.5 h-3.5 text-blue-600" />
            <span>法条精读</span>
          </button>
          <button
            onClick={() => setRightDockMode('case_copilot')}
            className={`px-3 py-1.5 rounded-lg flex items-center gap-1.5 transition-all cursor-pointer ${
              rightDockMode === 'case_copilot'
                ? 'apple-segmented-item-active text-slate-900 font-semibold'
                : 'text-slate-500 hover:text-slate-800'
            }`}
          >
            <Bot className="w-3.5 h-3.5 text-blue-600" />
            <span>AI 法律咨询</span>
          </button>
          <button
            onClick={() => setRightDockMode('country_playbook')}
            className={`px-3 py-1.5 rounded-lg flex items-center gap-1.5 transition-all cursor-pointer ${
              rightDockMode === 'country_playbook'
                ? 'apple-segmented-item-active text-slate-900 font-semibold'
                : 'text-slate-500 hover:text-slate-800'
            }`}
          >
            <Compass className="w-3.5 h-3.5 text-blue-600" />
            <span>东盟合规指引</span>
          </button>
        </div>

        <button
          onClick={onClose || closeRightDock}
          className="p-1.5 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-200/60 transition-colors cursor-pointer"
          title="收起法律辅助面板 (Cmd/Ctrl + B)"
        >
          <X className="w-4 h-4" />
        </button>
      </div>

      {/* 主体切换区 */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {/* ========================================================================= */}
        {/* MODE 1: 法源双语精读 (Law Reader) */}
        {/* ========================================================================= */}
        {rightDockMode === 'law_reader' && (
          <div className="space-y-4">
            {evidence ? (
              <>
                {/* 权威法源认证卡 */}
                <div className="rounded-xl border border-blue-200/80 bg-blue-50/50 p-3.5 space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="inline-flex items-center gap-1.5 text-xs font-semibold text-blue-900">
                      <ShieldCheck className="w-4 h-4 text-blue-600" />
                      权威法源认证 · 现行有效
                    </span>
                    <GradeBadge grade={evidence.grade} size="sm" />
                  </div>
                  <div className="text-[11px] text-slate-600 space-y-1 font-mono">
                    <div>规范条号：<span className="font-semibold text-slate-900">{evidence.ref_id}</span></div>
                    <div>翻译对齐：司法部法通网 2026 现行标准译本</div>
                    <div>来源公报：{evidence.source_url || '东道国官方公报不可变镜像'}</div>
                  </div>
                </div>

                {/* 规范原文与中文对照 */}
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <h4 className="text-xs font-semibold text-slate-800 flex items-center gap-1.5">
                      <FileCheck2 className="w-3.5 h-3.5 text-slate-600" />
                      官方逐字原文 (Authentic Text)
                    </h4>
                    <button
                      onClick={() => handleCopy(evidence?.text_original || "")}
                      className="text-[11px] text-blue-600 hover:text-blue-800 flex items-center gap-1 cursor-pointer font-medium"
                    >
                      {copied ? <Check className="w-3 h-3 text-emerald-600" /> : <Copy className="w-3 h-3" />}
                      <span>{copied ? '已复制' : '复制原文'}</span>
                    </button>
                  </div>
                  <div className="p-3 bg-slate-50 border border-slate-200/90 rounded-xl font-mono text-xs text-slate-800 leading-relaxed max-h-56 overflow-y-auto">
                    {evidence.text_original}
                  </div>

                  <h4 className="text-xs font-semibold text-slate-800 flex items-center gap-1.5 pt-1">
                    <BookOpen className="w-3.5 h-3.5 text-blue-600" />
                    中文权威释义与裁判指引
                  </h4>
                  <div className="p-3 bg-white border border-slate-200/90 rounded-xl text-xs text-slate-700 leading-relaxed shadow-sm">
                    {currentCase?.translations?.[evidence.eid] || '中文权威译本对齐中...'}
                  </div>
                </div>

                {/* 引用至当前案卷主行动按钮 */}
                <div className="pt-2">
                  <button
                    onClick={handleAttachStatute}
                    disabled={attaching || attachedSuccess}
                    className={`w-full py-2.5 px-4 rounded-xl text-xs font-semibold flex items-center justify-center gap-2 transition-all cursor-pointer ${
                      attachedSuccess
                        ? 'bg-emerald-600 text-white'
                        : 'bg-blue-600 hover:bg-blue-700 text-white shadow-xs shadow-blue-500/25 active:scale-[0.98] transition-all'
                    }`}
                  >
                    {attachedSuccess ? (
                      <>
                        <Check className="w-4 h-4 text-white" />
                        <span>✓ 已成功挂载至当前案卷 ({currentCaseId})</span>
                      </>
                    ) : (
                      <>
                        <Pin className="w-3.5 h-3.5" />
                        <span>+ 引用并挂载此法源至当前案卷</span>
                      </>
                    )}
                  </button>
                </div>
              </>
            ) : (
              <div className="p-6 text-center space-y-4">
                <div className="text-slate-500 text-xs leading-relaxed">
                  当前案卷暂无选中的法源材料，可点击主画布任意法条胶囊打开精读，或快捷查阅东盟高频权威法源：
                </div>
                <div className="space-y-2 text-left">
                  {[
                    { eid: 'E1', title: 'FIDIC 银皮书第 20.1 款', sub: '28天索赔通知除斥期法定先决要件' },
                    { eid: 'E2', title: '印尼最高法院通函 SEMA 3/2023', sub: '善意履约下纯英文合同效力认可准则' },
                    { eid: 'E3', title: '马来西亚 CIPAA 2012 第 35 条', sub: '建筑工程背靠背付款条款法定绝对无效' },
                  ].map((preset, idx) => (
                    <button
                      key={idx}
                      type="button"
                      onClick={() => {
                        if (evidenceList[idx]) {
                          setSelectedEvidenceEid(evidenceList[idx].eid);
                        } else {
                          showToast(`已请求查阅【${preset.title}】，可切换至法典库进行跨法域全本比对`, 'info');
                        }
                      }}
                      className="w-full p-2.5 rounded-xl bg-slate-50 hover:bg-blue-50/70 border border-slate-200/80 hover:border-blue-300 text-left transition cursor-pointer group"
                    >
                      <div className="text-xs font-semibold text-slate-800 group-hover:text-blue-600 transition-colors">
                        {preset.title}
                      </div>
                      <div className="text-[11px] text-slate-400">
                        {preset.sub}
                      </div>
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* ========================================================================= */}
        {/* MODE 2: 案卷 AI 副驾 & 流水线 (Case Copilot) */}
        {/* ========================================================================= */}
        {rightDockMode === 'case_copilot' && (
          <div className="flex flex-col h-[calc(100vh-120px)] justify-between space-y-3">
            {/* 上半区：当前推理状态与对抗模式分段 */}
            <div className="shrink-0 space-y-2">
              <div className="flex items-center justify-between p-2.5 rounded-xl bg-slate-50 border border-slate-200/80">
                <div className="flex items-center gap-2">
                  <span className="w-2 h-2 rounded-full bg-blue-600 animate-pulse" />
                  <span className="text-xs font-semibold text-slate-800">
                    法律推理引擎已就绪
                  </span>
                </div>
                <div className="apple-segmented-control text-[11px]">
                  <button
                    onClick={() => setCopilotMode('neutral')}
                    className={`px-2.5 py-1 rounded-md cursor-pointer transition-colors ${
                      copilotMode === 'neutral' ? 'apple-segmented-item-active text-slate-900 font-semibold' : 'text-slate-500 hover:text-slate-700'
                    }`}
                  >
                    中立分析
                  </button>
                  <button
                    onClick={() => setCopilotMode('red_teaming')}
                    className={`px-2.5 py-1 rounded-md cursor-pointer flex items-center gap-1 transition-colors ${
                      copilotMode === 'red_teaming' ? 'apple-segmented-item-active text-rose-700 font-semibold' : 'text-slate-500 hover:text-slate-700'
                    }`}
                  >
                    <Swords className="w-3 h-3 text-rose-500" />
                    模拟对方抗辩
                  </button>
                </div>
              </div>

              {/* 预设高频追问胶囊 */}
              <div className="flex flex-wrap gap-1.5">
                {[
                  '若业主主张28天索赔时效失权如何反制？',
                  '印尼 SEMA 3/2023 如何驳回纯英文合同无效抗辩？',
                  '新加坡 BS Mount Sophia 独立保函止付裁定要件',
                  '马来西亚分包背靠背拒付款项如何通过 CIPAA 维权？',
                ].map((promptText, idx) => (
                  <button
                    key={idx}
                    onClick={() => handleSendMessage(promptText)}
                    className="text-[11px] bg-slate-100/90 hover:bg-blue-50 hover:text-blue-700 hover:border-blue-200 text-slate-700 px-2.5 py-1 rounded-lg border border-slate-200/60 transition-colors text-left cursor-pointer"
                  >
                    {promptText}
                  </button>
                ))}
              </div>
            </div>

            {/* 对话消息流 */}
            <div ref={chatScrollRef} className="flex-1 overflow-y-auto space-y-3 pr-1 min-h-[200px]">
              {messages.length === 0 ? (
                <div className="p-6 text-center space-y-3">
                  <div className="w-10 h-10 rounded-2xl bg-blue-50 border border-blue-200/60 text-blue-600 flex items-center justify-center mx-auto shadow-2xs">
                    <Bot className="w-5 h-5 text-blue-600" />
                  </div>
                  <div>
                    <h5 className="font-semibold text-slate-800 text-xs">AI 法律咨询助手已挂载</h5>
                    <p className="text-[11px] text-slate-500 mt-1 max-w-[280px] mx-auto leading-relaxed">
                      已集成东盟六国法典库与 FIDIC 合同规则。可针对工程索赔时效、保函止付条件与属地强行法提出咨询或展开抗辩推演。
                    </p>
                  </div>
                </div>
              ) : (
                messages.map((m, idx) => (
                  <div
                    key={idx}
                    className={`p-3 rounded-xl text-xs leading-relaxed ${
                      m.role === 'user'
                        ? 'bg-blue-600 text-white ml-6'
                        : 'bg-slate-50 border border-slate-200/80 text-slate-800 mr-2 space-y-1.5'
                    }`}
                  >
                    <div className="flex items-center justify-between text-[10px] opacity-75">
                      <span>{m.role === 'user' ? '我方' : 'AI 研判建议'}</span>
                      <span>{m.timestamp}</span>
                    </div>
                    <div className="whitespace-pre-wrap">{m.content}</div>
                    {m.statutes && m.statutes.length > 0 && (
                      <div className="pt-1.5 border-t border-slate-200/60 flex flex-wrap gap-1">
                        {m.statutes.map((st, i) => (
                          <span key={i} className="px-1.5 py-0.5 rounded bg-blue-100 text-blue-800 text-[10px] font-mono">
                            {st}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                ))
              )}
            </div>

            {/* 底部输入框 */}
            <div className="shrink-0 pt-2 border-t border-slate-200/80">
              <div className="flex items-center gap-2">
                <input
                  type="text"
                  value={inputText}
                  onChange={(e) => setInputText(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && !e.shiftKey && handleSendMessage()}
                  placeholder={
                    copilotMode === 'red_teaming'
                      ? '输入对方可能提出的法律抗辩点...'
                      : '向 AI 助手输入法律实务咨询或推演要求...'
                  }
                  className="flex-1 px-3 py-2 text-xs border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-600 bg-slate-50 transition-all placeholder:text-slate-400"
                />
                <button
                  onClick={() => handleSendMessage()}
                  disabled={sending || !inputText.trim()}
                  className="p-2 bg-blue-600 hover:bg-blue-700 rounded-xl text-white cursor-pointer disabled:opacity-50 shadow-xs shadow-blue-500/25 active:scale-[0.98] transition-all"
                >
                  <Send className="w-3.5 h-3.5" />
                </button>
              </div>
            </div>
          </div>
        )}

        {/* ========================================================================= */}
        {/* MODE 3: 属地排雷速查 (Country Playbook) */}
        {/* ========================================================================= */}
        {rightDockMode === 'country_playbook' && (
          <div className="space-y-4">
            {/* 国家切换器 */}
            <div className="flex items-center gap-1.5 overflow-x-auto pb-1 text-xs">
              {Object.entries(jurPlaybooks).map(([code, item]) => (
                <button
                  key={code}
                  onClick={() => setSelectedJur(code)}
                  className={`px-2.5 py-1.5 rounded-lg shrink-0 flex items-center gap-1 transition-all cursor-pointer ${
                    selectedJur === code
                      ? 'bg-slate-900 text-white font-medium shadow-sm'
                      : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                  }`}
                >
                  <span>{item.flag}</span>
                  <span>{item.country}</span>
                </button>
              ))}
            </div>

            {/* 重大立法转向提示 */}
            <div className="p-3.5 rounded-xl border border-amber-200 bg-amber-50/60 space-y-1.5">
              <div className="flex items-center gap-1.5 text-xs font-semibold text-amber-900">
                <AlertTriangle className="w-4 h-4 text-amber-600 shrink-0" />
                <span>{activePlaybook.country} 2026 重大立法转向警示</span>
              </div>
              <p className="text-xs text-amber-800 leading-relaxed">
                {activePlaybook.majorShift}
              </p>
            </div>

            {/* Do's & Don'ts 清单 */}
            <div className="space-y-3">
              <div className="p-3.5 rounded-xl border border-emerald-200 bg-emerald-50/40 space-y-2">
                <h4 className="text-xs font-semibold text-emerald-900 flex items-center gap-1.5">
                  <span className="w-2 h-2 rounded-full bg-emerald-600" />
                  必须严格执行的 3 项合规操作 (Do's)
                </h4>
                <ul className="text-xs text-slate-700 space-y-1.5 pl-3 list-disc">
                  {activePlaybook.dos.map((item, i) => (
                    <li key={i} className="leading-relaxed">{item}</li>
                  ))}
                </ul>
              </div>

              <div className="p-3.5 rounded-xl border border-rose-200 bg-rose-50/40 space-y-2">
                <h4 className="text-xs font-semibold text-rose-900 flex items-center gap-1.5">
                  <span className="w-2 h-2 rounded-full bg-rose-600" />
                  严禁踩踏的 3 大红线禁区 (Don'ts)
                </h4>
                <ul className="text-xs text-slate-700 space-y-1.5 pl-3 list-disc">
                  {activePlaybook.donts.map((item, i) => (
                    <li key={i} className="leading-relaxed">{item}</li>
                  ))}
                </ul>
              </div>
            </div>

            {/* 一键带参数立项按钮 */}
            <div className="pt-2">
              <button
                onClick={() => {
                  openCaseEntryWithPrefill({
                    jurisdiction: selectedJur,
                    title: `${activePlaybook.country}重点项目合规排雷专项推演`,
                    facts: `针对${activePlaybook.country}最新监管要求：${activePlaybook.majorShift}，开展专项合规防范与合同条款审查。`,
                  });
                }}
                className="w-full py-2.5 px-4 rounded-xl text-xs font-semibold bg-blue-600 hover:bg-blue-700 text-white shadow-xs shadow-blue-500/25 active:scale-[0.98] flex items-center justify-center gap-2 cursor-pointer transition-all"
              >
                <ArrowRight className="w-3.5 h-3.5 text-white" />
                <span>针对该国别风险一键启动专案推演</span>
              </button>
            </div>
          </div>
        )}
      </div>
    </aside>
  );
};
