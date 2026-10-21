import React, { useState } from 'react';
import { useApp } from '../../context/AppContext';
import { lawAgentApi } from '../../api/lawAgentApi';
import { CaseMeta, LifecycleStage, ProjectArchetype } from '../../types/lawAgent';
import { ASEAN_JURISDICTIONS, getJurisdictionConfig } from '../../configs/jurisdictions';
import {
  ShieldCheck,
  X,
  Plus,
  Trash2,
  ArrowRight,
  FileCheck2,
  Sparkles,
  Layers,
  Building2,
  GitMerge,
  Briefcase,
  AlertTriangle,
} from 'lucide-react';

interface CaseEntryModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const CaseEntryModal: React.FC<CaseEntryModalProps> = ({ isOpen, onClose }) => {
  const { loadCase, showToast, openPipelineAnimation } = useApp();

  const [jurisdiction, setJurisdiction] = useState<string>('asean_id');
  const [projectHostCountry, setProjectHostCountry] = useState<string>('asean_id');
  const [governingLawOption, setGoverningLawOption] = useState<string>('same');
  const [lifecycleStage, setLifecycleStage] = useState<LifecycleStage>('execution_dispute');
  const [projectArchetypes, setProjectArchetypes] = useState<ProjectArchetype[]>(['EPC_CONTRACTING']);
  const [fidicBookEdition, setFidicBookEdition] = useState<string>('1999_SILVER');

  const [title, setTitle] = useState('');
  const [factsZh, setFactsZh] = useState('');
  const [claimsZh, setClaimsZh] = useState('');
  const [contractType, setContractType] = useState('国际工程总承包 EPC 合同 (FIDIC 银皮书)');
  const [partiesStr, setPartiesStr] = useState('中资央企建设总承包商, 东道国电力项目业主');
  const [contractDate, setContractDate] = useState('2024-03-15');
  const [eventDate, setEventDate] = useState('2025-08-20');
  const [choiceOfLaw, setChoiceOfLaw] = useState('印度尼西亚实体法 (Indonesian Law)');
  const [disputeResolution, setDisputeResolution] = useState<string>('SIAC');
  const [consentAccepted, setConsentAccepted] = useState(false);
  const [materials, setMaterials] = useState<
    Array<{ name: string; desc_zh: string; excerpt_zh: string }>
  >([
    {
      name: 'EPC 合同专用条件第 8.4 条 & 20.1 条',
      desc_zh: '约定不可预见现场条件工期顺延及 28 天索赔失权通知时效',
      excerpt_zh: '承包商须在知悉延误事件后28天内向工程师发出书面索赔通知，否则丧失工期与费用索赔权利。',
    },
  ]);
  const [submitting, setSubmitting] = useState(false);

  if (!isOpen) return null;

  const toggleArchetype = (arch: ProjectArchetype) => {
    if (projectArchetypes.includes(arch)) {
      if (projectArchetypes.length > 1) {
        setProjectArchetypes(projectArchetypes.filter((a) => a !== arch));
      } else {
        showToast('至少保留一项项目业态标签', 'warning');
      }
    } else {
      setProjectArchetypes([...projectArchetypes, arch]);
    }
  };

  const handleAddMaterial = () => {
    setMaterials([...materials, { name: '', desc_zh: '', excerpt_zh: '' }]);
  };

  const handleRemoveMaterial = (index: number) => {
    setMaterials(materials.filter((_, idx) => idx !== index));
  };

