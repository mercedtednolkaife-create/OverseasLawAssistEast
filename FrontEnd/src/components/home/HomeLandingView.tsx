import React, { useState } from 'react';
import { useApp } from '../../context/AppContext';
import { lawAgentApi } from '../../api/lawAgentApi';
import { AseanVectorBackground } from './AseanVectorBackground';
import {
  Search,
  ArrowRight,
  FileCheck2,
  BookOpen,
  Sliders,
  FolderOpen,
  FolderPlus,
  Plus,
  Copy,
  Check,
  X,
  FileText,
  ChevronRight,
} from 'lucide-react';

interface QuickQAItem {
  query: string;
  verdict: string;
  lawBasis: {
    country: string;
    flag: string;
    normId: string;
    title: string;
    quote: string;
  };
  strategy: string;
  targetJurisdiction: string;
  suggestedStage: 'pre_investment' | 'execution_dispute';
}

const KNOWLEDGE_BASE_PRESETS: Record<string, QuickQAItem> = {
  'sema_3_2023': {
    query: '印尼最高法院 SEMA 3/2023 对纯英文合同效力影响与司法抗辩',
    verdict: '最高法院指导意见明确：除非能证明当事人存在恶意 (itikad tidak baik)，法院不得仅因涉外商事合同未签署印尼语译本宣告自始无效。',
    lawBasis: {
      country: '印度尼西亚',
      flag: '🇮🇩',
      normId: 'ID:SEMA_3_2023',
      title: '印尼最高法院 2023 年第 3 号通告 (SEMA No. 3/2023)',
      quote: '涉及外国当事人的商事协议未采用印尼语订立的，若无恶意证明，不得仅以此为由认定合同绝对无效。',
    },
    strategy: '历史存量纯英文合同获司法保护，恶意无效抗辩被有效阻断；但在新签约阶段仍须落实双语同文签署以满足行政合规。',
    targetJurisdiction: 'asean_id',
    suggestedStage: 'execution_dispute',
  },
  'cipaa_sec35': {
    query: '马来西亚 CIPAA 2012 第 35 条背靠背 (Pay-when-paid) 付款条款效力',
    verdict: '马来西亚法定绝对无效 (Void ab initio)。分包合同中任何以业主付款为前提的约定均不具有法律约束力。',
    lawBasis: {
      country: '马来西亚',
      flag: '🇲🇾',
      normId: 'MY:CIPAA_2012:Sec35',
      title: '马来西亚《建设工程付款与快速裁决法》(CIPAA 2012) 第 35 条',
      quote: '建设合同中任何规定一方有义务付款须以第三方付款为条件的条款，一律自始无效。',
    },
    strategy: '总承包商不得以业主拖欠工程款为由抗辩拒付；分包商可随时发起 45 天快速裁决并申请依法停工。示范条款应设立独立的工程量核验支付周期。',
    targetJurisdiction: 'asean_my',
    suggestedStage: 'execution_dispute',
  },
  'fidic_20_1': {
    query: 'FIDIC 20.1 款 28 天索赔通知失权前置条件与反制路径',
    verdict: '未在 28 天内发出索赔通知面临程序性失权 (Condition Precedent Bar)，但可通过业主阻碍原则与东道国强行法反制。',
    lawBasis: {
      country: '国际工程范本',
      flag: '🌐',
      normId: 'FIDIC_SILVER_1999:Clause_20.1',
      title: 'FIDIC 银皮书/黄皮书第 20.1 款 (承包商索赔程序)',
      quote: '承包商须在知悉延误事件后 28 天内发出索赔通知，否则免除业主一切责任，承包商丧失工期顺延与额外付款权利。',
    },
    strategy: '主张“业主阻碍原则 (Prevention Principle)”与不当得利；若业主或工程师已有实际知悉或会议纪要留痕，可抗辩 28 天要件已实质满足。',
    targetJurisdiction: 'asean_id',
    suggestedStage: 'execution_dispute',
  },
  'mount_sophia': {
    query: '新加坡 BS Mount Sophia 判例独立保函“显失公平 (Unconscionability)”止付救济',
    verdict: '新加坡司法确立：除欺诈例外之外，“显失公平 (Unconscionability)”构成止付见索即付保函的独立衡平法救济标准。',
    lawBasis: {
      country: '新加坡',
      flag: '🇸🇬',
      normId: 'SG:Precedent:BS_Mount_Sophia',
      title: '新加坡最高法院 BS Mount Sophia Pte Ltd v. Join-Aim Pte Ltd [2012] SGCA 28',
      quote: '独立履约保函受显失公平衡平法管辖。当发包人索兑缺乏善意依据或出于恶意施压时，法院有权裁定临时禁令止付。',
    },
    strategy: '合同专用条件若约定“放弃申请任何保函止付禁令”，在新加坡法下可主张显失公平救济依然不可约定排除，应立即申请法院禁令。',
    targetJurisdiction: 'asean_sg',
    suggestedStage: 'execution_dispute',
  },
  'ph_ra11966': {
    query: '菲律宾 PPP 法典 (RA 11966) 明文废止旧 BOT 法与换届终止公允补偿机制',
    verdict: '全面废止实施三十年的旧 BOT 法 (RA 7718)，建立统一特许经营法治体系及公允终止补偿规则。',
    lawBasis: {
      country: '菲律宾',
      flag: '🇵🇭',
      normId: 'PH:RA_11966:The_PPP_Code',
      title: '菲律宾共和国法案第 11966 号《公私合营法典》(The PPP Code 2023)',
      quote: '废止旧法。因政府原因提前终止特许权协议的，应当依照公允审计标准支付全部未清偿债务及历史权益投入的公允价值补偿。',
    },
    strategy: '新建特许经营合同严禁援引旧 BOT 法条款；合同中必须设立包含加权资金成本 (WACC) 的终止清算公式，防止换届政治风险导致资产沉没。',
    targetJurisdiction: 'asean_ph',
    suggestedStage: 'pre_investment',
  },
  'vn_2025_construction': {
    query: '越南《2025年新建设法》(Law 135/2025/QH15) 违约金封顶与预定赔偿 (LD) 机制',
    verdict: '第 86.2 条正式确立“预定损害赔偿 (Liquidated Damages)”制度，打破了旧法下仅承认违约部分 12% 惩罚金的刚性规则。',
    lawBasis: {
      country: '越南',
      flag: '🇻🇳',
      normId: 'VN:Law_135_2025:Art86',
      title: '越南第 135/2025/QH15 号《新建设法》第 86.2 条',
      quote: '建设合同双方可依法约定工期延误预定损害赔偿金；当约定金额超出实际合理损失的，一方有权请求仲裁庭或法院予以公平核减。',
    },
    strategy: '新签越南 EPC 合同应重新设计误期损害赔偿与封顶条款 (Cap 通常约定 10%~15%)，并在合同中设立情势变更与不可抗力免责梯度。',
    targetJurisdiction: 'asean_vn',
    suggestedStage: 'pre_investment',
  },
};

