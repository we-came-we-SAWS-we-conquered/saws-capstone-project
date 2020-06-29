import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

pd.set_option('display.max_columns', None)

from math import sqrt
from scipy import stats

plt.figure(figsize=(16,8))

def get_age_visual(df):
    plt.figure(figsize=(16,8))
    sns.swarmplot(x="root_cause", y="age", data=df)
    plt.ylabel("Age of Sewer")
    plt.xlabel("Root Cause of SSO Event")
    plt.show()

def age_stats(df):
    root_cause_values = df.root_cause.value_counts()
    root_cause_list = root_cause_values.index.to_list()
    # confidence level = 99%
    alpha = 1 - .99
    overall_age = df.age.mean()
    related_list = []
    print('\n\nHypothesis Testing:')
    for l in root_cause_list:
        if l != 'by pass pump leak':
            i = df[df.root_cause == l].age
            t, p = stats.ttest_1samp(i, overall_age)
        
            print(f'Root Cause: {l}')
            print(f'H_null: The age of the sewer is not correlated as the cause of the pipe damage involving {l}')
            print(f'H_alt: The age of the sewer is correlated as the cause of the pipe damage involving {l}') 
            print(' with an alpha of {:.2f} and a p-value of {}:\n'.format(alpha, p))
        
            if p < alpha:
                print(f"We reject the null hypothesis. ")
                print(f"  The age of the sewer is correlated as the cause of the pipe damage involving {l}\n")          
                related_list.extend(l)
            else:
                print(f"We fail to reject the null hypothesis.")
                print(f"  The age of the sewer is not correlated as the cause of the pipe damage involving {l}\n")
        print('-'*100)           
    return related_list

def age_explore(df):
    '''
    Returns a list
    - displays the visual of age vs root causes
    - prints the stats test for all root causes and age of sewer
    '''
    get_age_visual(df)
    return age_stats(df)



def get_rainfall_visual(df):
    plt.figure(figsize=(16,8))
    sns.swarmplot(x="root_cause", y="precipitation", data=df)
    plt.ylabel("Precipitation")
    plt.xlabel("Root Cause of SSO Event")
    plt.show()
    
    
def rainfall_stats(df):
    root_cause_values = df.root_cause.value_counts()
    root_cause_list = root_cause_values.index.to_list()
    # confidence level = 99%
    alpha = 1 - .99
    overall_rainfall = df.precipitation.mean()
    related_list = []
    print('\n\nHypothesis Testing:')
    for l in root_cause_list:
        if l != 'by pass pump leak':
            i = df[df.root_cause == l].precipitation
            t, p = stats.ttest_1samp(i, overall_rainfall)
        
            print(f'Root Cause: {l}')
            print(f'H_null: The amount of rainfall is not correlated as the cause of the pipe damage involving {l}')
            print(f'H_alt: The amount of rainfall is correlated as the cause of the pipe damage involving {l}') 
            print(' with an alpha of {:.2f} and a p-value of {}:\n'.format(alpha, p))
        
            if p < alpha:
                print(f"We reject the null hypothesis. ")
                print(f"  The amount of rainfall is correlated as the cause of the pipe damage involving {l}\n")          
                related_list.extend(l)
            else:
                print(f"We fail to reject the null hypothesis.")
                print(f"  The amount of rainfall is not correlated as the cause of the pipe damage involving {l}\n")
        print('-'*100)           
    return related_list    

def rainfall_explore(df):
    '''
    Returns a list
    - displays the visual of rainfall vs root causes
    - prints the stats test for all root causes and rainfall
    '''
    df = df[df.precipitation != 'unknown']
    get_rainfall_visual(df)
    return rainfall_stats(df)

def get_rain_visual(df):
    plt.figure(figsize=(16,8))
    sns.catplot(x='precipitation', y='root_cause', hue="rain", data=df)
    plt.ylabel("Root Cause of SSO Event")
    plt.xlabel("Precipitation")
    plt.show()

