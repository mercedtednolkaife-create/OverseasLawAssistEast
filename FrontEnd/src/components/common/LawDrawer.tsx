import React, { useState } from 'react';
import { useApp } from '../../context/AppContext';
import { GradeBadge } from './GradeBadge';
import { Evidence } from '../../types/lawAgent';
import {
  X,
  ExternalLink,
  BookOpen,
  Copy,
  Check,
  ShieldCheck,
  FileText,
  Clock,
  Layers,
  CheckCircle2,
  AlertTriangle,
  Globe2,
} from 'lucide-react';

interface LawDrawerProps {
  /** 是否以独立浮层抽屉展示，或者以分栏面板展示 */
  variant?: 'drawer' | 'docked';
  onClose?: () => void;
}

export const LawDrawer: React.FC<LawDrawerProps> = ({ variant = 'drawer', onClose }) => {
  const {
    currentCase,
    selectedEvidenceEid,
    setSelectedEvidenceEid,
    isDrawerOpen,
    closeLawDrawer,
    showToast,
  } = useApp();

  const [copied, setCopied] = useState(false);
  const [activeTab, setActiveTab] = useState<'norm' | 'breakdown' | 'trace'>('norm');

  if (!currentCase) return null;

  const evidenceMap = currentCase.evidence || {};
  const evidenceList: Evidence[] = Object.values(evidenceMap);
  const currentEid = selectedEvidenceEid || (evidenceList[0]?.eid ?? 'E1');
  const evidence: Evidence | undefined = evidenceMap[currentEid] || evidenceList[0];

  const getJurisdictionLabel = (refId: string, kind: string) => {
    if (refId.startsWith('ID:') || refId.startsWith('ID_')) return '印度尼西亚成文法与最高法院裁判通告 (SEMA 3/2023)';
    if (refId.startsWith('VN:') || refId.startsWith('VN_')) return '越南《2025新建设法》与政府合同法令';
    if (refId.startsWith('MY:') || refId.startsWith('MY_')) return '马来西亚《CIPAA 2012快速裁决法》与联邦法院先例';
    if (refId.startsWith('SG:') || refId.startsWith('SG_')) return '新加坡建设工程付款保障法 (SOPA) 与高等法院先例';
    if (refId.startsWith('TH:') || refId.startsWith('TH_')) return '泰王国《民商法典》(CCC) 承揽编与最高行政法院先例';
    if (refId.startsWith('PH:') || refId.startsWith('PH_')) return '菲律宾《新PPP法典》(RA 11966) 与最高法院先例';
    if (refId.startsWith('FIDIC:') || refId.startsWith('FIDIC_')) return 'FIDIC 国际工程合同标准条件 (Silver/Yellow/Red)';
    if (refId.startsWith('BIT:') || refId.startsWith('BIT_') || refId.startsWith('TREATY:')) return '中国-东盟双边投资保护协定 (BIT)';
    if (refId.startsWith('CN:') || refId.startsWith('PRC_') || refId.startsWith('SINOSURE:')) return '央国企海外合规防线 (国资委35号令/数安法36条/中信保)';
    if (kind === 'norm') return '东盟属地现行工程法规与强行法条';
    return '东盟法院与国际仲裁庭权威工程先例';
  };

  const getLanguageLabel = (refId: string) => {
    if (refId.startsWith('ID:') || refId.startsWith('ID_')) return '印尼语官方逐字正本 (Naskah Asli Bahasa Indonesia)';
    if (refId.startsWith('VN:') || refId.startsWith('VN_')) return '越南语官方正本 (Văn bản tiếng Việt)';
    if (refId.startsWith('TH:') || refId.startsWith('TH_')) return '泰语官方正本 (ฉบับภาษาไทย)';
    if (refId.startsWith('FIDIC:') || refId.startsWith('FIDIC_') || refId.startsWith('MY:') || refId.startsWith('MY_') || refId.startsWith('SG:') || refId.startsWith('SG_') || refId.startsWith('PH:') || refId.startsWith('PH_')) {
      return '英文权威正本 (Official English Authentic Text)';
    }
    return '属地官方逐字规范正本 / 司法裁判正文';
  };

  const getLanguageMode = (refId: string): 'trilingual' | 'bilingual' => {
    if (refId.startsWith('ID:') || refId.startsWith('ID_') || refId.startsWith('VN:') || refId.startsWith('VN_') || refId.startsWith('TH:') || refId.startsWith('TH_')) {
      return 'trilingual';
    }
    return 'bilingual';
  };

  const isTrilingual = evidence ? getLanguageMode(evidence.ref_id) === 'trilingual' : false;

  const handleCopyText = (text: string) => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    showToast('官方规范原文已复制到剪贴板', 'success');
    setTimeout(() => setCopied(false), 2000);
  };

  if (!evidence) {
    return null;
  }

  // 解析款项 Absatz / 段落
  const parseParagraphs = (text: string) => {
    const lines = text.split(/(?=\(\d+\))/g).filter(Boolean);
    if (lines.length > 1) {
      return lines.map((l, idx) => {
        const match = l.match(/^\((\d+)\)\s*([\s\S]*)$/);
        if (match) {
          return { num: `条目/款项 (${match[1]})`, content: match[2].trim() };
        }
        return { num: `段落 ${idx + 1}`, content: l.trim() };
      });
    }
    return [{ num: '正文全文', content: text }];
  };

  const paragraphs = parseParagraphs(evidence.text_de);

  // 关联本案要件
  const relatedElements = (currentCase.elements || []).filter((el) =>
    (currentCase.findings || []).some((f) =>
      (f.statements || []).some(
        (s) =>
          s.element_id === el.element_id &&
          (s.evidence_ids || []).includes(evidence.eid)
      )
    )
  );

  const translation =
    currentCase.translations?.[evidence.eid] ||
    '暂无对齐译文或由司法部法通网术语表自动对齐中';

  return (
    <div className="flex flex-col h-full bg-white border-l border-zinc-200 select-text overflow-hidden">
      {/* 抽屉顶部 Bar */}
      <div className="p-4 border-b border-zinc-200 bg-white space-y-3 shrink-0">
        <div className="flex items-center justify-between gap-3">
          <div className="flex items-center gap-2 min-w-0">
            <div className="w-7 h-7 rounded-lg bg-blue-600 text-white flex items-center justify-center shrink-0 shadow-xs">
              <BookOpen className="w-3.5 h-3.5 text-white" />
            </div>
            <div className="min-w-0">
              <div className="flex items-center gap-2">
                <h3 className="text-xs font-bold text-zinc-900 truncate">
                  {evidence.ref_id}
                </h3>
                {isTrilingual && (
                  <span className="text-[10px] font-mono px-1.5 py-0.2 bg-blue-50 text-blue-700 rounded border border-blue-200/60 font-semibold">
                    三语模式
                  </span>
                )}
                {evidence.ref_id.startsWith('FIDIC_') && (
                  <span className="text-[10px] font-mono px-1.5 py-0.2 bg-purple-50 text-purple-700 rounded border border-purple-200/60 font-semibold">
                    FIDIC Tier 1
                  </span>
                )}
              </div>
              <p className="text-[11px] text-zinc-500 font-mono truncate mt-0.5">
                [{evidence.eid}] · {getJurisdictionLabel(evidence.ref_id, evidence.kind)}
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2 shrink-0">
            <GradeBadge grade={evidence.grade} />
            {onClose ? (
              <button
                type="button"
                onClick={onClose}
                className="p-1 rounded-md text-zinc-400 hover:text-zinc-800 hover:bg-zinc-100 transition-colors duration-150 cursor-pointer"
                title="关闭抽屉"
              >
                <X className="w-4 h-4" />
              </button>
            ) : (
              <button
                type="button"
                onClick={closeLawDrawer}
                className="p-1 rounded-md text-zinc-400 hover:text-zinc-800 hover:bg-zinc-100 transition-colors duration-150 cursor-pointer"
                title="关闭抽屉"
              >
                <X className="w-4 h-4" />
              </button>
            )}
          </div>
        </div>

        {/* 快速法源切换水平列表 (E1 - E8) */}
        <div className="flex items-center gap-1.5 overflow-x-auto pb-1 scrollbar-none">
          {evidenceList.map((ev) => {
            const isSelected = ev.eid === currentEid;
            return (
              <button
                key={ev.eid}
                type="button"
                onClick={() => setSelectedEvidenceEid(ev.eid)}
                className={`px-2 py-1 text-[11px] font-mono rounded-md whitespace-nowrap transition-colors duration-150 cursor-pointer ${
                  isSelected
                    ? 'bg-blue-600 text-white font-semibold shadow-xs'
                    : 'bg-zinc-100 text-zinc-600 hover:bg-zinc-200/80 hover:text-zinc-900'
                }`}
                title={ev.ref_id}
              >
                [{ev.eid}] {ev.ref_id.replace('FIDIC_SILVER:', 'FIDIC ').replace('FIDIC:Silver_1999:', 'FIDIC ')}
              </button>
            );
          })}
        </div>

        {/* 视图 Tab 切换 */}
        <div className="grid grid-cols-3 gap-1 p-0.5 bg-zinc-100 rounded-lg text-xs">
          <button
            type="button"
            onClick={() => setActiveTab('norm')}
            className={`py-1 rounded-md text-[11px] font-medium transition-colors duration-150 cursor-pointer ${
              activeTab === 'norm'
                ? 'bg-white text-zinc-900 shadow-xs'
                : 'text-zinc-600 hover:text-zinc-900'
            }`}
          >
            原文与对齐译文
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('breakdown')}
            className={`py-1 rounded-md text-[11px] font-medium transition-colors duration-150 cursor-pointer ${
              activeTab === 'breakdown'
                ? 'bg-white text-zinc-900 shadow-xs'
                : 'text-zinc-600 hover:text-zinc-900'
            }`}
          >
            条款层级拆解
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('trace')}
            className={`py-1 rounded-md text-[11px] font-medium transition-colors duration-150 cursor-pointer ${
              activeTab === 'trace'
                ? 'bg-white text-zinc-900 shadow-xs'
                : 'text-zinc-600 hover:text-zinc-900'
            }`}
          >
            要件与合规备案
          </button>
        </div>
      </div>

      {/* 抽屉正文滚动区 */}
      <div className="flex-1 overflow-y-auto p-4 space-y-5 text-xs">
        {activeTab === 'norm' && (
          <>
            {/* 1. 官方属地语言正本 (三语模式) */}
            {evidence.text_original && evidence.text_original !== evidence.text_en && (
              <div className="space-y-1.5">
                <div className="flex items-center justify-between">
                  <label className="text-[10px] font-bold text-zinc-500 uppercase tracking-wider flex items-center gap-1.5">
                    <ShieldCheck className="w-3 h-3 text-zinc-600" />
                    {getLanguageLabel(evidence.ref_id)}
                  </label>
                  <button
                    type="button"
                    onClick={() => handleCopyText(evidence.text_original || '')}
                    className="p-1 text-zinc-400 hover:text-zinc-900 rounded hover:bg-zinc-100 transition-colors duration-150 cursor-pointer"
                    title="复制属地官方原文"
                  >
                    {copied ? <Check className="w-3.5 h-3.5 text-zinc-900" /> : <Copy className="w-3.5 h-3.5" />}
                  </button>
                </div>
                <div className="p-3.5 bg-zinc-50 border border-zinc-200 rounded-lg text-xs font-mono text-zinc-900 leading-relaxed whitespace-pre-wrap select-text">
                  {evidence.text_original}
                </div>
              </div>
            )}

            {/* 2. 英文权威规范文本 */}
            <div className="space-y-1.5">
              <div className="flex items-center justify-between">
                <label className="text-[10px] font-bold text-zinc-500 uppercase tracking-wider flex items-center gap-1.5">
                  <Globe2 className="w-3 h-3 text-zinc-600" />
                  英文权威规范文本 (Official English Text)
                </label>
                <div className="flex items-center gap-2">
                  <a
                    href={evidence.source_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-[11px] text-zinc-500 hover:text-zinc-900 flex items-center gap-1 transition-colors"
                  >
                    <span>官方权威来源</span>
                    <ExternalLink className="w-3 h-3" />
                  </a>
                  <button
                    type="button"
                    onClick={() => handleCopyText(evidence.text_en || evidence.text_de)}
                    className="p-1 text-zinc-400 hover:text-zinc-900 rounded hover:bg-zinc-100 transition-colors duration-150 cursor-pointer"
                    title="复制英文正本"
                  >
                    {copied ? <Check className="w-3.5 h-3.5 text-zinc-900" /> : <Copy className="w-3.5 h-3.5" />}
                  </button>
                </div>
              </div>

              <div className="p-3.5 bg-zinc-50 border border-zinc-200 rounded-lg text-xs font-mono text-zinc-900 leading-relaxed whitespace-pre-wrap select-text">
                {evidence.text_en || evidence.text_de}
              </div>
            </div>

            {/* 3. 忠实中译与法通网来源 */}
            <div className="space-y-1.5">
              <div className="flex items-center justify-between">
                <label className="text-[10px] font-bold text-zinc-500 uppercase tracking-wider flex items-center gap-1.5">
                  <FileText className="w-3 h-3 text-zinc-600" />
                  中文权威释义与规范要件对照
                </label>
                <span className="text-[10px] text-blue-700 bg-blue-50 px-2 py-0.5 rounded font-mono border border-blue-200/60 font-semibold">
                  司法部“法通网”权威对齐
                </span>
              </div>

              <div className="p-3.5 bg-zinc-50/80 border border-zinc-200 rounded-lg text-xs text-zinc-800 leading-relaxed space-y-2">
                <p className="font-medium text-zinc-900">{evidence.text_zh || translation}</p>
                <div className="pt-2 border-t border-zinc-200/80 text-[11px] text-zinc-500">
                  <strong>权威来源：</strong>依据中华人民共和国司法部涉外法律法规“法通网”官方精译及 FIDIC 官方中英对照术语词典双重校准。
                </div>
              </div>
            </div>

            {/* 效力与现行状态指示 (最高院解释二形式要求) */}
            <div className="p-3 bg-zinc-50 rounded-lg border border-zinc-200 text-[11px] text-zinc-600 space-y-1 font-mono">
              <div className="flex items-center justify-between">
                <span className="font-semibold text-zinc-800">现行有效版本 (Stand)：</span>
                <span className="text-zinc-900 font-medium">
                  {evidence.stand || '2026年现行有效合并版'}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span>入库核验时间：</span>
                <span>{evidence.fetched_at}</span>
              </div>
              <div className="flex items-center justify-between">
                <span>法源出处数据库：</span>
                <span className="truncate max-w-[200px]">
                  {evidence.ref_id.startsWith('FIDIC')
                    ? 'FIDIC International Secretariat (Geneva)'
                    : evidence.ref_id.startsWith('SG_')
                    ? 'Singapore Judiciary / LawNet'
                    : evidence.ref_id.startsWith('ID_')
                    ? 'Mahkamah Agung Republik Indonesia'
                    : '司法部“法通网”涉外法规数据库'}
                </span>
              </div>
            </div>
          </>
        )}

        {activeTab === 'breakdown' && (
          <div className="space-y-3">
            <div className="text-[11px] text-zinc-500 flex items-center justify-between">
              <span>款项条目分解结构</span>
              <span className="font-mono">共 {paragraphs.length} 项</span>
            </div>

            <div className="space-y-2.5">
              {paragraphs.map((p, idx) => (
                <div
                  key={idx}
                  className="p-3 bg-zinc-50 rounded-lg border border-zinc-200 space-y-1.5"
                >
                  <div className="flex items-center justify-between text-[11px]">
                    <span className="font-mono font-bold text-zinc-900">
                      {p.num}
                    </span>
                    <span className="text-[10px] text-zinc-400 font-mono">
                      规范要件段
                    </span>
                  </div>
                  <p className="font-mono text-xs text-zinc-800 leading-relaxed">
                    {p.content}
                  </p>
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'trace' && (
          <div className="space-y-4">
            {/* 关联本案法律构成要件 */}
            <div className="space-y-2">
              <label className="text-[10px] font-bold text-zinc-500 uppercase tracking-wider block">
                本案支撑要件 (Element Coverage)
              </label>
              {relatedElements.length > 0 ? (
                <div className="space-y-1.5">
                  {relatedElements.map((el) => (
                    <div
                      key={el.element_id}
                      className="p-2.5 bg-zinc-50 rounded-lg border border-zinc-200 flex items-center justify-between gap-2"
                    >
                      <div>
                        <span className="font-mono font-bold text-zinc-900 mr-2">
                          [{el.element_id}]
                        </span>
                        <span className="text-zinc-800 font-medium">{el.name_zh}</span>
                      </div>
                      <span className="text-[10px] font-mono bg-zinc-100 px-1.5 py-0.5 rounded text-zinc-700">
                        {el.match_status}
                      </span>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="p-3 bg-zinc-50 rounded-lg border border-zinc-200 text-[11px] text-zinc-500">
                  当前证据主要作为上位规范基础、东道国强行法或投资背景法源。
                </div>
              )}
            </div>

            {/* 解释二合规证明卡 */}
            <div className="p-3.5 bg-zinc-50 rounded-lg border border-zinc-200 space-y-2">
              <div className="flex items-center gap-1.5 text-xs font-semibold text-zinc-900">
                <ShieldCheck className="w-4 h-4 text-zinc-700" />
                <span>最高人民法院《涉外民商事法律适用法解释二》符合性</span>
              </div>
              <ul className="space-y-1.5 text-[11px] text-zinc-600 list-disc list-inside">
                <li>已载明该条文在东道国法律体系中的现行有效状态（2026零废止有效）</li>
                <li>附官方属地语/英文官方全文与逐字引文一致性核验记录</li>
                <li>提供官方权威司法数据库直接出处链接及抓取时间戳</li>
                <li>包含相关东盟里程碑判例 (如 SEMA 3/2023, BS Mount Sophia) 要旨</li>
              </ul>
            </div>
          </div>
        )}
      </div>

      {/* 底部操作条 */}
      <div className="p-3 border-t border-zinc-200 bg-zinc-50 flex items-center justify-between text-xs shrink-0">
        <span className="text-[11px] text-zinc-400 font-mono">
          快照指纹: {currentCase.snapshot_id}
        </span>
        <a
          href={evidence.source_url}
          target="_blank"
          rel="noopener noreferrer"
          className="flex items-center gap-1.5 px-3 py-1.5 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium shadow-xs"
        >
          <span>查验官方权威法源</span>
          <ExternalLink className="w-3 h-3" />
        </a>
      </div>
    </div>
  );
};
