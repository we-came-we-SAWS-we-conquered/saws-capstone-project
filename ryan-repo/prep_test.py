import pandas as pd
import acquire


def remove_weather_columns(df):
    '''
    Takes in the weather dataframe, removes listed columns and returns the dataframe
    '''
    return df.drop(
        columns=[
            "STATION",
            "AWND",
            "FMTM",
            "PGTM",
            "WDF2",
            "WDF5",
            "WSF2",
            "WSF5",
            "WT06",
            "WT07",
            "WT08",
            "WT10",
            "WT11",
            "WT13",
            "WT17",
            "WT18",
            "WT19",
        ]
    )


def fix_weather_column_names(df):
    keys = df.columns.tolist()

    values = [
        "date",
        "precipitation",
        "snowfall",
        "snow_depth",
        "avg_temp",
        "max_temp",
        "min_temp",
        "foggy",
        "heavy_fog",
        "thunder",
        "hail",
        "blowing_snow",
        "rain",
    ]

    col_name_dict = dict(zip(keys, values))

    return df.rename(columns=col_name_dict)

def handle_missing_weather_data(df):
    df.avg_temp = df.avg_temp.fillna((df.max_temp + df.min_temp) / 2)
    
    boolean_columns = ['foggy','heavy_fog','thunder','hail','blowing_snow','rain']

    for column in boolean_columns:
        df[f'{column}'] = df[f'{column}'].fillna(0).astype(int)
    
    return df

def add_features(df):
    rolling_periods = [7, 14, 30]
    features = ['precipitation', 'avg_temp', 'max_temp', 'min_temp']

    for feature in features:
        for period in rolling_periods:
            df[f'{feature}_rolling_{period}'] = df[f'{feature}'].rolling(period).mean()
    
    return df

def prep_weather_data():
    weather = acquire.acquire_weather()
    weather = remove_weather_columns(weather)
    weather = fix_weather_column_names(weather)
    weather = handle_missing_weather_data(weather)
    weather.date = pd.to_datetime(weather.date)
    weather = weather.sort_values("date").set_index("date")
    weather = add_features(weather)
    
    return weather