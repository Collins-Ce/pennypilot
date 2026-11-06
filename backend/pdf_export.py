from io import BytesIO
from datetime import date
from calendar import month_name

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    KeepTogether
)

from matplotlib.figure import Figure

from backend.analytics import (
    get_monthly_summary,
    get_expense_breakdown
)


def generate_monthly_pdf(user_id, year, month, file_path):
    summary = get_monthly_summary(user_id, year, month)
    breakdown = get_expense_breakdown(user_id, year, month)

    document = SimpleDocTemplate(
        file_path,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "PennyPilotTitle",
        parent=styles["Title"],
        textColor=colors.HexColor("#183153"),
        fontSize=22,
        spaceAfter=8
    )

    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        textColor=colors.HexColor("#64748B"),
        fontSize=11,
        alignment=1,
        spaceAfter=20
    )

    story = []

    # Report heading
    story.append(Paragraph("PennyPilot", title_style))
    story.append(
        Paragraph(
            f"Financial Report - {month_name[month]} {year}",
            subtitle_style
        )
    )

    # Monthly summary table
    summary_data = [
        ["Financial Summary", "Amount"],
        ["Total Income", f"Rs. {summary['total_income']:,.2f}"],
        ["Total Expenses", f"Rs. {summary['total_expenses']:,.2f}"],
        ["Net Balance", f"Rs. {summary['balance']:,.2f}"]
    ]

    summary_table = Table(
        summary_data,
        colWidths=[3.5 * inch, 2.5 * inch]
    )

    summary_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#183153")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#F3F6FA")),
        ("TEXTCOLOR", (0, 1), (-1, -1), colors.HexColor("#183153")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("ALIGN", (1, 1), (1, -1), "RIGHT"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ("PADDING", (0, 0), (-1, -1), 9)
    ]))

    story.append(summary_table)
    story.append(Spacer(1, 25))

    # Expense category table
    story.append(
        Paragraph("Expense Breakdown", styles["Heading2"])
    )
    story.append(Spacer(1, 8))

    expense_data = [["Category", "Amount"]]

    for item in breakdown:
        expense_data.append([
            item["category_name"],
            f"Rs. {item['total']:,.2f}"
        ])

    if not breakdown:
        expense_data.append(["No expenses recorded", "Rs. 0.00"])

    expense_table = Table(
        expense_data,
        colWidths=[3.5 * inch, 2.5 * inch],
        repeatRows=1
    )

    expense_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2563EB")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#F8FAFC")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ("ALIGN", (1, 1), (1, -1), "RIGHT"),
        ("PADDING", (0, 0), (-1, -1), 8),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold")
    ]))

    story.append(expense_table)
    story.append(Spacer(1, 25))

    # Income vs expense chart
    story.append(
        Paragraph("Income vs Expenses", styles["Heading2"])
    )
    story.append(Spacer(1, 8))

    chart = Figure(figsize=(6, 2.8), dpi=100)
    axis = chart.add_subplot(111)

    labels = ["Income", "Expenses"]
    values = [
        float(summary["total_income"]),
        float(summary["total_expenses"])
    ]

    axis.bar(labels, values)
    axis.set_ylabel("Amount (Rs.)")
    axis.set_title(f"{month_name[month]} {year}")
    axis.grid(axis="y", alpha=0.25)

    chart_buffer = BytesIO()
    chart.tight_layout()
    chart.savefig(chart_buffer, format="png", dpi=150)
    chart_buffer.seek(0)

    story.append(
        Image(chart_buffer, width=6 * inch, height=2.8 * inch)
    )

    document.build(story)
    chart_buffer.close()

    return True