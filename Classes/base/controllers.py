from Classes.base.models import BaseModel
from Classes.base.views import StartView, BaseView


class StartController:
    def __init__(self, view: StartView):
        self.view = view

    def click_play(self):
        chosen_game = self.view.chosen_game.get()
        chosen_game_name = games_dict[chosen_game].replace(" ", "")
        start_game(self.view.master, chosen_game_name)

class BaseController:
    def __init__(self, model: BaseModel, view: BaseView):
        self.model = model
        self.view = view
        self.grid_size = model.game_data["grid_size"]

        self.starting_drag_position = (0, 0)
        self.drag_data = {"x": 0, "y": 0, "item": None}

        self.view.master.bind("<Escape>", self.quit)

        if hasattr(self.view, "canvas_area"):
            # add bindings to drag canvas
            self.view.canvas_area.bind("<ButtonPress-2>", self.pick_up_canvas)
            self.view.canvas_area.bind("<ButtonRelease-2>", self.drop_canvas)
            self.view.canvas_area.bind("<B2-Motion>", self.drag_canvas)

            # add bindings to drag cards
            # self.view.play_area.tag_bind("movable", "<ButtonPress-1>", self.pick_up_card)
            # self.view.play_area.tag_bind("movable", "<ButtonRelease-1>", self.drop_card)
            # self.view.play_area.tag_bind("movable", "<B1-Motion>", self.drag_card)

    def click_on_card(self, args):
        pass

    def quit(self, _):
        self.view.master.destroy()

    def pick_up_canvas(self, event: Event):
        if hasattr(self.view, 'canvas_area'):
            self.view.canvas_area.config(xscrollincrement=1)
            self.view.canvas_area.config(yscrollincrement=1)
            self.drag_data["x"], self.drag_data["y"] = (event.x, event.y)

    def drop_canvas(self, _):
        if hasattr(self.view, 'canvas_area'):
            self.view.canvas_area.config(xscrollincrement=0)
            self.view.canvas_area.config(yscrollincrement=0)
            self.drag_data["x"], self.drag_data["y"] = (0, 0)

    def drag_canvas(self, event: Event):
        if hasattr(self.view, 'canvas_area'):
            delta_x = self.drag_data["x"] - event.x
            delta_y = self.drag_data["y"] - event.y
            self.view.canvas_area.xview("scroll", delta_x, "units")
            self.view.canvas_area.yview("scroll", delta_y, "units")
            self.drag_data["x"], self.drag_data["y"] = (event.x, event.y)