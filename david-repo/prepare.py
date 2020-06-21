import pandas as pd
import numpy as np

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

def create_311_coulmns(df):
    '''
    Returns a dataframe
        - creates new columns of the following:
            - zip_code, the zip_code of the report
            - assigned_due_date, date case assigned to a deptment
            - reported_date, date the case was reported 
            - closed_date, date the case was closed
            - due_date, date the case should be completed
            - case_days_length, length of days from report to close
            - report_to_assigned_days_length, length of days from report to assigned
            - days_past_due_length, length of days past the due date
    '''
    df['zip_code'] = df.event_address.str.extract(r'.+(\d{5}?)$')
    df['assigned_due_date'] = df.assigned_due_date.fillna(df.date_time_opened)
    df['reported_date'] = pd.to_datetime(df['date_time_opened'])
    df['closed_date'] = pd.to_datetime(df['date_time_closed'])
    df['due_date'] = pd.to_datetime(df['assigned_due_date'])
    df['closed_date'] = df.closed_date.fillna(pd.to_datetime('today'))
    df['case_days_length'] = df.closed_date - df.reported_date
    df['case_days_length'] = df.case_days_length.fillna(df.case_days_length.max())
    df['report_to_assigned_days_length'] = df.due_date - df.reported_date
    df['report_to_assigned_days_length'] = df.report_to_assigned_days_length.fillna(df.report_to_assigned_days_length.max())
    df['days_past_due_length'] = df.closed_date - df.due_date
    df['days_past_due_length'] = df.days_past_due_length.fillna(df.days_past_due_length.max())
    
    return df

def drop_311_columns(df):
    return df.drop(columns=(['date_time_opened', 'assigned_due_date', 'date_time_closed', 'xcoord', 'ycoord']))

def prepare_311(df):
    '''
    Returns a dataframe
    '''
    df = rename_311_columns(df)
    keys = df.columns.to_list()
    values = df.columns.to_list()
    values = [v.lower() for v in values]
    dictionary = dict(zip(keys, values))
    df = df.rename(columns=dictionary)
    df = create_311_coulmns(df)
    df = drop_311_columns(df)
    
    return df
    