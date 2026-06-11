import json, sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'c:\Users\lehmanna\Desktop\stage\projet\notebook\preparation.ipynb', encoding='utf-8') as f:
    nb = json.load(f)
print(f"{len(nb['cells'])} cellules")
for i, cell in enumerate(nb['cells']):
    src = ''.join(cell['source'])
    first = src.split('\n')[0][:90]
    print(f"{i:2d}. [{cell['cell_type']:8s}] {cell.get('id','?'):20s} {first}")
