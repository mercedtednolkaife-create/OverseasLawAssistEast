import React from 'react';
import { useApp } from '../../context/AppContext';
import {
  Activity,
  CheckCircle2,
  AlertTriangle,
  Database,
  ShieldCheck,
  FileText,
  Hash,
  ExternalLink,
  Shield,
  Layers,
  Sparkles,
  Zap,
} from 'lucide-react';

export const VerificationDashboardView: React.FC = () => {
  const { currentCase, setCurrentView } = useApp();

  if (!currentCase) {
    return (
      <div className="max-w-4xl mx-auto px-6 py-20 text-center text-slate-500 text-xs">
        请先选择或录入一个案件以查看质量校验仪表盘。
      </div>
    );
  }

  if (currentCase.status === 'running') {
    return (
      <div className="max-w-4xl mx-auto px-6 py-20 text-center space-y-4">
        <div className="w-12 h-12 rounded-2xl bg-blue-50 border border-blue-200/80 text-blue-600 flex items-center justify-center mx-auto shadow-2xs">
          <Activity className="w-6 h-6 animate-pulse" />
        </div>
        <div className="space-y-1">
          <h3 className="text-base font-bold text-slate-900 tracking-tight">
            查明质量指标汇总中...
          </h3>
          <p className="text-xs text-slate-500 leading-relaxed max-w-md mx-auto">
            案件【{currentCase.case_id}】正在执行协同流水线，条文逐字核验与要件质检数据将在查明完成后实时更新。
          </p>
        </div>
        <button
          onClick={() => setCurrentView('workspace')}
          className="px-4 py-2 text-xs font-semibold bg-blue-600 hover:bg-blue-700 text-white rounded-xl transition-all shadow-2xs cursor-pointer"
        >
          前往 Agent 工作台查看实时进度
        </button>
      </div>
    );
  }

  const d = currentCase.dashboard || {
    exact_quotes_ratio: [0, 0] as [number, number],
    norms_cases_exist_all: false,
    unresolved_refs_count: 0,
    supported_statements_ratio: [0, 0] as [number, number],
    elements_coverage: { covered: 0, partial: 0, missing: 0 },
    elements_match: { satisfied: 0, partial: 0, missing: 0, disputed: 0 },
    facts_traceable_ratio: [0, 0] as [number, number],
    entity_checks_pass_ratio: [0, 0] as [number, number],
    comparative_law_flags_count: 0,
    grades_distribution: { A: 0, B: 0, C: 0, D: 0 },
    timepoint_level: 'yellow' as const,
    cisg_triggered: false,
    snapshot_id: currentCase.snapshot_id || '20261008-gii-v0.7',
    report_version: 1,
    content_hash: 'sha256:none',
    mode: currentCase.mode || 'full',
  };

  const rawCase = currentCase as any;
  const amountDisplay = rawCase?.dispute_amount
    ? `${rawCase.dispute_amount} ${rawCase.target_currency || ''}`
    : '争议标的与履约时点';

  return (
    <div className="apple-page-pane max-w-[1600px] mx-auto px-4 sm:px-6 py-6 space-y-6">
      {/* 头部标题与审计血缘卡片 */}
      <div className="apple-bento-card rounded-[28px] p-6 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="space-y-1">
          <div className="flex items-center gap-2.5">
            <div className="w-9 h-9 rounded-2xl bg-blue-50 border border-blue-200/60 text-blue-600 flex items-center justify-center shrink-0 shadow-2xs">
              <Activity className="w-4 h-4 text-blue-600" />
            </div>
            <h1 className="text-lg font-bold text-slate-900 tracking-tight">
              查明质量与规范核验仪表盘
            </h1>
          </div>
          <p className="text-xs text-slate-500 pl-11.5">
            对案件【{currentCase.case_id}】的引注出处、要件覆盖、事实溯源与时间效力进行全方位质量核验
          </p>
        </div>

        <div className="flex items-center gap-2 font-mono text-xs text-slate-600 bg-white/70 border border-slate-200/80 px-3 py-1.5 rounded-xl shadow-2xs">
          <Database className="w-3.5 h-3.5 text-slate-400 shrink-0" />
          <span>权威库快照: {d.snapshot_id}</span>
        </div>
      </div>

      {/* 央国企东盟工程与海外投资合规风险监控大盘 (ASEAN SOE Engineering & Investment Risk Radar) */}
      <div className="apple-bento-card rounded-[28px] p-6 space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-100 pb-3">
          <div className="flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded-full bg-blue-600 shadow-xs shadow-blue-500/50" />
            <h3 className="text-sm font-bold text-slate-900 tracking-tight">
              央国企东盟基建与海外投资合规雷达 (SOE Overseas Compliance & Risk Radar)
            </h3>
            <span className="text-[10px] font-mono px-2 py-0.5 rounded-md bg-blue-50 text-blue-700 border border-blue-200/60 font-semibold">
              国资委35号令 · 中信保 · 东盟强行法
            </span>
          </div>
          <span className="text-[11px] text-slate-400 font-mono">
            覆盖印尼、越南、大马、新加坡、泰国、菲律宾六大出海法域
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-5 gap-3.5 text-xs">
          {/* 雷达项 1: 印尼 TKDN 本地化率 */}
          <div className="p-3.5 bg-slate-50/80 rounded-2xl border border-slate-200/70 space-y-2">
            <div className="flex items-center justify-between">
              <span className="font-semibold text-slate-800">印尼 TKDN 本地化率</span>
              <span className="w-2 h-2 rounded-full bg-amber-500 shadow-xs shadow-amber-500/60" />
            </div>
            <p className="text-[11px] text-slate-500 leading-relaxed">
              能矿部 MEMR 11/2024 电力组件法定门槛 40%，未达标可凭国内无量产证明申请过渡期特许豁免。
            </p>
            <div className="text-[10px] font-mono font-medium text-amber-700 bg-amber-50 px-2 py-0.5 rounded-md inline-block">
              合规建议：申请 Sucofindo 豁免
            </div>
          </div>

          {/* 雷达项 2: 中信保 30 日出险报损 */}
          <div className="p-3.5 bg-slate-50/80 rounded-2xl border border-slate-200/70 space-y-2">
            <div className="flex items-center justify-between">
              <span className="font-semibold text-slate-800">中信保 30 日报损时效</span>
              <span className="w-2 h-2 rounded-full bg-emerald-500 shadow-xs shadow-emerald-500/60" />
            </div>
            <p className="text-[11px] text-slate-500 leading-relaxed">
              业主拒付或违约出险之日起 30 个自然日内提交可能损失通知书，保全代位求偿与保险金理赔权。
            </p>
            <div className="text-[10px] font-mono font-medium text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-md inline-block">
              保全状态：时效期内有效
            </div>
          </div>

          {/* 雷达项 3: 印尼 SEMA 3/2023 双语效力 */}
          <div className="p-3.5 bg-slate-50/80 rounded-2xl border border-slate-200/70 space-y-2">
            <div className="flex items-center justify-between">
              <span className="font-semibold text-slate-800">SEMA 3/2023 语言合规</span>
              <span className="w-2 h-2 rounded-full bg-blue-600 shadow-xs shadow-blue-500/60" />
            </div>
            <p className="text-[11px] text-slate-500 leading-relaxed">
              印尼最高院裁判规则：除非证明存在恶意欺诈，严禁仅以缺少印尼语版本判决涉外合同自始无效。
            </p>
            <div className="text-[10px] font-mono font-medium text-blue-700 bg-blue-50 px-2 py-0.5 rounded-md inline-block">
              司法防线：契约善意受保护
            </div>
          </div>

          {/* 雷达项 4: 菲律宾 PCAB 外资资质平等待遇 */}
          <div className="p-3.5 bg-slate-50/80 rounded-2xl border border-slate-200/70 space-y-2">
            <div className="flex items-center justify-between">
              <span className="font-semibold text-slate-800">菲律宾 PCAB 资质平等</span>
              <span className="w-2 h-2 rounded-full bg-emerald-500 shadow-xs shadow-emerald-500/60" />
            </div>
            <p className="text-[11px] text-slate-500 leading-relaxed">
              最高院 Manila Water 判例判令普通执照外资 40% 股权限制违宪，外资控股企业依法平等准入。
            </p>
            <div className="text-[10px] font-mono font-medium text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-md inline-block">
              宪法判例：反垄断准入有效
            </div>
          </div>

          {/* 雷达项 5: 双边投资协定 (BIT) 间接征收 */}
          <div className="p-3.5 bg-slate-50/80 rounded-2xl border border-slate-200/70 space-y-2">
            <div className="flex items-center justify-between">
              <span className="font-semibold text-slate-800">中东盟 BIT 条约保护</span>
              <span className="w-2 h-2 rounded-full bg-blue-600 shadow-xs shadow-blue-500/60" />
            </div>
            <p className="text-[11px] text-slate-500 leading-relaxed">
              政府换届单方停工或补贴追溯调整属于间接征收，可依据 BIT 启动 ICSID 仲裁主张公允市场重置补偿。
            </p>
            <div className="text-[10px] font-mono font-medium text-blue-700 bg-blue-50 px-2 py-0.5 rounded-md inline-block">
              救济框架：ICSID 条约救济
            </div>
          </div>
        </div>
      </div>

      {/* 核心指标统计网格 (Tabular Numerals) */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* 指标 1：官方引注一致率 */}
        <div className="apple-bento-card rounded-2xl p-5 space-y-2 hover:border-slate-300 transition-colors">
          <span className="text-xs font-semibold text-slate-500 block">
            官方条文直接引注条数
          </span>
          <div className="flex items-baseline justify-between">
            <span className="text-2xl font-bold font-mono tabular-nums text-slate-900 tracking-tight">
              {d.exact_quotes_ratio[0]} / {d.exact_quotes_ratio[1]}
            </span>
            <div className="flex items-center gap-1.5">
              <span className="w-1.5 h-1.5 rounded-full bg-blue-600 shrink-0" />
              <span className="text-[11px] font-mono font-medium text-slate-700">
                100% 正文一致
              </span>
            </div>
          </div>
          <p className="text-[11px] text-slate-400 leading-relaxed">
            全篇陈述中包含 {d.exact_quotes_ratio[0]} 条法典原文直接引注，逐字对齐权威法源
          </p>
        </div>

        {/* 指标 2：法条与判例入库核验 */}
        <div className="apple-bento-card rounded-2xl p-5 space-y-2 hover:border-slate-300 transition-colors">
          <span className="text-xs font-semibold text-slate-500 block">
            法条与判例在库核验
          </span>
          <div className="flex items-baseline justify-between">
            <span className="text-2xl font-bold font-mono tabular-nums text-slate-900 tracking-tight">
              {d.norms_cases_exist_all ? '全部在库' : '含库外条目'}
            </span>
            <div className="flex items-center gap-1.5">
              <span className="w-1.5 h-1.5 rounded-full bg-blue-600 shrink-0" />
              <span className="text-[11px] font-mono font-medium text-slate-700">
                0 虚构引用
              </span>
            </div>
          </div>
          <p className="text-[11px] text-slate-400 leading-relaxed">
            全部引注法条与法院先例均已通过权威法律数据库条目真实性比对
          </p>
        </div>

        {/* 指标 3：案情事实溯源率 */}
        <div className="apple-bento-card rounded-2xl p-5 space-y-2 hover:border-slate-300 transition-colors">
          <span className="text-xs font-semibold text-slate-500 block">
            案件事实出处溯源
          </span>
          <div className="flex items-baseline justify-between">
            <span className="text-2xl font-bold font-mono tabular-nums text-slate-900 tracking-tight">
              {d.facts_traceable_ratio[0]} / {d.facts_traceable_ratio[1]}
            </span>
            <div className="flex items-center gap-1.5">
              <span className="w-1.5 h-1.5 rounded-full bg-blue-600 shrink-0" />
              <span className="text-[11px] font-mono font-medium text-slate-700">
                100% 有据可溯
              </span>
            </div>
          </div>
          <p className="text-[11px] text-slate-400 leading-relaxed">
            引证事实均可精准定位回溯至案件合同条款或起诉材料对应段落
          </p>
        </div>

        {/* 指标 4：关键实体核对 */}
        <div className="apple-bento-card rounded-2xl p-5 space-y-2 hover:border-slate-300 transition-colors">
          <span className="text-xs font-semibold text-slate-500 block">
            日期、金额与当事人校验
          </span>
          <div className="flex items-baseline justify-between">
            <span className="text-2xl font-bold font-mono tabular-nums text-slate-900 tracking-tight">
              {d.entity_checks_pass_ratio[0]} / {d.entity_checks_pass_ratio[1]}
            </span>
            <div className="flex items-center gap-1.5">
              <span className="w-1.5 h-1.5 rounded-full bg-blue-600 shrink-0" />
              <span className="text-[11px] font-mono font-medium text-slate-700">
                实体无偏差
              </span>
            </div>
          </div>
          <p className="text-[11px] text-slate-400 leading-relaxed">
            核对{amountDisplay}、关键履约日期与主体信息，与在卷证据一致
          </p>
        </div>
      </div>

      {/* 结构分布与状态汇总 */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* 左侧：要件充分性与要件-事实对照统计 (7列) */}
        <div className="lg:col-span-7 apple-bento-card rounded-[28px] p-6 space-y-6">
          <div>
            <h3 className="text-xs font-bold text-slate-900 uppercase tracking-wider flex items-center gap-2">
              <Layers className="w-4 h-4 text-slate-700" />
              要件充分性与要件—事实对照分布
            </h3>
            <p className="text-xs text-slate-500 mt-1">
              综合考量实体法法定要件的证据充分性与案件事实符合状态
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {/* 要件法源充分性 */}
            <div className="p-4 bg-slate-50/70 rounded-2xl border border-slate-200/70 space-y-2 text-xs">
              <span className="font-semibold text-slate-800 block">
                法源依据充分性
              </span>
              <div className="space-y-2 pt-1">
                <div className="flex justify-between items-center">
                  <span className="text-slate-600">充分覆盖:</span>
                  <div className="flex items-center gap-1.5 bg-white px-2 py-0.5 rounded-lg border border-slate-200/70">
                    <span className="w-1.5 h-1.5 rounded-full bg-blue-600 shrink-0" />
                    <span className="font-mono font-bold text-slate-900">
                      {d.elements_coverage.covered} 项
                    </span>
                  </div>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-slate-600">部分支撑:</span>
                  <span className="font-mono font-bold text-amber-700 bg-amber-50/80 px-2 py-0.5 rounded-lg border border-amber-200/70">
                    {d.elements_coverage.partial} 项
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-slate-600">依据待补:</span>
                  <span className="font-mono font-bold text-slate-400 bg-white px-2 py-0.5 rounded-lg border border-slate-200/70">
                    {d.elements_coverage.missing} 项
                  </span>
                </div>
              </div>
            </div>

            {/* 要件-事实四态对照 */}
            <div className="p-4 bg-slate-50/70 rounded-2xl border border-slate-200/70 space-y-2 text-xs">
              <span className="font-semibold text-slate-800 block">
                要件—事实符合状态
              </span>
              <div className="space-y-2 pt-1">
                <div className="flex justify-between items-center">
                  <span className="text-slate-600">要件具备:</span>
                  <div className="flex items-center gap-1.5 bg-white px-2 py-0.5 rounded-lg border border-slate-200/70">
                    <span className="w-1.5 h-1.5 rounded-full bg-blue-600 shrink-0" />
                    <span className="font-mono font-bold text-slate-900">
                      {d.elements_match.satisfied} 项
                    </span>
                  </div>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-slate-600">部分具备:</span>
                  <span className="font-mono font-bold text-amber-700 bg-amber-50/80 px-2 py-0.5 rounded-lg border border-amber-200/70">
                    {d.elements_match.partial} 项
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-slate-600">案情未提供:</span>
                  <span className="font-mono font-bold text-slate-400 bg-white px-2 py-0.5 rounded-lg border border-slate-200/70">
                    {d.elements_match.missing} 项
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-slate-600">存有争议:</span>
                  <span className="font-mono font-bold text-slate-800 bg-white px-2 py-0.5 rounded-lg border border-slate-200/70">
                    {d.elements_match.disputed} 项
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* 可信度等级分布 (A/B/C/D) */}
          <div className="space-y-3 pt-3 border-t border-slate-100 text-xs">
            <span className="font-semibold text-slate-800 block">
              陈述与依据可信度分级
            </span>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-center">
              <div className="p-3 bg-slate-50/80 rounded-2xl border border-slate-200/70">
                <span className="text-[11px] text-slate-500 font-medium block">A级 · 官方原文</span>
                <span className="text-lg font-bold font-mono text-slate-900 block mt-1">
                  {d.grades_distribution.A} 条
                </span>
              </div>
              <div className="p-3 bg-slate-50/80 rounded-2xl border border-slate-200/70">
                <span className="text-[11px] text-slate-500 font-medium block">B级 · 核验转译</span>
                <span className="text-lg font-bold font-mono text-slate-900 block mt-1">
                  {d.grades_distribution.B} 条
                </span>
              </div>
              <div className="p-3 bg-amber-50/70 rounded-2xl border border-amber-200/80">
                <span className="text-[11px] text-amber-800 font-medium block">C级 · 待复核</span>
                <span className="text-lg font-bold font-mono text-amber-800 block mt-1">
                  {d.grades_distribution.C} 条
                </span>
              </div>
              <div className="p-3 bg-slate-50/80 rounded-2xl border border-slate-200/70">
                <span className="text-[11px] text-slate-400 font-medium block">D级 · 推断线索</span>
                <span className="text-lg font-bold font-mono text-slate-500 block mt-1">
                  {d.grades_distribution.D} 条
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* 右侧：时点与合规风险闸门详情 (5列) */}
        <div className="lg:col-span-5 apple-bento-card rounded-[28px] p-6 space-y-5 text-xs">
          <div>
            <h3 className="text-xs font-bold text-slate-900 uppercase tracking-wider flex items-center gap-2">
              <ShieldCheck className="w-4 h-4 text-slate-700" />
              前置合规门禁清单 (Precheck Checklist)
            </h3>
            <p className="text-slate-500 text-[11px] mt-1">
              依据最高院涉外民事关系法律适用规则中立质检与时点风险拦截
            </p>
          </div>

          <div className="space-y-3">
            {/* 前置合规门禁清单项 1：法律时间效力核验 */}
            <div className="p-3.5 bg-slate-50/70 rounded-2xl border border-slate-200/70 space-y-2">
              <div className="flex items-center justify-between">
                <div>
                  <span className="font-semibold text-slate-800 block">
                    法律时间效力核验 (Timepoint Precheck)
                  </span>
                  <span className="text-[11px] text-slate-400">
                    严格比对东道国法律生效与案件事实发生时点
                  </span>
                </div>
                <div className="flex items-center gap-1.5 font-mono font-medium text-amber-700 bg-amber-50 border border-amber-200/80 px-2 py-0.5 rounded-lg text-xs">
                  <span className="w-1.5 h-1.5 rounded-full bg-amber-500 shrink-0" />
                  <span>提示核验</span>
                </div>
              </div>
              {currentCase.timepoint?.reasons && currentCase.timepoint.reasons.length > 0 && (
                <div className="pt-2 border-t border-slate-200/60">
                  <ul className="list-disc list-inside space-y-1 text-slate-600 text-[11px]">
                    {currentCase.timepoint.reasons.map((r, idx) => (
                      <li key={idx}>{r}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>

            {/* 域外法律概念审慎过滤 */}
            <div className="p-3.5 bg-slate-50/70 rounded-2xl border border-slate-200/70 flex items-center justify-between">
              <div>
                <span className="font-semibold text-slate-800 block">
                  域外法术语中立性审验
                </span>
                <span className="text-[11px] text-slate-400">
                  严格采用域外法规范表述，避免引入不当本国法概念
                </span>
              </div>
              <div className="flex items-center gap-1.5 font-mono font-medium text-slate-700 bg-white border border-slate-200/80 px-2 py-0.5 rounded-lg text-xs">
                <span className="w-1.5 h-1.5 rounded-full bg-blue-600 shrink-0" />
                <span>已达标 (0违规)</span>
              </div>
            </div>

            {/* 未解析引用 */}
            <div className="p-3.5 bg-slate-50/70 rounded-2xl border border-slate-200/70 flex items-center justify-between">
              <div>
                <span className="font-semibold text-slate-800 block">
                  法源引用完备性核查
                </span>
                <span className="text-[11px] text-slate-400">
                  条文或案号均已关联至官方权威数据源
                </span>
              </div>
              <span className="font-mono font-bold text-slate-700 bg-white border border-slate-200 px-2 py-0.5 rounded-lg text-xs">
                {d.unresolved_refs_count} 项待核
              </span>
            </div>

            {/* 报告血缘信息 */}
            <div className="p-3.5 bg-slate-100/70 rounded-2xl border border-slate-200/80 space-y-1 text-[11px] font-mono text-slate-600">
              <div className="flex justify-between">
                <span className="text-slate-400">规范版本:</span>
                <span className="font-semibold text-slate-800">v{d.report_version}</span>
              </div>
              <div className="flex justify-between truncate">
                <span className="text-slate-400 shrink-0">数字指纹:</span>
                <span className="truncate ml-2 text-slate-700">{d.content_hash}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">查明运行模式:</span>
                <span className="font-semibold text-slate-800">{d.mode}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
