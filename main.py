import tkinter as tk

from frontend.login import LoginFrame
from frontend.register import RegisterFrame


class PennyPilotApp:

    def __init__(self, root):
        self.root = root
        self.root.title("PennyPilot - Personal Finance Tracker")
        self.root.geometry("900x650")
        self.root.minsize(750, 550)
        self.root.configure(bg="#F3F6FA")

        self.current_user = None
        self.current_frame = None

        self.show_login()

    def clear_screen(self):
        if self.current_frame:
            self.current_frame.destroy()

    def show_login(self):
        self.clear_screen()
        self.current_frame = LoginFrame(self.root, self)
        self.current_frame.pack(fill="both", expand=True)

    def show_register(self):
        self.clear_screen()
        self.current_frame = RegisterFrame(self.root, self)
        self.current_frame.pack(fill="both", expand=True)

    def show_dashboard(self):
        self.clear_screen()

        # Temporary dashboard placeholder.
        self.current_frame = tk.Frame(
            self.root, bg="#F3F6FA"
        )
        self.current_frame.pack(fill="both", expand=True)

        tk.Label(
            self.current_frame,
            text=f"Welcome, {self.current_user['name']}!",
            font=("Arial", 25, "bold"),
            bg="#F3F6FA",
            fg="#183153"
        ).pack(pady=100)

        tk.Label(
            self.current_frame,
            text="Your PennyPilot dashboard is coming next.",
            font=("Arial", 13),
            bg="#F3F6FA",
            fg="#64748B"
        ).pack()

        tk.Button(
            self.current_frame,
            text="Logout",
            command=self.logout,
            bg="#DC2626",
            fg="white",
            bd=0,
            padx=25,
            pady=10
        ).pack(pady=25)

    def logout(self):
        self.current_user = None
        self.show_login()


if __name__ == "__main__":
    root = tk.Tk()
    app = PennyPilotApp(root)
    root.mainloop()