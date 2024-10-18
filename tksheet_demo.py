import tkinter as tk
from tkinter import N, S, E, W
import tksheet
import pandas

# Source: https://github.com/ragardner/tksheet/issues/78

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.sheet = tksheet.Sheet(self, width=800, height=500)
        
        self.sheet.enable_bindings(("all"))
        self.sheet.grid(row=0, column=0, sticky=N+S+E+W)
        self.sheet.grid_columnconfigure(1, weight=3)
        self.sheet.grid_rowconfigure(1, weight=3)

        self.columnconfigure(0, weight=3)
        self.rowconfigure(0, weight=3)


    def load_file(self, filename):
        """Loads the file into application by placing it into spreadsheet."""

        if not filename.lower().endswith(".csv"):
            self.df = pandas.read_excel(filename, engine='openpyxl')
        else:
            self.df = pandas.read_csv(filename)

        df_rows = self.df.to_numpy().tolist()  
        self.sheet.headers(self.df.columns.tolist())
        self.sheet.set_sheet_data(df_rows)


if __name__ == "__main__":
    app = Application()
    app.load_file('sample.csv')
    app.mainloop()