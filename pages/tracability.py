import dash
from dash import callback, html, dcc, Output, Input, State, MATCH, ALL, dash_table
import pandas as pd
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from datetime import date
import numpy as np
import math
from tenebrios_utils import apiCalls, formatting
from ui_components import common


dash.register_page(__name__)


CYCLE_PAGE_SIZE = 5

all_columns = apiCalls.get_all_columns()
all_actions = apiCalls.get_all_actions()

#########
# Alert #
#########


def refresh_btn_toast(text: str):
    return dbc.Toast(
        text,
        id="positioned-toast",
        header="Notification",
        is_open=False,
        dismissable=True,
        icon="primary",
        style={"position": "fixed", "top": 66, "right": 10, "width": 350, "z-index": 1},
    )


######################
# En Cours Dashboard #
######################


def latest_breeding_listgroup(df_column):
    # Change empty strings to pd.NaN
    pd.options.mode.use_inf_as_na = True
    return dbc.ListGroup(
        [
            dbc.ListGroupItem(
                [
                    html.Div(
                        html.H5(
                            dmc.Highlight(
                                f"{formatting.add_space_before_caps(action[1]['resourcetype'])}",
                                highlight=formatting.add_space_before_caps(
                                    action[1]["resourcetype"]
                                ),
                                className="mb-1 text-center text-nowrap bd-highlight",
                            )
                        )
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                html.P(
                                    f'{key}: {value.strftime("%B %d, %Y") if type(value) == pd.Timestamp else value}'
                                ),
                                width=6,
                                class_name="text-center",
                            )
                            for key, value in action[1].items()
                            if not pd.isna(value)
                        ],
                    ),
                ]
            )
            for action in df_column[::-1].iterrows()
        ]
    )


def df_columns_type_fix(df_column):
    df_column["anomaly"] = df_column["anomaly"].astype("boolean")
    df_column["is_imw100_weighted"] = df_column["is_imw100_weighted"].astype("boolean")
    df_column["son_arrival_date"] = pd.to_datetime(df_column["son_arrival_date"])
    df_column["marc_arrival_date"] = pd.to_datetime(df_column["marc_arrival_date"])
    df_column["date"] = pd.to_datetime(df_column["date"])
    df_column = df_column.replace("", np.nan)
    return df_column


def fetch_df_column(column):
    df = pd.DataFrame(apiCalls.get_column_actions(column))
    # Filter by the current column
    df_column = df.query(f'column == "{column}"')
    # Only keep the latest breeding
    date_mec = df_column.query('resourcetype == "MiseEnCulture"')["date"][0]
    df_column = df_column[(df["date"] >= date_mec)]
    # Convert to right types
    df_column = df_columns_type_fix(df_column)
    return df_column


def modal_body(df_column):
    last_action = df_column.iloc[-1]
    # Infere the inputs
    date_recolte = None
    harvested_qty = "Élevage en cours"
    if last_action["resourcetype"] == "Recolte":
        date_recolte = last_action["date"]
        harvested_qty = last_action["harvested_quantity"]
    date_mec = df_column.iloc[0]["date"]
    return dbc.ModalBody(
        [
            dbc.Row(
                dbc.Col(
                    html.P(
                        f'Date de mise en culture : {date_mec.strftime("%B %d, %Y")}'
                    )
                )
            ),
            dbc.Row(
                dbc.Col(
                    html.P(
                        f'Date de récolte : {date_recolte.strftime("%B %d, %Y") or "Élevage en cours"}'
                    )
                )
            ),
            dbc.Row(
                [
                    dbc.Col(html.P(f"Poids récolte totale du lot :{harvested_qty}")),
                    dbc.Col(html.P(f"Poids moyen par bac : {None}")),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(html.H3(f"Historique :"), class_name="text-center"),
                    dbc.Col(latest_breeding_listgroup(df_column), width="12"),
                ]
            ),
        ]
    )


