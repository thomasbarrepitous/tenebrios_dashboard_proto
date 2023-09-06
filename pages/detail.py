import dash
from dash import html
import dash_bootstrap_components as dbc
import json
import requests
import dash_mantine_components as dmc
from datetime import datetime
import pandas as pd

dash.register_page(__name__, path_template="/tracability/<recolte_nb>")


API_URL = f"http://127.0.0.1:8000/api/actions"

with open("auth.json") as auth_file:
    auth_json = json.loads(auth_file.read())
    auth = (auth_json["username"], auth_json["password"])


def layout(recolte_nb=None):
    return display_layout(recolte_nb)


# Fetch specific recolte in the API
def get_details_from_recolte_nb(recolte_nb):
    """Fetch all actions for given recolte_nb."""
    return json.loads(
        requests.get(f"{API_URL}/recolte-nb/{recolte_nb}", auth=auth).text
    )


def get_date_mec_from_actions_df(actions_df: pd.DataFrame) -> datetime:
    """Return the date of the Mise En Culture."""
    return actions_df.query("resourcetype == 'MiseEnCulture'")["date"].values[0]


def get_date_recolte_from_actions_df(actions_df: pd.DataFrame) -> datetime:
    """Return the date of the Recolte."""
    return actions_df.query("resourcetype == 'Recolte'")["date"].values[0]


def get_nb_bacs_from_actions_df(actions_df: pd.DataFrame) -> int:
    pass


def get_qte_recolte_from_actions_df(actions_df: pd.DataFrame) -> int:
    return sum(
        actions_df.query("resourcetype == 'Recolte'")["harvested_quantity"].values
    )


def get_total_son_from_actions_df(actions_df: pd.DataFrame) -> int:
    return sum(
        actions_df.query("resourcetype == 'NourrisageSon'")["given_quantity"].values
    )


def get_total_nourriture_humide_from_actions_df(actions_df: pd.DataFrame) -> int:
    return sum(
        actions_df.query("resourcetype == 'NourrisageHumide'")["given_quantity"].values
    )


def get_feed_ratio_conversion_from_actions_df(actions_df: pd.DataFrame) -> int:
    # return get_total_son_from_actions_df(actions_df) / get_qte_recolte_from_actions_df(
    #     actions_df
    # )
    pass


def get_croissance_journaliere_moyenne_from_actions_df(actions_df: pd.DataFrame) -> int:
    pass


def get_assimilation_moyenne_from_actions_df(actions_df: pd.DataFrame) -> int:
    pass


def calculate_indicators(actions_df: pd.DataFrame) -> dict:
    map = {
        # Indicateurs Totaux / Globaux
        "date_mec": get_date_mec_from_actions_df(actions_df),
        "date_recolte": get_date_recolte_from_actions_df(actions_df),
        "nb_bacs": get_nb_bacs_from_actions_df(actions_df),
        "qte_recolte": get_qte_recolte_from_actions_df(actions_df),
        # Indicateurs Moyens
        "total_son": get_total_son_from_actions_df(actions_df),
        "total_nourriture_humide": get_total_nourriture_humide_from_actions_df(
            actions_df
        ),
        "feed_ratio_conversion": get_feed_ratio_conversion_from_actions_df(actions_df),
        "croissance_journaliere_moyenne": get_croissance_journaliere_moyenne_from_actions_df(
            actions_df
        ),
        "assimilation_moyenne": get_assimilation_moyenne_from_actions_df(actions_df),
    }
    print(map)
    return map


def action_item_component(action):
    """Build one item of the full historical actions accordion."""
    action_date = datetime.strptime(action["date"], "%Y-%m-%dT%H:%M:%S.%fZ")
    return dmc.AccordionItem(
        [
            dmc.AccordionControl(
                f'{action["resourcetype"]} du {action_date.strftime("%B %d, %Y")}'
            ),
            dmc.AccordionPanel(f"{action}"),
        ],
        value=action["date"],
    )


def display_top_title(actions):
    return [dbc.Row(html.H2(actions[0]["recolte_nb"], className="text-center"))]


def display_indicators_layout(actions):
    """Display indicators layout of the details app."""
    actions_df = pd.DataFrame(actions)
    indicators_dict = calculate_indicators(actions_df)
    return [
        dbc.Row(dmc.Divider(label=html.H3("Indicateurs"), labelPosition="center")),
        dbc.Row(
            html.H4("Indicateurs globaux"),
            className="text-center text-decoration-underline",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H4(f"Date de mise en culture"),
                        html.P(indicators_dict["date_mec"]),
                    ]
                ),
                dbc.Col(
                    [
                        html.H4(f"Date de recolte"),
                        html.P(indicators_dict["date_recolte"]),
                    ]
                ),
                dbc.Col(
                    [
                        html.H4(f"Nombre de bacs"),
                        html.P(f'{indicators_dict["nb_bacs"] or 0} bacs'),
                    ]
                ),
                dbc.Col(
                    [
                        html.H4(f"Quantite recoltee"),
                        html.P(f'{indicators_dict["qte_recolte"]} g'),
                    ]
                ),
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
                dbc.Col([html.H4(f"Feed Ratio Conversion "), html.P()]),
                dbc.Col(
                    [html.H4(f"Croissance journalière moyenne"), html.P("13 aout 3932")]
                ),
                dbc.Col([html.H4(f"Assimilation moyenne "), html.P("13 aout 3932")]),
            ]
        ),
    ]


def display_historical_actions_layout(actions):
    """Display all actions of given recolte_nb in an accordion."""
    return [
        dbc.Row(
            dmc.Divider(label=html.H3("Toutes les actions"), labelPosition="center")
        ),
        dbc.Row(
            [dmc.Accordion(action_item_component(action)) for action in actions],
        ),
    ]


def display_layout(recolte_nb):
    """Full layout of detail page."""
    actions = get_details_from_recolte_nb(recolte_nb)
    return dbc.Container(
        display_top_title(actions)
        + display_indicators_layout(actions)
        + display_historical_actions_layout(actions)
    )
