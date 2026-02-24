import tkinter as tk
from tkinter import ttk

from globals import TITLE_FONT, BASIC_FONT


# Model
class OptionsModel:
    def __init__(self):
        self.options = {}
        self.difficulty = "Normal"

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty
        self.options["difficulty"] = difficulty


# View
class OptionsView(tk.Toplevel):
    def __init__(self, parent: tk.Tk, game_name: str) -> None:
        super().__init__(parent)
        self.parent = parent
        self.game_name = game_name
        self.controller = None

        self.title(f"Options for {game_name}")
        
        # Get screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Calculate position to center the window
        window_width = 400
        window_height = 300
        offset_x = (screen_width - window_width) // 2
        offset_y = (screen_height - window_height) // 2
        
        # Set geometry with position
        self.geometry(f"{window_width}x{window_height}+{offset_x}+{offset_y}")
        self.resizable(False, False)

        # Configure grid
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Configure styles
        style_buttons = ttk.Style()
        my_button_style = "MyButton.TButton"
        style_buttons.configure(my_button_style, font=BASIC_FONT)
        radio_style_buttons = ttk.Style()
        my_radio_button_style = "MyRadioButton.Toolbutton"
        radio_style_buttons.configure(
            my_radio_button_style, font=BASIC_FONT, background="white", anchor="c"
        )
        radio_style_buttons.map(
            my_radio_button_style,
            foreground=[("selected", "black"), ("!selected", "grey")],
        )

        # Insert title
        ttk.Label(self, text=f"Options for {game_name}", font=TITLE_FONT).grid(
            column=0, row=0, pady=10
        )

        # Add widgets for game options here
        # For example, a checkbox for difficulty level
        ttk.Label(self, text="Difficulty Level:", font=BASIC_FONT).grid(
            column=0, row=1, pady=10
        )
        self.difficulty_var = tk.StringVar(value="Normal")
        self.difficulty_combobox = ttk.Combobox(
            self, textvariable=self.difficulty_var, values=["Easy", "Normal", "Hard"], font=BASIC_FONT
        )
        self.difficulty_combobox.grid(column=0, row=2, pady=10)

        # Add a button to confirm the options
        self.confirm_button = ttk.Button(self, text="Confirm", style=my_button_style, command=self.on_confirm)
        self.confirm_button.grid(column=0, row=3, pady=20)

    def set_controller(self, controller):
        self.controller = controller

    def on_confirm(self):
        if self.controller:
            self.controller.on_confirm()


# Controller
class OptionsController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.set_controller(self)

    def on_confirm(self):
        difficulty = self.view.difficulty_var.get()
        self.model.set_difficulty(difficulty)
        self.view.destroy()


# Factory class to create and manage the MVC components
class OptionsWindow:
    def __init__(self, parent: tk.Tk, game_name: str) -> None:
        self.model = OptionsModel()
        self.view = OptionsView(parent, game_name)
        self.controller = OptionsController(self.model, self.view)
        self.view.mainloop()

    def get_options(self):
        return self.model.options