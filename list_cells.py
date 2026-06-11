import json, sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'c:\Users\lehmanna\Desktop\stage\projet\notebook\eda.ipynb', encoding='utf-8') as f:
    nb = json.load(f)
for i, cell in enumerate(nb['cells']):
    cid = cell.get('id','?')
    ctype = cell['cell_type']
    src = ''.join(cell['source'])
    first_line = src.split('\n')[0][:90]
    nlines = len(cell['source'])
    print(f'{i:2d}. [{ctype:8s}] {cid:25s} ({nlines:3d} lines) {first_line}')
