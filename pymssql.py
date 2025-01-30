import pyodbc
connectionString = "Driver={ODBC Driver 17 for SQL Server};UID=sa;PWD=examlyMssql@123; server=localhost;Database=testDharan;Trusted_Connection=No;Persist Security Info=False;Encrypt=No"
conn = pyodbc.connect(connectionString)
cursor = conn.cursor()

# Step 1: Create a new table (if not exists)
cursor.execute("""
    IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'TestTable')
    BEGIN
        CREATE TABLE TestTable (
            ID INT IDENTITY(1,1) PRIMARY KEY,
            Name NVARCHAR(50),
            Age INT,
            City NVARCHAR(50)
        )
    END
""")
conn.commit()

print("Table created successfully (if it didn't exist).")

# Step 2: Insert test data
cursor.execute("INSERT INTO TestTable (Name, Age, City) VALUES (?, ?, ?)", ("Alice", 25, "New York"))
cursor.execute("INSERT INTO TestTable (Name, Age, City) VALUES (?, ?, ?)", ("Bob", 30, "Los Angeles"))
cursor.execute("INSERT INTO TestTable (Name, Age, City) VALUES (?, ?, ?)", ("Charlie", 28, "Chicago"))
conn.commit()

print("Test data inserted successfully.")

# Step 3: Fetch and print the data
cursor.execute("SELECT * FROM TestTable")
rows = cursor.fetchall()

print("\nRetrieved Data:")
for row in rows:
    print(f"ID: {row.ID}, Name: {row.Name}, Age: {row.Age}, City: {row.City}")

# Close connection
cursor.close()
conn.close()