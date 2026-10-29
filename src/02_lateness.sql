-- Mart 2: Delivery Lateness & Review Scores
-- Goal: Does delivering an order late ruin the customer's review score?

WITH DELIVERED_ORDERS AS (
    SELECT
        ORDER_ID,
 
        -- Calculate days between estimated delivery and actual delivery
        -- Positive number = late. Negative = early.
        DATEDIFF('day', ORDER_ESTIMATED_DELIVERY_DATE, ORDER_DELIVERED_CUSTOMER_DATE) AS DELAY_DAYS
    FROM
        RAW_ORDERS
    WHERE
        ORDER_STATUS = 'delivered'
        AND ORDER_DELIVERED_CUSTOMER_DATE IS NOT NULL
), REVIEW_SCORES AS (
    SELECT
        ORDER_ID,
        REVIEW_SCORE
    FROM
        RAW_ORDER_REVIEWS
)
SELECT
    CASE
        WHEN DELAY_DAYS > 0 THEN
            '1. Late'
        ELSE
            '2. On Time or Early'
    END                              AS DELIVERY_STATUS,
    COUNT(O.ORDER_ID)                AS TOTAL_ORDERS,
 
    -- What is the average review score for these orders?
    ROUND(AVG(R.REVIEW_SCORE), 2)    AS AVG_REVIEW_SCORE,
 
    -- Calculate the % of 1-star reviews
    ROUND(100.0 * SUM(
        CASE
            WHEN R.REVIEW_SCORE = 1 THEN
                1
            ELSE
                0
        END) / COUNT(O.ORDER_ID), 2) AS PCT_1_STAR
FROM
    DELIVERED_ORDERS O
    LEFT JOIN REVIEW_SCORES R
    ON O.ORDER_ID = R.ORDER_ID
GROUP BY
    1
ORDER BY
    1;