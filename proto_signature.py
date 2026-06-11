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
q_men = pd.read_parquet(CLEAN / 'Questionnaires/q_menage.parquet')
q_ind = pd.read_parquet(CLEAN / 'Questionnaires/q_individu.parquet')

# ===== reproduit les day-types (k=4) =====
co2['DATE']  = co2['DATE_HEURE'].dt.normalize()
co2['heure'] = co2['DATE_HEURE'].dt.hour
pts = co2.groupby(['CODELIEU','DATE']).size()
co2c = co2.set_index(['CODELIEU','DATE']).loc[pts[pts >= 138].index].reset_index()
stats = co2c.groupby('CODELIEU')['VALEUR'].agg(['mean','std'])
co2c = co2c.merge(stats, on='CODELIEU')
co2c['z'] = (co2c['VALEUR'] - co2c['mean']) / co2c['std']
prof = co2c.groupby(['CODELIEU','DATE','heure'])['z'].mean().unstack('heure').dropna()

km  = KMeans(n_clusters=4, n_init=30, random_state=42)
lab = km.fit_predict(prof.values)
prof_l = pd.DataFrame({'daytype': lab}, index=prof.index)
prof_l['we'] = prof_l.index.get_level_values('DATE').dayofweek >= 5

# ===== signature logement : % de chaque day-type, semaine vs week-end =====
sig_sem = (prof_l[~prof_l['we']].groupby('CODELIEU')['daytype']
           .value_counts(normalize=True).unstack(fill_value=0).add_prefix('sem_dt'))
sig_we  = (prof_l[prof_l['we']].groupby('CODELIEU')['daytype']
           .value_counts(normalize=True).unstack(fill_value=0).add_prefix('we_dt'))
sig = sig_sem.join(sig_we, how='inner')   # logements avec jours semaine ET week-end
print(f'Signatures logement : {len(sig)} logements x {sig.shape[1]} dims')

X = sig.values
rng = np.random.RandomState(0)
print(f"\n{'k':>2} {'silhouette':>10} {'stab. ARI':>10}  tailles")
results = {}
for k in range(2, 7):
    kml = KMeans(n_clusters=k, n_init=30, random_state=42)
    l   = kml.fit_predict(X)
    sil = silhouette_score(X, l)
    aris = []
    for _ in range(8):
        idx = rng.choice(len(X), int(0.8*len(X)), replace=False)
        l2  = KMeans(n_clusters=k, n_init=30, random_state=rng.randint(1e6)).fit_predict(X[idx])
        aris.append(adjusted_rand_score(l[idx], l2))
    results[k] = l
    print(f'{k:>2} {sil:>10.3f} {np.mean(aris):>10.3f}  {np.bincount(l)}')

K = 4
lab_log = pd.Series(results[K], index=sig.index, name='cluster')

print(f'\n=== k={K} : composition moyenne (% de jours par day-type) ===')
print('day-types: DT0=plat/absent  DT1=presence continue  DT2=pic nocturne/matinal  DT3=nuit haute+absence diurne')
comp = sig.groupby(lab_log).mean().round(2)
print((comp * 100).round(0).to_string())

# ===== validation : presence declaree par cluster logement =====
sem['present'] = sem['IDN_PIECE'].notna() & (sem['IDN_PIECE'] != 90)
sem['heure']   = (sem['CODE_HEURE'].str[2:].astype(int) - 1001) // 6
pres_h = sem.groupby(['CODELIEU','heure'])['present'].mean().unstack('heure')
common = lab_log.index.intersection(pres_h.index)
print(f'\n=== Presence declaree par cluster logement ({len(common)} logements) ===')
heures_aff = [0, 3, 6, 9, 12, 15, 18, 21]
hdr = '  '.join(f'{h:>5}h' for h in heures_aff)
print(f"{'cl':<4} {'n':>4}  {hdr}")
for c in range(K):
    m = pres_h.loc[common][lab_log.loc[common] == c].mean()
    vals = '  '.join(f'{100*m[h]:>5.0f}%' for h in heures_aff)
    print(f'C{c:<3} {(lab_log.loc[common]==c).sum():>4}  {vals}')

# ===== caracterisation menages =====
print('\n=== Colonnes q_menage ===')
print(list(q_men.columns))
print('\n=== Colonnes q_individu ===')
print(list(q_ind.columns))
