import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

pd.set_option('display.max_columns', None)
plt.rcParams.update({'font.size': 15})

from math import sqrt
from scipy import stats

plt.figure(figsize=(16,8))
alpha = 1 - .99

# Explore Visuals
def get_age_visual(df):
    plt.figure(figsize=(20,8))
    sns.swarmplot(x="root_cause", y="age", data=df)
    plt.ylabel("Age of Sewer")
    plt.xlabel("Root Cause of SSO Event")
    plt.show()
    
def get_rainfall_visual(df):
    plt.figure(figsize=(20,8))
    sns.swarmplot(x="root_cause", y="precipitation", data=df)
    plt.ylabel("Precipitation")
    plt.xlabel("Root Cause of SSO Event")
    plt.show()
    
def get_rain_visual(df):
    plt.figure(figsize=(20,8))
    sns.catplot(x='precipitation', y='root_cause', hue="rain", data=df)
    plt.ylabel("Root Cause of SSO Event")
    plt.xlabel("Precipitation")
    plt.show()
    
def get_max_temp_visual(df):
    plt.figure(figsize=(20,8))
    sns.swarmplot(x="root_cause", y="max_temp", data=df)
    plt.xlabel("Root Cause of SSO Event")
    plt.ylabel("Max Temperature F°")
    plt.show()
    
def get_min_temp_visual(df):
    plt.figure(figsize=(20,8))
    sns.swarmplot(x="root_cause", y="min_temp", data=df)
    plt.xlabel("Root Cause of SSO Event")
    plt.ylabel("Minimum Temperature in F°")
    plt.show()
    
def get_avg_temp_visual(df):
    plt.figure(figsize=(20,8))
    sns.swarmplot(x="root_cause", y="avg_temp", data=df)
    plt.xlabel("Root Cause of SSO Event")
    plt.ylabel("Average Temperature in F°")
    plt.show()   

    
# Explore stats

# Age of Sewer
def age_stats(df, alpha):
    root_cause_values = df.root_cause.value_counts()
    root_cause_list = root_cause_values.index.to_list()
    overall_age = df.age.mean()

    print('\n\nHypothesis Testing:')
    print(f'H_null: The age of the sewer is not correlated as the cause of the pipe damage involving a root_cause.')
    print(f'H_alt: The age of the sewer is correlated as the cause of the pipe damage involving a root cause.')

    root_causes = ''
    for l in root_cause_list:
        root_causes += f'{l}, '
    print(f'\nRoot Causes: \n\t{root_causes}\n')

    related_list = []
    not_related_list = []
    plot_list = []
    related_list.append("We reject the null hypothesis that the age of the sewer is not correlated as the cause of the pipe damage invloving: \n")
    not_related_list.append("We fail to reject the null hypothesis that the age of the sewer is not correlated as the cause of the pipe damage invloving: \n")

    for l in root_cause_list:
        if l != 'by pass pump leak':
            i = df[df.root_cause == l].age
            t, p = stats.ttest_1samp(i, overall_age)
        
            if p < alpha:
                related_list.append(' {} with an alpha of {:.2f} and a p-value of {}:'.format(l, alpha, p))
                plot_list.append()
            
            else:
                not_related_list.append(' {} with an alpha of {:.2f} and a p-value of {}:'.format(l, alpha, p))
            
    for r in related_list:
        print(r)
    print('-'*100)
    for n in not_related_list:
        print(n)
        
