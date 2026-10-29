# Milestone 5: Revenue at Risk

## The Business Question
How much money is the business losing because customers are having bad first experiences and never returning?

## Methodology
1. Identify every customer's first order.
2. Flag if that first order was a "Bad Experience" (delivered late OR received a 1-star review).
3. Filter for customers who never bought a second time.
4. Sum the total payment value (revenue) of these lost customers.

## Assumptions & Limitations
- We are assuming the revenue from their first order is the baseline. We cannot know exactly what they *would* have spent if they had returned, but we use their first order value as a conservative proxy for lost lifetime value.
- We are only analyzing delivered orders.

### Results
- **Lost Customers:** 11,735
- **Revenue at Risk (BRL):** 2,210,179.89
- **Conclusion:** A conservative estimate of $2.2M in lost lifetime value is tied directly to customers who had a late delivery or 1-star review on their first order and never returned.