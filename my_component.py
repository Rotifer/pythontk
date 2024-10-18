import tkinter as tk

class MyComponent(tk.Frame):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, kwargs)
        self.parent = parent
        self.pack(expand=True, fill="both")
        self.add_widgets()

    def add_widgets(self):
        lbl = tk.Label(self, text="A widget", bg="red")
        lbl.pack(expand=True, fill="both", padx=10, pady=10)


my_component = MyComponent()
my_component.mainloop()