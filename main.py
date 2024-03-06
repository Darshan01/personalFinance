import datetime
import csv
from bofa import Bofa
from discover import DiscoverCredit
from financeReaders import FinanceReader

def main():
    dates = ("02/01/2024", "02/29/2024")
    
    dreader = DiscoverCredit('./csv/discover.csv', dates)
    bofa = Bofa('./csv/bofa.csv', dates)
    
    combined = FinanceReader.combine(dreader, bofa)
    
    combined.printSpendingCategories(outPath="./output/spending.txt")
    combined.printIncomeCategories(outPath="./output/income.txt")

 



if __name__ == "__main__":
    main()