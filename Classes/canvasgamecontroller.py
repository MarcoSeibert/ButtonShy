import pywinstyles

from tkinter import Event
import tkinter as tk

from Classes.base.models import BaseModel
from Classes.base.views import BaseView
from globals import LEFT_MOUSE_BUTTON


class CanvasGameController:
    def __init__(self, model: BaseModel, view: BaseView):
        self.model = model
        self.view = view

        self.active_card_image = None
        self.drag_data = {"x": 0, "y": 0, "item": None}
        self.grid_size = self.model.game_data["grid_size"]

        # add bindings to drag canvas
        self.view.canvas_area.bind("<ButtonPress-2>", self.pick_up_canvas)
        self.view.canvas_area.bind("<ButtonRelease-2>", self.drop_canvas)
        self.view.canvas_area.bind("<B2-Motion>", self.drag_canvas)
        self.view.canvas_area.bind("<ButtonPress-1>", self.print_coords)

        # add bindings to drag cards
        self.view.canvas_area.tag_bind("movable", "<ButtonPress-1>", self.pick_up_card)
        self.view.canvas_area.tag_bind("movable", "<ButtonRelease-1>", self.drop_card)
        self.view.canvas_area.tag_bind("movable", "<B1-Motion>", self.drag_card)

        self.image_approve = tk.PhotoImage(
            file="Resources/Assets/Approve.png", format="png"
        )
        self.image_decline = tk.PhotoImage(
            file="Resources/Assets/Decline.png", format="png"
        )
        self.image_turn = tk.PhotoImage(file="Resources/Assets/Turn.png", format="png")

    def print_coords(self, event: Event) -> None:
        print(f"coords: {event.x}, {event.y}")

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

    def pick_up_card(self, event: Event):
        x = self.view.canvas_area.canvasx(event.x)
        y = self.view.canvas_area.canvasy(event.y)
        self.drag_data["item"] = self.view.canvas_area.find_closest(x, y)[0]
        self.drag_data["x"] = x
        self.drag_data["y"] = y
        self.show_buttons(False)

    def drop_card(self, event: Event):
        grid_x_pix = self.view.canvas_area.canvasx(event.x, self.grid_size[0])
        grid_y_pix = self.view.canvas_area.canvasy(event.y, self.grid_size[1])
        self.view.canvas_area.coords(self.drag_data["item"], grid_x_pix, grid_y_pix)
        self.drag_data["item"] = 0
        self.drag_data["x"] = 0
        self.drag_data["y"] = 0
        self.show_buttons(True, grid_x_pix, grid_y_pix)

    def drag_card(self, event: Event):
        x = self.view.canvas_area.canvasx(event.x)
        y = self.view.canvas_area.canvasy(event.y)
        delta_x = x - self.drag_data["x"]
        delta_y = y - self.drag_data["y"]
        self.view.canvas_area.move(self.drag_data["item"], delta_x, delta_y)
        self.drag_data["x"] = x
        self.drag_data["y"] = y

    def show_buttons(self, active: bool, grid_x_pix: int = 0, grid_y_pix: int = 0):
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

    def play_card2(self, event: Event):
        self.active_card_image = event.widget.cget("image")[0]
        pywinstyles.set_opacity(event.widget, value=0.5, color="#000001")
        self.draw_card(self.active_card_image, [30, 18], True)
        # self.view.canvas_area.create_image(
        #     self.grid_size[0] * 30,
        #     self.grid_size[1] * 18,
        #     image=self.active_card_image,
        #     tag="movable",
        # )
        self.show_buttons(True, self.grid_size[0] * 30, self.grid_size[1] * 18)
        for i, card in enumerate(self.view.hand_area.winfo_children()):
            card.unbind(LEFT_MOUSE_BUTTON)

    def draw_card(self, card_image, coordinates, movable=False):
        tag = "movable" if movable else None
        self.view.canvas_area.create_image(
            self.grid_size[0] * coordinates[0],
            self.grid_size[1] * coordinates[1],
            image=card_image,
            tag=tag,
        )
