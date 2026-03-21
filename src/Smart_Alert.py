import pandas as pd
import os
import requests

BOT_TOKEN = "8578701576:AAEDZBJmIGGLKQj7p39SzWOsuYUcCP18TrY"

def send_telegram_alert(message, chat_id, username):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, data=payload)

        if response.status_code == 200:
            print(f"✅ Alert sent to Telegram for {username}")
        else:
            print(f"❌ Telegram Error: {response.text}")
    except Exception as e:
        print(f"Telegram Connection Error: {e}")

def run_smart_analysis(username, expense_file="expenses.csv", accounts_file="accounts.csv",):
    
    if not all(os.path.exists(f) for f in [expense_file, accounts_file,]):
        print("[!] Files missing. Waiting for user data...")
        return

    try:
        acc_df = pd.read_csv(accounts_file)
        user_row = acc_df[acc_df['Username'] == username].iloc[0]

        chat_id = str(user_row['Telegram_ID'])
        
        allowance_data = str(user_row['Allowance']).split(";")
        allowance_list = [float(x) for x in allowance_data]

        full_allowance = allowance_list[-1]
        user_threshold_value = allowance_list[0]

        expense_df = pd.read_csv(expense_file, names=["date", "category", "amount"])
        total_spent = expense_df["amount"].sum()
        
        if full_allowance == 0: return 
        spending_ratio = total_spent / full_allowance

        alert_msg = ""
        hard_limit = 0.85
        
        if spending_ratio >= hard_limit:
            alert_msg = f"🚨 *CRITICAL ALERT: {username.upper()}*\n"
            alert_msg += f"You have spent *{spending_ratio*100:.1f}%* of your allowance!\n"
            alert_msg += f"Remaining: ${full_allowance - total_spent:.2f}"
        
        elif total_spent >= user_threshold_value:

            custom_percent = (user_threshold_value / full_allowance) * 100
            alert_msg = f"⚠️ *BUDGET NOTICE: {username.upper()}*\n"
            alert_msg += f"You reached your personal limit of *{custom_percent:.0f}%*.\n"
            alert_msg += f"Current Spend: ${total_spent:.2f} / ${full_allowance:.2f}"

        if alert_msg:
            send_telegram_alert(alert_msg, chat_id, username)
        else:
            print(f"📊 {username}'s spending is safe ({spending_ratio*100:.1f}% used).")

    except Exception as e:
        print(f"Error in Smart Alert: {e}")
