import dash
import dash_bootstrap_components as dbc
from tenebrios_utils.apiCalls import get_action_by_id
from ui_components import common, edit

dash.register_page(__name__, path_template="/tracability/action/<action_id>")


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


def display_edit_form(action: dict):
    return dbc.Form(
        [
            common.centered_title(action["recolte_nb"]),
            edit.basic_edit_input(action["recolte_nb"], "Recolte number"),
            edit.basic_edit_input(action["column"], "Column"),
            common.date_picker_form("Date", value=action["date"]),
            edit.basic_edit_input(action["given_quantity"], "Given quantity"),
            edit.basic_edit_input(action["given_quantity_bac"], "Given quantity / bac"),
            common.date_picker_form(
                "Marc Arrival Date", value=action["marc_arrival_date"]
            ),
            edit.basic_edit_switch("Is Anomaly", action["anomaly"]),
            edit.basic_edit_text_area("Anomaly Comment", action["anomaly_comment"]),
            edit.basic_edit_switch("Is IMW100 Weighted", action["is_imw100_weighted"]),
            edit.basic_edit_text_area("IMW100 Weight", action["imw100_weight"]),
        ],
        id="edit_form",
    )


def display_layout(action: dict):
    return dbc.Container(display_edit_form(action))


def layout(action_id):
    action = get_action_by_id(action_id)
    return display_layout(action)
