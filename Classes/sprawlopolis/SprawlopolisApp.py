import types

from Classes.base.apps import BaseApp
from Classes.base.boardstate import BaseBoardstate
from Classes.sprawlopolis.SprawlopolisBoardstate import SprawlopolisBoardstate


class SprawlopolisApp(BaseApp):
    def __init__(self, chosen_game_name):
        super().__init__(chosen_game_name)

        print(
            f"Typ von play_card in boardstate: {type(self.model.boardstate.play_card)}"
        )
        print(
            f"Ist play_card eine Methode: {hasattr(self.model.boardstate.play_card, '__self__')}"
        )
        print(f"MRO von SprawlopolisBoardstate: {SprawlopolisBoardstate.__mro__}")
        print(
            f"play_card in SprawlopolisBoardstate: {SprawlopolisBoardstate.play_card}"
        )
        print(f"play_card in BaseBoardstate: {BaseBoardstate.play_card}")

        self.model.boardstate.play_card = types.MethodType(
            BaseBoardstate.play_card, self.model.boardstate
        )

        self.model.boardstate.play_card(card_id=15, position=(18, 30))
