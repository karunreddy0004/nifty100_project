from company_analysis import company_report
from sector_analysis import sector_analysis
from screener import stock_screener
from ranking import top_rankings

while True:

    print("\n====== NIFTY100 DASHBOARD ======")
    print("1. Company Report")
    print("2. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        company = input("Company ID: ").upper()
        year = int(input("Year: "))
        company_report(company, year)

    elif choice == "2":
        print("Goodbye!")
        break

    else:
        print("Invalid choice.")