import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd

def select_csv():
    try:
        file_path = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=(("CSV files", "*.csv"),)
        )

        if not file_path:
            return

        # Convert CSV to DataFrame
        df = pd.read_csv(file_path)

        # Display basic info
        messagebox.showinfo(
            "Success",
            f"CSV loaded successfully!\n\nRows: {df.shape[0]}\nColumns: {df.shape[1]}"
        )

        print(df.head())  # Preview in console

    except Exception as e:
        messagebox.showerror("Error", str(e))

# Tkinter window
root = tk.Tk()
root.title("CSV to DataFrame")
root.geometry("400x200")

btn = tk.Button(root, text="Upload CSV", command=select_csv)
btn.pack(pady=40)

root.mainloop()
 