"""核心数据模型与状态对象定义
严格对齐技术方案 v0.7 第 5.1 节与前端 TypeScript 契约 (FrontEnd/src/types/lawAgent.ts)
"""

from enum import Enum
from typing import List, Dict, Tuple, Optional, Literal, Any
from pydantic import BaseModel, Field


UserRole = Literal["public", "judicial", "practitioner"]
RunMode = Literal["full", "lite", "retrieval"]
CaseWorkflowStatus = Literal[
    "draft", "running", "paused_cisg", "paused_s3", "paused_s8", "completed", "failed"
]


class LifecycleStage(str, Enum):
    """项目生命周期阶段：投前并购与签约审查 vs 履约索赔与争议解决"""
    PRE_INVESTMENT = "pre_investment"         # 模式一：投前并购、准入与签约合规审查
    EXECUTION_DISPUTE = "execution_dispute"   # 模式二：履约索赔、保函止付与争议解决


class ProjectArchetype(str, Enum):
    """工程与投资业态标签：支持多选组合"""
    EPC_CONTRACTING = "EPC_CONTRACTING"       # 国际工程总承包/施工承包 (FIDIC Red/Yellow/Silver)
    PPP_CONCESSION = "PPP_CONCESSION"         # 绿地特许经营/投建营一体化 (BOT/BOOT/PPP)
    CROSS_BORDER_MA = "CROSS_BORDER_MA"       # 褐地跨境股权并购 (SPA/SHA)
    JV_CONSORTIUM = "JV_CONSORTIUM"           # 属地合资或非法人联营体 (KSO/JO)


class SecurityRiskLevel(str, Enum):
    """国家安全与经济安全风险等级"""
    CRITICAL = "critical"   # 红色致命：触发主权违约/隐性征收/制裁黑名单/跨境调证违法
    HIGH = "high"           # 橙色高危：触发关键基础设施外资国安审查/强制股权剥离/合同无效红线
    CAUTION = "caution"     # 黄色关注：触发本地化率(TKDN)偏差/外劳配额/习惯法征地抗争
    SAFE = "safe"           # 绿色常规：一般商事工程履约争议


class SecurityAlertItem(BaseModel):
    """安全哨兵强类型风险预警项目"""
    risk_level: SecurityRiskLevel
    category: Literal[
        "national_security_review",
        "resource_nationalism_tkdn",
        "creeping_expropriation",
        "sanctions_debarment_risk",
        "cross_border_data_art36",
        "sasac_supervision_redline"
    ]
    title_zh: str
    fact_anchor_ids: List[str] = Field(default_factory=list, description="触发预警的事实锚点 F#")
    host_law_basis: List[str] = Field(default_factory=list, description="东道国法源 doc_id")
    prc_or_treaty_basis: List[str] = Field(default_factory=list, description="国内监管法或BIT条约依据 doc_id")
    sinosure_preservation_guide: Optional[str] = Field(None, description="中信保海外投资险/特险30日报损与代位求偿保全指引")
    mandatory_human_checklist: List[str] = Field(default_factory=list, description="央国企法务强制人工核验事项")
    mitigation_actions: List[str] = Field(default_factory=list, description="可执行对冲与反制建议")


