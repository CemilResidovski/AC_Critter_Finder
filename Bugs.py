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

"""TODO: new_bugs() - check which bugs are available this month that weren't last month"""
"""TODO: expiring_bugs() (name pending), check bugs available this month that won't be available next month"""
"""TODO: get_info(bug) - return information on when & where bug will be available"""