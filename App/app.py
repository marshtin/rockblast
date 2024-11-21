from dash import Dash
from components import layout  # Importa el layout principal
from callbacks.routes_callback import register_routes_callbacks  # Callbacks de rutas
from callbacks.dropdown_callbacks import register_dropdown_callbacks  # Callbacks del dropdown
from database.queries import fetch_gps_data, fetch_database_version
from database.connection import close_conn

# Obtén la versión de la base de datos
db_version = fetch_database_version()
print(f"Database version: {db_version}")

# Obtén los datos de GPS
gps_data = fetch_gps_data()
print(f"Datos de gps: {gps_data}")

app = Dash(__name__, suppress_callback_exceptions=True)

# Asigna el layout a la aplicación
app.layout = layout.layout

# Registrar todos los callbacks al inicio
register_routes_callbacks(app)
register_dropdown_callbacks(app)  

# Cerrar la conexión al finalizar
@app.server.teardown_appcontext
def cleanup(_):
    close_conn()

if __name__ == "__main__":
    app.run_server(debug=True)
