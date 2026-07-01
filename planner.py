import tkinter as tk
from tkinter import messagebox, colorchooser
from datetime import datetime
import json

FILENAME = "planner_data.json"
DATE_FORMAT = "%d/%m/%y"

class Subject:
    """
    Represents a school subject with a name, colour, and list of
    tasks. Holds tasks.
    Name: The display name of the subject.
    Colour: The background colour the subject would have in the UI.
    Tasks: A list containing all the tasks within this class.
    """
    def __init__(self, name, colour):
        self.name = name
        self.colour = colour
        self.tasks = []

    def __str__(self):
        '''
        Returns the subject name as a string.
        '''
        return self.name
    
    def add_task(self, task):
        '''
        Adds a task to a subject's task list.
        '''
        self.tasks.append(task)

    def remove_task(self, task):
        '''
        Removes a task from this subject's task list.
        '''
        self.tasks.remove(task)

    def convert_to_dictionary(self):
        '''
        Converts the subject and all tasks within the subject into a
        dictionary so that it's readable by JSON
        Returns a dictionary of the subject's name, colour, and tasks.
        '''
        return {
            "name": self.name,
            "colour": self.colour,
            "tasks": [task.convert_to_dictionary() for task in self.tasks]
        }


class Task:
    """
    Represents a task linked to a subject.
    Name: The title of the task.
    Description: A short description of the task.
    Due date: When this task is due in a DD/MM/YY Format.
    Completed: Whether the task is checked or not in the GUI. Defaults
    to uncompleted when first created.
    """
    def __init__(self, name, description, due_date):
        self.name = name
        self.description = description
        self.due_date = due_date
        self.completed = False

    def convert_to_dictionary(self):
        '''
        Converts the task list into a dictionary so that it is readable
        by JSON.
        Returns a dictionary containing the tasks name, description,
        due ate, and completed status.
        '''
        return {
            "name": self.name,
            "description": self.description,
            "due_date": self.due_date,
            "completed": self.completed
        }
        
