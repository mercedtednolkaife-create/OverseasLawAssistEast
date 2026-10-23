import React, { useState } from 'react';
import { useApp } from '../../context/AppContext';
import { lawAgentApi } from '../../api/lawAgentApi';
import {
  AlertTriangle,
  Info,
  Shield,
  X,
  CheckCircle2,
  XCircle,
  ExternalLink,
  BookOpen,
  Compass,
  ArrowRight,
  TrendingUp,
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

const LEGISLATIVE_SHIFTS: LegislativeShift[] = [
  {
    id: 'vn_2025_construction',
    country: '越南',
    countryFlag: '🇻🇳',
    title: '《2025年新建设法》(Law 135/2025/QH15) 正式施行',
    effectiveDate: '2026年7月1日施行',
    coreShift: '第 86.2 条正式确立“预定损害赔偿 (Liquidated Damages)”制度，打破了旧法下仅承认违规部分 12% 法定惩罚金封顶与实际损失的规则。',
    practiceImpact: '新签越南 EPC 合同必须重新设计工期误期损害赔偿与封顶条款，并严格把关情势变更免除违约金情形。',
    alertType: 'critical',
  },
  {
    id: 'id_sema_3_2023',
    country: '印度尼西亚',
    countryFlag: '🇮🇩',
    title: '最高法院 SEMA No. 3/2023 通告推翻纯英文合同无效判例',
    effectiveDate: '现行持续有效',
    coreShift: '最高法院发布指导意见明确：除非能证明当事人存在恶意 (itikad tidak baik)，法院不得仅因涉外商事合同未签署印尼语译本宣告自始无效。',
    practiceImpact: '极大减轻了中资企业历史纯英文合同被恶意宣告无效的风险；但在新项目签约阶段仍须落实双语同文签署以满足行政合规。',
    alertType: 'warning',
  },
  {
    id: 'ph_ra11966_ppp',
    country: '菲律宾',
    countryFlag: '🇵🇭',
    title: '《菲律宾公私合营法典》(The PPP Code, RA 11966) 明文废止旧 BOT 法',
    effectiveDate: '现行全面实施',
    coreShift: '全面明文废止实施三十余年的《BOT法案》(RA 6957/RA 7718)，建立中央与地方统一的特许经营法治体系及公允终止补偿规则。',
    practiceImpact: '严禁在新建特许经营合同中继续援引旧 BOT 法法条，应全面依照 RA 11966 重新梳理特许权提前终止补偿公式。',
    alertType: 'critical',
  },
  {
    id: 'my_cipaa_sec35',
    country: '马来西亚',
    countryFlag: '🇲🇾',
    title: '《CIPAA 2012》第35条背靠背条款法定绝对无效常态化执行',
    effectiveDate: '现行严格执行',
    coreShift: '联邦法院最新判例重申：任何以第三方付款为条件的背靠背付款条款 (Pay-when-paid) 在马来西亚一律绝对无效。',
    practiceImpact: '总承包商不得以业主拖欠工程款为由拒付本地分包商，分包商可随时发起 45 天快速裁决并申请依法停工。',
    alertType: 'warning',
  },
];

const RISK_DOMAINS = [
  '01 资质牌照与施工许可准入',
  '02 外资股比限制与代持合规',
  '03 土地物权与习惯法征拆 (Hak Ulayat)',
  '04 涉外合同语言法定签署要求',
  '05 本地化率 (TKDN) 与土著配额',
  '06 外籍劳工配额与工作签证',
  '07 工期延误、28天失权与违约金封顶',
  '08 背靠背付款条款效力 (Pay-when-paid)',
  '09 见索即付独立保函显失公平止付',
  '10 电价补贴/特许权单方变更与隐性征收',
  '11 税务常设机构 (PE) 判定与预提税',
  '12 外汇汇出与涉外工程数据出境 (数安法36条)',
];

const ASEAN_COUNTRIES = [
  { id: 'asean_id', name: '印度尼西亚', flag: '🇮🇩' },
  { id: 'asean_vn', name: '越南', flag: '🇻🇳' },
  { id: 'asean_my', name: '马来西亚', flag: '🇲🇾' },
  { id: 'asean_sg', name: '新加坡', flag: '🇸🇬' },
  { id: 'asean_th', name: '泰国', flag: '🇹🇭' },
  { id: 'asean_ph', name: '菲律宾', flag: '🇵🇭' },
];

export const RiskPromptDashboard: React.FC = () => {
  const { openLawDrawer, loadCase, openPipelineAnimation, setCurrentView, showToast, openRightDock } = useApp();
  const [isLaunching, setIsLaunching] = useState(false);
  const [selectedCell, setSelectedCell] = useState<{
    domain: string;
    country: string;
    countryId: string;
    flag: string;
    data: RiskCellData;
  } | null>(null);

  const handleLaunchRiskSandbox = async () => {
    if (!selectedCell) return;
    try {
      setIsLaunching(true);
      showToast(`正在为【${selectedCell.country} · ${selectedCell.domain}】立项并启动专项推演流水线...`, 'info');

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
      setCurrentView('workspace');
      showToast(`已成功为【${selectedCell.country} · ${selectedCell.domain}】创建专项审查案卷！`, 'success');
    } catch (err: any) {
      showToast(err.message || '立项推演启动失败', 'error');
    } finally {
      setIsLaunching(false);
    }
  };

  // 模拟并计算单元格数据
  const getCellData = (domainIdx: number, countryId: string): RiskCellData => {
    // 默认高危/关注矩阵规则
    if (domainIdx === 2 && countryId === 'asean_id') {
      return {
        level: 'critical',
        summary: '印尼原住民习惯法土地 (Hak Ulayat) 征拆受阻为最核心工程拖延根因。',
        scenario: '业主以林业部或内政部证书移交场地，但地方原住民部落首领带人封锁进场道路，业主拒绝承担顺延责任。',
        statute: 'ID_UU:2_2017:Art57 & Agrarian Law No. 5/1960',
        statuteText: '习惯法土地权益受宪法保护，未经部族充分协商与足额补偿不得强制施工。',
        dos: [
          '签约前必须要求业主出具省级土地局关于清除 Hak Ulayat 负担的证明；',
          '在 FIDIC 专用条件中将习惯法封路列为业主必须承担的特别风险；',
          '设立属地社区关系公关专职工作组，建立善意沟通机制。',
        ],
        donts: [
          '严禁在未见习惯法协议前盲目出动大型设备强行清表；',
          '严禁接受业主将征地拆迁包死在总包固定总价内；',
          '严禁与当地部族发生肢体冲突导致恶性国际舆论。',
        ],
      };
    }

    if (domainIdx === 7 && (countryId === 'asean_my' || countryId === 'asean_sg')) {
      return {
        level: 'critical',
        summary: '马来西亚 CIPAA 第35条与新加坡 SOPA 第9条明确宣布背靠背付款一律绝对无效。',
        scenario: '总包商因业主延迟支付进度款，援引分包合同中的 Pay-when-paid 拒绝向属地分包商付款，被直接提起快速裁决。',
        statute: countryId === 'asean_my' ? 'MY_CIPAA:Sec35' : 'SG_SOPA:Sec9',
        statuteText: '任何以第三方付款为先决条件的背靠背付款条款均属法定绝对无效。',
        dos: [
          '全面清理分包合同中的“见业主付款后付款”措辞；',
          '改用“经独立工程师核验达标后 X 日内付款”的受控节点条款；',
          '在遭受业主拖欠时同步向业主启动法定快速裁决程序。',
        ],
        donts: [
          '严禁以业主未付款作为拒绝参与 CIPAA/SOPA 快速裁决的抗辩理由；',
          '严禁无视快速裁决员的付款命令导致被申请强制执行；',
          '严禁扣压属地分包商正当计量款项。',
        ],
      };
    }

    if (domainIdx === 3 && countryId === 'asean_id') {
      return {
        level: 'high',
        summary: '印尼《语言法》(UU 24/2009) 要求签署印尼语版本，SEMA 3/2023 已推翻机械无效裁决。',
        scenario: '业主在工程产生巨额索赔时，突然向印尼法院起诉主张纯英文补充协议由于缺少印尼语版本自始无效。',
        statute: 'ID_SEMA:3_2023 & PR No. 63/2019',
        statuteText: '除非证明存在恶意，法院不得仅因缺少印尼语文本认定涉外合同无效。',
        dos: [
          '新签合同与补充协议必须同时签署印尼语与英语版本；',
          '在合同中明确约定英文版为争议解决唯一准据语言；',
          '固定双方长期善意履行英文协议的事实凭证以证明无恶意。',
        ],
        donts: [
          '严禁仅签署单语英文备忘录即开工重大变更工程；',
          '严禁在印尼语译本中出现关键技术与商务参数的实质性翻译偏离；',
          '严禁在法庭答辩时自认存在规避语言法的故意。',
        ],
      };
    }

    if (domainIdx === 8 && countryId === 'asean_sg') {
      return {
        level: 'high',
        summary: '新加坡高等法院确立“显失公平 (Unconscionability)”作为独立保函止付标准。',
        scenario: '业主明知自身存在重大过错且工程款被严重拖欠，为施加商业压力恶意向开证行突击索兑履约保函。',
        statute: 'SG_BSMountSophia:2016',
        statuteText: '只要能初步证明业主索兑行为缺乏诚实信用或显失公平，法院即可裁定签发止付禁令。',
        dos: [
          '在保函条款中明确约定新加坡法院管辖并适用 BS Mount Sophia 原则；',
          '在收到索兑通知后 24 小时内启动新加坡高等法院紧急临时禁令程序；',
          '系统梳理业主违约证据链证明索兑行为具有恶意或显失公平。',
        ],
        donts: [
          '严禁在保函开立时盲目接受不可撤销见索即付无任何异议限制条款；',
          '严禁忽视业主的口头威胁，未提前准备禁令申请草案；',
          '严禁在境外保函争议中直接向国内基层法院寻求不具备执行力的止付令。',
        ],
      };
    }

    if (domainIdx === 9) {
      return {
        level: countryId === 'asean_vn' || countryId === 'asean_ph' ? 'critical' : 'high',
        summary: '特许权单方终止或电价补贴追溯下调，涉及间接征收与双边投资协定 (BIT) 防线。',
        scenario: '政府换届后以环保审查或反腐调查为由单方撤权或暂停 PPA 特许经营协议，拒付重置成本补偿。',
        statute: 'BIT_CHINA_ASEAN:Art6 & PRC_SASAC:Order35',
        statuteText: '征收或等同措施须给予迅速、充分、有效的公允市场价值补偿。',
        dos: [
          '发生政府单方废约之日起 30 日内向中国信保正式提交出险可能损失通知书；',
          '向东道国政府发出正式 BIT 条约违约与投资仲裁友好磋商函；',
          '完整保全项目全部历史投资审计报告与资金流向底稿。',
        ],
        donts: [
          '严禁超过 30 日期限未向信保报损导致代位求偿权丧失；',
          '严禁现场项目部签署任何自愿交还特许权的免责备忘录；',
          '严禁在未经国资委批准前私自接受严重不对等的打折退款和解方案。',
        ],
      };
    }

    if (domainIdx === 4 && countryId === 'asean_id') {
      return {
        level: 'high',
        summary: '印尼能矿部 MEMR Reg 11/2024 电力设备本地化率 (TKDN) 强制达标红线。',
        scenario: '电力基础设施项目因逆变器、变压器本土采购比例未达标，被业主依工业部规程按日计提巨额罚金。',
        statute: 'ID_MEMR:Reg11_2024',
        statuteText: '新能源电力设备应优先采购经 TKDN 官方认证本土产品，否则须依法取得豁免批文。',
        dos: [
          '联合业主向能矿部申请本土无法供应特定精密设备的技术豁免批文；',
          '在分包采购合同中向供货商严格传导 TKDN 证书核验责任；',
          '保留本土企业无法提供同等合格产品的多方询价记录以资抗辩。',
        ],
        donts: [
          '严禁私自采购未经申报鉴定的走私或无票进口机电设备；',
          '严禁在投标书中弄虚作假虚构本地化率；',
          '严禁忽视东道国工业部定期开展的属地化突击核查。',
        ],
      };
    }

    if (domainIdx === 11) {
      return {
        level: 'critical',
        summary: '我国《数据安全法》第36条工程图纸与地质数据跨境调证审批红线。',
        scenario: '境外诉讼或仲裁庭下达开示命令，要求中资承包商直接提供国内存储的工程勘察与深化施工图纸。',
        statute: 'PRC_DATA_SEC:Art36',
        statuteText: '非经主管机关批准，境内组织、个人不得向外国司法或执法机构提供境内数据。',
        dos: [
          '依法向我国司法部或行业主管部委提交境外调证前置审批请示；',
          '在境外仲裁中援引我国强行法提出法定不可抗力抗辩；',
          '对非涉密商事材料进行脱敏脱密处理。',
        ],
        donts: [
          '严禁私自通过境外云盘或跨境专线直传敏感工程 GIS/地质测绘图纸；',
          '严禁在未获批准前直接响应境外法院的大范围强制证据开示令；',
          '严禁在涉密图纸上隐匿国家重要基础设施战略标记。',
        ],
      };
    }

    // 常规单元格
    return {
      level: domainIdx % 3 === 0 ? 'high' : domainIdx % 2 === 0 ? 'caution' : 'safe',
      summary: '东道国建设工程常规合规管控要点。',
      scenario: '项目正常履约中的合同与行政监管要求。',
      statute: 'Host Country Statutory Code & FIDIC Standard',
      statuteText: '依据东道国现行建设工程法规及合同约定履行。',
      dos: ['落实日常履约留痕；', '规范合同变更发函；', '配合属地劳工与税务审计。'],
      donts: ['严禁擅自停工；', '严禁无签证实施重大变更；', '严禁违规雇佣非法劳工。'],
    };
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

  return (
    <div className="space-y-6">
      {/* 顶部：重大立法与司法转向实时预警栏 (Legislative & Judicial Shift Alerts) */}
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-red-600 animate-pulse" />
            <h3 className="text-sm font-bold text-zinc-900">
              东盟重大立法与司法转向实时预警雷达 (Legislative & Judicial Shift Alerts)
            </h3>
          </div>
          <span className="text-[11px] text-zinc-400 font-medium">
            2026 现行有效法源动态追踪 · 杜绝经验主义踩坑
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3">
          {LEGISLATIVE_SHIFTS.map((shift) => (
            <div
              key={shift.id}
              onClick={() => {
                openRightDock('country_playbook');
                showToast(`已在右侧副驾坞载入【${shift.country}】2026 最新立法预警`, 'info');
              }}
              className={`p-4 rounded-xl border transition-all cursor-pointer hover:shadow-xs hover:border-slate-400/80 ${
                shift.alertType === 'critical'
                  ? 'bg-red-50/40 border-red-200/80'
                  : 'bg-amber-50/30 border-amber-200/70'
              }`}
            >
              <div className="flex items-center justify-between mb-1.5">
                <span className="text-xs font-bold text-zinc-900 flex items-center gap-1">
                  <span>{shift.countryFlag}</span>
                  <span>{shift.country}</span>
                </span>
                <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-white/80 border border-zinc-200 text-zinc-600 font-semibold">
                  {shift.effectiveDate}
                </span>
              </div>

              <h4 className="text-xs font-bold text-zinc-900 line-clamp-1 mb-1">
                {shift.title}
              </h4>

              <p className="text-[11px] text-zinc-700 line-clamp-3 leading-relaxed mb-2 font-medium">
                {shift.coreShift}
              </p>

              <div className="pt-2 border-t border-zinc-200/60 text-[10px] text-zinc-500 leading-snug">
                <span className="font-semibold text-zinc-700">【实务对策】</span>
                {shift.practiceImpact}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* 6x12 Risk Prompt Matrix */}
      <div className="bg-white rounded-2xl border border-zinc-200/80 p-6 shadow-xs space-y-4">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 border-b border-zinc-100 pb-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-blue-600" />
              <h3 className="text-base font-bold text-zinc-900">
                东盟 6 国 × 12 大高频工程合规风险提示矩阵 (6×12 Risk Matrix)
              </h3>
            </div>
            <p className="text-xs text-zinc-500 mt-1">
              点击任意单元格即可穿透弹出标准化《建设工程专项风险提示卡 (Do's & Don'ts)》
            </p>
          </div>

          {/* 图例 */}
          <div className="flex items-center gap-3 text-xs text-zinc-600">
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
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse min-w-[700px]">
            <thead>
              <tr className="border-b border-zinc-200 bg-zinc-50/60">
                <th className="py-2.5 px-3 text-xs font-bold text-zinc-700 w-64">
                  工程核心风险域 (12大类)
                </th>
                {ASEAN_COUNTRIES.map((c) => (
                  <th key={c.id} className="py-2.5 px-3 text-xs font-bold text-zinc-800 text-center">
                    <span className="mr-1">{c.flag}</span>
                    <span>{c.name}</span>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-zinc-100 text-xs">
              {RISK_DOMAINS.map((domain, dIdx) => (
                <tr key={dIdx} className="hover:bg-zinc-50/60 transition-colors">
                  <td className="py-3 px-3 font-medium text-zinc-800 text-xs">
                    {domain}
                  </td>
                  {ASEAN_COUNTRIES.map((c) => {
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
                          className="p-1.5 rounded-lg hover:bg-zinc-100 transition-colors inline-flex items-center gap-1.5 cursor-pointer group"
                          title="点击查看风险提示卡"
                        >
                          {getLevelDot(data.level)}
                          <span className="text-[11px] font-mono font-medium text-zinc-500 group-hover:text-zinc-900">
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

      {/* 弹窗：建设工程专项风险提示卡 (Risk Alert Card Modal) */}
      {selectedCell && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-zinc-900/40 backdrop-blur-xs animate-in fade-in duration-200">
          <div className="bg-white rounded-2xl max-w-2xl w-full border border-zinc-200 shadow-xl overflow-hidden animate-in zoom-in-95 duration-200 space-y-5 p-6 select-text max-h-[90vh] overflow-y-auto">
            {/* 弹窗顶栏 */}
            <div className="flex items-start justify-between border-b border-zinc-100 pb-3">
              <div>
                <div className="flex items-center gap-2">
                  <span className="text-xl">{selectedCell.flag}</span>
                  <span className="text-xs font-bold text-zinc-500 uppercase">
                    {selectedCell.country} · 建设工程专项风险提示卡
                  </span>
                </div>
                <h3 className="text-base font-bold text-zinc-900 mt-1">
                  {selectedCell.domain}
                </h3>
              </div>
              <button
                onClick={() => setSelectedCell(null)}
                className="p-1 text-zinc-400 hover:text-zinc-800 hover:bg-zinc-100 rounded-lg transition-colors cursor-pointer"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* 风险级别与警示摘要 */}
            <div className="p-4 rounded-xl bg-red-50/40 border border-red-200/80 space-y-1.5">
              <div className="flex items-center gap-2">
                {getLevelDot(selectedCell.data.level)}
                <span className="text-xs font-bold text-red-900">
                  【风险警示】{getLevelBadgeText(selectedCell.data.level)}
                </span>
              </div>
              <p className="text-xs text-red-800 leading-relaxed font-medium">
                {selectedCell.data.summary}
              </p>
            </div>

            {/* 触发场景与典型发难手法 */}
            <div className="space-y-1.5">
              <h4 className="text-xs font-bold text-zinc-900">
                【触发场景与东道国常见发难手法】
              </h4>
              <p className="text-xs text-zinc-700 leading-relaxed bg-zinc-50 p-3.5 rounded-xl border border-zinc-200/60 font-medium">
                {selectedCell.data.scenario}
              </p>
            </div>

            {/* 现行法定依据 */}
            <div className="space-y-1.5">
              <h4 className="text-xs font-bold text-zinc-900">
                【现行法定依据与司法规则】
              </h4>
              <div className="p-3.5 rounded-xl bg-blue-50/40 border border-blue-200/60 space-y-1 text-xs">
                <span className="font-mono font-bold text-blue-800 block">
                  {selectedCell.data.statute}
                </span>
                <p className="text-zinc-700 italic">
                  "{selectedCell.data.statuteText}"
                </p>
              </div>
            </div>

            {/* 红线防范动作 Do's & Don'ts */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {/* Do's */}
              <div className="p-4 rounded-xl bg-emerald-50/40 border border-emerald-200/70 space-y-2">
                <div className="text-xs font-bold text-emerald-900 flex items-center gap-1.5">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                  <span>必须落实的防御动作 (Do's)</span>
                </div>
                <div className="space-y-1.5 text-xs text-zinc-800 font-medium">
                  {selectedCell.data.dos.map((d, idx) => (
                    <div key={idx} className="flex items-start gap-1.5">
                      <span className="text-emerald-600 font-bold">✓</span>
                      <span>{d}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Don'ts */}
              <div className="p-4 rounded-xl bg-red-50/40 border border-red-200/70 space-y-2">
                <div className="text-xs font-bold text-red-900 flex items-center gap-1.5">
                  <XCircle className="w-4 h-4 text-red-600" />
                  <span>严禁触碰的红线禁令 (Don'ts)</span>
                </div>
                <div className="space-y-1.5 text-xs text-zinc-800 font-medium">
                  {selectedCell.data.donts.map((d, idx) => (
                    <div key={idx} className="flex items-start gap-1.5">
                      <span className="text-red-600 font-bold">✕</span>
                      <span>{d}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* 底栏按钮 */}
            <div className="pt-3 border-t border-zinc-100 flex flex-wrap items-center justify-between gap-3">
              <div className="flex items-center gap-2">
                <button
                  onClick={handleLaunchRiskSandbox}
                  disabled={isLaunching}
                  className="flex items-center gap-1.5 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-xl text-xs font-semibold transition-all duration-150 cursor-pointer shadow-xs disabled:opacity-50"
                >
                  <Compass className="w-4 h-4" />
                  <span>{isLaunching ? '正在立项并启动...' : '针对该国别风险启动专项审查推演'}</span>
                </button>
                <button
                  onClick={() => {
                    openRightDock('country_playbook');
                    showToast(`已在右侧副驾坞载入【${selectedCell.country}】排雷速查手册`, 'info');
                  }}
                  className="px-3 py-2 bg-slate-100 hover:bg-slate-200 text-slate-800 rounded-xl text-xs font-semibold transition-colors flex items-center gap-1.5 cursor-pointer"
                >
                  <BookOpen className="w-3.5 h-3.5 text-blue-600" />
                  <span>右侧副驾精读</span>
                </button>
              </div>

              <button
                onClick={() => setSelectedCell(null)}
                className="px-4 py-2 bg-zinc-100 text-zinc-700 rounded-xl text-xs font-semibold hover:bg-zinc-200 transition-colors cursor-pointer"
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
