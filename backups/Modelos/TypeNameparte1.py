# Script 1: get_type_names.py

import pandas as pd
import pandas.io.sql as sqlio
import psycopg2

# Configuración de la conexión a la base de datos
def connect():
    conn = None
    try:
        conn = psycopg2.connect(
            host="rockblast-g4.cfwy4giwk9t5.sa-east-1.rds.amazonaws.com",
            database="datasources",
            user="uss_tei_g4",
            password="uss_tei_g4",
            port="5432"
        )
        print('Connected to the PostgreSQL database...')
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return conn

def close_conn(conn):
    if conn:
        conn.close()
        print('Database connection closed.')

# Obtener los nombres de tipo disponibles en la base de datos
def get_distinct_type_names(conn):
    if conn is None:
        raise Exception("Failed to connect to the database. Please check your configuration.")
    
    query = "SELECT DISTINCT type_name FROM sandbox.fleet"
    df_type_names = sqlio.read_sql_query(query, conn)
    return df_type_names['type_name'].tolist()

if __name__ == "__main__":
    conn = connect()
    if conn is None:
        exit(1)
    
    try:
        # Obtener los nombres de tipo disponibles en la base de datos
        type_names = get_distinct_type_names(conn)
        print("Available type names:", type_names)
        
        # Guardar los nombres de tipo en un archivo o base de datos si es necesario
        with open('processed_type_names.txt', 'w') as f:
            for type_name in type_names:
                f.write(type_name + '\n')
        
    finally:
        close_conn(conn)
