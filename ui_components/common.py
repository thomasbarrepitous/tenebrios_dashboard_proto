import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash import html
from datetime import date


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
                        "index": f"{title.replace(' ', '').lower()}",
                    },
                )
            ),
        ],
        className="mb-3",
    )
