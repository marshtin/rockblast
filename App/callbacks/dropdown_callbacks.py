from dash import Input, Output, State
from utils.load_tiff import transformar_tiff
import plotly.graph_objects as go
from database.queries import visualizename_data
import dash

def register_dropdown_callbacks(app):
    @app.callback(
        Output("map-image", "figure"),
        [Input("tiff-dropdown", "value"),
         Input("add-button", "n_clicks")],
        [State("map-image", "figure")]
    )
    def update_map(selected_tiff, n_clicks, current_figure):
        # Verificar cuál de los inputs disparó el callback
        ctx = dash.callback_context

        if not ctx.triggered:
            # Si no ha habido un disparador, retorna el estado actual
            return current_figure

        # Comprobar cuál fue el input que disparó el callback
        trigger = ctx.triggered[0]['prop_id'].split('.')[0]

        # Si se seleccionó un TIFF en el dropdown
        if trigger == "tiff-dropdown" and selected_tiff:
            # Cargar el archivo TIFF seleccionado
            tiff_path = f"rockblast/App/data/{selected_tiff}.tif"
            tiff_base64, extent = transformar_tiff(tiff_path)
            
            # Definir el layout del gráfico para el TIFF
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

            # Retornar el gráfico vacío (sin puntos) al seleccionar un nuevo TIFF
            return go.Figure(layout=layout, data=[])

        # Si el desencadenante fue el botón "Agregar Puntos"
        if trigger == "add-button" and n_clicks:
            # Si ya se tiene un gráfico con un TIFF y se agregan puntos, solo se actualizan los puntos
            x_query, y_query = visualizename_data()
            # Verificar si los datos de los puntos son válidos
            if x_query and y_query:
                points = go.Scatter(
                    x=x_query,
                    y=y_query,
                    mode='markers',
                    marker=dict(size=6, color='blue'),
                    name='Puntos'
                )

                # Agregar los puntos a los datos de la figura actual
                current_data = current_figure.get('data', [])
                current_data.append(points)
                current_figure['data'] = current_data

            # Retornar la figura con puntos agregados
            return current_figure

        # Retornar el gráfico actual si no se ha hecho ninguna acción
        return current_figure
