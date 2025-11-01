WITH product_monthly AS (
    SELECT
        p.product_id,
        p.product_name,
        p.category,
        DATE_TRUNC('month', s.order_date) AS month,
        SUM(s.net_amount) AS total_sales
    FROM staging.stg_orders AS s
    JOIN staging.stg_products AS p
        ON s.product_id = p.product_id
    GROUP BY 1, 2, 3, 4
),
growth AS (
    SELECT
        product_id,
        product_name,
        category,
        month,
        total_sales,
        LAG(total_sales) OVER (
            PARTITION BY product_id ORDER BY month
        ) AS prev_month_sales,
        CASE
            WHEN LAG(total_sales) OVER (
                PARTITION BY product_id ORDER BY month
            ) > 0 THEN
                ROUND(
                    (total_sales - LAG(total_sales) OVER (
                        PARTITION BY product_id ORDER BY month
                    )) / LAG(total_sales) OVER (
                        PARTITION BY product_id ORDER BY month
                    ) * 100,
                    2
                )
            ELSE NULL
        END AS growth_pct
    FROM product_monthly
)
SELECT
    product_id,
    product_name,
    category,
    month,
    total_sales,
    growth_pct
FROM growth
ORDER BY month DESC, total_sales DESC;