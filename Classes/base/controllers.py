from tkinter import Event

from Classes.base.models import BaseModel
from Classes.base.views import StartView, BaseView
from Classes.events import BoardStateEvent


class StartController:
    def __init__(self, view: StartView):
        self.view = view

    def click_play(self) -> None:
        chosen_game = self.view.chosen_game.get()
        self.view.master.start_game(chosen_game)


class BaseController:
    def __init__(self, model: BaseModel, view: BaseView):
        self.model = model
        self.view = view
        self.model.add_observer(self)
        self.grid_size = model.game_data["grid_size"]

        self.view.master.bind("<Escape>", self.quit)

    def click_on_card(self, args):
        pass

    def quit(self, _) -> None:
        self.view.master.destroy()

    def on_boardstate_change(self, event: BoardStateEvent):
        """Wird aufgerufen, wenn sich der BoardState ändert."""
        if event.type == "CARD_PLAYED":
            print(
                f"Controller: Karte {event.data['card_id']} auf {event.data['position']} gespielt!"
            )
            # Hier die View aktualisieren, z. B.:
            # self.view.update_card(event.data["card_id"], event.data["position"]
