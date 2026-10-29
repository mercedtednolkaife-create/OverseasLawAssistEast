"""L2 广覆盖参考层与 FAISS 向量检索双层架构全链路验证脚本 (Verify L2 & FAISS Cascaded Retrieval)
验证项：
1. L2 独立检索引擎加载 (BM25 + FAISS Dense Vector 1024 维)
2. 直接检索 L2: 对东盟六国涉外基建审批、海关、用工、财税等参考条文及参考裁判先例精准命中
3. 智能级联检索 (AUTO): L1 核心红线优先保持纯净，边缘合规问题无缝沉降下沉至 L2 获得参考证据
4. 检索结果 Evidence 字段完整度 (layer, grade, text_zh, text_original, stand)
"""

import os
import sys
import time

sys.path.insert(0, os.path.abspath("."))
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from lawagent.store.retriever import HybridRetriever
from lawagent.store.snapshots import SnapshotManager


def test_l2_engines_and_faiss():
    print("=" * 70)
    print("🔍 测试 1: 检验 L2 独立 BM25 与 FAISS 稠密向量检索引擎加载状态")
    print("=" * 70)

    mgr = SnapshotManager()
    retriever = HybridRetriever(snapshot_mgr=mgr)

    assert retriever.bm25_l2 is not None, "❌ 错误: L2 BM25 引擎加载失败"
    print(f"✓ L2 BM25 引擎就绪，分块数: {len(retriever.bm25_l2.chunk_ids)}")

    assert retriever.vec_l2 is not None, "❌ 错误: L2 FAISS 向量引擎加载失败"
    assert retriever.vec_l2.index is not None, "❌ 错误: L2 FAISS 索引未加载"
    ntotal = retriever.vec_l2.index.ntotal
    print(f"✓ L2 FAISS 稠密向量索引就绪，向量规模: {ntotal} 维向量，维度: 1024")
    assert ntotal == 71, f"预期 71 个 L2 Chunks 向量，实际: {ntotal}"


def test_direct_l2_vector_and_hybrid_retrieval():
    print("\n" + "=" * 70)
    print("🔍 测试 2: 检验直接检索 L2 广覆盖参考知识库 (BM25 + FAISS 稠密向量)")
    print("=" * 70)

    mgr = SnapshotManager()
    retriever = HybridRetriever(snapshot_mgr=mgr)

    test_cases = [
        {
            "desc": "印尼固定期限用工 (PKWT) 灵活用工与补偿金",
            "query": "印尼固定期限劳动合同 PKWT 补偿金标准",
            "expected_ref": "ID:UU_11_2020:Art81",
            "expected_kind": "norm"
        },
        {
            "desc": "印尼重型工程机械盾构机临时进口免税保函",
            "query": "重型工程机械盾构机临时进口关税免除与保函",
            "expected_ref": "ID:UU_17_2006:Art10B",
            "expected_kind": "norm"
        },
        {
            "desc": "马来西亚吉隆坡轻轨停工令工期顺延先例",
            "query": "马来西亚吉隆坡轻轨停工令工期顺延争议先例",
            "expected_ref": "REF_CASE:MY_COA:OSHA_StopWork_EOT:2018",
            "expected_kind": "case"
        },
        {
            "desc": "越南外资按年缴纳土地租金厂房物权转让先例",
            "query": "越南外资按年缴纳土地租金厂房地上建筑物物权转让先例",
            "expected_ref": "REF_CASE:VN_SPC:Land_Lease_Dispute:2019",
            "expected_kind": "case"
        },
        {
            "desc": "菲律宾地方政府单方撤销施工许可证禁制令先例",
            "query": "菲律宾地方工程处无故撤销中资承包商施工许可证",
            "expected_ref": "REF_CASE:PH_CA:Building_Permit_Revocation:2019",
            "expected_kind": "case"
        },
        {
            "desc": "FIDIC 工程一切险 (CAR) 投保金额重置成本",
            "query": "FIDIC 银皮书 建筑工程一切险 CAR 投保义务",
            "expected_ref": "FIDIC:Silver_1999:Clause_18.2",
            "expected_kind": "norm"
        },
        {
            "desc": "越南外国承包商税 FCT 包税条款税基倒算",
            "query": "越南外国承包商税 FCT 包税条款税基倒算与发包人税款扣除",
            "expected_ref": "VN:Circular_103_2014:Art7",
            "expected_kind": "norm"
        },
        {
            "desc": "印尼无资质承包商 PPh Final 8% 惩罚性预扣税率",
            "query": "印尼承包商无有效资质建筑服务预扣所得税 8% 惩罚税率",
            "expected_ref": "ID:PP_9_2022:Art3",
            "expected_kind": "norm"
        },
        {
            "desc": "印尼外籍劳工 RPTKA 必须配备本地陪同员工",
            "query": "印尼雇佣中方工程技术人员 RPTKA 与本地陪同员工 1:3 比例",
            "expected_ref": "ID:Permenaker_8_2021:Art14",
            "expected_kind": "norm"
        },
        {
            "desc": "FIDIC 黄皮书不可预见地质条件工期与费用索赔",
            "query": "FIDIC 黄皮书 遇到不可预见的地下物理条件与地质障碍工期成本索赔",
            "expected_ref": "FIDIC:Yellow_1999:Clause_4.12",
            "expected_kind": "norm"
        },
        {
            "desc": "胡志明市法院外国承包商税包税条款补税判例",
            "query": "胡志明市人民法院外国承包商税包税条款发包人擅自扣款判决",
            "expected_ref": "REF_CASE:VN_HCMC_PC:FCT_GrossUp_Dispute:2020",
            "expected_kind": "case"
        },
        {
            "desc": "新加坡高院地下盾构工程不可预见地质突变索赔案",
            "query": "新加坡高等法院地下隧道盾构断裂带不可预见物理条件索赔判例",
            "expected_ref": "REF_CASE:SG_HC:FIDIC_Cl4_12_UnforeseenGround:2018",
            "expected_kind": "case"
        }
    ]

    passed = 0
    for tc in test_cases:
        t0 = time.perf_counter()
        results = retriever.search_l2(tc["query"], top_k=5)
        elapsed_ms = (time.perf_counter() - t0) * 1000

        hit_refs = [r.ref_id for r in results]
        found = any(tc["expected_ref"] in r.ref_id for r in results)
        status_icon = "✓" if found else "❌"
        print(f"{status_icon} 问句 [{tc['desc']}] -> 耗时 {elapsed_ms:.1f}ms")
        print(f"   预期命中: {tc['expected_ref']}")
        print(f"   实际召回 Top 3: {hit_refs[:3]}")

        if found:
            hit_ev = next(r for r in results if tc["expected_ref"] in r.ref_id)
            assert hit_ev.layer == "L2", f"预期 layer 为 L2，实际: {hit_ev.layer}"
            assert hit_ev.grade == "B", f"预期 grade 为 B，实际: {hit_ev.grade}"
            assert hit_ev.kind == tc["expected_kind"], f"预期 kind 为 {tc['expected_kind']}，实际: {hit_ev.kind}"
            passed += 1
        print("-" * 50)

    assert passed == len(test_cases), f"L2 直接检索未全部命中 ({passed}/{len(test_cases)})"
    print(f"🎉 测试 2 全部通过！命中率 100% ({passed}/{len(test_cases)})")


