import React, { useState, useMemo, useEffect } from 'react';
import { useApp } from '../../context/AppContext';
import { lawAgentApi } from '../../api/lawAgentApi';
import {
  Download,
  CheckCircle2,
  AlertCircle,
  FileCheck,
  ShieldCheck,
  Building,
  Compass,
  AlertTriangle,
  Activity,
  Loader2,
} from 'lucide-react';

type CheckStatus = 'passed' | 'flawed' | 'failed';

const JUR_NAMES: Record<string, string> = {
  asean_id: '印度尼西亚',
  asean_vn: '越南',
  asean_my: '马来西亚',
  asean_sg: '新加坡',
  asean_th: '泰国',
  asean_ph: '菲律宾',
};

const ARCHETYPE_NAMES: Record<string, string> = {
  EPC_CONTRACTING: 'EPC 总承包',
  PPP_CONCESSION: 'BOT / PPP 特许经营',
  CROSS_BORDER_MA: '跨境股权并购',
  JV_CONSORTIUM: '属地联营体 (KSO/JO)',
};

interface StageGuideline {
  id: string;
  stageName: string;
  stageNumber: string;
  subTitle: string;
  coreFocus: string;
  // 三道防线清单
  defenseLines: {
    line1_operational: {
      title: string;
      checklists: string[];
      riskTip: string;
    };
    line2_legal: {
      title: string;
      checklists: string[];
      riskTip: string;
    };
    line3_audit: {
      title: string;
      checklists: string[];
      riskTip: string;
    };
  };
}

