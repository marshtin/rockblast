from dash import dcc, html

tabla_operadores_layout = html.Div(
    children=[
        # Encabezado de la página de tabla de operadores
        html.Div(
            className="operators-tab-header",
            children=[
                html.Div(
                    className="redirection",
                    children=html.A(
                        href="/",
                        children=[
                            html.Img(src="assets/pngs/back.png", alt="icono de regreso"),
                            "Volver al Dashboard"
                        ]
                    )
                ),
                html.H2("Tabla de Operadores"),
            ]
        ),
        
        # Aquí las tablas de operadores (como ya lo tienes)
        html.Div(
            className="tables-container",
            children=[
                # Tu código para las tablas de operadores
            ]
        )
    ]
)
