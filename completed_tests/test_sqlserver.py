import pandas as pd
import pyodbc

conn = pyodbc.connect(
    "Driver={SQL Server};"
    "Server=XW3ZRBRW3\ROCKBLAST;"
    "Database=datasources;"
    "Trusted_Connection=yes;"
    )

df = pd.read_sql_query("SELECT * FROM equipment", conn)

print(df)
