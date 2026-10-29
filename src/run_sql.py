import duckdb
import sys
from pathlib import Path

def run_sql(filepath):
    con = duckdb.connect("data/olist.duckdb")
    sql = Path(filepath).read_text()
    
    print(f"Executing {filepath}...\n")
    # Execute the SQL and fetch the result as a pandas dataframe to print nicely
    result = con.execute(sql).fetchdf()
    print(result.to_string(index=False))
    con.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python src/run_sql.py path/to/file.sql")
        sys.exit(1)
    run_sql(sys.argv[1])