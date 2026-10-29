import React, { useState, useEffect, useMemo } from 'react';
import {
  X,
  Check,
  ChevronRight,
  FileText,
  ShieldCheck,
} from 'lucide-react';

export interface PipelineCaseMeta {
  id?: string;
  title: string;
  criticalDate?: string;
  contractAmount?: number;
  coverDiffAmount?: number;
  buyerCountry?: string;
  sellerCountry?: string;
  jurisdiction?: 'asean_id' | 'asean_vn' | 'asean_my' | 'asean_sg' | 'asean_th' | 'asean_ph' | string;
  stage?: string;
  isPreInvestment?: boolean;
}

interface CasePipelineAnimationModalProps {
  isOpen: boolean;
  onClose: () => void;
  onComplete?: () => void;
  caseMeta?: PipelineCaseMeta;
}

// 5 阶段查明流水线定义，文字纯净精炼，节奏平衡自然
export const buildPipelineStages = (caseMeta?: PipelineCaseMeta) => {
  const isPreInv =
    caseMeta?.isPreInvestment ||
    caseMeta?.stage === 'pre_investment' ||
    (caseMeta?.title && (caseMeta.title.includes('并购') || caseMeta.title.includes('PPP') || caseMeta.title.includes('投资')));

  if (isPreInv) {
    return [
      {
        id: 'asean-gate',
        stepNumber: '01',
        title: 'Agent正在执行投资准入识别、东道国外资限制与央企合规前置审查',
        coreAction: '核验东道国外商投资负面清单（泰FBA/菲PCAB/印尼投资法）、土地所有权限制及国资委35号令门禁',
        durationMs: 3200,
        pills: ['东道国外资准入', '负面清单核查', '国资委35号令门禁'],
      },
      {
        id: 'decomposition',
        stepNumber: '02',
        title: 'Agent正在执行跨境投资与工程准入合规要项结构化拆解',
        coreAction: '将投资合规要项拆解为外资股权红线(40%)、本地化率(TKDN)、PPP特许经营换届征收与中信保30日报损',
        durationMs: 3200,
        pills: ['外资持股比例', 'TKDN/准入牌照', '中信保报损时效'],
      },
      {
        id: 'hybrid-rag',
        stepNumber: '03',
        title: 'Agent正在执行东盟外资法典、BOI政策通告与特许经营判例检索',
        coreAction: '检索东道国外资法典、菲律宾Manila Water判例、中菲/中越双边投资协定(BIT)与PPP法典现行规范',
        durationMs: 3200,
        pills: ['外资保护条约', '权威司法先例', 'BOI投资优惠'],
      },
      {
        id: 'verification',
        stepNumber: '04',
        title: 'Agent正在执行东道国政府批文防伪与投前尽调证据闭环核验',
        coreAction: '对齐东道国投资部(BKPM/BOI)官方正本，核验特许权协议、征地环评批文与合资联营架构真实性',
        durationMs: 3200,
        pills: ['投资部一手批文', '尽调证据链闭环', '穿透式合规审查'],
      },
      {
        id: 'synthesis',
        stepNumber: '05',
        title: 'Agent正在执行投前准入构成要件评估与合规落地审查意见书生成',
        coreAction: '完成准入要件充分性评估与投资架构对冲设计，生成投前合规审查意见书与双包落地指引',
        durationMs: 3200,
        pills: ['准入合规评估', '投资对冲方案', '合规意见书就绪'],
      },
    ];
  }

  return [
    {
      id: 'asean-gate',
      stepNumber: '01',
      title: 'Agent正在执行准据法识别、东道国强行法与央企安全审查',
      coreAction: '核验合同选法有效性、东道国强行法（印尼建筑法/越南新建设法/马来CIPAA）及国资委35号令安全门禁',
      durationMs: 3200,
      pills: ['东道国准据法', '强行法审查', '国资委35号令门禁'],
    },
    {
      id: 'decomposition',
      stepNumber: '02',
      title: 'Agent正在执行涉外建设工程争议焦点结构化拆解',
      coreAction: '将工程诉求拆解为工期顺延(EOT)、FIDIC 20.1 28天索赔失权通知、背靠背付款及本地化率(TKDN)争点',
      durationMs: 3200,
      pills: ['FIDIC 8.4/20.1 时效', '背靠背付款效力', 'TKDN 配额审查'],
    },
    {
      id: 'hybrid-rag',
      stepNumber: '03',
      title: 'Agent正在执行东盟法典、司法通告与工程裁判先例检索',
      coreAction: '检索东道国成文法典、印尼SEMA 3/2023、新加坡BS Mount Sophia保函止付先例与FIDIC通用条件',
      durationMs: 3200,
      pills: ['东盟现行法条', '权威裁判先例', 'FIDIC GC vs PC'],
    },
    {
      id: 'verification',
      stepNumber: '04',
      title: 'Agent正在执行司法部“法通网”官方规范防伪与工程证据核验',
      coreAction: '对齐司法部法通网与东盟一手正本，完成停工令、工程师指令、签证单与第三方认证真实性核验',
      durationMs: 3200,
      pills: ['官方多语正本', '工程留痕证据闭环', '三道防线合规审查'],
    },
    {
      id: 'synthesis',
      stepNumber: '05',
      title: 'Agent正在执行法定构成要件审查与央企合规查明意见书生成',
      coreAction: '完成违约责任阻断与保函止付构成要件核验，生成出海基建央企法庭级查明意见书与信保保全指引',
      durationMs: 3200,
      pills: ['法定构成要件审查', '保函抗辩救济', '查明意见书就绪'],
    },
  ];
};
export const CasePipelineAnimationModal: React.FC<CasePipelineAnimationModalProps> = ({
  isOpen,
  onClose,
  onComplete,
  caseMeta = {
    title: '印尼爪哇燃煤/光伏混动电站 EPC 征地迟延与 TKDN 争议案',
    buyerCountry: '中国',
    sellerCountry: '印度尼西亚',
    jurisdiction: 'asean_id',
  },
}) => {
  const stages = useMemo(() => buildPipelineStages(caseMeta), [caseMeta]);
  const [activeIndex, setActiveIndex] = useState(0);
  const [stageProgress, setStageProgress] = useState(0);
  const [isFinished, setIsFinished] = useState(false);

  useEffect(() => {
    if (isOpen) {
      setActiveIndex(0);
      setStageProgress(0);
      setIsFinished(false);
    }
  }, [isOpen]);

  // 平滑过渡定时器
  useEffect(() => {
    if (!isOpen || isFinished) return;
    const currentStage = stages[activeIndex];
    const duration = currentStage.durationMs || 3200;
    const intervalMs = 40;
    const increment = (intervalMs / duration) * 100;

    const timer = setInterval(() => {
      setStageProgress((prev) => {
        if (prev + increment >= 100) {
          if (activeIndex < stages.length - 1) {
            setActiveIndex((idx) => idx + 1);
            return 0;
          } else {
            setIsFinished(true);
            return 100;
          }
        }
        return prev + increment;
      });
    }, intervalMs);

    return () => clearInterval(timer);
  }, [isOpen, isFinished, activeIndex, stages]);

  // 完成后平滑自动切入案卷分析 (留存 1.6s 供用户感知推演完毕)
  useEffect(() => {
    if (isFinished && isOpen) {
      const autoTimer = setTimeout(() => {
        if (onComplete) onComplete();
      }, 1600);
      return () => clearTimeout(autoTimer);
    }
  }, [isFinished, isOpen, onComplete]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6 overflow-hidden select-none animate-in fade-in duration-300">
      {/* 磨砂半透明遮罩 */}
      <div
        className="fixed inset-0 bg-slate-950/40 backdrop-blur-xl transition-opacity"
        onClick={onClose}
      />

      <div className="relative z-10 w-full max-w-4xl flex flex-col items-center">
        {/* 顶部控制栏 - 极简纯净 Apple Bento Glass 风格 */}
        <div className="w-full flex items-center justify-between gap-3 mb-4 px-6 py-4 bg-white/95 backdrop-blur-2xl border border-slate-200/90 rounded-[28px] shadow-[0_8px_30px_rgba(0,0,0,0.06)]">
          <div className="flex items-center gap-3.5 min-w-0">
            <div className="w-9 h-9 rounded-2xl bg-blue-600 text-white flex items-center justify-center shrink-0 shadow-xs shadow-blue-500/25">
              <ShieldCheck className="w-4 h-4 text-white" />
            </div>
            <div className="min-w-0">
              <div className="flex items-center gap-2">
                <span className="w-1.5 h-1.5 rounded-full bg-blue-600 shrink-0" />
                <span className="text-xs font-semibold text-blue-600 font-mono tracking-wide">
                  Agent 正在实时查明推演 ({activeIndex + 1} / {stages.length})
                </span>
              </div>
              <p className="text-sm font-bold text-slate-900 truncate max-w-sm sm:max-w-xl mt-0.5">
                {caseMeta.title}
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2 shrink-0">
            <button
              type="button"
              onClick={onClose}
              className="p-2 text-slate-400 hover:text-slate-800 rounded-xl hover:bg-slate-100 transition-all cursor-pointer active:scale-[0.98]"
              title="关闭"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* 空间 3D 景深卡片栈 */}
        <div className="relative w-full h-[410px] sm:h-[440px] flex items-center justify-center overflow-hidden py-4">
          {stages.map((stage, index) => {
            const offset = index - activeIndex;
            if (Math.abs(offset) > 2) return null;

            const isCurrent = offset === 0;
            const translateY = offset * 138;
            const scale = isCurrent ? 1 : Math.abs(offset) === 1 ? 0.92 : 0.84;
            const blurPx = isCurrent ? 0 : Math.abs(offset) === 1 ? 3 : 6;
            const opacity = isCurrent ? 1 : Math.abs(offset) === 1 ? 0.5 : 0.16;
            const zIndex = 30 - Math.abs(offset) * 10;

            return (
              <div
                key={stage.id}
                onClick={() => {
                  setActiveIndex(index);
                  setStageProgress(50);
                  setIsFinished(false);
                }}
                style={{
                  transform: `translateY(${translateY}px) scale(${scale})`,
                  filter: `blur(${blurPx}px)`,
                  opacity,
                  zIndex,
                  transition: 'all 600ms cubic-bezier(0.16, 1, 0.3, 1)',
                }}
                className={`absolute w-full max-w-3xl rounded-[32px] p-8 sm:p-9 transition-shadow ${
                  isCurrent
                    ? 'apple-bento-card border-slate-300/90 shadow-[0_20px_50px_rgba(0,0,0,0.12)] cursor-default'
                    : 'bg-white/80 backdrop-blur-xl border border-slate-200/70 shadow-sm cursor-pointer'
                }`}
              >
                {/* 阶段标题与序号 */}
                <div className="flex items-center justify-between gap-4">
                  <div className="flex items-center gap-4">
                    <div
                      className={`w-12 h-12 rounded-2xl flex items-center justify-center font-mono text-base font-bold transition-colors ${
                        index < activeIndex || isFinished
                          ? 'bg-blue-600 text-white shadow-xs shadow-blue-500/25'
                          : isCurrent
                          ? 'bg-slate-900 text-white'
                          : 'bg-slate-100 text-slate-400'
                      }`}
                    >
                      {index < activeIndex || isFinished ? <Check className="w-5 h-5 stroke-[2.5]" /> : stage.stepNumber}
                    </div>
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="text-[11px] font-mono font-bold uppercase tracking-wider text-slate-400">
                          STEP 0{index + 1}
                        </span>
                        {isCurrent && (
                          <span className="w-1.5 h-1.5 rounded-full bg-blue-600 shrink-0 animate-pulse" />
                        )}
                      </div>
                      <h3 className="text-lg sm:text-xl font-bold text-slate-900 tracking-tight mt-0.5">
                        {stage.title}
                      </h3>
                    </div>
                  </div>

                  <span
                    className={`px-3 py-1 rounded-full text-xs font-semibold ${
                      index < activeIndex || isFinished
                        ? 'bg-emerald-50 text-emerald-700 border border-emerald-200/80'
                        : isCurrent
                        ? 'bg-blue-50 text-blue-700 border border-blue-200/80'
                        : 'bg-slate-100 text-slate-500 border border-slate-200/80'
                    }`}
                  >
                    {index < activeIndex || isFinished ? '已完成' : isCurrent ? '执行中' : '等待中'}
                  </span>
                </div>

                {/* 核心动作描述 */}
                <div className="mt-5 px-5 py-4 rounded-2xl bg-slate-50/80 border border-slate-200/80 space-y-3">
                  <p className="text-sm font-medium text-slate-800 leading-relaxed">
                    {stage.coreAction}
                  </p>
                  {/* 当前步骤平滑进度条 */}
                  {isCurrent && !isFinished && (
                    <div className="w-full bg-slate-200/70 h-1.5 rounded-full overflow-hidden">
                      <div
                        className="h-full bg-blue-600 rounded-full transition-all duration-75 ease-linear shadow-xs"
                        style={{ width: `${stageProgress}%` }}
                      />
                    </div>
                  )}
                </div>

                {/* 阶段要点徽标 */}
                <div className="mt-4 flex flex-wrap items-center gap-2">
                  {stage.pills.map((pill, pIdx) => {
                    const activePill =
                      index < activeIndex ||
                      isFinished ||
                      (isCurrent && stageProgress >= (pIdx + 1) * 30);
                    return (
                      <span
                        key={pIdx}
                        className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium transition-all ${
                          activePill
                            ? 'bg-slate-900 text-white shadow-2xs'
                            : 'bg-slate-100 text-slate-400'
                        }`}
                      >
                        <span
                          className={`w-1.5 h-1.5 rounded-full ${
                            activePill ? 'bg-blue-400' : 'bg-slate-300'
                          }`}
                        />
                        {pill}
                      </span>
                    );
                  })}
                </div>
              </div>
            );
          })}
        </div>

        {/* 完成后弹出查看查明报告按钮 - Apple Bento Card 风格 */}
        {isFinished ? (
          <div className="w-full max-w-3xl flex items-center justify-between px-7 py-4 apple-bento-card rounded-[28px] mt-3 animate-in fade-in slide-in-from-bottom-2 duration-300 shadow-xl">
            <div className="flex items-center gap-2.5">
              <span className="w-2 h-2 rounded-full bg-blue-600" />
              <span className="text-xs font-semibold text-slate-800">
                全流程 5 项查明与要件核验已执行完毕
              </span>
            </div>
            <button
              type="button"
              onClick={() => {
                if (onComplete) {
                  onComplete();
                } else {
                  onClose();
                }
              }}
              className="inline-flex items-center gap-2 px-6 py-2.5 text-xs font-semibold text-white bg-blue-600 hover:bg-blue-700 rounded-xl transition-all cursor-pointer shadow-xs shadow-blue-500/25 active:scale-[0.98]"
            >
              <FileText className="w-4 h-4 text-white" />
              <span>查看Agent查明报告</span>
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        ) : (
          <div className="h-10 mt-3" />
        )}
      </div>
    </div>
  );
};
