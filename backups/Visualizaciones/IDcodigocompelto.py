import pandas as pd
import pandas.io.sql as sqlio
import psycopg2
import warnings
import plotly.graph_objs as go

warnings.simplefilter(action='ignore', category=UserWarning)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

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

# Obtener los IDs de equipos disponibles en la base de datos
def get_distinct_equipment_ids(conn):
    if conn is None:
        raise Exception("Failed to connect to the database. Please check your configuration.")
    
    query = "SELECT DISTINCT equipment_id FROM sandbox.fleet"
    df_equipment_ids = sqlio.read_sql_query(query, conn)
    return df_equipment_ids['equipment_id'].tolist()

# Obtener datos de la tabla fleet según el equipment_id y las dos consultas
def get_fleet_data_by_equipment_id(conn, equipment_id):
    if conn is None:
        raise Exception("Failed to connect to the database. Please check your configuration.")
    
    query_with_speed = f"SELECT * FROM sandbox.fleet WHERE equipment_id = '{equipment_id}' AND elevation != 0 AND speed > 0"
    query_without_speed = f"SELECT * FROM sandbox.fleet WHERE equipment_id = '{equipment_id}' AND elevation != 0 AND speed = 0"
    
    df_with_speed = sqlio.read_sql_query(query_with_speed, conn)
    df_without_speed = sqlio.read_sql_query(query_without_speed, conn)
    
    return df_with_speed, df_without_speed

# Visualizar los datos con Plotly
def visualize_fleet_data_combined(df_with_speed_list, df_without_speed_list, equipment_id):
    traces = []

    for df_with_speed in df_with_speed_list:
        if not df_with_speed.empty:
            x_with_speed = df_with_speed['latitude'].tolist()
            y_with_speed = df_with_speed['longitude'].tolist()
            z_with_speed = df_with_speed['elevation'].tolist()
            s_with_speed = df_with_speed['speed'].tolist()

            trace_with_speed = go.Scatter3d(
                x=x_with_speed,
                y=y_with_speed,
                z=z_with_speed,
                mode='markers',
                marker=dict(
                    size=5,
                    color=s_with_speed,
                    colorscale='Viridis',
                    opacity=0.8,
                ),
                name=f'Con velocidad (Equipment ID: {equipment_id})'
            )
            traces.append(trace_with_speed)

    for df_without_speed in df_without_speed_list:
        if not df_without_speed.empty:
            x_without_speed = df_without_speed['latitude'].tolist()
            y_without_speed = df_without_speed['longitude'].tolist()
            z_without_speed = df_without_speed['elevation'].tolist()

            trace_without_speed = go.Scatter3d(
                x=x_without_speed,
                y=y_without_speed,
                z=z_without_speed,
                mode='markers',
                marker=dict(
                    size=5,
                    color='blue',
                    opacity=0.8,
                ),
                name=f'Sin velocidad (Equipment ID: {equipment_id})'
            )
            traces.append(trace_without_speed)

    if traces:
        layout = go.Layout(
            title=f'Datos del Fleet - Equipment ID: {equipment_id}',
            scene=dict(
                xaxis=dict(title='Latitud'),
                yaxis=dict(title='Longitud'),
                zaxis=dict(title='Elevación'),
            )
        )

        fig = go.Figure(data=traces, layout=layout)
        fig.show()
    else:
        print("No data available for visualization.")

# Main
if __name__ == "__main__":
    conn = connect()
    if conn is None:
        exit(1)
    
    try:
        # Obtener los IDs de equipos disponibles en la base de datos
        equipment_ids = get_distinct_equipment_ids(conn)
        print("Available equipment IDs:", equipment_ids)
        
        processed_equipment_ids = []  # Lista para almacenar los IDs de equipos procesados
        
        for equipment_id in equipment_ids:
            print(f"Processing data for equipment ID: {equipment_id}")
            
            # Obtener datos del equipo específico
            df_with_speed, df_without_speed = get_fleet_data_by_equipment_id(conn, equipment_id)
            
            # Agregar el ID de equipo a la lista de procesados
            processed_equipment_ids.append(equipment_id)
        
        # Visualizar los datos combinados para cada equipo procesado
        for equipment_id in processed_equipment_ids:
            df_with_speed, df_without_speed = get_fleet_data_by_equipment_id(conn, equipment_id)
            visualize_fleet_data_combined([df_with_speed], [df_without_speed], equipment_id)
        
    finally:
        close_conn(conn)
    
    print("Processed equipment IDs:", processed_equipment_ids)  # Imprimir los IDs de equipo procesados al final
