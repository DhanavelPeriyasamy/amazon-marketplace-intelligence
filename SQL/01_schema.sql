CREATE TABLE IF NOT EXISTS product_master (
    product_id TEXT PRIMARY KEY,
    product_name TEXT NOT NULL,
    category TEXT,
    discounted_price NUMERIC(12,2),
    actual_price NUMERIC(12,2),
    discount_percentage NUMERIC(6,2),
    rating NUMERIC(3,2),
    rating_count BIGINT,
    sentiment_score INTEGER,
    sentiment TEXT
);
