import csv
import datetime
from financeReaders import FinanceReader

class DiscoverCredit(FinanceReader):
    
    def __init__(self, file: str=None, dates: str|tuple=None):
        if file is None:
            print("Please specify a file for the DiscoverCredit class.\n")
            return
            
        super().__init__(file, dates)
        
        with open(self._file, 'r') as f:
            buf = list(csv.reader(f))
            for column in range(len(buf[0])):
                for i in range(1,len(buf)):
                    self._mainDict[buf[0][column]].append(buf[i][column])     
        f.close()
        
        if dates is not None:
            self.cutoffDate(dates)
        self.categorize()
        
    
    def cutoffDate(self, dates):
        if type(dates) == str:
            for start in range(len(self._mainDict['Trans. Date'])):
                if datetime.datetime.strptime(self._mainDict['Trans. Date'][start], '%m/%d/%Y') >= datetime.datetime.strptime(dates, '%m/%d/%Y'):
                    break
            
            for column in self._mainDict:
                self._mainDict[column] = self._mainDict[column][start:]
            
            return
            
        for start in range(len(self._mainDict['Trans. Date'])):
            if datetime.datetime.strptime(self._mainDict['Trans. Date'][start], '%m/%d/%Y') >= datetime.datetime.strptime(dates[0], '%m/%d/%Y'):
                break
        
        for end in range(len(self.mainDict['Trans. Date']) - 1, -1, -1):
            if datetime.datetime.strptime(self._mainDict['Trans. Date'][end], '%m/%d/%Y') <= datetime.datetime.strptime(dates[1], '%m/%d/%Y'):
                break
        
        for column in self._mainDict:
            self._mainDict[column] = self._mainDict[column][start:end+1]

    def categorize(self):
        if self._categorized:
            return
        
        for i in range(len(self._mainDict['Trans. Date'])):
            if self._mainDict['Category'][i] == 'Restaurants' or self._mainDict['Category'][i] == 'Supermarkets':
                self._spending['Food'].append([self._mainDict[key][i] for key in self._mainDict if key != 'Category' and key !='Post Date'])
            if self._mainDict['Category'][i] == 'Education':
                self._spending['Education'].append([self._mainDict[key][i] for key in self._mainDict if key != 'Category' and key !='Post Date'])
            if self._mainDict['Category'][i] == 'Gasoline':
                self._spending['Gas'].append([self._mainDict[key][i] for key in self._mainDict if key != 'Category' and key !='Post Date'])
            if self._mainDict['Category'][i] == 'Travel/ Entertainment':
                self._spending['Entertainment'].append([self._mainDict[key][i] for key in self._mainDict if key != 'Category' and key !='Post Date'])
            
            if self._mainDict['Category'][i] == 'Awards and Rebate Credits':
                self._income['Rewards'].append([self._mainDict[key][i][1:] if key == 'Amount' else self._mainDict[key][i] for key in self._mainDict if key != 'Category' and key !='Post Date'])
        
        self._spendingSummaries = self.returnSummaries(self._spending)
        self._incomeSummaries = self.returnSummaries(self._income)
        
        self._categorized = True
    
            

   