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
    def __init__(self, username, password, phone_number):
        self.username = username
        self.password = hashlib.sha256(password.encode()).hexdigest()
        self.phone_number = phone_number


class AccountManager:
    def __init__(self, filename="accounts.csv"):
        self.accounts = {}
        self.filename = filename
        self.logged_in = False
        self.load_accounts()

    # --- CSV Persistence ---
    def save_accounts(self):
        try:
            with open(self.filename, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Username", "Password", "Phone"])
                for user in self.accounts.values():
                    writer.writerow([user.username, user.password, user.phone_number])
        except Exception as e:
            raise SignupError(f"Error saving accounts: {e}")

    def load_accounts(self):
        try:
            with open(self.filename, mode="r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    user = User(row["Username"], row["Password"], row["Phone"])
                    # Password already hashed in file
                    user.password = row["Password"]
                    self.accounts[user.username] = user
        except FileNotFoundError:
            # No accounts yet
            pass

    # --- Validation Helpers (Condition Checks) ---
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
            (not re.search(r"[a-zA-Z!@#$%^&*(),.?\":{}|<>]", pn), "Invalid characters"),
        ]
        failed = [msg for check, msg in suffix if not check]
        return (pn[:3] in prefix and not failed, failed)

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

            user = User(username, password, phone_number)
            self.accounts[username] = user
            self.save_accounts()
            print("Account created successfully!")

        except Exception as e:
            raise SignupError(f"Signup failed: {e}")

    def login(self):
        try:
            username = input("Username: ")
            password = self.masked_input("Password: ")
            secure_password = hashlib.sha256(password.encode()).hexdigest()

            if username in self.accounts and self.accounts[username].password == secure_password:
                print("Login Successful!")
                self.logged_in = True
            else:
                self.logged_in = False
                raise LoginError("Incorrect username or password.")
        except LoginError as e:
            print(e)


# --- Main Program ---
if __name__ == "__main__":
    manager = AccountManager()
    attempts = 0

    while True:
        have_acc = input("Already have account?(yes/no): ")
        if have_acc.lower() == "no":
            try:
                manager.sign_up()
                attempts = 0
            except SignupError as e:
                print(e)

        elif have_acc.lower() == "yes":
            try:
                manager.login()
                if not manager.logged_in:
                    attempts += 1
                    if attempts >= 3:
                        raise LoginError("Too many failed login attempts!")
                else:
                    break
            except LoginError as e:
                print(e)
                if attempts >= 3:
                    break

        else:
            break