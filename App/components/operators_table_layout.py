from dash import dcc, html

tabla_operadores_layout = html.Div(
    children=[
        # Encabezado de la página de tabla de operadores
        html.Div(
            className="operators-header",
            children=[
                html.H2("Tabla de Operadores"),
                html.A("Volver a la página principal", href="/")
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