def column_card(column):
    df_column = fetch_df_column(column)
    return dbc.Col(
        dbc.Card(
            [
                dbc.CardHeader(
                    html.H4(f"Colonne {column}", className="card-title text-center"),
                ),
                dbc.CardBody(
                    [
                        html.H6(
                            f"Dernière action : {formatting.add_space_before_caps(df_column.iloc[-1]['resourcetype'])}",
                            className="card-subtitle",
                        ),
                        html.P(
                            f"Date : {df_column.iloc[-1]['date'].strftime('%B %d, %Y')}",
                            className="card-text",
                        ),
                        dbc.Button(
                            "Voir détails",
                            color="primary",
                            id={"type": "button_modal", "index": column},
                            className="me-1",
                            n_clicks=0,
                        ),
                        dbc.Modal(
                            [
                                dbc.ModalHeader(dbc.ModalTitle(f"Colonne {column}")),
                                modal_body(df_column),
                            ],
                            id={"type": "modal_column", "index": column},
                            size="lg",
                            is_open=False,
                        ),
                    ]
                ),
            ],
            style={"width": "18rem"},
        )
    )


def display_column_cards(columns):
    cards = dbc.Row([column_card(column["column"]) for column in columns])
    return cards


#################
# Cycle history #
#################


def filter_cycle(columns):
    return dbc.Col(
        [
            dmc.MultiSelect(
                label="Filtrer par colonne",
                placeholder="Choisis une ou plusieurs colonne!",
                id="framework-multi-select",
                value=[],
                data=[
                    {"value": column["column"], "label": column["column"]}
                    for column in columns
                ],
                style={"width": 400, "marginBottom": 10},
            ),
            dmc.Text(id="multi-selected-value"),
        ],
        width={"size": 4, "offset": 4},
    )


def display_pagination_cycle(current_page: int, total_page_size: int):
    return dbc.Col(
        dmc.Pagination(
            total=total_page_size,
            boundaries=1,
            page=current_page,
            id="pagination-cycle",
        ),
        width={"size": 2, "offset": 5},
    )


def display_cycle(recolte_nb: str):
    harvest_cycle = apiCalls.get_cycle_from_recolte(recolte_nb)
    return dbc.Col(
        dmc.NavLink(
            label=dmc.Highlight(
                f'{harvest_cycle[0]["recolte_nb"]} : {harvest_cycle[0]["date"]} -> {harvest_cycle[1]["date"]}',
                highlight=harvest_cycle[0]["recolte_nb"],
                highlightColor="primary",
                className="mb-1 text-center text-nowrap bd-highlight",
            ),
            href=f'/tracability/recolte/{harvest_cycle[0]["recolte_nb"]}',
        ),
        width={"size": 6, "offset": 3},
        className="text-center",
    )


def display_historical_cycle(columns):
    cycles_display = dbc.Row(
        [
            dbc.Row(filter_cycle(columns)),
            dbc.Row(id="display-cycle"),
            dbc.Row([display_pagination_cycle(1, 1)], id="pagination-div"),
        ]
    )
    return cycles_display


########################
# Historical breedings #
########################


def display_raw_data(actions):
    return dash_table.DataTable(
        actions,
        css=[
            {
                "selector": ".dash-spreadsheet td div",
                "rule": """
                    line-height: 15px;
                    max-height: 30px; min-height: 30px; height: 30px;
                    display: block;
                    overflow-y: hidden;

                        """,
            }
        ],
        style_data={
            "whiteSpace": "normal",
        },
        page_current=0,
        page_size=6,
        page_action="native",
    )


def display_centered_title(title: str):
    return dbc.Row(
        [
            dbc.Col(
                html.H2(f"{title}"),
                width={"size": 6, "offset": 3},
                className="text-center",
            ),
            html.Hr(),
        ]
    )


#########
# Input #
#########


