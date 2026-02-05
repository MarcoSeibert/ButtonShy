from typing import TYPE_CHECKING

from Classes.canvasgameview import CanvasGameView

if TYPE_CHECKING:
    from Classes.sprawlopolis.SprawlopolisApp import SprawlopolisApp
from Classes.base.views import BaseView
import tkinter as tk
from tkinter import ttk
from globals import BASIC_FONT, BOLD_FONT


class SprawlopolisView(BaseView, CanvasGameView):
    def __init__(self, parent: SprawlopolisApp) -> None:
        BaseView.__init__(self, parent)
        CanvasGameView.__init__(self, parent)

        # add area for decks
        self.deck_area = tk.LabelFrame(
            self, text="Deck", foreground="black", font=BASIC_FONT, relief="flat"
        )
        self.deck_area.grid(column=7, row=17, columnspan=6, rowspan=2)

        # add area for hand cards
        self.hand_area = tk.LabelFrame(
            self, text="Hand", foreground="black", font=BASIC_FONT, relief="flat"
        )
        self.hand_area.grid(column=1, columnspan=6, row=17, rowspan=2)

        # add area for score cards
        self.score_area = tk.LabelFrame(
            self, foreground="black", font=BASIC_FONT, relief="flat"
        )
        self.score_area.grid(column=13, columnspan=2, row=1, rowspan=12)

        # insert scorecard
        ## load images
        self.orange_block = tk.PhotoImage(
            file="Resources/Assets/Sprawlopolis/Orange.png"
        )
        self.blue_block = tk.PhotoImage(file="Resources/Assets/Sprawlopolis/Blue.png")
        self.gray_block = tk.PhotoImage(file="Resources/Assets/Sprawlopolis/Gray.png")
        self.green_block = tk.PhotoImage(file="Resources/Assets/Sprawlopolis/Green.png")
        self.streets = tk.PhotoImage(file="Resources/Assets/Sprawlopolis/Street.png")
        ## add cells
        ### for blocks
        ttk.Label(self, image=self.orange_block).grid(column=13, row=13, sticky="e")
        self.orange_score = ttk.Label(self, text="0", font=BOLD_FONT)
        self.orange_score.grid(column=14, row=13)
        ttk.Label(self, image=self.blue_block).grid(column=13, row=14, sticky="e")
        self.blue_score = ttk.Label(self, text="0", font=BOLD_FONT)
        self.blue_score.grid(column=14, row=14)
        ttk.Label(self, image=self.gray_block).grid(column=15, row=13, sticky="e")
        self.gray_score = ttk.Label(self, text="0", font=BOLD_FONT)
        self.gray_score.grid(column=16, row=13)
        ttk.Label(self, image=self.green_block).grid(column=15, row=14, sticky="e")
        self.green_score = ttk.Label(self, text="0", font=BOLD_FONT)
        self.green_score.grid(column=16, row=14)
        ### for streets
        ttk.Label(self, image=self.streets).grid(column=13, row=15, sticky="e")
        self.street_score = ttk.Label(self, text="0", font=BOLD_FONT)
        self.street_score.grid(column=14, row=15)
        ### for goal
        ttk.Label(self, text="Goal Score:", font=BOLD_FONT).grid(
            column=13, row=17, columnspan=2
        )
        self.goal_score = ttk.Label(self, text="0", font=BOLD_FONT)
        self.goal_score.grid(column=15, row=17, sticky="w")
        ### for total
        ttk.Label(self, text="Total Score:", font=BOLD_FONT).grid(
            column=13, row=18, columnspan=2
        )
        self.total_score = ttk.Label(self, text="0", font=BOLD_FONT)
        self.total_score.grid(column=15, row=18, sticky="w")

    def add_card_to_canvas(self, *args, **kwargs) -> None:
        return CanvasGameView.add_card_to_canvas(self, *args, **kwargs)

    def delete_card_from_canvas(self, *args, **kwargs) -> None:
        return CanvasGameView.delete_card_from_canvas(self, *args, **kwargs)
