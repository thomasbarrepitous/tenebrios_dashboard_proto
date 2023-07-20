import dash
from dash import Dash, html, dcc, Output, Input, dash_table
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import requests
import json


app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.FLATLY], suppress_callback_exceptions=True,
           meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,'}])
server = app.server
app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    html.H1('TenebriOS Project'),
    html.Div(
        [
            html.Div(
                dcc.Link(
                    f"{page['name']} - {page['path']}", href=page["relative_path"]
                )
            )
            for page in dash.page_registry.values()
        ]
    ),
    dash.page_container
])


if __name__ == '__main__':
    app.run_server(debug=True)
