/**
 * 涉外法查明辅助 Agent 前端主入口
 * 遵循现代法律科技与 AI 融合设计规范 (Linear / Claude / Gemini 风格)
 */

import React, { useState, useRef, useEffect } from 'react';
import { AppProvider, useApp } from './context/AppContext';
import { Sidebar } from './components/common/Sidebar';
import { TopBar } from './components/common/TopBar';
import { UnifiedRightDock } from './components/common/UnifiedRightDock';
import { CommandPaletteModal } from './components/common/CommandPaletteModal';
import { LawModal } from './components/common/LawModal';
import { HomeLandingView } from './components/home/HomeLandingView';
import { CaseListView } from './components/cases/CaseListView';
import { CaseAnalysisView } from './components/analysis/CaseAnalysisView';
import { NormSearchEngineView } from './components/search/NormSearchEngineView';
import { MaterialVerificationView } from './components/verification/MaterialVerificationView';
import { ExpertConsultsView } from './components/consults/ExpertConsultsView';
import { CasePipelineAnimationModal } from './components/workspace/CasePipelineAnimationModal';
import { CaseEntryModal } from './components/cases/CaseEntryModal';
import { ComplianceCenterView } from './components/compliance/ComplianceCenterView';
import { AseanVectorBackground } from './components/home/AseanVectorBackground';
import { ShieldCheck, CheckCircle2, AlertCircle, Info, X } from 'lucide-react';

