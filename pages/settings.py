import dash
from dash import callback, html, dcc, Output, Input, dash_table
import dash_bootstrap_components as dbc


dash.register_page(__name__)

#######################
# Settings appearance #
#######################


def user_welcome_message(username: str):
    return dbc.Label(f"Welcome user {username}")


def settings_switch(label: str):
    return dbc.Row(
        [
            dbc.Label(f'{label}', width="auto"),
            dbc.Col(
                [
                    dbc.Switch(
                        label="On",
                        value=True,
                    )
                ]
            )
        ],
        align="center",
    )


def settings_input(label: str):
    return dbc.Row(
        [
            dbc.Label(f"{label}", width="auto"),
            dbc.Col(
                dbc.Input(type="number", min=0, max=10, step=1),
            ),
        ]
    )


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


settings_tracability_weeks_checklist = dbc.Row(
    [
        dbc.Col(
            [
                dbc.Label(f"Semaine {i}"),
                dbc.Checkbox(
                    id=f"semaine-{i}-checkbox",
                    value=False,
                )
            ],
        ) for i in range(1, 11)
    ],
    align="center",
)

# settings_tracability_weeks_table = dbc.Row([
#     table_header = [
#     html.Thead(html.Tr([html.Th("First Name"), html.Th("Last Name")]))
# ],

# row1 = html.Tr([html.Td("Arthur"), html.Td("Dent")])
# row2 = html.Tr([html.Td("Ford"), html.Td("Prefect")])
# row3 = html.Tr([html.Td("Zaphod"), html.Td("Beeblebrox")])
# row4 = html.Tr([html.Td("Trillian"), html.Td("Astra")])

# table_body = [html.Tbody([row1, row2, row3, row4])]

# table = dbc.Table(table_header + table_body, bordered=True)
# ]
# )

accordion_weather_item = dbc.AccordionItem(
    [
        settings_switch("Setting example 1 :"),
        settings_input("Setting example 2 :")
    ],
    title="Weather Station"
)


accordion_tracability_item = dbc.AccordionItem(
    [
        settings_input("Nombre de semaines d'élevage :"),
        settings_input("Semaine début nourrisage humide :"),
        settings_input("Bacs par batch :"),
        dbc.Row(dbc.Col(dbc.Label("Qte donnée par nourrisage batch :"))),
        settings_input("Combien de fois mettez vous le son ?"),
        dbc.Row(
            dbc.Label("Aux quelles semaines ?")
        ),
        settings_tracability_weeks_checklist,
    ],
    title="Tracability"
)


accordion_other_item = dbc.AccordionItem(
    [
        # Styling test in progress
        settings_switch("Setting example 1 :"),
        html.Hr(
            style={
                "borderWidth": "0.5vh",
                "width": "100%",
                "borderColor": "secondary",
                "opacity": "unset",
            }
        ),
        settings_input("Setting example 2 :"),
        html.Hr(
            style={
                "borderWidth": "0.5vh",
                "width": "100%",
                "borderColor": "secondary",
                "opacity": "unset",
            }
        ),
        settings_input("Setting example 3 :"),
    ],
    title="Other"
)


settings_core = dbc.Row(
    dbc.Accordion(
        [
            accordion_weather_item,
            accordion_tracability_item,
            accordion_other_item
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
