from dash import dcc, html
import geopandas as gpd
import plotly.graph_objs as go
from rasterio.plot import reshape_as_image
from utils.load_tiff import transformar_tiff

# Lista de alertas (camiones con velocidad baja)
alertas = [
    "Camión 1 - Hola", "Camión 2 - Cómo", "Camión 3 - Estás", 
    "Camión 4 - Bajo", "Camión 5 - Bajo", "Camión 6 - Bajo", 
    "Camión 7 - Bajo", "Camión 8 - Bajo", "Camión 9 - Bajo", 
    "Camión 10 - Bajo", "Camión 11 - Bajo", "Camión 12 - Bajo"
]

camiones = [
    "gps_c07", "gps_c130", "gps_c15", "gps_c17", 
    "gps_c37", "gps_c49", "gps_c56"
]

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
                            html.Span(alerta)
                        ]) for alerta in alertas
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
                        dcc.Dropdown(
                            id="camion-dropdown",
                            options=[
                                {"label": camion, "value": camion}
                                for camion in camiones
                            ],
                            placeholder="Seleccionar Camión",
                            className="dccDropdown"
                        ),
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
                                html.Button("Agregar Puntos", className="add-button", id="add-button"),
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

