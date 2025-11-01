WITH base AS (
    SELECT
        c.customer_id,
        c.first_name,
        c.last_name,
        c.region,
        i.total_spent,
        i.total_orders,
        i.avg_order_value,
        CASE
            WHEN i.total_spent >= 10000 THEN 'Platinum'
            WHEN i.total_spent BETWEEN 5000 AND 9999 THEN 'Gold'
            WHEN i.total_spent BETWEEN 1000 AND 4999 THEN 'Silver'
            ELSE 'Bronze'
        END AS customer_segment
    FROM intermediate.int_customer_metricsAS i
    JOIN {{ staging.stg_customers }} AS c
        ON i.customer_id = c.customer_id
)
SELECT
    region,
    customer_segment,
    COUNT(DISTINCT customer_id) AS num_customers,
    ROUND(AVG(total_spent), 2) AS avg_ltv,
    ROUND(AVG(total_orders), 2) AS avg_orders
FROM base
GROUP BY 1, 2
ORDER BY region, avg_ltv DESC;
