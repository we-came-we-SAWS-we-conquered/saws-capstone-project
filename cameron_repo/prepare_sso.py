import pandas as pd
import numpy as np
import acquire_sso
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
    df = acquire_sso.acquire_sso()
    bad_features = list(df.columns[~df.columns.isin(features)])
    df = df.drop(columns = bad_features)
    df = df.drop(columns = ['TIMEINT','STEPS_TO_PREVENT'])
    return df

def prepare_sso_df(df = filter_sso_features()):
    '''
    This function fixes datatypes, creates an extra feature, 
    and fills some of the null values
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
    df['days_since_cleaned'] = (df.SPILL_START - df.LASTCLND).dt.days
    return df

    #####################################################################

def prepare_sso_df2(df = filter_sso_features()):
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

#     def read_sso_dict():
#     '''
#     This function gets the data dictionary for SSO data and creates 
#     a csv
#     '''
#     if os.path.isfile('sso_dict.csv'):
#         df_dict = pd.read_csv('sso_dict.csv')
#     else:
#         url_sso_dict = '''https://storage.googleapis.com/sa_saws_data/SAWS_SSO_DataFieldDescription_MM.xlsx'''
#         df_dict = pd.read_excel(url_sso_dict)
#         df_dict.to_csv('sso_dict.csv', index=False)
#     return df_dict

# def get_sso_dict_features(df_dict = read_sso_dict()):
#     '''
#     This function prepares the data dictionary to filter the
#     SSO data with.
#     '''
#     unused = ['Disregard','Ignore','Service Req # (internal use only)',
#             'Not Used','Old mapping system reference (internal only)']
#     ready1_dict = df_dict[~df_dict['Data Description'].isin(unused)]
#     null_fields = ['SPILL_START_2','SPILL_START_3',
#                 'SPILL_STOP_2','SPILL_STOP_3']
#     final_dict = ready1_dict[~ready1_dict.Field.isin(null_fields)]\
#                         .reset_index(drop=True)
#     features_to_use = list(final_dict.Field)
#     return features_to_use

# def filter_sso_features(features = get_sso_dict_features()):
#     '''
#     This function gets the sso_data and filters out features
#     based on previous function
#     '''
#     df = acquire.acquire_sso()
#     bad_features = list(df.columns[~df.columns.isin(features)])
#     df = df.drop(columns = bad_features)
#     df = df.drop(columns = ['TIMEINT','STEPS_TO_PREVENT'])
#     return df

# def prepare_sso_df(df = filter_sso_features()):
#     '''
#     This function fixes datatypes, creates an extra feature, 
#     fills some of the null values, and renames columns
#     '''
#     string_features = ['SSO_ID','SPILL_ADDRESS','COUNCIL_DISTRICT',]
#     for col in string_features:
#         df[col] = df[col].astype(str)
#     time_features = ['REPORTDATE','SPILL_START','SPILL_STOP',
#                     'ResponseDTTM', 'LASTCLND']
#     for col in time_features:
#         df[col] = pd.to_datetime(df[col])   
#     fill_features = ['NUM_SPILLS_24MOS','PREVSPILL_24MOS','HRS_2',
#                     'HRS_3','GAL_2','GAL_3']
#     for col in fill_features:
#         df[col] = df[col].fillna(0)  
#     df.Root_Cause = df.Root_Cause.str.strip()
#     df.ResponseTime = df.ResponseTime * 60
#     df['days_since_cleaned'] = (df.SPILL_START - df.LASTCLND).dt.days
#     df.columns = ['sso_id','report_date','spill_address_num','spill_st_name',
#         'total_gal','gals_ret','spill_start','spill_stop','hrs','cause',
#         'comments','actions','watershed','unit_id','unit_id2','discharge_to',
#         'discharge_route','council_district','month','year','week',
#         'earz_zone','pipe_diam','pipe_len','pipe_type','inst_year','inches_no',
#         'rainfall_last3','spill_address_full','num_spills_recorded',
#         'num_spills_24mos','prevspill_24mos','unit_type','asset_type',
#         'last_cleaned','response_time','response_dttm','public_notice',
#         'root_cause','hrs_2','gal_2','hrs_3','gal_3','days_since_cleaned']
#     df.root_cause = df.root_cause.str.lower()
#     return df

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
    df.days_since_cleaned = df.days_since_cleaned.astype(float)\
                            .fillna(df.days_since_cleaned.median())
    df.zip_code = df.zip_code.str.strip()
    
    df.inst_year = df.inst_year.replace(9999,pd.NA)
    df['age'] = df.spill_start.dt.year - df.inst_year
    df.inst_year = df.inst_year.astype(str).replace('nan', 'unknown')
    df.age = df.age.replace([-3,-2,-1], pd.NA)
    z = pd.cut(df.age, bins=list(range(0,130,5)))
    df['age_binned'] = z
    df['hours_spilled'] = df.spill_stop - df.spill_start
    df.hours_spilled = df.hours_spilled / timedelta (hours=1)
    df.discharge_route = df.discharge_route.fillna('none')
    df.earz_zone = df.earz_zone.replace(np.NaN, 0.0)\
                                        .apply(round).astype(str)
    df.unit_type = df.unit_type.fillna('unknown')
    df.asset_type = df.asset_type.fillna('unknown')
    df.root_cause = df.root_cause.fillna('other')
    # df.age = df.age.fillna(df.age.median())
    df.pipe_type = df.pipe_type.fillna('unknown')
    df.pipe_diam = df.pipe_diam.fillna(df.pipe_diam.median())
    df.pipe_len = df.pipe_len.fillna(df.pipe_len.median())
    return df