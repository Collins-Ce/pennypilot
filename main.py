import tkinter as tk

from frontend.login import LoginFrame
from frontend.register import RegisterFrame
from frontend.dashboard import DashboardFrame
from frontend.transactions import TransactionsFrame


class PennyPilotApp:

    def __init__(self, root):
        self.root = root
        self.root.title("PennyPilot - Personal Finance Tracker")
        self.root.geometry("1100x700")
        self.root.minsize(850, 600)
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
        self.current_frame = DashboardFrame(self.root, self)
        self.current_frame.pack(fill="both", expand=True)

    
    def show_transactions(self):
        self.clear_screen()
        self.current_frame = TransactionsFrame(self.root, self)
        self.current_frame.pack(fill="both", expand=True)


    def logout(self):
        self.current_user = None
        self.show_login()


if __name__ == "__main__":
    root = tk.Tk()
    app = PennyPilotApp(root)
    root.mainloop()