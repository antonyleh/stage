import json, sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'c:\Users\lehmanna\Desktop\stage\projet\notebook\eda.ipynb'
with open(path, encoding='utf-8') as f:
    nb = json.load(f)

NEW_SOURCE = (
    "def _plot_pca_clusters(ax, x2d, lbls, n_clusters, title, ev_ratio):\n"
    "    ax.scatter(x2d[:, 0], x2d[:, 1], c=lbls, cmap='tab10', s=40, alpha=0.7)\n"
    "    for c in range(n_clusters):\n"
    "        mask = lbls == c\n"
    "        if mask.sum() == 0: continue\n"
    "        cx, cy = x2d[mask, 0].mean(), x2d[mask, 1].mean()\n"
    "        ax.annotate(f'C{c}', (cx, cy), fontsize=9, fontweight='bold', ha='center',\n"
    "                    bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8, edgecolor='grey'))\n"
    "    ax.set_xlabel(f'PC1 ({ev_ratio[0]*100:.1f}%)')\n"
    "    ax.set_ylabel(f'PC2 ({ev_ratio[1]*100:.1f}%)')\n"
    "    ax.set_title(title, fontweight='bold'); ax.grid(True, alpha=0.2)"
)

for cell in nb['cells']:
    if cell.get('id') == 'plot_helper':
        cell['source'] = NEW_SOURCE.splitlines(keepends=True)
        cell['outputs'] = []
        cell['execution_count'] = None

with open(path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print("Done.")
