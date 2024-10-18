import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from excel_info import ExcelInfo

"""Basic working class to open Excel files, list the sheets and view samples 
of data from the sheets.
Needs more work!
"""
class ExcelBrowser(tk.Frame):
    btn_color = "#080808"
    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = parent
        self.excel_info = None
        self.lbl_excel_filepath = None
        self.frm_excel =  ttk.Frame(self, 
                                    width=600)
        self.frm_excel.pack(padx=10, 
                            pady=20)
        self.frm_excel.pack_propagate(False)
        self.sheet_names = []
        self.make_select_widgets()

    def make_select_widgets(self):
        btn_open_excel = tk.Button(self.frm_excel, 
                                   text="Select Excel file",
                                   bg="red",
                                   command=self.select_excel_filepath)
        btn_open_excel.grid(row=0, 
                            column=0, 
                            padx=5, 
                            pady=5,
                            ipadx=50)
        self.lbl_excel_filepath = tk.Label(self.frm_excel, 
                                           text="Path to Excel file....", 
                                           fg="white",
                                           anchor="w")
        self.btn_data_browser = tk.Button(self.frm_excel,
                                          text="Browse Data",
                                          command=self.make_table_display)
        self.lbl_excel_filepath.grid(row=0, 
                                     column=1, 
                                     padx=5, 
                                     pady=5, 
                                     ipadx=50)
        self.lbl_excel_filepath.grid_propagate(False)
        self.cbo_sheet_names = ttk.Combobox(self.frm_excel, 
                                            values=self.sheet_names)
        self.cbo_sheet_names.grid(row=0, 
                                  column=2,
                                  ipadx=50)
        self.btn_data_browser.grid(row=0,
                                   column=3,
                                   padx=5,
                                   pady=5)

    def select_excel_filepath(self):
        filetypes = (
            ("All files", "*.*"),
        )
        excel_filepath = fd.askopenfilename(title="Select Excel file",
                                            initialdir=".",
                                            filetypes=filetypes)
        self.lbl_excel_filepath["text"] = os.path.basename(excel_filepath)
        self.lbl_excel_filepath.config(fg="black")
        self.excel_info = ExcelInfo(excel_filepath)
        self.sheet_names = self.excel_info.sheet_names
        self.cbo_sheet_names.config(values=self.sheet_names)

    def make_table_display(self):
        """Add a scrollable tabular display widget
        """
        frm_table_display = tk.Frame(self,
                                     width=600)
        frm_table_display.pack()
        lbl_rows_to_fetch = tk.Label(frm_table_display,
                                     text="Rows to fetch",
                                     relief="raised")
        txt_rows_to_fetch = tk.Entry(frm_table_display,
                                     bg="red")
        btn_fetch_rows = tk.Button(frm_table_display,
                                   text="Get Rows",
                                   command=self.get_rows,
                                   bg="blue",
                                   relief="sunken")
        lbl_rows_to_fetch.grid(row=0, 
                               column=0, 
                               padx=5, 
                               pady=5)
        txt_rows_to_fetch.grid(row=1, 
                               column=1,
                               padx=5,
                               pady=5)
        btn_fetch_rows.grid(row=2, 
                            column=2,
                            padx=5,
                            pady=5)
        column_count = self.excel_info.get_last_column_for_sheet(self.cbo_sheet_names.get())
        table = ttk.Treeview(frm_table_display, 
                             column=tuple([f"c{i}" for i in range(1,column_count + 1)]), 
                             show='headings')
        xscrollbar = ttk.Scrollbar(frm_table_display, orient='horizontal', command=table.xview)
        table.configure(xscrollcommand=xscrollbar.set)
        table.grid(row=3,
                   column=0,
                   columnspan=4)
        xscrollbar.grid(row=4,
                        column=0,
                        sticky="ew")
    def get_rows(self):
        pass
root = tk.Tk()
root.geometry("1000x800")
xl_browser = ExcelBrowser(root)
xl_browser.pack()
root.mainloop()