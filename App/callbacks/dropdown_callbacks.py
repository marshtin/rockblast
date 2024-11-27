from dash import Input, Output
from utils.load_tiff import transformar_tiff
import plotly.graph_objects as go

def register_dropdown_callbacks(app, points):
    @app.callback(
        Output("map-image", "figure"),
        [Input("tiff-dropdown", "value")]
    )
    def update_tiff_image(selected_tiff):
        if selected_tiff:
            # Cargar el archivo TIFF seleccionado
            tiff_path = f"rockblast/App/data/{selected_tiff}.tif"
            tiff_base64, extent = transformar_tiff(tiff_path)
            
            # Crear los datos del gráfico
            data = [
                go.Scatter(
                    x=points.geometry.x,
                    y=points.geometry.y,
                    mode='markers',
                    marker=dict(size=6, color='blue'),
                    name='Puntos'
                )
            ]
            
            # Definir el layout del gráfico
            layout = go.Layout(
                title=f'TIFF con Puntos - {selected_tiff}',
                images=[{
                    'source': f"data:image/png;base64,{tiff_base64}",
                    'xref': "x",
                    'yref': "y",
                    'x': extent[0],
                    'y': extent[3],
                    'sizex': extent[1] - extent[0],
                    'sizey': extent[3] - extent[2],
                    'sizing': "stretch",
                    'layer': "below"
                }],
                xaxis=dict(range=[extent[0], extent[1]], visible=False, scaleanchor="y", scaleratio=1),
                yaxis=dict(range=[extent[2], extent[3]], visible=False),
                showlegend=True,
                autosize=True
            )
            
            # Retornar la figura construida
            return go.Figure(data=data, layout=layout)
        
        # Retornar un gráfico vacío si no hay un TIFF seleccionado
        return go.Figure()
