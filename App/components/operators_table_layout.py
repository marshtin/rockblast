from dash import html

tabla_operadores_layout = html.Div(
    className="operators-tab-container",
    children=[
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
                html.Button("Actualizar Resumen", className="refresh-button", id="refresh-operadores"),
                html.Button("Descargar", className="download-button", id="download-operadores-report")
            ]
        ),
        html.Div(
            id='tables-container',
            className="tables-container"  # Clase para ajustar el contenedor
        )
    ]
)
