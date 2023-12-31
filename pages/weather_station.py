import dash
from dash import callback, html, dcc, Output, Input, dash_table
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.graph_objects as go


dash.register_page(__name__)


# TODO : Refactor this


################
### Averages ###
################


def average_temp_fig(value, delta):
    return go.Figure(
        go.Indicator(
            mode="gauge+number+delta",
            delta={"reference": delta, "suffix": "°C"},
            number={"suffix": "°C"},
            value=value,
            title={"text": "Temperature °C"},
            gauge={
                "axis": {"range": [None, 40], "tickwidth": 1, "tickcolor": "darkblue"},
                "bar": {"color": "green"},
                "steps": [
                    {"range": [0, 5], "color": "#002947"},
                    {"range": [5, 10], "color": "#176dae"},
                    {"range": [10, 18], "color": "#70d4ff"},
                    {"range": [18, 22], "color": "#FFF2CE"},
                    {"range": [22, 30], "color": "#FEB938"},
                    {"range": [30, 35], "color": "#FD9415"},
                    {"range": [35, 40], "color": "#E23201"},
                ],
            },
        ),
        go.Layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"),
    )


def average_humidity_fig(value, delta):
    return go.Figure(
        go.Indicator(
            mode="gauge+number+delta",
            delta={"reference": delta, "suffix": "%"},
            number={"suffix": "%"},
            value=value,
            title={"text": "Humidity %"},
            gauge={
                "axis": {"range": [30, 100], "tickwidth": 1, "tickcolor": "darkblue"},
                "bar": {"color": "green"},
                "steps": [
                    {"range": [30, 40], "color": "#002947"},
                    {"range": [40, 50], "color": "#176dae"},
                    {"range": [50, 60], "color": "#70d4ff"},
                    {"range": [60, 70], "color": "#FFF2CE"},
                    {"range": [70, 80], "color": "#FEB938"},
                    {"range": [80, 90], "color": "#FD9415"},
                    {"range": [90, 100], "color": "#E23201"},
                ],
            },
        ),
        go.Layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"),
    )


def average_co2_fig(value, delta):
    return go.Figure(
        go.Indicator(
            mode="gauge+number+delta",
            delta={"reference": delta, "suffix": "ppm"},
            number={"suffix": "ppm"},
            value=value,
            title={"text": "CO2 ppm"},
            gauge={
                "axis": {"range": [500, 1300], "tickwidth": 1, "tickcolor": "darkblue"},
                "bar": {"color": "green"},
                "steps": [
                    {"range": [500, 600], "color": "#002947"},
                    {"range": [600, 700], "color": "#176dae"},
                    {"range": [700, 800], "color": "#70d4ff"},
                    {"range": [800, 1000], "color": "#FFF2CE"},
                    {"range": [1000, 1100], "color": "#FEB938"},
                    {"range": [1100, 1200], "color": "#FD9415"},
                    {"range": [1200, 1300], "color": "#E23201"},
                ],
            },
        ),
        go.Layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"),
    )


#########################
### Average over time ###
#########################


def overtime_fig(df):
    fig = px.line(df, x="created_time", y="value", color="sensor_nb")
    fig.update_layout(
        {
            "plot_bgcolor": "rgba(0, 0, 0, 0)",
            "paper_bgcolor": "rgba(0, 0, 0, 0)",
        }
    )
    return fig


def points_fig(df):
    fig = px.area(
        df,
        x="created_time",
        y="value",
        color="sensor_nb",
        facet_col="sensor_nb",
        facet_col_wrap=2,
    )
    fig.update_layout(
        {
            "plot_bgcolor": "rgba(0, 0, 0, 0)",
            "paper_bgcolor": "rgba(0, 0, 0, 0)",
        }
    )
    return fig


#################
### Datatable ###
#################


def datatable_raw(df):
    return dash_table.DataTable(
        id="datatable-paging",
        columns=[{"name": i, "id": i} for i in sorted(df.columns)],
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
        data=df.to_dict("records"),
        page_current=0,
        page_size=10,
        page_action="native",
    )


##############
### Layout ###
##############


layout = dbc.Container(
    [
        dbc.Row(
            html.H1(
                children="Conditions salle d'élevage", style={"textAlign": "center"}
            ),
        ),
        # Current average
        dbc.Row(
            [
                dbc.Col(id="average_temperature_graph"),
                dbc.Col(id="average_co2_graph"),
                dbc.Col(id="average_humidity_graph"),
            ]
        ),
        # Point by point
        dbc.Row(id="point_graph"),
        # Over time
        dbc.Row(
            [
                dbc.Col(html.P("Select sensor type:"), width=6),
                dbc.Col(
                    dcc.Dropdown(
                        id="dd_sensor_type",
                        options=["temperature", "humidity", "co2"],
                        value="temperature",
                        clearable=False,
                    ),
                    width=6,
                ),
                dbc.Col(id="graph_overtime", width=12),
                dbc.Col(
                    id="raw_datatable",
                    width={"size": 10, "offset": 1},
                ),
            ]
        ),
        dcc.Interval(
            id="interval-component",
            interval=10 * 1000,  # in milliseconds
            n_intervals=0,
        ),
    ],
    fluid=True,
)


#################
### Callbacks ###
#################


@callback(
    Output("average_temperature_graph", "children"),
    Output("average_humidity_graph", "children"),
    Output("average_co2_graph", "children"),
    Input("interval-component", "n_intervals"),
)
def update_averages(n):
    df = get_df_from_db()
    return (
        dcc.Graph(
            figure=average_temp_fig(
                df.query("level_0 == 'temperature'").iloc[-1]["value"],
                df.query("level_0 == 'temperature'").iloc[-2]["value"],
            )
        ),
        dcc.Graph(
            figure=average_humidity_fig(
                df.query("level_0 == 'humidity'").iloc[-1]["value"],
                df.query("level_0 == 'humidity'").iloc[-2]["value"],
            )
        ),
        dcc.Graph(
            figure=average_co2_fig(
                df.query("level_0 == 'co2'").iloc[-1]["value"],
                df.query("level_0 == 'co2'").iloc[-2]["value"],
            )
        ),
    )


@callback(
    Output("graph_overtime", "children"),
    Input("dd_sensor_type", "value"),
    Input("interval-component", "n_intervals"),
)
def update_overtime(dd_value, n):
    df = get_df_from_db()
    return dcc.Graph(figure=overtime_fig(df.query(f'level_0 == "{dd_value}"')))


@callback(Output("point_graph", "children"), Input("interval-component", "n_intervals"))
def update_points(n):
    df = get_df_from_db()
    return [
        dbc.Col(
            dcc.Graph(figure=points_fig(df.query("level_0 == 'temperature'"))), width=4
        ),
        dbc.Col(
            dcc.Graph(figure=points_fig(df.query("level_0 == 'humidity'"))), width=4
        ),
        dbc.Col(dcc.Graph(figure=points_fig(df.query("level_0 == 'co2'"))), width=4),
    ]


@callback(
    Output("raw_datatable", "children"), Input("interval-component", "n_intervals")
)
def update_points(n):
    df = get_df_from_db()
    return datatable_raw(df)
