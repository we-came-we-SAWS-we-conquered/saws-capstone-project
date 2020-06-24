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
    df['zip_code'] = df.event_address.str.extract(r'.+(\d{5}?)$').astype('str')
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
    
    return df
    