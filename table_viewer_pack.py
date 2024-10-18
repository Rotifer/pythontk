from tkinter import ttk
import tkinter as tk
from excel_info import ExcelInfo

# https://stackoverflow.com/questions/19646752/python-scrollbar-on-text-widget
# https://stackoverflow.com/questions/53339791/tkinter-resize-window-without-scrollbar-disappearing
"""Display tabular data in a tree viewer

The column names are supplied as a list and the data as a list of lists.

column_names = ["Name", "Address", "Age"]
data_rows = [["Joe", "Main Street", 34],
             ["Mary", "Somewhere", 56],
             ["Fred", "Village Green", 87]]


root = tk.Tk()
tv = TableViewer(root, column_names, data_rows)
tv.pack()
root.mainloop()
"""

class TableViewer(tk.Frame):
    def __init__(self, parent, column_names, data_rows, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = parent
        self.column_names = column_names
        self.data_rows = data_rows
        self.frm_table = tk.Frame(self)
        self.column_count = len(self.column_names)
        self.build_table()

    def build_table(self):
        """Create and populate the data table.
        """
        self.frm_table.pack()
        columns = tuple([f"c{i}" for i in range(1, self.column_count + 1)])
        self.table = ttk.Treeview(self.frm_table, 
                             columns=columns, 
                             show='headings')
        scr_x = ttk.Scrollbar(self.frm_table,
                              orient="horizontal",
                              command=self.table.xview)
        self.table.configure(xscrollcommand=scr_x.set)
        scr_y = ttk.Scrollbar(self.frm_table,
                              orient="vertical",
                              command=self.table.yview)
        self.table.configure(yscrollcommand=scr_y.set)
        scr_y.pack(side="right", fill="y")
        scr_x.pack(side="bottom", fill="x")
        self.table.pack(side="left", expand=True, fill="both")        
        self.populate_table()

    def populate_table(self):
        for i in range(1, self.column_count + 1):
            self.table.column(f"#{i}", anchor=tk.CENTER)
            self.table.heading(f"#{i}", text=f"{self.column_names[i-1]}")
        for data_row in self.data_rows:
            self.table.insert("", tk.END, values=data_row)


def get_data():
    excel_filepath = "simple_grid.xlsx"
    sheet_name = "Sheet1"
    excel_info = ExcelInfo(excel_filepath)
    headings = excel_info.get_row_values(sheet_name, 1)
    rows = []
    for i in range(2, 11):
        sheet_row = excel_info.get_row_values(sheet_name, i)
        rows.append(sheet_row)
    return headings, rows

column_names, data_rows = get_data()
root = tk.Tk()
root.geometry("1000x500")
tv = TableViewer(root, column_names, data_rows)
tv.pack()
root.mainloop()