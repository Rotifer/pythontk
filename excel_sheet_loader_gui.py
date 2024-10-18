import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from excel_info import ExcelInfo
from duckdb_info import DuckDBInfo
from excel_sheet_loader import ExcelSheetLoader

class ExcelSheetLoaderForm(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, kwargs)
        self.parent  = parent
        self.excel_filepath = None
        self.duckdb_filepath = None
        self.excel_info = None
        self.duckdb_info = None
        self.excel_sht_ldr = None
        self.make_frame_file_select()
        self.make_frame_display_sheets_tables()
        self.make_frame_upload_sheet()

    def make_frame_file_select(self):
        frm_select_files = tk.LabelFrame(self,
                                         text="Select Excel and DuckDB Files")
        btn_create_new_db = ttk.Button(frm_select_files,
                                       text="New DuckDB",
                                       command=self.create_new_duckdb_file)
        self.ent_new_db_name = ttk.Entry(frm_select_files,
                                         width=20)
        btn_select_excel_file = ttk.Button(frm_select_files, 
                                           text="Select Excel File",
                                           command=self.select_excel_filepath)
        self.btn_select_duckdb_file = ttk.Button(frm_select_files, 
                                                 text="Select DuckDB File",
                                                 command=self.select_duckdb_filepath)
        self.lbl_select_excel_file = ttk.Label(frm_select_files, width=20)
        self.lbl_select_duckdb_file = ttk.Label(frm_select_files, width=20)
        btn_create_new_db.grid(row=0,
                               column=0,
                               ipadx=17)
        self.ent_new_db_name.grid(row=0,
                                  column=1)
        btn_select_excel_file.grid(row=1, 
                                   column=0,
                                   padx=10,
                                   pady=10,
                                   ipadx=7)
        self.lbl_select_excel_file.grid(row=1, 
                                        column=1,
                                        padx=10,
                                        pady=10)
        self.btn_select_duckdb_file.grid(row=2,
                                         column=0,
                                         padx=10,
                                         pady=10)
        self.lbl_select_duckdb_file.grid(row=2, 
                                         column=1,
                                         padx=10,
                                         pady=10)
        frm_select_files.grid(row=0,
                              column=0,
                              stick="ew")
    
    def make_frame_display_sheets_tables(self):
        frm_display_shts_tbls = tk.LabelFrame(self,
                                         text="Available Sheets and Tables")
        frm_sheet_names = ttk.LabelFrame(frm_display_shts_tbls, 
                                    text="Sheet Names")
        frm_table_names = ttk.LabelFrame(frm_display_shts_tbls,
                                    text="Table Names")
        self.cbo_sheet_names = ttk.Combobox(frm_sheet_names)
        self.cbo_table_names = ttk.Combobox(frm_table_names)
        frm_sheet_names.grid(row=0, 
                             column=0,
                             sticky="w",
                             ipadx=73)
        frm_table_names.grid(row=0,
                             column=1,
                             sticky="e", 
                             ipadx=73)
        self.cbo_sheet_names.grid(row=0,
                                  column=0,
                                  sticky="ew")
        self.cbo_table_names.grid(row=0,
                                  column=0,
                                  sticky="ew")
        frm_display_shts_tbls.grid(row=1,
                                   column=0,
                                   sticky="ew")
        self.cbo_sheet_names.bind("<<ComboboxSelected>>", 
                                  self.sheet_selected)

    def make_frame_upload_sheet(self):
        frm_upload_sheet = ttk.LabelFrame(self,
                                          text="Upload Selected Sheet")
        frm_new_table_name = ttk.LabelFrame(frm_upload_sheet,
                                        text="New Table Name")
        self.ent_new_table_name = ttk.Entry(frm_new_table_name,
                                            width=40)
        frm_description = ttk.LabelFrame(frm_upload_sheet,
                                         text="Table Description")
        self.txt_new_description = tk.Text(frm_description,
                                           height=3,
                                           width=100)
        btn_upload_sheet = ttk.Button(frm_upload_sheet,
                                      text="Upload Sheet",
                                      command=self.load_sheet_to_new_table)
        btn_append_sheet_data = ttk.Button(frm_upload_sheet,
                                           text="Append Sheet",
                                           command=self.append_sheet_data_to_table)
        frm_new_table_name.grid(row=0,
                                column=0,
                                columnspan=2,
                                sticky="ew")
        self.ent_new_table_name.grid(row=0,
                                     column=0)
        frm_description.grid(row=1,
                             column=0,
                             columnspan=2)
        self.txt_new_description.grid(row=0,
                                      column=0)
        btn_upload_sheet.grid(row=2,
                              column=0)
        btn_append_sheet_data.grid(row=2,
                                   column=1)
        frm_upload_sheet.grid(row=2,
                              column=0)
        
    def make_frame_database_feedback(self):
        self.frm_feedback = ttk.LabelFrame(self,
                                      text="Database Feedback")
        self.txt_feedback = tk.Text(self.frm_feedback,
                                    height=5,
                                    width=100)
        self.txt_feedback.grid(row=0,
                               column=0)

    # Actions
    def create_new_duckdb_file(self):
        self.btn_select_duckdb_file.configure(state="disabled")
        new_duckdb_filename = self.ent_new_db_name.get()
        target_dirname = fd.askdirectory(initialdir=".")
        self.duckdb_filepath = os.path.join(target_dirname, new_duckdb_filename)
        self.duckdb_info = DuckDBInfo(self.duckdb_filepath)

    def select_excel_filepath(self):
        filetypes = (
            ("Excel files (new)", "*.xlsx"),
            ("Excel files (old)", "*.xls"),
        )
        self.excel_filepath = fd.askopenfilename(title="Select Excel file",
                                            initialdir=".",
                                            filetypes=filetypes)
        self.lbl_select_excel_file["text"] = os.path.basename(self.excel_filepath)
        self.excel_info = ExcelInfo(self.excel_filepath)
        self.cbo_sheet_names.config(values=self.excel_info.sheet_names)

    def select_duckdb_filepath(self):
        filetypes = (
            ("DuckDB files", "*.ddb"),
            ("DuckDB files", "*.db"),
        )
        self.duckdb_filepath = fd.askopenfilename(title="Select DuckDB file",
                                            initialdir=".",
                                            filetypes=filetypes)
        self.lbl_select_duckdb_file["text"] = os.path.basename(self.duckdb_filepath)
        self.duckdb_info = DuckDBInfo(self.duckdb_filepath)
        self.cbo_table_names.config(values=self.duckdb_info.table_names)

    def sheet_selected(self, event):
        selected_sheet_name = self.cbo_sheet_names.get()
        self.ent_new_table_name.delete(0, "end")
        self.ent_new_table_name.insert(0, selected_sheet_name)
    
    def load_sheet_to_new_table(self):
        xl_sh_ldr = ExcelSheetLoader(self.duckdb_filepath,
                                     self.excel_filepath)
        load_sheet_name = self.cbo_sheet_names.get()
        new_table_name = self.ent_new_table_name.get()
        table_description = self.txt_new_description.get("0.0", "end")
        xl_sh_ldr.load_sheet_to_ddb(load_sheet_name, table_description,new_table_name)
        table_names_updated = self.duckdb_info.table_names
        self.cbo_table_names.config(values=table_names_updated)
        try:
            self.frm_feedback.grid_forget()
        except Exception as ex:
            print(ex)
        self.make_frame_database_feedback()
        self.frm_feedback.grid(row=3,
                               column=0)
        feedback = self.duckdb_info.get_table_comment(new_table_name)
        self.txt_feedback.insert("1.0", feedback)
        
    def append_sheet_data_to_table(self):
        xl_sh_ldr = ExcelSheetLoader(self.duckdb_filepath,
                                     self.excel_filepath)
        append_sheet_name = self.cbo_sheet_names.get()
        target_table_name = self.cbo_table_names.get()
        xl_sh_ldr.append_sheet_data_to_table(append_sheet_name,
                                             target_table_name)
        try:
            self.frm_feedback.grid_forget()
        except Exception as ex:
            print(ex)
        self.make_frame_database_feedback()
        self.frm_feedback.grid(row=3,
                               column=0)
        feedback = self.duckdb_info.get_table_comment(target_table_name)
        self.txt_feedback.insert("1.0", feedback)      
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("720x500")
    root.title("Load Excel Sheets to DuckDB")
    xlldr = ExcelSheetLoaderForm(root)
    xlldr.grid(row=0, column=0, sticky="nsew")
    xlldr.mainloop()