import pandas as pd
import numpy as np
import acquire
import os.path
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Nominatim
from datetime import timedelta

def read_sso_dict():
    '''
    This function gets the data dictionary for SSO data and creates 
    a csv
    '''
    if os.path.isfile('sso_dict.csv'):
        df_dict = pd.read_csv('sso_dict.csv')
    else:
        url_sso_dict = '''https://storage.googleapis.com/sa_saws_data/SAWS_SSO_DataFieldDescription_MM.xlsx'''
        df_dict = pd.read_excel(url_sso_dict)
        df_dict.to_csv('sso_dict.csv', index=False)
    return df_dict

def get_sso_dict_features(df_dict = read_sso_dict()):
    '''
    This function prepares the data dictionary to filter the
    SSO data with.
    '''
    unused = ['Disregard','Ignore','Service Req # (internal use only)',
            'Not Used','Old mapping system reference (internal only)']
    ready1_dict = df_dict[~df_dict['Data Description'].isin(unused)]
    null_fields = ['SPILL_START_2','SPILL_START_3',
                'SPILL_STOP_2','SPILL_STOP_3']
    final_dict = ready1_dict[~ready1_dict.Field.isin(null_fields)]\
                        .reset_index(drop=True)
    features_to_use = list(final_dict.Field)
    return features_to_use

def filter_sso_features(features = get_sso_dict_features()):
    '''
    This function gets the sso_data and filters out features
    based on previous function
    '''
    df = acquire.acquire_sso()
    bad_features = list(df.columns[~df.columns.isin(features)])
    df = df.drop(columns = bad_features)
    df = df.drop(columns = ['TIMEINT','STEPS_TO_PREVENT'])
    return df

def prepare_sso_df(df = filter_sso_features()):
    '''
    This function fixes datatypes, creates an extra feature, 
    fills some of the null values, and renames columns
    '''
    string_features = ['SSO_ID','SPILL_ADDRESS','COUNCIL_DISTRICT',]
    for col in string_features:
        df[col] = df[col].astype(str)
    time_features = ['REPORTDATE','SPILL_START','SPILL_STOP',
                    'ResponseDTTM', 'LASTCLND']
    for col in time_features:
        df[col] = pd.to_datetime(df[col])   
    fill_features = ['NUM_SPILLS_24MOS','PREVSPILL_24MOS','HRS_2',
                    'HRS_3','GAL_2','GAL_3']
    for col in fill_features:
        df[col] = df[col].fillna(0)  
    df.Root_Cause = df.Root_Cause.str.strip()
    df.ResponseTime = df.ResponseTime * 60
    df['days_since_cleaned'] = (df.SPILL_START - df.LASTCLND).dt.days
    df.columns = ['sso_id','report_date','spill_address_num','spill_st_name',
        'total_gal','gals_ret','spill_start','spill_stop','hrs','cause',
        'comments','actions','watershed','unit_id','unit_id2','discharge_to',
        'discharge_route','council_district','month','year','week',
        'earz_zone','pipe_diam','pipe_len','pipe_type','inst_year','inches_no',
        'rainfall_last3','spill_address_full','num_spills_recorded',
        'num_spills_24mos','prevspill_24mos','unit_type','asset_type',
        'last_cleaned','response_time','response_dttm','public_notice',
        'root_cause','hrs_2','gal_2','hrs_3','gal_3','days_since_cleaned']
    df.root_cause = df.root_cause.str.lower()
    return df

def prepare_sso_with_zipcodes(df = prepare_sso_df()):
    '''
    This function creates a zipcode column in the dataframe using 
    geopy against the street address given in the raw data.
    It checks if a csv exists, and uses that instead of running the
    code because it takes a very long time to gather all the data.
    It imputes some columns and adds a few new features.
    '''
    time_features = ['report_date','spill_start','spill_stop',
                    'response_dttm', 'days_since_cleaned']
    if os.path.isfile('SSO_with_zip_codes.csv'):
        df = pd.read_csv('SSO_with_zip_codes.csv', 
                            parse_dates= time_features, 
                            )
    else:
        locator = Nominatim(user_agent="myGeocoder")
        geocode = RateLimiter(locator.geocode, min_delay_seconds=.1, 
                            max_retries=10, error_wait_seconds=1)
        df['location'] = df['country_address'].apply(geocode)
        df['zip_code'] = 'None'
        for t,l in enumerate(df.location):
            if l is not None:
                df['zip_code'][t] = l.raw['display_name'].split(',')[-2]
    x = pd.cut(df.total_gal, bins=[0,15,50,250,1000, 5000,50000,2000000,
                               df.total_gal.max()])
    df['total_gal_binned'] = x
    df.days_since_cleaned = df.days_since_cleaned.astype(float)
    df.zip_code = df.zip_code.str.strip()
    
    df.inst_year = df.inst_year.replace(9999,pd.NA)
    df['age'] = df.spill_start.dt.year - df.inst_year
    df.inst_year = df.inst_year.astype(str).replace('nan', 'unknown')
    df.age = df.age.replace([-3,-2,-1], pd.NA)
    z = pd.cut(df.age, bins=list(range(0,130,5)))
    df['age_binned'] = z
    df['hours_spilled'] = df.spill_stop - df.spill_start
    df.hours_spilled = df.hours_spilled / timedelta (hours=1)
    df.discharge_route = df.discharge_route.replace(pd.NA,'none')
    df.earz_zone = df.earz_zone.replace(np.NaN, 0.0)\
                                        .apply(round).astype(str)
    df.unit_type = df.unit_type.replace(np.NaN, 'unknown')
    df.asset_type = df.asset_type.replace(np.NaN, 'unknown')

    # df = df[(df.zip_code != 'None') & (df.zip_code != 'Texas')]
    return df


