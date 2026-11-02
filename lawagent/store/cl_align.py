"""CL-Align 跨法系多语种法学概念对齐算子 (Cross-Lingual & Cross-Legal-System Concept Alignment)
核心定位与法理架构：
- 东盟区域内普通法系（新/马/缅/文）、大陆法系（越/柬/老/东帝汶/泰）与混合法系（印尼/菲）深度交织。
- 解决中文法律概念（如“违约金酌减”、“背靠背条款”、“情势变更”、“见索即付保函止付”）在不同东盟法域下的法定概念撕裂与语义鸿沟。
- 基于内置的 11 国多语种法学词典 (glossary.csv) 与跨法系教义规则库，将检索输入实时映射为具备属地实体法效力的法学概念张量与扩展词。
"""

import os
import re
import csv
import logging
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set, Any
from pathlib import Path

logger = logging.getLogger(__name__)

# 法系归类划分
COMMON_LAW_JURISDICTIONS = {"asean_sg", "asean_my", "asean_bn", "asean_mm"}
CIVIL_LAW_JURISDICTIONS = {"asean_vn", "asean_kh", "asean_la", "asean_tl", "asean_th"}
MIXED_JURISDICTIONS = {"asean_id", "asean_ph"}


@dataclass
class AlignedConcept:
    term_cn: str
    term_en: str
    term_local: str
    jurisdiction: str
    legal_definition: str
    legal_system_category: str = "general"
    doctrine_note: str = ""


@dataclass
class CLAlignResult:
    original_query: str
    jurisdiction: Optional[str]
    matched_concepts: List[AlignedConcept] = field(default_factory=list)
    expanded_tokens: List[str] = field(default_factory=list)
    cross_legal_system_doctrines: List[str] = field(default_factory=list)
    reformulated_query: str = ""
    concept_tags: List[Dict[str, str]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "original_query": self.original_query,
            "jurisdiction": self.jurisdiction,
            "matched_concepts_count": len(self.matched_concepts),
            "concept_tags": self.concept_tags,
            "expanded_tokens": self.expanded_tokens,
            "cross_legal_system_doctrines": self.cross_legal_system_doctrines,
            "reformulated_query": self.reformulated_query
        }


