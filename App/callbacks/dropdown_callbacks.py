from dash import Input, Output
from utils.load_tiff import transformar_tiff

def register_dropdown_callbacks(app):
    @app.callback(
        Output("map-image", "src"),
        [Input("tiff-dropdown", "value")]
    )
    def update_tiff_image(selected_tiff):
        if selected_tiff:
            tiff_path = f"data/{selected_tiff}.tif"  # Ruta basada en el valor del dropdown
            tiff_base64, _ = transformar_tiff(tiff_path)
            return f"data:image/png;base64,{tiff_base64}"
        return None  # No muestra imagen si no hay selección
