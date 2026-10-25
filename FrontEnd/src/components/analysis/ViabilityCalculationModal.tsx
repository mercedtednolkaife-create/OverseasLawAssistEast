import React from 'react';
import { X, Layers, Swords, BookOpen, CheckCircle2, ShieldCheck, Calculator } from 'lucide-react';

interface ViabilityAssessment {
  overallScore: number;
  ratingLabel: string;
  ratingLevel: 'high' | 'medium' | 'low';
  elementsScore: number;
  elementsDetail: string;
  defenseScore: number;
  defenseDetail: string;
  authorityScore: number;
  authorityDetail: string;
  complianceScore: number;
  complianceDetail: string;
}

interface ViabilityCalculationModalProps {
  isOpen: boolean;
  onClose: () => void;
  assessment: ViabilityAssessment;
  isPreInvestment?: boolean;
}

export const ViabilityCalculationModal: React.FC<ViabilityCalculationModalProps> = ({
  isOpen,
  onClose,
  assessment,
  isPreInvestment = false,
}) => {
  if (!isOpen) return null;

  // 各项加权贡献分
  const elemContrib = (assessment.elementsScore * 0.4).toFixed(1);
  const defContrib = (assessment.defenseScore * 0.3).toFixed(1);
  const authContrib = (assessment.authorityScore * 0.15).toFixed(1);
  const compContrib = (assessment.complianceScore * 0.15).toFixed(1);

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/40 backdrop-blur-md antialiased apple-modal-backdrop"
      onClick={onClose}
    >
      <div
        className="w-full max-w-2xl bg-white rounded-[28px] shadow-[0_24px_64px_rgba(0,0,0,0.18)] border border-black/[0.08] overflow-hidden flex flex-col max-h-[90vh] apple-modal-card"
        onClick={(e) => e.stopPropagation()}
      >
        {/* 头部 */}
        <div className="px-7 py-5 bg-white border-b border-slate-100 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <span className="p-2.5 rounded-2xl bg-slate-100 text-slate-800 border border-slate-200/60">
              <Calculator className="w-4 h-4" />
            </span>
            <div>
              <h3 className="text-base font-semibold text-slate-900 tracking-tight">
                {isPreInvestment ? '东盟投前合规就绪与落地指数测算依据' : '涉外争议裁决胜诉与抗辩量化测算依据'}
              </h3>
              <p className="text-xs text-slate-500 mt-0.5">
                {isPreInvestment
                  ? '基于外资股比准入、东道国强行法防线、双边条约救济与央国企安全哨兵的 4 维量化模型'
                  : '基于请求权要件齐备、程序失权抵御、官方权威法源与涉外司法质检的 4 维量化模型'}
              </p>
            </div>
          </div>
          <button
            type="button"
            onClick={onClose}
            className="p-2 rounded-full text-slate-400 hover:text-slate-700 hover:bg-slate-100 transition-colors cursor-pointer"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* 主体滚动区 */}
        <div className="p-7 overflow-y-auto space-y-5 text-xs">
          {/* 综合分与公式卡片 */}
          <div className="p-5 rounded-2xl bg-gradient-to-br from-slate-900 to-slate-800 text-white space-y-3 shadow-sm">
            <div className="flex items-center justify-between">
              <span className="text-slate-400 font-mono text-[11px] uppercase tracking-wider">
                {isPreInvestment ? 'PRE-INVESTMENT READINESS MODEL' : 'DISPUTE VIABILITY MODEL'}
              </span>
              <div className="flex items-center gap-1.5 text-xs text-slate-300">
                <span
                  className={`w-1.5 h-1.5 rounded-full shrink-0 ${
                    assessment.ratingLevel === 'high'
                      ? 'bg-emerald-400'
                      : assessment.ratingLevel === 'medium'
                      ? 'bg-blue-400'
                      : 'bg-amber-400'
                  }`}
                />
                <span className="font-medium">{assessment.ratingLabel}</span>
              </div>
            </div>
            <div className="flex items-baseline gap-2">
              <span className="text-4xl font-semibold font-mono text-white tracking-tight tabular-nums">
                {assessment.overallScore}%
              </span>
              <span className="text-slate-400 text-xs">
                {isPreInvestment ? '投前准入落地就绪度指数' : '索赔胜诉与抗辩综合指数'}
              </span>
            </div>
            <div className="pt-2.5 border-t border-white/10 font-mono text-[11px] text-slate-300 leading-relaxed">
              {isPreInvestment
                ? '加权公式 = 40% × 准入要件齐备 + 30% × 监管抗辩抵御 + 15% × 官方权威法源 + 15% × 出海国家安全质检'
                : '加权公式 = 40% × 实体请求权要件 + 30% × 程序失权与保函反制 + 15% × 官方权威法源 + 15% × 涉外司法质检'}
            </div>
          </div>

          {/* 4 大维度明细卡 */}
          <div className="space-y-3">
            <span className="text-xs font-semibold text-slate-700 block">
              各维度权重构成与客观依据
            </span>

            {/* 维度 1 */}
            <div className="p-4 rounded-2xl bg-slate-50/80 border border-slate-100 space-y-2">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2.5">
                  <Layers className="w-4 h-4 text-slate-500" />
                  <span className="font-semibold text-slate-900 text-xs sm:text-sm">
                    {isPreInvestment ? '1. 外资准入与东道国强行法要件齐备度 (权重 40%)' : '1. 实体请求权构成要件齐备度 (权重 40%)'}
                  </span>
                </div>
                <div className="flex items-baseline gap-1.5 font-mono">
                  <span className="font-semibold text-slate-900 text-sm tabular-nums">{assessment.elementsScore}%</span>
                  <span className="text-slate-400 text-[11px]">(贡献 {elemContrib} 分)</span>
                </div>
              </div>
              <p className="text-slate-600 leading-relaxed pl-6.5 text-xs">
                依据：{assessment.elementsDetail}
              </p>
            </div>

            {/* 维度 2 */}
            <div className="p-4 rounded-2xl bg-slate-50/80 border border-slate-100 space-y-2">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2.5">
                  <Swords className="w-4 h-4 text-slate-500" />
                  <span className="font-semibold text-slate-900 text-xs sm:text-sm">
                    {isPreInvestment ? '2. 政策变动与东道国监管抗辩抵御力 (权重 30%)' : '2. 程序失权抗辩与保函止付反制力 (权重 30%)'}
                  </span>
                </div>
                <div className="flex items-baseline gap-1.5 font-mono">
                  <span className="font-semibold text-slate-900 text-sm tabular-nums">{assessment.defenseScore}%</span>
                  <span className="text-slate-400 text-[11px]">(贡献 {defContrib} 分)</span>
                </div>
              </div>
              <p className="text-slate-600 leading-relaxed pl-6.5 text-xs">
                依据：{assessment.defenseDetail}
              </p>
            </div>

            {/* 维度 3 */}
            <div className="p-4 rounded-2xl bg-slate-50/80 border border-slate-100 space-y-2">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2.5">
                  <BookOpen className="w-4 h-4 text-slate-500" />
                  <span className="font-semibold text-slate-900 text-xs sm:text-sm">
                    {isPreInvestment ? '3. 官方投资协定与东道国规范权威度 (权重 15%)' : '3. 涉外法典判例与国际公约权威度 (权重 15%)'}
                  </span>
                </div>
                <div className="flex items-baseline gap-1.5 font-mono">
                  <span className="font-semibold text-slate-900 text-sm tabular-nums">{assessment.authorityScore}%</span>
                  <span className="text-slate-400 text-[11px]">(贡献 {authContrib} 分)</span>
                </div>
              </div>
              <p className="text-slate-600 leading-relaxed pl-6.5 text-xs">
                依据：{assessment.authorityDetail}
              </p>
            </div>

            {/* 维度 4 */}
            <div className="p-4 rounded-2xl bg-slate-50/80 border border-slate-100 space-y-2">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2.5">
                  <CheckCircle2 className="w-4 h-4 text-slate-500" />
                  <span className="font-semibold text-slate-900 text-xs sm:text-sm">
                    {isPreInvestment ? '4. 央国企涉外合规与信保质检通过率 (权重 15%)' : '4. 涉外司法防线质检通过率 (权重 15%)'}
                  </span>
                </div>
                <div className="flex items-baseline gap-1.5 font-mono">
                  <span className="font-semibold text-slate-900 text-sm tabular-nums">{assessment.complianceScore}%</span>
                  <span className="text-slate-400 text-[11px]">(贡献 {compContrib} 分)</span>
                </div>
              </div>
              <p className="text-slate-600 leading-relaxed pl-6.5 text-xs">
                依据：{assessment.complianceDetail}
              </p>
            </div>
          </div>

          {/* 司法规范提示 */}
          <div className="p-4 bg-slate-50 rounded-2xl border border-slate-100 flex items-start gap-3 text-slate-600 text-xs leading-relaxed">
            <ShieldCheck className="w-4 h-4 text-slate-500 shrink-0 mt-0.5" />
            <div>
              <strong className="text-slate-800">法律科技合规说明：</strong>
              {isPreInvestment
                ? '本测算严格基于东盟东道国外商投资法律、建设工程资质管理条例与中外双边投资保护协定展开，所呈指数反映“跨境投资落地合规度与风险可控度”，供投资并购与投标决策参考。'
                : '本测算严格基于在卷客观证据材料与官方现行法律规范展开，所呈指数反映“实体请求权胜诉确定性与程序抗辩阻断力”，供诉讼应对与和解决策参考。'}
            </div>
          </div>
        </div>

        {/* 底部按钮 */}
        <div className="px-7 py-4 bg-slate-50/60 border-t border-slate-100 flex items-center justify-end">
          <button
            type="button"
            onClick={onClose}
            className="px-5 py-2 text-xs font-medium text-slate-700 bg-white hover:bg-slate-100 border border-slate-200/80 rounded-xl transition-all cursor-pointer shadow-2xs"
          >
            完成审阅
          </button>
        </div>
      </div>
    </div>
  );
};
