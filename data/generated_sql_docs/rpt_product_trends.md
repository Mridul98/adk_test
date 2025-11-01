## Overview  
This model calculates the monthly total sales for each product and the month‑over‑month growth percentage, providing a view of sales performance and growth trends at the product level.

## Tables Involved  
- `staging.stg_orders`: Stores individual order records.  
- `staging.stg_products`: Stores product catalog information.

## Columns Used  
- `staging.stg_orders.order_date` – Date of the order.  
- `staging.stg_orders.net_amount` – Net amount of the order.  
- `staging.stg_orders.product_id` – Foreign key to the product.  
- `staging.stg_products.product_id` – Primary key of the product.  
- `staging.stg_products.product_name` – Name of the product.  
- `staging.stg_products.category` – Category of the product.  
- `staging.stg_orders.product_id` (joined) – Join key.  
- `staging.stg_orders.order_date` (used in DATE_TRUNC) – Derived column `month`.  
- `staging.stg_orders.net_amount` (aggregated) – Derived column `total_sales`.  
- `product_monthly.prev_month_sales` – Lagged sales value.  
- `product_monthly.growth_pct` – Calculated growth percentage.

## Logic Explanation  
1. **product_monthly CTE** – Joins `stg_orders` with `stg_products` on `product_id`. For each product and month (truncated to month start), it sums `net_amount` to produce `total_sales`.  
2. **growth CTE** – For each product, orders the monthly records chronologically and uses `LAG` to retrieve the previous month’s `total_sales` (`prev_month_sales`). It then calculates `growth_pct` as the percentage change from the previous month, rounding to two decimal places; if the previous month’s sales are zero or null, `growth_pct` is set to null.  
3. **Final SELECT** – Projects the product identifiers, names, category, month, total sales, and growth percentage from the `growth` CTE, ordering the results by month descending and then by total sales descending.

## Grain of Data  
The result set is at the **product‑by‑month** granularity.
