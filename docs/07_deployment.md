# Milestone 7: Deployment

## Objective
Deploy the Streamlit application to the public internet so that stakeholders and recruiters can access the interactive dashboard without needing to set up a local environment.

## Architecture & Hosting
- **Platform:** Streamlit Community Cloud (Free tier).
- **Source Control:** GitHub (`NeatCodes0/olist-revenue-leak`).
- **CI/CD:** Streamlit Cloud is configured to automatically pull from the `main` branch. Any future `git push` to `main` will automatically trigger a rebuild and update the live app.

## The Deployment Process
1. Connected Streamlit Community Cloud to the GitHub account.
2. Selected the `olist-revenue-leak` repository, the `main` branch, and `app.py` as the main file path.
3. Streamlit Cloud automatically reads `requirements.txt` to install dependencies.

## Troubleshooting: The `requirements.txt` Pitfall
During the initial deployment, the build failed with a `pywinpty` installation error. 

**Root Cause:** Running `pip freeze > requirements.txt` on a local Windows machine captures OS-specific packages (like `pywinpty`) that cannot be built on Streamlit's Linux-based servers.
**Solution:** We replaced the entire `requirements.txt` with only the strictly necessary top-level packages, letting Streamlit's environment resolve the correct Linux-compatible versions.

**Current `requirements.txt`:**
streamlit
pandas
duckdb
plotly

## Handling the Database
Because `.duckdb` files are binary and can be locked during operation, we included the locally built database file in the GitHub repository. Streamlit Cloud reads this file directly in read-only mode (`read_only=True`). 
*(Note: If the raw data updates, the database must be rebuilt locally and pushed to GitHub).*

## Live Application
- **URL:** [https://olist-revenue-leak-kt3gon3jagfsclsymh7r3c.streamlit.app/](https://olist-revenue-leak-kt3gon3jagfsclsymh7r3c.streamlit.app/)
- **Security:** The app is configured to run in `read_only=True` mode to prevent end-users from locking or corrupting the database.