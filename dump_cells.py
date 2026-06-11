import json, sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'c:\Users\lehmanna\Desktop\stage\projet\notebook\eda.ipynb', encoding='utf-8') as f:
    nb = json.load(f)

ids = sys.argv[1].split(',')
for cell in nb['cells']:
    if cell.get('id') in ids:
        print(f"===== {cell['id']} =====")
        print(''.join(cell['source']))
        print()
