import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('attendance.db')  # Update the path if your database is in a different location

# Create a cursor object
cursor = conn.cursor()

# Function to fetch and print data from a table
def fetch_data(table_name):
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    print(f"\nAdmin Details in {table_name}:")
    for row in rows:
        print(row)

# List of tables to fetch data from
tables = ["users"]  # Add more table names if you have more tables

for table in tables:
    fetch_data(table)

# Close the connection
conn.close()