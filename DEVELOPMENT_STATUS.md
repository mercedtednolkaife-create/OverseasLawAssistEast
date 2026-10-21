# 域外法查明辅助应用 (OverseasLawAssist) 开发状态与进度追踪

> **当前版本**：v2.2 (Third-Round Audit Full Implementation & Modern Industrial Design Ready)  
> **更新时间**：2026-10-21  
> **系统状态**：已全面落实《C:\Downloads\review_report_v3.md》所提全部 8 项收尾任务与 Apple/Microsoft Fluent 2 现代工业级视觉重构。涵盖准据法脱钩冲突检测 (Lex Loci Solutionis Override)、中信保 30 日出险报损时效算子、泰 FBA 与菲 PCAB 外资准入算子、东盟 6 国 Local Counsel / DAAB 专家协同工作台、Mica & Acrylic 现代光学材质与沙盘即时状态写回。全套 35/35 项单元与集成测试 100% 绿灯通过，前端生产构建 0 错误 0 警告 (Production Ready & Verified)。

---

## 1. 架构定位与纯净东盟业务全景

本系统定位于**中国出海基建央企/国企在东盟 6 国（印度尼西亚、越南、马来西亚、新加坡、泰国、菲律宾）建设工程与海外投资（EPC/PPP/特许经营/跨境并购/联营体）法律风险防范、合同条款体检、合规指引与争议推演专业工作台**。系统已彻底剥离德美历史法域，全面覆盖出海四大支柱应用场景与两大协同枢纽：

```
[用户层 / 前端交互工作台 (React 19 + TypeScript + Apple Bento 网格 + Mica/Acrylic 现代光学材质)]
                         │
        (Vite Proxy: /api -> http://127.0.0.1:8000)
                         │
[FastAPI 服务层 lawagent.api] ── [REST API / SSE 事件总线 / 双模 DOCX 导出 / 沙盘试算 / 异步线程卸载]
                         │
[LangGraph 核心推理状态图 StateGraph(CaseState)]
   S1 Extract ─> S2 Precheck ─> S3 Decompose ─> S4 Researcher ─> S5 Matcher
    └── S6 Strategist ─> S7 Drafter ─> Critic (V1-V12 哨兵一票否决) ─> S8 Review ─> S9 Export
                         │
[多法域注册中心 JurisdictionRegistry (纯净东盟 6 国 + FIDIC)]
   ├── asean_id: 印度尼西亚 (建筑法UU 2/2017第57条, SEMA 3/2023, MEMR 11/2024, 民法典第1338条)
   ├── asean_vn: 越南 (2025新建设法第86.2条LD预定赔偿, 210/2026建设合同法令, PPP法)
   ├── asean_my: 马来西亚 (CIPAA 2012 第35条反背靠背, 建筑工业发展局法 Act 520 CIDB)
   ├── asean_sg: 新加坡 (SOPA 2004 第9条反背靠背, BS Mount Sophia 显失公平保函止付)
   ├── asean_th: 泰国 (民商法典第596条违约金酌减, 外商经营法 FBA 1999, BOI 优惠政策)
   └── asean_ph: 菲律宾 (2023年PPP法典 RA 11966, PCAB 资质准入 RA 4566, Manila Water 案平等待遇)
                         │
[双 SQLite 数据库存储架构 (零欧美历史残留)]
   ├── 快照库 law.sqlite (不可变, 31 条成文法规范与条约, 7 篇金标准判例, 52 个切块, 司法部法通网三语对照)
   └── 运行库 state.sqlite (读写 WAL 模式, C101~C104 央企示范案, 6 大出海国 Local Counsel/DAAB 专家名录)
```

---

## 2. 四大支柱业务场景与两大协同枢纽实现一览

