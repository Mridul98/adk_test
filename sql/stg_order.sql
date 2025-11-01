WITH cleaned_orders AS (
    SELECT
        o.order_id,
        o.customer_id,
        TRY_TO_DATE(o.order_date) AS order_date,
        LOWER(TRIM(o.order_status)) AS order_status,
        oi.product_id,
        oi.quantity,
        oi.unit_price,
        oi.discount,
        (oi.quantity * oi.unit_price) - COALESCE(oi.discount, 0) AS net_amount
    FROM raw.orders AS o
    JOIN raw.order_items AS oi
        ON o.order_id = oi.order_id
    WHERE o.order_status IS NOT NULL
      AND TRY_TO_DATE(o.order_date) IS NOT NULL
)
SELECT
    order_id,
    customer_id,
    product_id,
    order_status,
    order_date,
    quantity,
    unit_price,
    discount,
    net_amount
FROM cleaned_orders;