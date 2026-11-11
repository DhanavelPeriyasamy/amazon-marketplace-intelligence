# Amazon Marketplace Intelligence

An end-to-end marketplace analytics project using Python, SQL and Streamlit. It explores product catalogue structure, pricing and discounts, rating distributions, review sentiment and product-level value signals.

## Live dashboard
Deploy this repository with Streamlit Community Cloud using **Streamlit/app.py** as the main file. The app accepts the source CSV through its sidebar uploader, so the dataset does not need to be committed to this public repository.

## Features
- Interactive KPI overview and category analysis
- Discount and price distribution analysis
- Product ratings and review-count exploration
- Lightweight review sentiment scoring
- Searchable product explorer with CSV export
- Python data-quality and cleaning pipeline
- PostgreSQL schema, analytical SQL and views
- Automated tests

## Run locally
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run Streamlit/app.py
```

Upload your permitted copy of the dataset in the app sidebar. Expected Amazon catalogue columns include `product_id`, `product_name`, `category`, `discounted_price`, `actual_price`, `discount_percentage`, `rating`, `rating_count`, `review_title` and `review_content`.

## Run tests
```bash
pytest -q
```

## Dataset and privacy
The raw CSV and processed CSV exports are intentionally excluded from this public repository. Confirm the dataset licence and redistribution rights before sharing it. The pipeline does not export `user_id` or `user_name` into processed analytics files. Do not upload personal identifiers or private customer information.

## Important analytical limitations
This dataset is a product catalogue and review snapshot, not transaction-level sales data. It cannot support claims about revenue, profit, units sold, inventory movement or sales trends over time. Review counts are not unique customer counts. Sentiment is a heuristic text score, not a validated machine-learning model.

## Project structure
- `Streamlit/` — interactive dashboard
- `Python/` — cleaning, profiling and sentiment pipeline
- `SQL/` — PostgreSQL schema, views and analytical queries
- `PowerBI/` — data model and DAX implementation notes
- `Reports/` — methodology, business questions and data-quality notes
- `tests/` — automated tests

## Author
Dhanavel Periyasamy
