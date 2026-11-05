import tkinter as tk
from tkinter import messagebox

from backend.auth import login_user


class LoginFrame(tk.Frame):

    def __init__(self, parent, app):
        super().__init__(parent, bg="#F3F6FA")
        self.app = app

        tk.Label(
            self,
            text="PennyPilot",
            font=("Arial", 28, "bold"),
            bg="#F3F6FA",
            fg="#183153"
        ).pack(pady=(60, 5))

        tk.Label(
            self,
            text="Navigate your money. Own your future.",
            font=("Arial", 11),
            bg="#F3F6FA",
            fg="#64748B"
        ).pack(pady=(0, 25))

        card = tk.Frame(self, bg="white", padx=35, pady=30)
        card.pack(padx=30)

        tk.Label(
            card,
            text="Welcome Back",
            font=("Arial", 20, "bold"),
            bg="white",
            fg="#183153"
        ).pack(pady=(0, 20))

        tk.Label(card, text="Email", bg="white").pack(anchor="w")
        self.email_entry = tk.Entry(
            card, width=35, font=("Arial", 11), bd=1, relief="solid"
        )
        self.email_entry.pack(pady=(5, 15), ipady=7)

        tk.Label(card, text="Password", bg="white").pack(anchor="w")
        self.password_entry = tk.Entry(
            card, width=35, font=("Arial", 11),
            bd=1, relief="solid", show="*"
        )
        self.password_entry.pack(pady=(5, 20), ipady=7)

        tk.Button(
            card,
            text="Login",
            command=self.login,
            bg="#2563EB",
            fg="white",
            font=("Arial", 11, "bold"),
            width=30,
            bd=0,
            cursor="hand2"
        ).pack(ipady=9)

        tk.Button(
            card,
            text="Create a new account",
            command=self.app.show_register,
            bg="white",
            fg="#2563EB",
            font=("Arial", 10),
            bd=0,
            cursor="hand2"
        ).pack(pady=(18, 0))

    def login(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get()

        if not email or not password:
            messagebox.showwarning(
                "Missing Information",
                "Please enter your email and password."
            )
            return

        try:
            user = login_user(email, password)

            if user:
                messagebox.showinfo(
                    "Login Successful",
                    f"Welcome, {user['name']}!"
                )
                self.app.current_user = user
                self.app.show_dashboard()
            else:
                messagebox.showerror(
                    "Login Failed",
                    "Invalid email or password."
                )

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"Unable to log in:\n{error}"
            )