| 业务场景 / 模块 | 核心功能与工作台支持 | 后端实现与专项算子 | 交付与展示产物 |
| :--- | :--- | :--- | :--- |
| **场景 A：境外投资准入与投前合规审查** (`pre_investment`) | • 外资准入负面清单与股权代持穿透核查<br>• 原住民习惯法土地 (Hak Ulayat) 权属尽调<br>• 国资委 35 号令事前论证与发改委 11 号令备案<br>• 跨境投资架构比选（直接投资 vs 新加坡中转 SPV vs 属地联营） | [`lawagent/flow/strategist.py`](file:///C:/Downloads/OverseasLawAssist/lawagent/flow/strategist.py)<br>`_build_asean_pre_investment_compliance_assessment`<br>[`lawagent/flow/sufficiency.py`](file:///C:/Downloads/OverseasLawAssist/lawagent/flow/sufficiency.py) 投前双模评估 | • 投前准入审查意见书<br>• 架构比选方案报告<br>• Word 意见书流式导出 |
| **场景 B：建设工程合同强行法红线体检工作台** (`CONTRACT_REDLINE_AUDIT`) | • 招标文件、EPC 主合同与分包协议强行法红线扫描<br>• 印尼 SEMA 3/2023 双语同文签署规则核验<br>• 马来 CIPAA 35 / 新加坡 SOPA 9 背靠背付款绝对无效<br>• 新加坡 BS Mount Sophia 保函显失公平止付救济<br>• 泰 FBA 附件三限制 / 菲 PCAB 资质平等待遇条款<br>• FIDIC 13.7 调价排除与 28 天索赔失权陷阱排查 | [`lawagent/api/routes/verify.py`](file:///C:/Downloads/OverseasLawAssist/lawagent/api/routes/verify.py)<br>`asyncio.to_thread` 线程池异步卸载<br>`ASEAN_CONTRACT_REDLINES` | • [`MaterialVerificationView.tsx`](file:///C:/Downloads/OverseasLawAssist/FrontEnd/src/components/verification/MaterialVerificationView.tsx)<br>• 条款红线 vs 意见书引证双模<br>• 一键复制示范合规条款 |
| **场景 C：工程履约索赔与交互式沙盘** (`execution_dispute`) | • FIDIC 银/黄/红核心条款跨版本智能降级检索<br>• 工期顺延 (EOT) 与 28 天除斥期反失权论证<br>• 印尼 MEMR 11/2024 本地化率 (TKDN) 豁免申请<br>• **What-If 交互式沙盘**：拖动滑块实时模拟 TKDN 比例、延误天数、通知送达天数、违约金上限与中信保 30 日时效 | [`lawagent/flow/security_sentinel.py`](file:///C:/Downloads/OverseasLawAssist/lawagent/flow/security_sentinel.py)<br>[`lawagent/api/routes/cases.py`](file:///C:/Downloads/OverseasLawAssist/lawagent/api/routes/cases.py)<br>`POST /cases/{id}/simulate-engineering` | • [`CaseAnalysisView.tsx`](file:///C:/Downloads/OverseasLawAssist/FrontEnd/src/components/analysis/CaseAnalysisView.tsx)<br>• 实时沙盘试算滑块面板<br>• 全局状态即时同步写回 |
| **场景 D：全周期合规打分与项目孵化** (SOP & Health Index) | • 五大阶段 × 三道防线核查清单在线自测<br>• 综合合规健康指数实时计算 (0-100分与红黄绿三态)<br>• **未达标项一键专项立项推演**：自动携带未达标点、国别与红线警示建卷启动 Agent 流水线<br>• 国别风险看板提示卡直通沙盘推演 | [`ComplianceGuidelineCenter.tsx`](file:///C:/Downloads/OverseasLawAssist/FrontEnd/src/components/compliance/ComplianceGuidelineCenter.tsx)<br>[`RiskPromptDashboard.tsx`](file:///C:/Downloads/OverseasLawAssist/FrontEnd/src/components/compliance/RiskPromptDashboard.tsx) | • 合规健康度仪表板<br>• 央国企合规指引手册 (Word)<br>• 国别风险提示卡与 Do's & Don'ts |
| **协同枢纽 1：东盟 Local Counsel 专家会商工作台** | • 预置东盟 6 国官方注册大律师与 DAAB 争端裁决专家<br>• 涵盖印尼 BANI、新加坡 SIAC、马来 AIAC、越南 VIAC、泰国 TAI、菲律宾 CIAC<br>• 严格落实利益冲突排查与会商意见全生命周期留痕 | [`lawagent/store/db.py`](file:///C:/Downloads/OverseasLawAssist/lawagent/store/db.py)<br>[`lawagent/api/routes/consults.py`](file:///C:/Downloads/OverseasLawAssist/lawagent/api/routes/consults.py)<br>`get_connection` 安全释放 | • [`ExpertConsultsView.tsx`](file:///C:/Downloads/OverseasLawAssist/FrontEnd/src/components/consults/ExpertConsultsView.tsx)<br>• 专家名录卡片与资质公示<br>• 专家意见归档与联动导出 |
| **协同枢纽 2：六国横向准入矩阵与立项比选闭环** | • 6 国法系、语种模式、2026 最新法典、准入联营红线、工程款追索与保函止付横向对比<br>• 支持用户多选 2~6 个目标东道国，一键孵化跨境投资准入比选专项立项案卷 | [`ASEANComparisonMatrix.tsx`](file:///C:/Downloads/OverseasLawAssist/FrontEnd/src/components/compliance/ASEANComparisonMatrix.tsx)<br>[`CaseEntryModal.tsx`](file:///C:/Downloads/OverseasLawAssist/FrontEnd/src/components/cases/CaseEntryModal.tsx) | • 毛玻璃吸顶对比表格<br>• 一键比选立项自动化流转 |

---

## 3. 当前运行环境与技术栈配置

- **操作系统**：Windows (x86_64)
- **后端环境**：Python 3.10.6, FastAPI, LangGraph, Pydantic v2
- **GPU 算力**：NVIDIA GeForce RTX 2070 SUPER (8GB VRAM, CUDA 12.8, BGE-M3 向量加速)
- **前端环境**：Node v24.12.0, Vite 8, React 19, TypeScript
- **大模型配置 (DashScope 兼容协议)**：
  - **Base URL**：`https://dashscope.aliyuncs.com/compatible-mode/v1`
  - **主推理模型**：`deepseek-v4.1-flash`（配合长文本指令遵循与高吞吐流式响应，网络受限时由本地规则引擎自适应兜底）
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

### Phase 5: 第三轮终审 8 项任务全面落地与视觉现代重构 (v2.2)
- [x] **准据法与工程所在国脱钩冲突检测 (Lex Loci Solutionis Override)**：`CaseMeta` 拆分东道国与准据法，`checks.py` 自动判定强行法穿透适用冲突；
- [x] **三大高价值算子**：
  1. `evaluate_sinosure_compliance()`：中信保 30 日出险报损时效审查算子，集成至工程沙盘第 4 滑块；
  2. `evaluate_ph_contractor_license()`：菲律宾 PCAB 资质准入与 Manila Water 案平等待遇审查；
  3. `evaluate_th_foreign_business_act()`：泰国 FBA 附件三工程限制与 BOI 优惠算子；
- [x] **去 AI 模板味与 Apple / Microsoft Fluent 2 视觉重构**：
  1. `index.css` 注入 Mica 环境微光画布（`.mica-canvas`）、Acrylic 亚克力高光卡片（`.acrylic-card`）与深空钛金属按钮（`.btn-space-titanium`）；
  2. 废除彩虹粗边框底框，升级为纯白/钛灰光学底色 + 发光呼吸状态胶囊（`.glow-dot-*`）+ 精密等宽数字（`tabular-nums`）；
  3. 全面重构 `ViabilityCalculationModal.tsx`、`DecompositionModal.tsx`、`FloatingOmniBar.tsx`、`CasePipelineAnimationModal.tsx`，投前模式自适应彻底消除陈旧诉讼话术；
- [x] **东盟 6 国 Local Counsel 专家名录**：印尼 BANI、新加坡 SIAC、大马 AIAC、越南 VIAC、泰国 TAI、菲律宾 CIAC 全面覆盖，会商数据库安全释放；
- [x] **性能优化与脚本统一**：`routes/verify.py` 采用 `asyncio.to_thread` 卸载；`scripts/build_asean_kb.py` 统一权威数据源；`scripts/seed_asean_cases.py` 补齐 C101~C104 全量初始参数与审计数据；
- [x] **自动化测试回归**：扩充至 **35/35 项测试全绿灯通过（耗时 14.09s）**，前端 Vite 构建耗时 271ms **0 错误 0 警告**。

---

## 5. 快速启动与验证命令

### 5.1 启动后端服务
```powershell
# 1. 确保已配置大模型 API Key
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

### 5.3 运行全量自动化测试与构建
```powershell
# 运行后端 35 项全量回归测试
python -m pytest tests/ -v

# 运行前端生产编译检查
npm --prefix FrontEnd run build
```

---

## 6. 下一步改进和优化方向 (Next-Step Roadmap)

经过对当前系统业务落地深度、高并发响应、涉外多语种支撑及央国企安全出海现实痛点的深入分析，规划以下五个高价值优化方向：

### 方向一：多模态 EPC 复杂合同与工程证据解析 (Multimodal Ingestion & OCR)
- **业务痛点**：中资出海企业面对数十乃至上百页的全英文/双语扫描版 EPC 主合同、专用条件 (PC)、会议纪要与工程变更令 (Variation Order)，人工整理事实录入成本极高。
- **实施内容**：
  1. 引入基于版面分析（Layout-Parser）与高精度 OCR 的多模态文档解析管线，支持 PDF、图片与 Word 格式工程证据直接解析；
  2. 智能提取合同解释优先级条款、索赔时效条款、预定赔偿封顶及工期网络关键节点，自动结构化灌入案件事实清单与工程参数。

### 方向二：东盟涉外仲裁与工程索赔判例库纵深扩充
- **业务痛点**：东盟各法域裁判先例分散，除现有的 7 篇金标准先例外，需要更多关于保函止付、不可抗力、隐性税费的细分先例支撑。
- **实施内容**：
  1. 深度清洗并入库新加坡国际仲裁中心 (SIAC)、印尼雅加达仲裁院 (BANI)、亚洲国际仲裁中心 (AIAC) 及国际商会仲裁院 (ICC) 涉及东盟大型工程的代表性脱敏裁决案例要旨；
  2. 丰富裁判文书图谱关联边（`PRECEDENT_FOLLOWS`, `OVERRULES`, `DISTINGUISHES`），使 Researcher 节点可根据事实争点精准推荐历史支持度高的类案判例。

### 方向三：工程多方博弈决策树与量化和解窗口期推演 (Game-Theoretic Settlement Radar)
- **业务痛点**：出海基建工程纠纷极少以“零和死战”终局，总承包商核心目标通常是通过商业让步和解保住项目现金流与履约保函。
- **实施内容**：
  1. 建立中资总包、东道国业主、属地分包商及项目融资行 (Lender) 四方博弈模型，基于决策树推演在各诉讼节点（保函索兑前、CIPAA 快速裁决前、SIAC 仲裁立案后）的利益敞口分布；
  2. 测算最优和解区间（Settlement Sweet-Spot）与条款让步边界，辅助法务合规团队从“单纯法律防卫”升级为“商务和解与利益保全”。

### 方向四：端侧/私有化 LLM 部署与物理隔离适配 (On-Premises & Air-Gapped Serving)
- **业务痛点**：特大型涉密基建工程、高精度地理信息数据受《数据安全法》第 36 条严格规制，严禁向境外或未经授权的公有云传输。
- **实施内容**：
  1. 适配 Ollama / vLLM / SGLang 本地推理引擎，支持 Qwen2.5-72B / DeepSeek-R1-Distill 等开源模型在企业私有算力服务器上一键部署；
  2. 提供纯内网离线工作模式切换，实现模型推理、向量检索与 SQLite 数据底座完全物理隔离。

### 方向五：东盟本土语种法律意见书与矢量 PDF 报告导出
- **业务痛点**：直接向东道国部委（如印尼 BKPM/MEMR、越南建设部 BXD）或当地法庭呈递文书时，需提供本土官方语言法律文书。
- **实施内容**：
  1. 在 DOCX 导出的基础上，引入 WeasyPrint / ReportLab 矢量排版引擎，支持导出带水印、页眉页脚、防伪指纹的高级法庭级排版 PDF 报告；
  2. 扩展生成印尼语（Bahasa Indonesia）、越南语（Tiếng Việt）或泰语法律意见摘要与合规示范条款，满足属地化呈报规范。