class CaseMeta(BaseModel):
    title: Optional[str] = None          # 案件规范化业务标题
    jurisdiction: str = "asean_id"       # 默认东盟印尼法域 (asean_id)
    contract_type: Optional[str] = None
    parties: List[str] = Field(default_factory=list)
    contract_date: Optional[str] = None  # ISO 日期，合同订立日 (必填)
    event_date: Optional[str] = None     # 主要事实发生日 (建议填写)
    choice_of_law: Optional[str] = None  # 选法条款 (如：印尼法 / 越南法 / 新加坡法 / FIDIC)
    signing_date: Optional[str] = None

    # 东盟基建与投资并购核心字段
    lifecycle_stage: Optional[LifecycleStage] = LifecycleStage.EXECUTION_DISPUTE
    project_archetypes: List[ProjectArchetype] = Field(default_factory=list)
    parent_case_id: Optional[str] = None
    fidic_book_edition: Optional[str] = None # '1999_SILVER' | '1999_YELLOW' | '1999_RED' 等
    host_country: Optional[str] = None       # 'ID' | 'VN' | 'MY' | 'SG' | 'TH' | 'PH'
    project_host_country: Optional[str] = None # 项目所在东道国，如 'asean_id', 'asean_vn'
    governing_law_jurisdiction: Optional[str] = None # 合同约定准据法/仲裁地，如 'asean_sg', 'asean_my'
    dispute_resolution: Optional[str] = None # 'SIAC' | 'BANI' | 'AIAC' | 'ICC' | 'Court' 等
    engineering_params: Dict[str, Any] = Field(default_factory=dict) # 结构化工程参数: declared_tkdn_pct, delay_days, main_ld_cap_pct, sub_ld_cap_pct 等

    # 历史字段废弃兼容器
    cisg_excluded: Optional[bool] = None
    both_merchants: Optional[bool] = None


class Claim(BaseModel):
    cid: str                             # 'C1'
    party: str
    text_zh: str


class Fact(BaseModel):
    fid: str                             # 'F1'
    text_zh: str
    span: Optional[Tuple[int, int]] = None  # 在 facts_zh 中的字符区间，用于 V10 溯源
    disputed: bool = False               # 各方主张对该事实不一致；S3 人工确认


class Material(BaseModel):
    mid: str                             # 'M1'
    name: str
    desc_zh: str
    excerpt_zh: Optional[str] = None     # 粘贴摘录
    fact_ids: List[str] = Field(default_factory=list)  # 意图证明的事实 F#


class Issue(BaseModel):
    issue_id: str
    kind: Literal["fact", "law"]         # 事实争点或法律争点
    text_zh: str
    claim_ids: List[str] = Field(default_factory=list)
    element_ids: List[str] = Field(default_factory=list)


class LegalQuestion(BaseModel):
    qid: str
    text_zh: str
    queries_target: List[str] = Field(default_factory=list) # 目标检索语句
    queries_de: List[str] = Field(default_factory=list)     # 历史兼容器
    template_id: Optional[str] = None
    must_norms: List[str] = Field(default_factory=list)
    status: Literal["draft", "confirmed"] = "draft"
    done: bool = False                   # 已完成 S4–S7


class Evidence(BaseModel):
    eid: str                             # 'E1'
    kind: Literal["norm", "case"]
    role: Literal["law", "similar"] = "law"
    ref_id: str                          # 如 'ID:SEMA_3_2023' 或 'FIDIC:Silver_1999:Clause_8.4'
    text_original: str = ""              # 官方规范或判例原文片段 (不超过 1500 字)
    text_de: str = ""                    # 兼容性镜像：自动同步自 text_original
    text_en: Optional[str] = None        # 英文对照
    text_zh: Optional[str] = None        # 权威中文释义
    language_mode: Literal["bilingual", "trilingual"] = "bilingual"
    translation_source: Optional[str] = "MOJ_FATONG_2026"
    fidic_tier: Optional[str] = None
    fidic_edition: Optional[str] = None
    source_url: str = ""
    stand: Optional[str] = None
    fetched_at: str = ""
    grade: Literal["A", "B", "C", "D"] = "A"

    def __init__(self, **data):
        if "text_original" not in data and "text_de" in data:
            data["text_original"] = data["text_de"]
        elif "text_de" not in data and "text_original" in data:
            data["text_de"] = data["text_original"]
        super().__init__(**data)


class ElementEvidence(BaseModel):
    eid: str
    relation: Literal["supports", "explains", "cited_by"] = "supports"


