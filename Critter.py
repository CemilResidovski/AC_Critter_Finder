import pandas as pd
import Utils
import calendar
from datetime import datetime
import regex as re

pd.options.display.max_colwidth = 100

month_to_num = {v.lower(): k for k,v in enumerate(calendar.month_abbr) if k > 0}

class Critter:

    def __init__(self, df, ctype):
        self.df = df
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

    '''TODO: check to see if all temporary dataframes take up unneccesary memory space, and if these canYshould be deleted from memory after they are dealt with'''
    def get_info(self, critter):
        '''Return info on when and where to find specific critter (name of a specific critter, e.g. 'Stringfish')'''

        critter_name_criterion = self.df[self.ctype].str.contains(critter, regex=True, flags=re.IGNORECASE)
        
        assert isinstance(critter, str) and len(self.df[critter_name_criterion]) > 0, f"No critter matching {critter} was found, make sure spelling is correct!"

        this_df = self.df[self.df['isMonth'] & self.df['isTime'] & critter_name_criterion][[self.ctype, 'location', 'Months', 'value', 'Times']]
        this_df['Times'] = this_df['Times'].astype(str)
        this_df['value'] = this_df['value'].apply(lambda v: int(v) if v != '?' else 0)
        
        group = this_df.groupby([self.ctype, 'location', 'Months', 'value'])
        
        #available times per (available) month and location for chosen critter(s)
        result_tmp = group['Times'].apply(','.join).reset_index() 
        result_tmp['Times'] = result_tmp['Times'].apply(lambda t: t.split(',')[0] + '-' + t.split(',')[-1]) #formatting times to only show range
        
        #sorting on months, needs to be done in order to formatt months correctly below
        result_tmp['MonthsNum'] = result_tmp['Months'].map(month_to_num)
        result_tmp = result_tmp.sort_values(by=[self.ctype, 'MonthsNum'])
        result_tmp.drop('MonthsNum', axis=1, inplace=True)

        group2 = result_tmp.groupby([self.ctype, 'location', 'value', 'Times'])

        result = group2['Months'].apply(','.join).reset_index()
        result['Months'] = result['Months'].apply(lambda m: m.split(',')[0] + '-' + m.split(',')[-1]) #formatting months to only show range

        return result.to_string(index=False)

    def most_valuable(self, top=10):
        this_df = self.df[self.df['isMonth'] & self.df['isTime']][[self.ctype, 'location', 'value' ]]
        this_df['value'] = this_df['value'].apply(lambda v: int(v) if v != '?' else 0)
        
        group = this_df.groupby([self.ctype, 'location'])
        
        result = group.mean().reset_index() #value per location and given critter type
        
        #sorting on values, descending, showing top 10  per default
        result = result.sort_values(by=['value', self.ctype], ascending=False)
        result = result.iloc[:top,:]

        return result.to_string(index=False)



class Fish:

    def __init__(self, ctype='fish'):
        self.df = FishDB.get_instance()
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
    
    def new_fish(self):
        return Critter(self.df, self.ctype).new()
    
    def expiring_fish(self):
        return Critter(self.df, self.ctype).expiring()
    
    def get_fish_info(self, critter):
        return Critter(self.df, self.ctype).get_info(critter)
    
    def most_valuable_fish(self):
        return Critter(self.df, self.ctype).most_valuable()

class Bug:

    def __init__(self, ctype='bug'):
        self.df = BugDB.get_instance()
        self.ctype = ctype

    def get_bugs(self):
        current_month_text = Utils.curr_month()
        current_hour = datetime.now().hour

        filter_month = (self.df['Months'] == current_month_text) & self.df['isMonth']
        filter_hour = (self.df['Times'] == current_hour) & self.df['isTime']

        result = self.df[filter_month & filter_hour][self.ctype].values
        return result
    
    def new_bugs(self):
        return Critter(self.df, self.ctype).new()
    
    def expiring_bugs(self):
        return Critter(self.df, self.ctype).expiring()
    
    def get_bug_info(self, critter):
        return Critter(self.df, self.ctype).get_info(critter)
    
    def most_valuable_bug(self):
        return Critter(self.df, self.ctype).most_valuable()


class FishDB:
    __instance = None
    
    @staticmethod 
    def get_instance():
        """ Static access method. """
        if FishDB.__instance is None:
            FishDB()
        return FishDB.__instance
    
    def __init__(self):
        """ Virtually private constructor. """
        if FishDB.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            print("Loading fish db for the first time, please be patient")
            FishDB.__instance = pd.read_excel("fish.xlsx")


class BugDB:
    __instance = None
    
    @staticmethod 
    def get_instance():
        """ Static access method. """
        if BugDB.__instance is None:
            BugDB()
        return BugDB.__instance
    
    def __init__(self):
        """ Virtually private constructor. """
        if BugDB.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            print("Loading bug db for the first time, please be patient")
            BugDB.__instance = pd.read_excel("bugs.xlsx")