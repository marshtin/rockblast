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
df = sqlio.read_sql_query("SELECT time, equipment_id, type, name, type_id, type_name, latitude, longitude, elevation, speed from sandbox.gps_c56 AS gps JOIN sandbox.equipment_clean AS eq ON gps.equipment_id = eq.id", conn)
display(df)

## Save in PostgreSQL DB
print("Writing in DB")
table = 'sandbox.fleet'
execute_values(conn, df, table)

#print("Saving data in csv")
#df.to_csv("fleet.csv")
close_conn(conn)
