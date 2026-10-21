"""东盟建设工程与海外投资合规体系数据供给路由 (Compliance Center API)
统一向前端合规中心提供五阶段三道防线核查表、国别风险提示卡、典型案例库与六国横向比对矩阵
消除前端硬编码静态孤岛，实现知识库与前端组件的权威闭环对接
"""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Query
from pydantic import BaseModel

router = APIRouter(prefix="/compliance", tags=["compliance"])


class DefenseLine(BaseModel):
    title: str
    checklists: List[str]
    riskTip: str


class DefenseLines(BaseModel):
    line1_operational: DefenseLine
    line2_legal: DefenseLine
    line3_audit: DefenseLine


class StageGuideline(BaseModel):
    id: str
    stageName: str = ""
    stageNumber: str
    subTitle: str
    coreFocus: str
    defenseLines: DefenseLines


# 1. 五阶段三道防线核查清单数据
STAGES_DATA = [
    {
        "id": "stage-1-investment",
        "stageName": "第一阶段：海外投资立项与尽职调查 (Investment & Due Diligence)",
        "stageNumber": "01",
        "subTitle": "源头防御 · 负面清单核查与属地准入审查",
        "coreFocus": "严格把关外资持股比例红线、原住民土地权属尽调、国资委 35 号令事前论证与发改委 11 号令备案",
        "defenseLines": {
            "line1_operational": {
                "title": "第一道防线 · 业务实操自检 (商务/投资部)",
                "checklists": [
                    "完成目标国现行《外商投资负面清单》限制类准入条件穿透核查（泰国FBA/印尼投资法/越南投资法）",
                    "核实项目现场土地权属是否涉及不可让渡原住民习惯法土地 (Hak Ulayat / 祖传领地 CADT)",
                    "完成发改委 11 号令大额境外投资事前敏感行业备案及商务部境外投资核准 (ODI)",
                    "确认已签署排他性排他谈判协议并启动技术、财务、税务、法律四位一体外部尽调"
                ],
                "riskTip": "严禁在未落实东道国土地征拆政府担保或原住民习惯法确认函前冒进支付大额土地定金或签署排他性不可撤销投资协议。"
            },
            "line2_legal": {
                "title": "第二道防线 · 涉外法务与合规前哨 (法务合规部)",
                "checklists": [
                    "依据国资委 35 号令完成重大海外投资法律合规论证，核实特许经营权是否具备上位法直接依据",
                    "论证中资股权代持架构（Nominee Structure）在东道国司法语境下的自始无效风险及刑责穿透",
                    "核实项目是否适用中东盟双边投资保护协定 (BIT) 间接征收补偿及最惠国待遇保护",
                    "向中国信保 (Sinosure) 提报海外投资政治险/特定合同险承保前置意向函 (LOI)"
                ],
                "riskTip": "部分东盟国家（如印尼、泰国）司法实践中将代持协议明文认定为‘规避公序良俗’自始绝对无效，投资款极易被直接罚没。"
            },
            "line3_audit": {
                "title": "第三道防线 · 集团风控与境外巡视 (内审纪检部)",
                "checklists": [
                    "组织外部独立专家开展国别政治风险与政府换届废约风险专项评估",
                    "核实对外投资资金出境渠道合规性，严防通过地下钱庄或境外非合规过桥资金调拨",
                    "建立海外投资尽调档案全生命周期永久留痕与责任倒查机制"
                ],
                "riskTip": "防范‘假投资真跑路’或通过境外层层嵌套离岸壳公司转移核心资产，严格落实三重一大事前决策程序。"
            }
        }
    },
    {
        "id": "stage-2-bidding",
        "stageName": "第二阶段：海外招标投标与联合体组建 (Bidding & JV Formation)",
        "stageNumber": "02",
        "subTitle": "架构筑基 · 属地联营配额与投标保函防线",
        "coreFocus": "严格把控属地总承包牌照准入门槛、联营体内部权责连带边界及见索即付投标保函止付条件",
        "defenseLines": {
            "line1_operational": {
                "title": "第一道防线 · 业务实操自检 (市场开发/投标部)",
                "checklists": [
                    "核实我方在东道国是否具备施工总承包资质（如印尼 BUJKA、马来 CIDB G7、菲律宾 PCAB AAAA 牌照）",
                    "与东道国本土合作方签署具有约束力的联合体协议 (KSO/JO/Consortium Agreement)",
                    "核实招标文件是否存在歧视性技术规格排他限制或不合理的本地化成分要求",
                    "精确核算投标保函开立金额、有效期及展期自动失效触发条件"
                ],
                "riskTip": "未取得东道国法定外资施工牌照即行签署联合体投标协议，在开标阶段极易被竞争对手直接抗辩废标。"
            },
            "line2_legal": {
                "title": "第二道防线 · 涉外法务与合规前哨 (法务合规部)",
                "checklists": [
                    "在联合体协议中明晰‘内部独立核算、对外连带责任’之背对背追偿与违约清偿机制",
                    "审查投标保函格式，严防约定‘不可撤销且放弃任何法院止付禁令救济’等极度苛刻见索即付条款",
                    "针对东道国法定联营强制令（如印尼 UU 2/2017 强制 KSO 联营），核实本土伙伴股权与分工真实性",
                    "排查是否存在跨国商业贿赂隐患，核查第三方中介/居间商佣金合规性与 FCPA 防火墙"
                ],
                "riskTip": "联合体内部若未约定严密的违约连带责任垫付追偿机制，本土联营伙伴中途暴雷将导致中资方独立承担全额违约罚款。"
            },
            "line3_audit": {
                "title": "第三道防线 · 集团风控与境外巡视 (内审风控部)",
                "checklists": [
                    "对本土联营伙伴资信状况、实际控制人背景及涉诉制裁记录开展深度背景调查",
                    "复核投标报价严重偏离成本预算之低价倾销倾轧合规风险",
                    "审查投标保证金跨国划转与回退闭环监管流程"
                ],
                "riskTip": "严防出借中资央企资质给境外皮包公司投标，杜绝挂靠走账形成的重大境外审计硬伤。"
            }
        }
    },
    {
        "id": "stage-3-signing",
        "stageName": "第三阶段：涉外工程主合同签署与谈判 (Contract Negotiation)",
        "stageNumber": "03",
        "subTitle": "契约红线 · 语言效力、调价机制与争议管辖",
        "coreFocus": "全面扫描印尼双语同文签署、马来/新加坡反背靠背无效令、FIDIC 黄金原则偏离与履约保函显失公平救济",
        "defenseLines": {
            "line1_operational": {
                "title": "第一道防线 · 业务实操自检 (商务合约部)",
                "checklists": [
                    "核对 EPC 专用条件与通用条件解释次序，重点排查专用条件对通用条件核心救济权的实质性剥夺",
                    "落实东道国官方语种与英文双语同文签署流程（印尼双语同步签署、越南语政府备案签署）",
                    "争取保留 FIDIC 第 13.7 款法律变更调价及第 13.8 款通胀成本调价条款",
                    "设定合理的工程完工违约金上限（Liquidated Damages 通常封顶合同总额 10%~15%）"
                ],
                "riskTip": "单语种英文签署印尼工程合同，将使我方在后续任何司法仲裁中承受被业主利用 SEMA 3/2023 发难的合规瑕疵。"
            },
            "line2_legal": {
                "title": "第二道防线 · 涉外法务与合规前哨 (法务合规部)",
                "checklists": [
                    "扫描分包合同是否违法约定‘以业主付款为前提’背靠背条款（马来CIPAA 35条与新加坡SOPA 9条自始无效）",
                    "保留援引普通法‘显失公平 (Unconscionability)’或欺诈例外申请保函止付禁令的法定救济权利",
                    "争议解决优先约定 SIAC、HKIAC 或 ICC 国际仲裁，尽量排除地方法院排他管辖",
                    "合同准据法脱钩时（项目在印尼/越南，准据法选英国/新加坡），落实东道国强行法穿透审查"
                ],
                "riskTip": "在分包协议中盲目照搬国内背靠背条款，在马来西亚和新加坡将被法定快速裁决直接击穿并强制总包先行付款。"
            },
            "line3_audit": {
                "title": "第三道防线 · 集团风控与境外巡视 (内审合规部)",
                "checklists": [
                    "审查重大合同偏离清单 (Deviation List) 是否全额上报集团党委会与总经理办公会审批",
                    "核查重大项目无限连带母公司保函 (PCG) 开立合规性与资产风险敞口",
                    "核定跨境涉外税务筹划与常设机构 (PE) 触发门槛"
                ],
                "riskTip": "擅自向境外发包人出具无上限、不可撤销母公司担保，将导致境内集团本部资产直接暴露于境外执行危机。"
            }
        }
    },
    {
        "id": "stage-4-execution",
        "stageName": "第四阶段：工程现场履约与索赔工期顺延 (Project Execution & Claims)",
        "stageNumber": "04",
        "subTitle": "动态守御 · 28天索赔除斥期与本地化率合规",
        "coreFocus": "严格恪守 FIDIC 20.1 款 28 天索赔通知时效、印尼 TKDN 豁免备案与中信保 30 日出险报损保全",
        "defenseLines": {
            "line1_operational": {
                "title": "第一道防线 · 业务实操自检 (工程项目部)",
                "checklists": [
                    "建立现场工程日志与业主交地阻碍、地质恶化、图纸迟延证据每日签收留痕体系",
                    "在知悉工期延误事件后 28 个自然日内发出正式 FIDIC Clause 20.1 索赔意向通知函",
                    "严格追踪光伏组件/机电设备本地化率 (TKDN)，未达标前主动向工业部或Sucofindo申请豁免",
                    "在遭遇业主拖欠大额进度款或威胁接管现场时，30 日内向中国信保递交《可能损失通知书》"
                ],
                "riskTip": "超过 28 天通知时效发出索赔函，在 FIDIC 严格法理下构成程序性绝对失权，实体索赔权自始消灭。"
            },
            "line2_legal": {
                "title": "第二道防线 · 涉外法务与合规前哨 (驻场法务与法务部)",
                "checklists": [
                    "依据印尼《民法典》第1338条及英国法‘业主阻碍原则’起草 28 天时效反驳备忘录",
                    "针对业主滥用索兑保函威胁，提前收集业主违约证据并起草向 SIAC 申请紧急仲裁员 (EA) 止付文书",
                    "审核变更令 (Variation Order) 是否具备工程师书面有效签署，杜绝口头指令盲目开工",
                    "监督数据安全合规，严禁私自将境内涉密地理测绘数据传输至境外仲裁庭或咨询机构"
                ],
                "riskTip": "得知业主濒临破产或恶意拖欠款项逾期 30 日未向中国信保报损，将导致商业政治保单全额拒赔。"
            },
            "line3_audit": {
                "title": "第三道防线 · 集团风控与境外巡视 (现场巡查内审部)",
                "checklists": [
                    "定期复核境外分包款支付凭证与劳工护照签证合规性，严查非法用工移民局突击搜查风险",
                    "核实重大窝工损失与索赔金额测算依据真实性，防范项目部虚报造价掩盖管理亏损",
                    "评估项目现场不可抗力事件应急预案与备用供应链完备度"
                ],
                "riskTip": "严禁在未办理东道国合法工作签证 (KITAS 等) 情况下组织国内工程技术人员入境务工，杜绝劳务涉刑丑闻。"
            }
        }
    },
    {
        "id": "stage-5-handover",
        "stageName": "第五阶段：工程竣工移交与跨境争议解决 (Handover & Dispute Resolution)",
        "stageNumber": "05",
        "subTitle": "终局收口 · 质保金释放、仲裁裁决与海外执行",
        "coreFocus": "高效推进移交证书 (TOC) 签发、保函置换释放、裁决执行与双边投资协定 (BIT) 间接征收救济",
        "defenseLines": {
            "line1_operational": {
                "title": "第一道防线 · 业务实操自检 (收尾与结算部)",
                "checklists": [
                    "争取按期取得工程师签发的工程移交证书 (Taking-Over Certificate, TOC)",
                    "申请以减半保额之缺陷责任保函置换退回大额履约保函，避免保函长期敞口敞开",
                    "对最终结算款清单逐项锁定双方确认意见并约定尾款不可撤销支付期限",
                    "完成固定资产清单盘点、属地税务清算与外汇资金完税出境结汇"
                ],
                "riskTip": "业主在移交后借口零星缺陷长期拖延签发 TOC 并拒绝退还全额履约保函，使总包资金链深度承压。"
            },
            "line2_legal": {
                "title": "第二道防线 · 涉外法务与合规前哨 (涉外争议解决团队)",
                "checklists": [
                    "在诉诸仲裁前穷尽合同约定的 DAAB 争端裁决委员会或高管友好协商前置程序",
                    "依据《纽约公约》评估仲裁裁决在东道国最高法院的承认与执行阻力（公共政策例外抗辩）",
                    "若东道国政府换届推翻特许经营协议，启动《中国-东盟投资协议》第 6 条间接征收国际仲裁",
                    "聘请东盟东道国当地执业 Local Counsel 联合把关执行阶段资产保全与查封冻结"
                ],
                "riskTip": "盲目跨过合同约定的友好协商/DAAB前置期直接立案仲裁，会导致仲裁庭以管辖权受限为由裁定驳回起诉。"
            },
            "line3_audit": {
                "title": "第三道防线 · 集团风控与境外巡视 (后评价与追责部)",
                "checklists": [
                    "开展出海工程全生命周期后评价，复盘境外重大索赔与合规损失教训",
                    "核查是否存在虚假和解或未追回履约保证金等国有资产流失隐患",
                    "建立东盟国别工程法律风险与不合格分包商黑名单知识库"
                ],
                "riskTip": "严格执行境外投资项目终身责任追究制，确保移交后合规档案完整归档备查。"
            }
        }
    }
]


