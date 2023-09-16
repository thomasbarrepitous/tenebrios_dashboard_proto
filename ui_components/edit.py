import dash_bootstrap_components as dbc
from dash import html


def basic_edit_input(value: str, label: str):
    return html.Div(
        [
            dbc.Label(label, html_for=f"edit-{label}"),
            dbc.Input(type="text", id=f"edit-{label}", placeholder=value),
        ],
        className="mb-3",
    )


def basic_edit_switch(label: str, value: bool = True):
    return html.Div(
        [
            dbc.Label(f"{label}", width="auto"),
            dbc.Col(
                [
                    dbc.Switch(
                        label=value,
                        value=value,
                    )
                ]
            ),
        ],
        align="center",
    )


def basic_edit_text_area(label: str, value: str = ""):
    html.Div(
        [
            dbc.Label(label),
            dbc.Textarea(className="mb-3", placeholder=value),
        ]
    )
