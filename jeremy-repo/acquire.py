import pandas as pd
import os.path
import requests
import io

def acquire_sso():
    '''
    Checks if csv exists; if yes, reads csv. If no, reads url
    into dataframe and writes to csv. Returns dataframe.
    '''
    if os.path.isfile('sso_data.csv'):
        sso_data = pd.read_csv('sso_data.csv')
    else:
        url_sso_data = ('https://storage.googleapis.com/sa_saws_data/SAWS_SSOs_2009-2018Mar_UploadData.xlsx')
        sso_data = pd.read_excel(url_sso_data)
        sso_data.to_csv('sso_data.csv', index=False)
    return sso_data

def acquire_weather():
    '''
    Takes no arguments and returns a pd.DataFrame with weather data
    '''
    if os.path.isfile('weather_data.csv'):
        weather_data = pd.read_csv('weather_data.csv')
    else:
        # Parameters for the query to the API
        dataset = 'dataset=daily-summaries'
        features = 'dataTypes=WT03,PRCP,WT05,WT06,WT07,WT08,SNWD,WT09,WDF2,WDF5,PGTM,WT11,TMAX,WT13,WSF2,FMTM,WSF5,SNOW,WT16,WT17,WT18,WT19,AWND,WT01,WT02,TAVG,TMIN,WT10,WT16'
        station = 'stations=USW00012921'
        start_date = 'startDate=2008-12-03'
        end_date = 'endDate=2019-04-03'
        include_attributes = 'includeAttributes=false'
        format_type = 'format=csv'
        
        # Request the data from NCEI API
        response = requests.get(f'''https://www.ncei.noaa.gov/access/services/data/v1?{dataset}&{features}&{station}&{start_date}&{end_date}&{include_attributes}&{format_type}''')
        
        # Read the csv data and return
        weather_data = pd.read_csv(io.StringIO(response.text))

        # Create a csv for future reads
        weather_data.to_csv('weather_data.csv', index=False)
    
    return weather_data

def acquire_311():
    '''
    Takes no arguments
    Returns 311 calls dataframe:
    - checks for csv locally
        - if present, reads to dataframe 
        - else, creates csv
    '''
    if os.path.isfile('data_311.csv'):
        data_311 = pd.read_csv('data_311.csv')
    else:
        url = "https://data.sanantonio.gov/dataset/93b0e7ee-3a55-4aa9-b27b-d1817e91aec3/resource/20eb6d22-7eac-425a-85c1-fdb365fd3cd7/download/allservicecalls.csv"
        data_311 = pd.read_csv(url)
        data_311.to_csv('data_311.csv', index=False)     
    return data_311