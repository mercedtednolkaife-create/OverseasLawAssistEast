"""只读快照库与快照生命周期管理器 (SnapshotManager)
对齐技术方案第 3.4 节与第 4.8 节：
- 案件固定快照 ID，恢复与追加问题沿用案件快照
- 内存中保留当前快照与上一个快照 (keep=2)
- 原子读取 data/current_snapshot 指针
"""

import os
import sqlite3
import threading
from typing import Optional, Dict, Any, List

KNOWN_NORM_ALIASES = {
    "ID_MEMR:REG11_2024": "ID:MEMR_11_2024",
    "ID_MEMR:11_2024": "ID:MEMR_11_2024",
    "ID_MEMR_11_2024": "ID:MEMR_11_2024",
    "ID:MEMR:REG11_2024": "ID:MEMR_11_2024",
    "ID_UU:2_2017:ART57": "ID:UU_2_2017:Art57",
    "ID_UU_2_2017:ART57": "ID:UU_2_2017:Art57",
    "ID_SEMA:3_2023": "ID:SEMA_3_2023",
    "ID_SEMA_3_2023": "ID:SEMA_3_2023",
    "VN_LAW135_2025:ART86_2": "VN:Law_135_2025:Art86.2",
    "VN_LAW135_2025:ART86.2": "VN:Law_135_2025:Art86.2",
    "VN_LAW_135_2025:ART86.2": "VN:Law_135_2025:Art86.2",
    "VN_LAW135_2025:ART146": "VN:Law_135_2025:Art146",
    "VN_DECREE210_2026:ART18": "VN:Decree_210_2026:Art18",
    "MY_CIPAA:SEC35": "MY:CIPAA_2012:Sec35",
    "MY_CIPAA:35": "MY:CIPAA_2012:Sec35",
    "MY_CIPAA_2012:SEC35": "MY:CIPAA_2012:Sec35",
    "MY_CIPAA:SEC13": "MY:CIPAA_2012:Sec13",
    "MY_CIPAA_2012:SEC13": "MY:CIPAA_2012:Sec13",
    "MY_ACT520:SEC25": "MY:Act_520_CIDB:Sec25",
    "MY_ACT_520_CIDB:SEC25": "MY:Act_520_CIDB:Sec25",
    "SG_SOPA:SEC9": "SG:SOPA_2004:Sec9",
    "SG_SOPA_2004:SEC9": "SG:SOPA_2004:Sec9",
    "SG_IAA:SEC12A": "SG:IAA_Cap_143A:Sec12A",
    "SG_IAA_CAP_143A:SEC12A": "SG:IAA_Cap_143A:Sec12A",
    "PH_RA11966:SEC18": "PH:RA_11966:Sec18",
    "PH_RA11966:PPP_CODE": "PH:RA_11966:Sec18",
    "PH_RA_11966:SEC18": "PH:RA_11966:Sec18",
    "TREATY:CN_ID_BIT:ART4": "TREATY:CN_ID_BIT_1992:Art4",
    "CN_ID_BIT:ART4": "TREATY:CN_ID_BIT_1992:Art4",
    "BIT_CHINA_ASEAN:ART6": "TREATY:CN_ID_BIT_1992:Art4",
    "PRC_SASAC:ORDER35": "CN:SASAC_Order_35:Art12",
    "PRC_DATA_SECURITY:ART36": "CN:Data_Security_Law:Art36",
    "DATA_SECURITY_LAW:ART36": "CN:Data_Security_Law:Art36",
    "SINOSURE:ART15": "SINOSURE:Overseas_Policy:Art15",
    "SINOSURE:OVERSEAS_POLICY:ART15": "SINOSURE:Overseas_Policy:Art15",
    "TH_FBA:LIST3": "TH:FBA_1999:List3",
    "TH_CCC:SEC596": "TH:CCC:Sec596",
    "FIDIC_SILVER:CLAUSE8.4": "FIDIC:Silver_1999:Clause_8.4",
    "FIDIC_SILVER:CLAUSE20.1": "FIDIC:Silver_1999:Clause_20.1",
    "FIDIC_SILVER:CLAUSE4.2": "FIDIC:Silver_1999:Clause_4.2",
    "FIDIC_SILVER:CLAUSE13.7": "FIDIC:Silver_1999:Clause_13.7",
    "FIDIC_SILVER:CLAUSE14.8": "FIDIC:Silver_1999:Clause_14.8",
    "VN_CIVIL_CODE:ART351": "VN:Civil_Code_2015:Art351",
    "VN_CIVIL_CODE:ART156": "VN:Civil_Code_2015:Art156",
    "VN_CIVIL_CODE:ART405": "VN:Civil_Code_2015:Art405",
    "VN_ELECTRICITY:ART28": "VN:Law_28_2004:Art28",
    "VN_INVESTMENT:ART9": "VN:Law_61_2020:Art9",
    "ID_PERPRES10_2021": "ID:Perpres_10_2021:Investment_List",
    "ID_ARBITRATION:ART66": "ID:UU_30_1999:Art66",
    "ID_UU30_1999:ART66": "ID:UU_30_1999:Art66",
    "ID_UU5_1960:ART3": "ID:UU_5_1960:Art3",
    "ID_UU24_2009:ART31": "ID:UU_24_2009:Art31",
    "ID_LANGUAGE_LAW:ART31": "ID:UU_24_2009:Art31",
    "MY_CONTRACTS:SEC75": "MY:Contracts_Act_1950:Sec75",
    "MY_CONTRACTS_ACT:SEC75": "MY:Contracts_Act_1950:Sec75",
    "MY_ARBITRATION:SEC11": "MY:Arbitration_Act_2005:Sec11",
    "MY_LIMITATION:SEC6": "MY:Limitation_Act_1953:Sec6",
    "SG_UCTA:SEC3": "SG:UCTA_Cap_396:Sec3",
    "SG_CIVIL_LAW:SEC4.8": "SG:Civil_Law_Act:Sec4.8",
    "TH_PPP:SEC50": "TH:PPP_Act_2562:Sec50",
    "TH_CCC:SEC383": "TH:CCC:Sec383",
    "TH_CCC:SEC674": "TH:CCC:Sec674",
    "PH_EO1008:SEC4": "PH:EO_1008:Sec4",
    "PH_CIAC:SEC4": "PH:EO_1008:Sec4",
    "PH_CIVIL_CODE:ART1715": "PH:Civil_Code:Art1715",
    "PH_RA9285:SEC34": "PH:RA_9285:Sec34",
    "FIDIC_SILVER:CLAUSE2.5": "FIDIC:Silver_1999:Clause_2.5",
    "FIDIC_SILVER:CLAUSE19.1": "FIDIC:Silver_1999:Clause_19.1",
    "FIDIC_SILVER:CLAUSE19.4": "FIDIC:Silver_1999:Clause_19.4",
    "FIDIC_SILVER:CLAUSE15.2": "FIDIC:Silver_1999:Clause_15.2",
    "FIDIC_SILVER:CLAUSE20.4": "FIDIC:Silver_1999:Clause_20.4",
    "FIDIC_YELLOW:CLAUSE17.3": "FIDIC:Yellow_1999:Clause_17.3",
    "FIDIC_RED:CLAUSE4.2": "FIDIC:Red_1999:Clause_4.2",
    "FIDIC_SILVER_2017:CLAUSE21.4": "FIDIC:Silver_2017:Clause_21.4",
    "CN_VN_BIT:ART4": "TREATY:CN_VN_BIT_1992:Art4",
    "CN_MY_BIT:ART5": "TREATY:CN_MY_BIT_1988:Art5",
    "CN_PH_BIT:ART4": "TREATY:CN_PH_BIT_1992:Art4",
    "CN_TH_BIT:ART5": "TREATY:CN_TH_BIT_1985:Art5",
    "ID_PP34_2021:ART3": "ID:PP_34_2021:Art3",
    "ID_LABOR:RPTKA": "ID:PP_34_2021:Art3",
    "ID_UU32_2009:ART40": "ID:UU_32_2009:Art40",
    "ID_AMDAL:ART40": "ID:UU_32_2009:Art40",
    "ID_PMK176_2009": "ID:PMK_176_2009:Art2",
    "ID_MASTERLIST": "ID:PMK_176_2009:Art2",
    "MY_EMPLOYMENT:SEC60K": "MY:Employment_Act_1955:Sec60K",
    "VN_LABOUR_CODE:ART151": "VN:Labour_Code_2019:Art151",
    "VN_FCT:ART11": "VN:Circular_103_2014:Art11",
    "TH_NEQA:SEC50": "TH:NEQA_2535:Sec50",
    "TH_EIA:SEC50": "TH:NEQA_2535:Sec50",
    "PH_RA10752:SEC5": "PH:RA_10752:Sec5",
    "FIDIC_SILVER:CLAUSE10.1": "FIDIC:Silver_1999:Clause_10.1",
    "FIDIC_SILVER:CLAUSE11.9": "FIDIC:Silver_1999:Clause_11.9",
    "FIDIC_SILVER:CLAUSE13.1": "FIDIC:Silver_1999:Clause_13.1",
    "FIDIC_SILVER:CLAUSE13.3": "FIDIC:Silver_1999:Clause_13.3",
    "FIDIC_YELLOW:CLAUSE12.3": "FIDIC:Yellow_1999:Clause_12.3",
    "FIDIC_SILVER_2017:CLAUSE13.3.1": "FIDIC:Silver_2017:Clause_13.3.1",
    "CN_SG_BIT:ART6": "TREATY:CN_SG_BIT_1985:Art6",
    # Phase 3: L1 核心争议攻防与涉外救济别名
    "ID_KUHPERDATA:ART1266": "ID:KUHPerdata:Art1266",
    "ID_CIVIL_CODE:ART1266": "ID:KUHPerdata:Art1266",
    "FIDIC_SILVER:CLAUSE16.1": "FIDIC:Silver_1999:Clause_16.1",
    "FIDIC_SILVER:CLAUSE16.2": "FIDIC:Silver_1999:Clause_16.2",
    "TH_CCC:SEC387": "TH:CCC:Sec387",
    "FIDIC_SILVER:CLAUSE1.14": "FIDIC:Silver_1999:Clause_1.14",
    "MY_PARTNERSHIP:SEC11": "MY:Partnership_Act_1961:Sec11",
    "MY_PARTNERSHIP_ACT:SEC11": "MY:Partnership_Act_1961:Sec11",
    "ID_KUHD:ART18": "ID:KUHD:Art18",
    "ID_COMMERCIAL_CODE:ART18": "ID:KUHD:Art18",
    "VN_CIVIL_CODE:ART509": "VN:Civil_Code_2015:Art509",
    "ID_STATE_TREASURY:ART50": "ID:UU_1_2004:Art50",
    "ID_UU1_2004:ART50": "ID:UU_1_2004:Art50",
    "ID_UU_1_2004:ART50": "ID:UU_1_2004:Art50",
    "SG_STATE_IMMUNITY:SEC5": "SG:State_Immunity_Act:Sec5",
    "MY_CIVIL_LAW:MAREVA": "MY:Civil_Law_Act:Mareva",
    "FIDIC_YELLOW:CLAUSE4.12": "FIDIC:Yellow_1999:Clause_4.12",
    "FIDIC_SILVER:CLAUSE4.10": "FIDIC:Silver_1999:Clause_4.10",
    "SG_MISREPRESENTATION:SEC2": "SG:Misrepresentation_Act:Sec2",
    "VN_TECH_TRANSFER:ART32": "VN:Law_07_2017:Art32",
    "VN_LAW07_2017:ART32": "VN:Law_07_2017:Art32",
    # Phase 4: L1 完善法源别名
    "VN_COMMERCIAL_LAW:ART301": "VN:Commercial_Law_2005:Art301",
    "VN_COMMERCIAL_LAW_2005:ART301": "VN:Commercial_Law_2005:Art301",
    "VN_COMMERCIAL_LAW:ART302": "VN:Commercial_Law_2005:Art302",
    "TH_ARBITRATION:SEC40": "TH:Arbitration_Act_2545:Sec40",
    "TH_ARBITRATION_ACT:SEC40": "TH:Arbitration_Act_2545:Sec40",
    "TH_CCC:SEC388": "TH:CCC:Sec388",
    "PH_CIVIL_CODE:ART1229": "PH:Civil_Code:Art1229",
    "PH_RA9184:SEC68": "PH:RA_9184:Sec68",
    "PH_PROCUREMENT:SEC68": "PH:RA_9184:Sec68",
    "MY_CIPAA:SEC30": "MY:CIPAA_2012:Sec30",
    "MY_CIPAA_2012:SEC30": "MY:CIPAA_2012:Sec30",
    "MY_LIMITATION:SEC6A": "MY:Limitation_Act_1953:Sec6A",
    "SG_SOPA:SEC15": "SG:SOPA_2004:Sec15",
    "SG_SOPA_2004:SEC15": "SG:SOPA_2004:Sec15",
    "FIDIC_SILVER:CLAUSE8.7": "FIDIC:Silver_1999:Clause_8.7",
    "FIDIC_SILVER:CLAUSE17.3": "FIDIC:Silver_1999:Clause_17.3",
    # Phase 5: L1 实体法条群与涉外法律冲突法专编别名
    "VN_COMMERCIAL_LAW:ART300": "VN:Commercial_Law_2005:Art300",
    "VN_COMMERCIAL_LAW:ART303": "VN:Commercial_Law_2005:Art303",
    "VN_COMMERCIAL_LAW:ART304": "VN:Commercial_Law_2005:Art304",
    "VN_COMMERCIAL_LAW:ART305": "VN:Commercial_Law_2005:Art305",
    "VN_COMMERCIAL_LAW:ART307": "VN:Commercial_Law_2005:Art307",
    "VN_CIVIL_CODE:ART663": "VN:Civil_Code_2015:Art663",
    "VN_CIVIL_CODE:ART670": "VN:Civil_Code_2015:Art670",
    "VN_CIVIL_CODE:ART683": "VN:Civil_Code_2015:Art683",
    "VN_INVESTMENT:ART8": "VN:Investment_Law_2020:Art8",
    "ID_KUHPERDATA:ART1243": "ID:KUHPerdata:Art1243",
    "ID_KUHPERDATA:ART1244": "ID:KUHPerdata:Art1244",
    "ID_KUHPERDATA:ART1245": "ID:KUHPerdata:Art1245",
    "ID_KUHPERDATA:ART1246": "ID:KUHPerdata:Art1246",
    "ID_KUHPERDATA:ART1247": "ID:KUHPerdata:Art1247",
    "ID_KUHPERDATA:ART1248": "ID:KUHPerdata:Art1248",
    "ID_KUHPERDATA:ART1339": "ID:KUHPerdata:Art1339",
    "ID_INVESTMENT:ART4": "ID:UU_25_2007:Art4",
    "ID_AB:ART17": "ID:AB_1847:Art17",
    "MY_CONTRACTS:SEC56": "MY:Contracts_Act_1950:Sec56",
    "MY_CONTRACTS:SEC65": "MY:Contracts_Act_1950:Sec65",
    "MY_CONTRACTS:SEC74": "MY:Contracts_Act_1950:Sec74",
    "MY_CIPAA:SEC5": "MY:CIPAA_2012:Sec5",
    "MY_CIPAA:SEC6": "MY:CIPAA_2012:Sec6",
    "MY_CIPAA:SEC15": "MY:CIPAA_2012:Sec15",
    "MY_CIPAA:SEC28": "MY:CIPAA_2012:Sec28",
    "MY_CIPAA:SEC29": "MY:CIPAA_2012:Sec29",
    "PH_CIVIL_CODE:ART1170": "PH:Civil_Code:Art1170",
    "PH_CIVIL_CODE:ART1191": "PH:Civil_Code:Art1191",
    "PH_CIVIL_CODE:ART1226": "PH:Civil_Code:Art1226",
    "PH_CIVIL_CODE:ART1227": "PH:Civil_Code:Art1227",
    "PH_CIVIL_CODE:ART1228": "PH:Civil_Code:Art1228",
    "PH_CIVIL_CODE:ART16": "PH:Civil_Code:Art16",
    "PH_CIVIL_CODE:ART17": "PH:Civil_Code:Art17",
    "TH_CCC:SEC380": "TH:CCC:Sec380",
    "TH_CCC:SEC381": "TH:CCC:Sec381",
    "TH_CCC:SEC386": "TH:CCC:Sec386",
    "TH_CCC:SEC587": "TH:CCC:Sec587",
    "TH_CCC:SEC605": "TH:CCC:Sec605",
    "TH_CONFLICT_OF_LAWS:SEC5": "TH:Conflict_of_Laws_2481:Sec5",
    "TH_CONFLICT_OF_LAWS:SEC9": "TH:Conflict_of_Laws_2481:Sec9",
    "TH_CONFLICT_OF_LAWS:SEC13": "TH:Conflict_of_Laws_2481:Sec13",
    "SG_SOPA:SEC11": "SG:SOPA_2004:Sec11",
    "SG_SOPA:SEC26": "SG:SOPA_2004:Sec26",
    # Phase 6: L1 缔约过失、现场移交与仲裁执行别名
    "VN_CIVIL_CODE:ART385": "VN:Civil_Code_2015:Art385",
    "VN_CIVIL_CODE:ART397": "VN:Civil_Code_2015:Art397",
    "VN_CIVIL_CODE:ART401": "VN:Civil_Code_2015:Art401",
    "ID_KUHPERDATA:ART1320": "ID:KUHPerdata:Art1320",
    "ID_KUHPERDATA:ART1328": "ID:KUHPerdata:Art1328",
    "ID_KUHPERDATA:ART1338": "ID:KUHPerdata:Art1338",
    "TH_CCC:SEC354": "TH:CCC:Sec354",
    "TH_CCC:SEC368": "TH:CCC:Sec368",
    "PH_CIVIL_CODE:ART1305": "PH:Civil_Code:Art1305",
    "PH_CIVIL_CODE:ART1318": "PH:Civil_Code:Art1318",
    "VN_LAND_LAW:ART124": "VN:Land_Law_2024:Art124",
    "VN_LAND_LAW:ART153": "VN:Land_Law_2024:Art153",
    "ID_LAND_ACQUISITION:ART14": "ID:UU_2_2012:Art14",
    "ID_LAND_ACQUISITION:ART19": "ID:UU_2_2012:Art19",
    "PH_RIGHT_OF_WAY:SEC4": "PH:RA_10752:Sec4",
    "TH_LAND_EXPROPRIATION:SEC12": "TH:Land_Expropriation_BE_2562:Sec12",
    "VN_CIVIL_PROCEDURE:ART423": "VN:Civil_Procedure_Code_2015:Art423",
    "VN_CIVIL_PROCEDURE:ART439": "VN:Civil_Procedure_Code_2015:Art439",
    "VN_CIVIL_PROCEDURE:ART440": "VN:Civil_Procedure_Code_2015:Art440",
    "ID_SEMA:3_2023_ARBITRATION": "ID:SEMA_3_2023:Arbitration_Enforcement",
    "MY_ARBITRATION:SEC37": "MY:Arbitration_Act_2005:Sec37",
    "MY_ARBITRATION:SEC39": "MY:Arbitration_Act_2005:Sec39",
    "PH_ADR:SEC42": "PH:RA_9285:Sec42",
    "VN_CONSTRUCTION_LAW:ART111": "VN:Construction_Law_2014:Art111",
    "TH_CCC:SEC600": "TH:CCC:Sec600",
}


