import json
import tkinter as tk
from Classes.base.controllers import StartController, BaseController
from Classes.base.views import StartView, BaseView
from Classes.base.models import BaseModel
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
        self.geometry(f"{self.window_width}x{self.window_height}+{self.offset_x}+{self.offset_y}")
        self.resizable(False, False)
        # self.iconbitmap("Resources/Icon.ico")


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
        app_game = BaseApp(chosen_game)
        app_game.focus_force()
        app_game.mainloop()


class BaseApp(App):
    def __init__(self, chosen_game):
        super().__init__(1E6, 1E6, 0)
        self.attributes("-fullscreen", True)
        self.chosen_game = chosen_game
        with open("Resources/Games.json") as json_file:
            json_data = json.load(json_file)["games"]
        self.game_data = get_game_data_by_name(json_data, games_dict[self.chosen_game])
        print(self.game_data)
        self.start_up()

    def start_up(self):
        # set up model
        base_model = BaseModel(self.game_data)

        # set up view
        base_view = BaseView(self)
        base_view.grid(row=0, column=0, pady=10, padx=10)

        # set up controller
        base_controller = BaseController(base_model, base_view)
        base_view.set_controller(base_controller)
