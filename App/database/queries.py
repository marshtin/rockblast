import pandas as pd
from database.connection import connect, close_conn
import geopandas as gpd
from shapely.geometry import Point
import pandas.io.sql as sqlio


def puntos_flota(query_aux):
    #Convierte los puntos de flota en un dataframe 
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
        s = df['speed'].tolist()
        return x, y, s #retorna longitud, latitud y velocidad
    
    except Exception as e:
        print(f"Error al cargar datos al dataframe: {e}")
        return [],[],[] #Retorna listas vacías en caso de error
    finally:
        # Cierra la conexión a la base de datos
        if conn:
            conn.close()
