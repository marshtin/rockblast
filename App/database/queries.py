import pandas as pd
from database.connection import connect, close_conn

def fetch_gps_data():
    """Consulta los datos de GPS y devuelve un DataFrame."""
    query = """
    SELECT time, latitude, longitude, elevation, speed 
    FROM sandbox.gps_c07 
    ORDER BY time
    """
    conn = connect()
    if conn is None:
        return pd.DataFrame()
    try:
        return pd.read_sql_query(query, conn)
    except Exception as e:
        print(f"Error al ejecutar fetch_gps_data: {e}")
        return pd.DataFrame()
    finally:
        # Si prefieres seguir cerrando la conexión después de cada consulta:
        # close_conn(conn)
        pass

def fetch_database_version():
    """Consulta la versión de la base de datos y devuelve un resultado."""
    query = "SELECT version()"
    conn = connect()
    if conn is None:
        return "Error: No se pudo conectar a la base de datos"
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        version = cursor.fetchone()
        return version[0] if version else "No se encontró versión"
    except Exception as e:
        print(f"Error al ejecutar fetch_database_version: {e}")
        return "Error al obtener la versión"
    finally:
        # Si prefieres seguir cerrando la conexión después de cada consulta:
        # close_conn(conn)
        pass
