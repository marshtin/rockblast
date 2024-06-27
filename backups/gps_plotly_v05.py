import pandas as pd
import pandas.io.sql as sqlio
from connect import *
import warnings
import plotly.graph_objs as go
from IPython.display import display
import plotly.express as px

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

# Determine the latest timestamp in the data
latest_timestamp = df['time'].max()

# Calculate the cutoff time for the last 24 hours
cutoff_time = latest_timestamp - pd.Timedelta(hours=4)

# Filter the DataFrame for the last 24 hours
df = df[df['time'] >= cutoff_time]
df_0 = df_0[df_0['time'] >= cutoff_time]

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

#fig = go.Figure(data=[trace1, trace2], layout=layout)
#fig.show()

# Sort the DataFrame by time
df = df.sort_values('time')

# Create a cumulative DataFrame for the animation
cumulative_df = pd.DataFrame(columns=df.columns)
frames_data = []
for i, row in df.iterrows():
    cumulative_df = pd.concat([cumulative_df, pd.DataFrame([row])], ignore_index=True)
    frame = cumulative_df.copy()
    frame['frame'] = i  # Assign a unique frame number
    frames_data.append(frame)

# Concatenate all frames to create the animation DataFrame
animation_df = pd.concat(frames_data)

# Create the animated scatter plot
fig = px.scatter_3d(animation_df, x='latitude', y='longitude', z='elevation',
                    animation_frame='frame', animation_group='frame',
                    color='speed', size='speed', size_max=55,
                    range_x=[df['latitude'].min(), df['latitude'].max()],
                    range_y=[df['longitude'].min(), df['longitude'].max()],
                    range_z=[df['elevation'].min(), df['elevation'].max()])

# Update the animation speed to 1000ms (1 second) per frame
fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 1

fig.show()

#print("Saving data in csv")
df.to_csv("test_timefilter.csv")

# Cerrar la conexión
close_conn(conn)

