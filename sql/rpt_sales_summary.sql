WITH base AS (
    SELECT
        c.region,
        p.category,
        s.order_date,
        SUM(s.net_amount) AS daily_sales
    FROM staging.stg_orders AS s
    JOIN raw.products AS p
        ON s.product_id = p.product_id
    JOIN raw.customers AS c
        ON s.customer_id = c.customer_id
    GROUP BY 1, 2, 3
),
monthly_aggregates AS (
    SELECT
        region,
        category,
        DATE_TRUNC('month', order_date) AS month,
        SUM(daily_sales) AS total_monthly_sales,
        COUNT(DISTINCT DATE(order_date)) AS active_days
    FROM base
    GROUP BY 1, 2, 3
),
yoy_growth AS (
    SELECT
        region,
        category,
        month,
        total_monthly_sales,
        LAG(total_monthly_sales) OVER (
            PARTITION BY region, category
            ORDER BY month
        ) AS prev_month_sales,
        CASE
            WHEN LAG(total_monthly_sales) OVER (
                PARTITION BY region, category
                ORDER BY month
            ) > 0 THEN
                ROUND(
                    (total_monthly_sales - LAG(total_monthly_sales) OVER (
                        PARTITION BY region, category
                        ORDER BY month
                    )) / LAG(total_monthly_sales) OVER (
                        PARTITION BY region, category
                        ORDER BY month
                    ) * 100,
                    2
                )
            ELSE NULL
        END AS month_over_month_growth_pct
    FROM monthly_aggregates
)
SELECT
    region,
    category,
    month,
    total_monthly_sales,
    prev_month_sales,
    month_over_month_growth_pct,
    active_days
FROM yoy_growth
ORDER BY region, category, month;