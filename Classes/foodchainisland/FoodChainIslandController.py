from functools import partial
from tkinter import Event

import PIL
from PIL import ImageTk, Image, ImageDraw

from Classes.base.controllers import BaseController
from Classes.base.models import BaseCard
from Classes.foodchainisland.FoodChainIslandModel import FoodChainIslandModel
from Classes.foodchainisland.FoodChainIslandView import FoodChainIslandView
from Utils.globals import LEFT_MOUSE_BUTTON, CARD_SIZE_ON_SCREEN


class FoodChainIslandController(BaseController):
    def __init__(self, model: FoodChainIslandModel, view: FoodChainIslandView) -> None:
        BaseController.__init__(self, model, view)
        self.zoom_image = None

        self.view.zoomed_label.grid(row=1, column=10, columnspan=2, rowspan=2)
        self.on_enter(1, None)
        self.on_leave(None)

        self.card_active = False
        self.highlight_active_card = None
        self.highlight_neighbours = {}

        # add the cards to the grid
        for i in range(4):
            for j in range(4):
                card = self.model.grid[i][j]  # type: ignore
                spot_on_grid = self.view.card_grid[i][j]  # type: ignore
                spot_on_grid.configure(image=card.front_image)
                spot_on_grid.bind(
                    LEFT_MOUSE_BUTTON, partial(self.choose_card, card, (i, j))
                )
                spot_on_grid.bind("<Enter>", partial(self.on_enter, card.card_id))
                spot_on_grid.bind("<Leave>", self.on_leave)

    def choose_card(self, card: BaseCard, pos: tuple, event: Event) -> None:
        x, y = pos
        neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]

        if not self.card_active:
            # Karte und passende Nachbarn aktivieren (gelb/grün umrandet)
            self._activate_card_and_neighbors(card, event, neighbors)
        else:
            # Karte und Nachbarn deaktivieren (Rahmen entfernen)
            self._deactivate_card_and_neighbors(card, event, neighbors)

    def _activate_card_and_neighbors(
        self, card: BaseCard, event: Event, neighbors: list
    ) -> None:
        self.card_active = True
        self.model.active_card = card

        # Aktive Karte gelb umrandet darstellen
        image = self.model.front_image_dict[card.card_id].resize(CARD_SIZE_ON_SCREEN)
        border = rounded_rectangle_image(
            CARD_SIZE_ON_SCREEN[0] + 10, CARD_SIZE_ON_SCREEN[1] + 10, 10, "yellow"
        )
        border.paste(image, (5, 5), image)
        self.highlight_active_card = ImageTk.PhotoImage(border)
        event.widget.config(image=self.highlight_active_card)

        # Passende Nachbarn grün umrandet darstellen
        for x1, y1 in neighbors:
            if self._is_valid_neighbor(x1, y1):
                neighbor_id = self.model.grid[x1][y1].card_id  # type: ignore
                if card.card_id - neighbor_id in [1, 2, 3]:
                    self._highlight_neighbor((x1, y1), "green")

    def _deactivate_card_and_neighbors(
        self, card: BaseCard, event: Event, neighbors: list
    ) -> None:
        if self.model.active_card == card:
            self.card_active = False
            self.model.active_card = None

            # Aktive Karte zurücksetzen
            event.widget.config(image=card.front_image)

            # Nachbarn zurücksetzen
            for x1, y1 in neighbors:
                if self._is_valid_neighbor(x1, y1):
                    neighbor_id = self.model.grid[x1][y1].card_id  # type: ignore
                    if int(card.card_id) - int(neighbor_id) in [1, 2, 3]:
                        self._highlight_neighbor((x1, y1), None)

    def _highlight_neighbor(self, pos: tuple, color: str | None) -> None:
        x1, y1 = pos
        neighbor = self.model.grid[x1][y1]  # type: ignore
        neighbor_image = self.model.front_image_dict[neighbor.card_id].resize(
            CARD_SIZE_ON_SCREEN
        )

        if color:
            border = rounded_rectangle_image(
                CARD_SIZE_ON_SCREEN[0] + 10, CARD_SIZE_ON_SCREEN[1] + 10, 10, color
            )
            border.paste(neighbor_image, (5, 5), neighbor_image)
            self.highlight_neighbours[pos] = ImageTk.PhotoImage(border)
        else:
            self.highlight_neighbours[pos] = ImageTk.PhotoImage(neighbor_image)

        self.view.card_grid[x1][y1].config(image=self.highlight_neighbours[pos])  # type: ignore

    def _is_valid_neighbor(self, x: int, y: int) -> bool:
        return x in self.view.card_grid and y in self.view.card_grid[x]  # type: ignore

    def on_enter(self, card_id: int, _) -> None:
        image = self.model.front_image_dict[card_id]
        self.zoom_image = ImageTk.PhotoImage(image)
        self.view.zoomed_label.config(image=self.zoom_image)

    def on_leave(self, _) -> None:
        self.zoom_image = None


def rounded_rectangle_image(x: int, y: int, r: int, color: str) -> PIL.Image.Image:
    image = Image.new("RGB", (x, y), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((0, 0, x, y), radius=r, fill=color)
    return image
