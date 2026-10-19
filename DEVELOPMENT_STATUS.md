# 域外法查明辅助应用 (OverseasLawAssist) 开发状态与进度追踪

> **当前阶段**：纯净聚焦东盟工程与出海央国企合规转型（Step 1 - Step 5 剥离德美与端到端基准验收）已圆满完成  
> **更新时间**：2026-10-19  
> **当前状态**：德美法域兼容代码及历史数据已 100% 物理剥离，系统纯净聚焦东盟 6 国建设工程与海外投资合规，全套 30/30 项测试持续 100% 绿灯（耗时 14.41s），前端生产构建 0 错误 0 警告，完全符合《前端设计原则.md》(Completed & Fully Verified)

---

## 1. 架构定位与纯净东盟基建工程合规设计

本系统目标定位为**中国出海基建央企/国企在东盟 6 国（印尼、越南、马来西亚、新加坡、泰国、菲律宾）建设工程（EPC/PPP/特许经营/M&A/联营体）法律风险防范、合规指引与争议推演专业工作台**。系统已彻底剥离宽泛的德美历史法域，全面确立了**“法源真实权威 ➔ 争点客观拆解 ➔ 要件严格涵摄 ➔ 动态攻防对抗 ➔ 国家安全哨兵 ➔ 双语报告导出”**的全链路闭环：

```
[用户层 / 前端 UI (React 19 + Tailwind CSS + 极简中性图标，严格对齐前端设计原则)]
                         │
        (Vite Proxy: /api -> http://127.0.0.1:8000)
                         │
[FastAPI 服务层 lawagent.api] ── [REST 接口 / 依赖注入 / 专家流转 / DOCX 导出]
                         │
[LangGraph 核心推理状态图 StateGraph(CaseState)]
   S1 Extract ─> S2 Precheck ─> S3 Decompose ─> S4 Researcher ─> S5 Matcher
    └── S6 Strategist ─> S7 Drafter ─> Critic (V1-V12 哨兵一票否决) ─> S8 Review ─> S9 Export
                         │
[多法域注册中心 JurisdictionRegistry (纯净东盟 6 国 + FIDIC)]
   ├── asean_id: 印度尼西亚 (建筑法第57条, SEMA 3/2023, MEMR 11/2024, 民法典第1338条)
   ├── asean_vn: 越南 (2025新建设法第86.2条LD预定赔偿, 210/2026建设合同法令)
   ├── asean_my: 马来西亚 (CIPAA 2012 第35条反背靠背, 建筑工业发展局法 Act 520)
   ├── asean_sg: 新加坡 (SOPA 2004 第9条反背靠背, BS Mount Sophia 显失公平保函止付)
   ├── asean_th: 泰国 (民商法典第596条违约金酌减, 外商经营法 FBA 1999)
   └── asean_ph: 菲律宾 (2023年PPP法典 RA 11966 特许权补偿, Manila Water 准入先例)
                         │
[双 SQLite 数据库存储架构 (零德美数据残留)]
   ├── 快照库 law.sqlite (只读, 25 条东盟成文法, 7 篇东盟工程判例, 46 分块, 司法部法通网三语对照)
   └── 运行库 state.sqlite (读写 WAL 模式, C101~C104 央企实战示范案, 3 大东盟特邀工程法专家)
```

---

## 2. 阶段规划与交付里程碑

| 阶段 | 核心任务 | 交付物 | 状态 |
| :--- | :--- | :--- | :--- |
| **Phase 1** | 基础骨架、配置管理、多法域抽象、双 SQLite 库、德联邦法官方 XML 采集与解析管线 | `lawagent/` 骨架、`law.sqlite` 快照库、`state.sqlite` 运行库、XML解析测试 | **已完成 (5/5 测试通过)** |
| **Phase 2** | 复合词拆分器、BM25 混合检索、本体边表构建、知识库预制、FAISS稠密向量与GPU加速 | 4,990 分块入库、BM25 索引持久化、FAISS 稠密索引、`HybridRetriever` 检索与扩展 | **已完成 (5/5 测试通过)** |
| **Phase 3** | LangGraph 工作流编排（S1~S9）、要素充分性迭代、Matcher 四态涵摄、中德术语翻译、双包起草与 Critic V1-V11 质检 | LangGraph 运行图、状态 Checkpoint、S1~S9 节点套件、11项质量门禁校验 | **已完成 (5/5 测试通过)** |
| **Phase 4** | FastAPI 接口、SSE 实时事件广播、前端去 Mock 彻底重构、Vite 代理配置与打包验证 | 前端 `mockData.ts` 彻底删除、全链路 API 打通、前端生产构建 0 错误 | **已完成 (8/8 测试通过)** |
| **Phase 5** | Word (DOCX) 双包报告导出生成、E1-E9 自动化基准评测套件、一票否决项验收 | `lawagent/api/export.py`、DOCX 导出端点、`eval/run.py` 评测报告 (验收通过) | **已完成 (4/4 测试通过)** |
| **Phase 6** | 三位一体涉美商事法架构、15篇金标准判例滚雪球扩充、CourtListener与Shepardizing存续状态机、涉外解释二定向校准器、Step编排与交互优化 | `courtlistener.py`、`us_admissibility_calibrator.py`、`test_us_architecture.py`、前端 Step 精炼显示 | **已完成 (4/4 测试通过)** |
| **Phase 7** | 东盟基建与投资并购转型基础架构：6国法域注册激活、欧美法域软屏蔽、项目生命周期阶段抽象（投前合规/履约争议）、工程与投资业态多选契约、安全哨兵强类型模型、跨阶段平滑流转接口与全套前端组件升级 | `lawagent/core/jurisdiction.py` (东盟6国+欧美软屏蔽)、`lawagent/core/types.py` (东盟类型扩展)、`lawagent/api/routes/cases.py` (阶段转换与元数据)、`FrontEnd/src/configs/jurisdictions.ts`、`CaseEntryModal.tsx`、`test_phase7_contracts.py` | **已完成 (5/5 测试通过)** |
| **Phase 8** | 东盟六国 2026 法源、法通网对齐与 FIDIC 双层入库：11 项多语言/分级字段扩展、25 核心法源（越南 2025 新建设法、印尼 SEMA 3/2023、菲 RA 11966 等）、FIDIC 银/黄/红 Tier 1 & Tier 2、3-Layer Legal GraphRAG 拓扑边与 6 大风险主题社区、BM25 全量重构 | `lawagent/store/db.py`、`lawagent/store/snapshots.py`、`lawagent/store/retriever.py`、`scripts/build_asean_kb.py`、`tests/test_phase8_kb.py` | **已完成 (6/6 测试通过)** |
| **Phase 9** | 双擎推理流、安全哨兵与“央国企合规体系建设中心”开发：`security_sentinel.py` 三层防御节点、TKDN/EOT 审查算子、前端三大中心模块（案例参考/合规指引/风险矩阵）、多语种法条抽屉与四列分层因果图 | `lawagent/flow/security_sentinel.py`、`lawagent/flow/nodes.py`、`FrontEnd/src/components/compliance/*`、`LawDrawer.tsx`、`InteractiveCitationGraph.tsx`、`test_phase9_sentinel.py` | **已完成 (6/6 测试通过)** |
| **Phase 10** | 东盟工程实战案例播种、端到端集成测试、双模板 DOCX 报告验证与 E1-E9 评测验收 | `scripts/seed_asean_cases.py`、`tests/test_asean_architecture.py`、DOCX 报告与合规手册流式导出、`eval/run.py` 全指标评测验收 | **已完成 (5/5 测试通过，全系统 50/50 测试通过，E1-E9 验收通过)** |

