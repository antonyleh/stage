import sys
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd
import numpy as np
from pathlib import Path

CLEAN = Path(r'c:\Users\lehmanna\Desktop\stage\projet\data\cln1\Clean')

co2     = pd.read_parquet(CLEAN / 'Mesures/co2.parquet')
confort = pd.read_parquet(CLEAN / 'Mesures/confort.parquet')

print('=== 1. Nombre de pièces mesurées par logement (CO2) ===')
n_pieces = co2.groupby('CODELIEU')['IDN_PIECE'].nunique()
print(n_pieces.value_counts().sort_index().to_string())
print(f'-> {100*(n_pieces > 1).mean():.1f}% des logements ont >1 pièce CO2')

print('\n=== confort (TPT/HRE) ===')
n_pieces_c = confort.groupby('CODELIEU')['IDN_PIECE'].nunique()
print(n_pieces_c.value_counts().sort_index().to_string())
print(f'-> {100*(n_pieces_c > 1).mean():.1f}% des logements ont >1 pièce confort')

print('\n=== 2. Doublons temporels (même CODELIEU, même DATE_HEURE, pièces diff.) ===')
dup = co2.duplicated(subset=['CODELIEU', 'DATE_HEURE'], keep=False)
print(f'CO2 : {dup.sum():,} lignes en doublon temporel ({100*dup.mean():.1f}%)')
dup_c = confort.duplicated(subset=['CODELIEU', 'DATE_HEURE'], keep=False)
print(f'Confort : {dup_c.sum():,} lignes ({100*dup_c.mean():.1f}%)')

print('\n=== 3. Régularité du pas de temps (par logement×pièce, CO2) ===')
# échantillon de 30 logements pour aller vite
sample = co2['CODELIEU'].drop_duplicates().sample(30, random_state=0)
gaps_stats = []
for cl in sample:
    sub = co2[co2['CODELIEU'] == cl]
    for p, g in sub.groupby('IDN_PIECE'):
        dt = g.sort_values('DATE_HEURE')['DATE_HEURE'].diff().dropna()
        if len(dt) < 10: continue
        dt_min = dt.dt.total_seconds() / 60
        gaps_stats.append({
            'CODELIEU': cl, 'piece': p, 'n': len(g),
            'pas_median_min': dt_min.median(),
            'pct_pas_10min': 100 * (dt_min == 10).mean(),
            'n_trous_sup_1h': int((dt_min > 60).sum()),
            'plus_gros_trou_h': dt_min.max() / 60,
        })
gs = pd.DataFrame(gaps_stats)
print(gs.describe().round(2).to_string())
print(f"\n-> logements×pièces avec au moins 1 trou >1h : {100*(gs['n_trous_sup_1h']>0).mean():.0f}%")

print('\n=== 4. Durée de mesure par logement (CO2) ===')
dur = co2.groupby('CODELIEU')['DATE_HEURE'].agg(lambda s: (s.max()-s.min()).total_seconds()/86400)
print(dur.describe().round(1).to_string())
