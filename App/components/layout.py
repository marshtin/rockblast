from dash import dcc, html
from dash.dependencies import Input, Output

layout = html.Div(
    className="container",
    style={'font-family': 'Noto Sans, sans-serif'},
    children=[

        # Componente para manejar la URL
        dcc.Location(id='url', refresh=False),  # Detecta las rutas
        
        html.Div(id='page-content')  # Aquí cambiará el contenido dependiendo de la ruta
    ]
)