---

## 3. 当前运行环境与模型配置

- **操作系统**：Windows (x86_64)
- **Python 环境**：Python 3.10.6
- **GPU 算力**：NVIDIA GeForce RTX 2070 SUPER (8GB VRAM, CUDA 12.8, BGE-M3 向量加速)
- **前端环境**：Node v24.12.0, Vite 8, React 19, TypeScript
- **大模型配置 (DashScope 兼容模式)**：
  - **Base URL**：`https://dashscope.aliyuncs.com/compatible-mode/v1`
  - **API Key**：从环境变量 `OPENAI_API_KEY` 动态读取
  - **主生成与推理模型**：`deepseek-v4.1-flash`（配合长文本指令遵循与高吞吐低延迟流式响应，同时在网络受限时由本地规则引擎自适应兜底）
  - **校验裁判模型**：`deepseek-v4-pro-0813`（专职执行 V1-V11 全套质量门禁审查与一票否决拦截）
- **服务端口规范**：
  - **后端 FastAPI**：`http://127.0.0.1:8000`
  - **前端工作台**：`http://localhost:3000`

---

## 4. 全量开发任务执行详细记录

### Phase 1: 工程骨架、数据抽象与官方数据入库
- [x] Python 依赖与 CUDA 环境核验（安装 rank-bm25, snowballstemmer, sse-starlette, slowapi, langgraph-checkpoint-sqlite）
- [x] DashScope API 连通性测试与多模型探查（DeepSeek 与 Qwen 连通）
- [x] 创建 `lawagent/` 完整目录结构与 `configs/` 配置文件（`models.yaml`, `roles.yaml`, `tokens.yaml`, `limits.yaml`, `retrieval.yaml`, `quality_gate.yaml`）
- [x] 实现 `lawagent/core/jurisdiction.py` 多法域与语言核心抽象协议（解耦 Jurisdiction, Extractor, Normalizer, Splitter）
- [x] 实现 `lawagent/core/types.py` 完整状态对象定义（对齐前端 TypeScript 契约与技术方案 5.1 节）
- [x] 实现 `lawagent/store/` 双库模型：快照库 `law.sqlite` 与运行库 `state.sqlite`
- [x] 实现 `lawagent/llm/client.py` 结构化输出客户端（支持 json_repair、Pydantic 验证及主备自动故障转移）
- [x] 成功采集并解析入库德国联邦法官方法典（4,569 条成文法：BGB 2551条、HGB 696条、GmbHG 127条、ZPO 1094条、EGBGB 250条），含 Absatz 与 Nummer 细化结构
- [x] 预制并复核 `kb/de_federal/` 示范数据集（包含物之瑕疵 `kauf_mangel.yaml`、给付迟延 `verzug_schaden.yaml`、40+ 核心民商法术语 `glossary.csv`、重大修订时点表 `timepoints.yaml` 与本体 `ontology.yaml`）
- [x] 编写并运行阶段 1 单元测试套件 `tests/test_phase1.py`（5/5 全部通过）

### Phase 2: 复合词拆分、混合检索与 FAISS 向量索引
- [x] 实现德美双语复合词对称拆分与分词处理器 `lawagent/store/compound.py`
- [x] 实现法条与判例切块模块 `lawagent/store/chunker.py`（生成带上下文前缀 ctx_prefix 的 chunks）
- [x] 构建 BM25 检索引擎 `lawagent/store/bm25.py` 并完成索引持久化缓存
- [x] 基于本地 NVIDIA GPU (CUDA) 构建 BGE-M3 FAISS 稠密向量索引 (`lawagent/store/vec.py`)
- [x] 实现本体图扩展存储模块 `lawagent/store/graph.py`（基于 edges 与递归 CTE 实现受限 1~2 跳图遍历与热门判例查询）
- [x] 实现重排抽象层 `lawagent/store/rerank.py`（支持 Cross-Encoder 与平滑加权回退）
- [x] 实现端到端混合检索器 `lawagent/store/retriever.py`（整合精确通道、术语库扩充、BM25 全文检索、向量检索、RRF 融合、图扩展、重排与 Evidence 封装）
- [x] 编写并运行阶段 2 单元测试套件 `tests/test_phase2.py`（5/5 全部通过）

