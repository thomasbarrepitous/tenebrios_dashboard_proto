import requests
import json
from . import apiAuth


API_URL = f"http://127.0.0.1:8000/api/actions"


def post_action(post_data):
    response = requests.post(API_URL, data=post_data, auth=apiAuth.auth)
    if response.status_code == 201:
        print(f"POST request successful. Response: {response.text}")
    else:
        print(f"POST request failed. Status Code: {response.text}")
    return response.status_code


def get_all_actions():
    return json.loads(requests.get(f"{API_URL}", auth=apiAuth.auth).text)


def get_column_actions(column: str):
    return json.loads(
        requests.get(f"{API_URL}?column={column}", auth=apiAuth.auth).text
    )


def get_all_columns():
    return json.loads(requests.get(f"{API_URL}/columns", auth=apiAuth.auth).text)


def get_cycle_from_recolte(recolte_nb: str):
    return json.loads(
        requests.get(f"{API_URL}/recolte-nb/{recolte_nb}/cycle", auth=apiAuth.auth).text
    )


def get_all_recolte_paginated(filters, current_page, cycle_page_size):
    r_uri = f"{API_URL}/recolte-nb?{filters}&limit={cycle_page_size}&offset={(current_page-1)*cycle_page_size}"
    return json.loads(requests.get(r_uri, auth=apiAuth.auth).text)