const MainLayout: React.FC = () => {
  const {
    currentView,
    toasts,
    removeToast,
    isDrawerOpen,
    closeLawDrawer,
    isRightDockOpen,
    closeRightDock,
    isPipelineAnimationOpen,
    closePipelineAnimation,
    openPipelineAnimation,
    setCurrentView,
    currentCase,
    currentCaseId,
    switchingCaseId,
    sidebarCollapsed,
    setSidebarCollapsed,
    isCaseEntryModalOpen,
    closeCaseEntryModal,
  } = useApp();

  const mainScrollRef = useRef<HTMLElement>(null);

  // 当切换视图或切换具体案卷时，立即重置视口滚动条至顶部，杜绝视口错位
  useEffect(() => {
    mainScrollRef.current?.scrollTo({ top: 0, left: 0, behavior: 'instant' });
  }, [currentView, currentCase?.case_id]);

  const renderCurrentView = () => {
    switch (currentView) {
      case 'home':
        return <HomeLandingView />;
      case 'cases':
        return <CaseListView />;
      case 'entry':
        return <CaseEntryModal isOpen={true} onClose={() => setCurrentView('cases')} />;
      case 'analysis':
        return <CaseAnalysisView />;
      case 'search':
        return <NormSearchEngineView />;
      case 'verification':
        return <MaterialVerificationView />;
      case 'consults':
        return <ExpertConsultsView />;
      case 'compliance':
        return <ComplianceCenterView />;
      default:
        return <HomeLandingView />;
    }
  };

  return (
    <div className="min-h-screen flex bg-[#F6F8FA] text-zinc-900 antialiased font-sans">
      {/* 左侧可折叠导航边栏 */}
      <Sidebar
        collapsed={sidebarCollapsed}
        onToggleCollapse={() => setSidebarCollapsed(!sidebarCollapsed)}
      />

      {/* 右侧主工作区 */}
      <div className="flex-1 flex flex-col min-w-0 min-h-screen">
        <TopBar
          collapsed={sidebarCollapsed}
          onToggleCollapse={() => setSidebarCollapsed(!sidebarCollapsed)}
        />

        {/* 工作区画布主体 (支持分栏与抽屉并排工作台) */}
        <div className="flex-1 flex min-w-0 overflow-hidden relative">
          {/* 主视口工作流画布 */}
          <main
            ref={mainScrollRef}
            className="flex-1 min-w-0 overflow-y-auto relative"
          >
            {/* 非主页其它页面顶部：展示更精简优雅的东盟山海与日光射线矢量背景 */}
            {currentView !== 'home' && (
              <AseanVectorBackground variant="compact" />
            )}

            {/* 专案研判视图中以 currentCase?.case_id 或 currentCaseId 为联合 key，确保切案时触发优雅动效 */}
            <div
              key={currentView === 'analysis' ? `analysis-${currentCase?.case_id || currentCaseId || 'init'}` : currentView}
              className="apple-page-pane min-h-full relative z-10"
            >
              {renderCurrentView()}
            </div>

            {/* 底部法治合规备案与说明条 (极简克制) */}
            {(
              <footer className="border-t border-slate-200/80 bg-white/70 backdrop-blur-md py-4 px-6 text-xs text-slate-500 mt-12">
                <div className="max-w-[1500px] mx-auto flex flex-col sm:flex-row items-center justify-between gap-3">
                  <div className="flex items-center gap-2">
                    <ShieldCheck className="w-3.5 h-3.5 text-blue-600" />
                    <span className="font-semibold text-slate-800">
                      OverseasLawAssist 域外法查明与深度研判智能工作台
                    </span>
                    <span>·</span>
                    <span className="font-mono text-[11px] text-slate-400">
                      东盟官方司法公报 / 司法部法通网 / FIDIC 国际工程范本 / 国资委海外合规
                    </span>
                  </div>
                  <div className="text-[11px] text-slate-400 font-mono">
                    最高院《涉外民事关系法律适用法解释（二）》规范 · 智能辅助决策
                  </div>
                </div>
              </footer>
            )}
          </main>

          {/* 右侧统一副驾坞 / 对照窗 (Unified Right Dock) - 桌面端右侧分栏 (注入 Apple Spring 物理动效) */}
          {(isRightDockOpen || isDrawerOpen) && (
            <div className="hidden lg:block w-[440px] xl:w-[460px] shrink-0 h-full border-l border-slate-200/80 bg-white z-20 apple-drawer-spring shadow-2xl">
              <UnifiedRightDock onClose={closeRightDock} />
            </div>
          )}

          {/* 移动端/窄屏下的抽屉遮罩与侧滑抽屉 */}
          {(isRightDockOpen || isDrawerOpen) && (
            <div className="lg:hidden fixed inset-0 z-50 flex justify-end bg-black/40 apple-modal-backdrop" onClick={closeRightDock}>
              <div className="w-full max-w-md h-full bg-white shadow-2xl apple-drawer-spring" onClick={(e) => e.stopPropagation()}>
                <UnifiedRightDock onClose={closeRightDock} />
              </div>
            </div>
          )}
        </div>
      </div>

      {/* 全局 3D 景深查明推演动画弹窗 */}
      <CasePipelineAnimationModal
        isOpen={isPipelineAnimationOpen}
        onClose={closePipelineAnimation}
        onComplete={() => {
          closePipelineAnimation();
          setCurrentView('analysis');
        }}
        caseMeta={{
          title: currentCase?.meta?.title || currentCase?.title || '东盟工程与投资合规风险研判案',
          buyerCountry: '中资出海企业 · 联合体',
          sellerCountry: '东盟东道国项目业主',
          criticalDate: currentCase?.meta?.contract_date || '2024-03-15',
          jurisdiction: currentCase?.meta?.jurisdiction || 'asean_id',
        }}
      />

      {/* 浮层法条小弹窗 (点击任意条文或法源时原地弹出查看，避免滚屏迷失) */}
      <LawModal />

      {/* 全局新建案件查明弹窗 (Apple Bento 动效) */}
      <CaseEntryModal
        isOpen={isCaseEntryModalOpen}
        onClose={closeCaseEntryModal}
      />

      {/* 全局聚焦命令面板 (Spotlight / Linear Cmd/Ctrl+K) */}
      <CommandPaletteModal />

      {/* 全局 Toast 通知容器 */}
      <div className="fixed bottom-5 right-5 z-50 space-y-2 max-w-sm w-full pointer-events-none">
        {toasts.map((t) => (
          <div
            key={t.id}
            className={`pointer-events-auto p-3.5 rounded-2xl border shadow-lg text-xs flex items-start justify-between gap-3 transition-all ${
              t.type === 'success'
                ? 'bg-white text-zinc-900 border-emerald-200'
                : t.type === 'error'
                ? 'bg-white text-zinc-900 border-rose-200'
                : t.type === 'warning'
                ? 'bg-white text-zinc-900 border-amber-200'
                : 'bg-white text-zinc-900 border-zinc-200'
            }`}
          >
            <div className="flex items-start gap-2.5">
              {t.type === 'success' && (
                <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
              )}
              {t.type === 'error' && (
                <AlertCircle className="w-4 h-4 text-rose-600 shrink-0 mt-0.5" />
              )}
              {t.type === 'warning' && (
                <AlertCircle className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
              )}
              {t.type === 'info' && (
                <Info className="w-4 h-4 text-blue-600 shrink-0 mt-0.5" />
              )}
              <span className="leading-relaxed font-medium">{t.message}</span>
            </div>
            <button
              onClick={() => removeToast(t.id)}
              className="text-zinc-400 hover:text-zinc-700 p-0.5 shrink-0 rounded transition-colors cursor-pointer"
            >
              <X className="w-3.5 h-3.5" />
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default function App() {
  return (
    <AppProvider>
      <MainLayout />
    </AppProvider>
  );
}
