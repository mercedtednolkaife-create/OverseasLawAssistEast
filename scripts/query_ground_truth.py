# -*- coding: utf-8 -*-
import sqlite3, sys
sys.stdout.reconfigure(encoding='utf-8')
conn = sqlite3.connect('data/snapshots/20261021-asean-v2.2/law.sqlite')
c = conn.cursor()

def search_norms(kw):
    sql = "SELECT norm_id, law, enbez, title FROM norms WHERE norm_id LIKE ? OR law LIKE ? OR title LIKE ? LIMIT 4"
    return c.execute(sql, (f'%{kw}%', f'%{kw}%', f'%{kw}%')).fetchall()

def search_cases(kw):
    sql1 = "SELECT case_id, court, az, leitsatz FROM cases WHERE case_id LIKE ? OR leitsatz LIKE ? LIMIT 3"
    sql2 = "SELECT case_id, court, az, leitsatz FROM reference_cases WHERE case_id LIKE ? OR leitsatz LIKE ? LIMIT 3"
    return c.execute(sql1, (f'%{kw}%', f'%{kw}%')).fetchall() + c.execute(sql2, (f'%{kw}%', f'%{kw}%')).fetchall()

keywords = [
    'TKDN', 'Quantum', 'Meruit', 'Contracts', 'Risk', 'DAB', 'DAAB', 'CISG', 'Expropriation', 'Subcontract',
    'UU_24', 'Perppu', 'Civil_Code'
]

for kw in keywords:
    print(f'=== KW: {kw} ===')
    n = search_norms(kw)
    cs = search_cases(kw)
    for r in n: 
        print('  NORM:', r[0], '|', r[1], '|', (r[3] or '')[:35])
    for r in cs: 
        print('  CASE:', r[0], '|', r[1], '|', (r[3] or '')[:35])
