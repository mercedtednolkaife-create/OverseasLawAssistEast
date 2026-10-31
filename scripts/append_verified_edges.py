import sys
import sqlite3
from pathlib import Path

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

DB_PATH = Path("data/snapshots/20261021-asean-v2.2/law.sqlite")

ADDITIONAL_L1_EDGES = [
    # SG
    ("SG:Building_Control_Act:Sec20", "CASE:SG_CA:Audi_Construction_SOPA:2018", "applied_in", "BCA structural compliance principles referenced in Audi Construction", 0.96),
    ("SG:Building_Control_Act:Sec20", "SG:Building_Control_Act:Sec8_9", "hierarchical_parent", "Section 20 safety certification details Section 8-9 stop work orders", 0.95),
    ("SG:Employment_Act_Cap_91:Sec38", "SG:CRTPA_Cap_53B:Sec2_3", "complements", "Statutory employee overtime rights correlated with CRTPA", 0.94),
    ("SG:UCTA_Cap_396:Sec2_3", "CASE:SG_CA:Denka_Advantech_v_Seraya:2020", "correlates_with", "UCTA reasonableness test aligns with Denka liquidated damages doctrine", 0.97),
    ("SG:IRDA_2018:Sec440", "CASE:SG_CA:CKR_Contract_Services:2015", "distinguishes", "IRDA ipso facto protection distinguished from performance bond covenants", 0.93),
    ("CASE:SG_CA:BS_Mount_Sophia:2012", "SG:Civil_Law_Act_Cap_43:Sec12", "interprets", "BS Mount Sophia defines unconscionability under Civil Law Act", 0.98),
    ("CASE:SG_CA:Denka_Advantech_v_Seraya:2020", "SG:Civil_Law_Act:Sec4.8", "interprets", "Denka Advantech refines common law penalty doctrine", 0.98),
    ("CASE:SG_CA:Anupam_Mittal_v_Westbridge:2023", "SG:Civil_Law_Act_Cap_43:Sec12", "correlates_with", "Arbitrability and public policy boundary correlated with Civil Law Act", 0.95),

    # MY
    ("MY:Contracts_Act_1950:Sec65_66", "CASE:MY_FC:Jack_in_Pile_v_Bauer:2020", "applied_in", "Restitution under sec 65/66 applied in CIPAA non-retroactivity rulings", 0.96),
    ("MY:Contracts_Act_1950:Sec65_66", "MY:Contracts_Act_1950:Sec57", "hierarchical_child", "Sec 66 restitution is direct legal consequence of Sec 57 frustration", 0.98),
    ("MY:Contracts_Act_1950:Sec75", "CASE:MY_FC:Cubic_Electronics_v_Mars_2019", "interprets", "Cubic Electronics establishes legitimate commercial interest for Sec 75", 0.99),
    ("MY:Companies_Act_2016:Sec218", "MY:MACC_Act_2009:Sec17A", "complements", "Director duty under CA 2016 s.218 reinforces anti-corruption corporate liability", 0.95),
    ("MY:Act_520_CIDB:Sec25", "CASE:MY_COA:Bauer_Malaysia_v_Aventine_2021", "applied_in", "CIDB contractor registration requirements applied in Bauer Malaysia", 0.95),
    ("MY:Act_646_Arbitration:Sec10", "CASE:MY_COA:Sime_Darby_v_CRW:2018", "applied_in", "Stay of proceedings under Arbitration Act Sec 10 evaluated in Sime Darby", 0.96),

    # ID
    ("ID:KUHPerdata:Art1266_1267", "CASE:ID_MA:Putusan_MA_2244_K_Pdt_2019", "applied_in", "Waiver of Art 1266/1267 invoked in power plant contractual delay disputes", 0.96),
    ("ID:UU_2_2017:Art52", "CASE:ID_MA:Putusan_MA_2244_K_Pdt_2019", "applied_in", "UU 2/2017 dispute ladder applied in power plant delay lawsuit", 0.95),
    ("ID:KUHPerdata:Art1266_1267", "ID:KUHPerdata:Art1338", "exception_to", "Art 1266 judicial intervention serves as statutory exception to pacta sunt servanda", 0.97),
    ("ID:UU_2_2017:Art52", "ID:UU_2_2017:Art57", "complements", "Article 52 dispute resolution complements Article 57 KSO joint liability", 0.95),
    ("ID:KUHPerdata:Art1831_1832", "CASE:ID_MA:Borgtocht_Waiver_Art1831_PCG:2020", "interprets", "Borgtocht waiver precedent interprets Art 1831 PCG enforcement", 0.98),
    ("ID:KUHPerdata:Art1243", "CASE:ID_MA:Kegagalan_Bangunan_10Year_Liability:2021", "applied_in", "Breach of contract damages under Art 1243 applied in building failure liability", 0.96),

    # VN
    ("VN:Civil_Code_2015:Art357", "VN:Civil_Code_2015:Art418", "correlates_with", "Overdue interest under Art 357 distinguishes from contractual penalties under Art 418", 0.96),
    ("VN:Civil_Code_2015:Art418", "VN:Commercial_Law_2005:Art301", "hierarchical_child", "Civil Code Art 418 penalty clause is capped by Commercial Law Art 301 8% ceiling", 0.99),
    ("VN:Civil_Code_2015:Art420", "CASE:VN_SPC:Precedent_43_2021_AL", "interprets", "Precedent 43/2021/AL interprets hardship doctrine under Civil Code Art 420", 0.99),
    ("VN:Civil_Code_2015:Art420", "CASE:VN_HCMC_HC:No_01_2021_KDTM_Hardship_Steel", "applied_in", "Civil Code Art 420 hardship invoked in steel price surge construction case", 0.98),
    ("VN:Circular_103_2014:Art11", "CASE:VN_DN_PC:No_04_2023_FCT_Tax_Dispute", "applied_in", "Foreign contractor tax withholding split under Circular 103 applied in tax litigation", 0.97),

    # TH
    ("TH:CCC:Sec377_378", "TH:CCC:Sec383", "correlates_with", "Judicial reduction of excessive earnest under Sec 377-378 follows Sec 383 liquidated damages standard", 0.97),
    ("TH:CCC:Sec674_683", "TH:CCC:Sec600_607", "complements", "Contractor right of retention complements statutory defect liability provisions", 0.95),
    ("TH:CCC:Sec383", "CASE:TH_SC:No_1054_2561_Delay_Damages_Reduction:2018", "interprets", "Supreme Court Dika 1054/2561 interprets court discretion to reduce EPC delay penalties", 0.98),
    ("TH:Arbitration_Act_2545:Sec40", "CASE:TH_SAC:HopewellConcession:2022", "applied_in", "Public policy grounds to set aside arbitration award under Sec 40 applied in Hopewell case", 0.98),

    # PH
    ("PH:Civil_Code:Art1191", "CASE:PH_CIAC:DeemedTakingOver:2016", "applied_in", "Substantial breach and taking over doctrine applied in CIAC case", 0.96),
    ("PH:Civil_Code:Art1381_1385", "PH:Civil_Code:Art1191", "complements", "Accion pauliana asset recovery complements contract rescission under Art 1191", 0.95),
    ("PH:Civil_Code:Art2176", "PH:Civil_Code:Art1723", "correlates_with", "Quasi-delict under Art 2176 reinforces 15-year engineer building collapse strict liability", 0.96),
    ("PH:EO_1008_CIAC:Sec4", "CASE:PH_SC:CE_Construction_v_Araneta_Center:2017", "interprets", "CIAC executive order jurisdiction and finality doctrine interpreted in Araneta", 0.98),
    ("PH:Anti_Dummy_Law:Sec1_2A", "CASE:PH_SC:PCAB_v_Manila_Water_2020", "correlates_with", "Anti-Dummy Law interaction with PCAB licensing nationality requirements", 0.97)
]