  // 示范案 1: 印尼爪哇电站 EPC 征地延误与 TKDN 处罚案 (C101)
  const handleFillDemoID = () => {
    setJurisdiction('asean_id');
    setProjectHostCountry('asean_id');
    setGoverningLawOption('same');
    setLifecycleStage('execution_dispute');
    setProjectArchetypes(['EPC_CONTRACTING', 'JV_CONSORTIUM']);
    setFidicBookEdition('1999_SILVER');
    setTitle('印尼爪哇燃煤/光伏混动电站 EPC 习惯法土地征拆迟延与 TKDN 处罚争议案');
    setFactsZh(`2024年3月15日，中资央企所属联合体与印尼国家电力公司(PLN)项目公司订立《爪哇燃煤与光伏电站EPC总承包合同》（FIDIC银皮书），约定印尼法为准据法，SIAC新加坡仲裁。
工程推进中因属地村民依据原住民习惯法土地（Hak Ulayat）阻挠施工，业主交地迟延达180天。承包商于受阻第45天向业主发出工期顺延(EOT)及赶工费用索赔通知。
业主以“超出FIDIC第20.1条28天通知时效已失权”、“补充协议仅签署英文本未签署印尼语文书依《语言法》自始无效”以及“逆变器辅机未达工业部MOI 35/2025法定TKDN本地化率”为由拒付工程进度款4,200万美元，并向雅加达开证行发出没收履约保函通告。`);
    setClaimsZh(`承包商主张：1. 原住民习惯法征地受阻依法构成业主风险，请求顺延工期180天并补偿赶工停窝工损失；2. 依据印尼最高院 SEMA 3/2023，无恶意事实下不得仅以缺少印尼语版本判合同无效；3. TKDN未能达标系因国内无合格产能，申请法定豁免并禁止业主索兑保函。
业主抗辩：28天通知属除斥期间逾期失权；纯外文协议违反公共秩序；TKDN不达标构成重大实质违约。`);
    setContractType('电站新能源工程 EPC 总承包');
    setPartiesStr('中资联合体总包商, 印尼 PLN 项目公司');
    setContractDate('2024-03-15');
    setEventDate('2025-08-20');
    setChoiceOfLaw('印度尼西亚共和国法律');
    setDisputeResolution('SIAC');
    setConsentAccepted(true);
    showToast('已填入印尼基建 EPC 示范案要素 (C101)', 'info');
  };

  // 示范案 2: 越南沿海海上风电 M&A + EPC 保函恶意索兑案 (C102)
  const handleFillDemoVN = () => {
    setJurisdiction('asean_vn');
    setProjectHostCountry('asean_vn');
    setGoverningLawOption('asean_sg');
    setLifecycleStage('execution_dispute');
    setProjectArchetypes(['CROSS_BORDER_MA', 'EPC_CONTRACTING']);
    setFidicBookEdition('1999_YELLOW');
    setTitle('越南沿海 350MW 海上风电并购路条与 EPC 见索即付保函恶意索兑案');
    setFactsZh(`中资央企收购越南本土新能源项目公司80%股权以获取风电路条，并由集团工程局总包施工。
因越南工贸部(MOIT)实施新FIT补贴电价过渡机制，项目投产后收益预期下滑。业主在并网商运日前夕，以台风导致工期违约及海缆敷设技术偏离为由，主张按旧建设法12%法定最高违约金扣款，并向河内分行突袭发起10%见索即付履约保函全额索兑。`);
    setClaimsZh(`总包商主张：1. 台风构成不可抗力事件；2. 依据越南《2025新建设法》(Law 135/2025/QH15)第86.2条，预定违约金须以合理实际损失为基础，不得滥用最高罚金；3. 依据中越BIT条约与SIAC紧急仲裁程序，申请紧急止付令。
业主抗辩：见索即付保函具有独立抽象性，不受基础合同履行争议抗辩阻却。`);
    setContractType('海上风电投建营与 EPC 承揽');
    setPartiesStr('中资海外投资集团, 越南风电联营业主');
    setContractDate('2024-05-10');
    setEventDate('2025-09-01');
    setChoiceOfLaw('越南社会主义共和国法律');
    setDisputeResolution('SIAC');
    setConsentAccepted(true);
    showToast('已填入越南并购 + EPC 示范案要素 (C102)', 'info');
  };

  // 示范案 3: 马来西亚轨交枢纽 CIPAA 快速法定裁决与背靠背无效案 (C103)
  const handleFillDemoMY = () => {
    setJurisdiction('asean_my');
    setProjectHostCountry('asean_my');
    setGoverningLawOption('same');
    setLifecycleStage('execution_dispute');
    setProjectArchetypes(['EPC_CONTRACTING']);
    setFidicBookEdition('1999_RED');
    setTitle('马来西亚吉隆坡轨道交通枢纽 CIPAA 极速工程款追索与背靠背抗辩案');
    setFactsZh(`中资总承包商承接吉隆坡轻轨枢纽标段，马来西亚业主拖欠工程款达 4,500 万令吉。中资总包商以分包合同中订有“背靠背付款条款 (Pay-when-paid)”为由，暂缓向当地土著分包商支付钢结构分包款。
土著分包商直接向吉隆坡仲裁中心(AIAC)依据《CIPAA 2012》发起极速法定裁决程序。`);
    setClaimsZh(`分包商主张：依据《CIPAA 2012》第 35 条，建设工程分包合同中任何“以业主付款为前提”的背靠背条款自始无效，总包商必须在 10 日内无条件给付分包工程款。
总包商主张：双方意思自治自愿签署背靠背条款，且业主正处于重组，应中止裁决。`);
    setContractType('轨道交通土建与机电总承包');
    setPartiesStr('中资工程海外局, 马来西亚土著分包商');
    setContractDate('2023-11-01');
    setEventDate('2025-04-12');
    setChoiceOfLaw('马来西亚联邦法律 (CIPAA 2012 适用)');
    setDisputeResolution('STATUTORY_ADJUDICATION');
    setConsentAccepted(true);
    showToast('已填入马来西亚 CIPAA 示范案要素 (C103)', 'info');
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!factsZh.trim()) {
      showToast('案情事实经过为必填项', 'warning');
      return;
    }
    if (!contractDate) {
      showToast('合同订立日为锁定法典版本的必填项', 'error');
      return;
    }
    if (!consentAccepted) {
      showToast('请阅读并勾选合规确认声明', 'warning');
      return;
    }

