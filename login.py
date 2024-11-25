import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttkb
from utils import load_data, USER_DATABASE, users
from dashboard import dashboard

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
    login_window.iconbitmap('')

    ttkb.Label(login_window, text="Username:", font=("Helvetica", 12)).pack(pady=5)
    entry_username = ttkb.Entry(login_window, bootstyle="info")
    entry_username.pack()

    ttkb.Label(login_window, text="Password:", font=("Helvetica", 12)).pack(pady=5)
    entry_password = ttkb.Entry(login_window, show="*", bootstyle="info")
    entry_password.pack()

    ttkb.Button(login_window, text="Login", command=authenticate, bootstyle="success").pack(pady=10)
    login_window.mainloop()
