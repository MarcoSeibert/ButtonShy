import tkinter as tk
from tkinter import ttk

from Classes.adragonsgift.ADragonsGiftApp import ADragonsGiftApp
from Classes.base.views import BaseView
from Classes.canvasgameview import CanvasGameView
from Utils.globals import BASIC_FONT, BOLD_FONT


class ADragonsGiftView(BaseView, CanvasGameView):
    def __init__(self, parent: ADragonsGiftApp) -> None:
        BaseView.__init__(self, parent)
        CanvasGameView.__init__(self, parent)

        # add area for decks
        self.deck_area = tk.LabelFrame(
            self, text="Deck", foreground="black", font=BASIC_FONT, relief="flat"
        )
        self.deck_area.grid(column=7, row=17, columnspan=6, rowspan=2)

        # add area for hand card
        self.hand_area = tk.LabelFrame(
            self, text="Hand", foreground="black", font=BASIC_FONT, relief="flat"
        )
        self.hand_area.grid(column=1, columnspan=3, row=17, rowspan=2)

        # add area for gift card
        self.gift_area = tk.LabelFrame(
            self, text="Gift", foreground="black", font=BASIC_FONT, relief="flat"
        )
        self.gift_area.grid(column=4, columnspan=3, row=17, rowspan=2)

        # add area for transport cards
        self.transport_area = tk.LabelFrame(
            self, foreground="black", font=BASIC_FONT, relief="flat"
        )
        self.transport_area.grid(column=13, columnspan=2, row=1, rowspan=12)

        # add current score
        ttk.Label(self, text="Current Score:", font=BOLD_FONT).grid(
            column=13, row=18, columnspan=2
        )
        self.score = ttk.Label(self, text="0", font=BOLD_FONT)
        self.score.grid(column=15, row=18, sticky="w")

    def add_card_to_canvas(self, *args, **kwargs) -> None:
        return CanvasGameView.add_card_to_canvas(self, *args, **kwargs)

    def delete_card_from_canvas(self, *args, **kwargs) -> None:
        return CanvasGameView.delete_card_from_canvas(self, *args, **kwargs)
