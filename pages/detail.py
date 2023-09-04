import dash
from dash import html
import dash_bootstrap_components as dbc
import json
import requests
import dash_mantine_components as dmc
from datetime import datetime


dash.register_page(__name__, path_template="/tracability/<recolte_nb>")


details = []

API_URL = f"http://127.0.0.1:8000/api/actions"


with open("auth.json") as auth_file:
    auth_json = json.loads(auth_file.read())
    auth = (auth_json["username"], auth_json["password"])


def layout(recolte_nb=None):
    return display_details(recolte_nb)


def map_values_polymorphictype(key: int) -> str | None:
    map = {
        11: "Mise en culture",
        12: "Nourrisage Humide",
        13: "Nourrisage Son",
        14: "Recolte",
        15: "Tamisage",
    }
    return map.get(key)


# Fetch specific recolte in the API
def get_details_from_recolte_nb(recolte_nb):
    return json.loads(
        requests.get(f"{API_URL}/recolte-nb/{recolte_nb}", auth=auth).text
    )


def display_detail(action):
    action_date = datetime.strptime(action["date"], "%Y-%m-%dT%H:%M:%S.%fZ")
    return dmc.AccordionItem(
        [
            dmc.AccordionControl(
                f'{map_values_polymorphictype(action["polymorphic_ctype"])} du {action_date.strftime("%B %d, %Y")}'
            ),
            dmc.AccordionPanel(action["date"]),
        ],
        value=action["date"],
    )


def display_details(recolte_nb):
    actions = get_details_from_recolte_nb(recolte_nb)
    return dbc.Container(
        [
            dbc.Row(
                dbc.Col(
                    html.H2(actions[0]["recolte_nb"]), width={"size": 3, "offset": 5}
                )
            ),
            dbc.Row(dmc.Divider(label=html.H3("Indicateurs"), labelPosition="center")),
            dbc.Row(
                [
                    dbc.Col(html.H4("okdawkdwa")),
                    dbc.Col(html.H4("daiwj")),
                ]
            ),
            dbc.Row(
                dmc.Divider(label=html.H3("Toutes les actions"), labelPosition="center")
            ),
            dbc.Row(
                [dmc.Accordion(display_detail(action)) for action in actions],
            ),
        ]
    )
