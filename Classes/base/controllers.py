from Classes.base.events import ModelObserver, ModelEvent
from Classes.base.models import BaseModel
from Classes.base.views import StartView, BaseView
from functions import start_game
from start_up import games_dict


class StartController:
    def __init__(self, view: StartView) -> None:
        self.view = view

    def click_play(self) -> None:
        chosen_game = self.view.chosen_game.get()
        chosen_game_name = games_dict[chosen_game].replace(" ", "")
        start_game(self.view.master, chosen_game_name)


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
