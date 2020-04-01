from datetime import datetime
import pandas as pd
import numpy
import csv

months = ["m", "jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
current_month = months[datetime.now().month]
current_hour = datetime.now().hour

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
        "sea": ["Sea", "Pier"],
        "pond": ["Pond"],
        "any": ["River", "River (Clifftop)", "River (mouth)", "Sea", "Sea (rainy days)", "Pier", "Pond"]}
    return locations[loc]

def get_fish(size, loc):
    size = __format_size(size)
    loc = __format_loc(loc)

    filter_month = (df['Months'] == current_month) & df['isMonth']
    filter_hour = (df['Times'] == current_hour) & df['isTime']
    filter_loc = (df['location'].isin(loc))
    filter_size = (df['shadowSize'].isin(size))

    result = df[filter_month & filter_hour & filter_loc & filter_size]['fish'].values
    return result