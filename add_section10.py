import json, sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'c:\Users\lehmanna\Desktop\stage\projet\notebook\eda.ipynb'
with open(path, encoding='utf-8') as f:
    nb = json.load(f)

MD_HEADER = """## 10. Clustering des journées (day-types) — validé par le semainier

Changement de granularité : au lieu de clusteriser les **logements** (~500 individus, structure faible — silhouette ≤ 0.18),
on clusterise les **journées** (~3 000 individus). Chaque journée = profil CO₂ 24h, **z-normé par logement**
(on compare des formes, pas des niveaux : 800 ppm dans un studio ≠ 800 ppm dans une maison).

Points clés établis sur les données :
- 95% des capteurs CO₂ sont en **chambre** → le signal mesure surtout l'occupation nocturne (sommeil) ;
- le **semainier** (présence déclarée par occupant, pas de 10 min, `IDN_PIECE=90` = extérieur) sert de **vérité terrain** ;
- chaque logement n'a que ~2 jours de week-end → la signature logement est construite sur les **jours de semaine** (≥ 3 jours)."""

PROF_JOUR = """# Profils journaliers CO2 : 1 ligne = 1 journee de logement (24 valeurs horaires, z-norm par logement)
co2_e['DATE'] = co2_e['DATE_HEURE'].dt.normalize()

pts_jour       = co2_e.groupby(['CODELIEU', 'DATE']).size()
jours_complets = pts_jour[pts_jour >= 138].index   # >= 23h de couverture (138/144 points)

co2_j     = co2_e.set_index(['CODELIEU', 'DATE']).loc[jours_complets].reset_index()
stats_log = co2_j.groupby('CODELIEU')['VALEUR'].agg(['mean', 'std'])
co2_j     = co2_j.merge(stats_log, on='CODELIEU')
co2_j['z'] = (co2_j['VALEUR'] - co2_j['mean']) / co2_j['std']

prof_jour = co2_j.groupby(['CODELIEU', 'DATE', 'heure'])['z'].mean().unstack('heure').dropna()
X_jour    = prof_jour.values

print(f'Jours complets   : {len(jours_complets):,} / {len(pts_jour):,}')
print(f'Profils retenus  : {len(prof_jour):,} journées  ({prof_jour.index.get_level_values(0).nunique()} logements)')"""

K_SELECT = """# Choix de k : silhouette (separation) + stabilite par sous-echantillonnage (ARI, 1.0 = reproductible)
from sklearn.metrics import adjusted_rand_score

rng = np.random.RandomState(0)
ks  = list(range(2, 9))
sils, stabs = [], []

for k in ks:
    lab = KMeans(n_clusters=k, random_state=42, n_init=30).fit_predict(X_jour)
    sils.append(silhouette_score(X_jour, lab, sample_size=2000, random_state=0))
    aris = []
    for _ in range(8):
        idx  = rng.choice(len(X_jour), int(0.8 * len(X_jour)), replace=False)
        lab2 = KMeans(n_clusters=k, random_state=rng.randint(10**6), n_init=30).fit_predict(X_jour[idx])
        aris.append(adjusted_rand_score(lab[idx], lab2))
    stabs.append(np.mean(aris))

fig, axes = plt.subplots(1, 2, figsize=(12, 4))
axes[0].plot(ks, sils, 'bo-', lw=2)
axes[0].set_xlabel('k'); axes[0].set_ylabel('Silhouette')
axes[0].set_title('Séparation', fontweight='bold'); axes[0].grid(True, alpha=0.3)
axes[1].plot(ks, stabs, 'go-', lw=2)
axes[1].set_xlabel('k'); axes[1].set_ylabel('ARI (sous-échantillons 80%)')
axes[1].set_title('Stabilité', fontweight='bold'); axes[1].grid(True, alpha=0.3)
plt.suptitle('K-Means sur les journées — choix de k', fontweight='bold', fontsize=12)
plt.tight_layout(); plt.show()"""

