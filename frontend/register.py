import tkinter as tk
from tkinter import messagebox

from backend.auth import register_user


class RegisterFrame(tk.Frame):

    def __init__(self, parent, app):
        super().__init__(parent, bg="#F3F6FA")
        self.app = app

        tk.Label(
            self,
            text="Create Your Account",
            font=("Arial", 24, "bold"),
            bg="#F3F6FA",
            fg="#183153"
        ).pack(pady=(45, 20))

        card = tk.Frame(self, bg="white", padx=35, pady=30)
        card.pack(padx=30)

        tk.Label(card, text="Full Name", bg="white").pack(anchor="w")
        self.name_entry = self.create_entry(card)

        tk.Label(card, text="Email Address", bg="white").pack(anchor="w")
        self.email_entry = self.create_entry(card)

        tk.Label(card, text="Password", bg="white").pack(anchor="w")
        self.password_entry = self.create_entry(card, show="*")

        tk.Label(card, text="Confirm Password", bg="white").pack(anchor="w")
        self.confirm_entry = self.create_entry(card, show="*")

        tk.Button(
            card,
            text="Register",
            command=self.register,
            bg="#16A34A",
            fg="white",
            font=("Arial", 11, "bold"),
            width=30,
            bd=0,
            cursor="hand2"
        ).pack(pady=(15, 5), ipady=9)

        tk.Button(
            card,
            text="Already have an account? Login",
            command=self.app.show_login,
            bg="white",
            fg="#2563EB",
            bd=0,
            cursor="hand2"
        ).pack(pady=10)

    def create_entry(self, parent, show=None):
        entry = tk.Entry(
            parent,
            width=35,
            font=("Arial", 11),
            bd=1,
            relief="solid",
            show=show
        )
        entry.pack(pady=(5, 12), ipady=7)
        return entry

    def register(self):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get()
        confirm = self.confirm_entry.get()

        if not all([name, email, password, confirm]):
            messagebox.showwarning(
                "Missing Information",
                "Please fill in all fields."
            )
            return

        if password != confirm:
            messagebox.showerror(
                "Password Error",
                "Passwords do not match."
            )
            return

        try:
            success, message = register_user(name, email, password)

            if success:
                messagebox.showinfo("Success", message)
                self.app.show_login()
            else:
                messagebox.showerror("Registration Failed", message)

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"Unable to register:\n{error}"
            )