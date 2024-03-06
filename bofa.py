import csv
import datetime
from collections import defaultdict
from financeReaders import FinanceReader

class Bofa(FinanceReader):
    
    def __init__(self, file: str=None, dates: str|tuple=None):
        if file is None:
            print("Please specify a file for the Bank of America (Bofa) class.")
            return
        
        super().__init__(file, dates)
        
        self._file = file
        with open(self._file, 'r') as f:
            buf = list(csv.reader(f))
            for cat in range(len(buf[6]) - 1):
                for i in range(8,len(buf)):
                    self._mainDict[buf[6][cat]].append(buf[i][cat])
                    
        f.close()
        
        if dates is not None:
            self.cutoffDate(dates)
        self.categorize()
    
    def cutoffDate(self, dates):
        if type(dates) == str:
            for start in range(len(self._mainDict['Date'])):
                if datetime.datetime.strptime(self._mainDict['Date'][start], '%m/%d/%Y') >= datetime.datetime.strptime(dates, '%m/%d/%Y'):
                    break
            
            for column in self._mainDict:
                self._mainDict[column] = self._mainDict[column][start:]
                
            return

        for start in range(len(self._mainDict['Date'])):
                if datetime.datetime.strptime(self._mainDict['Date'][start], '%m/%d/%Y') >= datetime.datetime.strptime(dates[0], '%m/%d/%Y'):
                    break
                
        for end in range(len(self._mainDict['Date']) - 1, -1, -1):
            if datetime.datetime.strptime(self._mainDict['Date'][end], '%m/%d/%Y') <= datetime.datetime.strptime(dates[1], '%m/%d/%Y'):
                break
        
        for column in self._mainDict:
            self._mainDict[column] = self._mainDict[column][start:end+1]
            
            
    def categorize(self):
        if self._categorized:
            return True
        
        for i in range(len(self._mainDict['Date'])):
            if float(self._mainDict['Amount'][i].replace(",","")) > 0:
                if "rutgers" in self._mainDict['Description'][i].lower():
                    self._income['Paychecks'].append([self._mainDict[key][i] for key in self._mainDict if key != 'Category'])
            
            
        self._spendingSummaries = self.returnSummaries(self._spending)
        self._incomeSummaries = self.returnSummaries(self._income)
        self._categorized = True
    
