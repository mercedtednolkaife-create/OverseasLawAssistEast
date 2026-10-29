import sys
import os
import sqlite3

sys.path.insert(0, os.path.abspath("."))
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from lawagent.store.snapshots import SnapshotManager
from lawagent.store.graph import SQLiteGraphStore
from lawagent.store.retriever import HybridRetriever

def verify_all():
    print("=" * 70)
    print("🔍 东盟法源与判例全量扩充成果综合验收")
    print("=" * 70)

    mgr = SnapshotManager()
    snap_id = mgr.get_current_snapshot_id()
    snap_dir = os.path.join(mgr.base_dir, snap_id)
    db_path = os.path.join(snap_dir, "law.sqlite")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # 1. 规模统计
    cur.execute("SELECT count(*) FROM norms")
    n_norms = cur.fetchone()[0]
    cur.execute("SELECT count(*) FROM cases")
    n_cases = cur.fetchone()[0]
    cur.execute("SELECT count(*) FROM edges")
    n_edges = cur.fetchone()[0]
    cur.execute("SELECT count(*) FROM hot_norm_cases")
    n_hot = cur.fetchone()[0]
    cur.execute("SELECT count(*) FROM chunks")
    n_chunks = cur.fetchone()[0]
    cur.execute("SELECT count(*) FROM risk_communities")
    n_rc = cur.fetchone()[0]

    print(f"📊 数据库物理统计:")
    print(f"  • 成文法规范总数 (norms): {n_norms} (预期 106)")
    print(f"  • 裁判先例总数 (cases): {n_cases} (预期 30)")
    print(f"  • 拓扑对抗边总数 (edges): {n_edges} (预期 57)")
    print(f"  • 热门法条判例映射 (hot_norm_cases): {n_hot} (预期 32)")
    print(f"  • 风险社区总数 (risk_communities): {n_rc} (预期 12)")
    print(f"  • 知识库切块数 (chunks): {n_chunks} (预期 196)")

    assert n_norms == 106, f"Norms count mismatch: {n_norms} != 106"
    assert n_cases == 30, f"Cases count mismatch: {n_cases} != 30"
    assert n_edges == 57, f"Edges count mismatch: {n_edges} != 57"
    assert n_hot == 32, f"Hot norm cases mismatch: {n_hot} != 32"
    assert n_rc == 12, f"Risk communities mismatch: {n_rc} != 12"
    assert n_chunks == 196, f"Chunks count mismatch: {n_chunks} != 196"
    print("✓ 规模断言 100% 吻合！")

    # 2. 检查悬挂外键 (Dangling Edges)
    cur.execute("SELECT norm_id FROM norms")
    all_norm_ids = {r[0] for r in cur.fetchall()}
    cur.execute("SELECT case_id FROM cases")
    all_case_ids = {r[0] for r in cur.fetchall()}
    all_valid_ids = all_norm_ids.union(all_case_ids)

    cur.execute("SELECT src, dst, rel FROM edges")
    dangling_edges = []
    for src, dst, rel in cur.fetchall():
        if src not in all_valid_ids or dst not in all_valid_ids:
            dangling_edges.append((src, dst, rel))

    print(f"\n🔗 知识图谱悬挂边检查: {len(dangling_edges)} 条")
    if dangling_edges:
        print(f"❌ 发现悬挂边: {dangling_edges}")
    else:
        print(f"✓ 全图 {n_edges} 条拓扑关系边 100% 闭环，0 悬挂外键！")
    assert len(dangling_edges) == 0

    # 3. 检查 hot_norm_cases 映射完整性
    cur.execute("SELECT norm_id, case_id FROM hot_norm_cases")
    dangling_hot = []
    for n_id, c_id in cur.fetchall():
        if n_id not in all_norm_ids or c_id not in all_case_ids:
            dangling_hot.append((n_id, c_id))
    print(f"\n⚖️ 重点法条判例关联检查: {len(dangling_hot)} 处断裂")
    if dangling_hot:
        print(f"❌ 发现断裂 hot_cases: {dangling_hot}")
    else:
        print(f"✓ {n_hot} 组法条与金标准判例映射 100% 闭环！")
    assert len(dangling_hot) == 0

    # 4. 别名归一化与快速查询 (norm_lookup) 验收
    test_aliases = [
        ("VN_CIVIL_CODE:ART351", "VN:Civil_Code_2015:Art351"),
        ("VN_CIVIL_CODE:ART405", "VN:Civil_Code_2015:Art405"),
        ("MY_CONTRACTS:SEC75", "MY:Contracts_Act_1950:Sec75"),
        ("PH_EO1008:SEC4", "PH:EO_1008:Sec4"),
        ("FIDIC_SILVER:CLAUSE2.5", "FIDIC:Silver_1999:Clause_2.5"),
        ("FIDIC_SILVER_2017:CLAUSE21.4", "FIDIC:Silver_2017:Clause_21.4"),
        ("ID_LANGUAGE_LAW:ART31", "ID:UU_24_2009:Art31"),
        ("CN_TH_BIT:ART5", "TREATY:CN_TH_BIT_1985:Art5"),
        ("ID_LABOR:RPTKA", "ID:PP_34_2021:Art3"),
        ("ID_AMDAL:ART40", "ID:UU_32_2009:Art40"),
        ("TH_EIA:SEC50", "TH:NEQA_2535:Sec50"),
        ("FIDIC_SILVER:CLAUSE10.1", "FIDIC:Silver_1999:Clause_10.1"),
        ("CN_SG_BIT:ART6", "TREATY:CN_SG_BIT_1985:Art6"),
        # Phase 3 新增别名
        ("ID_KUHPERDATA:ART1266", "ID:KUHPerdata:Art1266"),
        ("FIDIC_SILVER:CLAUSE16.1", "FIDIC:Silver_1999:Clause_16.1"),
        ("FIDIC_SILVER:CLAUSE1.14", "FIDIC:Silver_1999:Clause_1.14"),
        ("MY_PARTNERSHIP:SEC11", "MY:Partnership_Act_1961:Sec11"),
        ("ID_STATE_TREASURY:ART50", "ID:UU_1_2004:Art50"),
        ("SG_STATE_IMMUNITY:SEC5", "SG:State_Immunity_Act:Sec5"),
        ("FIDIC_YELLOW:CLAUSE4.12", "FIDIC:Yellow_1999:Clause_4.12"),
        ("SG_MISREPRESENTATION:SEC2", "SG:Misrepresentation_Act:Sec2"),
        # Phase 4 别名
        ("VN_COMMERCIAL_LAW:ART301", "VN:Commercial_Law_2005:Art301"),
        ("TH_ARBITRATION:SEC40", "TH:Arbitration_Act_2545:Sec40"),
        ("PH_CIVIL_CODE:ART1229", "PH:Civil_Code:Art1229"),
        ("MY_CIPAA:SEC30", "MY:CIPAA_2012:Sec30"),
        ("SG_SOPA:SEC15", "SG:SOPA_2004:Sec15"),
        ("FIDIC_SILVER:CLAUSE8.7", "FIDIC:Silver_1999:Clause_8.7"),
    ]
    print("\n🏷️ 规范别名解析测试:")
    for alias, expected in test_aliases:
        res = mgr.norm_lookup(alias, snap_id)
        assert res is not None and res["norm_id"] == expected, f"Lookup failed for {alias}: got {res}"
        print(f"  • {alias:30s} -> {res['norm_id']} ({res['title'][:30]}...)")
    print("✓ 别名归一化 100% 正确！")

    # 5. GraphRAG 混合检索与拓扑穿透实测
    print("\n🧠 GraphRAG 智能检索与多跳推理端到端实测:")
    retriever = HybridRetriever(mgr)

    test_queries = [
        {
            "title": "菲律宾建筑工程 CIAC 专属管辖权排他裁判",
            "q": "菲律宾工程总承包中约定境外 SIAC 仲裁是否会被当地法院推翻？CIAC 专属管辖权强行法依据与最高法院判例是什么？",
            "expect_norms": ["PH:EO_1008:Sec4"],
            "expect_cases": ["CASE:PH_SC:Hutama_RSEA:2018"]
        },
        {
            "title": "马来西亚延误违约金合理性举证责任倒置",
            "q": "马来西亚 EPC 项目发包人主张延误违约金 LDs 时是否需要举证证明客观实际损失？Cubic Electronics 联邦法院判例与合同法第75条规则",
            "expect_norms": ["MY:Contracts_Act_1950:Sec75"],
            "expect_cases": ["CASE:MY_FC:CubicElectronics:2019"]
        },
        {
            "title": "越南弃光限电格式免责条款自始无效抗辩",
            "q": "越南国家电力公司 EVN 在 PPA 协议中订立弃光限电无偿豁免条款是否有效？民法典第405条与电力法第28条消纳义务",
            "expect_norms": ["VN:Civil_Code_2015:Art405", "VN:Law_28_2004:Art28"],
            "expect_cases": ["CASE:VN_Hanoi_HC:EPC_Dispute:2020"]
        },
        {
            "title": "印尼涉外合同语言法合规与 SIAC 裁决中雅加达法院执行许可",
            "q": "中资企业在印尼签署纯英文 EPC 合同是否有效？2009年第24号法律第31条、最高法院 SEMA 3/2023 及 SIAC 裁决 Exequatur 执行判例",
            "expect_norms": ["ID:UU_24_2009:Art31", "ID:SEMA_3_2023", "ID:UU_30_1999:Art66"],
            "expect_cases": ["CASE:ID_PN_JakPus:Exequatur_SIAC:2022"]
        },
        {
            "title": "印尼光伏电站总包未批先用中国技术工人导致移民局查封营地停工",
            "q": "中资总包未依法取得 RPTKA 及工作签证导致技术工人被印尼移民局遣返停工，PP 34/2021 法规与最高院不可抗力驳回判例",
            "expect_norms": ["ID:PP_34_2021:Art3"],
            "expect_cases": ["CASE:ID_MA:LaborShutdown:2020"]
        },
        {
            "title": "泰国基建项目因环保诉讼导致 EIA 环评撤销停工政府赔偿责任",
            "q": "泰国工业港口工程因环保组织起诉环境影响评估 EIA 程序瑕疵被法院勒令停工，NEQA 第50条与最高行政法院赔偿特许经营商利息判例",
            "expect_norms": ["TH:NEQA_2535:Sec50"],
            "expect_cases": ["CASE:TH_SAC:EIA_Suspension:2017"]
        },
        {
            "title": "菲律宾光伏电站发包人提前并网商业发电构成 FIDIC 推定接收",
            "q": "菲律宾光伏电站发包人未经出具 TOC 证书提前商业并网发电，FIDIC 第10.1款推定工程接收与 CIAC 阻断延误违约金判例",
            "expect_norms": ["FIDIC:Silver_1999:Clause_10.1"],
            "expect_cases": ["CASE:PH_CIAC:DeemedTakingOver:2016"]
        },
        {
            "title": "FIDIC 争端裁决委员会 DAB 决定独立违约可仲裁终审判例",
            "q": "新加坡终审法院关于 FIDIC 第20.4款 DAB 裁决拒不遵从能否独立申请终局仲裁裁决强制执行，CRW 案判例",
            "expect_norms": ["FIDIC:Silver_1999:Clause_20.4"],
            "expect_cases": ["CASE:SG_CA:CRW_DAB_Final:2015"]
        },
        {
            "title": "印尼工程合同解除经法院裁决强行法与自愿弃权条款效力",
            "q": "印尼工程总包单方解约撤场是否受民法典第1266条经法院判决强制管辖，最高法院关于合同自愿放弃1266条有效性终审判决",
            "expect_norms": ["ID:KUHPerdata:Art1266"],
            "expect_cases": ["CASE:ID_MA:Waive1266_Termination:2018"]
        },
        {
            "title": "马来西亚联营体工程伙伴违约合伙人连带责任与追偿",
            "q": "马来西亚 EPC 项目联合体本地伙伴破产违约，FIDIC 第1.14款连带责任与1961年合伙法第11条清偿与追偿规则",
            "expect_norms": ["FIDIC:Silver_1999:Clause_1.14", "MY:Partnership_Act_1961:Sec11"],
            "expect_cases": []
        },
        {
            "title": "涉外裁决执行中东道国国有资产执行豁免屏障与商业例外抗辩",
            "q": "印尼或菲律宾国有水务及电网公司主张主权资产执行豁免，印尼国家金库法第50条与新加坡国家豁免法第5条商业交易例外判例",
            "expect_norms": ["ID:UU_1_2004:Art50", "SG:State_Immunity_Act:Sec5"],
            "expect_cases": ["CASE:PH_SC:MWSS_v_Consortium:2019"]
        },
        {
            "title": "FIDIC 银皮书现场地质资料隐瞒与虚假陈述刺破固定总价",
            "q": "FIDIC 银皮书第4.10款现场数据与新加坡虚假陈述法第2条，发包人隐瞒不利地质报告能否刺破 EPC 总价包干索赔工期窝工",
            "expect_norms": ["FIDIC:Silver_1999:Clause_4.10", "SG:Misrepresentation_Act:Sec2"],
            "expect_cases": ["CASE:MY_FC:Bumi_Geotechnical:2017"]
        },
        {
            "title": "越南商业法第301条法定8%违约金上限与FIDIC延误违约金强制压降",
            "q": "越南大型光伏电站总承包中发包人依 FIDIC 专用条件主张扣除 10% 延误违约金，商业法第301条法定8%上限强行法抗辩与河内高级法院判决",
            "expect_norms": ["VN:Commercial_Law_2005:Art301"],
            "expect_cases": ["CASE:VN_Hanoi_HC:PenaltyCap_8Pct:2021"]
        },
        {
            "title": "菲律宾建筑工程违约金过高民法典第1229条衡平酌减标杆判例",
            "q": "菲律宾工程发包人以工期滞后为由主张全额扣除高额日计违约金，民法典第1229条显失公平衡平酌减与最高法院 Ligutan 先例",
            "expect_norms": ["PH:Civil_Code:Art1229"],
            "expect_cases": ["CASE:PH_SC:Ligutan_LD_Reduction:2002"]
        },
        {
            "title": "马来西亚分包商依据 CIPAA 第30条向发包人申请直接支付",
            "q": "马来西亚 EPC 项目分包商取得 CIPAA 裁决后总包未履行，依据第30条向发包人直接付款请求与联邦法院 CTCI 案裁判规则",
            "expect_norms": ["MY:CIPAA_2012:Sec30"],
            "expect_cases": ["CASE:MY_FC:CTCI_CIPAA_DirectPay:2020"]
        }
    ]

    for idx, tq in enumerate(test_queries, 1):
        print(f"\n--- 测试用例 {idx}: {tq['title']} ---")
        evidences = retriever.search(tq["q"], top_k=6, snapshot_id=snap_id)
        recalled_ref_ids = [ev.ref_id for ev in evidences]

        print(f"  • 召回 Evidence 总数: {len(evidences)}")
        print(f"  • 核心命中 ref_ids: {recalled_ref_ids}")

        # 断言期望的法条或判例至少有核心命中
        for exp_n in tq["expect_norms"]:
            assert any(exp_n in ref for ref in recalled_ref_ids), f"Expected norm {exp_n} not recalled in query {idx}!"
            print(f"    ✓ 成功命中法条: {exp_n}")
        for exp_c in tq["expect_cases"]:
            assert any(exp_c in ref for ref in recalled_ref_ids), f"Expected case {exp_c} not recalled in query {idx}!"
            print(f"    ✓ 成功命中判例: {exp_c}")

    conn.close()
    print("\n" + "=" * 70)
    print("🏆 恭喜！东盟六国与 FIDIC 数据库扩充及 GraphRAG 全链路验证 100% 通过！")
    print("=" * 70)

if __name__ == "__main__":
    verify_all()
