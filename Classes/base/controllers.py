from Classes.base.models import BaseModel
from Classes.base.views import StartView, BaseView


class StartController:
    def __init__(self, view: StartView):
        self.view = view

    def click_play(self):
        chosen_game = self.view.chosen_game.get()
        self.view.master.start_game(chosen_game)

class BaseController:
    def __init__(self, model: BaseModel, view: BaseView):
        self.model = model
        self.view = view
