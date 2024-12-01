from dash import html
from dash.dependencies import Input, Output
from components.main_layout import main_layout
from components.operators_table_layout import tabla_operadores_layout
from utils.load_tiff import save_cache

def register_routes_callbacks(app):
    @app.callback(
        Output('page-content', 'children'),
        [Input('url', 'pathname')]
    )
    def display_page(pathname):
        if pathname == '/tabla-operadores':
            return tabla_operadores_layout  # Página de tablas
        elif pathname == '/':  # Página principal
            return main_layout
        else:
            return html.Div("Página no encontrada")  # Página de error 404