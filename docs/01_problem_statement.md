# Why is revenue leaking even though we keep getting new customers?

## The situation

We are a Brazilian online marketplace. Order volume grew steadily from 2016 to 2018.
But almost every customer buys exactly once and never returns. Meanwhile, a
significant share of orders arrive later than the delivery date we promised, and
those orders tend to receive bad (1-star) reviews.

## The question

Is a bad first experience — late delivery leading to a bad review — the reason
customers don't come back? And how much revenue does that cost us per month?

## Why this matters (the decision)

Leadership has budget to spend on retention and logistics next quarter. They need
to choose between:
  (a) fixing delivery times in specific states and with specific sellers,
  (b) running recovery campaigns for customers who had a bad first experience,
  (c) seller quality programs.

This analysis produces a ranked target list and a dollar estimate so that
decision can be made with evidence rather than intuition.

## What "done" looks like

Someone who has never seen the data opens the app, reads it for five minutes,
and can say: "Fix deliveries in these 5 states and with these 20 sellers, and
we recover roughly $X per month."

## What we are NOT doing

- We are not predicting the future (no forecasting).
- We are not analyzing marketing spend or ad channels — we don't have that data.
- We are not measuring page views or carts — we only see an order once it is
  placed. Our "funnel" is the order's status journey, not the customer's
  click journey. We state this on the app's Methods page.
- We are not claiming proof of cause and effect. We show strong evidence,
  quantify uncertainty, and list the confounders we could not rule out.

## How this could go wrong (and how we prevent it)

1. We build charts nobody acts on.
   → Prevented by the "What done looks like" paragraph above.
2. We use the wrong customer identifier and think everyone is a repeat buyer
   when they are not.
   → Prevented by an explicit test in the data-quality suite.
3. The app looks polished but we cannot explain our own numbers under
   interview questioning.
   → Prevented by writing down every metric definition before computing it.
4. We never put a dollar figure on the problem, so the story is
   "here are some charts" instead of "here is the money."
   → Prevented by making "revenue at risk" a required output.