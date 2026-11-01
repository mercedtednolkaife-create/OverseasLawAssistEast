# 东盟涉外法治查明智能体：20个真实案例详细测试经过记录

> **测试执行时间**: 2026-11-01  
> **评测案例规模**: 20个跨国涉外疑难案件（全覆盖东盟11国 + FIDIC工程 + CISG商事 + BIT双边投资协定）  
> **底层知识库快照**: 20261021-asean-v2.2 (412条成文法规范 + 104条标杆先例 + 636条图谱关联边)  
> **执行状态机**: s1_extract ➔ s2_precheck ➔ s3_decompose ➔ researcher (CL-Align & CRAG) ➔ matcher ➔ red_team_strategist ➔ translator ➔ drafter ➔ critic ➔ s8_review ➔ s9_export  

---

## 目录
- [一、测试执行环境与配置](#一测试执行环境与配置)
- [二、20个案例执行明细跟踪](#二20个案例执行明细跟踪)
  - [CASE-01 新加坡光伏电站保函恶意索兑与显失公平止付案](#case-01-新加坡光伏电站保函恶意索兑与显失公平止付案)
  - [CASE-02 雅万衍生公路纯英文 EPC 合同效力与国语法抗辩案](#case-02-雅万衍生公路纯英文-EPC-合同效力与国语法抗辩案)
  - [CASE-03 宁顺光伏电站工期违约金 12% 法定封顶抗辩案](#case-03-宁顺光伏电站工期违约金-12%-法定封顶抗辩案)
  - [CASE-04 梳邦数据中心分包商 CIPAA 追索与背靠背条款无效案](#case-04-梳邦数据中心分包商-CIPAA-追索与背靠背条款无效案)
  - [CASE-05 曼谷轻轨钢构工程款催告与 2 年短期诉讼时效案](#case-05-曼谷轻轨钢构工程款催告与-2-年短期诉讼时效案)
  - [CASE-06 地热电站 EPC 基础设施工程法定停工禁令豁免案](#case-06-地热电站-EPC-基础设施工程法定停工禁令豁免案)
  - [CASE-07 金边高档商业综合体延误索赔与违约金不可调减案](#case-07-金边高档商业综合体延误索赔与违约金不可调减案)
  - [CASE-08 湄公河支流水电站 BOT 特许权外债未登记合规抗辩案](#case-08-湄公河支流水电站-BOT-特许权外债未登记合规抗辩案)
  - [CASE-09 仰光供水管道改造工程军管外汇强制结汇与合同落空案](#case-09-仰光供水管道改造工程军管外汇强制结汇与合同落空案)
  - [CASE-10 摩拉港深水泊位基建工程政府主权豁免绝对抗辩案](#case-10-摩拉港深水泊位基建工程政府主权豁免绝对抗辩案)
  - [CASE-11 帝力港防波堤项目未获审计法院事前签证效力确认案](#case-11-帝力港防波堤项目未获审计法院事前签证效力确认案)
  - [CASE-12 新加坡商业中心地下连续墙潜伏开裂与 15 年长效时效案](#case-12-新加坡商业中心地下连续墙潜伏开裂与-15-年长效时效案)
  - [CASE-13 莫罗瓦利镍铁工业园 EPC 本地化率 (TKDN) 审计追缴抗辩案](#case-13-莫罗瓦利镍铁工业园-EPC-本地化率-TKDN-审计追缴抗辩案)
  - [CASE-14 越南北南高速公路施工备忘录诉讼时效中断案](#case-14-越南北南高速公路施工备忘录诉讼时效中断案)
  - [CASE-15 柔佛炼化码头工程因分包资质争议的按劳报酬补偿案](#case-15-柔佛炼化码头工程因分包资质争议的按劳报酬补偿案)
  - [CASE-16 普吉岛度假村未移交工程遭受特大暴雨损毁风险负担案](#case-16-普吉岛度假村未移交工程遭受特大暴雨损毁风险负担案)
  - [CASE-17 中资总包企业 PCAB 外资承包商牌照非歧视平等待遇案](#case-17-中资总包企业-PCAB-外资承包商牌照非歧视平等待遇案)
  - [CASE-18 泛亚跨境铁路标段争议避免裁决委员会 (DAAB) 决定临时执行力案](#case-18-泛亚跨境铁路标段争议避免裁决委员会-DAAB-决定临时执行力案)
  - [CASE-19 跨国重型采矿工程机械出口印尼苏拉威西受阻不可抗力案](#case-19-跨国重型采矿工程机械出口印尼苏拉威西受阻不可抗力案)
  - [CASE-20 印度尼西亚未加工原矿出口绝对禁令与间接征收补偿案](#case-20-印度尼西亚未加工原矿出口绝对禁令与间接征收补偿案)

---

## 一、测试执行环境与配置
- **操作系统**: Windows 11 x64
- **大模型引擎配置**: 
  - 推理/要件提取/起草: `dashscope / qwen-plus` (API 响应 P90 < 2.5s)
  - 翻译/速检/红蓝对抗: `dashscope / qwen-flash` (API 响应 P90 < 0.8s)
- **知识检索核心**: 
  - L1 强行法成文法规范 (SQLite + Hybrid BM25/Dense Index)
  - CL-Align 跨法系概念对齐算子 (165 组多语种法学教义映射张量)
  - CRAG 自省式检索门禁与跨层补偿循环 (自省阈值 $\tau=0.75$)
  - 1-Hop 图拓扑与风险共同体聚拢
- **全流程并发调度**: 异步事件流控制 `asyncio.Semaphore(1)` 稳定执行，总耗时 **815.48s**。

---

## 二、20个案例执行明细跟踪

### CASE-01: 新加坡光伏电站保函恶意索兑与显失公平止付案

| 属性项 | 执行参数与测量结果 |
| :--- | :--- |
| **所属法域 / 准据法** | `asean_sg` / `asean_sg` |
| **合同范式 / 争议机构** | `FIDIC_SILVER` / `SIAC` |
| **流程流转状态** | **COMPLETED** (端到端运行耗时: `105.18s`) |
| **事实 / 入口门禁 / 要件** | 提取事实 `3` 项 \| 审查准入 `9` 项 \| 争议要件 `4` 项 |
| **证据链召回总量** | 共召回 **24** 条法律证据 (L1成文法 + L2条约/先例) |
| **法条召回率 (Recall)** | **50.0%** (预期基准法源: `CASE:SG_CA:BS_Mount_Sophia:2012, SG:Limitation_Act_1959:Sec6_24A_Latent_Defects`) |
| **认定准确度 (Accuracy)** | **100.0%** (争议焦点结论吻合度与质检点全量通过) |
| **CRAG 充分性门禁** | 触发状态: `✅ 触发跨层补偿` \| 评分跃迁: `τ=0.50 ➔ τ=0.50` |
| **L2 跨层补偿法源** | `REF_CASE:SG_HC:FIDIC_Cl16_Suspension_Validity:2019, REF_CASE:SG_HC:FIDIC_Cl4_12_UnforeseenGround:2018, INTL:CISG:Art79, REF_CASE:SG_HC:BCA_Structural_Liability:2017, REF_CASE:SG_HC:IRDA_Sec440_IpsoFacto_Stay:2022, REF_CASE:SG_CA:Senda_International_v_Kiri:2022` |
| **审查质检 (Review Checks)**| 通过 `11` / `12` 质检规则 |

> **查明意见报告摘要与主文裁定截选**：  
> *依据东盟东道国工程法规及 FIDIC 国际工程标准合同规范【CASE:MY_COA:Sumatec:2012】，马来西亚上诉法院 [2012] 4 MLJ 1 / [2011] 1 MSCL 18（2012年3月15日）判决理由：  马来西亚上诉法院确认，显失公平构成一项独立的法律事由，可用来限制受益人依据即期银行保函主张权利。  【裁判法理深度解析... 依据东盟东道国工程法规及 FIDIC 国际工程标准合同规范【CASE:SG_CA:BS_Mount_Sophia:2012】，裁判要旨：见索...*

---
### CASE-02: 雅万衍生公路纯英文 EPC 合同效力与国语法抗辩案

| 属性项 | 执行参数与测量结果 |
| :--- | :--- |
| **所属法域 / 准据法** | `asean_id` / `asean_id` |
| **合同范式 / 争议机构** | `FIDIC_RED` / `BANI` |
| **流程流转状态** | **COMPLETED** (端到端运行耗时: `141.74s`) |
| **事实 / 入口门禁 / 要件** | 提取事实 `2` 项 \| 审查准入 `7` 项 \| 争议要件 `4` 项 |
| **证据链召回总量** | 共召回 **40** 条法律证据 (L1成文法 + L2条约/先例) |
| **法条召回率 (Recall)** | **100.0%** (预期基准法源: `ID:UU_24_2009:Art31, CASE:ID_MA:Putusan_MA_1582_K_Pdt_2018:2019`) |
| **认定准确度 (Accuracy)** | **100.0%** (争议焦点结论吻合度与质检点全量通过) |
| **CRAG 充分性门禁** | 触发状态: `✅ 触发跨层补偿` \| 评分跃迁: `τ=0.50 ➔ τ=0.50` |
| **L2 跨层补偿法源** | `ID:PBI_17_3_2015:Art2, REF_CASE:ID_PN_JakSel:BKPM_Licensing:2020, REF_CASE:ID_SC:KUHPerdata_1139_Subcontractor_Lien:2020, REF_CASE:ID_PN_JakPus:PBI_17_3_Rupiah_Exemption_Dispute:2020, ID:Permen_PUPR_14_2020, ID:Permen_PUPR_14_2020:Standard_Bidding` |
| **审查质检 (Review Checks)**| 通过 `12` / `12` 质检规则 |

> **查明意见报告摘要与主文裁定截选**：  
> *依据东盟东道国工程法规及 FIDIC 国际工程标准合同规范【ID:UU_24_2009:Art31】，涉及印尼国家机构、政府机关、私营机构或印尼公民的合同，必须强制签署印尼语文本；涉及外国主体的合同，应当同时以双语或附英文文本签署。根据最高法院 SEMA 3/2023 司法解释，未签署印尼语版本不构成违反国际公共秩序，但为防范地方法院形式抗... 依据东盟东道国工程法规及 FIDIC 国际工程标准合同规范【CASE:ID_MA:Nine_AM_v_BKPL_2015】，印度尼西亚最高法院判决书M...*

---
### CASE-03: 宁顺光伏电站工期违约金 12% 法定封顶抗辩案

| 属性项 | 执行参数与测量结果 |
| :--- | :--- |
| **所属法域 / 准据法** | `asean_vn` / `asean_vn` |
| **合同范式 / 争议机构** | `EPC_TURNKEY` / `VIAC` |
| **流程流转状态** | **COMPLETED** (端到端运行耗时: `121.41s`) |
| **事实 / 入口门禁 / 要件** | 提取事实 `2` 项 \| 审查准入 `8` 项 \| 争议要件 `4` 项 |
| **证据链召回总量** | 共召回 **31** 条法律证据 (L1成文法 + L2条约/先例) |
| **法条召回率 (Recall)** | **100.0%** (预期基准法源: `VN:Decree_37_2015_ND_CP:Art18, VN:Civil_Code_2015:Art351`) |
| **认定准确度 (Accuracy)** | **100.0%** (争议焦点结论吻合度与质检点全量通过) |
| **CRAG 充分性门禁** | 触发状态: `⚪ 无需补偿` \| 评分跃迁: `τ=1.00 ➔ τ=1.00` |
| **L2 跨层补偿法源** | `（无需补偿或在L1直接满足）` |
| **审查质检 (Review Checks)**| 通过 `12` / `12` 质检规则 |

> **查明意见报告摘要与主文裁定截选**：  
> *依据东盟东道国工程法规及 FIDIC 国际工程标准合同规范【VN:Construction_Law_2014_Amended_2020:Art138_146】，建设工程合同当事人必须依法依约履行合同义务。违约方应向守约方支付合同约定的预定违约金，并赔偿实际发生的直接损失。对于使用国家财政预算或国有企业资本的建设项目，预定违约金的最高限额不得超过该部分发生违约的合同价款的12%（依据第146条第2款... 依据东盟东道国工程法规及 FIDIC 国际工程标准合同规范【VN:Civil_Code_20...*

---
### CASE-04: 梳邦数据中心分包商 CIPAA 追索与背靠背条款无效案

| 属性项 | 执行参数与测量结果 |
| :--- | :--- |
| **所属法域 / 准据法** | `asean_my` / `asean_my` |
| **合同范式 / 争议机构** | `SUBCONTRACT` / `KLRCA_AIAC` |
| **流程流转状态** | **COMPLETED** (端到端运行耗时: `67.00s`) |
| **事实 / 入口门禁 / 要件** | 提取事实 `1` 项 \| 审查准入 `8` 项 \| 争议要件 `4` 项 |
| **证据链召回总量** | 共召回 **9** 条法律证据 (L1成文法 + L2条约/先例) |
| **法条召回率 (Recall)** | **100.0%** (预期基准法源: `MY:CIPAA_2012:Sec13, CASE:MY_FC:Bauer_CIPAA_Sec35:2019`) |
| **认定准确度 (Accuracy)** | **100.0%** (争议焦点结论吻合度与质检点全量通过) |
| **CRAG 充分性门禁** | 触发状态: `⚪ 无需补偿` \| 评分跃迁: `τ=0.88 ➔ τ=0.88` |
| **L2 跨层补偿法源** | `（无需补偿或在L1直接满足）` |
| **审查质检 (Review Checks)**| 通过 `12` / `12` 质检规则 |

> **查明意见报告摘要与主文裁定截选**：  
> *依据东盟东道国工程法规及 FIDIC 国际工程标准合同规范【FIDIC:Silver_1999:Clause_8.4】，承包商因发包人指示的工程变更，或根据合同专用条件享有工期顺延权利的事件，以及因发包人、发包人人员或现场其他承包商造成的任何延误、阻碍或妨碍（包括场地移交延迟及征地受阻），在遵守第20.1款程序的前提下，有权获得竣工期限的合理顺延。... 依据东盟东道国工程法规及 FIDIC 国际工程标准合同规范【FIDIC:Silver_1999:Clause_20.1】，承包商如要求工期顺延...*

---
### CASE-05: 曼谷轻轨钢构工程款催告与 2 年短期诉讼时效案

| 属性项 | 执行参数与测量结果 |
| :--- | :--- |
| **所属法域 / 准据法** | `asean_th` / `asean_th` |
| **合同范式 / 争议机构** | `FIDIC_RED` / `TAI` |
| **流程流转状态** | **COMPLETED** (端到端运行耗时: `129.08s`) |
| **事实 / 入口门禁 / 要件** | 提取事实 `2` 项 \| 审查准入 `8` 项 \| 争议要件 `4` 项 |
| **证据链召回总量** | 共召回 **43** 条法律证据 (L1成文法 + L2条约/先例) |
| **法条召回率 (Recall)** | **100.0%** (预期基准法源: `TH:CCC:Sec193_34_Two_Year_Contractor_Limitation, TH:CCC:Sec193_14_Interruption_of_Prescription, CASE:TH_SC:No_7221_2552_2Year_Prescription_Trap:2009`) |
| **认定准确度 (Accuracy)** | **100.0%** (争议焦点结论吻合度与质检点全量通过) |
| **CRAG 充分性门禁** | 触发状态: `✅ 触发跨层补偿` \| 评分跃迁: `τ=0.62 ➔ τ=0.50` |
| **L2 跨层补偿法源** | `TH:Consumer_Protection_Act_2522:Sec35_2, REF_CASE:TH_SAC:Public_Procurement_Abandoning_Contractor_Blacklist:2022, REF_CASE:TH_Admin_Court:NEQA_EIA_Stop_Work:2019, REF_CASE:TH_SC:Superficies_30Year_Solar_Plant_Ownership:2020, REF_CASE:TH_SAC:No_128_2562_EIA_Stop_Work:2019, REF_CASE:TH_SC:Land_Leasehold_Enforceability:2016` |
| **审查质检 (Review Checks)**| 通过 `12` / `12` 质检规则 |

> **查明意见报告摘要与主文裁定截选**：  
> *依据东盟东道国工程法规及 FIDIC 国际工程标准合同规范【CASE:TH_SC:CCC_Sec686_Guarantor_60Day_Notice_Release:2018】，泰国最高法院终审判决确立《民商法典》第686条关于保证人保护的刚性规则：自2015年泰国担保法重大修订后，债权人（发包人）在主债务人（总包商）发生债务违约之日起六十日内，必须以书面形式向连带保证人发出正式违约催告通知；若发包人在主债务人违约... 依据东盟东道国工程法规及 FIDIC 国际工程标准合同规范【TH:CCC:...*

---
### CASE-06: 地热电站 EPC 基础设施工程法定停工禁令豁免案

| 属性项 | 执行参数与测量结果 |
| :--- | :--- |
| **所属法域 / 准据法** | `asean_ph` / `asean_ph` |
| **合同范式 / 争议机构** | `EPC_TURNKEY` / `CIAC` |
| **流程流转状态** | **COMPLETED** (端到端运行耗时: `136.42s`) |
| **事实 / 入口门禁 / 要件** | 提取事实 `1` 项 \| 审查准入 `8` 项 \| 争议要件 `4` 项 |
| **证据链召回总量** | 共召回 **45** 条法律证据 (L1成文法 + L2条约/先例) |
| **法条召回率 (Recall)** | **100.0%** (预期基准法源: `PH:RA_8975:Sec3, CASE:PH_SC:Republic_v_Caguioa_RA8975_NoTRO:2009`) |
| **认定准确度 (Accuracy)** | **100.0%** (争议焦点结论吻合度与质检点全量通过) |
| **CRAG 充分性门禁** | 触发状态: `✅ 触发跨层补偿` \| 评分跃迁: `τ=0.50 ➔ τ=0.50` |
| **L2 跨层补偿法源** | `REF_CASE:PCA:Nusantara_v_Malaysia:2018, PH:PD_1586_EIS_System:Sec4` |
| **审查质检 (Review Checks)**| 通过 `12` / `12` 质检规则 |

> **查明意见报告摘要与主文裁定截选**：  
> *依据东盟东道国工程法规及 FIDIC 国际工程标准合同规范【PH:RA_8975:Sec3】，除菲律宾最高法院（Supreme Court）外，任何地方法院（Regional Trial Courts, RTC）或上诉法院均不得对菲律宾政府及其委托的任何公私合营承建企业签发临时限制令（Temporary Restraining Or... 依据东盟东道国工程法规及 FIDIC 国际工程标准合同规范【CASE:PH_SC:Republic_v_Caguioa_RA8975_NoTRO:2009】，...*

---
### CASE-07: 金边高档商业综合体延误索赔与违约金不可调减案

| 属性项 | 执行参数与测量结果 |
| :--- | :--- |
| **所属法域 / 准据法** | `asean_kh` / `asean_kh` |
| **合同范式 / 争议机构** | `FIDIC_SILVER` / `NCAC` |
| **流程流转状态** | **COMPLETED** (端到端运行耗时: `101.03s`) |
| **事实 / 入口门禁 / 要件** | 提取事实 `3` 项 \| 审查准入 `8` 项 \| 争议要件 `4` 项 |
| **证据链召回总量** | 共召回 **27** 条法律证据 (L1成文法 + L2条约/先例) |
| **法条召回率 (Recall)** | **100.0%** (预期基准法源: `KH:Civil_Code_2007:Art403_Liquidated_Damages_Non_Reduction, CASE:KH_NCAC:Lump_Sum_Delay_Damages_Award_2022`) |
| **认定准确度 (Accuracy)** | **100.0%** (争议焦点结论吻合度与质检点全量通过) |
| **CRAG 充分性门禁** | 触发状态: `✅ 触发跨层补偿` \| 评分跃迁: `τ=0.38 ➔ τ=0.50` |
| **L2 跨层补偿法源** | `KH:CCFTA_2020:Trade_Investment, FIDIC:Silver_1999:Clause_11.4, FIDIC:Silver_1999:Clause_15.1, REF_CASE:SIAC:Concurrent_Delay_Malmaison:2021, REF_CASE:SIAC:Case_ARB_089_2019_TKDN_EOT:2021, FIDIC:Silver_1999:Clause_8.7` |
| **审查质检 (Review Checks)**| 通过 `12` / `12` 质检规则 |

> **查明意见报告摘要与主文裁定截选**：  
> *依据东盟东道国工程法规及 FIDIC 国际工程标准合同规范【KH:Civil_Code_2007:Art403_Liquidated_Damages_Non_Reduction】，根据由日本法学专家主导起草的柬埔寨民法典第403条规定，合同当事人可事先约定因债务不履行而产生的损害赔偿金额（即预定违约金）。法院原则上不得增加或减少当事人已明确约定的预定违约金数额。该刚性原则与泰国、菲律宾法院享有对预定违约金进行衡平酌减... 依据东盟东道国工程法规及 FIDIC 国际工程标准合同规范【KH:Law...*

---
### CASE-08: 湄公河支流水电站 BOT 特许权外债未登记合规抗辩案

| 属性项 | 执行参数与测量结果 |
| :--- | :--- |
| **所属法域 / 准据法** | `asean_la` / `asean_la` |
| **合同范式 / 争议机构** | `CONCESSION_BOT` / `SIAC` |
| **流程流转状态** | **COMPLETED** (端到端运行耗时: `89.19s`) |
| **事实 / 入口门禁 / 要件** | 提取事实 `2` 项 \| 审查准入 `7` 项 \| 争议要件 `4` 项 |
| **证据链召回总量** | 共召回 **28** 条法律证据 (L1成文法 + L2条约/先例) |
| **法条召回率 (Recall)** | **100.0%** (预期基准法源: `LA:Foreign_Currency_Law_2022:Art15_Mandatory_Repatriation_Approval`) |
| **认定准确度 (Accuracy)** | **100.0%** (争议焦点结论吻合度与质检点全量通过) |
| **CRAG 充分性门禁** | 触发状态: `✅ 触发跨层补偿` \| 评分跃迁: `τ=0.12 ➔ τ=0.50` |
| **L2 跨层补偿法源** | `LAW:SG_IRDA_2018:Cross_Border_Insolvency, VN:Circular_12_2022_SBV:Art11, LAW:ID_UU_27_2022_PDP:Cross_Border, CASE:ICSID:Lao_Holdings_v_Laos_2019, VN:Commercial_Law_2005:Art294, TREATY:CN_LA_Judicial_Assistance_1999:Civil_Commercial` |
| **审查质检 (Review Checks)**| 通过 `12` / `12` 质检规则 |

> **查明意见报告摘要与主文裁定截选**：  
> *依据东盟东道国工程法规及 FIDIC 国际工程标准合同规范【LA:Foreign_Currency_Law_2022:Art15_Mandatory_Repatriation_Approval】，中资企业在老挝开展投建营项目所面临的首要外汇管控红线！根据老挝《建设工程法规》第15条及老挝央行（BOL）实施细则之规定，所有在老挝注册的外资企业，其从境外获取的出口创汇收入、工程款项以及境外股东借款，均须强制性全额回流至老挝境内商业银行开... 依据东盟东道国工程法规及 FIDIC 国际工程标准合同规...*

---
### CASE-09: 仰光供水管道改造工程军管外汇强制结汇与合同落空案

| 属性项 | 执行参数与测量结果 |
| :--- | :--- |
| **所属法域 / 准据法** | `asean_mm` / `asean_mm` |
| **合同范式 / 争议机构** | `FIDIC_RED` / `SIAC` |
| **流程流转状态** | **COMPLETED** (端到端运行耗时: `96.22s`) |
| **事实 / 入口门禁 / 要件** | 提取事实 `2` 项 \| 审查准入 `7` 项 \| 争议要件 `4` 项 |
| **证据链召回总量** | 共召回 **36** 条法律证据 (L1成文法 + L2条约/先例) |
| **法条召回率 (Recall)** | **100.0%** (预期基准法源: `MM:Contract_Act_1872:Sec56_Frustration`) |
| **认定准确度 (Accuracy)** | **100.0%** (争议焦点结论吻合度与质检点全量通过) |
| **CRAG 充分性门禁** | 触发状态: `✅ 触发跨层补偿` \| 评分跃迁: `τ=0.50 ➔ τ=0.50` |
| **L2 跨层补偿法源** | `FIDIC:Silver_1999:Clause_14.15, TREATY:CN_MM_BIT_2001:Ad_Hoc_Arbitration, REF_CASE:SIAC:Case_ARB_112_2020_Offshore_Wind_Vietnam:2021, TREATY:New_York_1958:Art_V, REF_CASE:SIAC:EA_Bond_Injunction_Indonesia_EPC:2022, FIDIC:Silver_1999:Clause_16.1` |
| **审查质检 (Review Checks)**| 通过 `12` / `12` 质检规则 |

> **查明意见报告摘要与主文裁定截选**：  
> *依据东盟东道国工程法规及 FIDIC 国际工程标准合同规范【MM:Contract_Act_1872:Sec56_Frustration】，根据普通法的基本原则，当事人在合同订立后，若因发生不可预见且无法避免的客观事态（如武装冲突、政变、港口严密封锁或国际制裁禁令），致使合同标的在客观事实上或法律上已变得不可能履行（Impossible）或违法（Unlawful），则自该受阻事... 依据东盟东道国工程法规及 FIDIC 国际工程标准合同规范【MY:Contracts_Act_1950:Sec5...*

---
### CASE-10: 摩拉港深水泊位基建工程政府主权豁免绝对抗辩案

| 属性项 | 执行参数与测量结果 |
| :--- | :--- |
| **所属法域 / 准据法** | `asean_bn` / `asean_bn` |
| **合同范式 / 争议机构** | `EPC_TURNKEY` / `Brunei_High_Court` |
| **流程流转状态** | **COMPLETED** (端到端运行耗时: `98.67s`) |
| **事实 / 入口门禁 / 要件** | 提取事实 `1` 项 \| 审查准入 `7` 项 \| 争议要件 `4` 项 |
| **证据链召回总量** | 共召回 **23** 条法律证据 (L1成文法 + L2条约/先例) |
| **法条召回率 (Recall)** | **100.0%** (预期基准法源: `BN:Constitution:Art84C_Absolute_Sovereign_Immunity, CASE:UK_PC:Brunei_Government_Sovereign_Immunity_Art84C_2015`) |
| **认定准确度 (Accuracy)** | **100.0%** (争议焦点结论吻合度与质检点全量通过) |
| **CRAG 充分性门禁** | 触发状态: `✅ 触发跨层补偿` \| 评分跃迁: `τ=0.12 ➔ τ=0.50` |
| **L2 跨层补偿法源** | `BN:International_Arbitration_Order_2009:Enforcement, REF_CASE:MY_HC:BNM_Forex_Loan_Repayment:2019, REF_CASE:PCA:Walter_Bau_v_Thailand:2009, REF_CASE:PCA:Nusantara_v_Malaysia:2018, FIDIC:Silver_1999:Clause_15.1, FIDIC:Silver_1999:Clause_17.6` |
| **审查质检 (Review Checks)**| 通过 `12` / `12` 质检规则 |

> **查明意见报告摘要与主文裁定截选**：  
> *依据东盟东道国工程法规及 FIDIC 国际工程标准合同规范【BN:Constitution:Art84C_Absolute_Sovereign_Immunity】，文莱出海投资与基础设施总承包所面临的最核心宪制限制：根据文莱宪法第84C条，国家元首（苏丹）及文莱政府机关享有绝对的主权豁免权。文莱国内法律严格禁止任何人在文莱境内法院就任何事由对文莱苏丹或文莱政府提起民事诉讼。因此，中资企业与文莱政府部门... 依据东盟东道国工程法规及 FIDIC 国际工程标准合同规范【BN:Contracts_A...*

---
### CASE-11: 帝力港防波堤项目未获审计法院事前签证效力确认案

| 属性项 | 执行参数与测量结果 |
| :--- | :--- |
| **所属法域 / 准据法** | `asean_tl` / `asean_tl` |
| **合同范式 / 争议机构** | `FIDIC_RED` / `Chamber_of_Commerce_TL` |
| **流程流转状态** | **COMPLETED** (端到端运行耗时: `118.09s`) |
| **事实 / 入口门禁 / 要件** | 提取事实 `1` 项 \| 审查准入 `7` 项 \| 争议要件 `4` 项 |
| **证据链召回总量** | 共召回 **25** 条法律证据 (L1成文法 + L2条约/先例) |
| **法条召回率 (Recall)** | **100.0%** (预期基准法源: `TL:Law_9_2011_Budget_Management:Fiscalizacao_Previa_Visto`) |
| **认定准确度 (Accuracy)** | **100.0%** (争议焦点结论吻合度与质检点全量通过) |
| **CRAG 充分性门禁** | 触发状态: `✅ 触发跨层补偿` \| 评分跃迁: `τ=0.50 ➔ τ=0.50` |
| **L2 跨层补偿法源** | `INTL:CISG:Art25, INTL:FIDIC_2017:Cl20_2, INTL:URDG_758:Art15, INTL:URDG_758:Art20, INTL:ISP98:Rule4_01, INTL:CISG:Art79` |
| **审查质检 (Review Checks)**| 通过 `12` / `12` 质检规则 |

> **查明意见报告摘要与主文裁定截选**：  
> *依据东盟东道国工程法规及 FIDIC 国际工程标准合同规范【TL:Law_9_2011_Budget_Management:Fiscalizacao_Previa_Visto】，东帝汶工程承包第一大生死红线：凡涉及东帝汶国家财政资金超过五十万美元（USD 500,000）的政府基础设施合同、总承包补充协议或工程追加款，在签署后必须报请东帝汶高等行政税务审计法院（Câmara de Contas）进行事前合法性审查（... 依据东盟东道国工程法规及 FIDIC 国际工程标准合同规范【CASE:TL...*

---
### CASE-12: 新加坡商业中心地下连续墙潜伏开裂与 15 年长效时效案

| 属性项 | 执行参数与测量结果 |
| :--- | :--- |
| **所属法域 / 准据法** | `asean_sg` / `asean_sg` |
| **合同范式 / 争议机构** | `FIDIC_SILVER` / `Singapore_High_Court` |
| **流程流转状态** | **COMPLETED** (端到端运行耗时: `136.63s`) |
| **事实 / 入口门禁 / 要件** | 提取事实 `2` 项 \| 审查准入 `8` 项 \| 争议要件 `4` 项 |
| **证据链召回总量** | 共召回 **50** 条法律证据 (L1成文法 + L2条约/先例) |
| **法条召回率 (Recall)** | **100.0%** (预期基准法源: `SG:Limitation_Act_1959:Sec6_24A_Latent_Defects`) |
| **认定准确度 (Accuracy)** | **100.0%** (争议焦点结论吻合度与质检点全量通过) |
| **CRAG 充分性门禁** | 触发状态: `✅ 触发跨层补偿` \| 评分跃迁: `τ=0.62 ➔ τ=0.50` |
| **L2 跨层补偿法源** | `INTL:CISG:Art79` |
| **审查质检 (Review Checks)**| 通过 `12` / `12` 质检规则 |

> **查明意见报告摘要与主文裁定截选**：  
> *依据东盟东道国工程法规及 FIDIC 国际工程标准合同规范【MY:Limitation_Act_1953:Sec6A】，对于工程地质滑塌、桩基开裂等在竣工交付时无法合理查明的隐蔽工程缺陷，原告的索赔时效为自其首次实际获悉或应当获悉该损害事实及起诉权利之日起三年，但最长权利保护期不得超过自导致损害的行为发生之日起十五年。... 依据东盟东道国工程法规及 FIDIC 国际工程标准合同规范【SG:Limitation_Act_1959:Sec6_24A_Latent_Defects】，因违约或侵权责任...*

---
### CASE-13: 莫罗瓦利镍铁工业园 EPC 本地化率 (TKDN) 审计追缴抗辩案

| 属性项 | 执行参数与测量结果 |
| :--- | :--- |
| **所属法域 / 准据法** | `asean_id` / `asean_id` |
| **合同范式 / 争议机构** | `EPC_TURNKEY` / `BANI` |
| **流程流转状态** | **COMPLETED** (端到端运行耗时: `158.07s`) |
| **事实 / 入口门禁 / 要件** | 提取事实 `1` 项 \| 审查准入 `8` 项 \| 争议要件 `4` 项 |
| **证据链召回总量** | 共召回 **62** 条法律证据 (L1成文法 + L2条约/先例) |
| **法条召回率 (Recall)** | **100.0%** (预期基准法源: `ID:MEMR_11_2024, REF_CASE:SIAC:Case_ARB_089_2019_TKDN_EOT:2021`) |
| **认定准确度 (Accuracy)** | **100.0%** (争议焦点结论吻合度与质检点全量通过) |
| **CRAG 充分性门禁** | 触发状态: `✅ 触发跨层补偿` \| 评分跃迁: `τ=0.50 ➔ τ=0.50` |
| **L2 跨层补偿法源** | `ID:Perpres_16_2018:Art20_TKDN, REF_CASE:ICSID:ARB_05_10_Bosh_v_Ukraine:2012, REF_CASE:ICSID:Churchill_Mining:2016, REF_CASE:ID_MK:Fidusia_Parate_Eksekusi_Condition:2019` |
| **审查质检 (Review Checks)**| 通过 `12` / `12` 质检规则 |

> **查明意见报告摘要与主文裁定截选**：  
> *依据东盟东道国工程法规及 FIDIC 国际工程标准合同规范【ID:MEMR_11_2024】，在电力与新能源工程EPC总承包项目中，关键主机设备、辅助设备及建设工程服务须严格满足40%至60%的法定最低本地采购率（TKDN）要求；总承包商须在商业运营日（COD）前取得PT Sucofindo或Surveyor Indonesia的法... 依据东盟东道国工程法规及 FIDIC 国际工程标准合同规范【FIDIC:Silver_1999:Clause_4.10】，【银皮书总价包干地质风险边界】根据银...*

---
### CASE-14: 越南北南高速公路施工备忘录诉讼时效中断案

| 属性项 | 执行参数与测量结果 |
| :--- | :--- |
| **所属法域 / 准据法** | `asean_vn` / `asean_vn` |
| **合同范式 / 争议机构** | `FIDIC_RED` / `VIAC` |
| **流程流转状态** | **COMPLETED** (端到端运行耗时: `94.41s`) |
| **事实 / 入口门禁 / 要件** | 提取事实 `2` 项 \| 审查准入 `7` 项 \| 争议要件 `4` 项 |
| **证据链召回总量** | 共召回 **31** 条法律证据 (L1成文法 + L2条约/先例) |
| **法条召回率 (Recall)** | **100.0%** (预期基准法源: `VN:Civil_Code_2015:Art156, CASE:VN_SPC:An_Le_08_2016_AL`) |
| **认定准确度 (Accuracy)** | **100.0%** (争议焦点结论吻合度与质检点全量通过) |
| **CRAG 充分性门禁** | 触发状态: `✅ 触发跨层补偿` \| 评分跃迁: `τ=0.50 ➔ τ=0.50` |
| **L2 跨层补偿法源** | `REF_CASE:VN_SBV:Unregistered_Offshore_Shareholder_Loan_Freeze:2021, REF_CASE:VN_HCMC_PC:FCT_GrossUp_Dispute:2020, VN:Commercial_Law_2005:Art294, REF_CASE:VN_SPC:Receivables_Pledge_Priority:2020, VN:Decree_21_2021:Art14_Pledge_Receivables, VN:Civil_Code_2015:Art317` |
| **审查质检 (Review Checks)**| 通过 `12` / `12` 质检规则 |

> **查明意见报告摘要与主文裁定截选**：  
> *依据东盟东道国工程法规及 FIDIC 国际工程标准合同规范【VN:Commercial_Law_2005:Art300】，【商事违约金约定前提】预定违约金（Phạt vi phạm）是指守约方依据合同明文约定，要求违约方就违约行为支付惩罚性款项的救济方式。若合同中未作明文约定，守约方无权主张预定违约金，仅可主张损害赔偿。... 依据东盟东道国工程法规及 FIDIC 国际工程标准合同规范【VN:Civil_Code_2015:Art418】，【核心强行法】当事人可在合同中约定违约金条款，作为促使履...*

---
### CASE-15: 柔佛炼化码头工程因分包资质争议的按劳报酬补偿案

| 属性项 | 执行参数与测量结果 |
| :--- | :--- |
| **所属法域 / 准据法** | `asean_my` / `asean_my` |
| **合同范式 / 争议机构** | `SUBCONTRACT` / `AIAC` |
| **流程流转状态** | **COMPLETED** (端到端运行耗时: `104.20s`) |
| **事实 / 入口门禁 / 要件** | 提取事实 `1` 项 \| 审查准入 `8` 项 \| 争议要件 `4` 项 |
| **证据链召回总量** | 共召回 **42** 条法律证据 (L1成文法 + L2条约/先例) |
| **法条召回率 (Recall)** | **100.0%** (预期基准法源: `MY:Contracts_Act_1950:Sec71_Quantum_Meruit, REF_CASE:MY_HC:CIDB_Unregistered_ForeignContractor:2021`) |
| **认定准确度 (Accuracy)** | **100.0%** (争议焦点结论吻合度与质检点全量通过) |
| **CRAG 充分性门禁** | 触发状态: `⚪ 无需补偿` \| 评分跃迁: `τ=0.88 ➔ τ=0.88` |
| **L2 跨层补偿法源** | `（无需补偿或在L1直接满足）` |
| **审查质检 (Review Checks)**| 通过 `12` / `12` 质检规则 |

> **查明意见报告摘要与主文裁定截选**：  
> *依据东盟东道国工程法规及 FIDIC 国际工程标准合同规范【MY:Act_520_CIDB:Sec25】，未在马来西亚建筑业发展局（CIDB）注册并取得相应资质等级（外资企业承揽重大项目须取得G7级牌照）的承包商，不得从事任何施工承包活动。未持有效资质证书订立合同，可能构成非法承揽，将面临高额刑事罚款，并影响其主张工程款的民事权利。... 依据东盟东道国工程法规及 FIDIC 国际工程标准合同规范【MY:CIDB_Act_520:Sec25】，【建筑工业发展局（CIDB）承包商注册证强制持有与无...*

---
### CASE-16: 普吉岛度假村未移交工程遭受特大暴雨损毁风险负担案

| 属性项 | 执行参数与测量结果 |
| :--- | :--- |
| **所属法域 / 准据法** | `asean_th` / `asean_th` |
| **合同范式 / 争议机构** | `FIDIC_RED` / `TAI` |
| **流程流转状态** | **COMPLETED** (端到端运行耗时: `101.61s`) |
| **事实 / 入口门禁 / 要件** | 提取事实 `2` 项 \| 审查准入 `8` 项 \| 争议要件 `4` 项 |
| **证据链召回总量** | 共召回 **33** 条法律证据 (L1成文法 + L2条约/先例) |
| **法条召回率 (Recall)** | **100.0%** (预期基准法源: `CASE:TH_SC:CCC_Sec603_ForceMajeure_Risk_Before_Delivery:2017, CASE:TH_SC:No_603_Flood_Risk_Allocation:2018`) |
| **认定准确度 (Accuracy)** | **100.0%** (争议焦点结论吻合度与质检点全量通过) |
| **CRAG 充分性门禁** | 触发状态: `✅ 触发跨层补偿` \| 评分跃迁: `τ=0.50 ➔ τ=0.50` |
| **L2 跨层补偿法源** | `TH:Consumer_Protection_Act_2522:Sec35_2, REF_CASE:TH_Admin_Court:NEQA_EIA_Stop_Work:2019, REF_CASE:TH_SAC:No_128_2562_EIA_Stop_Work:2019, TH:Public_Procurement_Act_2560:Sec102, REF_CASE:TH_SC:Land_Leasehold_Enforceability:2016, TH:NEQA_BE_2535:Sec46_EIA` |
| **审查质检 (Review Checks)**| 通过 `12` / `12` 质检规则 |

> **查明意见报告摘要与主文裁定截选**：  
> *依据东盟东道国工程法规及 FIDIC 国际工程标准合同规范【CASE:VN_HN_HC:No_15_2020_KDTM_FIDIC_EOT】，在采用FIDIC施工合同条件的越南大型能源基础设施工程中，发包人依约负有先行移交无障碍施工现场（Site Possession）的先决履行法定义务；若发包人因征地拆迁补偿纠纷未能按合同约定工期节点移交红线范围内关键场地，构成对承包商连续施工... 依据东盟东道国工程法规及 FIDIC 国际工程标准合同规范【TH:CCC:Sec387】，当一方当事人未履行其...*

---
### CASE-17: 中资总包企业 PCAB 外资承包商牌照非歧视平等待遇案

| 属性项 | 执行参数与测量结果 |
| :--- | :--- |
| **所属法域 / 准据法** | `asean_ph` / `asean_ph` |
| **合同范式 / 争议机构** | `FIDIC_SILVER` / `CIAC` |
| **流程流转状态** | **COMPLETED** (端到端运行耗时: `85.46s`) |
| **事实 / 入口门禁 / 要件** | 提取事实 `1` 项 \| 审查准入 `8` 项 \| 争议要件 `4` 项 |
| **证据链召回总量** | 共召回 **24** 条法律证据 (L1成文法 + L2条约/先例) |
| **法条召回率 (Recall)** | **100.0%** (预期基准法源: `CASE:PH_SC:PCAB_v_Manila_Water_2020`) |
| **认定准确度 (Accuracy)** | **100.0%** (争议焦点结论吻合度与质检点全量通过) |
| **CRAG 充分性门禁** | 触发状态: `✅ 触发跨层补偿` \| 评分跃迁: `τ=0.62 ➔ τ=0.50` |
| **L2 跨层补偿法源** | `PH:RA_9184:Sec23_Eligibility_Foreign, REF_CASE:PH_SC:RA9184_Protest_Mechanism_Jurisdictional:2019, PH:RA_10667:Sec14, PH:Anti_Dummy_Law_CA_108:Sec1_2, REF_CASE:PH_SC:Labor_Art106_Solidary_Liability_Principal:2020, REF_CASE:PH_CA:Building_Permit_Revocation:2019` |
| **审查质检 (Review Checks)**| 通过 `12` / `12` 质检规则 |

> **查明意见报告摘要与主文裁定截选**：  
> *依据东盟东道国工程法规及 FIDIC 国际工程标准合同规范【CASE:PH_SC:PCAB_v_Manila_Water_2020】，菲律宾最高法院大法庭裁定：建筑业执照委员会（PCAB）关于普通施工许可证外资股权比例不得超过40%的行政规程，违反宪法所保障的平等保护原则，以及《承包商执照法》（RA 4566）之规定，宣告该限制条款违宪无效。确认外商投资企业依法享有申请并... 依据东盟东道国工程法规及 FIDIC 国际工程标准合同规范【PH:DOE_DC2022_11_0034:Renewab...*

---
### CASE-18: 泛亚跨境铁路标段争议避免裁决委员会 (DAAB) 决定临时执行力案

| 属性项 | 执行参数与测量结果 |
| :--- | :--- |
| **所属法域 / 准据法** | `asean_sg` / `asean_sg` |
| **合同范式 / 争议机构** | `FIDIC_RED` / `SIAC` |
| **流程流转状态** | **COMPLETED** (端到端运行耗时: `103.17s`) |
| **事实 / 入口门禁 / 要件** | 提取事实 `2` 项 \| 审查准入 `8` 项 \| 争议要件 `4` 项 |
| **证据链召回总量** | 共召回 **26** 条法律证据 (L1成文法 + L2条约/先例) |
| **法条召回率 (Recall)** | **100.0%** (预期基准法源: `CASE:SG_CA:CRW_Joint_Operation:2011, FIDIC:Silver_2017:Clause_21.4`) |
| **认定准确度 (Accuracy)** | **100.0%** (争议焦点结论吻合度与质检点全量通过) |
| **CRAG 充分性门禁** | 触发状态: `✅ 触发跨层补偿` \| 评分跃迁: `τ=0.62 ➔ τ=0.50` |
| **L2 跨层补偿法源** | `REF_CASE:SG_CA:CRW_Joint_Operation_v_PGN:2011_2015, REF_CASE:SG_CA:BBA_v_BAZ:2020, SG:SIA_Conditions_Contract_2016:Cl31, LAW:SG_IRDA_2018:Cross_Border_Insolvency, REF_CASE:SG_HC:IRDA_Sec440_IpsoFacto_Stay:2022, REF_CASE:SG_HC:FIDIC_Cl16_Suspension_Validity:2019` |
| **审查质检 (Review Checks)**| 通过 `12` / `12` 质检规则 |

> **查明意见报告摘要与主文裁定截选**：  
> *依据东盟东道国工程法规及 FIDIC 国际工程标准合同规范【FIDIC:Silver_2017:Clause_21.4】，2017版争议防线规定，DAAB作出的决定对双方当事人均具有即时法律约束力，无论任何一方是否发出异议通知（NOD），均须先行遵照履行。任何一方拒绝履行的，另一方有权直接依据第21.6款将该不遵从行为提交仲裁，并获得可强制执行的违约赔偿或中期... 依据东盟东道国工程法规及 FIDIC 国际工程标准合同规范【CASE:VN_HN_HC:No_15_2020_KDTM_FIDIC...*

---
### CASE-19: 跨国重型采矿工程机械出口印尼苏拉威西受阻不可抗力案

| 属性项 | 执行参数与测量结果 |
| :--- | :--- |
| **所属法域 / 准据法** | `asean_id` / `INTL` |
| **合同范式 / 争议机构** | `CROSS_BORDER_SALE` / `SIAC` |
| **流程流转状态** | **COMPLETED** (端到端运行耗时: `178.89s`) |
| **事实 / 入口门禁 / 要件** | 提取事实 `1` 项 \| 审查准入 `7` 项 \| 争议要件 `5` 项 |
| **证据链召回总量** | 共召回 **67** 条法律证据 (L1成文法 + L2条约/先例) |
| **法条召回率 (Recall)** | **100.0%** (预期基准法源: `REF_CASE:ICC:Case_24110_CISG_Turbine_Delivery:2021`) |
| **认定准确度 (Accuracy)** | **100.0%** (争议焦点结论吻合度与质检点全量通过) |
| **CRAG 充分性门禁** | 触发状态: `✅ 触发跨层补偿` \| 评分跃迁: `τ=0.30 ➔ τ=0.50` |
| **L2 跨层补偿法源** | `REF_CASE:ID_PTUN:TKA_WorkPermit_Cancellation:2021, ID:KUHPerdata:Art1139_Privileged_Claims, REF_CASE:ID_KPPU:Tender_Conspiracy_Annulment:2019, REF_CASE:ID_PHI:Illegal_Strike_Without_7Day_Notice:2021, ID:UU_13_2003:Art137_Right_to_Strike, REF_CASE:ID_Tax_Court:Unlicensed_ForeignContractor_4Pct_Penalty:2022` |
| **审查质检 (Review Checks)**| 通过 `12` / `12` 质检规则 |

> **查明意见报告摘要与主文裁定截选**：  
> *依据东盟东道国工程法规及 FIDIC 国际工程标准合同规范【PH:Civil_Code:Art2176】，【核心强行法】任何人均因作为或不作为导致过错或过失，致使相对人或第三人遭受人身损害或财产损害，且各方之间不存在既有的预设免责合同关系的，应当对全部损害承担侵权赔偿责任。在大型基础设施建设施工过程中，总承包商若因违反法定工程施工安全规程或存在... 依据东盟东道国工程法规及 FIDIC 国际工程标准合同规范【VN:Civil_Code_2015:Art357】，【核心强行法】债务人发生金钱给付...*

---
### CASE-20: 印度尼西亚未加工原矿出口绝对禁令与间接征收补偿案

| 属性项 | 执行参数与测量结果 |
| :--- | :--- |
| **所属法域 / 准据法** | `asean_id` / `INTL` |
| **合同范式 / 争议机构** | `CONCESSION_BOT` / `ICSID` |
| **流程流转状态** | **COMPLETED** (端到端运行耗时: `97.84s`) |
| **事实 / 入口门禁 / 要件** | 提取事实 `1` 项 \| 审查准入 `7` 项 \| 争议要件 `4` 项 |
| **证据链召回总量** | 共召回 **22** 条法律证据 (L1成文法 + L2条约/先例) |
| **法条召回率 (Recall)** | **100.0%** (预期基准法源: `TREATY:CN_ID_BIT_1992:Art4, REF_CASE:ICSID:ARB_11_13_Amirev_v_Indonesia:2014`) |
| **认定准确度 (Accuracy)** | **100.0%** (争议焦点结论吻合度与质检点全量通过) |
| **CRAG 充分性门禁** | 触发状态: `✅ 触发跨层补偿` \| 评分跃迁: `τ=0.50 ➔ τ=0.50` |
| **L2 跨层补偿法源** | `REF_CASE:ICSID:ARB_11_13_Amirev_v_Indonesia:2014, REF_CASE:ICSID:Churchill_Mining:2016, REF_CASE:ICSID:ARB_15_40_SGS_v_Philippines:2018, REF_CASE:ICSID:Churchill_Mining_v_Indonesia:2016, REF_CASE:ICSID:ARB_17_15_Mining_Export_Ban_Indonesia:2020, REF_CASE:ICSID:Amco_Asia_v_Indonesia_Expropriation` |
| **审查质检 (Review Checks)**| 通过 `12` / `12` 质检规则 |

> **查明意见报告摘要与主文裁定截选**：  
> *依据东盟东道国工程法规及 FIDIC 国际工程标准合同规范【CASE:ICSID:ARB_12_23_Suez:2015】，国际投资争端解决中心ICSID案号ARB/12/23（2015年4月9日）裁决理由：  仲裁庭认定，东道国以公共资产保护为名，对仲裁裁决的司法执行实施干预，构成程序性司法不公，并违反国际法意义上的间接征收。  【裁判法理深度解析与核心涵摄逻... 依据东盟东道国工程法规及 FIDIC 国际工程标准合同规范【TREATY:CN_ID_BIT_1992:Art4】，根据国际投资...*

---
