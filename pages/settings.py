import dash
from dash import callback, html, dcc, Output, Input, dash_table
import dash_bootstrap_components as dbc

dash.register_page(__name__)

#######################
# Settings appearance #
#######################


def user_welcome_message(username: str):
    return dbc.Label(f"Welcome user {username}")


settings_title = dbc.Row(
    [
        html.Hr(),
        dbc.Col(
            html.H2(f'Settings'),
            width={"size": 6, "offset": 3},
            className='text-center'
        ),
        html.Hr()
    ]
)

settings_core = accordion = dbc.Row(
    dbc.Accordion(
        [
            dbc.AccordionItem(
                [
                    
                ],
                title="Weather Station",
            ),
            dbc.AccordionItem(
                [],
                title="Tracability",
            ),
            dbc.AccordionItem(
                [],
                title="Other",
            ),
        ],
        always_open=True,
        flush=True
    )
)


layout = dbc.Container(
    [
        settings_title,
        user_welcome_message("Admin"),
        settings_core
    ]
)
