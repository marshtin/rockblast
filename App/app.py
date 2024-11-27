import os
from dash import Dash
from components import layout  # Importa el layout principal
from callbacks.routes_callback import register_routes_callbacks  # Callbacks de rutas
from callbacks.dropdown_callbacks import register_dropdown_callbacks  # Callbacks del dropdown
#from database.queries import fetch_gps_data_to_geojson 
from database.connection import close_conn
#import geopandas as gpd

app = Dash(__name__, suppress_callback_exceptions=True)

# Asigna el layout a la aplicación
app.layout = layout.layout

""" # Ruta del archivo GeoJSON
geojson_file = "rockblast/App/data/gps_points.geojson"  # Ruta donde se guardará el GeoJSON

# Verificar o crear el archivo GeoJSON
if not os.path.exists(geojson_file):
    success = fetch_gps_data_to_geojson(geojson_file)
else:
    success = True  # Asumimos éxito si el archivo ya existe

# Cargar puntos desde el GeoJSON
if success:
    try:
        points = gpd.read_file(geojson_file)  # Cargar puntos desde el archivo GeoJSON
        print(f"Archivo GeoJSON cargado con éxito desde {geojson_file}")
    except Exception as e:
        points = None
        print(f"Error al cargar puntos desde el GeoJSON: {e}")
else:
    points = None
    print("Advertencia: No se cargaron puntos desde la base de datos.") """

# Registrar todos los callbacks al inicio
register_routes_callbacks(app)
register_dropdown_callbacks(app)

# Cerrar la conexión al finalizar
@app.server.teardown_appcontext
def cleanup(_):
    close_conn()

if __name__ == "__main__":
    app.run_server(debug=True)
