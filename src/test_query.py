import duckdb

con = duckdb.connect("data/olist.duckdb")

# Test 1: How many total "customer_id" records are there? (One per order)
total_ids = con.execute("SELECT COUNT(customer_id) AS count FROM raw_customers").fetchone()[0]

# Test 2: How many ACTUAL unique people are there? (customer_unique_id)
unique_people = con.execute("SELECT COUNT(DISTINCT customer_unique_id) AS count FROM raw_customers").fetchone()[0]

print(f"Total customer_id records (orders): {total_ids:,}")
print(f"Total unique people (customer_unique_id): {unique_people:,}")