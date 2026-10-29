import React, { useState, useEffect } from 'react';
import { useApp } from '../../context/AppContext';
import { lawAgentApi } from '../../api/lawAgentApi';
import { DEFAULT_REFERENCE_CASES } from './complianceDefaultData';
import {
  ArrowRight,
  Copy,
  Check,
  Play,
  AlertTriangle,
  Layers,
  Loader2,
} from 'lucide-react';

interface Case5DItem {
  id: string;
  code: string;
  title: string;
  jurisdiction: string;
  countryName: string;
  countryFlag: string;
  stage: string;
  archetypes: string[];
  summary: string;
  // 5D Review Card Data
  dimension1_structure: {
    parties: { role: string; name: string }[];
    dealSummary: string;
  };
  dimension2_rootCause: {
    coreDiagnosis: string;
    contractPitfall: string;
    triggerFactors: string[];
  };
  dimension3_legalAnchors: {
    normId: string;
    nameZh: string;
    statuteSnippet: string;
    keyRule: string;
  }[];
  dimension4_modelClauses: {
    title: string;
    enClause: string;
    zhExplanation: string;
  }[];
  dimension5_simulation: {
    initialFacts: string;
    initialClaims: string;
  };
}

export const CaseReferenceHub: React.FC = () => {
  const { openCaseEntryModal, openCaseEntryWithPrefill, showToast, openRightDock, setPrefillIntakeParams } = useApp();
  const [cases, setCases] = useState<Case5DItem[]>(DEFAULT_REFERENCE_CASES as unknown as Case5DItem[]);
  const [loading, setLoading] = useState<boolean>(false);
  const [selectedCase, setSelectedCase] = useState<Case5DItem | null>((DEFAULT_REFERENCE_CASES[0] as unknown as Case5DItem) || null);
  const [filterJur, setFilterJur] = useState<string>('all');
  const [copiedId, setCopiedId] = useState<string | null>(null);

  useEffect(() => {
    let mounted = true;
    lawAgentApi
      .getReferenceCases()
      .then((data) => {
        if (mounted && Array.isArray(data) && data.length > 0) {
          const list = data as Case5DItem[];
          setCases(list);
          if (!selectedCase || !list.some((c) => c.id === selectedCase.id)) {
            setSelectedCase(list[0]);
          }
        }
      })
      .catch((err) => {
        console.warn('Reference cases background fetch failed, using fallback:', err);
      });
    return () => {
      mounted = false;
    };
  }, []);

  const filteredCases = cases.filter((c) => {
    if (filterJur !== 'all' && c.jurisdiction !== filterJur) return false;
    return true;
  });

  const handleCopyClause = (text: string, id: string) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    showToast('示范反制条款已复制到剪贴板', 'success');
    setTimeout(() => setCopiedId(null), 2000);
  };

  const handleOpenPlaybook = (item: Case5DItem) => {
    setSelectedCase(item);
    openRightDock('country_playbook');
    showToast(`已在右侧辅助面板展开【${item.countryName}】合规指引与实务复盘手册`, 'info');
  };

  const handleSimulateCase = (item: Case5DItem) => {
    if (setPrefillIntakeParams) {
      setPrefillIntakeParams({
        title: item.title,
        jurisdiction: item.jurisdiction,
        raw_text: `${item.dimension5_simulation.initialFacts}\n\n【诉求】${item.dimension5_simulation.initialClaims}`,
        facts: item.dimension5_simulation.initialFacts,
        claims: item.dimension5_simulation.initialClaims,
      });
    }
    openCaseEntryWithPrefill({
      facts_zh: item.dimension5_simulation.initialFacts,
      claims_zh: item.dimension5_simulation.initialClaims,
      meta: {
        jurisdiction: item.jurisdiction,
        contract_type: item.archetypes.join('+'),
        choice_of_law: `${item.countryName}法律及 FIDIC 国际工程标准合同`,
      },
    });
  };

  return (
    <div className="space-y-5">
      {/* 顶部标题与筛选 */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 apple-bento-card p-5">
        <div>
          <div className="flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded-full bg-blue-600 shadow-xs shadow-blue-500/40" />
            <h2 className="text-base font-bold text-slate-900 tracking-tight">
              中资出海基建典型实务案例库
            </h2>
          </div>
          <p className="text-xs text-slate-500 mt-1">
            覆盖投前、招投标、施工履约至争议解决：包含交易架构、风险根因、核心法源、示范条款与沙盘推演
          </p>
        </div>

        {/* 国别快速过滤 */}
        <div className="flex items-center gap-1.5 overflow-x-auto pb-1 text-xs">
          <button
            onClick={() => setFilterJur('all')}
            className={`px-3 py-1.5 rounded-xl font-medium transition-all cursor-pointer ${
              filterJur === 'all'
                ? 'bg-blue-600 text-white shadow-xs shadow-blue-500/25 font-semibold'
                : 'bg-slate-100 text-slate-600 hover:bg-slate-200/80'
            }`}
          >
            全部案例
          </button>
          {[
            { id: 'asean_id', name: '印尼' },
            { id: 'asean_vn', name: '越南' },
            { id: 'asean_my', name: '马来西亚' },
            { id: 'asean_ph', name: '菲律宾' },
          ].map((item) => (
            <button
              key={item.id}
              onClick={() => setFilterJur(item.id)}
              className={`px-3 py-1.5 rounded-xl font-medium transition-all cursor-pointer ${
                filterJur === item.id
                  ? 'bg-blue-600 text-white shadow-xs shadow-blue-500/25 font-semibold'
                  : 'bg-slate-100 text-slate-600 hover:bg-slate-200/80'
              }`}
            >
              {item.name}
            </button>
          ))}
        </div>
      </div>

      {/* 案例列表与复盘卡展示区 */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
        {/* 左侧：标杆案例选择卡 (4 cols) */}
        <div className="lg:col-span-4 space-y-3">
          {filteredCases.map((item) => {
            const isSelected = selectedCase?.id === item.id;
            return (
              <div
                key={item.id}
                onClick={() => setSelectedCase(item)}
                className={`p-4 rounded-2xl border transition-all cursor-pointer ${
                  isSelected
                    ? 'bg-blue-50/50 border-blue-600 ring-1 ring-blue-600/30 shadow-xs'
                    : 'apple-bento-card hover:border-slate-300'
                }`}
              >
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-1.5">
                    <span className="text-base">{item.countryFlag}</span>
                    <span className="text-xs font-bold text-slate-900">{item.countryName}</span>
                    <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-slate-100 text-slate-600 font-semibold">
                      {item.code}
                    </span>
                  </div>
                  <span className="text-[11px] text-slate-400 font-medium">
                    {item.stage}
                  </span>
                </div>

                <h3 className="text-xs font-bold text-slate-800 line-clamp-2 leading-relaxed mb-2">
                  {item.title}
                </h3>

                <p className="text-[11px] text-slate-500 line-clamp-2 leading-normal">
                  {item.summary}
                </p>

                <div className="flex flex-wrap gap-1 mt-3">
                  {item.archetypes.map((arch) => (
                    <span
                      key={arch}
                      className="text-[10px] px-2 py-0.5 rounded-full bg-slate-50 border border-slate-200/80 text-slate-600 font-mono"
                    >
                      {arch}
                    </span>
                  ))}
                </div>

                <div className="flex items-center justify-between gap-2 pt-2.5 border-t border-slate-100 mt-3">
                  <button
                    type="button"
                    onClick={(e) => {
                      e.stopPropagation();
                      handleOpenPlaybook(item);
                    }}
                    className="text-[11px] font-semibold text-blue-600 hover:text-blue-800 flex items-center gap-1 cursor-pointer"
                  >
                    <span>合规指引精读</span>
                    <ArrowRight className="w-3 h-3" />
                  </button>
                  <button
                    type="button"
                    onClick={(e) => {
                      e.stopPropagation();
                      handleSimulateCase(item);
                    }}
                    className="text-[11px] font-semibold text-slate-700 hover:text-slate-900 bg-slate-100 hover:bg-slate-200 px-2.5 py-1 rounded-lg flex items-center gap-1 cursor-pointer"
                  >
                    <Play className="w-2.5 h-2.5 fill-current text-slate-800" />
                    <span>以此建案</span>
                  </button>
                </div>
              </div>
            );
          })}
        </div>

        {/* 右侧：五维合规复盘卡详情 (8 cols) */}
        {loading && !selectedCase ? (
          <div className="lg:col-span-8 apple-bento-card p-12 flex flex-col items-center justify-center space-y-3 min-h-[380px]">
            <Loader2 className="w-8 h-8 text-blue-600 animate-spin" />
            <p className="text-xs text-slate-500 font-medium">正在载入案例复盘数据...</p>
          </div>
        ) : selectedCase ? (
        <div className="lg:col-span-8 apple-bento-card p-6 space-y-6">
          {/* 复盘卡头 */}
          <div className="border-b border-slate-100 pb-4 flex flex-col md:flex-row md:items-center justify-between gap-3">
            <div>
              <div className="flex items-center gap-2">
                <span className="text-lg">{selectedCase.countryFlag}</span>
                <h3 className="text-sm font-bold text-slate-900">
                  {selectedCase.code} · {selectedCase.title}
                </h3>
              </div>
              <p className="text-xs text-slate-500 mt-1">
                适用法域：{selectedCase.countryName} ({selectedCase.jurisdiction}) · 阶段：{selectedCase.stage}
              </p>
            </div>

            <div className="flex items-center gap-2 shrink-0">
              <button
                onClick={() => handleOpenPlaybook(selectedCase)}
                className="px-3 py-2 bg-slate-100 hover:bg-slate-200 text-slate-800 rounded-xl text-xs font-semibold transition-colors flex items-center gap-1.5 cursor-pointer"
              >
                <Layers className="w-3.5 h-3.5 text-blue-600" />
                <span>国别指引</span>
              </button>
              <button
                onClick={() => handleSimulateCase(selectedCase)}
                className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-xl text-xs font-semibold flex items-center gap-1.5 cursor-pointer shadow-xs shadow-blue-500/25 active:scale-[0.98] transition-all"
              >
                <Play className="w-3.5 h-3.5 fill-current text-white" />
                <span>以此案例立项研判</span>
              </button>
            </div>
          </div>

          {/* 维度 1: 交易架构与案情还原 */}
          <div className="space-y-3">
            <div className="flex items-center gap-2">
              <span className="w-1.5 h-1.5 rounded-full bg-slate-400" />
              <h4 className="text-xs font-bold text-slate-900 tracking-wider">
                维度 1 · 交易架构与案情还原
              </h4>
            </div>
            <div className="p-4 rounded-xl bg-slate-50/80 border border-slate-200/70 space-y-3">
              <p className="text-xs text-slate-700 leading-relaxed font-medium">
                {selectedCase.dimension1_structure.dealSummary}
              </p>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-2 text-xs">
                {selectedCase.dimension1_structure.parties.map((p, idx) => (
                  <div key={idx} className="p-2.5 rounded-lg bg-white border border-slate-200/80">
                    <span className="text-[10px] text-slate-400 block font-medium">{p.role}</span>
                    <span className="text-xs font-bold text-slate-800 line-clamp-2 mt-0.5">{p.name}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* 维度 2: 暴雷根因诊断 */}
          <div className="space-y-3">
            <div className="flex items-center gap-2">
              <span className="w-1.5 h-1.5 rounded-full bg-rose-500" />
              <h4 className="text-xs font-bold text-slate-900 tracking-wider">
                维度 2 · 争议根因与合同缺陷诊断
              </h4>
            </div>
            <div className="p-4 rounded-xl bg-rose-50/40 border border-rose-200/70 space-y-2">
              <div className="text-xs font-bold text-rose-900">
                核心业务漏洞：{selectedCase.dimension2_rootCause.coreDiagnosis}
              </div>
              <div className="text-xs text-slate-600">
                合同条款缺陷：{selectedCase.dimension2_rootCause.contractPitfall}
              </div>
              <div className="mt-2 space-y-1">
                {selectedCase.dimension2_rootCause.triggerFactors.map((f, idx) => (
                  <div key={idx} className="text-xs text-slate-700 flex items-start gap-1.5">
                    <AlertTriangle className="w-3.5 h-3.5 text-amber-500 shrink-0 mt-0.5" />
                    <span>{f}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* 维度 3: 核心裁判规则与法源锚点 */}
          <div className="space-y-3">
            <div className="flex items-center gap-2">
              <span className="w-1.5 h-1.5 rounded-full bg-blue-600" />
              <h4 className="text-xs font-bold text-slate-900 tracking-wider">
                维度 3 · 裁判规则与法源依据
              </h4>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
              {selectedCase.dimension3_legalAnchors.map((anchor, idx) => (
                <div key={idx} className="p-3 rounded-xl bg-slate-50/80 border border-slate-200/80 space-y-1.5">
                  <span className="text-[10px] font-mono font-bold text-blue-700 bg-blue-50 px-1.5 py-0.5 rounded border border-blue-200/60">
                    {anchor.normId}
                  </span>
                  <div className="text-xs font-bold text-slate-900 mt-1">{anchor.nameZh}</div>
                  <p className="text-[11px] text-slate-500 line-clamp-2 italic">
                    "{anchor.statuteSnippet}"
                  </p>
                  <p className="text-[11px] text-slate-700 font-medium">
                    {anchor.keyRule}
                  </p>
                </div>
              ))}
            </div>
          </div>

          {/* 维度 4: 央国企合规启示与示范反制条款 */}
          <div className="space-y-3">
            <div className="flex items-center gap-2">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-600" />
              <h4 className="text-xs font-bold text-slate-900 tracking-wider">
                维度 4 · 合规防范建议与示范条款
              </h4>
            </div>
            <div className="space-y-3">
              {selectedCase.dimension4_modelClauses.map((clause, idx) => (
                <div key={idx} className="p-4 rounded-xl bg-slate-50/80 border border-slate-200/80 space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-bold text-slate-900">{clause.title}</span>
                    <button
                      onClick={() => handleCopyClause(clause.enClause, `${selectedCase.id}-${idx}`)}
                      className="px-2.5 py-1 rounded-lg text-[11px] bg-white border border-slate-200 hover:bg-slate-100 transition-colors flex items-center gap-1 cursor-pointer font-medium text-slate-700"
                    >
                      {copiedId === `${selectedCase.id}-${idx}` ? (
                        <>
                          <Check className="w-3 h-3 text-emerald-600" />
                          <span className="text-emerald-600">已复制</span>
                        </>
                      ) : (
                        <>
                          <Copy className="w-3 h-3 text-slate-500" />
                          <span>复制英文条款</span>
                        </>
                      )}
                    </button>
                  </div>
                  <div className="p-3 rounded-lg bg-white border border-slate-200/80 font-mono text-[11px] text-slate-700 leading-relaxed select-all">
                    {clause.enClause}
                  </div>
                  <p className="text-xs text-slate-600 font-medium leading-relaxed">
                    【实务要旨】{clause.zhExplanation}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </div>
        ) : null}
      </div>
    </div>
  );
};
