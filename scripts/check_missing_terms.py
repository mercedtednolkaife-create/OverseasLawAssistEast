import sys
import sqlite3
from pathlib import Path

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

DB_PATH = Path("data/snapshots/20261021-asean-v2.2/law.sqlite")
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

def search_any(term):
    results = {}
    for tbl, col in [('norms', 'norm_id'), ('reference_norms', 'norm_id'), ('cases', 'case_id'), ('reference_cases', 'case_id')]:
        c.execute(f"SELECT {col} FROM {tbl} WHERE {col} LIKE '%{term}%' OR {col} LIKE '%{term.replace(':', '_')}%'")
        matches = [r[0] for r in c.fetchall()]
        if matches:
            results[tbl] = matches
    return results

terms_to_check = [
    # L1 Statutes
    ("PERMA_3_2023", "ID:PERMA_3_2023:Art4_5"),
    ("OSHA", "MY:OSHA_1994_ActA1648:Sec15_20"),
    ("433B", "MY:National_Land_Code_Act828:Sec433B"),
    ("Art8_11", "CN:SPC_Foreign_Law_Ascertainment_2023:Art8_11"),
    ("Order_11", "CN:NDRC_Order_11:Art13_14"),
    
    # L1 Cases
    ("Precedent_43", "CASE:VN_SPC:Precedent_43_2021_AL"),
    ("VIAC_Award", "CASE:VN_Hanoi_HC:VIAC_Award_Enforcement_2022"),
    ("2244", "CASE:ID_MA:Putusan_MA_2244_K_Pdt_2019"),
    ("EPC_Bond_PMH", "CASE:ID_PN_JakPus:EPC_Bond_PMH_Injunction_2021"),
    ("Cubic", "CASE:MY_FC:Cubic_Electronics_2019"),
    ("Denka", "CASE:SG_CA:Denka_Advantech_2020"),
    ("CKR", "CASE:SG_CA:CKR_Contract_Services_2015"),
    ("Hopewell", "CASE:TH_SAC:Hopewell_Concession_2022"),
    ("1054", "CASE:TH_SC:Supreme_Court_1054_2561"),
    ("Araneta", "CASE:PH_SC:CE_Construction_v_Araneta_2017"),
    
    # L2 Statutes
    ("Decree_15_2021", "VN:Decree_15_2021:Art102_103"),
    ("Decree_10_2021", "VN:Decree_10_2021:Art14_15"),
    ("Clause_21", "FIDIC:2017_Suite:Clause_21"),
    ("URDG_758", "ICC:URDG_758:Art15_20"),
    ("Art5_Art7", "DTA:CN_ID:Art5_Art7"),
    ("Art5_Art12", "DTA:CN_VN:Art5_Art12"),
    
    # L2 Cases
    ("Fraport", "REF_CASE:ICSID:Fraport_v_Philippines:2014"),
    ("Walter_Bau", "REF_CASE:PCA:Walter_Bau_v_Thailand:2009")
]

for term, original in terms_to_check:
    res = search_any(term)
    print(f"\nSearching for '{term}' (Review spec: {original}):")
    if res:
        for tbl, matches in res.items():
            print(f"  In {tbl}: {matches}")
    else:
        print("  --> NOT FOUND")

conn.close()
