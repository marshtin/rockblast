import dash
from dash import dcc, html, callback, Output, Input, ctx
import pandas as pd
import pandas.io.sql as sqlio
import plotly.graph_objs as go
from connect import *
import warnings

# Configuraciones para ignorar advertencias y mostrar todas las columnas
warnings.simplefilter(action='ignore', category=UserWarning)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

# Crear la aplicación Dash
app = dash.Dash(__name__)
conn = connect()

#Lista nombre de camiones
# Obtener los nombres de tipo disponibles en la base de datos (ahora será 'name' en lugar de 'type_name')
def get_distinct_names(conn):
    if conn is None:
        raise Exception("Failed to connect to the database. Please check your configuration.")
    
    query = "SELECT DISTINCT name FROM sandbox.fleet"
    df_type_names = sqlio.read_sql_query(query, conn)
    return df_type_names['name'].tolist()

lista_name = get_distinct_names(conn)

#Lista nombre de flota de camiones
# Obtener los nombres de tipo disponibles en la base de datos
def get_distinct_type_names(conn):
    if conn is None:
        raise Exception("Failed to connect to the database. Please check your configuration.")
    
    query = "SELECT DISTINCT type_name FROM sandbox.fleet"
    df_type_names = sqlio.read_sql_query(query, conn)
    return df_type_names['type_name'].tolist()

lista_type_name = get_distinct_type_names(conn)

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

app.layout = html.Div([
    # Incluir Google Fonts
    html.Link(
        href="https://fonts.googleapis.com/css2?family=Noto+Sans:wght@400;700&display=swap",
        rel="stylesheet"
    ),

    #Banner de la página
    html.Div([
        html.H1('Velocidades por caminos',style={'color': '#0693e3'}),
        html.Img(src='assets/Rockblast.png')
    ], className='banner', style={'font-family': 'Noto Sans, sans-serif'}),

    html.Div([

        #Filtro Buscar por ID (Menú Desplegable)
        html.Div([
            html.P('Filtro por ID', className='fix_label', style={'margin-top': '2px', 'color': 'black', 'font-size': '20px', 'margin': '10px', 'font-family': 'Noto Sans, sans-serif'}),
            dcc.Dropdown(
                id='dropdown-1',
                className='custom-dropdown',
                options=[{'label': nombre_camion, 'value': nombre_camion} for nombre_camion in lista_name],  #Recorre la lista de nombre de camiones
                placeholder='Seleccione una opción',
                style={'width': '100%', 'height': '50px', 'font-size': '20px', 'font-family': 'Noto Sans, sans-serif'}
            ),
            html.Button('Aplicar Cambios', id='save-button-1', n_clicks=0, style={'margin-top': '10px', 'width': '100%', 'font-size': '20px', 'font-family': 'Noto Sans, sans-serif'}),
        ], className='create_container2 four columns', style={'margin-bottom': '20px', 'width': '33%'}),

        #Filtro Buscar por Flota
        html.Div([
            html.P('Filtro por Flota', className='fix_label', style={'margin-top': '2px', 'color': 'black', 'font-size': '20px', 'margin': '10px', 'font-family': 'Noto Sans, sans-serif'}),
            dcc.Dropdown(
                id='dropdown-2',
                className='custom-dropdown',
                options=[{'label': nombre_flota, 'value': nombre_flota} for nombre_flota in lista_type_name],  #Recorre la lista de nombre de flota de camiones
                placeholder='Seleccione una opción',
                style={'width': '100%', 'height': '50px', 'font-size': '20px', 'font-family': 'Noto Sans, sans-serif'}
            ),
            html.Button('Aplicar Cambios', id='save-button-2', n_clicks=0, style={'margin-top': '10px', 'width': '100%', 'font-size': '20px', 'font-family': 'Noto Sans, sans-serif'}),
        ], className='create_container2 four columns', style={'margin-bottom': '20px', 'width': '33%'}),

        #Filtro Ingresar Flota personalizada
        html.Div([
            html.P('Ingresar Flota Personalizada', className='fix_label', style={'margin-top': '2px', 'color': 'black', 'font-size': '20px', 'margin': '10px', 'font-family': 'Noto Sans, sans-serif'}),
            dcc.Input(id='flota-personalizada', type='text', placeholder='Ingrese un ID', style={'width': '100%', 'height': '50px', 'font-size': '20px', 'font-family': 'Noto Sans, sans-serif'}),
            html.Button('Aplicar Cambios', id='save-button-3', n_clicks=0, style={'margin-top': '10px', 'width': '100%', 'font-size': '20px', 'font-family': 'Noto Sans, sans-serif'}),
        ], className='create_container2 four columns', style={'margin-bottom': '20px', 'width': '33%'}),
        
    ], className='row flex-display', style={'width': '100%', 'font-family': 'Noto Sans, sans-serif'}),

    html.Div(id='output-state', style={'margin-top': '10px', 'font-family': 'Noto Sans, sans-serif'}),

    html.Div([
        html.Div([
            dcc.Graph(
                id='3d-scatter-plot',
                figure={}
            )
        ], style={'flex': '1', 'padding': '10px'}),

        html.Div([
            dcc.Graph(
                id='2d-scatter-plot',
                figure={}
            )
        ], style={'flex': '1', 'padding': '10px'})
    ], style={'display': 'flex'}),

    html.Div([
        html.Button('Velocidad En Camino', id='button-1', style={'font-size': '20px', 'padding': '15px 30px', 'margin': '10px', 'font-family': 'Noto Sans, sans-serif'}),
        html.Button('Velocidad 0', id='button-2', style={'font-size': '20px', 'padding': '15px 30px', 'margin': '10px', 'font-family': 'Noto Sans, sans-serif'}),
        html.Button('Limpiar Filtros', id='button-3', style={'font-size': '20px', 'padding': '15px 30px', 'margin': '10px', 'font-family': 'Noto Sans, sans-serif'})
    ], style={'display': 'flex', 'justify-content': 'center', 'margin-top': '20px'})


], style={'font-family': 'Noto Sans, sans-serif'})

