# Milestone 2: Data Acquisition & Profiling

## The Data Source
We are using the Brazilian E-Commerce Public Dataset by Olist (available on Kaggle). 
It contains 100k anonymized orders from multiple marketplaces between 2016 and 2018.

## How we acquired it
We used the Kaggle CLI to pull the data directly into the environment to ensure reproducibility.
Commands used:
    $env:KAGGLE_API_TOKEN="[redacted]"
    kaggle datasets download -d olistbr/brazilian-ecommerce -p data/raw --unzip

## Data Profiling (Raw Row Counts)
Upon download, we verified the row counts to ensure data integrity. 

| File                             | Row Count (approx) | Description                      |
| :------------------------------- | :----------------- | :------------------------------- |
| olist_customers_dataset.csv      | 99,441             | Customer location and unique IDs |
| olist_orders_dataset.csv         | 99,441             | Order status and timestamps      |
| olist_order_items_dataset.csv    | 112,650            | Items purchased per order        |
| olist_order_payments_dataset.csv | 103,886            | Payment methods and values       |
| olist_order_reviews_dataset.csv  | 104,165*           | Customer satisfaction scores     |
| olist_products_dataset.csv       | 32,951             | Product attributes               |
| olist_sellers_dataset.csv        | 3,095              | Seller location                  |
| olist_geolocation_dataset.csv    | 1,000,163          | Zip code lat/long                |

*Note: The raw line count of reviews is slightly inflated due to multi-line text in review comments.*

## Key Data Quirks Identified
1. The Customer ID Trap: customer_id is unique per order. customer_unique_id is unique per person. We must use customer_unique_id for any retention/repeat-purchase analysis.
2. Order-to-Customer Ratio: There are 99,441 orders and ~96k unique customers. This immediately validates our hypothesis that the marketplace suffers from severe retention issues.