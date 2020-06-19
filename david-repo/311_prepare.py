import pandas as pd
import numpy as np

def prepare_311(df):
    df = df.rename(columns=
        {
            "Late (Yes/No)": "Late", 
            "Council District": "Council_District", 
            "Report Starting Date": "Report_Start_Date", 
            "Report Ending Date": "Report_Ending_Date"
        })
    df.dropna(subset=['XCOORD', 'YCOORD'], inplace=True)
    
    
    