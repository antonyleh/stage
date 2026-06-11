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
    "\n"
    "# Logements presents dans les 3 signaux\n"
    "lieux_valides = (\n"
    "    set(co2_e['CODELIEU'])\n"
    "    & set(confort_e['CODELIEU'])\n"
    ")\n"
    "\n"
    "# Nombre de points bruts disponibles par logement (min des 3 signaux)\n"
    "n_pts_per = {}\n"
    "for cl in lieux_valides:\n"
    "    n_pts_per[cl] = min(\n"
    "        df_m[df_m['CODELIEU'] == cl][col].dropna().shape[0]\n"
    "        for df_m, col, _ in MESURES_PROF\n"
    "    )\n"
    "\n"
    "# Tronquer au nombre de jours complets communs a tous\n"
    "N_POINTS = min(n_pts_per.values())\n"
    "N_DAYS   = N_POINTS // PTS_PAR_JOUR\n"
    "N_POINTS = N_DAYS * PTS_PAR_JOUR\n"
    "print(f'Points par logement : {N_POINTS}  ({N_DAYS} jours x {PTS_PAR_JOUR} mesures/jour)')\n"
    "print(f'Logements retenus   : {len(lieux_valides)} / {len(log)}')\n"
    "\n"
    "# Construction : 1 ligne = 1 logement, 1 colonne = 1 mesure brute\n"
    "rows = []\n"
    "for cl in sorted(lieux_valides):\n"
    "    row = {'CODELIEU': cl}\n"
    "    for df_m, col_name, prefix in MESURES_PROF:\n"
    "        vals = (df_m[df_m['CODELIEU'] == cl]\n"
    "                .sort_values('DATE_HEURE')[col_name]\n"
    "                .dropna().values[:N_POINTS])\n"
    "        for i, v in enumerate(vals):\n"
    "            d, p = divmod(i, PTS_PAR_JOUR)\n"
    "            row[f'{prefix}_d{d}_{p:03d}'] = v\n"
    "    rows.append(row)\n"
    "\n"
    "df_prof = pd.DataFrame(rows).set_index('CODELIEU').dropna()\n"
    "print(f'Shape df_prof : {df_prof.shape}')\n"
    "print(f'  -> {len(df_prof)} logements x {N_DAYS} jours x 3 signaux x {PTS_PAR_JOUR} pts = {N_DAYS*3*PTS_PAR_JOUR} features')\n"
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
