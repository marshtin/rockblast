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

#-----------QUERYS-----------
def get_data_from_db_combined():
    """
    Obtiene datos de las tablas `average_payload_totalloads`, `average_payload_totaldumps`
    y operadores con menor y mayor tiempo detenido, devolviendo los resultados en tres DataFrames separados.
    
    :return: Una tupla de DataFrames (df_top_load, df_top_dumps, df_time_extremes)
    """
    # Configura tu conexión a la base de datos
    conn = connect()
    
    # Consulta SQL para la tabla average_payload_totalloads
    query_loads = """
    SELECT 
        truck_operator_id,
        CONCAT(truck_operator_first_name, ' ', truck_operator_last_name) AS full_name,
        average_payload 
    FROM 
        sandbox.average_payload_totalloads
    WHERE 
        truck_operator_id IS NOT NULL 
        AND truck_operator_last_name IS NOT NULL 
        AND truck_operator_first_name IS NOT NULL 
        AND average_payload IS NOT NULL
    ORDER BY 
        average_payload DESC
    LIMIT 5;
    """
    
    # Consulta SQL para la tabla average_payload_totaldumps
    query_dumps = """
    SELECT 
        truck_operator_id,
        CONCAT(truck_operator_first_name, ' ', truck_operator_last_name) AS full_name,
        average_payload 
    FROM 
        sandbox.average_payload_totaldumps
    WHERE 
        truck_operator_id IS NOT NULL 
        AND truck_operator_last_name IS NOT NULL 
        AND truck_operator_first_name IS NOT NULL 
        AND average_payload IS NOT NULL
    ORDER BY 
        average_payload DESC
    LIMIT 5;
    """
    
    # Consulta SQL para los operadores con menor y mayor tiempo detenido
    query_time_extremes = """
    WITH extremos AS (
        SELECT 
            operador,
            promedio_tiempo_detenido,
            RANK() OVER (ORDER BY promedio_tiempo_detenido ASC) AS rank_asc,
            RANK() OVER (ORDER BY promedio_tiempo_detenido DESC) AS rank_desc
        FROM sandbox.operadores_promedios_tiempo
    )
    SELECT 
        (SELECT operador FROM extremos WHERE rank_asc = 1) AS operador_con_menor_tiempo,
        (SELECT operador FROM extremos WHERE rank_desc = 1) AS operador_con_mayor_tiempo,
        ((MAX(promedio_tiempo_detenido) - MIN(promedio_tiempo_detenido)) / MIN(promedio_tiempo_detenido))::numeric * 100 AS diferencia_porcentual
    FROM extremos;
    """
    
    # Ejecuta las consultas y carga los datos en DataFrames
    df_top_load = pd.read_sql_query(query_loads, conn)
    df_top_dumps = pd.read_sql_query(query_dumps, conn)
    df_time_extremes = pd.read_sql_query(query_time_extremes, conn)
    
    # Cierra la conexión
    conn.close()
    
    return df_top_load, df_top_dumps, df_time_extremes