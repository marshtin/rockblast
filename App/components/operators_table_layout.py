from dash import dcc, html

tabla_operadores_layout = html.Div(
    className="table-section",  # Aplicar la clase principal para el contenedor de tablas
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
                html.Button("Resumen de Operadores", className="add-button", id="add-operadores")
            ]
        ),
        
        # Contenedor de las tablas
        html.Div(
            className="tables-container",  # Clase para organizar las tablas
            children=[
                # Contenedor para las tablas dinámicas generadas por Dash
                html.Div(
                    id='table-container',  # Este ID se utiliza en el callback para insertar las tablas
                    className="table-container"  # Clase individual para las tablas
                )
            ]
        )
    ]
)
