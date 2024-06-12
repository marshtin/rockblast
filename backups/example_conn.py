import pandas as pd
import pandas.io.sql as sqlio
from connect import *
import warnings
import plotly.graph_objs as go

conn = connect()

df = sqlio.read_sql_query("SELECT * FROM sandbox.gps_c07", conn)

close_conn(conn)
