import csv
import datetime
from financeReaders import FinanceReader

class DiscoverCredit(FinanceReader):
    
    #TODO fully implement categorization, hopefully with AI
    def __init__(self, file: str=None, dates: str|tuple=None):
        if file is None:
            print("Please specify a file for the DiscoverCredit class.\n")
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
            
            for column in range(len(buf[0])):
                
                for i in range(1,len(buf)):
                    
                    self._mainDict[buf[0][column]].append(buf[i][column])    
                    
                    if buf[0][column] == "Trans. Date" and dates is None:
                        if minDate > datetime.datetime.strptime(buf[i][column], '%m/%d/%Y'):
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

        
        for start in range(len(self._mainDict['Trans. Date'])):
            if datetime.datetime.strptime(self._mainDict['Trans. Date'][start], '%m/%d/%Y') >= self.dates[0]:
                break
        
        for end in range(len(self.mainDict['Trans. Date']) - 1, -1, -1):
            if datetime.datetime.strptime(self._mainDict['Trans. Date'][end], '%m/%d/%Y') <= self.dates[1]:
                break
        
        for column in self._mainDict:
            self._mainDict[column] = self._mainDict[column][start:end+1]
        
        self.categorize()

    def categorize(self):
        for i in range(len(self._mainDict['Trans. Date'])):
            
            #spending
            if self._mainDict['Category'][i] == 'Restaurants' or self._mainDict['Category'][i] == 'Supermarkets':
                self._spending['Food'].append([self._mainDict[key][i] for key in self._mainDict if key != 'Category' and key !='Post Date'])
                
            elif self._mainDict['Category'][i] == 'Education':
                self._spending['Education'].append([self._mainDict[key][i] for key in self._mainDict if key != 'Category' and key !='Post Date'])
                
            elif self._mainDict['Category'][i] == 'Gasoline':
                self._spending['Gas/Convenience'].append([self._mainDict[key][i] for key in self._mainDict if key != 'Category' and key !='Post Date'])
                
            elif self._mainDict['Category'][i] == 'Travel/ Entertainment':
                self._spending['Entertainment'].append([self._mainDict[key][i] for key in self._mainDict if key != 'Category' and key !='Post Date'])
            
            #income
            elif self._mainDict['Category'][i] == 'Awards and Rebate Credits':
                self._income['Rewards'].append([self._mainDict[key][i][1:] if key == 'Amount' else self._mainDict[key][i] for key in self._mainDict if key != 'Category' and key !='Post Date'])

            elif self._mainDict['Category'][i] == 'Payments and Credits':
                pass
            
            else:
                self._spending['Other'].append([self._mainDict[key][i] for key in self._mainDict if key != 'Category' and key !='Post Date'])
           
   
        
        self._spendingSummaries = self.returnSummaries(self._spending)
        self._incomeSummaries = self.returnSummaries(self._income)
        
        self._categorized = True
    
            

   