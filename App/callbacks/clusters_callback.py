from dash import Input, Output, dcc, html, State
from utils.clusters import *
import plotly.graph_objs as go

"""
def register_update_clusters(app):
    @app.callback(
        Output('cluster-image', 'figure'),
        Input('cluster-button', 'n_clicks')
    )
    def update_clusters(n_clicks):
        if n_clicks > 0:
            query = "SELECT time, latitude, longitude, elevation, speed FROM sandbox.gps_c07 ORDER BY time"
            df, cluster_info = create_and_save_clusters(query)

            # Create the plotly figure
            fig = go.Figure()

            # Generate random colors for each cluster
            colors = generate_random_colors(len(df['cluster'].unique()))

            for i, cluster in enumerate(df['cluster'].unique()):
                cluster_data = df[df['cluster'] == cluster]

                # Plot the Convex Hull
                points = cluster_data[['longitude', 'latitude']].values
                hull = cluster_info[cluster]['convex_hull']
                hull_points = points[hull.vertices]
                hull_points = np.append(hull_points, [hull_points[0]], axis=0)  # Close the hull

                fig.add_trace(go.Scatter(
                    x=hull_points[:, 0],
                    y=hull_points[:, 1],
                    mode='lines',
                    name=f'Cluster {cluster}',
                    line=dict(color='black'),
                    fill='toself',
                    fillcolor=colors[i]  # Use the generated color
                ))

            fig.update_layout(
                title='GPS Data Clustering with Convex Hull Boundaries',
                xaxis_title='Latitude',
                yaxis_title='Longitude'
            )
            
            return fig

        # Return an empty figure if the button has not been clicked
        return go.Figure()

    # Define the callback to toggle the visibility of clusters
    @app.callback(
        Output('cluster-image', 'figure', allow_duplicate=True),
        Output('clusters-visible', 'data'),
        Input('toggle-clusters-button', 'n_clicks'),
        State('cluster-image', 'figure'),
        State('clusters-visible', 'data'),
        prevent_initial_call=True
    )
    def toggle_clusters(n_clicks, figure, clusters_visible):
        if n_clicks > 0:
            new_visibility = not clusters_visible
            for trace in figure['data']:
                trace['visible'] = new_visibility

            return figure, new_visibility

        return figure, clusters_visible
        """