# 域外法查明辅助应用 (OverseasLawAssist) 开发状态与进度追踪

> **当前版本**：v3.1 (Master Full-Stack Refactoring & Audit Closure Implementation)  
> **更新时间**：2026-10-23  
> **系统状态**：已全面落实《重构方案.md》与《重构审查报告.md》提出的全部 P0/P1/P2 遗漏点与进一步优化项。系统全面对齐 Apple HIG × Fluent 2 视觉质感与纯净东盟业务逻辑；合规中心实现国别速查副驾坞联动与 3 行熔断；沙盘推演具备 350ms 智能防抖实时更新、基准对比徽章与一键重置；图谱法条直出法源双语精读坞与权威背书；建案与核验支持 .docx/.txt 索赔函拖拽解析与 Redline 增删对比；后端工作流与节点全面补齐战术卡自动生成与文件解析接口。后端 38/38 项测试 100% 绿灯通过，前端 Vite 生产构建 0 错误 0 警告 (100% Production Ready & Verified)。

---

## 1. 架构定位与纯净东盟业务全景

本系统定位于**中国出海基建央企/国企在东盟 6 国（印度尼西亚、越南、马来西亚、新加坡、泰国、菲律宾）建设工程与海外投资（EPC/PPP/特许经营/跨境并购/联营体）法律风险防范、合同条款体检、合规指引与争议推演专业工作台**。

```
[用户层 / 前端交互工作台 (React 19 + TypeScript + Apple Bento 网格 + Mica/Acrylic 光学材质)]
   ├── 三层业务空间架构：
   │    ├── 80% 专案深度研判舱 (Case Cockpit · 活跃案卷树 · 双模四切面矩阵)
   │    ├── 15% 轻量化独立工具箱 (Toolbox · 合同红线扫描 · 法典检索 · 专家避冲) ──> [+挂载至案卷]
   │    └── 5%  东盟合规知识底座 (Compliance Base · 五阶段体检 · 6x12排雷矩阵 · 5D案例)
   ├── 单实例多模态右侧副驾坞 (UnifiedRightDock: 法源双语精读 / 案卷AI副驾 / 属地排雷速查)
   └── 全局聚焦命令舱 (CommandPaletteModal: Cmd/Ctrl + K 秒级检索与模式跳转)
                         │
        (Vite Proxy: /api -> http://127.0.0.1:8000)
                         │
[FastAPI 服务层 lawagent.api] ── [REST API / SSE 事件流 / 智能要素抽提 / 双模沙盘推演 / 成果挂载 / DOCX 导出]
                         │
[LangGraph 核心推理状态图 StateGraph(CaseState)]
   S1 Extract ─> S2 Precheck ─> S3 Decompose ─> S4 Researcher ─> S5 Matcher
    └── S6 Strategist ─> S7 Drafter ─> Critic (V1-V12 哨兵一票否决) ─> S8 Review ─> S9 Export
                         │
[多法域注册中心 JurisdictionRegistry (纯净东盟 6 国 + FIDIC)]
   ├── asean_id: 印度尼西亚 (建筑法UU 2/2017第57条, SEMA 3/2023双语令, MEMR 11/2024 TKDN豁免, 民法典第1338条)
   ├── asean_vn: 越南 (2025新建设法第86.2条LD预定赔偿, 210/2026建设合同法令, PPP法第64/2020号)
   ├── asean_my: 马来西亚 (CIPAA 2012 第35条反背靠背, 建筑工业发展局法 Act 520 CIDB)
   ├── asean_sg: 新加坡 (SOPA 2004 第9条反背靠背, BS Mount Sophia / JBE 显失公平保函止付)
   ├── asean_th: 泰国 (民商法典第596条违约金酌减, 外商经营法 FBA 1999 附件三, BOI 优惠政策)
   └── asean_ph: 菲律宾 (2023年PPP法典 RA 11966, PCAB 资质准入 RA 4566, Manila Water 案平等待遇)
                         │
[双 SQLite 数据库存储架构 (零欧美历史残留)]
   ├── 快照库 law.sqlite (不可变, 31 条成文法规范与条约, 7 篇金标准判例, 52 个切块, 司法部法通网三语对照)
   └── 运行库 state.sqlite (读写 WAL 模式, C101~C104 央企示范案, 案卷成果挂载 attached_artifacts, 战术指引 tactical_guidance)
```

