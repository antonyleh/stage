import json, sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'c:\Users\lehmanna\Desktop\stage\projet\notebook\eda.ipynb'
with open(path, encoding='utf-8') as f:
    nb = json.load(f)

new_source = (
    "from sklearn.preprocessing import StandardScaler\n"
    "from sklearn.decomposition import PCA\n"
    "from sklearn.cluster import KMeans\n"
    "from sklearn.mixture import GaussianMixture\n"
    "from sklearn.metrics import silhouette_score\n"
    "\n"
    "MESURES_PROF = [\n"
    "    (co2_e,     'VALEUR',     'co2'),\n"
    "    (confort_e, 'VALEUR_TPT', 'tpt'),\n"
    "    (confort_e, 'VALEUR_HRE', 'hre'),\n"
    "]\n"
    "PTS_PAR_JOUR = 144  # 6 mesures/h x 24h\n"
    "MIN_JOURS    = 3\n"
    "\n"
    "# Réutilisation de coverage (section 8) — déjà calculé\n"
    "lieux_valides = coverage.loc[\n"
    "    coverage['n_min'] >= MIN_JOURS * PTS_PAR_JOUR, 'CODELIEU'\n"
    "].tolist()\n"
    "N_POINTS = (coverage.set_index('CODELIEU')\n"
    "            .loc[lieux_valides, 'n_min'].min() // PTS_PAR_JOUR) * PTS_PAR_JOUR\n"
    "N_DAYS   = N_POINTS // PTS_PAR_JOUR\n"
    "print(f'Seuil     : {MIN_JOURS} jours minimum')\n"
    "print(f'Logements : {len(lieux_valides)} / {len(log)}')\n"
    "print(f'Features  : {N_DAYS} jours x 3 signaux x {PTS_PAR_JOUR} mesures = {N_DAYS*3*PTS_PAR_JOUR}')\n"
    "\n"
    "# Construction vectorisée — 1 ligne = 1 logement, 1 colonne = 1 mesure brute\n"
    "dfs = []\n"
    "for df_m, col_name, prefix in MESURES_PROF:\n"
    "    tmp = (df_m[df_m['CODELIEU'].isin(lieux_valides)]\n"
    "           .dropna(subset=[col_name])\n"
    "           .sort_values(['CODELIEU', 'DATE_HEURE'])\n"
    "           .assign(pos=lambda x: x.groupby('CODELIEU').cumcount())\n"
    "           .query(f'pos < {N_POINTS}')[['CODELIEU', 'pos', col_name]])\n"
    "    tmp = tmp.copy()\n"
    "    d = tmp['pos'] // PTS_PAR_JOUR\n"
    "    p = tmp['pos'] % PTS_PAR_JOUR\n"
    "    tmp['feat'] = prefix + '_d' + d.astype(str) + '_' + p.astype(str).str.zfill(3)\n"
    "    dfs.append(tmp.pivot(index='CODELIEU', columns='feat', values=col_name))\n"
    "\n"
    "df_prof = pd.concat(dfs, axis=1)\n"
    "df_prof.columns.name = None\n"
    "df_prof = df_prof.dropna()\n"
    "print(f'Shape df_prof : {df_prof.shape}')\n"
    "display(df_prof.iloc[:3, :6].round(2))"
)

for cell in nb['cells']:
    if cell.get('id') == 'prof_build':
        cell['source'] = new_source
        cell['outputs'] = []
        cell['execution_count'] = None
        break

with open(path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print("Done.")
