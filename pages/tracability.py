import dash
from dash import callback, html, dcc, Output, Input, dash_table
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import requests
import json
from datetime import date

dash.register_page(__name__)


#############
# Dashboard #
#############

def render_dashboard():
    pass


#########
# Input #
#########

def title_form(title: str):
    return dbc.Row(
        [
            html.Hr(),
            dbc.Col(
                html.H2(f'{title}'),
                width={"size": 6, "offset": 3},
                className='text-center'
            ),
            html.Hr()
        ]
    )


def qte_donnee_duo_form(qte_name: str):
    return dbc.Row(
        [
            dbc.Label(f"{qte_name}/bac", width="auto"),
            dbc.Col(
                dbc.InputGroup(
                    [
                        dbc.Input(placeholder="Quantité", type="number"),
                        dbc.InputGroupText("G"),
                    ]
                ),
            ),
            dbc.Label(f"{qte_name} total", width="auto"),
            dbc.Col(
                dbc.InputGroup(
                    [
                        dbc.Input(placeholder="Quantité", type="number"),
                        dbc.InputGroupText("KG"),
                    ]
                ),
            )
        ],
        className="mb-3",
    )


def qte_donnee_form(qte_name: str):
    return dbc.Row(
        [
            dbc.Label(f"{qte_name}", width="auto"),
            dbc.Col(
                dbc.InputGroup(
                    [
                        dbc.Input(placeholder="Quantité", type="number"),
                        dbc.InputGroupText("KG"),
                    ]
                ),
            ),
        ],
        className="mb-3",
    )


def date_picker_form(title: str):
    return dbc.Row(
        [
            dbc.Label(f"{title}", width="auto"),
            dbc.Col(
                dcc.DatePickerSingle(
                    # min_date_allowed=date(1995, 8, 5),
                    # max_date_allowed=date(2017, 9, 19),
                    # initial_visible_month=date(2017, 8, 5),
                    date=date.today(),
                )
            ),
        ],
        className="mb-3",
    )


header_input = dbc.Row([
    dbc.Col(html.H4(f'{date.today().strftime("%B %d, %Y")}')),
    dbc.Col(html.H4(f'Colonne n°17')),
    dbc.Col(
        dbc.InputGroup(
            [
                dbc.InputGroupText("Action"),
                dbc.Select(
                    id="select-actions-input",
                    options=[
                        {"label": "Nourrisage Humide", "value": "marc"},
                        {"label": "Nourrisage Son", "value": "son"},
                        {"label": "Tamisage", "value": "tamise"},
                        {"label": "Récolte", "value": "recolte"},
                    ],
                    value="marc"
                )
            ]
        )
    )
], class_name="text-center")


column_form = dbc.Row(
    [
        dbc.Label("Colonne", width="auto"),
        dbc.Col(
            dbc.Input(
                type="number", placeholder="Entrer colonne"
            ),
        ),
    ],
    className="mb-3",
)


anomalie_marc_form = dbc.Row(
    [
        dbc.Label("Anomalie", width="auto"),
        dbc.Col(
            dbc.RadioItems(
                id="anomalie-radios",
                className="btn-group",
                inputClassName="btn-check",
                labelClassName="btn btn-outline-primary",
                labelCheckedClassName="active",
                options=[
                    {"label": "Oui", "value": True},
                    {"label": "Non", "value": False},
                ],
                value=False,
            ),
            className="radio-group",
            width="auto"
        ),
        dbc.Col(id="anomalie-radios-output")
    ],
    className="mb-3",
)


pesage_marc_form = dbc.Row(
    [
        dbc.Label(
            "Pesage IMW100 (Individual Mass Weight pour 100 larves)", width="auto"),
        dbc.Col(
            dbc.RadioItems(
                id="pesage-radios",
                className="btn-group",
                inputClassName="btn-check",
                labelClassName="btn btn-outline-primary",
                labelCheckedClassName="active",
                options=[
                    {"label": "Oui", "value": True},
                    {"label": "Non", "value": False},
                ],
                value=False,
            ),
            className="radio-group",
            width="auto"
        ),
        dbc.Col(id="pesage-radios-output")
    ],
    className="mb-3",
)


form_input_marc = [
    title_form("Marc de pomme"),
    column_form,
    date_picker_form("Date"),
    qte_donnee_duo_form("Marc"),
    date_picker_form("Date arrivage"),
    anomalie_marc_form,
    pesage_marc_form
]


form_input_son = [
    title_form("Son de blé"),
    column_form,
    date_picker_form("Date"),
    qte_donnee_duo_form("Son"),
    date_picker_form("Date arrivage"),
]


form_input_tamise = [
    title_form("Tamisage"),
    column_form,
    date_picker_form("Date"),
    qte_donnee_form("Qte tamisée"),
]


form_input_recolte = [
    title_form("Récolte"),
    column_form,
    date_picker_form("Date"),
    qte_donnee_form("Qte récoltée"),
]


##########
# Layout #
##########


layout = dbc.Container(
    [
        dbc.Row(html.H1('Tracability Dashboard',
                style={'textAlign': 'center'})),
        dbc.Row(
            dcc.Tabs(
                id="tabs-tracability",
                value='input-tab',
                children=[
                    dcc.Tab(label='Dashboard', value='dashboard-tab'),
                    dcc.Tab(label='Input', value='input-tab'),
                ]

            )
        ),
        dbc.Row(html.Div(id='tabs-tracability-content'))
    ],
    fluid=True)


############
# Callback #
############

@callback(Output("pesage-radios-output", "children"), [Input("pesage-radios", "value")])
def display_pesage_comment(value):
    if value:
        return [
            dbc.Input(
                type="text", placeholder="Commentaire ..."
            ),
        ]


@callback(Output("anomalie-radios-output", "children"), [Input("anomalie-radios", "value")])
def display_anomalie_comment(value):
    if value:
        return [
            dbc.Input(
                type="text", placeholder="Commentaire ..."
            ),
        ]


@callback(Output('tabs-tracability-content', 'children'),
          Input('tabs-tracability', 'value'))
def render_content(tab):
    if tab == 'dashboard-tab':
        return render_dashboard()
    elif tab == 'input-tab':
        return [header_input, dbc.Form(id="form-input-module")]


@callback(Output('form-input-module', 'children'),
          Input('select-actions-input', 'value'))
def render_action_form(action):
    if action == 'marc':
        return form_input_marc
    elif action == 'son':
        return form_input_son
    elif action == 'tamise':
        return form_input_tamise
    elif action == 'recolte':
        return form_input_recolte
