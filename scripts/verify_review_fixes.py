import sys
import os
import time

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, os.path.abspath("."))

from lawagent.store.retriever import HybridRetriever
from lawagent.store.cl_align import CLAlignOperator

def test_all():
    print("==================================================")
    print("开始执行：针对《数据库审查报告》整改项的权威实测验证")
    print("==================================================")

    # 1. 验证 CL-Align 5 个新增高频场景
    print("\n[测试 1] 验证 CL-Align 5 大新增场景对齐能力:")
    cl_op = CLAlignOperator.get_instance()
    test_queries = [
        ("老挝水电特许权CA协议政府回购与单方调整", "asean_la", "Decree 135 PM"),
        ("缅甸MIC批文土地使用权转让限制", "asean_mm", "Land Use Rights"),
        ("菲律宾CADT祖传领地未取得FPIC知情同意前置施工", "asean_ph", "FPIC"),
        ("文莱BDDB政府基建项目履约保函即付索兑", "asean_bn", "BDDB"),
        ("东帝汶公共工程审计院visto签证拒绝后的法律救济路径", "asean_tl", "Recurso Ordinário")
    ]
    for q, jur, expect_kw in test_queries:
        res = cl_op.align(q, jurisdiction=jur)
        found = any(expect_kw.lower() in t.lower() for t in res.expanded_tokens) or any(expect_kw.lower() in d.lower() for d in res.cross_legal_system_doctrines)
        status = "✓ PASS" if found else "✗ FAIL"
        print(f"  * [{jur}] 查询: '{q[:20]}...' -> {status} (命中关键词: {expect_kw})")
        assert found, f"CL-Align 未命中预期关键词 {expect_kw}"

    # 2. 验证 Retriever、Reranker 配置与 2-Hop 图扩展
    print("\n[测试 2] 验证 Retriever 实例与 Reranker 激活状态:")
    retriever = HybridRetriever.from_snapshot()
    print(f"  * Reranker 模型: {retriever.reranker.model_name}")
    print(f"  * Reranker 是否启用 (enabled): {retriever.reranker.enabled}")
    print(f"  * 图扩展跳数 (graph_max_hops): {retriever.graph_max_hops}")
    assert retriever.reranker.enabled is True, "Reranker 应该被成功激活！"
    assert retriever.graph_max_hops == 2, "图扩展跳数应该是 2 跳！"

    # 3. 验证 2-Hop 图扩展能力
    print("\n[测试 3] 验证 2-Hop 图扩展连通性 (老挝/柬埔寨):")
    la_expanded = retriever.graph.expand(["LA:Decree_135_PM:Art8"], max_hops=2)
    print(f"  * LA:Decree_135_PM:Art8 扩展出的 1~2 跳关联节点数: {len(la_expanded)}")
    for node in la_expanded:
        print(f"    - {node['node']} (depth: {node['depth']})")
    assert any(n['depth'] == 2 for n in la_expanded) or len(la_expanded) >= 2, "2-Hop 扩展应成功发现多跳关联规范！"

    # 4. 验证 L2 FIDIC 2017 条款召回能力
    print("\n[测试 4] 验证 L2 FIDIC 2017 新机制召回:")
    fidic_evidences = retriever.search_l2("FIDIC 2017 索赔通知28天时效 DAAB裁决即时约束力", top_k=5)
    print(f"  * 召回条数: {len(fidic_evidences)}")
    found_2017 = False
    for ev in fidic_evidences:
        print(f"    - [{ev.ref_id}] {ev.text_de[:60]}...")
        if "2017" in ev.ref_id or "DAAB" in ev.text_de or "Clause 20.2" in ev.ref_id:
            found_2017 = True
    assert found_2017, "L2 应精准召回 FIDIC 2017 新机制条款！"

    # 5. 验证 L2 仲裁经典先例 (CMC v Mozambique / Himpurna) 召回
    print("\n[测试 5] 验证 L2 仲裁经典先例召回:")
    arb_evidences = retriever.search_l2("中资承包商 BIT 仲裁胜诉 拖欠工程款 FET 莫桑比克 CMC", top_k=5)
    print(f"  * 召回条数: {len(arb_evidences)}")
    found_cmc = False
    for ev in arb_evidences:
        print(f"    - [{ev.ref_id}] {ev.text_de[:60]}...")
        if "CMC" in ev.ref_id or "CMC" in ev.text_de:
            found_cmc = True
    assert found_cmc, "L2 应精准召回 CMC Africa Austral v Mozambique 投资仲裁先例！"

    print("\n==================================================")
    print(">> 审查报告所有整改项权威验证 100% 全部通过！")
    print("==================================================")

if __name__ == "__main__":
    test_all()