export const HomeLandingView: React.FC = () => {
  const {
    casesList,
    loadCase,
    setCurrentView,
    openCaseEntryModal,
    openCaseEntryWithPrefill,
    showToast,
  } = useApp();

  const [searchQuery, setSearchQuery] = useState('');
  const [activeQA, setActiveQA] = useState<QuickQAItem | null>(null);
  const [searching, setSearching] = useState(false);
  const [copied, setCopied] = useState(false);

  const sampleKeywords = [
    { label: '印尼外文合同效力 (SEMA 3/2023)', key: 'sema_3_2023' },
    { label: 'FIDIC 28天索赔时效抗辩', key: 'fidic_20_1' },
    { label: '马来西亚背靠背支付无效 (CIPAA 35)', key: 'cipaa_sec35' },
    { label: '新加坡保函显失公平止付', key: 'mount_sophia' },
  ];

  const handleSelectPreset = (key: string) => {
    const item = KNOWLEDGE_BASE_PRESETS[key];
    if (item) {
      setSearchQuery(item.query);
      setActiveQA(item);
    }
  };

  const handleSearchWithQuery = async (queryText: string) => {
    const q = queryText.trim();
    if (!q) return;

    setSearching(true);
    let matched: QuickQAItem | null = null;

    // 1. 优先调用后端真实 Hybrid Search 检索引擎 (SQLite + BM25 + Vector)
    try {
      const searchResults = await lawAgentApi.searchNormsAndCases(q);
      if (searchResults && searchResults.length > 0) {
        const topItem = searchResults[0];
        const countryName = topItem.id.startsWith('ID')
          ? '印度尼西亚'
          : topItem.id.startsWith('VN')
          ? '越南'
          : topItem.id.startsWith('MY')
          ? '马来西亚'
          : topItem.id.startsWith('SG')
          ? '新加坡'
          : topItem.id.startsWith('TH')
          ? '泰国'
          : topItem.id.startsWith('PH')
          ? '菲律宾'
          : '东盟区域法治底座';
        const flag = topItem.id.startsWith('ID')
          ? '🇮🇩'
          : topItem.id.startsWith('VN')
          ? '🇻🇳'
          : topItem.id.startsWith('MY')
          ? '🇲🇾'
          : topItem.id.startsWith('SG')
          ? '🇸🇬'
          : topItem.id.startsWith('TH')
          ? '🇹🇭'
          : topItem.id.startsWith('PH')
          ? '🇵🇭'
          : '🌐';
        const targetJur = topItem.id.startsWith('VN')
          ? 'asean_vn'
          : topItem.id.startsWith('MY')
          ? 'asean_my'
          : topItem.id.startsWith('SG')
          ? 'asean_sg'
          : topItem.id.startsWith('TH')
          ? 'asean_th'
          : topItem.id.startsWith('PH')
          ? 'asean_ph'
          : 'asean_id';

        matched = {
          query: q,
          verdict: topItem.text_zh_machine || `检出权威法条：${topItem.title || topItem.id}`,
          lawBasis: {
            country: countryName,
            flag: flag,
            normId: topItem.id,
            title: topItem.title || topItem.id,
            quote: (topItem.text_de || topItem.text_zh_machine || '').slice(0, 200),
          },
          strategy: '建议针对本条法律要件创建专案案卷，载入工程工期延误、索赔通知时效或属地准入指标开展研判。',
          targetJurisdiction: targetJur,
          suggestedStage: 'execution_dispute',
        };
      }
    } catch (err) {
      console.warn('Real search call failed or empty, checking fallback presets:', err);
    }

    // 2. 本地高频预设作为离线/无网络情况下的降级兜底
    if (!matched) {
      const queryLower = q.toLowerCase();
      if (queryLower.includes('sema') || queryLower.includes('印尼语') || queryLower.includes('英文') || queryLower.includes('印尼')) {
        matched = KNOWLEDGE_BASE_PRESETS['sema_3_2023'];
      } else if (queryLower.includes('cipaa') || queryLower.includes('背靠背') || queryLower.includes('马') || queryLower.includes('pay')) {
        matched = KNOWLEDGE_BASE_PRESETS['cipaa_sec35'];
      } else if (queryLower.includes('fidic') || queryLower.includes('20.1') || queryLower.includes('28') || queryLower.includes('索赔')) {
        matched = KNOWLEDGE_BASE_PRESETS['fidic_20_1'];
      } else if (queryLower.includes('sophia') || queryLower.includes('保函') || queryLower.includes('止付') || queryLower.includes('新')) {
        matched = KNOWLEDGE_BASE_PRESETS['mount_sophia'];
      } else if (queryLower.includes('ppp') || queryLower.includes('11966') || queryLower.includes('菲') || queryLower.includes('bot')) {
        matched = KNOWLEDGE_BASE_PRESETS['ph_ra11966'];
      } else if (queryLower.includes('越') || queryLower.includes('135') || queryLower.includes('违约金') || queryLower.includes('ld')) {
        matched = KNOWLEDGE_BASE_PRESETS['vn_2025_construction'];
      }
    }

    if (!matched) {
      showToast('未在东盟重点法域法典及先例库中检索到直接匹配法条，建议尝试精确条号或实务关键词', 'warning');
      setSearching(false);
      return;
    }

    setActiveQA(matched);
    setSearching(false);
  };

  const handleSearchSubmit = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    await handleSearchWithQuery(searchQuery);
  };

  const handleCopyText = (text: string) => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    showToast('研判要点与法条依据已复制到剪贴板', 'success');
    setTimeout(() => setCopied(false), 2000);
  };

  const handleUpgradeToCase = (qa: QuickQAItem) => {
    openCaseEntryWithPrefill({
      jurisdiction: qa.targetJurisdiction,
      lifecycle_stage: qa.suggestedStage,
      title: `${qa.lawBasis.country}出海工程【${qa.lawBasis.title}】研判案卷`,
      facts: `【案件事实与咨询背景】\n针对：${qa.query}\n\n【初步法理判定】\n${qa.verdict}\n\n【权威法律依据】\n${qa.lawBasis.normId} · ${qa.lawBasis.title}\n"${qa.lawBasis.quote}"`,
      claims: `依据 ${qa.lawBasis.title} 主张排除违约责任、阻断失权抗辩并寻求合规保护。`,
    });
  };

  return (
    <div className="relative min-h-full pb-8">
      {/* 整个主页全景山海日光矢量背景 (仿 aiclipmaxx 现代极简风格) */}
      <AseanVectorBackground />

      <div className="relative z-10 max-w-[1540px] mx-auto px-4 sm:px-6 py-4 sm:py-5 space-y-4 select-none">
        {/* ========================================================================= */}
        {/* 顶部 Hero 检索区域 (The Omni-Legal Bar) */}
        {/* ========================================================================= */}
        <section className="apple-bento-card rounded-[24px] p-5 sm:p-6 shadow-2xs space-y-3">
          <div className="max-w-4xl mx-auto text-center space-y-2.5">
            <h1 className="text-xl sm:text-2xl font-bold text-slate-900 tracking-tight">
              东盟基建工程与涉外投资法律智能工作台
            </h1>

            <p className="text-xs text-slate-500 max-w-xl mx-auto font-normal">
              涵盖东盟六国投资准入、涉外合同合规审查、现行法规检索与索赔争议研判
            </p>

            {/* 全局检索输入框：统一蓝色行动按钮 */}
            <form onSubmit={handleSearchSubmit} className="pt-0.5">
              <div className="relative max-w-2xl mx-auto">
                <Search className="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="输入东道国法律问题、法条号或索赔争议要点..."
                  className="w-full pl-10 pr-24 py-2.5 rounded-xl border border-slate-200/90 text-xs sm:text-sm text-slate-900 bg-white/95 shadow-2xs focus:outline-none focus:ring-2 focus:ring-blue-500/10 focus:border-blue-600 transition-all placeholder:text-slate-400"
                />
                <button
                  type="submit"
                  disabled={searching || !searchQuery.trim()}
                  className="absolute right-1.5 top-1/2 -translate-y-1/2 px-3.5 py-1.5 rounded-lg text-xs font-semibold text-white bg-blue-600 hover:bg-blue-700 transition-all shadow-xs shadow-blue-500/25 active:scale-[0.98] cursor-pointer disabled:opacity-50"
                >
                  {searching ? '研判中...' : '即时研判'}
                </button>
              </div>
            </form>

            {/* 典型高频法源热词 */}
            <div className="flex flex-wrap items-center justify-center gap-1.5 pt-0.5 text-xs">
              <span className="text-[11px] text-slate-400 font-medium">快捷检索：</span>
              {sampleKeywords.map((item) => (
                <button
                  key={item.key}
                  type="button"
                  onClick={() => handleSelectPreset(item.key)}
                  className="text-[11px] px-2.5 py-0.5 rounded-lg bg-white/75 hover:bg-white text-slate-700 transition-colors cursor-pointer border border-slate-200/60 font-medium active:scale-[0.98]"
                >
                  {item.label}
                </button>
              ))}
            </div>
          </div>
        </section>

        {/* 智能研判结果原地展开卡片 */}
        {activeQA && (
          <section className="apple-bento-card rounded-[24px] p-4 sm:p-5 space-y-3.5 shadow-sm border border-blue-200/80 animate-in fade-in slide-in-from-top-2 duration-200">
            <div className="flex items-center justify-between border-b border-slate-100 pb-2.5">
              <div className="flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-blue-600" />
                <h3 className="text-xs sm:text-sm font-bold text-slate-900 flex items-center gap-2">
                  <span>研判结论与法定依据</span>
                  <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-blue-50 text-blue-700 border border-blue-200 font-medium">
                    {activeQA.lawBasis.country} · {activeQA.lawBasis.normId}
                  </span>
                </h3>
              </div>

              <div className="flex items-center gap-2">
                <button
                  type="button"
                  onClick={() =>
                    handleCopyText(
                      `${activeQA.verdict}\n\n依据：${activeQA.lawBasis.title}\n${activeQA.strategy}`
                    )
                  }
                  className="px-2.5 py-1 text-[11px] text-slate-600 hover:text-slate-900 rounded-lg hover:bg-slate-100 flex items-center gap-1 transition-colors cursor-pointer"
                >
                  {copied ? (
                    <Check className="w-3.5 h-3.5 text-blue-600" />
                  ) : (
                    <Copy className="w-3.5 h-3.5 text-slate-400" />
                  )}
                  <span>{copied ? '已复制' : '复制'}</span>
                </button>

                <button
                  type="button"
                  onClick={() => setActiveQA(null)}
                  className="p-1 rounded-lg text-slate-400 hover:text-slate-600 hover:bg-slate-100 cursor-pointer"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-3">
              <div className="p-3 rounded-xl bg-slate-50 border border-slate-200/70 space-y-1">
                <div className="text-[11px] font-bold text-slate-800">判定结论</div>
                <p className="text-xs text-slate-700 leading-relaxed">{activeQA.verdict}</p>
              </div>

              <div className="p-3 rounded-xl bg-slate-50 border border-slate-200/70 space-y-1">
                <div className="text-[11px] font-bold text-slate-800">法定依据与法条正本</div>
                <div className="text-xs text-slate-900 font-semibold">
                  {activeQA.lawBasis.flag} {activeQA.lawBasis.title}
                </div>
                <blockquote className="text-[11px] text-slate-600 italic border-l-2 border-blue-500 pl-2 leading-relaxed">
                  "{activeQA.lawBasis.quote}"
                </blockquote>
              </div>

              <div className="p-3 rounded-xl bg-slate-50 border border-slate-200/70 space-y-1">
                <div className="text-[11px] font-bold text-slate-800">实务对策与建议</div>
                <p className="text-xs text-slate-700 leading-relaxed">{activeQA.strategy}</p>
              </div>
            </div>

            <div className="pt-2 flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-t border-slate-100">
              <span className="text-[11px] text-slate-400 font-mono">
                司法部“法通网”现行法源对齐
              </span>

              <div className="flex items-center gap-2">
                <button
                  type="button"
                  onClick={() => setCurrentView('search')}
                  className="px-3 py-1.5 rounded-lg border border-slate-200 text-xs font-medium text-slate-700 hover:bg-slate-50 transition-colors cursor-pointer"
                >
                  在法典库精读 ➔
                </button>
                <button
                  type="button"
                  onClick={() => handleUpgradeToCase(activeQA)}
                  className="px-3.5 py-1.5 rounded-lg text-xs font-semibold text-white bg-blue-600 hover:bg-blue-700 transition-all shadow-xs shadow-blue-500/25 active:scale-[0.98] cursor-pointer flex items-center gap-1.5"
                >
                  <Plus className="w-3.5 h-3.5" />
                  <span>以此立项研判 ➔</span>
                </button>
              </div>
            </div>
          </section>
        )}

        {/* 核心业务枢纽 (4 大工作台卡片：已清理冗余标签，紧凑高质感) */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3.5">
          {/* Hub 1: 专案深度研判舱 */}
          <div
            onClick={() => setCurrentView('analysis')}
            className="group apple-bento-card rounded-[22px] p-4 sm:p-4.5 flex flex-col justify-between space-y-3 hover:border-blue-500/60 hover:shadow-md transition-all duration-200 cursor-pointer active:scale-[0.98]"
          >
            <div className="space-y-2">
              <div className="w-8 h-8 rounded-xl bg-blue-50 border border-blue-200/60 text-blue-600 flex items-center justify-center shrink-0 shadow-2xs">
                <FileText className="w-4 h-4 text-blue-600" />
              </div>
              <div>
                <h3 className="text-xs sm:text-sm font-bold text-slate-900 group-hover:text-blue-600 transition-colors">
                  专案深度法律研判
                </h3>
                <p className="text-[11px] text-slate-500 mt-0.5 leading-normal">
                  出海工程投资准入与索赔争议深度研判
                </p>
              </div>
            </div>
            <div className="pt-2 border-t border-slate-100 flex items-center justify-between text-xs font-medium text-blue-600">
              <span>进入专案研判</span>
              <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
            </div>
          </div>

          {/* Hub 2: 涉外合同合规审查 */}
          <div
            onClick={() => setCurrentView('verification')}
            className="group apple-bento-card rounded-[22px] p-4 sm:p-4.5 flex flex-col justify-between space-y-3 hover:border-blue-500/60 hover:shadow-md transition-all duration-200 cursor-pointer active:scale-[0.98]"
          >
            <div className="space-y-2">
              <div className="w-8 h-8 rounded-xl bg-blue-50 border border-blue-200/60 text-blue-600 flex items-center justify-center shrink-0 shadow-2xs">
                <FileCheck2 className="w-4 h-4 text-blue-600" />
              </div>
              <div>
                <h3 className="text-xs sm:text-sm font-bold text-slate-900 group-hover:text-blue-600 transition-colors">
                  涉外合同合规审查
                </h3>
                <p className="text-[11px] text-slate-500 mt-0.5 leading-normal">
                  工程专用条件合规核验与示范替代条款
                </p>
              </div>
            </div>
            <div className="pt-2 border-t border-slate-100 flex items-center justify-between text-xs font-medium text-blue-600">
              <span>进入合同审查</span>
              <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
            </div>
          </div>

          {/* Hub 3: 东盟法规与裁判库 */}
          <div
            onClick={() => setCurrentView('search')}
            className="group apple-bento-card rounded-[22px] p-4 sm:p-4.5 flex flex-col justify-between space-y-3 hover:border-blue-500/60 hover:shadow-md transition-all duration-200 cursor-pointer active:scale-[0.98]"
          >
            <div className="space-y-2">
              <div className="w-8 h-8 rounded-xl bg-blue-50 border border-blue-200/60 text-blue-600 flex items-center justify-center shrink-0 shadow-2xs">
                <BookOpen className="w-4 h-4 text-blue-600" />
              </div>
              <div>
                <h3 className="text-xs sm:text-sm font-bold text-slate-900 group-hover:text-blue-600 transition-colors">
                  东盟法规与裁判库
                </h3>
                <p className="text-[11px] text-slate-500 mt-0.5 leading-normal">
                  重点法域现行法典、法通网权威译本与裁判先例
                </p>
              </div>
            </div>
            <div className="pt-2 border-t border-slate-100 flex items-center justify-between text-xs font-medium text-blue-600">
              <span>检索法规判例</span>
              <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
            </div>
          </div>

          {/* Hub 4: 央国企涉外合规评估中心 */}
          <div
            onClick={() => setCurrentView('compliance')}
            className="group apple-bento-card rounded-[22px] p-4 sm:p-4.5 flex flex-col justify-between space-y-3 hover:border-blue-500/60 hover:shadow-md transition-all duration-200 cursor-pointer active:scale-[0.98]"
          >
            <div className="space-y-2">
              <div className="w-8 h-8 rounded-xl bg-blue-50 border border-blue-200/60 text-blue-600 flex items-center justify-center shrink-0 shadow-2xs">
                <Sliders className="w-4 h-4 text-blue-600" />
              </div>
              <div>
                <h3 className="text-xs sm:text-sm font-bold text-slate-900 group-hover:text-blue-600 transition-colors">
                  涉外合规评估中心
                </h3>
                <p className="text-[11px] text-slate-500 mt-0.5 leading-normal">
                  三道防线合规自测评估与各法域合规要点矩阵
                </p>
              </div>
            </div>
            <div className="pt-2 border-t border-slate-100 flex items-center justify-between text-xs font-medium text-blue-600">
              <span>开展合规评估</span>
              <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
            </div>
          </div>
        </div>

        {/* ========================================================================= */}
        {/* 出海重点案卷与标杆示范卷宗 (保持原有完整尺寸) */}
        {/* ========================================================================= */}
        <section className="apple-bento-card rounded-[24px] p-5 sm:p-6 space-y-3.5 shadow-2xs">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-100 pb-3">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center">
                <FolderOpen className="w-4 h-4" />
              </div>
              <div>
                <h2 className="text-sm font-bold text-slate-900">
                  出海重点案卷与标杆示范卷宗
                </h2>
              </div>
            </div>

            <div className="flex items-center gap-2">
              <button
                type="button"
                onClick={openCaseEntryModal}
                className="px-3.5 py-1.5 rounded-xl text-xs font-semibold text-white bg-blue-600 hover:bg-blue-700 transition-all shadow-xs shadow-blue-500/25 active:scale-[0.98] cursor-pointer flex items-center gap-1.5"
              >
                <Plus className="w-3.5 h-3.5" />
                <span>录入新项目</span>
              </button>
              <button
                type="button"
                onClick={() => setCurrentView('cases')}
                className="text-xs text-blue-600 hover:text-blue-800 font-medium px-2 py-1 cursor-pointer"
              >
                全部 ({casesList.length}) ➔
              </button>
            </div>
          </div>

          {casesList.length === 0 ? (
            <div className="p-8 text-center bg-slate-50/60 rounded-2xl border border-dashed border-slate-300 space-y-3">
              <div className="w-10 h-10 rounded-2xl bg-blue-50 text-blue-600 flex items-center justify-center mx-auto border border-blue-200/60 shadow-xs">
                <FolderPlus className="w-5 h-5" />
              </div>
              <div className="space-y-1">
                <p className="text-sm font-semibold text-slate-800">暂无专案卷宗，从这里开始您的第一个出海项目</p>
                <p className="text-xs text-slate-500">支持录入东盟六国涉外工程 EPC、特许经营 BOT 或海外投资并购专案，启动全流程法律分析与论证研判</p>
              </div>
              <div className="pt-2 flex items-center justify-center gap-3">
                <button
                  type="button"
                  onClick={openCaseEntryModal}
                  className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl text-xs font-semibold text-white bg-blue-600 hover:bg-blue-700 transition shadow-xs cursor-pointer"
                >
                  <Plus className="w-3.5 h-3.5" />
                  <span>立即创建专案</span>
                </button>
              </div>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3 pt-1">
              {casesList.slice(0, 4).map((c) => {
              const isPreInv = c.lifecycle_stage === 'pre_investment';
              return (
                <div
                  key={c.case_id}
                  onClick={() => {
                    loadCase(c.case_id);
                    setCurrentView('analysis');
                  }}
                  className="p-4 rounded-2xl border border-slate-200/80 hover:border-blue-500/60 bg-white hover:bg-slate-50/70 transition-all duration-150 cursor-pointer flex flex-col justify-between space-y-2.5 group shadow-2xs active:scale-[0.98]"
                >
                  <div className="space-y-1.5">
                    <div className="flex items-center justify-between">
                      <span className="font-mono text-xs font-bold text-blue-600">
                        {c.case_id}
                      </span>
                      <span
                        className={`text-[10px] px-2 py-0.5 rounded-md font-medium ${
                          isPreInv
                            ? 'bg-indigo-50 text-indigo-700 border border-indigo-200/80'
                            : 'bg-purple-50 text-purple-700 border border-purple-200/80'
                        }`}
                      >
                        {isPreInv ? '投前准入' : '履约争议'}
                      </span>
                    </div>

                    <h3 className="text-xs font-semibold text-slate-900 group-hover:text-blue-600 transition-colors line-clamp-2 leading-snug">
                      {c.title}
                    </h3>
                  </div>

                  <div className="pt-2 border-t border-slate-100 flex items-center justify-between text-[11px] text-slate-400 font-mono">
                    <span>{c.jurisdiction || '东盟'}</span>
                    <span className="text-blue-600 group-hover:translate-x-0.5 transition-transform flex items-center gap-0.5 font-sans font-medium">
                      进入 ➔
                    </span>
                  </div>
                </div>
              );
            })}
            </div>
          )}
        </section>

        {/* 底部：东盟重点法域最新立法与司法动态提示 */}
        <section className="apple-bento-card rounded-2xl p-4 text-xs space-y-2.5">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-100 pb-2.5">
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-blue-600" />
              <span className="font-bold text-slate-800 text-xs">
                东盟重点法域最新立法与司法动态提示
              </span>
              <span className="text-[10px] text-slate-400 font-mono hidden sm:inline">
                / Recent Legal Developments
              </span>
            </div>
            <button
              type="button"
              onClick={() => setCurrentView('compliance')}
              className="text-blue-600 hover:text-blue-700 font-medium cursor-pointer flex items-center gap-1 text-[11px] self-start sm:self-auto"
            >
              <span>查看跨国合规评估与比选</span>
              <ChevronRight className="w-3.5 h-3.5" />
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-2.5 pt-0.5">
            <div className="p-2.5 rounded-xl bg-slate-50/70 border border-slate-100 space-y-1">
              <div className="flex items-center gap-1.5 font-semibold text-slate-800 text-[11px]">
                <span>🇻🇳</span>
                <span>越南《2025新建设法》</span>
              </div>
              <p className="text-[11px] text-slate-500 leading-normal">
                确立工程预定违约金（LD）机制，打破旧法仅认可 12% 惩罚性违约金的刚性限制。
              </p>
            </div>

            <div className="p-2.5 rounded-xl bg-slate-50/70 border border-slate-100 space-y-1">
              <div className="flex items-center gap-1.5 font-semibold text-slate-800 text-[11px]">
                <span>🇮🇩</span>
                <span>印尼最高院 SEMA 3/2023</span>
              </div>
              <p className="text-[11px] text-slate-500 leading-normal">
                最高法院确立：除证明当事人恶意串通外，涉外合同未签署印尼语译本不必然绝对无效。
              </p>
            </div>

            <div className="p-2.5 rounded-xl bg-slate-50/70 border border-slate-100 space-y-1">
              <div className="flex items-center gap-1.5 font-semibold text-slate-800 text-[11px]">
                <span>🇵🇭</span>
                <span>菲律宾新 PPP 法典 (RA 11966)</span>
              </div>
              <p className="text-[11px] text-slate-500 leading-normal">
                全面废止实施 30 年的旧 BOT 法，确立特许经营因政府原因终止的公允审计清算补偿规则。
              </p>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
};