@callback(
    Output(component_id='3d-scatter-plot', component_property='figure'),
    Output(component_id='2d-scatter-plot', component_property='figure'),
    Input(component_id='save-button-1', component_property='n_clicks'),
    Input(component_id='save-button-2', component_property='n_clicks'),
    Input(component_id='save-button-3', component_property='n_clicks')
)
def update_graphs(btn1, btn2, btn3):
    fig = go.Figure()
    fig2 = go.Figure()
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0] if not None else 'No clicks yet'
    
    # Conectar a la base de datos
    conn = connect()

    if 'save-button-1' in changed_id:
        query_aux = 'c07'
    elif 'save-button-2' in changed_id:
        query_aux = 'c15'
    elif 'save-button-3' in changed_id:
        query_aux = 'c56'
    else:
        query_aux = 'empty'

    df = sqlio.read_sql_query(f"SELECT * FROM sandbox.gps_{query_aux} WHERE elevation != 0 AND speed > 0", conn)
    df_0 = sqlio.read_sql_query(f"SELECT * FROM sandbox.gps_{query_aux} WHERE elevation != 0 AND speed = 0", conn)

    # Preparación de datos para el gráfico
    x = df['latitude'].tolist()
    y = df['longitude'].tolist()
    z = df['elevation'].tolist()
    s = df['speed'].tolist()

    x0 = df_0['latitude'].tolist()
    y0 = df_0['longitude'].tolist()
    z0 = df_0['elevation'].tolist()

    fig = {'data': [
                        go.Scatter3d(
                            x=x,
                            y=y,
                            z=z,
                            mode='markers',
                            marker=dict(
                                size=5,
                                color=s,
                                colorscale='Viridis',
                                opacity=0.8,
                            ),
                            name='Con velocidad'
                        ),
                        go.Scatter3d(
                            x=x0,
                            y=y0,
                            z=z0,
                            mode='markers',
                            marker=dict(
                                size=5,
                                color='red',
                                opacity=0.8,
                            ),
                            name='Sin velocidad'
                        )
                    ],
                    'layout': go.Layout(
                        title='Velocidades en camino',
                        scene=dict(
                            xaxis=dict(title='Latitud'),
                            yaxis=dict(title='Longitud'),
                            zaxis=dict(title='Elevación'),
                        ),
                        font=dict(family='Noto Sans, sans-serif')
                    )
                }
    
    fig2 = {'data': [
                        go.Scatter(
                            x=x,
                            y=y,
                            mode='markers',
                            marker=dict(
                                size=5,
                                color=s,
                                colorscale='Viridis',
                                opacity=0.8,
                            ),
                            name='Con velocidad'
                        ),
                        go.Scatter(
                            x=x0,
                            y=y0,
                            mode='markers',
                            marker=dict(
                                size=5,
                                color='red',
                                opacity=0.8,
                            ),
                            name='Sin velocidad'
                        )
                    ],
                    'layout': go.Layout(
                        title='Velocidades en camino (2D)',
                        xaxis=dict(title='Latitud'),
                        yaxis=dict(title='Longitud'),
                        font=dict(family='Noto Sans, sans-serif')
                    )
                }
    # Cerrar la conexión
    close_conn(conn)
    return fig, fig2

if __name__ == '__main__':
    conn = connect()
    if conn is None:
        exit(1)
    app.run_server(debug=False)
    close_conn(conn)
