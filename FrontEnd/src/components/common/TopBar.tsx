import React, { useState, useRef, useEffect } from 'react';
import { useApp } from '../../context/AppContext';
import { lawAgentApi } from '../../api/lawAgentApi';
import {
  ChevronDown,
  GitBranch,
  ShieldAlert,
  Bot,
  BookOpen,
  Compass,
  Download,
  Check,
  FolderOpen,
  Wrench,
  Sparkles,
} from 'lucide-react';

interface TopBarProps {
  collapsed?: boolean;
  onToggleCollapse?: () => void;
}

export const TopBar: React.FC<TopBarProps> = () => {
  const {
    currentView,
    currentCase,
    currentCaseId,
    casesList,
    loadCase,
    openRightDock,
    showToast,
    refreshCurrentCase,
  } = useApp();

  const [caseMenuOpen, setCaseMenuOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);
  const [transitioning, setTransitioning] = useState(false);

  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target as Node)) {
        setCaseMenuOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const isCaseCockpit = currentView === 'analysis';
  const isPreInv = currentCase?.meta?.lifecycle_stage === 'pre_investment';

  const hostJur = currentCase?.meta?.jurisdiction || 'asean_id';
  const govLaw = currentCase?.meta?.choice_of_law || currentCase?.meta?.governing_law_jurisdiction || hostJur;
  const hasLexLociConflict = hostJur !== govLaw;

  // 阶段流转切换
  const handleToggleStage = async () => {
    if (!currentCaseId || transitioning) return;
    const targetStage = isPreInv ? 'execution_dispute' : 'pre_investment';
    setTransitioning(true);
    try {
      await lawAgentApi.transitionStage(currentCaseId, {
        target_stage: targetStage,
        inherit_params: true,
      });
      showToast(
        `✓ 案卷已成功切换至【${targetStage === 'pre_investment' ? '投前准入审查模式' : '履约索赔争议模式'}】`,
        'success'
      );
      await refreshCurrentCase();
    } catch (e: any) {
      showToast(e.message || '阶段切换失败', 'error');
    } finally {
      setTransitioning(false);
    }
  };

  const handleExportDocx = () => {
    if (!currentCaseId) return;
    const url = `/api/cases/${currentCaseId}/export/docx`;
    window.open(url, '_blank');
    showToast('正在导出最高法院标准查明意见书 (.docx)...', 'info');
  };

  // 工具箱模式下的视图标题
  const toolTitles: Record<string, string> = {
    verification: '涉外合同强行法红线 & 外律意见书扫描核验仪',
    search: '东盟六国法典与 FIDIC 国际工程判例搜索引擎',
    consults: '东盟 Local Counsel 专家会商与利益冲突避冲库',
    compliance: '五阶段合规健康度体检 & 六国横向比选中心',
    cases: '专案档案库与历史查明卷宗',
    workspace: 'AI 协同推演工作区',
    review: '法律意见书呈报端',
    dashboard: '防线门禁指标仪表板',
  };

  return (
    <header className="h-14 bg-white/80 backdrop-blur-xl border-b border-slate-200/80 px-4 flex items-center justify-between sticky top-0 z-20 shadow-xs">
      {/* ========================================================================= */}
      {/* 形态 A：专案研判舱 (analysis) */}
      {/* ========================================================================= */}
      {isCaseCockpit ? (
        <>
          {/* 左侧：案卷选择器 + 母子血缘 + 准据法冲突穿透胶囊 */}
          <div className="flex items-center gap-2 min-w-0" ref={dropdownRef}>
            <div className="relative">
              <button
                onClick={() => setCaseMenuOpen(!caseMenuOpen)}
                className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-xl bg-slate-100/90 hover:bg-slate-200/80 text-xs font-semibold text-slate-800 transition-colors cursor-pointer border border-slate-200/70"
              >
                <span className="font-mono text-blue-600">{currentCaseId || 'C101'}</span>
                <span className="truncate max-w-[150px]">{currentCase?.title || '案卷研判中'}</span>
                <ChevronDown className="w-3.5 h-3.5 text-slate-400" />
              </button>

              {caseMenuOpen && (
                <div className="absolute left-0 top-full mt-1.5 w-64 bg-white rounded-xl shadow-xl border border-slate-200 p-1.5 z-50 space-y-0.5 max-h-72 overflow-y-auto apple-modal-card">
                  {casesList.map((c) => (
                    <button
                      key={c.case_id}
                      onClick={() => {
                        loadCase(c.case_id);
                        setCaseMenuOpen(false);
                      }}
                      className={`w-full text-left px-2.5 py-2 rounded-lg text-xs flex items-center justify-between transition-colors cursor-pointer ${
                        c.case_id === currentCaseId
                          ? 'bg-blue-50 text-blue-900 font-semibold'
                          : 'text-slate-700 hover:bg-slate-50'
                      }`}
                    >
                      <div className="min-w-0 truncate">
                        <span className="font-mono text-blue-600 font-semibold mr-1.5">{c.case_id}</span>
                        <span>{c.title}</span>
                      </div>
                      {c.case_id === currentCaseId && <Check className="w-3.5 h-3.5 text-blue-600 shrink-0" />}
                    </button>
                  ))}
                </div>
              )}
            </div>

            {/* 母子案卷血缘胶囊 */}
            {currentCase?.meta?.parent_case_id && (
              <span className="hidden xl:inline-flex items-center gap-1 px-2 py-0.5 rounded-md bg-slate-100 text-slate-600 font-mono text-[11px] border border-slate-200">
                <GitBranch className="w-3 h-3 text-slate-400" />
                <span>{currentCase.meta.parent_case_id} ➔ {currentCaseId}</span>
              </span>
            )}

            {/* 准据法脱钩冲突穿透警示 (Lex Loci Solutionis Override) */}
            {hasLexLociConflict && (
              <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-lg bg-amber-50 text-amber-800 text-[11px] font-medium border border-amber-200/80 shadow-2xs">
                <ShieldAlert className="w-3.5 h-3.5 text-amber-600" />
                <span>准据法脱钩穿透 (Lex Loci)</span>
              </span>
            )}
          </div>

          {/* 中央：灵动岛式生命周期模式分段控制器 */}
          <div className="apple-segmented-control text-xs">
            <button
              onClick={() => isPreInv && handleToggleStage()}
              disabled={transitioning}
              className={`px-3 py-1 rounded-lg flex items-center gap-1.5 transition-all cursor-pointer ${
                !isPreInv
                  ? 'apple-segmented-item-active text-slate-900 font-semibold'
                  : 'text-slate-500 hover:text-slate-800'
              }`}
            >
              <span className="w-1.5 h-1.5 rounded-full bg-amber-500" />
              <span>履约争议模式</span>
            </button>
            <button
              onClick={() => !isPreInv && handleToggleStage()}
              disabled={transitioning}
              className={`px-3 py-1 rounded-lg flex items-center gap-1.5 transition-all cursor-pointer ${
                isPreInv
                  ? 'apple-segmented-item-active text-slate-900 font-semibold'
                  : 'text-slate-500 hover:text-slate-800'
              }`}
            >
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
              <span>投前准入模式</span>
            </button>
          </div>

          {/* 右侧：副驾坞模态触发按钮组 + 导出公文 */}
          <div className="flex items-center gap-1.5">
            <button
              onClick={() => openRightDock('case_copilot')}
              className="p-1.5 px-2.5 rounded-xl border border-slate-200/80 bg-slate-50 hover:bg-slate-100 text-slate-700 text-xs font-medium flex items-center gap-1.5 transition-colors cursor-pointer"
              title="呼出案卷 AI 副驾"
            >
              <Bot className="w-3.5 h-3.5 text-emerald-600" />
              <span className="hidden sm:inline">AI 副驾</span>
            </button>

            <button
              onClick={() => openRightDock('law_reader')}
              className="p-1.5 px-2.5 rounded-xl border border-slate-200/80 bg-slate-50 hover:bg-slate-100 text-slate-700 text-xs font-medium flex items-center gap-1.5 transition-colors cursor-pointer"
              title="查看权威法源正本 (B)"
            >
              <BookOpen className="w-3.5 h-3.5 text-blue-600" />
              <span className="hidden sm:inline">法源 (B)</span>
            </button>

            <button
              onClick={() => openRightDock('country_playbook')}
              className="p-1.5 px-2.5 rounded-xl border border-slate-200/80 bg-slate-50 hover:bg-slate-100 text-slate-700 text-xs font-medium flex items-center gap-1.5 transition-colors cursor-pointer"
              title="属地合规排雷指南"
            >
              <Compass className="w-3.5 h-3.5 text-amber-600" />
              <span className="hidden sm:inline">排雷指南</span>
            </button>

            <button
              onClick={handleExportDocx}
              className="p-1.5 px-3 rounded-xl btn-space-titanium text-white text-xs font-semibold flex items-center gap-1.5 cursor-pointer shadow-sm ml-1"
            >
              <Download className="w-3.5 h-3.5" />
              <span>导出意见书 (.docx)</span>
            </button>
          </div>
        </>
      ) : (
        /* ========================================================================= */
        /* 形态 B：独立公共工具箱模式 */
        /* ========================================================================= */
        <>
          <div className="flex items-center gap-3">
            <span className="px-2.5 py-1 rounded-lg bg-slate-900 text-white text-[11px] font-semibold flex items-center gap-1.5 shadow-2xs">
              <Wrench className="w-3 h-3 text-slate-300" />
              独立实务工具模式 · 操作不改动现有案卷
            </span>
            <span className="text-xs font-bold text-slate-800">
              {toolTitles[currentView] || '实务工具箱'}
            </span>
          </div>

          <div className="flex items-center gap-2">
            <span className="text-xs text-slate-400">挂载目标案卷：</span>
            <div className="relative" ref={dropdownRef}>
              <button
                onClick={() => setCaseMenuOpen(!caseMenuOpen)}
                className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-xl bg-slate-100 hover:bg-slate-200/80 text-xs font-semibold text-slate-800 transition-colors cursor-pointer border border-slate-200"
              >
                <span className="font-mono text-blue-600">{currentCaseId || 'C101'}</span>
                <span className="truncate max-w-[140px]">{currentCase?.title || '示范案卷'}</span>
                <ChevronDown className="w-3.5 h-3.5 text-slate-400" />
              </button>

              {caseMenuOpen && (
                <div className="absolute right-0 top-full mt-1.5 w-64 bg-white rounded-xl shadow-xl border border-slate-200 p-1.5 z-50 space-y-0.5 max-h-72 overflow-y-auto apple-modal-card">
                  {casesList.map((c) => (
                    <button
                      key={c.case_id}
                      onClick={() => {
                        loadCase(c.case_id);
                        setCaseMenuOpen(false);
                      }}
                      className={`w-full text-left px-2.5 py-2 rounded-lg text-xs flex items-center justify-between transition-colors cursor-pointer ${
                        c.case_id === currentCaseId
                          ? 'bg-blue-50 text-blue-900 font-semibold'
                          : 'text-slate-700 hover:bg-slate-50'
                      }`}
                    >
                      <div className="min-w-0 truncate">
                        <span className="font-mono text-blue-600 font-semibold mr-1.5">{c.case_id}</span>
                        <span>{c.title}</span>
                      </div>
                      {c.case_id === currentCaseId && <Check className="w-3.5 h-3.5 text-blue-600 shrink-0" />}
                    </button>
                  ))}
                </div>
              )}
            </div>

            <button
              onClick={() => openRightDock('country_playbook')}
              className="p-1.5 px-2.5 rounded-xl border border-slate-200 bg-slate-50 hover:bg-slate-100 text-slate-700 text-xs font-medium flex items-center gap-1.5 transition-colors cursor-pointer"
            >
              <Compass className="w-3.5 h-3.5 text-amber-600" />
              <span>属地排雷</span>
            </button>
          </div>
        </>
      )}
    </header>
  );
};
