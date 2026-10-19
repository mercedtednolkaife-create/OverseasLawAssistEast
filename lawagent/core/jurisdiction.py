"""多法域与多语言可扩展性核心抽象 (Multi-Jurisdiction & Language Architecture)
遵循技术方案与可扩展架构设计，支持按法域（Jurisdiction）插拔：
- 法源目录与代码体系 (Norms / Codes)
- 引用抽取器与规范化解析器 (CitationExtractor, NormNormalizer)
- 语言形态学与复合词拆分器 (LanguageSplitter)
- 时点有效性规则 (TimepointRule)
"""

from typing import Protocol, runtime_checkable, Dict, Any, List, Optional
from dataclasses import dataclass, field


@dataclass
class JurisdictionMetadata:
    """法域元数据定义"""
    code: str                         # 如 'asean_id', 'asean_vn', 'asean_my'
    name_zh: str                      # 如 '印度尼西亚工程与投资法'
    primary_language: str             # 如 'id', 'vi', 'en', 'th'
    citation_standard: str            # 如 'indonesia_statute', 'vietnam_law'
    default_laws: List[str] = field(default_factory=list)
    is_active: bool = True            # 是否激活推荐
    flag: str = ""                    # 国旗/区域标识 emoji
    region: str = "asean"             # 'asean' | 'other'
    language_mode: str = "trilingual" # 'bilingual' (新/马/菲) | 'trilingual' (印/越/泰)
    description_zh: str = ""          # 简要实务说明


@runtime_checkable
class CitationExtractor(Protocol):
    """候选引用抽取器协议：从文本中提取未规范化的法条或案号候选片段"""
    def candidates(self, text: str) -> List[Dict[str, Any]]:
        """返回格式：[{'kind': 'norm' | 'case', 'raw': str, 'span': (start, end)}]"""
        ...


@runtime_checkable
class NormNormalizer(Protocol):
    """法条规范化解析器协议：将原始引用字符串转为标准数据库检索 ID"""
    def normalize(self, raw: str) -> List[Dict[str, Any]]:
        """返回格式：[{'id': 'ID:UU_2_2017:Art57', 'depth': 'clause'|'section', 'clause': '57', 'open_ended': bool}]"""
        ...


@runtime_checkable
class LanguageSplitter(Protocol):
    """特定语言分词/形态学拆分协议（例如德语复合词拆分）"""
    def split(self, word: str) -> List[str]:
        """将复合词拆分为基本词根列表"""
        ...


class IdentitySplitter:
    """默认/直通拆分器"""
    def split(self, word: str) -> List[str]:
        return [word.lower()]


class JurisdictionRegistry:
    """全局多法域服务注册中心"""
    _jurisdictions: Dict[str, JurisdictionMetadata] = {}
    _citation_extractors: Dict[str, CitationExtractor] = {}
    _normalizers: Dict[str, NormNormalizer] = {}
    _splitters: Dict[str, LanguageSplitter] = {}

    @classmethod
    def register(
        cls,
        meta: JurisdictionMetadata,
        citation_extractor: Optional[CitationExtractor] = None,
        normalizer: Optional[NormNormalizer] = None,
        splitter: Optional[LanguageSplitter] = None,
    ):
        cls._jurisdictions[meta.code] = meta
        if citation_extractor:
            cls._citation_extractors[meta.code] = citation_extractor
        if normalizer:
            cls._normalizers[meta.code] = normalizer
        if splitter:
            cls._splitters[meta.code] = splitter

    @classmethod
    def get(cls, code: str) -> Optional[JurisdictionMetadata]:
        return cls._jurisdictions.get(code)

    @classmethod
    def get_citation_extractor(cls, code: str) -> Optional[CitationExtractor]:
        return cls._citation_extractors.get(code)

    @classmethod
    def get_normalizer(cls, code: str) -> Optional[NormNormalizer]:
        return cls._normalizers.get(code)

    @classmethod
    def get_splitter(cls, code: str) -> LanguageSplitter:
        return cls._splitters.get(code, IdentitySplitter())

    @classmethod
    def list_jurisdictions(cls, active_only: bool = False) -> List[JurisdictionMetadata]:
        all_items = list(cls._jurisdictions.values())
        if active_only:
            return [j for j in all_items if j.is_active]
        return all_items


