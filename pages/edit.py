import dash
from dash import callback, Output, Input, State, ALL, html, dcc
import dash_bootstrap_components as dbc
from tenebrios_utils import formatting, apiCalls
from ui_components import common, edit
from dash.exceptions import PreventUpdate

dash.register_page(
    __name__,
    path_template="/tracability/action/<action_id>",
)


def display_edit_form_mec(action: dict):
    return dbc.Form(
        [
            common.centered_title(action["recolte_nb"]),
            common.centered_title(
                formatting.add_space_before_caps(action["resourcetype"])
            ),
            edit.basic_edit_input(action["recolte_nb"], "Recolte number"),
            edit.basic_edit_input(action["column"], "Column"),
            common.date_picker_form("Date", value=action["date"]),
        ],
        id="edit-form-mec",
    )


def display_edit_form_marc(action: dict):
    return dbc.Form(
        [
            common.centered_title(action["recolte_nb"]),
            common.centered_title(
                formatting.add_space_before_caps(action["resourcetype"])
            ),
            edit.basic_edit_input(action["recolte_nb"], "Recolte number"),
            edit.basic_edit_input(action["column"], "Column"),
            common.date_picker_form("Date", value=action["date"]),
            edit.basic_edit_input(action["given_quantity"], "Given quantity"),
            edit.basic_edit_input(action["given_quantity_bac"], "Given quantity / bac"),
            common.date_picker_form(
                "Marc Arrival Date", value=action["marc_arrival_date"]
            ),
            edit.basic_edit_switch("Is Anomaly", action["anomaly"]),
            html.Div(
                edit.basic_edit_text_area("Anomaly Comment", ""),
                id="anomalie-switch-output",
            ),
            edit.basic_edit_switch("Is IMW100 Weighted", action["is_imw100_weighted"]),
            html.Div(
                edit.basic_edit_text_area("IMW100 Weight", ""),
                id="pesage-switch-output",
            ),
        ],
        id="edit-form-marc",
    )


def display_edit_form_son(action: dict):
    return dbc.Form(
        [
            common.centered_title(action["recolte_nb"]),
            common.centered_title(
                formatting.add_space_before_caps(action["resourcetype"])
            ),
            edit.basic_edit_input(action["recolte_nb"], "Recolte number"),
            edit.basic_edit_input(action["column"], "Column"),
            common.date_picker_form("Date", value=action["date"]),
            edit.basic_edit_input(action["given_quantity"], "Given quantity"),
            edit.basic_edit_input(action["given_quantity_bac"], "Given quantity / bac"),
            common.date_picker_form(
                "Son Arrival Date", value=action["son_arrival_date"]
            ),
        ],
        id="edit-form-recolte",
    )


def display_edit_form_tamisage(action: dict):
    return dbc.Form(
        [
            common.centered_title(action["recolte_nb"]),
            common.centered_title(
                formatting.add_space_before_caps(action["resourcetype"])
            ),
            edit.basic_edit_input(action["recolte_nb"], "Recolte number"),
            edit.basic_edit_input(action["column"], "Column"),
            common.date_picker_form("Date", value=action["date"]),
            edit.basic_edit_input(action["sieved_quantity"], "Sieved quantity"),
        ],
        id="edit-form-recolte",
    )


def display_edit_form_recolte(action: dict):
    return dbc.Form(
        [
            common.centered_title(action["recolte_nb"]),
            common.centered_title(
                formatting.add_space_before_caps(action["resourcetype"])
            ),
            edit.basic_edit_input(action["recolte_nb"], "Recolte number"),
            edit.basic_edit_input(action["column"], "Column"),
            common.date_picker_form("Date", value=action["date"]),
            edit.basic_edit_input(action["harvested_quantity"], "Harvested quantity"),
        ],
        id="edit-form-recolte",
    )


def display_layout():
    return dbc.Container(
        [
            dcc.Location(id="url", refresh=False),
            dcc.Store(id="api-action-store"),
            html.Div(id="edit-action-form"),
            common.send_form_button(),
            common.refresh_page_button("Reinitialiser"),
            common.delete_form_button(href="/tracability"),
            html.Div(id="dummy-output"),
        ]
    )


def layout(action_id):
    return display_layout()


#############
# Callbacks #
#############


@callback(
    Output("api-action-store", "data"),
    Input("url", "pathname"),
)
def update_action_store(pathname):
    action_id = pathname.split("/")[-1]
    return apiCalls.get_action_by_id(action_id)


@callback(
    Output("dummy-output", "children"),
    Input("submit-button", "n_clicks"),
    Input("url", "pathname"),
    State({"type": "input-data", "index": ALL}, "id"),
    State({"type": "input-data", "index": ALL}, "value"),
    State({"type": "date-data", "index": ALL}, "id"),
    State({"type": "date-data", "index": ALL}, "date"),
    State("api-action-store", "data"),
)
def send_put_request(
    n_clicks, pathname, input_ids, input_values, date_ids, date_values, action
):
    "Capture all input and date IDs and values and send them to the API"
    action_id = pathname.split("/")[-1]
    if n_clicks:
        put_data: dict = {}
        input_ids = date_ids + input_ids
        input_values = date_values + input_values
        for id, values in zip(input_ids, input_values):
            # Elements' IDs are generated by their labels, so we need to parse them back to the API's request IDs
            put_data[formatting.form_index_to_request_id_edit(id["index"])] = values
        if action["resourcetype"] == "NourrissageHumide":
            # Check the state of the switches and reset text area values if switches are off
            if not put_data["anomaly"]:
                put_data[
                    formatting.form_index_to_request_id_edit("textarea-anomaly-comment")
                ] = ""
            if not put_data["is_imw100_weighted"]:
                put_data[
                    formatting.form_index_to_request_id_edit("textarea-imw100-weight")
                ] = ""
        apiCalls.put_action(put_data, action_id)
    return None


@callback(
    Output("anomalie-switch-output", "style"),
    [Input({"type": "input-data", "index": "switch-is-anomaly"}, "value")],
)
def display_anomalie_comment(value):
    if value:
        return {"display": "block"}
    return {"display": "none"}


@callback(
    Output("pesage-switch-output", "style"),
    [Input({"type": "input-data", "index": "switch-is-imw100-weighted"}, "value")],
)
def display_pesage_comment(value):
    if value:
        return {"display": "block"}
    return {"display": "none"}


@callback(Output("refresh_page_button", "href"), [Input("url", "pathname")])
def refresh_page_button(relative_pathname):
    return relative_pathname


@callback(
    Output("dummy-output", "childre", allow_duplicate=True),
    Input("delete-button", "n_clicks"),
    State("url", "pathname"),
    prevent_initial_call=True,
)
def delete_page_button(n_clicks, pathname):
    if n_clicks > 0:
        action_id = pathname.split("/")[-1]
        apiCalls.delete_action(action_id)


@callback(
    Output("edit-action-form", "children"),
    Input("api-action-store", "data"),
)
def render_action_form(action):
    if action is None:
        raise PreventUpdate
    elif action["resourcetype"] == "NourrissageHumide":
        return display_edit_form_marc(action)
    elif action["resourcetype"] == "NourrissageSon":
        return display_edit_form_son(action)
    elif action["resourcetype"] == "Tamisage":
        return display_edit_form_tamisage(action)
    elif action["resourcetype"] == "Recolte":
        return display_edit_form_recolte(action)
    elif action["resourcetype"] == "MiseEnCulture":
        return display_edit_form_mec(action)
