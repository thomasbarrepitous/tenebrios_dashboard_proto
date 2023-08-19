import dash
from dash import callback, html, dcc, Output, Input, State, MATCH, ALL, dash_table
import pandas as pd
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import requests
import json
from datetime import date
import numpy as np
import re

API_URL = f'http://127.0.0.1:8000/api/actions'

with open('auth.json') as auth_file:
    auth_json = json.loads(auth_file.read())
    auth = (auth_json["username"], auth_json["password"])


dash.register_page(__name__)


######################
# En Cours Dashboard #
######################

def add_space_before_caps(str):
    return re.sub('([A-Z])', r' \1', str)


def latest_breeding_listgroup(df_column):
    # Change empty strings to pd.NaN
    pd.options.mode.use_inf_as_na = True
    return dbc.ListGroup(
        [
            dbc.ListGroupItem(
                [
                    html.Div(
                        html.H5(dmc.Highlight(
                            f"{add_space_before_caps(action[1]['resourcetype'])}", highlight=add_space_before_caps(action[1]['resourcetype']), className="mb-1 text-center text-nowrap bd-highlight"))
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                html.P(
                                    f'{key}: {value.strftime("%B %d, %Y") if type(value) == pd.Timestamp else value}'),
                                width=6,
                                class_name='text-center'
                            )
                            for key, value in action[1].items() if not pd.isna(value)
                        ],
                    )
                ]
            )
            for action in df_column[::-1].iterrows()
        ]
    )


def df_columns_type_fix(df_column):
    df_column['anomaly'] = df_column['anomaly'].astype('boolean')
    df_column['is_imw100_weighted'] = df_column['is_imw100_weighted'].astype(
        'boolean')
    df_column['son_arrival_date'] = pd.to_datetime(
        df_column['son_arrival_date'])
    df_column['marc_arrival_date'] = pd.to_datetime(
        df_column['marc_arrival_date'])
    df_column = df_column.replace('', np.nan)
    return df_column


def fetch_df_column(column):
    # Filtering by Ctype is a current restriction
    # imposed by the polymorphic design some models in the API.
    # For more informations : https://github.com/denisorehovsky/django-rest-polymorphic
    r = requests.get(
        f'{API_URL}?column={column}', auth=auth).text
    df = pd.read_json(r)
    # Filter by the current column
    df_column = df.query(f'column == "{column}"')
    # Only keep the latest breeding
    date_mec = df_column.query(
        'resourcetype == "MiseEnCulture"')['date'][0]
    df_column = df_column[(df['date'] >= date_mec.to_pydatetime())]
    # Convert to right types
    df_column = df_columns_type_fix(df_column)
    return df_column


def modal_body(df_column):
    last_action = df_column.iloc[-1]
    # Infere the inputs
    date_recolte = 'Élevage en cours'
    harvested_qty = 'Élevage en cours'
    if last_action['resourcetype'] == "Recolte":
        date_recolte = last_action['date']
        harvested_qty = last_action['harvested_quantity']
    date_mec = df_column.iloc[0]['date']
    return dbc.ModalBody(
        [
            dbc.Row(
                dbc.Col(html.P(f'Date de mise en culture : {date_mec.strftime("%B %d, %Y")}'))),
            dbc.Row(
                dbc.Col(html.P(f'Date de récolte : {date_recolte.strftime("%B %d, %Y")}'))),
            dbc.Row(
                [
                    dbc.Col(
                        html.P(f'Poids récolte totale du lot :{harvested_qty}')),
                    dbc.Col(
                        html.P(f'Poids moyen par bac : {None}'))
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        html.H3(f'Historique :'), class_name='text-center'),
                    dbc.Col(
                        latest_breeding_listgroup(df_column),
                        width='12'
                    )
                ]
            )
        ]
    )


def column_card(column):
    df_column = fetch_df_column(column)
    return dbc.Col(
        dbc.Card(
            [
                dbc.CardHeader(html.H4(f"Colonne {column}",
                                       className="card-title text-center"),),
                dbc.CardBody(
                    [
                        html.H6(f"Dernière action : {add_space_before_caps(df_column.iloc[-1]['resourcetype'])}",
                                className="card-subtitle"),
                        html.P(
                            f"Date : {df_column.iloc[-1]['date'].strftime('%B %d, %Y')}",
                            className="card-text",
                        ),
                        dbc.Button("Voir détails", color="primary", id={
                            "type": "button_modal", "index": column}, className="me-1", n_clicks=0),
                        dbc.Modal(
                            [
                                dbc.ModalHeader(
                                    dbc.ModalTitle(f"Colonne {column}")),
                                modal_body(df_column),
                            ],
                            id={"type": "modal_column", "index": column},
                            size="lg",
                            is_open=False,
                        )
                    ]
                )
            ],
            style={"width": "18rem"}
        )
    )


def display_column_cards():
    columns = json.loads(requests.get(
        f'{API_URL}/columns', auth=auth).text)
    cards = dbc.Row(
        [
            column_card(column['column'])
            for column in columns
        ]
    )
    return cards


########################
# Historical breedings #
########################

def breeding_table(df: pd.DataFrame, title: str):
    return dbc.Col(
        [
            html.H2(title),
            dbc.Table.from_dataframe(
                df, striped=True, bordered=True, hover=True)
        ],
        className='text-center'
    )


def display_historical_breedings():
    historic_breedings = json.loads(requests.get(
        f'{API_URL}/historic-breedings', auth=auth).text)
    if historic_breedings%2 == 0:
        start_breeding_df, end_breeding_df = pd.DataFrame(
            historic_breedings[0::2]), pd.DataFrame(historic_breedings[1::2])
    breedings_lists = dbc.Row(
        [
            breeding_table(start_breeding_df, 'Mise en culture'),
            breeding_table(end_breeding_df, 'Recolte')
        ]
    )
    return breedings_lists


########################
# Historical breedings #
########################

def display_raw_data():
    historic_breedings = json.loads(requests.get(
        f'{API_URL}/historic-breedings', auth=auth).text)
    return dash_table.DataTable(historic_breedings, css=[{
        'selector': '.dash-spreadsheet td div',
        'rule': '''
                    line-height: 15px;
                    max-height: 30px; min-height: 30px; height: 30px;
                    display: block;
                    overflow-y: hidden;

                        '''
    }],
        style_data={
            'whiteSpace': 'normal',
    },
        page_current=0,
        page_size=6,
        page_action='native')


def display_centered_title(title: str):
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


dashboard = [
    display_centered_title('En Cours'),
    display_column_cards(),
    display_centered_title('Historique élevage'),
    display_historical_breedings(),
    display_centered_title('Données brutes'),
    display_raw_data()
]


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
        return dashboard
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


#################
# Column Modals #
#################

def toggle_modal(n1, is_open):
    if n1:
        return not is_open
    return is_open


@callback(
    Output({"type": "modal_column", "index": MATCH}, "is_open"),
    Input({"type": "button_modal", "index": MATCH}, "n_clicks"),
    State({"type": "modal_column", "index": MATCH}, "is_open"),
)
def toggle_modal_callback(n1, is_open):
    return toggle_modal(n1, is_open)
