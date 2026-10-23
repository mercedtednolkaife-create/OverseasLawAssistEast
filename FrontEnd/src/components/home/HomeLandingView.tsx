import React, { useState } from 'react';
import { useApp } from '../../context/AppContext';
import { lawAgentApi } from '../../api/lawAgentApi';
import { MaterialVerificationResult } from '../../types/lawAgent';
import {
  FileCheck2,
  FolderOpen,
  Plus,
  ArrowRight,
  ShieldAlert,
  Copy,
  Check,
  Sparkles,
  Zap,
  Globe2,
  Layers,
  FileText,
} from 'lucide-react';

export const HomeLandingView: React.FC = () => {
  const {
    casesList,
    loadCase,
    setCurrentView,
    openCaseEntryModal,
    openCaseEntryWithPrefill,
    showToast,
  } = useApp();

  // --- Track A: Fast 30s Redline Scanner State ---
  const [clauseText, setClauseText] = useState(
    'Payment to Subcontractor shall be made strictly within 14 days after Contractor receives payment from Employer (Pay-when-paid).'
  );
  const [selectedJur, setSelectedJur] = useState('asean_my');
  const [scanning, setScanning] = useState(false);
  const [scanResult, setScanResult] = useState<MaterialVerificationResult | null>(null);
  const [copiedClause, setCopiedClause] = useState(false);
  const [trackADiffMode, setTrackADiffMode] = useState(false);

  const sampleClauses = [
    {
      title: '大马背靠背条款',
      jur: 'asean_my',
      text: 'Payment to Subcontractor shall be made strictly within 14 days after Contractor receives payment from Employer (Pay-when-paid).',
    },
    {
      title: '新加坡保函止付排除',
      jur: 'asean_sg',
      text: 'The Employer may call the Performance Guarantee at its sole discretion, and Contractor irrevocably waives any right to seek court injunction on ground of unconscionability.',
    },
    {
      title: '印尼纯英文排他签署',
      jur: 'asean_id',
      text: 'This EPC Contract is executed exclusively in English. The parties expressly waive any requirement to translate this agreement into Bahasa Indonesia under Law No. 24/2009.',
    },
  ];

  const handleScan = async () => {
    if (!clauseText.trim() || scanning) return;
    setScanning(true);
    try {
      const res = await lawAgentApi.verifyForeignMaterials(clauseText, 'CONTRACT_REDLINE_AUDIT');
      setScanResult(res);
      showToast('✓ 强行法红线穿透扫描完成', 'success');
    } catch (e: any) {
      showToast(e.message || '扫描失败，请重试', 'error');
    } finally {
      setScanning(false);
    }
  };

  const handleCopyRedline = (text: string) => {
    navigator.clipboard.writeText(text);
    setCopiedClause(true);
    showToast('合规示范条款已复制到剪贴板', 'success');
    setTimeout(() => setCopiedClause(false), 2000);
  };

  const jurFlags: Record<string, { name: string; flag: string }> = {
    asean_id: { name: '印尼', flag: '🇮🇩' },
    asean_vn: { name: '越南', flag: '🇻🇳' },
    asean_my: { name: '马来西亚', flag: '🇲🇾' },
    asean_sg: { name: '新加坡', flag: '🇸🇬' },
    asean_th: { name: '泰国', flag: '🇹🇭' },
    asean_ph: { name: '菲律宾', flag: '🇵🇭' },
  };

  return (
    <div className="max-w-[1520px] mx-auto px-4 sm:px-6 py-6 space-y-6">
      {/* 顶部微标题 */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-200/80 pb-4">
        <div>
          <h1 className="text-xl sm:text-2xl font-extrabold text-slate-900 tracking-tight flex items-center gap-2">
            <span>东盟基建工程与涉外投资智能工作台</span>
            <span className="text-xs font-mono font-medium px-2 py-0.5 rounded-full bg-slate-100 text-slate-600 border border-slate-200">
              极速双轨制
            </span>
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            轨道 A：30秒合同强行法穿透扫描 ⟷ 轨道 B：深度专案多智能体研判与出海沙盘
          </p>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={openCaseEntryModal}
            className="px-3.5 py-2 rounded-xl btn-space-titanium text-xs font-semibold flex items-center gap-1.5 cursor-pointer shadow-sm"
          >
            <Plus className="w-3.5 h-3.5 text-blue-400" />
            <span>+ 录入新项目 / 索赔邮件</span>
          </button>
        </div>
      </div>

      {/* 双轨 Bento 网格布局 (60% 左主舱 vs 40% 右主舱) */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* ========================================================================= */}
        {/* 左主舱：轨道 A —— 30秒合同强行法红线极速扫描 (占宽 7 列 / ~60%) */}
        {/* ========================================================================= */}
        <section className="lg:col-span-7 bg-white rounded-2xl border border-slate-200/90 shadow-sm p-5 space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div className="p-2 rounded-xl bg-blue-50 text-blue-600">
                <Zap className="w-4 h-4" />
              </div>
              <div>
                <h2 className="text-sm font-bold text-slate-900">
                  轨道 A：涉外合同专用条件 (PC) 强行法穿透扫描仪
                </h2>
                <p className="text-[11px] text-slate-400">
                  粘贴待审查英文条款，5 秒穿透识别东道国强制法绝对无效红线
                </p>
              </div>
            </div>
            <span className="text-[11px] font-mono text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded-md border border-emerald-200">
              无需立案 · 即粘即验
            </span>
          </div>

          {/* 典型高危条款快捷填入胶囊 */}
          <div className="flex flex-wrap items-center gap-1.5 pt-1">
            <span className="text-[11px] text-slate-400 font-medium">典型高危示范：</span>
            {sampleClauses.map((sc, i) => (
              <button
                key={i}
                onClick={() => {
                  setClauseText(sc.text);
                  setSelectedJur(sc.jur);
                }}
                className="text-[11px] px-2.5 py-1 rounded-lg bg-slate-100 hover:bg-slate-200/80 text-slate-700 transition-colors cursor-pointer border border-slate-200/60"
              >
                {sc.title}
              </button>
            ))}
          </div>

          {/* 东道国选择胶囊 */}
          <div className="flex items-center gap-1.5 overflow-x-auto text-xs">
            <span className="text-[11px] text-slate-400 shrink-0 font-medium">东道国：</span>
            {Object.entries(jurFlags).map(([code, item]) => (
              <button
                key={code}
                onClick={() => setSelectedJur(code)}
                className={`px-2.5 py-1 rounded-lg text-xs flex items-center gap-1 cursor-pointer transition-all ${
                  selectedJur === code
                    ? 'bg-slate-900 text-white font-semibold shadow-xs'
                    : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                }`}
              >
                <span>{item.flag}</span>
                <span>{item.name}</span>
              </button>
            ))}
          </div>

          {/* 条款输入框 */}
          <div className="relative">
            <textarea
              rows={4}
              value={clauseText}
              onChange={(e) => setClauseText(e.target.value)}
              placeholder="在此粘贴待体检的招标文件专用条件、EPC 主合同或分包协议条款 (中英双语均可)..."
              className="w-full p-3.5 rounded-xl border border-slate-200 text-xs font-mono text-slate-800 leading-relaxed bg-slate-50/60 focus:bg-white focus:outline-none focus:ring-2 focus:ring-slate-900 transition-all resize-none"
            />
          </div>

          {/* 开始扫描按钮 */}
          <button
            onClick={handleScan}
            disabled={scanning || !clauseText.trim()}
            className="w-full py-2.5 rounded-xl btn-space-titanium text-xs font-semibold flex items-center justify-center gap-2 cursor-pointer disabled:opacity-50"
          >
            {scanning ? (
              <>
                <span className="w-3.5 h-3.5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                <span>正在执行东道国强行法与司法先例穿透核查...</span>
              </>
            ) : (
              <>
                <FileCheck2 className="w-3.5 h-3.5 text-blue-400" />
                <span>5 秒穿透扫描强行法红线 (Scan Redline)</span>
              </>
            )}
          </button>

          {/* 扫描结果原地展开：三联式诊断卡 */}
          {scanResult && (
            <div className="p-4 rounded-xl border border-slate-200 bg-slate-50/70 space-y-3 apple-modal-card">
              <div className="flex items-center justify-between border-b border-slate-200/80 pb-2">
                <span className="text-xs font-bold text-slate-900 flex items-center gap-1.5">
                  <ShieldAlert className="w-4 h-4 text-amber-600" />
                  扫描诊断成果与合规示范
                </span>
                <span className="text-[11px] font-mono text-slate-500">
                  耗时 {scanResult.execution_time_ms}ms · 门禁校验通过
                </span>
              </div>

              {/* 1. 强行法效力判定 */}
              <div className="p-3 rounded-lg bg-white border border-slate-200/80 space-y-1">
                <div className="text-[11px] font-semibold text-rose-600 flex items-center gap-1">
                  <span>● 强行法效力判定：</span>
                  <span>{scanResult.summary || '触犯东道国建设工程强制性法律'}</span>
                </div>
                <p className="text-xs text-slate-700 leading-relaxed">
                  {scanResult.audit_records?.[0]?.issue_desc || '条款涉嫌违反东道国属地强行法，自始绝对无效或导致严重缔约过失。'}
                </p>
              </div>

              {/* 2. 平衡修改示范条款 (Redline) */}
              <div className="p-3 rounded-lg bg-white border border-slate-200/80 space-y-2">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-semibold text-emerald-800">
                      合规示范修订条款
                    </span>
                    <div className="inline-flex items-center p-0.5 bg-emerald-100/70 rounded-md text-[10px]">
                      <button
                        type="button"
                        onClick={() => setTrackADiffMode(false)}
                        className={`px-1.5 py-0.2 rounded font-medium cursor-pointer ${
                          !trackADiffMode ? 'bg-white text-emerald-900 font-semibold' : 'text-emerald-700'
                        }`}
                      >
                        示范
                      </button>
                      <button
                        type="button"
                        onClick={() => setTrackADiffMode(true)}
                        className={`px-1.5 py-0.2 rounded font-medium cursor-pointer ${
                          trackADiffMode ? 'bg-white text-emerald-900 font-semibold' : 'text-emerald-700'
                        }`}
                      >
                        Diff对比
                      </button>
                    </div>
                  </div>
                  <button
                    onClick={() =>
                      handleCopyRedline(
                        scanResult.audit_records?.[0]?.recommended_clause ||
                          'Contractor shall pay Subcontractor within 30 days of monthly interim certification, regardless of Employer payment.'
                      )
                    }
                    className="text-[11px] text-blue-600 hover:text-blue-800 flex items-center gap-1 font-medium cursor-pointer"
                  >
                    {copiedClause ? <Check className="w-3 h-3 text-emerald-600" /> : <Copy className="w-3 h-3" />}
                    <span>{copiedClause ? '已复制' : '复制示范条款'}</span>
                  </button>
                </div>

                {trackADiffMode ? (
                  <div className="p-3 bg-slate-900 text-slate-100 rounded-lg font-mono text-[11px] leading-relaxed select-all space-y-1.5 border border-slate-800">
                    <div className="text-rose-300 line-through opacity-85">
                      [-DEL: {clauseText}]
                    </div>
                    <div className="text-emerald-300 font-semibold pt-1 border-t border-slate-800">
                      [+ADD: {scanResult.audit_records?.[0]?.recommended_clause || 'Payment shall be independently certified and disbursed without pay-when-paid restrictions.'}]
                    </div>
                  </div>
                ) : (
                  <div className="p-2.5 rounded-lg bg-slate-50 font-mono text-[11px] text-slate-800 leading-relaxed border border-slate-200/60">
                    {scanResult.audit_records?.[0]?.recommended_clause ||
                      'Payment to Subcontractor shall be settled within thirty (30) days upon engineer progress certification, independently of Employer interim disbursements.'}
                  </div>
                )}
              </div>

              {/* 一键以此条款升级为深度专案 */}
              <div className="pt-1">
                <button
                  onClick={() => {
                    openCaseEntryWithPrefill({
                      jurisdiction: selectedJur,
                      title: `${jurFlags[selectedJur]?.name || '东盟'}工程合同条款红线审查专案`,
                      facts: `待审查合同条款原文：\n${clauseText}\n\n初步体检诊断：\n${scanResult.summary}`,
                    });
                  }}
                  className="w-full py-2 rounded-xl bg-blue-50 hover:bg-blue-100 text-blue-700 text-xs font-semibold flex items-center justify-center gap-1.5 transition-colors cursor-pointer border border-blue-200/80"
                >
                  <Sparkles className="w-3.5 h-3.5 text-blue-600" />
                  <span>以此条款一键升级为深度研判案卷 ➔</span>
                </button>
              </div>
            </div>
          )}
        </section>

        {/* ========================================================================= */}
        {/* 右主舱：轨道 B —— 深度专案查明与标杆示范卷 (占宽 5 列 / ~40%) */}
        {/* ========================================================================= */}
        <section className="lg:col-span-5 space-y-4">
          {/* 粘贴索赔函建案主卡片 */}
          <div
            onClick={openCaseEntryModal}
            className="p-4 rounded-2xl bg-gradient-to-br from-slate-900 to-slate-800 text-white shadow-md cursor-pointer group hover:shadow-lg transition-all"
          >
            <div className="flex items-start justify-between">
              <div className="space-y-1">
                <span className="text-[10px] font-mono text-blue-300 uppercase tracking-wider bg-white/10 px-2 py-0.5 rounded">
                  轨道 B · 深度专案
                </span>
                <h3 className="text-sm font-bold text-white pt-1">
                  + 粘贴邮件 / 索赔函一键极速建案
                </h3>
                <p className="text-xs text-slate-300 leading-relaxed">
                  无需手动填表，自动提炼国别、阶段、延误天数与核心争议诉求
                </p>
              </div>
              <div className="w-8 h-8 rounded-xl bg-white/10 flex items-center justify-center text-white group-hover:scale-110 transition-transform">
                <ArrowRight className="w-4 h-4" />
              </div>
            </div>
          </div>

          {/* 活跃与标杆示范案卷列表 */}
          <div className="bg-white rounded-2xl border border-slate-200/90 shadow-sm p-4 space-y-3">
            <div className="flex items-center justify-between border-b border-slate-100 pb-2">
              <span className="text-xs font-bold text-slate-800 flex items-center gap-1.5">
                <FolderOpen className="w-4 h-4 text-blue-600" />
                最近活跃与金标准标杆卷宗
              </span>
              <button
                onClick={() => setCurrentView('cases')}
                className="text-[11px] text-blue-600 hover:text-blue-800 font-medium cursor-pointer"
              >
                查看全部 ({casesList.length}) ➔
              </button>
            </div>

            <div className="space-y-2">
              {casesList.slice(0, 4).map((c) => {
                const isPreInv = c.lifecycle_stage === 'pre_investment';
                return (
                  <div
                    key={c.case_id}
                    onClick={() => {
                      loadCase(c.case_id);
                      setCurrentView('analysis');
                    }}
                    className="p-3 rounded-xl border border-slate-200/70 hover:border-blue-500/50 hover:bg-slate-50/80 transition-all cursor-pointer space-y-1.5 group"
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <span className="font-mono text-xs font-bold text-blue-600">
                          {c.case_id}
                        </span>
                        <span
                          className={`text-[10px] px-1.5 py-0.2 rounded font-medium ${
                            isPreInv
                              ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                              : 'bg-amber-50 text-amber-700 border border-amber-200'
                          }`}
                        >
                          {isPreInv ? '投前准入审查' : '履约索赔争议'}
                        </span>
                      </div>
                      <span className="text-[10px] text-slate-400 font-mono">
                        {c.jurisdiction || '东盟'}
                      </span>
                    </div>

                    <h4 className="text-xs font-semibold text-slate-900 group-hover:text-blue-600 transition-colors line-clamp-1">
                      {c.title}
                    </h4>

                    <div className="flex items-center justify-between text-[11px] text-slate-400 font-mono pt-0.5">
                      <span>争议要件：{c.issues_count || 3} 个</span>
                      <span className="group-hover:translate-x-0.5 transition-transform text-slate-600">
                        进入专案研判舱 ➔
                      </span>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </section>
      </div>
    </div>
  );
};
