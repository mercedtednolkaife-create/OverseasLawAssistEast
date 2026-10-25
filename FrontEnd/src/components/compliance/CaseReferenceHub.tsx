import React, { useState, useEffect } from 'react';
import { useApp } from '../../context/AppContext';
import { lawAgentApi } from '../../api/lawAgentApi';
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
  const [cases, setCases] = useState<Case5DItem[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [selectedCase, setSelectedCase] = useState<Case5DItem | null>(null);
  const [filterJur, setFilterJur] = useState<string>('all');
  const [copiedId, setCopiedId] = useState<string | null>(null);

  useEffect(() => {
    let mounted = true;
    lawAgentApi
      .getReferenceCases()
      .then((data) => {
        if (mounted && Array.isArray(data) && data.length > 0) {
          setCases(data as Case5DItem[]);
          setSelectedCase(data[0] as Case5DItem);
        }
      })
      .catch((err) => {
        console.error('Failed to load reference cases:', err);
      })
      .finally(() => {
        if (mounted) setLoading(false);
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
    showToast(`已在右侧副驾坞展开【${item.countryName}】属地排雷与 5D 复盘手册`, 'info');
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
    <div className="space-y-6">
      {/* 顶部标题与筛选 */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-white p-5 rounded-2xl border border-zinc-200/80 shadow-xs">
        <div>
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-blue-600" />
            <h2 className="text-base font-bold text-zinc-900">
              中资出海基建典型参考案例库 (5D Case Review Cards)
            </h2>
          </div>
          <p className="text-xs text-zinc-500 mt-1">
            独创五维合规复盘卡：交易架构 ➔ 暴雷根因 ➔ 核心法源 ➔ 示范反制条款 ➔ 一键沙盘推演
          </p>
        </div>

        {/* 国别快速过滤 */}
        <div className="flex items-center gap-1.5 overflow-x-auto pb-1 text-xs">
          <button
            onClick={() => setFilterJur('all')}
            className={`px-3 py-1.5 rounded-lg font-medium transition-colors cursor-pointer ${
              filterJur === 'all'
                ? 'bg-zinc-900 text-white shadow-xs'
                : 'bg-zinc-100 text-zinc-600 hover:bg-zinc-200/70'
            }`}
          >
            全部标杆案
          </button>
          {[
            { id: 'asean_id', name: '印尼' },
            { id: 'asean_vn', name: '越南' },
            { id: 'asean_my', name: '大马/新' },
            { id: 'asean_ph', name: '菲律宾' },
          ].map((item) => (
            <button
              key={item.id}
              onClick={() => setFilterJur(item.id)}
              className={`px-3 py-1.5 rounded-lg font-medium transition-colors cursor-pointer ${
                filterJur === item.id
                  ? 'bg-zinc-900 text-white shadow-xs'
                  : 'bg-zinc-100 text-zinc-600 hover:bg-zinc-200/70'
              }`}
            >
              {item.name}
            </button>
          ))}
        </div>
      </div>

      {/* 案例列表与 5D 复盘卡展示区 */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* 左侧：4大标杆案例选择卡 (4 cols) */}
        <div className="lg:col-span-4 space-y-3">
          {filteredCases.map((item) => {
            const isSelected = selectedCase?.id === item.id;
            return (
              <div
                key={item.id}
                onClick={() => setSelectedCase(item)}
                className={`p-4 rounded-xl border transition-all cursor-pointer ${
                  isSelected
                    ? 'bg-white border-blue-600 ring-1 ring-blue-600 shadow-sm'
                    : 'bg-white border-zinc-200/80 hover:border-zinc-300 hover:shadow-xs'
                }`}
              >
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-1.5">
                    <span className="text-base">{item.countryFlag}</span>
                    <span className="text-xs font-bold text-zinc-900">{item.countryName}</span>
                    <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-zinc-100 text-zinc-600 font-semibold">
                      {item.code}
                    </span>
                  </div>
                  <span className="text-[11px] text-zinc-400 font-medium">
                    {item.stage}
                  </span>
                </div>

                <h3 className="text-xs font-bold text-zinc-800 line-clamp-2 leading-relaxed mb-2">
                  {item.title}
                </h3>

                <p className="text-[11px] text-zinc-500 line-clamp-2 leading-normal">
                  {item.summary}
                </p>

                <div className="flex flex-wrap gap-1 mt-3">
                  {item.archetypes.map((arch) => (
                    <span
                      key={arch}
                      className="text-[10px] px-2 py-0.5 rounded-full bg-zinc-50 border border-zinc-200/60 text-zinc-600 font-mono"
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
                    <span>右侧副驾 5D 复盘</span>
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
        {loading ? (
          <div className="lg:col-span-8 bg-white rounded-2xl border border-zinc-200/80 p-12 shadow-xs flex flex-col items-center justify-center space-y-3 min-h-[400px]">
            <Loader2 className="w-8 h-8 text-blue-600 animate-spin" />
            <p className="text-xs text-zinc-500 font-medium">正在从东盟工程合规案库加载权威 5D 标杆案卷...</p>
          </div>
        ) : selectedCase ? (
        <div className="lg:col-span-8 bg-white rounded-2xl border border-zinc-200/80 p-6 shadow-xs space-y-6">
          {/* 复盘卡头 */}
          <div className="border-b border-zinc-100 pb-4 flex flex-col md:flex-row md:items-center justify-between gap-3">
            <div>
              <div className="flex items-center gap-2">
                <span className="text-lg">{selectedCase.countryFlag}</span>
                <h3 className="text-sm font-bold text-zinc-900">
                  {selectedCase.code} · {selectedCase.title}
                </h3>
              </div>
              <p className="text-xs text-zinc-500 mt-1">
                适用法域：{selectedCase.countryName} ({selectedCase.jurisdiction}) · 阶段：{selectedCase.stage}
              </p>
            </div>

            <div className="flex items-center gap-2 shrink-0">
              <button
                onClick={() => handleOpenPlaybook(selectedCase)}
                className="px-3 py-2 bg-slate-100 hover:bg-slate-200 text-slate-800 rounded-xl text-xs font-semibold transition-colors flex items-center gap-1.5 cursor-pointer"
              >
                <Layers className="w-3.5 h-3.5 text-blue-600" />
                <span>副驾精读</span>
              </button>
              <button
                onClick={() => handleSimulateCase(selectedCase)}
                className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-xl text-xs font-semibold flex items-center gap-1.5 cursor-pointer shadow-xs shadow-blue-500/25 active:scale-[0.98] transition-all"
              >
                <Play className="w-3.5 h-3.5 fill-current text-emerald-400" />
                <span>以此案为蓝本沙盘推演</span>
              </button>
            </div>
          </div>

          {/* 维度 1: 交易架构与案情还原 */}
          <div className="space-y-3">
            <div className="flex items-center gap-2">
              <span className="w-1.5 h-1.5 rounded-full bg-zinc-400" />
              <h4 className="text-xs font-bold text-zinc-900 uppercase tracking-wider">
                维度 1【交易架构与案情还原】
              </h4>
            </div>
            <div className="p-4 rounded-xl bg-zinc-50/70 border border-zinc-200/60 space-y-3">
              <p className="text-xs text-zinc-700 leading-relaxed font-medium">
                {selectedCase.dimension1_structure.dealSummary}
              </p>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-2 text-xs">
                {selectedCase.dimension1_structure.parties.map((p, idx) => (
                  <div key={idx} className="p-2.5 rounded-lg bg-white border border-zinc-200/60">
                    <span className="text-[10px] text-zinc-400 block font-medium">{p.role}</span>
                    <span className="text-xs font-bold text-zinc-800 line-clamp-2 mt-0.5">{p.name}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* 维度 2: 暴雷根因诊断 (Root Cause) */}
          <div className="space-y-3">
            <div className="flex items-center gap-2">
              <span className="w-1.5 h-1.5 rounded-full bg-red-500" />
              <h4 className="text-xs font-bold text-zinc-900 uppercase tracking-wider">
                维度 2【暴雷根因诊断 (Root Cause)】
              </h4>
            </div>
            <div className="p-4 rounded-xl bg-red-50/30 border border-red-200/60 space-y-2">
              <div className="text-xs font-bold text-red-900">
                核心业务漏洞：{selectedCase.dimension2_rootCause.coreDiagnosis}
              </div>
              <div className="text-xs text-zinc-600">
                合同条款缺陷：{selectedCase.dimension2_rootCause.contractPitfall}
              </div>
              <div className="mt-2 space-y-1">
                {selectedCase.dimension2_rootCause.triggerFactors.map((f, idx) => (
                  <div key={idx} className="text-xs text-zinc-700 flex items-start gap-1.5">
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
              <h4 className="text-xs font-bold text-zinc-900 uppercase tracking-wider">
                维度 3【核心裁判规则与法源锚点】
              </h4>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
              {selectedCase.dimension3_legalAnchors.map((anchor, idx) => (
                <div key={idx} className="p-3 rounded-xl bg-zinc-50 border border-zinc-200/70 space-y-1.5">
                  <span className="text-[10px] font-mono font-bold text-blue-700 bg-blue-50 px-1.5 py-0.5 rounded">
                    {anchor.normId}
                  </span>
                  <div className="text-xs font-bold text-zinc-900 mt-1">{anchor.nameZh}</div>
                  <p className="text-[11px] text-zinc-500 line-clamp-2 italic">
                    "{anchor.statuteSnippet}"
                  </p>
                  <p className="text-[11px] text-zinc-700 font-medium">
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
              <h4 className="text-xs font-bold text-zinc-900 uppercase tracking-wider">
                维度 4【央国企合规启示与示范反制条款 (Model Counter-Clause)】
              </h4>
            </div>
            <div className="space-y-3">
              {selectedCase.dimension4_modelClauses.map((clause, idx) => (
                <div key={idx} className="p-4 rounded-xl bg-zinc-50 border border-zinc-200/80 space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-bold text-zinc-900">{clause.title}</span>
                    <button
                      onClick={() => handleCopyClause(clause.enClause, `${selectedCase.id}-${idx}`)}
                      className="px-2 py-1 rounded text-[11px] bg-white border border-zinc-200 hover:bg-zinc-100 transition-colors flex items-center gap-1 cursor-pointer font-medium"
                    >
                      {copiedId === `${selectedCase.id}-${idx}` ? (
                        <>
                          <Check className="w-3 h-3 text-emerald-600" />
                          <span className="text-emerald-600">已复制</span>
                        </>
                      ) : (
                        <>
                          <Copy className="w-3 h-3 text-zinc-500" />
                          <span>复制英文条文</span>
                        </>
                      )}
                    </button>
                  </div>
                  <div className="p-2.5 rounded-lg bg-white border border-zinc-200/60 font-mono text-[11px] text-zinc-700 leading-relaxed select-all">
                    {clause.enClause}
                  </div>
                  <p className="text-xs text-zinc-600 font-medium leading-relaxed">
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