class ElementState(BaseModel):
    qid: str
    element_id: str                      # 如 'e1', 'e2', 'q'
    name_zh: str
    status: Literal["covered", "partial", "missing"] = "missing"
    links: List[ElementEvidence] = Field(default_factory=list)
    scores: Dict[str, float] = Field(default_factory=dict)  # eid -> 重排得分
    gap_note: Optional[str] = None
    rounds: int = 0                      # 改写检索轮数 (上限 2)
    fact_links: List[str] = Field(default_factory=list)     # 候选关联的事实 F#
    slot_hits: Dict[str, List[str]] = Field(default_factory=dict)  # slot_id -> fact_ids
    material_links: List[str] = Field(default_factory=list) # 候选关联的证据材料 M#
    match_status: Optional[Literal["satisfied", "partial", "missing", "disputed"]] = None
    match_note: Optional[str] = None


ReviewErrorType = Literal[
    "citation", "translation", "missing_element", "overreach",
    "comparative_pollution", "sufficiency", "fact_error", "other"
]


class Statement(BaseModel):
    sid: str
    text_zh: str
    type: Literal["quote", "paraphrase", "inference"]
    evidence_ids: List[str] = Field(default_factory=list)
    part: Literal["A", "B"] = "A"        # A 查明材料包，B 咨询准备包
    fact_ids: List[str] = Field(default_factory=list)       # B 部分陈述引用的事实 F#
    material_ids: List[str] = Field(default_factory=list)   # B 部分陈述引用的证据材料 M#
    element_id: Optional[str] = None     # 所属要件
    quote_de: Optional[str] = None
    grade: Optional[Literal["A", "B", "C", "D"]] = None
    status: Literal["ok", "fail", "downgraded"] = "ok"
    review_action: Optional[Literal["accept", "edit", "reject"]] = None
    review_note: Optional[str] = None
    error_type: Optional[ReviewErrorType] = None


class Finding(BaseModel):
    qid: str
    statements: List[Statement] = Field(default_factory=list)
    gaps: List[str] = Field(default_factory=list)


class EntryCheckItem(BaseModel):
    name: str
    status: Literal["satisfied", "unsatisfied", "uncertain"]
    detail: str


class SimilarCaseItem(BaseModel):
    case_id: str
    eid: str
    court: str
    az: str
    date: str
    similarity_points: List[str] = Field(default_factory=list)
    difference_points: List[str] = Field(default_factory=list)
    court_view_quote_de: str
    court_view_zh: str
    divergence_flag: Literal["consistent", "divergent", "undetermined"] = "undetermined"


class CheckItem(BaseModel):
    code: str                            # V1 - V11
    status: Literal["pass", "fail", "downgraded"]
    qid: Optional[str] = None
    sid: Optional[str] = None
    eid: Optional[str] = None
    reason: str


class DashboardMetrics(BaseModel):
    exact_quotes_ratio: Tuple[int, int] = (0, 0)
    norms_cases_exist_all: bool = True
    unresolved_refs_count: int = 0
    supported_statements_ratio: Tuple[int, int] = (0, 0)
    elements_coverage: Dict[str, int] = Field(default_factory=lambda: {"covered": 0, "partial": 0, "missing": 0})
    elements_match: Dict[str, int] = Field(default_factory=lambda: {"satisfied": 0, "partial": 0, "missing": 0, "disputed": 0})
    facts_traceable_ratio: Tuple[int, int] = (0, 0)
    entity_checks_pass_ratio: Tuple[int, int] = (0, 0)
    comparative_law_flags_count: int = 0
    grades_distribution: Dict[str, int] = Field(default_factory=lambda: {"A": 0, "B": 0, "C": 0, "D": 0})
    timepoint_level: Literal["green", "red", "yellow"] = "yellow"
    cisg_triggered: bool = False
    snapshot_id: str = ""
    report_version: int = 1
    content_hash: str = ""
    mode: RunMode = "full"


class SavedInsight(BaseModel):
    insight_id: str
    case_id: str
    category: Literal["memo", "counsel_question", "trial_outline", "red_team_defense"] = "memo"
    title: str
    content: str
    source_model: Optional[str] = None
    referenced_statutes: List[str] = Field(default_factory=list)
    created_at: str = ""


