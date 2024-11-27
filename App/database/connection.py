import psycopg2
import psycopg2.extras as extras
import warnings

warnings.simplefilter(action='ignore', category=UserWarning)

# Configuración de conexión
DB_PARAMS = {
    "host": "rockblast.cvqg4kkc8mu2.sa-east-1.rds.amazonaws.com",
    "database": "postgres",
    "port": "5432",
    "user": "rockblast",
    "password": "uss_teii_2024"
}

# Conexión global
conn = None

def connect():
    """Establece y retorna una conexión a la base de datos solo si no está conectada aún."""
    global conn
    if conn is None:
        try:
            print('Connecting to the PostgreSQL database...')
            conn = psycopg2.connect(**DB_PARAMS)
            print('Connected')
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error al conectar: {error}")
            return None
    return conn

def close_conn():
    """Cierra la conexión activa a la base de datos."""
    global conn
    if conn is not None:
        conn.close()
        print('Database connection closed.')
        conn = None

def execute_values(df, table):
    """Inserta múltiples registros desde un DataFrame a una tabla usando `execute_values`."""
    conn = connect()
    if conn is None:
        return
    tuples = [tuple(x) for x in df.to_numpy()]
    cols = ','.join(list(df.columns))
    query = f"INSERT INTO {table}({cols}) VALUES %s"
    cursor = conn.cursor()
    try:
        extras.execute_values(cursor, query, tuples)
        conn.commit()
        print("execute_values() done")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error en execute_values: {error}")
        conn.rollback()
    finally:
        cursor.close()
