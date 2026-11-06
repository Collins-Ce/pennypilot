from tkinter import Tk, filedialog
from backend.pdf_export import generate_monthly_pdf

user_id = int(input("Enter your user ID: "))
year = int(input("Enter report year (e.g. 2026): "))
month = int(input("Enter report month (1-12): "))

root = Tk()
root.withdraw()

file_path = filedialog.asksaveasfilename(
    defaultextension=".pdf",
    filetypes=[("PDF Files", "*.pdf")],
    initialfile="PennyPilot_Financial_Report.pdf"
)

root.destroy()

if file_path:
    try:
        generate_monthly_pdf(user_id, year, month, file_path)
        print("PDF generated successfully!")
        print("Saved to:", file_path)
    except Exception as error:
        print("PDF generation failed:", error)
else:
    print("Export cancelled.")