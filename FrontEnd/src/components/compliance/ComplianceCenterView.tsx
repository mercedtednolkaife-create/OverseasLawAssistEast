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
  Plus,
  Play,
} from 'lucide-react';

export type ComplianceTab = 'cases' | 'guidelines' | 'risk_radar' | 'matrix';

export const ComplianceCenterView: React.FC = () => {
  const { setCurrentView, openCaseEntryModal } = useApp();
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
      {/* 顶部决策看板 Header Banner */}
      <div className="bg-gradient-to-r from-zinc-900 via-zinc-800 to-zinc-900 text-white rounded-2xl p-6 sm:p-8 shadow-sm relative overflow-hidden">
        <div className="relative z-10 max-w-3xl space-y-3">
          <div className="inline-flex items-center gap-2 px-2.5 py-1 rounded-full bg-blue-500/10 border border-blue-400/20 text-blue-300 text-xs font-semibold">
            <span className="w-1.5 h-1.5 rounded-full bg-blue-400" />
            <span>国务院国资委 35 号令合规贯通架构 · 2026 现行有效法源</span>
          </div>

          <h1 className="text-xl sm:text-2xl font-bold tracking-tight text-white">
            央国企东盟工程与投资合规体系建设中心
          </h1>

          <p className="text-xs sm:text-sm text-zinc-300 leading-relaxed font-normal">
            聚焦中资央国企出海东盟“投建营一体化”全链条法律风险防范。集成 5D 典型案例复盘、全生命周期“三道防线”SOP、6×12 场景化风险矩阵及一键生成交底合规手册。
          </p>

          <div className="flex items-center gap-3 pt-2">
            <button
              onClick={() => openCaseEntryModal()}
              className="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-xl text-xs font-semibold transition-colors shadow-xs flex items-center gap-1.5 cursor-pointer"
            >
              <Plus className="w-3.5 h-3.5" />
              <span>新建个案查明</span>
            </button>
            <button
              onClick={() => setCurrentView('workspace')}
              className="px-4 py-2 bg-white/10 hover:bg-white/15 text-white rounded-xl text-xs font-semibold transition-colors flex items-center gap-1.5 cursor-pointer border border-white/10"
            >
              <span>进入个案工作台</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>

        {/* 装饰徽章 */}
        <div className="absolute right-6 -bottom-6 opacity-10 pointer-events-none hidden lg:block">
          <Compass className="w-56 h-56 text-white" />
        </div>
      </div>

      {/* 四大核心模块切换 Tab */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-2 bg-zinc-100 p-1 rounded-2xl">
        {tabs.map((tab) => {
          const isSelected = activeTab === tab.id;
          const IconComp = tab.icon;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as ComplianceTab)}
              className={`p-3 rounded-xl text-left transition-all cursor-pointer flex items-center gap-3 ${
                isSelected
                  ? 'bg-white text-zinc-900 shadow-xs'
                  : 'text-zinc-600 hover:text-zinc-900 hover:bg-zinc-200/50'
              }`}
            >
              <div
                className={`w-8 h-8 rounded-lg flex items-center justify-center shrink-0 ${
                  isSelected ? 'bg-blue-600 text-white' : 'bg-zinc-200/80 text-zinc-600'
                }`}
              >
                <IconComp className="w-4 h-4" />
              </div>
              <div className="min-w-0">
                <div className="text-xs font-bold truncate">{tab.label}</div>
                <div className="text-[11px] text-zinc-400 truncate mt-0.5">{tab.sub}</div>
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
