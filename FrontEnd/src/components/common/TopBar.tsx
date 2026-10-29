import React, { useState, useRef, useEffect } from 'react';
import { useApp } from '../../context/AppContext';
import {
  ChevronDown,
  PanelLeft,
  GitBranch,
  Bot,
  BookOpen,
  Compass,
  Download,
  Check,
  Gavel,
  ShieldCheck,
  Landmark,
  Loader2,
} from 'lucide-react';

interface TopBarProps {
  collapsed?: boolean;
  onToggleCollapse?: () => void;
}

export const TopBar: React.FC<TopBarProps> = ({ collapsed, onToggleCollapse }) => {
  const {
    currentView,
    setCurrentView,
    currentCase,
    currentCaseId,
    casesList,
    loadCase,
    switchingCaseId,
    isRightDockOpen,
    openRightDock,
    closeRightDock,
    openCaseEntryModal,
    showToast,
    refreshCurrentCase,
  } = useApp();

  const [caseMenuOpen, setCaseMenuOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

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
  const isHome = currentView === 'home';
  const isPreInv = currentCase?.meta?.lifecycle_stage === 'pre_investment';

  const handleExportDocx = () => {
    if (!currentCaseId) return;
    const url = `/api/cases/${currentCaseId}/export/docx`;
    window.open(url, '_blank');
    showToast('正在导出最高法院标准查明意见书 (.docx)...', 'info');
  };

  // 工具箱模式下的视图标题
  const toolTitles: Record<string, string> = {
    home: '工作台总览',
    verification: '涉外合同合规审查',
    search: '东盟法规与裁判库',
    consults: '属地法律顾问库',
    compliance: '合规审查与法域比选',
    cases: '专案档案库',
  };

  return (
    <header className="h-14 bg-white/80 backdrop-blur-xl border-b border-slate-200/80 px-4 flex items-center justify-between sticky top-0 z-20 shadow-xs">
      {/* ========================================================================= */}
      {/* 形态 A：专案研判舱 (analysis) */}
      {/* ========================================================================= */}
      {isCaseCockpit ? (
        <>
          {/* 左侧：案卷选择器 + 母子血缘 (边栏已有折叠控件，顶栏去除重复) */}
          <div className="flex items-center gap-2.5 min-w-0 shrink-0" ref={dropdownRef}>
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
                  {casesList.map((c) => {
                    const isSwitching = switchingCaseId === c.case_id;
                    const isActive = c.case_id === currentCaseId;
                    return (
                      <button
                        key={c.case_id}
                        onClick={() => {
                          if (c.case_id !== currentCaseId || currentView !== 'analysis') {
                            loadCase(c.case_id);
                            setCurrentView('analysis');
                          }
                          setCaseMenuOpen(false);
                        }}
                        className={`w-full text-left px-2.5 py-2 rounded-lg text-xs flex items-center justify-between transition-colors cursor-pointer ${
                          isActive
                            ? 'bg-blue-50 text-blue-900 font-semibold'
                            : 'text-slate-700 hover:bg-slate-50'
                        }`}
                      >
                        <div className="min-w-0 truncate">
                          <span className="font-mono text-blue-600 font-semibold mr-1.5">{c.case_id}</span>
                          <span>{c.title}</span>
                        </div>
                        {isSwitching ? (
                          <Loader2 className="w-3.5 h-3.5 animate-spin text-blue-600 shrink-0" />
                        ) : isActive ? (
                          <Check className="w-3.5 h-3.5 text-blue-600 shrink-0" />
                        ) : null}
                      </button>
                    );
                  })}
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
          </div>

          {/* 中央：案卷阶段只读徽标 (案卷类型强隔离：投前合规审查卷 vs 工程履约争议卷) */}
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-slate-100/90 border border-slate-200/80 shadow-2xs backdrop-blur-md select-none">
            {isPreInv ? (
              <>
                <span className="w-1.5 h-1.5 rounded-full bg-indigo-600 animate-pulse" />
                <ShieldCheck className="w-3.5 h-3.5 text-indigo-600" />
                <span className="text-xs font-semibold text-slate-800">
                  投前准入与合规审查卷
                </span>
                <span className="text-[10px] font-mono text-indigo-700 bg-indigo-50 border border-indigo-200/60 px-1.5 py-0.2 rounded-md">
                  投前阶段
                </span>
              </>
            ) : (
              <>
                <span className="w-1.5 h-1.5 rounded-full bg-purple-600 animate-pulse" />
                <Gavel className="w-3.5 h-3.5 text-purple-600" />
                <span className="text-xs font-semibold text-slate-800">
                  工程履约与索赔争议卷
                </span>
                <span className="text-[10px] font-mono text-purple-700 bg-purple-50 border border-purple-200/60 px-1.5 py-0.2 rounded-md">
                  履约阶段
                </span>
              </>
            )}
          </div>

          {/* 右侧：导出公文 + 统一法律辅助面板开关 (去除与右侧栏头部重复的三组切换控件) */}
          <div className="flex items-center gap-2 shrink-0">
            <button
              onClick={handleExportDocx}
              className="p-1.5 px-3 rounded-xl bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold flex items-center gap-1.5 cursor-pointer shadow-xs shadow-blue-500/25 active:scale-[0.98] transition-all"
            >
              <Download className="w-3.5 h-3.5" />
              <span>导出意见书 (.docx)</span>
            </button>

            <button
              type="button"
              onClick={() => (isRightDockOpen ? closeRightDock() : openRightDock('case_copilot'))}
              className={`p-1.5 px-3 rounded-xl border text-xs font-semibold flex items-center gap-1.5 transition-all cursor-pointer ${
                isRightDockOpen
                  ? 'bg-blue-50 border-blue-200 text-blue-700 shadow-xs'
                  : 'border-slate-200/80 bg-slate-50 hover:bg-slate-100 text-slate-700'
              }`}
              title={isRightDockOpen ? "收起法律辅助面板" : "展开 AI 法律助手"}
            >
              <Bot className="w-3.5 h-3.5 text-blue-600" />
              <span>AI 法律助手</span>
            </button>
          </div>
        </>
      ) : isHome ? (
        /* ========================================================================= */
        /* 形态 B：工作台总览模式 (Home Overview) */
        /* ========================================================================= */
        <>
          {/* 左侧：标题与状态指示 */}
          <div className="flex items-center gap-2.5 min-w-0 shrink-0">
            <div className="flex items-center gap-2">
              <div className="w-7 h-7 rounded-lg bg-blue-50 border border-blue-200/60 flex items-center justify-center text-blue-600 shadow-2xs">
                <Landmark className="w-3.5 h-3.5" />
              </div>
              <div className="flex items-center gap-1.5">
                <span className="text-xs font-bold text-slate-900 tracking-tight">工作台总览</span>
                <span className="text-[10px] text-slate-400 font-mono hidden sm:inline">/ Overview</span>
              </div>
            </div>
          </div>

          {/* 右侧：仅保留 AI 法律助手，彻底去除与边栏重复的新建案卷、专案研判及检索框 */}
          <div className="flex items-center gap-2 shrink-0">
            <button
              type="button"
              onClick={() => (isRightDockOpen ? closeRightDock() : openRightDock('case_copilot'))}
              className={`p-1.5 px-3 rounded-xl border text-xs font-semibold flex items-center gap-1.5 transition-all cursor-pointer ${
                isRightDockOpen
                  ? 'bg-blue-50 border-blue-200 text-blue-700 shadow-xs'
                  : 'border-slate-200/80 bg-white hover:bg-slate-50 text-slate-700 shadow-2xs'
              }`}
              title={isRightDockOpen ? "收起法律辅助面板" : "展开 AI 法律助手"}
            >
              <Bot className="w-3.5 h-3.5 text-blue-600" />
              <span>AI 法律助手</span>
            </button>
          </div>
        </>
      ) : (
        /* ========================================================================= */
        /* 形态 C：独立公共实务工具箱模式 */
        /* ========================================================================= */
        <>
          <div className="flex items-center gap-2.5 min-w-0 shrink-0">
            <div className="flex items-center gap-2">
              <span className="text-xs font-bold text-slate-800">
                {toolTitles[currentView] || '实务工具箱'}
              </span>
            </div>
          </div>

          <div className="flex items-center gap-2 shrink-0">
            <span className="text-xs text-slate-400">当前案卷：</span>
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
                  {casesList.map((c) => {
                    const isSwitching = switchingCaseId === c.case_id;
                    const isActive = c.case_id === currentCaseId;
                    return (
                      <button
                        key={c.case_id}
                        onClick={() => {
                          if (c.case_id !== currentCaseId || currentView !== 'analysis') {
                            loadCase(c.case_id);
                            setCurrentView('analysis');
                          }
                          setCaseMenuOpen(false);
                        }}
                        className={`w-full text-left px-2.5 py-2 rounded-lg text-xs flex items-center justify-between transition-colors cursor-pointer ${
                          isActive
                            ? 'bg-blue-50 text-blue-900 font-semibold'
                            : 'text-slate-700 hover:bg-slate-50'
                        }`}
                      >
                        <div className="min-w-0 truncate">
                          <span className="font-mono text-blue-600 font-semibold mr-1.5">{c.case_id}</span>
                          <span>{c.title}</span>
                        </div>
                        {isSwitching ? (
                          <Loader2 className="w-3.5 h-3.5 animate-spin text-blue-600 shrink-0" />
                        ) : isActive ? (
                          <Check className="w-3.5 h-3.5 text-blue-600 shrink-0" />
                        ) : null}
                      </button>
                    );
                  })}
                </div>
              )}
            </div>

            <button
              onClick={() => (isRightDockOpen ? closeRightDock() : openRightDock('country_playbook'))}
              className={`p-1.5 px-3 rounded-xl border text-xs font-semibold flex items-center gap-1.5 transition-all cursor-pointer ${
                isRightDockOpen
                  ? 'bg-blue-50 border-blue-200 text-blue-700 shadow-xs'
                  : 'border-slate-200 bg-slate-50 hover:bg-slate-100 text-slate-700'
              }`}
              title={isRightDockOpen ? "收起法律辅助面板" : "查阅东道国合规指引"}
            >
              <Compass className="w-3.5 h-3.5 text-amber-600" />
              <span>合规指引</span>
            </button>
          </div>
        </>
      )}
    </header>
  );
};
