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
df = sqlio.read_sql_query("SELECT * FROM sandbox.curated_data", conn)

## New Dataframe
print("Creating new dataframe")
new_df = pd.DataFrame(columns=['time', 'equipment_id', 'latitude', 'longitude', 'elevation', 'speed'])

for ind in df.index:
    delta = df['sample_time'][ind]
    #print("OG Timestamp: " + str(df['time'][ind]) + "       Delta time: " + str(delta))
    lat = 0
    lon = 0
    ele = 0
    for i in range(0, 15):
        lat_col = "lat" + str(i)
        lon_col = "lon" + str(i)
        ele_col = "ele" + str(i)
        speed_col = "sp" + str(i)
        lat += df[lat_col][ind]
        lon += df[lon_col][ind]
        ele += df[ele_col][ind]
        new_df.loc[len(new_df)] = [df['time'][ind] + pd.Timedelta(seconds=delta*i), df['equipment_id'][ind], lat, lon, ele, df[speed_col][ind]]
        
#display(df)

## Save in PostgreSQL DB
print("Writing in DB")
table = 'sandbox.clean_data'
execute_values(conn, new_df, table)

print("Saving data in csv")
new_df.to_csv("clean_data.csv")
close_conn(conn)
