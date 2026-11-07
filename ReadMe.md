# 澜衡-数字化涉外经贸法律查明平台 (Lanheng LegalPlatform)

> **版本**：v7.0 正式生产基线版 (Enterprise Benchmark Edition)  
> **更新时间**：2026-11-07  
> **项目定位**：专为涉外审判法官、国际商事仲裁员、涉外经贸与出海基建央国企法务合规人员及跨境争议解决律师研发的**数字化涉外经贸法律查明、合规风险阻断与争议推演工作台**。

---

## 一、 项目背景与核心价值

在中国企业深入参与共建“一带一路”、推进数字化涉外经贸、算电协同与深化区域经济合作的背景下，出海企业与法务团队常面临多重制度环境挑战：
1. **多法系交错与多语种法律查明成本高**：东盟 11 国横跨普通法系、大陆法系与混合法系，成文法典及部委规章涵盖印尼语、越南语、泰语、高棉语、老挝语等多种属地语言，一手正本查明壁垒高；
2. **东道国强行法与合同约定准据法的脱钩冲突 (Lex Loci Override)**：涉外合同约定适用英美法或离岸法律，但履行地在属地资质、本地化率、外汇管制、土地权属等方面的强行性规范依法具有排他效力，不可协议排除；
3. **合同严苛失权程序与背靠背付款阻断**：国际标准合同（如 FIDIC 第 20.1 款 28 天索赔通知期）的严苛适用，以及分包合同“以业主付款为前提（Pay-when-paid）”条款在属地法下的效力分歧；
4. **见索即付保函恶意索兑与出口信用保险理赔时效约束**；
5. **东道国政策调整、间接征收与国际投资争端（ISDS）救济前置壁垒**。

**澜衡-数字化涉外经贸法律查明平台** 彻底摈弃传统通用大语言模型普遍存在的“法条虚构”、“模板化行文”以及脱离工程实务的“单一伪量化胜诉率”，依托确定性工作流、双层数据底座、跨法系概念对齐算子与真实 SQLite 持久化，提供专业严谨的假定条件推演矩阵（Condition Precedent If-Then Matrix），为涉外经贸决策提供高质量的法理支撑与战术方案。

---

## 二、 核心功能矩阵与业务切面

