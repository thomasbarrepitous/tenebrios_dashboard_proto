from datetime import datetime
import pandas as pd
import re


def timestamp_to_readable_datetime(date: str) -> datetime:
    return datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")


def api_date_to_datetime(date: str) -> datetime:
    return pd.to_datetime(date, format="%Y-%m-%dT%H:%M:%S.%fZ")


def add_space_before_caps(str: str) -> str:
    return re.sub("([A-Z])", r" \1", str)


def format_to_form_index(label: str) -> str:
    label = label.replace("/ ", "")
    return label.replace(" ", "-").lower()


# TODO: Unifiy all form indexes
def form_index_to_request_id(form_index: str) -> str:
    if form_index == "Marc-bac":
        return "given_quantity_bac"
    elif form_index == "Marc-total":
        return "given_quantity"
    elif form_index == "Son-bac":
        return "given_quantity_bac"
    elif form_index == "Son-total":
        return "given_quantity"
    elif form_index == "datearrivagemarc":
        return "marc_arrival_date"
    elif form_index == "datearrivageson":
        return "son_arrival_date"
    elif form_index == "Qtetamisée":
        return "sieved_quantity"
    elif form_index == "Qterécoltée":
        return "harvested_quantity"
    return form_index


def form_index_to_request_id_edit(form_index: str) -> str:
    index_to_request_map = {
        "edit-recolte-number": "recolte_nb",
        "edit-column": "column",
        "edit-given-quantity-bac": "given_quantity_bac",
        "edit-given-quantity": "given_quantity",
        "marc-arrival-date": "marc_arrival_date",
        "son-arrival-date": "son_arrival_date",
        # "sieved-quantity": "sieved_quantity",
        # "harvested-quantity": "harvested_quantity",
        "switch-is-anomaly": "anomaly",
        "textarea-anomaly-comment": "anomaly_comment",
        "switch-is-imw100-weighted": "is_imw100_weighted",
        "textarea-imw100-weight": "imw100_weight",
    }
    return index_to_request_map.get(form_index, form_index)
