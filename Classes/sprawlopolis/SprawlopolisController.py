from functools import partial
from tkinter import ttk
import pywinstyles

from Classes.base.controllers import BaseController
from Classes.base.events import ModelEvent
from Classes.canvasgamecontroller import CanvasGameController
from Classes.sprawlopolis.SprawlopolisModel import SprawlopolisModel
from Classes.sprawlopolis.SprawlopolisView import SprawlopolisView
from globals import LEFT_MOUSE_BUTTON


class SprawlopolisController(BaseController, CanvasGameController):
    def __init__(self, model: SprawlopolisModel, view: SprawlopolisView) -> None:
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
                image=self.model.hand_cards[i].front_image,
                background="#000001",
            )
            pywinstyles.set_opacity(card, color="#000001")
            card.bind(
                LEFT_MOUSE_BUTTON, partial(self.play_card, self.model.hand_cards[i])
            )

        # add deck to the grid
        self.next_card = ttk.Label(self.view.deck_area)
        self.next_card.grid(column=7, row=17, rowspan=2, columnspan=6)
        # add image to the card
        image = self.model.cards[0].front_image
        for card in self.view.deck_area.winfo_children():
            card.configure(image=image, background="#000001")
            pywinstyles.set_opacity(card, color="#000001")

    def on_model_change(self, event: ModelEvent) -> None:
        """Reagiert auf Events vom Model."""
        if event.type == "FIRST_CARD_PLAYED":
            card = event.data["card"]
            print(f"Controller: Erste Karte {card.card_id} gespielt!")

            # update the deck
            image = self.model.cards[0].front_image
            for deck in self.view.deck_area.winfo_children():
                deck.configure(image=image, background="#000001")

            # show the first card on the canvas
            self.view.add_card_to_canvas(
                card, "front", (30, 18), self.grid_size, movable=False
            )

        elif event.type == "CARD_PLAYED":
            card = event.data["card"]
            print(f"Controller: Karte {card.card_id} gespielt!")
            self.active_card_image = card.front_image
            # pywinstyles.set_opacity(event.widget, value=0.5, color="#000001") brauchen wir erst für spätere Karten
            self.view.canvas_area.create_image(
                self.grid_size[0] * 30,
                self.grid_size[1] * 18,
                image=self.active_card_image,
                tag="movable",
            )
