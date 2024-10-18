from tkinter import ttk
import tkinter as tk
from excel_info import ExcelInfo
columns = []
def get_data():
    excel_filepath = "TheraSAbDab_SeqStruc_OnlineDownload.xlsx"
    sheet_name = "TheraSAbDab_June24"
    excel_info = ExcelInfo(excel_filepath)
    headings = excel_info.get_row_values(sheet_name, 1)
    rows = []
    for i in range(2, 11):
        sheet_row = excel_info.get_row_values(sheet_name, i)
        rows.append(sheet_row)
    for row in rows:
        print(row) 
        tree.insert("", tk.END, values=row)  

root = tk.Tk()
frm = tk.Frame(root)
frm.pack()
tree = ttk.Treeview(frm, columns=tuple([f"c{i}" for i in range(1,25)]), show='headings')
for i in range(1, 25):
    tree.column(f"#{i}", anchor=tk.CENTER)
    tree.heading(f"#{i}", text=f"col_{i}")
scrollbar = ttk.Scrollbar(frm, orient='horizontal', command=tree.xview)
tree.configure(xscrollcommand=scrollbar.set)
tree.pack()
scrollbar.pack(fill="both", expand=True)
button1 = tk.Button(text="Display data", command=get_data)
button1.pack(pady=10)
root.mainloop()