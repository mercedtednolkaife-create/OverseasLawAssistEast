import React, { useState, useEffect, useMemo } from 'react';
import { useApp } from '../../context/AppContext';
import { lawAgentApi } from '../../api/lawAgentApi';
import { NormOrCaseItem, SearchFilter } from '../../types/lawAgent';
import {
  searchLocalNormsAndCases,
  DEFAULT_SEARCH_ITEMS,
  SEARCH_JURISDICTIONS,
  getItemJurisdiction,
} from './normSearchDefaultData';
import {
  Search,
  ExternalLink,
  BookOpen,
  Paperclip,
  Check,
  ShieldCheck,
  Loader2,
  Copy,
  Scale,
  Sparkles,
  Filter,
  X,
} from 'lucide-react';

export const NormSearchEngineView: React.FC = () => {
  const {
    currentCase,
    currentCaseId,
    openRightDock,
    showToast,
    refreshCurrentCase,
    searchDefaultKind,
    searchDefaultQuery,
  } = useApp();

  const [query, setQuery] = useState(searchDefaultQuery || '');
  const [selectedJur, setSelectedJur] = useState<string>('all');
  const [selectedLaw, setSelectedLaw] = useState<string>('all');
  const [selectedKind, setSelectedKind] = useState<'all' | 'norm' | 'case'>(searchDefaultKind || 'all');
  const [items, setItems] = useState<NormOrCaseItem[]>(() =>
    searchLocalNormsAndCases(searchDefaultQuery || '', 'all', searchDefaultKind || 'all', 'all')
  );
  const [loading, setLoading] = useState(false);
  const [selectedItem, setSelectedItem] = useState<NormOrCaseItem | null>(() => {
    const initList = searchLocalNormsAndCases(searchDefaultQuery || '', 'all', searchDefaultKind || 'all', 'all');
    return initList[0] || null;
  });

  const [attaching, setAttaching] = useState(false);
  const [attachedSuccess, setAttachedSuccess] = useState(false);
  const [copiedField, setCopiedField] = useState<'original' | 'zh' | null>(null);

  const hotKeywords = [
    '印尼 SEMA 3/2023 双语令',
    '新加坡 BS Mount Sophia 保函止付',
    '马来西亚 CIPAA 35条背靠背',
    '越南 2025新建设法工期顺延',
    '泰国 FBA 建筑外资准入',
    '菲律宾 PCAB 资质许可',
    'FIDIC 20.1 索赔通知时效',
    '国资委35号令 境外合规',
  ];

  // 同步外部/首页传入的检索参数
  useEffect(() => {
    if (searchDefaultQuery !== undefined) {
      setQuery(searchDefaultQuery);
    }
  }, [searchDefaultQuery]);

  useEffect(() => {
    if (searchDefaultKind) {
      setSelectedKind(searchDefaultKind);
    }
  }, [searchDefaultKind]);

  // 执行综合检索与国别过滤
  const handleSearch = async (targetQuery?: string, targetJur?: string) => {
    const q = targetQuery !== undefined ? targetQuery : query;
    const jur = targetJur !== undefined ? targetJur : selectedJur;

    // 1. 先行执行即时本地权威知识库检索（0ms 响应，杜绝白屏与等待）
    const localResults = searchLocalNormsAndCases(q, selectedLaw, selectedKind, jur);
    setItems(localResults);
    if (!selectedItem || !localResults.some((i) => i.id === selectedItem.id)) {
      setSelectedItem(localResults[0] || null);
    }

    // 2. 向后端检索接口请求动态更新（静默对齐）
    setLoading(true);
    try {
      const filters: SearchFilter = {
        law: selectedLaw === 'all' ? undefined : selectedLaw,
        kind: selectedKind,
      };
      const res = await lawAgentApi.searchNormsAndCases(q, filters);
      const safeItems = Array.isArray(res) ? res : [];
      if (safeItems.length > 0) {
        // 如果当前勾选了特定法域，同步进行法域过滤
        const filteredRes = jur === 'all'
          ? safeItems
          : safeItems.filter((item) => getItemJurisdiction(item).code === jur);

        if (filteredRes.length > 0) {
          setItems(filteredRes);
          if (!selectedItem || !filteredRes.some((i) => i.id === selectedItem.id)) {
            setSelectedItem(filteredRes[0]);
          }
        }
      }
    } catch (err: any) {
      console.warn('法源后台同步失败，使用本地权威法源兜底:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    handleSearch(query, selectedJur);
  }, [selectedJur, selectedLaw, selectedKind]);

  // 挂载至案卷附表
  const handleAttachToCase = async () => {
    if (!selectedItem) return;
    if (!currentCaseId) {
      showToast('请先选择或新建目标案卷以挂载法源', 'warning');
      return;
    }
    setAttaching(true);
    try {
      await lawAgentApi.attachCaseArtifact(currentCaseId, {
        artifact_type: 'statute_pin',
        title: `${selectedItem.id} · ${selectedItem.title}`,
        jurisdiction: currentCase?.meta?.jurisdiction || 'asean_id',
        summary: selectedItem.text_zh_machine?.slice(0, 200) || selectedItem.title,
        source_url: selectedItem.source_url,
      });
      setAttachedSuccess(true);
      showToast(`✓ 已成功将法源【${selectedItem.id}】挂载至案卷【${currentCaseId}】`, 'success');
      await refreshCurrentCase();
      setTimeout(() => setAttachedSuccess(false), 2500);
    } catch (e: any) {
      showToast(e.message || '挂载失败', 'error');
    } finally {
      setAttaching(false);
    }
  };

  // 复制条文或判例内容
  const handleCopyText = (text: string, type: 'original' | 'zh') => {
    navigator.clipboard.writeText(text);
    setCopiedField(type);
    showToast(`${type === 'original' ? '官方原文' : '中文权威释义'}已复制至剪贴板`, 'success');
    setTimeout(() => setCopiedField(null), 2000);
  };

  const currentJur = selectedItem ? getItemJurisdiction(selectedItem) : null;

  return (
    <div className="max-w-[1600px] mx-auto px-4 sm:px-6 py-6 space-y-6">
      {/* 顶部检索控制台 Header Banner */}
      <div className="apple-bento-card rounded-[28px] p-6 sm:p-7 relative overflow-hidden space-y-4">
        <div className="relative z-10 max-w-5xl space-y-2">
          <div className="inline-flex items-center gap-2 px-2.5 py-1 rounded-full bg-blue-50 border border-blue-200/80 text-blue-700 text-xs font-semibold">
            <span className="w-1.5 h-1.5 rounded-full bg-blue-600 animate-pulse" />
            <span>2026 现行有效法源 · 官方公报权威对齐</span>
          </div>

          <h1 className="text-xl sm:text-2xl font-bold tracking-tight text-slate-900">
            东盟工程法规与裁判库
          </h1>

          <p className="text-xs sm:text-sm text-slate-600 leading-relaxed font-normal">
            收录东盟六国建设工程强行法、FIDIC 标准范本及最高法院司法裁判先例，支持中外双语对照研读。
          </p>

          {/* 法域快速筛选胶囊条 */}
          <div className="flex flex-wrap items-center gap-2 pt-1">
            <span className="text-xs text-slate-400 font-medium">法域：</span>
            {SEARCH_JURISDICTIONS.map((j) => {
              const isSelected = selectedJur === j.code;
              return (
                <button
                  key={j.code}
                  type="button"
                  onClick={() => {
                    setSelectedJur(j.code);
                    handleSearch(query, j.code);
                  }}
                  className={`px-3 py-1.5 rounded-xl text-xs font-medium border transition-all cursor-pointer flex items-center gap-1.5 ${
                    isSelected
                      ? 'bg-blue-600 text-white border-blue-600 shadow-xs shadow-blue-500/25 font-semibold'
                      : 'bg-white/80 text-slate-600 border-slate-200/80 hover:bg-white hover:text-slate-900 shadow-2xs'
                  }`}
                >
                  <span>{j.flag}</span>
                  <span>{j.name}</span>
                  <span
                    className={`text-[10px] font-mono px-1 py-0.2 rounded ${
                      isSelected ? 'bg-blue-700 text-blue-100' : 'bg-slate-100 text-slate-500'
                    }`}
                  >
                    {j.count}
                  </span>
                  {isSelected && <Check className="w-3 h-3 text-white ml-0.5" />}
                </button>
              );
            })}
          </div>
        </div>

        {/* 装饰水印图标 */}
        <div className="absolute right-6 -bottom-6 opacity-5 pointer-events-none hidden lg:block">
          <Scale className="w-56 h-56 text-slate-900" />
        </div>

        {/* 检索输入框与过滤控制器 */}
        <div className="pt-2 border-t border-slate-100/90 flex flex-col md:flex-row gap-3">
          {/* 输入框 */}
          <div className="relative flex-1">
            <Search className="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
              placeholder="输入关键词、法条号或案由检索..."
              className="w-full pl-10 pr-9 py-2.5 text-xs border border-slate-200/90 rounded-2xl focus:outline-none focus:ring-2 focus:ring-blue-500/10 focus:border-blue-600/80 bg-slate-50/50 focus:bg-white transition-all text-slate-900 shadow-2xs"
            />
            {query && (
              <button
                type="button"
                onClick={() => {
                  setQuery('');
                  handleSearch('', selectedJur);
                }}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 cursor-pointer"
              >
                <X className="w-3.5 h-3.5" />
              </button>
            )}
          </div>

          <div className="flex items-center gap-2 flex-wrap sm:flex-nowrap">
            {/* 具体法典下拉过滤 */}
            <select
              value={selectedLaw}
              onChange={(e) => setSelectedLaw(e.target.value)}
              className="px-3 py-2.5 text-xs border border-slate-200/80 rounded-xl bg-white text-slate-700 font-medium focus:outline-none focus:ring-2 focus:ring-blue-500/10 focus:border-blue-600/80 shadow-2xs cursor-pointer max-w-[210px]"
            >
              <option value="all">全部法典与范本</option>
              <optgroup label="🇮🇩 印度尼西亚法源">
                <option value="UU_2_2017">UU 2/2017 · 建筑服务法</option>
                <option value="SEMA_3_2023">SEMA 3/2023 · 合同语言通告</option>
                <option value="MEMR_11_2024">MEMR 11/2024 · 本地化率 (TKDN)</option>
                <option value="KUHPerdata">KUHPerdata · 民法典第1338条</option>
              </optgroup>
              <optgroup label="🇻🇳 越南法源">
                <option value="Law_135_2025">Law 135/2025 · 2025新建设法</option>
                <option value="Decree_210_2026">Decree 210/2026 · 违约金上限</option>
              </optgroup>
              <optgroup label="🇲🇾 马来西亚法源">
                <option value="CIPAA_2012">CIPAA 2012 · 施工付款裁决法</option>
                <option value="Act_520_CIDB">Act 520 · 建筑工业发展局法令</option>
              </optgroup>
              <optgroup label="🇸🇬 新加坡法源">
                <option value="SOPA_2004">SOPA 2004 · 施工付款保障法</option>
              </optgroup>
              <optgroup label="🇹🇭 泰国法源">
                <option value="CCC">CCC · 民商法典承揽编</option>
                <option value="FBA_1999">FBA 1999 · 外商经营法</option>
              </optgroup>
              <optgroup label="🇵🇭 菲律宾法源">
                <option value="RA_11966">RA 11966 · 菲律宾新 PPP 法案</option>
              </optgroup>
              <optgroup label="📑 FIDIC 国际工程合同范本">
                <option value="FIDIC_SILVER">FIDIC 银皮书 (EPC交钥匙)</option>
                <option value="FIDIC_YELLOW">FIDIC 黄皮书 (设计建造)</option>
                <option value="FIDIC_RED">FIDIC 红皮书 (施工合同)</option>
              </optgroup>
              <optgroup label="🛡️ 央企合规与条约">
                <option value="SASAC_Order_35">国资委35号令 · 境外合规</option>
                <option value="Data_Security_Law">数据安全法第36条 · 跨境审查</option>
                <option value="BIT">中印尼双边投资协定 (BIT)</option>
                <option value="SINOSURE">中信保 · 海外项目险索赔条款</option>
              </optgroup>
            </select>

            {/* 类型分段切换 */}
            <div className="flex items-center p-1 bg-slate-100 rounded-xl border border-slate-200/70 text-xs">
              <button
                type="button"
                onClick={() => setSelectedKind('all')}
                className={`px-2.5 py-1.5 rounded-lg font-medium transition-all cursor-pointer ${
                  selectedKind === 'all'
                    ? 'bg-white text-blue-700 shadow-2xs font-semibold'
                    : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                全部
              </button>
              <button
                type="button"
                onClick={() => setSelectedKind('norm')}
                className={`px-2.5 py-1.5 rounded-lg font-medium transition-all cursor-pointer ${
                  selectedKind === 'norm'
                    ? 'bg-white text-blue-700 shadow-2xs font-semibold'
                    : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                法条 (31)
              </button>
              <button
                type="button"
                onClick={() => setSelectedKind('case')}
                className={`px-2.5 py-1.5 rounded-lg font-medium transition-all cursor-pointer ${
                  selectedKind === 'case'
                    ? 'bg-white text-blue-700 shadow-2xs font-semibold'
                    : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                判例 (7)
              </button>
            </div>

            <button
              onClick={() => handleSearch()}
              className="px-5 py-2.5 text-xs font-semibold text-white bg-blue-600 hover:bg-blue-700 rounded-xl transition-all shadow-xs shadow-blue-500/25 shrink-0 cursor-pointer active:scale-[0.98] flex items-center gap-1.5"
            >
              <Search className="w-3.5 h-3.5" />
              <span>检索</span>
            </button>
          </div>
        </div>

        {/* 热门实务检索词胶囊 */}
        <div className="flex flex-wrap items-center gap-2 pt-2 border-t border-slate-100">
          <span className="text-[11px] text-slate-400 font-medium">快捷检索：</span>
          {hotKeywords.map((kw) => (
            <button
              key={kw}
              type="button"
              onClick={() => {
                setQuery(kw);
                handleSearch(kw, selectedJur);
              }}
              className="px-2.5 py-1 text-[11px] font-mono font-medium rounded-lg bg-slate-100/80 hover:bg-blue-50 hover:text-blue-600 text-slate-600 transition-colors border border-slate-200/60 cursor-pointer"
            >
              {kw}
            </button>
          ))}
        </div>
      </div>

      {/* 结果分栏展示区 */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* 左侧：法条与判例列表 (5列) */}
        <div className="lg:col-span-5 apple-bento-card rounded-[28px] divide-y divide-slate-100/80 overflow-hidden shadow-2xs">
          <div className="px-5 py-3.5 bg-slate-50/80 text-xs font-semibold text-slate-600 flex items-center justify-between">
            <span className="flex items-center gap-1.5">
              <BookOpen className="w-3.5 h-3.5 text-blue-600" />
              <span>法源列表 ({items.length})</span>
            </span>
            <span className="text-[11px] text-slate-400 font-mono">
              现行有效
            </span>
          </div>

          {loading ? (
            <div className="p-12 text-center text-xs text-slate-400 flex flex-col items-center justify-center gap-2">
              <Loader2 className="w-5 h-5 text-blue-600 animate-spin" />
              <span>正在对齐法源...</span>
            </div>
          ) : items.length === 0 ? (
            <div className="p-12 text-center text-xs text-slate-400 space-y-1">
              <p className="font-semibold text-slate-600">未检索到匹配的条文或裁判先例</p>
              <p className="text-[11px]">请切换法源分类或调整关键词</p>
            </div>
          ) : (
            <div className="max-h-[720px] overflow-y-auto divide-y divide-slate-100">
              {items.map((item) => {
                const isSelected = selectedItem?.id === item.id;
                const jur = getItemJurisdiction(item);
                return (
                  <div
                    key={item.id}
                    onClick={() => setSelectedItem(item)}
                    className={`p-4 text-xs cursor-pointer transition-all duration-150 ${
                      isSelected
                        ? 'bg-blue-50/70 text-slate-900 border-l-4 border-blue-600'
                        : 'hover:bg-slate-50/80 text-slate-700 border-l-4 border-transparent'
                    }`}
                  >
                    <div className="flex items-center justify-between gap-2 mb-1.5">
                      <div className="flex items-center gap-1.5 truncate">
                        <span className="text-sm">{jur.flag}</span>
                        <span className="font-mono font-bold text-slate-900 truncate">
                          {item.id}
                        </span>
                      </div>
                      <div className="flex items-center gap-1 shrink-0">
                        {item.layer === 'L2' ? (
                          <span className="text-[10px] px-1.5 py-0.5 rounded-md font-mono font-medium bg-amber-50 text-amber-700 border border-amber-200/80">
                            L2参考
                          </span>
                        ) : (
                          <span className="text-[10px] px-1.5 py-0.5 rounded-md font-mono font-medium bg-emerald-50 text-emerald-700 border border-emerald-200/80">
                            L1核心
                          </span>
                        )}
                        <span
                          className={`text-[10px] px-2 py-0.5 rounded-md uppercase font-mono font-medium border ${
                            item.kind === 'norm'
                              ? 'bg-blue-50 text-blue-700 border-blue-200/80'
                              : 'bg-purple-50 text-purple-700 border-purple-200/80'
                          }`}
                        >
                          {item.kind === 'norm' ? '法条' : '判例'}
                        </span>
                      </div>
                    </div>

                    <h4 className="text-xs font-semibold text-slate-900 line-clamp-2 leading-relaxed">
                      {item.title}
                    </h4>

                    <p className="text-[11px] text-slate-500 line-clamp-2 mt-1 leading-relaxed">
                      {item.text_zh_machine}
                    </p>
                  </div>
                );
              })}
            </div>
          )}
        </div>

        {/* 右侧：法源条文与裁判深度研读卡 (7列) */}
        <div className="lg:col-span-7 apple-bento-card rounded-[28px] p-6 space-y-5 sticky top-16 shadow-2xs">
          {selectedItem ? (
            <>
              {/* 头部元数据与操作 */}
              <div className="border-b border-slate-100 pb-4 space-y-3">
                <div className="flex flex-wrap items-center justify-between gap-3">
                  <div className="flex items-center gap-2">
                    <span className="text-lg">{currentJur?.flag}</span>
                    <span className="text-base font-bold font-mono text-slate-900">
                      {selectedItem.id}
                    </span>
                    <span
                      className={`text-[10px] px-2 py-0.5 rounded-md font-mono font-semibold border ${
                        selectedItem.layer === 'L2'
                          ? 'bg-amber-50 text-amber-700 border-amber-200'
                          : 'bg-emerald-50 text-emerald-700 border-emerald-200'
                      }`}
                    >
                      {selectedItem.layer === 'L2' ? 'L2 广覆盖参考' : 'L1 核心强行法'}
                    </span>
                    <span
                      className={`text-[10px] px-2 py-0.5 rounded-md uppercase font-mono font-semibold border ${
                        selectedItem.kind === 'norm'
                          ? 'bg-blue-50 text-blue-700 border-blue-200'
                          : 'bg-purple-50 text-purple-700 border-purple-200'
                      }`}
                    >
                      {selectedItem.kind === 'norm' ? '成文法条' : '裁判先例'}
                    </span>
                  </div>

                  <div className="flex items-center gap-2">
                    {/* 双语对照研读按钮 */}
                    <button
                      type="button"
                      onClick={() => openRightDock('law_reader', selectedItem.id)}
                      className="text-xs text-slate-700 hover:text-slate-900 bg-white hover:bg-slate-50 border border-slate-200/90 px-3 py-1.5 rounded-xl flex items-center gap-1.5 font-medium transition-all shadow-2xs hover:border-slate-300 active:scale-[0.98] cursor-pointer"
                      title="呼出右侧并排对照研读副驾舱"
                    >
                      <BookOpen className="w-3.5 h-3.5 text-blue-600" />
                      <span>双语对照 ➔</span>
                    </button>

                    {/* 挂载至案卷附表 */}
                    <button
                      type="button"
                      onClick={handleAttachToCase}
                      disabled={attaching}
                      className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-semibold transition-all cursor-pointer shadow-2xs ${
                        attachedSuccess
                          ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                          : 'bg-white hover:bg-slate-50 text-slate-800 border border-slate-200/90'
                      }`}
                    >
                      {attaching ? (
                        <>
                          <Loader2 className="w-3.5 h-3.5 animate-spin text-blue-600" />
                          <span>挂载中...</span>
                        </>
                      ) : attachedSuccess ? (
                        <>
                          <Check className="w-3.5 h-3.5 text-emerald-600" />
                          <span>✓ 已引用到案卷</span>
                        </>
                      ) : (
                        <>
                          <Paperclip className="w-3.5 h-3.5 text-slate-500" />
                          <span>+ 引用到案卷</span>
                        </>
                      )}
                    </button>

                    {/* 官方出处外链 */}
                    {selectedItem.source_url && (
                      <a
                        href={selectedItem.source_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-xs text-slate-500 hover:text-blue-600 flex items-center gap-1 font-mono transition-colors ml-1"
                        title="查看官方公报出处"
                      >
                        <span>官方出处 ↗</span>
                      </a>
                    )}
                  </div>
                </div>

                {/* 现行有效官方标准认证胶囊 */}
                <div className="p-2.5 bg-blue-50/50 rounded-2xl border border-blue-200/70 flex items-center justify-between text-xs text-blue-900">
                  <div className="flex items-center gap-2">
                    <ShieldCheck className="w-4 h-4 text-blue-600 shrink-0" />
                    <span className="font-semibold">【现行有效】</span>
                    <span className="text-[11px] text-blue-700/90 font-mono hidden sm:inline">
                      官方公报现行编目 · 司法部“法通网”涉外法规库对齐
                    </span>
                  </div>
                </div>

                <div>
                  <h3 className="text-sm font-bold text-slate-900 leading-snug">
                    {selectedItem.title}
                  </h3>
                  {selectedItem.heading_path && (
                    <p className="text-[11px] text-slate-400 font-mono mt-1">
                      {selectedItem.heading_path}
                    </p>
                  )}
                </div>
              </div>

              {/* 官方外文逐字原文 */}
              <div className="space-y-1.5">
                <div className="flex items-center justify-between">
                  <label className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider block">
                    官方正本原文
                  </label>
                  {selectedItem.text_de && (
                    <button
                      type="button"
                      onClick={() => handleCopyText(selectedItem.text_de || '', 'original')}
                      className="text-[11px] text-slate-500 hover:text-blue-600 flex items-center gap-1 cursor-pointer transition-colors"
                    >
                      {copiedField === 'original' ? (
                        <>
                          <Check className="w-3 h-3 text-emerald-600" />
                          <span className="text-emerald-600 font-medium">已复制原文</span>
                        </>
                      ) : (
                        <>
                          <Copy className="w-3 h-3" />
                          <span>复制原文</span>
                        </>
                      )}
                    </button>
                  )}
                </div>
                <div className="p-4 bg-slate-50/80 rounded-2xl border border-slate-200/70 text-xs font-mono text-slate-900 leading-relaxed whitespace-pre-wrap max-h-56 overflow-y-auto">
                  {selectedItem.text_de}
                </div>
              </div>

              {/* 中文权威释义与裁判要旨 */}
              <div className="space-y-1.5">
                <div className="flex items-center justify-between">
                  <label className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider">
                    中文权威释义
                  </label>
                  <div className="flex items-center gap-2">
                    <span className="text-[10px] text-blue-700 bg-blue-50 px-2 py-0.5 rounded font-mono border border-blue-200/60 font-semibold">
                      法通网对齐
                    </span>
                    {selectedItem.text_zh_machine && (
                      <button
                        type="button"
                        onClick={() => handleCopyText(selectedItem.text_zh_machine || '', 'zh')}
                        className="text-[11px] text-slate-500 hover:text-blue-600 flex items-center gap-1 cursor-pointer transition-colors"
                      >
                        {copiedField === 'zh' ? (
                          <>
                            <Check className="w-3 h-3 text-emerald-600" />
                            <span className="text-emerald-600 font-medium">已复制中文</span>
                          </>
                        ) : (
                          <>
                            <Copy className="w-3 h-3" />
                            <span>复制中文</span>
                          </>
                        )}
                      </button>
                    )}
                  </div>
                </div>
                <div className="p-4 bg-slate-50/50 rounded-2xl border border-slate-200/70 text-xs text-slate-800 leading-relaxed whitespace-pre-wrap max-h-56 overflow-y-auto">
                  {selectedItem.text_zh_machine}
                </div>
              </div>

              {/* 效力与数据出处底栏 */}
              <div className="p-3 bg-slate-50/80 rounded-2xl border border-slate-200/60 text-[11px] text-slate-600 font-mono space-y-1">
                <div className="flex items-center justify-between">
                  <div>
                    <span className="font-semibold text-slate-700">现行版本：</span>{' '}
                    <span>{selectedItem.stand || '2026年现行版'}</span>
                  </div>
                  <div>
                    <span className="font-semibold text-slate-700">效力层级：</span>{' '}
                    <span>{selectedItem.kind === 'norm' ? '法定强行规范' : '终审裁判先例'}</span>
                  </div>
                </div>
                <div>
                  <span className="font-semibold text-slate-700">数据来源：</span>{' '}
                  <span>
                    {selectedItem.id.startsWith('FIDIC')
                      ? 'FIDIC 国际工程师联合会日内瓦秘书处'
                      : selectedItem.id.startsWith('SG_')
                      ? '新加坡最高法院判例数据库 (LawNet)'
                      : selectedItem.id.startsWith('ID_')
                      ? '印度尼西亚最高法院案例公开平台 (Mahkamah Agung)'
                      : selectedItem.id.startsWith('MY_')
                      ? '马来西亚司法公报与联邦法院裁判文书库'
                      : selectedItem.id.startsWith('VN_')
                      ? '越南最高人民法院司法判例公报中心'
                      : '中华人民共和国司法部“法通网”涉外法规数据库'}
                  </span>
                </div>
              </div>
            </>
          ) : (
            <div className="p-16 text-center text-xs text-slate-400">
              请在左侧列表选择条目以展开详细条文与款项释义
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
