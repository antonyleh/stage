import sys
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd
from pathlib import Path

CLEAN = Path(r'c:\Users\lehmanna\Desktop\stage\projet\data\cln1\Clean')
for name in ['Comportement/semainier.parquet', 'Comportement/journalier.parquet']:
    df = pd.read_parquet(CLEAN / name)
    print(f'===== {name} =====')
    print(f'shape: {df.shape}, logements: {df["CODELIEU"].nunique() if "CODELIEU" in df else "?"}')
    print('colonnes:', list(df.columns))
    print(df.head(8).to_string())
    print()
