import tkinter as tk
from tkinter import N, S, E, W
import tksheet
import pandas

# Source: https://github.com/ragardner/tksheet/issues/78

class TableViewer(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.frm_table = tk.Frame(self)
        self.frm_table.pack()
        self.table = tksheet.Sheet(self.frm_table, width=800, height=500)
        
        self.table.enable_bindings(("all"))
        self.table.grid(row=0, column=0, sticky=N+S+E+W)
        self.table.grid_columnconfigure(1, weight=3)
        self.table.grid_rowconfigure(1, weight=3)

        self.frm_table.columnconfigure(0, weight=3)
        self.frm_table.rowconfigure(0, weight=3)


    def load_file(self, filename):
        """Loads the file into application by placing it into spreadsheet."""

        if not filename.lower().endswith(".csv"):
            self.df = pandas.read_excel(filename, engine='openpyxl')
        else:
            self.df = pandas.read_csv(filename)

        df_rows = self.df.to_numpy().tolist()
        print(df_rows) 
        self.table.headers(self.df.columns.tolist())
        self.table.set_sheet_data(df_rows)



root = tk.Tk()
tv = TableViewer(root)
tv.pack()
tv.load_file('sample.csv')
root.mainloop()