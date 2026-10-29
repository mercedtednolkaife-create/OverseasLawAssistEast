import urllib.request
import json

req = urllib.request.Request('http://127.0.0.1:8000/api/cases/C254944')
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode('utf-8'))

print("=== CASE STATUS & NODE ===")
print("Case ID:", data.get("case_id"))
print("Title:", data.get("title"))
print("Status:", data.get("status"))
print("Current Node:", data.get("current_node"))

sa = data.get("strategic_assessment", {})
print("\n=== PIVOTAL FACTORS ===")
for pf in sa.get("pivotal_factors", []):
    print(" *", pf)

print("\n=== OUTCOME BRANCHES ===")
for ob in sa.get("outcome_branches", []):
    btype = ob.get("branch_type")
    title = ob.get("title")
    cond = ob.get("condition_precedent")
    print(f" * [{btype}] {title} | 前提条件: {cond}")

print("\n=== RED TEAM DEFENSES ===")
for rd in sa.get("red_team_defenses", []):
    did = rd.get("defense_id")
    claim = rd.get("opposing_claim")
    cw = rd.get("counter_weapons")
    print(f" * [{did}] 对方抗辩: {claim} | 反制武器: {cw}")

print("\n=== ACTIONABLE CHECKLIST ===")
for ac in sa.get("actionable_checklist", []):
    print(" *", ac)