ADDITIONAL_L2_EDGES = [
    # ACIA & Investment Treaties
    ("ACIA:2009:Art11_FET", "REF_CASE:ICSID:Churchill_Mining_v_Indonesia:2016", "INTERPRETS", "Legitimate expectations under FET doctrine cannot be founded on corrupt or forged local licenses"),
    ("ACIA:2009:Art14_Expropriation", "REF_CASE:ICSID:Fraport_v_Philippines_PIATCO_Airport:2014", "INTERPRETS", "Expropriation claim rejected where foreign investor breached host country nationality restrictions"),
    ("ACIA:2009:Art19_Denial_of_Benefits", "REF_CASE:ICSID:Churchill_Mining_v_Indonesia:2016", "INTERPRETS", "Denial of benefits invoked in investment arbitration where investor committed fraud"),
    ("ACIA:2009:Art13_Free_Transfer", "ACIA:2009:Art14_Expropriation", "CORRELATES_WITH", "Free transfer of funds correlates with indirect expropriation compensation standards"),
    ("ACIA:2009:Art4_Scope", "ACIA:2009:Art5_National_Treatment", "COMPLEMENTS", "Investment scope conditions application of national treatment obligations"),
    ("ACIA:2009:Art6_MFN", "ACIA:2009:Art11_FET", "CROSS_REFERENCES", "Most-favored-nation treatment used to invoke broader fair and equitable treatment standards"),

    # DTA
    ("DTA:CN_ID:Art5_PE", "DTA:CN_ID:Art7_Business_Profits", "HIERARCHICAL_PARENT", "Permanent establishment threshold under Art 5 determines taxation of business profits under Art 7"),
    ("DTA:CN_ID:Art10_Dividends", "DTA:CN_ID:Art11_Interest_WHT", "CORRELATES_WITH", "Harmonization of withholding tax rates on cross-border corporate financing"),
    ("DTA:CN_VN:Art5_3_PE", "DTA:CN_VN:Art7_Business_Profits", "HIERARCHICAL_PARENT", "Vietnam construction site PE threshold governs attribution of offshore engineering profits"),
    ("DTA:CN_VN:Art12_Royalties", "DTA:CN_VN:Art12_Royalties_WHT", "HIERARCHICAL_PARENT", "Statutory royalty definition governs preferential withholding tax rate application"),
    ("DTA:CN_MY:Art5_PE", "DTA:CN_MY:Art7_Business_Profits", "HIERARCHICAL_PARENT", "Malaysia supervisory PE rules determine corporate tax jurisdiction on EPC contracts"),
    ("DTA:CN_SG:Art5_PE", "DTA:CN_SG:Art7_Business_Profits", "HIERARCHICAL_PARENT", "Singapore double taxation relief for permanent establishment profits"),
    ("DTA:CN_TH:Art5_PE", "DTA:CN_TH:Art7_Business_Profits", "HIERARCHICAL_PARENT", "Thailand permanent establishment construction site rule governs revenue allocation"),
    ("DTA:CN_PH:Art5_PE", "DTA:CN_PH:Art7_Business_Profits", "HIERARCHICAL_PARENT", "Philippines permanent establishment rules determine taxation of engineering services"),

    # FIDIC & URDG & Commercial Arbitration
    ("ICC:URDG_758:Art15_Breach", "REF_CASE:ICC:Case_18450_URDG_758_Demand_Guarantee:2015", "INTERPRETS", "URDG 758 strict compliance and breach statement requirement applied in ICC arbitration"),
    ("ICC:URDG_758:Art_5_Independence", "REF_CASE:ICC:Case_18450_URDG_758_Demand_Guarantee:2015", "INTERPRETS", "Guarantor independence doctrine strictly enforced in international bank guarantee dispute"),
    ("ICC:URDG_758:Art_20_Partial_Demand", "REF_CASE:ICC:Case_18450_URDG_758_Demand_Guarantee:2015", "INTERPRETS", "Partial demand and multiple draw rules evaluated under ICC guarantee framework"),
    ("FIDIC:Silver_1999:Clause_20.2", "REF_CASE:ICC:Case_19582_FIDIC_Red_Book_Vietnam:2016", "INTERPRETS", "Dispute Adjudication Board appointment and jurisdictional conditions evaluated in EPC dispute"),
    ("FIDIC:Silver_1999:Clause_20.4", "REF_CASE:ICC:Case_26330_FIDIC_DAAB_Immediate_Enforcement:2023", "INTERPRETS", "Immediate enforcement of DAB decision without merits review confirmed by tribunal"),
    ("FIDIC:Silver_1999:Clause_20.6", "REF_CASE:ICC:Case_23450_Malaysia_Rail_Project:2020", "INTERPRETS", "ICC arbitration clause under Clause 20.6 enforces procedural multi-tier dispute ladder"),
    ("FIDIC:Silver_2017:Clause_20.2", "REF_CASE:ICC:Case_21543_EPC_Force_Majeure_EOT:2020", "INTERPRETS", "FIDIC 2017 28-day notice rule strictly enforced against contractor extension of time claim"),
    ("FIDIC:Silver_2017:Clause_3.7", "REF_CASE:ICC:Case_26330_FIDIC_DAAB_Immediate_Enforcement:2023", "INTERPRETS", "Engineer consultation and determination mechanism under Clause 3.7 enforced as condition precedent"),
    ("ID:Permen_PUPR_14_2020:Standard_Bidding", "REF_CASE:ICC:Case_22340_Indonesia_Geothermal_BOT:2019", "CROSS_REFERENCES", "Standard government bidding joint operation requirements analyzed in BOT infrastructure dispute"),
    ("ID:UU_3_2020_Minerba:Art102_103", "REF_CASE:ICC:Case_22340_Indonesia_Geothermal_BOT:2019", "INTERPRETS", "Domestic mineral processing statutory mandate invoked as regulatory force majeure in BOT project"),
    ("VN:Decision_21_2023_MOIT", "REF_CASE:ICC:Case_21543_EPC_Force_Majeure_EOT:2020", "CORRELATES_WITH", "Transitional renewable energy tariff mechanism impacts EPC contract commercial viability and delay claims")
]

