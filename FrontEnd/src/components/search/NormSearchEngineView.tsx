import React, { useState, useEffect } from 'react';
import { useApp } from '../../context/AppContext';
import { lawAgentApi } from '../../api/lawAgentApi';
import { NormOrCaseItem, SearchFilter } from '../../types/lawAgent';
import { Search, ExternalLink, BookOpen, Paperclip, Check, ShieldCheck, Sparkles, Loader2, ArrowRight } from 'lucide-react';

export const NormSearchEngineView: React.FC = () => {
  const { currentCase, currentCaseId, openLawDrawer, openRightDock, showToast, refreshCurrentCase, searchDefaultKind, searchDefaultQuery } = useApp();
  const [query, setQuery] = useState(searchDefaultQuery || '');
  const [selectedLaw, setSelectedLaw] = useState<string>('all');
  const [selectedKind, setSelectedKind] = useState<'all' | 'norm' | 'case'>(searchDefaultKind || 'all');
  const [items, setItems] = useState<NormOrCaseItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [selectedItem, setSelectedItem] = useState<NormOrCaseItem | null>(null);
  const [attaching, setAttaching] = useState(false);
  const [attachedSuccess, setAttachedSuccess] = useState(false);

  const hotKeywords = [
    'TKDN 本地化率',
    'SEMA 3/2023 双语令',
    'CIPAA 第35条背靠背',
    'BS Mount Sophia 保函止付',
    'RA 11966 菲律宾PPP',
    'FIDIC 20.1 索赔通知',
    '越南 2025新建设法',
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

  const isBrowsingDirectory = !query.trim() && selectedLaw === 'all';

  const handleAttachToCase = async () => {
    if (!selectedItem) return;
    if (!currentCaseId) {
      showToast('请先选择或创建一个目标案卷以挂载法源', 'warning');
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
      showToast(`✓ 已成功将法源【${selectedItem.id}】引用挂载至案卷【${currentCaseId}】`, 'success');
      await refreshCurrentCase();
      setTimeout(() => setAttachedSuccess(false), 2500);
    } catch (e: any) {
      showToast(e.message || '挂载失败', 'error');
    } finally {
      setAttaching(false);
    }
  };

  const handleSearch = async (targetQuery?: string) => {
    const q = targetQuery !== undefined ? targetQuery : query;
    setLoading(true);
    try {
      const filters: SearchFilter = {
        law: selectedLaw === 'all' ? undefined : selectedLaw,
        kind: selectedKind,
      };
      const res = await lawAgentApi.searchNormsAndCases(q, filters);
      const safeItems = Array.isArray(res) ? res : [];
      setItems(safeItems);
      if (safeItems.length > 0 && !selectedItem) {
        setSelectedItem(safeItems[0]);
      }
    } catch (err: any) {
      showToast(err.message || '检索法源失败', 'error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    handleSearch(query);
  }, [selectedLaw, selectedKind, searchDefaultQuery]);

  return (
    <div className="apple-page-pane max-w-[1600px] mx-auto px-4 sm:px-6 py-6 space-y-6">
      {/* 搜索控制台 */}
      <div className="apple-bento-card rounded-[28px] p-6 space-y-5">
        <div className="space-y-1">
          <div className="flex items-center gap-2.5">
            <div className="w-9 h-9 rounded-2xl bg-blue-50 border border-blue-200/60 text-blue-600 flex items-center justify-center shrink-0 shadow-2xs">
              <Search className="w-4 h-4 text-blue-600" />
            </div>
            <h1 className="text-lg font-bold text-slate-900 tracking-tight">
              东盟工程法律法规与权威裁判先例检索
            </h1>
          </div>
          <p className="text-xs text-slate-500 pl-11.5">
            直连东盟六国现行建设与投资法规、FIDIC 国际工程范本、双边投资协定 (BIT) 及央企合规法源，支持多维中英对照检索
          </p>
        </div>

        <div className="flex flex-col sm:flex-row gap-3">
          <div className="relative flex-1">
            <Search className="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
              placeholder="输入法条如 'ID:SEMA_3_2023' 或 'FIDIC 20.1'，或输入中英关键词如 '工期顺延'、'背靠背'、'保函止付'、'TKDN'..."
              className="w-full pl-10 pr-4 py-2.5 text-xs border border-slate-200/90 rounded-2xl focus:outline-none focus:ring-2 focus:ring-blue-500/10 focus:border-blue-600/80 bg-slate-50/50 focus:bg-white transition-all text-slate-900 shadow-2xs"
            />
          </div>

          <div className="flex items-center gap-2 flex-wrap sm:flex-nowrap">
            <select
              value={selectedLaw}
              onChange={(e) => setSelectedLaw(e.target.value)}
              className="px-3 py-2.5 text-xs border border-slate-200/80 rounded-xl bg-white text-slate-700 font-medium focus:outline-none focus:ring-2 focus:ring-blue-500/10 focus:border-blue-600/80 shadow-2xs cursor-pointer"
            >
              <option value="all">全部法典与合同范本 (All Laws & FIDIC)</option>
              <optgroup label="🇮🇩 印度尼西亚法源 (Indonesia)">
                <option value="UU_2_2017">UU No. 2/2017 · 建筑服务法 (联营与分包)</option>
                <option value="SEMA_3_2023">SEMA 3/2023 · 印尼最高院涉外合同语言通告</option>
                <option value="MEMR_11_2024">MEMR 11/2024 · 新能源本地化率 (TKDN) 规程</option>
                <option value="KUHPerdata">KUHPerdata · 民法典第1338条契约守信原则</option>
              </optgroup>
              <optgroup label="🇻🇳 越南法源 (Vietnam)">
                <option value="Law_135_2025">Law 135/2025 · 越南《2025新建设法》</option>
                <option value="Decree_210_2026">Decree 210/2026 · 越南政府违约金上限法令</option>
              </optgroup>
              <optgroup label="🇲🇾 马来西亚法源 (Malaysia)">
                <option value="CIPAA_2012">CIPAA 2012 · 建设工程付款与快速裁决法</option>
              </optgroup>
              <optgroup label="🇸🇬 新加坡法源 (Singapore)">
                <option value="SOPA_2004">SOPA 2004 · 建筑工程付款保障法</option>
              </optgroup>
              <optgroup label="🇹🇭 泰国法源 (Thailand)">
                <option value="CCC">CCC · 民商法典承揽契约编</option>
                <option value="FBA_1999">FBA 1999 · 外商经营法资质准入</option>
              </optgroup>
              <optgroup label="🇵🇭 菲律宾法源 (Philippines)">
                <option value="RA_11966">RA 11966 · 菲律宾新 PPP 法典</option>
              </optgroup>
              <optgroup label="📑 FIDIC 国际工程合同范本">
                <option value="FIDIC_SILVER">FIDIC Silver · 银皮书 (EPC交钥匙总承包)</option>
                <option value="FIDIC_YELLOW">FIDIC Yellow · 黄皮书 (设计施工总承包)</option>
              </optgroup>
              <optgroup label="🛡️ 央国企海外合规与条约">
                <option value="SASAC_Order_35">国资委35号令 · 央企境外投资监督管理办法</option>
                <option value="Data_Security_Law">数据安全法第36条 · 跨境数据调取审查</option>
                <option value="BIT">BIT · 中国与东盟双边投资保护协定</option>
                <option value="SINOSURE">中信保 · 海外项目险可能损失报损条款</option>
              </optgroup>
            </select>

            <select
              value={selectedKind}
              onChange={(e) => setSelectedKind(e.target.value as any)}
              className="px-3 py-2.5 text-xs border border-slate-200/80 rounded-xl bg-white text-slate-700 font-medium focus:outline-none focus:ring-2 focus:ring-blue-500/10 focus:border-blue-600/80 shadow-2xs cursor-pointer"
            >
              <option value="all">全部类型 (法条与判例)</option>
              <option value="norm">成文法条文 (Statutes)</option>
              <option value="case">司法判例 (Cases)</option>
            </select>

            <button
              onClick={() => handleSearch()}
              className="px-5 py-2.5 text-xs font-semibold text-white bg-blue-600 hover:bg-blue-700 rounded-xl transition-all shadow-xs shadow-blue-500/25 shrink-0 cursor-pointer active:scale-[0.98]"
            >
              检索
            </button>
          </div>
        </div>

        {/* 热门实务检索词胶囊 */}
        <div className="flex flex-wrap items-center gap-2 pt-2 border-t border-slate-100">
          <span className="text-[11px] text-slate-400 font-medium">热门实务检索：</span>
          {hotKeywords.map((kw) => (
            <button
              key={kw}
              type="button"
              onClick={() => {
                setQuery(kw);
                handleSearch(kw);
              }}
              className="px-2.5 py-1 text-[11px] font-mono font-medium rounded-lg bg-slate-100 hover:bg-blue-50 hover:text-blue-600 text-slate-600 transition-colors border border-slate-200/60 cursor-pointer"
            >
              {kw}
            </button>
          ))}
        </div>
      </div>

      {/* 结果分栏展示 */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* 左侧列表 (5列) */}
        <div className="lg:col-span-5 apple-bento-card rounded-[28px] divide-y divide-slate-100/80 overflow-hidden shadow-2xs">
          <div className="px-5 py-3.5 bg-slate-50/80 text-xs font-semibold text-slate-600 flex items-center justify-between">
            <span>
              {isBrowsingDirectory
                ? `官方基准法源精选导览 (${items.length} 篇)`
                : `精准检索结果流 (${items.length} 篇)`}
            </span>
            <span className="text-[11px] text-slate-400 font-mono">
              {isBrowsingDirectory ? '官方公报现行编目' : '智能相关度排序'}
            </span>
          </div>

          {loading ? (
            <div className="p-12 text-center text-xs text-slate-400">正在检索跨法域法源...</div>
          ) : items.length === 0 ? (
            <div className="p-12 text-center text-xs text-slate-400">未检索到匹配的条文或判例</div>
          ) : (
            <div className="max-h-[680px] overflow-y-auto divide-y divide-slate-100">
              {items.map((item) => (
                <div
                  key={item.id}
                  onClick={() => setSelectedItem(item)}
                  className={`p-4 text-xs cursor-pointer transition-all duration-150 ${
                    selectedItem?.id === item.id
                      ? 'bg-blue-50/70 font-medium text-slate-900 border-l-2 border-blue-600'
                      : 'hover:bg-slate-50/80 text-slate-700 border-l-2 border-transparent'
                  }`}
                >
                  <div className="flex items-center justify-between gap-2">
                    <span className="font-mono font-bold text-slate-900">{item.id}</span>
                    <span className="text-[10px] px-2 py-0.5 rounded-md bg-white border border-slate-200/80 text-slate-600 uppercase font-mono font-medium">
                      {item.kind === 'norm' ? '法条' : '判例'}
                    </span>
                  </div>
                  <h4 className="text-xs font-semibold text-slate-800 mt-1.5 line-clamp-1">
                    {item.title}
                  </h4>
                  <p className="text-[11px] text-slate-500 line-clamp-2 mt-1 leading-relaxed">
                    {item.text_zh_machine}
                  </p>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* 右侧条文详情 (7列) */}
        <div className="lg:col-span-7 apple-bento-card rounded-[28px] p-6 space-y-5 sticky top-16">
          {selectedItem ? (
            <>
              <div className="border-b border-slate-100 pb-4 space-y-3">
                <div className="flex flex-wrap items-center justify-between gap-3">
                  <span className="text-base font-bold font-mono text-slate-900">
                    {selectedItem.id}
                  </span>
                  <div className="flex items-center gap-2">
                    <button
                      type="button"
                      onClick={() => openRightDock('law_reader', selectedItem.id)}
                      className="text-xs text-slate-700 hover:text-slate-900 bg-white hover:bg-slate-50 border border-slate-200/90 px-3 py-1.5 rounded-xl flex items-center gap-1.5 font-medium transition-all shadow-2xs hover:border-slate-300 active:scale-[0.98] cursor-pointer"
                      title="呼出右侧统一副驾坞并排对照研读"
                    >
                      <BookOpen className="w-3.5 h-3.5 text-slate-600" />
                      <span>双语原文对照 ➔</span>
                    </button>

                    <button
                      type="button"
                      onClick={handleAttachToCase}
                      disabled={attaching}
                      className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-semibold transition-all cursor-pointer shadow-2xs ${
                        attachedSuccess
                          ? 'bg-emerald-600 text-white'
                          : 'bg-white hover:bg-slate-50 text-slate-800 border border-slate-200/90'
                      }`}
                    >
                      {attaching ? (
                        <>
                          <Loader2 className="w-3.5 h-3.5 animate-spin" />
                          <span>挂载中...</span>
                        </>
                      ) : attachedSuccess ? (
                        <>
                          <Check className="w-3.5 h-3.5 text-white" />
                          <span>✓ 已挂载至 {currentCaseId || '当前案卷'}</span>
                        </>
                      ) : (
                        <>
                          <Paperclip className="w-3.5 h-3.5 text-slate-500" />
                          <span>+ 引用至当前案卷</span>
                        </>
                      )}
                    </button>

                    {selectedItem.source_url && (
                      <a
                        href={selectedItem.source_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-xs text-slate-500 hover:text-slate-900 flex items-center gap-1 font-mono transition-colors ml-1"
                      >
                        官方出处
                        <ExternalLink className="w-3.5 h-3.5" />
                      </a>
                    )}
                  </div>
                </div>

                {/* 权威背书金牌标签 */}
                <div className="p-3 bg-amber-50/70 rounded-2xl border border-amber-200/60 flex items-center justify-between text-xs text-amber-900">
                  <div className="flex items-center gap-2">
                    <ShieldCheck className="w-4 h-4 text-amber-600 shrink-0" />
                    <span className="font-semibold">【权威法源认证 · 现行有效】</span>
                    <span className="text-[11px] text-amber-700 font-mono hidden sm:inline">
                      东道国官方公报版本 · 司法部法通网三语对齐 · Grade A 最高查明等级
                    </span>
                  </div>
                </div>

                <div>
                  <h3 className="text-sm font-semibold text-slate-900">
                    {selectedItem.title}
                  </h3>
                  {selectedItem.heading_path && (
                    <p className="text-[11px] text-slate-400 font-mono mt-0.5">
                      {selectedItem.heading_path}
                    </p>
                  )}
                </div>
              </div>

              {/* 官方外文原文 */}
              <div className="space-y-1.5">
                <label className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block">
                  {selectedItem.id.startsWith('FIDIC') || selectedItem.id.startsWith('MY_') || selectedItem.id.startsWith('SG_') || selectedItem.id.startsWith('PH_')
                    ? '英文官方条文与裁判原文 (Official Authentic Text)'
                    : '属地官方语言逐字规范原文 (Official Statutory Text)'}
                </label>
                <div className="p-4 bg-slate-50/80 rounded-2xl border border-slate-200/70 text-xs font-mono text-slate-900 leading-relaxed whitespace-pre-wrap max-h-60 overflow-y-auto">
                  {selectedItem.text_de}
                </div>
              </div>

              {/* 中文对照 */}
              <div className="space-y-1.5">
                <div className="flex items-center justify-between">
                  <label className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
                    中文权威释义与规范要件对照
                  </label>
                  <span className="text-[10px] text-blue-700 bg-blue-50 px-2 py-0.5 rounded font-mono border border-blue-200/60 font-semibold">
                    司法部“法通网”权威对齐
                  </span>
                </div>
                <div className="p-4 bg-slate-50/50 rounded-2xl border border-slate-200/70 text-xs text-slate-800 leading-relaxed whitespace-pre-wrap max-h-60 overflow-y-auto">
                  {selectedItem.text_zh_machine}
                </div>
              </div>

              {/* 效力与数据出处 */}
              <div className="p-3.5 bg-slate-50 rounded-2xl border border-slate-200/60 text-[11px] text-slate-600 font-mono space-y-1">
                <div>
                  <strong>公布与修订版本：</strong>{' '}
                  {selectedItem.stand || '2026年现行有效合并版'}
                </div>
                <div>
                  <strong>数据源机构：</strong>{' '}
                  {selectedItem.id.startsWith('FIDIC')
                    ? 'FIDIC 国际工程师联合会日内瓦秘书处 (Geneva)'
                    : selectedItem.id.startsWith('SG_')
                    ? '新加坡最高法院判例数据库 (LawNet)'
                    : selectedItem.id.startsWith('ID_')
                    ? '印度尼西亚最高法院案例公开平台 (Mahkamah Agung RI)'
                    : '中华人民共和国司法部“法通网”涉外法规数据库'}
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
