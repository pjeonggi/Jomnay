import csv 
import os 
from datetime import datetime

class Expense:
    def __init__(self, username, amount, date, category):
        self.username = username
        self.amount = amount
        self.date = date 
        self.category = category

    def __str__(self):
        return f"{self.date} | {self.category.ljust(12)} | ${self.amount:.2f}"


class ExpenseTracker:
    def __init__(self, username, filename="expenses.csv"):
        self.filename = filename
        self.username = username
        self.history = []
        self.load_from_csv()

    def add_expense(self):
        print("\n--- Add New Expense ---")
        try:
            amount = float(input("Enter amount spent: "))
            date = input("Enter date (YYYY-MM-DD): ")
            category = input("Enter category: ")

            new_expense = Expense(self.username, amount, date, category)
            self.history.append(new_expense)
            self.save_to_csv(new_expense)

            print("✅ Expense saved!")

        except ValueError:
            print("Invalid input.")

    def save_to_csv(self, expense):
        with open(self.filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            # ✅ FIXED FORMAT
            writer.writerow([expense.username, expense.amount, expense.date, expense.category])

    def load_from_csv(self):
        if os.path.exists(self.filename):
            with open(self.filename, mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) == 4:
                        try:
                            username, amount, date, category = row
                            if username == self.username:
                                self.history.append(
                                    Expense(username, float(amount), date, category)
                                )
                        except:
                            continue

    def show_history(self):
        print("\n--- Expense History ---")
        if not self.history:
            print("No transactions found")
        else:
            for item in self.history:
                print(item)
        
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
               
    