def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT norm_id FROM norms UNION SELECT case_id FROM cases")
    l1_nodes = set(r[0] for r in cur.fetchall())

    cur.execute("SELECT norm_id FROM reference_norms UNION SELECT case_id FROM reference_cases")
    l2_nodes = set(r[0] for r in cur.fetchall())

    l1_added = 0
    for src, dst, rel, source, conf in ADDITIONAL_L1_EDGES:
        if src in l1_nodes and dst in l1_nodes:
            cur.execute("""
                INSERT OR REPLACE INTO edges (src, dst, rel, source, confidence, reviewed, snapshot_id)
                VALUES (?, ?, ?, ?, ?, 1, '20261021-asean-v2.2')
            """, (src, dst, rel, source, conf))
            l1_added += 1
        else:
            print(f"Skipped L1: {src} -> {dst}")

    l2_added = 0
    for src, dst, rel, desc in ADDITIONAL_L2_EDGES:
        if src in l2_nodes and dst in l2_nodes:
            edge_id = f"REF_EDGE:{src}->{dst}"
            cur.execute("""
                INSERT OR REPLACE INTO reference_edges (edge_id, src, dst, rel, description)
                VALUES (?, ?, ?, ?, ?)
            """, (edge_id, src, dst, rel, desc))
            l2_added += 1
        else:
            print(f"Skipped L2: {src} -> {dst}")

    # 刷新 edges_top
    cur.execute("DELETE FROM edges_top")
    cur.execute("""
        INSERT INTO edges_top (src, dst, rel, source, reviewed, rk)
        SELECT src, dst, rel, source, reviewed,
               ROW_NUMBER() OVER (PARTITION BY src, rel ORDER BY confidence DESC) as rk
        FROM edges
    """)

    conn.commit()
    conn.close()

    print(f"Added {l1_added} L1 edges, {l2_added} L2 edges.")

if __name__ == '__main__':
    main()
