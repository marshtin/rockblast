from dash import Input, Output, State
from utils.load_tiff import transformar_tiff
from utils.clusters import create_and_save_clusters, generate_random_colors
from utils.point_colors import generate_point_colors
from database.queries import *
import plotly.graph_objects as go
from database.queries import puntos_flota
from components.main_layout import alertas
import dash
import numpy as np
from dash import html, dcc

# Callback to update the alert container

def register_alerts_callbacks(app):
    @app.callback(
        Output('alert-container', 'children'),
        Input('alert-store', 'data')
    )
    def update_alerts(alertas):
        return [
            html.Div(
                className="alert-item",
                children=[
                    html.Img(src="assets/pngs/icono_alerta.png", alt="Icono de alerta"),
                    html.Span(alerta)
                ]
            ) for alerta in alertas
        ]