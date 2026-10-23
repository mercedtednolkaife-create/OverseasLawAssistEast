import React, { useState, useEffect, useRef, useMemo } from 'react';
import { useApp } from '../../context/AppContext';
import {
  Search,
  FolderOpen,
  Sliders,
  Scale,
  ShieldCheck,
  FileCheck2,
  Users,
  FileText,
  Plus,
  BookOpen,
  ArrowRight,
  Sparkles,
  Command,
} from 'lucide-react';

export const CommandPaletteModal: React.FC = () => {
  const {
    isCommandPaletteOpen,
    closeCommandPalette,
    casesList,
    loadCase,
    setCurrentView,
    openCaseEntryModal,
    openRightDock,
    currentCase,
  } = useApp();

  const [query, setQuery] = useState('');
  const [selectedIndex, setSelectedIndex] = useState(0);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (isCommandPaletteOpen) {
      setQuery('');
      setSelectedIndex(0);
      setTimeout(() => inputRef.current?.focus(), 50);
    }
  }, [isCommandPaletteOpen]);

  // Command items definitions
  const allItems = useMemo(() => {
    const items = [
      // Actions
      {
        id: 'action-new-case',
        category: '快捷操作',
        title: '新建查明案卷 / 导入索赔邮件',
        desc: '支持粘贴原始英文邮件一键智能要素抽提',
        icon: Plus,
        action: () => {
          closeCommandPalette();
          openCaseEntryModal();
        },
      },
      {
        id: 'action-open-copilot',
        category: '快捷操作',
        title: '呼出案卷 AI 专属副驾坞',
        desc: '进入 S1~S9 推理对话与红队攻防对抗',
        icon: Sparkles,
        action: () => {
          closeCommandPalette();
          openRightDock('case_copilot');
        },
      },
      {
        id: 'action-open-playbook',
        category: '快捷操作',
        title: '东盟属地排雷与合规手册 (Playbook)',
        desc: '查看 6 国 12 风险域 Do\'s & Don\'ts',
        icon: ShieldCheck,
        action: () => {
          closeCommandPalette();
          openRightDock('country_playbook');
        },
      },
      // Tools
      {
        id: 'tool-scanner',
        category: '实务工具',
        title: '合同强行法红线 & 外律意见书扫描核验仪',
        desc: '5秒穿透扫描背靠背、保函止付与语言法红线',
        icon: FileCheck2,
        action: () => {
          closeCommandPalette();
          setCurrentView('verification');
        },
      },
      {
        id: 'tool-search',
        category: '实务工具',
        title: '东盟六国与 FIDIC 权威法典判例库',
        desc: '中英双语检索 31 部现行有效法典与 7 篇金标准先例',
        icon: Scale,
        action: () => {
          closeCommandPalette();
          setCurrentView('search');
        },
      },
      {
        id: 'tool-experts',
        category: '实务工具',
        title: '东盟 Local Counsel 与 DAAB 专家会商枢纽',
        desc: 'SIAC/BANI/AIAC/VIAC 注册资深大律师利益冲突排查',
        icon: Users,
        action: () => {
          closeCommandPalette();
          setCurrentView('consults');
        },
      },
      {
        id: 'tool-compliance',
        category: '实务工具',
        title: '五阶段合规体检打分 & 六国横向比选',
        desc: '实时测算健康度指数与未达标项定向立项',
        icon: Sliders,
        action: () => {
          closeCommandPalette();
          setCurrentView('compliance');
        },
      },
    ];

    // Append case items
    casesList.forEach((c) => {
      items.push({
        id: `case-${c.case_id}`,
        category: '专案案卷直达',
        title: `${c.case_id} · ${c.title}`,
        desc: `法域: ${c.jurisdiction || '东盟'} | 阶段: ${c.lifecycle_stage === 'pre_investment' ? '投前准入' : '履约索赔'}`,
        icon: FolderOpen,
        action: () => {
          closeCommandPalette();
          loadCase(c.case_id);
          setCurrentView('analysis');
        },
      });
    });

    return items;
  }, [casesList, closeCommandPalette, loadCase, openCaseEntryModal, openRightDock, setCurrentView]);

  const filteredItems = useMemo(() => {
    if (!query.trim()) return allItems;
    const q = query.toLowerCase();
    return allItems.filter(
      (item) =>
        item.title.toLowerCase().includes(q) ||
        item.desc.toLowerCase().includes(q) ||
        item.category.toLowerCase().includes(q)
    );
  }, [allItems, query]);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      setSelectedIndex((prev) => (prev + 1) % filteredItems.length);
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setSelectedIndex((prev) => (prev - 1 + filteredItems.length) % filteredItems.length);
    } else if (e.key === 'Enter') {
      e.preventDefault();
      if (filteredItems[selectedIndex]) {
        filteredItems[selectedIndex].action();
      }
    } else if (e.key === 'Escape') {
      e.preventDefault();
      closeCommandPalette();
    }
  };

  if (!isCommandPaletteOpen) return null;

  return (
    <div
      className="fixed inset-0 z-50 flex items-start justify-center pt-20 px-4 bg-slate-900/40 backdrop-blur-sm apple-modal-backdrop"
      onClick={closeCommandPalette}
    >
      <div
        className="w-full max-w-xl bg-white/95 backdrop-blur-2xl rounded-2xl shadow-2xl border border-slate-200/90 overflow-hidden flex flex-col apple-modal-card"
        onClick={(e) => e.stopPropagation()}
        onKeyDown={handleKeyDown}
      >
        {/* 顶部搜索框 */}
        <div className="flex items-center px-4 py-3.5 border-b border-slate-200/80 gap-3">
          <Search className="w-4 h-4 text-slate-400 shrink-0" />
          <input
            ref={inputRef}
            type="text"
            value={query}
            onChange={(e) => {
              setQuery(e.target.value);
              setSelectedIndex(0);
            }}
            placeholder="搜索案卷、跳转工具、切换模式、检索法源... (↑↓ 导航, Enter 选择)"
            className="flex-1 bg-transparent text-sm text-slate-900 placeholder:text-slate-400 focus:outline-none"
          />
          <kbd className="px-1.5 py-0.5 text-[10px] font-mono text-slate-400 bg-slate-100 rounded border border-slate-200">
            ESC
          </kbd>
        </div>

        {/* 搜索结果列表 */}
        <div className="max-h-[380px] overflow-y-auto p-2 space-y-1">
          {filteredItems.length === 0 ? (
            <div className="py-8 text-center text-xs text-slate-400">
              未找到匹配的案卷或功能指令
            </div>
          ) : (
            filteredItems.map((item, idx) => {
              const Icon = item.icon;
              const isSelected = idx === selectedIndex;
              return (
                <div
                  key={item.id}
                  onClick={item.action}
                  onMouseEnter={() => setSelectedIndex(idx)}
                  className={`px-3 py-2.5 rounded-xl flex items-center justify-between cursor-pointer transition-colors ${
                    isSelected ? 'bg-slate-900 text-white' : 'text-slate-700 hover:bg-slate-100'
                  }`}
                >
                  <div className="flex items-center gap-3 min-w-0">
                    <div
                      className={`p-1.5 rounded-lg shrink-0 ${
                        isSelected ? 'bg-white/20 text-white' : 'bg-slate-100 text-slate-600'
                      }`}
                    >
                      <Icon className="w-4 h-4" />
                    </div>
                    <div className="min-w-0">
                      <div className="text-xs font-semibold truncate flex items-center gap-2">
                        <span>{item.title}</span>
                        <span
                          className={`text-[10px] font-normal px-1.5 py-0.2 rounded ${
                            isSelected ? 'bg-white/20 text-slate-200' : 'bg-slate-100 text-slate-400'
                          }`}
                        >
                          {item.category}
                        </span>
                      </div>
                      <div
                        className={`text-[11px] truncate ${
                          isSelected ? 'text-slate-300' : 'text-slate-400'
                        }`}
                      >
                        {item.desc}
                      </div>
                    </div>
                  </div>
                  {isSelected && <ArrowRight className="w-3.5 h-3.5 text-white/80 shrink-0 ml-2" />}
                </div>
              );
            })
          )}
        </div>

        {/* 底部提示栏 */}
        <div className="px-4 py-2 border-t border-slate-100 bg-slate-50/60 text-[11px] text-slate-400 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Command className="w-3 h-3" />
            <span>Cmd/Ctrl + K 随时呼出</span>
          </div>
          <div>当前案卷：{currentCase?.case_id || '未选择'}</div>
        </div>
      </div>
    </div>
  );
};