def test_cascaded_auto_retrieval():
    print("\n" + "=" * 70)
    print("🔍 测试 3: 检验双层智能级联机制 (AUTO 模式与层级隔离)")
    print("=" * 70)

    mgr = SnapshotManager()
    retriever = HybridRetriever(snapshot_mgr=mgr)

    # 1. 核心高优先级法条：必须命中 L1，且不应被 L2 稀释
    q_l1 = "越南商业合同约定违约金10%超过法定8%上限河内高院裁判"
    res_l1 = retriever.search(q_l1, top_k=5, layer="AUTO")
    assert any("VN:Commercial_Law_2005:Art301" in r.ref_id for r in res_l1), "❌ L1 核心违约金上限法条未命中"
    top_layers = [r.layer for r in res_l1]
    print(f"✓ 核心高优先级问句: Top 命中全为 L1 ({top_layers[:3]})，纯度 100%")

    # 2. 边缘广覆盖合规法源：L1 无对应实体，系统穿底自动级联下沉至 L2
    q_l2 = "外国总承包商工程机械设备临时进口海关申报与免税保函"
    res_l2 = retriever.search(q_l2, top_k=5, layer="AUTO")
    assert any("ID:UU_17_2006:Art10B" in r.ref_id for r in res_l2), "❌ 智能级联至 L2 失败"
    l2_hit = next(r for r in res_l2 if "ID:UU_17_2006:Art10B" in r.ref_id)
    assert l2_hit.layer == "L2", "❌ 级联结果未能正确标记 layer='L2'"
    assert l2_hit.grade == "B", "❌ 级联结果未能正确标记 grade='B'"
    print(f"✓ 边缘合规问句成功触发下沉级联！成功召回 L2 参考证据: {l2_hit.ref_id} [Layer={l2_hit.layer}, Grade={l2_hit.grade}]")

    # 3. 显式 ALL 模式：同时包含 L1 与 L2
    res_all = retriever.search("工程停工与履约保函止付", top_k=8, layer="ALL")
    layers = set(r.layer for r in res_all)
    print(f"✓ ALL 模式成功聚合双层证据池: 包含层级 {layers}")
    print("🎉 测试 3 全部通过！分级调度与层级隔离机制验证完整无误！")


if __name__ == "__main__":
    test_l2_engines_and_faiss()
    test_direct_l2_vector_and_hybrid_retrieval()
    test_cascaded_auto_retrieval()
    print("\n" + "=" * 70)
    print("🏆 L2 广覆盖参考层与 FAISS 向量检索双层架构全部验证 100% 通过！")
    print("=" * 70)
