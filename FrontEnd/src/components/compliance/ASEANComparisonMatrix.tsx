import React, { useState, useEffect } from 'react';
import { useApp } from '../../context/AppContext';
import { lawAgentApi } from '../../api/lawAgentApi';
import { DEFAULT_COMPARISON_MATRIX } from './complianceDefaultData';
import {
  Check,
  Loader2,
  ArrowRight,
} from 'lucide-react';

interface ComparisonRow {
  dimension: string;
  id: string;
  vn: string;
  my: string;
  sg: string;
  th: string;
  ph: string;
}

const COUNTRIES = [
  { key: 'id', name: '印度尼西亚', flag: '🇮🇩', code: 'asean_id' },
  { key: 'vn', name: '越南', flag: '🇻🇳', code: 'asean_vn' },
  { key: 'my', name: '马来西亚', flag: '🇲🇾', code: 'asean_my' },
  { key: 'sg', name: '新加坡', flag: '🇸🇬', code: 'asean_sg' },
  { key: 'th', name: '泰国', flag: '🇹🇭', code: 'asean_th' },
  { key: 'ph', name: '菲律宾', flag: '🇵🇭', code: 'asean_ph' },
];

export const ASEANComparisonMatrix: React.FC = () => {
  const { openCaseEntryModal, openCaseEntryWithPrefill, showToast, setPrefillIntakeParams } = useApp();
  const [selectedKeys, setSelectedKeys] = useState<string[]>(['id', 'vn']);
  const [matrixData, setMatrixData] = useState<ComparisonRow[]>(DEFAULT_COMPARISON_MATRIX as unknown as ComparisonRow[]);
  const [loading, setLoading] = useState<boolean>(false);

  useEffect(() => {
    let mounted = true;
    lawAgentApi
      .getComparisonMatrix()
      .then((data) => {
        if (mounted && Array.isArray(data) && data.length > 0) {
          setMatrixData(data);
        }
      })
      .catch((err) => {
        console.warn('Comparison matrix background fetch failed, using fallback:', err);
      });
    return () => {
      mounted = false;
    };
  }, []);

  const toggleCountry = (key: string) => {
    if (selectedKeys.includes(key)) {
      if (selectedKeys.length <= 1) {
        showToast('至少保留一个对比国别', 'info');
        return;
      }
      setSelectedKeys(selectedKeys.filter((k) => k !== key));
    } else {
      setSelectedKeys([...selectedKeys, key]);
    }
  };

  const handleLaunchComparison = () => {
    const selectedCountries = COUNTRIES.filter((c) => selectedKeys.includes(c.key));
    const selectedNames = selectedCountries.map((c) => c.name).join('、');
    const selectedCodes = selectedCountries.map((c) => c.code);

    if (setPrefillIntakeParams) {
      setPrefillIntakeParams({
        title: `东盟${selectedCountries.length}国投前准入与强行法合规横向比选专案`,
        jurisdiction: selectedCodes[0] || 'asean_id',
        compared_jurisdictions: selectedCodes,
        stage: 'pre_investment',
        claims: `开展【${selectedNames}】东道国外资准入负面清单、土地权属、联营体强制要求与保函止付尺度横向比选论证。`,
        facts: `中资企业拟在东盟开展重大基建投资与并购，重点在【${selectedNames}】之间进行多法域投资环境与强行法红线比选。`,
        raw_text: `中资企业拟在东盟开展重大基建投资与并购，重点在【${selectedNames}】之间进行多法域投资环境与强行法红线比选。`
      });
    }

    showToast(`已选定【${selectedNames}】（${selectedCodes.length}国）启动投前准入合规比选立项`, 'success');
    openCaseEntryWithPrefill({
      facts_zh: `中资企业拟在东盟开展重大基建投资与并购，重点在【${selectedNames}】之间进行多法域投资环境与强行法红线比选。`,
      claims_zh: `开展【${selectedNames}】东道国外资准入负面清单、土地权属、联营体强制要求与保函止付尺度横向比选论证。`,
      meta: {
        jurisdiction: selectedCodes[0] || 'asean_id',
        lifecycle_stage: 'pre_investment',
        choice_of_law: '多国准入横向比选',
      }
    });
  };

  return (
    <div className="apple-bento-card p-6 space-y-5">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-100 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded-full bg-blue-600 shadow-xs shadow-blue-500/40" />
            <h3 className="text-base font-bold text-slate-900 tracking-tight">
              东盟重点法域实务横向对比
            </h3>
          </div>
          <p className="text-xs text-slate-500 mt-1">
            横向比对东盟重点法域法律体系、合同语言要求、现行成文法典、准入联营红线与争议解决先例
          </p>
        </div>

        {/* 一键比选立项操作区 */}
        <div className="flex items-center gap-2.5 shrink-0">
          <div className="text-xs text-slate-500 hidden sm:block">
            已勾选 <strong className="text-blue-600 font-mono font-bold">{selectedKeys.length}</strong> 个法域
          </div>
          <button
            type="button"
            onClick={handleLaunchComparison}
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-xl text-xs font-semibold flex items-center gap-1.5 cursor-pointer shadow-xs shadow-blue-500/25 active:scale-[0.98] transition-all"
          >
            <span>发起跨法域比选立项</span>
            <ArrowRight className="w-3.5 h-3.5 ml-0.5" />
          </button>
        </div>
      </div>

      {/* 国别勾选选择胶囊条 */}
      <div className="flex flex-wrap items-center gap-2 text-xs">
        <span className="text-slate-400 font-medium">聚焦对比：</span>
        {COUNTRIES.map((c) => {
          const isSelected = selectedKeys.includes(c.key);
          return (
            <button
              key={c.key}
              type="button"
              onClick={() => toggleCountry(c.key)}
              className={`px-3 py-1.5 rounded-xl text-xs font-medium border transition-all cursor-pointer flex items-center gap-1.5 ${
                isSelected
                  ? 'bg-blue-50 text-blue-800 border-blue-200/90 shadow-2xs font-semibold'
                  : 'bg-slate-50/80 text-slate-600 border-slate-200/80 hover:bg-slate-100'
              }`}
            >
              <span>{c.flag}</span>
              <span>{c.name}</span>
              {isSelected && <Check className="w-3 h-3 text-blue-600" />}
            </button>
          );
        })}
      </div>

      <div className="overflow-x-auto rounded-xl border border-slate-200/80">
        <table className="w-full text-left border-collapse min-w-[900px]">
          <thead>
            <tr className="border-b border-slate-200 bg-slate-50/90">
              <th className="py-3 px-3.5 text-xs font-bold text-slate-700 w-44">
                实务审查维度
              </th>
              {COUNTRIES.map((c) => {
                const isSelected = selectedKeys.includes(c.key);
                return (
                  <th
                    key={c.key}
                    onClick={() => toggleCountry(c.key)}
                    className={`py-3 px-3 text-xs font-bold transition-colors cursor-pointer select-none ${
                      isSelected ? 'text-blue-900 bg-blue-50/50' : 'text-slate-700'
                    }`}
                  >
                    <div className="flex items-center gap-1.5">
                      <span>{c.flag}</span>
                      <span>{c.name}</span>
                      {isSelected && <span className="w-1.5 h-1.5 rounded-full bg-blue-600" />}
                    </div>
                  </th>
                );
              })}
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 text-xs text-slate-700">
            {loading && matrixData.length === 0 ? (
              <tr>
                <td colSpan={7} className="py-16 text-center text-slate-400">
                  <div className="flex flex-col items-center justify-center gap-2">
                    <Loader2 className="w-6 h-6 text-blue-600 animate-spin" />
                    <span className="text-xs font-medium">正在载入横向比对矩阵...</span>
                  </div>
                </td>
              </tr>
            ) : (
            matrixData.map((row, idx) => (
              <tr key={idx} className="hover:bg-slate-50/70 transition-colors">
                <td className="py-3.5 px-3.5 font-semibold text-slate-900 bg-slate-50/40">
                  {row.dimension}
                </td>
                <td className={`py-3.5 px-3 leading-relaxed ${selectedKeys.includes('id') ? 'bg-blue-50/20' : ''}`}>
                  {row.id}
                </td>
                <td className={`py-3.5 px-3 leading-relaxed ${selectedKeys.includes('vn') ? 'bg-blue-50/20' : ''}`}>
                  {row.vn}
                </td>
                <td className={`py-3.5 px-3 leading-relaxed ${selectedKeys.includes('my') ? 'bg-blue-50/20' : ''}`}>
                  {row.my}
                </td>
                <td className={`py-3.5 px-3 leading-relaxed ${selectedKeys.includes('sg') ? 'bg-blue-50/20' : ''}`}>
                  {row.sg}
                </td>
                <td className={`py-3.5 px-3 leading-relaxed ${selectedKeys.includes('th') ? 'bg-blue-50/20' : ''}`}>
                  {row.th}
                </td>
                <td className={`py-3.5 px-3 leading-relaxed ${selectedKeys.includes('ph') ? 'bg-blue-50/20' : ''}`}>
                  {row.ph}
                </td>
              </tr>
            )))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