# 跨法系深度教义规则库 (针对东盟高频争议概念)
CROSS_LEGAL_SYSTEM_RULES: Dict[str, Dict[str, Any]] = {
    "违约金": {
        "keywords": ["违约金", "违约金酌减", "违约金过高", "罚金", "惩罚性违约金", "工期违约金", "ld", "liquidated damages"],
        "mappings": {
            "common_law": {
                "doctrine_note": "普通法系无大陆法系之'法官自由酌减'机制，适用惩罚性条款无效规则 (Penalty Doctrine)。违约金条款要么被认定为真实损失预估 (Genuine Pre-estimate of Loss) 全额支持，要么因惩罚性 (Penalty Clause) 自始绝对无效。",
                "tokens": ["liquidated damages", "penalty doctrine", "genuine pre-estimate", "Denka Advantech", "Cubic Electronics", "unenforceable penalty", "Cavendish"],
                "statute_refs": ["Denka Advantech [2020] SGCA 119", "Cubic Electronics [2019] 6 MLJ 15", "Contracts Act Sec 74 75"]
            },
            "asean_vn": {
                "doctrine_note": "越南大陆法系下商事合同违约金受《商事法》第301条8%上限强行法刚性限制；建设工程合同依据《建设法》第146条/新建设法第86.2条，使用国家资本工程违约金上限为12%，民间投资项目允许约定违约金与实际合理损害赔偿（Bồi thường thiệt hại）并用，超出法定上限部分无效。",
                "tokens": ["mức phạt vi phạm", "penalty cap 8%", "Điều 301 Luật Thương mại", "Luật Xây dựng Điều 146", "Luật Xây dựng 2025 Điều 86.2", "bồi thường thiệt hại", "phạt hợp đồng"],
                "statute_refs": ["VN:Commercial_Law_2005:Art301", "VN:Decree_37_2015:Art14", "VN:Construction_Law_2014:Art146"]
            },
            "asean_kh": {
                "doctrine_note": "柬埔寨民法典第403条明文确立违约金不可增减原则：当事人事先约定违约金的，法院原则上无权增加或减少违约金金额（沿袭日本民法传统）。",
                "tokens": ["Article 403 Civil Code", "damages stipulated in advance", "inalterability of penalty", "សំណងជំងឺចិត្ត"],
                "statute_refs": ["KH:Civil_Code_2007:Art403"]
            },
            "asean_ph": {
                "doctrine_note": "菲律宾民法典第1229条明文赋予法官衡平酌减权：当主债务已被部分或不规则履行，或违约金数额明显不公、过高 (iniquitous or unconscionable) 时，法院得依法衡平酌减。",
                "tokens": ["Article 1229 Civil Code", "equitable reduction of penalty", "iniquitous or unconscionable", "liquidated damages"],
                "statute_refs": ["PH:Civil_Code_RA386:Art1229"]
            },
            "asean_th": {
                "doctrine_note": "泰国民商法典第383条规定，当约定的违约金数额不成比例地过高时，法院有权依职权将其酌减至合理数额。",
                "tokens": ["Section 383 CCC", "disproportionately high penalty", "reduce to reasonable amount", "Kha-phat"],
                "statute_refs": ["TH:CCC:Sec383"]
            },
            "asean_tl": {
                "doctrine_note": "东帝汶民法典第746条规定违约金条款 (Cláusula Penal)，明确赋予法院在违约金显失公平时依衡平原则酌减的司法权力。",
                "tokens": ["Artigo 746 Código Civil", "cláusula penal", "redução equitativa", "indemnização fixada"],
                "statute_refs": ["TL:Civil_Code_2011:Art746"]
            },
            "asean_id": {
                "doctrine_note": "印尼民法典第1249条确认当事人约定违约金后不得请求额外赔偿，结合第1338条与最高法院第3/2023号通告 (SEMA 3/2023) 客观善意原则审视违约赔偿合理性。",
                "tokens": ["Pasal 1249 KUHPerdata", "ganti rugi denda keterlambatan", "itikad baik", "SEMA 3 2023"],
                "statute_refs": ["ID:KUHPerdata:Art1249", "ID:KUHPerdata:Art1338"]
            }
        }
    },
    "背靠背": {
        "keywords": ["背靠背", "背靠背条款", "条件支付", "pay when paid", "pay if paid"],
        "mappings": {
            "common_law": {
                "doctrine_note": "新加坡与马来西亚成文法明文确立背靠背付款条款自始绝对无效！新加坡 SOPA 第9条与马来西亚 CIPAA 第35条明令禁止任何附条件付款条款 (Conditional Payment is Void)。",
                "tokens": ["pay when paid void", "conditional payment void", "Section 35 CIPAA", "Section 9 SOPA", "statutory adjudication"],
                "statute_refs": ["MY:Act_736_CIPAA:Sec35", "SG:SOPA_Cap30B:Sec9"]
            },
            "general": {
                "doctrine_note": "大陆法系与混合法系下无类似 CIPAA 的强制无效法条，属于合同自由约定范畴，但可依据同时履行抗辩权、先履行抗辩权或善意履行原则进行限制解释。",
                "tokens": ["conditional payment", "back to back clause", "klausul pembayaran berturut", "syarat pembayaran"],
                "statute_refs": ["ID:KUHPerdata:Art1338"]
            }
        }
    },
    "情势变更": {
        "keywords": ["情势变更", "情势变迁", "不可抗力", "合同受阻", "hardship", "frustration", "force majeure"],
        "mappings": {
            "common_law": {
                "doctrine_note": "普通法系无大陆法系之法定情势变更制度！当事人不得以履行艰难或物价上涨主张变更，必须严格证明达到合同目的落空/受阻 (Doctrine of Frustration) 或触发合同明文 Force Majeure 条款。",
                "tokens": ["doctrine of frustration", "force majeure", "radical change in obligation", "Contract Act Section 56"],
                "statute_refs": ["MY:Contracts_Act_1950:Sec57", "MM:Contract_Act_1872:Sec56"]
            },
            "asean_vn": {
                "doctrine_note": "越南2015年民法典第420条设立'基础情况重大改变' (Hoàn cảnh thay đổi cơ bản) 制度，规定情势变更时双方须在合理期限内重新协商；协商不成可请求法院终止或调整合同。",
                "tokens": ["Điều 420 BLDS", "hoàn cảnh thay đổi cơ bản", "thay đổi hợp đồng", "hardship renegotiation"],
                "statute_refs": ["VN:Civil_Code_2015:Art420"]
            },
            "asean_id": {
                "doctrine_note": "印尼民法典第1244-1245条规定不可抗力 (Keadaan Kahar)，最高法院 SEMA 3/2023 确立客观善意履行原则，法官有权对因不可抗力导致严重失衡的合同进行司法平衡。",
                "tokens": ["keadaan kahar", "overmacht", "force majeure", "Pasal 1244 KUHPerdata", "SEMA 3 2023"],
                "statute_refs": ["ID:KUHPerdata:Art1244", "ID:KUHPerdata:Art1245"]
            }
        }
    },
    "诉讼时效": {
        "keywords": ["诉讼时效", "消灭时效", "时效中断", "除斥期间", "limitation period", "prescription"],
        "mappings": {
            "asean_th": {
                "doctrine_note": "泰国民商法典第193/34(1)条规定商人/承揽人工程施工款追索适用 2 年超短消灭时效！且第193/14条规定普通催款函不发生中断效力，必须起诉或获书面承认。",
                "tokens": ["Section 193 34 CCC", "two year short prescription", "Section 193 14 interrupt", "Ayu Khwam", "Dika 7221 2552"],
                "statute_refs": ["TH:CCC:Sec193_34", "TH:CCC:Sec193_14"]
            },
            "asean_sg": {
                "doctrine_note": "新加坡《时效法》第6条规定合同与侵权诉讼时效为6年；第24A条针对潜伏性工程结构缺陷 (Latent Defects) 规定自知悉起3年、最长15年绝对封顶。",
                "tokens": ["Limitation Act Section 6", "Section 24A", "latent defects 15 years", "breach of contract 6 years"],
                "statute_refs": ["SG:Limitation_Act:Sec6", "SG:Limitation_Act:Sec24A"]
            },
            "asean_ph": {
                "doctrine_note": "菲律宾民法典第1144条书面合同为10年；第1145条口头/不当得利为6年；关键特别规则：第1155条规定庭外书面催告函 (Extrajudicial Demand) 即可直接中断诉讼时效！",
                "tokens": ["Article 1144 Civil Code", "Article 1145", "Article 1155 extrajudicial demand", "prescription interrupt"],
                "statute_refs": ["PH:Civil_Code_RA386:Art1144", "PH:Civil_Code_RA386:Art1155"]
            },
            "asean_vn": {
                "doctrine_note": "越南民法典第429条规定合同争议起诉时效原则为3年；最高人民法院 Án lệ số 12/2017/AL 指导性判例确立了达成和解或撤诉后重新起诉的时效起算规则。",
                "tokens": ["Điều 429 BLDS", "thời hiệu khởi kiện 3 năm", "Án lệ 12 2017 AL"],
                "statute_refs": ["VN:Civil_Code_2015:Art429", "CASE:VN_SC:An_Le_12_2017:2017"]
            }
        }
    },
    "保函止付": {
        "keywords": ["保函止付", "独立保函", "见索即付保函", "保函欺诈", "injunction", "on demand bond", "unconscionability"],
        "mappings": {
            "common_law": {
                "doctrine_note": "新马普通法不仅承认欺诈例外 (Fraud Exception)，新加坡更开创确立了显失公平独立止付标准 (Unconscionability Exception, BS Mount Sophia 判例)，只要证明受益人索赔恶意或显失公平即可申请禁令。",
                "tokens": ["unconscionability exception", "BS Mount Sophia", "performance bond injunction", "Sumatec", "fraud exception"],
                "statute_refs": ["CASE:SG_CA:BS_Mount_Sophia:2012", "CASE:MY_FC:Sumatec:2012"]
            },
            "general": {
                "doctrine_note": "大陆法系与 URDG 758 国际惯例下原则上仅承认欺诈例外 (Fraud Exception)，需提供明显的欺诈或伪造证据方能申请法院采取临时紧急保全措施。",
                "tokens": ["URDG 758", "fraud exception", "perbuatan curang", "lừa đảo", "interim injunction"],
                "statute_refs": ["STD:URDG_758:Art15", "STD:URDG_758:Art20"]
            }
        }
    },
    "不当得利与变更": {
        "keywords": ["无变更令", "变更索赔", "额外工程", "不当得利", "实际施工", "quantum meruit", "unjust enrichment", "variation"],
        "mappings": {
            "common_law": {
                "doctrine_note": "在无书面变更指令 (VO) 情况下，马来西亚 Contracts Act Sec 71 及新加坡普通法确立 Quantum Meruit（按劳计酬不当得利），以防止雇主受领实际工程成果后不当获利 (Bina Puri 判例)。",
                "tokens": ["Quantum Meruit", "Contracts Act Section 71", "Bina Puri", "unjust enrichment", "variation without order"],
                "statute_refs": ["MY:Contracts_Act_1950:Sec71", "CASE:MY_HC:Bina_Puri_v_Hing_Nyit:2015"]
            },
            "asean_ph": {
                "doctrine_note": "菲律宾民法典第1724条规定总价合同变更无书面定价协议不赔铁律；但最高法院 CE Construction 案确立若业主已实际受领受益，可依民法典第2142条不当得利判决补偿实际成本。",
                "tokens": ["Article 1724 Civil Code", "Article 2142 Solutio Indebiti", "CE Construction Araneta", "Quantum Meruit"],
                "statute_refs": ["PH:Civil_Code_RA386:Art1724", "PH:Civil_Code_RA386:Art2142", "CASE:PH_SC:CE_Construction_v_Araneta:2015"]
            },
            "asean_id": {
                "doctrine_note": "印尼民法典第1610条规定固定总价工程未经定作人书面同意禁止因涨价追加价款，实务中需依托 FIDIC 13.7/13.8 调差约定进行抗辩。",
                "tokens": ["Pasal 1610 KUHPerdata", "pekerjaan tambah kurang", "harga borongan tetap"],
                "statute_refs": ["ID:KUHPerdata:Art1610"]
            }
        }
    },
    "主权豁免": {
        "keywords": ["主权豁免", "政府豁免", "苏丹豁免", "sovereign immunity", "state immunity"],
        "mappings": {
            "asean_bn": {
                "doctrine_note": "文莱宪法第84C条规定文莱苏丹与政府部委享有绝对主权豁免 (Absolute Sovereign Immunity)，国内法院无权受理对政府诉讼！基建合同必须约定离岸仲裁与放弃豁免条款。",
                "tokens": ["Constitution of Brunei Article 84C", "absolute sovereign immunity", "Sultan in Council", "offshore arbitration waiver"],
                "statute_refs": ["BN:Constitution:Art84C"]
            }
        }
    },
    "事前审计签证": {
        "keywords": ["事前审计", "事前核准", "审计法院", "visto", "prior audit", "fiscalizacao"],
        "mappings": {
            "asean_tl": {
                "doctrine_note": "东帝汶国家审计院法第9/2011号确立事前核准签证 (Visto) 铁律：超50万美元公共合同未获审计院签发 Visto 前抢先施工，财政部依法拒绝拨付工程款！",
                "tokens": ["Tribunal de Contas", "Câmara de Contas", "Visto prévio", "Fiscalização Prévia", "Law No 9 2011"],
                "statute_refs": ["TL:Law_9_2011_Audit_Court:Art5", "TL:Budget_Law:Art32", "CASE:TL_CC:Recusa_de_Visto_Grid:2020"]
            }
        }
    },
    "外汇管制与强制结汇": {
        "keywords": ["强制结汇", "外汇管制", "结汇令", "外债审批", "foreign exchange", "currency surrender"],
        "mappings": {
            "asean_mm": {
                "doctrine_note": "缅甸外汇管理法 (FEML 2012) 与央行 2022 年第 12 号通告强制要求外币收入须在 1 个营业日内按官方价结汇为缅币，跨境偿还外债须经 FESC 严苛审批。",
                "tokens": ["CBM Notification 12 2022", "FEML 2012", "mandatory conversion", "Kyat surrender", "FESC approval"],
                "statute_refs": ["MM:FEML_2012:Sec38", "MM:CBM_Notification:No12_2022"]
            },
            "asean_la": {
                "doctrine_note": "老挝2022年外汇管理法第15/NA号规定离岸股东借款与外债必须事先获取老挝央行 (BOL) 核准证明 (Approval Certificate) 方能合法购汇还本付息。",
                "tokens": ["Law No 15 NA", "Bank of Lao PDR", "BOL offshore loan approval", "foreign currency management"],
                "statute_refs": ["LA:Law_15_NA_FX:Art18", "LA:Law_15_NA_FX:Art26"]
            }
        }
    },
    "特许经营续约与政府调整": {
        "keywords": ["特许经营协议", "水电特许权", "ca协议", "单方修改", "政府回购", "concession agreement", "ca renewal", "decree 135 pm"],
        "mappings": {
            "asean_la": {
                "doctrine_note": "老挝第135/PM号特许经营政令第8条与第15条规定，国家在公共利益或环境安全需要时保留单方调整特许权（CA）技术规范与回购电站之主权，投资者有权依据水电商业法与双边投资协定（BIT）申请合理估值赔偿。",
                "tokens": ["Decree 135 PM", "Concession Agreement", "Hydropower Business Law", "early termination compensation", "PPA renegotiation", "Electricity Law Art 35"],
                "statute_refs": ["LA:Decree_135_PM:Art8", "LA:Decree_135_PM:Art15", "LA:Hydropower_Law_2017:Art21"]
            }
        }
    },
    "土地使用权与MIC转让批文": {
        "keywords": ["土地使用权", "mic批文", "长期租赁", "土地转让", "land use rights", "mic permit", "transferability"],
        "mappings": {
            "asean_mm": {
                "doctrine_note": "缅甸投资法（MIL 2016）第50条与投资细则规定，外资企业经缅甸投资委员会（MIC）批准可租赁土地最长50年+10年+10年，但该土地使用权（Land Use Rights）若需转让、抵押或分租，必须重新向 MIC 报批，擅自转让将导致投资许可撤销与土地收回。",
                "tokens": ["Myanmar Investment Law Sec 50", "MIC Permit", "Land Use Rights transfer", "Form 7", "long term land lease", "SEZ Law Sec 30"],
                "statute_refs": ["MM:Investment_Law_2016:Sec50", "MM:Investment_Rules_2017:Rule112", "MM:SEZ_Law_2014:Sec30"]
            }
        }
    },
    "原住民领地与知情同意程序": {
        "keywords": ["祖传领地", "原住民知情同意", "fpic", "cadt", "原住民权利", "indigenous peoples", "ancestral domain"],
        "mappings": {
            "asean_ph": {
                "doctrine_note": "菲律宾《原住民权利法》（IPRA, RA 8371）第59条规定，任何在原住民祖传领地（CADT）范围内开展的基建与能源项目，必须事先取得国家原住民委员会（NCIP）主持的'自由事先知情同意'（FPIC）并获得合规证明书（CP），未获 FPIC 擅自施工的，法院将下达禁制令并强制复原。",
                "tokens": ["RA 8371 IPRA Sec 59", "CADT", "Free and Prior Informed Consent FPIC", "NCIP Certification Precondition", "ancestral domain injunction"],
                "statute_refs": ["PH:RA_8371_IPRA:Sec59", "PH:RA_8371_IPRA:Sec7"]
            }
        }
    },
    "政府采购框架与保函索兑": {
        "keywords": ["bddb", "文莱政府工程", "pwd合同", "政府保函索兑", "文莱基建", "bddb framework", "performance bond call"],
        "mappings": {
            "asean_bn": {
                "doctrine_note": "文莱发展与经济委员会（BDDB）及公共工程局（PWD）标准合同规定，政府工程履约保函具有高度无条件即付性，且依据文莱宪法第84C条政府绝对豁免权，承包商无法向民事法院申请对政府业主的临时禁令，只能在争议裁决或仲裁阶段主张不当索兑之损害赔偿。",
                "tokens": ["BDDB framework", "PWD Standard Form", "Constitution Art 84C", "unconditional bond call", "Crown Proceedings Act"],
                "statute_refs": ["BN:Constitution:Art84C", "BN:PWD_Form_Contract:Clause38"]
            }
        }
    },
    "事前审计签证拒绝救济": {
        "keywords": ["visto拒绝", "签证拒绝", "审计院复议", "救济路径", "recusa de visto", "recurso de visto"],
        "mappings": {
            "asean_tl": {
                "doctrine_note": "东帝汶审计院法（Law 9/2011）第45-48条规定，公共工程合同若遭审计院拒发 Visto 签证，总承包商与项目部可在15日内向审计院全会提起复议（Recurso Ordinário），若全会维持拒绝，可进一步向上诉法院（Court of Appeal）提出司法审查诉讼，诉讼期间暂停工程开工。",
                "tokens": ["Recusa de Visto", "Recurso Ordinário", "Law No 9 2011 Art 45", "Tribunal de Recurso", "Câmara de Contas appeal"],
                "statute_refs": ["TL:Law_9_2011_Audit_Court:Art45", "TL:Law_9_2011_Audit_Court:Art48"]
            }
        }
    },
    "反制裁与长臂管辖": {
        "keywords": ["反制裁", "长臂管辖", "单边制裁", "OFAC", "SDN", "实体清单", "阻断办法", "次级制裁", "反外国制裁法", "sanctions", "secondary sanctions"],
        "mappings": {
            "general": {
                "doctrine_note": "中国《反外国制裁法》第12条严禁任何组织和个人执行或协助外国歧视性限制措施；商务部《阻断外国法律与措施不当域外适用办法》（2021年1号令）第5条要求30日内报告，第7条可发布不得承认阻断令；受害方有权向中国法院提起民事侵权索赔并申请财产保全。",
                "tokens": ["Anti-Foreign Sanctions Law Art 12", "MOFCOM Order 1 2021", "Blocking Statute", "Unreliable Entity List", "反外国制裁法第12条", "商务部阻断办法"],
                "statute_refs": ["CN:Anti_Foreign_Sanctions_Law:Art3_4_12_15", "CN:MOFCOM_Order_1_2021:Blocking_Statute", "CN:State_Council_AFSL_Reg_2025:Art1_22"]
            },
            "common_law": {
                "doctrine_note": "英美普通法在 Lamesa Investments Ltd v Cynergy Bank Ltd [2020] EWCA Civ 821 先例中确立：单边制裁是否构成履行不能取决于合同特殊措辞（如 mandatory provision of law）；普通法 Ralli Bros 规则仅在合同履行地（Lex Loci Solutionis）法使履行为非法时免责，外国单边长臂制裁原则上不构成合法履行不能。",
                "tokens": ["Lamesa Investments v Cynergy Bank", "Ralli Brothers doctrine", "lex loci solutionis illegality", "unilateral extraterritorial sanctions defence", "force majeure sanctions"],
                "statute_refs": ["REF_CASE:UK_CA:Lamesa_v_Cynergy_2020", "REF_CASE:SG_SICC:Sanctions_LC_Payment_2023"]
            }
        }
    },
    "出口管制与供应链断供": {
        "keywords": ["出口管制", "物项管制", "供应链断供", "断供", "两用物项", "商务部管制", "export control", "dual use items"],
        "mappings": {
            "general": {
                "doctrine_note": "中国《出口管制法》第12条与第44条对管制物项、两用物项及军民两用技术出境实施严格最终用户与最终用途许可制度，违反构成行政及刑事违法；与东道国技术引进或转售要求产生冲突时，必须履行中国商务部许可前置程序。",
                "tokens": ["Export Control Law Art 12", "end user end use certification", "two way export control compliance", "出口管制法", "最终用户证明"],
                "statute_refs": ["CN:Export_Control_Law_2020:Art12_44"]
            }
        }
    }
}


