import json, sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'c:\Users\lehmanna\Desktop\stage\projet\notebook\eda.ipynb'
with open(path, encoding='utf-8') as f:
    nb = json.load(f)

n_fixed = 0
for cell in nb['cells']:
    src = cell['source']
    if isinstance(src, str):
        lines = src.splitlines(keepends=True)
        cell['source'] = lines
        n_fixed += 1

with open(path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print(f"Normalisé {n_fixed} cellules. Total cellules : {len(nb['cells'])}")
