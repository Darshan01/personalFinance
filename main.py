import datetime
import csv
from bofa import Bofa
from discover import Discover
from collections import defaultdict

def main():
    dreader = Discover('./csv/discoverFeb.csv')
    dreader.cutoffDate('02/02/2024')
    dreader.categorize()
    print(dreader.getSummaries())



if __name__ == "__main__":
    main()