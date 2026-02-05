from tkinter.ttk import Label
from typing import TYPE_CHECKING
import tkinter as tk
from tkinter import ttk

if TYPE_CHECKING:
    from Classes.base.apps import BaseApp
    from Classes.base.models import BaseCard


class CanvasGameView:
    def __init__(self, parent: BaseApp) -> None:
        self.hand_area = None
        self.images_on_canvas = []
        self.vbar = None
        self.hbar = None
        self.canvas_area = None
        self.canvas = None
        self.parent = parent
        self.set_canvas_area()

    def set_canvas_area(self) -> None:
        self.canvas = self.parent.game_data["canvas_size"]
        canvas_x = self.canvas[0]
        canvas_y = self.canvas[1]
        self.canvas_area = tk.Canvas(
            self,
            width=canvas_x,
            height=canvas_y,
            background="white",
            scrollregion=(0, 0, 4 * canvas_x, 4 * canvas_y),
        )
        self.canvas_area.xview_moveto(0.375)
        self.canvas_area.yview_moveto(0.375)
        self.canvas_area.grid(column=1, row=1, columnspan=12, rowspan=15)
        ## add scrollbars
        self.hbar = ttk.Scrollbar(self, orient=tk.HORIZONTAL)
        self.hbar.config(command=self.canvas_area.xview)
        self.hbar.grid(column=1, row=16, columnspan=12, sticky="we")
        self.vbar = ttk.Scrollbar(self, orient=tk.VERTICAL)
        self.vbar.config(command=self.canvas_area.yview)
        self.vbar.grid(column=0, row=1, rowspan=15, sticky="ns")
        self.canvas_area.config(
            xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set
        )

    def add_card_to_canvas(
        self,
        card: BaseCard,
        side: str,
        position: tuple,
        grid_size: tuple,
        movable: bool = True,
    ) -> None:
        image = None
        if side == "front":
            image = card.front_image
        elif side == "back":
            image = card.back_image
        self.images_on_canvas.append(image)
        coords = (grid_size[0] * position[0], grid_size[1] * position[1])
        if movable:
            tag = "movable"
        else:
            tag = None
        self.canvas_area.create_image(coords[0], coords[1], image=image, tag=tag)

    def delete_card_from_canvas(self, card: Label) -> None:
        self.canvas_area.delete(card)
