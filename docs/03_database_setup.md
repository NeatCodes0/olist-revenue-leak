# Milestone 3: Database Setup & Architecture

## Why DuckDB?
For this project, we are using DuckDB. 
- It is an in-process SQL OLAP database.
- It requires zero configuration or server setup.
- It reads CSV/Parquet instantly and executes analytical queries (window functions, CTEs) incredibly fast.
- It stores the entire database in a single file (data/olist.duckdb), making the project fully portable.

## The Raw Ingestion Layer
We wrote a Python script (src/build_db.py) to automate the ingestion. It reads all 9 CSVs from data/raw/ and creates corresponding tables inside the database.

### Naming Convention
To distinguish untouched raw data from our clean analytical models, we prefix all raw tables with raw_.
- olist_orders_dataset.csv becomes table raw_orders
- olist_customers_dataset.csv becomes table raw_customers

### How to rebuild the database
If the data is ever lost or the CSVs change, the database can be rebuilt from scratch by running:
    python src/build_db.py