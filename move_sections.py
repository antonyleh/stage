import json, sys
sys.stdout.reconfigure(encoding='utf-8')

eda_path  = r'c:\Users\lehmanna\Desktop\stage\projet\notebook\eda.ipynb'
prep_path = r'c:\Users\lehmanna\Desktop\stage\projet\notebook\preparation.ipynb'

with open(eda_path, encoding='utf-8') as f:
    eda = json.load(f)
with open(prep_path, encoding='utf-8') as f:
    prep = json.load(f)

# --- cellules a deplacer (sections 2 a 5 d'eda) ---
MOVE_IDS = ['c80aac63', 'f16b3ecd',                                   # 2. Vue d'ensemble
            '4ccfa668', '899a330b', '058db02f', 'e058d666',           # 3. Mesures physiques
            '54ff719e', '80de4e1d',
            'efb4f279', 'd60f18fe', '38df7673',                       # 4. Variables logement
            '3b04ad8e', 'd32e2bd6']                                   # 5. Variables occupants

moved   = [c for c in eda['cells'] if c.get('id') in MOVE_IDS]
assert len(moved) == len(MOVE_IDS), f'trouvé {len(moved)} cellules au lieu de {len(MOVE_IDS)}'

# --- renumerotation des titres dans les cellules deplacees (2-5 -> 7-10) ---
RENUM_MOVED = {'## 2.': '## 7.', '## 3.': '## 8.', '## 4.': '## 9.', '## 5.': '## 10.'}
for c in moved:
    if c['cell_type'] == 'markdown':
        src = ''.join(c['source'])
        for old, new in RENUM_MOVED.items():
            if src.startswith(old):
                src = src.replace(old, new, 1)
        c['source'] = src.splitlines(keepends=True)

# --- cellule pont : copie de la config d'eda (recharge les parquets nettoyes + enrichissement) ---
cfg = next(c for c in eda['cells'] if c.get('id') == '93b0a497')
bridge_md = {
    'id': 'prep_reload_md', 'cell_type': 'markdown', 'metadata': {},
    'source': ("## 6. Rechargement des données nettoyées (enrichies)\n\n"
               "Les sections suivantes (analyse univariée) travaillent sur les données **nettoyées**\n"
               "sauvegardées en section 5, rechargées et enrichies (zone climatique, saison, pièce).")
              .splitlines(keepends=True),
}
bridge_code = {
    'id': 'prep_reload', 'cell_type': 'code', 'metadata': {},
    'source': list(cfg['source']), 'outputs': [], 'execution_count': None,
}

prep['cells'].extend([bridge_md, bridge_code] + moved)

# --- eda : retirer les cellules deplacees + renumeroter 6-9 -> 2-5 ---
eda['cells'] = [c for c in eda['cells'] if c.get('id') not in MOVE_IDS]
RENUM_EDA = {'## 6.': '## 2.', '## 7.': '## 3.', '## 8.': '## 4.', '## 9.': '## 5.'}
for c in eda['cells']:
    if c['cell_type'] == 'markdown':
        src = ''.join(c['source'])
        changed = False
        for old, new in RENUM_EDA.items():
            if src.startswith(old):
                src = src.replace(old, new, 1)
                changed = True
        # references croisees dans le texte
        if 'section 8' in src:
            src = src.replace('section 8', 'section 4'); changed = True
        if 'section 9' in src:
            src = src.replace('section 9', 'section 5'); changed = True
        if changed:
            c['source'] = src.splitlines(keepends=True)

# verification : signaler toute mention restante de 'section N'
import re
for c in eda['cells']:
    src = ''.join(c['source'])
    for m in re.findall(r'[Ss]ection\s+\d+', src):
        print(f"  ref dans eda [{c.get('id')}]: {m}")
for c in prep['cells']:
    src = ''.join(c['source'])
    for m in re.findall(r'[Ss]ection\s+\d+', src):
        print(f"  ref dans prep [{c.get('id')}]: {m}")

with open(eda_path, 'w', encoding='utf-8') as f:
    json.dump(eda, f, ensure_ascii=False, indent=1)
with open(prep_path, 'w', encoding='utf-8') as f:
    json.dump(prep, f, ensure_ascii=False, indent=1)

print(f'eda  : {len(eda["cells"])} cellules')
print(f'prep : {len(prep["cells"])} cellules')
