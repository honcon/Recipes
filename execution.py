import tkinter as tk
from backend import db, utilities
from tkinter import messagebox, ttk


class Execution(tk.Toplevel):
    def __init__(self, parent, recipe_id, *args, **kwargs):
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        
        self.title(f"Εκτέλεση Συνταγής {recipe_id}")
