import pandas as pd
import pandas.io.sql as sqlio
import psycopg2
import warnings

warnings.simplefilter(action='ignore', category=UserWarning)

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

# Obtener todos los valores distintos de la columna type_name
def get_distinct_type_names():
    conn = connect()
    if conn is None:
        raise Exception("Failed to connect to the database. Please check your configuration.")
    
    query = "SELECT DISTINCT type_name FROM sandbox.fleet"
    df_type_names = sqlio.read_sql_query(query, conn)
    
    close_conn(conn)
    return df_type_names['type_name'].tolist()

# Obtener datos de la tabla fleet según el type_name
def get_fleet_data_by_type(type_name):
    conn = connect()
    if conn is None:
        raise Exception("Failed to connect to the database. Please check your configuration.")
    
    query = f"SELECT * FROM sandbox.fleet WHERE type_name = '{type_name}'"
    df_fleet = sqlio.read_sql_query(query, conn)
    
    close_conn(conn)
    return df_fleet

# Separar los datos por equipment_id
def separate_data_by_equipment_id(df_fleet):
    separated_data = {equipment_id: df for equipment_id, df in df_fleet.groupby('equipment_id')}
    return separated_data

# Main
if __name__ == "__main__":
    type_names = get_distinct_type_names()
    print("Available type names:", type_names)
    
    for type_name in type_names:
        print(f"Processing data for type_name: {type_name}")
        fleet_data = get_fleet_data_by_type(type_name)
        separated_fleet_data = separate_data_by_equipment_id(fleet_data)
        
        # Imprimir los datos separados por equipment_id
        for equipment_id, data in separated_fleet_data.items():
            print(f"\nData for Equipment ID {equipment_id}:")
            print(data)