### Phase 3: LangGraph 工作流与推理全节点
- [x] 实现入口预检与重大修订时点核验模块 `lawagent/flow/checks.py`（CISG 触发闸门、时点红黄两态不设绿态、准据法入口清单）
- [x] 实现构成要件充分性评估模块 `lawagent/flow/sufficiency.py`（评估 covered/partial/missing，提供改写缺口指导）
- [x] 实现要件事实涵摄匹配与判例比对模块 `lawagent/flow/matcher.py`（四态涵摄判定、V10 事实溯源与实体一致性核查、类案对比）
- [x] 实现质量门禁与防线核验模块 `lawagent/flow/critic.py`（V1-V11 全套核验、V8 严禁绝对诉讼预测客观防线、计算 DashboardMetrics）
- [x] 实现推理工作流全节点套件 `lawagent/flow/nodes.py`（S1 Extract -> S2 Precheck -> S3 Decompose -> S4 Researcher -> S5 Matcher -> S6 Strategist -> S7 Drafter -> Critic -> S8 Review -> S9 Export）
- [x] 编排 LangGraph 状态图与断点恢复调度器 `lawagent/flow/graph.py`（支持 SqliteSaver 与 MemorySaver 检查点持久化）
- [x] 编写并运行阶段 3 单元测试套件 `tests/test_phase3.py`（5/5 全部通过）

### Phase 4: FastAPI 服务端、SSE 事件流与前端去 Mock 彻底重构
- [x] 实现应用依赖注入单例管理 `lawagent/api/deps.py`
- [x] 实现实时工作流流式事件广播总线 `lawagent/api/sse.py`
- [x] 实现案件管理与工作流驱动路由 `lawagent/api/routes/cases.py`（包含增删查改、run 工作流、confirm 闸门、followup 追加问题、statement 审核、SSE 事件流与 traces 接口）
- [x] 实现法律规范与法院判例全文检索路由 `lawagent/api/routes/search.py`
- [x] 实现外国法证据材料智能核验路由 `lawagent/api/routes/verify.py`
- [x] 实现特邀法律专家名录与会商流转路由 `lawagent/api/routes/consults.py`
- [x] 实现 FastAPI 主入口 `lawagent/api/main.py`（CORS 跨域、lifespan 启动生命周期、自动播种真实涉外法律案件）
- [x] 彻底删除前端 `FrontEnd/src/api/mockData.ts` 与所有本地内存 mock fallback 逻辑
- [x] 重构前端 API 客户端 `lawAgentApi.ts` 与 `client.ts`，配置 Vite 反向代理 `/api -> http://127.0.0.1:8000`
- [x] 成功安装前端所有依赖并完成 Vite 生产打包验证（`npm run build` 打包产物 0 警告 0 报错）
- [x] 编写并运行阶段 4 单元测试套件 `tests/test_phase4.py`（8/8 全部通过）

### Phase 5: 规范导出、评测套件与验收
- [x] 实现符合最高人民法院《涉外民事关系法律适用法解释（二）》第三条规范标准的 DOCX 报告生成器 `lawagent/api/export.py`
- [x] 提供 `GET /api/cases/{case_id}/export/docx` 下载接口，生成包含 A包（查明文本包）与 B包（咨询准备包）的标准法律意见书
- [x] 实现 E1-E9 自动化基准评测套件 `eval/run.py`，支持召回率、MRR、一票否决项校验与自动化报告落盘
- [x] 运行全量单元测试套件，全量测试全部通过
- [x] 执行 E1-E9 评测，验收结论：**PASSED**（幻觉数=0，溯源错误数=0，绝对预测数=0，法条召回率@10=100%，要件覆盖率=100%）

### Phase 6: 三位一体涉美商事法落地、金标准先例扩充与交互优化
- [x] **涉美核心成文法精选入库**：精选入库《美国统一商法典》(UCC 49 条，涵盖买卖、投资证券与担保交易核心编)、特拉华州普通公司法 (DGCL 7 条) 与美国法典 (28 U.S.C. § 1782 等 12 条)，全量成文法扩充至 **4,642 条**、切块扩充至 **5,132 Chunks**；
- [x] **15 篇全美金标准权威先例滚雪球沉淀**：
  - 深度清洗并入库 15 篇全美里程碑金标准先例（*Eastern Air Lines*, *Step-Saver*, *Delano Growers*, *Intel v. AMD*, *ZF Automotive*, *Unocal*, *Delchi Carrier*, *Hall Street*, *Mitsubishi Motors*, *First Options*, *Kahn v. MFW*, *AMF*, *Eastern Air Lines v. Gulf Oil*, *ProCD* 等），全量判例库扩充至 **27 篇**；
  - 预编译生成 **119 条拓扑边表 (`edges`)** 与 **47 条热门规范判例映射 (`hot_norm_cases`)**，实现成文法检索自动通过图扩散带出金标准先例；
- [x] **Tier 2 CourtListener 动态检索与 Shepardizing 存续状态机**：
  - 实现 `lawagent/integrations/courtlistener.py`，集成远程案例库检索并构建 SCOTUS (1.0)、Circuit (0.85)、State Supreme (0.80) 法院层级加权算法；
  - 实现先验 Shepardizing/KeyCite 效力检验器，对已被后续判例推翻的失效先例（如 *Roto-Lith*）实施**一票否决拦截剔除**；
- [x] **Tier 3 涉外司法实务定向校准器 (USAdmissibilityCalibrator)**：
  - 实现 `lawagent/flow/us_admissibility_calibrator.py`，严格对接最高人民法院《涉外民事关系法律适用法解释（二）》第三条查明规范；
  - 自动化输出五项涉美专属入口审查清单（选法协议、CISG 排斥、UCC § 2-104 商人认定、UCC § 2-725 时效及海牙附加证明书 Apostille）、举证责任分配与八项必备要素合规证明报告；
