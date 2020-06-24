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
    df = df[df.age != 'unknown']
    get_age_visual(df)
    return age_stats(df)
    