import tkinter as tk
import tkinter.filedialog as fd
import tksheet
from tkinter import ttk

"""
Composed of three child frames that use the grid geometry manager to arrange the frames in 
a dashboard-like format
Functionality specification:
Three panels (frames):
1. Top open and close buttons and label to display the selected DuckDB database path
2: Side panel with drop-downs to display tables and views in the selected database
3. Main panel with a table to display
    1. The comment for the selected object
    2. A tabular display for the selected object's column details
    3. The object's DDL
To implement:
- Ability to edit and update the object's comment
- Button to open a DuckDB file and display the path
- Button to attach another DuckDB database?? (not implemented, might not implement)
- Side-bar to display drop-downs for the tables and views in the selected database

Further work

- Styles are delivberately awful
- Make it into an attachabel component for a main app
    - To do so, it should inherit from tk.Frame so __init__ will need to be re-worked
"""

class App(tk.Tk):
    def __init__(self, title, height, width, resizable_x=True, resizable_y=True):
        super().__init__()
        self.title(title)
        self.geometry(f"{height}x{width}")
        self.resizable(resizable_x, resizable_y)
        self.create_frame_layout()
        self.create_top_widgets()
        self.create_side_widgets()
        self.create_main_widgets()
        self.mainloop()
		
    def create_frame_layout(self):
        frm_container = tk.Frame(self)
        frm_container.pack(side="left", anchor="ne", fill="both", expand=True)
        self.frm_top = tk.Frame(frm_container, bg="blue")
        self.frm_side = tk.Frame(frm_container, bg="red")
        self.frm_main = tk.Frame(frm_container, bg="black")
        frm_container.rowconfigure(0, weight=1)
        frm_container.rowconfigure(1, weight=8)
        frm_container.columnconfigure(0, weight=1)
        frm_container.columnconfigure(1, weight=3)
        self.frm_top.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.frm_side.grid(row=1, column=0, sticky="nsew")
        self.frm_main.grid(row=1, column=1, sticky="nsew")
        
    def create_top_widgets(self):
        btn_open_file = tk.Button(self.frm_top, 
                                  text="Open", 
                                  width=20,
                                  command=self.get_ddb_filepath)
        btn_close_file = tk.Button(self.frm_top, 
                                   text="Close", 
                                   width=20,
                                   command=self.close)
        self.lbl_ddb_filepath = tk.Label(self.frm_top, 
                                         text="", 
                                         width=50)
        btn_open_file.grid(row=0, 
                           column=0,
                           sticky="e", 
                           padx=150, 
                           pady=10, 
                           ipadx=50)
        btn_close_file.grid(row=0, 
                            column=1, 
                            sticky="w", 
                            padx=5, 
                            pady=10, 
                            ipadx=50)
    
    def close(self):
        self.destroy()
    
    def create_side_widgets(self):
        lbl_table_names = tk.Label(self.frm_side, 
                                   text="Table Names") 
        table_names = ["Python", "Ruby", "Perl", "JavaScript", "Java", "C++", "C", "Go", "Rust"]
        cbo_table_names = ttk.Combobox(self.frm_side, 
                                       values=table_names)
        lbl_view_names = tk.Label(self.frm_side, 
                                  text="View Names") 
        view_names = ["Unix", "Linux", "Windows", "Mac OS X"]
        cbo_view_names = ttk.Combobox(self.frm_side, 
                                      values=view_names)
        lbl_table_names.grid(row=0, 
                             column=0, 
                             padx=5, 
                             pady=5)
        cbo_table_names.grid(row=1, 
                             column=0, 
                             padx=5, 
                             pady=5)
        lbl_view_names.grid(row=2, 
                            column=0, 
                            padx=5, 
                            pady=5)
        cbo_view_names.grid(row=3, column=0, padx=5, pady=5)

    def create_main_widgets(self):
        sheet_data = [["gene_id", "INTEGER"],
                      ["gene_name", "VARCHAR"],
                      ["gene_build", "VARCHAR"],
                      ["gene_start_position", "INTEGER"],
                      ["gene_end_position", "INTEGER"]]
        lbl_catalog_comment = tk.Label(self.frm_main, 
                                       text="Catalog Comment")
        txt_catalog_comment = tk.Text(self.frm_main, 
                                      width=100, 
                                      height=5)
        lbl_object_columns = tk.Label(self.frm_main, 
                                      text="Object columns")
        tsh_object_columns = tksheet.Sheet(self.frm_main, 
                                           width=500, 
                                           height=200)
        tsh_object_columns.enable_bindings(("all"))
        tsh_object_columns.headers(["Column Name", "Data type"])
        tsh_object_columns.set_sheet_data(sheet_data)
        lbl_object_ddl = tk.Label(self.frm_main, 
                                  text = "Object DDL")
        txt_object_ddl = tk.Text(self.frm_main,
                                  width=100, 
                                  height=5)
        lbl_catalog_comment.grid(row=0, 
                                 column=0, 
                                 padx=5, 
                                 pady=5)
        txt_catalog_comment.grid(row=1, 
                                 column=0, 
                                 padx=5, 
                                 pady=5)
        lbl_object_columns.grid(row=2, 
                                column=0, 
                                padx=5, 
                                pady=5)
        tsh_object_columns.grid(row=3, 
                                column=0, 
                                padx=5, 
                                pady=5)
        lbl_object_ddl.grid(row=4, 
                            column=0, 
                            padx=5, 
                            pady=5)
        txt_object_ddl.grid(row=5, 
                            column=0, 
                            padx=5, 
                            pady=5)
    
    def get_ddb_filepath(self):
        filetypes = (
            ("All files", "*.*"),
        )
        ddb_filepath = fd.askopenfilename(title="Select DuckDB file",
                                            initialdir=".",
                                            filetypes=filetypes)
        self.lbl_ddb_filepath["text"] = ddb_filepath
        self.lbl_ddb_filepath.grid(row=1, 
                                   column=0,
                                   columnspan=2, 
                                   padx=5, 
                                   pady=5, 
                                   sticky="ew")

app = App("Testing grid", 1000, 1000, False, False)