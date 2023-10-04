import dash_bootstrap_components as dbc
from dash import html, dcc
from datetime import date
from tenebrios_utils import formatting


def centered_title(title: str):
    return dbc.Row(
        [
            html.Hr(),
            dbc.Col(
                html.H2(f"{title}"),
                width={"size": 6, "offset": 3},
                className="text-center",
            ),
            html.Hr(),
        ]
    )


def date_picker_form(title: str, value: date = date.today()):
    index = f"{formatting.format_to_form_index(title)}"
    return dbc.Row(
        [
            dbc.Label(f"{title}", width="auto"),
            dbc.Col(
                dcc.DatePickerSingle(
                    # min_date_allowed=date(1995, 8, 5),
                    # max_date_allowed=date(2017, 9, 19),
                    # initial_visible_month=date(2017, 8, 5),
                    date=value,
                    id={
                        "type": "date-data",
                        "index": index,
                    },
                )
            ),
        ],
        className="mb-3",
    )


def send_form_button(title: str = "Confirmer"):
    return dbc.Row(
        dbc.Button(
            title,
            id="submit-button",
            n_clicks=0,
            type="submit",
            size="lg",
            className="me-md-2",
        ),
    )


def clear_form_button(title: str = "Effacer"):
    return dbc.Row(
        dbc.Button(
            title, type="clear", size="lg", className="me-md-2", color="secondary"
        ),
    )


def refresh_page_button(title: str = "Rafraichir"):
    return dbc.Row(
        dbc.Button(
            title,
            type="clear",
            size="lg",
            className="me-md-2 btn",
            color="secondary",
        )
    )
