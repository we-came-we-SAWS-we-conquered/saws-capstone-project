import pandas as pd
from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype

import prepare


def remove_columns(df):
    columns_to_drop_from_model = [
        "sso_id",
        "report_date",
        "spill_address_num",
        "spill_st_name",
        "spill_stop",
        "spill_start",
        "cause",
        "comments",
        "actions",
        "month",
        "year",
        "week",
        "spill_address_full",
        "last_cleaned",
        "response_dttm",
        "prevspill_24mos",
        "public_notice",
        "country_address",
        "location",
        "inches_no",
        "rainfall_last3",
        "unit_id",
        "unit_id2",
        "zip_code",
        "discharge_to",
        "discharge_route",
        "council_district",
        "hours_spilled",
        "hrs",
        "gals_ret",
        "response_time"
    ]

    return df.drop(columns=columns_to_drop_from_model)


def fix_nas(df):
    df.pipe_type = df.pipe_type.fillna('Unknown')
    df.root_cause = df.root_cause.fillna('Unknown')
    df.days_since_cleaned = df.days_since_cleaned.fillna(df.days_since_cleaned.median())
    df.pipe_diam = df.pipe_diam.fillna(df.pipe_diam.median())
    df.pipe_len = df.pipe_len.fillna(df.pipe_len.median())
    df.age = df.age.replace('unknown', 0)
    df.age = df.age.replace(0, df.age.median())
    return df


def encode_categorical_columns(df):
    categorical_columns = [
        "watershed",
        "earz_zone",
        "pipe_type",
        "inst_year",
        "unit_type",
        "asset_type",
        "age_binned",
        "total_gal_binned",
    ]

    for column in categorical_columns:

        if is_numeric_dtype(df[f"{column}"]):
            values = df[f"{column}"].unique()

            for value in values:
                df[f"{column}_is_{value}"] = (df[f"{column}"] == value).astype(int)

            df = df.drop(columns=column)

        elif is_string_dtype(df[f"{column}"]):
            values = df[f"{column}"].astype(str).str.lower().unique()

            for value in values:
                df[f"{column}_is_{value}"] = (df[f"{column}"] == value).astype(int)

            df = df.drop(columns=column)

    return df


def get_model_data():
    data = prepare.get_data()
    data = remove_columns(data)
    data = fix_nas(data)
    data = encode_categorical_columns(data)

    return data