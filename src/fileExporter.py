import pandas as pd
import os

class FileExporter:
    def __init__(self, file):
        self.file = file
        self.data = None
        # export to same folder as the source file
        self.output_dir = os.path.dirname(self.file) or "."
        # all of these columns needed in csv file
        self.required_columns = ["username", "date", "item", "amount", "category", "time", "day"]

    def check_file(self):
        if not os.path.exists(self.file):
            print(f"Error: {self.file} not found.")
            exit()

    def read_file(self):
        # read the CSV file
        self.data = pd.read_csv(self.file)

        # convert to lowercase so we can know the column names without worrying about case sensitivity
        self.data.columns = self.data.columns.str.lower()

    def check_columns(self):
        for col in self.required_columns:
            if col not in self.data.columns:
                print(f"Error: Missing required column {col}")
                exit()

    def clean_data(self):
        # Convert date column to datetime
        self.data["date"] = pd.to_datetime(self.data["date"], errors="coerce")

        # Convert amount to numeric
        self.data["amount"] = pd.to_numeric(self.data["amount"], errors="coerce")

    def export_all(self):
        output_path = os.path.join(self.output_dir, "myExpenses1.csv")
        self.data.to_csv(output_path, index=False)
        print("All expenses exported successfully")

    def item_summary(self):
        # summarize expenses by username and item
        item_summary = self.data.groupby(["username", "item"])["amount"].sum().reset_index()

        # Export item summary
        output_path = os.path.join(self.output_dir, "item_summary.csv")
        item_summary.to_csv(output_path, index=False)
        print("Item summary exported successfully")

    def monthly_summary(self):
        # Create monthly summary
        self.data["month"] = self.data["date"].dt.to_period("M").astype(str)

        monthly_summary = self.data.groupby(["username", "month"])["amount"].sum().reset_index()

        # Export monthly summary
        output_path = os.path.join(self.output_dir, "monthly_summary.csv")
        monthly_summary.to_csv(output_path, index=False)
        print("Monthly summary exported successfully")

    def category_summary(self):
        # summarize expenses by username and category
        category_summary = self.data.groupby(["username", "category"])["amount"].sum().reset_index()

        output_path = os.path.join(self.output_dir, "category_summary.csv")
        category_summary.to_csv(output_path, index=False)
        print("Category summary exported successfully")

    def amount_summary(self):
        # total expense amount per username
        amount_summary = (
            self.data.groupby("username")["amount"].sum().reset_index(name="total_amount")
        )

        output_path = os.path.join(self.output_dir, "amount_summary.csv")
        amount_summary.to_csv(output_path, index=False)
        print("Amount summary exported successfully")

