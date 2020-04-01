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
        "largeish": ["large", "x large", "largest"],
        "smallish": ["smallest", "small"],
        "any": ["smallest", "small", "medium", "large", "x large", "largest"]
    }
    if size in sizes:
        return sizes[size]
    return size.lower()

def __format_loc(loc):
    locations = {
        "river": "River",
        "rivercliff": "River (Clifftop)",
        "rivermouth": "River (mouth)",
        "sea": ["Sea", "Pier"],
        "pond": "Pond",
        "any": ["River", "River (Clifftop)", "River (mouth)", "Sea", "Sea (rainy days)", "Pier", "Pond"]}
    return locations[loc.lower()]

"""TODO: add get_fish functionality using pandas"""
def get_fish(size, loc):
    size = __format_size(size)
    loc = __format_loc(loc)

    filter_month = (df['Months'] == current_month) & df['isMonth']
    filter_hour = (df['Times'] == current_hour) & df['isTime']
    filter_loc = (df['location'] == loc)
    filter_size = (df['shadowSize'] == size)

    result = df[filter_month & filter_hour & filter_loc & filter_size]['fish'].values
    return result


# print(get_fish("large", "River"))
# locs = ['River']
# filter_month = (df['Months'] == current_month) & df['isMonth']
# filter_hour = (df['Times'] == current_hour) & df['isTime']
# filter_loc = df['location'] in locs
# result = df[filter_month & filter_hour]['fish'].values
# print(result)

# def get_fish(size, loc):
#     """filter first by loc, then size, then time"""
#     size = __format_size(size) 
#     loc = __format_loc(loc)

#     possible_fish = []
#     for fish in df_excel:
#         if fish["location"] in loc or ("Sea" in fish["location"] and "Sea" in loc):
#             if fish["shadowSize"].casefold() in size:
#                 if fish[current_month] and current_hour in fish["time"]:
#                     f = fish["fish"]
#                     if "pier" in fish["location"].casefold():
#                         f += " (pier)"
#                     elif "rain" in fish["location"].casefold():
#                         f += " (rainy days)"
#                     possible_fish.append(f)
#     return possible_fish