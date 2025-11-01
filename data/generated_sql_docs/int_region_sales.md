## Overview  
This model aggregates sales performance by region and product category on a monthly basis, providing total sales, order counts, and unique customer counts.

## Tables Involved  
- `staging.stg_orders`: source of order transactions.  
- `staging.stg_products`: source of product details.  
- `staging.stg_customersAS`: source of customer details.

## Columns Used  
- `staging.stg_orders.order_id`: unique identifier for each order.  
- `staging.stg_orders.order_date`: date the order was placed.  
- `staging.stg_orders.net_amount`: monetary value of the order.  
- `staging.stg_orders.product_id`: foreign key to product.  
- `staging.stg_orders.customer_id`: foreign key to customer.  
- `staging.stg_products.product_id`: primary key of product.  
- `staging.stg_products.category`: product category.  
- `staging.stg_customersAS.customer_id`: primary key of customer.  
- `staging.stg_customersAS.region`: geographic region of the customer.  
- `staging.stg_orders.month` (derived): `DATE_TRUNC('month', s.order_date)`.  
- `regional_sales.total_sales` (derived): `SUM(s.net_amount)`.  
- `regional_sales.total_orders` (derived): `COUNT(DISTINCT s.order_id)`.  
- `regional_sales.unique_customers` (derived): `COUNT(DISTINCT s.customer_id)`.

## Logic Explanation  
1. **CTE `regional_sales`**  
   - **Joins**:  
     - `stg_orders` joined to `stg_products` on `product_id`.  
     - `stg_orders` joined to `stg_customersAS` on `customer_id`.  
   - **Derived column**: `month` is the first day of the month of each order date.  
   - **Aggregations**:  
     - `total_sales`: sum of `net_amount` per group.  
     - `total_orders`: count of distinct `order_id` per group.  
     - `unique_customers`: count of distinct `customer_id` per group.  
   - **Grouping**: by `region`, `category`, and `month`.  
2. **Final SELECT** returns all columns from the CTE, providing a monthly snapshot of sales metrics per region and category.

## Grain of Data  
The result set is at the monthly level, aggregated by customer region and product category.
