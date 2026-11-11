# Power BI model and DAX

## Model
Use `product_master` as the product-level fact-like table. The dataset is a catalogue snapshot, not a transaction fact table. Avoid revenue, units-sold, inventory or time-intelligence measures unless a separate transactional dataset is introduced.

## Suggested measures
```DAX
Product Count = DISTINCTCOUNT(product_master[product_id])

Average Rating = AVERAGE(product_master[rating])

Average Discount % = AVERAGE(product_master[discount_percentage])

Reviewed Product Count =
CALCULATE(
    DISTINCTCOUNT(product_master[product_id]),
    FILTER(product_master, NOT ISBLANK(product_master[rating_count]))
)

High Rated Products =
CALCULATE(
    [Product Count],
    FILTER(product_master, product_master[rating] >= 4)
)
```

## Suggested report pages
1. Executive overview — product count, average rating, average discount, category distribution.
2. Pricing intelligence — actual vs discounted price, discount bands and outliers.
3. Customer voice — rating distribution and heuristic sentiment.
4. Product explorer — category and product drill-through.

Use clear labels that rating counts are platform-provided review counts, not unique customers.
