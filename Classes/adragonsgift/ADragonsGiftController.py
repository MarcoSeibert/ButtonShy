from functools import partial
from tkinter import ttk

import pywinstyles

from Classes.adragonsgift.ADragonsGiftModel import ADragonsGiftModel
from Classes.adragonsgift.ADragonsGiftView import ADragonsGiftView
from Classes.base.controllers import BaseController
from Classes.base.events import ModelEvent
from Classes.base.models import BaseCard
from Classes.canvasgamecontroller import CanvasGameController
from Utils.globals import LEFT_MOUSE_BUTTON


class ADragonsGiftController(BaseController, CanvasGameController):
    def __init__(self, model: ADragonsGiftModel, view: ADragonsGiftView) -> None:
        BaseController.__init__(self, model, view)
        CanvasGameController.__init__(self, model, view)

        # show score
        self.view.score.config(text=self.model.score)  # type: ignore

        # add transport cards to the grid
        self.transport_card = ttk.Label(self.view.transport_area)  # type: ignore
        self.transport_card = ttk.Label(self.view.transport_area)  # type: ignore
        self.transport_card = ttk.Label(self.view.transport_area)  # type: ignore
        for i, card in enumerate(self.view.transport_area.winfo_children()):  # type: ignore
            card.grid(column=13, row=4 * i + 1, columnspan=2, rowspan=4)
            card.config(
                image=self.model.transport_cards[i].back_image, background="#100001"  # type: ignore
            )
            card.bind(
                LEFT_MOUSE_BUTTON, partial(self.activate_transport, self.model.transport_cards[i])  # type: ignore
            )
            pywinstyles.set_opacity(card, color="#100001")

        # add initial hand card to the grid
        self.hand_card = ttk.Label(self.view.hand_area)  # type: ignore
        self.hand_card.grid(column=1, row=17, rowspan=2, columnspan=2)
        # add image to the card
        self.hand_card.config(
            image=self.model.hand_card.front_image, background="#000001"  # type: ignore
        )
        pywinstyles.set_opacity(self.hand_card, color="#000001")
        self.hand_card.bind(
            LEFT_MOUSE_BUTTON, partial(self.play_card, self.model.hand_card)  # type: ignore
        )

        # add gift card to the grid
        self.gift_card = ttk.Label(self.view.gift_area)  # type: ignore
        self.gift_card.grid(column=4, row=17, rowspan=2, columnspan=3)
        # add image to the card
        self.gift_card.config(
            image=self.model.gift_card.front_image, background="#000001"  # type: ignore
        )
        pywinstyles.set_opacity(self.gift_card, color="#000001")
        self.gift_card.bind(
            LEFT_MOUSE_BUTTON, partial(self.play_gift_card, self.model.gift_card)  # type: ignore
        )

        # add deck to the grid
        self.next_card = ttk.Label(self.view.deck_area)  # type: ignore
        self.next_card.grid(column=7, row=17, rowspan=2, columnspan=6)
        # add image to the card
        image = self.model.village_cards[0].front_image  # type: ignore
        for card in self.view.deck_area.winfo_children():  # type: ignore
            card.configure(image=image, background="#000001")
            pywinstyles.set_opacity(card, color="#000001")

    def activate_transport(self, card: BaseCard, _) -> None:
        # todo
        print(f"Activating transport card {card.card_id}")

    def play_gift_card(self, card: BaseCard, _) -> None:
        # todo
        print(f"Playing gift card {card.card_id}")

    def press_approve(self, _) -> None:
        # todo
        print("Press approve")

    def press_decline(self, _) -> None:
        # todo
        print("Press decline")

    def press_turn(self, _) -> None:
        # todo
        print("Press turn")

    def on_model_change(self, event: ModelEvent) -> None:
        """Reagiert auf Events vom Model."""
        if event.type == "FIRST_CARD_PLAYED":
            self.controller_play_first_card(event)

    def controller_play_first_card(self, event: ModelEvent) -> None:
        card = event.data["card"]
        # update the deck
        image = self.model.village_cards[0].front_image  # type: ignore
        for deck in self.view.deck_area.winfo_children():  # type: ignore
            deck.configure(image=image, background="#000001")
        # show the first card on the canvas
        self.view.add_card_to_canvas(
            card, "front", self.model.start_position_on_canvas, self.grid_size, movable=False  # type: ignore
        )
