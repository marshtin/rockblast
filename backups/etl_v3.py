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
df = sqlio.read_sql_query("SELECT time, equipment_id, sample_time, latitudes, longitudes, elevations, speeds FROM raw_data.shift_gps", conn)

print("Splitting geography data")
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

## Split speeds
df[['sp0','sp1','sp2','sp3','sp4','sp5','sp6','sp7','sp8','sp9','sp10','sp11','sp12','sp13','sp14','sp15']] = df['speeds'].str.split(',', expand=True) 
df = df.dropna(how='any',axis=0)
df = df.drop('speeds', axis=1)

print("Converting data types")
convert_dict = {'lat0': int,
                'lat1': int,
                'lat2': int,
                'lat3': int,
                'lat4': int,
                'lat5': int,
                'lat6': int,
                'lat7': int,
                'lat8': int,
                'lat9': int,
                'lat10': int,
                'lat11': int,
                'lat12': int,
                'lat13': int,
                'lat14': int,
                'lat15': int,
                'lon0': int,
                'lon1': int,
                'lon2': int,
                'lon3': int,
                'lon4': int,
                'lon5': int,
                'lon6': int,
                'lon7': int,
                'lon8': int,
                'lon9': int,
                'lon10': int,
                'lon11': int,
                'lon12': int,
                'lon13': int,
                'lon14': int,
                'lon15': int,
                'ele0': int,
                'ele1': int,
                'ele2': int,
                'ele3': int,
                'ele4': int,
                'ele5': int,
                'ele6': int,
                'ele7': int,
                'ele8': int,
                'ele9': int,
                'ele10': int,
                'ele11': int,
                'ele12': int,
                'ele13': int,
                'ele14': int,
                'ele15': int,
                'sp0': int,
                'sp1': int,
                'sp2': int,
                'sp3': int,
                'sp4': int,
                'sp5': int,
                'sp6': int,
                'sp7': int,
                'sp8': int,
                'sp9': int,
                'sp10': int,
                'sp11': int,
                'sp12': int,
                'sp13': int,
                'sp14': int,
                'sp15': int
                }

lat_lon_list = ['lat0',
                'lat1',
                'lat2',
                'lat3',
                'lat4',
                'lat5',
                'lat6',
                'lat7',
                'lat8',
                'lat9',
                'lat10',
                'lat11',
                'lat12',
                'lat13',
                'lat14',
                'lat15',
                'lon0',
                'lon1',
                'lon2',
                'lon3',
                'lon4',
                'lon5',
                'lon6',
                'lon7',
                'lon8',
                'lon9',
                'lon10',
                'lon11',
                'lon12',
                'lon13',
                'lon14',
                'lon15'
                ]

ele_list = ['ele0',
            'ele1',
            'ele2',
            'ele3',
            'ele4',
            'ele5',
            'ele6',
            'ele7',
            'ele8',
            'ele9',
            'ele10',
            'ele11',
            'ele12',
            'ele13',
            'ele14',
            'ele15'
            ]

df = df.astype(convert_dict)

## Fix geo data
print("Fixing geo data")
for col in lat_lon_list:
    df[col] = df[col]/(60*60*1000)

for col in ele_list:
    df[col] = df[col]/100

#display(df)

## Save in PostgreSQL DB
print("Writing in DB")
table = 'sandbox.curated_data'
execute_values(conn, df, table)

print("Saving data in csv")
df.to_csv("curated_data.csv")
close_conn(conn)
