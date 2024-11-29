from dash import Input, Output, State
from utils.load_tiff import transformar_tiff
from utils.clusters import create_and_save_clusters, generate_random_colors
from utils.point_colors import generate_point_colors
from database.queries import *
import plotly.graph_objects as go
from database.queries import puntos_flota
from components.main_layout import camiones
import dash
import numpy as np

def register_dropdown_callbacks(app):
    @app.callback(
        Output("map-image", "figure"),
        [Input("tiff-dropdown", "value"),
         Input("camion-dropdown", "value"),
         Input("add-map-points-button", "n_clicks"),
         Input("delete-map-points-button", "n_clicks"),
         Input('cluster-button', "n_clicks")],
        [State("map-image", "figure"), State("points-cleared", "data")]
    )
    def update_map(selected_tiff, selected_camion, n_clicks_add, n_clicks_delete, n_clicks_cluster, current_figure, points_cleared):
        # Verificar cuál de los inputs disparó el callback
        ctx = dash.callback_context

        if not ctx.triggered:
            return current_figure

        # Comprobar cuál fue el input que disparó el callback
        trigger = ctx.triggered[0]['prop_id'].split('.')[0]

        # Convert current_figure a go.Figure object si existe, o inicializar uno nuevo
        if current_figure:
            current_figure = go.Figure(current_figure)
        else:
            current_figure = go.Figure()

        # Si se seleccionó un TIFF en el dropdown
        if trigger == "tiff-dropdown" and selected_tiff:
            tiff_path = f"rockblast/App/data/{selected_tiff}.tif"
            tiff_base64, extent = transformar_tiff(tiff_path)

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
            return go.Figure(layout=layout, data=[])

        # Si se presionó el botón "Agregar Puntos"
        if trigger == "add-map-points-button" and n_clicks_add:
            if selected_camion:
                # Recuperar los puntos de flota
                x_query, y_query, s_query = puntos_flota(selected_camion)
                
                if x_query and y_query and s_query:
                    # Generar colores únicos para cada camión
                    color_map = dict(zip(camiones, generate_point_colors(len(camiones))))
                    # Texto para mostrar velocidad en el tooltip
                    tooltips = [f"Velocidad: {speed} km/h" for speed in s_query]

                    points = go.Scatter(
                        x=x_query,
                        y=y_query,
                        mode='markers',
                        marker=dict(
                            size= 8,  # Tamaño fijo
                            color=color_map[selected_camion],  # Color dinámico basado en el camión
                            opacity=0.8
                        ),
                        text=tooltips,  # Información mostrada en el tooltip
                        hoverinfo='text',  # Muestra únicamente el texto en el tooltip
                        name=f'Puntos Camión {selected_camion}'
                    )
                    current_figure.add_trace(points)
                    

            return current_figure

        # Si se presionó el botón "Borrar Puntos"
        if trigger == "delete-map-points-button" and n_clicks_delete:
            new_data = [
                trace for trace in current_figure.data
                if not (trace.name and trace.name.startswith('Puntos Camión'))
            ]
            current_figure.data = new_data
            return current_figure
    
        # Si se presionó el botón "Actualizar Clusters"
        if trigger == "cluster-button" and n_clicks_cluster:
            query = "SELECT time, latitude, longitude, elevation, speed FROM sandbox.gps_c07 ORDER BY time"
            df, cluster_info = create_and_save_clusters(query)
            colors = generate_random_colors(len(df['cluster'].unique()))

            for i, cluster in enumerate(df['cluster'].unique()):
                cluster_data = df[df['cluster'] == cluster]
                points = cluster_data[['longitude', 'latitude']].values
                hull = cluster_info[cluster]['convex_hull']
                hull_points = points[hull.vertices]
                hull_points = np.append(hull_points, [hull_points[0]], axis=0)

                current_figure.add_trace(go.Scatter(
                    x=hull_points[:, 0],
                    y=hull_points[:, 1],
                    mode='lines',
                    name=f'Cluster {cluster}',
                    line=dict(color='black'),
                    fill='toself',
                    fillcolor=colors[i],
                    visible=True,
                    customdata=['cluster']
                ))

            current_figure.update_layout(
                title='GPS Data Clustering with Convex Hull Boundaries',
                xaxis_title='Longitude',
                yaxis_title='Latitude'
            )
            return current_figure

        return current_figure

    # Define the callback para alternar la visibilidad de clusters
    @app.callback(
        [Output("map-image", "figure", allow_duplicate=True), Output("clusters-visible", "data")],
        [Input("toggle-clusters-button", "n_clicks")],
        [State("map-image", "figure"), State("clusters-visible", "data")],
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
    
    # Callback para actualizar el estado de "puntos limpiados"
    @app.callback(
        Output("points-cleared", "data"),
        [Input("delete-map-points-button", "n_clicks")],
        [State("points-cleared", "data")]
    )
    def update_points_cleared(n_clicks_delete, points_cleared):
        if n_clicks_delete:
            return True
        return points_cleared