# Rainfall Stats
def rainfall_stats(df, alpha):
    root_cause_values = df.root_cause.value_counts()
    root_cause_list = root_cause_values.index.to_list()
    overall_rainfall = df.precipitation.mean()

    print('\n\nHypothesis Testing:')
    print(f'H_null: The amount of rainfall is not correlated as the cause of the pipe damage involving a root_cause.')
    print(f'H_alt: The amount of rainfall is correlated as the cause of the pipe damage involving a root cause.')

    root_causes = ''
    for l in root_cause_list:
        root_causes += f'{l}, '
    print(f'\nRoot Causes: \n\t{root_causes}\n')

    related_list = []
    not_related_list = []
    related_list.append("We reject the null hypothesis that the amount of rainfall is not correlated as the cause of the pipe damage invloving: \n")
    not_related_list.append("We fail to reject the null hypothesis that the amount of rainfall is not correlated as the cause of the pipe damage invloving: \n")

    for l in root_cause_list:
        if l != 'by pass pump leak':
            i = df[df.root_cause == l].precipitation
            t, p = stats.ttest_1samp(i, overall_rainfall)
        
            if p < alpha:
                related_list.append(' {} with an alpha of {:.2f} and a p-value of {}:'.format(l, alpha, p))
            
            else:
                not_related_list.append(' {} with an alpha of {:.2f} and a p-value of {}:'.format(l, alpha, p))
            
    for r in related_list:
        print(r)
    print('-'*100)
    for n in not_related_list:
        print(n)

        
def rain_stats_overview(df, alpha):
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

        
# Rain Stats
def rain_stats(df, alpha):
    root_cause_values = df.root_cause.value_counts()
    root_cause_list = root_cause_values.index.to_list()
    overall_rainfall = df.precipitation.mean()

    print('\n\nHypothesis Testing:')
    print(f'H_null: Rain is not correlated as the cause of the pipe damage involving a root_cause.')
    print(f'H_alt: Rain is correlated as the cause of the pipe damage involving a root cause.')

    root_causes = ''
    for l in root_cause_list:
        root_causes += f'{l}, '
    print(f'\nRoot Causes: \n\t{root_causes}\n')
    
    rain = df.rain
    related_list = []
    not_related_list = []
    related_list.append("We reject the null hypothesis that rain is not correlated as the cause of the pipe damage invloving: \n")
    not_related_list.append("We fail to reject the null hypothesis that rain is not correlated as the cause of the pipe damage invloving: \n")

    for l in root_cause_list:
        if l != 'by pass pump leak': 
            i = df[df.root_cause == l].rain
            contingency_table = pd.crosstab(i, rain)
            test_results = stats.chi2_contingency(contingency_table)
            _, p, _, expected = test_results
  
            if p < alpha:
                related_list.append(' {} with an alpha of {:.2f} and a p-value of {}:'.format(l, alpha, p))
            
            else:
                not_related_list.append(' {} with an alpha of {:.2f} and a p-value of {}:'.format(l, alpha, p))
            
    for r in related_list:
        print(r)
    print('-'*100)
    for n in not_related_list:
        print(n)
        
# Max Temp Stats
def max_temp_stats(df, alpha):
    root_cause_values = df.root_cause.value_counts()
    root_cause_list = root_cause_values.index.to_list()
    overall_max_temp = df.max_temp.mean()

    print('\n\nHypothesis Testing:')
    print(f'H_null: Max tempurature is not correlated as the cause of the pipe damage involving a root_cause.')
    print(f'H_alt: Max tempurature is correlated as the cause of the pipe damage involving a root cause.')

    root_causes = ''
    for l in root_cause_list:
        root_causes += f'{l}, '
    print(f'\nRoot Causes: \n\t{root_causes}\n')

    related_list = []
    not_related_list = []
    related_list.append("We reject the null hypothesis that max tempurature is not correlated as the cause of the pipe damage invloving: \n")
    not_related_list.append("We fail to reject the null hypothesis that max tempurature is not correlated as the cause of the pipe damage invloving: \n")

    for l in root_cause_list:
        if l != 'by pass pump leak':
            i = df[df.root_cause == l].max_temp
            t, p = stats.ttest_1samp(i, overall_max_temp)
        
            if p < alpha:
                related_list.append(' {} with an alpha of {:.2f} and a p-value of {}:'.format(l, alpha, p))
            
            else:
                not_related_list.append(' {} with an alpha of {:.2f} and a p-value of {}:'.format(l, alpha, p))
            
    for r in related_list:
        print(r)
    print('-'*100)
    for n in not_related_list:
        print(n)
        