- [x] **工作台 Step 编排与前端交互深度优化**：
  - 前端 Step 步骤卡片标题由动态过滤序号重构为计算全局确定性索引 `Step {globalStepIndex}. {step.name}`，与顶部全景时间轴严格对齐；
  - 进行中步骤（`running`）采用精炼高亮微胶囊展示，待执行步骤（`pending`）完全隐藏，完成步骤清晰呈现指标与日志；
  - 清理全量调试注释与残留跟踪标记，确保前端代码纯净；
- [x] **涉美架构全套单元测试闭环**：
  - 编写并运行 `tests/test_us_architecture.py`（4/4 全部通过）；
  - 全系统全阶段单元测试扩充至 **28/28 项测试持续 100% 绿灯全绿**。

### Phase 7: 东盟国家建设工程与跨境投资并购转型基础 (Phase 7 ASEAN Foundation)
- [x] **多法域注册中心东盟 6 国激活与欧美法域软屏蔽**：
  - 在 `lawagent/core/jurisdiction.py` 注册印尼（`asean_id`）、越南（`asean_vn`）、马来西亚（`asean_my`）、新加坡（`asean_sg`）、泰国（`asean_th`）、菲律宾（`asean_ph`）6 大活跃法域，配置旗帜、官方语言、引证标准与首批代表性法规；
  - 欧美历史法域（`de_federal`、`us_commercial`）实施 `is_active=False` 软屏蔽，既支持新案界面过滤，又保障历史已建案件与 Phase 1~6 单元测试完全绿灯兼容。
- [x] **东盟基建与投资并购核心数据类型扩展**：
  - 在 `lawagent/core/types.py` 扩展项目生命周期阶段（`LifecycleStage`: `pre_investment` 投前并购与签约合规审查 / `execution_dispute` 履约索赔、保函止付与争议解决）；
  - 扩展工程投资业态多选标签（`ProjectArchetype`: `EPC_CONTRACTING`, `PPP_CONCESSION`, `CROSS_BORDER_MA`, `JV_CONSORTIUM`）；
  - 扩展 `CaseMeta`、`CaseState`（`parent_case_id`、`security_alerts`）与 `CaseSummary`。
- [x] **国家安全与经济安全哨兵强类型模型 (Security Sentinel)**：
  - 实现 `SecurityAlertItem` 与 `SecurityRiskLevel`（`critical`, `high`, `caution`, `safe`）；
  - 强类型覆盖：关键基础设施外资国安审查、资源民族主义与本地化率（TKDN）偏离、征收与国有化（含隐性征收）、多边金融机构制裁黑名单、数据与图纸跨境调证违法（数据安全法第36条）、国资委海外投资监管红线以及中信保 30 日报损与代位求偿保全指引。
- [x] **项目生命周期跨阶段平滑流转契约**：
  - 实现 `POST /api/cases/{case_id}/transition-stage` 端点，支持从投前合规阶段无缝衍生履约争议阶段案件（或反向衍生）；
  - 自动继承国别、业态、合同版本、准据法、事实清单与法律争议焦点，形成关联母子案追踪链。
- [x] **法域元数据查询接口规范**：
  - 实现 `GET /api/jurisdictions`，支持 `active_only` 过滤，为前端多端展示提供动态法域元数据支撑。
- [x] **前端法域配置与录入弹窗全面升级 (FrontEnd UI)**：
  - 建立 `FrontEnd/src/configs/jurisdictions.ts` 集中管理东盟 6 国与历史法域；
  - 重构 `CaseEntryModal.tsx`：东盟 6 国网格化选择、生命周期模式二选一切换、四大业态多选组合胶囊、印尼/越南/马来西亚三大央企实战示范案一键导入；
  - 升级 `CasePipelineAnimationModal.tsx`，展示东盟五阶段智能流水线；
  - 升级 `CaseListView.tsx`，动态呈现东盟法域国旗名称与生命周期微型指示器。
- [x] **严格落实《前端设计原则.md》视觉范式**：
  - 彻底清除 `Scale`（天平）与 `Gavel`（法槌）拟物化法器图标，转用中性严谨的 `FileSearch`、`Compass` 等分析型符号；
  - 彻底杜绝糖果色药丸标签，统一采用 Apple 6px 微型指示圆点 + 中性中灰文字（`w-1.5 h-1.5 rounded-full`）；
  - 全局维持 95% 中性黑白灰 + 5% 严谨语义强调色；
  - 前端 `npm run build` 成功完成，0 报错 0 警告。
- [x] **Phase 7 契约与接口单元测试套件**：
  - 编写并运行 `tests/test_phase7_contracts.py`（5/5 全部通过）；
  - 全系统单元测试持续 **33/33 项测试 100% 绿灯全绿**。

### Phase 8: 东盟六国 2026 法源、法通网对齐与 FIDIC 双层入库 (Phase 8 ASEAN Knowledge Base)
- [x] **数据库 Schema 向后兼容扩展（11 项新字段 + 风险社区表）**：
  - 在 `lawagent/store/db.py` 中扩展 `SNAPSHOT_DB_SCHEMA`，在 `norms` 表增加 `language_mode`, `lang_original`, `text_original`, `text_en`, `text_zh`, `translation_source`, `norm_category`, `fidic_tier`, `fidic_edition`, `elements_json`, `mandatory_level` 11 个列；
  - 升级 `init_snapshot_db` 逻辑：对既有旧库自动执行 `ALTER TABLE norms ADD COLUMN ...` 无损升级；
  - 新增 `risk_communities` 表，支持跨国工程风险主题子图社区的结构化存储。
