# Milestone 6: Streamlit Decision Surface

## Objective
Create a self-serve web application where business stakeholders (Growth and CX leads) can view the quantified revenue leak and identify which regions are driving the problem.

## Architecture
- **Frontend/Backend:** Streamlit (Python).
- **Data Layer:** The app connects directly to `data/olist.duckdb` using the `duckdb` Python package.
- **Interactivity:** Users can filter by State to see how the revenue leak changes geographically.

## Deployment
The app will be deployed for free using Streamlit Community Cloud.