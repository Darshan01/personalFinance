from bofa import Bofa
from discover import DiscoverCredit
from financeReaders import FinanceReader

def main():
    dates = ("02/01/2024", "02/29/2024")
    
    discover2023 = DiscoverCredit('./csv/discover23.csv')
    discover2024 = DiscoverCredit('./csv/discover24.csv')
    
    bofa2023 = Bofa('./csv/bofa23.csv')
    bofa2024 = Bofa('./csv/bofa24.csv')
    
    discover = FinanceReader.combine(discover2023, discover2024)
    bofa = FinanceReader.combine(bofa2023, bofa2024)
    
    combined = FinanceReader.combine(discover, bofa)
    combined.cutoffDate(dates)
    
    combined.printSpendingCategories(outPath="./output/spending.txt")
    combined.printIncomeCategories(outPath="./output/income.txt")

 



if __name__ == "__main__":
    main()