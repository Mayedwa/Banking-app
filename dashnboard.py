import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttkb
from utils import save_data, load_data, TRANSACTION_DATABASE, users, transactions
from transaction_utils import record_transaction

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
        transactions_window.iconbitmap('')

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
    dashboard_window.iconbitmap('')

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
