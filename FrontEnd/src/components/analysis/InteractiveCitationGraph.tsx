import React, { useState, useMemo, useRef, useEffect, useCallback } from 'react';
import { useApp } from '../../context/AppContext';
import { lawAgentApi } from '../../api/lawAgentApi';
import { getJurisdictionConfig } from '../../configs/jurisdictions';
import {
  Share2,
  ExternalLink,
  CheckCircle2,
  Check,
  Plus,
  Maximize2,
  Sparkles,
  BookOpen,
  ArrowRight,
  ShieldCheck,
  Compass,
  Scale,
} from 'lucide-react';

interface InteractiveCitationGraphProps {
  activeNormId?: string;
  onSelectNorm: (normId: string) => void;
  fullscreen?: boolean;
  filterIssueId?: string;
  onOpenFullscreen?: () => void;
}

interface GraphLink {
  from: string;
  to: string;
  chainId: number;
  isCrossLink?: boolean;
}

export const InteractiveCitationGraph: React.FC<InteractiveCitationGraphProps> = ({
  activeNormId,
  onSelectNorm,
  fullscreen = false,
  filterIssueId = 'all',
  onOpenFullscreen,
}) => {
  const { currentCase, setCurrentCase, openRightDock, showToast } = useApp();
  const [internalIssueFilter, setInternalIssueFilter] = useState<string>('all');
  const [pinnedNormId, setPinnedNormId] = useState<string | null>(null);

  // 悬停交互与点击锁定状态：hoveredNodeId 与 selectedNodeId
  const [hoveredNodeId, setHoveredNodeId] = useState<string | null>(null);
  const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null);
  const [activeInspectorNode, setActiveInspectorNode] = useState<any>(null);

  const containerRef = useRef<HTMLDivElement>(null);
  const gridContainerRef = useRef<HTMLDivElement>(null);
  const nodeRefs = useRef<Record<string, HTMLDivElement | null>>({});
  const rafIdRef = useRef<number | null>(null);

  const [svgPaths, setSvgPaths] = useState<Array<{
    id: string;
    d: string;
    chainId: number;
    from: string;
    to: string;
    isCrossLink?: boolean;
    x1: number;
    y1: number;
    x2: number;
    y2: number;
  }>>([]);

  const activeFilter = filterIssueId !== 'all' ? filterIssueId : internalIssueFilter;
  const isPreInv = currentCase?.meta?.lifecycle_stage === 'pre_investment';

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

  // =========================================================================
  // 1. 动态自适应四层因果知识图谱数据生成 (深度绑定当前案卷上下文，无缝对齐真实争点)
  // =========================================================================

  const rawIssues = currentCase?.issues || [];
  const rawFacts = currentCase?.facts || [];
  const rawElements = currentCase?.elements || [];
  const rawEvidence = currentCase?.evidence || {};
  const rawFindings = currentCase?.findings || [];
  const rawSa = currentCase?.strategic_assessment;
  const hostJur = currentCase?.meta?.jurisdiction || 'asean_id';

  // Tier 1: 在案事实要件
  const factsList = useMemo(() => {
    if (rawIssues.length > 0 && rawFacts.length > 0) {
      return rawFacts.map((f, idx) => {
        const matchedElems = rawElements.filter((e) => (e.fact_links || []).includes(f.fid));
        const matchedIssues = rawIssues.filter((iss) =>
          matchedElems.some((e) => (iss.element_ids || []).includes(e.element_id))
        );

        let primaryChainId = 1;
        if (matchedIssues.length > 0) {
          const issueIdx = rawIssues.findIndex((iss) => iss.issue_id === matchedIssues[0].issue_id);
          primaryChainId = issueIdx >= 0 ? issueIdx + 1 : 1;
        } else if (rawIssues.length > 0) {
          primaryChainId = (idx % rawIssues.length) + 1;
        }

        let shortTitle = f.text_zh;
        if (shortTitle.length > 38) {
          shortTitle = shortTitle.slice(0, 38) + '...';
        }

        return {
          id: f.fid,
          tag: f.fid,
          chainId: primaryChainId,
          title: shortTitle,
          full_text: f.text_zh,
          status: '在案确认事实',
          matchedIssueIds: matchedIssues.map((iss) => `I${rawIssues.indexOf(iss) + 1}`),
        };
      });
    }

    if (isPreInv) {
      return [
        {
          id: 'F1',
          tag: 'F1',
          chainId: 1,
          title: '拟投资东道国特许经营基础设施，外资股比拟设为 49%',
          full_text: '项目投资方案设计设立印尼属地项目公司(PMA)，中资持股49%，属地国企持股51%，触发外资准入强行持牌审查。',
          status: '已确定架构',
        },
        {
          id: 'F2',
          tag: 'F2',
          chainId: 2,
          title: '原住民习惯法土地征拆与特许权期限，面临政权更迭征收敞口',
          full_text: '特许经营权期限拟定为30年，核心厂址涉及属地原住民部落土地，存在换届政策转向与特许权撤销风险。',
          status: '要害事实',
        },
        {
          id: 'F3',
          tag: 'F3',
          chainId: 3,
          title: '拟采购关键发电设备自国内出口，东道国要求高本地化率 (TKDN)',
          full_text: 'EPC施工合同要求设备本地化率达40%，国内先进成套机电设备需向能矿部申请工业产能不足法定豁免。',
          status: '双方核实',
        },
        {
          id: 'F4',
          tag: 'F4',
          chainId: 4,
          title: '属于境外重大国有资产投资，面临国资委35号令与数据跨境门禁',
          full_text: '境外投资金额超过3亿美元，属于国资委35号令特别监管类项目，且涉密工程地理测绘数据禁止违规跨境。',
          status: '监管事实',
        },
      ];
    }

    if (hostJur === 'asean_my') {
      return [
        {
          id: 'F1',
          tag: 'F1',
          chainId: 1,
          title: '吉隆坡轻轨工程分包背靠背付款 (Pay-when-paid) 纠纷',
          full_text: '总承包商以分包合同中订有“以发包人付款为前提”条款为由暂缓付款，分包商向 AIAC 提起 CIPAA 极速法定裁决。',
          status: '已确认事实',
        },
        {
          id: 'F2',
          tag: 'F2',
          chainId: 2,
          title: '承包商于工程阻工后知悉并发出索赔通知',
          full_text: '因发包人迟延提供工作面与变更指令，承包商发出索赔通知，发包人抗辩已过合同 28 天除斥期失权。',
          status: '双方确认',
        },
        {
          id: 'F3',
          tag: 'F3',
          chainId: 3,
          title: '属地 CIDB 施工资质合规与工程款分包扣减争议',
          full_text: '发包人主张总包商与分包商应依据 CIDB Act 520 承担属地劳工与工程资质连带责任并要求扣除款项。',
          status: '已确认事实',
        },
        {
          id: 'F4',
          tag: 'F4',
          chainId: 4,
          title: '业主威胁向商业银行发起见索即付履约保函索兑',
          full_text: '在 CIPAA 裁决审理期间，发包人向开证银行出具违约函件，企图恶意全额索兑履约保函。',
          status: '核心争议',
        },
      ];
    }

    return [
      {
        id: 'F1',
        tag: 'F1',
        chainId: 1,
        title: '原住民习惯法土地 (Hak Ulayat) 征拆阻工迟延交地 180 天',
        full_text: '印尼国家电力公司(PLN)迟延交付现场达180天，属地村民依据原住民习惯法土地设置障碍，总包商无法连续施工。',
        status: '已确认事实',
      },
      {
        id: 'F2',
        tag: 'F2',
        chainId: 2,
        title: '总包商于知悉受阻第35天发索赔函且未签署印尼语版本',
        full_text: '总包商于事件发生第35天向监理工程师发出EOT工期顺延通知，业主抗辩已过FIDIC 20.1条28天除斥期失权，且主张外文合同无效。',
        status: '双方确认',
      },
      {
        id: 'F3',
        tag: 'F3',
        chainId: 3,
        title: '逆变器本土化率仅 28%（法定 40%），工业部下达滞纳金通知',
        full_text: '属地工业部MOI审计认定逆变器及辅机本土化率未达标，业主据此对已完工合格工程量扣减4200万美元进度款。',
        status: '已确认事实',
      },
      {
        id: 'F4',
        tag: 'F4',
        chainId: 4,
        title: '业主突击向开证行发起 10% 见索即付履约保函恶意全额索兑',
        full_text: '在双方争议尚处于友好协商期间，业主向雅加达开证行出具虚假违约声明，突袭索兑见索即付履约保函。',
        status: '核心争议',
      },
    ];
  }, [currentCase, isPreInv, hostJur]);

  // Tier 2: 争议焦点与法定要件
  const issuesList = useMemo(() => {
    if (rawIssues.length > 0) {
      const chineseNums = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十'];
      return rawIssues.map((iss, idx) => {
        const chainId = idx + 1;
        const matchingElems = rawElements.filter((el) => (iss.element_ids || []).includes(el.element_id));
        const elemSummary = matchingElems.length > 0
          ? matchingElems.map((e) => e.name_zh).join(' · ')
          : (iss.kind === 'fact' ? '案件事实要件审查' : '法定实体构成要件');

        let shortName = iss.text_zh;
        if (shortName.length > 42) {
          shortName = shortName.slice(0, 42) + '...';
        }

        return {
          id: `I${chainId}`,
          code: isPreInv ? `支柱${chineseNums[idx] || chainId}` : `争点${chineseNums[idx] || chainId}`,
          chainId,
          name: shortName,
          elem: elemSummary,
          desc: iss.text_zh,
        };
      });
    }

    if (isPreInv) {
      return [
        {
          id: 'I1',
          code: '争点一',
          chainId: 1,
          name: '东道国外资持牌准入 (BUJKA/PCAB) 与强行联营体穿透',
          elem: '外资股比上限穿透与属地公司名义代持(Nominee)无效刑事阻却',
          desc: '核查东道国建筑法外资股比限制，论证属地联营体(JO/KSO)的法定持牌资质。',
        },
        {
          id: 'I2',
          code: '争点二',
          chainId: 2,
          name: '特许经营协议换届政策变更与 BIT 间接征收保护伞',
          elem: '特许权单方废除构成隐性征收(Creeping Expropriation)要件',
          desc: '论证政策转向与电价调整是否构成违反双边投资保护协定(BIT)公平公正待遇。',
        },
        {
          id: 'I3',
          code: '争点三',
          chainId: 3,
          name: '属地化率 (TKDN) 阶梯达标要求与技术准入豁免',
          elem: '国内无合格本土产能前提下的法定豁免审批程序要件',
          desc: '论证印尼能矿部 MEMR 11/2024 豁免准入红线，防范后续履约违约罚款。',
        },
        {
          id: 'I4',
          code: '争点四',
          chainId: 4,
          name: '国资委 35 号令事前论证合规与跨境数据出境审批',
          elem: '重大投资决策尽调全流程留痕与涉密数据合规审查',
          desc: '满足国资委境外投资事前法律意见书硬性门槛，完成数据安全法第36条核验。',
        },
      ];
    }

    if (hostJur === 'asean_my') {
      return [
        {
          id: 'I1',
          code: '争点一',
          chainId: 1,
          name: 'CIPAA 2012 第35条背靠背条款法定绝对无效与款项保障',
          elem: '马来西亚 2012 年建筑业付款与裁决法第 35 条强行法',
          desc: '依 CIPAA 第35条，有条件付款条款（Pay-when-paid）自始无效，总包商不得据此拒付分包款。',
        },
        {
          id: 'I2',
          code: '争点二',
          chainId: 2,
          name: '预防原则 (Prevention Principle) 与工程延误时间重置',
          elem: '发包人交地阻碍导致违约金 (LD) 机制失效要件',
          desc: '普通法权威先例：发包人违约造成延误且阻碍顺延时，时间恢复自由 (Time at large)，发包人无权扣除 LD。',
        },
        {
          id: 'I3',
          code: '争点三',
          chainId: 3,
          name: 'CIDB Act 520 建筑行业资质与本地劳工分包配额',
          elem: '马来西亚建筑工业发展局第 520 号法案合规要件',
          desc: '核查分包工程属地执照登记要求与土著分包比例，防范行政处罚及工程款抗辩。',
        },
        {
          id: 'I4',
          code: '争点四',
          chainId: 4,
          name: 'AIAC 极速裁决与商业银行保函欺诈止付',
          elem: '亚洲国际仲裁中心 (AIAC) 法定裁决程序与止付禁令标准',
          desc: '在 CIPAA 裁决审理期间，以恶意突击索兑构成显失公平为由向吉隆坡高院申请保函止付令。',
        },
      ];
    }

    if (hostJur === 'asean_vn') {
      return [
        {
          id: 'I1',
          code: '争点一',
          chainId: 1,
          name: '2025新建设法第 86.2 条发包人交地迟延与工期顺延',
          elem: '越南 2025 新建设法 (Law 135/2025) 第 86.2 条延误归责要件',
          desc: '论证现场交地迟延属发包人违约责任，承包商享有依法顺延工期抗辩权。',
        },
        {
          id: 'I2',
          code: '争点二',
          chainId: 2,
          name: '越南商法典第 301 条预定损害赔偿 8% 法定上限红线',
          elem: '违约金与预定损害赔偿法定强行上限封顶要件',
          desc: '依据越南 2005 年商法第 301 条，违约金不得超过违约部分合同金额之 8%。',
        },
        {
          id: 'I3',
          code: '争点三',
          chainId: 3,
          name: '投资法 (Law 61/2020) 属地资质许可与外汇结汇合规',
          elem: '越南外商投资登记证 (IRC) 与外国承包商施工许可要件',
          desc: '核查外国承包商施工许可证 (Contractor Permit)，防范行政处罚风险。',
        },
        {
          id: 'I4',
          code: '争点四',
          chainId: 4,
          name: 'VIAC 越南国际仲裁与保函紧急临时保护措施',
          elem: '越仲 VIAC 仲裁规则临时措施与商业银行止付要件',
          desc: '向仲裁庭或越南法院申请针对见索即付保函的紧急临时保全命令。',
        },
      ];
    }

    return [
      {
        id: 'I1',
        code: '争点一',
        chainId: 1,
        name: 'FIDIC 8.4 工期顺延 (EOT) 与习惯法免责抗辩',
        elem: '延误归责于业主现场交付义务违约 (FIDIC Clause 17.3)',
        desc: '论证原住民征地受阻依法属于业主应承担的风险，承包商享有顺延工期抗辩权。',
      },
      {
        id: 'I2',
        code: '争点二',
        chainId: 2,
        name: 'SEMA 3/2023 善意原则反 28 天除斥期失权',
        elem: '非恶意持续通知与实质知悉事实排除程序失权要件',
        desc: '印尼最高院司法判例：在无恶意且事实已实质知悉前提下，不得仅依形式时效剥夺权利。',
      },
      {
        id: 'I3',
        code: '争点三',
        chainId: 3,
        name: '属地采购率 (TKDN) 产能不足豁免抗辩与反索赔',
        elem: '东道国国内无合格产能事实构成履行不能与罚金抗辩',
        desc: '依据能矿部 MEMR 11/2024，证明属地市场无法提供合格逆变器，豁免罚金扣除。',
      },
      {
        id: 'I4',
        code: '争点四',
        chainId: 4,
        name: 'BS Mount Sophia 显失公平保函止付与背靠背无效',
        elem: '独立保函恶意滥用欺诈标准与 CIPAA 第35条强行无效',
        desc: '在实体争议未决且无真实损失事实下突袭索兑，构成显失公平止付要件。',
      },
    ];
  }, [currentCase, isPreInv, hostJur]);

  // Tier 3: 现行成文法典与基线
  const normsList = useMemo(() => {
    const evEntries = Object.entries(rawEvidence);
    if (rawIssues.length > 0 && evEntries.length > 0) {
      return evEntries.map(([eid, ev], idx) => {
        const matchedStatements = rawFindings.flatMap((fn) => fn.statements || []).filter(
          (s) => (s.evidence_ids || []).includes(eid)
        );
        const matchedElementIds = matchedStatements
          .map((s) => s.element_id)
          .filter(Boolean) as string[];

        rawElements.forEach((el) => {
          if ((el.links || []).some((l) => l.eid === eid) && !matchedElementIds.includes(el.element_id)) {
            matchedElementIds.push(el.element_id);
          }
        });

        const matchedIssues = rawIssues.filter((iss) =>
          (iss.element_ids || []).some((elId) => matchedElementIds.includes(elId))
        );

        let primaryChainId = 1;
        if (matchedIssues.length > 0) {
          const issueIdx = rawIssues.findIndex((iss) => iss.issue_id === matchedIssues[0].issue_id);
          primaryChainId = issueIdx >= 0 ? issueIdx + 1 : 1;
        } else if (rawIssues.length > 0) {
          primaryChainId = (idx % rawIssues.length) + 1;
        }

        const zhTrans = currentCase?.translations?.[eid];
        let normName = ev.ref_id.replace(/[:_]/g, ' ');
        if (ev.ref_id.includes('CIPAA:Sec35') || ev.ref_id.includes('MY_CIPAA:Sec35')) {
          normName = '马来西亚 CIPAA 2012 第 35 条 [背靠背无效]';
        } else if (ev.ref_id.includes('CIPAA:Sec13') || ev.ref_id.includes('MY_CIPAA:Sec13')) {
          normName = '马来西亚 CIPAA 2012 第 13 条 [快速裁决执行]';
        } else if (ev.ref_id.includes('BS_Mount_Sophia')) {
          normName = '新加坡最高院 BS Mount Sophia [2016] 判例 [显失公平]';
        } else if (ev.ref_id.includes('UU:2_2017:Art57') || ev.ref_id.includes('UU:2_2017')) {
          normName = '印尼《建筑服务法》第 2/2017 号第 57 条 [交地补偿]';
        } else if (ev.ref_id.includes('SEMA:3_2023')) {
          normName = '印尼最高院司法通告 SEMA No. 3/2023 [善意履约原则]';
        } else if (ev.ref_id.includes('MEMR:Reg11_2024') || ev.ref_id.includes('11_2024')) {
          normName = '印尼能矿部 MEMR 11/2024 [光伏组件 TKDN 豁免]';
        } else if (ev.ref_id.includes('135_2025_QH15:Art86') || ev.ref_id.includes('135_2025')) {
          normName = '越南《2025新建设法》(Law 135/2025) 第 86.2 条 [工期顺延]';
        } else if (ev.ref_id.includes('210_2026_ND_CP') || ev.ref_id.includes('210_2026')) {
          normName = '越南第 210/2026/ND-CP 号建设合同法令 [延误免责]';
        } else if (ev.ref_id.includes('11966')) {
          normName = '菲律宾 PPP 法典 (RA 11966) [特许权终止公允补偿]';
        } else if (ev.ref_id.includes('ManilaWater')) {
          normName = '菲律宾最高院 PCAB v. Manila Water [废除外资牌照限制]';
        } else if (ev.ref_id.includes('BIT_CHINA_ASEAN')) {
          normName = '中国-东盟投资协定 (BIT) 第 6 条 [间接征收保护]';
        } else if (ev.ref_id.includes('FIDIC')) {
          normName = 'FIDIC 银皮书国际工程合同基准条款';
        }

        return {
          id: `N${idx + 1}`,
          code: ev.ref_id,
          chainId: primaryChainId,
          name: normName,
          category: ev.kind === 'case' ? '司法权威先例' : (isPreInv ? '东道国投资强行法' : '东道国现行成文法'),
          authority_grade: ev.grade === 'A' ? '现行有效强行法 (Grade A)' : '金标准法源',
          full_quote: zhTrans || ev.text_de || ev.ref_id,
          ref_id: ev.ref_id,
          matchedIssueIds: matchedIssues.map((iss) => `I${rawIssues.indexOf(iss) + 1}`),
        };
      });
    }

    if (isPreInv) {
      return [
        {
          id: 'N1',
          code: hostJur === 'asean_my' ? 'MY_CIDB:Act520' : (hostJur === 'asean_vn' ? 'VN_INV:61_2020' : 'ID_UU:2_2017:Art57'),
          chainId: 1,
          name: hostJur === 'asean_my' ? '马来西亚建筑工业发展局法 CIDB Act 520' : (hostJur === 'asean_vn' ? '越南投资法与外国承包商资质规程' : '印尼建筑法第 2/2017 号第 57 条'),
          category: '东道国强行法',
          authority_grade: '现行成文强行法',
          full_quote: hostJur === 'asean_my' ? '所有在马来西亚境内实施的建筑工程均须由持有效 CIDB 注册证书的主体承揽，禁止无牌挂靠。' : (hostJur === 'asean_vn' ? '外商投资企业必须在计划投资部取得投资登记证 (IRC) 及对应工程承包许可。' : '外商独资或控股企业承接工程必须与属地持牌企业组建联合体(JO)，禁止名义代持。'),
          ref_id: hostJur === 'asean_my' ? 'MY_CIDB:Act520' : (hostJur === 'asean_vn' ? 'VN_INV:61_2020' : 'ID_UU:2_2017:Art57'),
        },
        {
          id: 'N2',
          code: 'BIT_CHINA_ASEAN:Art6',
          chainId: 2,
          name: '中国-东盟投资协定 (BIT) 第 6 条',
          category: '国际投资保护条约',
          authority_grade: '国际投资仲裁条约',
          full_quote: '缔约任何一方不得对缔约另一方投资者的投资采取征收、国有化或具有同等效力的间接措施，除非给予迅速、充分、有效的补偿。',
          ref_id: 'BIT_CHINA_ASEAN:Art6',
        },
        {
          id: 'N3',
          code: hostJur === 'asean_my' ? 'MY_MOF:Bumiputera_Policy' : (hostJur === 'asean_vn' ? 'VN_DECREE:35_2021' : 'ID_MEMR:11_2024'),
          chainId: 3,
          name: hostJur === 'asean_my' ? '马来西亚财政部土著分包与采购指引' : (hostJur === 'asean_vn' ? '越南 35/2021/ND-CP 号公私合作规程' : '印尼能矿部 MEMR 第 11/2024 号令'),
          category: '部委规章与指标',
          authority_grade: '现行部委规章',
          full_quote: hostJur === 'asean_my' ? '大型基础设施项目应满足属地分包与土著供应商采购配额，以确保项目准入与合规审查通过。' : (hostJur === 'asean_vn' ? 'PPP项目投资人应依投资法典合规办理本地分包与环境影响评估许可。' : '若国内市场无合格产能或产品未能通过国际认证，经部委专家组核准可给予 100% 临时进口豁免。'),
          ref_id: hostJur === 'asean_my' ? 'MY_MOF:Bumiputera_Policy' : (hostJur === 'asean_vn' ? 'VN_DECREE:35_2021' : 'ID_MEMR:11_2024'),
        },
        {
          id: 'N4',
          code: 'PRC_SASAC:Order35',
          chainId: 4,
          name: '国资委 35 号令 & 数据安全法第 36 条',
          category: '中国法出海管辖',
          authority_grade: '中央企业特别监管令',
          full_quote: '央企境外重大投资必须完成事前国别法律风险穿透论证；涉密工程数据非经审批不得向外国司法或执法机构提供。',
          ref_id: 'PRC_SASAC:Order35',
        },
      ];
    }

    if (hostJur === 'asean_my') {
      return [
        {
          id: 'N1',
          code: 'MY_CIPAA:2012:Sec35',
          chainId: 1,
          name: '马来西亚 CIPAA 2012 第 35 条 [背靠背无效]',
          category: '东道国特别法定强行法',
          authority_grade: '联邦议会强行法 (Tier 1)',
          full_quote: '建筑合同中任何规定“以第三方付款为条件”的支付条款（Pay-when-paid / Pay-if-paid），自始绝对无效且不可执行。',
          ref_id: 'MY_CIPAA:2012:Sec35',
        },
        {
          id: 'N2',
          code: 'MY_CONTRACTS:1950:Sec56',
          chainId: 2,
          name: '马来西亚 1950 年合同法第 56 条与阻碍原则',
          category: '普通法核心合同法典',
          authority_grade: '联邦成文法与判例法',
          full_quote: '若因合同一方自身阻碍致使履约迟延，非违约方有权主张合理工期宽延，发包人不得就自身违约延误扣取违约金。',
          ref_id: 'MY_CONTRACTS:1950:Sec56',
        },
        {
          id: 'N3',
          code: 'MY_CIDB:Act520',
          chainId: 3,
          name: '马来西亚建筑工业发展局法 (CIDB Act 520)',
          category: '行业监管与资质强行法',
          authority_grade: '属地行业法定规章',
          full_quote: '所有在马来西亚境内实施的建筑工程及分包商均须持有 CIDB 颁发的有效注册等级证书，未持有者面临工程款抗辩与行政罚金。',
          ref_id: 'MY_CIDB:Act520',
        },
        {
          id: 'N4',
          code: 'MY_HC:Alstom_v_Insigma:2018',
          chainId: 4,
          name: '马来西亚高院 Alstom v. Insigma 判例',
          category: '普通法保函止付权威先例',
          authority_grade: '马来西亚高等法院判例',
          full_quote: '在当事人存在实质工程争议且索兑缺乏真诚基础时，若继续索兑构成极度显失公平 (Unconscionability)，法院有权签发临时止付令。',
          ref_id: 'MY_HC:Alstom_v_Insigma:2018',
        },
      ];
    }

    if (hostJur === 'asean_vn') {
      return [
        {
          id: 'N1',
          code: 'VN_CONST_LAW:2025:Art86',
          chainId: 1,
          name: '越南《2025新建设法》(Law 135/2025) 第 86.2 条',
          category: '东道国建设法强行法',
          authority_grade: '越南国会法典 (Tier 1)',
          full_quote: '发包人未按期移交施工场地导致关键路径阻断的，承包商享有依法顺延竣工期限之法定权利，发包人不得主张预定损害赔偿。',
          ref_id: 'VN_CONST_LAW:2025:Art86',
        },
        {
          id: 'N2',
          code: 'VN_COMM_LAW:2005:Art301',
          chainId: 2,
          name: '越南 2005 年商法典第 301 条 [违约金 8% 封顶]',
          category: '民商法典法定强行规则',
          authority_grade: '国会商事成文法典',
          full_quote: '合同双方约定的违约赔偿金总额不得超过受违约影响合同部分价值的 8%，超出部分自始无效。',
          ref_id: 'VN_COMM_LAW:2005:Art301',
        },
        {
          id: 'N3',
          code: 'VN_INV_LAW:61_2020',
          chainId: 3,
          name: '越南 2020 年投资法 (Law 61/2020/QH14)',
          category: '外商投资监管法典',
          authority_grade: '现行投资成文法典',
          full_quote: '外商投资建设工程应依法办理投资登记证 (IRC) 及承包商许可证，合规进行属地劳工聘用与外汇结汇。',
          ref_id: 'VN_INV_LAW:61_2020',
        },
        {
          id: 'N4',
          code: 'VIAC_RULES:2024:Art21',
          chainId: 4,
          name: '越南国际仲裁中心 (VIAC) 仲裁规则第 21 条',
          category: '国际仲裁保全规则',
          authority_grade: '权威仲裁机构规则',
          full_quote: '仲裁庭有权根据当事人申请裁定紧急临时保护措施，包括责令发包人暂缓保函索兑以避免不可弥补之损害。',
          ref_id: 'VIAC_RULES:2024:Art21',
        },
      ];
    }

    return [
      {
        id: 'N1',
        code: 'FIDIC_SILVER:Clause8.4',
        chainId: 1,
        name: 'FIDIC 银皮书第 8.4 条 [工期顺延]',
        category: 'FIDIC 国际工程基准',
        authority_grade: '行业合同基准 (Tier 1)',
        full_quote: '如因业主未根据第2.1条要求提供现场占有权或可归责于雇主的阻碍导致延误，承包商有权要求顺延竣工时间。',
        ref_id: 'FIDIC_SILVER:Clause8.4',
      },
      {
        id: 'N2',
        code: 'ID_SEMA:3_2023',
        chainId: 2,
        name: '印尼最高院司法通函 SEMA 3/2023',
        category: '最高法院司法规则',
        authority_grade: '最高法院司法指引',
        full_quote: '各方在商事合同订立与履约中应遵循民法典第1338条善意原则；无恶意事实下，未签署印尼文文本不得单独作为合同无效之诉由。',
        ref_id: 'ID_SEMA:3_2023',
      },
      {
        id: 'N3',
        code: 'ID_MOI:35_2025',
        chainId: 3,
        name: '印尼工业部 MOI 35/2025 本地化率规程',
        category: '东道国行政规章',
        authority_grade: '现行部委强行规程',
        full_quote: '新能源电站机电设备本地化率达标评估应扣除不可抗力及供应链短缺不可归责期间。',
        ref_id: 'ID_MOI:35_2025',
      },
      {
        id: 'N4',
        code: 'SG_BSMountSophia:2016',
        chainId: 4,
        name: '新加坡最高院 BS Mount Sophia [2016]',
        category: '国际仲裁权威先例',
        authority_grade: '普通法上诉庭先例',
        full_quote: '见索即付保函虽具独立性，但在索兑人缺乏善意根据、构成显失公平 (Unconscionability) 时，法院应予禁令止付。',
        ref_id: 'SG_BSMountSophia:2016',
      },
    ];
  }, [currentCase, isPreInv, hostJur]);

  // Tier 4: 司法判例与反制方案
  const precedentsList = useMemo(() => {
    if (rawIssues.length > 0) {
      const chineseNums = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十'];
      return rawIssues.map((iss, idx) => {
        const chainId = idx + 1;
        const ob = rawSa?.outcome_branches?.[idx];
        const rd = rawSa?.red_team_defenses?.[idx];

        let title = ob?.title || rd?.opposing_claim;
        let ruling = ob?.condition_precedent || rd?.opposing_basis || '严格遵循东道国现行法典与最高法院金标准先例。';
        let strategy = ob?.outcome_summary || rd?.factual_counter_point || '全面锁定在案证据，向法庭/仲裁庭提交实体确权与保全主张。';
        let typeName = '司法确权对策';

        if (iss.text_zh.includes('CIPAA') || iss.text_zh.includes('背靠背')) {
          typeName = '法定裁决抗辩';
          title = '【CIPAA 裁决反制】援引 CIPAA 第 35 条主张背靠背条款自始绝对无效';
          ruling = '马来西亚联邦法院裁判规则：CIPAA 具有法定强制力，任何以发包人付款为前提之分包条款均属无效。';
          strategy = '向 AIAC 提交法定裁决抗辩状，主张分包工程进度款立即清偿，锁定发包人连带责任。';
        } else if (iss.text_zh.includes('保函') || iss.text_zh.includes('BS Mount Sophia') || iss.text_zh.includes('显失公平')) {
          typeName = '司法禁令救济';
          title = '【高院保函禁令】向新加坡高等法院申请见索即付保函显失公平止付令';
          ruling = '新加坡上诉庭 BS Mount Sophia [2016] 规则：在索兑缺乏真诚基础时，构成显失公平 (Unconscionability) 止付要件。';
          strategy = '24小时内向法院申请民事单方禁令，并向开证行送达止付通知，向中国信保提交 30 日出险报损。';
        } else if (iss.text_zh.includes('习惯法') || iss.text_zh.includes('Hak Ulayat') || iss.text_zh.includes('交地迟延')) {
          typeName = '工期顺延确权';
          title = '【FIDIC 8.4 顺延】习惯法土地受阻工期顺延与费用全额补偿';
          ruling = '印尼《建筑服务法》第57条及 FIDIC 8.4：业主因原住民土地征拆迟延交付构成实质违约，工期法定顺延。';
          strategy = '出示土地移交迟延备忘录，驳回发包人违约金主张，锁定工期顺延与窝工补偿。';
        } else if (iss.text_zh.includes('SEMA') || iss.text_zh.includes('印尼语') || iss.text_zh.includes('语言法')) {
          typeName = '善意履约抗辩';
          title = '【SEMA 3/2023】印尼最高院善意原则排除纯英文协议机械无效抗辩';
          ruling = '印尼最高法院 SEMA No. 3/2023 司法通告：涉外商事合同缺少印尼语译本不得单独宣告合同无效。';
          strategy = '提交双语谈判往来邮件及履约事实记录，依法驳回业主恶意无效抗辩。';
        } else if (iss.text_zh.includes('TKDN') || iss.text_zh.includes('本地化率')) {
          typeName = '法定技术豁免';
          title = '【TKDN 法定豁免】依据能矿部 MEMR 11/2024 申请国内无量产豁免批文';
          ruling = '印尼能矿部 MEMR Reg 11/2024：属地工业无合格量产能力前提下，依法核发技术豁免批文。';
          strategy = '凭 Sucofindo 检验证明向能矿部与工业部备案，阻断业主从工程款中扣除罚款。';
        } else if (iss.text_zh.includes('新建设法') || iss.text_zh.includes('预定损害赔偿')) {
          typeName = '法定封顶抗辩';
          title = '【2025新建设法】援引越南新建设法 86.2 条及商法 301 条违约金法定上限';
          ruling = '越南《2025新建设法》第 86.2 条：发包人交地迟延归责于发包人，违约金不得超过法定上限。';
          strategy = '向发包人发出法定核减通知函，向 VIAC 申请临时保护措施阻断保函索兑。';
        } else if (iss.text_zh.includes('PPP') || iss.text_zh.includes('特许经营')) {
          typeName = '条约征收补偿';
          title = '【BIT 间接征收】依据中国-东盟投资协定第 6 条主张公允市场价值赔偿';
          ruling = '中国-东盟全面经济合作框架协议投资协议第 6 条：东道国征收必须给予迅速、充分、有效补偿。';
          strategy = '搭建新加坡 SPV 激活国际投资仲裁保护伞，锁定特许权公允终止补偿。';
        } else if (iss.text_zh.includes('PCAB') || iss.text_zh.includes('资质')) {
          typeName = '国民待遇救济';
          title = '【PCAB 平等待遇】援引最高院 Manila Water 先例废除外资施工资质限制';
          ruling = '菲律宾最高法院 PCAB v. Manila Water 先例：违宪废除常规承包商牌照外资股比限制。';
          strategy = '向菲律宾承包商执照局申请正规施工牌照，防范属地工程款抗辩。';
        } else if (!title) {
          title = `【争点${chineseNums[idx] || chainId}决策】权威法源支持与攻防对策`;
        }

        return {
          id: `P${chainId}`,
          code: `P${chainId}`,
          chainId,
          type: typeName,
          title,
          ruling,
          strategy,
        };
      });
    }

    if (isPreInv) {
      return [
        {
          id: 'P1',
          code: 'P1',
          chainId: 1,
          type: '架构防火墙',
          title: '【第三国 SPV】通过新加坡/香港设立 SPV 激活 BIT 条约保护伞',
          ruling: 'ICSID 裁判规则：间接控股投资者通过双重 SPV 穿透结构享有完整 BIT 投资条约实体管辖权。',
          strategy: '建立双层 SPV 防火墙，植入特许权稳定条款 (Stabilization Clause)。',
        },
        {
          id: 'P2',
          code: 'P2',
          chainId: 2,
          type: '稳定条款救济',
          title: '【国际投资仲裁】特许权变更植入 ICSID / SIAC 仲裁与补偿救济',
          ruling: 'Saluka v. Czech Republic 先例：监管政策不可抗变动导致商业价值归零构成间接征收。',
          strategy: '合同明确约定单方调价或违约撤销特许权由 SIAC 国际仲裁管辖并适用市场公允价值赔偿。',
        },
        {
          id: 'P3',
          code: 'P3',
          chainId: 3,
          type: '准入牌照隔离',
          title: '【联营责任隔离】签署属地联营体 (JO/KSO) 权责隔离与牌照合规协议',
          ruling: 'PCAB v. Manila Water 裁判先例：合法联营体不以本地股东绝对实控为前提。',
          strategy: '与属地持牌企业签署明确权责分工协议，避免连带债务无序扩张。',
        },
        {
          id: 'P4',
          code: 'P4',
          chainId: 4,
          type: '国资与信保保全',
          title: '【国资与信保】完成国资委 35 号令备案并投保中信保海外投资险',
          ruling: '中信保承保实务：东道国法律政策征收与汇兑限制属于政治风险核心承保范围。',
          strategy: '提前办理 30 日内出险报损留痕，出具符合司法部规范的标准域外法查明意见书。',
        },
      ];
    }

    if (hostJur === 'asean_my') {
      return [
        {
          id: 'P1',
          code: 'P1',
          chainId: 1,
          type: '法定裁决抗辩',
          title: '【CIPAA 裁决反制】援引 CIPAA 第 35 条主张背靠背条款自始无效',
          ruling: '马来西亚联邦法院裁判规则：CIPAA 具有法定强制力，任何以业主付款为前提之分包条款均属无效。',
          strategy: '向 AIAC 提交法定裁决抗辩状，主张分包工程进度款立即清偿，锁定发包人连带责任。',
        },
        {
          id: 'P2',
          code: 'P2',
          chainId: 2,
          type: '阻碍原则先例',
          title: '【普通法防阻原则】援引 Peak v McKinney 先例主张时间恢复自由',
          ruling: '马来西亚高等法院先例：发包人延误场地交付阻却工期违约金适用，时间归于自由(Time at large)。',
          strategy: '发出索赔确认函，论证发包人未及时提供工作面导致 LD 违约金条款整体失效。',
        },
        {
          id: 'P3',
          code: 'P3',
          chainId: 3,
          type: 'CIDB 资质抗辩',
          title: '【CIDB 合规救济】援引 CIDB Act 520 厘清总包与分包法定资质责任边界',
          ruling: '马来西亚高院判例：分包商登记瑕疵不免除发包人已完工合格工程款支付义务。',
          strategy: '向发包人提交 CIDB 备案批文及合格凭证，阻却发包人借故扣留已完工工程款。',
        },
        {
          id: 'P4',
          code: 'P4',
          chainId: 4,
          type: '司法禁令救济',
          title: '【高院保函禁令】向吉隆坡高院申请见索即付保函恶意索兑禁止令',
          ruling: 'Alstom v. Insigma 规则：在索兑构成显失公平且 AIAC 裁决未决期间，法院签发临时禁令止付。',
          strategy: '24 小时内向吉隆坡高等法院申请民事单方禁令，并向开证行送达止付通知书。',
        },
      ];
    }

    if (hostJur === 'asean_vn') {
      return [
        {
          id: 'P1',
          code: 'P1',
          chainId: 1,
          type: '新建设法索赔',
          title: '【新建设法索赔】依据 2025 新建设法第 86.2 条发出工期顺延通告',
          ruling: '越南建设法规程：发包人迟延交地构成关键路径停工不可归责事实，法定工期顺延。',
          strategy: '向发包人发出法定索赔通知函，锁定关键路径受阻工期，阻断违约金计取。',
        },
        {
          id: 'P2',
          code: 'P2',
          chainId: 2,
          type: '法定封顶抗辩',
          title: '【商法 301 条封顶】援引越南商法第 301 条强制截断超额 8% 违约金',
          ruling: '越南最高法院裁判先例：任何约定超出 8% 封顶之违约金条款超出部分依法不予执行。',
          strategy: '向发包人出示商事法典 8% 强行封顶条款，阻断业主恶意索兑保函超额扣罚。',
        },
        {
          id: 'P3',
          code: 'P3',
          chainId: 3,
          type: '资质许可合规',
          title: '【投资法合规】依 2020 年投资法完成承包商许可证与外汇结汇备案',
          ruling: '越南计划投资部规程：持有外国承包商许可证享有合法外汇利润汇出与工程款受偿保障。',
          strategy: '提交建设部 (BXD) 核发之施工许可及劳工配额清单，化解属地行政合规风险。',
        },
        {
          id: 'P4',
          code: 'P4',
          chainId: 4,
          type: 'VIAC 临时保全',
          title: '【仲裁临时措施】依据 VIAC 规则第 21 条申请保函暂缓索兑保护令',
          ruling: 'VIAC 紧急仲裁规则：为避免当事人发生难以弥补之严重财务损害，有权签发临时救济令。',
          strategy: '48 小时内向 VIAC 仲裁委员会递交紧急临时保护措施申请书，送达开证行。',
        },
      ];
    }

    return [
      {
        id: 'P1',
        code: 'P1',
        chainId: 1,
        type: '合同免责反驳',
        title: '【示范反制条款】原住民习惯法土地免责专用条件与工期补偿主张',
        ruling: 'FIDIC 索赔裁判规则：现场交地违约阻却工期违约金(LD)扣减，承包商有权主张窝工停工补偿。',
        strategy: '向业主发出抗辩函，锁定 180 天业主风险延误，反向主张 3,800 万美元赶工费用。',
      },
      {
        id: 'P2',
        code: 'P2',
        chainId: 2,
        type: '司法抗辩先例',
        title: '【印尼高院抗辩】援引 SEMA 3/2023 善意履约推定反 28 天形式失权',
        ruling: '印尼最高法院判例：在持续通报且业主实质知悉延误事实下，单纯超出28天不得直接判令实体权利丧失。',
        strategy: '提交往来会议纪要与催告函，证明业主自始知悉事实，排除 20.1 条失权抗辩。',
      },
      {
        id: 'P3',
        code: 'P3',
        chainId: 3,
        type: '部委豁免救济',
        title: '【部委豁免申请】依据能矿部 MEMR 11/2024 申请属地产能不足豁免',
        ruling: '印尼工业部听证会实务：具备国际产能合格资质且属地无法供货时，依法给予免罚放行。',
        strategy: '调取属地 3 家供应商拒单证明，向印尼能源部提出法定豁免申请，阻却违约金扣减。',
      },
      {
        id: 'P4',
        code: 'P4',
        chainId: 4,
        type: '程序仲裁禁令',
        title: '【仲裁禁令救济】SIAC 紧急仲裁员 (EA) 独立保函临时止付令',
        ruling: 'BS Mount Sophia 规则：在恶意突击索兑且可能造成不可弥补损害时，签发保函止付裁决。',
        strategy: '48 小时内向 SIAC 申请紧急仲裁员程序，向开证行送达保函冻结令。',
      },
    ];
  }, [currentCase, isPreInv, hostJur]);

  // =========================================================================
  // 2. 动态拓扑连线矩阵定义 (主干因果链 + 跨链交叉涵摄)
  // =========================================================================
  const graphLinks: GraphLink[] = useMemo(() => {
    if (rawIssues.length > 0 && issuesList.length > 0) {
      const links: GraphLink[] = [];

      // 1. Facts -> Issues
      factsList.forEach((f) => {
        const targetIssueId = `I${f.chainId}`;
        links.push({
          from: f.id,
          to: targetIssueId,
          chainId: f.chainId,
        });

        // 交叉连线：若事实同时关涉其他争点
        (f as any).matchedIssueIds?.forEach((issId: string) => {
          if (issId !== targetIssueId && issuesList.some((i) => i.id === issId)) {
            const matchedIssue = issuesList.find((i) => i.id === issId);
            links.push({
              from: f.id,
              to: issId,
              chainId: matchedIssue?.chainId || f.chainId,
              isCrossLink: true,
            });
          }
        });
      });

      // 2. Issues -> Norms
      normsList.forEach((norm) => {
        const sourceIssueId = `I${norm.chainId}`;
        links.push({
          from: sourceIssueId,
          to: norm.id,
          chainId: norm.chainId,
        });

        // 交叉连线：若法规同时关涉其他争点
        (norm as any).matchedIssueIds?.forEach((issId: string) => {
          if (issId !== sourceIssueId && issuesList.some((i) => i.id === issId)) {
            links.push({
              from: issId,
              to: norm.id,
              chainId: norm.chainId,
              isCrossLink: true,
            });
          }
        });
      });

      // 3. Norms -> Precedents
      precedentsList.forEach((p) => {
        const matchingNorms = normsList.filter((n) => n.chainId === p.chainId);
        if (matchingNorms.length > 0) {
          matchingNorms.forEach((n) => {
            links.push({
              from: n.id,
              to: p.id,
              chainId: p.chainId,
            });
          });
        } else {
          links.push({
            from: `I${p.chainId}`,
            to: p.id,
            chainId: p.chainId,
          });
        }
      });

      return links;
    }

    return [
      { from: 'F1', to: 'I1', chainId: 1 },
      { from: 'I1', to: 'N1', chainId: 1 },
      { from: 'N1', to: 'P1', chainId: 1 },
      { from: 'F2', to: 'I2', chainId: 2 },
      { from: 'I2', to: 'N2', chainId: 2 },
      { from: 'N2', to: 'P2', chainId: 2 },
      { from: 'F3', to: 'I3', chainId: 3 },
      { from: 'I3', to: 'N3', chainId: 3 },
      { from: 'N3', to: 'P3', chainId: 3 },
      { from: 'F4', to: 'I4', chainId: 4 },
      { from: 'I4', to: 'N4', chainId: 4 },
      { from: 'N4', to: 'P4', chainId: 4 },
      { from: 'F1', to: 'I2', chainId: 1, isCrossLink: true },
      { from: 'I1', to: 'N2', chainId: 2, isCrossLink: true },
      { from: 'N4', to: 'P2', chainId: 4, isCrossLink: true },
    ];
  }, [rawIssues.length, factsList, issuesList, normsList, precedentsList]);

  // 点击或悬停的激活锚点目标 ID
  const activeTargetId = hoveredNodeId || selectedNodeId;

  // 使用有向因果图闭包计算当前应点亮的全部节点集合与连线集合 (有向因果链路双向约束，杜绝全图泛滥)
  const { activeNodeIds, activeLinkIds } = useMemo(() => {
    if (!activeTargetId) {
      return { activeNodeIds: new Set<string>(), activeLinkIds: new Set<string>() };
    }

    const forwardMap = new Map<string, string[]>();
    const backwardMap = new Map<string, string[]>();

    graphLinks.forEach((l) => {
      if (!forwardMap.has(l.from)) forwardMap.set(l.from, []);
      forwardMap.get(l.from)!.push(l.to);

      if (!backwardMap.has(l.to)) backwardMap.set(l.to, []);
      backwardMap.get(l.to)!.push(l.from);
    });

    const activeNodes = new Set<string>([activeTargetId]);

    // 正向因果推演：向下游合法延展 (事实 -> 争点 -> 法条 -> 对策)
    const forwardQueue = [activeTargetId];
    while (forwardQueue.length > 0) {
      const curr = forwardQueue.shift()!;
      const neighbors = forwardMap.get(curr) || [];
      for (const next of neighbors) {
        if (!activeNodes.has(next)) {
          activeNodes.add(next);
          forwardQueue.push(next);
        }
      }
    }

    // 反向事实溯源：向上游合法回溯 (对策 -> 法条 -> 争点 -> 事实)
    const backwardQueue = [activeTargetId];
    while (backwardQueue.length > 0) {
      const curr = backwardQueue.shift()!;
      const parents = backwardMap.get(curr) || [];
      for (const prev of parents) {
        if (!activeNodes.has(prev)) {
          activeNodes.add(prev);
          backwardQueue.push(prev);
        }
      }
    }

    // 精确提取处于激活通路的链路
    const activeLinks = new Set<string>();
    graphLinks.forEach((l, idx) => {
      if (activeNodes.has(l.from) && activeNodes.has(l.to)) {
        activeLinks.add(`link-${idx}-${l.from}-${l.to}`);
      }
    });

    return { activeNodeIds: activeNodes, activeLinkIds: activeLinks };
  }, [activeTargetId, graphLinks]);

  // 重新计算并测量 SVG 连线坐标 (带隐藏节点跳过，避免无效计算与异常路径)
  const recomputeLinks = useCallback(() => {
    if (!containerRef.current) return;
    const containerRect = containerRef.current.getBoundingClientRect();
    const paths: Array<{
      id: string;
      d: string;
      chainId: number;
      from: string;
      to: string;
      isCrossLink?: boolean;
      x1: number;
      y1: number;
      x2: number;
      y2: number;
    }> = [];

    graphLinks.forEach((link, idx) => {
      const fromEl = nodeRefs.current[link.from];
      const toEl = nodeRefs.current[link.to];
      if (!fromEl || !toEl) return;

      // 性能与逻辑优化：若节点处于隐藏状态（如被 activeFilter 过滤），直接跳过计算
      if (fromEl.offsetParent === null || toEl.offsetParent === null) return;

      const fromRect = fromEl.getBoundingClientRect();
      const toRect = toEl.getBoundingClientRect();

      // 连接起点：左卡片右侧中点
      const x1 = fromRect.right - containerRect.left;
      const y1 = fromRect.top + fromRect.height / 2 - containerRect.top;

      // 连接终点：右卡片左侧中点
      const x2 = toRect.left - containerRect.left;
      const y2 = toRect.top + toRect.height / 2 - containerRect.top;

      const dx = Math.max(24, (x2 - x1) * 0.44);
      const d = `M ${x1} ${y1} C ${x1 + dx} ${y1}, ${x2 - dx} ${y2}, ${x2} ${y2}`;

      paths.push({
        id: `link-${idx}-${link.from}-${link.to}`,
        d,
        chainId: link.chainId,
        from: link.from,
        to: link.to,
        isCrossLink: link.isCrossLink,
        x1,
        y1,
        x2,
        y2,
      });
    });

    setSvgPaths(paths);
  }, [graphLinks]);

  // 高性能调度器：使用 requestAnimationFrame 防抖，杜绝滚动和微交互导致的布局抖动 (Layout Thrashing)
  const scheduleRecompute = useCallback(() => {
    if (rafIdRef.current !== null) {
      cancelAnimationFrame(rafIdRef.current);
    }
    rafIdRef.current = requestAnimationFrame(() => {
      recomputeLinks();
      rafIdRef.current = null;
    });
  }, [recomputeLinks]);

  // 监听容器真实尺寸变化与滤镜改变，彻底解绑鼠标 hover 导致的无谓重测
  useEffect(() => {
    scheduleRecompute();
    const container = containerRef.current;
    if (!container) return;

    let ro: ResizeObserver | null = null;
    if (typeof ResizeObserver !== 'undefined') {
      ro = new ResizeObserver(() => {
        scheduleRecompute();
      });
      ro.observe(container);
    }

    window.addEventListener('resize', scheduleRecompute);
    const t = setTimeout(scheduleRecompute, 120);

    return () => {
      if (ro) ro.disconnect();
      window.removeEventListener('resize', scheduleRecompute);
      clearTimeout(t);
      if (rafIdRef.current !== null) {
        cancelAnimationFrame(rafIdRef.current);
      }
    };
  }, [scheduleRecompute, activeFilter, factsList, issuesList, normsList, precedentsList]);

  // 精准默认激活的检视节点（优先对齐当前过滤选中的争点）
  const activeInspector = useMemo(() => {
    if (activeInspectorNode) return activeInspectorNode;
    if (activeFilter !== 'all') {
      const targetChainId = parseInt(activeFilter.replace(/\D/g, ''), 10);
      const matchedNorm = normsList.find((n) => n.chainId === targetChainId);
      if (matchedNorm) return matchedNorm;
      const matchedIssue = issuesList.find((i) => i.id === activeFilter || i.chainId === targetChainId);
      if (matchedIssue) return matchedIssue;
    }
    return normsList[0] || issuesList[0] || factsList[0];
  }, [activeInspectorNode, activeFilter, normsList, issuesList, factsList]);

  return (
    <div
      ref={containerRef}
      className={`relative w-full h-full flex flex-col justify-between ${
        fullscreen ? 'select-text' : 'apple-bento-card rounded-2xl p-5 shadow-xs'
      }`}
    >
      {/* 嵌入态顶部简要标题栏 (非全屏时显示) */}
      {!fullscreen && (
        <div className="flex items-center justify-between border-b border-slate-100 pb-3 mb-3">
          <div className="flex items-center gap-2">
            <div className="w-6 h-6 rounded-lg bg-blue-50 text-blue-600 flex items-center justify-center border border-blue-100">
              <Share2 className="w-3.5 h-3.5 text-blue-600" />
            </div>
            <h3 className="text-xs font-bold text-slate-900 tracking-tight">
              法源因果拓扑图谱 (Causal Topology)
            </h3>
            <span className="text-[10px] text-slate-400 font-mono hidden sm:inline">
              事实 ➔ 争点 ➔ 规范 ➔ 对策
            </span>
          </div>

          <div className="flex items-center gap-2">
            {onOpenFullscreen && (
              <button
                type="button"
                onClick={onOpenFullscreen}
                className="px-2.5 py-1 rounded-xl bg-blue-50 text-blue-700 hover:bg-blue-100/80 border border-blue-200/80 text-xs font-semibold flex items-center gap-1.5 transition-all cursor-pointer shadow-2xs active:scale-95"
              >
                <Maximize2 className="w-3.5 h-3.5" />
                <span>全屏沉浸探索</span>
              </button>
            )}
          </div>
        </div>
      )}

      {/* SVG 矢量动态连线画布层 (置于 z-25 覆盖于导轨底色之上，透传鼠标事件至卡片) */}
      <svg className="pointer-events-none absolute inset-0 w-full h-full z-25 overflow-visible">
        <defs>
          <linearGradient id="gradient-active-link" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="#3b82f6" />
            <stop offset="45%" stopColor="#6366f1" />
            <stop offset="100%" stopColor="#8b5cf6" />
          </linearGradient>
          <linearGradient id="gradient-cross-link" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="#0ea5e9" />
            <stop offset="100%" stopColor="#a855f7" />
          </linearGradient>
        </defs>

        {svgPaths.map((p) => {
          const isFilterMatched = activeFilter === 'all' || activeFilter === `I${p.chainId}`;
          if (!isFilterMatched) return null;

          const isLinkActive = activeLinkIds.has(p.id);
          const isAnyActive = activeNodeIds.size > 0;

          if (!isLinkActive) {
            return (
              <g key={p.id}>
                <path
                  d={p.d}
                  fill="none"
                  stroke={p.isCrossLink ? 'rgba(148, 163, 184, 0.4)' : 'rgba(203, 213, 225, 0.75)'}
                  strokeWidth={p.isCrossLink ? 1.2 : 1.5}
                  strokeDasharray={p.isCrossLink ? '4 3' : undefined}
                  opacity={isAnyActive ? 0.16 : 0.7}
                  className="transition-all duration-200"
                />
                <circle cx={p.x1} cy={p.y1} r={2} fill="#cbd5e1" opacity={isAnyActive ? 0.16 : 0.6} />
                <circle cx={p.x2} cy={p.y2} r={2} fill="#cbd5e1" opacity={isAnyActive ? 0.16 : 0.6} />
              </g>
            );
          }

          return (
            <g key={p.id} className="transition-all duration-200">
              {/* Layer 1: 环境光晕 */}
              <path
                d={p.d}
                fill="none"
                stroke={p.isCrossLink ? 'url(#gradient-cross-link)' : 'url(#gradient-active-link)'}
                strokeWidth={6.5}
                strokeLinecap="round"
                className="apple-glow-breathe pointer-events-none"
              />

              {/* Layer 2: 实体导轨光缆 */}
              <path
                d={p.d}
                fill="none"
                stroke={p.isCrossLink ? 'url(#gradient-cross-link)' : 'url(#gradient-active-link)'}
                strokeWidth={2.4}
                strokeLinecap="round"
                strokeDasharray={p.isCrossLink ? '5 3' : undefined}
                opacity={0.95}
              />

              {/* Layer 3: 白光脉冲流动束 */}
              {!p.isCrossLink && (
                <path
                  d={p.d}
                  fill="none"
                  stroke="#ffffff"
                  strokeWidth={1.8}
                  strokeLinecap="round"
                  className="apple-link-pulse pointer-events-none"
                />
              )}

              {/* 起止端磁吸同心锚点 */}
              <circle cx={p.x1} cy={p.y1} r={4.5} fill="#3b82f6" opacity={0.25} />
              <circle cx={p.x1} cy={p.y1} r={2.8} fill="#3b82f6" stroke="#ffffff" strokeWidth={1} />
              <circle cx={p.x2} cy={p.y2} r={4.5} fill="#8b5cf6" opacity={0.25} />
              <circle cx={p.x2} cy={p.y2} r={2.8} fill="#8b5cf6" stroke="#ffffff" strokeWidth={1} />
            </g>
          );
        })}
      </svg>

      {/* 四列分层网格展示 */}
      <div
        ref={gridContainerRef}
        onClick={() => {
          setSelectedNodeId(null);
          setHoveredNodeId(null);
        }}
        onScroll={scheduleRecompute}
        className="grid grid-cols-1 md:grid-cols-4 gap-4 sm:gap-5 relative z-20 flex-1 overflow-y-auto pr-1 pb-1"
      >
        {/* ========================================================================= */}
        {/* Column 1: 在案事实要件 (深海矿石灰 Slate-Titanium) */}
        {/* ========================================================================= */}
        <div className="bg-slate-900/[0.025] backdrop-blur-2xl rounded-[22px] p-3 border border-black/[0.06] shadow-2xs flex flex-col space-y-2.5">
          <div className="flex items-center justify-between px-1.5 shrink-0 pb-2 border-b border-black/[0.05]">
            <span className="text-xs font-semibold text-slate-800 flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-slate-400 ring-2 ring-slate-300/50" />
              <span>案件事实要件</span>
            </span>
            <span className="text-[10px] font-mono text-slate-500 bg-black/[0.04] px-1.5 py-0.5 rounded">Facts</span>
          </div>

          <div className="space-y-2.5 flex-1 flex flex-col justify-between">
            {factsList.map((f) => {
              const isFilteredOut = activeFilter !== 'all' && activeFilter !== `I${f.chainId}`;
              const isSelected = selectedNodeId === f.id;
              const isHovered = hoveredNodeId === f.id;
              const isTarget = isSelected || isHovered;
              const isActive = activeNodeIds.has(f.id);
              const isDimmed = activeNodeIds.size > 0 && !isActive;

              return (
                <div
                  key={f.id}
                  ref={(el) => {
                    nodeRefs.current[f.id] = el;
                  }}
                  onMouseEnter={() => {
                    setHoveredNodeId(f.id);
                    setActiveInspectorNode(f);
                  }}
                  onMouseLeave={() => setHoveredNodeId(null)}
                  onClick={(e) => {
                    e.stopPropagation();
                    setSelectedNodeId((prev) => (prev === f.id ? null : f.id));
                    setActiveInspectorNode(f);
                  }}
                  className={`apple-graph-card p-3 rounded-[16px] border text-xs cursor-pointer relative group transition-all duration-200 ${
                    isFilteredOut
                      ? 'hidden'
                      : isTarget
                      ? 'bg-white border-slate-600 shadow-md ring-2 ring-slate-400/25 -translate-y-0.5'
                      : isActive
                      ? 'bg-white border-slate-500 shadow-sm ring-1 ring-slate-400/20'
                      : isDimmed
                      ? 'opacity-25 grayscale-[0.45] scale-[0.985] bg-white/40 border-black/[0.04] hover:opacity-100 hover:grayscale-0 hover:scale-100'
                      : 'bg-white/90 backdrop-blur-xl border-black/[0.07] hover:border-slate-300 shadow-[0_1px_3px_rgba(0,0,0,0.03)] hover:shadow-[0_4px_14px_rgba(0,0,0,0.06)] hover:-translate-y-0.5'
                  }`}
                >
                  <div className="flex items-center justify-between mb-1.5">
                    <span
                      className={`font-mono font-semibold text-[10px] px-1.5 py-0.5 rounded-md border ${
                        isActive
                          ? 'bg-slate-800 text-white border-slate-800'
                          : 'bg-black/[0.04] text-slate-700 border-black/[0.06]'
                      }`}
                    >
                      {f.tag}
                    </span>
                    <div className="flex items-center gap-1.5">
                      {isSelected && (
                        <span className="text-[9px] font-semibold text-slate-700 bg-slate-100 px-1 py-0.2 rounded border border-slate-200">
                          锁定
                        </span>
                      )}
                      <span className="text-[10px] font-medium text-slate-500">
                        {f.status}
                      </span>
                    </div>
                  </div>
                  <p className="text-xs font-semibold text-slate-900 leading-snug line-clamp-2">
                    {f.title}
                  </p>
                  <div className="mt-2 pt-1.5 border-t border-slate-100 flex items-center justify-between text-[10px] text-slate-400 font-mono">
                    <span>因果源点</span>
                    <span className="text-blue-600 font-sans font-medium group-hover:underline">穿透展开 ➔</span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* ========================================================================= */}
        {/* Column 2: 争议焦点与法定要件 (皇家钴蓝 Cobalt-Blue) */}
        {/* ========================================================================= */}
        <div className="bg-slate-900/[0.025] backdrop-blur-2xl rounded-[22px] p-3 border border-black/[0.06] shadow-2xs flex flex-col space-y-2.5">
          <div className="flex items-center justify-between px-1.5 shrink-0 pb-2 border-b border-black/[0.05]">
            <span className="text-xs font-semibold text-slate-800 flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-blue-500 ring-2 ring-blue-300/50" />
              <span>争议焦点拆解</span>
            </span>
            <span className="text-[10px] font-mono text-blue-600 bg-blue-50 px-1.5 py-0.5 rounded border border-blue-100">Issues</span>
          </div>

          <div className="space-y-2.5 flex-1 flex flex-col justify-between">
            {issuesList.map((iss) => {
              const isFilteredOut = activeFilter !== 'all' && activeFilter !== iss.id;
              const isSelected = selectedNodeId === iss.id;
              const isHovered = hoveredNodeId === iss.id;
              const isTarget = isSelected || isHovered;
              const isActive = activeNodeIds.has(iss.id);
              const isDimmed = activeNodeIds.size > 0 && !isActive;

              return (
                <div
                  key={iss.id}
                  ref={(el) => {
                    nodeRefs.current[iss.id] = el;
                  }}
                  onMouseEnter={() => {
                    setHoveredNodeId(iss.id);
                    setActiveInspectorNode(iss);
                  }}
                  onMouseLeave={() => setHoveredNodeId(null)}
                  onClick={(e) => {
                    e.stopPropagation();
                    setSelectedNodeId((prev) => (prev === iss.id ? null : iss.id));
                    setActiveInspectorNode(iss);
                  }}
                  className={`apple-graph-card p-3 rounded-[16px] border text-xs cursor-pointer relative group transition-all duration-200 ${
                    isFilteredOut
                      ? 'hidden'
                      : isTarget
                      ? 'bg-white border-blue-600 shadow-md ring-2 ring-blue-500/25 -translate-y-0.5'
                      : isActive
                      ? 'bg-white border-blue-500 shadow-sm ring-1 ring-blue-400/20'
                      : isDimmed
                      ? 'opacity-25 grayscale-[0.45] scale-[0.985] bg-white/40 border-black/[0.04] hover:opacity-100 hover:grayscale-0 hover:scale-100'
                      : 'bg-white/90 backdrop-blur-xl border-black/[0.07] hover:border-blue-300 shadow-[0_1px_3px_rgba(0,0,0,0.03)] hover:shadow-[0_4px_14px_rgba(0,0,0,0.06)] hover:-translate-y-0.5'
                  }`}
                >
                  <div className="flex items-center justify-between mb-1.5">
                    <span
                      className={`font-mono font-semibold text-[10px] px-1.5 py-0.5 rounded-md border ${
                        isActive
                          ? 'bg-blue-600 text-white border-blue-600'
                          : 'bg-blue-50/80 text-blue-700 border-blue-200/60'
                      }`}
                    >
                      {iss.code}
                    </span>
                    <div className="flex items-center gap-1.5">
                      {isSelected && (
                        <span className="text-[9px] font-semibold text-blue-700 bg-blue-50 px-1 py-0.2 rounded border border-blue-200">
                          锁定
                        </span>
                      )}
                      <span
                        className={`w-2 h-2 rounded-full transition-all ${
                          isActive ? 'bg-blue-600 ring-4 ring-blue-400/30 animate-pulse' : 'bg-slate-300'
                        }`}
                      />
                    </div>
                  </div>
                  <h4 className="text-xs font-semibold text-slate-900 leading-snug line-clamp-2">
                    {iss.name}
                  </h4>
                  <div className="mt-2 pt-1.5 border-t border-slate-100 text-[10px] text-slate-600 truncate">
                    要件：{iss.elem}
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* ========================================================================= */}
        {/* Column 3: 现行成文法典 (翡翠常青 Emerald-Green) */}
        {/* ========================================================================= */}
        <div className="bg-slate-900/[0.025] backdrop-blur-2xl rounded-[22px] p-3 border border-black/[0.06] shadow-2xs flex flex-col space-y-2.5">
          <div className="flex items-center justify-between px-1.5 shrink-0 pb-2 border-b border-black/[0.05]">
            <span className="text-xs font-semibold text-slate-800 flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-emerald-500 ring-2 ring-emerald-300/50" />
              <span>东盟现行法典</span>
            </span>
            <span className="text-[10px] font-mono text-emerald-700 bg-emerald-50 px-1.5 py-0.5 rounded border border-emerald-100">Norms</span>
          </div>

          <div className="space-y-2.5 flex-1 flex flex-col justify-between">
            {normsList.map((norm) => {
              const isFilteredOut = activeFilter !== 'all' && activeFilter !== `I${norm.chainId}`;
              const isSelected = selectedNodeId === norm.id;
              const isHovered = hoveredNodeId === norm.id;
              const isTarget = isSelected || isHovered;
              const isActive = activeNodeIds.has(norm.id);
              const isDimmed = activeNodeIds.size > 0 && !isActive;

              return (
                <div
                  key={norm.id}
                  ref={(el) => {
                    nodeRefs.current[norm.id] = el;
                  }}
                  onMouseEnter={() => {
                    setHoveredNodeId(norm.id);
                    setActiveInspectorNode(norm);
                  }}
                  onMouseLeave={() => setHoveredNodeId(null)}
                  onClick={(e) => {
                    e.stopPropagation();
                    setSelectedNodeId((prev) => (prev === norm.id ? null : norm.id));
                    setActiveInspectorNode(norm);
                    onSelectNorm(norm.ref_id);
                  }}
                  className={`apple-graph-card p-3 rounded-[16px] border text-xs cursor-pointer relative group transition-all duration-200 ${
                    isFilteredOut
                      ? 'hidden'
                      : isTarget
                      ? 'bg-white border-emerald-600 shadow-md ring-2 ring-emerald-500/25 -translate-y-0.5'
                      : isActive
                      ? 'bg-white border-emerald-500 shadow-sm ring-1 ring-emerald-400/20'
                      : isDimmed
                      ? 'opacity-25 grayscale-[0.45] scale-[0.985] bg-white/40 border-black/[0.04] hover:opacity-100 hover:grayscale-0 hover:scale-100'
                      : 'bg-white/90 backdrop-blur-xl border-black/[0.07] hover:border-emerald-300 shadow-[0_1px_3px_rgba(0,0,0,0.03)] hover:shadow-[0_4px_14px_rgba(0,0,0,0.06)] hover:-translate-y-0.5'
                  }`}
                >
                  <div className="flex items-center justify-between mb-1.5">
                    <span
                      className={`font-mono font-semibold text-[10px] px-1.5 py-0.5 rounded-md border truncate max-w-[130px] ${
                        isActive
                          ? 'bg-emerald-600 text-white border-emerald-600'
                          : 'bg-emerald-50 text-emerald-800 border-emerald-200/80'
                      }`}
                    >
                      {norm.code}
                    </span>
                    <div className="flex items-center gap-1.5">
                      {isSelected && (
                        <span className="text-[9px] font-semibold text-emerald-700 bg-emerald-50 px-1 py-0.2 rounded border border-emerald-200">
                          锁定
                        </span>
                      )}
                      <span className="text-[10px] font-medium text-slate-500">
                        {norm.category}
                      </span>
                    </div>
                  </div>

                  <p className="text-xs font-semibold text-slate-900 leading-snug line-clamp-2">
                    {norm.name}
                  </p>

                  <div className="flex items-center justify-between pt-1.5 mt-2 border-t border-slate-100">
                    <span
                      onClick={(e) => {
                        e.stopPropagation();
                        onSelectNorm(norm.ref_id);
                        openRightDock('law_reader', norm.ref_id);
                      }}
                      className="text-[10px] text-blue-600 font-medium flex items-center gap-1 hover:underline cursor-pointer"
                    >
                      <span>精读条文</span>
                      <ExternalLink className="w-2.5 h-2.5" />
                    </span>

                    <button
                      type="button"
                      onClick={(e) => {
                        e.stopPropagation();
                        handleAttachStatute(norm);
                      }}
                      className={`text-[10px] px-2 py-0.5 rounded-md font-medium flex items-center gap-1 cursor-pointer transition-all ${
                        pinnedNormId === norm.id
                          ? 'bg-emerald-600 text-white shadow-2xs'
                          : 'bg-black/[0.03] text-slate-700 border border-black/[0.06] hover:bg-black/[0.06]'
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
                          <span>引用</span>
                        </>
                      )}
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* ========================================================================= */}
        {/* Column 4: 司法先例与反制方案 (紫晶罗兰 Amethyst-Violet) */}
        {/* ========================================================================= */}
        <div className="bg-slate-900/[0.025] backdrop-blur-2xl rounded-[22px] p-3 border border-black/[0.06] shadow-2xs flex flex-col space-y-2.5">
          <div className="flex items-center justify-between px-1.5 shrink-0 pb-2 border-b border-black/[0.05]">
            <span className="text-xs font-semibold text-slate-800 flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-purple-500 ring-2 ring-purple-300/50" />
              <span>裁判对策与反制</span>
            </span>
            <span className="text-[10px] font-mono text-purple-700 bg-purple-50 px-1.5 py-0.5 rounded border border-purple-100">Strategy</span>
          </div>

          <div className="space-y-2.5 flex-1 flex flex-col justify-between">
            {precedentsList.map((p) => {
              const isFilteredOut = activeFilter !== 'all' && activeFilter !== `I${p.chainId}`;
              const isSelected = selectedNodeId === p.id;
              const isHovered = hoveredNodeId === p.id;
              const isTarget = isSelected || isHovered;
              const isActive = activeNodeIds.has(p.id);
              const isDimmed = activeNodeIds.size > 0 && !isActive;

              return (
                <div
                  key={p.id}
                  ref={(el) => {
                    nodeRefs.current[p.id] = el;
                  }}
                  onMouseEnter={() => {
                    setHoveredNodeId(p.id);
                    setActiveInspectorNode(p);
                  }}
                  onMouseLeave={() => setHoveredNodeId(null)}
                  onClick={(e) => {
                    e.stopPropagation();
                    setSelectedNodeId((prev) => (prev === p.id ? null : p.id));
                    setActiveInspectorNode(p);
                  }}
                  className={`apple-graph-card p-3 rounded-[16px] border text-xs cursor-pointer relative group transition-all duration-200 ${
                    isFilteredOut
                      ? 'hidden'
                      : isTarget
                      ? 'bg-white border-purple-600 shadow-md ring-2 ring-purple-500/25 -translate-y-0.5'
                      : isActive
                      ? 'bg-white border-purple-500 shadow-sm ring-1 ring-purple-400/20'
                      : isDimmed
                      ? 'opacity-25 grayscale-[0.45] scale-[0.985] bg-white/40 border-black/[0.04] hover:opacity-100 hover:grayscale-0 hover:scale-100'
                      : 'bg-white/90 backdrop-blur-xl border-black/[0.07] hover:border-purple-300 shadow-[0_1px_3px_rgba(0,0,0,0.03)] hover:shadow-[0_4px_14px_rgba(0,0,0,0.06)] hover:-translate-y-0.5'
                  }`}
                >
                  <div className="flex items-center justify-between mb-1.5">
                    <span
                      className={`font-mono font-semibold text-[10px] px-1.5 py-0.5 rounded-md border ${
                        isActive
                          ? 'bg-purple-600 text-white border-purple-600'
                          : 'bg-purple-50 text-purple-800 border-purple-200/80'
                      }`}
                    >
                      {p.type}
                    </span>
                    <div className="flex items-center gap-1.5">
                      {isSelected && (
                        <span className="text-[9px] font-semibold text-purple-700 bg-purple-50 px-1 py-0.2 rounded border border-purple-200">
                          锁定
                        </span>
                      )}
                      <CheckCircle2
                        className={`w-3.5 h-3.5 ${
                          isActive ? 'text-purple-600' : 'text-slate-400'
                        }`}
                      />
                    </div>
                  </div>

                  <p className="text-xs font-semibold text-slate-900 leading-snug line-clamp-2">
                    {p.title}
                  </p>

                  <div className="mt-2 pt-1.5 border-t border-slate-100 text-[10px] text-slate-600 truncate">
                    对策：{p.strategy}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* ========================================================================= */}
      {/* 底部 Apple 风格微型透视信息坞 (Inspector Dock) */}
      {/* ========================================================================= */}
      {fullscreen && (
        <div className="mt-3 pt-3 border-t border-black/[0.06] bg-white/85 backdrop-blur-2xl rounded-2xl p-3 sm:p-3.5 flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs shadow-[0_12px_40px_rgba(0,0,0,0.06)] border border-black/[0.06] transition-all">
          <div className="flex items-center gap-2.5 min-w-0">
            <div className="w-7 h-7 rounded-xl bg-slate-900 text-white flex items-center justify-center shrink-0 shadow-2xs">
              <Sparkles className="w-3.5 h-3.5 text-blue-400" />
            </div>
            <div className="min-w-0">
              <div className="flex items-center gap-2 flex-wrap">
                <span className="font-semibold text-slate-900">
                  当前节点：{activeInspector?.code || activeInspector?.tag || '全部'} · {activeInspector?.name || activeInspector?.title}
                </span>
                {selectedNodeId && (
                  <span className="text-[10px] font-semibold text-blue-700 bg-blue-50 px-2 py-0.5 rounded-full border border-blue-200">
                    已锁定全链透视 (点击空白处重置)
                  </span>
                )}
                {activeNodeIds.size > 1 && (
                  <span className="text-[10px] font-mono text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-full border border-emerald-200">
                    已穿透关联 {activeNodeIds.size} 处因果要素
                  </span>
                )}
              </div>
              <p className="text-[11px] text-slate-500 truncate mt-0.5">
                {activeInspector?.full_quote || activeInspector?.ruling || activeInspector?.full_text || '点击或悬停节点即可点亮完整多分支因果链条'}
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2 shrink-0">
            <div className="flex items-center gap-3 text-[11px] text-slate-400 mr-2">
              <span className="flex items-center gap-1.5">
                <span className="w-2 h-2 rounded-full bg-blue-500 shadow-[0_0_6px_rgba(59,130,246,0.6)]" />
                <span>实线：主因果链</span>
              </span>
              <span className="flex items-center gap-1.5">
                <span className="w-2 h-2 rounded-full bg-purple-400" />
                <span>虚线：交叉涵摄</span>
              </span>
            </div>

            {activeInspector?.ref_id && (
              <button
                type="button"
                onClick={() => {
                  onSelectNorm(activeInspector.ref_id);
                  openRightDock('law_reader', activeInspector.ref_id);
                  showToast(`已在右侧辅助面板载入【${activeInspector.code || activeInspector.name}】条文`, 'info');
                }}
                className="px-3.5 py-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-white text-xs font-semibold flex items-center gap-1.5 shadow-2xs cursor-pointer active:scale-95 transition-all"
              >
                <BookOpen className="w-3.5 h-3.5" />
                <span>查阅法条全文</span>
              </button>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
