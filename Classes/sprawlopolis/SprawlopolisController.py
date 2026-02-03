from Classes.base.controllers import BaseController
from Classes.sprawlopolis.SprawlopolisModel import SprawlopolisModel
from Classes.sprawlopolis.SprawlopolisView import SprawlopolisView

import tkinter as tk
from tkinter import ttk
import pywinstyles

from globals import LEFT_MOUSE_BUTTON


class SprawlopolisController(BaseController):
    def __init__(self, model:SprawlopolisModel, view:SprawlopolisView):
        super().__init__(model, view)

        self.active_card_image = None
        self.number_of_decks = 1
        self.grid_size = self.model.game_data["grid_size"]


        self.image_approve = tk.PhotoImage(file="Resources/Assets/Sprawlopolis/Approve.png", format="png")
        self.image_decline = tk.PhotoImage(file="Resources/Assets/Sprawlopolis/Decline.png", format="png")
        self.image_turn = tk.PhotoImage(file="Resources/Assets/Sprawlopolis/Turn.png", format="png")

        # add scoring cards to the grid
        self.scoring_card = ttk.Label(self.view.score_area)
        self.scoring_card = ttk.Label(self.view.score_area)
        self.scoring_card = ttk.Label(self.view.score_area)
        if self.number_of_decks == 3:
            self.scoring_card = ttk.Label(self.view.score_area)
            for i, card in enumerate(self.view.score_area.winfo_children()):
                card.grid(column=13, row=3 * i + 1, columnspan=2, rowspan=3)
        else:
            for i, card in enumerate(self.view.score_area.winfo_children()):
                card.grid(column=13, row=4 * i + 1, columnspan=2, rowspan=4)
        # add images to the cards
        for i, card in enumerate(self.view.score_area.winfo_children()):
            card.config(image=self.model.score_cards[i].back_image, background="#100001")
            pywinstyles.set_opacity(card, color="#100001")

        # add initial hand cards to the grid
        for _ in range(3):
            self.hand_card = ttk.Label(self.view.hand_area)
        for i, card in enumerate(self.view.hand_area.winfo_children()):
            card.grid(column=1 + 2 * i, row=17, rowspan=2, columnspan=2)
        # add images to the cards
        for i, card in enumerate(self.view.hand_area.winfo_children()):
            card.config(image=self.model.hand_cards[i].front_image, background="#000001")
            pywinstyles.set_opacity(card, color="#000001")
            # card.bind(LEFT_MOUSE_BUTTON, self.play_card)

        # add deck to the grid
        self.next_card = ttk.Label(self.view.deck_area)
        self.next_card.grid(column=7, row=17, rowspan=2, columnspan=6)
        # add image to the card
        image = self.model.cards[0].front_image
        for card in self.view.deck_area.winfo_children():
            card.configure(image=image, background="#000001")
            pywinstyles.set_opacity(card, color="#000001")

    def show_buttons(self, param: bool, grid_x_pix: int = 0, grid_y_pix: int = 0):
        if param:
            self.view.play_area.create_image(grid_x_pix - self.grid_size[0], grid_y_pix - self.grid_size[1],
                                             image=self.image_approve, tags=("canvas_buttons", "approve"))
            self.view.play_area.create_image(grid_x_pix - self.grid_size[0], grid_y_pix,
                                             image=self.image_turn, tags=("canvas_buttons", "turn"))
            self.view.play_area.create_image(grid_x_pix - self.grid_size[0], grid_y_pix + self.grid_size[1],
                                             image=self.image_decline, tags=("canvas_buttons", "decline"))
        else:
            self.view.play_area.delete("canvas_buttons")