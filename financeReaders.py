import csv
import abc
import datetime
from collections import defaultdict
import math

class FinanceReader():
    #TODO implement cashflow
    #TODO implement date cutoffs on categorized dictionary
    
    def __init__(self, file: str=None, dates: str|tuple=None):        
        self._file = file
        self._mainDict = defaultdict(list)
        self._spending = {"Food": [], "Entertainment": [], "Education" : [], "Shopping": [], "Bills/Tickets": [], "Gas": [], "Other": []}
        self._income = {"Rewards" : [], "Paychecks" : [], "Gifts" : []}
        self._categorized = False

        self._spendingSummaries = {}
        self._incomeSummaries = {}
    
    @classmethod
    def combine(cls, obj1, obj2):
        if obj1.categorized == False: obj1.categorize()
        if obj2.categorized == False: obj2.categorize()
        
        spending = {}
        income = {}
        
        for key in obj1.spending:
            spending[key] = sorted(obj1.spending[key] + obj2.spending[key], key=lambda x: datetime.datetime.strptime(x[0], '%m/%d/%Y'))
        for key in obj1.income:
            income[key] = obj1._income[key] + obj2._income[key]

        combined = FinanceReader()
        combined.spending = spending
        combined.income = income
        combined.categorized = True
        
        return combined
    
    @abc.abstractmethod
    def cutoffDate(self, dates):
        ...
    
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