"""Load locally generated product analytics into PostgreSQL.

Set DATABASE_URL, for example:
postgresql+psycopg2://user:password@localhost:5432/amazon_analytics
"""
import os
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine, text

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "Dataset" / "processed" / "product_master.csv"

def main():
    url = os.getenv("DATABASE_URL")
    if not url:
        raise SystemExit("Set DATABASE_URL before running this script.")
    if not CSV.exists():
        raise SystemExit(f"Processed dataset not found: {CSV}. Run Python/01_profile_and_clean.py first.")
    df = pd.read_csv(CSV)
    # Never load direct user identifiers into the analytical table.
    df = df.drop(columns=[c for c in ["user_id", "user_name", "username"] if c in df.columns])
    engine = create_engine(url, pool_pre_ping=True)
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS product_master (
                product_id TEXT PRIMARY KEY,
                product_name TEXT NOT NULL,
                category TEXT,
                discounted_price NUMERIC(12,2),
                actual_price NUMERIC(12,2),
                discount_percentage NUMERIC(6,2),
                rating NUMERIC(3,2),
                rating_count BIGINT,
                review_title TEXT,
                review_content TEXT
            )
        """))
        # Replace the snapshot atomically as one transaction.
        conn.execute(text("TRUNCATE TABLE product_master"))
        df.to_sql("product_master", conn, if_exists="append", index=False, method="multi", chunksize=500)
    print(f"Loaded {len(df):,} product rows into PostgreSQL.")

if __name__ == "__main__":
    main()
