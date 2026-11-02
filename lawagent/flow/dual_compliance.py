# -*- coding: utf-8 -*-
"""中-东盟双向合规审查与法域冲突消解引擎 (DualComplianceEngine)
对齐《功能优化及审查.md》第一部分核心技术规范：
1. 投资准入与双边审批互锁算子 (evaluate_dual_investment_access)
2. 跨境融资担保与外汇闭环算子 (evaluate_dual_guarantee_fx)
3. 数据跨境与技术出口双向管制算子 (evaluate_dual_data_and_export_control)
4. 工程分包、本地化配额与劳工双向合规算子 (evaluate_dual_epc_execution)
5. 出险保全与争端救济双向联动算子 (evaluate_dual_dispute_sinosure)
"""

from typing import List, Dict, Any, Optional
from lawagent.core.types import CaseState, DualComplianceItem, DualComplianceAudit


class DualComplianceEngine:
    """中-东盟双向合规审查与冲突消解引擎"""

    @classmethod
    def evaluate(cls, state: CaseState) -> DualComplianceAudit:
        items: List[DualComplianceItem] = []

        items.extend(cls.evaluate_dual_investment_access(state))
        items.extend(cls.evaluate_dual_guarantee_fx(state))
        items.extend(cls.evaluate_dual_data_and_export_control(state))
        items.extend(cls.evaluate_dual_epc_execution(state))
        items.extend(cls.evaluate_dual_dispute_sinosure(state))

        # 计算得分与冲突计数
        collision_count = sum(1 for it in items if it.status == "collision")
        violations = sum(1 for it in items if it.status == "violation")
        warnings = sum(1 for it in items if it.status == "warning")

        # 100分基准倒扣分制
        prc_score = max(0.0, 100.0 - (violations * 15.0) - (warnings * 5.0) - (collision_count * 10.0))
        host_score = max(0.0, 100.0 - (violations * 10.0) - (warnings * 5.0) - (collision_count * 8.0))

        # 梳理审批流互锁链 (Approval Chain)
        jur = (state.meta.jurisdiction or "asean_id").replace("asean_", "").upper()
        approval_chain = cls._build_approval_chain(jur)

        # 汇总综述
        summary_zh = (
            f"中-东盟双向合规核验完成：发现 {collision_count} 处母国与东道国强行法冲突碰撞点，"
            f"{warnings} 处合规关注项。中方合规指数: {prc_score:.1f}，东道国属地合规指数: {host_score:.1f}。"
        )

        return DualComplianceAudit(
            prc_score=prc_score,
            host_score=host_score,
            collision_count=collision_count,
            items=items,
            approval_chain=approval_chain,
            summary_zh=summary_zh
        )

    @classmethod
    def evaluate_dual_investment_access(cls, state: CaseState) -> List[DualComplianceItem]:
        """1. 投资准入与双边审批互锁算子"""
        items: List[DualComplianceItem] = []
        jur = (state.meta.jurisdiction or "asean_id").replace("asean_", "").upper()
        full_text = f"{state.facts_zh or ''} {state.claims_zh or ''} {' '.join(state.meta.parties or [])}"

        is_investment = (
            state.meta.lifecycle_stage == "pre_investment"
            or any(w in full_text for w in ["投资", "并购", "特许权", "股权", "SPV", "设立公司", "出资"])
        )

        eng_params = getattr(state.meta, "engineering_params", {}) or {}
        declared_equity = eng_params.get("declared_equity_pct")

        if is_investment:
            # 互锁冲突检测：先有鸡还是先有蛋困境
            # 国内发改委11号令与东道国公司设立/特许权审批互锁
            items.append(DualComplianceItem(
                dimension="投资准入与双边审批",
                side="bidirectional_conflict",
                status="collision",
                rule_code="DC_ACCESS_INTERLOCK_01",
                title_zh="发改委11号令境外投资备案与东道国特许权/公司设立先决条件互锁冲突",
                prc_statute="CN:NDRC_Order_11:Art13_14",
                host_statute=f"{jur}:Law_on_Investment" if jur != "ID" else "ID:UU_25_2007:Art7_Expropriation",
                collision_desc="中方发改委11号令与商务部3号令要求在项目交割或对外签署拘束性投资协议前取得ODI备案，否则外汇无法汇出；但东道国（如印尼OSS-RBA、越南IRC/ERC、老挝CA特许权、东帝汶Visto）常要求先设立属地项目实体并注资验资才颁发许可证。",
                mitigation_clause_zh="《附双方法定审批生效先决条件条款》：双方确认本协议自中方完成国家发改委境外投资备案（ODI）且东道国投资主管机关颁发正式准入许可之日起生效；任何一方未获本国监管批准不承担缔约过失责任。",
                action_guidance="在主合同或合资备忘录中明确将双边监管批文设为并列且独立的法定生效先决条件（Conditions Precedent）。"
            ))

            # 中方国资委35号令非主业投资负面清单
            items.append(DualComplianceItem(
                dimension="投资准入与双边审批",
                side="prc_outbound",
                status="pass",
                rule_code="DC_ACCESS_SASAC_35",
                title_zh="国资委35号令央企境外主业投资合规核验",
                prc_statute="CN:SASAC_Order_35:Art12",
                host_statute=None,
                collision_desc=None,
                mitigation_clause_zh=None,
                action_guidance="确保本项目属于集团向国资委报备的境外主业范畴，未列入境外投资禁止类负面清单。"
            ))

        if declared_equity is not None and declared_equity > 49.0:
            items.append(DualComplianceItem(
                dimension="投资准入与双边审批",
                side="host_country",
                status="collision" if declared_equity > 70.0 else "warning",
                rule_code="DC_ACCESS_EQUITY_CAP",
                title_zh=f"东道国外资持股比例红线审查（当前申报: {declared_equity}%）",
                prc_statute="CN:NDRC_Order_11:Art14",
                host_statute=f"{jur}:Foreign_Investment_Negative_List",
                collision_desc=f"东道国关键基础设施或受限领域设有限制（通常持股上限49%），申报持股比例达 {declared_equity}%，若未获特别豁免，面临属地投资审查驳回或股权代持穿透无效法律风险。",
                mitigation_clause_zh="《股权分步交割与无投票权优先股合规条款》：双方同意首期交割外资持股比例严格恪守法定上限49%，溢出部分通过符合东道国公司法的无投票权优先股或可转债方式落实合法投资权益。",
                action_guidance="核实东道国最新外资负面清单及特别豁免政策，杜绝通过无有效保护的影子代持架构规避外资审查。"
            ))

        return items

    @classmethod
    def evaluate_dual_guarantee_fx(cls, state: CaseState) -> List[DualComplianceItem]:
        """2. 跨境融资担保与外汇闭环算子"""
        items: List[DualComplianceItem] = []
        full_text = f"{state.facts_zh or ''} {state.claims_zh or ''} {state.meta.contract_type or ''}"

        has_guarantee = any(w in full_text for w in ["担保", "母公司担保", "PCG", "保函", "内保外贷", "联营体", "KSO", "合资"])

        if has_guarantee:
            # 国资委75号文严禁超股比担保 vs 东道国连带责任
            items.append(DualComplianceItem(
                dimension="融资担保与外汇管制",
                side="bidirectional_conflict",
                status="collision",
                rule_code="DC_GUARANTEE_OVERCAP_02",
                title_zh="国资委75号令严禁超股比担保与东道国联营体对外连带责任冲突",
                prc_statute="CN:SASAC_Notice_75_2021:Guarantee_Risk",
                host_statute="ID:UU_2_2017:Art57" if "ID" in full_text else "FIDIC:Silver_1999:Clause_4.2",
                collision_desc="东盟项目业主（特别是印尼KSO合资或EPC银团）常要求中方总包母公司提供100%全额母公司履约担保（PCG）；但国资委75号文严禁央企对非全资控股主体提供超股权比例担保，直接面临国资合规处罚。",
                mitigation_clause_zh="《按股比分割独立保函与反担保联动条款》：各方同意母公司保证责任严格按各自持股比例（49%:51%）分别开立不可撤销独立保函；外方伙伴须通过第一流国际商业银行向中方出具不可撤销无条件见索即付反担保（Counter-Guarantee）。",
                action_guidance="杜绝签署任何形式的非对称连带保证合同，建立离岸资金托管（Escrow Account）或要求外方出具背对背银行保函。"
            ))

            # 外管局29号文内保外贷登记
            items.append(DualComplianceItem(
                dimension="融资担保与外汇管制",
                side="prc_outbound",
                status="warning",
                rule_code="DC_SAFE_29_REGISTRATION",
                title_zh="外管局29号文内保外贷15个工作日法定登记时效",
                prc_statute="CN:SAFE_Notice_29_2014:Crossborder_Security",
                host_statute=None,
                collision_desc=None,
                mitigation_clause_zh="《外汇登记合规履行条款》：担保人应在担保合同签订之日起15个工作日内向外汇局办理内保外贷签约登记，受益人须配合提供必要之项目证明文件。",
                action_guidance="担保合同签署后15日内必须完成外管局系统报备，否则发生索赔时外汇无法合规购汇汇出。"
            ))

        return items

    @classmethod
    def evaluate_dual_data_and_export_control(cls, state: CaseState) -> List[DualComplianceItem]:
        """3. 数据跨境与技术出口双向管制算子"""
        items: List[DualComplianceItem] = []
        full_text = f"{state.facts_zh or ''} {state.claims_zh or ''}"

        has_data_or_tech = any(w in full_text for w in [
            "调证", "数据", "测绘", "图纸", "源码", "发现程序", "Discovery", "出口管制", "两用物项", "EAR", "技术转让"
        ])

        if has_data_or_tech:
            # 数安法第36条 vs 境外仲裁/法院调证令
            items.append(DualComplianceItem(
                dimension="数据出境与出口管制",
                side="bidirectional_conflict",
                status="collision",
                rule_code="DC_DATA_ART36_DISCOVERY_03",
                title_zh="《数据安全法》第36条境内数据司法保护与境外仲裁证据开示令冲突",
                prc_statute="CN:Data_Security_Law:Art36",
                host_statute="SG:IAA_Cap_143A:Sec12A",
                collision_desc="境外仲裁庭或外国法院签发证据开示令（Discovery Order）要求提供工程底层地质、电网调度数据；而中国《数据安全法》第36条与《国际刑事司法协助法》明确规定非经中方主管机关批准严禁向外国司法/执法机构提供境内数据，直接形成二难困境。",
                mitigation_clause_zh="《涉密数据主权豁免与仲裁保护令申请条款》：当事人确认受中国《数据安全法》第36条强行法约束，任何证据交换须经脱敏处理；当事人同意向仲裁庭共同申请保护令（Protective Order）并以独立第三方专家在华验证替代直接出境。",
                action_guidance="第一时间向司法部及行业主管部委提交紧急依职权审批申请，同步向仲裁庭提交主权法律冲突抗辩并申请保护令。"
            ))

            # 中方两用物项与技术出口管制
            items.append(DualComplianceItem(
                dimension="数据出境与出口管制",
                side="prc_outbound",
                status="warning",
                rule_code="DC_EXPORT_CONTROL_PRC",
                title_zh="《出口管制法》两用物项与特种技术出境前置许可核验",
                prc_statute="CN:Export_Control_Law_2020:Art12_44",
                host_statute=None,
                collision_desc=None,
                mitigation_clause_zh=None,
                action_guidance="核查出口设备与技术是否落入两用物项管制清单，杜绝未经商务部许可证擅自向境外实体移交。"
            ))

        return items

    @classmethod
    def evaluate_dual_epc_execution(cls, state: CaseState) -> List[DualComplianceItem]:
        """4. 工程分包、本地化配额与劳工双向合规算子"""
        items: List[DualComplianceItem] = []
        jur = (state.meta.jurisdiction or "asean_id").replace("asean_", "").upper()
        full_text = f"{state.facts_zh or ''} {state.claims_zh or ''}"
        eng_params = getattr(state.meta, "engineering_params", {}) or {}
        declared_tkdn = eng_params.get("declared_tkdn_pct")

        # 马来 CIPAA 35条 / 新加坡 SOPA 9条 禁止背靠背条款
        if any(w in full_text for w in ["背靠背", "pay-when-paid", "pay when paid", "分包", "cipaa", "sopa"]) or jur in ["MY", "SG"]:
            items.append(DualComplianceItem(
                dimension="分包工程与本地化劳工",
                side="host_country",
                status="warning",
                rule_code="DC_EPC_BACK_TO_BACK_VOID",
                title_zh="马来西亚CIPAA/新加坡SOPA背靠背付款条款法定绝对无效",
                prc_statute=None,
                host_statute="MY:CIPAA_2012:Sec35" if jur == "MY" else "SG:SOPA_2004:Sec9",
                collision_desc="中资总包商若在分包合同中约定以业主付款为前提支付分包款（Pay-when-paid），在马/新属地成文法下被判定绝对无效，分包商可直接通过法定审裁追讨到期款并强制执行利息。",
                mitigation_clause_zh="《合规分包付款节点与审裁排除示范条款》：总承包商应将付款节点设定为以具体里程碑验收合格为准，并约定独立的工程款对账核查期，避免使用触发CIPAA/SOPA法定无效的附条件支付措辞。",
                action_guidance="全面清理存量分包合同中的背靠背付款条款，防范分包商依据东道国法定审裁程序实施保全扣划。"
            ))

        # 印尼 TKDN 本地化率合规
        if "ID" in jur or "tkdn" in full_text.lower():
            items.append(DualComplianceItem(
                dimension="分包工程与本地化劳工",
                side="host_country",
                status="warning",
                rule_code="DC_EPC_TKDN_AUDIT",
                title_zh="印尼能源矿产部MEMR 11/2024电力工程TKDN本地化率达标审查",
                prc_statute=None,
                host_statute="ID:MEMR_11_2024",
                collision_desc="未达标印尼属地化率（TKDN）将面临审计追缴5%~10%惩罚性扣款，且无法取得商业运营COD证书。",
                mitigation_clause_zh="《TKDN前置联合验资与不可抗力调减条款》：因东道国国内产业链短缺导致本地设备无法采购的，总包商有权向业主申请豁免调减TKDN基准指标。",
                action_guidance="委托权威机构（如Sucofindo）进行采购前置预核验并保留完备属地供应链发票凭证。"
            ))

        # 申报 TKDN 本地化率不足
        if declared_tkdn is not None and declared_tkdn < 40.0:
            items.append(DualComplianceItem(
                dimension="分包工程与本地化劳工",
                side="host_country",
                status="collision" if declared_tkdn < 30.0 else "warning",
                rule_code="DC_EPC_TKDN_DEFICIT",
                title_zh=f"本地化率（TKDN）不达标追缴预警（当前申报: {declared_tkdn}%）",
                prc_statute=None,
                host_statute="ID:MEMR_11_2024" if "ID" in jur else f"{jur}:Local_Content_Regulation",
                collision_desc=f"当前申报本地化率仅为 {declared_tkdn}%，低于东道国成文法或招标文件要求的40%基准红线，面临巨额惩罚性扣款及COD验收受阻。",
                mitigation_clause_zh="《本地化率属地采购替代与不可抗力豁免条款》：总承包商应制定分阶段属地化采购替代清单，并明确约定东道国本土供应链产能短缺情形下的指标调减机制。",
                action_guidance="委托具备属地法定验资资质的第三方机构（如PT Sucofindo）提前核验发票，防范结算审计罚金。"
            ))

        # 越南：第15/2021/ND-CP号法令 第103条 外国承包商许可证（FLC）
        if "VN" in jur or "越南" in full_text or "vietnam" in full_text.lower():
            items.append(DualComplianceItem(
                dimension="分包工程与本地化劳工",
                side="host_country",
                status="warning",
                rule_code="DC_EPC_VN_CONTRACTOR_PERMIT",
                title_zh="越南建设部Decree 15/2021外国承包商许可证（FLC）强制准入核验",
                prc_statute=None,
                host_statute="VN:Decree_15_2021_ND_CP:Art103",
                collision_desc="依据越南第15/2021/ND-CP号法令第103条，外国承包商在越南开展工程承包必须与越方本土承包商组成联营体或使用越方分包商，并在实质性签约与施工前取得建设厅（DOC）颁发的外国承包商许可证，否则合同无效并面临行政停工。",
                mitigation_clause_zh="《外国承包商许可证取得与开工先决条件条款》：本合同签署后，双方共同配合向项目所在地建设行政部门提报申请材料，以承包商取得正式外国承包商许可证作为实质开工的前提先决条件。",
                action_guidance="在中标后15日内与本土联营体伙伴完成文件公证认证并提报DOC核发FLC执照。"
            ))

        # 菲律宾：PCAB承包商特别许可（RA 4566）
        if "PH" in jur or "菲律宾" in full_text or "philippines" in full_text.lower():
            items.append(DualComplianceItem(
                dimension="分包工程与本地化劳工",
                side="host_country",
                status="warning",
                rule_code="DC_EPC_PH_PCAB_LICENSE",
                title_zh="菲律宾PCAB承包商特别许可（Special License RA 4566）核验",
                prc_statute=None,
                host_statute="PH:RA_4566:Contractors_License_Law",
                collision_desc="依据菲律宾共和国第4566号法案（RA 4566），外资承包商必须依法向菲律宾承包商认可委员会（PCAB）申请单项工程特别执照（Special License），且必须委任常驻合资格法定授权代表（STE），未持牌展业构成违法施工。",
                mitigation_clause_zh="《PCAB特别许可取得及STE指定示范条款》：总承包商应在进场前取得PCAB有效特别许可，业主须配合出具项目立项与授标凭证，因许可审批行政延误导致的工期由业主予以合理展延。",
                action_guidance="提前3个月向PCAB准备合资格技术人员（STE）资历认证与外资施工特别执照申请材料。"
            ))

        # 泰国：外商经营法（FBA B.E. 2542 附表三建筑工程限制）
        if "TH" in jur or "泰国" in full_text or "thailand" in full_text.lower():
            items.append(DualComplianceItem(
                dimension="分包工程与本地化劳工",
                side="host_country",
                status="warning",
                rule_code="DC_EPC_TH_FBA_RESTRICTION",
                title_zh="泰国《外商经营法》(FBA B.E.2542)附表三施工建筑外资准入限制核验",
                prc_statute=None,
                host_statute="TH:Foreign_Business_Act_1999:Schedule_3_Art10",
                collision_desc="泰国《外商经营法》附表三第10条规定建筑工程属于限制外国人经营的行业，除非获得投资促进委员会（BOI）特别优惠证书或取得商业部外商经营许可证（FBL），否则外资持股比例不得达到或超过50%。",
                mitigation_clause_zh="《BOI投资促进证书前置或FBL许可示范条款》：双方确认本工程承包合同以承包商取得泰国BOI投资促进批准或商业发展厅（DBD）颁发的FBL外商经营许可证为生效前置要件。",
                action_guidance="核验是否具备BOI特许资质或通过与合规泰资控股伙伴组建KSO联合体方式合法展业。"
            ))

        return items

    @classmethod
    def evaluate_dual_dispute_sinosure(cls, state: CaseState) -> List[DualComplianceItem]:
        """5. 出险保全与争端救济双向联动算子"""
        items: List[DualComplianceItem] = []
        jur = (state.meta.jurisdiction or "asean_id").replace("asean_", "").upper()
        full_text = f"{state.facts_zh or ''} {state.claims_zh or ''}"

        # 中信保30日出险报损时效与FIDIC 28天通知双轨互锁
        items.append(DualComplianceItem(
            dimension="争议救济与信保出险",
            side="bidirectional_conflict",
            status="warning",
            rule_code="DC_DISPUTE_SINOSURE_FIDIC_05",
            title_zh="中国信保30日出险报损窗口期与合同28天索赔时效双轨互锁",
            prc_statute="SINOSURE:Overseas_Policy:Art15",
            host_statute="FIDIC:Silver_1999:Clause_20.1",
            collision_desc="FIDIC第20.1款规定承包商知悉延误后28天内须发索赔通知，否则丧失索赔权；而中国信保保单要求在被保险人知晓可能出险事故之日起30天内向信保发出正式《可能损失通知书》，未经信保同意严禁私自签署放弃权益协议。",
            mitigation_clause_zh="《代位求偿权保留与信保出险联动报备条款》：当发生业主拖欠或保函索兑险情时，承包商在向工程师发出工期/费用索赔通知的同时，须于30日内同步向中国信保递交报损预警并保全代位求偿权证据链。",
            action_guidance="建立双向时效日历，严格在28天合同窗口与30天信保窗口内同步闭环发函。"
        ))

        return items

    @classmethod
    def _build_approval_chain(cls, jur: str) -> List[Dict[str, str]]:
        """构建中-东盟全流程法定双边审批链条"""
        return [
            {
                "step": "第一阶段 · 境外投资立项",
                "authority": "国家发改委 (NDRC)",
                "item": "境外投资项目敏感类核准 / 非敏感类备案 (11号令)",
                "timing": "项目主协议签署或对外投资实施前",
                "risk_consequence": "未经核准/备案擅自出海面临发改委责令中止或停止实施、通报批评及纳入严重失信清单",
                "status": "必须于签约交割前完成"
            },
            {
                "step": "第二阶段 · 境外投资证书",
                "authority": "商务部 (MOFCOM)",
                "item": "企业境外投资证书 (ODI 商务备案)",
                "timing": "取得发改委备案证明后、外汇汇出前",
                "risk_consequence": "未取得境外投资证书无法完成银行真实性审核，资金无法合法合规购汇跨境划转",
                "status": "资金汇出前置法定必备"
            },
            {
                "step": "第三阶段 · 跨境担保与外汇登记",
                "authority": "国家外汇管理局 (SAFE)",
                "item": "直接投资外汇登记与跨境担保/内保外贷登记 (29号文/37号文)",
                "timing": "担保合同签署之日起15个工作日内 / 资金出境前",
                "risk_consequence": "逾期未登记导致境外担保履约款无法购汇对外支付，面临涉外汇违法处罚",
                "status": "15个工作日法定登记时效"
            },
            {
                "step": "第四阶段 · 属地执照与特许准入",
                "authority": f"东道国主管机构 ({jur} BKPM/BOI/MIDA/PCAB)",
                "item": "外商投资许可 / 施工总包特别牌照 / 特许经营准入",
                "timing": "项目实质开工、进场施工或商业运营前",
                "risk_consequence": "无牌展业或违反负面清单直接导致合同无效、行政查封及巨额连带罚款",
                "status": "东道国实体合法展业前置"
            },
            {
                "step": "第五阶段 · 阻断报告与信保报损",
                "authority": "商务部阻断机制 / 中国信保 (Sinosure)",
                "item": "《阻断办法》情况报告 / 信保30日出险报损通知",
                "timing": "知悉单边长臂限制或出险事实之日起30日内",
                "risk_consequence": "未履行报告导致丧失国内司法追偿保护，逾期报损将遭信保拒赔",
                "status": "遇涉外长臂或出险法定触发"
            }
        ]
