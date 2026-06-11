import json, sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'c:\Users\lehmanna\Desktop\stage\projet\notebook\eda.ipynb'
with open(path, encoding='utf-8') as f:
    nb = json.load(f)

# ── 1. Cellule helper (après 87953961, avant section 8) ──────────────────
cell_helper = {
    "cell_type": "code", "id": "plot_helper", "metadata": {}, "outputs": [], "execution_count": None,
    "source": (
        "def plot_weekly_profiles(cluster_map, labels, k_bic, method_name):\n"
        "    SIGNALS = [\n"
        "        (co2_e,     'VALEUR',     'CO2 (ppm)',  '#4C72B0'),\n"
        "        (confort_e, 'VALEUR_TPT', 'Temp. (°C)', '#C44E52'),\n"
        "        (confort_e, 'VALEUR_HRE', 'Humid. (%)', '#55A868'),\n"
        "    ]\n"
        "    k_clusters = sorted(set(labels))\n"
        "    ncols = min(len(k_clusters), 4)\n"
        "    nrows = (len(k_clusters) + ncols - 1) // ncols\n"
        "    for df_m, col_m, label_m, color_m in SIGNALS:\n"
        "        fig, axes = plt.subplots(nrows, ncols, figsize=(ncols*5, nrows*3.5),\n"
        "                                 sharey=True, sharex=True)\n"
        "        axes_flat = axes.flatten() if len(k_clusters) > 1 else [axes]\n"
        "        for i, c in enumerate(k_clusters):\n"
        "            ax  = axes_flat[i]\n"
        "            lieux_c = [l for l, cl in cluster_map.items() if cl == c]\n"
        "            sub = df_m[df_m['CODELIEU'].isin(lieux_c)]\n"
        "            n   = sub['CODELIEU'].nunique()\n"
        "            if n == 0: ax.axis('off'); continue\n"
        "            profils = sub.groupby(['CODELIEU','cal_pos'])[col_m].mean().unstack('cal_pos')\n"
        "            for _, row_p in profils.iterrows():\n"
        "                ax.plot(row_p.index, row_p.values, color=color_m, alpha=0.2, lw=0.6)\n"
        "            ax.axvspan(120, 168, color='#FFD700', alpha=0.08)\n"
        "            ax.set_xticks(tick_pos); ax.set_xticklabels(tick_labels, fontsize=8)\n"
        "            ax.set_xlim(0, 168)\n"
        "            for xv in tick_pos[1:-1]: ax.axvline(xv, color='grey', lw=0.5, ls='--', alpha=0.4)\n"
        "            ax.grid(True, alpha=0.2)\n"
        "            ax.set_title(f'C{c}  (n={n})', fontweight='bold', fontsize=10)\n"
        "            if i % ncols == 0: ax.set_ylabel(label_m, fontsize=9)\n"
        "        for i in range(len(k_clusters), len(axes_flat)): axes_flat[i].axis('off')\n"
        "        plt.suptitle(f'Profils {label_m} — Lun → Dim — {method_name} (k={k_bic})\\n'\n"
        "                     '(chaque courbe = 1 logement  |  jaune = week-end)',\n"
        "                     fontweight='bold', fontsize=12)\n"
        "        plt.tight_layout(); plt.show()"
    )
}

# ── 2. profiles_by_cluster (section 8) simplifié ─────────────────────────
src_s8_profiles = (
    "cluster_map = dict(zip(df_acf.index, labels))\n"
    "plot_weekly_profiles(cluster_map, labels, k_bic, 'ACF-GMM')"
)

# ── 3. prof_build corrigé (N_POINTS bug + suppression col_map) ───────────
src_prof_build = (
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
    "MIN_JOURS    = 3    # exclure les logements avec moins de 3 jours complets\n"
    "\n"
    "# Nombre de points bruts par logement (min des 3 signaux)\n"
    "lieux_communs = set(co2_e['CODELIEU']) & set(confort_e['CODELIEU'])\n"
    "n_pts_per = {\n"
    "    cl: min(df_m[df_m['CODELIEU'] == cl][col].dropna().shape[0]\n"
    "            for df_m, col, _ in MESURES_PROF)\n"
    "    for cl in lieux_communs\n"
    "}\n"
    "\n"
    "# Garder uniquement les logements avec au moins MIN_JOURS jours complets\n"
    "lieux_valides = {cl for cl, n in n_pts_per.items() if n >= MIN_JOURS * PTS_PAR_JOUR}\n"
    "N_POINTS = min(n_pts_per[cl] for cl in lieux_valides)\n"
    "N_DAYS   = N_POINTS // PTS_PAR_JOUR\n"
    "N_POINTS = N_DAYS * PTS_PAR_JOUR\n"
    "print(f'Seuil        : {MIN_JOURS} jours minimum')\n"
    "print(f'Logements    : {len(lieux_valides)} / {len(log)}')\n"
    "print(f'Points/logement : {N_POINTS}  ({N_DAYS} jours x {PTS_PAR_JOUR} mesures)')\n"
    "\n"
    "# 1 ligne = 1 logement, 1 colonne = 1 mesure brute\n"
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
    "print(f'Shape df_prof : {df_prof.shape}  ({N_DAYS*3*PTS_PAR_JOUR} features)')\n"
    "display(df_prof.iloc[:3, :6].round(2))"
)

# ── 4. profiles_by_cluster_prof (section 9) simplifié ────────────────────
src_s9_profiles = (
    "cluster_map = dict(zip(df_prof.index, labels))\n"
    "plot_weekly_profiles(cluster_map, labels, k_bic, 'Profil-GMM')"
)

# ── Application des modifications ─────────────────────────────────────────
new_cells = []
for cell in nb['cells']:
    cid = cell.get('id', '')

    if cid == '87953961':
        new_cells.append(cell)
        new_cells.append(cell_helper)
        continue

    if cid == 'profiles_by_cluster':
        cell['source'] = src_s8_profiles
        cell['outputs'] = []; cell['execution_count'] = None

    if cid == 'prof_build':
        cell['source'] = src_prof_build
        cell['outputs'] = []; cell['execution_count'] = None

    if cid == 'profiles_by_cluster_prof':
        cell['source'] = src_s9_profiles
        cell['outputs'] = []; cell['execution_count'] = None

    new_cells.append(cell)

nb['cells'] = new_cells

with open(path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print("Done.")
ids = [c.get('id','?') for c in nb['cells']]
for i, cid in enumerate(ids):
    print(f"  {i:2d}. {cid}")
