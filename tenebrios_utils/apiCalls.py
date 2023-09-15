import requests
import json
from tenebrios_utils import apiAuth
import pandas as pd


API_URL = f"http://127.0.0.1:8000/api"


###################
### Tracability ###
###################


def post_action(post_data):
    response = requests.post(f"{API_URL}/actions", data=post_data, auth=apiAuth.auth)
    if response.status_code == 201:
        print(f"POST request successful. Response: {response.text}")
    else:
        print(f"POST request failed. Status Code: {response.text}")
    return response.status_code


def get_action_by_id(action_id: str) -> dict:
    r = requests.get(f"{API_URL}/actions/{action_id}", auth=apiAuth.auth)
    if r.status_code != 200:
        print(f"Error code {r.status_code}")
        return {}
    action = json.loads(r.text)
    return action


def get_all_actions():
    return json.loads(requests.get(f"{API_URL}/actions", auth=apiAuth.auth).text)


def get_column_actions(column: str):
    return json.loads(
        requests.get(f"{API_URL}/actions?column={column}", auth=apiAuth.auth).text
    )


def get_all_columns():
    return json.loads(
        requests.get(f"{API_URL}/actions/columns", auth=apiAuth.auth).text
    )


def get_cycle_from_recolte(recolte_nb: str):
    return json.loads(
        requests.get(
            f"{API_URL}/actions/recolte-nb/{recolte_nb}/cycle", auth=apiAuth.auth
        ).text
    )


def get_all_recolte_paginated(filters, current_page, cycle_page_size):
    r_uri = f"{API_URL}/actions/recolte-nb?{filters}&limit={cycle_page_size}&offset={(current_page-1)*cycle_page_size}"
    return json.loads(requests.get(r_uri, auth=apiAuth.auth).text)


# Fetch specific recolte in the API
def get_details_from_recolte_nb(recolte_nb):
    """Fetch all actions for given recolte_nb."""
    return json.loads(
        requests.get(
            f"{API_URL}/actions/recolte-nb/{recolte_nb}", auth=apiAuth.auth
        ).text
    )


#######################
### Weather Station ###
#######################


def get_sensor_by_name(suffix):
    return json.loads(requests.get(f"{API_URL}{suffix}/", auth=apiAuth.auth).text)


def get_df_from_db():
    co2_r, temperature_r, humidity_r = (
        get_sensor_by_name("co2"),
        get_sensor_by_name("temperature"),
        get_sensor_by_name("humidity"),
    )
    df = pd.concat(
        [
            pd.DataFrame.from_records(co2_r),
            pd.DataFrame.from_records(temperature_r),
            pd.DataFrame.from_records(humidity_r),
        ],
        keys=["co2", "temperature", "humidity"],
    )
    df = df.reset_index()
    return df
