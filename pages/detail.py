import dash
from dash import html
import dash_bootstrap_components as dbc
import json
import requests

dash.register_page(__name__, path_template="/tracability/<recolte_nb>")


details = []


API_URL = f'http://127.0.0.1:8000/api/actions'


with open('auth.json') as auth_file:
    auth_json = json.loads(auth_file.read())
    auth = (auth_json["username"], auth_json["password"])



def layout(recolte_nb=None):
    return display_details(recolte_nb)


# Fetch specific recolte in the API
def get_details_from_recolte_nb(recolte_nb):
    return json.loads(requests.get(
        f'{API_URL}/recolte-nb/{recolte_nb}', auth=auth).text)


def display_details(recolte_nb):
    actions = get_details_from_recolte_nb(recolte_nb)
    return dbc.Container(
            [
                dbc.Row(
                ),
            ]
         )
