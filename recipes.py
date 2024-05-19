import tkinter as tk


class Recipes(tk.Frame):
    def __init__(self, *args, **kwargs):
        # super().__init__(parent, *args, **kwargs)
        # self.parent = parent
        tk.Frame.__init__(self, *args, **kwargs)
        self.label = tk.Label(self, text="Recipes", font=("Arial", 24), border=1, relief="solid", padx=10, pady=10)
        self.label.pack(fill="x")

