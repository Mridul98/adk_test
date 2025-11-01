WITH regional_sales AS (
    SELECT
        c.region,
        p.category,
        DATE_TRUNC('month', s.order_date) AS month,
        SUM(s.net_amount) AS total_sales,
        COUNT(DISTINCT s.order_id) AS total_orders,
        COUNT(DISTINCT s.customer_id) AS unique_customers
    FROM staging.stg_orders AS s
    JOIN staging.stg_products AS p
        ON s.product_id = p.product_id
    JOIN staging.stg_customersAS c
        ON s.customer_id = c.customer_id
    GROUP BY 1, 2, 3
)
SELECT * FROM regional_sales;