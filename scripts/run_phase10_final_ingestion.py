# -*- coding: utf-8 -*-
"""
run_phase10_final_ingestion.py - 《数据库审查.md》最新版终极全量入库总执行脚本
全流程覆盖：
1. 写入 65 条 L1 强行法条 (norms) 并同步构建 L1 文本切片 (chunks)
2. 写入 52 条 L2 参考规程与多边条约 (reference_norms) 并构建 (reference_chunks)
3. 写入 30 篇 L1 涉东盟标杆判例 (cases) 并构建 L1 判例切片 (chunks)
4. 写入 26 篇 L2 国际投资商事仲裁裁决 (reference_cases) 并构建 (reference_chunks)
5. 建立 94 条 L1 拓扑边 (edges) 与 69 条 L2 参考边 (reference_edges)，严格保持 0 悬空边
6. 全量刷新物化加速表 edges_top 与 hot_norm_cases
7. 同步扩充静态知识库文件：kb/asean/glossary.csv (+30), timepoints.yaml (+4), commentary.json (+20)
8. 执行严密的全表数据完整性与质量底线审计验证
"""
import os
import sys
import json
import sqlite3
import yaml

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

DB_PATH = "data/snapshots/20261021-asean-v2.2/law.sqlite"
SNAP_ID = "20261021-asean-v2.2"

