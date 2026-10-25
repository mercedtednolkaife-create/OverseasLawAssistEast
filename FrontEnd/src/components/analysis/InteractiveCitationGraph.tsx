import React, { useState, useMemo, useRef, useEffect, useCallback } from 'react';
import { useApp } from '../../context/AppContext';
import { lawAgentApi } from '../../api/lawAgentApi';
import {
  Share2,
  ExternalLink,
  CheckCircle2,
  BookmarkCheck,
  Check,
  Plus,
  Maximize2,
  ShieldCheck,
  Briefcase,
  Layers,
  ArrowRight,
  Info,
  Sparkles,
  BookOpen,
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
  const nodeRefs = useRef<Record<string, HTMLDivElement | null>>({});
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
  // 1. 严格四层逻辑知识图谱数据生成 (依据案卷阶段自适应切换)
  // =========================================================================

  // Tier 1: 在案事实要件
  const factsList = useMemo(() => {
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

    // 履约争议模式 (Mode 2)
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
  }, [isPreInv]);

  // Tier 2: 争议焦点与法定要件
  const issuesList = useMemo(() => {
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
  }, [isPreInv]);

  // Tier 3: 现行成文法典与基线
  const normsList = useMemo(() => {
    if (isPreInv) {
      return [
        {
          id: 'N1',
          code: 'ID_UU:2_2017:Art57',
          chainId: 1,
          name: '印尼建筑法第 2/2017 号第 57 条',
          category: '东道国强行法',
          authority_grade: '现行成文强行法',
          full_quote: '外商独资或控股企业承接工程必须与属地持牌企业组建联合体(JO)，禁止名义代持。',
          ref_id: 'ID_UU:2_2017:Art57',
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
          code: 'ID_MEMR:11_2024',
          chainId: 3,
          name: '印尼能矿部 MEMR 第 11/2024 号令',
          category: '部委规章与指标',
          authority_grade: '现行部委规章',
          full_quote: '若国内市场无合格产能或产品未能通过国际认证，经部委专家组核准可给予 100% 临时进口豁免。',
          ref_id: 'ID_MEMR:11_2024',
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
  }, [isPreInv]);

  // Tier 4: 司法判例与反制方案
  const precedentsList = useMemo(() => {
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
  }, [isPreInv]);

  // =========================================================================
  // 2. 因果拓扑连线矩阵定义 (主因果链 1~4 + 关键交叉因果影响)
  // =========================================================================
  const graphLinks: GraphLink[] = useMemo(() => [
    // 主链路 1: 现场交地/资质 ➔ EOT/准入 ➔ FIDIC 8.4/建筑法 ➔ 示范反制
    { from: 'F1', to: 'I1', chainId: 1 },
    { from: 'I1', to: 'N1', chainId: 1 },
    { from: 'N1', to: 'P1', chainId: 1 },

    // 主链路 2: 通知时效/习惯法 ➔ 28天/BIT ➔ SEMA 3/2023/BIT ➔ 善意反失权
    { from: 'F2', to: 'I2', chainId: 2 },
    { from: 'I2', to: 'N2', chainId: 2 },
    { from: 'N2', to: 'P2', chainId: 2 },

    // 主链路 3: 本地化率/TKDN ➔ 采购指标 ➔ MOI/MEMR ➔ 产能豁免
    { from: 'F3', to: 'I3', chainId: 3 },
    { from: 'I3', to: 'N3', chainId: 3 },
    { from: 'N3', to: 'P3', chainId: 3 },

    // 主链路 4: 突袭保函/国资 ➔ 显失公平/35号令 ➔ BS Mount Sophia/国资 ➔ 紧急仲裁止付
    { from: 'F4', to: 'I4', chainId: 4 },
    { from: 'I4', to: 'N4', chainId: 4 },
    { from: 'N4', to: 'P4', chainId: 4 },

    // 交叉因果穿透拓扑 (体现法律实务真实网络)
    { from: 'F1', to: 'I2', chainId: 1, isCrossLink: true }, // 交地受阻持续事实影响索赔通知起算点
    { from: 'I1', to: 'N2', chainId: 2, isCrossLink: true }, // 工期顺延权利受善意原则支持
    { from: 'N4', to: 'P2', chainId: 4, isCrossLink: true }, // 显失公平抗辩支撑善意原则
  ], []);

  // 点击或悬停的激活锚点目标 ID
  const activeTargetId = hoveredNodeId || selectedNodeId;

  // 使用有向因果图闭包计算当前应点亮的全部节点集合与连线集合 (广度优先双向遍历)
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

    // 正向 BFS：收集下游直接与间接影响的全部节点 (事实 -> 争点 -> 法条 -> 对策)
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

    // 反向 BFS：收集上游因果渊源的所有支撑节点 (对策 -> 法条 -> 争点 -> 事实)
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

    // 提取子图内所有相连的链路 ID
    const activeLinks = new Set<string>();
    graphLinks.forEach((l, idx) => {
      if (activeNodes.has(l.from) && activeNodes.has(l.to)) {
        activeLinks.add(`link-${idx}-${l.from}-${l.to}`);
      }
    });

    return { activeNodeIds: activeNodes, activeLinkIds: activeLinks };
  }, [activeTargetId, graphLinks]);

  // 重新计算并测量 SVG 连线坐标
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

      const fromRect = fromEl.getBoundingClientRect();
      const toRect = toEl.getBoundingClientRect();

      // 连接起点：左卡片右侧中点
      const x1 = fromRect.right - containerRect.left;
      const y1 = fromRect.top + fromRect.height / 2 - containerRect.top;

      // 连接终点：右卡片左侧中点
      const x2 = toRect.left - containerRect.left;
      const y2 = toRect.top + toRect.height / 2 - containerRect.top;

      const dx = Math.max(20, (x2 - x1) * 0.45);
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

  useEffect(() => {
    recomputeLinks();
    window.addEventListener('resize', recomputeLinks);
    // 增加多微帧重算，保证弹窗弹性滑入过程中 SVG 贝塞尔曲线实时贴合锚点
    const t1 = setTimeout(recomputeLinks, 60);
    const t2 = setTimeout(recomputeLinks, 180);
    const t3 = setTimeout(recomputeLinks, 360);
    return () => {
      window.removeEventListener('resize', recomputeLinks);
      clearTimeout(t1);
      clearTimeout(t2);
      clearTimeout(t3);
    };
  }, [recomputeLinks, factsList, issuesList, normsList, precedentsList, activeFilter, selectedNodeId, hoveredNodeId]);

  // 默认激活的检视节点（若未悬停则显示第一行规范）
  const activeInspector = activeInspectorNode || normsList[0];

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
            <Share2 className="w-4 h-4 text-blue-600" />
            <h3 className="text-xs font-bold text-slate-900">
              四层穿透因果拓扑图谱 (Causal Topology)
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
        </defs>

        {svgPaths.map((p) => {
          const isFilterMatched = activeFilter === 'all' || activeFilter === `I${p.chainId}`;
          if (!isFilterMatched) return null;

          const isLinkActive =
            activeLinkIds.has(p.id) ||
            (activeNodeIds.has(p.from) && activeNodeIds.has(p.to));
          const isAnyActive = activeNodeIds.size > 0;

          if (!isLinkActive) {
            return (
              <g key={p.id}>
                <path
                  d={p.d}
                  fill="none"
                  stroke={p.isCrossLink ? 'rgba(148, 163, 184, 0.45)' : 'rgba(203, 213, 225, 0.85)'}
                  strokeWidth={p.isCrossLink ? 1.2 : 1.6}
                  strokeDasharray={p.isCrossLink ? '4 3' : undefined}
                  opacity={isAnyActive ? 0.2 : 0.75}
                  className="transition-all duration-300"
                />
                {/* 静息态端点微光定位点 */}
                <circle cx={p.x1} cy={p.y1} r={2} fill="#cbd5e1" opacity={isAnyActive ? 0.2 : 0.6} />
                <circle cx={p.x2} cy={p.y2} r={2} fill="#cbd5e1" opacity={isAnyActive ? 0.2 : 0.6} />
              </g>
            );
          }

          return (
            <g key={p.id} className="transition-all duration-300">
              {/* Layer 1: macOS 柔光环境呼吸光晕 (基于 SVG 实体多层发光，杜绝纯水平线零高度剪裁 Bug) */}
              <path
                d={p.d}
                fill="none"
                stroke="url(#gradient-active-link)"
                strokeWidth={6.5}
                strokeLinecap="round"
                className="apple-glow-breathe pointer-events-none"
              />

              {/* Layer 2: 核心能量导轨实体光缆 */}
              <path
                d={p.d}
                fill="none"
                stroke="url(#gradient-active-link)"
                strokeWidth={2.4}
                strokeLinecap="round"
                opacity={0.95}
              />

              {/* Layer 3: 类 macOS 高频流动白光光子脉冲束 (循环平滑光斑流) */}
              <path
                d={p.d}
                fill="none"
                stroke="#ffffff"
                strokeWidth={1.8}
                strokeLinecap="round"
                className="apple-link-pulse pointer-events-none"
              />

              {/* Layer 4: 起始端磁吸锚点 (含微光外晕) */}
              <circle cx={p.x1} cy={p.y1} r={4.5} fill="#3b82f6" opacity={0.3} />
              <circle cx={p.x1} cy={p.y1} r={2.8} fill="#3b82f6" stroke="#ffffff" strokeWidth={1} />

              {/* Layer 5: 终止端磁吸接收锚点 (含微光外晕) */}
              <circle cx={p.x2} cy={p.y2} r={4.5} fill="#8b5cf6" opacity={0.3} />
              <circle cx={p.x2} cy={p.y2} r={2.8} fill="#8b5cf6" stroke="#ffffff" strokeWidth={1} />
            </g>
          );
        })}
      </svg>

      {/* 四列分层网格展示 (每个分栏置于 macOS 高透毛玻璃导轨卡槽中) */}
      <div
        onClick={() => setSelectedNodeId(null)}
        onScroll={recomputeLinks}
        className="grid grid-cols-1 md:grid-cols-4 gap-4 sm:gap-5 relative z-20 flex-1 overflow-y-auto pr-1 pb-1"
      >
        {/* ========================================================================= */}
        {/* Column 1: 在案事实要件 */}
        {/* ========================================================================= */}
        <div className="bg-slate-900/[0.025] backdrop-blur-2xl rounded-[22px] p-3 border border-black/[0.06] shadow-2xs flex flex-col space-y-2.5">
          <div className="flex items-center justify-between px-1.5 shrink-0 pb-2 border-b border-black/[0.05]">
            <span className="text-xs font-semibold text-slate-800 flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-slate-400" />
              <span>案件事实</span>
            </span>
            <span className="text-[10px] font-mono text-slate-400">Facts</span>
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
                  className={`apple-graph-card p-3 rounded-[16px] border text-xs cursor-pointer relative group ${
                    isFilteredOut
                      ? 'hidden'
                      : isTarget
                      ? 'bg-white border-blue-500 shadow-md ring-2 ring-blue-500/20 -translate-y-0.5'
                      : isActive
                      ? 'bg-white border-blue-500/90 shadow-sm ring-1 ring-blue-400/20'
                      : isDimmed
                      ? 'opacity-35 grayscale-[0.35] bg-white/60 border-black/[0.04] hover:opacity-100 hover:grayscale-0'
                      : 'bg-white/90 backdrop-blur-xl border-black/[0.08] hover:border-black/[0.16] shadow-[0_1px_3px_rgba(0,0,0,0.04),0_1px_1px_rgba(0,0,0,0.02)] hover:shadow-[0_4px_12px_rgba(0,0,0,0.06)] hover:-translate-y-0.5'
                  }`}
                >
                  <div className="flex items-center justify-between mb-1.5">
                    <span
                      className={`font-mono font-semibold text-[10px] px-1.5 py-0.5 rounded-md border ${
                        isActive
                          ? 'bg-blue-600 text-white border-blue-600'
                          : 'bg-black/[0.04] text-slate-700 border-black/[0.06]'
                      }`}
                    >
                      {f.tag}
                    </span>
                    <div className="flex items-center gap-1.5">
                      {isSelected && (
                        <span className="text-[9px] font-semibold text-blue-700 bg-blue-50 px-1 py-0.2 rounded border border-blue-200">
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
        {/* Column 2: 争议焦点与法定要件 */}
        {/* ========================================================================= */}
        <div className="bg-slate-900/[0.025] backdrop-blur-2xl rounded-[22px] p-3 border border-black/[0.06] shadow-2xs flex flex-col space-y-2.5">
          <div className="flex items-center justify-between px-1.5 shrink-0 pb-2 border-b border-black/[0.05]">
            <span className="text-xs font-semibold text-slate-800 flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-blue-500" />
              <span>争点要件</span>
            </span>
            <span className="text-[10px] font-mono text-slate-400">Issues</span>
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
                  className={`apple-graph-card p-3 rounded-[16px] border text-xs cursor-pointer relative group ${
                    isFilteredOut
                      ? 'hidden'
                      : isTarget
                      ? 'bg-white border-indigo-500 shadow-md ring-2 ring-indigo-500/20 -translate-y-0.5'
                      : isActive
                      ? 'bg-white border-indigo-500/90 shadow-sm ring-1 ring-indigo-400/20'
                      : isDimmed
                      ? 'opacity-35 grayscale-[0.35] bg-white/60 border-black/[0.04] hover:opacity-100 hover:grayscale-0'
                      : 'bg-white/90 backdrop-blur-xl border-black/[0.08] hover:border-black/[0.16] shadow-[0_1px_3px_rgba(0,0,0,0.04),0_1px_1px_rgba(0,0,0,0.02)] hover:shadow-[0_4px_12px_rgba(0,0,0,0.06)] hover:-translate-y-0.5'
                  }`}
                >
                  <div className="flex items-center justify-between mb-1.5">
                    <span
                      className={`font-mono font-semibold text-[10px] px-1.5 py-0.5 rounded-md border ${
                        isActive
                          ? 'bg-indigo-600 text-white border-indigo-600'
                          : 'bg-black/[0.04] text-slate-700 border-black/[0.06]'
                      }`}
                    >
                      {iss.code}
                    </span>
                    <div className="flex items-center gap-1.5">
                      {isSelected && (
                        <span className="text-[9px] font-semibold text-indigo-700 bg-indigo-50 px-1 py-0.2 rounded border border-indigo-200">
                          锁定
                        </span>
                      )}
                      <span
                        className={`w-1.5 h-1.5 rounded-full ${
                          isActive ? 'bg-indigo-500 animate-pulse' : 'bg-slate-300'
                        }`}
                      />
                    </div>
                  </div>
                  <h4 className="text-xs font-semibold text-slate-900 leading-snug line-clamp-1">
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
        {/* Column 3: 现行成文法典与基线 */}
        {/* ========================================================================= */}
        <div className="bg-slate-900/[0.025] backdrop-blur-2xl rounded-[22px] p-3 border border-black/[0.06] shadow-2xs flex flex-col space-y-2.5">
          <div className="flex items-center justify-between px-1.5 shrink-0 pb-2 border-b border-black/[0.05]">
            <span className="text-xs font-semibold text-slate-800 flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-emerald-500" />
              <span>现行法典</span>
            </span>
            <span className="text-[10px] font-mono text-slate-400">Norms</span>
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
                  className={`apple-graph-card p-3 rounded-[16px] border text-xs cursor-pointer relative group ${
                    isFilteredOut
                      ? 'hidden'
                      : isTarget
                      ? 'bg-white border-emerald-500 shadow-md ring-2 ring-emerald-500/20 -translate-y-0.5'
                      : isActive
                      ? 'bg-white border-emerald-500/90 shadow-sm ring-1 ring-emerald-400/20'
                      : isDimmed
                      ? 'opacity-35 grayscale-[0.35] bg-white/60 border-black/[0.04] hover:opacity-100 hover:grayscale-0'
                      : 'bg-white/90 backdrop-blur-xl border-black/[0.08] hover:border-black/[0.16] shadow-[0_1px_3px_rgba(0,0,0,0.04),0_1px_1px_rgba(0,0,0,0.02)] hover:shadow-[0_4px_12px_rgba(0,0,0,0.06)] hover:-translate-y-0.5'
                  }`}
                >
                  <div className="flex items-center justify-between mb-1.5">
                    <span
                      className={`font-mono font-semibold text-[10px] px-1.5 py-0.5 rounded-md border ${
                        isActive
                          ? 'bg-emerald-600 text-white border-emerald-600'
                          : 'bg-black/[0.04] text-slate-700 border-black/[0.06]'
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

                  <p className="text-xs font-semibold text-slate-900 leading-snug line-clamp-1">
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
                      <span>精读</span>
                      <ExternalLink className="w-2.5 h-2.5" />
                    </span>

                    <button
                      type="button"
                      onClick={(e) => {
                        e.stopPropagation();
                        handleAttachStatute(norm);
                      }}
                      className={`text-[10px] px-1.5 py-0.5 rounded-md font-medium flex items-center gap-1 cursor-pointer transition-all ${
                        pinnedNormId === norm.id
                          ? 'bg-emerald-600 text-white'
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
        {/* Column 4: 司法先例与反制方案 */}
        {/* ========================================================================= */}
        <div className="bg-slate-900/[0.025] backdrop-blur-2xl rounded-[22px] p-3 border border-black/[0.06] shadow-2xs flex flex-col space-y-2.5">
          <div className="flex items-center justify-between px-1.5 shrink-0 pb-2 border-b border-black/[0.05]">
            <span className="text-xs font-semibold text-slate-800 flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-purple-500" />
              <span>裁判对策</span>
            </span>
            <span className="text-[10px] font-mono text-slate-400">Strategy</span>
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
                  className={`apple-graph-card p-3 rounded-[16px] border text-xs cursor-pointer relative group ${
                    isFilteredOut
                      ? 'hidden'
                      : isTarget
                      ? 'bg-white border-purple-500 shadow-md ring-2 ring-purple-500/20 -translate-y-0.5'
                      : isActive
                      ? 'bg-white border-purple-500/90 shadow-sm ring-1 ring-purple-400/20'
                      : isDimmed
                      ? 'opacity-35 grayscale-[0.35] bg-white/60 border-black/[0.04] hover:opacity-100 hover:grayscale-0'
                      : 'bg-white/90 backdrop-blur-xl border-black/[0.08] hover:border-black/[0.16] shadow-[0_1px_3px_rgba(0,0,0,0.04),0_1px_1px_rgba(0,0,0,0.02)] hover:shadow-[0_4px_12px_rgba(0,0,0,0.06)] hover:-translate-y-0.5'
                  }`}
                >
                  <div className="flex items-center justify-between mb-1.5">
                    <span
                      className={`font-mono font-semibold text-[10px] px-1.5 py-0.5 rounded-md border ${
                        isActive
                          ? 'bg-purple-600 text-white border-purple-600'
                          : 'bg-black/[0.04] text-slate-700 border-black/[0.06]'
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

                  <p className="text-xs font-semibold text-slate-900 leading-snug line-clamp-1">
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
        <div className="mt-3 pt-3 border-t border-black/[0.06] bg-white/80 backdrop-blur-2xl rounded-2xl p-3 sm:p-3.5 flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs shadow-[0_12px_40px_rgba(0,0,0,0.08)] border border-black/[0.06]">
          <div className="flex items-center gap-2.5 min-w-0">
            <div className="w-6 h-6 rounded-lg bg-slate-900 text-white flex items-center justify-center shrink-0 shadow-2xs">
              <Sparkles className="w-3.5 h-3.5" />
            </div>
            <div className="min-w-0">
              <div className="flex items-center gap-2">
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
              <span className="flex items-center gap-1">
                <span className="w-2 h-2 rounded-full bg-blue-500" />
                <span>实线：主因果链</span>
              </span>
              <span className="flex items-center gap-1">
                <span className="w-2 h-2 rounded-full bg-slate-300" />
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
