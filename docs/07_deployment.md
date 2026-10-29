# Milestone 7: Deployment

## Objective
Deploy the Streamlit application to the public internet so that stakeholders and recruiters can access the interactive dashboard without needing to set up a local environment.

## Architecture & Hosting
- **Platform:** Streamlit Community Cloud (Free tier).
- **Source Control:** GitHub (`NeatCodes0/olist-revenue-leak`).
- **CI/CD:** Streamlit Cloud is configured to automatically pull from the `main` branch. Any future `git push` to `main` will automatically trigger a rebuild and update the live app.

## Deployment Steps
1. Connected Streamlit Community Cloud to the GitHub account.
2. Selected the `olist-revenue-leak` repository and the `main` branch.
3. Set the main file path to `app.py`.
4. Streamlit Cloud automatically reads `requirements.txt` to install dependencies (Pandas, DuckDB, Plotly, Streamlit).

## Handling the Database
Because `.duckdb` files are binary and can be locked during operation, we included the locally built database file in the GitHub repository. Streamlit Cloud reads this file directly in read-only mode (`read_only=True`). 
*(Note: If the raw data updates, the database must be rebuilt locally and pushed to GitHub).*

## Live Application
- **URL:** [Insert your live Streamlit URL here]
- **Security:** The app is configured to run in `read_only=True` mode to prevent end-users from locking or corrupting the database.