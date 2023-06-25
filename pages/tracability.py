import dash
from dash import callback, html, dcc, Output, Input, dash_table
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import requests
import json


dash.register_page(__name__)


layout = []
