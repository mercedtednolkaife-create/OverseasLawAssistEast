import sys
import sqlite3
import re
from pathlib import Path

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

DB_PATH = Path("data/snapshots/20261021-asean-v2.2/law.sqlite")
REVIEW_PATH = Path(r"C:\Downloads\OverseasLawAssistEast\数据库审查.md")

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# Get all IDs in DB
c.execute("SELECT norm_id FROM norms")
norms_l1 = set(r[0] for r in c.fetchall())

c.execute("SELECT norm_id FROM reference_norms")
norms_l2 = set(r[0] for r in c.fetchall())

c.execute("SELECT case_id FROM cases")
cases_l1 = set(r[0] for r in c.fetchall())

c.execute("SELECT case_id FROM reference_cases")
cases_l2 = set(r[0] for r in c.fetchall())

all_norms = norms_l1 | norms_l2
all_cases = cases_l1 | cases_l2
all_ids = all_norms | all_cases

print(f"Total IDs in DB: norms_l1={len(norms_l1)}, norms_l2={len(norms_l2)}, cases_l1={len(cases_l1)}, cases_l2={len(cases_l2)}")

# Read review file and extract specific items
with open(REVIEW_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# Specifically check Third Part L1 statutes and cases mentioned
part3_statutes = [
    "VN:Civil_Code_2015:Art420",
    "VN:Law_31_2024:Art127_128",
    "VN:Law_61_2020:Art24_26",
    "VN:Civil_Procedure_Code_2015:Art111_114",
    "VN:Decree_70_2023:Art1_2",
    "ID:KUHPerdata:Art1831_1832",
    "ID:UU_6_2023_CiptaKerja:Art42",
    "ID:UU_7_2011_Currency:Art21",
    "ID:UU_4_1996_HakTanggungan:Art4",
    "ID:PERMA_3_2023:Art4_5",
    "MY:Contracts_Act_1950:Sec57",
    "MY:OSHA_1994_ActA1648:Sec15_20",
    "MY:National_Land_Code_Act828:Sec433B",
    "MY:MACC_Act_2009:Sec17A",
    "SG:Building_Control_Act:Sec8_9",
    "SG:UCTA_Cap_396:Sec2_3",
    "SG:IRDA_2018:Sec440",
    "TH:CCC:Sec383",
    "TH:CCC:Sec600_607",
    "TH:FBA_1999:Sec36",
    "PH:Civil_Code:Art1723",
    "PH:RA_11659_PSA_2022:Sec2_4",
    "PH:EO_1008_CIAC:Sec4",
    "CN:SPC_Foreign_Law_Ascertainment_2023:Art1_3",
    "CN:SPC_Foreign_Law_Ascertainment_2023:Art8_11",
    "CN:NDRC_Order_11:Art13_14",
    "CN:SAFE_Notice_29:Art12_13"
]

part3_cases = [
    "CASE:VN_SPC:Precedent_43_2021_AL",
    "CASE:VN_Hanoi_HC:VIAC_Award_Enforcement_2022",
    "CASE:ID_MA:Putusan_MA_2244_K_Pdt_2019",
    "CASE:ID_PN_JakPus:EPC_Bond_PMH_Injunction_2021",
    "CASE:MY_FC:Cubic_Electronics_2019",
    "CASE:MY_FC:Jack_In_Pile_v_Bauer_2020",
    "CASE:SG_CA:Denka_Advantech_2020",
    "CASE:SG_CA:CKR_Contract_Services_2015",
    "CASE:TH_SAC:Hopewell_Concession_2022",
    "CASE:TH_SC:Supreme_Court_1054_2561",
    "CASE:PH_SC:PCAB_v_Manila_Water_2020",
    "CASE:PH_SC:CE_Construction_v_Araneta_2017"
]

part4_statutes = [
    "VN:Decree_15_2021:Art102_103",
    "VN:Decree_10_2021:Art14_15",
    "ID:Permen_PUPR_14_2020:Standard_Bidding",
    "VN:Decision_21_2023_MOIT",
    "ID:UU_3_2020_Minerba:Art102_103",
    "FIDIC:2017_Suite:Clause_20.2",
    "FIDIC:2017_Suite:Clause_21",
    "ICC:URDG_758:Art15_20",
    "DTA:CN_ID:Art5_Art7",
    "DTA:CN_VN:Art5_Art12"
]

part4_cases = [
    "REF_CASE:ICSID:Churchill_Mining_v_Indonesia:2016",
    "REF_CASE:ICSID:Fraport_v_Philippines:2014",
    "REF_CASE:PCA:Walter_Bau_v_Thailand:2009"
]

def check_list(name, id_list, target_set):
    print(f"\n--- Checking {name} ({len(id_list)} items) ---")
    matched = 0
    for item in id_list:
        if item in target_set:
            matched += 1
            print(f"  [EXACT MATCH] {item}")
        else:
            # check fuzzy
            fuzzy = [x for x in target_set if item.lower() in x.lower() or x.lower() in item.lower()]
            if fuzzy:
                matched += 1
                print(f"  [FUZZY MATCH] {item} -> {fuzzy}")
            else:
                print(f"  [MISSING] {item}")
    print(f"Result for {name}: {matched}/{len(id_list)} matched.")

check_list("Part 3 L1 Statutes", part3_statutes, norms_l1)
check_list("Part 3 L1 Cases", part3_cases, cases_l1)
check_list("Part 4 L2 Statutes", part4_statutes, norms_l2)
check_list("Part 4 L2 Cases", part4_cases, cases_l2)

conn.close()
