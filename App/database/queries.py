import pandas as pd
from database.connection import connect, close_conn
import geopandas as gpd
from shapely.geometry import Point
import pandas.io.sql as sqlio


def visualizename_data(query_aux):
    #Query de camion 7
    #query = (f"SELECT time, latitude, longitude, elevation, speed FROM sandbox.gps_c07 ORDER BY time")
    query2= (f"""SELECT time, latitude, longitude, elevation, speed 
        FROM sandbox.{query_aux} 
        WHERE time >= (
            SELECT MAX(time) - INTERVAL '2 HOURS' 
            FROM sandbox.{query_aux}
            )
        ORDER BY time;""")
    conn = connect()
    if conn is None:
        print("No se pudo establecer conexión con la base de datos.")
        return False
    try:
        # Cargar los datos en un DataFrame
        df = pd.read_sql_query(query2, conn)
        
        # Preparación de datos para el gráfico
        x = df['longitude'].tolist()
        y = df['latitude'].tolist()
        #z = df['elevation'].tolist()
        #s = df['speed'].tolist()
        return x, y
    
    except Exception as e:
        print(f"Error al cargar datos al dataframe: {e}")
        return False
    finally:
        # Cierra la conexión a la base de datos
        if conn:
            conn.close()
    
