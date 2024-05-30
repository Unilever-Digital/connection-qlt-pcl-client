import tkinter as tk
from tkinter import messagebox

class HomeApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Set window title and size
        self.title("Quality server")
        self.geometry("400x200")  # Adjust window size as needed

        # Initialize UI elements
        self.init_ui()

    def init_ui(self):
        # Create labels
        self.label_background = tk.Label(self, text="Quality server")
        self.label_background.grid(row=0, column=0, columnspan=2, sticky="nsew")  # Adjust grid layout as needed

        self.label_privacy = tk.Label(self, text="Privacy @2023", fg="black")
        self.label_privacy.grid(row=1, column=1, sticky="se")  # Adjust grid layout as needed

        # ... (add more UI elements using Tkinter widgets like Button, Entry, etc.)

    def close(self, event=None):
        # Confirmation dialog before closing
        if messagebox.askquestion("Quit?", "Are you sure you want to quit?") == "yes":
            super().destroy()  # Close the window