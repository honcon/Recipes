import tkinter as tk
from backend import db, utilities
from tkinter import messagebox, ttk

class Welcome(tk.Frame):
    def __init__(self, parent, recipe_id, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.label = tk.Label(self, text="Καλώς ήρθατε στην συνταγη!", font=("Arial", 24), border=0, relief="solid", padx=10, pady=10)
        self.label.pack(fill="x")

class Step(tk.Frame):
    def __init__(self, parent, step_data, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.step_data = step_data

        self.label = tk.Label(self, text=f"Βήμα {self.step_data['number']}", font=("Arial", 16), border=0, relief="solid", padx=10, pady=10)
        self.label.pack(fill="x")

        self.description = tk.Label(self, text=self.step_data["description"], font=("Arial", 12), border=0, relief="solid", padx=10, pady=10)
        self.description.pack(fill="x")


class Finish(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.label = tk.Label(self, text="Η συνταγή ολοκληρώθηκε!", font=("Arial", 24), border=0, relief="solid", padx=10, pady=10)
        self.label.pack(fill="x")


class Execution(tk.Toplevel):
    def __init__(self, parent, recipe_id, *args, **kwargs):
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        
        self.title(f"Εκτέλεση Συνταγής id:{recipe_id}")
        self.recipe_id = recipe_id
        self.selected_step = -1

        self.progress = tk.DoubleVar()
        self.progress.set(0)

        response = utilities.get_full_recipe(recipe_id)

        if response["success"]:
            self.recipe = response["recipe"]
        else:
            messagebox.showerror("Σφάλμα", response["message"], parent=parent)
            self.destroy()
            return

        self.head_frame = tk.Frame(self)
        self.head_frame.columnconfigure(0, weight=1 )
        self.head_frame.pack(fill="x")

        self.label = tk.Label(self.head_frame, text=f"Εκτέλεση συνταγής {self.recipe["name"]}", font=("Arial", 24), border=0, relief="solid", padx=10, pady=10, borderwidth=0)
        self.label.grid(row=0, column=0, sticky="w")
        
        self.progress_label_frame = tk.Frame(self.head_frame)
        self.progress_label_frame.grid(row=0, column=1, sticky="e", padx=10)
        self.progress_label_frame.columnconfigure(0, weight=1)

        self.progress_label = tk.Label(self.progress_label_frame, text="Πρόοδος", font=("Arial", 12))
        self.progress_label.grid(row=0, column=0, sticky="e")
        self.progress_label_percentage = tk.Label(self.progress_label_frame, textvariable=self.progress, font=("Arial", 12))
        self.progress_label_percentage.grid(row=0, column=1, sticky="w")
        self.progress_label_percentage_sign = tk.Label(self.progress_label_frame, text="%", font=("Arial", 12))
        self.progress_label_percentage_sign.grid(row=0, column=2, sticky="w")

        self.progressbar = ttk.Progressbar(self.head_frame, orient="horizontal", length=200, mode="determinate", variable=self.progress, maximum=100)
        self.progressbar.grid(row=1, column=0, columnspan=2, sticky="we", padx=10)


        self.previous_button = tk.Button(self.head_frame, text="Προηγούμενο", command=self.previous_step, state="disabled")
        self.previous_button.grid(row=2, column=0, sticky="w", padx=10, pady=10)

        self.next_button = tk.Button(self.head_frame, text="Επόμενο", command=self.next_step)
        self.next_button.grid(row=2, column=1, sticky="e", padx=10, pady=10)

        self.mainframe = tk.Frame(self, borderwidth=1, relief='solid', padx=10, pady=10)
        self.mainframe.pack(fill="both", expand=True)

        Welcome(self, recipe_id).place(in_=self.mainframe, x=0, y=0, relwidth=1, relheight=1)

    def update_progress(self):
        total_time = self.recipe["execution_time"]

        if self.selected_step == -1:
            self.progress.set(0)
        elif self.selected_step == len(self.recipe["steps"]):
            self.progress.set(100)
        else:
            elapsed_time = 0
            for i in range(self.selected_step):
                elapsed_time += self.recipe["steps"][i]["execution_time"]

            percentage = int((elapsed_time / total_time) * 100)
            self.progress.set(percentage)

    def previous_step(self):
        self.selected_step -= 1
        if self.selected_step >= 0:
            Step(self, self.recipe["steps"][self.selected_step]).place(in_=self.mainframe, x=0, y=0, relwidth=1, relheight=1)
            self.previous_button["state"] = "normal"
            self.next_button["state"] = "normal"
        else:
            Welcome(self, self.recipe_id).place(in_=self.mainframe, x=0, y=0, relwidth=1, relheight=1)
            self.previous_button["state"] = "disabled"
            self.next_button["state"] = "normal"
        
        self.update_progress()

    def next_step(self):
        self.selected_step += 1

        if self.selected_step < len(self.recipe["steps"]):
            Step(self, self.recipe["steps"][self.selected_step]).place(in_=self.mainframe, x=0, y=0, relwidth=1, relheight=1)
            self.previous_button["state"] = "normal"
            self.next_button["state"] = "normal"
        else:
            Finish(self).place(in_=self.mainframe, x=0, y=0, relwidth=1, relheight=1)
            self.previous_button["state"] = "normal"
            self.next_button["state"] = "disabled"

        self.update_progress()