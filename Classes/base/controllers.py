from tkinter import Event

from Classes.base.models import BaseModel
from Classes.base.views import StartView, BaseView


class StartController:
    def __init__(self, view: StartView):
        self.view = view

    def click_play(self):
        chosen_game = self.view.chosen_game.get()
        self.view.master.start_game(chosen_game)

class BaseController:
    def __init__(self, model: BaseModel, view: BaseView):
        self.model = model
        self.view = view
        self.grid_size = model.grid_size

        self.starting_drag_position = (0, 0)
        self.drag_data = {"x": 0, "y": 0, "item": None}

        self.view.master.bind("<Escape>", self.quit)

        if hasattr(self.view, "play_area"):
            # add bindings to drag canvas
            self.view.play_area.bind("<ButtonPress-2>", self.pick_up_canvas)
            self.view.play_area.bind("<ButtonRelease-2>", self.drop_canvas)
            self.view.play_area.bind("<B2-Motion>", self.drag_canvas)

            # add bindings to drag cards
            self.view.play_area.tag_bind("movable", "<ButtonPress-1>", self.pick_up_card)
            self.view.play_area.tag_bind("movable", "<ButtonRelease-1>", self.drop_card)
            self.view.play_area.tag_bind("movable", "<B1-Motion>", self.drag_card)


    def click_on_card(self, args):
        pass

    def pick_up_canvas(self, event: Event):
        if hasattr(self.view, 'play_area'):
            self.view.play_area.config(xscrollincrement=1)
            self.view.play_area.config(yscrollincrement=1)
            self.drag_data["x"], self.drag_data["y"] = (event.x, event.y)

    def drop_canvas(self, _):
        if hasattr(self.view, 'play_area'):
            self.view.play_area.config(xscrollincrement=0)
            self.view.play_area.config(yscrollincrement=0)
            self.drag_data["x"], self.drag_data["y"] = (0, 0)

    def drag_canvas(self, event: Event):
        if hasattr(self.view, 'play_area'):
            delta_x = self.drag_data["x"] - event.x
            delta_y = self.drag_data["y"] - event.y
            self.view.play_area.xview("scroll", delta_x, "units")
            self.view.play_area.yview("scroll", delta_y, "units")
            self.drag_data["x"], self.drag_data["y"] = (event.x, event.y)

    def pick_up_card(self, event: Event):
        if hasattr(self.view, 'play_area'):
            x = self.view.play_area.canvasx(event.x, self.grid_size[0])
            y = self.view.play_area.canvasy(event.y, self.grid_size[1])
            closest = self.view.play_area.find_closest(x, y)
            if closest:
                self.drag_data["item"] = closest[0]
                self.drag_data["x"] = x
                self.drag_data["y"] = y

    def drop_card(self, event: Event):
        if hasattr(self.view, 'play_area'):
            grid_x_pix = self.view.play_area.canvasx(event.x)
            grid_y_pix = self.view.play_area.canvasy(event.y)
            self.view.play_area.coords(self.drag_data["item"], grid_x_pix, grid_y_pix)
            self.drag_data["item"] = 0
            self.drag_data["x"] = 0
            self.drag_data["y"] = 0

    def drag_card(self, event: Event):
        if hasattr(self.view, 'play_area'):
            x = self.view.play_area.canvasx(event.x)
            y = self.view.play_area.canvasy(event.y)
            delta_x = x - self.drag_data["x"]
            delta_y = y - self.drag_data["y"]
            self.view.play_area.move(self.drag_data["item"], delta_x, delta_y)
            self.drag_data["x"] = x
            self.drag_data["y"] = y

    def quit(self, _):
        self.view.master.destroy()