from collections import defaultdict
from tkinter import ttk

import tkinter as tk

from Classes.base.views import BaseView
from Classes.foodchainisland.FoodChainIslandApp import FoodChainIslandApp


class FoodChainIslandView(BaseView):
    def __init__(self, parent: FoodChainIslandApp) -> None:
        BaseView.__init__(self, parent)

        self.card_grid = defaultdict(lambda: defaultdict(ttk.Label))

        for i in range(4):
            self.grid_rowconfigure(i + 1, minsize=220)
            self.grid_columnconfigure(i + 1, minsize=170)
            for j in range(4):
                self.card_grid[j][i] = ttk.Label(self)
                self.card_grid[j][i].grid(column=j + 1, row=i + 1)
