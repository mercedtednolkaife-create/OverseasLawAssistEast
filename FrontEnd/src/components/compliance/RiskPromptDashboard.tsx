import React, { useState, useEffect } from 'react';
import { useApp } from '../../context/AppContext';
import { lawAgentApi } from '../../api/lawAgentApi';
import { DEFAULT_RISK_MATRIX } from './complianceDefaultData';
import {
  X,
  CheckCircle2,
  XCircle,
  BookOpen,
  Compass,
  Loader2,
} from 'lucide-react';

type RiskLevel = 'critical' | 'high' | 'caution' | 'safe';

interface RiskCellData {
  level: RiskLevel;
  summary: string;
  scenario: string;
  statute: string;
  statuteText: string;
  dos: string[];
  donts: string[];
}

interface LegislativeShift {
  id: string;
  country: string;
  countryFlag: string;
  title: string;
  effectiveDate: string;
  coreShift: string;
  practiceImpact: string;
  alertType: 'warning' | 'info' | 'critical';
}

export const RiskPromptDashboard: React.FC = () => {
  const { openLawDrawer, loadCase, openPipelineAnimation, setCurrentView, showToast, openRightDock } = useApp();
  const [isLaunching, setIsLaunching] = useState(false);
  const [loading, setLoading] = useState(false);
  const [shifts, setShifts] = useState<LegislativeShift[]>(DEFAULT_RISK_MATRIX.shifts as unknown as LegislativeShift[]);
  const [domains, setDomains] = useState<string[]>(DEFAULT_RISK_MATRIX.domains);
  const [countries, setCountries] = useState<Array<{ id: string; name: string; flag: string }>>(DEFAULT_RISK_MATRIX.supported_countries);
  const [matrixCells, setMatrixCells] = useState<Record<string, RiskCellData>>(DEFAULT_RISK_MATRIX.matrix as unknown as Record<string, RiskCellData>);
  const [selectedCell, setSelectedCell] = useState<{
    domain: string;
    country: string;
    countryId: string;
    flag: string;
    data: RiskCellData;
  } | null>(null);

  useEffect(() => {
    let mounted = true;
    lawAgentApi
      .getRiskMatrix()
      .then((data) => {
        if (mounted && data) {
          if (Array.isArray(data.shifts) && data.shifts.length > 0) setShifts(data.shifts);
          if (Array.isArray(data.domains) && data.domains.length > 0) setDomains(data.domains);
          if (Array.isArray(data.supported_countries) && data.supported_countries.length > 0) setCountries(data.supported_countries);
          if (data.matrix && typeof data.matrix === 'object' && Object.keys(data.matrix).length > 0) setMatrixCells(data.matrix);
        }
      })
      .catch((err) => {
        console.warn('Risk matrix background fetch failed, using fallback:', err);
      });
    return () => {
      mounted = false;
    };
  }, []);

  const handleLaunchRiskSandbox = async () => {
    if (!selectedCell) return;
    try {
      setIsLaunching(true);
      showToast(`正在为【${selectedCell.country} · ${selectedCell.domain}】立项并启动合规审查流水线...`, 'info');

      const isPre =
        selectedCell.domain.includes('准入') ||
        selectedCell.domain.includes('股比') ||
        selectedCell.domain.includes('土地') ||
        selectedCell.domain.includes('外资');
      const stage = isPre ? 'pre_investment' : 'execution_dispute';

      const res = await lawAgentApi.createCase({
        title: `【${selectedCell.country}专项风险审查】${selectedCell.domain}`,
        facts_zh: `针对${selectedCell.country}建设工程投资合规，专项查明【${selectedCell.domain}】风险要件：\n\n【典型触发场景与发难手法】\n${selectedCell.data.scenario}\n\n【现行法定依据】\n${selectedCell.data.statute}: "${selectedCell.data.statuteText}"\n\n【合规红线禁令】\n${selectedCell.data.donts.join('；')}`,
        claims_zh: `1. 查明${selectedCell.country}法律对“${selectedCell.domain}”的具体强制性规定及属地裁判裁判尺度；\n2. 提出针对“${selectedCell.data.summary}”的合同防御与履约救济方案。`,
        meta: {
          title: `【${selectedCell.country}专项风险审查】${selectedCell.domain}`,
          jurisdiction: selectedCell.countryId,
          lifecycle_stage: stage,
          contract_type: '涉外建设工程与海外投资专项合规审查',
          contract_date: new Date().toISOString().split('T')[0],
          parties: ['中资出海企业/总承包商', `${selectedCell.country}东道国业主/属地监管当局`],
          choice_of_law: `${selectedCell.country}现行实体法与强制性规范`,
          dispute_resolution: 'SIAC',
        },
        materials: [
          {
            name: selectedCell.data.statute,
            desc_zh: selectedCell.domain,
            excerpt_zh: selectedCell.data.statuteText,
          },
        ],
        consent_version: 'v1.0',
      });

      setSelectedCell(null);
      await loadCase(res.case_id, true);
      openPipelineAnimation();
      setCurrentView('analysis');
      showToast(`已成功为【${selectedCell.country} · ${selectedCell.domain}】创建专项审查案卷！`, 'success');
    } catch (err: any) {
      showToast(err.message || '立项推演启动失败', 'error');
    } finally {
      setIsLaunching(false);
    }
  };

  // 从后端风险矩阵映射表检索单元格数据
  const getCellData = (domainIdx: number, countryId: string): RiskCellData => {
    const key = `${domainIdx}_${countryId}`;
    return (
      matrixCells[key] || {
        level: 'safe',
        summary: '常规合规管控要点。',
        scenario: '项目正常履约中的合同与行政监管要求。',
        statute: 'Host Country Statutory Code & FIDIC Standard',
        statuteText: '依据东道国现行建设工程行政规程及 FIDIC 施工标准规范执行。',
        dos: ['落实日常履约留痕；', '规范合同变更发函；', '配合属地劳工与税务审计。'],
        donts: ['严禁擅自停工；', '严禁无签证实施重大变更；', '严禁违规雇佣非法劳工。'],
      }
    );
  };

  const getLevelDot = (level: RiskLevel) => {
    switch (level) {
      case 'critical':
        return <span className="w-2 h-2 rounded-full bg-red-600 shrink-0 shadow-xs" title="极高危风险" />;
      case 'high':
        return <span className="w-2 h-2 rounded-full bg-amber-500 shrink-0" title="高危风险" />;
      case 'caution':
        return <span className="w-2 h-2 rounded-full bg-blue-500 shrink-0" title="中度关注" />;
      case 'safe':
        return <span className="w-2 h-2 rounded-full bg-emerald-500 shrink-0" title="常规可控" />;
    }
  };

  const getLevelBadgeText = (level: RiskLevel) => {
    switch (level) {
      case 'critical':
        return '极高危 🔴';
      case 'high':
        return '高危 🟠';
      case 'caution':
        return '中度关注 🟡';
      case 'safe':
        return '常规可控 🟢';
    }
  };

  if (loading && shifts.length === 0) {
    return (
      <div className="py-24 apple-bento-card flex flex-col items-center justify-center space-y-3 min-h-[380px]">
        <Loader2 className="w-8 h-8 text-blue-600 animate-spin" />
        <p className="text-xs text-slate-500 font-medium">正在载入风险提示与立法预警...</p>
      </div>
    );
  }

  return (
    <div className="space-y-5">
      {/* 顶部：重大立法与司法转向实时预警栏 */}
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-red-600 animate-pulse" />
            <h3 className="text-sm font-bold text-slate-900">
              东盟重大立法与司法动态预警
            </h3>
          </div>
          <span className="text-[11px] text-slate-400 font-medium">
            2026 现行有效法源动态追踪 · 规避经验主义合规盲区
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3">
          {shifts.map((shift) => (
            <div
              key={shift.id}
              onClick={() => {
                openRightDock('country_playbook');
                showToast(`已在右侧辅助面板载入【${shift.country}】最新立法预警`, 'info');
              }}
              className={`p-4 rounded-2xl border transition-all cursor-pointer hover:shadow-xs hover:border-slate-300 ${
                shift.alertType === 'critical'
                  ? 'bg-rose-50/40 border-rose-200/80'
                  : 'bg-amber-50/40 border-amber-200/80'
              }`}
            >
              <div className="flex items-center justify-between mb-1.5">
                <span className="text-xs font-bold text-slate-900 flex items-center gap-1">
                  <span>{shift.countryFlag}</span>
                  <span>{shift.country}</span>
                </span>
                <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-white/90 border border-slate-200 text-slate-600 font-semibold">
                  {shift.effectiveDate}
                </span>
              </div>

              <h4 className="text-xs font-bold text-slate-900 line-clamp-1 mb-1">
                {shift.title}
              </h4>

              <p className="text-[11px] text-slate-700 line-clamp-3 leading-relaxed mb-2 font-medium">
                {shift.coreShift}
              </p>

              <div className="pt-2 border-t border-slate-200/70 text-[10px] text-slate-500 leading-snug">
                <span className="font-semibold text-slate-700">【实务对策】</span>
                {shift.practiceImpact}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* 风险提示矩阵 */}
      <div className="apple-bento-card p-6 space-y-4">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 border-b border-slate-100 pb-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-blue-600 shadow-xs shadow-blue-500/40" />
              <h3 className="text-base font-bold text-slate-900 tracking-tight">
                东盟工程核心合规风险提示矩阵
              </h3>
            </div>
            <p className="text-xs text-slate-500 mt-1">
              点击单元格查阅该法域针对性风险要点、法定依据与防范举措
            </p>
          </div>

          {/* 图例 */}
          <div className="flex items-center gap-3 text-xs text-slate-600">
            <span className="flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-full bg-red-600" />
              <span>极高危 (🔴)</span>
            </span>
            <span className="flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-full bg-amber-500" />
              <span>高危 (🟠)</span>
            </span>
            <span className="flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-full bg-blue-500" />
              <span>中度关注 (🟡)</span>
            </span>
            <span className="flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-full bg-emerald-500" />
              <span>常规可控 (🟢)</span>
            </span>
          </div>
        </div>

        {/* 矩阵表格 */}
        <div className="overflow-x-auto rounded-xl border border-slate-200/80">
          <table className="w-full text-left border-collapse min-w-[700px]">
            <thead>
              <tr className="border-b border-slate-200 bg-slate-50/90">
                <th className="py-2.5 px-3.5 text-xs font-bold text-slate-700 w-64">
                  工程核心风险域
                </th>
                {countries.map((c) => (
                  <th key={c.id} className="py-2.5 px-3 text-xs font-bold text-slate-800 text-center">
                    <span className="mr-1">{c.flag}</span>
                    <span>{c.name}</span>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 text-xs">
              {domains.map((domain, dIdx) => (
                <tr key={dIdx} className="hover:bg-slate-50/70 transition-colors">
                  <td className="py-3 px-3.5 font-medium text-slate-800 text-xs">
                    {domain}
                  </td>
                  {countries.map((c) => {
                    const data = getCellData(dIdx, c.id);
                    return (
                      <td key={c.id} className="py-3 px-3 text-center">
                        <button
                          onClick={() =>
                            setSelectedCell({
                              domain,
                              country: c.name,
                              countryId: c.id,
                              flag: c.flag,
                              data,
                            })
                          }
                          className="p-1.5 rounded-lg hover:bg-slate-100 transition-colors inline-flex items-center gap-1.5 cursor-pointer group"
                          title="点击查看风险提示卡"
                        >
                          {getLevelDot(data.level)}
                          <span className="text-[11px] font-mono font-medium text-slate-500 group-hover:text-slate-900">
                            {getLevelBadgeText(data.level).split(' ')[0]}
                          </span>
                        </button>
                      </td>
                    );
                  })}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* 弹窗：建设工程专项风险提示卡 */}
      {selectedCell && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/40 backdrop-blur-xs animate-in fade-in duration-200">
          <div className="bg-white rounded-2xl max-w-2xl w-full border border-slate-200/90 shadow-xl overflow-hidden animate-in zoom-in-95 duration-200 space-y-5 p-6 select-text max-h-[90vh] overflow-y-auto">
            {/* 弹窗顶栏 */}
            <div className="flex items-start justify-between border-b border-slate-100 pb-3">
              <div>
                <div className="flex items-center gap-2">
                  <span className="text-xl">{selectedCell.flag}</span>
                  <span className="text-xs font-bold text-slate-500">
                    {selectedCell.country} · 建设工程专项风险提示
                  </span>
                </div>
                <h3 className="text-base font-bold text-slate-900 mt-1">
                  {selectedCell.domain}
                </h3>
              </div>
              <button
                onClick={() => setSelectedCell(null)}
                className="p-1 text-slate-400 hover:text-slate-800 hover:bg-slate-100 rounded-lg transition-colors cursor-pointer"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* 风险级别与警示摘要 */}
            <div className="p-4 rounded-xl bg-rose-50/40 border border-rose-200/80 space-y-1.5">
              <div className="flex items-center gap-2">
                {getLevelDot(selectedCell.data.level)}
                <span className="text-xs font-bold text-rose-900">
                  【风险等级】{getLevelBadgeText(selectedCell.data.level)}
                </span>
              </div>
              <p className="text-xs text-rose-800 leading-relaxed font-medium">
                {selectedCell.data.summary}
              </p>
            </div>

            {/* 触发场景与典型发难手法 */}
            <div className="space-y-1.5">
              <h4 className="text-xs font-bold text-slate-900">
                【触发场景与东道国常见发难手法】
              </h4>
              <p className="text-xs text-slate-700 leading-relaxed bg-slate-50/80 p-3.5 rounded-xl border border-slate-200/70 font-medium">
                {selectedCell.data.scenario}
              </p>
            </div>

            {/* 现行法定依据 */}
            <div className="space-y-1.5">
              <h4 className="text-xs font-bold text-slate-900">
                【现行法定依据与司法规则】
              </h4>
              <div className="p-3.5 rounded-xl bg-blue-50/40 border border-blue-200/60 space-y-1 text-xs">
                <span className="font-mono font-bold text-blue-800 block">
                  {selectedCell.data.statute}
                </span>
                <p className="text-slate-700 italic">
                  "{selectedCell.data.statuteText}"
                </p>
              </div>
            </div>

            {/* 红线防范动作 */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {/* Do's */}
              <div className="p-4 rounded-xl bg-emerald-50/40 border border-emerald-200/70 space-y-2">
                <div className="text-xs font-bold text-emerald-900 flex items-center gap-1.5">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                  <span>实务推荐防御动作</span>
                </div>
                <div className="space-y-1.5 text-xs text-slate-800 font-medium">
                  {selectedCell.data.dos.map((d, idx) => (
                    <div key={idx} className="flex items-start gap-1.5">
                      <span className="text-emerald-600 font-bold">✓</span>
                      <span>{d}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Don'ts */}
              <div className="p-4 rounded-xl bg-rose-50/40 border border-rose-200/70 space-y-2">
                <div className="text-xs font-bold text-rose-900 flex items-center gap-1.5">
                  <XCircle className="w-4 h-4 text-rose-600" />
                  <span>合规红线禁令</span>
                </div>
                <div className="space-y-1.5 text-xs text-slate-800 font-medium">
                  {selectedCell.data.donts.map((d, idx) => (
                    <div key={idx} className="flex items-start gap-1.5">
                      <span className="text-rose-600 font-bold">✕</span>
                      <span>{d}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* 底栏按钮 */}
            <div className="pt-3 border-t border-slate-100 flex flex-wrap items-center justify-between gap-3">
              <div className="flex items-center gap-2">
                <button
                  onClick={handleLaunchRiskSandbox}
                  disabled={isLaunching}
                  className="flex items-center gap-1.5 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-xl text-xs font-semibold transition-all duration-150 cursor-pointer shadow-xs shadow-blue-500/25 active:scale-[0.98] disabled:opacity-50"
                >
                  <Compass className="w-4 h-4" />
                  <span>{isLaunching ? '正在立项并启动...' : '针对该国别风险启动专项审查推演'}</span>
                </button>
                <button
                  onClick={() => {
                    openRightDock('country_playbook');
                    showToast(`已在右侧辅助面板载入【${selectedCell.country}】合规速查手册`, 'info');
                  }}
                  className="px-3.5 py-2 bg-slate-100 hover:bg-slate-200 text-slate-800 rounded-xl text-xs font-semibold transition-colors flex items-center gap-1.5 cursor-pointer"
                >
                  <BookOpen className="w-3.5 h-3.5 text-blue-600" />
                  <span>在侧栏中查阅</span>
                </button>
              </div>

              <button
                onClick={() => setSelectedCell(null)}
                className="px-4 py-2 bg-slate-100 text-slate-700 rounded-xl text-xs font-semibold hover:bg-slate-200 transition-colors cursor-pointer"
              >
                已了解并关闭
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
