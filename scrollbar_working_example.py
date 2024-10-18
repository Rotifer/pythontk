import tkinter as tk
from tkinter import ttk

class BookApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Books and Websites")
        self.setup_gui()

    def setup_gui(self):
        self.master.title("Books and Websites")
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        self.notebook = ttk.Notebook(self.master)
        self.notebook.grid(row=0, column=0, sticky="nsew")

        self.main_frame = ttk.Frame(self.notebook)
        self.main_frame.grid_rowconfigure(0, weight=0)  
        self.main_frame.grid_columnconfigure(0, weight=0)  
        self.notebook.add(self.main_frame, text='Main')

        self.secondary_frame = ttk.Frame(self.notebook)
        self.secondary_frame.grid_rowconfigure(0, weight=0) 
        self.secondary_frame.grid_columnconfigure(0, weight=0)  
        self.notebook.add(self.secondary_frame, text='Secondary')

        self.book_frame = ttk.LabelFrame(self.main_frame, text="Book stuff", padding=(10, 10), width=700, height=175)
        self.book_frame.grid(row=0, column=1, pady=10, padx=10)
        
        # Allow children frames to expand horizontally
        self.book_frame.grid_columnconfigure(0, weight=1)

        # Prevent the frame itself from resizing
        self.book_frame.grid_propagate(flag=False)

        self.details_tree = ttk.Treeview(self.book_frame, columns=("Title", "Year", "Publisher", "ISBN", "Genre", "Description"), show="headings", height=4)
        self.vsb = ttk.Scrollbar(self.book_frame, orient="vertical", command=self.details_tree.yview)
        self.hsb = ttk.Scrollbar(self.book_frame, orient="horizontal", command=self.details_tree.xview)
        self.details_tree.configure(yscrollcommand=self.vsb.set, xscrollcommand=self.hsb.set)
        
        self.details_tree.tag_configure('evenrow', background='#FFFFFF')
        self.details_tree.tag_configure('oddrow', background='#d3d3d3')
        
        self.details_tree.grid(row=0, column=0, sticky='nsew')
        self.vsb.grid(row=0, column=1, sticky='ns')
        self.hsb.grid(row=1, column=0, sticky='ew')

        self.details_tree.column("Title", width=100)
        self.details_tree.column("Year", width=50)
        self.details_tree.column("Publisher", width=100)
        self.details_tree.column("ISBN", width=100)
        self.details_tree.column("Genre", width=100)
        self.details_tree.column("Description", width=1000) 

        self.details_tree.heading("Title", text="Title")
        self.details_tree.heading("Year", text="Year")
        self.details_tree.heading("Publisher", text="Publisher")
        self.details_tree.heading("ISBN", text="ISBN")
        self.details_tree.heading("Genre", text="Genre")
        self.details_tree.heading("Description", text="Description")

        dummy_values = ("Dummy Title", "2023", "Dummy Publisher", "1234567890", "Dummy Genre", "This is a dummy description." * 10)
        
        for x in range(0, 10):
            self.details_tree.insert("", "end", values=dummy_values)

def main():
    root = tk.Tk()
    app = BookApp(root)
    # root.geometry("600x400")
    root.mainloop()

if __name__ == "__main__":
    main()