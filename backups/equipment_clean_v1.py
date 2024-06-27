import pandas as pd
import pandas.io.sql as sqlio
import sqlalchemy
from IPython.display import display
from connect import *
import warnings
warnings.simplefilter(action='ignore', category=UserWarning)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

conn = connect()
cur = conn.cursor()
cur.execute('SELECT version()')
db_version = cur.fetchone()
print(db_version)

## Downloading data from AWS
print("Gathering data")
df = sqlio.read_sql_query("SELECT eq.id, eq.type, eq.name, eq.equipment_type_id AS type_id, en.name AS type_name FROM raw_data.equipment AS eq JOIN raw_data.enum_tables AS en ON CAST(eq.equipment_type_id AS varchar) = CAST(en.id AS varchar)", conn)
df.sort_values('id')
display(df)

## Save in PostgreSQL DB
print("Writing in DB")
table = 'sandbox.equipment_clean'
execute_values(conn, df, table)

print("Saving data in csv")
df.to_csv("equipment_full.csv")
close_conn(conn)
