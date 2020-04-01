from datetime import datetime
import pandas as pd
import Utils

df = pd.read_excel('fish.xlsx')

def __format_size(size):
    sizes = {
        "largeish": ["Large", "X Large", "Largest"],
        "smallish": ["Smallest", "Small"],
        "any": ["Smallest", "Small", "Medium", "large", "Large", "X Large", "Largest"]
    }
    if size in sizes:
        return sizes[size]
    return [size.capitalize()]

def __format_loc(loc):
    locations = {
        "river": ["River"],
        "rivercliff": ["River (Clifftop)"],
        "rivermouth": ["River (mouth)"],
        "sea": ["Sea", "Pier", "Sea (rainy days)"],
        "pond": ["Pond"],
        "any": ["River", "River (Clifftop)", "River (mouth)", "Sea", "Sea (rainy days)", "Pier", "Pond"]}
    if loc in locations:
        return locations[loc]
    return [loc.capitalize()]

def get_fish(size, loc):
    size = __format_size(size)
    loc = __format_loc(loc)
    current_month_text = Utils.curr_month()
    current_hour = datetime.now().hour

    filter_month = (df['Months'] == current_month_text) & df['isMonth']
    filter_hour = (df['Times'] == current_hour) & df['isTime']
    filter_loc = (df['location'].isin(loc))
    filter_size = (df['shadowSize'].isin(size))

    result = df[filter_month & filter_hour & filter_loc & filter_size]['fish'].values
    return result

"""TODO: fix this (only return one fish/value)"""
def new_fish():
    current_month_text = Utils.curr_month()
    prev_month_text = Utils.prev_month()
    filter_months = (df['Months'] == current_month_text) & (df['Months'] != prev_month_text)

    result = df[filter_months]['fish'].values
    return result


"""TODO: expiring_fish() (name pending), check fishes available this month that won't be available next month"""