class OutcomeBranch(BaseModel):
    branch_type: Literal["favorable", "unfavorable", "uncertain"] = "favorable"
    title: str
    condition_precedent: str          # 假定事实/前提要件
    substantive_basis: List[str] = Field(default_factory=list) # 适用法条/权威先例
    key_evidence_required: List[str] = Field(default_factory=list) # 所需关键证据
    outcome_summary: str              # 裁判倾向推演 (严守条件句)
    risk_level: Literal["low", "medium", "high"] = "medium"


class RedTeamDefense(BaseModel):
    defense_id: str                   # 'D1', 'D2', 'D3'
    opposing_claim: str               # 对方可能主张的抗辩切入点
    lethal_index: Literal["high", "critical", "medium"] = "high" # 威胁烈度
    opposing_basis: str               # 对方依据之条文/判例
    counter_weapons: List[str] = Field(default_factory=list) # 我方反制依据与裁判武器 (先例、除外例外规则)
    factual_counter_point: str        # 事实反驳突破口
    evidence_checklist: List[str] = Field(default_factory=list) # 下一步关键调取证据清单


class StrategicAssessment(BaseModel):
    case_id: str
    pivotal_factors: List[str] = Field(default_factory=list) # 胜败摇摆关键变量 / 心证分水岭
    outcome_branches: List[OutcomeBranch] = Field(default_factory=list)
    red_team_defenses: List[RedTeamDefense] = Field(default_factory=list)
    actionable_checklist: List[str] = Field(default_factory=list)
    updated_at: str = ""


class CaseState(BaseModel):
    case_id: str
    title: Optional[str] = None          # 案件规范化业务标题
    snapshot_id: str
    mode: RunMode = "full"
    facts_zh: str
    claims_zh: Optional[str] = None
    meta: CaseMeta = Field(default_factory=CaseMeta)
    flags: List[str] = Field(default_factory=list)
    timepoint: Dict[str, Any] = Field(default_factory=lambda: {"level": "yellow", "reasons": []})
    entry_checks: List[EntryCheckItem] = Field(default_factory=list)
    facts: List[Fact] = Field(default_factory=list)
    claims: List[Claim] = Field(default_factory=list)
    materials: List[Material] = Field(default_factory=list)
    issues: List[Issue] = Field(default_factory=list)
    questions: List[LegalQuestion] = Field(default_factory=list)
    elements: List[ElementState] = Field(default_factory=list)
    evidence: Dict[str, Evidence] = Field(default_factory=dict)
    translations: Dict[str, str] = Field(default_factory=dict)  # eid -> zh
    similar_cases: List[SimilarCaseItem] = Field(default_factory=list)
    counsel_questions: List[str] = Field(default_factory=list)
    findings: List[Finding] = Field(default_factory=list)
    checks: List[CheckItem] = Field(default_factory=list)
    saved_insights: List[SavedInsight] = Field(default_factory=list)
    strategic_assessment: Optional[StrategicAssessment] = None  # 方案A：胜败边界推演与红队攻防对抗
    unparsed_refs: List[Dict[str, Any]] = Field(default_factory=list)
    dashboard: DashboardMetrics = Field(default_factory=DashboardMetrics)
    parent_case_id: Optional[str] = None
    security_alerts: List[SecurityAlertItem] = Field(default_factory=list)
    engineering_audit: Optional[Dict[str, Any]] = None  # 结构化工程专项算子(TKDN, EOT, 接口传导)与合规核对表结果
    status: CaseWorkflowStatus = "draft"
    created_at: str = ""
    updated_at: str = ""
    current_node: Optional[str] = None
    retry: Dict[str, int] = Field(default_factory=dict)          # qid -> retry_count


class CaseSummary(BaseModel):
    case_id: str
    title: str
    contract_type: str
    contract_date: Optional[str] = None
    created_at: str
    updated_at: str
    status: CaseWorkflowStatus
    mode: RunMode
    snapshot_id: str
    issues_count: int
    lifecycle_stage: Optional[LifecycleStage] = LifecycleStage.EXECUTION_DISPUTE
    project_archetypes: List[ProjectArchetype] = Field(default_factory=list)
    jurisdiction: Optional[str] = None
    parent_case_id: Optional[str] = None
