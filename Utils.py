import pandas as pd
from datetime import datetime

months = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
current_month = datetime.now().month - 1

def format_month(month):
    return months[(month + 12) % 12]

def curr_month():
    return months[current_month]

def prev_month():
    return format_month(current_month - 1)

def next_month():
    return format_month(current_month + 1)

def format_size(size):
    sizes = {
        "largeish": ["Large", "X Large", "Largest"],
        "smallish": ["Smallest", "Small"],
        "any": ["Smallest", "Small", "Medium", "large", "Large", "X Large", "Largest"]
    }
    if size in sizes:
        return sizes[size]
    return [size.capitalize()]

def format_loc(loc):
    locations = {
        "river": ["River"],
        "rivercliff": ["River (Clifftop)"],
        "rivermouth": ["River (mouth)"],
        "sea": ["Sea", "Pier", "Sea (rainy days)"],
        "pond": ["Pond"],
        "any": ["River", "River (Clifftop)", "River (mouth)", "Sea", "Sea (rainy days)", "Pier", "Pond"],
        "rivers": ["River", "River (Clifftop)", "River (mouth)"]
    }
    if loc in locations:
        return locations[loc]
    return [loc.capitalize()]

def crosstable_to_tidy(table=None, attribute_field_name=None, data_field_name=None, sheet='all', qualifying_fields=1):

    ''' Reads a file or dataframe that contains data of crosstable structure, i.e. orthogonal, 
        and returns a tidy dataframe, more suitable for further analysis.
        
        {table: path/url string to excel file or pandas.core.frame.DataFrame object,
        attribute_field_name: name of column that will be stacked,
        data_field_name: name of column that will contain data values,
        sheet: load specific sheet or ('all') loop through and concatenate crosstables from all excel-file sheets,
        qualifying_fields: number of table columns that should be left as-is}'''

    if isinstance(table, str):
        if sheet == 'all':
            df_crosstab_dict = pd.read_excel(table, sheet_name=None, index_col=list(range(qualifying_fields)))
            df_crosstab_tmp = [v for v in df_crosstab_dict.values()]
            df_crosstab = pd.concat(df_crosstab_tmp)
        else:
            df_crosstab = pd.read_excel(table, sheet_name=sheet, index_col=list(range(qualifying_fields)))
    elif isinstance(table, pd.core.frame.DataFrame):
        df_crosstab = table        
    else:
        return 'No data was passed to function'

    if not isinstance(df_crosstab.index, pd.MultiIndex):
        df_crosstab = df_crosstab.set_index(list(df_crosstab.columns[:qualifying_fields]))

    df_crosstab = df_crosstab.stack().reset_index()

    col_names = [attribute_field_name, data_field_name]
    col_names_map = dict(zip(df_crosstab.columns[qualifying_fields:], col_names))
    df_crosstab.rename(columns=col_names_map, inplace=True)

    return df_crosstab

def fish_dataframe(fishes_input):
    fish_dict = {i: d for i, d in enumerate(fishes_input)}
    times = {}
    for k in fish_dict.keys():
        diff = set(range(24)) - fish_dict[k]['time'] #missing hours
        diffs = ['NA']*len(diff) #'NA' inplace of missing hours
        times[k] = list(fish_dict[k]['time']) + diffs #add missing hours to original times

    df = pd.DataFrame(fish_dict).transpose()
    df_time = pd.DataFrame(times).transpose()

    df_base = df[['fish', 'location', 'shadowSize', 'value']]
    df_months = df[['fish', 'location', 'shadowSize', 'value',  'jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']]
    df_times = pd.merge(df_base, df_time, how='outer', on=df.index)

    df_months_tidy = crosstable_to_tidy(df_months, 'Months', 'isMonth', qualifying_fields=4)
    df_times_tidy = crosstable_to_tidy(df_times.drop('key_0', axis=1), 'Times', 'isTime', qualifying_fields=4)
    df_times_tidy['isTime'] = df_times_tidy['isTime'].apply(lambda x: True if x != 'NA' else False)

    df_final = pd.merge(df_months_tidy, df_times_tidy, how='outer', on=['fish', 'location', 'shadowSize', 'value'])

    return df_final

def bugs_dataframe(bugs_input):
    bugs_dict = {i: d for i, d in enumerate(bugs_input)}
    times = {}
    for k in bugs_dict.keys():
        if 'time' in bugs_dict[k].keys(): #some bugs.txt elements do not contain 'time'
            diff = set(range(25)) - bugs_dict[k]['time'] #missing hours
            diffs = ['NA']*len(diff) #'NA' inplace of missing hours
            times[k] = list(bugs_dict[k]['time']) + diffs #add missing hours to original times
        else:
            diffs = ['NA']*len(range(24))
            times[k] = diffs #add missing hours to original times
        

    df = pd.DataFrame(bugs_dict).transpose()
    df_time = pd.DataFrame(times).transpose()

    df_base = df[['bug', 'location', 'value']]
    df_months = df[['bug', 'location', 'value', 'jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']]
    df_times = pd.merge(df_base, df_time, how='outer', on=df.index)

    df_months_tidy = crosstable_to_tidy(df_months, 'Months', 'isMonth', qualifying_fields=3)
    df_times_tidy = crosstable_to_tidy(df_times.drop('key_0', axis=1), 'Times', 'isTime', qualifying_fields=3)
    df_times_tidy['isTime'] = df_times_tidy['isTime'].apply(lambda x: True if x != 'NA' else False)

    df_final = pd.merge(df_months_tidy, df_times_tidy, how='outer', on=['bug', 'location', 'value'])

    return df_final

def time_range(start, end):
    if end < start:
        end += 24
    time = set()
    for x in range(start, end + 1):
        time.add(x % 24)
    return(time)

def time_formatting(string):
    string = string.split('-')
    start = string[0].strip().split()
    start_time = int(start[0])
    if "p" in start[1]:
        start_time += 12
    end = string[1].strip().split()
    end_time = int(end[0])
    if "p" in end[1]:
        end_time += 12
    range_set = time_range(start_time, end_time)
    return range_set


"""TODO: handle different ranges of time ranges "9 a.m. - 4 p.m., 9 p.m. - 4 a.m."""
def time_format(string):
    if "All day" in string:
        return time_range(0, 23)
    elif "," in string:
        ranges = string.split(',')
        result_set = set()
        for t_r in ranges:
            result_set = result_set.union(time_formatting(t_r))
        return result_set
    else:
        return time_formatting(string)

def raw_data_to_tidy_excel(critter_data, critter_type, file_name):
    critter_copy = []

    for critter in critter_data:
        if type(critter['time']) == str:
            c = critter
            c['time'] = time_format(critter['time'])
            critter_copy.append(c)
        else:
            critter_copy.append(critter)
    
    critter_tuple = tuple(critter_copy)
    if critter_type == "fish":
        df = fish_dataframe(critter_tuple)
    else:
        df = bugs_dataframe(critter_tuple)
    df.to_excel(file_name + ".xlsx")