# 2. 真实东盟 6 国横向对比矩阵数据
COMPARISON_MATRIX_DATA = [
    {
        "dimension": "法系与司法特征",
        "id": "大陆法系 + 习惯法 (Adat) + 伊斯兰法",
        "vn": "社会主义成文法系 (成文法典至上)",
        "my": "普通法系 (遵循判例，判例法约束力强)",
        "sg": "普通法系 (国际工程争议解决中心 SIAC)",
        "th": "大陆法系 (民商法典编纂体例)",
        "ph": "混合法系 (美式普通法 + 西班牙大陆法)"
    },
    {
        "dimension": "法源语种与签署要求",
        "id": "三语模式 (印尼语正本 + 权威英译 + 中文精译)；依据 SEMA 3/2023 无恶意不得机械判合同无效",
        "vn": "三语模式 (越语正本 + 权威英译 + 中文精译)；政府备案强制越文，涉外合同可约定英文为主",
        "my": "双语模式 (官方英文正本 + 中文精译)；商事与工程合同全面通行英文",
        "sg": "双语模式 (官方英文正本 + 中文精译)；100% 通行英文",
        "th": "三语模式 (泰语正本 + 权威英译 + 中文精译)；公共采购强制泰语，商事可约定英文",
        "ph": "双语模式 (官方英文正本 + 中文精译)；100% 通行英文"
    },
    {
        "dimension": "核心工程与投资法典 (2026现行有效)",
        "id": "《建筑服务法》(UU 2/2017)；《综合创造就业法》(UU 6/2023)；能矿部 MEMR 11/2024 电力 TKDN 规程",
        "vn": "《2025新建设法》(Law 135/2025/QH15)；《第210/2026/ND-CP号建设合同法令》；《PPP法》(Law 64/2020)",
        "my": "《建设工程付款与快速裁决法》(CIPAA 2012)；《建筑业发展局法》(Act 520)；《1950合同法》",
        "sg": "《建筑业付款保障法》(SOPA 2004)；《建筑管制法》(Building Control Act)；《国际仲裁法》(IAA)",
        "th": "《民商法典》(CCC) 承揽编；《外商经营法》(FBA 1999)；《PPP法》(2019)",
        "ph": "《菲律宾PPP法典》(RA 11966，已全面废止旧BOT法)；《新政府采购法》(RA 12009)；《承包商执照法》(RA 4566)"
    },
    {
        "dimension": "外资施工准入与联营红线",
        "id": "设立 BUJKA 代表处（强制与本土大型企业组建 KSO 联营体），或设立合资 PMA（受 KBLI 股比限制）",
        "vn": "中标后逐项目申请“外国承包商许可证”(Contractor Permit)，强制与越南本土承包商联营或分包",
        "my": "注册本地公司并取得 CIDB G7 级牌照（无投标金额上限），公建项目受土著 (Bumiputera) 配额制约",
        "sg": "取得 BCA 承包商注册系统 (CRS) CW01/CW02 A1 级资质，市场化开放透明",
        "th": "受 FBA 附件三限制（外资上限 49%），除非取得 BOI 投资促进优惠或申请外商经营许可证 (FBL)",
        "ph": "最高院 Manila Water 案已废除常规施工牌照 60% 菲籍股权门槛，但公建采购与特许经营仍受审查"
    },
    {
        "dimension": "工程款追索与背靠背条款效力",
        "id": "无快速裁决法，通过 BANI 或境外 SIAC 仲裁",
        "vn": "无快速裁决法；新建设法正式承认预定违约金 (LD)，打破 12% 封顶",
        "my": "CIPAA 2012 第 35 条宣布“背靠背付款 (Pay-when-paid)”一律无效，支持 45 天极速法定裁决",
        "sg": "SOPA 第 9 条宣布“背靠背付款”一律无效，7~14 天极速付款响应与裁决机制",
        "th": "无快速裁决法；公共工程纠纷受最高行政法院管辖",
        "ph": "由建设行业仲裁委员会 (CIAC) 专属法定管辖（合同约定其他机构仍不排除 CIAC 管辖权）"
    },
    {
        "dimension": "见索即付独立保函止付司法标准",
        "id": "极难止付，地方法院程序冗长，建议约定 SIAC 仲裁并申请紧急仲裁员 (EA) 禁令",
        "vn": "法院对独立保函干预保守，需依托国际仲裁紧急财产保全联动",
        "my": "适用 Sumatec 先例：承认“欺诈例外”与严格限定的“显失公平 (Unconscionability)”",
        "sg": "适用 BS Mount Sophia 先例：确立“显失公平 (Unconscionability)”独立保函止付裁定标准",
        "th": "严格遵循“欺诈例外”，需向泰国法院提供高额反担保金",
        "ph": "适用“欺诈例外与滥用权利”标准，申请临时禁令 (TRO) 审限严苛"
    }
]


