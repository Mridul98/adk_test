WITH customer_orders AS (
    SELECT
        s.customer_id,
        COUNT(DISTINCT s.order_id) AS total_orders,
        SUM(s.net_amount) AS total_spent,
        AVG(s.net_amount) AS avg_order_value,
        MAX(s.order_date) AS last_order_date
    FROM staging.stg_orders AS s
    GROUP BY s.customer_id
),
joined_customers AS (
    SELECT
        c.customer_id,
        c.first_name,
        c.last_name,
        c.region,
        co.total_orders,
        co.total_spent,
        co.avg_order_value,
        co.last_order_date
    FROM raw.customers AS c
    LEFT JOIN customer_orders AS co
        ON c.customer_id = co.customer_id
)
SELECT
    customer_id,
    first_name,
    last_name,
    region,
    COALESCE(total_orders, 0) AS total_orders,
    COALESCE(total_spent, 0) AS total_spent,
    COALESCE(avg_order_value, 0) AS avg_order_value,
    last_order_date
FROM joined_customers;