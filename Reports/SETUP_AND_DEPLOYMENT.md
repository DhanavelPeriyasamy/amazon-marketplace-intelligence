# Local setup and database loading

## Python workflow

1. Put your licensed source CSV at `Dataset/raw/amazon.csv`.
2. Install dependencies from the repository root: `pip install -r requirements.txt`.
3. Run `python Python/01_profile_and_clean.py`.
4. Run `python Python/02_analyze_reviews.py`.
5. Start the dashboard: `streamlit run Streamlit/app.py`.

## PostgreSQL

Create a PostgreSQL database, set the `DATABASE_URL` environment variable, then run:

```bash
python Python/03_export_to_postgres.py
```

Example connection string:

```text
postgresql+psycopg2://username:password@localhost:5432/amazon_analytics
```

Never commit database passwords, access tokens, customer identifiers or private source datasets. The export script removes direct user identifiers and replaces the product snapshot table in a single database transaction.

## Streamlit Community Cloud

Select this repository, branch `main`, and main file `Streamlit/app.py`. The app uses CSV upload so the source file can remain private and local.
