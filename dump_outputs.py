import json, sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'c:\Users\lehmanna\Desktop\stage\projet\notebook\eda.ipynb', encoding='utf-8') as f:
    nb = json.load(f)

ids = sys.argv[1].split(',')
for cell in nb['cells']:
    if cell.get('id') in ids:
        print(f"===== {cell['id']} (outputs) =====")
        for out in cell.get('outputs', []):
            ot = out.get('output_type')
            if ot == 'stream':
                print(''.join(out.get('text', [])))
            elif ot in ('execute_result', 'display_data'):
                data = out.get('data', {})
                if 'text/plain' in data:
                    print(''.join(data['text/plain'])[:3000])
                else:
                    print(f"[{ot}: {list(data.keys())}]")
            elif ot == 'error':
                print('ERROR:', out.get('ename'), out.get('evalue'))
        print()
