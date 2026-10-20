import React, { useState, useMemo } from 'react';
import { useApp } from '../../context/AppContext';
import { lawAgentApi } from '../../api/lawAgentApi';
import {
  Download,
  CheckCircle2,
  AlertCircle,
  FileCheck,
  ShieldCheck,
  Layers,
  Building,
  Users,
  Compass,
  FileText,
  Clock,
  ArrowRight,
  ChevronDown,
  AlertTriangle,
  Activity,
  Sparkles,
} from 'lucide-react';

type CheckStatus = 'passed' | 'flawed' | 'failed';

const JUR_NAMES: Record<string, string> = {
  asean_id: '印度尼西亚',
  asean_vn: '越南',
  asean_my: '马来西亚',
  asean_sg: '新加坡',
  asean_th: '泰国',
  asean_ph: '菲律宾',
};

const ARCHETYPE_NAMES: Record<string, string> = {
  EPC_CONTRACTING: 'EPC 总承包',
  PPP_CONCESSION: 'BOT / PPP 特许经营',
  CROSS_BORDER_MA: '跨境股权并购',
  JV_CONSORTIUM: '属地联营体 (KSO/JO)',
};

interface StageGuideline {
  id: string;
  stageName: string;
  stageNumber: string;
  subTitle: string;
  coreFocus: string;
  // 三道防线清单
  defenseLines: {
    line1_operational: {
      title: string;
      checklists: string[];
      riskTip: string;
    };
    line2_legal: {
      title: string;
      checklists: string[];
      riskTip: string;
    };
    line3_audit: {
      title: string;
      checklists: string[];
      riskTip: string;
    };
  };
}