# Min Temp Stats
def min_temp_stats(df, alpha):
    root_cause_values = df.root_cause.value_counts()
    root_cause_list = root_cause_values.index.to_list()
    overall_low_temp = df.min_temp.mean()

    print('\n\nHypothesis Testing:')
    print(f'H_null: Minimum temperature is not correlated as the cause of the pipe damage involving a root_cause.')
    print(f'H_alt: Minimum temperature is correlated as the cause of the pipe damage involving a root cause.')

    root_causes = ''
    for l in root_cause_list:
        root_causes += f'{l}, '
    print(f'\nRoot Causes: \n\t{root_causes}\n')

    related_list = []
    not_related_list = []
    related_list.append("We reject the null hypothesis that minimum temperature is not correlated as the cause of the pipe damage invloving: \n")
    not_related_list.append("We fail to reject the null hypothesis that minimum temperature is not correlated as the cause of the pipe damage invloving: \n")

    for l in root_cause_list:
        if l != 'by pass pump leak':
            i = df[df.root_cause == l].max_temp
            t, p = stats.ttest_1samp(i, overall_low_temp)
        
            if p < alpha:
                related_list.append(' {} with an alpha of {:.2f} and a p-value of {}:'.format(l, alpha, p))
            
            else:
                not_related_list.append(' {} with an alpha of {:.2f} and a p-value of {}:'.format(l, alpha, p))
            
    for r in related_list:
        print(r)
    print('-'*100)
    for n in not_related_list:
        print(n)    
    
# Avgerage Temp Stats
def avg_temp_stats(df, alpha):
    root_cause_values = df.root_cause.value_counts()
    root_cause_list = root_cause_values.index.to_list()
    overall_avg_temp = df.avg_temp.mean()

    print('\n\nHypothesis Testing:')
    print(f'H_null: The average temperature is not correlated as the cause of the pipe damage involving a root_cause.')
    print(f'H_alt: The average temperature is correlated as the cause of the pipe damage involving a root cause.')

    root_causes = ''
    for l in root_cause_list:
        root_causes += f'{l}, '
    print(f'\nRoot Causes: \n\t{root_causes}\n')

    related_list = []
    not_related_list = []
    related_list.append("We reject the null hypothesis that the average temperature is not correlated as the cause of the pipe damage invloving: \n")
    not_related_list.append("We fail to reject the null hypothesis that the average temperature is not correlated as the cause of the pipe damage invloving: \n")

    for l in root_cause_list:
        if l != 'by pass pump leak':
            i = df[df.root_cause == l].avg_temp
            t, p = stats.ttest_1samp(i, overall_avg_temp)
        
            if p < alpha:
                related_list.append(' {} with an alpha of {:.2f} and a p-value of {}:'.format(l, alpha, p))
            
            else:
                not_related_list.append(' {} with an alpha of {:.2f} and a p-value of {}:'.format(l, alpha, p))
            
    for r in related_list:
        print(r)
    print('-'*100)
    for n in not_related_list:
        print(n)     

# function for calling each explore       
def explore_age(df):
    '''
    Displays the information of age vs root causes
    - displays
    '''
    get_age_visual(df)
    age_stats(df, alpha)
    
def explore_rainfall(df):
    '''
    Displays the information of rainfall vs root causes
    -
    '''
    df = df[df.precipitation != 'unknown']
    get_rainfall_visual(df)
    rainfall_stats(df, alpha)
    
def explore_rain(df):
    '''
    Displays the information of rain vs root causes
    - 
    '''
    df = df[df.rain != 'unknown']
    rain_stats_overview(df, alpha)
    get_rain_visual(df)
    rain_stats(df, alpha)
    
def explore_max_temp(df):
    '''
    Displays the information of max temp vs root causes
    - 
    '''
    df = df[df.max_temp != 'unknown']
    get_max_temp_visual(df)
    max_temp_stats(df, alpha)
    
def explore_min_temp(df):
    '''
    Displays the information of min temp vs root causes
    - 
    '''
    df = df[df.min_temp != 'unknown']
    get_min_temp_visual(df)
    min_temp_stats(df, alpha)

def explore_avg_temp(df):
    '''
    Displays the information of avg temp vs root causes
    - 
    '''
    df = df[df.avg_temp != 'unknown']
    get_avg_temp_visual(df)
    avg_temp_stats(df, alpha)
          
