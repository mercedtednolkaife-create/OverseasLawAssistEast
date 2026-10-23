import React, { useState } from 'react';
import { useApp } from '../../context/AppContext';
import { CaseReferenceHub } from './CaseReferenceHub';
import { ComplianceGuidelineCenter } from './ComplianceGuidelineCenter';
import { RiskPromptDashboard } from './RiskPromptDashboard';
import { ASEANComparisonMatrix } from './ASEANComparisonMatrix';
import {
  ShieldAlert,
  Compass,
  FileCheck2,
  TrendingUp,
  TableProperties,
  ArrowRight,
  BookOpen,
  Sparkles,
  Layers,
} from 'lucide-react';

export type ComplianceTab = 'cases' | 'guidelines' | 'risk_radar' | 'matrix';

export const ComplianceCenterView: React.FC = () => {
  const { openRightDock } = useApp();
  const [activeTab, setActiveTab] = useState<ComplianceTab>('cases');

  const tabs = [
    {
      id: 'cases',
      label: '5D 典型案例参考库',
      sub: '四大标杆案例与五维复盘卡',
      icon: Compass,
    },
    {
      id: 'guidelines',
      label: '全周期合规指引引擎',
      sub: '五阶段 SOP 与三道防线核查',
      icon: FileCheck2,
    },
    {
      id: 'risk_radar',
      label: '风险提示与立法预警',
      sub: '6×12 风险矩阵与修法雷达',
      icon: TrendingUp,
    },
    {
      id: 'matrix',
      label: '六国实务横向对比',
      sub: '东盟六国成文法与司法规则对比',
      icon: TableProperties,
    },
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 py-6 space-y-6">
      {/* 顶部决策看板 Header Banner (Apple HIG x Fluent 2 视觉令牌) */}
      <div className="acrylic-card p-6 sm:p-7 shadow-xs relative overflow-hidden">
        <div className="relative z-10 max-w-4xl space-y-3">
          <div className="inline-flex items-center gap-2 px-2.5 py-1 rounded-full bg-blue-50 border border-blue-200 text-blue-700 text-xs font-semibold">
            <span className="w-1.5 h-1.5 rounded-full bg-blue-600 animate-pulse" />
            <span>国务院国资委 35 号令合规贯通架构 · 2026 现行有效法源</span>
          </div>

          <h1 className="text-xl sm:text-2xl font-bold tracking-tight text-slate-900">
            央国企东盟工程与投资合规体系建设中心
          </h1>

          <p className="text-xs sm:text-sm text-slate-600 leading-relaxed font-normal">
            聚焦中资央国企出海东盟“投建营一体化”全链条法律风险防范。集成 5D 典型案例复盘、全生命周期“三道防线”SOP、6×12 场景化风险矩阵及一键生成交底合规手册。
          </p>

          <div className="flex flex-wrap items-center gap-2.5 pt-1">
            <button
              onClick={() => openRightDock('country_playbook')}
              className="btn-space-titanium px-4 py-2 rounded-xl text-xs font-semibold flex items-center gap-2 cursor-pointer shadow-xs"
            >
              <BookOpen className="w-3.5 h-3.5 text-blue-300" />
              <span>呼出右侧属地排雷速查坞</span>
              <kbd className="text-[10px] bg-slate-800 text-slate-300 px-1.5 py-0.5 rounded font-mono">Cmd+B</kbd>
            </button>
            <div className="flex items-center gap-1.5 text-xs text-slate-500 pl-2">
              <span className="text-[11px] text-slate-400">已收录东道国：</span>
              <span className="px-2 py-0.5 rounded-md bg-slate-100 text-slate-700 font-medium">🇮🇩 印尼</span>
              <span className="px-2 py-0.5 rounded-md bg-slate-100 text-slate-700 font-medium">🇻🇳 越南</span>
              <span className="px-2 py-0.5 rounded-md bg-slate-100 text-slate-700 font-medium">🇲🇾 马来西亚</span>
              <span className="px-2 py-0.5 rounded-md bg-slate-100 text-slate-700 font-medium">🇸🇬 新加坡</span>
              <span className="px-2 py-0.5 rounded-md bg-slate-100 text-slate-700 font-medium">🇹🇭 泰国</span>
              <span className="px-2 py-0.5 rounded-md bg-slate-100 text-slate-700 font-medium">🇵🇭 菲律宾</span>
            </div>
          </div>
        </div>

        {/* 装饰徽章 */}
        <div className="absolute right-6 -bottom-6 opacity-5 pointer-events-none hidden lg:block">
          <Compass className="w-56 h-56 text-slate-900" />
        </div>
      </div>

      {/* 四大核心模块切换 Tab */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-2 bg-slate-200/50 p-1 rounded-2xl">
        {tabs.map((tab) => {
          const isSelected = activeTab === tab.id;
          const IconComp = tab.icon;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as ComplianceTab)}
              className={`p-3 rounded-xl text-left transition-all cursor-pointer flex items-center gap-3 ${
                isSelected
                  ? 'bg-white text-slate-900 shadow-sm'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-white/60'
              }`}
            >
              <div
                className={`w-8 h-8 rounded-lg flex items-center justify-center shrink-0 ${
                  isSelected ? 'bg-slate-900 text-white' : 'bg-slate-200 text-slate-600'
                }`}
              >
                <IconComp className="w-4 h-4" />
              </div>
              <div className="min-w-0">
                <div className="text-xs font-bold truncate">{tab.label}</div>
                <div className="text-[11px] text-slate-400 truncate mt-0.5">{tab.sub}</div>
              </div>
            </button>
          );
        })}
      </div>

      {/* 子模块视图渲染 */}
      <div>
        {activeTab === 'cases' && <CaseReferenceHub />}
        {activeTab === 'guidelines' && <ComplianceGuidelineCenter />}
        {activeTab === 'risk_radar' && <RiskPromptDashboard />}
        {activeTab === 'matrix' && <ASEANComparisonMatrix />}
      </div>
    </div>
  );
};
