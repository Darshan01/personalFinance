import csv
import datetime
from collections import defaultdict

class financeReaders:
    _file = None
    _mainDict = defaultdict(list)
    _categories = {"food": [], "entertainment": [], "education" : [], "shopping": [], "tickets": []}
    
    def __init__(self, file):
        self._file = file
        with open(self._file, 'r') as f:
            buf = list(csv.reader(f))
            for cat in range(len(buf[0])):
                for i in range(1,len(buf)):
                    self._mainDict[buf[0][cat]].append(buf[i][cat])
                    
        f.close()
    
    def getMainDict(self):
        return self._mainDict
    
    def getCategories(self):
        return self._categories
    
    # Additional methods and attributes can be added here