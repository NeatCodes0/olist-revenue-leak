-- Mart 3: Retention & The First Order Experience
-- Goal: If a customer's FIRST order is late, are they less likely to buy again?

WITH ALL_DELIVERED_ORDERS AS (
    SELECT
        O.ORDER_ID,
        C.CUSTOMER_UNIQUE_ID,
        O.ORDER_PURCHASE_TIMESTAMP,
 
        -- Calculate if the order was late
        CASE
            WHEN DATEDIFF('day', O.ORDER_ESTIMATED_DELIVERY_DATE, O.ORDER_DELIVERED_CUSTOMER_DATE) > 0 THEN
                1
            ELSE
                0
        END                                                                                           AS WAS_LATE,
 
        -- Rank the orders for each customer based on date (1 = first order, 2 = second, etc.)
        ROW_NUMBER() OVER (PARTITION BY C.CUSTOMER_UNIQUE_ID ORDER BY O.ORDER_PURCHASE_TIMESTAMP ASC) AS ORDER_SEQ
    FROM
        RAW_ORDERS    O
        JOIN RAW_CUSTOMERS C
        ON O.CUSTOMER_ID = C.CUSTOMER_ID
    WHERE
        O.ORDER_STATUS = 'delivered'
), CUSTOMER_SUMMARY AS (
    SELECT
        CUSTOMER_UNIQUE_ID,
        COUNT(ORDER_ID)    AS TOTAL_LIFETIME_ORDERS,
 
        -- Check if their very first order (order_seq = 1) was late
        MAX(
            CASE
                WHEN ORDER_SEQ = 1 AND WAS_LATE = 1 THEN
                    1
                ELSE
                    0
            END)           AS FIRST_ORDER_WAS_LATE
    FROM
        ALL_DELIVERED_ORDERS
    GROUP BY
        1
)
SELECT
    CASE
        WHEN FIRST_ORDER_WAS_LATE = 1 THEN
            '1. First Order was Late'
        ELSE
            '2. First Order was On Time'
    END                                      AS FIRST_EXPERIENCE,
    COUNT(CUSTOMER_UNIQUE_ID)                AS TOTAL_CUSTOMERS,
 
    -- How many of these customers bought more than once?
    SUM(
        CASE
            WHEN TOTAL_LIFETIME_ORDERS > 1 THEN
                1
            ELSE
                0
        END)                                 AS CUSTOMERS_WHO_RETURNED,
 
    -- What is the repeat purchase rate as a percentage?
    ROUND(100.0 * SUM(
        CASE
            WHEN TOTAL_LIFETIME_ORDERS > 1 THEN
                1
            ELSE
                0
        END) / COUNT(CUSTOMER_UNIQUE_ID), 2) AS REPEAT_RATE_PCT
FROM
    CUSTOMER_SUMMARY
GROUP BY
    1
ORDER BY
    1;