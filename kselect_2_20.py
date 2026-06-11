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
pts = co2.groupby(['CODELIEU','DATE']).size()
co2c = co2.set_index(['CODELIEU','DATE']).loc[pts[pts >= 138].index].reset_index()
stats = co2c.groupby('CODELIEU')['VALEUR'].agg(['mean','std'])
co2c = co2c.merge(stats, on='CODELIEU')
co2c['z'] = (co2c['VALEUR'] - co2c['mean']) / co2c['std']
prof = co2c.groupby(['CODELIEU','DATE','heure'])['z'].mean().unstack('heure').dropna()
X = prof.values
print(f'{len(X):,} journées\n')

rng = np.random.RandomState(0)
print(f"{'k':>2} {'silhouette':>10} {'stab. ARI':>10}  taille min/max")
for k in range(2, 21):
    lab = KMeans(n_clusters=k, random_state=42, n_init=30).fit_predict(X)
    sil = silhouette_score(X, lab, sample_size=2000, random_state=0)
    aris = []
    for _ in range(8):
        idx  = rng.choice(len(X), int(0.8*len(X)), replace=False)
        lab2 = KMeans(n_clusters=k, random_state=rng.randint(10**6), n_init=30).fit_predict(X[idx])
        aris.append(adjusted_rand_score(lab[idx], lab2))
    sizes = np.bincount(lab)
    print(f'{k:>2} {sil:>10.3f} {np.mean(aris):>10.3f}  {sizes.min():>4} / {sizes.max()}')
