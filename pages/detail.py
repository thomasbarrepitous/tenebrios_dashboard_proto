import dash
from dash import html
import dash_bootstrap_components as dbc
import json
import requests
import dash_mantine_components as dmc
from datetime import datetime


dash.register_page(__name__, path_template="/tracability/<recolte_nb>")


actions = []

API_URL = f"http://127.0.0.1:8000/api/actions"


with open("auth.json") as auth_file:
    auth_json = json.loads(auth_file.read())
    auth = (auth_json["username"], auth_json["password"])


def layout(recolte_nb=None):
    return display_layout(recolte_nb)


def ctype_to_name(key: int) -> str | None:
    map = {
        11: "Mise en culture",
        12: "Nourrisage Humide",
        13: "Nourrisage Son",
        14: "Recolte",
        # 15: "Tamisage",
    }
    return map.get(key)


# Fetch specific recolte in the API
def get_details_from_recolte_nb(recolte_nb):
    return json.loads(
        requests.get(f"{API_URL}/recolte-nb/{recolte_nb}", auth=auth).text
    )


def action_item_component(action):
    action_date = datetime.strptime(action["date"], "%Y-%m-%dT%H:%M:%S.%fZ")
    return dmc.AccordionItem(
        [
            dmc.AccordionControl(
                f'{ctype_to_name(action["polymorphic_ctype"])} du {action_date.strftime("%B %d, %Y")}'
            ),
            dmc.AccordionPanel(action["date"]),
        ],
        value=action["date"],
    )


def display_top_title(actions):
    return [dbc.Row(html.H2(actions[0]["recolte_nb"], className="text-center"))]


def display_indicators_layout():
    return [
        dbc.Row(dmc.Divider(label=html.H3("Indicateurs"), labelPosition="center")),
        dbc.Row(
            html.H4("Indicateurs globaux"),
            className="text-center text-decoration-underline",
        ),
        dbc.Row(
            [
                dbc.Col([html.H4(f"Date de mise en culture"), html.P("13 aout 3932")]),
                dbc.Col([html.H4(f"Date de recolte"), html.P("14 aout 1093")]),
                dbc.Col([html.H4(f"Nombre de bacs"), html.P("111")]),
                dbc.Col([html.H4(f"Quantite recoltee"), html.P("11")]),
            ]
        ),
        dbc.Row(
            html.H4("Indicateurs moyens"),
            className="text-center text-decoration-underline",
        ),
        dbc.Row(
            [
                dbc.Col([html.H4(f"IWM à la récolte"), html.P("13 aout 3932")]),
                dbc.Col([html.H4(f"Son total donné"), html.P("13 aout 3932")]),
                dbc.Col(
                    [
                        html.H4(f"Nourriture humide totale donnée"),
                        html.P("13 aout 3932"),
                    ]
                ),
                dbc.Col([html.H4(f"Feed Ratio Conversion "), html.P("13 aout 3932")]),
                dbc.Col(
                    [html.H4(f"Croissance journalière moyenne"), html.P("13 aout 3932")]
                ),
                dbc.Col([html.H4(f"Assimilation moyenne "), html.P("13 aout 3932")]),
            ]
        ),
    ]


def display_historical_actions_layout(actions):
    return [
        dbc.Row(
            dmc.Divider(label=html.H3("Toutes les actions"), labelPosition="center")
        ),
        dbc.Row(
            [dmc.Accordion(action_item_component(action)) for action in actions],
        ),
    ]


def display_layout(recolte_nb):
    actions = get_details_from_recolte_nb(recolte_nb)
    return dbc.Container(
        display_top_title(actions)
        + display_indicators_layout()
        + display_historical_actions_layout(actions)
    )