const LIFECYCLE_GUIDELINES: StageGuideline[] = [
  {
    id: 'stage_1',
    stageNumber: '01',
    stageName: '前期跟踪与立项尽调',
    subTitle: '投资并购准入、国资备案与土地习惯法排查',
    coreFocus: '外资准入负面清单核查、国资委 35 号令事前论证、合作伙伴背景与多边制裁筛查、原住民习惯法土地 (Hak Ulayat) 权属前置尽调。',
    defenseLines: {
      line1_operational: {
        title: '海外市场部 / 属地开拓团队实操清单',
        checklists: [
          '取得东道国投资主管部委（如印尼 BKPM / 菲律宾 BOI / 泰国 BOI）关于本项目行业分类的外资股比与准入确认函；',
          '对项目地块进行现场踏勘，排查是否存在原住民习惯法部落、生态红线或未征拆农田争议；',
          '摸排当地电网或特许经营主体财务支付信用记录。',
        ],
        riskTip: '切勿在未明确土地性质前提前签署具有排他性或高额定金罚款的谅解备忘录 (MOU)。',
      },
      line2_legal: {
        title: '涉外法务合规官审查要点',
        checklists: [
          '核实项目主体及联合体各方均不在世行/亚行跨行联合除名 (Cross-Debarment) 及制裁名单中；',
          '严格依据国资委 35 号令准备境外投资可行性研究与合规性专项法律意见书；',
          '设计防范隐性征收的跨境投资架构（建议通过新加坡/香港中转以激活双边投资协定 BIT 保护）。',
        ],
        riskTip: '涉及国家安全与敏感基础设施的，必须提前论证当地外资国安审查审批风险。',
      },
      line3_audit: {
        title: '集团内部审计 / 国资监管穿透核查表',
        checklists: [
          '穿透审查境外项目资本金出境通道是否履行发改委、商务部与外管局 (ODI) 审批备案；',
          '核查非主业境外投资是否履行国资委专项核准程序；',
          '建立境外投资全周期风险评估档案底稿。',
        ],
        riskTip: '严禁向未经集团董事会批准的境外项目主体提供母公司连带兜底担保。',
      },
    },
  },
  {
    id: 'stage_2',
    stageNumber: '02',
    stageName: '招投标与联营体组建',
    subTitle: '施工牌照准入、联合体责任隔离与反腐败合规',
    coreFocus: '属地法定施工牌照 (BUJKA / PCAB / CIDB / BCA) 合规、强制联营体 (KSO/JO) 协议连带责任隔离、外籍与本土劳工配额审查。',
    defenseLines: {
      line1_operational: {
        title: '商务投标与属地施工组实操清单',
        checklists: [
          '完成属地施工许可执照注册或申请（如印尼 BUJKA 代表处、马来西亚 CIDB G7 牌照）；',
          '与合资格的东道国本土一类施工企业签署联合运营体协议 (KSO/JO Agreement)；',
          '测算投标文件中的本地化率 (TKDN) 成本及属地劳工聘用比例。',
        ],
        riskTip: '避免盲目承诺无法落地的属地采购比例，防止履约阶段遭受巨额行政罚款。',
      },
      line2_legal: {
        title: '涉外法务合规官审查要点',
        checklists: [
          '审查 KSO 联营体协议，明确约定内部损益分摊与违约追索机制，设立单方违约防火墙；',
          '排查招标文件是否存在单方严重失衡条款（如完全免除业主交地迟延责任）；',
          '开展属地中介代理商反海外商业贿赂背景审查并签署合规承诺书。',
        ],
        riskTip: '菲律宾最高院 PCAB v. Manila Water 虽然打破外资股比限制，但公建招投标仍受特别法规约束。',
      },
      line3_audit: {
        title: '纪检监督与内控合规核查表',
        checklists: [
          '核实海外投标保证金与保函开立流程规范性；',
          '核查第三方代理佣金支付是否符合国资反商业贿赂合规红线；',
          '对联营体合作伙伴资信等级实施穿透核查。',
        ],
        riskTip: '严禁以任何咨询费、中介费名义向东道国公职人员或其利益关联方输送利益。',
      },
    },
  },
  {
    id: 'stage_3',
    stageNumber: '03',
    stageName: '合同谈判与签署红线',
    subTitle: 'FIDIC 黄金原则、双语法定要求与保函止付约定',
    coreFocus: 'FIDIC 银皮书专用条件审查、双语/三语文本同步签署与准据语言约定、见索即付保函反欺诈索兑限制条款、PPA/EPC 接口风险传导。',
    defenseLines: {
      line1_operational: {
        title: '合同谈判小组实操清单',
        checklists: [
          '核实工程合同价格调整公式，锁定主要原材料（钢材、水泥）与汇率波动分担机制；',
          '落实开工预付款支付与动员期挂钩时间表；',
          '确认移交施工红线图与现场地质资料的正式签收程序。',
        ],
        riskTip: '严禁在专用条件中放弃第 14.8 款延误付款利息或接受不合理的逾期违约金无封顶条款。',
      },
      line2_legal: {
        title: '涉外法务合规官审查要点',
        checklists: [
          '印尼项目严格依据印尼最高法院 SEMA 3/2023 通告，实现印尼语与英语版本同步同文签署；',
          '越南项目严格依据《2025新建设法》第 86.2 条重构预定损害赔偿 (LD) 封顶条款；',
          '马来西亚/新加坡项目坚决剔除背靠背付款条款 (CIPAA 35条与 SOPA 9条法定绝对无效)；',
          '在履约保函条款中约定：争议受新加坡法院专属管辖，准用 BS Mount Sophia 显失公平止付规则。',
        ],
        riskTip: '准据法与争议解决优先约定 SIAC/ICC 境外仲裁，并授权仲裁庭签发紧急禁令。',
      },
      line3_audit: {
        title: '集团法律与风控委员会穿透核查表',
        checklists: [
          '复核合同文本与集团标准海外工程示范文本的黄金原则偏离度报告；',
          '核查保函开立金额、期限与履约进度减额机制是否匹配；',
          '评估特许经营协议与 EPC 总包合同的背靠背接口风险敞口。',
        ],
        riskTip: '对包含政治风险、电价调整风险的重大涉外项目，须报请集团党委会/执委会审议。',
      },
    },
  },
  {
    id: 'stage_4',
    stageNumber: '04',
    stageName: '现场履约与过程留痕',
    subTitle: '28天索赔通知时效、工期延误留痕与 TKDN 认证',
    coreFocus: '开工令与交地纪要签收、28天索赔通知标准化发函模板、外籍劳工配额与工作签台账、TKDN 本地采购认证留痕、工程进度款法定催告函。',
    defenseLines: {
      line1_operational: {
        title: '现场项目经理与工程管理部实操清单',
        checklists: [
          '接收场地受阻时，必须在 24 小时内形成现场阻工纪要并由监理工程师签字确认；',
          '任何业主风险导致的延误事件，必须在 28 天内正式发出 FIDIC 20.1 索赔意向通知函；',
          '每月更新 Primavera P6 关键路径进度计划并形成不可抗力延期对比报告；',
          '严格保存本地采购设备发票与工业部 TKDN 原产地合格证书。',
        ],
        riskTip: '切勿通过口头或非正式即时通讯沟通替代正式 FIDIC 合同信函，防范机械失权。',
      },
      line2_legal: {
        title: '驻场涉外法务与索赔顾问审查要点',
        checklists: [
          '审核项目部对外发出的每一份工期顺延 (EOT) 与附加费用索赔报告；',
          '业主发出违约警告函时，即刻开展抗辩函件起草，援引善意原则 (Itikad Baik) 反制；',
          '对拖欠工程款情形，依据东道国法定付款保障法（如 CIPAA/SOPA）起草正式催告函。',
        ],
        riskTip: '如需签署工期顺延补充备忘录，印尼法域必须同步签署印尼语译本并备案。',
      },
      line3_audit: {
        title: '海外项目现场巡视与合规内审表',
        checklists: [
          '抽查外籍中方管理人员与技术工人的工作签证、劳工配额合规档案；',
          '核查现场资金结算与分包款支付是否严格依工程进度验收单执行；',
          '检查涉外安全保卫与突发社区群体性事件应急预案演练记录。',
        ],
        riskTip: '严禁违规挂靠、虚假发票结算或拖欠当地劳工薪资引发国际舆论风险。',
      },
    },
  },
  {
    id: 'stage_5',
    stageNumber: '05',
    stageName: '竣工移交、争议解决与退出清算',
    subTitle: '保函安全退还、CIPAA快速裁决、信保报损与数据调证',
    coreFocus: '缺陷责任期保函减额退还、CIPAA/SOPA 快速法定裁决应对、SIAC 紧急仲裁保函止付、中信保 30 日报损保全、《数据安全法》第36条跨境调证审批。',
    defenseLines: {
      line1_operational: {
        title: '收尾清算组与资产移交团队实操清单',
        checklists: [
          '取得最终竣工验收证书 (Taking-Over Certificate) 后即刻向银行办理履约保函减额 50%；',
          '完成最终工程结算对账单签署，锁定无争议已确认款项；',
          '妥善办理设备移交、竣工图纸档案移交与属地税务清算注销。',
        ],
        riskTip: '在未取得全额最终付款或可靠支付担保前，严禁盲目向业主全额交还现场管领权。',
      },
      line2_legal: {
        title: '国际争议解决与涉外法务专家审查要点',
        checklists: [
          '业主发生恶意索兑保函迹象时，第一时间向新加坡国际仲裁中心 (SIAC) 申请紧急仲裁员止付禁令；',
          '遭遇东道国政府单方废约或隐性征收，严格在 30 个自然日内向中国信保提交正式《可能损失通知书》；',
          '若境外仲裁庭要求调取工程高精度测绘地质数据，依法依规报请我国司法部/主管机关批准（数安法36条）。',
        ],
        riskTip: '未经中信保书面同意，严禁擅自签署任何免除东道国政府责任的和解协议。',
      },
      line3_audit: {
        title: '终期项目后评价与国资审计核查表',
        checklists: [
          '审查海外项目投资回报率、合同结算利润与当初可行性研究报告的偏离度；',
          '核实全部对外保函、备用信用证是否已全部注销解除敞口；',
          '归档全生命周期合规档案与典型经验复盘手册，作为后续海外项目风控基线。',
        ],
        riskTip: '对因主观重大过失导致国资流失或重大境外败诉的，依法依规启动责任倒查追责。',
      },
    },
  },
];

