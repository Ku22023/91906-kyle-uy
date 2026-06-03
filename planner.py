import tkinter as tk
from tkinter import messagebox
import json

tasks = []
subjects = []

class Subject:
    """
    """
    def __init__(self, name, colour):
        self.name = name
        self.colour = colour

class Task:
    """
    """
    def __init__(self, subject, name, description, due_date):
        self.subject = subject
        self.name = name
        self.description = description
        self.due_date = due_date

class PlannerApp:
    """
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Planeroo")
        self.root.geometry("650x800")

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
        create_task_window = tk.Toplevel(self.root)
        create_task_window.title("Create a Task")
        create_task_window.geometry("400x200")


        #Title Frame
        label = tk.Label(create_task_window, text="Creatingiuuyy a Task")
        label.pack(pady=10)


        #Frame with all the information collection
        input_frame = tk.Frame(create_task_window, width=20, height=20)
        input_frame.pack(padx=3, pady=3)


        input_frame.columnconfigure(0, weight=1)
        input_frame.columnconfigure(1, weight=1)
        input_frame.columnconfigure(2, weight=1)

        input_frame.rowconfigure(0, weight=1)
        input_frame.rowconfigure(1, weight=1)
        input_frame.rowconfigure(2, weight=1)

        input_frame.task_title_label = tk.Label(input_frame, \
                                         text="Task Title:")
        input_frame.task_title = tk.Entry(input_frame)

        input_frame.task_title_label.grid(column=0, row=0, padx=5)
        input_frame.task_title.grid(column=1, row=0, padx=5,)
        

        input_frame.task_description_label = tk.Label(input_frame, \
                                               text="Task Description:")
        input_frame.task_description = tk.Entry(input_frame)

        input_frame.task_description_label.grid(column=0, row=1, padx=5,)
        input_frame.task_description.grid(column=1, row=1, padx=5)

        input_frame.task_due_date_label = tk.Label(input_frame, \
                                                   text="Due Date (DD/MM/YY):")
        input_frame.task_due_date = tk.Entry(input_frame)

        input_frame.task_due_date_label.grid(column=0, row=2, padx=5)
        input_frame.task_due_date.grid(column=1, row=2, padx=5)
        input_frame.pack()


        #Frame with buttons to cancel or Continue
        button_frame = tk.Frame(create_task_window, width=40, height=80)
        button_frame.submit_btn = tk.Button(button_frame, text="Add",
                                    command = self.process_decision)
        button_frame.submit_btn.pack(side="left", padx=5)

        button_frame.cancel_btn = tk.Button(button_frame, \
                                    text="Cancel",
                                    command = self.process_decision)
        
        button_frame.cancel_btn.pack(side="right", padx=5)
        button_frame.pack(pady=10)



    def create_subject(self):
        pass

    def process_decision(self):
        print("hello")


class CreateWindow:
    pass



if __name__ == "__main__":
    main_window = tk.Tk()
    app = PlannerApp(main_window)
    main_window.mainloop()

    