class PlannerApp:
    """
    Main TKinter GUI application for the study planner.
    It manages the display of subjects and tasks, handles the user
    input through dialog windows, as well as verifying the inputs,
    and manages the saving and loading of JSON files.
    Subjects: List of Subject Objects that are loaded
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Planeroo")
        self.root.geometry("650x800")
        self.subjects = []
        self.load_data()

        self.title_label = tk.Label(root, text="Planeroo",
                                    font=("Arial", 16))
        self.title_label.pack(pady=1)   

        frame = tk.Frame(root)
        frame.pack(padx=5, pady=1)

        self.create_task_btn = tk.Button(frame,
                                        text="Create Task",
                                        command=self.create_task,
                                        width=12, height=2)
        self.create_task_btn.pack(side="left", padx=5)

        self.create_subject_btn = tk.Button(frame, 
                                            text="Create Subject",
                                            command=self.create_subject,
                                            width=12, height=2)
        self.create_subject_btn.pack(side="right", padx=5)
        

        filter_frame = tk.Frame(root)
        filter_frame.pack(pady=5)
        tk.Label(filter_frame, 
                 text="Show:"
                ).pack(side="left", padx="5")
        
        self.filter_mode = tk.StringVar(value="all")
        for label, value in [
            ("All", "all"),
            ("Complete", "complete"),
            ("Incomplete", "incomplete")
        ]:
            tk.Radiobutton(filter_frame,
                            text=label,
                            variable=self.filter_mode,
                            value=value,
                            command=self.refresh_display
                        ).pack(side="left")
            
        self.canvas = tk.Canvas(root)
        self.scrollbar = tk.Scrollbar(root, 
                                      orient="vertical",
                                      command=self.canvas.yview)
        
        # Updates the scrollable area whenever the window changes size.
        self.display_frame = tk.Frame(self.canvas)
        self.display_frame.bind(
            # Creates a function that runs whenever display_frame 
            # changes size. It updates the canvas scroll region so the
            # scrollbar knows how much content can be scrolled.
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion = self.canvas.bbox("all")
            )
        )

        self.canvas_window = self.canvas.create_window(
            (0,0), window=self.display_frame, anchor="nw")

        self.canvas.bind("<Configure>", self.resize_canvas)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True, 
                         padx=10, pady=10)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        self.refresh_display()
            
    def resize_canvas(self, event):
        '''
        Resizes the inner display frame to match the canvas width when
        the window is resized by the user.
        '''
        self.canvas.itemconfig(self.canvas_window,
                               width=event.width)
        
    def create_task(self):
        '''
        Opens the create task dialog window, and shows an error if no
        subjects exist yet, since a task must belong to a subject.
        '''
        if len(self.subjects) != 0:
            self.create_task_window = tk.Toplevel(self.root)
            self.create_task_window.title("Create a Task")
            self.create_task_window.geometry("400x200")

            label = tk.Label(self.create_task_window, text="Creating a Task")
            label.pack(pady=10)

            # Freezes main screen, makes it un-interactable while a pop
            # up window is open.
            self.create_task_window.transient(self.root)
            self.create_task_window.grab_set()

            input_frame = tk.Frame(self.create_task_window, 
                                   width=20, height=20)
            input_frame.pack(padx=3, pady=3)


            input_frame.columnconfigure(0, weight=1)
            input_frame.columnconfigure(1, weight=1)
            input_frame.columnconfigure(2, weight=1)
            input_frame.columnconfigure(3, weight=1)

            input_frame.rowconfigure(0, weight=1)
            input_frame.rowconfigure(1, weight=1)
            input_frame.rowconfigure(2, weight=1)
            input_frame.rowconfigure(3, weight=1)

            input_frame.task_title_label = tk.Label(input_frame,
                                                    text="Task Title:")
            self.task_title = tk.Entry(input_frame)
            input_frame.task_title_label.grid(column=0, row=0, padx=5)
            self.task_title.grid(column=1, row=0, padx=5)
            
            input_frame.task_description_label = tk.Label(input_frame,
                                                    text="Task Description:")
            self.task_description = tk.Entry(input_frame)
            input_frame.task_description_label.grid(column=0, row=1, padx=5)
            self.task_description.grid(column=1, row=1, padx=5)

            input_frame.task_subject_label = tk.Label(input_frame, 
                                                    text="Subject:")
            self.selected_subjects = tk.StringVar(value=self.subjects[0])
            self.task_subject = tk.OptionMenu(input_frame, 
                                            self.selected_subjects, 
                                            *self.subjects)

            input_frame.task_subject_label.grid(column=0, row=2, padx=5)
            self.task_subject.grid(column=1, row=2, padx=5)

            input_frame.task_due_date_label = tk.Label(input_frame,
                                                text="Due Date (DD/MM/YY):")
            self.task_due_date = tk.Entry(input_frame)

            input_frame.task_due_date_label.grid(column=0, row=3, padx=5)
            self.task_due_date.grid(column=1, row=3, padx=5)

            button_frame = tk.Frame(self.create_task_window,
                                    width=40, height=80)
            button_frame.submit_btn = tk.Button(button_frame, text="Add",
                                        command=self.process_task)
            button_frame.submit_btn.pack(side="left", padx=5)

            button_frame.cancel_btn = tk.Button(button_frame, 
                                                text="Cancel",
                                    command=self.create_task_window.destroy)
            
            button_frame.cancel_btn.pack(side="right", padx=5)
            button_frame.pack(pady=10)

            # Freezes main screen, makes it un-interactable while a pop
            # up window is open.
            self.root.wait_window(self.create_task_window)
        else:
            messagebox.showerror("Error", 
                                 "Please create a subject first!")

    def create_subject(self):
        '''
        Opens the create subject dialog window. Allows the user to
        enter a subject name and choose a colour using the colour
        picker.
        '''
        self.create_subject_window = tk.Toplevel(self.root)
        self.create_subject_window.title("Create a Subject")
        self.create_subject_window.geometry("400x200")

        label = tk.Label(self.create_subject_window, 
                         text="Creating a Subject")
        label.pack(pady=10)

        # Prevents the main/home window from being interactable while
        # user is in this pop-up menu.
        self.create_subject_window.transient(self.root)
        self.create_subject_window.grab_set()

        input_frame = tk.Frame(self.create_subject_window,
                                width=20, height=20)
        input_frame.pack(padx=3, pady=3)

        input_frame.columnconfigure(0, weight=1)
        input_frame.columnconfigure(1, weight=1)
        input_frame.columnconfigure(2, weight=1)
        input_frame.columnconfigure(3, weight=1)

        input_frame.rowconfigure(0, weight=1)
        input_frame.rowconfigure(1, weight=1)
        input_frame.rowconfigure(2, weight=1)
        input_frame.rowconfigure(3, weight=1)

        input_frame.subject_title_label = tk.Label(input_frame,
                                        text="Subject Name:")
        self.subject_title = tk.Entry(input_frame)

        input_frame.subject_title_label.grid(column=0, row=0, padx=5)
        self.subject_title.grid(column=1, row=0, padx=5,)
        

        self.selected_colour = "#FFFFFF"
        input_frame.subject_colour_label = tk.Label(input_frame,
                                                text="Colour:")
        self.subject_colour = tk.Button(input_frame, 
                                        text="Choose Colour",
                                        command=self.choose_colour)
        self.colour_preview = tk.Label(input_frame, 
                                       width=3, 
                                       bg=self.selected_colour)
        self.colour_preview.grid(column=2, row=3, padx=2)

        input_frame.subject_colour_label.grid(column=0, row=3, padx=2)
        self.subject_colour.grid(column=1, row=3, padx=2, pady=3)

        button_frame = tk.Frame(self.create_subject_window, 
                                width=40, height=80)
        button_frame.submit_btn = tk.Button(button_frame,
                                            text="Add",
                                    command=self.process_subject)
        button_frame.submit_btn.pack(side="left", padx=5)

        button_frame.cancel_btn = tk.Button(button_frame,
                                text="Cancel",
                                command=self.create_subject_window.destroy)
        
        button_frame.cancel_btn.pack(side="right", padx=5)
        button_frame.pack(pady=10)

        # Prevents the main/home window from being interactable while
        # user is in this pop-up menu.
        self.root.wait_window(self.create_subject_window)

    def choose_colour(self):
        '''
        Opens the system's colour picker and updates the preview window.
        If the user cancels without choosing a colour, the previously
        selected colour is used.
        '''
        colour = colorchooser.askcolor(title="Choose a subject colour!")

        if colour[1] is not None:
            self.selected_colour = colour[1]
            self.colour_preview.config(bg=self.selected_colour)


    def process_task(self):
        '''
        Validates inputs from the task creation and creates a new task
        if all inputs are valid.
        Checks that all fields are filled in and the date is correct
        before creating the task and adding it to the correct subject.
        '''
        title = self.task_title.get()
        description = self.task_description.get()
        due_date = self.task_due_date.get()
        
        if not title.strip() or not description.strip():
            messagebox.showerror("Error",
                                "Please fill out all fields!")
        else:
            date_validation = self.check_date(due_date)
            if date_validation == True:
                
                # Gets the subject name that the user has selected in
                # the drop-down menu.
                selected_name = self.selected_subjects.get()
                for subj in self.subjects:  
                    # Matches selected subject name to actual Subject
                    # object.
                    if subj.name == selected_name:
                        # Creates a new Task object from the user input.
                        homework = Task(title, description, due_date)
                        subj.add_task(homework)

                        subj.tasks.sort(
                            # Sorts tasks so that the earliest dates
                            # appear first. Lambda creates a small
                            # function that converts each task's
                            # due_date string into a datetime object so
                            # that python can compare them properly.
                            key=lambda t: datetime.strptime(t.due_date,
                                                            DATE_FORMAT)
                        )
                self.save_data()
                self.create_task_window.destroy()
                messagebox.showinfo("Planeroo",
                                    "Task successfully created!")
                self.refresh_display()

    def check_date(self, due_date):
        '''
        Validates the due date string format and checks if the date is
        real, and is not in the past. Returns a boolean where it is
        True if the date is valid and not in the past, or False if date
        date cannot exist or has already passed.
        '''
        try:
            due_date = datetime.strptime(due_date, DATE_FORMAT)
        except ValueError:
            messagebox.showerror("Error", 
                            "Please enter a valid date in DD/MM/YY format.")
            return False

        if due_date.date() < datetime.now().date():
            messagebox.showerror("Error",
                                 "Due date has already passed!")
            return False
        else:
            return True

    def process_subject(self):
        '''
        Validates task form inputs and creates a new Subject if they are
        valid. Rejects empty names and duplicated names.
        '''
        title = self.subject_title.get()
        colour = self.selected_colour

        if not title.strip():
            messagebox.showerror("Error", 
                                "Please fill out all fields!")
            return
        
        for subject in self.subjects:
            if subject.name.lower() == title.lower():
                messagebox.showerror("Error", 
                            f"Subject named {subject.name} already exists!")
                return
            
        new_subject = Subject(title, colour)
        self.subjects.append(new_subject)
        self.save_data()
        self.refresh_display()

        self.create_subject_window.destroy()
        messagebox.showinfo("Planeroo",
                        f"Subject called {title} was successfully created!")
    
    def refresh_display(self):
        '''
        Clears and puts back all subjects and their tasks on the display
        frame, updating its data.
        '''
        self.clear_display()

        for subject in self.subjects:
            self.display_subject(subject)

    def clear_display(self):
        '''
        Removes all widgets from the display frame.
        '''
        for widget in self.display_frame.winfo_children():
            widget.destroy()

    def display_subject(self, subject):
        '''
        Shows a subject's frame and all its tasks onto the display.
        Takes in a subject, which it displays.
        '''  
        subject_frame = tk.Frame(self.display_frame,
                                bg=subject.colour, 
                                relief="ridge", 
                                bd=2)
        subject_frame.pack(fill="x", pady=5, expand=True)

        header = tk.Frame(subject_frame, 
                        bg=subject.colour)
        header.pack(fill="x")

        task_count = len(subject.tasks)

        tk.Label(header, 
                text=f"{subject.name} ({task_count} tasks)", 
                bg=subject.colour, 
                font=("Arial", 12, "bold")
            ).pack(side="left", padx=5)
        
        tk.Button(
            # Creates a function that runs only when button is clicked,
            # s=subject stores the current subject so the correct
            # subject is passed onto delete_subject() instead of using
            # whatever subject is in the loop.
            header,
            text="Delete Subject",
            command=lambda s=subject: self.delete_subject(s)
        ).pack(side="right", padx=5, pady=5)

        for task in subject.tasks:
            self.display_task(subject_frame, subject, task)

    def display_task(self, parent, subject, task):
        '''
        Chooses which tasks display, depending on the current filter.
        It displays the selected tasks though, skips tasks that aren't
        selected by the filter.
        '''
        mode = self.filter_mode.get()
        if mode == "complete" and not task.completed:
            return
        if mode == "incomplete" and task.completed:
            return

        task_frame = tk.Frame(parent,
                              bg=subject.colour)
        task_frame.pack(fill="x", padx=20, pady=2, expand=True)

        top_row = tk.Frame(task_frame,
                           bg=subject.colour)
        top_row.pack(fill="x", expand=True)

        top_row.columnconfigure(0, weight=1)
        completed_var = tk.BooleanVar(value=task.completed)

        check = tk.Checkbutton(
            # Lambda lets the Checkbutton call toggle_task() with the
            # current task and Boolean Variable when clicked. t=task
            # and v=completed_var save their current values so each
            # taskbox updates with the correct task.
            top_row,
            text=f"{task.name} - {task.due_date}",
            variable=completed_var,
            bg=subject.colour,
            anchor="w",
            command = lambda t=task, v=completed_var: self.toggle_task(t,v)
        )
        check.grid(row=0, column=0, sticky="ew")

        delete = tk.Button(
            # Creates a function which runs when the button is clicked,
            # saving the current subject and task so the correct task
            # is deleted, even though the button is created in a loop.
            top_row,
            text="Delete",
            command = lambda s=subject, t=task: self.delete_task(s,t)
        )
        delete.grid(row=0, column=1, padx=5)

        tk.Label(
            task_frame,
            text=f"- {task.description}",
            bg=subject.colour,
        ).pack(side="left", padx=40)

    def _on_mousewheel(self, event):
        '''
        Scrolls on the canvas when the mouse or trackpad is used.
        '''
        first, last = self.canvas.yview()
        if first == 0.0 and last == 1.0:
            return

        self.canvas.yview_scroll(int(-1 * (event.delta /120 )), "units")

    def toggle_task(self, task, var):
        '''
        Toggles a task's completed state then saves the updated data.
        '''
        # Updates the task completion state.
        task.completed = var.get()
        self.save_data()
        self.refresh_display()

    def delete_task(self, subject, task):
        '''
        Asks the user for confirmation if they want to delete a task.
        Then deletes the task.
        '''
        # Asks the user for confirmation before deleting.
        confirm = messagebox.askyesno(
            "Delete Task",
            f"Are you sure you want to delete {task.name}?")

        if confirm:
            subject.remove_task(task)
            self.save_data()
            self.refresh_display()
    
    def delete_subject(self, subject):
        '''
        Asks the user for confirmation if they want to delete a subject,
        and all the tasks within that subject.
        '''
        confirm = messagebox.askyesno(
            "Delete Subject",
            f"Are you sure you want to delete {subject.name} and its tasks?")

        if confirm:
            self.subjects.remove(subject)
            self.save_data()
            self.refresh_display()

    
    def save_data(self):
        '''
        Puts all subjects and tasks into a JSON readable format and
        writes them into a JSON file. (planner_data.json)
        '''
        data = {
            "subjects": [subject.convert_to_dictionary() 
                         for subject in self.subjects]
        }

        with open(FILENAME, "w") as file:
            json.dump(data, file, indent=4)

    def load_data(self):
        '''
        Loads subjects and tasks from planner_data.json if the file
        exists. If no file is present, then a new one is created, but
        if the file is corrupted, then it informs the user and creates a
        new file.   
        '''
        try:
            with open(FILENAME, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            messagebox.showinfo("Planeroo",
                                "Welcome! Create a subject to get started")
            return
        except json.JSONDecodeError:
            messagebox.showerror(
                "Error",
                ("The planner data file is corrupted. "
                "A new planner will be started.")
            )
            self.save_data()
            return
        
        for subject_data in data["subjects"]:
            subject = Subject(
                subject_data["name"],
                subject_data["colour"],
            )
            self.subjects.append(subject)

            # Rebuilds Task objects and attaches them to the correct
            # subject.
            for task_data in subject_data["tasks"]:
                task = Task(
                    task_data["name"],
                    task_data["description"],
                    task_data["due_date"]
                )
                task.completed = task_data["completed"]
                subject.add_task(task)

if __name__ == "__main__":
    main_window = tk.Tk()
    app = PlannerApp(main_window)
    main_window.mainloop()