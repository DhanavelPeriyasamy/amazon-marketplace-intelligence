# Methodology

1. Standardise column names and parse currency/percentage values.
2. Deduplicate product records by product_id, keeping the first observed row.
3. Exclude user_id and user_name from generated analytics outputs.
4. Calculate category-level product counts, average rating and average discount.
5. Apply a transparent keyword sentiment score to available review title/body text.

## Limitations
- Snapshot data does not provide transaction-level sales or revenue.
- rating_count is not a count of unique customers.
- Keyword sentiment is a simple heuristic and may miss negation, sarcasm and context.
- A discount-based value index is a descriptive heuristic, not a recommendation guarantee.
