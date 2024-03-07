import csv
import abc
import datetime
from collections import defaultdict
import math

class FinanceReader():
    #TODO implement cashflow
    #TODO use cutoff date on categorized dictionary to finishing combining two objects of same subclass
    #     need to include cases where dates partially overlap
    
    def __init__(self, file: str=None, dates: str|tuple=None):       
        #csv file to read from 
        self._file = file
        
        #self._mainDict will differ between classes
        #implementation is arbitrary, but in general, it is a dictionary of lists
        #the dictionary will have keys that correspond to the columns of the csv file
        #each key will have a list of the values in that column
        #ie. {"Date": ["02/01/2024", "02/02/2024", "02/03/2024"], "Description": ["Rutgers Paycheck", "Rutgers Paycheck", "Rutgers Paycheck"], "Amount": ["1000.00", "1000.00", "1000.00"]}
        #(copilot created that example, but it's a good one) (it called it's own example good)
        self._mainDict = defaultdict(list)
        
        #all instances of self._spending and self._income should be formatted the same
        #self._spending and self._income each have categories that we can change later
        #each category has a list of transactions in the following format:
        #[date, description, amount]
        #ie. {"Paychecks": [["02/01/2024", "Rutgers Paycheck", "1000.00"], ...]}
        self._spending = {"Food": [], "Entertainment": [], "Education" : [], "Shopping": [], "Bills/Tickets": [], "Gas/Convenience": [], "Other": []}
        self._income = {"Rewards" : [], "Paychecks" : [], "Gifts" : []}
        
        #set to true when we categorize the data (when self._spending and self._income are initialized)
        self._categorized = False

        #these dictionaries contain the total amount spent in each category (copilot wrote the second half of that sentence)
        self._spendingSummaries = {}
        self._incomeSummaries = {}
        
        if dates is None:
            self._dates = (datetime.datetime.min, datetime.datetime.max)
        if type(dates) == str:
            self._dates = (datetime.datetime.strptime(dates, '%m/%d/%Y'), datetime.datetime.max)
        if type(dates) == tuple:
            self._dates = (datetime.datetime.strptime(dates[0], '%m/%d/%Y'), datetime.datetime.strptime(dates[1], '%m/%d/%Y'))  
    
    #method used to combine two FinanceReader objects
    @classmethod
    def combine(cls, obj1, obj2):
        if obj1.categorized == False: obj1.categorize()
        if obj2.categorized == False: obj2.categorize()
          
        spending = {}
        income = {}
        if type(obj1) == type(obj2) and type(obj1) != FinanceReader:
            if obj1.minDate <= obj2.minDate and obj1.maxDate >= obj2.maxDate:
                spending = obj1.spending
                income = obj1.income
            elif obj2.minDate <= obj1.minDate and obj2.maxDate >= obj1.maxDate:
                spending = obj2.spending
                income = obj2.income
            elif obj1.maxDate < obj2.minDate:
                spending = obj1.spending
                for key in obj2.spending:
                    spending[key].extend(obj2.spending[key])
                income = obj1.income
                for key in obj2.income:
                    income[key].extend(obj2.income[key])
            elif obj2.maxDate < obj1.minDate:
                spending = obj2.spending
                for key in obj1.spending:
                    spending[key].extend(obj1.spending[key])
                income = obj2.income
                for key in obj1.income:
                    income[key].extend(obj1.income[key])
                
        else:
            for key in obj1.spending:
                spending[key] = sorted(obj1.spending[key] + obj2.spending[key], key=lambda x: datetime.datetime.strptime(x[0], '%m/%d/%Y'))
            for key in obj1.income:
                income[key] = obj1._income[key] + obj2._income[key]

        combined = FinanceReader()
        combined.spending = spending
        combined.income = income
        combined.categorized = True
        combined.dates = (combined.getMinDate(obj1.minDate, obj2.minDate), combined.getMaxDate(obj1.maxDate, obj2.maxDate))
        
        return combined
    
    @abc.abstractmethod
    def cutoffDate(self, dates: str|tuple=None):
        if not self._categorized:
            return
        
        if type(dates) == tuple:
            self._dates = (datetime.datetime.strptime(dates[0], '%m/%d/%Y'), datetime.datetime.strptime(dates[1], '%m/%d/%Y'))
            self.cutoffDate()
            
        if type(dates) == str:
            self._dates = (datetime.datetime.strptime(dates, '%m/%d/%Y'), self.maxDate)
            self.cutoffDate()
        
        for key in self._spending:
            self._spending[key] = [i for i in self._spending[key] if datetime.datetime.strptime(i[0], '%m/%d/%Y') >= self.minDate and datetime.datetime.strptime(i[0], '%m/%d/%Y') <= self.maxDate]
            
        for key in self._income:
            self._income[key] = [i for i in self._income[key] if datetime.datetime.strptime(i[0], '%m/%d/%Y') >= self.minDate and datetime.datetime.strptime(i[0], '%m/%d/%Y') <= self.maxDate]
    
    def categorize(self):
        self._spendingSummaries = self.returnSummaries(self._spending)
        self._incomeSummaries = self.returnSummaries(self._income)
        if self._categorized == True:
            return
        print("Warning: do not use the financeReader class to read data. Output files will be empty. Instead, use a corresponding subclass.")
    
    def printSpendingCategories(self, outPath = None):
        if self._spendingSummaries == {}: self.categorize()
        
        if outPath == None:
            print(self._spending)
            return
        
        with open(outPath, 'w') as f:
            for key in self._spending:
                if self._spending[key] == []: continue
                f.write(key + '\n')
                f.write("------------------------------------------------------\n")
                f.write("Transaction Date     Description               Amount\n")
                for i in range(len(self._spending[key])):
                    f.write(self._spending[key][i][0] +  "           ")
                    f.write(self._spending[key][i][1][:14] + "            ")
                    f.write("$" + self._spending[key][i][2] +  "          ")
                    f.write("\n")
                f.write("------------------------------------------------------\n")
                f.write("Total:                                         $" + "{:.2f}".format(self._spendingSummaries[key]) + "\n")
                f.write("\n")
            f.write("\n")
            f.write("Grand Total:                                   $" + "{:.2f}".format(sum([math.fabs(self._spendingSummaries[key]) for key in self._spendingSummaries])) + "\n")
        return
    
    def printIncomeCategories(self, outPath = None):
        if self._incomeSummaries == {}: self.categorize()
        
        if outPath == None: 
            print(self._income)
            return
        
        with open(outPath, 'w') as f:
            for key in self._income:
                if self._income[key] == []: continue
                f.write(key + '\n')
                f.write("------------------------------------------------------\n")
                f.write("Transaction Date     Description               Amount\n")
                for i in range(len(self._income[key])):
                    f.write(self._income[key][i][0] +  "           ")
                    f.write(self._income[key][i][1][:14] + "            ")
                    f.write("$" + self._income[key][i][2] +  "          ")
                    f.write("\n")
                f.write("------------------------------------------------------\n")
                f.write("Total:                                         $" + "{:.2f}".format(math.fabs(self._incomeSummaries[key])) + "\n")
                f.write("\n")
            f.write("\n")
            f.write("Grand Total:                                   $" + "{:.2f}".format(sum([math.fabs(self._incomeSummaries[key]) for key in self._incomeSummaries])) + "\n")


    def returnSummaries(self, d):
        return dict([(key, sum([float(d[key][i][2]) for i in range(len(d[key]))])) for key in d if d[key] != []])
    
    def getMinDate(self, date1: datetime.datetime, date2: datetime.datetime):
        if date1 < date2:
            return date1
        else:
            return date2
        
    def getMaxDate(self, date1: datetime.datetime, date2: datetime.datetime):
        if date1 > date2:
            return date1
        else:
            return date2
    
    #Getters
    @property
    def spendingSummaries(self):
        return self._spendingSummaries

    @property
    def incomeSummaries(self):
        return self._incomeSummaries

    @property
    def mainDict(self):
        return self._mainDict
    
    @property
    def spending(self):
        return self._spending
    
    @property
    def income(self):
        return self._income
    
    @property
    def categorized(self):
        return self._categorized
    
    @property
    def dates(self):
        return self._dates
    
    @property
    def minDate(self):
        if type(self._dates) != tuple:
            return self._dates
        return self._dates[0]
    
    @property
    def maxDate(self):
        if type(self._dates) != tuple:
            return self._dates
        return self._dates[1]
    
    #Setters
    @spendingSummaries.setter
    def spendingSummaries(self, spendingSummaries):
        self._spendingSummaries = spendingSummaries
    
    @incomeSummaries.setter
    def incomeSummaries(self, incomeSummaries):
        self._incomeSummaries = incomeSummaries
    
    @mainDict.setter
    def mainDict(self, mainDict):
        self._mainDict = mainDict
    
    @spending.setter
    def spending(self, spending):
        self._spending = spending
    
    @income.setter
    def income(self, income):
        self._income = income  
    
    @categorized.setter
    def categorized(self, categorized):
        self._categorized = categorized
        
    @dates.setter
    def dates(self, dates):
        self._dates = dates