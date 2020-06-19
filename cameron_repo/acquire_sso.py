import pandas as pd
import os.path

def acquire_sso():
    if os.path.isfile('sso_data.csv'):
        sso_data = pd.read_csv('sso_data.csv')
    else:
        url_sso_data = ('https://storage.googleapis.com/sa_saws_data/SAWS_SSOs_2009-2018Mar_UploadData.xlsx')
        sso_data = pd.read_excel(url_sso_data)
        sso_data.to_csv('sso_data.csv', index=False)
    return sso_data