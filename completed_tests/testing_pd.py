import pandas as pd
import pandas.io.sql as sqlio
import sqlalchemy
from IPython.display import display
from connect import *
import warnings
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt

warnings.simplefilter(action='ignore', category=UserWarning)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

conn = connect()
cur = conn.cursor()
cur.execute('SELECT version()')
db_version = cur.fetchone()
print(db_version)

## Downloading data from AWS
print("Gathering data")
df = sqlio.read_sql_query("SELECT * FROM sandbox.gps_c07 WHERE elevation != 0 AND speed > 0", conn)
df_0 = sqlio.read_sql_query("SELECT * FROM sandbox.gps_c07 WHERE elevation != 0 AND speed = 0", conn)

x = df['latitude'].to_list()
y = df['longitude'].to_list()
z = df['elevation'].to_list()
s = df['speed'].to_list()

x0 = df_0['latitude'].to_list()
y0 = df_0['longitude'].to_list()
z0 = df_0['elevation'].to_list()

# Creating figure
fig = plt.figure(figsize = (100, 7))
ax = plt.axes(projection ="3d")
 
# Creating plot
p = ax.scatter3D(x, y, z, c = s, cmap = 'viridis')
q = ax.scatter3D(x0, y0, z0, color = 'red')
plt.title("Velocidades en camino")
ax.set_xlabel('latitude')
ax.set_ylabel('longitude')
ax.set_zlabel('elevation')
#fig.colorbar(p)

# show plot
plt.show()

##Closing connection
close_conn(conn)
