import pandas as pd
import acquire_sso
import os.path

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