export const ComplianceGuidelineCenter: React.FC = () => {
  const { showToast, loadCase, openPipelineAnimation, setCurrentView } = useApp();
  const [activeStageId, setActiveStageId] = useState<string>('stage_1');
  const [activeDefenseLine, setActiveDefenseLine] = useState<'line1' | 'line2' | 'line3'>('line1');
  const [exportJur, setExportJur] = useState<string>('asean_id');
  const [exportArchetype, setExportArchetype] = useState<string>('EPC_CONTRACTING');
  const [isExporting, setIsExporting] = useState<boolean>(false);
  const [isCreatingCase, setIsCreatingCase] = useState<boolean>(false);

  // 在线自测打分系统状态
  const [itemStatuses, setItemStatuses] = useState<Record<string, CheckStatus>>(() => {
    const init: Record<string, CheckStatus> = {};
    LIFECYCLE_GUIDELINES.forEach((stage) => {
      (['line1_operational', 'line2_legal', 'line3_audit'] as const).forEach((lineKey) => {
        const line = stage.defenseLines[lineKey];
        line.checklists.forEach((_, idx) => {
          const key = `${stage.id}_${lineKey}_${idx}`;
          if (stage.id === 'stage_1' && lineKey === 'line1_operational' && idx === 1) {
            init[key] = 'flawed'; // 土地原住民 Hak Ulayat 瑕疵
          } else if (stage.id === 'stage_3' && lineKey === 'line2_legal' && idx === 0) {
            init[key] = 'flawed'; // 印尼双语签署瑕疵
          } else if (stage.id === 'stage_4' && lineKey === 'line1_operational' && idx === 1) {
            init[key] = 'failed'; // 28天索赔通知时效未满足
          } else {
            init[key] = 'passed';
          }
        });
      });
    });
    return init;
  });

  const currentStage = LIFECYCLE_GUIDELINES.find((s) => s.id === activeStageId) || LIFECYCLE_GUIDELINES[0];

  // 当前阶段所有核验点
  const currentStageItems = useMemo(() => {
    const items: Array<{
      key: string;
      lineKey: string;
      lineTitle: string;
      text: string;
      status: CheckStatus;
    }> = [];
    (['line1_operational', 'line2_legal', 'line3_audit'] as const).forEach((lineKey) => {
      const line = currentStage.defenseLines[lineKey];
      line.checklists.forEach((text, idx) => {
        const key = `${currentStage.id}_${lineKey}_${idx}`;
        items.push({
          key,
          lineKey,
          lineTitle: line.title,
          text,
          status: itemStatuses[key] || 'passed',
        });
      });
    });
    return items;
  }, [currentStage, itemStatuses]);

  // 当前阶段未达标或瑕疵项
  const currentUnmetItems = useMemo(() => {
    return currentStageItems.filter((it) => it.status === 'flawed' || it.status === 'failed');
  }, [currentStageItems]);

  // 当前阶段得分 (0-100)
  const stageScore = useMemo(() => {
    if (currentStageItems.length === 0) return 100;
    const totalPoints = currentStageItems.reduce((acc, it) => {
      return acc + (it.status === 'passed' ? 100 : it.status === 'flawed' ? 50 : 0);
    }, 0);
    return Math.round(totalPoints / currentStageItems.length);
  }, [currentStageItems]);

  // 全项目总得分 (0-100)
  const overallScore = useMemo(() => {
    let totalItems = 0;
    let totalPoints = 0;
    LIFECYCLE_GUIDELINES.forEach((stage) => {
      (['line1_operational', 'line2_legal', 'line3_audit'] as const).forEach((lineKey) => {
        const line = stage.defenseLines[lineKey];
        line.checklists.forEach((_, idx) => {
          const key = `${stage.id}_${lineKey}_${idx}`;
          const status = itemStatuses[key] || 'passed';
          totalItems += 1;
          totalPoints += status === 'passed' ? 100 : status === 'flawed' ? 50 : 0;
        });
      });
    });
    return totalItems > 0 ? Math.round(totalPoints / totalItems) : 100;
  }, [itemStatuses]);

  // 一键将未达标项立项并启动专项推演
  const handleGenerateComplianceCase = async () => {
    if (currentUnmetItems.length === 0) {
      showToast('当前阶段所有审查要件均已达标，无须启动未达标专项查明！', 'info');
      return;
    }
    try {
      setIsCreatingCase(true);
      showToast(`正在将 ${currentUnmetItems.length} 项未达标要件汇编并启动专项法律推演...`, 'info');

      const jurName = JUR_NAMES[exportJur] || '东盟法域';
      const archName = ARCHETYPE_NAMES[exportArchetype] || '建设工程';
      const isPre = currentStage.id === 'stage_1';
      const stage = isPre ? 'pre_investment' : 'execution_dispute';

      const factsText = `本项目（${archName}，目标法域：${jurName}）在“${currentStage.stageName}”全周期合规自测中发现以下 ${currentUnmetItems.length} 项未达标或瑕疵要件：\n\n` +
        currentUnmetItems.map((u, i) => `${i + 1}. [${u.status === 'failed' ? '严重未达标' : '存在瑕疵'}] 【${u.lineTitle}】: ${u.text}`).join('\n\n') +
        `\n\n【防线红线禁令与监管警示】\n` +
        `- 实操红线：${currentStage.defenseLines.line1_operational.riskTip}\n` +
        `- 法务红线：${currentStage.defenseLines.line2_legal.riskTip}\n` +
        `- 审计红线：${currentStage.defenseLines.line3_audit.riskTip}`;

      const claimsText = `1. 专项查明${jurName}现行法律及属地行业监管对上述【${currentUnmetItems.map((u) => u.text.slice(0, 10)).join('、')}】未达标事实的法律效力、行政处罚或失权后果；\n2. 依据 FIDIC 标准条件与属地强行法，输出合规补救措施与条款谈判对冲方案。`;

      const res = await lawAgentApi.createCase({
        title: `【${currentStage.stageName}自检专项查明】${currentUnmetItems.length}项未达标风险点`,
        facts_zh: factsText,
        claims_zh: claimsText,
        meta: {
          title: `【${currentStage.stageName}自检专项查明】${currentUnmetItems.length}项未达标风险点`,
          jurisdiction: exportJur,
          lifecycle_stage: stage,
          contract_type: `${archName} (FIDIC 银皮书标准条件)`,
          contract_date: new Date().toISOString().split('T')[0],
          parties: ['中资出海企业/央企施工总包', `${jurName}东道国业主/属地监管主管机关`],
          choice_of_law: `${jurName}现行实体法与强制性规范`,
          dispute_resolution: 'SIAC',
        },
        materials: currentUnmetItems.map((u) => ({
          name: `${currentStage.stageName}合规自检记录`,
          desc_zh: u.lineTitle,
          excerpt_zh: u.text,
        })),
        consent_version: 'v1.0',
      });

      await loadCase(res.case_id, true);
      openPipelineAnimation();
      setCurrentView('workspace');
      showToast(`已成功将 ${currentUnmetItems.length} 项未达标点转化为专项查明案卷并启动多 Agent 推演流水线！`, 'success');
    } catch (err: any) {
      showToast(err.message || '专项立项推演失败', 'error');
    } finally {
      setIsCreatingCase(false);
    }
  };

  const handleExportHandbook = async () => {
    try {
      setIsExporting(true);
      showToast('正在为您汇编定制《央企海外工程专项合规指引手册 (DOCX)》...', 'info');
      const url = `/api/cases/compliance/handbook/docx?jurisdiction=${exportJur}&archetype=${exportArchetype}`;
      const res = await fetch(url);
      if (!res.ok) throw new Error('导出失败');
      const blob = await res.blob();
      const downloadUrl = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = downloadUrl;
      a.download = `Compliance_Handbook_${exportJur}_${exportArchetype}.docx`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(downloadUrl);
      showToast('合规指引手册 (DOCX) 已成功生成并下载！', 'success');
    } catch (e) {
      showToast('合规指引手册导出异常，请核验网络后重试', 'error');
    } finally {
      setIsExporting(false);
    }
  };

  const getLineData = () => {
    if (activeDefenseLine === 'line1') return currentStage.defenseLines.line1_operational;
    if (activeDefenseLine === 'line2') return currentStage.defenseLines.line2_legal;
    return currentStage.defenseLines.line3_audit;
  };

  const lineData = getLineData();

  return (
    <div className="space-y-6">
      {/* 顶部：手册定制导出工具条 */}
      <div className="bg-white p-5 rounded-2xl border border-zinc-200/80 shadow-xs flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-emerald-600" />
            <h2 className="text-base font-bold text-zinc-900">
              建设工程全周期合规指引引擎 (SOP & Checklists)
            </h2>
          </div>
          <p className="text-xs text-zinc-500 mt-1">
            对标国资委 35 号令与《中央企业合规管理办法》，贯通全生命周期五阶段与“三道防线”实操
          </p>
        </div>

        {/* 一键导出手册配置 */}
        <div className="flex items-center gap-2 flex-wrap">
          <select
            value={exportJur}
            onChange={(e) => setExportJur(e.target.value)}
            className="text-xs bg-zinc-50 border border-zinc-200 rounded-lg px-2.5 py-1.5 font-medium text-zinc-700 outline-none"
          >
            <option value="asean_id">🇮🇩 印度尼西亚 (SEMA 3/2023)</option>
            <option value="asean_vn">🇻🇳 越南 (2025新建设法)</option>
            <option value="asean_my">🇲🇾 马来西亚 (CIPAA 2012)</option>
            <option value="asean_sg">🇸🇬 新加坡 (SOPA / SIAC)</option>
            <option value="asean_th">🇹🇭 泰国 (CCC / FBA)</option>
            <option value="asean_ph">🇵🇭 菲律宾 (RA 11966 PPP)</option>
          </select>

          <select
            value={exportArchetype}
            onChange={(e) => setExportArchetype(e.target.value)}
            className="text-xs bg-zinc-50 border border-zinc-200 rounded-lg px-2.5 py-1.5 font-medium text-zinc-700 outline-none"
          >
            <option value="EPC_CONTRACTING">EPC 总承包 (FIDIC 银皮书)</option>
            <option value="PPP_CONCESSION">BOT / PPP 特许经营</option>
            <option value="CROSS_BORDER_MA">跨境股权并购 (SPA/SHA)</option>
            <option value="JV_CONSORTIUM">属地联营体 (KSO/JO)</option>
          </select>

          <button
            onClick={handleExportHandbook}
            disabled={isExporting}
            className="px-4 py-1.5 bg-zinc-900 text-white rounded-lg text-xs font-semibold hover:bg-zinc-800 transition-colors shadow-xs flex items-center gap-1.5 cursor-pointer disabled:opacity-50"
          >
            <Download className="w-3.5 h-3.5" />
            <span>{isExporting ? '正在汇编...' : '导出合规手册 (Word)'}</span>
          </button>
        </div>
      </div>

      {/* 全项目与阶段合规健康度仪表板 */}
      <div className="grid grid-cols-1 md:grid-cols-12 gap-4 items-stretch">
        {/* 全项目综合得分 */}
        <div className="md:col-span-5 bg-white p-4.5 rounded-2xl border border-zinc-200/80 shadow-xs flex items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <Activity className="w-4 h-4 text-blue-600" />
              <span className="text-xs font-bold text-zinc-900">
                出海工程全周期合规健康指数
              </span>
            </div>
            <p className="text-[11px] text-zinc-500">
              综合评估全生命周期五阶段三道防线实操核查点
            </p>
          </div>
          <div className="text-right shrink-0">
            <div className="flex items-baseline gap-1 justify-end">
              <span className={`text-2xl font-bold font-mono ${
                overallScore >= 80 ? 'text-emerald-600' : overallScore >= 60 ? 'text-amber-600' : 'text-rose-600'
              }`}>
                {overallScore}
              </span>
              <span className="text-xs text-zinc-400 font-mono">/ 100</span>
            </div>
            <span className={`inline-block px-2 py-0.5 rounded text-[10px] font-bold border mt-0.5 ${
              overallScore >= 80
                ? 'text-emerald-700 bg-emerald-50 border-emerald-200'
                : overallScore >= 60
                ? 'text-amber-700 bg-amber-50 border-amber-200'
                : 'text-rose-700 bg-rose-50 border-rose-200'
            }`}>
              {overallScore >= 80 ? '合规健康 · 低风险' : overallScore >= 60 ? '审慎关注 · 中风险' : '警报隐患 · 高风险'}
            </span>
          </div>
        </div>

        {/* 当前阶段健康度与一键立项推演卡片 */}
        <div className="md:col-span-7 bg-white p-4.5 rounded-2xl border border-zinc-200/80 shadow-xs flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <span className="text-xs font-bold text-zinc-900">
                Phase {currentStage.stageNumber} ({currentStage.stageName}) 健康度:
              </span>
              <span className={`font-mono text-sm font-bold ${
                stageScore >= 80 ? 'text-emerald-600' : stageScore >= 60 ? 'text-amber-600' : 'text-rose-600'
              }`}>
                {stageScore} 分
              </span>
            </div>
            <div className="flex items-center gap-2 text-[11px] text-zinc-500">
              <span>达标: {currentStageItems.filter(i => i.status === 'passed').length}项</span>
              <span>·</span>
              <span className="text-amber-600 font-medium">瑕疵: {currentStageItems.filter(i => i.status === 'flawed').length}项</span>
              <span>·</span>
              <span className="text-rose-600 font-medium">未达标: {currentStageItems.filter(i => i.status === 'failed').length}项</span>
            </div>
          </div>

          <div>
            <button
              onClick={handleGenerateComplianceCase}
              disabled={isCreatingCase || currentUnmetItems.length === 0}
              className={`flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-semibold transition-all duration-150 shadow-xs cursor-pointer ${
                currentUnmetItems.length > 0
                  ? 'bg-blue-600 hover:bg-blue-700 text-white'
                  : 'bg-zinc-100 text-zinc-400 cursor-not-allowed'
              }`}
            >
              <Compass className="w-3.5 h-3.5" />
              <span>
                {isCreatingCase
                  ? '正在立项推演...'
                  : currentUnmetItems.length > 0
                  ? `将未达标项(${currentUnmetItems.length})生成专项案卷推演`
                  : '本阶段全部达标'}
              </span>
            </button>
          </div>
        </div>
      </div>

      {/* 五阶段演进水平导航卡 */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
        {LIFECYCLE_GUIDELINES.map((stage) => {
          const isSelected = stage.id === activeStageId;
          return (
            <button
              key={stage.id}
              onClick={() => setActiveStageId(stage.id)}
              className={`p-3.5 rounded-xl border text-left transition-all cursor-pointer ${
                isSelected
                  ? 'bg-white border-blue-600 ring-1 ring-blue-600 shadow-xs'
                  : 'bg-white border-zinc-200/80 hover:border-zinc-300'
              }`}
            >
              <div className="flex items-center justify-between mb-1">
                <span
                  className={`text-[10px] font-mono font-bold px-1.5 py-0.5 rounded ${
                    isSelected ? 'bg-blue-600 text-white' : 'bg-zinc-100 text-zinc-600'
                  }`}
                >
                  Phase {stage.stageNumber}
                </span>
                {isSelected && <span className="w-1.5 h-1.5 rounded-full bg-blue-600" />}
              </div>
              <h3 className="text-xs font-bold text-zinc-900 line-clamp-1 mt-1">
                {stage.stageName}
              </h3>
              <p className="text-[11px] text-zinc-500 line-clamp-1 mt-0.5">
                {stage.subTitle}
              </p>
            </button>
          );
        })}
      </div>

      {/* 主体指引内容卡 */}
      <div className="bg-white rounded-2xl border border-zinc-200/80 p-6 shadow-xs space-y-6">
        {/* 阶段标题与核心关注 */}
        <div className="border-b border-zinc-100 pb-4">
          <div className="flex items-center gap-2">
            <span className="text-xs font-mono font-bold text-blue-600 bg-blue-50 px-2 py-0.5 rounded">
              Phase {currentStage.stageNumber}
            </span>
            <h3 className="text-sm font-bold text-zinc-900">
              {currentStage.stageName} · 实务操作指南
            </h3>
          </div>
          <p className="text-xs text-zinc-600 mt-2 font-medium leading-relaxed">
            【阶段核心关注】{currentStage.coreFocus}
          </p>
        </div>

        {/* 国资委“三道防线”角色切换器 */}
        <div>
          <div className="text-[11px] font-bold text-zinc-400 uppercase tracking-wider mb-2">
            国资委“三道防线”角色视角切换
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-2">
            {[
              {
                id: 'line1',
                label: '第一道防线',
                sub: '海外市场部 / 项目现场经理实操清单',
                icon: Building,
              },
              {
                id: 'line2',
                label: '第二道防线',
                sub: '涉外法务 / 专职合规官审查要点',
                icon: ShieldCheck,
              },
              {
                id: 'line3',
                label: '第三道防线',
                sub: '集团审计 / 纪检 / 国资监管穿透核查',
                icon: FileCheck,
              },
            ].map((tab) => {
              const isSelected = activeDefenseLine === tab.id;
              const IconComp = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveDefenseLine(tab.id as any)}
                  className={`p-3 rounded-xl border text-left transition-all cursor-pointer flex items-start gap-2.5 ${
                    isSelected
                      ? 'bg-zinc-900 border-zinc-900 text-white shadow-xs'
                      : 'bg-zinc-50 border-zinc-200/80 hover:bg-zinc-100/70 text-zinc-800'
                  }`}
                >
                  <IconComp
                    className={`w-4 h-4 mt-0.5 shrink-0 ${
                      isSelected ? 'text-white' : 'text-zinc-500'
                    }`}
                  />
                  <div>
                    <div className="text-xs font-bold leading-tight">{tab.label}</div>
                    <div
                      className={`text-[11px] mt-0.5 leading-snug line-clamp-1 ${
                        isSelected ? 'text-zinc-300' : 'text-zinc-500'
                      }`}
                    >
                      {tab.sub}
                    </div>
                  </div>
                </button>
              );
            })}
          </div>
        </div>

        {/* 审查动作清单与红线提示 */}
        <div className="space-y-4 pt-2">
          <div className="flex items-center gap-2">
            <span className="w-1.5 h-1.5 rounded-full bg-blue-600" />
            <h4 className="text-xs font-bold text-zinc-900">
              {lineData.title}
            </h4>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {lineData.checklists.map((check, idx) => {
              const currentLineKey = activeDefenseLine === 'line1' ? 'line1_operational' : activeDefenseLine === 'line2' ? 'line2_legal' : 'line3_audit';
              const itemKey = `${currentStage.id}_${currentLineKey}_${idx}`;
              const currentStatus = itemStatuses[itemKey] || 'passed';

              return (
                <div
                  key={idx}
                  className={`p-3.5 rounded-xl border transition-all text-xs space-y-2.5 ${
                    currentStatus === 'passed'
                      ? 'bg-zinc-50/80 border-zinc-200/70'
                      : currentStatus === 'flawed'
                      ? 'bg-amber-50/30 border-amber-200/80'
                      : 'bg-rose-50/30 border-rose-200/80'
                  }`}
                >
                  <div className="flex items-start gap-2 text-zinc-800 font-medium leading-relaxed">
                    {currentStatus === 'passed' && (
                      <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                    )}
                    {currentStatus === 'flawed' && (
                      <AlertTriangle className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
                    )}
                    {currentStatus === 'failed' && (
                      <AlertCircle className="w-4 h-4 text-rose-600 shrink-0 mt-0.5" />
                    )}
                    <span className="flex-1">{check}</span>
                  </div>

                  {/* 状态三选一切换器 */}
                  <div className="flex items-center justify-between pt-1 border-t border-zinc-200/40 text-[11px]">
                    <span className="text-zinc-400 font-medium">合规自检判定:</span>
                    <div className="flex items-center gap-1 bg-white p-0.5 rounded-lg border border-zinc-200/70 shadow-2xs">
                      <button
                        type="button"
                        onClick={() => setItemStatuses((prev) => ({ ...prev, [itemKey]: 'passed' }))}
                        className={`px-2 py-0.5 rounded text-[10px] font-semibold transition-colors cursor-pointer ${
                          currentStatus === 'passed'
                            ? 'bg-emerald-600 text-white'
                            : 'text-zinc-500 hover:text-emerald-700'
                        }`}
                      >
                        ✓ 已满足
                      </button>
                      <button
                        type="button"
                        onClick={() => setItemStatuses((prev) => ({ ...prev, [itemKey]: 'flawed' }))}
                        className={`px-2 py-0.5 rounded text-[10px] font-semibold transition-colors cursor-pointer ${
                          currentStatus === 'flawed'
                            ? 'bg-amber-500 text-white'
                            : 'text-zinc-500 hover:text-amber-700'
                        }`}
                      >
                        ! 瑕疵
                      </button>
                      <button
                        type="button"
                        onClick={() => setItemStatuses((prev) => ({ ...prev, [itemKey]: 'failed' }))}
                        className={`px-2 py-0.5 rounded text-[10px] font-semibold transition-colors cursor-pointer ${
                          currentStatus === 'failed'
                            ? 'bg-rose-600 text-white'
                            : 'text-zinc-500 hover:text-rose-700'
                        }`}
                      >
                        ✕ 未达标
                      </button>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>

          {/* 专属风险红线警示框 */}
          <div className="p-4 rounded-xl bg-amber-50/40 border border-amber-200/70 flex items-start gap-3">
            <AlertCircle className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
            <div>
              <span className="text-xs font-bold text-amber-900 block">
                【本防线红线禁令与违规追责风险】
              </span>
              <p className="text-xs text-amber-800 mt-0.5 leading-relaxed font-medium">
                {lineData.riskTip}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
