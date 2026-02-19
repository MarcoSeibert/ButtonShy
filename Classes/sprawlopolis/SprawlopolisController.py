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

        # show goal scores
        self.view.goal_score.config(text=self.model.goal)
        # add scoring cards to the grid
        self.scoring_card = ttk.Label(self.view.score_area)
        self.scoring_card = ttk.Label(self.view.score_area)
        self.scoring_card = ttk.Label(self.view.score_area)
        for i, card in enumerate(self.view.score_area.winfo_children()):
            card.grid(column=13, row=4 * i + 1, columnspan=2, rowspan=4)
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
            # update the deck
            image = self.model.cards[0].front_image
            for deck in self.view.deck_area.winfo_children():
                deck.configure(image=image, background="#000001")
            # show the first card on the canvas
            self.view.add_card_to_canvas(
                card, "front", (30, 18), self.grid_size, movable=False
            )
        elif event.type == "DRAW_NEW_CARD":
            if self.model.cards:
                image = self.model.cards[0].front_image
                for deck in self.view.deck_area.winfo_children():
                    deck.configure(image=image, background="#000001")
            else:
                for deck in self.view.deck_area.winfo_children():
                    deck.destroy()
            for i, card in enumerate(self.view.hand_area.winfo_children()):
                card.config(
                    image=self.model.hand_cards[i].front_image,
                    background="#000001",
                )
        elif event.type == "UPDATE_SCORES":
            scores = self.model.scores
            self.view.orange_score.config(text=scores["orange"])
            self.view.blue_score.config(text=scores["blue"])
            self.view.gray_score.config(text=scores["grey"])
            self.view.green_score.config(text=scores["green"])
            self.view.street_score.config(text=scores["streets"])

            self.view.goal_1.config(text=scores["goal_1"])
            self.view.goal_2.config(text=scores["goal_2"])
            self.view.goal_3.config(text=scores["goal_3"])
            self.view.total_score.config(text=sum(scores.values()))
