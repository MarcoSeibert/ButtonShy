from Classes.base.models import BaseModel
from Classes.base.views import StartView, BaseView
from functions import start_game
from start_up import games_dict


class StartController:
    def __init__(self, view: StartView):
        self.view = view

    def click_play(self) -> None:
        chosen_game = self.view.chosen_game.get()
        chosen_game_name = games_dict[chosen_game].replace(" ", "")
        start_game(self.view.master, chosen_game_name)


class BaseController:
    def __init__(self, model: BaseModel, view: BaseView):
        self.model = model
        self.view = view
        self.grid_size = model.game_data["grid_size"]

        self.view.master.bind("<Escape>", self.quit)

    def click_on_card(self, args):
        pass

    def quit(self, _) -> None:
        self.view.master.destroy()
