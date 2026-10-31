# -*- coding: utf-8 -*-
"""
拓扑因果关系与规范演进边 (L1 edges 与 L2 reference_edges)
两端节点严格闭环隔离，悬空边严格为 0。
"""

L1_EDGES = [
    # 印尼
    ("ID:KUHPerdata:Art1604_1616", "interprets", "CASE:ID_MA:Putusan_MA_601_K_Pdt_2015"),
    ("ID:KUHPerdata:Art1604_1616", "complements", "ID:KUHPerdata:Art1266"),
    ("ID:KUHPerdata:Art1967", "complements", "ID:KUHPerdata:Art1604_1616"),
    ("ID:PP_22_2020:Art14_21", "complements", "ID:UU_2_2017:Art57"),
    ("ID:PP_19_2021:PSN_Land", "complements", "ID:UU_2_2012:Art14"),
    ("ID:UU_21_2023:IKN_Capital", "complements", "ID:UU_6_2023_CiptaKerja:Art42"),
    ("ID:PERMA_3_2023:Art6_10", "interprets", "CASE:ID_MA:Tempo_v_Roche_2015"),
    ("ID:PERMA_3_2023:Art16_24", "interprets", "CASE:ID_MA:Putusan_MA_2244_K_Pdt_2019"),
    ("CASE:ID_MA:Pelindo_Immunity_2018", "applied_in", "ID:UU_1_2004:Art50"),
    ("CASE:ID_MA:DMRI_PKPU_2021", "applied_in", "ID:KUHPerdata:Art1831_1832"),

    # 越南
    ("VN:Law_61_2024_QH15:Art12_18", "complements", "VN:Law_61_2020:Art24_26"),
    ("VN:Resolution_01_2019_NQ_HDTP:Interest", "interprets", "CASE:VN_SPC:An_Le_08_2016_AL"),
    ("VN:Resolution_01_2014_NQ_HDTP:Art14", "interprets", "CASE:VN_SPC:An_Le_69_2023_AL"),
    ("VN:Law_29_2023_QH15:Art23_25", "complements", "VN:Law_31_2024:Art127_128"),
    ("CASE:VN_SPC:An_Le_37_2020_AL", "applied_in", "VN:Civil_Code_2015:Art420"),
    ("CASE:VN_SPC:An_Le_52_2021_AL", "applied_in", "VN:Law_31_2024:Art127_128"),

    # 马来西亚
    ("MY:Specific_Relief_Act_1950:Sec20_21", "complements", "MY:Contracts_Act_1950:Sec57"),
    ("MY:Specific_Relief_Act_1950:Sec50_53", "interprets", "CASE:MY_FC:Tindak_Murni_2020"),
    ("MY:Arbitration_Amendment_Act_2024:Sec4_7", "complements", "MY:Arbitration_Act_2005:Sec37"),
    ("MY:National_Land_Code_Act828:Sec221_228", "complements", "MY:National_Land_Code_Act828:Sec433B"),
    ("MY:Housing_Development_Act_118:Schedule_H", "complements", "MY:Contracts_Act_1950:Sec75"),
    ("CASE:MY_FC:SK_ME_Bersekutu_2019", "applied_in", "MY:Contracts_Act_1950:Sec57"),
    ("CASE:MY_FC:Sim_Siok_Eng_1978", "applied_in", "MY:Contracts_Act_1950:Sec75"),
    ("CASE:MY_FC:Ireka_Engineering_2020", "applied_in", "MY:CIPAA_2012:Sec35"),

    # 新加坡
    ("SG:SCJA_Cap322:Sec18D_18M", "complements", "SG:Building_Control_Act:Sec8_9"),
    ("SG:RECJA_1959_CCAA_2016:Foreign_Judgments", "complements", "SG:IRDA_2018:Sec440"),
    ("SG:WSH_Design_for_Safety_2015:Reg4_6", "complements", "SG:Building_Control_Act:Sec8_9"),
    ("SG:Building_Control_Licensing_Regs:CW01_CW02", "complements", "SG:Building_Control_Act:Sec8_9"),
    ("CASE:SG_CA:Orion_One_v_Dong_Cheng_2020", "applied_in", "SG:SOPA_2004:Sec15"),
    ("CASE:SG_CA:LW_Infrastructure_2012", "applied_in", "SG:Building_Control_Act:Sec8_9"),
    ("CASE:SG_CA:Diamond_Glass_2021", "applied_in", "SG:SOPA_2004:Sec15"),
    ("CASE:SG_CA:CAJ_v_CAI_2021", "applied_in", "SG:Building_Control_Act:Sec8_9"),

    # 泰国
    ("TH:Administrative_Court_Act_2542:Sec3_9_51", "interprets", "CASE:TH_SAC:Assembly_Or_221_223_2564"),
    ("TH:Administrative_Court_Act_2542:Sec3_9_51", "applied_in", "CASE:TH_SAC:Hopewell_Concession_2022"),
    ("TH:Business_Security_Act_2558:Sec8_15", "complements", "TH:CCC:Sec383"),
    ("TH:CCC:Sec681_1_686_Guarantee", "complements", "TH:CCC:Sec383"),
    ("CASE:TH_SC:Supreme_Court_6388_2556", "applied_in", "TH:CCC:Sec383"),

    # 菲律宾
    ("PH:DOE_DC2022_11_0034:Renewable_Energy", "complements", "PH:RA_11659_PSA_2022:Sec2_4"),
    ("PH:RA_12009:New_Government_Procurement_2024", "complements", "PH:EO_1008_CIAC:Sec4"),
    ("PH:Civil_Code:Art2242_2249", "complements", "PH:Civil_Code:Art1723"),
    ("PH:SC_Special_ADR_Rules:Rule12_13", "interprets", "CASE:PH_SC:CE_Construction_v_Araneta_2017"),
    ("CASE:PH_SC:Frabelle_Fishing_v_PAGCOR_2007", "applied_in", "PH:Civil_Code:Art1723"),
    ("CASE:PH_SC:DPWH_v_CMC_Monark_2017", "applied_in", "PH:EO_1008_CIAC:Sec4"),
    ("CASE:PH_SC:Wyeth_v_CIAC_2019", "applied_in", "PH:EO_1008_CIAC:Sec4"),

    # 中国涉外母法
    ("CN:Civil_Procedure_Law_2023:Foreign_Related_Sec", "governs", "CN:SPC_Foreign_Law_Ascertainment_2023:Art1_3"),
    ("CN:Civil_Procedure_Law_2023:Foreign_Related_Sec", "governs", "CN:SPC_Foreign_Law_Ascertainment_2023:Art8_11"),
    ("CN:SPC_Foreign_Law_Ascertainment_2023:Art6_10", "complements", "CN:SPC_Foreign_Law_Ascertainment_2023:Art8_11"),
    ("CN:SPC_Foreign_Law_Ascertainment_2023:Art6_10", "governs", "CASE:SG_CA:Orion_One_v_Dong_Cheng_2020"),
    ("CN:SPC_Foreign_Law_Ascertainment_2023:Art6_10", "governs", "CASE:MY_FC:Cubic_Electronics_2019")
]