def qte_donnee_duo_form(qte_name: str):
    return dbc.Row(
        [
            dbc.Label(f"{qte_name}/bac", width="auto"),
            dbc.Col(
                dbc.InputGroup(
                    [
                        dbc.Input(
                            placeholder="Quantité",
                            type="number",
                            id={
                                "type": "input-data",
                                "index": f"{qte_name.replace(' ', '')}-bac",
                            },
                        ),
                        dbc.InputGroupText("G"),
                    ]
                ),
            ),
            dbc.Label(f"{qte_name} total", width="auto"),
            dbc.Col(
                dbc.InputGroup(
                    [
                        dbc.Input(
                            placeholder="Quantité",
                            type="number",
                            id={
                                "type": "input-data",
                                "index": f"{qte_name.replace(' ', '')}-total",
                            },
                        ),
                        dbc.InputGroupText("KG"),
                    ]
                ),
            ),
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
                        dbc.Input(
                            placeholder="Quantité",
                            type="number",
                            id={
                                "type": "input-data",
                                "index": f"{qte_name.replace(' ', '')}",
                            },
                        ),
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
                    id={
                        "type": "date-data",
                        "index": f"{title.replace(' ', '').lower()}",
                    },
                )
            ),
        ],
        className="mb-3",
    )


header_input = dbc.Row(
    [
        dbc.Col(html.H4(f'{date.today().strftime("%B %d, %Y")}')),
        dbc.Col(html.H4(f"Colonne n°17")),
        dbc.Col(common.action_choice_dropdown()),
    ],
    class_name="text-center",
)


column_form = dbc.Row(
    [
        dbc.Label("Colonne", width="auto"),
        dbc.Col(
            dbc.Input(
                id={"type": "input-data", "index": "column"},
                type="string",
                placeholder="Entrer colonne",
            ),
        ),
    ],
    className="mb-3",
)


