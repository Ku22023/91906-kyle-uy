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
    
    def add_task(self, task):
        self.tasks.append(task)

    def remove_task(self, task):
        self.tasks.remove(task)

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
        

class PlannerApp:
    """
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Planeroo")
        self.root.geometry("650x800")
        self.tasks = {}
        self.subjects = []

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
        
    def create_task(self):
        if len(self.subjects) != 0:
            create_task_window = tk.Toplevel(self.root)
            create_task_window.title("Create a Task")
            create_task_window.geometry("400x200")


            #Title Frame
            label = tk.Label(create_task_window, text="Creating a Task")
            label.pack(pady=10)

            # Freezes main screen
            create_task_window.transient(self.root)
            create_task_window.grab_set()


            #Frame with all the information collection
            input_frame = tk.Frame(create_task_window, width=20, height=20)
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
            subject_names = [subject.name for subject in self.subjects]
            self.selected_subjects = tk.StringVar(value=subject_names[0])

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
            button_frame = tk.Frame(create_task_window, width=40, height=80)
            button_frame.submit_btn = tk.Button(button_frame, text="Add",
                                        command = self.process_decision)
            button_frame.submit_btn.pack(side="left", padx=5)

            button_frame.cancel_btn = tk.Button(button_frame, \
                                        text="Cancel",
                                        command = create_task_window.destroy)
            
            button_frame.cancel_btn.pack(side="right", padx=5)
            button_frame.pack(pady=10)

            #Freezes main window when popup opened
            self.root.wait_window(create_task_window)
        else:
            messagebox.showerror("error", "please create a subject first!")

    def create_subject(self):
        create_subject_window = tk.Toplevel(self.root)
        create_subject_window.title("Create a Subject")
        create_subject_window.geometry("400x200")


        #Title Frame
        label = tk.Label(create_subject_window, text="Creating a Task")
        label.pack(pady=10)

        # Freezes main screen
        create_subject_window.transient(self.root)
        create_subject_window.grab_set()


        #Frame with all the information collection
        input_frame = tk.Frame(create_subject_window, width=20, height=20)
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
                                        text="Subject Name:")
        self.task_title = tk.Entry(input_frame)

        input_frame.task_title_label.grid(column=0, row=0, padx=5)
        self.task_title.grid(column=1, row=0, padx=5,)
        


        input_frame.task_description_label = colorchooser.askcolor(input_frame)
        self.task_description = tk.Entry(input_frame)

        input_frame.task_description_label.grid(column=0, row=1, padx=5,)
        self.task_description.grid(column=1, row=1, padx=5)



        input_frame.task_due_date_label = tk.Label(input_frame, \
                                                text="Due Date (DD/MM/YY):")
        self.task_due_date = tk.Entry(input_frame)

        input_frame.task_due_date_label.grid(column=0, row=3, padx=5)
        self.task_due_date.grid(column=1, row=3, padx=5)
        input_frame.pack()


        #Frame with buttons to cancel or Continue
        button_frame = tk.Frame(create_subject_window, width=40, height=80)
        button_frame.submit_btn = tk.Button(button_frame, text="Add",
                                    command = self.process_decision)
        button_frame.submit_btn.pack(side="left", padx=5)

        button_frame.cancel_btn = tk.Button(button_frame, \
                                    text="Cancel",
                                    command = create_subject_window.destroy)
        
        button_frame.cancel_btn.pack(side="right", padx=5)
        button_frame.pack(pady=10)

        #Freezes main window when popup opened
        self.root.wait_window(create_subject_window)

    def choose_colour(self):
        colour = colorchooser.askcolor()[1]
        if colour:
            self.selected_colour = colour
        


    def process_decision(self):
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
            if date_validation == 1:
                messagebox.showinfo("Planeroo", "Task successfully created!")

                homework = Task(title, description, due_date)
                subject.tasks.append(homework)

        



    def check_date(self, due_date):
        try:
            due_date = datetime.strptime(due_date, "%d/%m/%y")
        except ValueError:
            messagebox.showerror("error", "please enter a valid date in DD/MM/YY format.")
            return 0

        if due_date.date() < datetime.now().date():
            messagebox.showerror("error", "due date has already passed!")
            return 0
        else:
            return 1





if __name__ == "__main__":
    main_window = tk.Tk()
    app = PlannerApp(main_window)
    main_window.mainloop()

    