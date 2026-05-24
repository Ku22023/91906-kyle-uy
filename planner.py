import tkinter as tk
from tkinter import messagebox
import json

class Subject:
    """
    """
    def __init__(self, name, colour):
        self.name = name
        self.colour = colour

class PlannerApp:
    """
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Planeroo")
        self.root.geometry("650x800")

        self.title_label = tk.Label(root, text="Planeroo", \
                                    font=("Arial", 16))
        self.title.pack(pady=10)


        self.create_task_btn = tk.Button(root, text="Create Task",
                                          command=self.create_task)
        self.create_task_btn.pack(side="left", padx=20, pady=20)

    