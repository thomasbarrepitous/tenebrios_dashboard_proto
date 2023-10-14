from tenebrios_utils import apiAuth
import pandas as pd
from datetime import datetime


def get_date_mec_from_actions_df(actions_df: pd.DataFrame) -> datetime:
    """Return the date of the Mise En Culture."""
    return actions_df.query("resourcetype == 'MiseEnCulture'")["date"].values[0]


def get_date_recolte_from_actions_df(actions_df: pd.DataFrame) -> datetime:
    """Return the date of the Recolte."""
    return actions_df.query("resourcetype == 'Recolte'")["date"].values[0]


def get_nb_bacs_from_actions_df(actions_df: pd.DataFrame) -> int:
    pass


def get_qte_recolte_from_actions_df(actions_df: pd.DataFrame) -> int:
    return sum(
        actions_df.query("resourcetype == 'Recolte'")["harvested_quantity"].values
    )


def get_imw_recolte_from_actions_df(actions_df: pd.DataFrame) -> int:
    actions_df["date"] = pd.to_datetime(actions_df["date"])
    filtered_df = actions_df[actions_df["imw100_weight"].notnull()]
    latest_row = filtered_df.loc[filtered_df["date"].idxmax()]
    return latest_row["imw100_weight"]


def get_total_son_from_actions_df(actions_df: pd.DataFrame) -> int:
    return sum(
        actions_df.query("resourcetype == 'NourrissageSon'")["given_quantity"].values
    )


def get_total_nourriture_humide_from_actions_df(actions_df: pd.DataFrame) -> int:
    return sum(
        actions_df.query("resourcetype == 'NourrissageHumide'")["given_quantity"].values
    )


def get_feed_ratio_conversion_from_actions_df(actions_df: pd.DataFrame) -> int:
    # filtered_df = actions_df.dropna(subset=["given_quantity", "sieved_quantity"])
    sum_of_given_over_sieved = (
        actions_df["given_quantity"].sum() / actions_df["sieved_quantity"].sum()
    )
    return sum_of_given_over_sieved.round(2)


def get_croissance_journaliere_moyenne_from_actions_df(actions_df: pd.DataFrame) -> int:
    pass


def get_assimilation_moyenne_from_actions_df(actions_df: pd.DataFrame) -> int:
    assimilation_moyenne = (
        actions_df["given_quantity"].sum() / actions_df["sieved_quantity"].sum()
    ) * 100
    return assimilation_moyenne
