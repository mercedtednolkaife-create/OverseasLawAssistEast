import re
import json
import sqlite3

def run():
    conn = sqlite3.connect('data/snapshots/20261021-asean-v2.2/law.sqlite')
    c = conn.cursor()

    with open('FrontEnd/src/components/search/normSearchDefaultData.ts', 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract DEFAULT_SEARCH_ITEMS json-like content
    m = re.search(r'export const DEFAULT_SEARCH_ITEMS: NormOrCaseItem\[\] = (\[[\s\S]*?\]);', content)
    if not m:
        print("Could not find DEFAULT_SEARCH_ITEMS")
        return

    items_json_str = m.group(1)
    items = json.loads(items_json_str)

    ALIAS_MAP = {
        "VN:Law_135_2025:Art86.2": "VN:Construction_Law_2014_Amended_2020:Art146",
        "VN:Law_135_2025:Art146": "VN:Construction_Law_2014_Amended_2020:Art146",
        "VN:Decree_210_2026:Art18": "VN:Decree_37_2015_ND_CP:Art18",
        "SG:Precedent:BS_Mount_Sophia": "CASE:SG_CA:BS_Mount_Sophia:2012",
        "CASE:SG_HC:BSMountSophia:2016": "CASE:SG_CA:BS_Mount_Sophia:2012",
        "SG:Precedent:JBE_Properties": "CASE:SG_CA:JBEProperties:2011",
        "PH:Precedent:PCAB_v_Manila_Water": "CASE:PH_SC:PCAB_v_Manila_Water_2020",
        "CASE:PH_SC:G.R.217590_ManilaWater:2020": "CASE:PH_SC:PCAB_v_Manila_Water_2020",
        "CASE:TH_SAC:HopewellConcession:2022": "CASE:TH_SAC:Hopewell_Concession_2022",
    }

    updated_count = 0
    for item in items:
        item_id = item.get("id", "")
        lookup_id = ALIAS_MAP.get(item_id, item_id)
        # Query norms table
        c.execute("SELECT text_original, text_en FROM norms WHERE norm_id = ?", (lookup_id,))
        row = c.fetchone()
        if not row:
            # Try reference_norms
            c.execute("SELECT text_original, text_en FROM reference_norms WHERE norm_id = ?", (lookup_id,))
            row = c.fetchone()
        if not row:
            # Try case
            c.execute("SELECT gruende, tenor FROM cases WHERE case_id = ?", (lookup_id,))
            row = c.fetchone()
        if not row:
            # Try reference_cases
            c.execute("SELECT gruende, tenor FROM reference_cases WHERE case_id = ?", (lookup_id,))
            row = c.fetchone()

        if row:
            orig, en = row
            official_text = orig if orig and len(orig.strip()) > 10 else (en if en else "")
            if official_text and official_text != item.get("text_zh_machine"):
                item["text_de"] = official_text
                updated_count += 1
            else:
                print(f"Skipped {item_id}: no distinct text")
        else:
            print(f"Not found in db: {item_id} (lookup: {lookup_id})")

    print(f"Updated {updated_count} / {len(items)} items with true foreign official text.")

    new_items_json = json.dumps(items, ensure_ascii=False, indent=2)
    new_content = content[:m.start(1)] + new_items_json + content[m.end(1):]

    with open('FrontEnd/src/components/search/normSearchDefaultData.ts', 'w', encoding='utf-8') as f:
        f.write(new_content)

    print("Successfully wrote updated normSearchDefaultData.ts")

if __name__ == '__main__':
    run()
