from dash import Input, Output, dcc, dash_table, html
from database.queries import *
from database.queries import get_data_from_db_combined
from dash import Input, Output, dcc, html
import pandas as pd
from io import BytesIO


def register_operator_callbacks(app):
    @app.callback(
        Output('tables-container', 'children'),  # Contenedor donde se mostrarán las tablas
        [Input('refresh-operadores', 'n_clicks'),  # Botón para refrescar los datos manualmente
         Input('url', 'pathname')]  # Detectar si la ruta es "/tabla-operadores"
    )
    def update_table(n_clicks, pathname):
        # Verificar si estamos en la página correcta
        if pathname == "/tabla-operadores":
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
            
        # Devolver un Div vacío si el botón no ha sido presionado y no estamos en la página "/tabla-operadores"
        return html.Div()

# Configurar la aplicación principal



def register_download_callback(app):
    @app.callback(
        Output("download-excel", "data"),  # Componente de descarga
        Input("download-operadores-report", "n_clicks")  # Botón que activa la descarga
    )
    def download_excel(n_clicks):
        print("entro")
        if n_clicks and n_clicks > 0:
            try:
 
                # Obtiene los datos de las consultas
                df_top_load, df_top_dumps, df_time_extremes = get_data_from_db_combined()

                # Crear un archivo Excel con varias hojas
                output = BytesIO()

                with pd.ExcelWriter(output, engine="xlsxwriter") as writer:

                    df_top_load.to_excel(writer, index=False, sheet_name="Ranking Carga")

                    df_top_dumps.to_excel(writer, index=False, sheet_name="Ranking Descarga")

                    df_time_extremes.to_excel(writer, index=False, sheet_name="Comparación Tiempos")

                # Asegurar que el buffer se reinicie para ser leído
                output.seek(0)

                # Preparar el archivo para la descarga
                return dcc.send_bytes(output.getvalue(), filename="ranking_operadores.xlsx")
            
            except Exception as e:
                # Manejar errores (puedes agregar logs aquí si es necesario)
                return dcc.send_string(f"Error al generar el archivo: {str(e)}", filename="error.txt")