import React, { useState, useEffect, useMemo } from 'react';
import { createPortal } from 'react-dom';
import { useApp } from '../../context/AppContext';
import {
  X,
  Share2,
} from 'lucide-react';
import { InteractiveCitationGraph } from './InteractiveCitationGraph';

interface CitationGraphFullscreenModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSelectNorm: (normId: string) => void;
}

export const CitationGraphFullscreenModal: React.FC<CitationGraphFullscreenModalProps> = ({
  isOpen,
  onClose,
  onSelectNorm,
}) => {
  const { currentCase } = useApp();
  const [selectedIssueFilter, setSelectedIssueFilter] = useState<string>('all');

  const isPreInv = currentCase?.meta?.lifecycle_stage === 'pre_investment';
  const jur = currentCase?.meta?.jurisdiction || 'asean_id';

  // 动态依据当前案卷真实存在的 issues 生成过滤 Tab，与案卷数据严格对齐
  const issueTabs = useMemo(() => {
    const rawIssues = currentCase?.issues || [];
    const chineseNums = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十'];
    if (rawIssues.length === 0) {
      return [
        { id: 'all', label: '全部' },
        { id: 'I1', label: isPreInv ? '支柱一' : '争点一' },
        { id: 'I2', label: isPreInv ? '支柱二' : '争点二' },
      ];
    }
    return [
      { id: 'all', label: '全部' },
      ...rawIssues.map((iss, idx) => ({
        id: iss.issue_id || `I${idx + 1}`,
        label: isPreInv ? `支柱${chineseNums[idx] || idx + 1}` : `争点${chineseNums[idx] || idx + 1}`,
      })),
    ];
  }, [currentCase?.issues, isPreInv]);

  // 当切换案件时，若原先选中的 filter 已不在当前案卷有效 Tab 中，自动重置为 'all'
  useEffect(() => {
    if (selectedIssueFilter !== 'all' && !issueTabs.some((t) => t.id === selectedIssueFilter)) {
      setSelectedIssueFilter('all');
    }
  }, [issueTabs, selectedIssueFilter]);

  // ESC 快捷键退出与背景滚动锁定
  useEffect(() => {
    if (!isOpen) return;

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        onClose();
      }
    };
    window.addEventListener('keydown', handleKeyDown);

    const prevOverflow = document.body.style.overflow;
    document.body.style.overflow = 'hidden';

    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      document.body.style.overflow = prevOverflow;
    };
  }, [isOpen, onClose]);

  if (!isOpen || !currentCase) return null;

  const countryLabels: Record<string, { flag: string; name: string }> = {
    asean_id: { flag: '🇮🇩', name: '印度尼西亚' },
    asean_vn: { flag: '🇻🇳', name: '越南' },
    asean_my: { flag: '🇲🇾', name: '马来西亚' },
    asean_sg: { flag: '🇸🇬', name: '新加坡' },
    asean_th: { flag: '🇹🇭', name: '泰国' },
    asean_ph: { flag: '🇵🇭', name: '菲律宾' },
  };

  const countryInfo = countryLabels[jur] || { flag: '🌏', name: '东盟涉外' };

  return createPortal(
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-2.5 sm:p-4 md:p-6 bg-slate-950/45 backdrop-blur-xl antialiased apple-modal-backdrop overflow-hidden select-none"
      onClick={onClose}
    >
      {/* 沉浸式全屏图谱舱：Apple/macOS 高透毛玻璃质感 + 极简微描边 + 柔和物理阴影 */}
      <div
        className="w-full h-full max-h-[96vh] max-w-[1780px] bg-white/95 backdrop-blur-3xl rounded-[24px] sm:rounded-[28px] shadow-[0_32px_96px_rgba(0,0,0,0.32)] border border-black/[0.08] flex flex-col overflow-hidden apple-modal-card"
        onClick={(e) => e.stopPropagation()}
      >
        {/* 顶部导航控制条：原生 Web Apple 极简毛玻璃横条 */}
        <div className="px-5 sm:px-7 py-3 border-b border-black/[0.06] bg-white/75 backdrop-blur-2xl flex flex-wrap items-center justify-between gap-3 shrink-0">
          {/* 左侧：专业图谱标识 + 案件元数据与国别徽标 */}
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-xl bg-blue-50 text-blue-600 border border-blue-200/60 flex items-center justify-center shadow-2xs shrink-0">
              <Share2 className="w-4 h-4 text-blue-600" />
            </div>

            <div className="flex items-center gap-2 flex-wrap">
              <span className="font-mono text-xs font-semibold text-slate-700 bg-black/[0.04] px-2 py-0.5 rounded-md border border-black/[0.06]">
                {currentCase.case_id}
              </span>
              <h2 className="text-sm font-bold text-slate-900 tracking-tight">
                法源因果拓扑图谱
              </h2>
              <span className="text-[11px] text-slate-600 bg-black/[0.04] px-2.5 py-0.5 rounded-full border border-black/[0.06] flex items-center gap-1.5">
                <span className={`w-1.5 h-1.5 rounded-full ${isPreInv ? 'bg-indigo-500' : 'bg-purple-500'}`} />
                <span className="font-medium">{isPreInv ? '投前准入' : '履约争议'}</span>
              </span>
              <span className="text-xs text-slate-500 font-medium hidden md:inline">
                · {countryInfo.flag} {countryInfo.name}
              </span>
            </div>
          </div>

          {/* 中间：4 层因果穿透引导面包屑 */}
          <div className="hidden xl:flex items-center gap-2 px-3.5 py-1 bg-black/[0.03] backdrop-blur-md rounded-full text-xs font-medium text-slate-600 border border-black/[0.04]">
            <span className="flex items-center gap-1.5 text-slate-800 font-medium">
              <span className="w-1.5 h-1.5 rounded-full bg-slate-400" />
              <span>案件事实</span>
            </span>
            <span className="text-slate-300 font-mono text-[10px]">➔</span>
            <span className="flex items-center gap-1.5 text-slate-800 font-medium">
              <span className="w-1.5 h-1.5 rounded-full bg-blue-500" />
              <span>争点要件</span>
            </span>
            <span className="text-slate-300 font-mono text-[10px]">➔</span>
            <span className="flex items-center gap-1.5 text-slate-800 font-medium">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
              <span>现行法典</span>
            </span>
            <span className="text-slate-300 font-mono text-[10px]">➔</span>
            <span className="flex items-center gap-1.5 text-slate-800 font-medium">
              <span className="w-1.5 h-1.5 rounded-full bg-purple-500" />
              <span>裁判对策</span>
            </span>
          </div>

          {/* 右侧：依据当前案卷自适应动态渲染的 Apple 分段选择器 + 原生关闭按钮 */}
          <div className="flex items-center gap-3">
            <span className="hidden lg:inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-blue-50/70 border border-blue-200/60 text-[11px] font-mono font-medium text-blue-700">
              <span className="w-1.5 h-1.5 rounded-full bg-blue-500 animate-pulse" />
              <span>共 {issueTabs.length - 1} 个因果支柱</span>
            </span>

            <div className="flex items-center p-0.5 bg-black/[0.04] backdrop-blur-md rounded-xl text-xs border border-black/[0.05] shadow-2xs">
              {issueTabs.map((tab) => (
                <button
                  key={tab.id}
                  type="button"
                  onClick={() => setSelectedIssueFilter(tab.id)}
                  className={`px-3 py-1 rounded-lg text-xs transition-all duration-200 cursor-pointer ${
                    selectedIssueFilter === tab.id
                      ? 'bg-white text-slate-900 shadow-sm font-semibold scale-[1.02]'
                      : 'text-slate-600 hover:text-slate-900 font-medium hover:bg-black/[0.02]'
                  }`}
                >
                  {tab.label}
                </button>
              ))}
            </div>

            <div className="h-4 w-[1px] bg-black/[0.08] mx-0.5" />

            <button
              type="button"
              onClick={onClose}
              className="group flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-black/[0.04] hover:bg-black/[0.08] active:scale-95 text-slate-600 hover:text-slate-900 transition-all cursor-pointer border border-black/[0.04]"
              title="关闭图谱 (Esc)"
            >
              <X className="w-3.5 h-3.5" />
              <span className="text-[11px] font-medium hidden sm:inline">关闭</span>
              <kbd className="hidden md:inline font-mono text-[9px] text-slate-400 bg-white/80 px-1 rounded border border-black/[0.08]">Esc</kbd>
            </button>
          </div>
        </div>

        {/* 交互式图谱主体画布 */}
        <div className="flex-1 overflow-hidden p-3.5 sm:p-5 relative flex flex-col min-h-0">
          <InteractiveCitationGraph
            fullscreen={true}
            filterIssueId={selectedIssueFilter}
            onSelectNorm={onSelectNorm}
          />
        </div>
      </div>
    </div>,
    document.body
  );
};