---

## 2. 核心重构模块与业务场景落地一览

| 模块分区 | 核心功能与工作台支持 | 后端实现与专项算子 | 交付与展示产物 |
| :--- | :--- | :--- | :--- |
| **首屏极速双轨制** (`HomeLandingView`) | • 轨道 A (60%): 30 秒合同强行法红线扫描，三联式诊断（效力判定 $\to$ 裁决后果 $\to$ 示范条款），支持一键升级专案<br>• 轨道 B (40%): 粘贴邮件/索赔函极速建案与 C101~C104 标杆卷精密卡片 | [`POST /api/cases/extract-intake`](file:///C:/Downloads/OverseasLawAssist/lawagent/api/routes/cases.py#L1461)<br>确定性正则规则引擎与多国法典特征提取 | • [`HomeLandingView.tsx`](file:///C:/Downloads/OverseasLawAssist/FrontEnd/src/components/home/HomeLandingView.tsx)<br>• 极速诊断卡与复制示范条款<br>• 标杆项目快速进入通道 |
| **智能要素抽提建案舱** (`CaseEntryModal`) | • 粘贴英文/中文往来邮件或索赔函，2 秒内自动提炼项目名称、东道国、准据法、阶段、业态、事实摘要与工程参数<br>• 支持从合规未达标项、六国比选矩阵及红线体检带参数预填孵化 | [`POST /api/cases/extract-intake`](file:///C:/Downloads/OverseasLawAssist/lawagent/api/routes/cases.py#L1461)<br>提取 `declared_tkdn_pct`, `delay_days`, `notice_days`, `sinosure_notice_days` 等 | • [`CaseEntryModal.tsx`](file:///C:/Downloads/OverseasLawAssist/FrontEnd/src/components/cases/CaseEntryModal.tsx)<br>• 高亮脉冲自动填单交互<br>• 多国比选立项闭环 |
| **专案深度研判舱（双模四切面）** (`CaseAnalysisView`) | • **切面 1（决策全景）**：三维定性遥测（实体法支持度/程序抗辩敞口/反制阻断预期）+ If-Then 矩阵 + 准据法脱钩穿透卡<br>• **切面 2（要件四态涵摄）**：主从分栏，要件四态胶囊比对 (`satisfied`, `partially_satisfied`, `missing`, `unclear`)<br>• **切面 3（工程沙盘与攻防工坊）**：左侧带法定刻度（28d失权、40%TKDN、30d信保）滑轨 + 右侧联动刷新中英双语谈判反驳话术卡与紧急发函清单<br>• **切面 4（法源图谱与公文交付）**：Critic 门禁遥测 + 3-Layer 图谱 + 双语意见书实时公文预览与一键 Word 导出 | [`POST /api/cases/{id}/simulate-engineering`](file:///C:/Downloads/OverseasLawAssist/lawagent/api/routes/cases.py#L1337)<br>生成并持久化 `tactical_guidance`<br>[`lawagent/flow/security_sentinel.py`](file:///C:/Downloads/OverseasLawAssist/lawagent/flow/security_sentinel.py)<br>投前合规推演与履约争议推演双模分流 | • [`CaseAnalysisView.tsx`](file:///C:/Downloads/OverseasLawAssist/FrontEnd/src/components/analysis/CaseAnalysisView.tsx)<br>• 键盘快捷键 `1/2/3/4` 瞬切<br>• 防抖与竞态锁支持 60fps 拖拽<br>• 最高法标准 Word 报告下载 |
| **轻量化独立工具箱与挂载闭环** (Toolbox) | • **合同红线核验仪**：合同红线扫描 vs 外律意见书验真，新增 `[+ 挂载体检记录至案卷]` 与 `[以此条款新建专案]`<br>• **六国法典检索库**：空状态展示基准法源导航目录，前置权威认证背书，新增 `[+ 引用至案卷]`<br>• **专家协同枢纽**：东盟 6 国在册仲裁员与避冲排查，新增 `[+ 挂载会商记录至案卷]` | [`POST /api/cases/{id}/attach-artifact`](file:///C:/Downloads/OverseasLawAssist/lawagent/api/routes/cases.py#L1607)<br>[`DELETE /api/cases/{id}/attach-artifact/{aid}`](file:///C:/Downloads/OverseasLawAssist/lawagent/api/routes/cases.py#L1638)<br>持久化至 `state.sqlite` 之 `attached_artifacts` | • [`MaterialVerificationView.tsx`](file:///C:/Downloads/OverseasLawAssist/FrontEnd/src/components/verification/MaterialVerificationView.tsx)<br>• [`NormSearchEngineView.tsx`](file:///C:/Downloads/OverseasLawAssist/FrontEnd/src/components/search/NormSearchEngineView.tsx)<br>• [`ExpertConsultsView.tsx`](file:///C:/Downloads/OverseasLawAssist/FrontEnd/src/components/consults/ExpertConsultsView.tsx)<br>• DOCX 报告自动生成专项附表 |
| **合规排雷知识底座** (`ComplianceCenter`) | • 五阶段 × 三道防线在线体检打分持久化至 `localStorage`，带一键重置<br>• 检出瑕疵项右侧动态浮现 `[针对此缺口发起专案推演]`<br>• 6×12 风险排雷矩阵与 5D 典型案例卡遵守 3 行文本熔断法则，点击滑出副驾坞模态 3 展开精读 | [`ComplianceGuidelineCenter.tsx`](file:///C:/Downloads/OverseasLawAssist/FrontEnd/src/components/compliance/ComplianceGuidelineCenter.tsx)<br>[`RiskPromptDashboard.tsx`](file:///C:/Downloads/OverseasLawAssist/FrontEnd/src/components/compliance/RiskPromptDashboard.tsx) | • 合规健康度仪表板 (0-100分)<br>• 央国企合规指引手册 (.docx)<br>• 属地排雷速查手册抽屉 |
| **单实例多模态统一副驾坞** (`UnifiedRightDock`) | • 固定停靠右侧 (`440px`)，支持快捷键 `Cmd/Ctrl + B` 开关<br>• 顶部 3 模态切换：`[法源双语精读]`、`[案卷 AI 副驾 & S1~S9 流水线]`、`[属地排雷速查]`<br>• 彻底取代底栏常驻黑条与多抽屉叠罗汉 | 整合原 `LawDrawer`、`AgentWorkspaceView`、`FloatingOmniBar` 与国别 Playbook | • [`UnifiedRightDock.tsx`](file:///C:/Downloads/OverseasLawAssist/FrontEnd/src/components/common/UnifiedRightDock.tsx)<br>• Apple Spring 物理抽屉动效 |
| **全局聚焦命令舱** (`CommandPaletteModal`) | • 快捷键 `Cmd/Ctrl + K` 唤出<br>• 支持全案卷快速跳转、法条检索、投前/履约阶段秒切、轻量工具呼出 | 全局命令分发机制 | • [`CommandPaletteModal.tsx`](file:///C:/Downloads/OverseasLawAssist/FrontEnd/src/components/common/CommandPaletteModal.tsx)<br>• macOS Spotlight / Linear 交互体验 |

---

## 3. 当前运行环境与技术栈配置

- **操作系统**：Windows (x86_64)
- **后端环境**：Python 3.10.6, FastAPI, LangGraph, Pydantic v2
- **GPU 算力**：NVIDIA GeForce RTX 2070 SUPER (8GB VRAM, CUDA 12.8, BGE-M3 向量加速)
- **前端环境**：Node v24.12.0, Vite 8, React 19, TypeScript
- **大模型配置 (DashScope 兼容协议)**：
  - **Base URL**：`https://dashscope.aliyuncs.com/compatible-mode/v1`
  - **主推理模型**：`deepseek-v4.1-flash`（高吞吐流式响应，网络受限时由本地规则引擎自适应兜底）
  - **裁判校验模型**：`deepseek-v4-pro-0813`（专职执行 V1-V12 全套质量门禁与一票否决拦截）
- **知识库规格 (Pure ASEAN & FIDIC)**：
  - **成文法与条约**：31 条东盟 6 国 2026 现行有效法典、FIDIC 核心条款、中国-东盟 BIT、国资委 35 号令、数据安全法第 36 条；
  - **司法裁判判例**：7 篇金标准裁判文书（*BS Mount Sophia*, *JBE Properties*, *SEMA 3/2023*, *Manila Water*, *CIPAA Bauer* 等）；
  - **语料切块数**：52 个语义分块（Chunks）；
  - **索引持久化**：`bm25.pkl` 词法索引与 `faiss.index` 密集向量索引双轨部署；
  - **统一构建源**：`scripts/build_asean_kb.py` 与 `scripts/build_pure_asean_kb.py` 完全对齐统一。
- **服务端口**：
  - 后端服务：`http://127.0.0.1:8000` (API Docs: `/docs`)
  - 前端服务：`http://localhost:3000`

---

## 4. 全量开发里程碑演进记录

### Phase 1: 东盟多法域注册与核心抽象
- [x] 多法域注册中心注销历史欧美法域，全面激活东盟 6 国（`asean_id`, `asean_vn`, `asean_my`, `asean_sg`, `asean_th`, `asean_ph`）；
- [x] 在 [`lawagent/core/types.py`](file:///C:/Downloads/OverseasLawAssist/lawagent/core/types.py) 中定义生命周期阶段（`LifecycleStage`）、工程业态（`ProjectArchetype`）、`SecurityAlertItem` 与结构化参数 [`EngineeringParams`](file:///C:/Downloads/OverseasLawAssist/lawagent/core/types.py)；
- [x] 实现跨阶段流转端点 `POST /api/cases/{case_id}/transition-stage`，支持母子案追踪与参数继承。

### Phase 2: 东盟法律知识库与 GraphRAG 构建
- [x] 采集入库东盟 6 国 2026 现行成文法、司法解释（印尼 SEMA 3/2023、越南 2025 新建设法、马来 CIPAA 2012、新加坡 SOPA 2004、菲律宾 RA 11966 PPP 法典、泰国 FBA 1999）；
- [x] 入库 FIDIC 银/黄/红多版本核心条款（Clause 20.1/20.2 索赔通知、8.4/8.5 EOT、4.2 保函、13.7 调价），实现条号跨版本等效降级检索机制（[`lawagent/store/snapshots.py`](file:///C:/Downloads/OverseasLawAssist/lawagent/store/snapshots.py)）；
- [x] 预建 3 层拓扑图谱（`MANDATORY_OVERRIDES`, `MODIFIES_JUDICIAL_RULE`, `REQUIRES_PRECONDITION`）与 6 大风险主题子图；
- [x] 完成 BGE-M3 向量嵌入与 GPU FAISS 稠密向量索引构建。

### Phase 3: 多 Agent 协同流与安全哨兵系统
- [x] 编排 LangGraph S1~S9 状态流转图，实现全流程确定性推理与断点恢复调度器；
- [x] 在 [`lawagent/flow/security_sentinel.py`](file:///C:/Downloads/OverseasLawAssist/lawagent/flow/security_sentinel.py) 中实现三层刚性安全哨兵（Tier 1 确定性引信 + Tier 2 独立哨兵评估 + Tier 3 Critic V12 一票否决）；
- [x] 实现工程专属审查算子：`evaluate_tkdn_compliance`（本地化率合规）、`evaluate_eot_delay_claim`（工期索赔 28 天通知时效）、`evaluate_interface_transmission`（接口传导与背靠背有效性）；
- [x] 在 [`lawagent/flow/strategist.py`](file:///C:/Downloads/OverseasLawAssist/lawagent/flow/strategist.py) 中实现投前合规推演与履约索赔推演双模分流。

### Phase 4: 前端核心工作台与四大切面升级
- [x] **合同条款强行法体检工作台** ([`MaterialVerificationView.tsx`](file:///C:/Downloads/OverseasLawAssist/FrontEnd/src/components/verification/MaterialVerificationView.tsx))：支持“条款体检 vs 意见书引证”双模，提供典型风险范本填入与示范条款一键复制；
- [x] **深度分析与交互式沙盘** ([`CaseAnalysisView.tsx`](file:///C:/Downloads/OverseasLawAssist/FrontEnd/src/components/analysis/CaseAnalysisView.tsx))：投前合规 vs 履约争议双模视图，拖动滑块实时调用后端 `/simulate-engineering` 并动态刷新；
- [x] **全周期合规自测打分中心** ([`ComplianceGuidelineCenter.tsx`](file:///C:/Downloads/OverseasLawAssist/FrontEnd/src/components/compliance/ComplianceGuidelineCenter.tsx))：实时计算健康度指数（0-100分），未达标项一键生成专项案卷启动推演；
- [x] **国别风险提示看板** ([`RiskPromptDashboard.tsx`](file:///C:/Downloads/OverseasLawAssist/FrontEnd/src/components/compliance/RiskPromptDashboard.tsx))：6国 × 12风险域矩阵，风险卡直通专项审查沙盘；
- [x] **双语查明报告呈报端** ([`ReportReviewView.tsx`](file:///C:/Downloads/OverseasLawAssist/FrontEnd/src/components/review/ReportReviewView.tsx))：区分投前审查意见书与涉外工程查明报告，自适应生成呈报标题与双模 Word 导出。

### Phase 5: 准据法脱钩冲突与工业级材质奠基 (v2.2)
- [x] **准据法与工程所在国脱钩冲突检测 (Lex Loci Solutionis Override)**：`CaseMeta` 拆分东道国与准据法，自动判定强行法穿透适用冲突；
- [x] **三大高价值算子实装**：中信保 30 日出险报损时效算子、菲律宾 PCAB 资质准入算子、泰国 FBA 附件三工程限制算子；
- [x] **东盟 6 国 Local Counsel 专家名录与避冲排查**：SIAC/BANI/AIAC/VIAC/TAI/CIAC 全面覆盖，会商记录安全释放。

### Phase 6: 全栈大师级重构与业务闭环终极落地 (v3.0 - Current)
- [x] **空间架构与去“AI 模板味”视觉革命**：
  1. 侧边栏彻底收敛为「80% 专案研判舱（带活跃案卷树与母子血缘）- 15% 独立工具箱 - 5% 合规底座」三层业务漏斗；
  2. 顶栏实现「专案研判舱（带灵动岛 S1~S9 遥测胶囊与双模切换）」与「独立公共工具（带挂载目标案卷选择器）」双态自适应；
  3. 彻底下线底部遮挡黑条 `FloatingOmniBar.tsx` 与全屏阻塞弹窗 `CasePipelineAnimationModal.tsx`，新建单实例多模态右侧副驾坞 [`UnifiedRightDock.tsx`](file:///C:/Downloads/OverseasLawAssist/FrontEnd/src/components/common/UnifiedRightDock.tsx) 与全局命令舱 [`CommandPaletteModal.tsx`](file:///C:/Downloads/OverseasLawAssist/FrontEnd/src/components/common/CommandPaletteModal.tsx)；
  4. 严格执行 **3 行文本熔断法则**，全面采用非对称 Bento 光学网格、光学呼吸圆点（`.glow-dot-*`）与精密等宽数字（`tabular-nums`）。
- [x] **首屏双轨制与极速要素抽提**：
  1. [`HomeLandingView.tsx`](file:///C:/Downloads/OverseasLawAssist/FrontEnd/src/components/home/HomeLandingView.tsx) 60% 轨道 A（30秒红线扫描仪）+ 40% 轨道 B（标杆案卷与邮件建案）；
  2. 实现 `POST /api/cases/extract-intake` 智能要素抽提，粘贴原始索赔邮件 2 秒自动提炼建案字段与数值工程参数；
- [x] **专案深度研判舱双模四切面矩阵**：
  1. 严格落实司法中立防线（V8 Anti-Predictive Guardrail），彻底根除单一百分比伪胜诉率，全面实装三维定性结论遥测带与 If-Then 假定条件推演矩阵；
  2. 切面 1~4 全面自适应投前准入模式与履约争议模式；
  3. 沙盘滑轨绘制法定红线刻度锚点（`28d 失权`、`30d 信保`、`40% TKDN`），滑块越过红线实时联动右侧中英双语谈判反驳话术卡与紧急发函清单，并具备弹簧呼吸动效与竞态防抖锁；
- [x] **轻量工具箱至案卷真实挂载闭环**：
  1. 实现 `POST /api/cases/{id}/attach-artifact` 与 `DELETE` 接口，合同红线体检、重点法条引证、专家避冲记录一键沉淀至案卷 SQLite 状态；
  2. 修复法典检索库“零状态显示 32 条结果”痛点，未输入时展示《权威基准法源导航目录》；
  3. 合规体检表打分状态通过 `localStorage` 安全持久化，未达标项直通带参数立项；
- [x] **DOCX 导出引擎全量对齐**：
  1. Word 报告同步输出三维定性结论表、If-Then 矩阵、Lex Loci 穿透专章、沙盘定格参数与动态双语谈判话术；
  2. 报告末尾自动生成《附件：专案挂载之合同条款红线体检与重点法源核验记录》；
- [x] **质量门禁与全量测试回归**：
  1. 后端自动化测试套件扩充至 **38/38 项测试 100% 绿灯全通过**；
  2. 前端 Vite 生产编译构建 **0 错误 0 警告**。

### Phase 7: 重构审查报告遗漏点与优化项全量闭环 (v3.1)
基于《重构审查报告.md》的全面专项核验与落地，完成以下 P0/P1/P2 级 8 项关键技术闭环：
- [x] **[P0] 合规中心全面接入 UnifiedRightDock 与 3 行熔断**：更新 `ComplianceCenterView.tsx`、`CaseReferenceHub.tsx`、`RiskPromptDashboard.tsx`、`ASEANComparisonMatrix.tsx`，移除遗留死链接，全面联动属地排雷副驾坞与建案预填传参；
- [x] **[P0] 知识图谱法条直出法源双语精读坞与权威认证**：`InteractiveCitationGraph.tsx` 节点点击直通 `openRightDock('law_reader')`，配备【权威认证 · 现行有效】金色标识与 `[+ 引用至当前案卷]` 功能；
- [x] **[P0] 核心推理图 nodes.py 补齐战术策略生成**：在 `red_team_strategist_node` 中调用 `build_tactical_guidance`，确保新建案件经过全流程图时自动生成初始攻防战术卡；
- [x] **[P1] 工程沙盘 350ms 防抖实时推演与基准对比徽章**：`CaseAnalysisView.tsx` 滑块拖动触发 350ms 防抖自动推演，动态渲染 `[+14d 较基准]` 相对偏移徽章，提供 `[↺ 恢复初始参数]`，话术卡配备 `NEW` 呼吸脉冲指示；
- [x] **[P1] 红线扫描与合同体检 Redline 增删对比视图**：`MaterialVerificationView.tsx` 与 `HomeLandingView.tsx` 提供 `[完整示范] vs [Redline 增删对比]` 双模切换，红标删除、绿标新增、橙标危险词汇；
- [x] **[P1] 切面 4 章节锚点快速定位与挂载成果移除**：切面 4 新增「目录锚点导航」胶囊（三维定性 / 假定推演 / 战术话术 / 挂载附件），挂载附件支持 `[× 移除挂载项]`；
- [x] **[P2] 支持 .docx / .txt / .md 索赔函拖拽上传与解析**：后端新增 `POST /api/cases/parse-doc` 接口，前端 `CaseEntryModal.tsx` 与 `MaterialVerificationView.tsx` 接入文件拖拽上传，自动解析文本并触发要素提取；
- [x] **[P2] 移除过时残存组件引用**：清理 `App.tsx` 中已弃用的 `LawDrawer` 导入，消除一切死代码。

---

## 5. 快速启动与验证命令

### 5.1 启动后端服务
```powershell
# 1. 确保已配置大模型 API Key（可选，无 Key 自动由本地规则引擎 100% 兜底）
$env:OPENAI_API_KEY="your-api-key-here"

# 2. 启动 FastAPI 后端服务
uvicorn lawagent.api.main:app --host 127.0.0.1 --port 8000 --reload
```
- 后端 Swagger 接口文档：`http://127.0.0.1:8000/docs`
- 健康检查探针：`http://127.0.0.1:8000/api/health`

### 5.2 启动前端应用
```powershell
cd FrontEnd
npm run dev
```
- 前端访问地址：`http://localhost:3000`
- 请求通过 Vite 代理自动转发至 `http://127.0.0.1:8000/api`。

### 5.3 运行全量自动化测试与生产构建
```powershell
# 运行后端 38 项全量回归测试
$env:PYTHONPATH="."
python -m pytest tests/ -v

# 运行前端生产编译检查 (TypeScript 类型检查 + Vite 打包)
npm --prefix FrontEnd run build
```

---

## 6. 下一步演进路线 (Next-Step Roadmap)

经过全栈大师级重构，系统交互体验与业务闭环已达桌面级高生产力标准，未来可向以下五个纵深方向演进：

### 方向一：多模态 EPC 复杂合同与工程证据解析 (Multimodal Ingestion & OCR)
- 引入版面分析（Layout-Parser）与高精度 OCR 管线，支持多页扫描版 EPC 主合同、专用条件 (PC)、会议纪要与工程变更令 (Variation Order) 直接上传解析，智能提取索赔时效与工期网络节点。

### 方向二：东盟涉外仲裁与工程索赔判例库纵深扩充
- 深度清洗并入库新加坡国际仲裁中心 (SIAC)、印尼雅加达仲裁院 (BANI)、亚洲国际仲裁中心 (AIAC) 涉及东盟大型工程的代表性脱敏裁决文书要旨，扩充裁判图谱关联边（`PRECEDENT_FOLLOWS`, `OVERRULES`）。

### 方向三：工程多方博弈决策树与量化和解窗口期推演 (Game-Theoretic Settlement Radar)
- 建立中资总包、东道国业主、属地分包商及项目融资行 (Lender) 四方博弈模型，基于决策树推演在各诉讼节点（保函索兑前、CIPAA 快速裁决前、SIAC 仲裁立案后）的最优和解区间（Settlement Sweet-Spot）。

### 方向四：端侧/私有化 LLM 部署与物理隔离适配 (On-Premises & Air-Gapped Serving)
- 适配 Ollama / vLLM 本地推理引擎，支持开源模型在企业私有算力服务器上一键部署，严格符合《数据安全法》第 36 条出海合规要求。

### 方向五：东盟本土语种法律意见书与矢量 PDF 报告导出
- 引入矢量排版引擎，扩展生成印尼语（Bahasa Indonesia）、越南语（Tiếng Việt）或泰语法律意见摘要与合规示范条款，满足直接向东道国部委与法庭呈递规范文书的需求。