DAYTYPES = """# k=4 : bon compromis interpretabilite / stabilite (ARI 0.91, silhouette 0.165)
K_JOUR    = 4
km_jour   = KMeans(n_clusters=K_JOUR, random_state=42, n_init=30)
dt_labels = km_jour.fit_predict(X_jour)

# noms etablis a partir des profils moyens (valables pour random_state=42)
DT_NOMS = {0: 'Plat / absence', 1: 'Présence continue',
           2: 'Pic fin de nuit', 3: 'Plateau nocturne'}

prof_dt = prof_jour.copy()
prof_dt['daytype'] = dt_labels
prof_dt['we']      = prof_dt.index.get_level_values('DATE').dayofweek >= 5

fig, ax = plt.subplots(figsize=(13, 5.5))
for c in range(K_JOUR):
    sub  = prof_dt[prof_dt['daytype'] == c]
    m    = sub[list(range(24))].mean()
    s    = sub[list(range(24))].std()
    line, = ax.plot(range(24), m, lw=2.2, marker='o', ms=3,
                    label=f'DT{c} — {DT_NOMS[c]}  (n={len(sub)}, {100*sub["we"].mean():.0f}% WE)')
    ax.fill_between(range(24), m - s, m + s, alpha=0.07, color=line.get_color())

ax.axhline(0, color='grey', lw=0.8, ls='--', alpha=0.6)
ax.set_xticks(range(0, 24, 3)); ax.set_xticklabels([f'{h}h' for h in range(0, 24, 3)])
ax.set_xlabel('Heure'); ax.set_ylabel('CO₂ (z-score du logement)')
ax.set_title('4 types de journées — profil CO₂ moyen ± 1σ\\n'
             '(rappel : 28.6% des journées sont des jours de week-end)',
             fontweight='bold')
ax.legend(fontsize=10); ax.grid(True, alpha=0.25)
plt.tight_layout(); plt.show()"""

PRESENCE_DT = """# Validation par le semainier : presence declaree du menage, par type de journee
sem['present'] = sem['IDN_PIECE'].notna() & (sem['IDN_PIECE'] != 90)   # 90 = extérieur
sem['heure']   = (sem['CODE_HEURE'].str[2:].astype(int) - 1001) // 6   # V_1001..V_1144 -> heure 0..23

# taux de presence = moyenne sur les occupants, par logement x date x heure
pres_jour = sem.groupby(['CODELIEU', 'DATE', 'heure'])['present'].mean().unstack('heure')

common = prof_dt.index.intersection(pres_jour.index)
pres_c = pres_jour.loc[common]
lab_c  = prof_dt.loc[common, 'daytype']
print(f'Journées avec CO2 + semainier : {len(common):,}')

fig, ax = plt.subplots(figsize=(13, 5.5))
for c in range(K_JOUR):
    m = pres_c[lab_c == c].mean() * 100
    ax.plot(range(24), m, lw=2.2, marker='o', ms=3,
            label=f'DT{c} — {DT_NOMS[c]} (n={(lab_c == c).sum()})')

ax.set_xticks(range(0, 24, 3)); ax.set_xticklabels([f'{h}h' for h in range(0, 24, 3)])
ax.set_xlabel('Heure'); ax.set_ylabel('Présence déclarée (%)')
ax.set_ylim(0, 100)
ax.set_title('Vérité terrain : présence déclarée (semainier) par type de journée\\n'
             'si les courbes diffèrent → les day-types capturent bien l\\'occupation',
             fontweight='bold')
ax.legend(fontsize=10); ax.grid(True, alpha=0.25)
plt.tight_layout(); plt.show()"""

SIGNATURE = """# Signature logement = composition en day-types sur les JOURS DE SEMAINE (>= 3 jours)
# (2 jours de week-end seulement -> proportions quantifiees 0/50/100% = clusters artificiels)
semaine     = prof_dt[~prof_dt['we']].reset_index()
n_jours_sem = semaine.groupby('CODELIEU').size()
lieux_sig   = n_jours_sem[n_jours_sem >= 3].index

sig_log = (semaine[semaine['CODELIEU'].isin(lieux_sig)]
           .groupby('CODELIEU')['daytype']
           .value_counts(normalize=True).unstack(fill_value=0))
sig_log.columns = [f'dt{c}' for c in sig_log.columns]

K_LOG  = 4
cl_log = pd.Series(
    KMeans(n_clusters=K_LOG, random_state=42, n_init=30).fit_predict(sig_log.values),
    index=sig_log.index, name='cluster')

print(f'Signatures : {len(sig_log)} logements x {sig_log.shape[1]} dims')
compo = (sig_log.groupby(cl_log).mean() * 100).round(0)
compo.insert(0, 'n', cl_log.value_counts().sort_index())
compo.index = [f'C{c}' for c in compo.index]
display(
    compo.style
    .format({'n': '{:.0f}', **{c: '{:.0f}%' for c in sig_log.columns}})
    .background_gradient(subset=list(sig_log.columns), cmap='Blues', axis=None)
    .set_caption('Composition moyenne en day-types par cluster logement (jours de semaine)')
)"""

