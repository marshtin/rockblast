from dash import Input, Output
from database.queries import *
from database.queries import get_data_from_db_combined
from dash import dash_table, html

def register_operator_callbacks(app):
    @app.callback(
        Output('tables-container', 'children'),  # Contenedor donde se mostrarán las tablas
        Input('refresh-operadores', 'n_clicks')  # Botón que activa el callback
    )
    def update_table(n_clicks):
        # Verificar si se presionó el botón
        if n_clicks and n_clicks > 0:
            try:
                # Obtener los datos de las tres consultas
                df_load, df_dumps, df_time_extremes = get_data_from_db_combined()

                # Verificar si se obtuvieron datos
                if not df_load.empty and not df_dumps.empty and not df_time_extremes.empty:
                    # Crear y devolver las tablas con los datos
                    return html.Div([
                        html.H3("Ranking de Carga"),  # Encabezado para la primera tabla
                        dash_table.DataTable(
                            id="table-loads",
                            columns=[
                                {"name": "ID del Operador", "id": "truck_operator_id"},
                                {"name": "Nombre Completo", "id": "full_name"},
                                {"name": "Carga Promedio", "id": "average_payload"}
                            ],
                            data=df_load.to_dict('records'),  # Convierte el DataFrame a lista de diccionarios
                            style_table={'overflowX': 'auto'},
                            style_cell={
                                'textAlign': 'left',
                                'padding': '10px',
                                'fontFamily': 'Arial, sans-serif',
                            },
                            style_header={
                                'backgroundColor': 'lightgrey',
                                'fontWeight': 'bold'
                            }
                        ),
                        html.H3("Ranking de Descargas"),  # Encabezado para la segunda tabla
                        dash_table.DataTable(
                            id="table-dumps",
                            columns=[
                                {"name": "ID del Operador", "id": "truck_operator_id"},
                                {"name": "Nombre Completo", "id": "full_name"},
                                {"name": "Carga Promedio", "id": "average_payload"}
                            ],
                            data=df_dumps.to_dict('records'),  # Convierte el DataFrame a lista de diccionarios
                            style_table={'overflowX': 'auto'},
                            style_cell={
                                'textAlign': 'left',
                                'padding': '10px',
                                'fontFamily': 'Arial, sans-serif',
                            },
                            style_header={
                                'backgroundColor': 'lightgrey',
                                'fontWeight': 'bold'
                            }
                        ),
                        html.H3("Comparación entre el mejor y el peor operador"),  # Encabezado para la tercera tabla
                        dash_table.DataTable(
                            id="table-time-extremes",
                            columns=[
                                {"name": "Operador con Menor Tiempo", "id": "operador_con_menor_tiempo"},
                                {"name": "Operador con Mayor Tiempo", "id": "operador_con_mayor_tiempo"},
                                {"name": "Diferencia Porcentual", "id": "diferencia_porcentual"}
                            ],
                            data=df_time_extremes.to_dict('records'),  # Convierte el DataFrame a lista de diccionarios
                            style_table={'overflowX': 'auto'},
                            style_cell={
                                'textAlign': 'left',
                                'padding': '10px',
                                'fontFamily': 'Arial, sans-serif',
                            },
                            style_header={
                                'backgroundColor': 'lightgrey',
                                'fontWeight': 'bold'
                            }
                        )
                    ])
                else:
                    # Mensaje si alguna consulta no devolvió datos
                    return html.Div("No se encontraron datos para mostrar.", style={'color': 'red'})

            except Exception as e:
                # Manejar errores durante la ejecución
                return html.Div(f"Error al cargar los datos: {str(e)}", style={'color': 'red'})
        
        # Devolver un Div vacío si el botón no ha sido presionado
        return html.Div()