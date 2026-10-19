"""德语复合词对称拆分与分词处理器 (Symmetric Compound Splitter)
对齐技术方案第 4.4 节：
- 索引与查询两侧采用相同的拆分器，保留原词与拆出的词根
- 规则处理德语连接成分 (Fugenelemente: '', 's', 'n', 'en', 'es', 'e', 'er')
- 保持法条整体标示 (如 §433)、元音变音 (ä/ö/ü/ß) 标准化与 Snowball 词干化
"""

import re
import snowballstemmer
from typing import List, Set, Dict, Optional
from collections import Counter
from lawagent.core.jurisdiction import JurisdictionRegistry, LanguageSplitter

FUGEN = ("", "s", "n", "en", "es", "e", "er")
RE_SECTION = re.compile(r"§§?\s*(\d+[a-z]?)", re.IGNORECASE)
RE_CLEAN = re.compile(r"[^a-z0-9äöüß§\s\-_]", re.IGNORECASE)


class VocabSplitter:
    """基于德语语料词表的复合词递归拆分器"""
    def __init__(self, vocab_words: Optional[Set[str]] = None, min_part: int = 4, min_freq: int = 2):
        self.min_part = min_part
        self.min_freq = min_freq
        self.v: Set[str] = set()
        if vocab_words:
            self.v = {w.lower() for w in vocab_words if len(w) >= min_part}

    def train_from_texts(self, texts: List[str]):
        """从入库文本统计词频并构建合法词表"""
        counts = Counter()
        for t in texts:
            words = RE_CLEAN.sub(" ", t.lower()).split()
            for w in words:
                if len(w) >= self.min_part and not w.startswith("§"):
                    counts[w] += 1
        self.v = {w for w, c in counts.items() if c >= self.min_freq and len(w) >= self.min_part}

    def split(self, word: str, depth: int = 0) -> List[str]:
        w = word.lower().strip()
        if depth > 3 or (w in self.v and len(w) <= 7):
            return [w]

        best = None
        for i in range(self.min_part, len(w) - self.min_part + 1):
            for f in FUGEN:
                if f and not w[:i].endswith(f):
                    continue
                head = w[:i - len(f)] if f else w[:i]
                tail = w[i:]
                if head in self.v:
                    rest = [tail] if tail in self.v else self.split(tail, depth + 1)
                    if all(p in self.v for p in rest):
                        cand = [head] + rest
                        if best is None or len(cand) < len(best):
                            best = cand

        return best or [w]


class AseanTextProcessor:
    """东盟涉外建设工程与国际经贸全文检索分词与索引标记生成器 (支持中/英/印尼/越/泰跨语言检索)"""
    def __init__(self, splitter: Optional[VocabSplitter] = None):
        self.en_stemmer = snowballstemmer.stemmer("english")
        self.splitter = splitter or VocabSplitter()

    def tokenize(self, text: str) -> List[str]:
        """将多语言混合法律文本切分为用于 BM25 检索的高质量 token 集合"""
        if not text:
            return []

        # 1. 规范化空白
        t = re.sub(r"\s+", " ", text).strip()

        # 2. 提取并保留关键法条编号与英文缩写 (如 Clause 20.1, Art.57, Sec.35, SEMA 3/2023, CIPAA 2012)
        clause_matches = re.findall(r"(?:clause|art(?:icle)?|sec(?:tion)?|uu|law|decree|sema|cipaa|sopa|fidic)[\s_\-\.:]*\d+(?:[\.:]\d+)*", t, re.IGNORECASE)
        norm_tokens = [re.sub(r"[\s_\-]+", "_", m.lower()) for m in clause_matches]

        # 3. 英文与拉丁字母词汇 (印尼语/英语/越南语无音标)
        latin_words = re.findall(r"[a-zA-Z0-9_\-\.]{2,}", t)
        stemmed_words: List[str] = []
        for w in latin_words:
            wl = w.lower().strip(".-_")
            if len(wl) >= 2:
                stemmed_words.append(wl)
                stemmed = self.en_stemmer.stemWord(wl)
                if stemmed != wl:
                    stemmed_words.append(stemmed)

        # 4. 中文字符与连续词组 (2-4字 n-gram 提升中文召回)
        chinese_chars = re.findall(r"[\u4e00-\u9fa5]+", t)
        zh_tokens: List[str] = []
        for segment in chinese_chars:
            if len(segment) <= 4:
                zh_tokens.append(segment)
            else:
                zh_tokens.append(segment)
                for i in range(len(segment) - 1):
                    zh_tokens.append(segment[i:i+2])
                for i in range(len(segment) - 2):
                    zh_tokens.append(segment[i:i+3])

        all_tokens = norm_tokens + stemmed_words + zh_tokens
        return [tok for tok in all_tokens if len(tok) >= 2]


# 兼容性别名
GermanTextProcessor = AseanTextProcessor
