WITH cleaned AS (
    SELECT
        customer_id,
        INITCAP(TRIM(first_name)) AS first_name,
        INITCAP(TRIM(last_name)) AS last_name,
        LOWER(email) AS email,
        INITCAP(TRIM(region)) AS region,
        TRY_TO_DATE(created_at) AS created_at,
        COALESCE(is_active, TRUE) AS is_active
    FROM raw.customers
    WHERE email LIKE '%@%'
)
SELECT * FROM cleaned;