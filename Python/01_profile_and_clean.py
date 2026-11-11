from pathlib import Path
import re
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "Dataset" / "raw" / "amazon.csv"
OUT = ROOT / "Dataset" / "processed"

def number(x):
    if pd.isna(x): return float("nan")
    s = re.sub(r"[^0-9.]", "", str(x).replace(",", ""))
    try: return float(s) if s else float("nan")
    except ValueError: return float("nan")

def clean(df):
    df = df.copy()
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    for col in ["discounted_price", "actual_price", "discount_percentage", "rating", "rating_count"]:
        if col in df:
            df[col] = df[col].map(number)
    if "product_id" in df:
        df = df.drop_duplicates(subset=["product_id"], keep="first")
    return df.drop(columns=[c for c in ["user_id", "user_name", "username"] if c in df.columns])

if __name__ == "__main__":
    if not SOURCE.exists():
        raise SystemExit(f"Place the source CSV at {SOURCE}")
    OUT.mkdir(parents=True, exist_ok=True)
    raw = pd.read_csv(SOURCE)
    cleaned = clean(raw)
    cleaned.to_csv(OUT / "product_master.csv", index=False)
    audit = pd.DataFrame({"column": cleaned.columns, "missing_values": [cleaned[c].isna().sum() for c in cleaned.columns], "missing_pct": [cleaned[c].isna().mean()*100 for c in cleaned.columns]})
    audit.to_csv(OUT / "data_quality_audit.csv", index=False)
    print(f"Processed {len(raw):,} rows into {len(cleaned):,} unique products.")
