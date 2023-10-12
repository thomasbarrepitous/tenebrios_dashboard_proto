import dash_bootstrap_components as dbc
from dash import html

from tenebrios_utils import formatting


def basic_edit_input(value: str, label: str):
    index = f"edit-{formatting.format_to_form_index(label)}"
    return html.Div(
        [
            dbc.Label(label, html_for=f"edit-{label.lower()}"),
            dbc.Input(
                type="text",
                id={"type": "input-data", "index": index},
                value=value,
                placeholder=value,
            ),
        ],
        className="mb-3",
    )


def basic_edit_switch(label: str, value: bool = True, id=None):
    if id is None:
        index = f"switch-{formatting.format_to_form_index(label)}"
        id = {
            "type": "input-data",
            "index": index,
        }
    return html.Div(
        [
            dbc.Label(f"{label}", width="auto"),
            dbc.Col(
                [
                    dbc.Switch(
                        label=value,
                        value=value,
                        id=id,
                    )
                ]
            ),
        ],
        # align="center",
    )


def basic_edit_text_area(label: str, value: str = ""):
    index = f"textarea-{formatting.format_to_form_index(label)}"
    return html.Div(
        [
            dbc.Label(label),
            dbc.Textarea(
                className="mb-3",
                placeholder=value,
                id={"type": "input-data", "index": index},
            ),
        ]
    )
