
WITH cleaned AS (
    SELECT
        product_id,
        INITCAP(TRIM(product_name)) AS product_name,
        INITCAP(TRIM(category)) AS category,
        LOWER(TRIM(brand)) AS brand,
        TRY_TO_DECIMAL(price, 10, 2) AS price,
        COALESCE(stock_quantity, 0) AS stock_quantity
    FROM raw.products
    WHERE product_id IS NOT NULL
)
SELECT * FROM cleaned;