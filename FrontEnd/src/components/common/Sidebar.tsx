import React from 'react';
import { useApp, ActiveView } from '../../context/AppContext';
import {
  Layers,
  Compass,
  FileCheck2,
  Scale,
  Users,
  Sliders,
  Plus,
  PanelLeftClose,
  PanelLeft,
  Search,
  Command,
  GitBranch,
  FolderArchive,
  ShieldCheck,
} from 'lucide-react';

interface SidebarProps {
  collapsed: boolean;
  onToggleCollapse: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ collapsed, onToggleCollapse }) => {
  const {
    currentView,
    setCurrentView,
    currentCaseId,
    casesList,
    loadCase,
    openCaseEntryModal,
    openCommandPalette,
  } = useApp();

  return (
    <aside
      className={`h-[calc(100vh-1.5rem)] sticky top-3 my-3 ml-3 rounded-[24px] apple-sidebar-panel flex flex-col justify-between transition-[width] duration-250 ease-in-out z-30 select-none overflow-x-hidden ${
        collapsed ? 'w-16' : 'w-[240px]'
      }`}
    >
      {/* 顶部区域：Logo、折叠与快速命令 */}
      <div className="p-3 space-y-2.5">
        {/* 标题与折叠按钮 */}
        {collapsed ? (
          <div className="flex flex-col items-center justify-center py-0.5">
            <button
              type="button"
              onClick={onToggleCollapse}
              title="展开侧边栏"
              className="w-10 h-10 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 flex items-center justify-center transition-all cursor-pointer"
            >
              <PanelLeft className="w-4 h-4" />
            </button>
          </div>
        ) : (
          <div className="flex items-center justify-between px-1 py-0.5">
            <div
              onClick={() => setCurrentView('home')}
              className="flex items-center gap-2 cursor-pointer group min-w-0"
              title="返回工作台总览"
            >
              <div className="w-7 h-7 rounded-lg bg-slate-900 text-white flex items-center justify-center shrink-0 shadow-sm">
                <ShieldCheck className="w-4 h-4 text-white" />
              </div>
              <div className="min-w-0">
                <span className="text-xs font-bold text-slate-900 tracking-tight block truncate group-hover:text-blue-600 transition-colors">
                  域外法查明助手
                </span>
                <span className="text-[10px] text-slate-400 font-mono block -mt-0.5">
                  东盟基建 · 2026 现行版
                </span>
              </div>
            </div>

            <button
              type="button"
              onClick={onToggleCollapse}
              title="收起侧边栏"
              className="p-1 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-100 transition-colors cursor-pointer"
            >
              <PanelLeftClose className="w-4 h-4" />
            </button>
          </div>
        )}

        {/* 全局录入案卷主行动按钮 (深空钛金属材质) */}
        {!collapsed ? (
          <button
            onClick={openCaseEntryModal}
            className="w-full flex items-center justify-between px-3 py-2 text-xs font-semibold rounded-xl btn-space-titanium cursor-pointer shadow-sm"
          >
            <span className="flex items-center gap-1.5">
              <Plus className="w-3.5 h-3.5" />
              <span>录入新项目 / 争议案卷</span>
            </span>
            <kbd className="text-[9px] bg-slate-800 text-slate-300 px-1 py-0.2 rounded font-mono border border-slate-700">
              S0
            </kbd>
          </button>
        ) : (
          <button
            onClick={openCaseEntryModal}
            title="录入新项目 / 争议案卷"
            className="w-10 h-10 mx-auto flex items-center justify-center rounded-xl btn-space-titanium cursor-pointer shadow-sm"
          >
            <Plus className="w-4 h-4" />
          </button>
        )}

        {/* Cmd/Ctrl + K 全局搜索条入口 */}
        {!collapsed && (
          <button
            onClick={openCommandPalette}
            className="w-full flex items-center justify-between px-2.5 py-1.5 text-xs text-slate-400 bg-slate-100/70 hover:bg-slate-100 rounded-xl border border-slate-200/60 cursor-pointer transition-colors"
          >
            <span className="flex items-center gap-2">
              <Search className="w-3.5 h-3.5 text-slate-400" />
              <span className="text-[11px] text-slate-500">全局指令 / 搜法条...</span>
            </span>
            <kbd className="text-[10px] font-mono text-slate-400 bg-white px-1.5 py-0.2 rounded border border-slate-200">
              ⌘K
            </kbd>
          </button>
        )}
      </div>

      {/* 中部导航区：严格收敛为「三层业务漏斗」 */}
      <div className="flex-1 overflow-y-auto px-2 space-y-4 py-1">
        {/* ========================================================================= */}
        {/* 第一层：专案深度研判舱 (核心精力 80%) */}
        {/* ========================================================================= */}
        <div className="space-y-1">
          {!collapsed && (
            <div className="px-2 text-[10px] font-semibold text-slate-400 uppercase tracking-wider">
              专案深度研判 (80%)
            </div>
          )}

          {/* 1. 工作台总览 */}
          <button
            onClick={() => setCurrentView('home')}
            className={`w-full flex items-center gap-2.5 px-2.5 py-1.5 rounded-xl text-xs font-medium transition-all cursor-pointer ${
              currentView === 'home'
                ? 'bg-slate-900 text-white shadow-sm'
                : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'
            }`}
            title="工作台总览"
          >
            <Compass className={`w-4 h-4 ${currentView === 'home' ? 'text-white' : 'text-slate-500'}`} />
            {!collapsed && <span>工作台总览</span>}
          </button>

          {/* 2. 专案研判舱 */}
          <button
            onClick={() => setCurrentView('analysis')}
            className={`w-full flex items-center gap-2.5 px-2.5 py-1.5 rounded-xl text-xs font-medium transition-all cursor-pointer ${
              currentView === 'analysis'
                ? 'bg-slate-900 text-white shadow-sm'
                : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'
            }`}
            title="专案深度研判舱"
          >
            <Layers className={`w-4 h-4 ${currentView === 'analysis' ? 'text-white' : 'text-slate-500'}`} />
            {!collapsed && <span>专案深度研判舱</span>}
          </button>

          {/* 内嵌活跃案卷树状列表 */}
          {!collapsed && (
            <div className="pl-3 pr-1 pt-1 space-y-0.5 border-l border-slate-200/80 ml-4">
              {casesList.slice(0, 5).map((c) => {
                const isActive = currentCaseId === c.case_id;
                const isPreInv = c.lifecycle_stage === 'pre_investment';
                return (
                  <button
                    key={c.case_id}
                    onClick={() => {
                      loadCase(c.case_id);
                      setCurrentView('analysis');
                    }}
                    className={`w-full text-left px-2 py-1.5 rounded-lg text-xs flex items-center justify-between group transition-colors cursor-pointer ${
                      isActive
                        ? 'bg-blue-50/80 text-blue-900 font-semibold'
                        : 'text-slate-600 hover:bg-slate-100/70 hover:text-slate-900'
                    }`}
                  >
                    <div className="flex items-center gap-1.5 min-w-0">
                      <span
                        className={`w-1.5 h-1.5 rounded-full shrink-0 ${
                          isPreInv ? 'bg-emerald-500' : 'bg-amber-500'
                        }`}
                      />
                      <span className="font-mono text-[11px] text-slate-400 shrink-0">
                        {c.case_id}
                      </span>
                      <span className="truncate text-[11px]">{c.title}</span>
                    </div>
                    {c.parent_case_id && (
                      <GitBranch className="w-3 h-3 text-slate-400 shrink-0" title="派生子案" />
                    )}
                  </button>
                );
              })}
              <button
                onClick={() => setCurrentView('cases')}
                className="w-full text-left px-2 py-1 text-[11px] text-slate-400 hover:text-blue-600 flex items-center gap-1 cursor-pointer transition-colors"
              >
                <FolderArchive className="w-3 h-3" />
                <span>查看全部案卷档案库 ➔</span>
              </button>
            </div>
          )}
        </div>

        {/* ========================================================================= */}
        {/* 第二层：轻量化实务即用工具箱 (日常高频 15%) */}
        {/* ========================================================================= */}
        <div className="space-y-1 pt-1">
          {!collapsed && (
            <div className="px-2 text-[10px] font-semibold text-slate-400 uppercase tracking-wider flex items-center justify-between">
              <span>独立工具箱 (15%)</span>
              <span className="text-[9px] text-slate-400 font-normal">可挂载至案卷</span>
            </div>
          )}

          <button
            onClick={() => setCurrentView('verification')}
            className={`w-full flex items-center gap-2.5 px-2.5 py-1.5 rounded-xl text-xs font-medium transition-all cursor-pointer ${
              currentView === 'verification'
                ? 'bg-slate-900 text-white shadow-sm'
                : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'
            }`}
            title="合同强行法红线扫描仪"
          >
            <FileCheck2 className={`w-4 h-4 ${currentView === 'verification' ? 'text-white' : 'text-slate-500'}`} />
            {!collapsed && <span>合同红线扫描仪</span>}
          </button>

          <button
            onClick={() => setCurrentView('search')}
            className={`w-full flex items-center gap-2.5 px-2.5 py-1.5 rounded-xl text-xs font-medium transition-all cursor-pointer ${
              currentView === 'search'
                ? 'bg-slate-900 text-white shadow-sm'
                : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'
            }`}
            title="东盟六国法典与判例库"
          >
            <Scale className={`w-4 h-4 ${currentView === 'search' ? 'text-white' : 'text-slate-500'}`} />
            {!collapsed && <span>六国法典判例库</span>}
          </button>

          <button
            onClick={() => setCurrentView('consults')}
            className={`w-full flex items-center gap-2.5 px-2.5 py-1.5 rounded-xl text-xs font-medium transition-all cursor-pointer ${
              currentView === 'consults'
                ? 'bg-slate-900 text-white shadow-sm'
                : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'
            }`}
            title="Local Counsel 专家与避冲库"
          >
            <Users className={`w-4 h-4 ${currentView === 'consults' ? 'text-white' : 'text-slate-500'}`} />
            {!collapsed && <span>Local Counsel 专家库</span>}
          </button>
        </div>

        {/* ========================================================================= */}
        {/* 第三层：东盟合规底座 (底层支撑 5%) */}
        {/* ========================================================================= */}
        <div className="space-y-1 pt-1">
          {!collapsed && (
            <div className="px-2 text-[10px] font-semibold text-slate-400 uppercase tracking-wider">
              合规底座 (5%)
            </div>
          )}

          <button
            onClick={() => setCurrentView('compliance')}
            className={`w-full flex items-center gap-2.5 px-2.5 py-1.5 rounded-xl text-xs font-medium transition-all cursor-pointer ${
              currentView === 'compliance'
                ? 'bg-slate-900 text-white shadow-sm'
                : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'
            }`}
            title="合规体检与六国比选"
          >
            <Sliders className={`w-4 h-4 ${currentView === 'compliance' ? 'text-white' : 'text-slate-500'}`} />
            {!collapsed && <span>合规体检 & 六国比选</span>}
          </button>
        </div>
      </div>

      {/* 底部信息栏 */}
      {!collapsed && (
        <div className="p-3 border-t border-slate-200/80 text-[11px] text-slate-400 flex items-center justify-between">
          <span className="font-mono">v2.5 Fluent 2</span>
          <span className="text-emerald-600 font-medium">● 知识库 2026 在线</span>
        </div>
      )}
    </aside>
  );
};