class SnapshotManager:
    def __init__(self, base_dir: str = "data/snapshots", pointer_file: str = "data/current_snapshot", keep: int = 2):
        self.base_dir = base_dir
        self.pointer_file = pointer_file
        self.keep = keep
        self._conns: Dict[str, sqlite3.Connection] = {}
        self._lock = threading.Lock()
        self.reload()

    def get_current_snapshot_id(self) -> str:
        """从指针文件获取当前生效的快照 ID"""
        if os.path.exists(self.pointer_file):
            with open(self.pointer_file, "r", encoding="utf-8") as f:
                snap_id = f.read().strip()
                if snap_id:
                    return snap_id
        # 若指针文件不存在，尝试取 snapshots 目录下最新的子目录
        if os.path.exists(self.base_dir):
            dirs = sorted([d for d in os.listdir(self.base_dir) if os.path.isdir(os.path.join(self.base_dir, d))])
            if dirs:
                return dirs[-1]
        return "20261021-asean-v2.2"

    def set_current_snapshot_id(self, snapshot_id: str):
        """原子切换当前快照指针"""
        os.makedirs(os.path.dirname(os.path.abspath(self.pointer_file)), exist_ok=True)
        tmp_file = f"{self.pointer_file}.tmp"
        with open(tmp_file, "w", encoding="utf-8") as f:
            f.write(snapshot_id)
        os.replace(tmp_file, self.pointer_file)
        self.reload()

    def snapshot_exists(self, snapshot_id: str) -> bool:
        """检查指定快照数据库是否存在"""
        db_path = os.path.join(self.base_dir, snapshot_id, "law.sqlite")
        return os.path.exists(db_path)

    def get_norm_by_id(self, norm_id: str, snapshot_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """按规范编号查询法条（norm_lookup 别名）"""
        return self.norm_lookup(norm_id, snapshot_id=snapshot_id)

    def reload(self):
        """重载快照连接，最多保留 keep 个活跃连接"""
        with self._lock:
            cur_id = self.get_current_snapshot_id()
            if cur_id not in self._conns:
                conn = self._open_conn(cur_id)
                if conn:
                    self._conns[cur_id] = conn

            # 清理超过 keep 个的陈旧连接
            if len(self._conns) > self.keep:
                keys = list(self._conns.keys())
                for k in keys[:-self.keep]:
                    self._conns[k].close()
                    del self._conns[k]

    def _open_conn(self, snapshot_id: str) -> Optional[sqlite3.Connection]:
        db_path = os.path.join(self.base_dir, snapshot_id, "law.sqlite")
        if not os.path.exists(db_path):
            return None
        conn = sqlite3.connect(db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn

    def get_connection(self, snapshot_id: Optional[str] = None) -> Optional[sqlite3.Connection]:
        snap_id = snapshot_id or self.get_current_snapshot_id()
        with self._lock:
            if snap_id in self._conns:
                return self._conns[snap_id]
            conn = self._open_conn(snap_id)
            if conn:
                self._conns[snap_id] = conn
                return conn
            # 若指定的历史快照在磁盘上不存在，优雅自动回退至当前主快照
            cur_id = self.get_current_snapshot_id()
            if cur_id != snap_id:
                if cur_id in self._conns:
                    return self._conns[cur_id]
                fallback_conn = self._open_conn(cur_id)
                if fallback_conn:
                    self._conns[cur_id] = fallback_conn
                    return fallback_conn
            return None

    def norm_lookup(self, law_or_id: str, enbez: Optional[str] = None, snapshot_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """精确按条号检索法条：
        支持 norm_lookup("ID:UU_2_2017:Art57")、norm_lookup("SG:SOPA_2004:Sec9")、norm_lookup("FIDIC:Silver_1999:Clause_20.1")
        """
        conn = self.get_connection(snapshot_id)
        if not conn:
            return None

        clean_input = law_or_id.strip()
        cur = conn.cursor()

        # -1. 别名与跨格式兼容映射
        raw_upper = clean_input.upper().replace(" ", "")
        if raw_upper.startswith("NORM:"):
            raw_upper = raw_upper[5:]
        if raw_upper in KNOWN_NORM_ALIASES:
            clean_input = KNOWN_NORM_ALIASES[raw_upper]
        elif clean_input.startswith("NORM:"):
            clean_input = clean_input[5:]

        # 0. 先尝试全字完全匹配 norm_id
        cur.execute(
            """SELECT * FROM norms
               WHERE norm_id = ? OR norm_id = ?
               LIMIT 1""",
            (clean_input, clean_input.replace(" ", ""))
        )
        row = cur.fetchone()
        if row:
            return dict(row)

        # 1. FIDIC 条号与跨版本等效降级检索支持
        if "FIDIC" in clean_input.upper():
            import re
            m = re.search(r'(\d+\.\d+)', clean_input)
            if m:
                clause_num = m.group(1)
                edition_kw = ""
                if "RED" in clean_input.upper():
                    edition_kw = "%Red%"
                elif "YELLOW" in clean_input.upper():
                    edition_kw = "%Yellow%"
                elif "2017" in clean_input.upper():
                    edition_kw = "%2017%"
                elif "SILVER" in clean_input.upper():
                    edition_kw = "%Silver%"

                if edition_kw:
                    cur.execute(
                        "SELECT * FROM norms WHERE norm_id LIKE ? AND (norm_id LIKE ? OR enbez LIKE ?) LIMIT 1",
                        (edition_kw, f"%Clause_{clause_num}%", f"%{clause_num}%")
                    )
                    r = cur.fetchone()
                    if r:
                        return dict(r)

                # 跨版本同条号降级召回：若特定版本未命中，降级召回该条号核心条款
                cur.execute(
                    "SELECT * FROM norms WHERE (law = 'FIDIC' OR norm_id LIKE 'FIDIC%') AND (norm_id LIKE ? OR enbez LIKE ?) ORDER BY norm_id ASC LIMIT 1",
                    (f"%Clause_{clause_num}%", f"%{clause_num}%")
                )
                r = cur.fetchone()
                if r:
                    return dict(r)

        if enbez is None and ":" in clean_input:
            parts = clean_input.split(":", 1)
            law, enbez_str = parts[0].strip(), parts[1].strip()
        else:
            law = clean_input
            enbez_str = enbez.strip() if enbez else ""

        # 标准化 enbez
        clean_enbez = enbez_str.replace(" ", "")
        if not clean_enbez.startswith("§") and not clean_enbez.startswith("Art") and not clean_enbez.startswith("Section") and not clean_enbez.startswith("Clause"):
            clean_enbez = f"§{clean_enbez}"
        spaced_enbez = clean_enbez.replace("§", "§ ")

        norm_id = f"{law}:{clean_enbez}".replace(" ", "")

        cur.execute(
            """SELECT * FROM norms
               WHERE norm_id = ?
                  OR norm_id = ?
                  OR (law = ? AND (enbez = ? OR REPLACE(enbez, ' ', '') = ?))
               LIMIT 1""",
            (norm_id, clean_input, law, spaced_enbez, clean_enbez)
        )
        row = cur.fetchone()
        if not row:
            # L2 广覆盖参考层回退查找
            cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='reference_norms'")
            if cur.fetchone():
                cur.execute(
                    """SELECT * FROM reference_norms
                       WHERE norm_id = ? OR norm_id = ? OR (law = ? AND (enbez = ? OR REPLACE(enbez, ' ', '') = ?))
                       LIMIT 1""",
                    (norm_id, clean_input, law, spaced_enbez, clean_enbez)
                )
                row = cur.fetchone()
        return dict(row) if row else None

    def get_kommentar(self, norm_id: str) -> Optional[Dict[str, Any]]:
        """按条文编号获取权威法典评注精要要旨"""
        clean_id = norm_id.replace("NORM:", "").strip()
        kommentar_file = "kb/asean/commentary.json"
        if os.path.exists(kommentar_file):
            try:
                import json
                with open(kommentar_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data.get(clean_id)
            except Exception:
                pass
        return None

    def case_lookup(self, case_id: str, snapshot_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """按 case_id 或 az 案号检索判例全文与元数据"""
        conn = self.get_connection(snapshot_id)
        if not conn:
            return None
        cur = conn.cursor()
        clean_cid = case_id.replace("CASE:", "").strip()
        cur.execute(
            """SELECT case_id, court, senate, decided, az, ecli, doctype, leitsatz, tenor, tatbestand, gruende, norms_meta, source_url
               FROM cases
               WHERE case_id = ? OR case_id = ? OR az = ? OR az LIKE ?
               LIMIT 1""",
            (clean_cid, case_id, case_id, f"%{clean_cid}%")
        )
        row = cur.fetchone()
        if not row:
            # L2 广覆盖参考裁判回退查找
            cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='reference_cases'")
            if cur.fetchone():
                cur.execute(
                    """SELECT case_id, court, senate, decided, az, ecli, doctype, leitsatz, tenor, tatbestand, gruende, norms_meta, source_url
                       FROM reference_cases
                       WHERE case_id = ? OR case_id = ? OR az = ? OR az LIKE ?
                       LIMIT 1""",
                    (clean_cid, case_id, case_id, f"%{clean_cid}%")
                )
                row = cur.fetchone()
        return dict(row) if row else None

    def get_all_norms(self, snapshot_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """获取当前快照所有法条记录 (用于索引构建与全量切块，支持东盟多语种文本)"""
        conn = self.get_connection(snapshot_id)
        if not conn:
            return []
        cur = conn.cursor()
        cur.execute(
            """SELECT * FROM norms
               ORDER BY law, norm_id"""
        )
        return [dict(r) for r in cur.fetchall()]

    def get_all_reference_norms(self, snapshot_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """获取 L2 广覆盖参考层全部法条记录"""
        conn = self.get_connection(snapshot_id)
        if not conn:
            return []
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='reference_norms'")
        if not cur.fetchone():
            return []
        cur.execute("SELECT * FROM reference_norms ORDER BY law, norm_id")
        return [dict(r) for r in cur.fetchall()]

    def get_all_reference_cases(self, snapshot_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """获取 L2 广覆盖参考层全部判例记录"""
        conn = self.get_connection(snapshot_id)
        if not conn:
            return []
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='reference_cases'")
        if not cur.fetchone():
            return []
        cur.execute("SELECT * FROM reference_cases ORDER BY decided DESC")
        return [dict(r) for r in cur.fetchall()]

    def get_all_cases(self, snapshot_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """获取当前快照所有判例记录 (用于切块与向量索引)"""
        conn = self.get_connection(snapshot_id)
        if not conn:
            return []
        cur = conn.cursor()
        cur.execute(
            """SELECT case_id, court, senate, decided, az, ecli, doctype, leitsatz, tenor, tatbestand, gruende, norms_meta, source_url
               FROM cases
               ORDER BY decided DESC"""
        )
        return [dict(r) for r in cur.fetchall()]

    def get_cites_of(self, norm_id: str, limit: int = 5, snapshot_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """查询适用该法条的权威判例 (按 hot_norm_cases 或 edges 查询)"""
        conn = self.get_connection(snapshot_id)
        if not conn:
            return []
        cur = conn.cursor()
        clean_norm = norm_id.replace("NORM:", "")
        cur.execute(
            """SELECT c.* FROM cases c
               JOIN hot_norm_cases h ON c.case_id = h.case_id
               WHERE h.norm_id = ?
               ORDER BY h.rank ASC
               LIMIT ?""",
            (clean_norm, limit)
        )
        rows = cur.fetchall()
        if not rows:
            cur.execute(
                """SELECT c.* FROM cases c
                   JOIN edges e ON f'CASE:' || c.case_id = e.src
                   WHERE e.dst = ? AND e.rel = 'APPLIES'
                   LIMIT ?""",
                (f"NORM:{clean_norm}", limit)
            )
            rows = cur.fetchall()
        return [dict(r) for r in rows]

    def get_norms_batch(self, norm_ids: List[str], snapshot_id: Optional[str] = None) -> Dict[str, Dict[str, Any]]:
        """批量获取法条记录 (避免单条循环查询 N+1 开销)"""
        if not norm_ids:
            return {}
        conn = self.get_connection(snapshot_id)
        if not conn:
            return {}
        cur = conn.cursor()
        clean_ids = [n.replace("NORM:", "").strip() for n in norm_ids]
        placeholders = ",".join(["?"] * len(clean_ids))
        cur.execute(f"SELECT * FROM norms WHERE norm_id IN ({placeholders})", clean_ids)
        return {r["norm_id"]: dict(r) for r in cur.fetchall()}

    def get_chunks_batch(self, chunk_ids: List[str], snapshot_id: Optional[str] = None) -> Dict[str, Dict[str, Any]]:
        """批量获取分块记录 (避免单条循环查询 N+1 开销)"""
        if not chunk_ids:
            return {}
        conn = self.get_connection(snapshot_id)
        if not conn:
            return {}
        cur = conn.cursor()
        placeholders = ",".join(["?"] * len(chunk_ids))
        cur.execute(f"SELECT * FROM chunks WHERE chunk_id IN ({placeholders})", chunk_ids)
        return {r["chunk_id"]: dict(r) for r in cur.fetchall()}