def main():
    print("=" * 70)
    print("  🚀 开始执行 Phase 10 终极全量入库流水线 (遵循最新《数据库审查.md》看板)")
    print("=" * 70)

    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"Database not found at {DB_PATH}")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # 1. 载入数据源模块
    print("\n[Step 1] 载入 Phase 10 数据源模块...")
    import scripts.data_phase10_deep_statutes as d_l1_norms
    import scripts.data_phase10_ref_statutes as d_l2_norms
    import scripts.data_phase10_deep_cases as d_cases
    import scripts.phase10_edges_data as d_edges

    l1_norms = d_l1_norms.ALL_PHASE10_L1_NORMS
    l2_norms = d_l2_norms.PHASE10_L2_REFERENCE_NORMS
    l1_cases = d_cases.PHASE10_L1_CASES
    l2_cases = d_cases.PHASE10_L2_REFERENCE_CASES
    l1_edges = d_edges.PHASE10_L1_EDGES
    l2_edges = d_edges.PHASE10_L2_REF_EDGES
    hot_mappings = d_edges.PHASE10_HOT_NORM_CASES

    print(f"-> 待入库 L1 法条: {len(l1_norms)} 条")
    print(f"-> 待入库 L2 规程: {len(l2_norms)} 条")
    print(f"-> 待入库 L1 判例: {len(l1_cases)} 篇")
    print(f"-> 待入库 L2 仲裁裁决: {len(l2_cases)} 篇")
    print(f"-> 待入库 L1 拓扑边: {len(l1_edges)} 条")
    print(f"-> 待入库 L2 拓扑边: {len(l2_edges)} 条")
    print(f"-> 待入库 核心判例映射: {len(hot_mappings)} 组")

    # 2. 插入 L1 强行法条 (norms) & 切片 (chunks)
    print("\n[Step 2] 注入 L1 强行法条到 norms 表并构建 chunks...")
    n_inserted = 0
    c_inserted = 0
    for n in l1_norms:
        cur.execute("""
            INSERT OR REPLACE INTO norms (
                norm_id, law, enbez, title, heading_path, language_mode,
                lang_original, text_original, text_en, text_zh,
                norm_category, mandatory_level, elements_json, snapshot_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            n["norm_id"], n["law"], n["enbez"], n["title"], n["heading_path"],
            n.get("language_mode", "bilingual"), n.get("lang_original", "en"),
            n.get("text_original", ""), n.get("text_en", ""), n["text_zh"],
            n.get("norm_category", "general"), n.get("mandatory_level", "mandatory"),
            n["elements_json"], SNAP_ID
        ))
        n_inserted += 1

        # 构建 chunk
        chunk_id = f"CHUNK:NORM:{n['norm_id']}:0"
        chunk_text = f"{n['title']}\n{n['text_zh']}\n{n.get('text_en','')}\n{n.get('text_original','')}".strip()
        cur.execute("""
            INSERT OR REPLACE INTO chunks (
                chunk_id, kind, ref_id, seq, text, ctx_prefix
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, (chunk_id, "norm", n["norm_id"], 0, chunk_text, n["heading_path"]))
        c_inserted += 1

    print(f"✓ 成功写入 {n_inserted} 条 L1 法条及 {c_inserted} 条对应全文切片")

    # 3. 插入 L2 参考规程 (reference_norms) & 切片 (reference_chunks)
    print("\n[Step 3] 注入 L2 参考规程到 reference_norms 表并构建 reference_chunks...")
    rn_inserted = 0
    rc_inserted = 0
    for n in l2_norms:
        cur.execute("""
            INSERT OR REPLACE INTO reference_norms (
                norm_id, law, enbez, title, heading_path, language_mode,
                lang_original, text_original, text_en, text_zh,
                norm_category, mandatory_level, fidic_tier, fidic_edition,
                elements_json, snapshot_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            n["norm_id"], n["law"], n["enbez"], n["title"], n["heading_path"],
            n.get("language_mode", "bilingual"), n.get("lang_original", "en"),
            n.get("text_original", ""), n.get("text_en", ""), n["text_zh"],
            n.get("norm_category", "general"), n.get("mandatory_level", "directory"),
            n.get("fidic_tier", None), n.get("fidic_edition", None),
            n["elements_json"], SNAP_ID
        ))
        rn_inserted += 1

        # 构建 ref chunk
        chunk_id = f"CHUNK:REF_NORM:{n['norm_id']}:0"
        chunk_text = f"{n['title']}\n{n['text_zh']}\n{n.get('text_en','')}".strip()
        cur.execute("""
            INSERT OR REPLACE INTO reference_chunks (
                chunk_id, kind, ref_id, seq, text
            ) VALUES (?, ?, ?, ?, ?)
        """, (chunk_id, "reference_norm", n["norm_id"], 0, chunk_text))
        rc_inserted += 1

    print(f"✓ 成功写入 {rn_inserted} 条 L2 规程及 {rc_inserted} 条对应参考切片")

    # 4. 插入 L1 标杆判例 (cases) & 切片 (chunks)
    print("\n[Step 4] 注入 L1 标杆判例到 cases 表并构建 chunks...")
    case_inserted = 0
    case_chunk_inserted = 0
    for c in l1_cases:
        cur.execute("""
            INSERT OR REPLACE INTO cases (
                case_id, court, senate, decided, az, ecli, doctype,
                leitsatz, tenor, tatbestand, gruende, norms_meta, snapshot_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            c["case_id"], c["court"], c["senate"], c["decided"], c["az"],
            c.get("ecli", ""), c.get("doctype", "judgment"),
            c["leitsatz"], c["tenor"], c["tatbestand"], c["gruende"],
            c.get("norms_meta", ""), SNAP_ID
        ))
        case_inserted += 1

        # 构建 chunk
        chunk_id = f"CHUNK:CASE:{c['case_id']}:0"
        prefix = f"{c['court']} {c['az']}"
        chunk_text = f"{c['leitsatz']}\n{c['tenor']}\n{c['tatbestand']}\n{c['gruende']}".strip()
        cur.execute("""
            INSERT OR REPLACE INTO chunks (
                chunk_id, kind, ref_id, seq, text, ctx_prefix
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, (chunk_id, "case", c["case_id"], 0, chunk_text, prefix))
        case_chunk_inserted += 1

    print(f"✓ 成功写入 {case_inserted} 篇 L1 标杆判例及 {case_chunk_inserted} 条判例切片")

    # 5. 插入 L2 参考仲裁裁决 (reference_cases) & 切片 (reference_chunks)
    print("\n[Step 5] 注入 L2 参考仲裁裁决到 reference_cases 表并构建 reference_chunks...")
    rcase_inserted = 0
    rcase_chunk_inserted = 0
    for c in l2_cases:
        cur.execute("""
            INSERT OR REPLACE INTO reference_cases (
                case_id, court, senate, decided, az, ecli, doctype,
                leitsatz, tenor, tatbestand, gruende, norms_meta, snapshot_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            c["case_id"], c["court"], c["senate"], c["decided"], c["az"],
            c.get("ecli", ""), c.get("doctype", "award"),
            c["leitsatz"], c["tenor"], c["tatbestand"], c["gruende"],
            c.get("norms_meta", ""), SNAP_ID
        ))
        rcase_inserted += 1

        # 构建 ref chunk
        chunk_id = f"CHUNK:REF_CASE:{c['case_id']}:0"
        chunk_text = f"{c['leitsatz']}\n{c['tenor']}\n{c['tatbestand']}\n{c['gruende']}".strip()
        cur.execute("""
            INSERT OR REPLACE INTO reference_chunks (
                chunk_id, kind, ref_id, seq, text
            ) VALUES (?, ?, ?, ?, ?)
        """, (chunk_id, "reference_case", c["case_id"], 0, chunk_text))
        rcase_chunk_inserted += 1

    print(f"✓ 成功写入 {rcase_inserted} 篇 L2 仲裁裁决及 {rcase_chunk_inserted} 条对应切片")

    # 6. 插入 L1 拓扑边 (edges)
    print("\n[Step 6] 注入 L1 拓扑关系边并进行严格合法性校验...")
    # 先查询全量有效实体合集
    cur.execute("SELECT norm_id FROM norms")
    valid_l1_norms = {r[0] for r in cur.fetchall()}
    cur.execute("SELECT case_id FROM cases")
    valid_l1_cases = {r[0] for r in cur.fetchall()}
    valid_l1_nodes = valid_l1_norms.union(valid_l1_cases)

    l1_edge_inserted = 0
    for e in l1_edges:
        src = e["src"]
        dst = e["dst"]
        if src not in valid_l1_nodes:
            raise ValueError(f"L1 Edge src invalid (dangling): {src}")
        if dst not in valid_l1_nodes:
            raise ValueError(f"L1 Edge dst invalid (dangling): {dst}")

        cur.execute("""
            INSERT OR REPLACE INTO edges (
                src, dst, rel, source, span, confidence, reviewed, snapshot_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            src, dst, e["rel"], e.get("source", "PHASE10_EXPANSION"),
            "", e.get("confidence", 0.95), 1, SNAP_ID
        ))
        l1_edge_inserted += 1

    print(f"✓ 成功建立 {l1_edge_inserted} 条合法 L1 拓扑关系边 (严格 0 悬空边)")

    # 7. 插入 L2 拓扑边 (reference_edges)
    print("\n[Step 7] 注入 L2 拓扑关系边并进行严格合法性校验...")
    cur.execute("SELECT norm_id FROM reference_norms")
    valid_l2_norms = {r[0] for r in cur.fetchall()}
    cur.execute("SELECT case_id FROM reference_cases")
    valid_l2_cases = {r[0] for r in cur.fetchall()}
    valid_l2_nodes = valid_l2_norms.union(valid_l2_cases)

    l2_edge_inserted = 0
    for e in l2_edges:
        src = e["src"]
        dst = e["dst"]
        if src not in valid_l2_nodes:
            raise ValueError(f"L2 Edge src invalid (dangling): {src}")
        if dst not in valid_l2_nodes:
            raise ValueError(f"L2 Edge dst invalid (dangling): {dst}")

        edge_id = f"REF_EDGE:{src}->{dst}"
        cur.execute("""
            INSERT OR REPLACE INTO reference_edges (
                edge_id, src, dst, rel, description
            ) VALUES (?, ?, ?, ?, ?)
        """, (edge_id, src, dst, e["rel"], e.get("description", "")))
        l2_edge_inserted += 1

    print(f"✓ 成功建立 {l2_edge_inserted} 条合法 L2 拓扑关系边 (严格 0 悬空边)")

    # 8. 刷新物化加速表
    print("\n[Step 8] 刷新物化加速表 edges_top 与 hot_norm_cases...")
    cur.execute("DELETE FROM edges_top")
    cur.execute("""
        INSERT INTO edges_top (src, dst, rel, source, reviewed, rk)
        SELECT src, dst, rel, source, reviewed,
               ROW_NUMBER() OVER (PARTITION BY src, rel ORDER BY confidence DESC) as rk
        FROM edges
    """)
    cur.execute("SELECT count(*) FROM edges_top")
    edges_top_count = cur.fetchone()[0]

    for n_id, c_id, rk in hot_mappings:
        cur.execute("INSERT OR REPLACE INTO hot_norm_cases(norm_id, case_id, rank) VALUES(?, ?, ?)", (n_id, c_id, rk))

    cur.execute("SELECT count(*) FROM hot_norm_cases")
    hot_count = cur.fetchone()[0]
    print(f"✓ edges_top 刷新完成 (当前行数: {edges_top_count})")
    print(f"✓ hot_norm_cases 映射更新完成 (当前行数: {hot_count})")

    # 提交事务
    conn.commit()
    print("✓ SQLite 主数据库全部写入提交完成！")

    # 9. 扩充静态知识库文件 (kb/asean/)
    print("\n[Step 9] 扩充 kb/asean/ 静态知识库文件...")
    update_static_knowledge_base()

    # 10. 终极数据看板全量核验
    print("\n[Step 10] 运行最终验收看板审计核对...")
    run_final_acceptance_audit(cur)

    conn.close()
    print("\n" + "=" * 70)
    print("  🎉 PHASE 10 全量入库流水线圆满完成，数据库各项指标全面超越验收标准！")
    print("=" * 70)


def update_static_knowledge_base():
    """扩充 glossary.csv (+30), timepoints.yaml (+4), commentary.json (+20)"""
    # 1. glossary.csv
    glossary_path = "kb/asean/glossary.csv"
    new_terms = [
        "防阻原则,Prevention Principle,Prinsip Pencegahan,asean_all,普通法核心法理：发包人自身的违约或阻碍行为导致承包商工期延误的，发包人丧失扣收误期违约金(LD)权利",
        "工期重回自由,Time at Large,Masa Bebas,asean_all,因发包人阻碍且合同顺延机制失效导致原固定竣工日瓦解，承包商仅负有在合理时间内完工之义务",
        "税收总额提升条款,Gross-up Clause,Klausul Peningkatan Pajak,asean_all,涉外合同约定支付款项为税后净额，属地发生预扣税时由发包人全额补足差额以确保承包商实收净额不变",
        "不答辩即失权原则,Preclusion Rule,Prinsip Kehilangan Hak,asean_sg,新加坡SOPA法定要求发包人在付款证明中必须列明扣款理由，未在法定期限列明者在后续仲裁中永久失权",
        "清洁原则,Clean Hands Doctrine,Prinsip Tangan Bersih,asean_all,国际公法原则：外国投资者通过行贿、伪造公文或欺诈手段设立的投资，自始丧失双边投资条约(BIT)受案保护资格",
        "主权规制警察权,Regulatory Police Powers,Kewenangan Polisi Regulasi,asean_all,主权国家为了公共福利与资源主权实施普遍非歧视性经济管制措施，依法不构成必须赔偿的间接征收",
        "反挂名法,Anti-Dummy Law,Batas Nominee,asean_ph,菲律宾CA 108法令：严禁利用菲律宾籍公民代持以规避宪法外资比例红线，违者处以5至15年监禁且资产全部充公没收",
        "法定清偿催告书,Statutory Demand,Tuntutan Statutori,asean_sg,新加坡及普通法法域下发出为期21天刚性偿债通知，逾期未付即构成无可辩驳的法定破产原因直接签发清盘令",
        "现金流无力偿债测试,Cash Flow Insolvency Test,Uji Arus Kas,asean_sg,破产法优先审查企业即期与可预见短期内现金偿付能力，凡无法按期支付到期债务即构成法定破产原因",
        "少数股东压迫,Minority Oppression,Penindasan Pemegang Saham Minoritas,asean_sg,大股东滥用控制地位侵害合资企业少数股东合理期待，法院依法有权判令大股东无折价公允强制收购",
        "纯劳务派遣禁止,Labor-Only Contracting Prohibition,Larangan Outsourcing Tenaga Murni,asean_ph,分包商无实质资本或由总包直接指挥施工的被强制定性为违法派遣，总包直接被拟制为全体工人的法定直聘雇主",
        "建筑结构十五年责任,Decennial / 15-Year Collapse Liability,Tanggung Jawab Kerusakan 15 Tahun,asean_ph,菲律宾民法典第1723条确立建筑物完工交工后15年内因缺陷倒塌由总包与设计工程师承担法定无过错连带责任",
        "变更调价双重书面要件,Two Written Requirements for Variations,Syarat Ganda Tertulis,asean_ph,菲律宾民法典第1724条规定承包商主张变更工程款必须同时持有书面变更授权与双方书面单价确认协议",
        "建筑仲裁委员会专属管辖,CIAC Exclusive Jurisdiction,Yurisdiksi Eksklusif CIAC,asean_ph,菲律宾第1008号行政令赋予CIAC对建设工程争议排他管辖权，自动排除普通初审法院RTC的民商审判管辖",
        "违约金司法衡减权,Equitable Mitigation of Penalty,Pengurangan Denda Sepihak,asean_th,泰国民商法典第383条与菲律宾第1229条赋予主审法官依职权强行大幅裁减畸高违约金并按已使用工程比例同等扣减",
        "迟延债务新法定年利率5%,New Default Statutory Interest Rate 5%,Suku Bunga Wanprestasi 5%,asean_th,泰王国2021年紧急法令废止旧法7.5%年息，规定无约定金钱债务自2021年4月11日起统一按年利率5%计收且禁计复利",
        "承揽瑕疵保修一年时效,One-Year Defect Claim Prescription,Daluwarsa Cacat 1 Tahun,asean_th,泰国民商法典第601条规定发包人在发现隐蔽工程瑕疵之日起必须在严格1年内向法院提起诉讼，逾期实体索赔权消灭",
        "外国承包商税,Foreign Contractor Tax (FCT),Thuế Nhà Thầu Nước Ngoài,asean_vn,越南对未在越设立法人机构的外国承包商征收的包含企业所得税(CIT)与增值税(VAT)的综合预扣代扣税收制度",
        "离岸与在岸分拆模式,Onshore/Offshore Split Contract,Hợp đồng tách Onshore/Offshore,asean_vn,涉外EPC将境外纯设备供货与境内建筑安装拆分为两份独立合同以合法将离岸供货利润剥离免征属地承包商税",
        "过渡期折价结算电价,Transitional Renewable Tariff,Giá Điện Chuyển Tiếp,asean_vn,越南工贸部Decision 21/2023针对未赶上FIT优惠电价的风电光伏设立的最高限价与临时按50%拨付结算的过渡机制",
        "作业许可证强制联营,Construction Operating License Joint Venture,Giấy phép hoạt động liên danh,asean_vn,越南Decree 15/2021要求外国承包商必须取得作业许可证且强制与越南本土承包商组建联营体或签署本土分包合同",
        "先诉抗辩权明示放弃,Waiver of Beneficium Excussionis,Pelepasan Hak Istimewa Pasal 1831,asean_id,印尼民法典第1832条允许担保人在保函中明文放弃主债务人财产先行清算抗辩，确立见索即付无条件直兑地位",
        "双币汇率浮动结算机制,Dual-Currency FX Linked Mechanism,Mekanisme Kurs Terkait,asean_id,涉外工程合同以美元核定基准价值、付款时依印尼央行JISDOR实时汇率折算为印尼盾划转以兼顾货币法合规与汇率防爆",
        "第一顺位最高额抵押权,First Ranking Hak Tanggungan,Hak Tanggungan Peringkat Pertama,asean_id,依据印尼1996年第4号法对外资工业土地及地上重型冶炼厂设立的具备终审生效判决最高执行力的法定物权抵押登记",
        "矿石基准指导价强制结算,Mandatory Mineral Benchmark Price (HPM),Harga Patokan Mineral (HPM),asean_id,印尼能矿部第11/2020号令强制要求境内冶炼厂采购镍矿必须与LME月度官方HPM公式挂钩，低于指导价协议自始无效",
        "固定期限劳动合同期满补偿金,PKWT Severance Compensation,Uang Kompensasi PKWT,asean_id,印尼PP 35/2021条例强制要求雇主在固定劳动合同期满终止时必须按工龄月数比例全额计发法定经济补偿金专项准备",
        "见索即付保函违约陈述必备要件,Mandatory Statement of Breach under URDG 758,Pernyataan Pelanggaran Wajib,asean_all,URDG 758第15条强制要求受益人索赔必须说明申请人在何种具体方面构成违约，欠缺具体陈述构成单据表面重大不符",
        "担保行五日严格审单期限,Guarantor 5 Business Days Examination,Batas Waktu Pemeriksaan 5 Hari,asean_all,URDG 758第20条赋予担保行自收到索赔单据次日起严格5个银行营业日审单时限，逾期未出具不符点通知丧失拒付抗辩权",
        "DAAB裁定即时强制拘束力,Immediate Binding Effect of DAAB Decision,Daya Mengikat Langsung DAAB,asean_all,FIDIC 2017第21.4款规定DAAB裁定签发后双方必须立即照章付款，发出不满意通知(NOD)不停止裁定立即履行金钱支付",
        "合理商业期待保护原则,Protection of Legitimate Expectations,Perlindungan Ekspektasi Sah,asean_all,国际投资法公平公正待遇(FET)核心教义，严禁东道国政府由于国内政治选票反复无常单方推翻特许权调价主权承诺"
    ]
    with open(glossary_path, "a", encoding="utf-8") as f:
        for t in new_terms:
            f.write(t + "\n")
    print(f"✓ 成功向 {glossary_path} 追加 30 组高对抗专业术语 (当前总行数: {len(open(glossary_path, encoding='utf-8').readlines())})")

    # 2. timepoints.yaml
    timepoints_path = "kb/asean/timepoints.yaml"
    new_tp = """
- timepoint_id: TP_TH_INTEREST_2021
  jurisdiction: asean_th
  law_name: 泰国《2021年第2564号修正民商法典紧急法令》
  effective_date: '2021-04-11'
  enacted_date: '2021-04-10'
  rule_type: statutory_overhaul
  alert_level: red
  condition: default_period >= 2021-04-11
  description: 彻底废除旧法年息7.5%标准，金钱债务迟延履行法定年利率统一下调为5%(基准3%+违约附加2%)，且严禁利滚利复利；2021年4月11日之后发生的违约利息强制适用新法5%。
- timepoint_id: TP_PH_PSA_2022
  jurisdiction: asean_ph
  law_name: 菲律宾《2022年公共服务法修正案》(Republic Act No. 11659)
  effective_date: '2023-04-01'
  enacted_date: '2022-03-21'
  rule_type: market_access
  alert_level: green
  condition: investment_date >= 2023-04-01
  description: 将宪法40%外资上限严格收窄限定于6类核心公用事业；电信、铁路、民航、高速公路、新能源物流全面开放100%外商独资控股。
- timepoint_id: TP_PH_GPRA_2024
  jurisdiction: asean_ph
  law_name: 菲律宾《2024年新政府采办改革法》(Republic Act No. 12009)
  effective_date: '2024-07-20'
  enacted_date: '2024-07-02'
  rule_type: public_procurement
  alert_level: yellow
  condition: bidding_date >= 2024-07-20
  description: 全面革新公共工程招投标模式，确立Fit-for-Purpose采购标准；涉外主权援助工程允许外国总承包商依持牌特别许可(Special License)直接参标，从严惩戒串标借资质。
- timepoint_id: TP_ID_PP_9_2022_TAX
  jurisdiction: asean_id
  law_name: 印尼政府关于建筑服务税之第9/2022号条例(PP No. 9/2022)
  effective_date: '2022-02-21'
  enacted_date: '2022-02-21'
  rule_type: tax_compliance
  alert_level: yellow
  condition: contract_payment >= 2022-02-21
  description: 重新核定建筑服务最终所得税(PPh Final)优惠税率；大型持照施工税率为2.65%，穿透确立独立税号联合体(NPWP KSO)在岸代扣代缴与发票责任。
"""
    with open(timepoints_path, "a", encoding="utf-8") as f:
        f.write(new_tp)
    print(f"✓ 成功向 {timepoints_path} 追加 4 大修法里程碑节点")

    # 3. commentary.json
    commentary_path = "kb/asean/commentary.json"
    with open(commentary_path, "r", encoding="utf-8") as f:
        comm_data = json.load(f)

    new_comments = {
        "VN:Civil_Code_2015:Art420": {
            "title": "情势变更原则在固定总价调价中的排他性适用",
            "jurisdiction": "asean_vn",
            "core_doctrine": "合同订立后发生不可预见客观剧变，继续按闭口总价履行将遭受显失公平严重损失的，享有法定重新谈判权；协商未果法院有权实质调增造价或解除合同。",
            "practical_tip": "钢材水泥等大宗建材暴涨超50%时，必须在28天内发出正式书面谈判通知，并收集工贸部官方基准价格走势作为司法介入证据。"
        },
        "VN:Law_31_2024:Art127_128": {
            "title": "工业用地土地使用权一次性缴费与持牌银行抵押限制",
            "jurisdiction": "asean_vn",
            "core_doctrine": "外资企业唯有一次性全额缴纳租期全部土地租金取得的工业用地土地使用权(LUR)，方可向越南境内持牌信贷机构设定抵押；按年交租土地严禁抵押土地使用权本身。",
            "practical_tip": "中资央企出海投建电站厂房若需项目融资质押，拿地时必须坚持选择'一次性缴费'模式，严防按年交租抵押自始无效引发银行提前抽贷。"
        },
        "ID:KUHPerdata:Art1831_1832": {
            "title": "保证人先诉抗辩权明示放弃与见索即付独立性",
            "jurisdiction": "asean_id",
            "core_doctrine": "保证人原则上享有先执行债务人财产抗辩权，但依据第1832条第1款明示放弃该抗辩权的，其地位等同于连带债务人，债权人享有无条件直兑保函权利。",
            "practical_tip": "审核印尼属地分包商履约保函时，必须强制在正文载明'明确放弃印尼民法典第1831条抗辩利益'，防范陷入漫长先诉诉讼泥潭。"
        },
        "ID:UU_7_2011_Currency:Art21": {
            "title": "境内交易强制使用印尼盾与双币折算汇率防爆条款",
            "jurisdiction": "asean_id",
            "core_doctrine": "境内交易除特定主权豁免外强制使用印尼盾结算，但约定以美元作为抗通胀计价基准、支付时按印尼央行JISDOR实时汇率折算为印尼盾划转的机制完全合法有效。",
            "practical_tip": "印尼长期承包工程坚决采用'美元计价基准+付款日实时汇率折算印尼盾支付'黄金条款，将印尼盾贬值风险100%全额推给业主承担。"
        },
        "ID:UU_4_1996_HakTanggungan:Art4": {
            "title": "外资工业建筑权HGB设立第一顺位抵押权",
            "jurisdiction": "asean_id",
            "core_doctrine": "外资PMA合法持有的HGB工业土地及地上重型冶炼设施可设立第一顺位抵押权，土地局登记核发之抵押权证书具备法院生效判决之同等强制执行力。",
            "practical_tip": "重资产出海放贷融资必须在拿地后到当地BPN完成APHT抵押登记并领取Sertifikat Hak Tanggungan，锁定随时直接申请法院拍卖的排他优先受偿权。"
        },
        "ID:UU_2_2017:Art30_KSO": {
            "title": "外国建筑代表处BUJKA强制组建联合体经营",
            "jurisdiction": "asean_id",
            "core_doctrine": "外国代表处严禁单边独立承揽施工，必须且仅能与具备Kualifikasi Besar资质的印尼本土企业组建联合体(KSO)，且常规工种由本土企业牵头。",
            "practical_tip": "核验印尼合作方SBU大级资质证书真伪，并在联合体协议中锁定中方在技术、质量、安全及财务审批上的唯一一票否决权。"
        },
        "MY:Contracts_Act_1950:Sec52_55": {
            "title": "防阻原则成文法渊源与发包人先期违约",
            "jurisdiction": "asean_my",
            "core_doctrine": "双务合同依约定次序履行，发包人迟延交地或阻碍施工构成法定阻碍违约，受阻碍方有权撤销合同索赔损失，发包人丧失扣罚工期违约金权利。",
            "practical_tip": "现场一旦发生发包人交地迟延，必须在24小时内固定无人机全景与警情记录并发出阻碍通知，彻底阻断业主索赔误期罚金(LAD)。"
        },
        "MY:CIPAA_2012:Sec35": {
            "title": "建筑业支付法禁止反背靠背条件支付条款",
            "jurisdiction": "asean_my",
            "core_doctrine": "任何使总包向分包付款义务取决于总包是否收到业主款项的Pay-when-paid条款依法自始绝对无效，分包商享有45天快速裁决刚性追款权。",
            "practical_tip": "在大马严禁依赖背靠背合同转嫁业主欠款风险，必须在签约前严审业主资信，并在主合同中设立严苛的付款延迟停工权。"
        },
        "MY:CIPAA_2012:Sec28_30": {
            "title": "快速裁决临时终局执行力与直付救济",
            "jurisdiction": "asean_my",
            "core_doctrine": "裁决员作出的支付裁决具备即时强制执行力，法院仅在债权人确凿破产例外下审慎暂缓执行；总承包商未履约的分包商有权申请发包人直接从上游向其直付。",
            "practical_tip": "工程款被拖欠时优先向AIAC提请CIPAA快速裁决，60天内结案并可直接向银行申请查封冻结发包人资金流。"
        },
        "SG:SOPA_2004:Sec9_15": {
            "title": "SOPA付款证明不答辩失权原则",
            "jurisdiction": "asean_sg",
            "core_doctrine": "发包人在收到付款主张书后未在法定14天内送达付款响应书或未列明扣款理由的，在后续快速裁决中永久失权，裁决员依法无权考虑新增抗辩理由。",
            "practical_tip": "发出SOPA付款主张后严密监控发包人14天回复，一旦对方超期或敷衍回复，立即启动快速裁决直接全额拿下胜诉裁决。"
        },
        "SG:CRTPA_Cap_53B:Sec2_3": {
            "title": "第三方执行权与合同相对性排除条款格式",
            "jurisdiction": "asean_sg",
            "core_doctrine": "合同明确赋予第三方以利益且未明文排除CRTPA适用的，最终业主或银团享有直接起诉分包商之诉讼权利；排他性排除条款可彻底切断第三方穿透侵权风险。",
            "practical_tip": "在分包或供货合同中必须粗体载明：'A person who is not a party to this Contract shall have no right under the CRTPA to enforce any of its terms.'"
        },
        "SG:IRDA_2018:Sec440": {
            "title": "破产重整法现金流无力偿债测试标准",
            "jurisdiction": "asean_sg",
            "core_doctrine": "审查债务人是否破产优先遵循现金流标准而非账面资产，只要企业在即期与近期无法以可用资金偿还到期债务，法院依法签发强制清盘破产令。",
            "practical_tip": "对恶意拖欠无争议欠款的境外债务人，委托新加坡律师送达为期21天Statutory Demand，以破产清盘核威慑迫使债务人快速清偿。"
        },
        "TH:CCC:Sec383": {
            "title": "泰国民法典违约金司法公平衡减权",
            "jurisdiction": "asean_th",
            "core_doctrine": "合同约定的违约金数额畸高不成比例时，主审法庭依法享有不受合同约定限制的自由裁量权，强行大幅核减违约金至合理数额并判令退还超扣款项。",
            "practical_tip": "面临业主全额扣罚天价违约金时，重点举证工程主体已投入部分使用且业主未受实际损失，争取法院核减50%~70%违约金。"
        },
        "TH:CCC:Sec600_607": {
            "title": "承揽隐蔽瑕疵一年短期起诉除斥时效",
            "jurisdiction": "asean_th",
            "core_doctrine": "工程移交后定作人发现隐蔽工程瑕疵的，必须在发现瑕疵之日起严格1年内向法院提起诉讼，逾期未诉其实体索赔权永久消灭，质保金必须全额退还。",
            "practical_tip": "工程竣工交工后严密核算1年时效，若业主发现质量问题超过1年未起诉，直接起诉要求法院强制退还全部质量保证金。"
        },
        "TH:Arbitration_Act_2545:Sec40": {
            "title": "撤销仲裁裁决90天除斥期间与公共秩序极度严格限制",
            "jurisdiction": "asean_th",
            "core_doctrine": "申请撤销仲裁裁决必须在收到裁决之日起严格90天内提出；执行裁决将导致国库承担巨额商业违约赔偿绝不构成违背国家公共政策之撤销事由。",
            "practical_tip": "在泰订立特许经营争议条款优先锁定中立国际仲裁地，若在属地获胜，利用90天除斥期间彻底封死政府行政机关翻案企图。"
        },
        "PH:Civil_Code:Art1723": {
            "title": "结构坍塌15年法定连带责任与合同DLP责任界分",
            "jurisdiction": "asean_ph",
            "core_doctrine": "工程竣工后15年内因缺陷倒塌的，总承包商与设计监理工程师承担法定无过错连带侵权责任；合同约定的1~2年DLP商业保修期绝不能免除该法定连带责任。",
            "practical_tip": "在菲承建大型高层公建，隐蔽工程与桩基数据必须实行终身数字化归档，并在分包合同中强制背靠背转嫁15年连带质量责任。"
        },
        "PH:Civil_Code:Art1724": {
            "title": "承揽工程增资变更调价双重书面法定形式要件",
            "jurisdiction": "asean_ph",
            "core_doctrine": "固定总价承包商主张变更追加价款，必须严格同时具备发包人书面变更授权与双方事前达成的书面追加金额协议两大要件；欠缺任一要件不当得利索赔被排他性驳回。",
            "practical_tip": "现场工程师切莫轻信业主口头承诺或周会纪要先行动工，坚决执行'无正式双方签字确认调价协议坚决不动工'铁律。"
        },
        "PH:EO_1008_CIAC:Sec4": {
            "title": "建筑业仲裁委员会CIAC原始专属管辖权",
            "jurisdiction": "asean_ph",
            "core_doctrine": "对发生在菲律宾境内的所有建设施工争议享有排他管辖权，只要合同提及自愿仲裁即自动排除普通法院管辖，RTC法院必须立即移送或驳回起诉。",
            "practical_tip": "工程款被拖欠切勿在低效拖沓的RTC地方法院缠诉，直接向CIAC提请仲裁，利用其严格6个月结案机制雷霆冻结业主在岸资产并追索工程款。"
        },
        "INTL:FIDIC_2017:Cl20_2": {
            "title": "承包商索赔通知28天绝对时效与失权除斥效力",
            "jurisdiction": "asean_all",
            "core_doctrine": "知悉或应当知悉索赔事件后严格28天内向工程师发出索赔意向通知，逾期未发通知其追加付款与工期顺延请求权自始消灭，雇主免除一切责任。",
            "practical_tip": "现场设立28天红色预警闹钟，发生暴雨或地质变动先在14天内发出一份简短的标准Notice of Claim锁定权利大门，后续再行补充详尽报告。"
        },
        "INTL:URDG_758:Art15": {
            "title": "见索即付独立保函索赔违约陈述必备单据要件",
            "jurisdiction": "asean_all",
            "core_doctrine": "受益人索赔单据中必须明确陈述承包商具体在何种方面违反了基础合同义务，欠缺具体违约事实陈述构成表面单据不符，担保行依法必须拒绝付款。",
            "practical_tip": "保函被突袭索兑时，督导开证行以URDG 758第15条穿透审单，若索赔函未列明具体违约条款与事实，银行在5个工作日内出具正式拒付通知成功拦截。"
        }
    }
    comm_data.update(new_comments)
    with open(commentary_path, "w", encoding="utf-8") as f:
        json.dump(comm_data, f, ensure_ascii=False, indent=2)
    print(f"✓ 成功向 {commentary_path} 追加 20 条实务评注 (当前总词条数: {len(comm_data)})")


def run_final_acceptance_audit(cur):
    """根据最新《数据库审查.md》第六部分验收看板核验指标"""
    print("\n" + "=" * 50)
    print("       📊 最终验收看板指标全面核验")
    print("=" * 50)

    cur.execute("SELECT count(*) FROM norms")
    c_norms = cur.fetchone()[0]

    cur.execute("SELECT count(*) FROM reference_norms")
    c_ref_norms = cur.fetchone()[0]

    c_total_norms = c_norms + c_ref_norms

    cur.execute("SELECT count(*) FROM cases")
    c_cases = cur.fetchone()[0]

    cur.execute("SELECT count(*) FROM reference_cases")
    c_ref_cases = cur.fetchone()[0]

    c_total_cases = c_cases + c_ref_cases

    cur.execute("SELECT count(*) FROM edges")
    c_edges = cur.fetchone()[0]

    cur.execute("SELECT count(*) FROM reference_edges")
    c_ref_edges = cur.fetchone()[0]

    # 悬空边检测
    cur.execute("""
        SELECT count(*) FROM edges
        WHERE src NOT IN (SELECT norm_id FROM norms UNION SELECT case_id FROM cases)
           OR dst NOT IN (SELECT norm_id FROM norms UNION SELECT case_id FROM cases)
    """)
    dangling_l1 = cur.fetchone()[0]

    cur.execute("""
        SELECT count(*) FROM reference_edges
        WHERE src NOT IN (SELECT norm_id FROM reference_norms UNION SELECT case_id FROM reference_cases)
           OR dst NOT IN (SELECT norm_id FROM reference_norms UNION SELECT case_id FROM reference_cases)
    """)
    dangling_l2 = cur.fetchone()[0]

    # 空壳 elements_json 检测
    cur.execute("SELECT count(*) FROM norms WHERE elements_json IS NULL OR elements_json = '[]' OR elements_json = ''")
    empty_elem_l1 = cur.fetchone()[0]
    cur.execute("SELECT count(*) FROM reference_norms WHERE elements_json IS NULL OR elements_json = '[]' OR elements_json = ''")
    empty_elem_l2 = cur.fetchone()[0]

    # 案例金标准字数检测
    cur.execute("""
        SELECT count(*) FROM cases
        WHERE length(leitsatz) < 150 OR length(tenor) < 150 OR length(tatbestand) < 200 OR length(gruende) < 350
    """)
    substandard_cases_l1 = cur.fetchone()[0]

    cur.execute("""
        SELECT count(*) FROM reference_cases
        WHERE length(leitsatz) < 150 OR length(tenor) < 150 OR length(tatbestand) < 200 OR length(gruende) < 350
    """)
    substandard_cases_l2 = cur.fetchone()[0]

    print(f"1. L1 核心强行法条 (norms):            {c_norms:<5} (目标: >= 348) -> {'✅ 达标' if c_norms >= 348 else '❌ 未达标'}")
    print(f"2. L2 参考规程条约 (reference_norms):  {c_ref_norms:<5} (目标: >= 281) -> {'✅ 达标' if c_ref_norms >= 281 else '❌ 未达标'}")
    print(f"3. 全库成文法及条约总数:               {c_total_norms:<5} (目标: >= 629) -> {'✅ 达标' if c_total_norms >= 629 else '❌ 未达标'}")
    print(f"4. L1 标杆判例 (cases):                {c_cases:<5} (目标: >= 127) -> {'✅ 达标' if c_cases >= 127 else '❌ 未达标'}")
    print(f"5. L2 参考判例 (reference_cases):      {c_ref_cases:<5} (目标: >= 88)  -> {'✅ 达标' if c_ref_cases >= 88 else '❌ 未达标'}")
    print(f"6. 全库裁判文书总数:                   {c_total_cases:<5} (目标: >= 215) -> {'✅ 达标' if c_total_cases >= 215 else '❌ 未达标'}")
    print(f"7. L1 拓扑边 (edges):                  {c_edges:<5} (目标: >= 420) -> {'✅ 达标' if c_edges >= 420 else '❌ 未达标'}")
    print(f"8. L2 拓扑边 (reference_edges):        {c_ref_edges:<5} (目标: >= 210) -> {'✅ 达标' if c_ref_edges >= 210 else '❌ 未达标'}")
    print(f"9. L1 拓扑悬空边 (Dangling):           {dangling_l1:<5} (目标: == 0)   -> {'✅ 达标' if dangling_l1 == 0 else '❌ 未达标'}")
    print(f"10. L2 拓扑悬空边 (Dangling):          {dangling_l2:<5} (目标: == 0)   -> {'✅ 达标' if dangling_l2 == 0 else '❌ 未达标'}")
    print(f"11. elements_json 空壳数:              {empty_elem_l1 + empty_elem_l2:<5} (目标: == 0)   -> {'✅ 达标' if (empty_elem_l1 + empty_elem_l2) == 0 else '❌ 未达标'}")
    print(f"12. 裁判文书字数不达标数:              {substandard_cases_l1 + substandard_cases_l2:<5} (目标: == 0)   -> {'✅ 达标' if (substandard_cases_l1 + substandard_cases_l2) == 0 else '❌ 未达标'}")
    print("=" * 50)

    assert c_norms >= 348, f"Norms below target: {c_norms} < 348"
    assert c_ref_norms >= 281, f"Reference norms below target: {c_ref_norms} < 281"
    assert c_total_norms >= 629, f"Total norms below target: {c_total_norms} < 629"
    assert c_cases >= 127, f"Cases below target: {c_cases} < 127"
    assert c_ref_cases >= 88, f"Reference cases below target: {c_ref_cases} < 88"
    assert c_total_cases >= 215, f"Total cases below target: {c_total_cases} < 215"
    assert c_edges >= 420, f"Edges below target: {c_edges} < 420"
    assert c_ref_edges >= 210, f"Reference edges below target: {c_ref_edges} < 210"
    assert dangling_l1 == 0, f"L1 dangling edges found: {dangling_l1}"
    assert dangling_l2 == 0, f"L2 dangling edges found: {dangling_l2}"
    assert (empty_elem_l1 + empty_elem_l2) == 0, "Empty elements_json found!"
    assert (substandard_cases_l1 + substandard_cases_l2) == 0, "Substandard cases found!"

if __name__ == "__main__":
    main()
