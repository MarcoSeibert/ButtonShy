import tkinter as tk
from functools import partial
from tkinter import ttk
from typing import TYPE_CHECKING

from globals import TITLE_FONT, BASIC_FONT, LEFT_MOUSE_BUTTON
from start_up import games_dict

if TYPE_CHECKING:
    from Classes.base.controllers import StartController, BaseController
    from Classes.base.apps import BaseApp

RETURN = "<Return>"


class StartView(ttk.Frame):
    def __init__(self, parent: tk.Tk) -> None:
        super().__init__(parent)
        self.controller = None
        self.chosen_game = tk.IntVar()
        self.chosen_game.set(0)

        # creating frame
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # insert title
        ttk.Label(self, text="Button Shy digital", font=TITLE_FONT).grid(
            column=0, row=0
        )

        # configure styles
        style_buttons = ttk.Style()
        my_button_style = "MyButton.TButton"
        style_buttons.configure(my_button_style, font=BASIC_FONT)
        radio_style_buttons = ttk.Style()
        my_radio_button_style = "MyRadioButton.Toolbutton"
        radio_style_buttons.configure(
            my_radio_button_style, font=BASIC_FONT, background="white", anchor="c"
        )
        radio_style_buttons.map(
            my_radio_button_style,
            foreground=[("selected", "black"), ("!selected", "gray")],
        )

        # set up game radio buttons
        for val, game in games_dict.items():
            self.radio_button = ttk.Radiobutton(
                self,
                text=game,
                variable=self.chosen_game,
                value=val,
                style=my_radio_button_style,
                width=20,
            )
            self.radio_button.bind(RETURN, partial(self.on_change_game, val))
            self.radio_button.grid(column=0, row=val + 1)
            if val == 0:
                self.radio_button.focus_set()

        # set up buttons
        self.line = ttk.Separator(self, orient=tk.HORIZONTAL)
        self.line.grid(column=0, row=len(games_dict) + 3, sticky=tk.EW, pady=5)

        self.button_play = ttk.Button(self, text="Play!", style=my_button_style)
        self.button_play.bind(LEFT_MOUSE_BUTTON, partial(self.on_play))
        self.button_play.bind(RETURN, partial(self.on_play))
        self.button_play.grid(column=0, row=len(games_dict) + 4)
        self.button_quit = ttk.Button(
            self, text="Quit!", style=my_button_style, command=self.on_quit
        )
        self.button_quit.grid(column=0, row=len(games_dict) + 5)
        self.button_quit.bind(RETURN, partial(self.on_quit))

    def on_change_game(self, *args) -> None:
        self.chosen_game.set(args[0])

    def on_play(self, _) -> None:
        if self.controller:
            self.controller.click_play()

    def on_quit(self) -> None:
        self.master.destroy()

    def set_controller(self, controller: StartController) -> None:
        self.controller = controller


class BaseView(ttk.Frame):
    def __init__(self, parent: BaseApp) -> None:
        super().__init__(parent)
        self.images_on_canvas = None
        self.deck_area = None
        self.hand_area = None
        self.play_area = None
        self.score_area = None
        self.vbar = None
        self.hbar = None
        self.canvas_area = None
        self.canvas = None
        self.controller = None
        self.parent = parent
        # Create menu bar
        menu_bar = tk.Menu(parent)
        file_menu = tk.Menu(menu_bar, tearoff=False, font=BASIC_FONT)
        file_menu.add_command(label="Quit", command=self.quit, underline=0)
        menu_bar.add_cascade(label="Menu", menu=file_menu, underline=0)
        self.parent.config(menu=menu_bar)

        self.grid_columnconfigure((15, 16), minsize=75)

        # insert title
        ttk.Label(self, text=self.parent.chosen_game, font=TITLE_FONT).grid(
            column=0, row=0, columnspan=17
        )

    def set_controller(self, controller: BaseController) -> None:
        self.controller = controller

    def quit(self) -> None:
        self.parent.destroy()

    def add_card_to_canvas(self, *args, **kwargs) -> None:
        # Placeholder for child class
        pass

    def delete_card_from_canvas(self, *args, **kwargs) -> None:
        # Placeholder for child class
        pass