- [x] **2026 现行有效东盟六国法源入库与司法部“法通网”权威译本对齐**：
  - 编写并执行 `scripts/build_asean_kb.py`，全量入库 25 条东盟六国 2026 核心成文法规范与先例；
  - **印尼 (`asean_id`)**：入库印尼最高法院 `SEMA No. 3/2023`（推翻无印尼语版本一律无效之机械判例）、建筑服务法 `UU 2/2017` 第 57 条、能矿部 `MEMR 11/2024` 电力本地化率（TKDN）及工业部 2025 新规；
  - **越南 (`asean_vn`)**：入库《2025新建设法》(Law 135/2025/QH15) 第 86.2 条（2026年7月1日施行，正式承认预定损害赔偿 LD，打破旧法 12% 罚金封顶限制）、《第 210/2026/ND-CP 号建设合同法令》第 146 条不可抗力与延误免责；
  - **马来西亚 (`asean_my`)**：入库《CIPAA 2012》第 35 条（背靠背付款 Pay-when-paid 强制无效）与第 13 条快速法定裁决执行；
  - **新加坡 (`asean_sg`)**：入库《SOPA 2004》第 9 条反背靠背条款与高等法院 *BS Mount Sophia / JBE Properties*（以显失公平 Unconscionability 独立标准止付独立保函）；
  - **泰国 (`asean_th`)**：入库《民商法典》(CCC) 承揽编第 587 条与《外商经营法》(FBA 1999) 建筑施工许可准入；
  - **菲律宾 (`asean_ph`)**：入库《菲律宾 PPP 法典》(RA 11966，全面废止旧 BOT 法 RA 7718) 特许权终止补偿条款，及最高法院 *PCAB v. Manila Water* (G.R. No. 217590) 废除外资常规执照股权限制。
- [x] **FIDIC 全量正本双层分级入库 (Tier 1 主动检索 + Tier 2 受控 Diff)**：
  - **Tier 1 (`core_dispute`)**：入库 FIDIC 银皮书/黄皮书/红皮书核心争议条款（Clause 8.4 工期延误 EOT、Clause 20.1 28天索赔失权通知、Clause 4.2 履约担保索兑限制、Clause 14.8 延误付款利息、Clause 17.3 业主风险）；
  - **Tier 2 (`baseline_reference`)**：入库合同文件优先解释次序（Clause 1.5）、法律变更调整（Clause 13.7）等基线比对参考条款；
  - 支持主动自然语言 RAG 与按条号精确受控比对双通道协同。
- [x] **国内涉外国资监管与条约依据红线入库**：
  - 入库国务院国资委《中央企业境外投资监督管理办法》（35 号令）境外重大工程负面清单与穿透核查红线；
  - 入库《中华人民共和国数据安全法》第 36 条（非经中国主管机关批准不得向外国司法或执法机构提供数据与图纸）；
  - 入库《中国-东盟全面经济合作框架协议投资协议》(BIT) 第 6 条（公平公正待遇 FET 与间接征收补偿标准）；
  - 入库中国出口信用保险公司（中信保 Sinosure）海外工程险/特险【30 日出险报损时效与代位求偿保全指引】。
- [x] **3-Layer Legal GraphRAG 拓扑边与 6 大风险主题社区构建**：
  - 构建三层拓扑边（`MANDATORY_OVERRIDES`, `MODIFIES_JUDICIAL_RULE`, `INTERPRETS`, `REQUIRES_PRECONDITION`, `CROSS_REF_CLAUSE`）；
  - 预制 6 大跨国工程风险主题子图社区（保函止付社区、习惯法征地社区、背靠背付款社区、CIPAA/SOPA 快速裁决社区、特许权终止与 BIT 征收社区、新法预定损害赔偿与 LD 社区）。
- [x] **BM25 检索索引全量重构与混合检索精准通道打通**：
  - 知识库切块扩充至 **5,157 Chunks**，全量重建 BM25 词法持久化索引；
  - 扩展 `HybridRetriever` 正则与精确匹配通道（`RE_NORM_EXACT`, `RE_CASE_EXACT`），支持东盟法规编号、FIDIC 条款、BIT 及国资委条规毫秒级精准召回。
- [x] **Phase 8 知识库与图谱单元测试套件**：
  - 编写并运行 `tests/test_phase8_kb.py`（6/6 全部通过）；
  - 全系统单元测试持续 **39/39 项测试 100% 绿灯全绿**。

### Phase 9: 双擎推理流、安全哨兵与“央国企合规体系建设中心”开发
- [x] **国家安全、经济安全与反隐性征收“三层刚性防御机制” (`security_sentinel.py`)**：
  - **Tier 1 (代码级特征引信)**：实现关键基础设施字典扫描（特高压/深水港码头/干线铁路/战略矿产）、世行/亚行跨行联合除名与制裁快照筛查、单方废约与隐性征收引信、数据安全法第36条跨境调证引信及国资委35号令境外投资红线；
  - **Tier 2 (独立安全哨兵评估引擎)**：实现 `SecuritySentinel.evaluate`，自动关联《中国-东盟 BIT 投资协定》第6条（FET 公平公正待遇与征收公允补偿）、《数据安全法》第36条、国资委35号令，并内置中国信保（Sinosure）海外投资与特险【30 日出险报损时效与代位求偿保全指引】；
  - **工程专属构成要件与传导审查算子**：
    - `evaluate_tkdn_compliance`：印尼光伏/电网 TKDN 本地化率构成要件审查（对齐 MEMR 11/2024 与 Sucofindo 认证）；
    - `evaluate_eot_delay_claim`：FIDIC 银皮书 Clause 8.4 工期延误 EOT 构成要件与 Clause 20.1 28天索赔时效反失权审查；
    - `evaluate_interface_transmission`：投建营一体化上游 PPA/特许经营协议与下游 EPC 接口传导风险审查（含马来 CIPAA 第35条背靠背绝对无效）；
  - **Tier 3 (质量门禁 Critic V12 一票否决熔断)**：实现 `check_critic_v12_security_gate`，若触发 CRITICAL/HIGH 风险但正文未生成有效反制对冲措施则强制熔断，并与 `run_critic_checks` 无缝整合。
