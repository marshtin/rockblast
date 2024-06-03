import psycopg2
import psycopg2.extras as extras
import numpy as np
from config import config
import warnings
warnings.simplefilter(action='ignore', category=UserWarning)

def connect(): 
	conn = None
	try: 
		# read connection parameters 
		params = config()

		#params = {"host": "rockblast-g4.cfwy4giwk9t5.sa-east-1.rds.amazonaws.com",
                #          "database": "datasources",
                #          "port": "5432",
                #          "user": "uss_tei_g4",
                #          "password": "uss_tei_g4"
                #          }

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

def execute_values(conn, df, table):
    # Create a list of tupples from the dataframe values
    tuples = [tuple(x) for x in df.to_numpy()]
    # Comma-separated dataframe columns
    cols = ','.join(list(df.columns))
    # SQL quert to execute
    query  = "INSERT INTO %s(%s) VALUES %%s" % (table, cols)
    cursor = conn.cursor()
    try:
        extras.execute_values(cursor, query, tuples)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cursor.close()
        return 1
    print("execute_values() done")
    cursor.close()