L2_EDGES = [
    ("TREATY:CAFTA_3.0_Upgrade:2024", "INTERPRETS", "REF_CASE:PCA:Trinh_Vinh_Binh_v_Vietnam:2019"),
    ("TREATY:DTA_BEPS_MLI:Art14_PE_Anti_Split", "complements", "DTA:CN_ID:Art5_Art7"),
    ("TREATY:DTA_BEPS_MLI:Art14_PE_Anti_Split", "complements", "DTA:CN_VN:Art5_Art12"),
    ("STD_CONTRACT:SG_PSSCOC_2020:Clause14_31", "complements", "FIDIC:2017_Suite:Clause_21"),
    ("STD_CONTRACT:MY_PWD_203A:Clause40_43", "complements", "FIDIC:2017_Suite:Clause_20.2"),
    ("REG:VN_Decree_80_2024:DPPA", "complements", "VN:Decree_15_2021:Art102_103"),
    ("LAW:ID_UU_27_2022_PDP:Cross_Border", "complements", "ID:UU_3_2020_Minerba:Art102_103"),
    ("LAW:SG_IRDA_2018:Cross_Border_Insolvency", "complements", "FIDIC:2017_Suite:Clause_21"),
    ("REF_CASE:SG_CA:CRW_Joint_Operation_v_PGN:2011_2015", "INTERPRETS", "FIDIC:2017_Suite:Clause_21"),
    ("REF_CASE:SG_CA:BBA_v_BAZ:2020", "INTERPRETS", "ICC:URDG_758:Art15_20"),
    ("REF_CASE:PCA:Trinh_Vinh_Binh_v_Vietnam:2019", "INTERPRETS", "DTA:CN_VN:Art5_Art12")
]
