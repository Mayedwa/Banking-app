import random
import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttkb
from utils import save_data, load_data, USER_DATABASE, users

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
    create_window.iconbitmap('')

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
