from dash import Input, Output, State
from utils.load_tiff import transformar_tiff
from utils.clusters import create_and_save_clusters, generate_random_colors
from database.queries import *
import plotly.graph_objects as go
from database.queries import visualizename_data
import dash
import numpy as np

def register_dropdown_callbacks(app):
    @app.callback(
        Output("map-image", "figure"),
        [Input("tiff-dropdown", "value"),
         Input("camion-dropdown", "value"),  # Añadir el dropdown de camión
         Input("add-button", "n_clicks"),
         Input('cluster-button', 'n_clicks')],
        [State("map-image", "figure")]
    )
    def update_map(selected_tiff, selected_camion, n_clicks, n_clicks_cluster, current_figure):
        # Verificar cuál de los inputs disparó el callback
        ctx = dash.callback_context

        if not ctx.triggered:
            # Si no ha habido un disparador, retorna el estado actual
            return current_figure

        # Comprobar cuál fue el input que disparó el callback
        trigger = ctx.triggered[0]['prop_id'].split('.')[0]

        # Convert current_figure to a go.Figure object
        if current_figure:
            current_figure = go.Figure(current_figure)
        else:
            current_figure = go.Figure()

        # Si se seleccionó un TIFF en el dropdown
        if trigger == "tiff-dropdown" and selected_tiff:
            # Cargar el archivo TIFF seleccionado
            tiff_path = f"App/data/{selected_tiff}.tif"
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
            if selected_camion:  # Verifica si se seleccionó un camión
                # Llamar a visualizename_data con el camión seleccionado
                x_query, y_query = visualizename_data(selected_camion)  # Pasar el camión seleccionado

                # Verificar si los datos de los puntos son válidos
                if x_query and y_query:
                    points = go.Scatter(
                        x=x_query,
                        y=y_query,
                        mode='markers',
                        marker=dict(size=6, color='blue'),
                        name=f'Puntos Camión {selected_camion}'  # Nombre del camión en la leyenda
                    )

                    # Agregar los puntos a los datos de la figura actual
                    current_data = current_figure.data
                    current_data.append(points)
                    current_figure.data = current_data

            # Retornar la figura con puntos agregados
            return current_figure

        # Si el desencadenante fue el botón "Actualizar Clusters"
        if trigger == "cluster-button" and n_clicks_cluster:
            query = "SELECT time, latitude, longitude, elevation, speed FROM sandbox.gps_c07 ORDER BY time"
            df, cluster_info = create_and_save_clusters(query)

            # Generate random colors for each cluster
            colors = generate_random_colors(len(df['cluster'].unique()))

            for i, cluster in enumerate(df['cluster'].unique()):
                cluster_data = df[df['cluster'] == cluster]

                # Plot the Convex Hull
                points = cluster_data[['longitude', 'latitude']].values
                hull = cluster_info[cluster]['convex_hull']
                hull_points = points[hull.vertices]
                hull_points = np.append(hull_points, [hull_points[0]], axis=0)  # Close the hull

                current_figure.add_trace(go.Scatter(
                    x=hull_points[:, 0],
                    y=hull_points[:, 1],
                    mode='lines',
                    name=f'Cluster {cluster}',
                    line=dict(color='black'),
                    fill='toself',
                    fillcolor=colors[i],  # Use the generated color
                    visible=True,  # Ensure the clusters are initially visible
                    customdata=['cluster']  # Add a custom identifier to the cluster traces
                ))

            current_figure.update_layout(
                title='GPS Data Clustering with Convex Hull Boundaries',
                xaxis_title='Latitude',
                yaxis_title='Longitude'
            )
            
            return current_figure

        # Retornar el gráfico actual si no se ha hecho ninguna acción
        return current_figure
    
    # Define the callback to toggle the visibility of clusters
    @app.callback(
        Output('map-image', 'figure', allow_duplicate=True),
        Output('clusters-visible', 'data'),
        Input('toggle-clusters-button', 'n_clicks'),
        State('map-image', 'figure'),
        State('clusters-visible', 'data'),
        prevent_initial_call=True
    )
    def toggle_clusters(n_clicks, figure, clusters_visible):
        if n_clicks > 0:
            new_visibility = not clusters_visible
            for trace in figure['data']:
                if 'customdata' in trace and trace['customdata'] == ['cluster']:
                    trace['visible'] = new_visibility

            return figure, new_visibility

        return figure, clusters_visible