系统构建了贯穿出海承包工程与境外投资全生命周期的六大业务工作台切面：

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│              澜衡-数字化涉外经贸法律查明平台双擎顶层架构                           │
├────────────────────────────────────────┬─────────────────────────────────────────┤
│   【引擎一：个案查明与争议推演工作台】 │   【引擎二：出海合规体系建设中心】      │
│   (Case-Driven Deep Legal Reasoning)   │   (Systematic Compliance Governance)    │
│                                        │                                         │
│  • 投前合规 / 履约争议双模动态自适应   │  ❶ 涉外建设工程与投资典型案例库 (5D 复盘)│
│  • 7 大专职 Agent 确定性推理流         │  ❷ 全周期五阶段 × 三道防线合规自测评估  │
│  • 双语/三语对照查验与因果穿透图谱     │  ❸ 场景化法律风险矩阵与重大立法变动监测 │
│  • 履行地法强行性规范脱钩冲突检测      │  ❹ 东盟全域涉外投资法律环境横向比选     │
│  • 交互式沙盘试算与多方攻防推演        │  ❺ 境外法律顾问 (Local Counsel) 专家会商 │
│  • CL-Align 概念对齐与 CRAG 自省跨层检索│ ❻ 项目专项法律风险审查报告自动汇编      │
└────────────────────────────────────────┴─────────────────────────────────────────┘
```

1. **境外投资准入与投前合规审查**：自动化审查外资股权比例、原住民土地权属、中资出海投资条约双轨制（CAFTA/BIT vs ACIA）及国际仲裁管辖路径；
2. **建设工程合同强行法合规性审查**：审查双语签署强制令、禁止背靠背条款、保函显失公平止付门槛、法定违约金上限及 FIDIC 黄金条款偏离度；
3. **工程履约索赔与交互式沙盘试算**：针对工期顺延、通知时效、本地化率（TKDN）及信保报损时效进行动态敏感度试算，构建假定条件推演矩阵；
4. **全周期合规评估与项目孵化**：覆盖五大业务阶段（前期尽调 $\rightarrow$ 招投标联营 $\rightarrow$ 合同谈判 $\rightarrow$ 现场履约 $\rightarrow$ 竣工移交）与三道防线核查，未达标项一键专项立项；
5. **境外法律顾问 (Local Counsel) 与 DAAB 专家会商**：对接在册权威大律师与争端裁决专家名录，全流程落实利益冲突排查；
6. **东盟涉外投资环境横向比选**：结构化对比东盟各成员国的法系特征、外资准入、付款效力及司法审查尺度，支持跨国比选立项。

---

## 三、 支持法域与权威数据底座

### 3.1 覆盖法域清单（东盟 11 国全域覆盖）
系统实现对东盟 11 个成员国及国际工程条约体系的全面覆盖：
- **普通法系及混合普通法系**：新加坡 (`asean_sg`)、马来西亚 (`asean_my`)、文莱 (`asean_bn`)、缅甸 (`asean_mm`)；
- **大陆法系及社会主义民法法系**：越南 (`asean_vn`)、泰国 (`asean_th`)、柬埔寨 (`asean_kh`)、老挝 (`asean_la`)、东帝汶 (`asean_tl`)；
- **混合法系（民法/习惯法/伊斯兰法/西班牙法）**：印度尼西亚 (`asean_id`)、菲律宾 (`asean_ph`)；
- **国际商事与投资条约**：联合国 CISG 国际货物销售合同公约、海牙《纽约公约》、华盛顿《ICSID 公约》、中外双边投资保护协定 (BIT)。

### 3.2 L1 核心强行法层与 L2 广覆盖参考层双层架构

| 维度指标 | L1 核心强行法层 (`law.sqlite`) | L2 广覆盖参考层 (`law.sqlite`) | 机制说明 |
| :--- | :--- | :--- | :--- |
| **定位与权威级** | 属地成文法中当事人不得协议排除的**强行性规范**及最高司法裁判先例 (Grade A) | 区域多边条约、双边投资协定、FIDIC 标准合同条件、参考判例 (Grade B) | 双层严格物理隔离，支持独立与级联检索 |
| **典型代表法源** | 印尼《国语法》第 31 条、越南建设工程法定违约金（商贸法第 301 条 8% 罚金上限 / 建设法第 146 条 12% 罚金上限，严格区别实际损失赔偿）、马来 CIPAA 第 35 条禁止背靠背、新加坡 15 年潜伏缺陷时效、泰国 2 年承揽时效、菲律宾 RA 8975 基建停工令豁免、柬埔寨民法典 403 条不可调减违约金、老挝外汇法外债审批、文莱宪法 84C 绝对主权豁免、东帝汶审计法院事前 Visto 签证 | 《东盟全面投资协定》(ACIA)、中国-东盟投资协议 (CAFTA)、双边投资保护协定 (BIT)、FIDIC 1999/2017 黄金条款、CISG 联合国国际货物销售公约、CRW 案 DAAB 决定即时执行力先例 | 确立实体法律权利义务边界，提供上位条约与国际商事仲裁法理补充 |
| **检索索引配置** | 独立 1024 维 BGE-M3 FAISS 向量索引 + 独立 BM25 词法倒排索引 | 独立 1024 维 BGE-M3 FAISS 向量索引 + 独立 BM25 词法倒排索引 | 支持稠密语义与条号、判例案号精确检索 |
| **图谱关联结构** | 因果关系拓扑网络（严格零悬空边） | 1-Hop 拓扑语义扩散与跨层补偿机制 | 支撑多跳推理与上位法追溯 |

---

## 四、 核心技术与算法创新亮点

### 1. LangGraph 确定性推理状态机
摒弃黑盒一次性生成，采用基于 LangGraph 构建的 10 个透明可控计算节点（`s1_extract` 抽取 $\rightarrow$ `s2_precheck` 准据法前置检查 $\rightarrow$ `s3_decompose` 要件拆解 $\rightarrow$ `researcher` 混合检索 ➔ `matcher` 构成要件涵摄 $\rightarrow$ `red_team_strategist` 红蓝对抗推演 ➔ `translator` 多语种对齐 ➔ `drafter` 报告起草 ➔ `critic` 质量门禁 ➔ `s8_review` 专家复核 ➔ `s9_export` 终审封包）。支持在核心环节设置人工阻断门禁，确保结论可控。

### 2. CL-Align 跨法系多语种法学概念对齐算子
针对东盟混合法系概念错位问题，在检索前端建立 `CLAlignOperator` 单例算子（[`lawagent/store/cl_align.py`](file:///C:/Downloads/OverseasLawAssistEast/OverseasLawAssistEast/lawagent/store/cl_align.py)）。依托 165 组多语种法学教义映射张量，将中文日常表述精准投射为属地法定概念（如将“违约金酌减”准确投射至越南法 12% 封顶、柬埔寨民法典 403 条不可调减或普通法 Penalty Rule），消除跨法系语义断层。

### 3. CRAG 自省式检索充分性门禁与跨层补偿循环
在检索与涵摄之间设立量化自省门禁（[`lawagent/flow/sufficiency.py`](file:///C:/Downloads/OverseasLawAssistEast/OverseasLawAssistEast/lawagent/flow/sufficiency.py)）。当系统判定 L1 核心层召回的法源对争议要件的覆盖度 $\tau < 0.75$ 时，自动触发改写查询并跨层调取 L2 区域多边条约与标杆判例图谱，将上位法与国际裁判规则定向注入证据链。

### 4. 履行地法脱钩冲突检测算子 (Lex Loci Override)
当项目履行地与合同约定的准据法脱钩时，自动启动公私法分流判定：公法强行性规范（属地资质、本地化配额、国语法强制令、土地征收、法定裁决）具有属地排他穿透力，不可约定排除；私法商事争议则交由当事人约定准据法审理。

### 5. Critic V1~V12 刚性质量门禁与安全守则
严格运行 12 项合规核验门禁：规范存在性（杜绝虚构法条）、无幻觉引述（陈述必绑定证据 EID）、事实溯源（分析必回溯 F# 事实编号）、司法中立防线（严禁出现“必胜”、“毫无疑问违约”等绝对预测词汇）、时点新旧法溯及力核验、央国企国家安全合规门禁及阻断令对冲防御。

### 6. 中-东盟双向合规审查与法域冲突消解引擎 (Dual Compliance Engine)
核心模块位于 [`lawagent/flow/dual_compliance.py`](file:///C:/Downloads/OverseasLawAssistEast/OverseasLawAssistEast/lawagent/flow/dual_compliance.py)，内设五大跨国业务域确定性双向核验算子：
- **投资准入与双边审批互锁算子**：对标中方发改委 11 号令、商务部 3 号令、国资委 35 号令 vs 东道国外资准入清单/OSS-RBA，输出《附双方法定审批生效先决条件条款》；
- **跨境融资担保与外汇闭环算子**：对标国资委 75 号文超股比担保禁止、外管局 29 号文内保外贷登记 vs 印尼 UU 2/2017 联营体连带责任、老挝外债 BOL 审批、缅甸 1 日强制结汇令，输出按股比分割保函与反担保结构；
- **数据跨境与技术出口管制算子**：对标《数据安全法》第 36 条、《出口管制法》两用物项清单 vs 境外法院/SIAC 证据开示令（新加坡 IAA 第 12A 条），输出脱敏处理与主管机关前置审批操作流；
- **工程分包与本地化配额算子**：对标央企分包审查 vs 马来 CIPAA 第 35 条 / 新加坡 SOPA 第 9 条背靠背付款绝对无效令、印尼 MEMR 11/2024 TKDN 配额；
- **出险保全与争端救济联动算子**：对标中国信保 30 日出险报损窗口期 vs FIDIC 28 天索赔通知时效与 BIT 180 天前置磋商期。
流水线中，`s2_precheck` 评估并生成 `dual_compliance_audit`；`s3_decompose` 自动注入冲突争点与强行法源；`drafter` 与 [`lawagent/api/export.py`](file:///C:/Downloads/OverseasLawAssistEast/OverseasLawAssistEast/lawagent/api/export.py) 输出专章及 5 级集团审批链条。

### 7. “反制裁、反干预、反长臂管辖”（三反）体系化防线
针对美欧对华次级制裁与域外长臂管辖冲击建立专项防线：
- **法源基座**：入库《反外国制裁法》（第 3、4、6、12、15 条）、2025 年国务院《实施〈反外国制裁法〉的规定》、商务部令 2021 年第 1 号《阻断外国法律与措施不当域外适用办法》（第 5、7、9 条）、《不可靠实体清单规定》、《出口管制法》与《外国国家豁免法》；L2 收录新加坡 MAS 2022 金融制裁指令（Sec 27A）及普通法 *Lamesa* 先例；
- **哨兵架构拆分**：在 [`lawagent/flow/security_sentinel.py`](file:///C:/Downloads/OverseasLawAssistEast/OverseasLawAssistEast/lawagent/flow/security_sentinel.py) 严格区分多边开发银行（世行/亚行）合规除名（`mdb_debarment_risk`）与美欧单边次级制裁（`unilateral_sanctions_long_arm`）；
- **30 日双边行动方案**：【3日内】启动合同替代币种（RMB/CIPS 或东道国本币）结算；【7日内】向业主出具属地大律师（Local Counsel）无域外效力意见函；【14日内】对配合制裁的外方依据《反外国制裁法》第 12 条向国内法院提起损害赔偿与财产保全；【30日内】向商务部履行阻断报告义务并向中信保报损；
- **合同毒丸红线审查**：在 [`lawagent/api/routes/verify.py`](file:///C:/Downloads/OverseasLawAssistEast/OverseasLawAssistEast/lawagent/api/routes/verify.py) 强制阻断“宽泛单边制裁无偿解约与保函没收条款”及“绕过主权审批的域外长臂调证条款”。

### 8. GraphRAG 跨层拓扑网络与统一视图 (`unified_edges`)
彻底解决传统单层图检索孤立缺陷：
- **统一跨层拓扑视图**：在 `law.sqlite` 建立 `unified_edges` 视图，打通 L1 属地强行法与 L2 国际条约，注入 120+ 跨层桥接边（涵盖东盟成文法 $\leftrightarrow$ CAFTA/ACIA/BIT $\leftrightarrow$ FIDIC 银皮书 $\leftrightarrow$ 中国母国强行法）；
- **语义优先级加权**：消除 35 组重复边，建立唯一索引约束，按强行法冲突（Tier 1: `overrides`, `conflicts_with`, `exception_to`）、判例互证（Tier 2: `applied_in`, `interprets`）及一般层级重算 `edges_top.rk`；
- **28 个高内聚风险社区**：覆盖东盟 11 国与中方母国规制，包含中文实务法理综述 (`community_summary_zh`) 与双向合规锚点；
- **真实拓扑穿透接口**：新增 `GET /api/search/graph-neighborhood` 端点，前端 [`InteractiveCitationGraph.tsx`](file:///C:/Downloads/OverseasLawAssistEast/OverseasLawAssistEast/FrontEnd/src/components/analysis/InteractiveCitationGraph.tsx) 动态调用展示真实 SQLite 跨层关联边。

### 9. 长耗时 AI 通信超时容灾与平滑降级机制
消除大模型深度推理导致的前端通信中断：
- **前端网络超时阈值基准放宽**：[`FrontEnd/src/api/client.ts`](file:///C:/Downloads/OverseasLawAssistEast/OverseasLawAssistEast/FrontEnd/src/api/client.ts) 默认超时由 25 秒调整为 60 秒，[`lawAgentApi.ts`](file:///C:/Downloads/OverseasLawAssistEast/OverseasLawAssistEast/FrontEnd/src/api/lawAgentApi.ts) 要素抽提配置 90 秒长超时；
- **后端主动超时熔断与零中断回退**：[`lawagent/api/routes/cases.py`](file:///C:/Downloads/OverseasLawAssistEast/OverseasLawAssistEast/lawagent/api/routes/cases.py) 在 `extract_case_intake` 中通过 `asyncio.wait_for(..., timeout=45.0)` 实施主动超时控制，超时自动平滑回退至毫秒级完成的本地确定性规则提取引擎，100% 确保接口返回有效 HTTP 200。

---

## 五、 真实案例基准评测验证与性能表现

系统选取了覆盖东盟 11 国及国际商事条约的 **20 个跨国涉外疑难真实案例** 进行全自动化批量验证测试（评测脚本位于 [`scripts/run_batch_evaluation_20.py`](file:///C:/Downloads/OverseasLawAssistEast/OverseasLawAssistEast/scripts/run_batch_evaluation_20.py)），实测指标如下：

### 5.1 核心评测指标综合仪表盘

| 核心评测维度 | 实测指标得分 | 传统通用 RAG 基准 | 表现说明 |
| :--- | :---: | :---: | :--- |
| **查明流程全通成功率 (Success Rate)** | **100.0% (20/20)** | 85.0% | 20 个大案全部成功闭环流转至 S9 终审归档，零异常中断 |
| **基准法条与判例召回率 (Statute Recall)** | **97.50%** | 68.5% | 结合 CL-Align 概念对齐算子后，多语种与概念断层显著拉平 |
| **实体结论裁判准确率 (Legal Accuracy)** | **100.00%** | 72.0% | 要件涵摄分析与判决主文精准命中属地成文法与判例先例 |
| **CRAG 跨层补偿触发率 (CRAG Trigger Rate)** | **85.0% (17/20)** | 0% (无自省) | 当 L1 单层不足时，自省门禁触发并跨层调取上位条约与先例 |
| **L2 跨层补充法源贡献总量** | **91 条** | 0 条 | 注入 CISG、BIT 投资条约、FIDIC 先例等跨国裁判规则 |
| **单案平均端到端耗时 (Avg Latency)** | **113.22 秒** | 120+ 秒 | 采用解耦分工调度，保障高密推理下的稳定产出 |
| **全量自动化单元测试通过率** | **100.0% (39/39)** | - | 覆盖 GraphRAG、CL-Align、CRAG、Critic、双向合规及阶段四 API 回归全部核心逻辑 |

### 5.2 真实司法判决与系统查明策略深度对比
评测对 20 个案例的真实法院/仲裁庭判决主文（Ground-Truth Holding）与系统查明策略进行了逐案比对：
- **实质法理吻合率达 100% (20/20)**：在胜诉/败诉风险定性、法庭裁决倾向判定、攻防救济路线规划上与真实最高法院先例及国际仲裁裁决保持高度实质一致；
- **排除了多项重大战略误判**：如在柬埔寨案中准确排除“请求法官酌减违约金”这一违反柬埔寨民法典 403 条的死路；在文莱案中准确预警宪法 84C 条绝对主权豁免并指导转向国际仲裁；在新加坡 DAAB 案中准确指导依据 CRW 规则申请即席裁决执行款项。

### 5.3 评测报告文档索引
- 📄 **测试结果汇总与分析报告**：[`docs/test_reports/evaluation_summary.md`](file:///C:/Downloads/OverseasLawAssistEast/OverseasLawAssistEast/docs/test_reports/evaluation_summary.md)
- 📋 **详细测试经过记录**：[`docs/test_reports/detailed_execution_log.md`](file:///C:/Downloads/OverseasLawAssistEast/OverseasLawAssistEast/docs/test_reports/detailed_execution_log.md)
- ⚖ **真实判决与系统查明策略深度对比表**：[`docs/test_reports/actual_ruling_comparison.md`](file:///C:/Downloads/OverseasLawAssistEast/OverseasLawAssistEast/docs/test_reports/actual_ruling_comparison.md)
- 💾 **原始结构化评测数据集**：[`docs/test_reports/evaluation_raw_data.json`](file:///C:/Downloads/OverseasLawAssistEast/OverseasLawAssistEast/docs/test_reports/evaluation_raw_data.json)

---

## 六、 快速上手与运行指南

### 6.1 Windows 用户一键启动（推荐）
项目已内置专属 Windows 一键运行脚本，支持自动环境自检、依赖检查、历史端口清理、前后端并行启动并在就绪后**自动调起默认浏览器打开系统主界面**：

* **一键启动并打开网页**：直接双击项目根目录下的 **`start.bat`**（或在 PowerShell 终端运行 `.\start.ps1`）；
* **一键停止前后端服务**：在启动控制台按回车键退出，或随时双击运行 **`stop.bat`** 释放端口。

```text
服务就绪后系统访问入口:
- 前端 Web 控制台:  http://localhost:3000
- 后端 API 根地址:  http://127.0.0.1:8000
- 交互式接口文档:  http://127.0.0.1:8000/docs
```

### 6.2 环境要求
- **Python**: 3.10+ (推荐 3.10 ~ 3.12)
- **Node.js**: 18.0+ (推荐 20+ LTS)
- **操作系统**: Windows 10/11 / macOS / Linux

### 6.3 手动分步启动方式

#### 1. 后端服务启动
```bash
# 1. 安装后端依赖
pip install -r requirements.txt

