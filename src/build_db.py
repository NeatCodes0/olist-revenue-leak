import duckdb
from pathlib import Path

# Set up paths
DB_PATH = "data/olist.duckdb"
RAW_DATA = "data/raw"

def build_database():
    print("Building DuckDB database...")
    
    # Connect to the database (this creates the file if it doesn't exist)
    con = duckdb.connect(DB_PATH)
    
    # Find all CSV files in the raw data folder
    csv_files = list(Path(RAW_DATA).glob("*.csv"))
    
    for file in csv_files:
        # Clean the table name (e.g., 'olist_orders_dataset.csv' -> 'raw_orders')
        table_name = file.stem.replace("olist_", "raw_").replace("_dataset", "")
        
        print(f"Loading {file.name} -> {table_name}")
        
        # Read the CSV and create a table in DuckDB
        con.execute(f"""
            CREATE OR REPLACE TABLE {table_name} AS 
            SELECT * FROM read_csv_auto('{file}')
        """)
    
    # Print a summary of what we just built
    print("\nDatabase built successfully! Tables created:")
    print(con.execute("SHOW TABLES").fetchdf())
    
    con.close()

if __name__ == "__main__":
    build_database()