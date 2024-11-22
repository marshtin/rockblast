from dash import dcc, html
import geopandas as gpd
import plotly.graph_objs as go
from rasterio.plot import reshape_as_image





points = gpd.read_file("Prueba1.geojson")


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
        # Contenedor del mapa
        html.Div(
            className="map-container",
            children=[
                dcc.Graph(
        id='map1',
        figure={
            'data': [
                go.Scatter(
                    x=points.geometry.x,
                    y=points.geometry.y,
                    mode='markers',
                    marker=dict(size=6, color='blue'),
                    name='Puntos'
                )
            ],
            'layout': go.Layout(
                title='TIFF con Puntos - Archivo 1',
                images=[{
                    'source': f"data:image/png;base64,{tiff_base64_1}",
                    'xref': "x",
                    'yref': "y",
                    'x': extent_1[0],
                    'y': extent_1[3],
                    'sizex': extent_1[1] - extent_1[0],
                    'sizey': extent_1[3] - extent_1[2],
                    'sizing': "stretch",
                    'layer': "below"
                }],
                xaxis=dict(range=[extent_1[0], extent_1[1]], visible=False, scaleanchor="y", scaleratio=1),
                yaxis=dict(range=[extent_1[2], extent_1[3]], visible=False),
                showlegend=True
            )
        },
        style={'width': '100vw', 'height': '100vh'}
    ),
                html.Img(id="map-image", className="map-image", src="")
            ]
        )
    ]
)
