import sys
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, adjusted_rand_score

CLEAN = Path(r'c:\Users\lehmanna\Desktop\stage\projet\data\cln1\Clean')
co2 = pd.read_parquet(CLEAN / 'Mesures/co2.parquet')

co2['DATE']  = co2['DATE_HEURE'].dt.normalize()
co2['heure'] = co2['DATE_HEURE'].dt.hour
co2['slot']  = co2['heure'] * 6 + co2['DATE_HEURE'].dt.minute // 10   # 0..143

pts = co2.groupby(['CODELIEU','DATE']).size()
co2c = co2.set_index(['CODELIEU','DATE']).loc[pts[pts >= 138].index].reset_index()
stats = co2c.groupby('CODELIEU')['VALEUR'].agg(['mean','std'])
co2c = co2c.merge(stats, on='CODELIEU')
co2c['z'] = (co2c['VALEUR'] - co2c['mean']) / co2c['std']

prof24  = co2c.groupby(['CODELIEU','DATE','heure'])['z'].mean().unstack('heure').dropna()
prof144 = co2c.groupby(['CODELIEU','DATE','slot'])['z'].mean().unstack('slot')
prof144 = prof144.interpolate(axis=1, limit=3).dropna()   # tolere qq slots manquants

common  = prof24.index.intersection(prof144.index)
X24, X144 = prof24.loc[common].values, prof144.loc[common].values
print(f'Journées comparées : {len(common):,}   (24 dims vs 144 dims)')

rng = np.random.RandomState(0)
print(f"\n{'repr':<10} {'k':>2} {'silhouette':>10} {'stab. ARI':>10}")
labs = {}
for name, X in [('horaire', X24), ('10 min', X144)]:
    for k in [4, 6]:
        lab = KMeans(n_clusters=k, random_state=42, n_init=30).fit_predict(X)
        sil = silhouette_score(X, lab, sample_size=2000, random_state=0)
        aris = []
        for _ in range(6):
            idx  = rng.choice(len(X), int(0.8*len(X)), replace=False)
            lab2 = KMeans(n_clusters=k, random_state=rng.randint(10**6), n_init=30).fit_predict(X[idx])
            aris.append(adjusted_rand_score(lab[idx], lab2))
        labs[(name, k)] = lab
        print(f'{name:<10} {k:>2} {sil:>10.3f} {np.mean(aris):>10.3f}')

print('\n=== Accord entre les deux partitions (mêmes journées) ===')
for k in [4, 6]:
    ari = adjusted_rand_score(labs[('horaire', k)], labs[('10 min', k)])
    print(f'k={k} : ARI(horaire, 10min) = {ari:.3f}')

# correlation moyenne entre slots adjacents (redondance)
r_adj = np.mean([np.corrcoef(X144[:, i], X144[:, i+1])[0, 1] for i in range(143)])
print(f'\nCorrélation moyenne entre 2 slots de 10 min adjacents : {r_adj:.3f}')
