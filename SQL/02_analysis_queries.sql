-- Category performance (catalogue and review indicators, not sales)
SELECT category, COUNT(DISTINCT product_id) AS products,
       ROUND(AVG(rating)::numeric, 2) AS avg_rating,
       ROUND(AVG(discount_percentage)::numeric, 2) AS avg_discount_pct
FROM product_master
GROUP BY category
ORDER BY products DESC;

-- Most reviewed products (rating_count is not unique customers)
SELECT product_id, product_name, rating, rating_count
FROM product_master
WHERE rating_count IS NOT NULL
ORDER BY rating_count DESC
LIMIT 20;

-- Discount outliers
SELECT product_id, product_name, actual_price, discounted_price, discount_percentage
FROM product_master
WHERE discount_percentage > 70
ORDER BY discount_percentage DESC;