def rain_stats_overview(df):
    contingency_table = pd.crosstab(df.root_cause, df.rain)
    test_results = stats.chi2_contingency(contingency_table)
    _, p, _, expected = test_results
    print("Contingency Table")
    print(contingency_table)
    print("*****************************************************************")
    # 99% confidence level
    alpha = 1 - .99
    print(f'H_null: Rain is not correlated with the cause of the pipe damage.')
    print(f'H_alt: Rain is correlated with the cause of the pipe damage.') 
    print(' with an alpha of {:.2f} and a p-value of {}:\n'.format(alpha, p))
        
    if p < alpha:
        print(f"We reject the null hypothesis. ")
        print(f"Rain is correlated with the cause of the pipe damage")          
    else:
        print(f"We fail to reject the null hypothesis.")
        print(f"Rain is not correlated with the cause of the pipe damage involving {l}\n")
        

def rain_stats(df):
    root_cause_values = df.root_cause.value_counts()
    root_cause_list = root_cause_values.index.to_list()
    # confidence level = 99%
    alpha = 1 - .99
    rain = df.rain
    related_list = []
    print('\n\nHypothesis Testing:')
    for l in root_cause_list:
        if l != 'by pass pump leak':
            i = df[df.root_cause == l].rain
            contingency_table = pd.crosstab(i, rain)
            test_results = stats.chi2_contingency(contingency_table)
            _, p, _, expected = test_results
        
            print(f'Root Cause: {l}')
            print(f'H_null: Rain is not correlated with the cause of the pipe damage involving {l}')
            print(f'H_alt: H_alt: Rain is correlated with the cause of the pipe damage involving {l}') 
            print(' with an alpha of {:.2f} and a p-value of {}:\n'.format(alpha, p))
        
            if p < alpha:
                print(f"We reject the null hypothesis. ")
                print(f"Rain is correlated with the cause of the pipe damage involving {l}\n")          
                related_list.extend(l)
            else:
                print(f"We fail to reject the null hypothesis.")
                print(f"Rain is not correlated with the cause of the pipe damage {l}\n")
        print('-'*100)           
    return related_list            


def rain_explore(df):
    '''
    Returns a list
    - displays the visual of rainfall vs root causes
    - prints the stats test for all root causes and rainfall
    '''
    df = df[df.rain != 'unknown']
    get_rain_visual(df)
    return rain_stats(df)


def get_max_temp_visual(df):
    plt.figure(figsize=(16,8))
    sns.swarmplot(x="root_cause", y="max_temp", data=df)
    plt.xlabel("Root Cause of SSO Event")
    plt.ylabel("Max Temperature F°")
    plt.show()
    
    
def max_temp_stats(df):
    root_cause_values = df.root_cause.value_counts()
    root_cause_list = root_cause_values.index.to_list()
    # confidence level = 99%
    alpha = 1 - .99
    overall_max_temp = df.max_temp.mean()
    related_list = []
    print('\n\nHypothesis Testing:')
    for l in root_cause_list:
        if l != 'by pass pump leak':
            i = df[df.root_cause == l].max_temp
            t, p = stats.ttest_1samp(i, overall_max_temp)
        
            print(f'Root Cause: {l}')
            print(f'H_null: The high temperature recorded during a specific event is not correlated as the cause of the pipe damage involving {l}')
            print(f'H_alt: The high temperature recorded during a specific event is correlated as the cause of the pipe damage involving {l}') 
            print(' with an alpha of {:.2f} and a p-value of {}:\n'.format(alpha, p))
        
            if p < alpha:
                print(f"We reject the null hypothesis. ")
                print(f"  The high temperature is the cause of the pipe damage involving {l}\n")          
                related_list.extend(l)
            else:
                print(f"We fail to reject the null hypothesis.")
                print(f"  The high temperature not correlated as the cause of the pipe damage involving {l}\n")
        print('-'*100)           
    return related_list    



