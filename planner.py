import tkinter as tk
from tkinter import messagebox
import json

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
        create_task_window.geometry("250x150")

        label = tk.Label(create_task_window, text="Creating a Task")
        label.pack(pady=10)


        frame = tk.Frame(create_task_window, width=200, height=200)
        self.task_title_label = tk.Label(create_task_window, text="Task Title:")
        self.task_title = tk.Entry(create_task_window)
        self.task_title_label.pack(padx=20, side="left")
        self.task_title.pack(padx=20, side="right")

        self.task_description_label = tk.Label(create_task_window, text="Task Description:")
        self.task_description = tk.Entry(create_task_window)
        self.task_description_label.pack(padx=20, side="left")
        self.task_description.pack(padx=20, side="right")


        self.submit_btn = tk.Button(self.create_task_window, text="Add",
                                    command = self.process_decision)
        self.submit_btn.pack(pady=10)
        self.cancel_btn = tk.Button(self.create_task_window, text="Cancel",
                                    command = self.process_decision)
        self.cancel_btn.pack(pady=10)

    def create_subject():
        pass



if __name__ == "__main__":
    main_window = tk.Tk()
    app = PlannerApp(main_window)
    main_window.mainloop()

    