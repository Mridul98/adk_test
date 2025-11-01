## Overview  
This model aggregates customer metrics by region and customer segment, producing counts of customers and average lifetime value (LTV) and order metrics for each segment.

## Tables Involved  
- `intermediate.int_customer_metricsAS`: Stores calculated customer metrics such as total spent, total orders, and average order value.  
- `staging.stg_customers`: Contains core customer demographic information including name and region.

## Columns Used  
- `intermediate.int_customer_metricsAS.customer_id` – Unique identifier for each customer.  
- `intermediate.int_customer_metricsAS.total_spent` – Total amount spent by the customer.  
- `intermediate.int_customer_metricsAS.total_orders` – Total number of orders placed by the customer.  
- `intermediate.int_customer_metricsAS.avg_order_value` – Average value per order for the customer.  
- `staging.stg_customers.customer_id` – Unique identifier for each customer.  
- `staging.stg_customers.first_name` – Customer’s first name.  
- `staging.stg_customers.last_name` – Customer’s last name.  
- `staging.stg_customers.region` – Geographic region of the customer.

## Logic Explanation  
1. **CTE `base`** – Joins `intermediate.int_customer_metricsAS` (`i`) with `staging.stg_customers` (`c`) on `customer_id`.  
   - Selects customer identifiers, names, region, and metric fields.  
   - Computes a `customer_segment` classification based on `total_spent` thresholds (Platinum, Gold, Silver, Bronze).  
2. **Final SELECT** – Aggregates the `base` CTE by `region` and `customer_segment`.  
   - `COUNT(DISTINCT customer_id)` yields the number of unique customers per segment.  
   - `AVG(total_spent)` and `AVG(total_orders)` provide average LTV and average orders, rounded to two decimal places.  
3. **Ordering** – Results are ordered first by `region` alphabetically, then by `avg_ltv` in descending order within each region.

## Grain of Data  
The output is aggregated at the **region × customer_segment** level, providing one row per unique combination of region and customer segment.
