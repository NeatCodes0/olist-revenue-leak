# Milestone 4: Analytics Models (SQL Marts)

In this milestone, we build the analytical layer of the database. Instead of writing one massive query, we build targeted "Marts" (tables/views designed to answer specific business questions).

## Mart 1: The Order Funnel (`01_funnel.sql`)
**Business Question:** How healthy is our operational pipeline? Where do orders drop off?
**Approach:** We use the `raw_orders` table to count how many orders successfully hit each milestone timestamp (`approved_at`, `delivered_carrier_date`, `delivered_customer_date`).
**Finding:** The operational funnel is highly efficient. 97% of all placed orders are successfully delivered to the customer. 

## Mart 2: Delivery Lateness vs. Reviews (`02_lateness.sql`)
**Business Question:** Does a late delivery actually cause bad review scores?
**Approach:** 
1. We filter for delivered orders.
2. We use `DATEDIFF` to calculate the gap between the `order_estimated_delivery_date` and the `order_delivered_customer_date`.
3. We use a `CASE WHEN` statement to bucket orders into "Late" (delay > 0 days) and "On Time".
4. We join this to the `raw_order_reviews` table to calculate the average review score and the percentage of 1-star reviews for each bucket.

## SQL Techniques Demonstrated
- **Common Table Expressions (CTEs):** Using `WITH ... AS (...)` to break down complex logic into readable steps.
- **Date Math:** `DATEDIFF('day', start_date, end_date)`.
- **Conditional Logic:** `CASE WHEN ... THEN ... ELSE ... END`.
- **Aggregations & Joins:** `LEFT JOIN` and `GROUP BY` with `AVG()` and `SUM()`.

### Mart 2 Results
- **On Time Orders:** Avg review score is 4.29, with 6.59% 1-star reviews.
- **Late Orders:** Avg review score plummets to 2.27, with 52.48% 1-star reviews.
- **Conclusion:** Late delivery is the single biggest driver of terrible customer experiences. Over half of late orders result in a 1-star review.

### Mart 3 Results
- Customers with a Late First Order: 2.55% repeat purchase rate.
- Customers with an On-Time First Order: 3.03% repeat purchase rate.
- **Conclusion:** While late deliveries hurt retention, the overall repeat purchase rate is shockingly low (~3%) across the entire platform. The business suffers from a structural retention issue, not just a logistics issue.