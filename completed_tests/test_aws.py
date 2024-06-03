import psycopg2
import pandas as pd
import pandas.io.sql as sqlio
import sqlalchemy
from IPython.display import display
from config import config
import warnings
warnings.simplefilter(action='ignore', category=UserWarning)

def connect(): 
	""" Connect to the PostgreSQL database server """
	conn = None
	try: 
		# read connection parameters 
		# params = config()

		params = {"host": "rockblast-g4.cfwy4giwk9t5.sa-east-1.rds.amazonaws.com",
                          "database": "datasources",
                          "port": "5432",
                          "user": "uss_tei_g4",
                          "password": "uss_tei_g4"
                          }

		# connect to the PostgreSQL server 
		print('Connecting to the PostgreSQL database...') 
		conn = psycopg2.connect(**params) 

		print('Connected')

		return conn

	except (Exception, psycopg2.DatabaseError) as error: 
		print(error)
		

def close_conn(conn):
    if conn is not None: 
        conn.close()
        print('Database connection closed.') 

conn = connect()
cur = conn.cursor()
cur.execute('SELECT version()')
db_version = cur.fetchone()
print(db_version)

df = sqlio.read_sql_query("SELECT * FROM raw_data.equipment", conn)
display(df)
close_conn(conn)
