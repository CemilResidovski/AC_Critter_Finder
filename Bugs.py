from datetime import datetime
import pandas as pd
import json
import Utils

df = pd.read_excel('bugs.xlsx')

def get_bugs():
    current_month_text = Utils.curr_month()
    current_hour = datetime.now().hour

    filter_month = (df['Months'] == current_month_text) & df['isMonth']
    filter_hour = (df['Times'] == current_hour) & df['isTime']

    result = df[filter_month & filter_hour]['bug'].values
    return result

"""TODO: verify if this returns correct results"""
def new_bugs():
    current_month_text = Utils.curr_month()
    prev_month_text = Utils.prev_month()
    
    filter_this_month = (df['Months'] == current_month_text) & (df['isMonth'])
    filter_prev_month = (df['Months'] == prev_month_text) & (df['isMonth'] == False)
    
    bugs_this_month = set(df[filter_this_month]['bug'].values) #bugs that are available current month
    bugs_prev_month = set(df[filter_prev_month]['bug'].values) #bugs that were not available previous month
    
    result = bugs_this_month.intersection(bugs_prev_month) #the intersection of above two sets
    return result

"""TODO: verify if this returns correct results (name pending)"""
def expiring_bugs():
    current_month_text = Utils.curr_month()
    next_month_text = Utils.next_month()
    
    filter_this_month = (df['Months'] == current_month_text) & (df['isMonth'])
    filter_next_month = (df['Months'] == next_month_text) & (df['isMonth'] == False)
    
    bugs_this_month = set(df[filter_this_month]['bug'].values) #bugs that are available current month
    bugs_next_month = set(df[filter_next_month]['bug'].values) #bugs that are not available next month
    
    result = bugs_this_month.intersection(bugs_next_month) #the intersection of above two sets
    return result

"""TODO: get_info(bug) - return information on when & where bug will be available"""
def get_info(bug):

    assert bug in df.bug.values, f"{bug} not found, make sure spelling is correct!"

    this_df = df[df['isMonth'] & df['isTime'] & (df['bug'] == bug)]
    this_df = this_df[['location', 'Months', 'Times']]
    this_df['Times'] = this_df['Times'].astype(str)
    
    group = this_df.groupby(['location', 'Months'])
    
    result = group['Times'].apply(','.join).reset_index() #available times per (available) month and location for chosen bug

    return result