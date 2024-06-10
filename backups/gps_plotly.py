import pandas as pd
import pandas.io.sql as sqlio
from connect import *
import warnings
import plotly.graph_objs as go

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

# Creación de gráfico con Plotly
trace1 = go.Scatter3d(
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
)

trace2 = go.Scatter3d(
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

layout = go.Layout(
    title='Velocidades en camino',
    scene=dict(
        xaxis=dict(title='Latitud'),
        yaxis=dict(title='Longitud'),
        zaxis=dict(title='Elevación'),
    )
)

fig = go.Figure(data=[trace1, trace2], layout=layout)
fig.show()

# Cerrar la conexión
close_conn(conn)

