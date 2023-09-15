import dash
from dash import html

from tenebrios_utils.apiCalls import get_action_by_id


dash.register_page(__name__, path_template="/tracability/action/<action_id>")


def display_layout(action: dict):
    return html.P(f"{action}")


def layout(action_id):
    action = get_action_by_id(action_id)
    return display_layout(action)
