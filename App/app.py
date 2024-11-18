from dash import Dash
from components import layout  # Importa el layout principal
from callbacks.routes_callback import register_routes_callbacks  # Callbacks de rutas
from callbacks.dropdown_callbacks import register_dropdown_callbacks  # Callbacks del dropdown

app = Dash(__name__, suppress_callback_exceptions=True)

# Asigna el layout a la aplicación
app.layout = layout.layout

# Registrar todos los callbacks al inicio
register_routes_callbacks(app)
register_dropdown_callbacks(app)  

if __name__ == "__main__":
    app.run_server(debug=True)
