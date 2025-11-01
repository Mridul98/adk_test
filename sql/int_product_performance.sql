WITH product_orders AS (
    SELECT
        s.product_id,
        COUNT(DISTINCT s.order_id) AS total_orders,
        SUM(s.quantity) AS total_quantity_sold,
        SUM(s.net_amount) AS total_revenue,
        AVG(s.unit_price) AS avg_selling_price
    FROM staging.stg_orders AS s
    GROUP BY s.product_id
),
final AS (
    SELECT
        p.product_id,
        p.product_name,
        p.category,
        p.brand,
        po.total_orders,
        po.total_quantity_sold,
        po.total_revenue,
        po.avg_selling_price
    FROM {{ ref('stg_products') }} AS p
    LEFT JOIN product_orders AS po
        ON p.product_id = po.product_id
)
SELECT * FROM final;