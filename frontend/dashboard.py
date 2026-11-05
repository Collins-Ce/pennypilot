import tkinter as tk
from tkinter import ttk, messagebox

from backend.analytics import get_dashboard_data


class DashboardFrame(tk.Frame):

    def __init__(self, parent, app):
        super().__init__(parent, bg="#F3F6FA")

        self.app = app
        self.user = app.current_user

        self.create_header()
        self.create_summary_cards()
        self.create_transactions_table()

        self.load_dashboard()

    def create_header(self):
        header = tk.Frame(self, bg="#183153", height=85)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="PennyPilot",
            font=("Arial", 23, "bold"),
            bg="#183153",
            fg="white"
        ).pack(side="left", padx=25)

        tk.Label(
            header,
            text=f"Welcome, {self.user['name']}",
            font=("Arial", 12),
            bg="#183153",
            fg="white"
        ).pack(side="left", padx=20)

        tk.Button(
            header,
            text="Reports",
            command=self.app.show_reports,
            bg="#7C3AED",
            fg="white",
            font=("Arial", 10, "bold"),
            bd=0,
            padx=15,
            pady=8,
            cursor="hand2"
        ).pack(side="right", padx=10)
        
        tk.Button(
            header,
            text="Manage Transactions",
            command=self.app.show_transactions,
            bg="#16A34A",
            fg="white",
            font=("Arial", 10, "bold"),
            bd=0,
            padx=15,
            pady=8,
            cursor="hand2"
        ).pack(side="right", padx=10)


        tk.Button(
            header,
            text="Logout",
            command=self.app.logout,
            bg="#DC2626",
            fg="white",
            font=("Arial", 10, "bold"),
            bd=0,
            padx=18,
            pady=8,
            cursor="hand2"
        ).pack(side="right", padx=25)

    def create_summary_cards(self):
        title = tk.Label(
            self,
            text="Financial Overview",
            font=("Arial", 21, "bold"),
            bg="#F3F6FA",
            fg="#183153"
        )
        title.pack(anchor="w", padx=30, pady=(25, 15))

        cards_frame = tk.Frame(self, bg="#F3F6FA")
        cards_frame.pack(fill="x", padx=20)

        self.balance_label = self.create_card(
            cards_frame, "Total Balance", "#183153"
        )

        self.income_label = self.create_card(
            cards_frame, "Total Income", "#16A34A"
        )

        self.expense_label = self.create_card(
            cards_frame, "Total Expenses", "#DC2626"
        )

    def create_card(self, parent, title, color):
        card = tk.Frame(
            parent,
            bg="white",
            padx=18,
            pady=20,
            highlightbackground="#E2E8F0",
            highlightthickness=1
        )

        card.pack(side="left", fill="both", expand=True, padx=8)

        tk.Label(
            card,
            text=title,
            font=("Arial", 11),
            bg="white",
            fg="#64748B"
        ).pack(anchor="w")

        value_label = tk.Label(
            card,
            text="₹0.00",
            font=("Arial", 20, "bold"),
            bg="white",
            fg=color
        )
        value_label.pack(anchor="w", pady=(12, 0))

        return value_label

    def create_transactions_table(self):
        section = tk.Frame(self, bg="#F3F6FA")
        section.pack(fill="both", expand=True, padx=30, pady=25)

        top = tk.Frame(section, bg="#F3F6FA")
        top.pack(fill="x", pady=(0, 12))

        tk.Label(
            top,
            text="Recent Transactions",
            font=("Arial", 17, "bold"),
            bg="#F3F6FA",
            fg="#183153"
        ).pack(side="left")

        tk.Button(
            top,
            text="Refresh",
            command=self.load_dashboard,
            bg="#2563EB",
            fg="white",
            bd=0,
            padx=15,
            pady=7,
            cursor="hand2"
        ).pack(side="right")

        columns = (
            "date",
            "type",
            "category",
            "amount",
            "description"
        )

        self.transaction_table = ttk.Treeview(
            section,
            columns=columns,
            show="headings",
            height=8
        )

        headings = {
            "date": "Date",
            "type": "Type",
            "category": "Category",
            "amount": "Amount",
            "description": "Description"
        }

        for column, heading in headings.items():
            self.transaction_table.heading(
                column, text=heading
            )

        self.transaction_table.column("date", width=110)
        self.transaction_table.column("type", width=100)
        self.transaction_table.column("category", width=130)
        self.transaction_table.column("amount", width=120)
        self.transaction_table.column("description", width=250)

        self.transaction_table.pack(
            fill="both", expand=True
        )

        self.transaction_table.tag_configure(
            "INCOME", foreground="#16A34A"
        )

        self.transaction_table.tag_configure(
            "EXPENSE", foreground="#DC2626"
        )

    def load_dashboard(self):
        try:
            data = get_dashboard_data(self.user["user_id"])

            self.balance_label.config(
                text=f"₹{data['balance']:,.2f}"
            )

            self.income_label.config(
                text=f"₹{data['total_income']:,.2f}"
            )

            self.expense_label.config(
                text=f"₹{data['total_expenses']:,.2f}"
            )

            # Clear old table entries.
            for item in self.transaction_table.get_children():
                self.transaction_table.delete(item)

            # Insert the latest transactions.
            for transaction in data["recent_transactions"]:
                self.transaction_table.insert(
                    "",
                    "end",
                    values=(
                        transaction["transaction_date"],
                        transaction["transaction_type"],
                        transaction["category_name"],
                        f"₹{transaction['amount']:,.2f}",
                        transaction["description"] or ""
                    ),
                    tags=(transaction["transaction_type"],)
                )

        except Exception as error:
            messagebox.showerror(
                "Dashboard Error",
                f"Could not load dashboard:\n{error}"
            )