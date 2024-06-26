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

# Obtener los nombres de tipo disponibles en la base de datos
def get_distinct_type_names(conn):
    if conn is None:
        raise Exception("Failed to connect to the database. Please check your configuration.")
    
    query = "SELECT DISTINCT type_name FROM sandbox.fleet"
    df_type_names = sqlio.read_sql_query(query, conn)
    return df_type_names['type_name'].tolist()

# Obtener datos de la tabla fleet según el type_name y las dos consultas
def get_fleet_data_by_type(conn, type_name):
    if conn is None:
        raise Exception("Failed to connect to the database. Please check your configuration.")
    
    query_with_speed = f"SELECT * FROM sandbox.fleet WHERE type_name = '{type_name}' AND elevation != 0 AND speed > 0"
    query_without_speed = f"SELECT * FROM sandbox.fleet WHERE type_name = '{type_name}' AND elevation != 0 AND speed = 0"
    
    df_with_speed = sqlio.read_sql_query(query_with_speed, conn)
    df_without_speed = sqlio.read_sql_query(query_without_speed, conn)
    
    return df_with_speed, df_without_speed

# Visualizar los datos con Plotly
def visualize_fleet_data_combined(df_with_speed_list, df_without_speed_list, type_name):
    grouped_data_with_speed = {}
    grouped_data_without_speed = {}

    colorscales = {
        'Magma': [
            '#000004', '#1d1147', '#51127c', '#822681', '#b5367a', '#e65462', '#fc8761', '#fdbd70', '#fbfdb7'
        ],
        'Viridis': [
            '#440154', '#482777', '#3f4a8a', '#31688e', '#26838f', '#1f9d8a', '#6cce5a', '#b6de2b', '#fee825'
        ],
        'Cividis': [
            '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728','#9467bd', '#8c564b', '#e377c2', '#7f7f7f','#bcbd22', '#17becf', '#aec7e8', '#ffbb78'
        ],
        'Plasma': [
            '#0d0887', '#5c02a3', '#9a179b', '#cb4678', '#eb7852', '#f0a13a', '#f8e43b', '#f0f921'
        ],
        'Inferno': [
            '#000004', '#1e141c', '#4a0403', '#721f05', '#9b2a02', '#cc4c02', '#ee8729', '#f4c63a', '#fbfd76'
        ],
        'Blues': [
            '#f7fbff', '#deebf7', '#c6dbef', '#9ecae1', '#6baed6', '#4292c6', '#2171b5', '#08519c', '#08306b'
        ],
        'Greens': [
            '#f7fcf5', '#e5f5e0', '#c7e9c0', '#a1d99b', '#74c476', '#41ab5d', '#238b45', '#006d2c', '#00441b'
        ],
        'Greys': [
            '#ffffff', '#f0f0f0', '#d9d9d9', '#bdbdbd', '#969696', '#737373', '#525252', '#252525', '#000000'
        ],
        'Oranges': [
            '#fff5eb', '#fee6ce', '#fdd0a2', '#fdae6b', '#fd8d3c', '#f16913', '#d94801', '#a63603', '#7f2704'
        ],
        'Reds': [
            '#fff5f0', '#fee0d2', '#fcbba1', '#fc9272', '#fb6a4a', '#ef3b2c', '#cb181d', '#a50f15', '#67000d'
        ],
        'YlGnBu': [
            '#ffffd9', '#edf8b1', '#c7e9b4', '#7fcdbb', '#41b6c4', '#1d91c0', '#225ea8', '#253494', '#081d58'
        ],
        'YlOrRd': [
            '#ffffb2', '#fed976', '#feb24c', '#fd8d3c', '#fc4e2a', '#e31a1c', '#bd0026', '#800026'
        ]
    }

    # Selección de una escala de colores (ejemplo: 'Viridis')
    selected_colorscale = 'Cividis'
    colors = colorscales[selected_colorscale]

    color_index = 0

    # Agrupar por name en df_with_speed
    for df_with_speed in df_with_speed_list:
        if not df_with_speed.empty:
            for name, group in df_with_speed.groupby('name'):
                if name not in grouped_data_with_speed:
                    grouped_data_with_speed[name] = {'x': [], 'y': [], 'z': [], 's': [], 'color': []}
                grouped_data_with_speed[name]['x'].extend(group['latitude'].tolist())
                grouped_data_with_speed[name]['y'].extend(group['longitude'].tolist())
                grouped_data_with_speed[name]['z'].extend(group['elevation'].tolist())
                grouped_data_with_speed[name]['s'].extend(group['speed'].tolist())
                grouped_data_with_speed[name]['color'].extend([colors[color_index]] * len(group))
                color_index = (color_index + 1) % len(colors)  # Avanzar al siguiente color en la escala

    # Agrupar por name en df_without_speed
    for df_without_speed in df_without_speed_list:
        if not df_without_speed.empty:
            for name, group in df_without_speed.groupby('name'):
                if name not in grouped_data_without_speed:
                    grouped_data_without_speed[name] = {'x': [], 'y': [], 'z': [], 'color': []}
                grouped_data_without_speed[name]['x'].extend(group['latitude'].tolist())
                grouped_data_without_speed[name]['y'].extend(group['longitude'].tolist())
                grouped_data_without_speed[name]['z'].extend(group['elevation'].tolist())
                grouped_data_without_speed[name]['color'].extend([colors[color_index]] * len(group))
                color_index = (color_index + 1) % len(colors)  # Avanzar al siguiente color en la escala

    traces = []

    # Crear trazas para datos con velocidad mayor a 0
    for name, data in grouped_data_with_speed.items():
        trace = go.Scatter3d(
            x=data['x'],
            y=data['y'],
            z=data['z'],
            mode='markers',
            marker=dict(
                size=5,
                color=data['color'],  # Usar la lista de colores asignada
                opacity=0.8,
            ),
            name=f'{name} - Con velocidad (Type: {type_name})'
        )
        traces.append(trace)

    # Crear trazas para datos con velocidad igual a 0
    for name, data in grouped_data_without_speed.items():
        trace = go.Scatter3d(
            x=data['x'],
            y=data['y'],
            z=data['z'],
            mode='markers',
            marker=dict(
                size=5,
                color=data['color'],  # Usar la lista de colores asignada
                opacity=0.8,
            ),
            name=f'{name} - Sin velocidad (Type: {type_name})'
        )
        traces.append(trace)

    if traces:
        layout = go.Layout(
            title=f'Datos del Fleet - Type: {type_name}',
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
        # Obtener los nombres de tipo disponibles en la base de datos
        type_names = get_distinct_type_names(conn)
        print("Available type names:", type_names)
        
        processed_type_names = []  # Lista para almacenar los nombres de tipo procesados
        
        for type_name in type_names:
            print(f"Processing data for type_name: {type_name}")
            
            # Obtener datos del tipo específico
            df_with_speed, df_without_speed = get_fleet_data_by_type(conn, type_name)
            # Guardar datos con velocidad en CSV
            #df_with_speed.to_csv(f"{type_name}_with_speed.csv")
            # Guardar datos sin velocidad en CSV
            #df_without_speed.to_csv(f"{type_name}_without_speed.csv")
            # Agregar el nombre de tipo a la lista de procesados
            processed_type_names.append(type_name)
        
        # Visualizar los datos combinados para cada tipo procesado
        for type_name in processed_type_names:
            df_with_speed, df_without_speed = get_fleet_data_by_type(conn, type_name)
            visualize_fleet_data_combined([df_with_speed], [df_without_speed], type_name)
        
    finally:
        close_conn(conn)
    
    print("Processed type names:", processed_type_names)  # Imprimir los nombres de tipo procesados al final
