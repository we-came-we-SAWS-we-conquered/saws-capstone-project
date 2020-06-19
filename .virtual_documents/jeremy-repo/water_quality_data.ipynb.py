import pandas as pd
import numpy as np


eaa = pd.read_csv("EAA.csv")
sara = pd.read_csv("sara_water_quality_data_Bexar.csv")


eaa.info()


eaa.isna().sum() / len(eaa) * 100


sara.info()


prcnt_sara = sara.isna().sum() / len(sara) * 100

prcnt_sara.sort_values(ascending=False)


url_data_dict_311 = '''https://storage.googleapis.com/sa_cosa_data/311DataExtractDataDictionary.xlsx'''
pd.read_excel(url_data_dict_311)



pd.set_option('max_colwidth', 500)
url_data_dict = '''https://storage.googleapis.com/sa_saws_data/\
SAWS_SSO_DataFieldDescription_MM.xlsx'''
sso = pd.read_excel(url_data_dict)


sso



