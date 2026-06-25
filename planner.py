import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from tkinter import colorchooser
import json



class Subject:
    """
    """
    def __init__(self, name, colour):
        self.name = name
        self.colour = colour
        self.tasks = []

    def __str__(self):
        return self.name
    
    def add_task(self, task):
        self.tasks.append(task)

    def remove_task(self, task):
        self.tasks.remove(task)

    def convert_to_dictionary(self):
        return {
            "name": self.name,
            "colour": self.colour,
            "tasks": [task.convert_to_dictionary() for task in self.tasks]
        }


class Task:
    """
    """
    def __init__(self, subject, name, description, due_date):
        self.subject = subject
        self.name = name
        self.description = description
        self.due_date = due_date
        self.completed = False
    def mark_complete(self):
        self.completed = True
    def convert_to_dictionary(self):
        return {
            "name": self.name,
            "description": self.description,
            "due_date": self.due_date,
            "completed": self.completed
        }
        

class PlannerApp:
    """
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Planeroo")
        self.root.geometry("650x800")
        self.subjects = []
        self.load_data()

        self.title_label = tk.Label(root, text="Planeroo", \
                                    font=("Arial", 16))
        self.title_label.pack(pady=10)

        frame = tk.Frame(root, width=200, height=200)
        frame.pack(padx=10, pady=10)

        self.create_task_btn = tk.Button(frame, text="Create Task",
                                          command=self.create_task,
                                          width=15, 
                                          height=3)
        self.create_task_btn.pack(side="left", 
                                  padx=5, pady=5)

        self.create_subject_btn = tk.Button(frame, 
                                            text="Create Subject",
                                            command=self.create_subject,
                                            width=15, 
                                            height=3)
        self.create_subject_btn.pack(side="right", 
                                    padx=5, pady=5)
        
        subject_display = tk.Frame(self.root, width=20, height=20)
        subject_display.pack(padx=3, pady=3)


        subject_display.columnconfigure(0, weight=1)

        filter_frame = tk.Frame(root)
        filter_frame.pack(pady=5)
        tk.Label(filter_frame, text="Show:").pack(side="left", padx="5")
        self.filter_mode = tk.StringVar(value="all")
        for label, value in [
            ("All", "all"),
            ("Complete", "complete"),
            ("Incomplete", "incomplete")
        ]:
            tk.Radiobutton(filter_frame, text=label, variable=self.filter_mode, value=value,
                           command=self.refresh_display).pack(side="left")
        self.display_frame = tk.Frame(root)
        self.display_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.refresh_display()
            

        
    def create_task(self):
        if len(self.subjects) != 0:
            self.create_task_window = tk.Toplevel(self.root)
            self.create_task_window.title("Create a Task")
            self.create_task_window.geometry("400x200")


            #Title Frame
            label = tk.Label(self.create_task_window, text="Creating a Task")
            label.pack(pady=10)

            # Freezes main screen
            self.create_task_window.transient(self.root)
            self.create_task_window.grab_set()


            #Frame with all the information collection
            input_frame = tk.Frame(self.create_task_window, width=20, height=20)
            input_frame.pack(padx=3, pady=3)


            input_frame.columnconfigure(0, weight=1)
            input_frame.columnconfigure(1, weight=1)
            input_frame.columnconfigure(2, weight=1)
            input_frame.columnconfigure(3, weight=1)

            input_frame.rowconfigure(0, weight=1)
            input_frame.rowconfigure(1, weight=1)
            input_frame.rowconfigure(2, weight=1)
            input_frame.rowconfigure(3, weight=1)

            input_frame.task_title_label = tk.Label(input_frame, \
                                            text="Task Title:")
            self.task_title = tk.Entry(input_frame)

            input_frame.task_title_label.grid(column=0, row=0, padx=5)
            self.task_title.grid(column=1, row=0, padx=5,)
            

            input_frame.task_description_label = tk.Label(input_frame, \
                                                text="Task Description:")
            self.task_description = tk.Entry(input_frame)

            input_frame.task_description_label.grid(column=0, row=1, padx=5,)
            self.task_description.grid(column=1, row=1, padx=5)


            input_frame.task_subject_label = tk.Label(input_frame, text="Subject:")
            self.selected_subjects = tk.StringVar(value=self.subjects[0])
            self.task_subject = tk.OptionMenu(input_frame, self.selected_subjects, *self.subjects)
            self.task_subject.grid(column=1, row=2, padx=5)


            input_frame.task_subject_label.grid(column=0, row=2, padx=5)
            self.task_subject.grid(column=1, row=2, padx=5)


            input_frame.task_due_date_label = tk.Label(input_frame, \
                                                    text="Due Date (DD/MM/YY):")
            self.task_due_date = tk.Entry(input_frame)

            input_frame.task_due_date_label.grid(column=0, row=3, padx=5)
            self.task_due_date.grid(column=1, row=3, padx=5)
            input_frame.pack()


            #Frame with buttons to cancel or Continue
            button_frame = tk.Frame(self.create_task_window, width=40, height=80)
            button_frame.submit_btn = tk.Button(button_frame, text="Add",
                                        command = self.process_task)
            button_frame.submit_btn.pack(side="left", padx=5)

            button_frame.cancel_btn = tk.Button(button_frame, \
                                        text="Cancel",
                                        command = self.create_task_window.destroy)
            
            button_frame.cancel_btn.pack(side="right", padx=5)
            button_frame.pack(pady=10)

            #Freezes main window when popup opened
            self.root.wait_window(self.create_task_window)
        else:
            messagebox.showerror("error", "please create a subject first!")

    def create_subject(self):
        self.create_subject_window = tk.Toplevel(self.root)
        self.create_subject_window.title("Create a Subject")
        self.create_subject_window.geometry("400x200")


        #Title Frame
        label = tk.Label(self.create_subject_window, text="Creating a Subject")
        label.pack(pady=10)

        # Freezes main screen
        self.create_subject_window.transient(self.root)
        self.create_subject_window.grab_set()


        #Frame with all the information collection
        input_frame = tk.Frame(self.create_subject_window, width=20, height=20)
        input_frame.pack(padx=3, pady=3)


        input_frame.columnconfigure(0, weight=1)
        input_frame.columnconfigure(1, weight=1)
        input_frame.columnconfigure(2, weight=1)
        input_frame.columnconfigure(3, weight=1)

        input_frame.rowconfigure(0, weight=1)
        input_frame.rowconfigure(1, weight=1)
        input_frame.rowconfigure(2, weight=1)
        input_frame.rowconfigure(3, weight=1)

        input_frame.subject_title_label = tk.Label(input_frame, \
                                        text="Subject Name:")
        self.subject_title = tk.Entry(input_frame)

        input_frame.subject_title_label.grid(column=0, row=0, padx=5)
        self.subject_title.grid(column=1, row=0, padx=5,)
        
        self.selected_colour = "#FFFFFF"


        input_frame.subject_colour_label = tk.Label(input_frame, \
                                                text="Colour:")
        self.subject_colour = tk.Button(input_frame, text="Choose Colour",
                                        command=self.choose_colour)
        self.colour_preview = tk.Label(input_frame, width=3, bg=self.selected_colour)
        self.colour_preview.grid(column=2, row=3, padx=2)

        input_frame.subject_colour_label.grid(column=0, row=3, padx=2)
        self.subject_colour.grid(column=1, row=3, padx=2, pady=3)
        input_frame.pack()


        #Frame with buttons to cancel or Continue
        button_frame = tk.Frame(self.create_subject_window, width=40, height=80)
        button_frame.submit_btn = tk.Button(button_frame, text="Add",
                                    command = self.process_subject)
        button_frame.submit_btn.pack(side="left", padx=5)

        button_frame.cancel_btn = tk.Button(button_frame, \
                                    text="Cancel",
                                    command = self.create_subject_window.destroy)
        
        button_frame.cancel_btn.pack(side="right", padx=5)
        button_frame.pack(pady=10)


        #Freezes main window when popup opened
        self.root.wait_window(self.create_subject_window)

    def choose_colour(self):
        colour = colorchooser.askcolor(title="Choose a colour for the subject!")

        if colour[1] is not None:
            self.selected_colour = colour[1]
            self.colour_preview.config(bg=self.selected_colour)


    def process_task(self):
        '''
        Makes sure all the data is correct and valid. 
        '''
        title = self.task_title.get()
        description = self.task_description.get()
        due_date = self.task_due_date.get()
        subject = self.selected_subjects.get()
        

            
        if len(title.strip()) == 0 or len(description.strip()) == 0:
            messagebox.showerror("error", "Please enter into all fields!")
        else:
            date_validation = self.check_date(due_date)
            if date_validation == True:

                homework = Task(subject, title, description, due_date)
                selected_name = self.selected_subjects.get()
                for subj in self.subjects:  
                    if subj.name == selected_name:
                        subj.add_task(homework)
                self.save_data()
                self.create_task_window.destroy()
                messagebox.showinfo("Planeroo", "Task successfully created!")
                self.refresh_display()


    def check_date(self, due_date):
        try:
            due_date = datetime.strptime(due_date, "%d/%m/%y")
        except ValueError:
            messagebox.showerror("error", "please enter a valid date in DD/MM/YY format.")
            return 0

        if due_date.date() < datetime.now().date():
            messagebox.showerror("error", "due date has already passed!")
            return False
        else:
            return True

    def process_subject(self):
        '''
        Makes sure all the data is correct and valid. 
        '''
        title = self.subject_title.get()
        colour = self.selected_colour
        

        if len(title.strip()) == 0:
            messagebox.showerror("error", "Please enter into all fields!")
            return
        
        for subject in self.subjects:
            if subject.name.lower() == title.lower():
                messagebox.showerror("error", "subject already exists!")
                return
        new_subject = Subject(title, colour)
        self.subjects.append(new_subject)
        self.save_data()
        self.refresh_display()

        self.create_subject_window.destroy()
        messagebox.showinfo("Planeroo", "Subject successfully created!")
    
    def save_data(self):
        data = {
            "subjects": [subject.convert_to_dictionary() for subject in self.subjects]
        }

        with open("planner_data.json", "w") as file:
            json.dump(data,file, indent=4)

    def load_data(self):
        try:
            with open("planner_data.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            return
        for subject_data in data["subjects"]:
            subject = Subject(
                subject_data["name"],
                subject_data["colour"],
            )
            self.subjects.append(subject)
    
            for task_data in subject_data["tasks"]:
                task = Task(
                    subject.name,
                    task_data["name"],
                    task_data["description"],
                    task_data["due_date"]
                )
                task.completed = task_data["completed"]
                subject.add_task(task)
    
    def refresh_display(self):
        for widget in self.display_frame.winfo_children():
            widget.destroy()

        for subject in self.subjects:
            subject_frame = tk.Frame(self.display_frame, bg=subject.colour, relief="ridge", bd=2)
            subject_frame.pack(fill="x", pady=5)
            tk.Label(subject_frame, 
                     text=subject.name, 
                     bg=subject.colour, 
                     font=("Arial", 12, "bold")
                ).pack(anchor="w", padx=5, pady=2)

            for task in subject.tasks:
                status = "✓" if task.completed else "x"
                tk.Label(subject_frame, 
                         text=f"{status} {task.name} - {task.due_date} \n {task.description}",
                        bg=subject.colour
                    ).pack(anchor="w", padx=20)

    def toggle_task(self, task, var):
        task.completed = bool(var.get)
        self.save_data()
        self.refresh_display


if __name__ == "__main__":
    main_window = tk.Tk()
    app = PlannerApp(main_window)
    main_window.mainloop()

    