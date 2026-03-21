import pandas as pd
import os
import requests

BOT_TOKEN = "8578701576:AAEDZBJmIGGLKQj7p39SzWOsuYUcCP18TrY"

def send_telegram_alert(message, chat_id, username):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}

    try:
        response = requests.post(url, data=payload)
        print("DEBUG:", response.text) 

        if response.status_code == 200:
            print(f"✅ Alert sent to {username}")
        else:
            print("❌ Telegram failed")

    except Exception as e:
        print("Telegram error:", e)


def run_smart_analysis(username, expense_file="expenses.csv", accounts_file="accounts.csv"):
    if not os.path.exists(expense_file) or not os.path.exists(accounts_file):
        return

    try:
       
        acc_df = pd.read_csv(accounts_file)

        user_data = acc_df[acc_df['Username'] == username]
        if user_data.empty:
            print("User not found")
            return

        user_row = user_data.iloc[0]

        chat_id = str(user_row['Telegram_ID'])

        allowance_data = str(user_row['Allowance']).split(";")
        allowance_list = [float(x) for x in allowance_data]

        threshold = allowance_list[0]
        full_allowance = allowance_list[-1]

        expense_df = pd.read_csv(
            expense_file,
            names=["username", "amount", "date", "category"],
            header=None
        )

        expense_df = expense_df[expense_df["username"] == username]

        expense_df["amount"] = pd.to_numeric(expense_df["amount"], errors='coerce')
        expense_df = expense_df.dropna(subset=["amount"])

        total_spent = expense_df["amount"].sum()

        if full_allowance == 0:
            return

        ratio = total_spent / full_allowance

    
        msg = ""

        if ratio >= 0.85:
            msg = (
                f"🚨 *Spending Alert: Critical Level Reached*\n\n"
                f"User: {username}\n"
                f"Usage: {ratio*100:.1f}% of total allowance\n"
                f"Remaining Balance: ${full_allowance - total_spent:.2f}\n\n"
                f"Please review your expenses to avoid exceeding your budget."
            )

        elif total_spent >= threshold:
            msg = (
                f"⚠️ *Spending Alert: Budget Threshold Reached*\n\n"
                f"User: {username}\n"
                f"Total Spent: ${total_spent:.2f}\n"
                f"Allowance: ${full_allowance:.2f}\n\n"
                f"You have reached your predefined spending limit. Consider monitoring your expenses closely."
            )

        if msg:
            send_telegram_alert(msg, chat_id, username)
        else:
            print(f"{username}: Spending is within safe limits ({ratio*100:.1f}% used).")

    except Exception as e:
        print("Smart Alert Error:", e)