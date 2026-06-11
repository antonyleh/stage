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

co2['DATE']  = co2['DATE_HEURE'].dt.normalize()
co2['heure'] = co2['DATE_HEURE'].dt.hour
pts = co2.groupby(['CODELIEU','DATE']).size()
co2c = co2.set_index(['CODELIEU','DATE']).loc[pts[pts >= 138].index].reset_index()
stats = co2c.groupby('CODELIEU')['VALEUR'].agg(['mean','std'])
co2c = co2c.merge(stats, on='CODELIEU')
co2c['z'] = (co2c['VALEUR'] - co2c['mean']) / co2c['std']
prof = co2c.groupby(['CODELIEU','DATE','heure'])['z'].mean().unstack('heure').dropna()

lab6 = KMeans(n_clusters=6, random_state=42, n_init=30).fit_predict(prof.values)

print('=== Profils moyens k=6 (pour verifier les noms) ===')
heures_aff = [0, 3, 6, 9, 12, 15, 18, 21]
hdr = '  '.join(f'{h:>5}h' for h in heures_aff)
print(f"{'type':<5} {'n':>5}  {hdr}")
pj = prof.copy(); pj['dt'] = lab6
for c in range(6):
    m = pj[pj['dt']==c][list(range(24))].mean()
    print(f"C{c:<4} {(lab6==c).sum():>5}  " + '  '.join(f'{m[h]:>6.2f}' for h in heures_aff))

# ===== signature semaine (>=3 jours) sur 6 day-types =====
dtypes = pd.DataFrame({'daytype': lab6}, index=prof.index).reset_index()
dtypes['we'] = dtypes['DATE'].dt.dayofweek >= 5
semaine = dtypes[~dtypes['we']]
nj = semaine.groupby('CODELIEU').size()
sig = (semaine[semaine['CODELIEU'].isin(nj[nj >= 3].index)]
       .groupby('CODELIEU')['daytype'].value_counts(normalize=True).unstack(fill_value=0))
sig.columns = [f'dt{c}' for c in sig.columns]
print(f'\nSignatures : {len(sig)} logements x {sig.shape[1]} dims')

X = sig.values
rng = np.random.RandomState(0)
print(f"\n{'k':>2} {'silhouette':>10} {'stab. ARI':>10}  tailles")
results = {}
for k in range(2, 8):
    l = KMeans(n_clusters=k, n_init=30, random_state=42).fit_predict(X)
    sil = silhouette_score(X, l)
    aris = []
    for _ in range(8):
        idx = rng.choice(len(X), int(0.8*len(X)), replace=False)
        l2  = KMeans(n_clusters=k, n_init=30, random_state=rng.randint(1e6)).fit_predict(X[idx])
        aris.append(adjusted_rand_score(l[idx], l2))
    results[k] = l
    print(f'{k:>2} {sil:>10.3f} {np.mean(aris):>10.3f}  {np.bincount(l)}')

for K in (4, 5):
    lab_log = pd.Series(results[K], index=sig.index)
    print(f'\n=== Composition par cluster logement (K={K}) ===')
    print((sig.groupby(lab_log).mean() * 100).round(0).to_string())

    sem['present'] = sem['IDN_PIECE'].notna() & (sem['IDN_PIECE'] != 90)
    sem['heure']   = (sem['CODE_HEURE'].str[2:].astype(int) - 1001) // 6
    sem['we']      = sem['DATE'].dt.dayofweek >= 5
    pres = sem[~sem['we']].groupby(['CODELIEU','heure'])['present'].mean().unstack('heure')
    common = lab_log.index.intersection(pres.index)
    print(f'Presence declaree semaine (nuit 0-6h / jour 9-17h), {len(common)} logements :')
    for c in range(K):
        sel = common[lab_log.loc[common] == c]
        m = pres.loc[sel].mean()
        n_ = m[[0,1,2,3,4,5]].mean(); j_ = m[[9,10,11,12,13,14,15,16,17]].mean()
        print(f'  C{c} (n={len(sel)}) : nuit {100*n_:.0f}%  jour {100*j_:.0f}%')
