import sqlite3

conn = sqlite3.connect('data/snapshots/20261021-asean-v2.2/law.sqlite')
cur = conn.cursor()

# Specific counts
fidic_cnt = cur.execute("SELECT count(*) FROM reference_norms WHERE norm_id LIKE 'FIDIC:%'").fetchone()[0] + cur.execute("SELECT count(*) FROM norms WHERE norm_id LIKE 'FIDIC:%'").fetchone()[0]
print(f'FIDIC current: {fidic_cnt}, target: 95, gap: {95 - fidic_cnt}')

dta_cnt = cur.execute("SELECT count(*) FROM reference_norms WHERE norm_id LIKE 'DTA:%'").fetchone()[0]
print(f'DTA current: {dta_cnt}, target: 24, gap: {24 - dta_cnt}')

bit_cnt = cur.execute("SELECT count(*) FROM reference_norms WHERE norm_id LIKE '%BIT%'").fetchone()[0] + cur.execute("SELECT count(*) FROM norms WHERE norm_id LIKE '%BIT%'").fetchone()[0]
print(f'BIT current: {bit_cnt}, target: 32, gap: {32 - bit_cnt}')

prc_cnt = cur.execute("SELECT count(*) FROM norms WHERE norm_id LIKE 'CN:%' OR norm_id LIKE 'SINOSURE:%'").fetchone()[0]
print(f'PRC outbound base current: {prc_cnt}, target: 24, gap: {24 - prc_cnt}')

acia_cafta_cnt = cur.execute("SELECT count(*) FROM reference_norms WHERE norm_id LIKE 'ACIA:%' OR norm_id LIKE 'CAFTA:%' OR norm_id LIKE 'RCEP:%'").fetchone()[0]
print(f'ACIA/CAFTA/RCEP current: {acia_cafta_cnt}, target: 32, gap: {32 - acia_cafta_cnt}')

conn.close()