# 2. 启动 FastAPI 后端服务 (默认运行在 http://localhost:8000)
python -m uvicorn lawagent.api.main:app --host 127.0.0.1 --port 8000 --reload
```

#### 2. 前端界面启动
```bash
# 进入前端工程目录
cd FrontEnd

# 安装依赖并启动开发服务器 (默认运行在 http://localhost:3000)
npm install
npm run dev
```

### 6.4 运行全量自动化测试与基准评测
```bash
# 运行全部 39 项单元测试（涵盖法条查明、图扩展、重排、概念对齐、CRAG充分性、智能建案、双向合规与阶段四 API）
python -m pytest tests/ -q

# 执行 20 案例自动化基准评测流水线
python scripts/run_batch_evaluation_20.py
```

---

## 七、 工程目录全景结构

```
OverseasLawAssistEast/
├── lawagent/                       # 后端核心源码包
│   ├── api/                        # RESTful 接口层与路由定义
│   ├── core/                       # 核心数据模型 (CaseState, Evidence 等)
│   ├── flow/                       # LangGraph 状态图与业务节点 (S1~S9)
│   ├── llm/                        # 大模型客户端与调用策略
│   └── store/                      # 知识库存储、CL-Align 对齐算子与混合检索引擎
├── FrontEnd/                       # 现代化前端界面工程 (React + TypeScript + Vite)
│   ├── src/components/             # 业务组件库 (验证、分析、合规、比选、会商等)
│   └── src/types/                  # 前端 TypeScript 类型定义
├── data/                           # 数据持久化目录
│   ├── snapshots/                  # 不可变法典快照 (SQLite + 索引文件)
│   └── state/                      # 案卷状态运行时数据库 (state.sqlite)
├── docs/                           # 项目文档与技术规范
│   └── test_reports/               # 真实案例测试报告与分析文档
│       ├── evaluation_summary.md   # 测试结果汇总报告
│       ├── detailed_execution_log.md # 详细测试经过记录
│       ├── actual_ruling_comparison.md # 真实判决与策略对比表
│       └── evaluation_raw_data.json # 评测原始数据集
├── scripts/                        # 数据库构建、修复、对齐与评测脚本
├── tests/                          # 自动化单元测试集 (39 passed)
├── 东盟域外法查明助手设计方案.md       # 系统架构与详细设计规范
└── ReadMe.md                       # 项目用户手册与技术全景指南
```

---

## 八、 声明与能力边界

1. **司法中立性**：本系统输出的法理分析、证据清单及战术建议均遵循中立性原则，仅供涉外法律实务与企业合规决策参考，不构成对任何司法或仲裁结果的承诺保证；
2. **法源溯源性**：系统引述的所有成文法条及裁判文书均已绑定底层数据库快照指纹，支持逐条溯源复验。