- [x] **东盟专属入口前置检查清单 (`checks.py`)**：
  - 实现 `calibrate_asean_entry_checks`，自适应校准生成东盟 5 项刚性前置合规审查清单（印尼 SEMA 3/2023 语言要求与有效性抗辩、BUJKA/PCAB/CIDB/BCA 施工牌照准入合规、马来 CIPAA 35 / 新加坡 SOPA 9 反背靠背付款强行法、国资委35号令重大境外投资备案）。
- [x] **双模板 Word (DOCX) 导出引擎与 REST 端点 (`export.py`, `cases.py`)**：
  - 升级 `generate_case_docx` 接入东盟多语种法条对照、FIDIC 条款分级及【国家安全、海外投资经济安全与反隐性征收专项预警】专章（含信保 30 日出险报损指南与法务核验勾选清单）；
  - 新增 `generate_compliance_handbook_docx`，支持按国别与组合业态导出《涉外工程专项合规指引手册 (DOCX)》（覆盖五阶段全生命周期、国资委“三道防线”角色审查清单与示范防御反制条款）；
  - 新增 `GET /cases/{case_id}/export/handbook/docx` 与 `GET /compliance/handbook/docx` 导出端点。
- [x] **前端【央国企合规体系建设中心】四大核心模块 (`FrontEnd/src/components/compliance/`)**：
  - `CaseReferenceHub.tsx`：建设工程典型参考案例库，独创“五维合规复盘卡 (5D Case Review Card)”数据结构（交易架构、暴雷根因、法源锚点、示范防御条款、一键沙盘推演），支持按 6 国 × 4 业态 × 8 风险环节多维检索；
  - `ComplianceGuidelineCenter.tsx`：全周期合规指引引擎，提供五阶段导航（立项尽调 $\rightarrow$ 招投标联营 $\rightarrow$ 合同签署 $\rightarrow$ 现场履约 $\rightarrow$ 移交争议）、国资委“三道防线”角色视角切换及一键导出 Word 手册；
  - `RiskPromptDashboard.tsx`：场景化风险提示与立法预警雷达，构建东盟 6 国 × 12 风险域矩阵（极高危/高危/关注/常规可控警示卡与 Do's & Don'ts 清单）及四大重大修法/司法转向实时提示；
  - `ASEANComparisonMatrix.tsx`：东盟六国涉外基建与并购实务横向对比矩阵（法系特征、语种模式、2026有效法典、施工准入、语言效力、背靠背效力、保函止付标准）；
  - `ComplianceCenterView.tsx`：合规体系中心多功能选项卡统一容器视图。
- [x] **前端核心组件升级与交互优化**：
  - `LawDrawer.tsx`：升级支持双语（新/马/菲）与三语（印/越/泰）自适应对照抽屉，挂载司法部“法通”网 (`lexcom.12348.gov.cn`) 权威中文译本核验标识与 FIDIC Tier 1/2 标签；
  - `InteractiveCitationGraph.tsx`：重构为四列分层因果穿透图谱（案件事实与证据 $\rightarrow$ 争议焦点与要件 $\rightarrow$ 命中法条与 FIDIC 基线 $\rightarrow$ 裁判先例与合规对策），支持按争点一键过滤；
  - `TopBar.tsx` & `Sidebar.tsx`：顶部导航栏与侧边栏支持【个案查明工作台】与【央国企合规体系中心】双视角无缝切换；
  - 严格遵循《前端设计原则.md》（无 Scale/Gavel 冗余图标，极简科技感，生产打包 `npm run build` 0 警告 0 错误）。
- [x] **Phase 9 单元测试套件闭环**：
  - 编写并运行 `tests/test_phase9_sentinel.py`（6/6 全部通过）；
  - 全系统 8 个测试模块持续 **45/45 项测试 100% 绿灯全绿**。

### Phase 10: 东盟工程实战案例播种、端到端集成测试、双模板 DOCX 报告验证与 E1-E9 评测验收 (Phase 10 E2E & Production Delivery)
- [x] **东盟四大经典央企实战示范案例播种入库 (`scripts/seed_asean_cases.py`, `main.py`)**：
  - 实现标准播种脚本并在应用启动生命周期中自动执行，播种至 `data/state.sqlite`：
    - **C101 (印尼爪哇光伏电网 EPC+O&M)**：印尼能矿部 MEMR 11/2024 电力 TKDN 40% 本地化率合规审查、SEMA 3/2023 语言抗辩反制、国企买方单方废约与间接征收（China-ID BIT 第4条）及中信保 30 日出险报损指引；
    - **C102 (越南北南高速公路 PPP 投资项目)**：2025 新建设法第 86.2 条预定损害赔偿（LD）效力承认、旧法 12% 封顶突破、第 210/2026/ND-CP 号法令不可抗力免责与 FIDIC 银皮书 Clause 8.4 工期顺延及 Clause 20.1 28天索赔时效反失权；
    - **C103 (马来西亚新山超大规模数据中心 PPA-EPC 接口案)**：投建营一体化上游 PPA 与下游 EPC 接口传导、CIPAA 2012 第35条背靠背付款法定自始无效、FIDIC Clause 4.2 独立履约保函见索即付防欺诈止付（Fraud Exception）；
    - **C104 (菲律宾新马尼拉水务特许经营与 EPC 联营体)**：RA 11966 新 PPP 法典第18条特许权提前终止补偿、PCAB v. Manila Water 牌照外资限制废止、股权代持（Nominee Arrangement）合规自查与国资委 35 号令负面清单。
  - 所有示范案例均挂载完整的五维复盘卡（5D Case Review Card）数据结构（`five_d_review`），并配置专属 `security_alerts`、事实清单、证据链及四态涵摄结论。
