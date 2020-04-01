from datetime import datetime
import pandas as pd
import Utils

df = pd.read_excel('fish.xlsx')

def get_fish(size, loc):
    size = Utils.format_size(size)
    loc = Utils.format_loc(loc)
    current_month_text = Utils.curr_month()
    current_hour = datetime.now().hour

    filter_month = (df['Months'] == current_month_text) & df['isMonth']
    filter_hour = (df['Times'] == current_hour) & df['isTime']
    filter_loc = (df['location'].isin(loc))
    filter_size = (df['shadowSize'].isin(size))

    result = df[filter_month & filter_hour & filter_loc & filter_size]['fish'].values
    return result

def new_fish():
    current_month_text = Utils.curr_month()
    prev_month_text = Utils.prev_month()
    
    filter_this_month = (df['Months'] == current_month_text) & (df['isMonth'])
    filter_prev_month = (df['Months'] == prev_month_text) & (df['isMonth'] == False)
    
    fish_this_month = set(df[filter_this_month]['fish'].values) #fish that are available current month
    fish_prev_month = set(df[filter_prev_month]['fish'].values) #fish that were not available previous month
    
    result = fish_this_month.intersection(fish_prev_month) #the intersection of above two sets
    
    return result

def expiring_fish():
    current_month_text = Utils.curr_month()
    next_month_text = Utils.next_month()
    
    filter_this_month = (df['Months'] == current_month_text) & (df['isMonth'])
    filter_next_month = (df['Months'] == next_month_text) & (df['isMonth'] == False)
    
    fish_this_month = set(df[filter_this_month]['fish'].values) #fish that are available current month
    fish_next_month = set(df[filter_next_month]['fish'].values) #fish that are not available next month
    
    result = fish_this_month.intersection(fish_next_month) #the intersection of above two sets
    
    return result

def get_info(fish):

    assert fish in df.fish.values, f"{fish} not found, make sure spelling is correct!"

    this_df = df[df['isMonth'] & df['isTime'] & (df['fish'] == fish)]
    this_df = this_df[['location', 'Months', 'Times']]
    this_df['Times'] = this_df['Times'].astype(str)
    
    group = this_df.groupby(['location', 'Months'])
    
    result = group['Times'].apply(','.join).reset_index() #available times per (available) month and location for chosen fish

    return result