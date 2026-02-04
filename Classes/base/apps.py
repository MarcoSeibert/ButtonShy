import json
import tkinter as tk
from importlib import import_module

from Classes.base.controllers import StartController
from Classes.base.views import StartView
from functions import get_game_data_by_name
from start_up import games_dict


class App(tk.Tk):
    def __init__(self, factor_x: float, factor_y: float, offset_factor_y: float = 1):
        super().__init__()

        # get some measurements
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.window_width = int(screen_width / factor_x)
        self.window_height = int(screen_height / factor_y)
        self.offset_x = (screen_width - self.window_width) // 2
        self.offset_y = offset_factor_y * (screen_height - self.window_height) // 2

        # set up basic parameters
        self.title("Button Shy Games")
        self.geometry(
            f"{self.window_width}x{self.window_height}+{self.offset_x}+{self.offset_y}"
        )
        self.resizable(False, False)
        # self.iconbitmap("Resources/Icon.ico")

        self.game_data = None
        self.chosen_game = None


class StartApp(App):
    def __init__(self):
        super().__init__(4, 2)

        # set up view
        view_start = StartView(self)
        view_start.grid(row=0, column=0, pady=10, padx=10)
        view_start.place(in_=self, anchor="c", relx=0.5, rely=0.5)

        # set up controller
        controller_start = StartController(view_start)
        view_start.set_controller(controller_start)

    def start_game(self, chosen_game):
        self.destroy()
        chosen_game_name = games_dict[chosen_game].replace(" ", "")
        app_class = getattr(
            import_module(f"Classes.{chosen_game_name.lower()}.{chosen_game_name}App"),
            f"{chosen_game_name}App",
        )
        app_game = app_class(chosen_game_name)
        app_game.focus_force()
        app_game.mainloop()


class BaseApp(App):
    def __init__(self, chosen_game_name):
        super().__init__(1e6, 1e6, 0)
        self.model = None
        self.view = None
        self.controller = None
        self.attributes("-fullscreen", True)
        with open("Resources/Games.json") as json_file:
            json_data = json.load(json_file)["games"]
        self.game_data = get_game_data_by_name(json_data, chosen_game_name)
        self.chosen_game = self.game_data["name"]
        self.chosen_game_compact = self.chosen_game.replace(" ", "")
        self.start_up()

    def start_up(self):
        # import the classes
        components = self.game_data["mvc_components"]
        model_class = getattr(
            import_module(
                f"Classes.{self.chosen_game_compact.lower()}.{self.chosen_game_compact}Model"
            ),
            components["model"],
        )
        controller_class = getattr(
            import_module(
                f"Classes.{self.chosen_game_compact.lower()}.{self.chosen_game_compact}Controller"
            ),
            components["controller"],
        )
        view_class = getattr(
            import_module(
                f"Classes.{self.chosen_game_compact.lower()}.{self.chosen_game_compact}View"
            ),
            components["view"],
        )

        # set up model
        self.model = model_class(self.game_data)

        # set up view
        self.view = view_class(self)
        self.view.grid(row=0, column=0, pady=10, padx=10)

        # set up controller
        self.controller = controller_class(self.model, self.view)
        self.view.set_controller(self.controller)
