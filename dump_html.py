import json, sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open(r'c:\Users\lehmanna\Desktop\stage\projet\notebook\eda.ipynb', encoding='utf-8') as f:
    nb = json.load(f)

ids = sys.argv[1].split(',')
for cell in nb['cells']:
    if cell.get('id') in ids:
        print(f"===== {cell['id']} =====")
        for out in cell.get('outputs', []):
            data = out.get('data', {})
            if 'text/html' in data:
                html = ''.join(data['text/html'])
                # crude table -> text extraction
                html = re.sub(r'<style.*?</style>', '', html, flags=re.S)
                rows = re.findall(r'<tr[^>]*>(.*?)</tr>', html, flags=re.S)
                cap = re.search(r'<caption[^>]*>(.*?)</caption>', html, flags=re.S)
                if cap:
                    print('CAPTION:', re.sub(r'<[^>]+>', '', cap.group(1)).strip())
                for r in rows:
                    cells = re.findall(r'<t[hd][^>]*>(.*?)</t[hd]>', r, flags=re.S)
                    cells = [re.sub(r'<[^>]+>', '', c).strip() for c in cells]
                    print(' | '.join(cells))
                print()
