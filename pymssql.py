import pyodbc

# Connect to SQL Server (without specifying a database)
connectionString = "Driver={ODBC Driver 17 for SQL Server};UID=sa;PWD=examlyMssql@123;Server=localhost;Trusted_Connection=No;Persist Security Info=False;Encrypt=No"
conn = pyodbc.connect(connectionString, autocommit=True)  # Enable autocommit
cursor = conn.cursor()

print("LOGGING IN...")

# Database name
db_name = "TestDatabase"

# Step 1: Create the database (if not exists)
cursor.execute(f"IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = '{db_name}') CREATE DATABASE {db_name}")
print(f"Database '{db_name}' created successfully (if it didn't exist).")

# Close initial connection
cursor.close()
conn.close()

# Step 2: Connect to the new database
connectionString = f"Driver={{ODBC Driver 17 for SQL Server}};UID=sa;PWD=examlyMssql@123;Server=localhost;Database={db_name};Trusted_Connection=No;Persist Security Info=False;Encrypt=No"
conn = pyodbc.connect(connectionString)  # Connect to the new database
cursor = conn.cursor()

# Step 3: Verify connection by printing the current database
cursor.execute("SELECT DB_NAME()")
db = cursor.fetchone()[0]
print(f"Connected to database: {db}")

# Step 4: Create a new table (if not exists)
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

# Step 5: Insert test data
cursor.execute("INSERT INTO TestTable (Name, Age, City) VALUES (?, ?, ?)", ("Alice", 25, "New York"))
cursor.execute("INSERT INTO TestTable (Name, Age, City) VALUES (?, ?, ?)", ("Bob", 30, "Los Angeles"))
cursor.execute("INSERT INTO TestTable (Name, Age, City) VALUES (?, ?, ?)", ("Charlie", 28, "Chicago"))
conn.commit()
print("Test data inserted successfully.")

# Step 6: Fetch and print the data
cursor.execute("SELECT * FROM TestTable")
rows = cursor.fetchall()

print("\nRetrieved Data:")
for row in rows:
    print(f"ID: {row.ID}, Name: {row.Name}, Age: {row.Age}, City: {row.City}")

# Close connection
cursor.close()
conn.close()