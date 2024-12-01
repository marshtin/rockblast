from dash import Dash
from components import layout  # Importa el layout principal
from callbacks.routes_callback import register_routes_callbacks  # Callbacks de rutas
from callbacks.dropdown_callbacks import register_dropdown_callbacks  # Callbacks del dropdown
from callbacks.operators_callbacks import register_operator_callbacks
from database.connection import close_conn
import atexit
from utils.load_tiff import save_cache  # Importa la función para guardar el caché

# Inicializa la app de Dash
app = Dash(__name__, suppress_callback_exceptions=True)

# Asigna el layout a la aplicación
app.layout = layout.layout

# Registrar todos los callbacks al inicio
register_routes_callbacks(app)
register_dropdown_callbacks(app)
register_operator_callbacks(app)

# Guardar el caché de TIFFs al salir de la aplicación
atexit.register(save_cache)

# Cerrar la conexión al finalizar
@app.server.teardown_appcontext
def cleanup(_):
    close_conn()


if __name__ == "__main__":
    app.run_server(debug=True, use_reloader=False)
