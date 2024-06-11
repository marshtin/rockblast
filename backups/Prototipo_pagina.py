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

app.layout = html.Div([
    html.Div([
        html.H1('Velocidades por caminos'),
        html.Img(src='assets/Rockblast.png')
    ], className='banner'),

    html.Div([
        html.Div([
            html.P('Ingresar ID', className='fix_label', style={'color': 'black', 'margin-top': '2px'}),
            dcc.Input(id='input-id', type='text', placeholder='Ingrese un ID'),
            html.Button('Guardar', id='save-button', n_clicks=0),
            html.Div(id='output-state', style={'margin-top': '10px'})
        ], className='create_container2 five columns', style={'margin-bottom': '20px'}),
    ], className='row flex-display'),

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
                    )
                )
            }
        )
    ]),

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
                )
            }
        )
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)

# Cerrar la conexión
close_conn(conn)
