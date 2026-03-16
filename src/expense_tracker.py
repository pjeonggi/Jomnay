import csv 
import os 
from datetime import datetime
# This class acts like a 'Template' for a single receipt
class Expense:
    def __init__(self,amount,date,category):
        self.amount = amount
        self.date = date 
        self.category = category
    # This tells Python how to print the expense in a nice format
    def __str__(self):
        return f"{self.date}| {self.category.ljust(12)} | ${self.amount: .2f}"
    

# This class manages the collection of all expenses
class ExpenseTracker:
    def __init__(self, filename = "expenses.csv"):
        self.filename = filename
        self.history = []
        # Automatically laod existing data when the program starts
        self.load_from_csv()

    def add_expense(self):
        print ("\n--- Add New Expense ---")
        try:
            amount = float(input("Enter amount spent: "))
            date = input("Enter date (ex., YYY-MM-DD): ")
            category = input ("Enter category (ex., Food, Transport):")
            new_expense = Expense (amount , date ,category)
            self.history.append(new_expense)
            self.save_to_csv(new_expense)
            print ("Expense Saved To file!")
        except ValueError:
            print ("Invalid input. Please enter a number for the amount.")

    def save_to_csv(self, expense):
        # 'a' means Append mode (adds to the end of the file)
        with open(self.filename, mode='a', newline='') as file:
            writer = csv.writer(file)      
            formatted_line = f"{expense.date}-> {expense.category} = {expense.amount}$"
            # wrap it in [] because writerow expects a list 
            writer.writerow([formatted_line])
            
    
    def load_from_csv(self):
        if os.path.exists(self.filename):
            with open(self.filename, mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) == 3:
                        try:
                            # This ensures we only load valid numeric data
                            saved_expense = Expense(float(row[0]), row[1], row[2])
                            self.history.append(saved_expense)
                        except ValueError:
                            # This skips the header row or any corrupted data
                            return
    def show_history(self):
           
           print ("\n--- Expense History---")
           if not self.history:
               print("No transactions found")
           else:
               print ("Date | Category | Amount ")
               print ("-> "  )
               for item in self.history:
                   print (item)
        
if __name__ =='__main__':
    tracker = ExpenseTracker()
    while True:
        # show the menu option 
        print ("\n1. Add Expense")
        print ("\n2. View History")
        print ("\n3. Exit")
        choice = input ("Choose an option : ")
        if choice =='1':
            tracker.add_expense()
        elif choice =='2':
            tracker.show_history()
        elif choice =='3':
            print ("Goodbye !")
            break 
        else :
            print ("Invalid choice , try again.")    
               
    