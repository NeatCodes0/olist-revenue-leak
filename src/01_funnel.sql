-- Mart 1: The Order Funnel
-- We count how many orders actually reached each stage based on timestamps.

SELECT
    COUNT(ORDER_ID)                      AS ORDERS_PLACED,
    COUNT(ORDER_APPROVED_AT)             AS ORDERS_APPROVED,
    COUNT(ORDER_DELIVERED_CARRIER_DATE)  AS ORDERS_SHIPPED,
    COUNT(ORDER_DELIVERED_CUSTOMER_DATE) AS ORDERS_DELIVERED
FROM
    RAW_ORDERS;