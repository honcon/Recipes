import tkinter as tk


class Ingredients(tk.Frame):
    def __init__(self, *args, **kwargs):
        # super().__init__(parent, *args, **kwargs)
        # self.parent = parent
        tk.Frame.__init__(self, *args, **kwargs)
        self.label = tk.Label(self, text="Ingredients", font=("Arial", 24), border=1, relief="solid", padx=10, pady=10)
        self.label.pack(fill="x")

