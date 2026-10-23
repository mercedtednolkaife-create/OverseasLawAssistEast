import React, { useState, useMemo } from 'react';
import { useApp } from '../../context/AppContext';
import { lawAgentApi } from '../../api/lawAgentApi';
import {
  Share2,
  Filter,
  ArrowRight,
  ExternalLink,
  ShieldAlert,
  CheckCircle2,
  Layers,
  Sparkles,
  BookmarkCheck,
  Check,
  Plus,
} from 'lucide-react';

interface InteractiveCitationGraphProps {
  activeNormId?: string;
  onSelectNorm: (normId: string) => void;
}

export const InteractiveCitationGraph: React.FC<InteractiveCitationGraphProps> = ({
  activeNormId,
  onSelectNorm,
}) => {
  const { currentCase, setCurrentCase, openRightDock, showToast } = useApp();
  const [selectedIssueId, setSelectedIssueId] = useState<string>('all');
  const [pinnedNormId, setPinnedNormId] = useState<string | null>(null);

  const handleAttachStatute = async (norm: { id: string; code: string; name: string; category: string }) => {
    if (!currentCase) {
      showToast('未选择目标案卷', 'error');
      return;
    }
    try {
      const updatedArtifacts = await lawAgentApi.attachCaseArtifact(currentCase.case_id, {
        artifact_type: 'statute_pin',
        title: `${norm.code} · ${norm.name}`,
        jurisdiction: currentCase.meta?.jurisdiction || 'asean_id',
        summary: `图谱核心法条引用：${norm.category} 规范基线，已锚定在案事实。`,
      });
      setPinnedNormId(norm.id);
      setCurrentCase({
        ...currentCase,
        attached_artifacts: updatedArtifacts,
      });
      showToast(`已将【${norm.code}】重点法源引用挂载至案卷！`, 'success');
      setTimeout(() => setPinnedNormId(null), 2500);
    } catch (e: any) {
      showToast(e.message || '挂载法条失败', 'error');
    }
  };

  // 1. 列 1：案件事实与材料
  const factsList = useMemo(() => {
    if (currentCase?.facts && currentCase.facts.length > 0) {
      return currentCase.facts.slice(0, 4).map((f) => ({
        id: f.fid,
        tag: f.fid,
        title: f.text_zh.slice(0, 36) + (f.text_zh.length > 36 ? '...' : ''),
        status: f.disputed ? '争议事实' : '已确认事实',
      }));
    }
    return [
      { id: 'F1', tag: 'F1', title: '原住民习惯法土地 (Hak Ulayat) 征拆阻工迟延交地 180 天', status: '已确认事实' },
      { id: 'F2', tag: 'F2', title: '总承包商知悉后 28 天内持续发送催告函但未签印尼语文本', status: '双方确认' },
      { id: 'F3', tag: 'F3', title: '光伏逆变器本土化率仅 28%（法定 40%），工业部下达滞纳金通知', status: '已确认事实' },
      { id: 'F4', tag: 'F4', title: '业主突击向开证行发起 10% 履约保函全额恶意索兑', status: '核心争议' },
    ];
  }, [currentCase]);

  // 2. 列 2：争议焦点与法定构成要件
  const issuesList = useMemo(() => {
    if (currentCase?.issues && currentCase.issues.length > 0) {
      return currentCase.issues.slice(0, 4).map((iss, idx) => ({
        id: iss.issue_id,
        code: `争议焦点 ${idx + 1}`,
        name: iss.text_zh.slice(0, 32) + (iss.text_zh.length > 32 ? '...' : ''),
        elem: (currentCase.elements || []).find((el) => iss.element_ids?.includes(el.element_id))?.name_zh || '法定强行法与合同要件',
      }));
    }
    return [
      {
        id: 'I1',
        code: '争议焦点一',
        name: 'FIDIC 8.4 工期顺延 (EOT) 与习惯法免责',
        elem: '延误归责于业主现场交付义务 (Clause 17.3)',
      },
      {
        id: 'I2',
        code: '争议焦点二',
        name: 'SEMA 3/2023 善意原则反 28 天失权',
        elem: '非恶意未签印尼语版不得宣告合同无效',
      },
      {
        id: 'I3',
        code: '争议焦点三',
        name: 'BS Mount Sophia 显失公平保函止付',
        elem: '无真实实体违约前提下保函索兑构成滥用',
      },
    ];
  }, [currentCase]);

  // 3. 列 3：命中法条与 FIDIC 基线
  const normsList = useMemo(() => {
    if (currentCase?.evidence && Object.keys(currentCase.evidence).length > 0) {
      return Object.values(currentCase.evidence).slice(0, 4).map((ev) => ({
        id: ev.ref_id,
        code: ev.ref_id.replace('FIDIC_SILVER:', 'FIDIC ').replace('FIDIC:Silver_1999:', 'FIDIC '),
        name: ev.text_zh ? ev.text_zh.slice(0, 18) + '...' : ev.ref_id,
        category: ev.ref_id.includes('FIDIC') ? 'FIDIC Tier 1' : '东盟法源',
      }));
    }
    return [
      { id: 'FIDIC_SILVER:Clause8.4', code: 'FIDIC 8.4', name: '竣工工期顺延 (EOT)', category: 'FIDIC Tier 1' },
      { id: 'FIDIC_SILVER:Clause20.1', code: 'FIDIC 20.1', name: '28天索赔时效与通知', category: 'FIDIC Tier 1' },
      { id: 'ID_SEMA:3_2023', code: 'SEMA 3/2023', name: '善意履约推定反无效', category: '印尼最高院' },
      { id: 'SG_BSMountSophia:2016', code: 'BS Mount Sophia', name: '显失公平保函止付', category: '新最高院' },
    ];
  }, [currentCase]);

  // 4. 列 4：裁判先例与合规对策
  const precedentsList = useMemo(() => {
    return [
      { id: 'P1', title: '【示范反制条款】原住民习惯法土地免责专用条件', type: '合同防御' },
      { id: 'P2', title: '【仲裁救济】SIAC 紧急仲裁员 (EA) 临时保函止付令', type: '程序禁令' },
      { id: 'P3', title: '【国资防线】中信保海外投资险 30 日出险报损留痕', type: '信保保全' },
      { id: 'P4', title: '【资质合规】BUJKA / PCAB 属地资质穿透核验与连带免除', type: '准入防线' },
    ];
  }, []);

  return (
    <div className="rounded-2xl bg-white border border-zinc-200/80 p-5 shadow-xs space-y-4 select-text">
      {/* 顶栏说明与争点过滤 */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-zinc-100 pb-3">
        <div className="flex items-center gap-2">
          <Share2 className="w-4 h-4 text-blue-600" />
          <h3 className="text-xs font-bold text-zinc-900">
            四列分层因果穿透因果图谱 (4-Column Causal Graph)
          </h3>
          <span className="text-[10px] text-zinc-400 font-mono">
            案件事实 ➔ 争点要件 ➔ 命中法条 ➔ 裁判对策
          </span>
        </div>

        {/* 争点快速过滤 */}
        <div className="flex items-center gap-1.5 text-xs">
          <span className="text-[11px] text-zinc-400">聚焦争点：</span>
          <button
            onClick={() => setSelectedIssueId('all')}
            className={`px-2 py-0.5 rounded text-[11px] font-medium transition-colors cursor-pointer ${
              selectedIssueId === 'all'
                ? 'bg-zinc-900 text-white'
                : 'bg-zinc-100 text-zinc-600 hover:bg-zinc-200/70'
            }`}
          >
            全景穿透
          </button>
          {issuesList.map((iss) => (
            <button
              key={iss.id}
              onClick={() => setSelectedIssueId(iss.id)}
              className={`px-2 py-0.5 rounded text-[11px] font-medium transition-colors cursor-pointer ${
                selectedIssueId === iss.id
                  ? 'bg-zinc-900 text-white'
                  : 'bg-zinc-100 text-zinc-600 hover:bg-zinc-200/70'
              }`}
            >
              {iss.code}
            </button>
          ))}
        </div>
      </div>

      {/* 四列分层网格展示 */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 relative">
        {/* Column 1: 案件事实与证据 */}
        <div className="space-y-2">
          <div className="flex items-center justify-between px-1">
            <span className="text-[11px] font-bold text-zinc-500 uppercase tracking-wider">
              列 1【案件事实与证据材料】
            </span>
            <span className="text-[10px] font-mono text-zinc-400">Facts & Evidence</span>
          </div>
          <div className="space-y-2">
            {factsList.map((f) => (
              <div
                key={f.id}
                className="p-3 rounded-xl bg-zinc-50 border border-zinc-200/80 text-xs space-y-1 hover:border-zinc-300 transition-colors"
              >
                <div className="flex items-center justify-between">
                  <span className="font-mono font-bold text-zinc-900 bg-white px-1.5 py-0.2 rounded border border-zinc-200">
                    {f.tag}
                  </span>
                  <span className="text-[10px] text-zinc-400">{f.status}</span>
                </div>
                <p className="text-[11px] text-zinc-700 leading-relaxed font-medium">
                  {f.title}
                </p>
              </div>
            ))}
          </div>
        </div>

        {/* Column 2: 争议焦点与要件 */}
        <div className="space-y-2">
          <div className="flex items-center justify-between px-1">
            <span className="text-[11px] font-bold text-blue-600 uppercase tracking-wider">
              列 2【争议焦点与法定要件】
            </span>
            <span className="text-[10px] font-mono text-zinc-400">Issues & Elements</span>
          </div>
          <div className="space-y-2">
            {issuesList.map((iss) => {
              const isDimmed = selectedIssueId !== 'all' && selectedIssueId !== iss.id;
              return (
                <div
                  key={iss.id}
                  className={`p-3 rounded-xl border text-xs space-y-1 transition-all ${
                    isDimmed
                      ? 'opacity-30 bg-zinc-50 border-zinc-200'
                      : 'bg-blue-50/40 border-blue-200/80 shadow-2xs'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span className="font-mono font-bold text-blue-700 text-[10px]">
                      {iss.code}
                    </span>
                    <span className="w-1.5 h-1.5 rounded-full bg-blue-600" />
                  </div>
                  <h4 className="text-xs font-bold text-zinc-900 leading-snug">
                    {iss.name}
                  </h4>
                  <p className="text-[11px] text-zinc-600 leading-tight">
                    要件核心：{iss.elem}
                  </p>
                </div>
              );
            })}
          </div>
        </div>

        {/* Column 3: 命中法条与 FIDIC 基线 */}
        <div className="space-y-2">
          <div className="flex items-center justify-between px-1">
            <span className="text-[11px] font-bold text-emerald-600 uppercase tracking-wider">
              列 3【命中法条与 FIDIC 基线】
            </span>
            <span className="text-[10px] font-mono text-zinc-400">Norms & Baseline</span>
          </div>
          <div className="space-y-2">
            {normsList.map((norm) => (
              <div
                key={norm.id}
                onClick={() => {
                  onSelectNorm(norm.id);
                  openRightDock('law_reader');
                }}
                className="p-3 rounded-xl bg-emerald-50/30 border border-emerald-200/70 text-xs space-y-1.5 hover:border-emerald-400 hover:shadow-xs transition-all cursor-pointer group"
              >
                <div className="flex items-center justify-between">
                  <span className="font-mono font-bold text-emerald-800 text-[11px] group-hover:text-emerald-900">
                    {norm.code}
                  </span>
                  <span className="text-[10px] font-mono px-1.5 py-0.2 rounded bg-white text-emerald-700 border border-emerald-200">
                    {norm.category}
                  </span>
                </div>
                <div className="inline-flex items-center gap-1 px-1.5 py-0.5 rounded bg-emerald-100/70 text-[10px] font-medium text-emerald-800">
                  <BookmarkCheck className="w-3 h-3 text-emerald-700" />
                  <span>权威认证 · 现行有效</span>
                </div>
                <p className="text-xs font-bold text-zinc-900">
                  {norm.name}
                </p>
                <div className="flex items-center justify-between pt-1 border-t border-emerald-100">
                  <div className="text-[10px] text-zinc-400 flex items-center gap-1 group-hover:text-blue-600">
                    <span>穿透副驾精读</span>
                    <ExternalLink className="w-3 h-3" />
                  </div>
                  <button
                    type="button"
                    onClick={(e) => {
                      e.stopPropagation();
                      handleAttachStatute(norm);
                    }}
                    className={`text-[10px] px-2 py-0.5 rounded font-medium flex items-center gap-0.5 cursor-pointer ${
                      pinnedNormId === norm.id
                        ? 'bg-emerald-600 text-white'
                        : 'bg-white text-emerald-700 border border-emerald-200 hover:bg-emerald-50'
                    }`}
                  >
                    {pinnedNormId === norm.id ? (
                      <>
                        <Check className="w-2.5 h-2.5" />
                        <span>已引用</span>
                      </>
                    ) : (
                      <>
                        <Plus className="w-2.5 h-2.5" />
                        <span>引用至案卷</span>
                      </>
                    )}
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Column 4: 裁判先例与合规对策 */}
        <div className="space-y-2">
          <div className="flex items-center justify-between px-1">
            <span className="text-[11px] font-bold text-zinc-700 uppercase tracking-wider">
              列 4【裁判先例与合规对策】
            </span>
            <span className="text-[10px] font-mono text-zinc-400">Precedents & Strategy</span>
          </div>
          <div className="space-y-2">
            {precedentsList.map((p) => (
              <div
                key={p.id}
                className="p-3 rounded-xl bg-zinc-50 border border-zinc-200/80 text-xs space-y-1.5 hover:border-zinc-300 transition-colors"
              >
                <div className="flex items-center justify-between">
                  <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-zinc-200/70 text-zinc-700 font-semibold">
                    {p.type}
                  </span>
                  <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
                </div>
                <p className="text-xs font-bold text-zinc-900 leading-relaxed">
                  {p.title}
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
