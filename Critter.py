import pandas as pd
import Utils
import calendar
from datetime import datetime
import regex as re
import collections
from operator import itemgetter
from itertools import groupby

pd.options.display.max_colwidth = 100

month_to_num = {v.lower(): k for k,v in enumerate(calendar.month_abbr) if k > 0}
num_to_month = {k: v.lower() for k,v in enumerate(calendar.month_abbr) if k > 0}

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

    '''TODO: keep here or in Utils?'''
    def _format_ranges(self, string_input):
        ''' Return range string, separated by semicolon if original range is broken, e.g. 0-4; 6-8, otherwise 0-8. 
        In this class used for months and times'''
        
        lst = list(map(int, string_input.split(',')))
        #magic
        ''' itertools.groupby groups the iterable into chunks,
            grouping by the key, which here is a lambda function that calculates the difference between two adjacent elements; 
            whenever the difference changes, we get a new chunk -> voila!
            operator.itemgetter(1) makes sure we produce the actual elements, and not the enumerator of these, which is at index 0
        '''
        ranges = [list(map(itemgetter(1), g)) for k, g in groupby(enumerate(lst), lambda x: x[0]-x[1])] 
        final_lst = []
        
        for elem in ranges:
            if len(elem) > 0:
                if len(elem) > 1:
                    substring = str(elem[0]) + '-' + str(elem[-1])
                else: 
                    substring = str(elem[0])
                final_lst.append(substring)

        result = '; '.join(final_lst)

        return result

    '''TODO: keep here or in Utils?'''
    def _month_ranges_totext(self, string_input):
        ''' Return month ranges as month names instead of numbers, e.g. 1-3;12 -> jan-mar;dec '''
        
        month_list = []
        for i, substring in enumerate(string_input.split(';')):
            s = substring.split('-')
            for digit in s:
                month_list.append((i,num_to_month[int(digit)]))

        months = collections.defaultdict(list)
        for i,v in month_list:
            months[i].append(v)

        new_substrings = []
        for i, v in months.items():
            new_substrings.append('-'.join(v))
        
        result = ';'.join(new_substrings)
    
        return result

    def get_info(self, critter, autostring=False):
        '''Return info on when and where to find specific critter (name of a specific critter, e.g. 'Stringfish')'''
        try:
            if autostring:
                flag = 0
            else:
                flag = re.IGNORECASE
            critter_name_criterion = self.df[self.ctype].str.contains(critter, regex=True, flags=flag)
            assert isinstance(critter, str) and len(self.df[critter_name_criterion]) > 0
        except AssertionError:
            print(f"No match on {critter} was found, make sure spelling is correct.")
        else:
            if self.ctype == "fish":
                columns = [self.ctype, 'shadowSize', 'location', 'Months', 'value', 'Times']
            else: 
                columns = [self.ctype, 'location', 'Months', 'value', 'Times']
            
            this_df = self.df[self.df['isMonth'] & self.df['isTime'] & critter_name_criterion][columns]
            this_df['Times'] = this_df['Times'].astype(str)
            this_df['value'] = this_df['value'].apply(lambda v: int(v) if v != '?' else 0)
            
            if self.ctype == "fish":
                this_df['shadowSize'] = this_df['shadowSize'].astype(str)
                group = this_df.groupby([self.ctype, 'shadowSize', 'location', 'Months', 'value'])
            else:
                group = this_df.groupby([self.ctype, 'location', 'Months', 'value'])
            
            #available times per (available) month and location for chosen critter(s)
            result_tmp = group['Times'].apply(','.join).reset_index() 
            result_tmp['Times'] = result_tmp['Times'].apply(self._format_ranges) #formatting times to only show range
            
            #sorting on months, needs to be done in order to formatt months correctly below
            result_tmp['MonthsNum'] = result_tmp['Months'].map(month_to_num) #getting month numbers
            result_tmp['MonthsNumStr'] = result_tmp['MonthsNum'].astype(str) #new column with month numbers as string representations
            result_tmp = result_tmp.sort_values(by=[self.ctype, 'MonthsNum']) #sorting
            
            result_tmp.drop('Months', axis=1, inplace=True) #drop original Months
            result_tmp.drop('MonthsNum', axis=1, inplace=True) #drop numeric month representation
            result_tmp = result_tmp.rename(columns = {'MonthsNumStr': 'Months'}) #keep only string representations of numbers as Months
            
            if self.ctype == "fish":
                group2 = result_tmp.groupby([self.ctype, 'shadowSize', 'location', 'value', 'Times'])
            else:
                group2 = result_tmp.groupby([self.ctype, 'location', 'value', 'Times'])

            result = group2['Months'].apply(','.join).reset_index()
            
            result['Months'] = result['Months'].apply(self._format_ranges) #formatting months to only show range
            
            result['Months'] = result['Months'].apply(self._month_ranges_totext) #month name range instead of numbers 

            new_times_df = pd.read_csv(f"{self.ctype} new.csv")
            new_times = new_times_df[['Name','Time of Day']]
            new_times = new_times.rename({'Name': self.ctype, 'Time of Day': 'New times'}, axis=1)

            result[f"{self.ctype} 2"] = result[self.ctype].apply(lambda s: (s.lower()).replace(' ', ''))
            new_times[f"{self.ctype} 2"] = new_times[self.ctype].apply(lambda s: (s.lower()).replace(' ', ''))
            
            final_result = pd.merge(result, new_times[[f"{self.ctype} 2", 'New times']], on = f"{self.ctype} 2", how='left')#if new times appears as NaN, the critter names in the data sources are not the same
            final_result.drop(f"{self.ctype} 2", axis=1, inplace=True)
            
            return final_result.to_string(index=False)

    def most_valuable(self, top=10):
        '''Return most valuable critters. Possible to show least valuable by adding a minus sign to top argument'''

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
    
    def get_fish_info(self, critter, autostring=False):
        return Critter(self.df, self.ctype).get_info(critter, autostring)
    
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
    
    def get_bug_info(self, critter, autostring=False):
        return Critter(self.df, self.ctype).get_info(critter, autostring)
    
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