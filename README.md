# Olist Revenue Leak Analysis

## Executive Summary
Olist (a Brazilian e-commerce marketplace) experienced rapid order volume growth between 2016 and 2018. However, top-line revenue growth masked a critical structural flaw: the repeat purchase rate was under 3%.

This project is an end-to-end data analysis that investigates why customers are not returning, quantifies the financial impact of a poor first experience, and provides a self-serve dashboard for business stakeholders.

**Live Dashboard:** [https://olist-revenue-leak-kt3gon3jagfsclsymh7r3c.streamlit.app/](https://olist-revenue-leak-kt3gon3jagfsclsymh7r3c.streamlit.app/)

## Business Problem
Initial exploration revealed a 97% delivery success rate, eliminating logistics failure as the primary churn driver. However, deeper analysis into delivery timestamps and review scores showed that when a delivery is late, the customer experience collapses.

This project answers three questions:
1. What is the operational impact of late deliveries on customer satisfaction?
2. Does a bad first experience suppress repeat purchases?
3. How much revenue is currently at risk due to these lost customers?

## Key Findings
- **The Review Crash:** On-time orders average a 4.29 review score. Late orders crash to 2.27, with over 52% of late orders receiving a 1-star review.
- **The Retention Gap:** Customers who receive a late first order only return at a 2.55% rate, compared to 3.03% for on-time orders.
- **Revenue at Risk:** An estimated 11,735 customers churned due to a bad first experience (late delivery or 1-star review). The total revenue at risk from these lost customers is R$ 2,210,179.89 (Brazilian Reais).

## Technical Stack & Architecture
- **Data Ingestion:** Python (Pandas) & Kaggle CLI
- **Data Warehouse:** DuckDB (In-process OLAP database)
- **Data Modeling:** Advanced SQL (CTEs, Window Functions, Date Math)
- **Frontend:** Streamlit
- **Visualization:** Plotly Express
- **Deployment:** Streamlit Community Cloud
- **Documentation:** Markdown

### Project Structure
```text
olist-revenue-leak/
│
├── data/                  # DuckDB file and raw CSVs (gitignored)
├── docs/                  # Markdown documentation for each milestone
├── src/                   # Python scripts and SQL analytics models
│   ├── 01_funnel.sql      # Mart 1: Order status funnel
│   ├── 02_lateness.sql    # Mart 2: Delivery delays vs. reviews
│   ├── 03_retention.sql   # Mart 3: First order experience vs. retention
│   ├── 04_revenue_at_risk.sql # Mart 4: Financial impact
│   ├── build_db.py        # Ingests CSVs into DuckDB
│   └── run_sql.py         # CLI tool to execute SQL files
├── app.py                 # Streamlit dashboard
├── requirements.txt       # Python dependencies
└── README.md
```

## Local Setup Instructions

To run this project locally, follow these steps:

### 1. Clone the Repository
```bash
git clone https://github.com/NeatCodes0/olist-revenue-leak.git
cd olist-revenue-leak
```

### 2. Set Up the Environment
Create a virtual environment and install the required dependencies:
```bash
python -m venv .venv
# On Windows use: .venv\Scripts\activate
# On Mac/Linux use: source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Data Acquisition
Download the [Olist Dataset from Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) and place the 9 CSV files into the `data/raw/` directory.

### 4. Build the Database
Execute the Python script to ingest the raw CSVs into the DuckDB database file:
```bash
python src/build_db.py
```

### 5. Launch the Application
Start the Streamlit server to view the dashboard locally:
```bash
streamlit run app.py
```

## Documentation
Detailed methodology, metric definitions, and SQL logic are documented in the `docs/` folder:
- [Milestone 1: Problem Formulation](docs/01_problem_statement.md)
- [Milestone 2: Data Acquisition](docs/02_data_acquisition.md)
- [Milestone 3: Database Setup](docs/03_database_setup.md)
- [Milestone 4: Analytics Models](docs/04_analytics_models.md)
- [Milestone 5: Revenue at Risk](docs/05_revenue_at_risk.md)
- [Milestone 6: Streamlit App](docs/06_streamlit_app.md)
- [Milestone 7: Deployment](docs/07_deployment.md)

---
*Developed as a professional Data Analyst portfolio project.*