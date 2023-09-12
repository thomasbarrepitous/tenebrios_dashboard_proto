import dash
from dash import html
import dash_bootstrap_components as dbc
import json
import requests
import dash_mantine_components as dmc
import pandas as pd


dash.register_page(__name__, path_template="/tracability/action/<action_id>")


API_URL = f"http://127.0.0.1:8000/api/actions"

with open("auth.json") as auth_file:
    auth_json = json.loads(auth_file.read())
    auth = (auth_json["username"], auth_json["password"])


def get_action(action_id: str) -> dict:
    r = requests.get(f"{API_URL}/{action_id}", auth=auth)
    if r.status_code == 200:
        action = json.loads(r.text)
        return action
    return {}


def display_layout(action: dict):
    return html.P(f"{action}")


def layout(action_id):
    action = get_action(action_id)
    return display_layout(action)
