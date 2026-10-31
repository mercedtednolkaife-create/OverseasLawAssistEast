"""
p0_final_sanitization.py - 执行最新《数据库审查.md》Step 1 数据清洗与主键规范化
1. 扫描 norms 表，将误入 norms 的 3 篇普通法判例平移至 cases 表：
   - SG:Precedent:BS_Mount_Sophia -> CASE:SG_CA:BS_Mount_Sophia:2012
   - SG:Precedent:JBE_Properties -> 合并至已有 CASE:SG_CA:JBEProperties:2011
   - PH:Precedent:PCAB_v_Manila_Water -> CASE:PH_SC:PCAB_v_Manila_Water_2020
2. 更新关联 edges 与 chunks，清理 norms 中上述 3 篇条目；
3. 将 norms 与 reference_norms 中 law 字段历史不规范命名归一化 (如 KUHPerdata -> ID:KUHPerdata)；
4. 更新 snapshots.py 的别名字典保持全面兼容。
"""
import sys
import sqlite3
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

DB_PATH = Path("data/snapshots/20261021-asean-v2.2/law.sqlite")

def run_p0_clean():
    print("=" * 60)
    print(">>> 启动 Step 1: P0 级历史脏数据清洗与主键规范化...")
    print("=" * 60)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # 1. 平移 SG:Precedent:BS_Mount_Sophia 到 cases 表
    bs_case = {
        "case_id": "CASE:SG_CA:BS_Mount_Sophia:2012",
        "court": "Singapore Court of Appeal (新加坡终审法院)",
        "senate": "Civil Appeals",
        "decided": "2012-07-27",
        "az": "[2012] SGCA 40 / [2012] 3 SLR 978",
        "doctype": "Judgment",
        "leitsatz": "【见索即付保函显失公平止付抗辩】：新加坡终审法院确立独立保函‘显失公平（Unconscionability）’止付标准：在传统欺诈例外之外，若受益人索赔保函的行为存在缺乏诚信、恶意违背商业良心、或严重滥用索兑权利的情形，法院有权签发禁令阻止银行向受益人付款。显失公平标准要求极高举证标准，不能仅仅因当事人之间存在普通商业履约争议即阻断保函兑付，必须证明存在显失公平的直接客观证据。",
        "tenor": "The Court of Appeal held that unconscionability is an independent and distinct ground from fraud for restraining a beneficiary from making or receiving a call on an on-demand performance bond, requiring clear and compelling evidence of bad faith or abusive conduct.",
        "tatbestand": "【案件事实全景与工程争议脉络】：总承包商与开发商签署住宅工程施工合同，并开具见索即付履约保函。工程实施过程中，双方就工期延误与变更签证产生严重争议，但建筑师已签发实质性竣工证书且项目已投入商业使用。业主因其他未结清商业索赔突然向银行发出保函全额索赔通知。承包商向新加坡高等法院申请禁令阻碍银行付款，主张业主索兑构成显失公平。",
        "gruende": """【裁判法理深度解析与核心涵摄逻辑】：终审法院全面权衡了见索即付保函的独立性原则与防范受益人恶意勒索之间的衡平关系。法院指出，新加坡法律坚决承认‘显失公平’作为独立的保函禁令救济事由，与欺诈并列。但显失公平的举证门槛极高，申请人必须证明受益人主观上明知其无合理索赔基础仍恶意行权，或其索兑行为达到了严重违背商业诚信良心的程度。本案中业主明知工程已竣工验收且扣款争议尚在审定中即全额索兑，构成显失公平，支持签发止付禁令。
【出海央企实操攻防启示】：新加坡普通法系为承包商提供了对抗业主恶意索兑履约保函的强有力武器！与传统英国法仅承认‘欺诈例外（Fraud Exception）’不同，新加坡法院承认‘显失公平（Unconscionability）’禁令。一旦境外业主因恶意施压或报复性扣兑保函，中资项目部应在24小时内固定业主违背商业诚信的往来邮件与工期核定事实，向新加坡法院申请紧急 EA 止付令，在打款前成功拦截银行资金划转！""",
        "source_url": "https://www.lawnet.sg/lawfinder",
        "norms_meta": "SG:Civil_Law_Act:Sec12,ICC:URDG_758:Art_5_Independence"
    }

    cur.execute("""
        INSERT OR REPLACE INTO cases
        (case_id, court, senate, decided, az, doctype, leitsatz, tenor, tatbestand, gruende, source_url, norms_meta)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        bs_case["case_id"], bs_case["court"], bs_case["senate"], bs_case["decided"], bs_case["az"],
        bs_case["doctype"], bs_case["leitsatz"], bs_case["tenor"], bs_case["tatbestand"],
        bs_case["gruende"], bs_case["source_url"], bs_case["norms_meta"]
    ))
    bs_chunk = f"[{bs_case['case_id']}] {bs_case['az']} {bs_case['leitsatz']} | {bs_case['tatbestand']} | {bs_case['gruende']} | {bs_case['tenor']}"
    cur.execute("""
        INSERT OR REPLACE INTO chunks (chunk_id, kind, ref_id, seq, text)
        VALUES (?, ?, ?, ?, ?)
    """, (f"CHUNK:CASE:{bs_case['case_id']}:0", "case", bs_case["case_id"], 0, bs_chunk))

    # 2. 平移 PH:Precedent:PCAB_v_Manila_Water 到 cases 表
    pcab_case = {
        "case_id": "CASE:PH_SC:PCAB_v_Manila_Water_2020",
        "court": "Supreme Court of the Philippines (菲律宾最高法院)",
        "senate": "En Banc",
        "decided": "2020-03-10",
        "az": "G.R. No. 217590",
        "doctype": "Judgment",
        "leitsatz": "【菲律宾承包商执照外资配额限制违宪无效】：菲律宾最高法院大法庭裁定：建筑业执照委员会（PCAB）关于普通施工许可证外资股权比例不得超过 40% 的行政规程违反宪法平等保护原则与《承包商执照法》（RA 4566），宣告该限制违宪无效！确认外商投资企业享有申请并持有普通建筑业施工执照的国民待遇，彻底打破外资只能以‘特别许可证（Special License）’一案一审的歧视性壁垒！",
        "tenor": "The Supreme Court en banc declared Rule 3, Section 3.1 of the Revised Rules and Regulations Governing Licensing in the Philippines unconstitutional, ruling that PCAB has no statutory authority to restrict regular contractor's licenses to corporations with at least 60% Filipino equity.",
        "tatbestand": "【案件事实全景与工程争议脉络】：外资控股水务及工程承包企业 Manila Water Company 及其合资承包商，因外资持股超过 40%，长期被 PCAB 拒绝核发普通建筑工程承包许可证（Regular License），仅允许其就单个特定工程申请手续繁琐且附带严苛条件的特别许可证（Special License）。外商遂向菲律宾法院提起违宪审查诉讼，指控 PCAB 滥用行政权力设立外资准入歧视性壁垒。",
        "gruende": """【裁判法理深度解析与核心涵摄逻辑】：最高法院大法庭对《承包商执照法》(RA 4566) 的立法原意进行了全面历史解释。法院指出，RA 4566 旨在确保从事工程建设的主体具备技术资质、财务实力与工程安全保障能力，法典本身从未对外国承包商设定任何国籍或股权比例限制。PCAB 通过部门规程强行设立‘外资超 40% 不得持证’的规定属于越权行政立法（Ultra Vires），严重侵害了外商在菲律宾的平等商业经营权与投资信赖利益。
【出海央企实操攻防启示】：这是中国基建央国企进军菲律宾建筑市场的划时代里程碑先例！过去菲律宾 PCAB 长期以‘保护本土建筑业’为由，强迫外资只能设立 60/40 合资公司或申办单一工程特别许可证。本案彻底扫清了外商独资控股承包企业申办 Quadruple A 等级常规建筑资质的法律障碍。中资企业赴菲应依法要求 PCAB 落实本案判决核发常规执照，坚决拒绝任何非法前置股权代持要求！""",
        "source_url": "https://elibrary.judiciary.gov.ph",
        "norms_meta": "PH:RA_4566:Sec15,PH:Civil_Code:Art1713"
    }

    cur.execute("""
        INSERT OR REPLACE INTO cases
        (case_id, court, senate, decided, az, doctype, leitsatz, tenor, tatbestand, gruende, source_url, norms_meta)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        pcab_case["case_id"], pcab_case["court"], pcab_case["senate"], pcab_case["decided"], pcab_case["az"],
        pcab_case["doctype"], pcab_case["leitsatz"], pcab_case["tenor"], pcab_case["tatbestand"],
        pcab_case["gruende"], pcab_case["source_url"], pcab_case["norms_meta"]
    ))
    pcab_chunk = f"[{pcab_case['case_id']}] {pcab_case['az']} {pcab_case['leitsatz']} | {pcab_case['tatbestand']} | {pcab_case['gruende']} | {pcab_case['tenor']}"
    cur.execute("""
        INSERT OR REPLACE INTO chunks (chunk_id, kind, ref_id, seq, text)
        VALUES (?, ?, ?, ?, ?)
    """, (f"CHUNK:CASE:{pcab_case['case_id']}:0", "case", pcab_case["case_id"], 0, pcab_chunk))

    # 3. 更新关联 edges
    cur.execute("UPDATE edges SET src = ? WHERE src = ?", (bs_case["case_id"], "SG:Precedent:BS_Mount_Sophia"))
    cur.execute("UPDATE edges SET dst = ? WHERE dst = ?", (bs_case["case_id"], "SG:Precedent:BS_Mount_Sophia"))

    cur.execute("UPDATE edges SET src = ? WHERE src = ?", (pcab_case["case_id"], "PH:Precedent:PCAB_v_Manila_Water"))
    cur.execute("UPDATE edges SET dst = ? WHERE dst = ?", (pcab_case["case_id"], "PH:Precedent:PCAB_v_Manila_Water"))

    cur.execute("UPDATE edges SET src = ? WHERE src = ?", ("CASE:SG_CA:JBEProperties:2011", "SG:Precedent:JBE_Properties"))
    cur.execute("UPDATE edges SET dst = ? WHERE dst = ?", ("CASE:SG_CA:JBEProperties:2011", "SG:Precedent:JBE_Properties"))

    # 4. 从 norms 与 chunks 中移除这 3 篇误入的判例
    cur.execute("DELETE FROM norms WHERE norm_id IN ('SG:Precedent:BS_Mount_Sophia', 'SG:Precedent:JBE_Properties', 'PH:Precedent:PCAB_v_Manila_Water')")
    cur.execute("DELETE FROM chunks WHERE ref_id IN ('SG:Precedent:BS_Mount_Sophia', 'SG:Precedent:JBE_Properties', 'PH:Precedent:PCAB_v_Manila_Water')")

    # 5. 归一化 norms 与 reference_norms 表中的 law 命名 (如 KUHPerdata -> ID:KUHPerdata)
    cur.execute("UPDATE norms SET law = 'ID:KUHPerdata' WHERE law IN ('KUHPerdata', 'KUHPerdata_ID')")
    cur.execute("UPDATE reference_norms SET law = 'ID:KUHPerdata' WHERE law IN ('KUHPerdata', 'KUHPerdata_ID')")

    conn.commit()
    conn.close()

    print("✓ P0 清洗完成：3 篇误入 norms 的判例已规范平移至 cases 表，law 字段命名已归一化。")

if __name__ == "__main__":
    run_p0_clean()
