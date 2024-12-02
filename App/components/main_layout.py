from dash import dcc, html
import plotly.graph_objs as go
from database.queries import nombres_flota

# Lista de alertas (camiones con velocidad baja)
alertas = []

camiones = [
    "gps_c07", "gps_c15", "gps_c17", 
    "gps_c37", "gps_c49", "gps_c56"
]

df_nombres_flota = nombres_flota()

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
                    id="alert-container",
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
                        dcc.Dropdown(
                            id="tiff-dropdown",
                            options=[
                                {"label": "REE.tif", "value": "REE"},
                                {"label": "RES.tif", "value": "RES"}
                            ],
                            placeholder="Seleccionar TIFF",
                            className="dccDropdown"
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
                        dcc.Dropdown(
                            id="flota-dropdown",
                            options=[
                                {"label": flota, "value": flota}
                                for flota in df_nombres_flota
                            ],
                            placeholder="Seleccionar Flota",
                            className="dccDropdown"
                        ),
                        html.Button("Agregar Puntos", className="add-button", id="add-map-points-button"),
                        html.Button("Quitar Puntos", className="delete-button", id="delete-map-points-button"),
                        html.Div(
                            className="operators",
                            children=[
                                dcc.Store(id="points-cleared", data=False), #Indica si los puntos se han borrado recientemente
                                html.H2("Reportes"),
                                dcc.Link("Tabla de Operadores", href="/tabla-operadores", className="redirection"),
                                dcc.Link("Generar Reporte", href="/reporte", className="redirection")
                            ]
                        ),
                        html.Div(
                            className="clusters",
                            children=[
                                html.Button("Generar clusters", className="cluster-button", id="cluster-button", n_clicks=0),
                                html.Button('Ocultar/Mostrar', className="cluster-button", id='toggle-clusters-button', n_clicks=0),
                                dcc.Store(id='clusters-visible', data=True)  # Store to keep track of clusters visibility
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
        ),
        # Store para mantener la lista de alertas
        dcc.Store(id='alertas-store', data=alertas)
    ]
)

