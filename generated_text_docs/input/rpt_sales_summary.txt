## Overview  
This model aggregates daily order amounts by region and product category, then computes monthly totals, active sales days, and month‑over‑month growth percentages for each region‑category pair.

## Tables Involved  
- **staging.stg_orders**: source of order details.  
- **raw.products**: source of product categories.  
- **raw.customers**: source of customer regions.

## Columns Used  
- **staging.stg_orders**:  
  - `product_id` – identifier for the purchased product.  
  - `customer_id` – identifier for the purchasing customer.  
  - `order_date` – date of the order.  
  - `net_amount` – monetary value of the order.  
- **raw.products**:  
  - `product_id` – identifier for the product.  
  - `category` – product category.  
- **raw.customers**:  
  - `customer_id` – identifier for the customer.  
  - `region` – geographic region of the customer.

## Logic Explanation  
1. **CTE `base`** – Joins orders with products and customers to attach `region` and `category` to each order. It groups by `region`, `category`, and `order_date` to calculate `daily_sales` (sum of `net_amount` per day).  
2. **CTE `monthly_aggregates`** – Uses `base` to aggregate daily sales into monthly totals. `DATE_TRUNC('month', order_date)` creates a `month` key. It sums `daily_sales` to get `total_monthly_sales` and counts distinct order dates to determine `active_days`.  
3. **CTE `yoy_growth`** – Adds month‑over‑month growth metrics. For each `region`/`category` partition, it uses a windowed `LAG` on `total_monthly_sales` to fetch the previous month’s sales (`prev_month_sales`). It then calculates `month_over_month_growth_pct` as the percentage change relative to the previous month, rounding to two decimals; if the previous month’s sales are zero or null, the growth is set to `NULL`.  
4. **Final SELECT** – Projects the calculated fields and orders the result by `region`, `category`, and `month`.

## Grain of Data  
The output is at the monthly level per `region` and `category` (one row per region‑category‑month combination).
