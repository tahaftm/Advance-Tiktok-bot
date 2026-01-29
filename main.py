import tkinter as tk
from tkinter import filedialog
import pandas as pd
from extract_info import extractAllinfo  # Import your function

def extracting_info():
    sku_value = sku_entry.get().strip()
    extractAllinfo(sku_value)  # sequential


def extracting_info_multiple():
    file_path = filedialog.askopenfilename(
        title="Select Excel File",
        filetypes=[("Excel Files", "*.xlsx *.xls")]
    )
    df = pd.read_excel(file_path)
    for sku in df['sku']:
        extractAllinfo(sku)  # sequential



# ------------------ GUI SETUP ------------------
root = tk.Tk()
root.title("Dropshipping Bot")
root.geometry("500x500")
root.resizable(False, False)

# Background color
root.configure(bg="#f0f2f5")

# ------------------ TITLE LABEL ------------------int(res.split(":")[1])  
title_label = tk.Label(
    root, text="Dropshipping Bot", 
    font=("Helvetica", 18, "bold"), 
    bg="#f0f2f5", fg="#333"
)
title_label.pack(pady=20)

# ------------------ SKU ENTRY ------------------
sku_frame = tk.Frame(root, bg="#f0f2f5")
sku_frame.pack(pady=10)

sku_label = tk.Label(sku_frame, text="Enter SKU:", font=("Helvetica", 12), bg="#f0f2f5")
sku_label.pack(side=tk.LEFT, padx=5)

sku_entry = tk.Entry(sku_frame, font=("Helvetica", 12), width=30)
sku_entry.pack(side=tk.LEFT, padx=5)

# ------------------ STATUS BOX ------------------
status_text = tk.Text(root, height=8, width=55, font=("Helvetica", 10))
status_text.pack(pady=10)
status_text.insert(tk.END, "Status: Waiting for SKU input...\n")
status_text.configure(state="disabled")  # read-only

# ------------------ SUBMIT BUTTON ------------------
submit_btn = tk.Button(
    root, text="Submit", font=("Helvetica", 12, "bold"),  
    bg="#4CAF50", fg="white", width=15, command=extracting_info, activebackground="#4CAF50", activeforeground="white"
)
submit_btn.pack(pady=10)

# ------------------ ITERATIVE BUTTON ------------------
loop_btn = tk.Button(
    root,
    text="Start Loop (10 Products)",
    font=("Helvetica", 12, "bold"),
    bg="#2196F3",
    fg="white",
    width=20,
    command=extracting_info_multiple,
    activebackground="#2196F3",
    activeforeground="white"
)
loop_btn.pack(pady=10)
# ------------------ RUN GUI ------------------ 
root.mainloop()
print("Done runnong")
