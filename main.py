import sys
import os
import csv

from src.member_access import UpdateInfo
from src.expense_tracker import ExpenseTracker
from src.saving_plan import SavingPlan
from src.Smart_Alert import run_smart_analysis
from src.fileExporter import FileExporter
from src.spendingTrend import SpendingTrend

def user_dashboard(username):
    tracker = ExpenseTracker(username)
    savings = SavingPlan(username=username)

    while True:
        print(f"\n=================================================================")
        print(f"                 JOMNAY - Welcome, {username}!")
        print(f"=================================================================")
        print("1. Add New Expense")
        print("2. View Expense History")
        print("3. Manage Savings Pot")
        print("4. View Spending Trends")
        print("5. Export Expense Reports (CSV)")
        print("6. Account Settings")
        print("7. Logout")
        
        choice = input("\nSelect an option: ").strip()

        if choice == '1':
            tracker.add_expense()
            run_smart_analysis(username)
            
        elif choice == '2':
            tracker.show_history()
            
        elif choice == '3':
            print("\n--- Savings Management ---")
            print("1. View Savings Pot / Withdraw")
            print("2. Move Monthly Surplus to Savings")
            s_choice = input("Select: ").strip()

            if s_choice == '1':
                savings.use_saving()

            elif s_choice == '2':
                savings.saving()

        elif choice == '4':
            trend = SpendingTrend()

            if not os.path.exists("expenses.csv"):
                print("No expense data found.")
                continue

            focus_month = input("Enter month (YYYY-MM) or leave blank: ").strip()
            focus_month = focus_month if focus_month else None

            with open("expenses.csv", newline="") as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) != 4:
                        continue

                    user, amount, date, category = row

                    if user != username:
                        continue

                    try:
                        amount = float(amount)
                    except:
                        continue

                    month = date[:7] 
                    trend.add_spending(month, category, amount)

            trend.print_report(focus_month)

            suggestions = trend.get_suggestions()
            print("\n💡 Suggestions:")
            for s in suggestions:
                print("-", s)

            export = input("Export to PDF? (y/n): ").strip().lower()
            if export == 'y':
                os.makedirs("reportPDF", exist_ok=True)
                filename = f"reportPDF/spending_trend_{username}.pdf"
                trend.export_to_pdf(filename, focus_month)
            
        elif choice == '5':
            if os.path.exists("expenses.csv"):
                exporter = FileExporter("expenses.csv")
                exporter.read_file()
                exporter.export_all()
                print("Reports exported successfully.")
            else:
                print("No data to export.")
            
        elif choice == '6':
            updater = UpdateInfo()
            updater.menu(username)
            
        elif choice == '7':
            print(f"Logging out... Goodbye {username}!")
            break


def start_app():
    auth = UpdateInfo()

    while True:
        print("\n******************************************************************")
        print("                       WELCOME TO JOMNAY         ")
        print("******************************************************************")
        print("1. Login\n2. Sign Up\n3. Forgot Password\n4. Exit")
        
        entry_choice = input("Selection: ").strip()
        
        if entry_choice == '1':
            username = auth.login()
            if auth.logged_in:
                user_dashboard(username)

        elif entry_choice == '2':
            auth.sign_up()

        elif entry_choice == '3':
            u = input("Username: ")
            auth.forgot_password(u)

        elif entry_choice == '4':
            sys.exit()


if __name__ == "__main__":
    start_app()