export const ComplianceGuidelineCenter: React.FC = () => {
  const { showToast, loadCase, openPipelineAnimation, setCurrentView, openCaseEntryWithPrefill } = useApp();
  const [stages, setStages] = useState<StageGuideline[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [activeStageId, setActiveStageId] = useState<string>('');

  useEffect(() => {
    let mounted = true;
    lawAgentApi
      .getComplianceGuidelines()
      .then((data) => {
        if (mounted && Array.isArray(data) && data.length > 0) {
          const list = data as StageGuideline[];
          setStages(list);
          setActiveStageId(list[0].id);
          setItemStatuses((prev) => {
            if (Object.keys(prev).length > 0) return prev;
            const init: Record<string, CheckStatus> = {};
            list.forEach((stage, sIdx) => {
              (['line1_operational', 'line2_legal', 'line3_audit'] as const).forEach((lineKey) => {
                const line = stage.defenseLines?.[lineKey];
                if (!line || !Array.isArray(line.checklists)) return;
                line.checklists.forEach((_, idx) => {
                  const key = `${stage.id}_${lineKey}_${idx}`;
                  if (sIdx === 0 && lineKey === 'line1_operational' && idx === 1) {
                    init[key] = 'flawed';
                  } else if (sIdx === 2 && lineKey === 'line2_legal' && idx === 0) {
                    init[key] = 'flawed';
                  } else if (sIdx === 3 && lineKey === 'line1_operational' && idx === 1) {
                    init[key] = 'failed';
                  } else {
                    init[key] = 'passed';
                  }
                });
              });
            });
            return init;
          });
        }
      })
      .catch((err) => {
        console.error('Failed to load compliance guidelines', err);
      })
      .finally(() => {
        if (mounted) setLoading(false);
      });
    return () => {
      mounted = false;
    };
  }, []);

  const [activeDefenseLine, setActiveDefenseLine] = useState<'line1' | 'line2' | 'line3'>('line1');
  const [exportJur, setExportJur] = useState<string>('asean_id');
  const [exportArchetype, setExportArchetype] = useState<string>('EPC_CONTRACTING');
  const [isExporting, setIsExporting] = useState<boolean>(false);
  const [isCreatingCase, setIsCreatingCase] = useState<boolean>(false);

  // 在线自测打分系统状态 (支持 localStorage 持久化)
  const [itemStatuses, setItemStatuses] = useState<Record<string, CheckStatus>>(() => {
    try {
      const saved = localStorage.getItem('compliance_guidelines_status');
      if (saved) return JSON.parse(saved);
    } catch {}
    return {};
  });

  useEffect(() => {
    try {
      localStorage.setItem('compliance_guidelines_status', JSON.stringify(itemStatuses));
    } catch {}
  }, [itemStatuses]);

  const handleResetChecklist = () => {
    localStorage.removeItem('compliance_guidelines_status');
    const init: Record<string, CheckStatus> = {};
    stages.forEach((stage) => {
      (['line1_operational', 'line2_legal', 'line3_audit'] as const).forEach((lineKey) => {
        const line = stage.defenseLines[lineKey];
        line.checklists.forEach((_, idx) => {
          const key = `${stage.id}_${lineKey}_${idx}`;
          init[key] = 'passed';
        });
      });
    });
    setItemStatuses(init);
    showToast('已重置体检清单状态', 'info');
  };

  const currentStage = stages.find((s) => s.id === activeStageId) || stages[0];

  // 当前阶段所有核验点
  const currentStageItems = useMemo(() => {
    if (!currentStage || !currentStage.defenseLines) return [];
    const items: Array<{
      key: string;
      lineKey: string;
      lineTitle: string;
      text: string;
      status: CheckStatus;
    }> = [];
    (['line1_operational', 'line2_legal', 'line3_audit'] as const).forEach((lineKey) => {
      const line = currentStage.defenseLines[lineKey];
      if (!line || !Array.isArray(line.checklists)) return;
      line.checklists.forEach((text, idx) => {
        const key = `${currentStage.id}_${lineKey}_${idx}`;
        items.push({
          key,
          lineKey,
          lineTitle: line.title,
          text,
          status: itemStatuses[key] || 'passed',
        });
      });
    });
    return items;
  }, [currentStage, itemStatuses]);

  // 当前阶段未达标或瑕疵项
  const currentUnmetItems = useMemo(() => {
    return currentStageItems.filter((it) => it.status === 'flawed' || it.status === 'failed');
  }, [currentStageItems]);

  // 当前阶段得分 (0-100)
  const stageScore = useMemo(() => {
    if (currentStageItems.length === 0) return 100;
    const totalPoints = currentStageItems.reduce((acc, it) => {
      return acc + (it.status === 'passed' ? 100 : it.status === 'flawed' ? 50 : 0);
    }, 0);
    return Math.round(totalPoints / currentStageItems.length);
  }, [currentStageItems]);

  // 全项目总得分 (0-100)
  const overallScore = useMemo(() => {
    let totalItems = 0;
    let totalPoints = 0;
    stages.forEach((stage) => {
      (['line1_operational', 'line2_legal', 'line3_audit'] as const).forEach((lineKey) => {
        const line = stage.defenseLines[lineKey];
        line.checklists.forEach((_, idx) => {
          const key = `${stage.id}_${lineKey}_${idx}`;
          const status = itemStatuses[key] || 'passed';
          totalItems += 1;
          totalPoints += status === 'passed' ? 100 : status === 'flawed' ? 50 : 0;
        });
      });
    });
    return totalItems > 0 ? Math.round(totalPoints / totalItems) : 100;
  }, [itemStatuses]);

  // 一键将未达标项立项并启动专项推演
  const handleGenerateComplianceCase = async () => {
    if (currentUnmetItems.length === 0) {
      showToast('当前阶段所有审查要件均已达标，无须启动未达标专项查明！', 'info');
      return;
    }
    try {
      setIsCreatingCase(true);
      showToast(`正在将 ${currentUnmetItems.length} 项未达标要件汇编并启动专项法律推演...`, 'info');

      const jurName = JUR_NAMES[exportJur] || '东盟法域';
      const archName = ARCHETYPE_NAMES[exportArchetype] || '建设工程';
      const isPre = currentStage?.id?.includes('investment') || currentStage?.id === 'stage_1';
      const stage = isPre ? 'pre_investment' : 'execution_dispute';

      const factsText = `本项目（${archName}，目标法域：${jurName}）在“${currentStage.stageName}”全周期合规自测中发现以下 ${currentUnmetItems.length} 项未达标或瑕疵要件：\n\n` +
        currentUnmetItems.map((u, i) => `${i + 1}. [${u.status === 'failed' ? '严重未达标' : '存在瑕疵'}] 【${u.lineTitle}】: ${u.text}`).join('\n\n') +
        `\n\n【防线红线禁令与监管警示】\n` +
        `- 实操红线：${currentStage.defenseLines.line1_operational.riskTip}\n` +
        `- 法务红线：${currentStage.defenseLines.line2_legal.riskTip}\n` +
        `- 审计红线：${currentStage.defenseLines.line3_audit.riskTip}`;

      const claimsText = `1. 专项查明${jurName}现行法律及属地行业监管对上述【${currentUnmetItems.map((u) => u.text.slice(0, 10)).join('、')}】未达标事实的法律效力、行政处罚或失权后果；\n2. 依据 FIDIC 标准条件与属地强行法，输出合规补救措施与条款谈判对冲方案。`;

      const res = await lawAgentApi.createCase({
        title: `【${currentStage.stageName}自检专项查明】${currentUnmetItems.length}项未达标风险点`,
        facts_zh: factsText,
        claims_zh: claimsText,
        meta: {
          title: `【${currentStage.stageName}自检专项查明】${currentUnmetItems.length}项未达标风险点`,
          jurisdiction: exportJur,
          lifecycle_stage: stage,
          contract_type: `${archName} (FIDIC 银皮书标准条件)`,
          contract_date: new Date().toISOString().split('T')[0],
          parties: ['中资出海企业/央企施工总包', `${jurName}东道国业主/属地监管主管机关`],
          choice_of_law: `${jurName}现行实体法与强制性规范`,
          dispute_resolution: 'SIAC',
        },
        materials: currentUnmetItems.map((u) => ({
          name: `${currentStage.stageName}合规自检记录`,
          desc_zh: u.lineTitle,
          excerpt_zh: u.text,
        })),
        consent_version: 'v1.0',
      });

      await loadCase(res.case_id, true);
      openPipelineAnimation();
      setCurrentView('analysis');
      showToast(`已成功将 ${currentUnmetItems.length} 项未达标点转化为专项查明案卷并启动多 Agent 推演流水线！`, 'success');
    } catch (err: any) {
      showToast(err.message || '专项立项推演失败', 'error');
    } finally {
      setIsCreatingCase(false);
    }
  };

  const handleExportHandbook = async () => {
    try {
      setIsExporting(true);
      showToast('正在为您汇编定制《央企海外工程专项合规指引手册 (DOCX)》...', 'info');
      const url = `/api/cases/compliance/handbook/docx?jurisdiction=${exportJur}&archetype=${exportArchetype}`;
      const res = await fetch(url);
      if (!res.ok) throw new Error('导出失败');
      const blob = await res.blob();
      const downloadUrl = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = downloadUrl;
      a.download = `Compliance_Handbook_${exportJur}_${exportArchetype}.docx`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(downloadUrl);
      showToast('合规指引手册 (DOCX) 已成功生成并下载！', 'success');
    } catch (e) {
      showToast('合规指引手册导出异常，请核验网络后重试', 'error');
    } finally {
      setIsExporting(false);
    }
  };

  const getLineData = () => {
    if (activeDefenseLine === 'line1') return currentStage.defenseLines.line1_operational;
    if (activeDefenseLine === 'line2') return currentStage.defenseLines.line2_legal;
    return currentStage.defenseLines.line3_audit;
  };

  const lineData = getLineData();

  if (loading || !currentStage) {
    return (
      <div className="py-24 bg-white rounded-2xl border border-zinc-200/80 shadow-xs flex flex-col items-center justify-center space-y-3 min-h-[400px]">
        <Loader2 className="w-8 h-8 text-blue-600 animate-spin" />
        <p className="text-xs text-zinc-500 font-medium">正在自东盟出海建设工程五阶段 × 三道防线知识库载入核查表...</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* 顶部：手册定制导出工具条 */}
      <div className="bg-white p-5 rounded-2xl border border-zinc-200/80 shadow-xs flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-emerald-600" />
            <h2 className="text-base font-bold text-zinc-900">
              建设工程全周期合规指引引擎 (SOP & Checklists)
            </h2>
          </div>
          <p className="text-xs text-zinc-500 mt-1">
            对标国资委 35 号令与《中央企业合规管理办法》，贯通全生命周期五阶段与“三道防线”实操
          </p>
        </div>

        {/* 一键导出手册配置 */}
        <div className="flex items-center gap-2 flex-wrap">
          <select
            value={exportJur}
            onChange={(e) => setExportJur(e.target.value)}
            className="text-xs bg-zinc-50 border border-zinc-200 rounded-lg px-2.5 py-1.5 font-medium text-zinc-700 outline-none"
          >
            <option value="asean_id">🇮🇩 印度尼西亚 (SEMA 3/2023)</option>
            <option value="asean_vn">🇻🇳 越南 (2025新建设法)</option>
            <option value="asean_my">🇲🇾 马来西亚 (CIPAA 2012)</option>
            <option value="asean_sg">🇸🇬 新加坡 (SOPA / SIAC)</option>
            <option value="asean_th">🇹🇭 泰国 (CCC / FBA)</option>
            <option value="asean_ph">🇵🇭 菲律宾 (RA 11966 PPP)</option>
          </select>

          <select
            value={exportArchetype}
            onChange={(e) => setExportArchetype(e.target.value)}
            className="text-xs bg-zinc-50 border border-zinc-200 rounded-lg px-2.5 py-1.5 font-medium text-zinc-700 outline-none"
          >
            <option value="EPC_CONTRACTING">EPC 总承包 (FIDIC 银皮书)</option>
            <option value="PPP_CONCESSION">BOT / PPP 特许经营</option>
            <option value="CROSS_BORDER_MA">跨境股权并购 (SPA/SHA)</option>
            <option value="JV_CONSORTIUM">属地联营体 (KSO/JO)</option>
          </select>

          <button
            onClick={handleExportHandbook}
            disabled={isExporting}
            className="px-4 py-1.5 bg-zinc-900 text-white rounded-lg text-xs font-semibold hover:bg-zinc-800 transition-colors shadow-xs flex items-center gap-1.5 cursor-pointer disabled:opacity-50"
          >
            <Download className="w-3.5 h-3.5" />
            <span>{isExporting ? '正在汇编...' : '导出合规手册 (Word)'}</span>
          </button>
        </div>
      </div>

      {/* 全项目与阶段合规健康度仪表板 */}
      <div className="grid grid-cols-1 md:grid-cols-12 gap-4 items-stretch">
        {/* 全项目综合得分 */}
        <div className="md:col-span-5 bg-white p-4.5 rounded-2xl border border-zinc-200/80 shadow-xs flex items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <Activity className="w-4 h-4 text-blue-600" />
              <span className="text-xs font-bold text-zinc-900">
                出海工程全周期合规健康指数
              </span>
            </div>
            <p className="text-[11px] text-zinc-500">
              综合评估全生命周期五阶段三道防线实操核查点
            </p>
          </div>
          <div className="text-right shrink-0">
            <div className="flex items-baseline gap-1 justify-end">
              <span className={`text-2xl font-bold font-mono ${
                overallScore >= 80 ? 'text-emerald-600' : overallScore >= 60 ? 'text-amber-600' : 'text-rose-600'
              }`}>
                {overallScore}
              </span>
              <span className="text-xs text-zinc-400 font-mono">/ 100</span>
            </div>
            <span className={`inline-block px-2.5 py-1 rounded-md text-xs font-bold border mt-0.5 ${
              overallScore >= 80
                ? 'text-emerald-700 bg-emerald-50 border-emerald-200'
                : overallScore >= 60
                ? 'text-amber-700 bg-amber-50 border-amber-200'
                : 'text-rose-700 bg-rose-50 border-rose-200'
            }`}>
              {overallScore >= 80 ? '合规健康 · 低风险' : overallScore >= 60 ? '审慎关注 · 中风险' : '警报隐患 · 高风险'}
            </span>
            <div className="w-28 bg-slate-100 h-1.5 rounded-full overflow-hidden mt-1.5 ml-auto">
              <div
                className={`h-full transition-all duration-500 rounded-full ${
                  overallScore >= 80 ? 'bg-emerald-500' : overallScore >= 60 ? 'bg-amber-500' : 'bg-rose-500'
                }`}
                style={{ width: `${overallScore}%` }}
              />
            </div>
          </div>
        </div>

        {/* 当前阶段健康度与一键立项推演卡片 */}
        <div className="md:col-span-7 bg-white p-4.5 rounded-2xl border border-zinc-200/80 shadow-xs flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <span className="text-xs font-bold text-zinc-900">
                Phase {currentStage.stageNumber} ({currentStage.stageName}) 健康度:
              </span>
              <span className={`font-mono text-sm font-bold ${
                stageScore >= 80 ? 'text-emerald-600' : stageScore >= 60 ? 'text-amber-600' : 'text-rose-600'
              }`}>
                {stageScore} 分
              </span>
            </div>
            <div className="flex items-center gap-2 text-[11px] text-zinc-500">
              <span>达标: {currentStageItems.filter(i => i.status === 'passed').length}项</span>
              <span>·</span>
              <span className="text-amber-600 font-medium">瑕疵: {currentStageItems.filter(i => i.status === 'flawed').length}项</span>
              <span>·</span>
              <span className="text-rose-600 font-medium">未达标: {currentStageItems.filter(i => i.status === 'failed').length}项</span>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={handleResetChecklist}
              className="px-3 py-2 rounded-xl text-xs font-medium text-zinc-600 hover:text-zinc-900 bg-zinc-100 hover:bg-zinc-200/80 border border-zinc-200 transition-colors cursor-pointer"
              title="重置体检打分至默认状态"
            >
              重置体检表
            </button>
            <button
              onClick={handleGenerateComplianceCase}
              disabled={isCreatingCase || currentUnmetItems.length === 0}
              className={`flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-semibold transition-all duration-150 shadow-xs cursor-pointer ${
                currentUnmetItems.length > 0
                  ? 'bg-blue-600 hover:bg-blue-700 text-white'
                  : 'bg-zinc-100 text-zinc-400 cursor-not-allowed'
              }`}
            >
              <Compass className="w-3.5 h-3.5" />
              <span>
                {isCreatingCase
                  ? '正在立项推演...'
                  : currentUnmetItems.length > 0
                  ? `将未达标项(${currentUnmetItems.length})生成专项案卷推演`
                  : '本阶段全部达标'}
              </span>
            </button>
          </div>
        </div>
      </div>

      {/* 五阶段演进水平导航卡 */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
        {stages.map((stage) => {
          const isSelected = stage.id === activeStageId;
          return (
            <button
              key={stage.id}
              onClick={() => setActiveStageId(stage.id)}
              className={`p-3.5 rounded-xl border text-left transition-all cursor-pointer ${
                isSelected
                  ? 'bg-white border-blue-600 ring-1 ring-blue-600 shadow-xs'
                  : 'bg-white border-zinc-200/80 hover:border-zinc-300'
              }`}
            >
              <div className="flex items-center justify-between mb-1">
                <span
                  className={`text-xs font-mono font-semibold px-2 py-0.5 rounded-md ${
                    isSelected ? 'bg-blue-600 text-white' : 'bg-zinc-100 text-zinc-600'
                  }`}
                >
                  Phase {stage.stageNumber}
                </span>
                {isSelected && <span className="w-1.5 h-1.5 rounded-full bg-blue-600" />}
              </div>
              <h3 className="text-xs font-bold text-zinc-900 line-clamp-1 mt-1">
                {stage.stageName}
              </h3>
              <p className="text-[11px] text-zinc-500 line-clamp-1 mt-0.5">
                {stage.subTitle}
              </p>
            </button>
          );
        })}
      </div>

      {/* 主体指引内容卡 */}
      <div className="bg-white rounded-2xl border border-zinc-200/80 p-6 shadow-xs space-y-6">
        {/* 阶段标题与核心关注 */}
        <div className="border-b border-zinc-100 pb-4">
          <div className="flex items-center gap-2">
            <span className="text-xs font-mono font-bold text-blue-600 bg-blue-50 px-2 py-0.5 rounded">
              Phase {currentStage.stageNumber}
            </span>
            <h3 className="text-sm font-bold text-zinc-900">
              {currentStage.stageName} · 实务操作指南
            </h3>
          </div>
          <p className="text-xs text-zinc-600 mt-2 font-medium leading-relaxed">
            【阶段核心关注】{currentStage.coreFocus}
          </p>
        </div>

        {/* 国资委“三道防线”角色切换器 */}
        <div>
          <div className="text-[11px] font-bold text-zinc-400 uppercase tracking-wider mb-2">
            国资委“三道防线”角色视角切换
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-2">
            {[
              {
                id: 'line1',
                label: '第一道防线',
                sub: '海外市场部 / 项目现场经理实操清单',
                icon: Building,
              },
              {
                id: 'line2',
                label: '第二道防线',
                sub: '涉外法务 / 专职合规官审查要点',
                icon: ShieldCheck,
              },
              {
                id: 'line3',
                label: '第三道防线',
                sub: '集团审计 / 纪检 / 国资监管穿透核查',
                icon: FileCheck,
              },
            ].map((tab) => {
              const isSelected = activeDefenseLine === tab.id;
              const IconComp = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveDefenseLine(tab.id as any)}
                  className={`p-3 rounded-xl border text-left transition-all cursor-pointer flex items-start gap-2.5 ${
                    isSelected
                      ? 'bg-zinc-900 border-zinc-900 text-white shadow-xs'
                      : 'bg-zinc-50 border-zinc-200/80 hover:bg-zinc-100/70 text-zinc-800'
                  }`}
                >
                  <IconComp
                    className={`w-4 h-4 mt-0.5 shrink-0 ${
                      isSelected ? 'text-white' : 'text-zinc-500'
                    }`}
                  />
                  <div>
                    <div className="text-xs font-bold leading-tight">{tab.label}</div>
                    <div
                      className={`text-[11px] mt-0.5 leading-snug line-clamp-1 ${
                        isSelected ? 'text-zinc-300' : 'text-zinc-500'
                      }`}
                    >
                      {tab.sub}
                    </div>
                  </div>
                </button>
              );
            })}
          </div>
        </div>

        {/* 审查动作清单与红线提示 */}
        <div className="space-y-4 pt-2">
          <div className="flex items-center gap-2">
            <span className="w-1.5 h-1.5 rounded-full bg-blue-600" />
            <h4 className="text-xs font-bold text-zinc-900">
              {lineData.title}
            </h4>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {lineData.checklists.map((check, idx) => {
              const currentLineKey = activeDefenseLine === 'line1' ? 'line1_operational' : activeDefenseLine === 'line2' ? 'line2_legal' : 'line3_audit';
              const itemKey = `${currentStage.id}_${currentLineKey}_${idx}`;
              const currentStatus = itemStatuses[itemKey] || 'passed';

              return (
                <div
                  key={idx}
                  className={`p-3.5 rounded-xl border transition-all text-xs space-y-2.5 ${
                    currentStatus === 'passed'
                      ? 'bg-zinc-50/80 border-zinc-200/70'
                      : currentStatus === 'flawed'
                      ? 'bg-amber-50/30 border-amber-200/80'
                      : 'bg-rose-50/30 border-rose-200/80'
                  }`}
                >
                  <div className="flex items-start gap-2 text-zinc-800 font-medium leading-relaxed">
                    {currentStatus === 'passed' && (
                      <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                    )}
                    {currentStatus === 'flawed' && (
                      <AlertTriangle className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
                    )}
                    {currentStatus === 'failed' && (
                      <AlertCircle className="w-4 h-4 text-rose-600 shrink-0 mt-0.5" />
                    )}
                    <span className="flex-1">{check}</span>
                  </div>

                  {/* 状态三选一切换器 */}
                  <div className="flex items-center justify-between pt-1 border-t border-zinc-200/40 text-[11px]">
                    <span className="text-zinc-400 font-medium">合规自检判定:</span>
                    <div className="flex items-center gap-1 bg-white p-0.5 rounded-lg border border-zinc-200/70 shadow-2xs">
                      <button
                        type="button"
                        onClick={() => setItemStatuses((prev) => ({ ...prev, [itemKey]: 'passed' }))}
                        className={`px-2 py-0.5 rounded text-xs font-medium transition-colors cursor-pointer ${
                          currentStatus === 'passed'
                            ? 'bg-emerald-600 text-white'
                            : 'text-zinc-500 hover:text-emerald-700'
                        }`}
                      >
                        ✓ 已满足
                      </button>
                      <button
                        type="button"
                        onClick={() => setItemStatuses((prev) => ({ ...prev, [itemKey]: 'flawed' }))}
                        className={`px-2 py-0.5 rounded text-xs font-medium transition-colors cursor-pointer ${
                          currentStatus === 'flawed'
                            ? 'bg-amber-500 text-white'
                            : 'text-zinc-500 hover:text-amber-700'
                        }`}
                      >
                        ! 瑕疵
                      </button>
                      <button
                        type="button"
                        onClick={() => setItemStatuses((prev) => ({ ...prev, [itemKey]: 'failed' }))}
                        className={`px-2 py-0.5 rounded text-xs font-medium transition-colors cursor-pointer ${
                          currentStatus === 'failed'
                            ? 'bg-rose-600 text-white'
                            : 'text-zinc-500 hover:text-rose-700'
                        }`}
                      >
                        ✕ 未达标
                      </button>
                    </div>
                  </div>

                  {/* 瑕疵或未达标时：一键发起专案推演 */}
                  {(currentStatus === 'flawed' || currentStatus === 'failed') && (
                    <div className="pt-2 border-t border-zinc-200/50 flex justify-end">
                      <button
                        type="button"
                        onClick={() => {
                          openCaseEntryWithPrefill({
                            title: `海外合规排雷专案 - ${check.slice(0, 26)}`,
                            jurisdiction: exportJur,
                            governing_law: 'asean_sg',
                            lifecycle_stage: activeStageId === 'stage_1' || activeStageId === 'stage_2' ? 'pre_investment' : 'execution_dispute',
                            facts: `合规审查项：${check}\n所属阶段：${currentStage.stageName} (${lineData.title})\n判定状态：${currentStatus === 'flawed' ? '存在合规瑕疵' : '完全未达标'}`,
                            claims: `针对 ${currentStage.stageName} 的 ${lineData.title} 合规缺口，开展专项法律调查与合规推演。`,
                          });
                          showToast('已携带该合规缺口发起专案建案！', 'info');
                        }}
                        className="inline-flex items-center gap-1 text-[11px] font-semibold text-blue-600 hover:text-blue-700 bg-blue-50/80 hover:bg-blue-100/80 px-2 py-1 rounded-lg border border-blue-200/60 transition-colors cursor-pointer"
                      >
                        <span>针对此缺口发起专案推演 ➔</span>
                      </button>
                    </div>
                  )}
                </div>
              );
            })}
          </div>

          {/* 专属风险红线警示框 */}
          <div className="p-4 rounded-xl bg-amber-50/40 border border-amber-200/70 flex items-start gap-3">
            <AlertCircle className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
            <div>
              <span className="text-xs font-bold text-amber-900 block">
                【本防线红线禁令与违规追责风险】
              </span>
              <p className="text-xs text-amber-800 mt-0.5 leading-relaxed font-medium">
                {lineData.riskTip}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
