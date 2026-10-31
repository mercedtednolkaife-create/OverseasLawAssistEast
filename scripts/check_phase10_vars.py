import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

import scripts.data_phase10_deep_statutes as s1
import scripts.data_phase10_ref_statutes as s2
import scripts.data_phase10_deep_cases as c1

print("s1 attributes:", [k for k in dir(s1) if not k.startswith('_')])
print("s2 attributes:", [k for k in dir(s2) if not k.startswith('_')])
print("c1 attributes:", [k for k in dir(c1) if not k.startswith('_')])

l1_norms_phase10 = getattr(s1, 'PHASE10_L1_NORMS', [])
print("PHASE10_L1_NORMS count:", len(l1_norms_phase10))

l2_norms_phase10 = getattr(s2, 'PHASE10_L2_REF_NORMS', getattr(s2, 'PHASE10_REF_NORMS', []))
print("L2 norms in s2 count:", len(l2_norms_phase10))

cases_phase10 = getattr(c1, 'PHASE10_DEEP_CASES', getattr(c1, 'ALL_CASES', []))
print("Cases in c1:", [k for k in dir(c1) if 'CASE' in k or 'case' in k])