- [x] **东盟专属端到端架构集成测试套件 (`tests/test_asean_architecture.py`)**：
  - `test_asean_demonstration_cases_integrity`：验证 C101~C104 示范案例各字段、业态、五维数据及安全警报的完整性；
  - `test_stage_transition_roundtrip`：验证投前合规与履约争议跨阶段往返流转、母子案关联链路及关键元数据继承；
  - `test_asean_dual_export_docx_validation`：验证个案裁判报告与涉外工程合规手册双 DOCX 文档流式导出，校验段落与表格文本完整性；
  - `test_critic_v12_security_gate_full_closure`：验证 Critic V12 安全门禁的拦截熔断（未提供对冲时拦截）与豁免闭环（包含中信保/BIT/对冲措施时放行）；
  - `test_end_to_end_asean_workflow_simulation`：仿真东盟全流程推理与状态流转；
  - 测试结果：**5/5 全部通过**。
- [x] **全系统 10 大测试模块 50/50 单元与集成测试 100% 全绿**：
  - `test_phase1.py` (5/5), `test_phase2.py` (5/5), `test_phase3.py` (5/5), `test_phase4.py` (8/8 -> 9/9), `test_phase7_contracts.py` (5/5), `test_phase8_kb.py` (6/6), `test_phase9_sentinel.py` (6/6), `test_us_architecture.py` (4/4), `test_asean_architecture.py` (5/5)；
  - 全量 50 项测试持续 100% 绿灯无回归！
- [x] **E1-E9 自动化基准评测套件验收 (`eval/run.py`)**：
  - 对齐东盟 5 大黄金评测题（`ID:SEMA_3_2023`, `MY:CIPAA_2012:Sec35`, `FIDIC:Silver_1999:Clause_8.4`, `VN:Law_135_2025:Art86.2`, `TREATY:CN_ID_BIT_1992:Art4`）；
  - 评测指标结果：
    - **Norm Recall@10**：**100.0%** (1.0)
    - **MRR**：**1.0000**
    - **幻觉计数**：**0** (一票否决门禁通过)
    - **事实溯源错误**：**0** (一票否决门禁通过)
    - **越权预测率**：**0.0%** (一票否决门禁通过)
    - **要件覆盖率**：**100.0%** (优于 >= 75% 阈值)
    - **验收结论**：**`acceptance_verdict: PASSED`**。

---

## 5. 系统启动与运行指引

### 5.1 启动后端 FastAPI 服务
```bash
# 确保系统环境变量 OPENAI_API_KEY 已设置
uvicorn lawagent.api.main:app --host 127.0.0.1 --port 8000 --reload
```
- 后端服务接口文档：`http://127.0.0.1:8000/docs`
- 健康检查：`http://127.0.0.1:8000/api/health`

### 5.2 启动前端应用
```bash
cd FrontEnd
npm run dev
```
- 前端访问地址：`http://localhost:3000`
- 前端请求将自动经 Vite 代理转发至 `http://127.0.0.1:8000/api`。

### 5.3 运行自动化测试与评测套件
```bash
# 运行全系统全部 50 项单元与集成测试
python -m pytest tests/ -v

# 运行 E1-E9 基准评测套件
python -m eval.run
```

---

## 6. 全面代码审查与优化记录 (Code Review & Optimization)

- [x] **白屏故障诊断与彻底修复 (React 19 Hook 顺序违规)**：
  - 将所有 Hook（`useMemo`, `useEffect`）重构至组件函数最顶层无条件执行，使用默认空结构防御；在 `FrontEnd/src/main.tsx` 引入全局 `ErrorBoundary` 组件，防止任何未捕获异常导致全屏空白；补充 `IntersectionObserver` 数据挂载监听依赖。
- [x] **前端 Mock 数据清查**：已彻底物理删除 `FrontEnd/src/api/mockData.ts`，全量组件均已切入直连后端真实 REST/SSE。
- [x] **Word DOCX 报告真实流式下载闭环**：在 `client.ts` 新增 `downloadBlob` 二进制下载工具，前端 `ReportReviewView.tsx` 直连后端 `GET /api/cases/{case_id}/export/docx` 流式下载端点，直接下载最高院《涉外民事关系法律适用法解释（二）》标准格式 Word 文档；新增合规手册流式下载端点 `GET /api/compliance/handbook/docx`。
- [x] **CrossEncoder 输入截断治理**：在 `lawagent/store/rerank.py` 中，对检索 Query 截断 $\le 256$ 字符、候选条文截断 $\le 1024$ 字符，模型预测增加 `max_length=512` 限制，消除输入爆炸风险，确保显存稳定。
- [x] **工作台 SSE 实时流广播与自动挂接**：在 `lawAgentApi.ts` 实现 `subscribeEvents`，并在 `AppContext.tsx` 中增加对 `running` 状态案件的 SSE 自动订阅（流式接收 `state_update` 与 `done` 事件并同步前端状态）。
- [x] **测试数据隔离与示范案件库丰富**：
  - 在 `test_phase4.py` 中引入测试用例自清理机制（`DELETE /api/cases/{case_id}`），杜绝后续跑测污染正式数据库；
  - 播种 3 起经典代表性涉德示范案件（C001, C002, C003）；
  - 播种 4 起东盟央企基建示范案例（C101 印尼光伏, C102 越南高速, C103 马来数据中心, C104 菲律宾水务），实现 5D 深度复盘与一键沙盘推演。
- [x] **LangGraph 异步工作流 Checkpointer 修复**：
  - 将 `LawWorkflowRunner` 默认检查点设置为 `MemorySaver`（全异步兼容），根除了 `SqliteSaver.aget_tuple` 抛出 `NotImplementedError` 导致的后台异步工作流异常退出问题。
