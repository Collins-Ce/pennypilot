import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import date

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from backend.pdf_export import generate_monthly_pdf

from backend.analytics import (
    get_monthly_summary,
    get_expense_breakdown,
    get_monthly_trends
)


class ReportsFrame(tk.Frame):

    def __init__(self, parent, app):
        super().__init__(parent, bg="#F3F6FA")

        self.app = app
        self.user_id = app.current_user["user_id"]

        today = date.today()

        self.month_names = [
            "January", "February", "March", "April",
            "May", "June", "July", "August",
            "September", "October", "November", "December"
        ]

        self.month_var = tk.StringVar(
            value=self.month_names[today.month - 1]
        )

        self.year_var = tk.StringVar(value=str(today.year))

        self.create_header()
        self.create_filters()
        self.create_summary()
        self.create_charts()

        self.load_reports()


    def create_header(self):

        header = tk.Frame(self, bg="#183153")
        header.pack(fill="x")

        tk.Label(
            header,
            text="Financial Reports",
            font=("Arial", 22, "bold"),
            bg="#183153",
            fg="white"
        ).pack(side="left", padx=25, pady=20)

        tk.Button(
            header,
            text="Dashboard",
            command=self.app.show_dashboard,
            bg="#2563EB",
            fg="white",
            bd=0,
            padx=15,
            pady=8,
            cursor="hand2"
        ).pack(side="right", padx=25)


    def create_filters(self):

        frame = tk.Frame(self, bg="#F3F6FA")
        frame.pack(fill="x", padx=25, pady=15)

        tk.Label(
            frame,
            text="Month:",
            bg="#F3F6FA",
            font=("Arial", 11)
        ).pack(side="left", padx=(0, 5))

        self.month_box = ttk.Combobox(
            frame,
            textvariable=self.month_var,
            values=self.month_names,
            state="readonly",
            width=15
        )

        self.month_box.pack(side="left", padx=5)

        tk.Label(
            frame,
            text="Year:",
            bg="#F3F6FA",
            font=("Arial", 11)
        ).pack(side="left", padx=(15, 5))

        years = [
            str(year)
            for year in range(
                date.today().year - 10,
                date.today().year + 2
            )
        ]

        self.year_box = ttk.Combobox(
            frame,
            textvariable=self.year_var,
            values=years,
            state="readonly",
            width=8
        )

        self.year_box.pack(side="left", padx=5)

        tk.Button(
            frame,
            text="Generate Report",
            command=self.load_reports,
            bg="#2563EB",
            fg="white",
            bd=0,
            padx=15,
            pady=8,
            cursor="hand2"
        ).pack(side="left", padx=15)

        tk.Button(
            frame,
            text="Download PDF",
            command=self.export_pdf,
            bg="#16A34A",
            fg="white",
            bd=0,
            padx=15,
            pady=8,
            cursor="hand2"
        ).pack(side="left", padx=5)


    def create_summary(self):

        frame = tk.Frame(self, bg="#F3F6FA")
        frame.pack(fill="x", padx=20, pady=5)

        self.income_label = self.create_summary_card(
            frame,
            "Monthly Income",
            "#16A34A"
        )

        self.expense_label = self.create_summary_card(
            frame,
            "Monthly Expenses",
            "#DC2626"
        )

        self.balance_label = self.create_summary_card(
            frame,
            "Monthly Balance",
            "#183153"
        )

    def create_summary_card(self, parent, title, color):

        card = tk.Frame(
            parent,
            bg="white",
            padx=15,
            pady=15,
            highlightbackground="#E2E8F0",
            highlightthickness=1
        )

        card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=7
        )

        tk.Label(
            card,
            text=title,
            bg="white",
            fg="#64748B",
            font=("Arial", 10)
        ).pack(anchor="w")

        label = tk.Label(
            card,
            text="₹0.00",
            bg="white",
            fg=color,
            font=("Arial", 18, "bold")
        )

        label.pack(anchor="w", pady=(8, 0))

        return label


    def create_charts(self):

        self.charts_frame = tk.Frame(
            self,
            bg="#F3F6FA"
        )

        self.charts_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        # Income vs Expenses chart

        self.bar_figure = Figure(
            figsize=(5, 2.5),
            dpi=100,
            constrained_layout=True
        )

        self.bar_axes = self.bar_figure.add_subplot(111)

        # Expense Breakdown chart

        self.pie_figure = Figure(
            figsize=(5.5, 2.5),
            dpi=100,
            constrained_layout=True
        )

        self.pie_axes = self.pie_figure.add_subplot(111)

        # Monthly Trends chart

        self.trend_figure = Figure(
            figsize=(10, 2.8),
            dpi=100,
            constrained_layout=True
        )

        self.trend_axes = self.trend_figure.add_subplot(111)

        # Create canvases

        self.bar_canvas = FigureCanvasTkAgg(
            self.bar_figure,
            master=self.charts_frame
        )

        self.pie_canvas = FigureCanvasTkAgg(
            self.pie_figure,
            master=self.charts_frame
        )

        self.trend_canvas = FigureCanvasTkAgg(
            self.trend_figure,
            master=self.charts_frame
        )

        # Place charts

        self.bar_canvas.get_tk_widget().grid(
            row=0,
            column=0,
            padx=5,
            pady=5,
            sticky="nsew"
        )

        self.pie_canvas.get_tk_widget().grid(
            row=0,
            column=1,
            padx=5,
            pady=5,
            sticky="nsew"
        )

        self.trend_canvas.get_tk_widget().grid(
            row=1,
            column=0,
            columnspan=2,
            padx=5,
            pady=10,
            sticky="nsew"
        )

        self.charts_frame.grid_columnconfigure(0, weight=1)
        self.charts_frame.grid_columnconfigure(1, weight=1)

        self.charts_frame.grid_rowconfigure(0, weight=1)
        self.charts_frame.grid_rowconfigure(1, weight=1)


    def load_reports(self):

        try:

            month = self.month_names.index(
                self.month_var.get()
            ) + 1

            year = int(self.year_var.get())

            summary = get_monthly_summary(
                self.user_id,
                year,
                month
            )

            expenses = get_expense_breakdown(
                self.user_id,
                year,
                month
            )

            trends = get_monthly_trends(
                self.user_id,
                6
            )

            income = summary["total_income"]
            expense = summary["total_expenses"]
            balance = summary["balance"]

            self.income_label.config(
                text=f"₹{income:,.2f}"
            )

            self.expense_label.config(
                text=f"₹{expense:,.2f}"
            )

            self.balance_label.config(
                text=f"₹{balance:,.2f}"
            )

            self.draw_bar_chart(income, expense)
            self.draw_pie_chart(expenses)
            self.draw_trend_chart(trends)

        except Exception as error:

            messagebox.showerror(
                "Report Error",
                f"Could not generate report:\n{error}"
            )


    def draw_bar_chart(self, income, expenses):

        self.bar_axes.clear()

        self.bar_axes.bar(
            ["Income", "Expenses"],
            [float(income), float(expenses)],
            color=["#16A34A", "#DC2626"],
            width=0.7
        )

        self.bar_axes.set_title(
            "Income vs Expenses",
            fontsize=13,
            fontweight="bold"
        )

        self.bar_axes.set_ylabel("Amount (₹)")

        self.bar_axes.grid(
            axis="y",
            alpha=0.2
        )

        self.bar_canvas.draw()


    def draw_pie_chart(self, expenses):

        self.pie_axes.clear()

        if expenses:

            labels = [
                item["category_name"]
                for item in expenses
            ]

            values = [
                float(item["total"])
                for item in expenses
            ]

            wedges, texts, autotexts = self.pie_axes.pie(
                values,
                labels=None,
                autopct="%1.1f%%",
                startangle=90,
                pctdistance=0.75,
                wedgeprops={
                    "width": 0.45,
                    "edgecolor": "white",
                    "linewidth": 1.5
                },
                textprops={
                    "fontsize": 8,
                    "fontweight": "bold"
                }
            )

            # Category names in a separate legend

            self.pie_axes.legend(
                wedges,
                labels,
                title="Categories",
                loc="center left",
                bbox_to_anchor=(1.0, 0.5),
                fontsize=8,
                title_fontsize=9
            )

            self.pie_axes.set_title(
                "Expense Breakdown",
                fontsize=13,
                fontweight="bold"
            )

            self.pie_axes.set_aspect("equal")

        else:

            self.pie_axes.text(
                0.5,
                0.5,
                "No expenses recorded",
                ha="center",
                va="center",
                fontsize=11
            )

            self.pie_axes.set_title(
                "Expense Breakdown",
                fontsize=13,
                fontweight="bold"
            )

        self.pie_canvas.draw()


    def draw_trend_chart(self, trends):

        self.trend_axes.clear()

        if trends:

            months = []
            income = []
            expenses = []

            for item in trends:

                month_value = str(item["month"])

                try:

                    month_number = int(
                        month_value.split("-")[-1]
                    )

                    month_label = date(
                        2000,
                        month_number,
                        1
                    ).strftime("%b")

                except (ValueError, TypeError):

                    month_label = month_value

                months.append(month_label)

                income.append(
                    float(item["income"])
                )

                expenses.append(
                    float(item["expenses"])
                )

            positions = list(range(len(months)))

            self.trend_axes.plot(
                positions,
                income,
                marker="o",
                linewidth=2,
                markersize=7,
                label="Income"
            )

            self.trend_axes.plot(
                positions,
                expenses,
                marker="o",
                linewidth=2,
                markersize=7,
                label="Expenses"
            )

            self.trend_axes.set_xticks(positions)

            self.trend_axes.set_xticklabels(
                months,
                rotation=0
            )

            self.trend_axes.legend(
                loc="best"
            )

            self.trend_axes.set_ylim(bottom=0)

            self.trend_axes.grid(
                axis="y",
                alpha=0.2
            )

        else:

            self.trend_axes.text(
                0.5,
                0.5,
                "No transaction history available",
                ha="center",
                va="center"
            )

        self.trend_axes.set_title(
            "Monthly Income & Expense Trends",
            fontsize=13,
            fontweight="bold"
        )

        self.trend_axes.set_ylabel(
            "Amount (₹)"
        )

        self.trend_canvas.draw()


    def export_pdf(self):

        try:

            month = self.month_names.index(
                self.month_var.get()
            ) + 1

            year = int(self.year_var.get())

            file_path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[
                    ("PDF Files", "*.pdf")
                ],
                initialfile=(
                    f"PennyPilot_Report_{year}_{month:02d}.pdf"
                )
            )

            if not file_path:
                return

            generate_monthly_pdf(
                self.user_id,
                year,
                month,
                file_path
            )

            messagebox.showinfo(
                "Export Successful",
                f"Financial report downloaded successfully!\n\n"
                f"Saved to:\n{file_path}"
            )

        except Exception as error:

            messagebox.showerror(
                "PDF Export Failed",
                f"Could not generate PDF:\n{error}"
            )