import tkinter as tk
from tkinter import Event

import pywinstyles

from Classes.base.models import BaseModel, BaseCard
from Classes.canvasgameview import CanvasGameView
from Utils.globals import LEFT_MOUSE_BUTTON

BUTTON_PRESS_1 = "<ButtonPress-1>"


class CanvasGameController:
    def __init__(self, model: BaseModel, view: CanvasGameView) -> None:
        x = self.model.start_position_on_canvas[0]  # type: ignore
        y = self.model.start_position_on_canvas[1]  # type: ignore
        self.drop_data = {"x": x, "y": y}
        self.active_widget = None
        self.model = model
        self.view = view

        self.active_card_image = None
        self.drag_data = {"x": 0, "y": 0, "item": None}
        self.grid_size = self.model.game_data["grid_size"]

        # add bindings to drag canvas
        self.view.canvas_area.bind("<ButtonPress-2>", self.pick_up_canvas)
        self.view.canvas_area.bind("<ButtonRelease-2>", self.drop_canvas)
        self.view.canvas_area.bind("<B2-Motion>", self.drag_canvas)
        self.view.canvas_area.bind("<ButtonPress-3>", self.debug_on_right_click)

        # add bindings to drag cards
        self.view.canvas_area.tag_bind("movable", BUTTON_PRESS_1, self.pick_up_card)
        self.view.canvas_area.tag_bind("movable", "<ButtonRelease-1>", self.drop_card)
        self.view.canvas_area.tag_bind("movable", "<B1-Motion>", self.drag_card)

        # add bindings to buttons
        self.view.canvas_area.tag_bind("approve", BUTTON_PRESS_1, self.press_approve)
        self.view.canvas_area.tag_bind("decline", BUTTON_PRESS_1, self.press_decline)
        self.view.canvas_area.tag_bind("turn", BUTTON_PRESS_1, self.press_turn)

        self.image_approve = tk.PhotoImage(
            file="Resources/Assets/Approve.png", format="png"
        )
        self.image_decline = tk.PhotoImage(
            file="Resources/Assets/Decline.png", format="png"
        )
        self.image_turn = tk.PhotoImage(file="Resources/Assets/Turn.png", format="png")

    def debug_on_right_click(self, event: Event) -> None:
        # Gets used when needed
        pass

    def pick_up_canvas(self, mouse_press_event: Event) -> None:
        self.view.canvas_area.config(xscrollincrement=1)
        self.view.canvas_area.config(yscrollincrement=1)
        self.drag_data["x"], self.drag_data["y"] = (
            mouse_press_event.x,
            mouse_press_event.y,
        )

    def drop_canvas(self, _) -> None:
        self.view.canvas_area.config(xscrollincrement=0)
        self.view.canvas_area.config(yscrollincrement=0)
        self.drag_data["x"], self.drag_data["y"] = (0, 0)

    def drag_canvas(self, mouse_move_event: Event) -> None:
        delta_x = self.drag_data["x"] - mouse_move_event.x
        delta_y = self.drag_data["y"] - mouse_move_event.y
        self.view.canvas_area.xview("scroll", delta_x, "units")
        self.view.canvas_area.yview("scroll", delta_y, "units")
        self.drag_data["x"], self.drag_data["y"] = (
            mouse_move_event.x,
            mouse_move_event.y,
        )

    def pick_up_card(self, event: Event) -> None:
        x = self.view.canvas_area.canvasx(event.x)
        y = self.view.canvas_area.canvasy(event.y)
        self.drag_data["item"] = self.view.canvas_area.find_withtag("movable")
        self.drag_data["x"] = x
        self.drag_data["y"] = y
        self.show_buttons(False)

    def drop_card(self, event: Event) -> None:
        grid_x_pix = self.view.canvas_area.canvasx(event.x, self.grid_size[0])
        grid_y_pix = self.view.canvas_area.canvasy(event.y, self.grid_size[1])
        grid_x = grid_x_pix / self.grid_size[0]
        grid_y = grid_y_pix / self.grid_size[1]

        if not self.model.is_placement_valid(grid_x, grid_y):
            x = self.model.start_position_on_canvas[0]  # type: ignore
            y = self.model.start_position_on_canvas[1]  # type: ignore
            grid_x_pix = x * self.grid_size[0]
            grid_y_pix = y * self.grid_size[1]
        self.drop_data["x"] = grid_x
        self.drop_data["y"] = grid_y
        self.view.canvas_area.coords(self.drag_data["item"], grid_x_pix, grid_y_pix)
        self.drag_data["item"] = 0
        self.drag_data["x"] = 0
        self.drag_data["y"] = 0
        self.show_buttons(True, grid_x_pix, grid_y_pix)

    def drag_card(self, event: Event) -> None:
        x = self.view.canvas_area.canvasx(event.x)
        y = self.view.canvas_area.canvasy(event.y)
        delta_x = x - self.drag_data["x"]
        delta_y = y - self.drag_data["y"]
        self.view.canvas_area.move(self.drag_data["item"], delta_x, delta_y)
        self.drag_data["x"] = x
        self.drag_data["y"] = y

    def show_buttons(
        self, active: bool, grid_x_pix: int = 0, grid_y_pix: int = 0
    ) -> None:
        if active:
            self.view.canvas_area.create_image(
                grid_x_pix - self.grid_size[0],
                grid_y_pix - self.grid_size[1],
                image=self.image_approve,
                tags=("canvas_buttons", "approve"),
            )
            self.view.canvas_area.create_image(
                grid_x_pix - self.grid_size[0],
                grid_y_pix,
                image=self.image_turn,
                tags=("canvas_buttons", "turn"),
            )
            self.view.canvas_area.create_image(
                grid_x_pix - self.grid_size[0],
                grid_y_pix + self.grid_size[1],
                image=self.image_decline,
                tags=("canvas_buttons", "decline"),
            )
        else:
            self.view.canvas_area.delete("canvas_buttons")

    def play_card(
        self,
        card: BaseCard,
        event: Event,
    ) -> None:
        self.model.active_card = card

        pywinstyles.set_opacity(event.widget, value=0.5, color="#000001")
        self.active_card_image = card.front_image
        self.view.add_card_to_canvas(card, "front", self.model.start_position_on_canvas, self.grid_size)  # type: ignore
        self.active_widget = event.widget

        event.widget.image = self.active_card_image

        objs_on_canvas = self.view.canvas_area.find_all()
        active_card_obj = None
        for obj in objs_on_canvas:
            if "movable" in self.view.canvas_area.gettags(obj):
                active_card_obj = obj
        self.view.canvas_area.itemconfigure(
            active_card_obj, image=self.active_card_image
        )

        x = self.model.start_position_on_canvas[0]  # type: ignore
        y = self.model.start_position_on_canvas[1]  # type: ignore
        self.show_buttons(True, self.grid_size[0] * x, self.grid_size[1] * y)
        for i, card_label in enumerate(self.view.hand_area.winfo_children()):
            card_label.unbind(LEFT_MOUSE_BUTTON)

    def press_approve(self, _) -> None:
        raise NotImplementedError

    def press_decline(self, _) -> None:
        raise NotImplementedError

    def press_turn(self, _) -> None:
        raise NotImplementedError