- [x] **工程内部编号与设计描述彻底清理**：
  - 彻底移除了前端界面中残留的设计方案功能编号（如 F31、F30、F16、F17、F25、F04、B1~B6），重构为专业极简编号（01~06）；
  - 清理了“依据第4.7节与第6.2节守护规则自动拦截”等工程设计口吻文字，重构为符合涉外法官与律师审阅习惯的“依据涉外法律客观中立规则与防线机制自动拦截”。
- [x] **全景案件总结与法律研判卡片**：
  - 在“案情深度分析”页面最顶端挂载 `<CaseExecutiveSummaryCard />`，支持【司法端（法官审理指引）】、【实务端（律师实务备忘）】、【公共端（商事合规与和解）】三重视角切换；涵盖涉外法律关系定性、争议焦点逻辑脉络、构成要件涵摄定性、核心法律风险与出庭/审理建议。
- [x] **Agent 工作台协同流水线与 Copilot 助手**：
  - 步进卡片时间轴完整展示专业 Agent 协同流水线，呈现使用的模型配置、输入输出摘要、耗时及 V1~V12 质检防线标签；
  - 右侧法律 Copilot 智能追问助手具备对话上下文感知能力，支持中立法理研判与对抗式红方反击演练模式无缝切换，并支持一键反哺成果至案件底稿。
- [x] **前端设计原则落地与视觉纯净性**：
  - 严格贯彻《前端设计原则.md》：彻底清除 `Scale` 与 `Gavel` 拟物化图标；标签统一使用 Apple 6px 微型指示圆点；色调克制严谨；
  - 前端执行 `npm run build` 成功完成，0 报错 0 警告。
- [x] **全套 50 项自动化测试持续 100% 绿灯，E1-E9 评测验收通过**：涵盖 Phase 1 至 Phase 10 全部 50 项单元与集成测试用例，全量通过，向后兼容性 100%。

---

## 7. 彻底剥离德美法域、纯净聚焦东盟基建工程与出海央国企合规防线总结 (Step 1 - Step 5 完成记录)

系统根据出海基建央企/国企在东盟 6 国（印尼、越南、马来西亚、新加坡、泰国、菲律宾）的真实业务痛点，彻底放弃宽泛兼容德美法域导致的数据与体验妥协，按 5 大步骤全面完成纯净化改造：

- [x] **Step 1: 核心数据模型、法域注册中心与前端契约纯净化**
  - JurisdictionRegistry 彻底注销 de_federal 与 us_commercial，仅保留东盟 6 国；
  - 	ypes.py 与前端 lawAgent.ts 契约全面切换至东盟基建场景（FIDIC Silver/Yellow/Red 双层条款、中国-东盟 BIT 投资协定、国资委 35 号令、数据安全法第 36 条）。
- [x] **Step 2: 后端推理流水线与分析引擎纯净化**
  - 物理删除 lawagent/flow/us_admissibility_calibrator.py 与 lawagent/integrations/courtlistener.py；
  - lawagent/flow/nodes.py、checks.py、matcher.py、critic.py 全面适配东盟强行法（语言效力、外资资质、背靠背付款、保函止付）；
  - lawagent/flow/strategist.py 重构为 4 大东盟专属策略体系（EPC 工期延误与 28 日除斥通知、保函见索即付与 BS Mount Sophia 显失公平止付、PPP 特许权撤销与 BIT 间接征收、CIPAA/SOPA 快速裁决）；
  - lawagent/api/export.py 严格锚定最高人民法院《涉外民事关系法律适用法》解释（二）及国务院国资委 35 号令合规交底要求。
- [x] **Step 3: 知识库与数据库纯净化**
  - 运行 scripts/build_pure_asean_kb.py，物理重构不可变快照库 law.sqlite 与索引缓存；
  - 录入 25 条东盟 6 国 2026 现行有效法源、FIDIC 核心条款、BIT 投资协定及国资监管条文；
  - 录入 7 篇金标准东盟真实裁判文书（BS Mount Sophia、JBE Properties、SEMA 3/2023、Manila Water、CIPAA Bauer 等）；
  - 物理删除 kb/de_federal/ 与 scripts/enrich_legal_knowledge.py，新建 kb/asean/（glossary.csv, 	imepoints.yaml, commentary.json）；
  - 数据库与向量/BM25 词表中历史德美条目完全清零（0 German/US norms, 0 German/US cases）。
- [x] **Step 4: 前端纯净化与视觉设计原则校准**
  - 物理移除废弃弹窗 CisgGateModal.tsx；
  - 全局代码扫描确认前端 0 处德美法域残留（us_commercial|de_federal|UCC|BGB|HGB|isUS 检出项为 0）；
  - 全局矢量图标扫描确认 0 处 Scale / Gavel 陈旧法槌天平图标，100% 对齐《前端设计原则.md》（6px 微圆点、95% 中性黑白灰极简克制着色、Progressive Disclosure 渐进展开）；
  - 前端编译构建 
pm run build 耗时 4.92s，0 错误，0 警告。
- [x] **Step 5: 测试套件更新与端到端基准验收**
  - 物理删除废弃德美测试文件：git rm tests/test_phase1.py tests/test_phase2.py tests/test_phase3.py tests/test_phase4.py tests/test_us_architecture.py；
  - 编写全新的端到端基准验收套件 	ests/test_asean_e2e.py（涵盖 DB 纯净度、法域注册、API 健康与案件详情、混合检索召回、证据材料核验、专家会商流转、追问闭环、DOCX 报告合规导出 8 大验收项）；
  - 全系统自动化测试执行：	ests/test_asean_architecture.py (5), 	ests/test_asean_e2e.py (8), 	ests/test_phase7_contracts.py (5), 	ests/test_phase8_kb.py (6), 	ests/test_phase9_sentinel.py (6)，**合计 30/30 全部通过，100% 绿灯（耗时 14.41s）**！

