from tkinter import Tk, filedialog
from backend.transaction import export_transactions_to_csv

user_id = int(input("Enter your user ID: "))

root = Tk()
root.withdraw()

file_path = filedialog.asksaveasfilename(
    defaultextension=".csv",
    filetypes=[("CSV Files", "*.csv")],
    initialfile="PennyPilot_Transactions.csv"
)

root.destroy()

if file_path:
    success, count = export_transactions_to_csv(user_id, file_path)

    if success:
        print(f"Export successful! {count} transactions exported.")
        print("Saved to:", file_path)
else:
    print("Export cancelled.")