import tkinter as tk
from backend import project10_db as db
from tkinter import messagebox, ttk
from tkscrolledframe import ScrolledFrame

# https://pythonassets.com/posts/drop-down-list-combobox-in-tk-tkinter/

class StepFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent.steps_frame, *args, **kwargs, bd=1, relief="raised")

        self.step_number = kwargs.get("step_number", 0)
        self.title = tk.StringVar(value=kwargs.get("title", ""))
        self.description = tk.StringVar(value=kwargs.get("description", ""))
        self.execution_time = tk.IntVar(value=kwargs.get("execution_time", 0))

        # step_frame = tk.Frame(self.steps_frame, border=1, relief="solid")
        # step_frame.grid(pady=5)
        self.pack(fill="x", expand=True)

        head_frame = tk.Frame(self, padx=10, pady=10)
        head_frame.columnconfigure(0, weight=1)
        step_label = tk.Label(head_frame, text=f"Βήμα {self.step_number}", font=("Helvetica", 13, "bold"), anchor="w")
        step_label.grid(row=0, column=0, sticky="w")

        delete_button = tk.Button(head_frame, text="Διαγραφή", command=lambda: parent.delete_step(self))
        delete_button.grid(row=0, column=1, sticky="e")
        
        head_frame.pack(fill="x", expand=True)
        separator = ttk.Separator(self, orient="horizontal") 
        separator.pack(fill="x")
        

        # Title

        title_frame = tk.Frame(self, padx=10, pady=10)
        title_frame.grid_columnconfigure(1, weight=1)

        title_label = tk.Label(title_frame, text="Τίτλος", font=("Helvetica", 12, "bold"), width=20, anchor="e")
        title_label.grid(row=0, column=0, sticky="w")

        title_entry = tk.Entry(title_frame, textvariable=self.title)
        title_entry.grid(row=0, column=1, sticky="we")

        title_frame.pack(fill="x", expand=True)

        # Execution Time in hours and minutes
        time_frame = tk.Frame(self, padx=10, pady=10)
        time_frame.grid_columnconfigure(1, weight=1)

        time_label = tk.Label(time_frame, text="Χρόνος Εκτέλεσης", font=("Helvetica", 12, "bold"), width=20, anchor="e")
        time_label.grid(row=0, column=0, sticky="w")

        time_entry = tk.Entry(time_frame, textvariable=self.execution_time)
        time_entry.grid(row=0, column=1, sticky="we")

        time_frame.pack(fill="x", expand=True)

        # Description

        description_frame = tk.Frame(self, padx=10, pady=10)
        description_frame.grid_columnconfigure(1, weight=1)

        description_label = tk.Label(description_frame, text="Περιγραφή", font=("Helvetica", 12, "bold"), width=20, anchor="e")
        description_label.grid(row=0, column=0, sticky="w")

        description_entry = tk.Text(description_frame, height=5, width=30)
        description_entry.insert(tk.END, self.description.get())

        description_entry.bind("<KeyRelease>", lambda e: self.description.set(description_entry.get("1.0", tk.END)))

        description_entry.grid(row=0, column=1, sticky="we")

        description_frame.pack(fill="x", expand=True)


class AddEditRecipe(tk.Toplevel):

    def __init__(self, parent, recipe_id, *args, **kwargs):
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        
        self.edit_mode = recipe_id and recipe_id > 0
        self.parent = parent

        self.categories = self.get_categories()
        
        self.name = tk.StringVar()
        self.steps = []

        self.title(f"Επεξεργασία Συνταγής {recipe_id}" if self.edit_mode else "Δημιουργία")

        top_bar = tk.Frame(self, padx=10, pady=10)
        top_bar.columnconfigure(0, weight=1)

        label_container = tk.Frame(top_bar)
        label_container.grid(row=0, column=0, sticky="w")

        self.label = tk.Label(label_container, text="Επεξεργασία συνταγής: " if self.edit_mode else "Νέα συνταγή: ", font=("Arial", 24))
        self.label_name = tk.Label(label_container, textvariable=self.name, font=("Arial", 24))

        self.label.grid(row=0, column=0, sticky="w")
        self.label_name.grid(row=0, column=1)

        self.save_button = tk.Button(top_bar, text="Αποθήκευση", command=self.save)
        self.save_button.grid(row=0, column=1, sticky="e")

        top_bar.pack(fill="x")
        
        left_frame = tk.Frame(self, padx=5, pady=5, border=0, relief="solid", width=200)
        main_frame = tk.Frame(self, padx=5, pady=5, border=0, relief="solid")

        left_frame.pack(side="left", fill="y", expand=False)
        main_frame.pack(fill="both", side="left", expand=True)


        # Basic Recipe Information

        self.recipe_name_label = tk.Label(left_frame, text="Όνομα Συνταγής", anchor="w", font=("Helvetica", 13, "bold"))
        self.recipe_name_label.pack(fill="x")

        self.recipe_name = tk.Entry(left_frame, textvariable=self.name)
        self.recipe_name.pack(fill="x")

        self.recipe_category_label = tk.Label(left_frame, text="Κατηγορία", anchor="w", font=("Helvetica", 13, "bold"))
        self.recipe_category_label.pack(fill="x")

        self.recipe_category = ttk.Combobox(left_frame, values=self.categories)
        self.recipe_category.pack(fill="x")

        self.recipe_difficulty_label = tk.Label(left_frame, text="Δυσκολία", anchor="w", font=("Helvetica", 13, "bold"))
        self.recipe_difficulty_label.pack(fill="x")

        self.recipe_difficulty = ttk.Combobox(left_frame, state="readonly", values=["Εύκολη", "Μέτρια", "Δύσκολη"])
        self.recipe_difficulty.pack(fill="x")

        self.recipe_time_label = tk.Label(left_frame, text="Χρόνος Προετοιμασίας", anchor="w", font=("Helvetica", 13, "bold"))
        self.recipe_time_label.pack(fill="x")

        self.recipe_time = tk.Entry(left_frame)
        self.recipe_time.pack(fill="x")

        # Steps

        self.add_step_button = tk.Button(main_frame, text="Προσθήκη Βήματος", command=self.add_step)
        self.add_step_button.pack()
        # scrollable frame for steps

        self.scrolled_frame = ScrolledFrame(main_frame)
        self.scrolled_frame.pack(fill="both", expand=True)
        self.steps_frame = self.scrolled_frame.display_widget(tk.Frame, fit_width=True)

    def delete_step(self, step):
        # self.steps.remove(step)
        print(self.steps.index({ "step_number": step.step_number }))
        # self.steps.pop(self.steps.index(step))
        # self.steps = [s for s in self.steps if s != step]
        # self.render_steps()

    def get_categories(self):
        categories = list(db.RecipeCategory.select())
        return [category.name for category in categories]

    def save(self):
        # alert user that the recipe was saved
        messagebox.showinfo("Αποθήκευση", "Η συνταγή αποθηκεώθηκε επιτυχώς", parent=self)

    def add_step(self):
        self.steps.append(StepFrame(self))
        # reorderging steps

    
    def delete_step(self, step):
        self.steps.remove(step)
        step.destroy()