import React, { useState, useEffect, useRef, useMemo } from 'react';
import { useApp } from '../../context/AppContext';
import { lawAgentApi } from '../../api/lawAgentApi';
import { SavedInsight } from '../../types/lawAgent';
import {
  Bot,
  Send,
  RotateCcw,
  Copy,
  Check,
  BookOpen,
  BookmarkPlus,
  FolderArchive,
  X,
  SlidersHorizontal,
  ChevronRight,
  ShieldCheck,
  Swords,
} from 'lucide-react';

export const AgentWorkspaceView: React.FC = () => {
  const {
    currentCaseId,
    currentCase,
    role,
    openLawModal,
    showToast,
    refreshCurrentCase,
  } = useApp();

  const case_id = currentCaseId || 'C001';

  // 对抗模式切换 (neutral | red_teaming)
  const [chatMode, setChatMode] = useState<'neutral' | 'red_teaming'>('neutral');

  // 研判洞察成果沉淀至底稿
  const [savedInsights, setSavedInsights] = useState<SavedInsight[]>([]);
  const [savingInsightIndex, setSavingInsightIndex] = useState<number | null>(null);
  const [savedInsightIndices, setSavedInsightIndices] = useState<Set<number>>(new Set());

  // 案件背景与争议要素抽屉 (默认折叠以保持聊天界面纯净专注)
  const [isContextDrawerOpen, setIsContextDrawerOpen] = useState<boolean>(false);

  // 对话列表
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
  const [copiedIndex, setCopiedIndex] = useState<number | null>(null);

  // 修复：消息滚动容器引用与初次挂载标记（彻底杜绝切换页面时默认滑到底部）
  const chatScrollContainerRef = useRef<HTMLDivElement>(null);
  const isInitialMount = useRef<boolean>(true);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  // 从当前案件动态提取争议焦点与抗辩要点
  const caseContext = useMemo(() => {
    const issuesList = currentCase?.issues || [];
    const choiceOfLaw = currentCase?.meta?.choice_of_law || '东盟属地现行实体法与 FIDIC 银皮书标准条件';

    return {
      choiceOfLaw,
      issues: issuesList,
      claimBasis:
        currentCase?.claims?.[0]?.text_zh ||
        'FIDIC Clause 8.4 工期顺延 (EOT) 与不可预见现场风险公允补偿请求权',
      defenseCore:
        currentCase?.strategic_assessment?.red_team_defenses?.[0]?.opposing_claim ||
        'FIDIC Clause 20.1 28天索赔失权抗辩 & 属地语言法合同自始无效抗辩',
      breakthroughPath:
        currentCase?.strategic_assessment?.outcome_branches?.[0]?.condition_precedent ||
        '援引印尼最高院 SEMA 3/2023 善意履约推定与实际知悉原则 (Actual Knowledge) 突破失权',
    };
  }, [currentCase]);

  // 快捷 Prompt 预设胶囊（精炼规范，去除多余 emoji，聚焦东盟工程与央企合规）
  const quickPromptsNeutral = useMemo(
    () => [
      {
        title: 'FIDIC 20.1 索赔突破',
        prompt: '外方业主主张我方逾期发出索赔通知依据第20.1款失权，我方如何援引实际知悉（Actual Knowledge）与诚信履约抗辩？',
      },
      {
        title: 'SEMA 3/2023 语言抗辩',
        prompt: '业主以涉案合同未依印尼语言法同时订立印尼语本为由主张自始无效，我方如何依据印尼最高院《2023年第3号通告》实施反制？',
      },
      {
        title: 'BS Mount Sophia 保函止付',
        prompt: '业主在实体违约责任未定前突袭向银行索兑10%履约保函，我方如何依据显失公平（Unconscionability）准则申请紧急仲裁员止付令？',
      },
      {
        title: 'CIPAA 35 背靠背无效',
        prompt: '马来西亚工程款追索中，总承包商能否援引业主未付款为由拒绝结算？CIPAA 2012 第35条强行法如何适用？',
      },
      {
        title: '国资委35号令与信保保全',
        prompt: '东道国发生政局变动导致特许权协议被撤销，依据国资委35号令与中信保30日报损要求，合规法务应立即采取哪些保全行动？',
      },
    ],
    []
  );

  const quickPromptsRedTeam = useMemo(
    () => [
      {
        title: 'FIDIC 20.1 严格除斥时效',
        prompt: '作为东道国业主大律师，如何援引 FIDIC 第20.1款的28天通知强行除斥期间，主张承包商索赔权利已彻底消灭？',
      },
      {
        title: '属地语言法自始无效发难',
        prompt: '业主大律师如何依据印尼 2009 年第 24 号《语言法》第 31 条，主张纯外文工程合同违反公共秩序并请求法院宣告无效？',
      },
      {
        title: 'TKDN 本地化率违约惩罚',
        prompt: '东道国工业部认定涉案光伏逆变器设备未达法定本地化率 (TKDN)，业主如何主张实质违约并从工程款中直接扣罚违约金？',
      },
      {
        title: 'BUJKA 属地施工资质瑕疵',
        prompt: '业主如何以中资承包商未依法组建合规 KSO 联营体或 BUJKA 执照展期瑕疵为由，主张分包合同无效并拒绝支付工程进度款？',
      },
      {
        title: '见索即付保函无条件划款',
        prompt: '业主大律师如何向开证行证明保函具有独立抽象性，阻断承包商以合同争议为由申请的任何禁令，促成银行无条件兑付？',
      },
    ],
    []
  );

  const quickPrompts = chatMode === 'red_teaming' ? quickPromptsRedTeam : quickPromptsNeutral;

  // 加载已沉淀的研判备忘
  const loadInsights = async () => {
    try {
      const list = await lawAgentApi.getCaseInsights(case_id);
      setSavedInsights(list || []);
    } catch {
      setSavedInsights(currentCase?.saved_insights || []);
    }
  };

  useEffect(() => {
    loadInsights();
  }, [case_id]);

  // 初始化问候语
  useEffect(() => {
    const defaultStatutes = [
      'FIDIC Silver 8.4/20.1',
      'SEMA 3/2023',
      'CIPAA 2012 Sec 35',
      'BS Mount Sophia',
      'RA 11966 PPP Code',
      'BIT Art.6',
    ];

    const greetingContent = `您好，我是本案【${case_id}】的东盟工程合规与法律风险防范 Agent。涉案争议焦点、FIDIC 条款、东道国现行强行法与司法裁判先例已就绪。您可以点击下方快捷问题开展工期索赔、保函止付、资质准入或国资监管合规演练，亦可切换【中立法理】与【外方业主反击】开展深度攻防推演。`;

    setMessages([
      {
        role: 'assistant',
        content: greetingContent,
        model: 'qwen3.8-flash',
        mode: 'neutral',
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        statutes: defaultStatutes,
      },
    ]);
  }, [case_id]);

  // 修复滑动到底部：仅在用户发送消息或收到新回复时滚动内部容器，首次挂载或切页时不滚动
  useEffect(() => {
    if (isInitialMount.current) {
      isInitialMount.current = false;
      return;
    }
    if (chatScrollContainerRef.current) {
      chatScrollContainerRef.current.scrollTo({
        top: chatScrollContainerRef.current.scrollHeight,
        behavior: 'smooth',
      });
    }
  }, [messages.length, sending]);

  const handleSend = async (contentToSend?: string) => {
    const text = (contentToSend || inputText).trim();
    if (!text || sending) return;

    const userMsg = {
      role: 'user' as const,
      content: text,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };

    const newMessages = [...messages, userMsg];
    setMessages(newMessages);
    setInputText('');
    setSending(true);

    try {
      const chatPayload = newMessages.map((m) => ({
        role: m.role,
        content: m.content,
      }));

      const res = await lawAgentApi.chatWithCase(case_id, chatPayload, role, chatMode);

      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: res.reply,
          model: res.model,
          mode: res.mode || chatMode,
          statutes: res.referenced_statutes,
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        },
      ]);
    } catch (err: any) {
      showToast(err.message || '咨询请求失败', 'error');
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: '抱歉，咨询处理出现异常，请检查后台服务连接状态后重试。',
          model: 'error',
          mode: chatMode,
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        },
      ]);
    } finally {
      setSending(false);
    }
  };

  // 研判成果沉淀至底稿（简化为唯一直观动作）
  const handleSaveInsight = async (
    index: number,
    content: string,
    category: 'memo' | 'trial_outline' | 'red_team_defense' = 'memo'
  ) => {
    if (savingInsightIndex !== null) return;
    setSavingInsightIndex(index);
    try {
      const lines = content.split('\n').map((l) => l.trim()).filter(Boolean);
      let title = '法律研判探索备忘';
      for (const line of lines) {
        const clean = line.replace(/^[#*\s-]+/, '').trim();
        if (clean && clean.length > 3) {
          title = clean.slice(0, 48);
          break;
        }
      }

      const res = await lawAgentApi.saveCaseInsight(case_id, {
        category,
        title,
        content,
        source_model: messages[index]?.model || 'qwen3.8-flash',
        referenced_statutes: messages[index]?.statutes || [],
      });

      setSavedInsights((prev) => [res, ...prev]);
      setSavedInsightIndices((prev) => new Set([...prev, index]));
      showToast('已成功沉淀至实务研判底稿', 'success');
      await refreshCurrentCase();
    } catch (err: any) {
      showToast(err.message || '沉淀失败', 'error');
    } finally {
      setSavingInsightIndex(null);
    }
  };

  const handleSelectIssueToPrompt = (issueText: string) => {
    const prompt =
      chatMode === 'red_teaming'
        ? `针对争议焦点：“${issueText}”，作为东道国业主大律师，你会如何组织进攻与质证，击溃中资承包商的索赔主张？`
        : `针对争议焦点：“${issueText}”，依据东盟属地法律及 FIDIC 银皮书国际工程标准条件，双方的举证责任分配与核心攻防要点是什么？`;
    setInputText(prompt);
    inputRef.current?.focus();
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleCopyMessage = (index: number, text: string) => {
    navigator.clipboard.writeText(text).then(() => {
      setCopiedIndex(index);
      showToast('已复制回复内容', 'success');
      setTimeout(() => setCopiedIndex(null), 2000);
    });
  };

  const handleClearHistory = () => {
    setMessages([
      {
        role: 'assistant',
        content: `会话记录已重置。您可以重新选择快捷问题，或切换【中立法理】与【外方业主反击】提出新的法律追问。`,
        model: 'qwen3.8-flash',
        mode: chatMode,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      },
    ]);
  };

  // 格式化文本中的 Markdown 标题与要点
  const renderFormattedContent = (content: string) => {
    const lines = content.split('\n');
    return (
      <div className="space-y-2 text-sm text-slate-800 leading-relaxed font-sans">
        {lines.map((line, i) => {
          if (line.startsWith('### ')) {
            return (
              <h4 key={i} className="text-sm font-bold text-slate-900 mt-3 mb-1">
                {line.replace('### ', '')}
              </h4>
            );
          }
          if (line.startsWith('## ')) {
            return (
              <h3 key={i} className="text-base font-bold text-slate-900 mt-3 mb-1">
                {line.replace('## ', '')}
              </h3>
            );
          }
          if (line.startsWith('**') && line.endsWith('**')) {
            return (
              <p key={i} className="font-semibold text-slate-900">
                {line.replace(/\*\*/g, '')}
              </p>
            );
          }
          if (line.startsWith('- ') || line.startsWith('* ')) {
            return (
              <div key={i} className="flex items-start gap-2 pl-2">
                <span className="w-1.5 h-1.5 rounded-full bg-slate-400 mt-2 shrink-0" />
                <span>{line.substring(2)}</span>
              </div>
            );
          }
          if (/^\d+\.\s/.test(line)) {
            return (
              <div key={i} className="flex items-start gap-2 pl-2">
                <span className="font-mono text-xs font-semibold text-slate-500 shrink-0 mt-0.5">
                  {line.match(/^\d+\./)?.[0]}
                </span>
                <span>{line.replace(/^\d+\.\s/, '')}</span>
              </div>
            );
          }
          if (line.trim() === '') {
            return <div key={i} className="h-1.5" />;
          }
          return <p key={i}>{line}</p>;
        })}
      </div>
    );
  };

  return (
    <div className="flex-1 flex h-full bg-[#F6F8FA] relative overflow-hidden min-w-0">
      {/* 核心主会话区域 (居中流式布局) */}
      <div className="flex-1 flex flex-col h-full min-w-0">
        {/* 顶部极简导航与控制栏：对齐 Apple Bento 视觉规范 */}
        <div className="h-14 border-b border-slate-200/80 bg-white/80 backdrop-blur-md px-4 sm:px-6 flex items-center justify-between gap-3 shrink-0 z-10">
          <div className="flex items-center gap-3 min-w-0">
            <div className="w-9 h-9 rounded-2xl bg-blue-50 border border-blue-200/60 text-blue-600 flex items-center justify-center shrink-0 shadow-2xs">
              <Bot className="w-4 h-4 text-blue-600" />
            </div>
            <div className="flex items-center gap-2 min-w-0">
              <h1 className="text-sm font-bold text-slate-900 tracking-tight truncate">
                查明Agent咨询
              </h1>
              <span className="font-mono text-xs font-semibold px-2 py-0.5 rounded-lg bg-slate-100 text-slate-700 border border-slate-200/70 shrink-0">
                {case_id}
              </span>
            </div>
          </div>

          {/* 右侧操作区：研判模式切换、要素抽屉与重置 */}
          <div className="flex items-center gap-2">
            {/* 中立研判 vs 对抗模式切换 */}
            <div className="flex items-center p-0.5 bg-slate-100/90 rounded-xl text-xs border border-slate-200/60">
              <button
                type="button"
                onClick={() => setChatMode('neutral')}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all duration-150 flex items-center gap-1.5 cursor-pointer ${
                  chatMode === 'neutral'
                    ? 'bg-white text-blue-600 shadow-2xs font-semibold'
                    : 'text-slate-600 hover:text-slate-900'
                }`}
                title="中立法理研判（法官/中立专家视角）"
              >
                <ShieldCheck className="w-3.5 h-3.5" />
                <span className="hidden sm:inline">中立法理</span>
              </button>
              <button
                type="button"
                onClick={() => setChatMode('red_teaming')}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all duration-150 flex items-center gap-1.5 cursor-pointer ${
                  chatMode === 'red_teaming'
                    ? 'bg-amber-500 text-white shadow-2xs font-semibold'
                    : 'text-slate-600 hover:text-slate-900'
                }`}
                title="东道国业主大律师出庭反击（模拟对抗质证）"
              >
                <Swords className="w-3.5 h-3.5" />
                <span>外方业主反击</span>
              </button>
            </div>

            {/* 案情要素抽屉开关 */}
            <button
              type="button"
              onClick={() => setIsContextDrawerOpen(!isContextDrawerOpen)}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl border text-xs font-medium transition-all duration-150 cursor-pointer ${
                isContextDrawerOpen
                  ? 'bg-blue-600 text-white border-blue-600 shadow-xs shadow-blue-500/20'
                  : 'bg-white hover:bg-slate-50 text-slate-700 border-slate-200/80 shadow-2xs'
              }`}
              title="查看案件要素与争议焦点"
            >
              <SlidersHorizontal className="w-3.5 h-3.5" />
              <span className="hidden sm:inline">案情要素</span>
              {caseContext.issues.length > 0 && (
                <span
                  className={`w-4 h-4 rounded-full text-[10px] font-mono flex items-center justify-center font-bold ${
                    isContextDrawerOpen ? 'bg-white/20 text-white' : 'bg-slate-100 text-slate-700'
                  }`}
                >
                  {caseContext.issues.length}
                </span>
              )}
            </button>

            {/* 清空会话历史 */}
            <button
              type="button"
              onClick={handleClearHistory}
              className="p-2 text-slate-400 hover:text-slate-700 hover:bg-slate-100 rounded-xl transition-colors cursor-pointer"
              title="重置会话"
            >
              <RotateCcw className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>

        {/* 消息对话滚动流 (居中流式排布) */}
        <div ref={chatScrollContainerRef} className="flex-1 overflow-y-auto px-4 sm:px-6 py-6 min-h-0">
          <div className="max-w-3xl mx-auto space-y-6">
            {messages.map((msg, index) => {
              const isUser = msg.role === 'user';
              return (
                <div
                  key={index}
                  className={`flex items-start gap-3.5 ${isUser ? 'flex-row-reverse' : ''}`}
                >
                  <div
                    className={`w-8 h-8 rounded-2xl flex items-center justify-center shrink-0 mt-0.5 shadow-xs ${
                      isUser
                        ? 'bg-blue-600 text-white shadow-blue-500/20 font-semibold text-xs'
                        : msg.mode === 'red_teaming'
                        ? 'bg-amber-500 text-white'
                        : 'bg-slate-100 border border-slate-200/80 text-blue-600'
                    }`}
                  >
                    {isUser ? (
                      '我'
                    ) : msg.mode === 'red_teaming' ? (
                      <Swords className="w-4 h-4" />
                    ) : (
                      <Bot className="w-4 h-4 text-blue-600" />
                    )}
                  </div>

                  <div className={`space-y-1.5 max-w-[85%] ${isUser ? 'items-end' : ''}`}>
                    <div
                      className={`flex items-center gap-2 text-[11px] text-slate-400 ${
                        isUser ? 'justify-end' : ''
                      }`}
                    >
                      <span className="font-medium text-slate-600">
                        {isUser
                          ? '提问'
                          : msg.mode === 'red_teaming'
                          ? '外方业主大律师反击'
                          : '查明Agent'}
                      </span>
                      <span>·</span>
                      <span className="font-mono">{msg.timestamp}</span>
                    </div>

                    <div
                      className={`p-4 sm:p-5 rounded-2xl text-sm leading-relaxed shadow-2xs ${
                        isUser
                          ? 'bg-blue-600 text-white rounded-tr-xs shadow-xs shadow-blue-500/20'
                          : msg.mode === 'red_teaming'
                          ? 'bg-white text-slate-800 border border-amber-200/90 rounded-tl-xs ring-1 ring-amber-100/60'
                          : 'bg-white text-slate-800 border border-slate-200/80 rounded-tl-xs'
                      }`}
                    >
                      {isUser ? (
                        <p className="whitespace-pre-wrap">{msg.content}</p>
                      ) : (
                        renderFormattedContent(msg.content)
                      )}
                    </div>

                    {!isUser && (
                      <div className="flex flex-wrap items-center justify-between gap-2 pt-1 text-xs">
                        <div className="flex flex-wrap items-center gap-1.5">
                          {msg.statutes && msg.statutes.length > 0 && (
                            <>
                              <span className="text-[11px] text-slate-400">援引法源:</span>
                              {msg.statutes.map((s, si) => (
                                <button
                                  key={si}
                                  type="button"
                                  onClick={() => openLawModal('E1')}
                                  className="px-2.5 py-0.5 rounded-lg text-xs font-mono bg-slate-100 hover:bg-blue-50 text-slate-700 hover:text-blue-700 border border-slate-200/70 transition-colors flex items-center gap-1.5 cursor-pointer"
                                  title="在弹窗中查看法条原文"
                                >
                                  <BookOpen className="w-3 h-3 text-slate-400" />
                                  <span>{s}</span>
                                </button>
                              ))}
                            </>
                          )}
                        </div>

                        {/* 复制与成果沉淀至底稿（精简为双动作） */}
                        <div className="flex items-center gap-1.5">
                          <button
                            type="button"
                            onClick={() =>
                              handleSaveInsight(
                                index,
                                msg.content,
                                msg.mode === 'red_teaming' ? 'red_team_defense' : 'memo'
                              )
                            }
                            disabled={savingInsightIndex === index}
                            className={`px-2.5 py-1 rounded-xl text-xs font-medium border transition-all flex items-center gap-1.5 cursor-pointer ${
                              savedInsightIndices.has(index)
                                ? 'bg-blue-600 text-white border-blue-600 shadow-xs'
                                : 'bg-white hover:bg-slate-50 text-slate-700 border-slate-200/80 shadow-2xs'
                            }`}
                            title="沉淀至实务研判底稿"
                          >
                            <BookmarkPlus className="w-3 h-3" />
                            <span>{savedInsightIndices.has(index) ? '已沉淀底稿' : '沉淀至底稿'}</span>
                          </button>

                          <button
                            type="button"
                            onClick={() => handleCopyMessage(index, msg.content)}
                            className="px-2.5 py-1 rounded-xl text-xs font-medium text-slate-600 hover:text-slate-900 bg-white hover:bg-slate-50 border border-slate-200/80 shadow-2xs flex items-center gap-1.5 transition-all cursor-pointer"
                            title="复制回复"
                          >
                            {copiedIndex === index ? (
                              <Check className="w-3 h-3 text-emerald-600" />
                            ) : (
                              <Copy className="w-3 h-3 text-slate-400" />
                            )}
                            <span>{copiedIndex === index ? '已复制' : '复制'}</span>
                          </button>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              );
            })}

            {/* 推理生成中状态 (呼吸微动效) */}
            {sending && (
              <div className="flex items-start gap-3.5 animate-in fade-in duration-300">
                <div
                  className={`w-8 h-8 rounded-2xl text-white flex items-center justify-center shrink-0 shadow-xs ${
                    chatMode === 'red_teaming' ? 'bg-amber-500' : 'bg-blue-600'
                  }`}
                >
                  <Bot className="w-4 h-4 text-white animate-pulse" />
                </div>
                <div className="p-4 sm:p-5 rounded-2xl rounded-tl-xs bg-white border border-slate-200/90 shadow-2xs space-y-2 max-w-[85%]">
                  <div className="flex items-center gap-2">
                    <span className="w-2 h-2 rounded-full bg-blue-600 animate-ping" />
                    <span className="text-xs font-semibold text-slate-800">
                      {chatMode === 'red_teaming'
                        ? '正在模拟对方律师质证抗辩要点...'
                        : '正在比对法源规范与先例涵摄...'}
                    </span>
                  </div>
                  <p className="text-xs text-slate-500 leading-relaxed">
                    {chatMode === 'red_teaming'
                      ? '正在分析索赔通知时点与除斥期间，比对 FIDIC 20.1 时效先例、属地语言强行法与本地化惩罚...'
                      : '正在检索东盟属地法规、FIDIC 标准条款及司法裁判先例，展开法律构成要件审查...'}
                  </p>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* 底部悬浮输入区域 (Apple Bento 风格输入舱) */}
        <div className="border-t border-slate-200/80 bg-white/90 backdrop-blur-md px-4 sm:px-6 py-3.5 shrink-0 z-10">
          <div className="max-w-3xl mx-auto space-y-2.5">
            {/* 快捷追问胶囊横向微条 */}
            <div className="flex items-center gap-1.5 overflow-x-auto no-scrollbar py-0.5">
              <span className="text-[11px] text-slate-400 font-medium shrink-0 flex items-center gap-1">
                快捷追问:
              </span>
              {quickPrompts.map((qp, i) => (
                <button
                  key={i}
                  type="button"
                  onClick={() => handleSend(qp.prompt)}
                  disabled={sending}
                  className="px-3 py-1.5 rounded-xl text-xs font-medium bg-white hover:bg-blue-50/50 hover:border-blue-300 hover:text-blue-600 text-slate-700 border border-slate-200/80 shadow-2xs active:scale-95 transition-all duration-150 whitespace-nowrap shrink-0 disabled:opacity-40 disabled:cursor-not-allowed cursor-pointer"
                >
                  {qp.title}
                </button>
              ))}
            </div>

            {/* 输入框主卡片 */}
            <div className="relative rounded-2xl border border-slate-200/90 bg-white shadow-2xs focus-within:border-blue-600/80 focus-within:ring-2 focus-within:ring-blue-500/10 transition-all p-2.5 pl-4">
              <textarea
                ref={inputRef}
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder={
                  chatMode === 'red_teaming'
                    ? `【外方业主大律师反击】向对方提出案情论辩或接受挑刺对抗审查（按 Enter 发送）...`
                    : `针对案件【${case_id}】追问（按 Enter 发送，Shift+Enter 换行）...`
                }
                rows={2}
                disabled={sending}
                className="w-full pr-14 text-xs sm:text-sm text-slate-900 placeholder:text-slate-400 resize-none outline-none focus:ring-0 disabled:bg-slate-50"
              />

              <div className="absolute right-2.5 bottom-2.5 flex items-center gap-1.5">
                <button
                  type="button"
                  onClick={() => handleSend()}
                  disabled={!inputText.trim() || sending}
                  className="w-8 h-8 rounded-xl text-white bg-blue-600 hover:bg-blue-700 active:scale-95 flex items-center justify-center transition-all shadow-xs shadow-blue-500/25 disabled:bg-slate-200 disabled:text-slate-400 disabled:cursor-not-allowed cursor-pointer"
                >
                  <Send className="w-3.5 h-3.5" />
                </button>
              </div>
            </div>

            <div className="flex items-center justify-between text-[11px] text-slate-400 px-1">
              <span>
                {chatMode === 'red_teaming' ? (
                  <span className="text-amber-600 font-medium">对抗演练模式 · 模拟出庭律师质证视角</span>
                ) : (
                  <span>四段论事实与要件涵摄推演模式</span>
                )}
              </span>
              <span>Enter 发送 · Shift+Enter 换行</span>
            </div>
          </div>
        </div>
      </div>

      {/* 右侧：案情要素与争议焦点抽屉 (折叠式 Bento 架构) */}
      {isContextDrawerOpen && (
        <div className="w-80 sm:w-96 border-l border-slate-200/80 bg-white shadow-lg flex flex-col h-full z-20 animate-in slide-in-from-right duration-200">
          <div className="p-4 border-b border-slate-200/80 flex items-center justify-between bg-slate-50/70">
            <div className="flex items-center gap-2">
              <SlidersHorizontal className="w-4 h-4 text-blue-600" />
              <h2 className="text-xs font-bold text-slate-900">案件要素与争议焦点</h2>
            </div>
            <button
              type="button"
              onClick={() => setIsContextDrawerOpen(false)}
              className="p-1 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-100 cursor-pointer"
            >
              <X className="w-4 h-4" />
            </button>
          </div>

          <div className="flex-1 overflow-y-auto p-4 space-y-4 text-xs">
            {/* 准据法与公约 */}
            <div className="p-3.5 rounded-2xl bg-slate-50/80 border border-slate-200/80 space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-slate-500 font-medium">选定准据法</span>
                <span className="font-semibold text-slate-800">{caseContext.choiceOfLaw}</span>
              </div>
              <div className="flex items-center justify-between pt-1.5 border-t border-slate-200/60">
                <span className="text-slate-500 font-medium">国际公约排除</span>
                <span className="font-mono text-emerald-700 font-medium">{caseContext.cisgStatus}</span>
              </div>
            </div>

            {/* 核心请求权与抗辩防线 */}
            <div className="space-y-2.5">
              <div className="p-3.5 rounded-2xl bg-slate-50/80 border border-slate-200/80 space-y-1">
                <span className="text-slate-500 font-medium block">原告实体请求权基础:</span>
                <p className="font-semibold text-slate-800 leading-relaxed">{caseContext.claimBasis}</p>
              </div>

              <div className="p-3.5 rounded-2xl bg-slate-50/80 border border-slate-200/80 space-y-1">
                <span className="text-slate-900 font-medium block flex items-center gap-1.5">
                  <span className="w-1.5 h-1.5 rounded-full bg-amber-500 shrink-0" />
                  <span className="border-b border-amber-500 pb-0.5">对方核心抗辩与失权点:</span>
                </span>
                <p className="font-semibold text-slate-800 leading-relaxed">{caseContext.defenseCore}</p>
              </div>
            </div>

            {/* 争议焦点列表 */}
            <div className="space-y-2 pt-2 border-t border-slate-100">
              <div className="flex items-center justify-between">
                <span className="font-semibold text-slate-900">争议焦点清单 ({caseContext.issues.length})</span>
                <span className="text-[10px] text-slate-400">点击直接追问</span>
              </div>

              <div className="space-y-2">
                {caseContext.issues.length === 0 ? (
                  <p className="text-slate-400 text-center py-4">本案暂无特定争议焦点</p>
                ) : (
                  caseContext.issues.map((iss, idx) => (
                    <div
                      key={iss.issue_id || idx}
                      onClick={() => handleSelectIssueToPrompt(iss.text_zh)}
                      className="p-3 rounded-xl bg-slate-50 hover:bg-blue-50/50 border border-slate-200/80 hover:border-blue-200/70 transition-all cursor-pointer group flex items-start justify-between gap-2"
                    >
                      <div className="space-y-1">
                        <span className="font-mono text-[10px] text-slate-400 block">焦点 #{idx + 1}</span>
                        <p className="text-xs text-slate-800 group-hover:text-blue-600 transition-colors leading-relaxed">
                          {iss.text_zh}
                        </p>
                      </div>
                      <ChevronRight className="w-4 h-4 text-slate-300 group-hover:text-blue-600 shrink-0 mt-1 transition-colors" />
                    </div>
                  ))
                )}
              </div>
            </div>

            {/* 已沉淀研判备忘底稿 */}
            {savedInsights.length > 0 && (
              <div className="space-y-2 pt-2 border-t border-slate-100">
                <div className="flex items-center gap-1.5 text-slate-900 font-semibold">
                  <FolderArchive className="w-3.5 h-3.5 text-blue-600" />
                  <span>已沉淀底稿 ({savedInsights.length})</span>
                </div>

                <div className="space-y-2">
                  {savedInsights.map((ins) => (
                    <div
                      key={ins.insight_id}
                      className="p-3 rounded-xl bg-slate-50 border border-slate-200/80 text-xs space-y-1"
                    >
                      <div className="flex items-center justify-between">
                        <span className="text-[10px] font-medium text-slate-500">
                          {ins.category === 'red_team_defense'
                            ? '出庭防守要点'
                            : ins.category === 'trial_outline'
                            ? '出庭质证提纲'
                            : '实务备忘'}
                        </span>
                        <span className="text-[9px] font-mono text-slate-400">{ins.insight_id}</span>
                      </div>
                      <p className="font-medium text-slate-800 line-clamp-2 leading-relaxed">{ins.title}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
