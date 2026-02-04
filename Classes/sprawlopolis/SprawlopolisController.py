from Classes.base.controllers import BaseController
from Classes.canvasgamecontroller import CanvasGameController
from Classes.sprawlopolis.SprawlopolisModel import SprawlopolisModel
from Classes.sprawlopolis.SprawlopolisView import SprawlopolisView

from tkinter import ttk
import pywinstyles

from globals import LEFT_MOUSE_BUTTON


class SprawlopolisController(BaseController, CanvasGameController):
    def __init__(self, model: SprawlopolisModel, view: SprawlopolisView):
        BaseController.__init__(self, model, view)
        CanvasGameController.__init__(self, model, view)

        # add scoring cards to the grid
        self.scoring_card = ttk.Label(self.view.score_area)
        self.scoring_card = ttk.Label(self.view.score_area)
        self.scoring_card = ttk.Label(self.view.score_area)
        for i, card in enumerate(self.view.score_area.winfo_children()):
            card.grid(column=13, row=4 * i + 1, columnspan=2, rowspan=4)
        # add images to the cards
        for i, card in enumerate(self.view.score_area.winfo_children()):
            card.config(
                image=self.model.score_cards[i].back_image, background="#100001"
            )
            pywinstyles.set_opacity(card, color="#100001")

        # add initial hand cards to the grid
        for _ in range(3):
            self.hand_card = ttk.Label(self.view.hand_area)
        for i, card in enumerate(self.view.hand_area.winfo_children()):
            card.grid(column=1 + 2 * i, row=17, rowspan=2, columnspan=2)
        # add images to the cards
        for i, card in enumerate(self.view.hand_area.winfo_children()):
            card.config(
                image=self.model.hand_cards[i].front_image, background="#000001"
            )
            pywinstyles.set_opacity(card, color="#000001")
            card.bind(LEFT_MOUSE_BUTTON, self.play_card2)

        # add deck to the grid
        self.next_card = ttk.Label(self.view.deck_area)
        self.next_card.grid(column=7, row=17, rowspan=2, columnspan=6)
        # add image to the card
        image = self.model.cards[0].front_image
        for card in self.view.deck_area.winfo_children():
            card.configure(image=image, background="#000001")
            pywinstyles.set_opacity(card, color="#000001")
