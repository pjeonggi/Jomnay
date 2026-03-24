import pandas as pd
import json
import os

class SavingPlan:
    def __init__(self, username, accounts_file="accounts.csv"):
        self.username = username
        self.saving_file = "Total_saving.json"
        self.accounts_file = accounts_file
        self.monthly_allowance = self.load_allowance()

    def load_allowance(self):
        """Pulls the total allowance from Smey's semicolon-separated list"""
        if not os.path.exists(self.accounts_file):
            print(f"[!] {self.accounts_file} not found. Using default $0.")
            return 0.0
        try:
            df = pd.read_csv(self.accounts_file)
            user_data = df[df['Username'] == self.username].iloc[0]

            allowance_str = str(user_data['Allowance']).split(";")
            return float(allowance_str[-1])
        except Exception as e:
            print(f"Could not load allowance for {self.username}: {e}")
            return 0.0

    def load_saving(self):
        if not os.path.exists(self.saving_file):
            return 0.0
        try:
            with open(self.saving_file, "r") as f:
                data = json.load(f)
                user_data = data.get(self.username, {})
                return float(user_data.get("Total_saved", 0.0))
        except (json.JSONDecodeError, KeyError):
            return 0.0

    def shared_json(self, new_total):
    
        all_data = {}
        if os.path.exists(self.saving_file):
            try:
                with open(self.saving_file, "r") as f:
                    all_data = json.load(f)
            except json.JSONDecodeError:
                all_data = {}

        all_data[self.username] = {"Total_saved": new_total}

        with open(self.saving_file, "w") as f:
            json.dump(all_data, f, indent=4)
        
    def saving(self, filename="expenses.csv"):
        if not os.path.exists(filename):
            print("\n[!] No expenses found ")
            return
        
        try:
            df = pd.read_csv(filename, names=["username", "amount", "date", "category"])
            
            user_expenses = df[df["username"] == self.username]
            total_spent = user_expenses["amount"].sum()
            
            availableFunds = self.monthly_allowance - total_spent

            if availableFunds <= 0:
                print(f"\nYour balance is ${availableFunds:.2f}. No money available to save.")
                return
            
            print(f"\n ----- JOMNAY SAVINGS ----- ")
            print(f"You have ${availableFunds:.2f} remaining in your allowance.")
            choice = input("Would you like to move these funds to your Savings Pot? (Yes/No): ").strip().lower()

            if choice == "yes":
                amount_input = input(f"How much do you want to save? Type 'All' or enter value: ").strip().lower()

                if amount_input == "all":
                    save_amount = availableFunds
                else:
                    try:
                        save_amount = float(amount_input)
                        
                        if save_amount > availableFunds:
                            print(f"ERROR!! You only have ${availableFunds:.2f} available.")
                            return
                    except ValueError:
                        print("Invalid amount entered.")
                        return
                    
                current_total = self.load_saving()
                new_total = current_total + save_amount
                self.shared_json(new_total)

                self.monthly_allowance -= save_amount
                print(f"\n${save_amount:.2f} moved to your Savings Pot.")
            
            else:
                return
        
        except Exception as e:
            print(f"An error occurred: {e}")

    def use_saving(self):
        current_saving = self.load_saving()

        print(f"\n ----- JOMNAY SAVINGS POT ----- ")
        print(f"You currently have ${current_saving:.2f} in savings.")

        if current_saving <= 0 :
            print("Your savings pot is empty.")
            return
        
        choice = input("Would you like to use some of your savings? (Yes/No): ").strip().lower()

        if choice == "yes" :
            amount_input = input(f"Enter the amount you want to use: ").strip()

            try:
                withdraw_amount = float(amount_input)
                if withdraw_amount > current_saving:
                    print(f"ERROR!! You only have ${current_saving:.2f} in your pot.")
                elif withdraw_amount <= 0:
                    print("Not enough")
                else:
                    self.monthly_allowance += withdraw_amount
                    new_total = current_saving - withdraw_amount
                    self.shared_json(new_total)

                    print(f"\nSuccess! ${withdraw_amount:.2f} added back to your allowance.")
            
            except ValueError:
                print("Invalid input. Please enter a valid number.")

        else:
            print("Transaction cancelled.")