# 311 prepare
def rename_311_columns(df):
    '''
    Returns a dataframe
        - renames columns of the dataframe:
            - removes spaces
            - improves naming convesion
    '''
    return df.rename(columns=
        {
            "CASEID": "CASE_ID",
            "OPENEDDATETIME": "DATE_TIME_OPENED",
            "SLA_Date": "assigned_Due_date",
            "CLOSEDDATETIME": "DATE_TIME_CLOSED",
            "Late (Yes/No)": "Late",
            "REASONNAME": "Reason_Name",
            "TYPENAME": "Event_Name",
            "CaseStatus": "Case_Status",
            "OBJECTDESC": "event_address",
            "Council District": "Council_District", 
            "Report Starting Date": "Report_Start_Date", 
            "Report Ending Date": "Report_Ending_Date"
        })


def negative_clean_up(value):
    """
    Converts all negative values to 0
    """
    if value<0:
        return 0
    else:
        return(value)

def create_311_coulmns(df):
    '''
    Returns a dataframe
        - creates new columns of the following:
            - zip_code, the zip_code of the report
            - assigned_due_date, date case assigned to a deptment
            - reported_date, date the case was reported 
            - closed_date, date the case was closed
            - due_date, date the case should be completed
            - case_days, length of days from report to close
            - report_to_assigned_days, length of days from report to assigned
            - days_past_due, length of days past the due date
            - 30_days, cases closed with 30 days or less from report to closed
            - 60_days, cases closed with 60 days or less from report to closed
            - 90_days, cases closed with 90 days or less from report to closed
    '''
    df['zip_code'] = df.event_address.str.extract(r'.+(\d{5}?)$').astype(str)
    df['assigned_due_date'] = df.assigned_due_date.fillna(df.date_time_opened)
    df['reported_date'] = pd.to_datetime(df['date_time_opened'])
    df['closed_date'] = pd.to_datetime(df['date_time_closed'])
    df['due_date'] = pd.to_datetime(df['assigned_due_date'])
    df['closed_date'] = df.closed_date.fillna(pd.to_datetime('today'))
    df['case_days'] = (df.closed_date - df.reported_date)
    df['case_days'] = (df.case_days.fillna(df.case_days.max())) 
    df['case_days'] = (df.case_days.dt.days)
    df['report_to_assigned_days'] = (df.due_date - df.reported_date)
    df['report_to_assigned_days'] = (df.report_to_assigned_days.fillna(df.report_to_assigned_days.max()))
    df['report_to_assigned_days'] = (df.report_to_assigned_days.dt.days)
    df['days_past_due'] = (df.closed_date - df.due_date)
    df['days_past_due'] = (df.days_past_due.fillna(df.days_past_due.max()))
    df['days_past_due'] = (df.days_past_due.dt.days)
    df['days_past_due'] = df['days_past_due'].apply(negative_clean_up)
    df['30_days'] = df.case_days <= 30
    df['60_days'] = ((df.case_days > 30) & (df.case_days <= 60))
    df['90_days'] = df.case_days >= 90
    
    return df

def drop_311_columns(df):
    return df.drop(columns=(['date_time_opened', 'assigned_due_date', 'date_time_closed', 'xcoord', 'ycoord']))

def prepare_311(df):
    '''
    Returns a cleaned dataframe of the 311 data 
    '''
    df = rename_311_columns(df)
    keys = df.columns.to_list()
    values = df.columns.to_list()
    values = [v.lower() for v in values]
    dictionary = dict(zip(keys, values))
    df = df.rename(columns=dictionary)
    df = create_311_coulmns(df)
    df = drop_311_columns(df)
    df = df[(df.event_name.str.contains('Drainage')) & (df.category == 'Streets & Infrastructure')]
    df.dropna(subset = ['zip_code'], inplace=True)
    df.dropna(subset = ['dept'], inplace=True)
    df.to_csv('cleaned_311.csv')
    df = pd.read_csv('cleaned_311.csv', index_col=0)
    
    return df

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
    '''
    Takes in the weather dataframe and fixes the column names and returns a dataframe
    '''
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
    '''
    Takes in the weather dataframe and handles missing data and returns a dataframe
    '''
    df.avg_temp = df.avg_temp.fillna((df.max_temp + df.min_temp) / 2)
    
    boolean_columns = ['foggy','heavy_fog','thunder','hail','blowing_snow','rain']

    for column in boolean_columns:
        df[f'{column}'] = df[f'{column}'].fillna(0).astype(int)
    
    return df

def add_features(df):
    '''
    Takes in the weather dataframe and adds new features and returns a dataframe
    '''
    rolling_periods = [7, 14, 30]
    features = ['precipitation', 'avg_temp', 'max_temp', 'min_temp']

    for feature in features:
        for period in rolling_periods:
            df[f'{feature}_rolling_{period}'] = df[f'{feature}'].rolling(period).mean()
    
    return df

def prep_weather_data():
    '''
    Takes no arguments and returns a clean weather dataframe
    '''
    weather = acquire.acquire_weather()
    weather = remove_weather_columns(weather)
    weather = fix_weather_column_names(weather)
    weather = handle_missing_weather_data(weather)
    weather.date = pd.to_datetime(weather.date)
    weather = weather.sort_values("date").set_index("date")
    weather = add_features(weather)
    
    return weather

def get_data():
    weather = prep_weather_data()
    sso = prepare_sso_with_zipcodes()
    data = sso.merge(weather, left_on='report_date', right_index=True)
    
    return data