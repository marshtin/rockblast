import pandas as pd
from database.connection import connect, close_conn


def puntos_camion(query_aux):
    #Convierte los puntos de camion en un dataframe 
    query_camion= (f"""SELECT time, latitude, longitude, elevation, speed 
        FROM sandbox.{query_aux} 
        WHERE time >= (
            SELECT MAX(time) - INTERVAL '4 HOURS' 
            FROM sandbox.{query_aux}
            )
        ORDER BY time;""")
    conn = connect()
    if conn is None:
        print("No se pudo establecer conexión con la base de datos.")
        return False
    try:
        # Cargar los datos en un DataFrame
        df = pd.read_sql_query(query_camion, conn)
        df_1 = df[df['speed'] > 0]

        # Preparación de datos para el gráfico
        x = df_1['longitude'].tolist()
        y = df_1['latitude'].tolist()
        #z = df['elevation'].tolist()
        s = df_1['speed'].tolist()
        
        df_0 = df[df['speed'] == 0]
        x_0 = df_0['longitude'].tolist()
        y_0 = df_0['latitude'].tolist()
        #z_0 = df['elevation'].tolist()
        s_0 = df_0['speed'].tolist()

        return x, y, s, x_0, y_0, s_0, df #retorna longitud, latitud y velocidad
      
    except Exception as e:
        print(f"Error al cargar datos al dataframe: {e}")
        return [],[],[],[],[],[], pd.DataFrame() #Retorna listas vacías en caso de error
    finally:
        # Cierra la conexión a la base de datos
        if conn:
            conn.close()

def nombres_flota():
    #Convierte los nombres de flota en un dataframe 
    query_nombres_flota= (f"SELECT DISTINCT type_name FROM sandbox.fleet")
    conn = connect()
    if conn is None:
        print("No se pudo establecer conexión con la base de datos.")
        return False
    try:
        # Cargar los datos en un DataFrame
        df_nombres_flota = pd.read_sql_query(query_nombres_flota, conn)
        # Retorna df con nombres de flota
        return df_nombres_flota['type_name'].tolist()

    except Exception as e:
        print(f"Error al cargar datos al dataframe: {e}")
        return [] #Retorna lista vacía en caso de error
    finally:
        # Cierra la conexión a la base de datos
        if conn:
            conn.close()


def puntos_flota(query_aux):
    #Convierte los puntos de flota en un dataframe 
    query_flota= (f"""SELECT time, latitude, longitude, elevation, speed 
        FROM sandbox.fleet 
        WHERE time >= (
            SELECT MAX(time) - INTERVAL '4 HOURS' 
            FROM sandbox.fleet
            )
        AND type_name = '{query_aux}'
        ORDER BY time;""")
    conn = connect()
    if conn is None:
        print("No se pudo establecer conexión con la base de datos.")
        return False
    try:
        # Cargar los datos en un DataFrame
        df_puntos_flota = pd.read_sql_query(query_flota, conn)
        
        # Preparación de datos para el gráfico
        x = df_puntos_flota['longitude'].tolist()
        y = df_puntos_flota['latitude'].tolist()
        #z = df['elevation'].tolist()
        s = df_puntos_flota['speed'].tolist()
        return x, y, s #retorna longitud, latitud y velocidad
    
    except Exception as e:
        print(f"Error al cargar datos al dataframe: {e}")
        return [],[],[] #Retorna listas vacías en caso de error
    finally:
        # Cierra la conexión a la base de datos
        if conn:
            conn.close()

# Query de filtro personalizado (en proceso)
def get_fleet_data_by_name(conn, custom_list):
    if conn is None:
        raise Exception("Failed to connect to the database. Please check your configuration.")
    query_aux = ''
    for id in custom_list:
        if custom_list.index(id) == 0:
            query_aux += f"'{id}'"
        else:
            query_aux += f" OR name = '{id}'"
    query_with_speed = f"SELECT * FROM sandbox.fleet WHERE name = {query_aux} AND elevation != 0 AND speed > 0"
    query_without_speed = f"SELECT * FROM sandbox.fleet WHERE name = {query_aux} AND elevation != 0 AND speed = 0"


#-----------QUERYS-----------
def get_data_from_db_combined():
    """
    Obtiene datos de las tablas `average_payload_totalloads`, `average_payload_totaldumps`
    y operadores con menor y mayor tiempo detenido, devolviendo los resultados en tres DataFrames separados.
    """
    # Usar un context manager para manejar la conexión
    with connect() as conn:
        # Ejecuta las consultas y carga los datos en DataFrames
        df_top_load = pd.read_sql_query("""
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
        """, conn)
        
        df_top_dumps = pd.read_sql_query("""
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
        """, conn)
        
        df_time_extremes = pd.read_sql_query("""
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
        """, conn)
    
    return df_top_load, df_top_dumps, df_time_extremes