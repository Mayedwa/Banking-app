import ttkbootstrap as ttkb
from create_account import create_account
from login import login

def main_menu():
    root = ttkb.Window(themename="darkly")
    root.title("Banking App")
    root.iconbitmap('')

    ttkb.Label(
        root,
        text="Welcome to the Banking App",
        font=("Helvetica", 16),
        bootstyle="light"
    ).pack(pady=20)

    ttkb.Button(root, text="Create Account", command=create_account, bootstyle="success").pack(pady=10)
    ttkb.Button(root, text="Login", command=login, bootstyle="info").pack(pady=10)
    ttkb.Button(root, text="Exit", command=root.destroy, bootstyle="danger").pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main_menu()
