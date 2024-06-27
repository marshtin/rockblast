import dash
from dash import dcc, html
import pandas as pd
import pandas.io.sql as sqlio
import plotly.graph_objs as go
from connect import *
import warnings

# Configuraciones para ignorar advertencias y mostrar todas las columnas
warnings.simplefilter(action='ignore', category=UserWarning)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

# Conectar a la base de datos
conn = connect()

# Descargar datos desde AWS
print("Gathering data")
df = sqlio.read_sql_query("SELECT * FROM sandbox.gps_c07 WHERE elevation != 0 AND speed > 0", conn)
df_0 = sqlio.read_sql_query("SELECT * FROM sandbox.gps_c07 WHERE elevation != 0 AND speed = 0", conn)

# Preparación de datos para el gráfico
x = df['latitude'].tolist()
y = df['longitude'].tolist()
z = df['elevation'].tolist()
s = df['speed'].tolist()

x0 = df_0['latitude'].tolist()
y0 = df_0['longitude'].tolist()
z0 = df_0['elevation'].tolist()

# Crear la aplicación Dash
app = dash.Dash(__name__)

#Lista nombre de camiones
lista_name = [
    "C07",
    "C130",
    "C15",
    "C17",
    "C37",
    "C49",
    "C56"
]

#Lista nombre de flota de camiones
lista_type_name = [
    "CAT 793 C",
    "CAT 797 B",
    "CAT 797 F",
    "KOM 930 E"
]
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
                figure={
                    'data': [
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
            )
        ], style={'flex': '1', 'padding': '10px'}),

        html.Div([
            dcc.Graph(
                id='2d-scatter-plot',
                figure={
                    'data': [
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
            )
        ], style={'flex': '1', 'padding': '10px'})
    ], style={'display': 'flex'}),

    html.Div([
        html.Button('Velocidad En Camino', id='button-1', style={'font-size': '20px', 'padding': '15px 30px', 'margin': '10px', 'font-family': 'Noto Sans, sans-serif'}),
        html.Button('Velocidad 0', id='button-2', style={'font-size': '20px', 'padding': '15px 30px', 'margin': '10px', 'font-family': 'Noto Sans, sans-serif'}),
        html.Button('Limpiar Filtros', id='button-3', style={'font-size': '20px', 'padding': '15px 30px', 'margin': '10px', 'font-family': 'Noto Sans, sans-serif'})
    ], style={'display': 'flex', 'justify-content': 'center', 'margin-top': '20px'})


], style={'font-family': 'Noto Sans, sans-serif'})

if __name__ == '__main__':
    app.run_server(debug=False)

# Cerrar la conexión
close_conn(conn)
