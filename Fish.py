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

"""TODO: verify if this returns correct results"""
def new_fish():
    current_month_text = Utils.curr_month()
    prev_month_text = Utils.prev_month()
    
    filter_this_month = (df['Months'] == current_month_text) & (df['isMonth'])
    filter_prev_month = (df['Months'] == prev_month_text) & (df['isMonth'] == False)
    
    fish_this_month = set(df[filter_this_month]['fish'].values) #fish that are available current month
    fish_prev_month = set(df[filter_prev_month]['fish'].values) #fish that were not available previous month
    
    result = fish_this_month.intersection(fish_prev_month) #the intersection of above two sets
    
    return result


"""TODO: verify if this returns correct results (name pending)"""
def expiring_fish():
    current_month_text = Utils.curr_month()
    next_month_text = Utils.next_month()
    
    filter_this_month = (df['Months'] == current_month_text) & (df['isMonth'])
    filter_next_month = (df['Months'] == next_month_text) & (df['isMonth'] == False)
    
    fish_this_month = set(df[filter_this_month]['fish'].values) #fish that are available current month
    fish_next_month = set(df[filter_next_month]['fish'].values) #fish that are not available next month
    
    result = fish_this_month.intersection(fish_next_month) #the intersection of above two sets
    
    return result

"""TODO: get_info(fish) - return information on when & where fish will be available"""