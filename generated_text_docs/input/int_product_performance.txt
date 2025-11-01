## Overview  
This model aggregates order metrics per product from the staging orders table and enriches them with product metadata from the products table, producing a product‑level summary of sales performance.

## Tables Involved  
- `staging.stg_orders`: raw order line items.  
- `public.stg_products`: product catalog information.

## Columns Used  
- `staging.stg_orders.product_id`: identifier linking orders to products.  
- `staging.stg_orders.order_id`: used to count distinct orders.  
- `staging.stg_orders.quantity`: summed to compute total quantity sold.  
- `staging.stg_orders.net_amount`: summed to compute total revenue.  
- `staging.stg_orders.unit_price`: averaged to compute average selling price.  
- `public.stg_products.product_id`: primary key for product lookup.  
- `public.stg_products.product_name`: product name.  
- `public.stg_products.category`: product category.  
- `public.stg_products.brand`: product brand.  
- `product_orders.total_orders`: derived count of distinct orders per product.  
- `product_orders.total_quantity_sold`: derived sum of quantity per product.  
- `product_orders.total_revenue`: derived sum of net_amount per product.  
- `product_orders.avg_selling_price`: derived average unit_price per product.

## Logic Explanation  
1. **CTE `product_orders`** – Aggregates the `staging.stg_orders` table by `product_id`.  
   - `COUNT(DISTINCT order_id)` → `total_orders`.  
   - `SUM(quantity)` → `total_quantity_sold`.  
   - `SUM(net_amount)` → `total_revenue`.  
   - `AVG(unit_price)` → `avg_selling_price`.  
   No filters are applied; all order lines are considered.

2. **CTE `final`** – Performs a left join between the product catalog (`stg_products`) and the aggregated order metrics (`product_orders`) on `product_id`.  
   - All products are retained; products without orders receive NULLs for the aggregated columns.  
   - Selected columns include product metadata and the aggregated metrics.

3. **Final SELECT** – Returns all columns from the `final` CTE, yielding one row per product.

## Grain of Data  
The result set is at the **product level**; each row represents a unique `product_id` with its associated sales metrics.
