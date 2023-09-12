import dash
from dash import html
import dash_bootstrap_components as dbc
import json
import requests
import dash_mantine_components as dmc
from datetime import datetime
import pandas as pd
import re
import math

dash.register_page(__name__, path_template="/tracability/recolte/<recolte_nb>")


API_URL = f"http://127.0.0.1:8000/api/actions"

with open("auth.json") as auth_file:
    auth_json = json.loads(auth_file.read())
    auth = (auth_json["username"], auth_json["password"])


def layout(recolte_nb=None):
    return display_layout(recolte_nb)


def timestamp_to_readable_datetime(date) -> datetime:
    return datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")


def api_date_to_datetime(date) -> datetime:
    return pd.to_datetime(date, format="%Y-%m-%dT%H:%M:%S.%fZ")


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


def get_imw_recolte_from_actions_df(actions_df: pd.DataFrame) -> int:
    actions_df["date"] = pd.to_datetime(actions_df["date"])
    filtered_df = actions_df[actions_df["imw100_weight"].notnull()]
    latest_row = filtered_df.loc[filtered_df["date"].idxmax()]
    return latest_row["imw100_weight"]


def get_total_son_from_actions_df(actions_df: pd.DataFrame) -> int:
    return sum(
        actions_df.query("resourcetype == 'NourrisageSon'")["given_quantity"].values
    )


def get_total_nourriture_humide_from_actions_df(actions_df: pd.DataFrame) -> int:
    return sum(
        actions_df.query("resourcetype == 'NourrisageHumide'")["given_quantity"].values
    )


def get_feed_ratio_conversion_from_actions_df(actions_df: pd.DataFrame) -> int:
    # filtered_df = actions_df.dropna(subset=["given_quantity", "sieved_quantity"])
    sum_of_given_over_sieved = (
        actions_df["given_quantity"].sum() / actions_df["sieved_quantity"].sum()
    )
    return sum_of_given_over_sieved.round(2)


def get_croissance_journaliere_moyenne_from_actions_df(actions_df: pd.DataFrame) -> int:
    pass


def get_assimilation_moyenne_from_actions_df(actions_df: pd.DataFrame) -> int:
    assimilation_moyenne = (
        actions_df["given_quantity"].sum() / actions_df["sieved_quantity"].sum()
    ) * 100
    return assimilation_moyenne


def calculate_indicators(actions_df: pd.DataFrame) -> dict:
    map = {
        # Indicateurs Totaux / Globaux
        "date_mec": get_date_mec_from_actions_df(actions_df),
        "date_recolte": get_date_recolte_from_actions_df(actions_df),
        "nb_bacs": get_nb_bacs_from_actions_df(actions_df),
        "qte_recolte": get_qte_recolte_from_actions_df(actions_df),
        # Indicateurs Moyens
        "imw_recolte": get_imw_recolte_from_actions_df(actions_df),
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
    return map


def action_item_component(action):
    """Build one item of the full historical actions accordion."""
    action_date = api_date_to_datetime(action["date"])
    accordion_action_title = re.sub(r"(\w)([A-Z])", r"\1 \2", action["resourcetype"])
    header = [html.Thead(html.Tr([html.Th(key) for key, value in action.items()]))]
    body = [html.Tbody(html.Tr([html.Td(value) for key, value in action.items()]))]
    return dmc.AccordionItem(
        [
            dmc.AccordionControl(
                f'{accordion_action_title} du {action_date.strftime("%B %d, %Y")}'
            ),
            dmc.AccordionPanel(dmc.Table(header + body)),
        ],
        value=action["date"],
    )


def display_top_title(actions):
    return [dbc.Row(html.H2(actions[0]["recolte_nb"], className="text-center"))]


def individual_indicator_component(indicator_name, indicator_value):
    return dbc.Col(
        dmc.Paper(
            [
                html.H4(indicator_name),
                html.P(indicator_value),
            ],
            shadow="xs",
            p="xl",
            #     style={"height": "20vh"},
        ),
        align="center",
        width=3,
    )


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
                individual_indicator_component(
                    f"Date de mise en culture", indicators_dict["date_mec"]
                ),
                individual_indicator_component(
                    f"Date de recolte", indicators_dict["date_recolte"]
                ),
                individual_indicator_component(
                    f"Nombre de bacs", indicators_dict["nb_bacs"]
                ),
                individual_indicator_component(
                    f"Quantite recoltee", f'{indicators_dict["qte_recolte"]} g'
                ),
            ]
        ),
        dbc.Row(
            html.H4(
                "Indicateurs moyens",
                className="text-center text-decoration-underline",
            ),
        ),
        dbc.Row(
            [
                individual_indicator_component(
                    f"IMW à la récolte", f'{indicators_dict["imw_recolte"]} g'
                ),
                individual_indicator_component(
                    f"Total son donné", f'{indicators_dict["total_son"]} g'
                ),
                individual_indicator_component(
                    f"Total nourriture humide donnée",
                    f'{indicators_dict["total_nourriture_humide"]} g',
                ),
                individual_indicator_component(
                    f"Feed Ratio Conversion", indicators_dict["feed_ratio_conversion"]
                ),
                individual_indicator_component(
                    f"Croissance journalière moyenne",
                    f'{indicators_dict["croissance_journaliere_moyenne"] or 0} %',
                ),
                individual_indicator_component(
                    f"Assimilation moyenne",
                    f'{indicators_dict["assimilation_moyenne"] or 0} %',
                ),
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
