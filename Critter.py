import pandas as pd
import Utils
import calendar
from datetime import datetime

month_to_num = {v.lower(): k for k,v in enumerate(calendar.month_abbr) if k > 0}
#current_month_text = Utils.curr_month()
#prev_month_text = Utils.prev_month()
#next_month_text = Utils.next_month()
#current_hour = datetime.now().hour

'''TODO: load files here or in main?'''
df_fish = pd.read_excel('fish.xlsx')
df_bugs = pd.read_excel('bugs.xlsx')

class Critter():

    def __init__(self, df, ctype):
        assert isinstance(df, pd.DataFrame), "df must be pandas dataframe with appropriate critter info!"
        self.df = df
        assert isinstance(ctype, str) and ctype.lower() in ['fish', 'bug'], "ctype must be \'fish\' or \'bug\'!"
        self.ctype = ctype

    def new(self):
        '''Return critters that are available current month but not previous month'''
        current_month_text = Utils.curr_month()
        prev_month_text = Utils.prev_month()
        
        filter_this_month = (self.df['Months'] == current_month_text) & (self.df['isMonth'])
        filter_prev_month = (self.df['Months'] == prev_month_text) & (self.df['isMonth'] == False)
        
        critter_this_month = set(self.df[filter_this_month][self.ctype].values) #critter that are available current month
        critter_prev_month = set(self.df[filter_prev_month][self.ctype].values) #critter that were not available previous month
        
        result = critter_this_month.intersection(critter_prev_month) #the intersection of above two sets
        
        return result
    
    def expiring(self):
        '''Return critters that are available current month but not next month'''
        current_month_text = Utils.curr_month()
        next_month_text = Utils.next_month()
        
        filter_this_month = (self.df['Months'] == current_month_text) & (self.df['isMonth'])
        filter_next_month = (self.df['Months'] == next_month_text) & (self.df['isMonth'] == False)
        
        critter_this_month = set(self.df[filter_this_month][self.ctype].values) #critter that are available current month
        critter_next_month = set(self.df[filter_next_month][self.ctype].values) #critter that are not available next month
        
        result = critter_this_month.intersection(critter_next_month) #the intersection of above two sets
        
        return result

    
    def get_info(self, critter):
        '''Return info on when and where to find specific critter (name of a specific critter, e.g. 'Stringfish')'''

        assert critter in self.df[self.ctype].values, f"{critter} not found, make sure spelling is correct!"

        this_df = self.df[self.df['isMonth'] & self.df['isTime'] & (self.df[self.ctype] == critter)]
        this_df = this_df[['location', 'Months', 'Times']]
        this_df['Times'] = this_df['Times'].astype(str)
        
        group = this_df.groupby(['location', 'Months'])
        
        result = group['Times'].apply(','.join).reset_index() #available times per (available) month and location for chosen critter
        
        #sorting on months
        result['MonthsNum'] = result['Months'].map(month_to_num)
        result = result.sort_values(by=['MonthsNum'])
        result.drop('MonthsNum', axis=1, inplace=True)
        
        return result

class Fish(Critter):

    def __init__(self, df, ctype='fish'):
        self.df = df
        self.ctype = ctype

    def get_fish(self, loc, size):
        size = Utils.format_size(size)
        loc = Utils.format_loc(loc)
        current_month_text = Utils.curr_month()
        current_hour = datetime.now().hour

        filter_month = (self.df['Months'] == current_month_text) & self.df['isMonth']
        filter_hour = (self.df['Times'] == current_hour) & self.df['isTime']
        filter_loc = (self.df['location'].isin(loc))
        filter_size = (self.df['shadowSize'].isin(size))

        result = self.df[filter_month & filter_hour & filter_loc & filter_size][self.ctype].values
        return result

class Bug(Critter):

    def __init__(self, df, ctype='bug'):
        self.df = df
        self.ctype = ctype

    def get_bugs(self):
        current_month_text = Utils.curr_month()
        current_hour = datetime.now().hour

        filter_month = (self.df['Months'] == current_month_text) & self.df['isMonth']
        filter_hour = (self.df['Times'] == current_hour) & self.df['isTime']

        result = self.df[filter_month & filter_hour][self.ctype].values

        return result

fish, bug = Fish(df_fish), Bug(df_bugs)

print(fish.get_fish('sea', 'small'))
print(bug.get_bugs())

#print(bug.new())
#print(fish.expiring())
#print(bug.expiring())
#print(fish.get_info('Stringfish'))
#print(bug.get_info('Common Butterfly'))