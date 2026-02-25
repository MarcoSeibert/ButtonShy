import json
import tkinter as tk
from datetime import datetime

from Classes.base.events import ModelObserver, ModelEvent
from Classes.base.models import BaseModel
from Classes.base.views import StartView, BaseView
from Classes.sprawlopolis.options_window import OptionsWindow
from Utils.functions import start_game
from Utils.start_up import games_dict


class StartController:
    def __init__(self, view: StartView) -> None:
        self.view = view

    def click_play(self) -> None:
        chosen_game = self.view.chosen_game.get()
        chosen_game_name = games_dict[chosen_game].replace(" ", "")
        # Show the options window
        if chosen_game_name == "Sprawlopolis":
            options_window = OptionsWindow(self.view.master, chosen_game_name)
            options_window.view.focus_force()
            self.view.master.wait_window(options_window.view)
            options = options_window.get_options()
        else:
            options = None
        start_game(self.view.master, chosen_game_name, options)


class BaseController(ModelObserver):
    def __init__(self, model: BaseModel, view: BaseView) -> None:
        self.model = model
        self.view = view
        self.model.add_observer(self)

        self.grid_size = model.game_data["grid_size"]
        self.view.master.bind("<Escape>", self.quit)

    def on_model_change(self, event: ModelEvent) -> None:
        raise NotImplementedError()

    def quit(self, _) -> None:
        self.view.master.destroy()

    def show_result_window(self, result: str) -> None:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        result_data = {
            "game": self.model.game_data["name"],
            "date": current_time,
            "result": result,
        }
        try:
            with open("game_results.json", "r") as f:
                results = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            results = []
        results.append(result_data)
        with open("game_results.json", "w") as f:
            json.dump(results, f, indent=4)

        result_window = tk.Toplevel()
        result_window.title("Game Result")
        label = tk.Label(result_window, text=f"Game Over: {result}")
        label.pack()
        close_button = tk.Button(
            result_window, text="Close", command=result_window.destroy
        )
        close_button.pack()
