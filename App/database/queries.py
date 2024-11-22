import pandas as pd
from database.connection import connect, close_conn
import geopandas as gpd
from shapely.geometry import Point

def fetch_gps_data_to_geojson(output_file):
    """
    Consulta los datos de GPS en EPSG:3857 y genera un archivo GeoJSON.
    
    Args:
        output_file (str): Ruta donde se guardará el archivo GeoJSON.
    
    Returns:
        bool: True si el archivo se creó correctamente, False si hubo un error.
    """
    query = """
    SELECT time, latitude, longitude, elevation, speed 
    FROM sandbox.gps_c07 
    ORDER BY time
    """
    conn = connect()
    if conn is None:
        print("No se pudo establecer conexión con la base de datos.")
        return False

    try:
        # Consulta los datos y los carga en un DataFrame
        df = pd.read_sql_query(query, conn)
        
        # Verifica si hay datos
        if df.empty:
            print("No se encontraron datos.")
            return False

        # Convierte los datos a un GeoDataFrame
        geometry = [Point(xy) for xy in zip(df['longitude'], df['latitude'])]
        gdf = gpd.GeoDataFrame(df, geometry=geometry)

        # Define el sistema de coordenadas como EPSG:3857 (ya está en este sistema)
        gdf.set_crs(epsg=3857, inplace=True)

        # Guarda el GeoDataFrame directamente como GeoJSON
        gdf.to_file(output_file, driver="GeoJSON")
        
        print(f"Archivo GeoJSON creado con éxito en {output_file}")
        return True
    except Exception as e:
        print(f"Error al generar el archivo GeoJSON: {e}")
        return False
    finally:
        # Cierra la conexión a la base de datos
        if conn:
            conn.close()



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
