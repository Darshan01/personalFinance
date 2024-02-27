import csv
import datetime
from financeReaders import financeReaders

class Discover(financeReaders):
    _file = None
    _categories = {"food": [], "entertainment": [], "education" : [], "shopping": [], "tickets": []}
    
    def __init__(self, file):
        super().__init__(file)
    
    def cutoffDate(self, date):
        flag = 0
        for i in range(len(self._mainDict['Trans. Date'])):
            flag = i
            if datetime.datetime.strptime(self._mainDict['Trans. Date'][i], '%m/%d/%Y') >= datetime.datetime.strptime(date, '%m/%d/%Y'):
                break
        for j in self._mainDict:
            self._mainDict[j] = self._mainDict[j][flag:]

    def categorize(self):
        for i in range(len(self._mainDict['Trans. Date'])):
            if self._mainDict['Category'][i] == 'Restaurants' or self._mainDict['Category'][i] == 'Supermarkets':
                self._categories['food'].append([self._mainDict[key][i] for key in self._mainDict if key != 'Category'])
    
    def getSummaries(self):
        return dict([(key, sum([float(self._categories[key][i][3]) for i in range(len(self._categories['food']))])) for key in self._categories if self._categories[key] != []])
                
    
    