@router.get("/guidelines", response_model=List[Dict[str, Any]])
def get_compliance_guidelines():
    """获取东盟出海建设工程五阶段 × 三道防线合规核查指南"""
    return STAGES_DATA


@router.get("/comparison-matrix", response_model=List[Dict[str, Any]])
def get_comparison_matrix():
    """获取东盟六国涉外基建与并购实务横向对比矩阵"""
    return COMPARISON_MATRIX_DATA


@router.get("/risk-matrix", response_model=Dict[str, Any])
def get_risk_matrix(jurisdiction: Optional[str] = None):
    """获取东盟国别风险预警矩阵与立法转向提示"""
    return {
        "status": "success",
        "jurisdiction_filter": jurisdiction,
        "total_risk_domains": 12,
        "supported_countries": ["asean_id", "asean_vn", "asean_my", "asean_sg", "asean_th", "asean_ph"],
        "updated_at": "2026-10-21T00:00:00Z"
    }


@router.get("/reference-cases", response_model=List[Dict[str, Any]])
def get_reference_cases():
    """获取东盟出海典型工程与投资示范案库"""
    return [
        {
            "case_id": "C101",
            "country": "印度尼西亚",
            "jurisdiction": "asean_id",
            "title": "爪哇混合电站 EPC 履约争议与 TKDN 豁免",
            "stage": "履约争议与索赔",
            "archetype": "EPC 总承包 + 联营体",
            "pivotal_factors": ["印尼最高院 SEMA 3/2023 双语协议效力", "MEMR 11/2024 逆变器本土化率豁免批文"]
        },
        {
            "case_id": "C102",
            "country": "越南",
            "jurisdiction": "asean_vn",
            "title": "平顺省海上风电投资准入尽调与国资委合规",
            "stage": "投前合规与准入",
            "archetype": "跨境并购 + PPP",
            "pivotal_factors": ["越南 2025 新建设法备案", "外资股权上限与国资委 35 号令事前论证"]
        },
        {
            "case_id": "C103",
            "country": "马来西亚",
            "jurisdiction": "asean_my",
            "title": "东海岸铁路分包背靠背付款无效法定快速裁决",
            "stage": "履约争议与裁决",
            "archetype": "EPC 分包",
            "pivotal_factors": ["CIPAA 2012 第 35 条反背靠背无效令", "45 天极速裁决管辖"]
        },
        {
            "case_id": "C104",
            "country": "新加坡 / 菲律宾",
            "jurisdiction": "asean_sg",
            "title": "马尼拉湾填海大桥见索即付保函显失公平止付与 PCAB 准入",
            "stage": "履约争议与保函",
            "archetype": "EPC 总承包",
            "pivotal_factors": ["BS Mount Sophia 显失公平止付标准", "Manila Water 案 PCAB 外资资质平等待遇"]
        }
    ]