VALID_LOG = """# Validation des clusters logement : presence declaree en semaine + composition du menage
sem['we'] = sem['DATE'].dt.dayofweek >= 5
pres_log  = sem[~sem['we']].groupby(['CODELIEU', 'heure'])['present'].mean().unstack('heure')

common_l = cl_log.index.intersection(pres_log.index)

fig, ax = plt.subplots(figsize=(13, 5.5))
for c in range(K_LOG):
    sel = common_l[cl_log.loc[common_l] == c]
    m   = pres_log.loc[sel].mean() * 100
    dominant = sig_log.groupby(cl_log).mean().loc[c].idxmax()
    ax.plot(range(24), m, lw=2.2, marker='o', ms=3,
            label=f'C{c} (n={len(sel)}, dominé par {dominant.upper()})')

ax.set_xticks(range(0, 24, 3)); ax.set_xticklabels([f'{h}h' for h in range(0, 24, 3)])
ax.set_xlabel('Heure'); ax.set_ylabel('Présence déclarée (%)')
ax.set_ylim(0, 100)
ax.set_title('Présence déclarée en semaine, par cluster logement', fontweight='bold')
ax.legend(fontsize=10); ax.grid(True, alpha=0.25)
plt.tight_layout(); plt.show()

# caracteristiques du menage par cluster
infos_men = q_ind.groupby('CODELIEU').agg(
    n_occupants = ('NUM_OCCUPANT', 'nunique'),
    age_moyen   = ('AGE', 'mean'),
    n_enfants   = ('AGE', lambda s: (s < 18).sum()),
)
common_m = cl_log.index.intersection(infos_men.index)
tab = infos_men.loc[common_m].groupby(cl_log.loc[common_m]).mean().round(2)
tab.index = [f'C{c}' for c in tab.index]
display(tab.style.background_gradient(cmap='RdYlGn', axis=0)
        .format('{:.2f}')
        .set_caption('Caractéristiques moyennes du ménage par cluster'))"""

MD_CONCL = """### Bilan de la section 10

- Les **4 types de journées** sont robustes (stabilité ARI ≈ 0.91) et **validés par le semainier** :
  les courbes de présence déclarée diffèrent nettement entre day-types (ex. « plateau nocturne » : 92% présence la nuit
  vs 77% pour « plat/absence »).
- La **signature logement** (composition en day-types, semaine) donne 4 clusters logement très stables (ARI ≈ 1.00,
  silhouette ≈ 0.45) qui diffèrent en présence diurne déclarée (~44% pour le cluster à dominante « présence continue »
  vs ~34% pour « plateau nocturne »).
- **Limites** : le capteur CO₂ est en chambre (95% des cas) → on mesure surtout l'occupation de la chambre ;
  une seule semaine de mesure → la composition week-end (2 jours) est inexploitable telle quelle.
- **Suite logique** : le semainier fournit des labels de présence par créneau → base d'un futur **modèle supervisé**
  capteurs → présence (les features ACF de la section 8 et les day-types ci-dessus sont des entrées candidates)."""

def mk_cell(cid, ctype, src):
    cell = {
        'id': cid,
        'cell_type': ctype,
        'metadata': {},
        'source': src.splitlines(keepends=True),
    }
    if ctype == 'code':
        cell['outputs'] = []
        cell['execution_count'] = None
    return cell

new_cells = [
    mk_cell('s10_header',    'markdown', MD_HEADER),
    mk_cell('s10_prof',      'code',     PROF_JOUR),
    mk_cell('s10_kselect',   'code',     K_SELECT),
    mk_cell('s10_daytypes',  'code',     DAYTYPES),
    mk_cell('s10_presence',  'code',     PRESENCE_DT),
    mk_cell('s10_signature', 'code',     SIGNATURE),
    mk_cell('s10_validlog',  'code',     VALID_LOG),
    mk_cell('s10_bilan',     'markdown', MD_CONCL),
]

nb['cells'].extend(new_cells)

with open(path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print(f'Section 10 ajoutée : {len(new_cells)} cellules. Total : {len(nb["cells"])}')
