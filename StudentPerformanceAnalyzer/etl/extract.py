import pandas as pd

def extract(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath, parse_dates=["exam_date"])
    print(f"[Extract] Loaded {len(df)} rows from {filepath}")
    return df