# =========================================================================
# 注册东盟核心六国法域（出海基建与投资并购核心法域，默认激活）
# =========================================================================

JurisdictionRegistry.register(
    JurisdictionMetadata(
        code="asean_id",
        name_zh="印度尼西亚工程与投资法",
        primary_language="id",
        citation_standard="indonesia_statute",
        default_laws=["UU_2_2017", "UU_6_2023", "SEMA_3_2023", "KUHPerdata", "MEMR_11_2024"],
        is_active=True,
        flag="🇮🇩",
        region="asean",
        language_mode="trilingual",
        description_zh="涵盖印尼《建筑服务法》、电力TKDN新规及SEMA 3/2023合同语言效力规则",
    )
)

JurisdictionRegistry.register(
    JurisdictionMetadata(
        code="asean_vn",
        name_zh="越南建设与投资法",
        primary_language="vi",
        citation_standard="vietnam_law",
        default_laws=["Law_135_2025_QH15", "Decree_210_2026_ND_CP", "Law_64_2020_PPP", "Civil_Code_2015"],
        is_active=True,
        flag="🇻🇳",
        region="asean",
        language_mode="trilingual",
        description_zh="涵盖越南《2025新建设法》第86.2条违约金规则、建设合同法令与PPP法典",
    )
)

JurisdictionRegistry.register(
    JurisdictionMetadata(
        code="asean_my",
        name_zh="马来西亚工程法",
        primary_language="en",
        citation_standard="malaysia_act",
        default_laws=["CIPAA_2012", "Act_520_CIDB", "Contracts_Act_1950"],
        is_active=True,
        flag="🇲🇾",
        region="asean",
        language_mode="bilingual",
        description_zh="涵盖马来西亚CIPAA 2012法定快速裁决、第35条背靠背付款无效及CIDB执照要求",
    )
)

JurisdictionRegistry.register(
    JurisdictionMetadata(
        code="asean_sg",
        name_zh="新加坡工程与国际仲裁",
        primary_language="en",
        citation_standard="singapore_act",
        default_laws=["SOPA_2004", "Building_Control_Act", "IAA_Cap_143A"],
        is_active=True,
        flag="🇸🇬",
        region="asean",
        language_mode="bilingual",
        description_zh="涵盖新加坡SOPA付款保障法、SIAC国际仲裁与BS Mount Sophia保函显失公平止付先例",
    )
)

JurisdictionRegistry.register(
    JurisdictionMetadata(
        code="asean_th",
        name_zh="泰国工程与商业法",
        primary_language="th",
        citation_standard="thailand_code",
        default_laws=["CCC_Hire_of_Work", "FBA_1999", "PPP_Act_2019"],
        is_active=True,
        flag="🇹🇭",
        region="asean",
        language_mode="trilingual",
        description_zh="涵盖泰国民商法典承揽编、外商经营法(FBA)限制与公共工程管辖规则",
    )
)

JurisdictionRegistry.register(
    JurisdictionMetadata(
        code="asean_ph",
        name_zh="菲律宾建设与PPP法",
        primary_language="en",
        citation_standard="philippines_ra",
        default_laws=["RA_11966_PPP_Code", "RA_12009_Procurement", "RA_4566_Contractors", "RA_11659_PSA"],
        is_active=True,
        flag="🇵🇭",
        region="asean",
        language_mode="bilingual",
        description_zh="涵盖菲律宾新《PPP法典》(RA 11966)、CIAC工程仲裁管辖及Manila Water外资牌照先例",
    )
)


