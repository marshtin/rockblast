from dash import dcc, html
import geopandas as gpd
import plotly.graph_objs as go
from rasterio.plot import reshape_as_image
from database.queries import fetch_gps_data_to_geojson
from utils.load_tiff import transformar_tiff



main_layout = html.Div(
    className="container",
    style={'font-family': 'Noto Sans, sans-serif'},  # Estilo global de fuente
    children=[
        # Barra lateral de alertas
        html.Div(
            className="sidebar",
            children=[
                html.H2("ALERTAS"),
                
                # Contenedor de alertas con barra deslizadora
                html.Div(
                    className="alert-container",
                    children=[
                        html.Div(className="alert-item", children=[
                            html.Img(src="assets/pngs/icono_alerta.png", alt="Icono de alerta"),
                            html.Span("Camión 1 - Bajo")
                        ]),
                        html.Div(className="alert-item", children=[
                            html.Img(src="assets/pngs/icono_alerta.png", alt="Icono de alerta"),
                            html.Span("Camión 2 - Bajo")
                        ]),
                        html.Div(className="alert-item", children=[
                            html.Img(src="assets/pngs/icono_alerta.png", alt="Icono de alerta"),
                            html.Span("Camión 3 - Bajo")
                        ]),
                        html.Div(className="alert-item", children=[
                            html.Img(src="assets/pngs/icono_alerta.png", alt="Icono de alerta"),
                            html.Span("Camión 4 - Bajo")
                        ]),
                        html.Div(className="alert-item", children=[
                            html.Img(src="assets/pngs/icono_alerta.png", alt="Icono de alerta"),
                            html.Span("Camión 5 - Bajo")
                        ]),
                        html.Div(className="alert-item", children=[
                            html.Img(src="assets/pngs/icono_alerta.png", alt="Icono de alerta"),
                            html.Span("Camión 6 - Bajo")
                        ]),
                        html.Div(className="alert-item", children=[
                            html.Img(src="assets/pngs/icono_alerta.png", alt="Icono de alerta"),
                            html.Span("Camión 7 - Bajo")
                        ]),
                        html.Div(className="alert-item", children=[
                            html.Img(src="assets/pngs/icono_alerta.png", alt="Icono de alerta"),
                            html.Span("Camión 8 - Bajo")
                        ]),
                        html.Div(className="alert-item", children=[
                            html.Img(src="assets/pngs/icono_alerta.png", alt="Icono de alerta"),
                            html.Span("Camión 9 - Bajo")
                        ]),
                        html.Div(className="alert-item", children=[
                            html.Img(src="assets/pngs/icono_alerta.png", alt="Icono de alerta"),
                            html.Span("Camión 10 - Bajo")
                        ]),
                        html.Div(className="alert-item", children=[
                            html.Img(src="assets/pngs/icono_alerta.png", alt="Icono de alerta"),
                            html.Span("Camión 11 - Bajo")
                        ]),
                        html.Div(className="alert-item", children=[
                            html.Img(src="assets/pngs/icono_alerta.png", alt="Icono de alerta"),
                            html.Span("Camión 12 - Bajo")
                        ])
                    ]
                ),
                # Botones debajo del contenedor de alertas
                html.Div(
                    className="sidebar-buttons",
                    children=[
                        html.Button("Borrar"),
                        html.Button("Detalle")
                    ]
                )
            ]
        ),
    
        # Encabezado con filtros y Operadores
        html.Div(
            className="header",
            children=[
                html.Div(
                    className="filters",
                    children=[
                        html.H2("Filtros"),
                        dcc.Checklist(
                            options=[{"label": "Flota", "value": "fleet"}],
                            id="fleet-checklist",
                            className="dccChecklist"
                        ),
                        dcc.Checklist(
                            options=[{"label": "ID", "value": "id"}],
                            id="id-checklist",
                            className="dccChecklist"
                        ),
                        dcc.Input(type="text", placeholder="Buscar",className="dccInput"),
                        html.Button("+", className="add-button"),
                        dcc.Dropdown(
                            id="tiff-dropdown",
                            options=[
                                {"label": "REE.tif", "value": "REE"},
                                {"label": "RES.tif", "value": "RES"}
                            ],
                            placeholder="Seleccionar TIFF",
                            className="dccDropdown"
                        ),
                        html.Div(
                            className="operators",
                            children=[
                                html.H2("Reportes"),
                                dcc.Link("Tabla de Operadores", href="/tabla-operadores", className="redirection"),
                                dcc.Link("Generar Reporte", href="/reporte", className="redirection")
                            ]
                        )
                    ]
                )
            ]
        ),
        html.Div(
        className="map-container",
            children=[
                dcc.Graph(
                    id='map-image',
                    config={'responsive': True},  # Asegura que sea responsivo
                    style={'height': '100%', 'width': '100%'},  # Expande al tamaño del contenedor
                    figure={
                        'data': [],
                        'layout': go.Layout(
                            title='Visualización Inicial',
                            xaxis=dict(visible=False),
                            yaxis=dict(visible=False),
                            margin=dict(l=0, r=0, t=0, b=0),  # Márgenes mínimos
                            height=None,  # Usa todo el espacio disponible
                            width=None
                        )
                    }
                )
            ]
        )
    ]
)

