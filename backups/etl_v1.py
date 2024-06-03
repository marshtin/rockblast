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

df = sqlio.read_sql_query("SELECT id, time, equipment_id, sample_time, latitudes, longitudes, elevations FROM raw_data.shift_gps", conn)

## Split latitudes
df[['lat0','lat1','lat2','lat3','lat4','lat5','lat6','lat7','lat8','lat9','lat10','lat11','lat12','lat13','lat14','lat15']] = df['latitudes'].str.split(',', expand=True) 
df = df.dropna(how='any',axis=0)
df = df.drop('latitudes', axis=1)

## Split longitudes
df[['lon0','lon1','lon2','lon3','lon4','lon5','lon6','lon7','lon8','lon9','lon10','lon11','lon12','lon13','lon14','lon15']] = df['longitudes'].str.split(',', expand=True) 
df = df.dropna(how='any',axis=0)
df = df.drop('longitudes', axis=1)

## Split elevations
df[['ele0','ele1','ele2','ele3','ele4','ele5','ele6','ele7','ele8','ele9','ele10','ele11','ele12','ele13','ele14','ele15']] = df['elevations'].str.split(',', expand=True) 
df = df.dropna(how='any',axis=0)
df = df.drop('elevations', axis=1)

display(df)
df.to_csv("etl_done")
close_conn(conn)
