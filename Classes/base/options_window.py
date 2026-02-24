import tkinter as tk
from tkinter import ttk


class OptionsWindow(tk.Toplevel):
    def __init__(self, parent, game_name):
        super().__init__(parent)
        self.parent = parent
        self.game_name = game_name
        self.options = {}

        self.title(f"Options for {game_name}")
        self.geometry("400x300")
        self.resizable(False, False)

        # Add widgets for game options here
        # For example, a checkbox for difficulty level
        self.difficulty_var = tk.StringVar(value="Normal")
        ttk.Label(self, text="Difficulty Level:").pack(pady=10)
        ttk.Combobox(self, textvariable=self.difficulty_var, values=["Easy", "Normal", "Hard"]).pack(pady=10)

        # Add a button to confirm the options
        self.confirm_button = ttk.Button(self, text="Confirm", command=self.on_confirm)
        self.confirm_button.pack(pady=20)

    def on_confirm(self):
        # Store the selected options
        self.options = {
            "difficulty": self.difficulty_var.get()
        }
        # Close the window
        self.destroy()