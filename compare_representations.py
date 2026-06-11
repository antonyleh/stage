import sys
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd
import numpy as np
from pathlib import Path
from statsmodels.tsa.stattools import acf
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
from sklearn.metrics import silhouette_score, adjusted_rand_score

CLEAN = Path(r'c:\Users\lehmanna\Desktop\stage\projet\data\cln1\Clean')
log     = pd.read_parquet(CLEAN / 'Referentiels/logements.parquet')
co2     = pd.read_parquet(CLEAN / 'Mesures/co2.parquet')
confort = pd.read_parquet(CLEAN / 'Mesures/confort.parquet')

for df in (co2, confort):
    df['jour_sem'] = df['DATE_HEURE'].dt.dayofweek
    df['heure']    = df['DATE_HEURE'].dt.hour
    df['cal_pos']  = df['jour_sem'] * 24 + df['heure']

# --- couverture (comme section 8) ---
MIN_POINTS = 482
cov = pd.DataFrame({'CODELIEU': log['CODELIEU']})
for df_m, col, p in [(co2,'VALEUR','co2'),(confort,'VALEUR_TPT','tpt'),(confort,'VALEUR_HRE','hre')]:
    cov = cov.merge(df_m.groupby('CODELIEU')[col].count().rename(f'n_{p}'), on='CODELIEU', how='left')
cov = cov.fillna(0)
cov['n_min'] = cov[['n_co2','n_tpt','n_hre']].min(axis=1)
valides = cov[cov['n_min'] > MIN_POINTS]['CODELIEU'].tolist()

# --- A. features ACF ---
rows = []
for cl in valides:
    row = {'CODELIEU': cl}
    for df_m, col, p in [(co2,'VALEUR','co2'),(confort,'VALEUR_TPT','tpt'),(confort,'VALEUR_HRE','hre')]:
        ts = df_m[df_m['CODELIEU']==cl].sort_values('DATE_HEURE')[col].dropna().values
        v = acf(ts, nlags=144, fft=True)
        for lag in [1,72,144]:
            row[f'{p}_acf_{lag}'] = v[lag]
    rows.append(row)
df_acf = pd.DataFrame(rows).set_index('CODELIEU').dropna()

# outlier capteur exclu partout pour comparer a logements identiques
df_acf = df_acf.drop('02-M028', errors='ignore')

# --- B. profils hebdo moyens (cal_pos) ---
co2_p = co2.groupby(['CODELIEU','cal_pos'])['VALEUR'].mean().unstack('cal_pos').add_prefix('co2_')
tpt_p = confort.groupby(['CODELIEU','cal_pos'])['VALEUR_TPT'].mean().unstack('cal_pos').add_prefix('tpt_')
hre_p = confort.groupby(['CODELIEU','cal_pos'])['VALEUR_HRE'].mean().unstack('cal_pos').add_prefix('hre_')
df_prof = co2_p.join(tpt_p, how='inner').join(hre_p, how='inner').dropna()

common = df_acf.index.intersection(df_prof.index)
df_acf, df_prof = df_acf.loc[common], df_prof.loc[common]
print(f'Logements communs : {len(common)}')

# --- C. features comportementales derivees (12) ---
def weekly_features(df_p, prefix):
    cols = [c for c in df_p.columns if c.startswith(prefix)]
    M = df_p[cols].values  # (n, 168)
    pos = np.arange(168)
    heure = pos % 24
    jour  = pos // 24
    we    = jour >= 5
    day   = (heure >= 8) & (heure < 19)
    return pd.DataFrame({
        f'{prefix}mean': M.mean(1),
        f'{prefix}amp':  M.max(1) - M.min(1),
        f'{prefix}we':   M[:, we].mean(1) - M[:, ~we].mean(1),
        f'{prefix}dn':   M[:, day].mean(1) - M[:, ~day].mean(1),
    }, index=df_p.index)

df_beh = pd.concat([weekly_features(df_prof, p) for p in ['co2_','tpt_','hre_']], axis=1)

# --- D. forme des profils (z-norm par logement puis PCA) ---
def shape_pca(df_p, prefix, n=8):
    cols = [c for c in df_p.columns if c.startswith(prefix)]
    M = df_p[cols].values
    Mz = (M - M.mean(1, keepdims=True)) / (M.std(1, keepdims=True) + 1e-9)  # forme pure
    return PCA(n_components=n, random_state=0).fit_transform(Mz)
X_shape = np.hstack([shape_pca(df_prof, p) for p in ['co2_','tpt_','hre_']])

REPRESENTATIONS = {
    'A. ACF 9 feats (actuel)':        StandardScaler().fit_transform(df_acf),
    'B. ACF 6 feats (sans lag-1)':    StandardScaler().fit_transform(df_acf[[c for c in df_acf.columns if '_acf_1' not in c or c.endswith(('72','144'))]].filter(regex='_(72|144)$')),
    'C. 12 feats comportementales':   StandardScaler().fit_transform(df_beh),
    'D. forme profils (z-norm+PCA)':  StandardScaler().fit_transform(X_shape),
}

rng = np.random.RandomState(0)
print(f"\n{'representation':<32} {'k':>2} {'silhouette':>10} {'stabilite ARI':>13}")
for name, X in REPRESENTATIONS.items():
    for k in [3, 4, 6, 8]:
        km = KMeans(n_clusters=k, n_init=30, random_state=42)
        lab = km.fit_predict(X)
        sil = silhouette_score(X, lab)
        # stabilite : refit sur 80% x10, ARI sur les points communs
        aris = []
        for _ in range(10):
            idx = rng.choice(len(X), int(0.8*len(X)), replace=False)
            km2 = KMeans(n_clusters=k, n_init=30, random_state=rng.randint(1e6))
            lab2 = km2.fit_predict(X[idx])
            aris.append(adjusted_rand_score(lab[idx], lab2))
        print(f'{name:<32} {k:>2} {sil:>10.3f} {np.mean(aris):>13.3f}')
    print()
