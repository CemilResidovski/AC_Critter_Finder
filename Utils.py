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
        diff = set(range(25)) - fish_dict[k]['time'] #missing hours
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
            diffs = ['NA']*len(range(25))
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