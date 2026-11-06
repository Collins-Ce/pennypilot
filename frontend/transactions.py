import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, datetime
from tkinter import filedialog

from backend.transaction import (
    get_categories,
    get_transactions,
    add_transaction,
    update_transaction,
    delete_transaction,
    export_transactions_to_csv
)


class TransactionsFrame(tk.Frame):

    def __init__(self, parent, app):
        super().__init__(parent, bg="#F3F6FA")

        self.app = app
        self.user_id = app.current_user["user_id"]
        self.records = {}

        self.create_header()
        self.create_table()
        self.load_transactions()

    def create_header(self):
        header = tk.Frame(self, bg="#183153")
        header.pack(fill="x")

        tk.Label(
            header,
            text="Transactions",
            font=("Arial", 22, "bold"),
            bg="#183153",
            fg="white"
        ).pack(side="left", padx=25, pady=20)

        tk.Button(
            header,
            text="Back to Dashboard",
            command=self.app.show_dashboard,
            bg="#2563EB",
            fg="white",
            bd=0,
            padx=15,
            pady=8
        ).pack(side="right", padx=25)

    def create_table(self):
        controls = tk.Frame(self, bg="#F3F6FA")
        controls.pack(fill="x", padx=25, pady=20)

        tk.Button(
            controls,
            text="+ Add Income",
            command=lambda: self.open_form("INCOME"),
            bg="#16A34A",
            fg="white",
            bd=0,
            padx=15,
            pady=10
        ).pack(side="left", padx=5)

        tk.Button(
            controls,
            text="+ Add Expense",
            command=lambda: self.open_form("EXPENSE"),
            bg="#DC2626",
            fg="white",
            bd=0,
            padx=15,
            pady=10
        ).pack(side="left", padx=5)

        tk.Button(
            controls,
            text="Edit Selected",
            command=self.edit_selected,
            bg="#2563EB",
            fg="white",
            bd=0,
            padx=15,
            pady=10
        ).pack(side="left", padx=5)

        tk.Button(
            controls,
            text="Delete Selected",
            command=self.delete_selected,
            bg="#64748B",
            fg="white",
            bd=0,
            padx=15,
            pady=10
        ).pack(side="left", padx=5)

        tk.Button(
            controls,
            text="Export CSV",
            command=self.export_csv,
            bg="#16A34A",
            fg="white",
            font=("Arial", 10, "bold"),
            bd=0,
            padx=15,
            pady=10,
            cursor="hand2"
        ).pack(side="left", padx=5)

        table_frame = tk.Frame(self, bg="#F3F6FA")
        table_frame.pack(fill="both", expand=True, padx=30, pady=10)

        columns = (
            "date", "type", "category", "amount", "description"
        )

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        headings = {
            "date": "Date",
            "type": "Type",
            "category": "Category",
            "amount": "Amount",
            "description": "Description"
        }

        for column, heading in headings.items():
            self.table.heading(column, text=heading)

        self.table.column("date", width=110)
        self.table.column("type", width=100)
        self.table.column("category", width=140)
        self.table.column("amount", width=130)
        self.table.column("description", width=250)

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.table.yview
        )

        self.table.configure(yscrollcommand=scrollbar.set)

        self.table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.table.tag_configure(
            "INCOME", foreground="#16A34A"
        )
        self.table.tag_configure(
            "EXPENSE", foreground="#DC2626"
        )

    def load_transactions(self):
        try:
            transactions = get_transactions(self.user_id)

            for item in self.table.get_children():
                self.table.delete(item)

            self.records.clear()

            for transaction in transactions:
                transaction_id = transaction["transaction_id"]
                self.records[transaction_id] = transaction

                self.table.insert(
                    "",
                    "end",
                    iid=str(transaction_id),
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
                "Error",
                f"Could not load transactions:\n{error}"
            )

    def open_form(self, transaction_type, existing=None):
        window = tk.Toplevel(self)
        window.title("Edit Transaction" if existing else "Add Transaction")
        window.geometry("420x510")
        window.resizable(False, False)
        window.configure(bg="#F3F6FA")
        window.transient(self)
        window.grab_set()

        tk.Label(
            window,
            text="Edit Transaction" if existing else "New Transaction",
            font=("Arial", 19, "bold"),
            bg="#F3F6FA",
            fg="#183153"
        ).pack(pady=20)

        form = tk.Frame(window, bg="white", padx=25, pady=20)
        form.pack(fill="both", padx=20, pady=5)

        tk.Label(form, text="Transaction Type", bg="white").pack(anchor="w")

        type_var = tk.StringVar(value=transaction_type)

        type_box = ttk.Combobox(
            form,
            textvariable=type_var,
            values=["INCOME", "EXPENSE"],
            state="readonly"
        )
        type_box.pack(fill="x", pady=(5, 12))

        tk.Label(form, text="Category", bg="white").pack(anchor="w")

        category_var = tk.StringVar()
        category_box = ttk.Combobox(
            form,
            textvariable=category_var,
            state="readonly"
        )
        category_box.pack(fill="x", pady=(5, 12))

        categories = []

        def load_categories(event=None):
            nonlocal categories

            try:
                categories = get_categories(type_var.get())
                category_box["values"] = [
                    item["category_name"] for item in categories
                ]

                if existing and type_var.get() == existing["transaction_type"]:
                    category_var.set(existing["category_name"])
                elif category_box["values"]:
                    category_box.current(0)

            except Exception as error:
                messagebox.showerror(
                    "Error", f"Could not load categories:\n{error}"
                )

        type_box.bind("<<ComboboxSelected>>", load_categories)

        tk.Label(form, text="Amount (₹)", bg="white").pack(anchor="w")
        amount_entry = tk.Entry(form)
        amount_entry.pack(fill="x", pady=(5, 12))

        tk.Label(form, text="Date (YYYY-MM-DD)", bg="white").pack(anchor="w")
        date_entry = tk.Entry(form)
        date_entry.pack(fill="x", pady=(5, 12))

        tk.Label(form, text="Description", bg="white").pack(anchor="w")
        description_entry = tk.Entry(form)
        description_entry.pack(fill="x", pady=(5, 12))

        if existing:
            amount_entry.insert(0, str(existing["amount"]))
            date_entry.insert(0, str(existing["transaction_date"]))
            description_entry.insert(
                0, existing["description"] or ""
            )
        else:
            date_entry.insert(0, date.today().isoformat())

        load_categories()

        def save():
            selected_name = category_var.get()

            selected_category = next(
                (
                    item for item in categories
                    if item["category_name"] == selected_name
                ),
                None
            )

            if not selected_category:
                messagebox.showwarning(
                    "Missing Category", "Please select a category."
                )
                return

            try:
                datetime.strptime(date_entry.get().strip(), "%Y-%m-%d")
            except ValueError:
                messagebox.showwarning(
                    "Invalid Date",
                    "Enter the date in YYYY-MM-DD format."
                )
                return

            if not amount_entry.get().strip():
                messagebox.showwarning(
                    "Missing Amount", "Please enter an amount."
                )
                return

            try:
                if existing:
                    success, message = update_transaction(
                        existing["transaction_id"],
                        self.user_id,
                        selected_category["category_id"],
                        type_var.get(),
                        amount_entry.get(),
                        description_entry.get(),
                        date_entry.get().strip()
                    )
                else:
                    success, message = add_transaction(
                        self.user_id,
                        selected_category["category_id"],
                        type_var.get(),
                        amount_entry.get(),
                        description_entry.get(),
                        date_entry.get().strip()
                    )

                if success:
                    messagebox.showinfo("Success", message)
                    window.destroy()
                    self.load_transactions()
                    self.app.show_dashboard()
                else:
                    messagebox.showerror("Error", message)

            except Exception as error:
                messagebox.showerror(
                    "Database Error", str(error)
                )

        tk.Button(
            form,
            text="Save Transaction",
            command=save,
            bg="#2563EB",
            fg="white",
            bd=0,
            pady=10
        ).pack(fill="x", pady=(10, 0))

    def edit_selected(self):
        selected = self.table.selection()

        if not selected:
            messagebox.showwarning(
                "Select Transaction",
                "Please select a transaction to edit."
            )
            return

        transaction_id = int(selected[0])
        transaction = self.records[transaction_id]

        self.open_form(
            transaction["transaction_type"],
            transaction
        )

    def delete_selected(self):
        selected = self.table.selection()

        if not selected:
            messagebox.showwarning(
                "Select Transaction",
                "Please select a transaction to delete."
            )
            return

        transaction_id = int(selected[0])

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this transaction?"
        )

        if not confirm:
            return

        try:
            success, message = delete_transaction(
                transaction_id, self.user_id
            )

            if success:
                messagebox.showinfo("Success", message)
                self.load_transactions()
                self.app.show_dashboard()
            else:
                messagebox.showerror("Error", message)

        except Exception as error:
            messagebox.showerror(
                "Database Error", str(error)
            )

    def export_csv(self):
        user_id = self.app.current_user["user_id"]

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")],
            initialfile="PennyPilot_Transactions.csv"
        )

        if not file_path:
            return

        try:
            success, count = export_transactions_to_csv(
                user_id, file_path
            )

            if success:
                messagebox.showinfo(
                    "Export Successful",
                    f"{count} transactions exported successfully!\n\n"
                    f"Saved to:\n{file_path}"
                )

        except Exception as e:
            messagebox.showerror(
                "Export Failed",
                f"Could not export transactions:\n{e}"
            )