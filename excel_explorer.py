import tkinter as tk
from tkinter import filedialog as fd
import tksheet
from excel_info import ExcelInfo
from tkinter import ttk

"""
Creates a frame with widgets for interacting with Excel spreadsheets to display data from sheets.
"""

class ExcelExplorer(tk.Frame):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, kwargs)
        self.parent = parent
        self.excel_info = None
        self.sheet_names = []
        self.header_row = []
        self.data_rows = []
        self.create_frame_layout()
        self.create_ctrl_widgets()
        self.create_data_widget()

    def create_frame_layout(self):
        frm_container = tk.Frame(self)
        frm_container.pack(side="left", 
                           anchor="ne", 
                           fill="both", 
                           expand=True)
        self.frm_ctrls = tk.Frame(frm_container, 
                                  bg="#9E9E9E")
        self.frm_data = tk.Frame(frm_container)
        self.frm_ctrls.pack(side="top", 
                            expand=True, 
                            fill="x", 
                            anchor="ne")
        self.frm_data.pack(side="bottom", 
                           expand=True, 
                           fill="both")

    def create_ctrl_widgets(self):
        btn_excel_filepath = ttk.Button(self.frm_ctrls, 
                                       text="Select Excel file",
                                       command=self.select_excel_filepath)
        self.lbl_excel_filepath = ttk.Label(self.frm_ctrls)
        lbl_sheet_names = ttk.Label(self.frm_ctrls, 
                                   text="Sheet Names:")
        lbl_rows_to_show = ttk.Label(self.frm_ctrls,
                                    text="Row count to preview:",
                                    width=15)
        self.cbo_sheet_names = ttk.Combobox(self.frm_ctrls, 
                                            values=self.sheet_names)
        btn_quit = ttk.Button(self.frm_ctrls,
                              text="Close",
                              command=self.quit)
        self.spn_rows_to_show = tk.Spinbox(self.frm_ctrls, 
                                      from_=50, 
                                      to=1000,
                                      increment=50,
                                      relief="sunken", 
                                      repeatdelay=500, 
                                      repeatinterval=100,
                                      font=("Arial", 12), 
                                      bg="lightgrey", 
                                      fg="blue",
                                      width=3)
        btn_show_sheet_data = tk.Button(self.frm_ctrls, 
                                        text="Preview Data", 
                                        command=self.show_sheet_data)
        btn_excel_filepath.grid(row=0, 
                                column=0,
                                ipadx=30,
                                pady=(10, 0),
                                sticky="ew",
                                padx=(50,5))
        lbl_sheet_names.grid(row=1, 
                             column=0,
                             ipadx=30,
                             pady=(10,0),
                             sticky="ew",
                             padx=(50,5))
        self.cbo_sheet_names.grid(row=1, 
                                  column=1,
                                  ipadx=30,
                                  pady=(10,0),
                                  sticky="ew")
        lbl_rows_to_show.grid(row=2, 
                              column=0,
                              pady=(10,0),
                              sticky="ew",
                              padx=(50,5))
        self.spn_rows_to_show.grid(row=2, 
                                   column=1,
                                   pady=(10,0),
                                   sticky="w")
        btn_show_sheet_data.grid(row=3, 
                                 column=0,
                                 pady=(10,10),
                                 sticky="ew",
                                 padx=(50,5))
        btn_quit.grid(row=3,
                      column=1,
                      pady=(10,0),
                      sticky="w")

    def create_data_widget(self):
        self.tsh_sheet_data = tksheet.Sheet(self.frm_data, 
                                            width=900, 
                                            height=600)
        self.tsh_sheet_data.enable_bindings(("all"))

    # Button actions
    def select_excel_filepath(self):
        filetypes = (
            ("Excel files (new)", "*.xlsx"),
            ("Excel files (old)", "*.xls"),
        )
        excel_filepath = fd.askopenfilename(title="Select Excel file",
                                            initialdir=".",
                                            filetypes=filetypes)
        self.excel_info = ExcelInfo(excel_filepath)
        self.lbl_excel_filepath["text"] = excel_filepath
        self.lbl_excel_filepath.grid(row=0, 
                                     column=1, 
                                     sticky="ew",
                                     pady=(10, 0))
        self.excel_info = ExcelInfo(excel_filepath)
        self.sheet_names = self.excel_info.sheet_names
        self.cbo_sheet_names["values"] = self.sheet_names

    def show_sheet_data(self):
        sheet_name = self.cbo_sheet_names.get()
        self.header_row = self.excel_info.get_row_values(sheet_name)
        self.data_rows = []
        last_row = int(self.spn_rows_to_show.get()) + 2
        for i in range(2, last_row):
            data_row = self.excel_info.get_row_values(sheet_name, i)
            self.data_rows.append(data_row)
        self.tsh_sheet_data.headers(self.header_row)
        self.tsh_sheet_data.set_sheet_data(self.data_rows)
        self.tsh_sheet_data.grid(row=0, 
                                 column=0, 
                                 sticky="nsew",
                                 padx=50,
                                 pady=50)

    def quit(self):
        self.parent.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1000x1000")
    root.title("Excel Explorer")
    xl_xplr = ExcelExplorer(root)
    print(issubclass(ExcelExplorer, tk.Frame))
    xl_xplr.pack(expand=True, fill="both")
    root.mainloop()