import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as ttkb
import random
import json
import os

# File paths for storing data
USER_DATABASE = "users.txt"
TRANSACTION_DATABASE = "transactions.txt"

# Utility functions
def save_data(file, data):
    with open(file, "w") as f:
        json.dump(data, f)

def load_data(file):
    if not os.path.exists(file):
        return {}
    try:
        with open(file, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

# Load user and transaction data
users = load_data(USER_DATABASE)
transactions = load_data(TRANSACTION_DATABASE)

# Record transaction function
def record_transaction(username, transaction_type, amount, recipient_account=None, sender_account=None):
    if username not in transactions:
        transactions[username] = []
    record = {
        "type": transaction_type,
        "amount": amount,
        "balance_after": users[username]["balance"],
    }
    if recipient_account:
        record["to_account"] = recipient_account
    if sender_account:
        record["from_account"] = sender_account

    transactions[username].append(record)
    save_data(TRANSACTION_DATABASE, transactions)

# GUI Functions
def create_account():
    def save_account():
        name = entry_name.get().strip()
        surname = entry_surname.get().strip()
        phone = entry_phone.get().strip()
        id_number = entry_id.get().strip()
        password = entry_password.get().strip()
        username = f"{name.lower()}.{surname.lower()}"
        account_number = random.randint(1000000000, 9999999999)

        if username in users:
            messagebox.showerror("Error", "User already exists!")
            return

        users[username] = {
            "name": name,
            "surname": surname,
            "phone": phone,
            "id_number": id_number,
            "password": password,
            "account_number": account_number,
            "balance": 0.0,
        }
        save_data(USER_DATABASE, users)
        messagebox.showinfo("Success", f"Account created successfully! Your username is '{username}'.")
        create_window.destroy()

    create_window = ttkb.Window(themename="darkly")
    create_window.title("Create Account")
    create_window.iconbitmap('')  # Removes the icon

    ttkb.Label(create_window, text="First Name:", font=("Helvetica", 12)).pack(pady=5)
    entry_name = ttkb.Entry(create_window, bootstyle="info")
    entry_name.pack()

    ttkb.Label(create_window, text="Surname:", font=("Helvetica", 12)).pack(pady=5)
    entry_surname = ttkb.Entry(create_window, bootstyle="info")
    entry_surname.pack()

    ttkb.Label(create_window, text="Phone:", font=("Helvetica", 12)).pack(pady=5)
    entry_phone = ttkb.Entry(create_window, bootstyle="info")
    entry_phone.pack()

    ttkb.Label(create_window, text="ID Number:", font=("Helvetica", 12)).pack(pady=5)
    entry_id = ttkb.Entry(create_window, bootstyle="info")
    entry_id.pack()

    ttkb.Label(create_window, text="Password:", font=("Helvetica", 12)).pack(pady=5)
    entry_password = ttkb.Entry(create_window, show="*", bootstyle="info")
    entry_password.pack()

    ttkb.Button(create_window, text="Create Account", command=save_account, bootstyle="success").pack(pady=10)
    create_window.mainloop()

def login():
    def authenticate():
        username = entry_username.get().strip()
        password = entry_password.get().strip()

        if username in users and users[username]["password"] == password:
            messagebox.showinfo("Success", f"Welcome back, {users[username]['name']}!")
            login_window.destroy()
            dashboard(username)
        else:
            messagebox.showerror("Error", "Invalid username or password. Please try again.")

    login_window = ttkb.Window(themename="darkly")
    login_window.title("Login")
    login_window.iconbitmap('')  # Removes the icon

    ttkb.Label(login_window, text="Username:", font=("Helvetica", 12)).pack(pady=5)
    entry_username = ttkb.Entry(login_window, bootstyle="info")
    entry_username.pack()

    ttkb.Label(login_window, text="Password:", font=("Helvetica", 12)).pack(pady=5)
    entry_password = ttkb.Entry(login_window, show="*", bootstyle="info")
    entry_password.pack()

    ttkb.Button(login_window, text="Login", command=authenticate, bootstyle="success").pack(pady=10)
    login_window.mainloop()

def dashboard(username):
    def view_balance():
        balance_label.config(text=f"Balance: R{users[username]['balance']:.2f}")

    def deposit():
        try:
            amount = float(deposit_entry.get().strip())
            users[username]["balance"] += amount
            record_transaction(username, "Deposit", amount)
            save_data(USER_DATABASE, users)
            view_balance()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount.")

    def transfer():
        recipient = transfer_entry_user.get().strip()
        try:
            amount = float(transfer_entry_amount.get().strip())
            if recipient not in users:
                messagebox.showerror("Error", "Recipient account not found.")
                return
            if amount > users[username]["balance"]:
                messagebox.showerror("Error", "Insufficient funds.")
                return
            users[username]["balance"] -= amount
            users[recipient]["balance"] += amount
            record_transaction(username, "Transfer Out", amount, recipient_account=users[recipient]["account_number"])
            record_transaction(recipient, "Transfer In", amount, sender_account=users[username]["account_number"])
            save_data(USER_DATABASE, users)
            messagebox.showinfo("Success", f"Transferred R{amount:.2f} to {recipient}.")
            view_balance()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount.")

    def show_transactions():
        transactions_window = ttkb.Toplevel()
        transactions_window.title("Transaction History")
        transactions_window.iconbitmap('')  # Removes the icon

        scrollbar = ttkb.Scrollbar(transactions_window)
        scrollbar.pack(side="right", fill="y")

        transaction_list = tk.Listbox(transactions_window, yscrollcommand=scrollbar.set, width=50, height=20)
        transaction_list.pack()

        if username in transactions:
            for record in transactions[username]:
                transaction_list.insert(tk.END, f"{record['type']}: R{record['amount']:.2f}")

        scrollbar.config(command=transaction_list.yview)

    dashboard_window = ttkb.Window(themename="darkly")
    dashboard_window.title("Dashboard")
    dashboard_window.iconbitmap('')  # Removes the icon

    balance_label = ttkb.Label(dashboard_window, text=f"Balance: R{users[username]['balance']:.2f}", font=("Helvetica", 16))
    balance_label.pack(pady=10)

    ttkb.Label(dashboard_window, text="Deposit Amount:", font=("Helvetica", 12)).pack()
    deposit_entry = ttkb.Entry(dashboard_window, bootstyle="info")
    deposit_entry.pack()
    ttkb.Button(dashboard_window, text="Deposit", command=deposit, bootstyle="success").pack(pady=5)

    ttkb.Label(dashboard_window, text="Transfer To:", font=("Helvetica", 12)).pack()
    transfer_entry_user = ttkb.Entry(dashboard_window, bootstyle="info")
    transfer_entry_user.pack()
    ttkb.Label(dashboard_window, text="Transfer Amount:", font=("Helvetica", 12)).pack()
    transfer_entry_amount = ttkb.Entry(dashboard_window, bootstyle="info")
    transfer_entry_amount.pack()
    ttkb.Button(dashboard_window, text="Transfer Funds", command=transfer, bootstyle="warning").pack(pady=5)

    ttkb.Button(dashboard_window, text="View Transactions", command=show_transactions, bootstyle="info").pack(pady=10)

    dashboard_window.mainloop()

# Main Menu
def main_menu():
    root = ttkb.Window(themename="darkly")
    root.title("Banking App")
    root.iconbitmap('')  # Removes the icon

    # Welcome message with white text color
    ttkb.Label(
        root,
        text="Welcome to the Banking App",
        font=("Helvetica", 16),
        bootstyle="light"  # White text style in ttkbootstrap
    ).pack(pady=20)

    ttkb.Button(root, text="Create Account", command=create_account, bootstyle="success").pack(pady=10)
    ttkb.Button(root, text="Login", command=login, bootstyle="info").pack(pady=10)
    ttkb.Button(root, text="Exit", command=root.destroy, bootstyle="danger").pack(pady=10)

    root.mainloop()

# Run the app
if __name__ == "__main__":
    main_menu()
