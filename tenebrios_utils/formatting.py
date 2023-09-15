from datetime import datetime
import pandas as pd
import re


def timestamp_to_readable_datetime(date) -> datetime:
    return datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")


def api_date_to_datetime(date) -> datetime:
    return pd.to_datetime(date, format="%Y-%m-%dT%H:%M:%S.%fZ")


def add_space_before_caps(str):
    return re.sub("([A-Z])", r" \1", str)