    setSubmitting(true);
    try {
      const govLawName = governingLawOption === 'same'
        ? `${currentJurisdictionConfig.name_zh}实体法`
        : governingLawOption === 'english_law'
        ? '英国普通法 (English Law)'
        : governingLawOption === 'asean_sg'
        ? '新加坡共和国法律 (Singapore Law)'
        : choiceOfLaw;

      const meta: CaseMeta = {
        jurisdiction: projectHostCountry,
        host_country: currentJurisdictionConfig.name_zh,
        project_host_country: projectHostCountry,
        governing_law_jurisdiction: govLawName,
        contract_type: contractType,
        parties: partiesStr.split(',').map((s) => s.trim()).filter(Boolean),
        contract_date: contractDate,
        event_date: eventDate || undefined,
        choice_of_law: `${govLawName} [争议管辖: ${disputeResolution}]`,
        lifecycle_stage: lifecycleStage,
        stage: lifecycleStage,
        project_archetypes: projectArchetypes,
        fidic_book_edition: fidicBookEdition,
      };

      const result = await lawAgentApi.createCase({
        title: title || `东盟涉外工程案件-${new Date().toLocaleDateString()}`,
        facts_zh: factsZh,
        claims_zh: claimsZh || undefined,
        meta,
        materials: materials.filter((m) => m.name.trim()),
        consent_version: 'v2026.10-asean',
      });

      onClose();
      await loadCase(result.case_id, true);
      openPipelineAnimation();
      showToast(`案件 ${result.case_id} 创建成功，已启动东盟涉外法律研判`, 'success');
    } catch (err: any) {
      showToast(err.message || '创建案件失败', 'error');
    } finally {
      setSubmitting(false);
    }
  };

  const currentJurisdictionConfig = getJurisdictionConfig(jurisdiction);

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-6 bg-slate-950/40 backdrop-blur-md antialiased apple-modal-backdrop overflow-y-auto"
      onClick={onClose}
    >
      <div
        className="bg-white/95 backdrop-blur-2xl rounded-[28px] border border-slate-200/90 max-w-4xl w-full my-auto shadow-[0_24px_64px_rgba(0,0,0,0.18)] apple-modal-card flex flex-col max-h-[92vh] overflow-hidden"
        onClick={(e) => e.stopPropagation()}
      >
        {/* 顶部标题区 */}
        <div className="px-6 py-5 border-b border-slate-200/80 flex items-center justify-between shrink-0 bg-white/70 backdrop-blur-md">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-2xl bg-blue-50 text-blue-600 border border-blue-200/60 flex items-center justify-center shadow-2xs">
              <ShieldCheck className="w-5 h-5 text-blue-600" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h2 className="text-sm sm:text-base font-bold text-slate-900 tracking-tight">
                  新建涉外工程与投资查明案件
                </h2>
                <span className="text-[10px] text-slate-500 font-mono bg-slate-100 px-2 py-0.5 rounded-md border border-slate-200">
                  东盟核心六国 · 2026 现行有效法源
                </span>
              </div>
              <p className="text-xs text-slate-500 mt-0.5">
                录入涉外工程合同架构、客观事实与争议焦点，启动智能研判与合规查明
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            {/* 快速示范填充按钮 */}
            <div className="hidden sm:flex items-center gap-1.5 mr-2">
              <button
                type="button"
                onClick={handleFillDemoID}
                className="flex items-center gap-1 px-2.5 py-1 text-xs font-medium text-slate-700 hover:text-blue-600 bg-white hover:bg-blue-50/50 border border-slate-200 rounded-xl transition-all shadow-2xs cursor-pointer active:scale-95"
                title="载入印尼电站 EPC 征地延误与 TKDN 案"
              >
                <span>🇮🇩 印尼示范案</span>
              </button>
              <button
                type="button"
                onClick={handleFillDemoVN}
                className="flex items-center gap-1 px-2.5 py-1 text-xs font-medium text-slate-700 hover:text-blue-600 bg-white hover:bg-blue-50/50 border border-slate-200 rounded-xl transition-all shadow-2xs cursor-pointer active:scale-95"
                title="载入越南风电并购与保函索兑案"
              >
                <span>🇻🇳 越南示范案</span>
              </button>
              <button
                type="button"
                onClick={handleFillDemoMY}
                className="flex items-center gap-1 px-2.5 py-1 text-xs font-medium text-slate-700 hover:text-blue-600 bg-white hover:bg-blue-50/50 border border-slate-200 rounded-xl transition-all shadow-2xs cursor-pointer active:scale-95"
                title="载入马来西亚 CIPAA 极速裁决案"
              >
                <span>🇲🇾 马来示范案</span>
              </button>
            </div>

            <button
              type="button"
              onClick={onClose}
              className="p-1.5 rounded-xl text-slate-400 hover:text-slate-700 hover:bg-slate-100 transition-colors cursor-pointer"
              title="关闭弹窗"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* 表单主体内容 */}
        <form onSubmit={handleSubmit} className="flex-1 overflow-y-auto p-6 space-y-6">
          {/* 小屏幕示范按钮 */}
          <div className="sm:hidden flex items-center gap-1.5 overflow-x-auto pb-1">
            <button
              type="button"
              onClick={handleFillDemoID}
              className="px-2.5 py-1 text-xs font-medium text-slate-700 bg-white border border-slate-200 rounded-lg shrink-0"
            >
              🇮🇩 印尼示范
            </button>
            <button
              type="button"
              onClick={handleFillDemoVN}
              className="px-2.5 py-1 text-xs font-medium text-slate-700 bg-white border border-slate-200 rounded-lg shrink-0"
            >
              🇻🇳 越南示范
            </button>
            <button
              type="button"
              onClick={handleFillDemoMY}
              className="px-2.5 py-1 text-xs font-medium text-slate-700 bg-white border border-slate-200 rounded-lg shrink-0"
            >
              🇲🇾 马来示范
            </button>
          </div>

          {/* 1. 目标东盟法域选择 */}
          <div className="apple-bento-card rounded-2xl p-5 space-y-3.5">
            <div className="flex items-center justify-between">
              <label className="block text-xs font-bold text-slate-900 tracking-tight">
                1. 目标涉外东道国法域 <span className="text-rose-500">*</span>
              </label>
              <span className="text-[11px] text-slate-500">
                当前语言模式：
                <span className="font-semibold text-slate-700 ml-1">
                  {currentJurisdictionConfig.language_mode === 'trilingual' ? '三语模式（属地官方语+英+中）' : '双语模式（官方英文+中）'}
                </span>
              </span>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-3 gap-2.5">
              {ASEAN_JURISDICTIONS.map((j) => {
                const isSelected = jurisdiction === j.code;
                return (
                  <button
                    key={j.code}
                    type="button"
                    onClick={() => {
                      setJurisdiction(j.code);
                      setChoiceOfLaw(`${j.name_zh}实体法`);
                    }}
                    className={`p-3 text-left rounded-xl border transition-all cursor-pointer ${
                      isSelected
                        ? 'border-blue-600 bg-blue-50/50 ring-1 ring-blue-500/20 text-slate-900 shadow-2xs'
                        : 'border-slate-200/80 bg-white/70 hover:bg-white text-slate-700'
                    }`}
                  >
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-xs sm:text-sm font-bold flex items-center gap-1.5">
                        <span>{j.flag}</span>
                        <span>{j.short_name}</span>
                      </span>
                      {isSelected ? (
                        <div className="flex items-center gap-1">
                          <span className="w-1.5 h-1.5 rounded-full bg-blue-600 animate-pulse" />
                          <span className="text-[10px] text-blue-700 font-semibold font-mono">ACTIVE</span>
                        </div>
                      ) : (
                        <span className="w-1.5 h-1.5 rounded-full bg-slate-300" />
                      )}
                    </div>
                    <p className="text-[11px] leading-relaxed text-slate-500 line-clamp-2">
                      {j.description_zh}
                    </p>
                  </button>
                );
              })}
            </div>

            {/* 实务焦点微提示 */}
            <div className="p-2.5 rounded-xl bg-slate-50 border border-slate-200/70 text-xs text-slate-600 flex items-start gap-2">
              <Sparkles className="w-3.5 h-3.5 text-blue-600 shrink-0 mt-0.5" />
              <div className="min-w-0">
                <span className="font-semibold text-slate-800">实务关注要害：</span>
                <span className="text-slate-600 ml-1">{currentJurisdictionConfig.practice_focus}</span>
              </div>
            </div>
          </div>

          {/* 2. 项目生命周期阶段与业态组合标签 */}
          <div className="apple-bento-card rounded-2xl p-5 space-y-4">
            <label className="block text-xs font-bold text-slate-900 tracking-tight">
              2. 项目生命周期阶段与业态组合标签
            </label>

            {/* 阶段选择器 (双模式切换) */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <button
                type="button"
                onClick={() => setLifecycleStage('execution_dispute')}
                className={`p-3.5 rounded-xl border text-left transition-all cursor-pointer ${
                  lifecycleStage === 'execution_dispute'
                    ? 'border-blue-600 bg-blue-50/50 ring-1 ring-blue-500/20 text-slate-900 shadow-2xs'
                    : 'border-slate-200 bg-white/70 hover:bg-white text-slate-600'
                }`}
              >
                <div className="flex items-center justify-between mb-1">
                  <span className="text-xs font-bold flex items-center gap-1.5">
                    <Briefcase className="w-3.5 h-3.5 text-blue-600" />
                    <span>履约索赔与争议推演模式 (Mode 2)</span>
                  </span>
                  {lifecycleStage === 'execution_dispute' && (
                    <span className="w-1.5 h-1.5 rounded-full bg-blue-600" />
                  )}
                </div>
                <p className="text-[11px] text-slate-500">
                  针对现场延误索赔、28天失权、工程款拖欠快速裁决及保函恶意索兑止付
                </p>
              </button>

              <button
                type="button"
                onClick={() => setLifecycleStage('pre_investment')}
                className={`p-3.5 rounded-xl border text-left transition-all cursor-pointer ${
                  lifecycleStage === 'pre_investment'
                    ? 'border-blue-600 bg-blue-50/50 ring-1 ring-blue-500/20 text-slate-900 shadow-2xs'
                    : 'border-slate-200 bg-white/70 hover:bg-white text-slate-600'
                }`}
              >
                <div className="flex items-center justify-between mb-1">
                  <span className="text-xs font-bold flex items-center gap-1.5">
                    <Building2 className="w-3.5 h-3.5 text-blue-600" />
                    <span>投前并购、准入与签约合规审查模式 (Mode 1)</span>
                  </span>
                  {lifecycleStage === 'pre_investment' && (
                    <span className="w-1.5 h-1.5 rounded-full bg-blue-600" />
                  )}
                </div>
                <p className="text-[11px] text-slate-500">
                  针对施工资质许可准入、外资股比、土地环评、合同语言法定要求及FIDIC偏离度审查
                </p>
              </button>
            </div>

            {/* 业态组合标签 (支持多选) */}
            <div className="space-y-1.5 pt-2 border-t border-slate-100">
              <span className="text-xs font-semibold text-slate-700 block">
                项目业务业态（支持组合标签）：
              </span>
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
                {[
                  { id: 'EPC_CONTRACTING', label: 'EPC 工程总承包', icon: <Briefcase className="w-3 h-3" /> },
                  { id: 'PPP_CONCESSION', label: 'PPP 特许经营/投建营', icon: <Building2 className="w-3 h-3" /> },
                  { id: 'CROSS_BORDER_MA', label: '跨境股权并购 M&A', icon: <GitMerge className="w-3 h-3" /> },
                  { id: 'JV_CONSORTIUM', label: '属地联营体 KSO/JO', icon: <Layers className="w-3 h-3" /> },
                ].map((item) => {
                  const isSelected = projectArchetypes.includes(item.id as ProjectArchetype);
                  return (
                    <button
                      key={item.id}
                      type="button"
                      onClick={() => toggleArchetype(item.id as ProjectArchetype)}
                      className={`px-3 py-2 text-xs rounded-xl border flex items-center justify-between transition-all cursor-pointer ${
                        isSelected
                          ? 'border-blue-500 bg-blue-50/70 text-slate-900 font-semibold'
                          : 'border-slate-200 bg-white hover:bg-slate-50 text-slate-600'
                      }`}
                    >
                      <span className="flex items-center gap-1.5">
                        {item.icon}
                        <span>{item.label}</span>
                      </span>
                      <span
                        className={`w-1.5 h-1.5 rounded-full ${
                          isSelected ? 'bg-blue-600' : 'bg-slate-200'
                        }`}
                      />
                    </button>
                  );
                })}
              </div>
            </div>

            {/* FIDIC 范本版本选择 */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2 text-xs">
              <div>
                <label className="block font-semibold text-slate-700 mb-1">
                  FIDIC 范本基准版本
                </label>
                <select
                  value={fidicBookEdition}
                  onChange={(e) => setFidicBookEdition(e.target.value)}
                  className="w-full px-3 py-2 border border-slate-200 rounded-xl bg-white font-medium focus:outline-none focus:border-blue-600/80 focus:ring-2 focus:ring-blue-500/10 shadow-2xs"
                >
                  <option value="1999_SILVER">1999版 银皮书 (EPC/交钥匙总承包)</option>
                  <option value="1999_YELLOW">1999版 黄皮书 (生产设备与设计-施工承包)</option>
                  <option value="1999_RED">1999版 红皮书 (施工总承包)</option>
                  <option value="2017_SILVER">2017版 银皮书 (更新版交钥匙合同)</option>
                  <option value="2017_YELLOW">2017版 黄皮书 (更新版设备与设计建造)</option>
                </select>
              </div>

              <div>
                <label className="block font-semibold text-slate-700 mb-1">
                  案件规范业务标题
                </label>
                <input
                  type="text"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  placeholder="例如：印尼爪哇电站 EPC 征地延误与 TKDN 处罚争议案"
                  className="w-full px-3 py-2 border border-slate-200 rounded-xl bg-white focus:outline-none focus:border-blue-600/80 focus:ring-2 focus:ring-blue-500/10 shadow-2xs"
                />
              </div>
            </div>
          </div>

          {/* 3. 案情经过与核心诉求 (针对投前合规审查自适应调整术语) */}
          <div className="apple-bento-card rounded-2xl p-5 space-y-4">
            <label className="block text-xs font-bold text-slate-900 tracking-tight">
              {lifecycleStage === 'pre_investment'
                ? '3. 拟投资项目客观概况与核心合规审查诉求'
                : '3. 客观事实经过与诉求主张'}
            </label>

            <div className="space-y-1.5">
              <div className="flex items-center justify-between">
                <span className="text-xs font-semibold text-slate-700">
                  {lifecycleStage === 'pre_investment' ? '拟投资项目概况与交易架构说明' : '案件事实经过'} <span className="text-rose-500">*</span>
                </span>
                <span className="text-[11px] text-slate-400">
                  {lifecycleStage === 'pre_investment'
                    ? '说明东道国股权架构、习惯法土地、设备采购计划、国资委35号令备案与出境数据'
                    : '详细说明合同订立、交地受阻、通知时效、牌照资质、TKDN认证及各方函件往来'}
                </span>
              </div>
              <textarea
                rows={4}
                value={factsZh}
                onChange={(e) => setFactsZh(e.target.value)}
                placeholder={
                  lifecycleStage === 'pre_investment'
                    ? "请详述拟投资/并购项目概况：东道国属地公司股权比例、特许经营权期限、土地不动产性质（是否涉及原住民习惯法土地）、拟采购设备进口与本地化计划、国资委35号令合规备案进展..."
                    : "请详述案件事实：合同版本与专用条件、现场征地与原住民习惯法受阻时间线、监理指令、28天索赔函件发出时间、本地化率审计与业主拒付理由..."
                }
                className="w-full px-3.5 py-2.5 text-xs sm:text-sm border border-slate-200 rounded-xl focus:outline-none focus:border-blue-600/80 focus:ring-2 focus:ring-blue-500/10 leading-relaxed bg-white transition-all shadow-2xs font-sans"
                required
              />
            </div>

            <div className="space-y-1.5">
              <span className="text-xs font-semibold text-slate-700 block">
                {lifecycleStage === 'pre_investment' ? '核心合规审查诉求（股比/土地/TKDN/国资备案等）' : '各方主张诉求与抗辩意见'}
              </span>
              <textarea
                rows={3}
                value={claimsZh}
                onChange={(e) => setClaimsZh(e.target.value)}
                placeholder={
                  lifecycleStage === 'pre_investment'
                    ? "投资人审查诉求：1. 评估东道国外商投资负面清单与施工资质持牌门槛；2. 核验印尼 MEMR 11/2024 本地化率豁免可行性；3. 论证特许经营合同与双边投资保护协定 (BIT) 保护架构..."
                    : "承包商主张：请求工期顺延EOT及费用补偿；主张无恶意事实下外文协议有效；申请保函止付...&#10;业主抗辩：28天时效已过失权；协议未签印尼语无效；TKDN违约罚金..."
                }
                className="w-full px-3.5 py-2.5 text-xs sm:text-sm border border-slate-200 rounded-xl focus:outline-none focus:border-blue-600/80 focus:ring-2 focus:ring-blue-500/10 leading-relaxed bg-white transition-all shadow-2xs font-sans"
              />
            </div>
          </div>

          {/* 4. 合同参数与法律适用条款 */}
          <div className="apple-bento-card rounded-2xl p-5 space-y-4">
            <label className="block text-xs font-bold text-slate-900 tracking-tight">
              4. 关键合同时间节点与争议解决条款
            </label>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3.5 text-xs">
              <div>
                <label className="block font-semibold text-slate-700 mb-1">
                  合同订立日 <span className="text-rose-500">*</span>
                </label>
                <input
                  type="date"
                  value={contractDate}
                  onChange={(e) => setContractDate(e.target.value)}
                  className="w-full px-3 py-2 border border-slate-200 rounded-xl bg-white font-mono focus:outline-none focus:border-blue-600/80 focus:ring-2 focus:ring-blue-500/10 shadow-2xs"
                  required
                />
                <span className="text-[10px] text-slate-400 mt-1 block">用于锁定东道国现行成文法典版本</span>
              </div>

              <div>
                <label className="block font-semibold text-slate-700 mb-1">
                  阻碍事件发生 / 索赔通知日
                </label>
                <input
                  type="date"
                  value={eventDate}
                  onChange={(e) => setEventDate(e.target.value)}
                  className="w-full px-3 py-2 border border-slate-200 rounded-xl bg-white font-mono focus:outline-none focus:border-blue-600/80 focus:ring-2 focus:ring-blue-500/10 shadow-2xs"
                />
                <span className="text-[10px] text-slate-400 mt-1 block">用于核验 28 天失权与除斥期间</span>
              </div>

              <div>
                <label className="block font-semibold text-slate-700 mb-1">
                  准据法条款约定
                </label>
                <input
                  type="text"
                  value={choiceOfLaw}
                  onChange={(e) => setChoiceOfLaw(e.target.value)}
                  className="w-full px-3 py-2 border border-slate-200 rounded-xl bg-white focus:outline-none focus:border-blue-600/80 focus:ring-2 focus:ring-blue-500/10 shadow-2xs"
                />
                <span className="text-[10px] text-slate-400 mt-1 block">如“印度尼西亚实体法”或“越南法”</span>
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5 pt-2 border-t border-slate-100 text-xs">
              <div>
                <label className="block font-semibold text-slate-700 mb-1">
                  合同当事各方
                </label>
                <input
                  type="text"
                  value={partiesStr}
                  onChange={(e) => setPartiesStr(e.target.value)}
                  className="w-full px-3 py-2 border border-slate-200 rounded-xl bg-white focus:outline-none focus:border-blue-600/80 focus:ring-2 focus:ring-blue-500/10 shadow-2xs"
                  placeholder="中资总包商, 东道国电力业主"
                />
              </div>

              <div>
                <label className="block font-semibold text-slate-700 mb-1">
                  争议解决与仲裁机构约定
                </label>
                <select
                  value={disputeResolution}
                  onChange={(e) => setDisputeResolution(e.target.value)}
                  className="w-full px-3 py-2 border border-slate-200 rounded-xl bg-white font-medium focus:outline-none focus:border-blue-600/80 focus:ring-2 focus:ring-blue-500/10 shadow-2xs"
                >
                  <option value="SIAC">SIAC 新加坡国际仲裁中心（含紧急仲裁员保函止付）</option>
                  <option value="STATUTORY_ADJUDICATION">东道国法定工程快速裁决（如马来 CIPAA / 新加坡 SOPA）</option>
                  <option value="LOCAL_ARBITRATION">属地专业工程仲裁（如印尼 BANI / 菲律宾 CIAC）</option>
                  <option value="ICC_HKIAC">ICC 国际商会仲裁院 / HKIAC 香港国际仲裁中心</option>
                  <option value="LITIGATION">东道国属地法院诉讼管辖</option>
                </select>
              </div>
            </div>
          </div>

          {/* 5. 证明材料与合同专用条件附件 */}
          <div className="apple-bento-card rounded-2xl p-5 space-y-4">
            <div className="flex items-center justify-between">
              <label className="text-xs font-bold text-slate-900 tracking-tight">
                5. 关键合同专用条件(PC)摘录与证据材料
              </label>
              <button
                type="button"
                onClick={handleAddMaterial}
                className="text-xs font-medium text-slate-700 hover:text-slate-900 bg-white border border-slate-200/80 hover:border-slate-300 px-2.5 py-1 rounded-lg transition-all shadow-2xs flex items-center gap-1 cursor-pointer active:scale-[0.98]"
              >
                <Plus className="w-3.5 h-3.5" />
                <span>添加摘录项</span>
              </button>
            </div>

            <div className="space-y-3">
              {materials.map((m, idx) => (
                <div
                  key={idx}
                  className="p-3.5 rounded-xl bg-white/70 border border-slate-200/80 space-y-2 text-xs relative"
                >
                  <div className="flex items-center justify-between gap-3">
                    <input
                      type="text"
                      value={m.name}
                      onChange={(e) => {
                        const updated = [...materials];
                        updated[idx].name = e.target.value;
                        setMaterials(updated);
                      }}
                      placeholder="材料名称，如《专用条件第 8.4 条不可预见现场条件》"
                      className="font-semibold text-slate-900 bg-white px-3 py-1.5 border border-slate-200 rounded-lg flex-1 focus:outline-none focus:border-blue-600/80 focus:ring-2 focus:ring-blue-500/10"
                    />
                    {materials.length > 1 && (
                      <button
                        type="button"
                        onClick={() => handleRemoveMaterial(idx)}
                        className="p-1 text-slate-400 hover:text-rose-600 rounded-lg cursor-pointer"
                        title="删除材料项"
                      >
                        <Trash2 className="w-3.5 h-3.5" />
                      </button>
                    )}
                  </div>

                  <textarea
                    rows={2}
                    value={m.excerpt_zh}
                    onChange={(e) => {
                      const updated = [...materials];
                      updated[idx].excerpt_zh = e.target.value;
                      setMaterials(updated);
                    }}
                    placeholder="粘贴关键条款原文摘录（用于与 FIDIC 通用条件正本进行红线对比与效力核验）..."
                    className="w-full px-3 py-2 bg-white border border-slate-200 rounded-lg focus:outline-none focus:border-blue-600/80 focus:ring-2 focus:ring-blue-500/10 leading-relaxed font-sans"
                  />
                </div>
              ))}
            </div>
          </div>

          {/* 底部合规声明与操作按钮 */}
          <div className="pt-2 flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-t border-slate-100">
            <label className="flex items-center gap-2.5 text-xs text-slate-600 cursor-pointer">
              <input
                type="checkbox"
                checked={consentAccepted}
                onChange={(e) => setConsentAccepted(e.target.checked)}
                className="w-4 h-4 rounded text-blue-600 border-slate-300 focus:ring-blue-500 cursor-pointer"
              />
              <span>已核验输入工程案件事实，确认启动东盟涉外法查明与合规推演</span>
            </label>

            <div className="flex items-center gap-2.5 shrink-0 self-end sm:self-center">
              <button
                type="button"
                onClick={onClose}
                className="px-4 py-2 text-xs sm:text-sm font-medium text-slate-600 hover:text-slate-900 hover:bg-slate-100 rounded-xl transition-all cursor-pointer"
              >
                取消
              </button>
              <button
                type="submit"
                disabled={submitting}
                className="px-5 py-2 text-xs sm:text-sm font-semibold text-white bg-blue-600 hover:bg-blue-700 rounded-xl transition-all shadow-xs shadow-blue-500/25 disabled:opacity-40 disabled:cursor-not-allowed flex items-center justify-center gap-2 cursor-pointer active:scale-[0.98]"
              >
                {submitting ? (
                  <>
                    <div className="w-3.5 h-3.5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                    <span>正在启动查明...</span>
                  </>
                ) : (
                  <>
                    <span>启动涉外法研判</span>
                    <ArrowRight className="w-4 h-4" />
                  </>
                )}
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
};
