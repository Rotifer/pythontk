import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox
import tksheet
from duckdb_info import DuckDBInfo
from tkinter import ttk

"""
Creates a frame with widgets for interacting with Excel spreadsheets to display data from sheets.
Basic working version but it needs:
- Documentation
- Re-factoring
- Testing
"""

class DuckDBExplorer(tk.Frame):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, kwargs)
        self.parent = parent
        self.duckdb_info = None
        self.view_and_table_names = []
        self.header_row = []
        self.data_rows = []
        self.create_frame_layout()
        self.create_ctrl_widgets()

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
        btn_duckdb_filepath = ttk.Button(self.frm_ctrls, 
                                       text="Select DuckDB file",
                                       command=self.select_duckdb_filepath)
        self.lbl_duckdb_filepath = ttk.Label(self.frm_ctrls,
                                             width=40)
        lbl_table_names = ttk.Label(self.frm_ctrls, 
                                   text="Table/View Names:")
        lbl_rows_to_show = ttk.Label(self.frm_ctrls,
                                    text="Row count to preview:",
                                    width=15)
        self.cbo_table_names = ttk.Combobox(self.frm_ctrls, 
                                            values=self.view_and_table_names)
        btn_quit = ttk.Button(self.frm_ctrls,
                              text="Close",
                              command=self.quit)
        self.spn_rows_to_show = tk.Spinbox(self.frm_ctrls, 
                                      from_=50, 
                                      to=1000,
                                      increment=50,
                                      repeatdelay=500, 
                                      repeatinterval=100,
                                      font=("Arial", 12), 
                                      bg="lightgrey", 
                                      fg="blue",
                                      width=3)
        btn_show_table_data = ttk.Button(self.frm_ctrls, 
                                        text="Preview Table/View Data", 
                                        command=self.show_table_data)
        btn_show_table_summary = ttk.Button(self.frm_ctrls,
                                            text="Show Table/View Summary",
                                            command=self.show_table_summary)
        btn_duckdb_filepath.grid(row=0, 
                                column=0,
                                ipadx=30,
                                pady=(10, 0),
                                sticky="ew",
                                padx=(50,5))
        lbl_table_names.grid(row=1, 
                             column=0,
                             ipadx=30,
                             pady=(10,0),
                             sticky="ew",
                             padx=(50,5))
        self.cbo_table_names.grid(row=1, 
                                  column=1,
                                  ipadx=30,
                                  pady=(10,0),
                                  sticky="ew")
        lbl_rows_to_show.grid(row=2, 
                              column=0,
                              pady=(10, 0),
                              sticky="ew",
                              padx=(50,5))
        self.spn_rows_to_show.grid(row=2, 
                                   column=1,
                                   pady=(10,0),
                                   sticky="w")
        btn_show_table_data.grid(row=3, 
                                 column=0,
                                 pady=(10,10),
                                 sticky="nsew",
                                 padx=(50,5))
        btn_show_table_summary.grid(row=3,
                                    column=1,
                                    pady=(10,10),
                                    sticky="nsew")
        btn_quit.grid(row=4,
                      column=0,
                      columnspan=2,
                      pady=(10,10),
                      sticky="nsew",
                      padx=(50,5))

    def create_data_widget(self):
        self.tsh_sheet_data = tksheet.Sheet(self.frm_data, 
                                            width=900, 
                                            height=600)
        self.tsh_sheet_data.enable_bindings(("all"))

    def create_table_info_widget(self):
        """Create a frame with all the widgets needed to provide information on a 
        selected view or table.

        TODO: Refactor this method, it's much too large and complex.
        """
        self.frm_tbl_info = tk.LabelFrame(self.frm_data,
                                     text="Table/View Information")
        frm_basic_info = tk.LabelFrame(self.frm_tbl_info,
                                       text="Basic Details")
        lbl_tbl_name = ttk.Label(frm_basic_info, 
                                    text="Name:",
                                    width=10)
        self.ent_tbl_name = ttk.Entry(frm_basic_info,
                                      width=40)
        lbl_tbl_type = ttk.Label(frm_basic_info, 
                                    text="Table Type:",
                                    width=10)
        self.ent_tbl_type = ttk.Entry(frm_basic_info,
                                      width=40)
        lbl_tbl_row_count = ttk.Label(frm_basic_info,
                                      text="Row Count:",
                                      width=10)
        self.ent_tbl_row_count = ttk.Entry(frm_basic_info,
                                           width=40)
        frm_tbl_comment = tk.LabelFrame(frm_basic_info,
                                        text="Table Comment")
        self.txt_tbl_comment = tk.Text(frm_tbl_comment,
                                  height=4,
                                  width=150,
                                  relief="raised")
        btn_tbl_comment_update = ttk.Button(frm_tbl_comment,
                                            text="Update Comment",
                                            command=self.update_table_comment)
        frm_tbl_columns = tk.LabelFrame(self.frm_tbl_info,
                                        text="Columns Details")
        frm_cols_types_sheet = tk.LabelFrame(frm_tbl_columns,
                                             text="Columns-Types")
        self.tsh_tbl_cols_types = tksheet.Sheet(frm_cols_types_sheet,
                                                width=400,
                                                height=400)
        frm_col_comments_mgr = tk.LabelFrame(frm_tbl_columns,
                                             text="Column Comments")
        self.cbo_table_columns = ttk.Combobox(frm_col_comments_mgr)
        self.cbo_table_columns.bind("<<ComboboxSelected>>", self.table_column_selection)
        frm_col_comment = tk.LabelFrame(frm_col_comments_mgr,
                                        text="Column Comment")
        self.txt_col_comment = tk.Text(frm_col_comment,
                                       height=3,
                                       width= 100)
        btn_update_col_comment = ttk.Button(frm_col_comment,
                                            text="Update Comment",
                                            command=self.update_column_comment)
        frm_cols_types_sheet.grid(row=0,
                                  column=0,
                                  sticky="nsew")
        frm_basic_info.grid(row=0,
                            column=0,
                            sticky="ew")
        frm_tbl_comment.grid(row=0,
                             column=2,
                             sticky="nsew",
                             rowspan=3)
        frm_tbl_columns.grid(row=2,
                             column=0,
                             sticky="ewns")
        lbl_tbl_name.grid(row=0,
                          column=0,
                          padx=5,
                          pady=5)
        self.ent_tbl_name.grid(row=0,
                               column=1,
                               sticky="ew",
                               padx=5,
                               pady=5)
        lbl_tbl_type.grid(row=1,
                          column=0,
                          padx=5,
                          pady=5)
        self.ent_tbl_type.grid(row=1,
                          column=1)
        lbl_tbl_row_count.grid(row=2,
                               column=0,
                               padx=5,
                               pady=5)
        self.ent_tbl_row_count.grid(row=2,
                                    column=1,
                               padx=5,
                               pady=5)
        self.txt_tbl_comment.grid(row=0,
                                  column=0,
                                  padx=5,
                                  pady=5)
        btn_tbl_comment_update.grid(row=1,
                                    column=0,
                                    padx=5,
                                    pady=5)
        frm_cols_types_sheet.grid(row=0,
                                  column=0,
                                  sticky="ewns")
        self.tsh_tbl_cols_types.grid(row=0,
                                     column=0,
                                     sticky="nsew")
        frm_col_comments_mgr.grid(row=0,
                                  column=1,
                                  sticky="nsew")
        self.cbo_table_columns.grid(row=0,
                                    column=0)
        frm_col_comment.grid(row=1,
                             column=0,
                             sticky="nsew")
        self.txt_col_comment.grid(row=0,
                                  column=0,
                                  sticky="nsew")
        btn_update_col_comment.grid(row=1,
                                    column=0)
    # Button actions
    def select_duckdb_filepath(self):
        filetypes = (
            ("DuckDB files (.db)", "*.db"),
            ("DuckDB files (.ddb)", "*.ddb"),
        )
        duckdb_filepath = fd.askopenfilename(title="Select DuckDB  database file",
                                            initialdir=".",
                                            filetypes=filetypes)
        self.duckdb_info = DuckDBInfo(duckdb_filepath)
        self.lbl_duckdb_filepath["text"] = duckdb_filepath
        self.lbl_duckdb_filepath.grid(row=0, 
                                     column=1, 
                                     sticky="ew",
                                     pady=(10, 0))
        self.excel_info = DuckDBInfo(duckdb_filepath)
        self.view_and_table_names = self.duckdb_info.view_and_table_names
        self.cbo_table_names["values"] = self.view_and_table_names

    def show_table_data(self):
        if hasattr(self, "frm_tbl_info"):
            self.frm_tbl_info.grid_forget()
        self.create_data_widget()
        self.tsh_sheet_data.headers([])
        self.tsh_sheet_data.set_sheet_data([])
        table_name = self.cbo_table_names.get()
        self.header_row = self.duckdb_info.get_table_column_names(table_name)
        row_count_limit = int(self.spn_rows_to_show.get())
        try:
            self.data_rows = self.duckdb_info.get_table_rows(table_name, 
                                                             row_count_limit)
        except Exception as ex:
            err_substr = "Binder Error: Contents of view were altered:"
            if err_substr in str(ex):
                messagebox.showerror("View definition error", 
                                     f"Problem with {table_name} definition")
            else:
                messagebox.showerror("General error", str(ex)[0:100])
        self.tsh_sheet_data.headers(self.header_row)
        self.tsh_sheet_data.set_sheet_data(self.data_rows)
        self.tsh_sheet_data.grid(row=0, 
                                 column=0, 
                                 sticky="nsew",
                                 padx=50,
                                 pady=50)
        
    def show_table_summary(self):
        """Remove the data view and replace it with a frame containing summary information for
        the selected view/table."""
        if hasattr(self, "tsh_sheet_grid"):
            self.tsh_sheet_data.grid_forget()
        self.create_table_info_widget()
        self.frm_tbl_info.grid(row=0,
                               column=0,
                               padx=10,
                               pady=10,
                               ipadx=50,
                               sticky="nsew")
        table_name = self.cbo_table_names.get()
        table_info_summary = self.duckdb_info.get_table_info_summary(table_name)
        print(table_info_summary)
        self.ent_tbl_name.delete(0, "end")
        self.ent_tbl_name.insert(0, table_info_summary["table_name"])
        self.ent_tbl_type.delete(0, "end")
        self.ent_tbl_type.insert(0, table_info_summary["table_type"])
        self.ent_tbl_row_count.delete(0, "end")
        self.ent_tbl_row_count.insert(0, table_info_summary["table_row_count"])
        self.txt_tbl_comment.delete(1.0, "end")
        self.txt_tbl_comment.insert(1.0, table_info_summary["table_comment"])
        self.tsh_tbl_cols_types.headers = ["Column Name", "Column Type"]
        self.tsh_tbl_cols_types.set_sheet_data(table_info_summary["table_columns_types"])
        self.cbo_table_columns["values"] = self.duckdb_info.get_table_column_names(table_name)

    def update_table_comment(self):
        """Add the updated comment for a table or view to the duckdb_tables or 
        duckdb_views metadata store.
        """
        table_name = self.cbo_table_names.get()
        print(type(table_name))
        table_comment = self.txt_tbl_comment.get(1.0, "end")
        table_type = self.ent_tbl_type.get()
        if table_type == "table":
            self.duckdb_info.update_table_comment(table_name, table_comment)
        elif table_type == "view":
            self.duckdb_info.update_view_comment(table_name, table_comment)
        messagebox.showinfo("Table/View Comments", f"{table_type.upper()} '{table_name}' comment updated!")

    def update_column_comment(self):
        """Update or add a comment to a column"""
        column_comment = self.txt_col_comment.get(1.0, "end")
        table_name = self.cbo_table_names.get()
        column_name = self.cbo_table_columns.get()
        self.duckdb_info.update_column_comment(table_name, column_name, column_comment)
        messagebox.showinfo("Column comments", "Column comment added")

    def table_column_selection(self, event):
        column_name = self.cbo_table_columns.get()
        messagebox.showinfo("Test binding", f"Column {column_name} selected!")
        selected_table_name = self.cbo_table_names.get()
        selected_column_name = self.cbo_table_columns.get()
        column_comment = self.duckdb_info.get_column_comment(selected_table_name,
                                                             selected_column_name)
        self.txt_col_comment.delete(1.0, "end")
        self.txt_col_comment.insert(1.0, column_comment)

    def quit(self):
        self.parent.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1800x500")
    root.title("DuckDB Explorer")
    ddb_xplr = DuckDBExplorer(root)
    ddb_xplr.pack(expand=True, fill="both")
    root.mainloop()