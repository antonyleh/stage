import sys
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, adjusted_rand_score

CLEAN = Path(r'c:\Users\lehmanna\Desktop\stage\projet\data\cln1\Clean')
co2 = pd.read_parquet(CLEAN / 'Mesures/co2.parquet')
sem = pd.read_parquet(CLEAN / 'Comportement/semainier.parquet')

# ============ 1. Profils journaliers CO2 (24h, z-norm par logement) ============
co2['DATE']  = co2['DATE_HEURE'].dt.normalize()
co2['heure'] = co2['DATE_HEURE'].dt.hour

# jours complets uniquement (>= 138/144 points, soit >= 23h de couverture)
pts = co2.groupby(['CODELIEU','DATE']).size()
jours_ok = pts[pts >= 138].index
print(f'Jours complets : {len(jours_ok):,} (sur {len(pts):,} jours logement)')

co2c = co2.set_index(['CODELIEU','DATE']).loc[jours_ok].reset_index()

# z-norm PAR LOGEMENT (preserve les differences entre jours d'un meme logement)
stats = co2c.groupby('CODELIEU')['VALEUR'].agg(['mean','std'])
co2c = co2c.merge(stats, on='CODELIEU')
co2c['z'] = (co2c['VALEUR'] - co2c['mean']) / co2c['std']

prof = co2c.groupby(['CODELIEU','DATE','heure'])['z'].mean().unstack('heure')
prof = prof.dropna()
print(f'Profils journaliers retenus : {len(prof):,} ({prof.index.get_level_values(0).nunique()} logements)')

X = prof.values  # (n_jours, 24)

# ============ 2. Choix de k : silhouette + stabilite ============
rng = np.random.RandomState(0)
print(f"\n{'k':>2} {'silhouette':>10} {'stab. ARI':>10}  tailles")
results = {}
for k in range(2, 9):
    km  = KMeans(n_clusters=k, n_init=30, random_state=42)
    lab = km.fit_predict(X)
    sil = silhouette_score(X, lab, sample_size=2000, random_state=0)
    aris = []
    for _ in range(8):
        idx  = rng.choice(len(X), int(0.8*len(X)), replace=False)
        lab2 = KMeans(n_clusters=k, n_init=30, random_state=rng.randint(1e6)).fit_predict(X[idx])
        aris.append(adjusted_rand_score(lab[idx], lab2))
    sizes = np.bincount(lab)
    results[k] = (km, lab)
    print(f'{k:>2} {sil:>10.3f} {np.mean(aris):>10.3f}  {sizes}')

# ============ 3. Interpretation pour k=4 ============
K = 4
km, lab = results[K]
prof_l = prof.copy()
prof_l['daytype'] = lab
prof_l['jour_sem'] = prof_l.index.get_level_values('DATE').dayofweek
prof_l['we'] = prof_l['jour_sem'] >= 5

print(f'\n=== k={K} : profil moyen z-CO2 par type de journee (6h..23h, pas 3h) ===')
heures_aff = [0, 3, 6, 9, 12, 15, 18, 21]
hdr = '  '.join(f'{h:>5}h' for h in heures_aff)
print(f"{'type':<6} {'n':>5} {'%WE':>5}  {hdr}")
for c in range(K):
    sub = prof_l[prof_l['daytype'] == c]
    m = sub[list(range(24))].mean()
    pct_we = 100 * sub['we'].mean()
    vals = '  '.join(f'{m[h]:>6.2f}' for h in heures_aff)
    print(f'C{c:<5} {len(sub):>5} {pct_we:>4.0f}%  {vals}')
print('(rappel : ~28.6% des jours sont des jours de week-end)')

# ============ 4. Validation : presence declaree (semainier) par type de journee ============
sem['present'] = sem['IDN_PIECE'].notna() & (sem['IDN_PIECE'] != 90)
sem['heure']   = (sem['CODE_HEURE'].str[2:].astype(int) - 1001) // 6  # V_1001.. -> heure 0..23

# taux de presence du menage : moyenne sur occupants, par logement x date x heure
pres = (sem.groupby(['CODELIEU','DATE','heure'])['present'].mean()
        .unstack('heure'))

# jointure avec les types de journees
common = prof_l.index.intersection(pres.index)
print(f'\nJours avec CO2 + semainier : {len(common):,}')
pres_c = pres.loc[common]
lab_c  = prof_l.loc[common, 'daytype']

print(f'\n=== Taux de presence declaree (%) par type de journee ===')
print(f"{'type':<6} {'n':>5}  {hdr}")
for c in range(K):
    m = pres_c[lab_c == c].mean()
    vals = '  '.join(f'{100*m[h]:>5.0f}%' for h in heures_aff)
    print(f'C{c:<5} {(lab_c==c).sum():>5}  {vals}')

# moyenne presence 9h-17h vs 0-6h par type
print(f'\n=== Resume : presence jour (9-17h) vs nuit (0-6h) ===')
for c in range(K):
    sub = pres_c[lab_c == c]
    j = sub[[9,10,11,12,13,14,15,16,17]].mean().mean()
    n = sub[[0,1,2,3,4,5]].mean().mean()
    print(f'C{c} : nuit {100*n:.0f}%  jour {100*j:.0f}%  (ecart {100*(n-j):+.0f} pts)')