def max_temp_explore(df):
    '''
    Returns a list
    - displays the visual of max_temp vs root causes
    - prints the stats test for all root causes and max_temp
    '''
    df = df[df.max_temp != 'unknown']
    get_max_temp_visual(df)
    return max_temp_stats(df)



def get_min_temp_visual(df):
    plt.figure(figsize=(16,8))
    sns.swarmplot(x="root_cause", y="min_temp", data=df)
    plt.xlabel("Root Cause of SSO Event")
    plt.ylabel("Minimum Temperature in F°")
    plt.show()
    
    
def min_temp_stats(df):
    root_cause_values = df.root_cause.value_counts()
    root_cause_list = root_cause_values.index.to_list()
    # confidence level = 99%
    alpha = 1 - .99
    overall_low_temp = df.min_temp.mean()
    related_list = []
    print('\n\nHypothesis Testing:')
    for l in root_cause_list:
        if l != 'by pass pump leak':
            i = df[df.root_cause == l].min_temp
            t, p = stats.ttest_1samp(i, overall_low_temp)
        
            print(f'Root Cause: {l}')
            print(f'H_null: The lowest recorded temperature during a specific event is not correlated as the cause of the pipe damage involving {l}')
            print(f'H_alt: The lowest recorded temperature during a specific event is correlated as the cause of the pipe damage involving {l}') 
            print(' with an alpha of {:.2f} and a p-value of {}:\n'.format(alpha, p))
        
            if p < alpha:
                print(f"We reject the null hypothesis. ")
                print(f"  The low temperature is correlated as the cause of the pipe damage involving {l}\n")          
                related_list.extend(l)
            else:
                print(f"We fail to reject the null hypothesis.")
                print(f"  The low temperature is not correlated as the cause of the pipe damage involving {l}\n")
        print('-'*100)           
    return related_list    



def min_temp_explore(df):
    '''
    Returns a list
    - displays the visual of min_temp vs root causes
    - prints the stats test for all root causes and min_temp
    '''
    df = df[df.min_temp != 'unknown']
    get_min_temp_visual(df)
    return min_temp_stats(df)


def get_avg_temp_visual(df):
    plt.figure(figsize=(16,8))
    sns.swarmplot(x="root_cause", y="avg_temp", data=df)
    plt.xlabel("Root Cause of SSO Event")
    plt.ylabel("Average Temperature in F°")
    plt.show()
    
    
def avg_temp_stats(df):
    root_cause_values = df.root_cause.value_counts()
    root_cause_list = root_cause_values.index.to_list()
    # confidence level = 99%
    alpha = 1 - .99
    overall_avg_temp = df.avg_temp.mean()
    related_list = []
    print('\n\nHypothesis Testing:')
    for l in root_cause_list:
        if l != 'by pass pump leak':
            i = df[df.root_cause == l].avg_temp
            t, p = stats.ttest_1samp(i, overall_avg_temp)
        
            print(f'Root Cause: {l}')
            print(f'H_null: The average temperature of a day a SSO event occured is not correlated as the cause of the pipe damage involving {l}')
            print(f'H_alt: The average temperature of a day a SSO event occured is correlated as the cause of the pipe damage involving {l}') 
            print(' with an alpha of {:.2f} and a p-value of {}:\n'.format(alpha, p))
        
            if p < alpha:
                print(f"We reject the null hypothesis. ")
                print(f"  The average temperature is correlated as the cause of the pipe damage involving {l}\n")          
                related_list.extend(l)
            else:
                print(f"We fail to reject the null hypothesis.")
                print(f"  The average temperature is not correlated as the cause of the pipe damage involving {l}\n")
        print('-'*100)           
    return related_list    



def avg_temp_explore(df):
    '''
    Returns a list
    - displays the visual of avg_temp vs root causes
    - prints the stats test for all root causes and avg_temp
    '''
    df = df[df.avg_temp != 'unknown']
    get_avg_temp_visual(df)
    return avg_temp_stats(df)