import hashlib
import msvcrt
import re
import csv

# --- Custom Exceptions ---
class LoginError(Exception):
    pass
class SignupError(Exception):
    pass

class User:
    def __init__(self, username, password, phone_number,telegram_id, allowance_list, hashed=False):
        self.username = username
        self.password = password if hashed else hashlib.sha256(password.encode()).hexdigest()
        self.phone_number = phone_number
        self.telegram_id = telegram_id
        self.allowance = allowance_list  # list of daily allowances

class AccountManager:
    def __init__(self, filename="accounts.csv"):
        self.accounts = {}
        self.filename = filename
        self.logged_in = False
        self.current_user = None 
        self.load_accounts()

    # --- CSV Persistence ---
    def save_accounts(self):
        try:
            with open(self.filename, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Username", "Password", "Phone","Telegram ID", "Allowance"])
                for user in self.accounts.values():
                    writer.writerow([
                        user.username,
                        user.password,
                        user.phone_number,
                        user.telegram_id,
                        ";".join(map(str, user.allowance))
                    ])
        except Exception as e:
            raise SignupError(f"Error saving accounts: {e}")

    def load_accounts(self):
        try:
            with open(self.filename, mode="r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    allowance_list = row["Allowance"].split(";") if row["Allowance"] else []
                    allowance_list = [float(x) for x in allowance_list]
                    user = User(
                        row["Username"],
                        row["Password"],
                        row["Phone"],
                        row["Telegram ID"],
                        allowance_list,
                        hashed=True
                    )
                    self.accounts[user.username] = user
        except FileNotFoundError:
            pass

    # --- Validation Helpers ---
    def is_taken(self, username):
        return username in self.accounts

    def masked_input(self, prompt):
        print(prompt, end="", flush=True)
        password = ""
        while True:
            ch = msvcrt.getch()
            if ch == b'\r':  # Enter
                print()
                break
            elif ch == b'\x08':  # Backspace
                if len(password) > 0:
                    password = password[:-1]
                    print("\b \b", end="", flush=True)
            else:
                password += ch.decode()
                print("●", end="", flush=True)
        return password

    def is_strong(self, pw):
        rules = [
            (len(pw) >= 9, "At least 9 characters"),
            (re.search(r"[a-z]", pw), "Lowercase letter"),
            (re.search(r"[A-Z]", pw), "Uppercase letter"),
            (re.search(r"\d", pw), "One digit"),
            (re.search(r"[!@#$%^&*(),.?\":{}|<>]", pw), "One special character"),
        ]
        failed = [msg for check, msg in rules if not check]
        return (not failed, failed)

    def is_phone_number(self, pn):
        prefix = {"011","012","014","017","077","078","085","089","092","095","099",
                  "018","088","090","097","031","060","066","067","068","096","010",
                  "015","016","069","070","081","086","087","093","098"}
        suffix = [
            (len(pn) >= 9, "At least 9 digits!"),
            (len(pn) <= 10, "Not a phone number!"),
            (not re.search(r"[a-zA-Z!@#$%^&*(),.?\":{}|<>]", pn), "Not a phone number!"),
        ]
        failed = [msg for check, msg in suffix if not check]
        return (pn[:3] in prefix and not failed, failed)
    
    def is_telegram_username(self, tu):
        rules = [
            (len(tu) >= 10, "At least 10 digit"),
            (not re.search(r"[a-zA-Z!@#$%^&*(),.?\":{}|<>]", tu), "Invalid characters"),
        ]
        failed = [msg for check, msg in rules if not check]
        return (not failed, failed)

    def input_allowance(self):
        mon_allowance = float(input("Input your monthly allowance: "))
        alert = input("Input percentage to alert when expense reach (default 85%): ").strip()

        daily_allowances = [
            mon_allowance * 0.85,   # default alert
            mon_allowance           # full allowance (last element)
        ]

        if alert.isdigit():
            alert_per = int(alert)
            if alert_per not in (0, 85):
                daily_allowances.insert(0, (mon_allowance * alert_per) / 100)

        return daily_allowances

    # --- Account Actions ---
    def sign_up(self):
        try:
            while True:
                username = input("Username: ")
                if self.is_taken(username):
                    print(f"FAILED: The username '{username}' is already taken.")
                else:
                    break

            while True:
                password = self.masked_input("Password: ")
                strong, message = self.is_strong(password)
                if strong:
                    break
                print("Weak password:", message)

            while True:
                phone_number = input("Phone number: ")
                valid, message = self.is_phone_number(phone_number)
                if valid:
                    break
                print("Invalid phone:", message)
            
            while True:
                telegram_id = input("Go to @userinfobot in Telegram and start bot\nTelegram ID(1130272106): ")
                valid, message = self.is_telegram_username(telegram_id)
                if valid:
                    break
                print("Invalid phone:", message)

            daily_allowances = self.input_allowance()

            user = User(username, password, phone_number,telegram_id, daily_allowances)
            self.accounts[username] = user
            self.save_accounts()
            print("Account created successfully!")
            print("Connect with our bot in Telegram now!")
            print("@JOMNAY_project_bot")

        except Exception as e:
            raise SignupError(f"Signup failed: {e}")

    def login(self):
        try:
            username = input("Username: ")
            password = self.masked_input("Password: ")
            secure_password = hashlib.sha256(password.encode()).hexdigest()

            if username in self.accounts and self.accounts[username].password == secure_password:
                print("Login Successful!")
                # ✅ Print the last element in allowance list (mon_allowance)
                print(f"Your monthly allowance: {self.accounts[username].allowance[-1]}")
                self.logged_in = True
                self.current_user = username
                return username
            else:
                self.logged_in = False
                self.current_user = None 
                raise LoginError("Incorrect username or password.")
        except LoginError as e:
            print(e)
            return None

class UpdateInfo(AccountManager):
    def update_username(self, old_username, new_username):
        if not self.logged_in or self.current_user != old_username:
            print("You must be logged in as the correct user to update username.")
            
        if old_username in self.accounts:
            user = self.accounts.pop(old_username)
            user.username = new_username
            self.accounts[new_username] = user
            self.save_accounts()
            print("Username updated successfully!")
        else:
            print("User not found.")

    def update_password(self):
        input_username = input("Enter your username: ")
        if not self.logged_in or self.current_user != input_username:
            print("You must be logged in as the correct user to update username.")

        while input_username in self.accounts:
            old_pw = self.masked_input("Enter old password: ")
            old_hash = hashlib.sha256(old_pw.encode()).hexdigest()
        
            if self.accounts[username].password != old_hash:
                print("Old password incorrect!")
                continue
                
            while True:
                new_pw = self.masked_input("Enter new password: ")
                new_hash = hashlib.sha256(new_pw.encode()).hexdigest()

                if new_hash == old_hash:
                    print("New password cannot be the same as old password. Try again.")
                else:
                    strong, message = self.is_strong(new_pw)
                    if not strong:
                        print("Weak password:", message)
                    else:
                        self.accounts[username].password = new_hash
                        self.save_accounts()
                        print("Password updated successfully!")
                        break
        else:
            print("User not found.")

    def forgot_password(self, username):
        if username in self.accounts:
            phone_check = input("Enter your registered phone number: ")
            if phone_check != self.accounts[username].phone_number:
                print("Phone number does not match our records!")
                return

            old_hash = self.accounts[username].password

            while True:
                new_pw = self.masked_input("Enter new password: ")
                new_hash = hashlib.sha256(new_pw.encode()).hexdigest()

                if new_hash == old_hash:
                    print("New password cannot be the same as old password. Try again.")
                else:
                    strong, message = self.is_strong(new_pw)
                    if not strong:
                        print("Weak password:", message)
                    else:
                        self.accounts[username].password = new_hash
                        self.save_accounts()
                        print("Password reset successfully!")
                        break
        else:
            print("User not found.")

    def update_phone(self, new_phone):
        if not self.logged_in:
            return ("You must be logged in to update phone number.")
        username = self.current_user

        if username in self.accounts:
            self.accounts[username].phone_number = new_phone
            self.save_accounts()
            print("Phone number updated successfully!")
        else:
            print("User not found.")

    def update_allowance(self, new_allowance_list):
        if not self.logged_in:
            return("You must be logged in to update allowance.")            
        username = self.current_user

        if username in self.accounts:
            self.accounts[username].allowance = new_allowance_list
            self.save_accounts()
            print("Allowance updated successfully!")
        else:
            print("User not found.")

    def menu(self, username):
        while True:
            print("\n--- Update Info ---")
            print("1. Update Username")
            print("2. Update Password")
            print("3. Update Phone Number")
            print("4. Update Allowance")
            print("5. Logout")

            choice = input("Choose an option: ")

            if choice == "1":
                old_username = input("Enter your current username: ")
                new_username = input("Enter new username: ")
                self.update_username(old_username, new_username)
                username = new_username  # update new username

            elif choice == "2":
                self.update_password()

            elif choice == "3":
                new_phone = input("New phone number: ")
                self.update_phone(new_phone)

            elif choice == "4":
                new_allowance = self.input_allowance()
                self.update_allowance(new_allowance)

            elif choice == "5":
                print("Logged out.")
                break

            else:
                print("Invalid choice.")

# --- Main Program ---
if __name__ == "__main__":
    user = UpdateInfo()
    attempts = 0

    while True:
        have_acc = input("Already have account?(yes/no/forgot): ")

        if have_acc.lower() == "no":
            try:
                user.sign_up()
                attempts = 0
            except SignupError as e:
                print(e)

        elif have_acc.lower() == "yes":
            try:
                username = user.login()
                if not user.logged_in:
                    attempts += 1
                    if attempts >= 3:
                        raise LoginError("Too many failed login attempts!")
                else:
                    user.menu(username)
                    break
            except LoginError as e:
                print(e)
                if attempts >= 3:
                    break

        elif have_acc.lower() == "forgot":
            try:
                username = input("Enter your username: ")
                user.forgot_password(username)
                if not user.logged_in:
                    attempts += 1
                    if attempts >= 3:
                        raise LoginError("Too many failed attempts!")
                else:
                    break
            except LoginError as e:
                print(e)
                if attempts >= 3:
                    break
        else:
            print("Exiting program.")
            break