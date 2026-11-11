CREATE OR REPLACE VIEW category_intelligence AS
SELECT category, COUNT(DISTINCT product_id) AS product_count,
       AVG(rating) AS average_rating,
       AVG(discount_percentage) AS average_discount_pct
FROM product_master
GROUP BY category;

CREATE OR REPLACE VIEW product_value_signals AS
SELECT product_id, product_name, category, rating, rating_count,
       discount_percentage,
       CASE WHEN rating IS NOT NULL AND discount_percentage IS NOT NULL
            THEN (rating / 5.0) * (1.0 + discount_percentage / 100.0)
            ELSE NULL END AS heuristic_value_index
FROM product_master;
