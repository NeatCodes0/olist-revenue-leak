-- Mart 4: Revenue at Risk
-- Goal: Calculate the total revenue tied to customers who had a bad first experience and never returned.

WITH CUSTOMER_ORDERS AS (
    SELECT
        C.CUSTOMER_UNIQUE_ID,
        O.ORDER_ID,
        O.ORDER_PURCHASE_TIMESTAMP,
 
        -- Calculate if the order was late
        CASE
            WHEN DATEDIFF('day', O.ORDER_ESTIMATED_DELIVERY_DATE, O.ORDER_DELIVERED_CUSTOMER_DATE) > 0 THEN
                1
            ELSE
                0
        END                                                                                           AS WAS_LATE,
 
        -- Rank the orders for each customer
        ROW_NUMBER() OVER (PARTITION BY C.CUSTOMER_UNIQUE_ID ORDER BY O.ORDER_PURCHASE_TIMESTAMP ASC) AS ORDER_SEQ
    FROM
        RAW_ORDERS    O
        JOIN RAW_CUSTOMERS C
        ON O.CUSTOMER_ID = C.CUSTOMER_ID
    WHERE
        O.ORDER_STATUS = 'delivered'
), FIRST_ORDER_REVIEWS AS (
    SELECT
        ORDER_ID,
        REVIEW_SCORE
    FROM
        RAW_ORDER_REVIEWS
),
 -- Bring it all together at the customer level
CUSTOMER_SUMMARY AS (
    SELECT
        CO.CUSTOMER_UNIQUE_ID,
        COUNT(CO.ORDER_ID)    AS TOTAL_LIFETIME_ORDERS,
        MAX(
            CASE
                WHEN CO.ORDER_SEQ = 1 THEN
                    CO.WAS_LATE
                ELSE
                    0
            END)              AS FIRST_ORDER_WAS_LATE,
        MAX(
            CASE
                WHEN CO.ORDER_SEQ = 1 THEN
                    R.REVIEW_SCORE
                ELSE
                    NULL
            END)              AS FIRST_ORDER_REVIEW,
 
        -- We need the order_id of the first order to calculate its value
        MAX(
            CASE
                WHEN CO.ORDER_SEQ = 1 THEN
                    CO.ORDER_ID
                ELSE
                    NULL
            END)              AS FIRST_ORDER_ID
    FROM
        CUSTOMER_ORDERS     CO
        LEFT JOIN FIRST_ORDER_REVIEWS R
        ON CO.ORDER_ID = R.ORDER_ID
    GROUP BY
        1
),
 -- Get the revenue for the first order
ORDER_REVENUE AS (
    SELECT
        ORDER_ID,
        SUM(PAYMENT_VALUE) AS ORDER_VALUE
    FROM
        RAW_ORDER_PAYMENTS
    GROUP BY
        1
)
SELECT
    COUNT(CS.CUSTOMER_UNIQUE_ID)   AS LOST_CUSTOMERS,
    ROUND(SUM(ORV.ORDER_VALUE), 2) AS TOTAL_REVENUE_AT_RISK
FROM
    CUSTOMER_SUMMARY CS
    LEFT JOIN ORDER_REVENUE ORV
    ON CS.FIRST_ORDER_ID = ORV.ORDER_ID
WHERE
    CS.TOTAL_LIFETIME_ORDERS = 1 -- They never bought again
    AND (CS.FIRST_ORDER_WAS_LATE = 1
    OR CS.FIRST_ORDER_REVIEW = 1);

-- They had a bad first experience