import sys
import os

from src.member_access import UpdateInfo
from src.expense_tracker import ExpenseTracker
from src.saving_plan import SavingPlan
from src.Smart_Alert import run_smart_analysis
from src.fileExporter import FileExporter

def user_dashboard(username):
    tracker = ExpenseTracker(username)   # ✅ FIXED HERE
    savings = SavingPlan(username=username)
    
    # Auto-run analysis when dashboard opens
    run_smart_analysis(username)

    while True:
        print(f"\n=======================================")
        print(f" --- JOMNAY - Welcome, {username}! --- ")
        print(f"=======================================")
        print("1. Add New Expense")
        print("2. View Expense History")
        print("3. Manage Savings Pot")
        print("4. Export Expense Reports (CSV)")
        print("5. Account Settings")
        print("6. Logout")
        
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
                run_smart_analysis(username)

            elif s_choice == '2':
                savings.saving()
            
        elif choice == '4':
            if os.path.exists("expenses.csv"):
                exporter = FileExporter("expenses.csv")
                exporter.read_file()
                exporter.export_all()
                print("Reports exported successfully.")
            else:
                print("No data to export.")
            
        elif choice == '5':
            updater = UpdateInfo()
            updater.menu(username)
            
        elif choice == '6':
            print(f"Logging out... Goodbye {username}!")
            break


def start_app():
    auth = UpdateInfo()

    while True:
        print(f"\n=======================================")
        print(f" ---       Welcome to JOMNAY       --- ")
        print(f"=======================================")
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