recolte_nb_form = dbc.Row(
    [
        dbc.Label("Recolte_nb", width="auto"),
        dbc.Col(
            dbc.Input(
                id={"type": "input-data", "index": "recolte_nb"},
                type="string",
                placeholder="Entrer recolte number",
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
                id={"type": "input-data", "index": "anomaly"},
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
            width="auto",
        ),
        dbc.Col(id="anomalie-radios-output"),
    ],
    className="mb-3",
)


pesage_marc_form = dbc.Row(
    [
        dbc.Label(
            "Pesage IMW100 (Individual Mass Weight pour 100 larves)", width="auto"
        ),
        dbc.Col(
            dbc.RadioItems(
                name="form-input",
                id={"type": "input-data", "index": "is_imw100_weighted"},
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
            width="auto",
        ),
        dbc.Col(id="pesage-radios-output"),
    ],
    className="mb-3",
)


send_form_button = dbc.Row(
    dbc.Button(
        "Confirmer",
        id="submit-button",
        n_clicks=0,
        type="submit",
        size="lg",
        className="me-md-2",
    ),
)


clear_form_button = dbc.Row(
    dbc.Button("Effacer", type="clear", size="lg", className="me-md-2"),
)


##########
# Layout #
##########

form_input_marc = [
    display_centered_title("Marc de pomme"),
    column_form,
    date_picker_form("Date"),
    qte_donnee_duo_form("Marc"),
    date_picker_form("Date arrivage marc"),
    anomalie_marc_form,
    pesage_marc_form,
    send_form_button,
]


form_input_son = [
    display_centered_title("Son de blé"),
    column_form,
    date_picker_form("Date"),
    qte_donnee_duo_form("Son"),
    date_picker_form("Date arrivage son"),
    send_form_button,
]


form_input_tamise = [
    display_centered_title("Tamisage"),
    column_form,
    date_picker_form("Date"),
    qte_donnee_form("Qte tamisée"),
    send_form_button,
]


form_input_recolte = [
    display_centered_title("Récolte"),
    column_form,
    date_picker_form("Date"),
    qte_donnee_form("Qte récoltée"),
    send_form_button,
]


form_input_mec = [
    display_centered_title("Mise en culture"),
    column_form,
    recolte_nb_form,
    date_picker_form("Date"),
    send_form_button,
]


dashboard = [
    display_centered_title("En Cours"),
    dmc.Button("Refresh", id="refresh-data-btn"),
    refresh_btn_toast("Data Refreshed !"),
    dbc.Spinner(html.Div(id="column-cards"), color="secondary", type="grow"),
    display_centered_title("Historique élevage"),
    dbc.Spinner(html.Div(id="historical-cycle"), color="secondary", type="grow"),
    display_centered_title("Données brutes"),
    dbc.Spinner(html.Div(id="raw-data"), color="secondary", type="grow"),
]


layout = dbc.Container(
    [
        dbc.Row(html.H1("Tracability Dashboard", style={"textAlign": "center"})),
        dbc.Row(
            dcc.Tabs(
                id="tabs-tracability",
                value="input-tab",
                children=[
                    dcc.Tab(label="Dashboard", value="dashboard-tab"),
                    dcc.Tab(label="Input", value="input-tab"),
                ],
            )
        ),
        dbc.Row(html.Div(id="tabs-tracability-content")),
        html.Div(id="output"),
    ],
    fluid=True,
)


############
# Callback #
############


@callback(
    Output("output", "children"),
    Input("submit-button", "n_clicks"),
    State({"type": "input-data", "index": ALL}, "id"),
    State({"type": "input-data", "index": ALL}, "value"),
    State({"type": "date-data", "index": ALL}, "id"),
    State({"type": "date-data", "index": ALL}, "date"),
)
def callback_send_post_request(
    n_clicks, input_ids, input_values, date_ids, date_values
):
    if n_clicks:
        post_data: dict = {}
        input_ids = date_ids + input_ids
        input_values = date_values + input_values
        for id, values in zip(input_ids, input_values):
            post_data[formatting.form_index_to_request_id(id["index"])] = values
        # POST request
        apiCalls.post_action(post_data)
        print(post_data)
    return ""


@callback(
    Output("pesage-radios-output", "children"),
    [Input({"type": "input-data", "index": "is_imw100_weighted"}, "value")],
)
def display_pesage_comment(value):
    if value:
        return [
            dbc.Input(
                type="text",
                placeholder="Commentaire ...",
                id={"type": "input-data", "index": "imw100_weight"},
            ),
        ]


@callback(
    Output("anomalie-radios-output", "children"),
    [Input({"type": "input-data", "index": "anomaly"}, "value")],
)
def display_anomalie_comment(value):
    if value:
        return [
            dbc.Input(
                type="text",
                placeholder="Commentaire ...",
                id={"type": "input-data", "index": "anomaly_comment"},
            ),
        ]


@callback(
    Output("tabs-tracability-content", "children"), Input("tabs-tracability", "value")
)
def render_content(tab):
    if tab == "dashboard-tab":
        return dashboard
    elif tab == "input-tab":
        return [header_input, dbc.Form(id="form-input-module")]


@callback(
    Output("form-input-module", "children"),
    Input({"type": "input-data", "index": "resourcetype"}, "value"),
)
def render_action_form(action):
    if action == "NourrissageHumide":
        return form_input_marc
    elif action == "NourrissageSon":
        return form_input_son
    elif action == "Tamisage":
        return form_input_tamise
    elif action == "Recolte":
        return form_input_recolte
    elif action == "MiseEnCulture":
        return form_input_mec


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


@callback(
    Output("display-cycle", "children"),
    Output("pagination-div", "children"),
    Input("pagination-cycle", "page"),
    Input("framework-multi-select", "value"),
)
def select_value(current_page, filters):
    uri_filters = ""
    if filters != []:
        uri_filters = "".join("column=" + filter + "&" for filter in filters)
    historical_harvests = apiCalls.get_all_recolte_paginated(
        uri_filters, current_page, CYCLE_PAGE_SIZE
    )
    return [
        [
            display_cycle(harvest["recolte_nb"])
            for harvest in historical_harvests["results"]
        ],
        display_pagination_cycle(
            current_page, math.ceil(historical_harvests["count"] / CYCLE_PAGE_SIZE)
        ),
    ]


@callback(
    Output("historical-cycle", "children"),
    Output("column-cards", "children"),
    Output("raw-data", "children"),
    Input("refresh-data-btn", "n_clicks"),
)
def populate_historical_cycle(n_clicks):
    return (
        display_historical_cycle(all_columns),
        display_column_cards(all_columns),
        display_raw_data(all_actions),
    )


@callback(Output("positioned-toast", "is_open"), Input("refresh-data-btn", "n_clicks"))
def refresh_data(n_clicks):
    if n_clicks:
        return True
    return False