class CLAlignOperator:
    """跨法系多语种法学概念对齐算子"""
    _instance: Optional["CLAlignOperator"] = None

    def __init__(self, glossary_path: Optional[str] = None):
        self.glossary_terms: List[AlignedConcept] = []
        self._load_glossary(glossary_path)

    @classmethod
    def get_instance(cls, glossary_path: Optional[str] = None) -> "CLAlignOperator":
        if cls._instance is None:
            cls._instance = cls(glossary_path)
        return cls._instance

    def _load_glossary(self, custom_path: Optional[str] = None):
        """加载 11 国术语表"""
        possible_paths = [
            custom_path,
            os.path.join(os.getcwd(), "kb", "asean", "glossary.csv"),
            os.path.join(os.getcwd(), "data", "kb", "asean", "glossary.csv"),
            str(Path(__file__).resolve().parent.parent.parent / "kb" / "asean" / "glossary.csv")
        ]
        chosen_path = next((p for p in possible_paths if p and os.path.exists(p)), None)
        if not chosen_path:
            logger.warning("CLAlignOperator: glossary.csv 未找到，使用内置教义词典")
            return

        try:
            with open(chosen_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    jur = row.get("Jurisdiction", "asean_all").strip()
                    sys_cat = "mixed"
                    if jur in COMMON_LAW_JURISDICTIONS:
                        sys_cat = "common_law"
                    elif jur in CIVIL_LAW_JURISDICTIONS:
                        sys_cat = "civil_law"

                    concept = AlignedConcept(
                        term_cn=row.get("Term_CN", "").strip(),
                        term_en=row.get("Term_EN", "").strip(),
                        term_local=row.get("Term_Local", "").strip(),
                        jurisdiction=jur,
                        legal_definition=row.get("Legal_Definition", "").strip(),
                        legal_system_category=sys_cat
                    )
                    self.glossary_terms.append(concept)
            logger.info(f"CLAlignOperator: 成功装载 {len(self.glossary_terms)} 组多语种跨法系术语")
        except Exception as e:
            logger.error(f"CLAlignOperator: 加载 glossary.csv 异常: {e}")

    def align(self, query: str, jurisdiction: Optional[str] = None) -> CLAlignResult:
        """执行概念对齐与多语种扩词"""
        if not query:
            return CLAlignResult(original_query="", jurisdiction=jurisdiction)

        q_lower = query.lower().strip()
        matched_concepts: List[AlignedConcept] = []
        expanded_tokens: List[str] = []
        cross_doctrines: List[str] = []
        concept_tags: List[Dict[str, str]] = []
        seen_tokens: Set[str] = set()

        # 1. 匹配 glossary.csv 词条
        for concept in self.glossary_terms:
            cn_match = concept.term_cn and concept.term_cn in query
            en_match = concept.term_en and concept.term_en.lower() in q_lower
            local_match = concept.term_local and concept.term_local.lower() in q_lower

            # 若限定了法域，优先匹配同法域或全局通用术语
            jur_match = (
                not jurisdiction
                or concept.jurisdiction in ("asean_all", "treaty", "asean_fidic")
                or concept.jurisdiction == jurisdiction
            )

            if (cn_match or en_match or local_match) and jur_match:
                matched_concepts.append(concept)
                tag_label = f"{concept.term_cn} ({concept.term_en})"
                if concept.term_local and concept.term_local != concept.term_en:
                    tag_label += f" / {concept.term_local}"
                concept_tags.append({
                    "term_cn": concept.term_cn,
                    "term_en": concept.term_en,
                    "term_local": concept.term_local,
                    "jurisdiction": concept.jurisdiction,
                    "label": tag_label
                })

                # 收集英文与属地语 token
                for t in [concept.term_en, concept.term_local]:
                    if t and t.lower() not in seen_tokens:
                        clean_t = re.sub(r"[()\/]", " ", t).strip()
                        if clean_t:
                            expanded_tokens.append(clean_t)
                            seen_tokens.add(t.lower())

        # 2. 匹配跨法系深度教义规则 (CROSS_LEGAL_SYSTEM_RULES)
        target_jur = jurisdiction or "asean_all"
        is_common_law = target_jur in COMMON_LAW_JURISDICTIONS
        is_civil_law = target_jur in CIVIL_LAW_JURISDICTIONS

        for rule_key, rule_data in CROSS_LEGAL_SYSTEM_RULES.items():
            keywords = rule_data.get("keywords", [])
            if any(kw in q_lower for kw in keywords):
                mappings = rule_data.get("mappings", {})
                
                # 确定适用的法系教义分支
                branch = None
                if target_jur in mappings:
                    branch = mappings[target_jur]
                elif is_common_law and "common_law" in mappings:
                    branch = mappings["common_law"]
                elif is_civil_law and "civil_law" in mappings:
                    branch = mappings["civil_law"]
                elif "general" in mappings:
                    branch = mappings["general"]

                if branch:
                    doc_note = branch.get("doctrine_note", "")
                    if doc_note and doc_note not in cross_doctrines:
                        cross_doctrines.append(doc_note)
                    for tok in branch.get("tokens", []):
                        if tok.lower() not in seen_tokens:
                            expanded_tokens.append(tok)
                            seen_tokens.add(tok.lower())
                    for s_ref in branch.get("statute_refs", []):
                        if s_ref.lower() not in seen_tokens:
                            expanded_tokens.append(s_ref)
                            seen_tokens.add(s_ref.lower())

        # 3. 构造重构查询词 (Reformulated Query)
        tokens_for_query = expanded_tokens[:6]
        tokens_str = " ".join(tokens_for_query)
        reformulated = f"{query} {tokens_str}".strip() if tokens_str else query

        return CLAlignResult(
            original_query=query,
            jurisdiction=jurisdiction,
            matched_concepts=matched_concepts,
            expanded_tokens=expanded_tokens,
            cross_legal_system_doctrines=cross_doctrines,
            reformulated_query=reformulated,
            concept_tags=concept_tags
        )
