import csv
import datetime
from financeReaders import FinanceReader

class Bofa(FinanceReader):
    #TODO fully implement categorization, hopefully with AI
    
    def __init__(self, file: str=None, dates: str|tuple=None):
        if file is None:
            print("Please specify a file for the Bank of America (Bofa) class.")
            return
        
        super().__init__(file, dates)
        
        if dates is None:
            minDate = datetime.datetime.max
            maxDate = datetime.datetime.min
        if type(dates) == str:
            minDate = datetime.datetime.strptime(dates, '%m/%d/%Y')
            maxDate = datetime.datetime.min
        
        with open(self._file, 'r') as f:
            
            buf = list(csv.reader(f))
            
            for column in range(len(buf[6]) - 1):
                
                for i in range(8,len(buf)):
                    
                    self._mainDict[buf[6][column]].append(buf[i][column])
                    
                    if buf[6][column] == "Date" and type(dates) != tuple:
                        if type(dates) != str and minDate > datetime.datetime.strptime(buf[i][column], '%m/%d/%Y'):
                            minDate = datetime.datetime.strptime(buf[i][column], '%m/%d/%Y')
                            
                        if maxDate < datetime.datetime.strptime(buf[i][column], '%m/%d/%Y'):
                            maxDate = datetime.datetime.strptime(buf[i][column], '%m/%d/%Y')
        
        
        if type(dates) != tuple:
            self.dates = (minDate, maxDate)
        if type(dates) == tuple:
            self.dates = (datetime.datetime.strptime(dates[0], '%m/%d/%Y'), datetime.datetime.strptime(dates[1], '%m/%d/%Y'))
        
        self.cutoffDate()
        
        
    
    def cutoffDate(self, dates: str|tuple=None):
        if type(dates) == tuple:
            self.dates = (datetime.datetime.strptime(dates[0], '%m/%d/%Y'), datetime.datetime.strptime(dates[1], '%m/%d/%Y'))
            self.cutoffDate()
            
        if type(dates) == str:
            self.dates = (datetime.datetime.strptime(dates, '%m/%d/%Y'), self.maxDate)
            self.cutoffDate()
        
        for start in range(len(self._mainDict['Date'])):
                if datetime.datetime.strptime(self._mainDict['Date'][start], '%m/%d/%Y') >= self.dates[0]:
                    break
                
        for end in range(len(self._mainDict['Date']) - 1, -1, -1):
            if datetime.datetime.strptime(self._mainDict['Date'][end], '%m/%d/%Y') <= self.dates[1]:
                break
        
        for column in self._mainDict:
            self._mainDict[column] = self._mainDict[column][start:end+1]
        
        self.categorize()
            
            
    def categorize(self):
        for i in range(len(self._mainDict['Date'])):
            
            #income
            if float(self._mainDict['Amount'][i].replace(",","")) > 0:
                if "rutgers" in self._mainDict['Description'][i].lower():
                    self._income['Paychecks'].append([self._mainDict[key][i] for key in self._mainDict if key != 'Category'])

            
        self._spendingSummaries = self.returnSummaries(self._spending)
        self._incomeSummaries = self.returnSummaries(self._income)
        self._categorized = True
    
