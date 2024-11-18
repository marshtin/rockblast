from dash import dcc, html

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
    
        # Contenedor principal del mapa y filtros
        html.Div(
            className="map-container",
            children=[
                # Filtros y operadores
                html.Div(
                    className="header",
                    children=[
                        html.Div(
                            className="filters",
                            children=[
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
                                        {"label": "REES.tif", "value": "RES"}
                                    ],
                                    placeholder="Seleccionar TIFF",
                                    className="dccDropdown"
                                )
                            ]
                        ),
                        html.Div(
                            className="operators",
                            children=[
                                dcc.Link("Tabla de Operadores", href="/tabla-operadores", className="redirection"),
                                dcc.Link("Generar Reporte", href="/reporte", className="redirection")
                            ]
                        )
                    ]
                ),
            
                 #Imagen del mapa
                 html.Img(id="map-image", className="map-image", src="")
            ]
        )
    ]
)
