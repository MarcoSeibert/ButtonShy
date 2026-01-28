import tkinter as tk
from globals import TITLE_FONT,BASIC_FONT, LEFT_MOUSE_BUTTON, GAMES
from tkinter import ttk
from functools import partial


class StartView(ttk.Frame):
    def __init__(self, parent: tk.Tk):
        super().__init__(parent)
        self.controller = None
        self.chosen_game = tk.IntVar()
        self.chosen_game.set(0)

        # creating frame
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # insert title
        ttk.Label(self, text="Button Shy digital", font=TITLE_FONT).grid(column=0, row=0)

        # configure styles
        style_buttons = ttk.Style()
        my_button_style = "MyButton.TButton"
        style_buttons.configure(my_button_style, font=BASIC_FONT)
        radio_style_buttons = ttk.Style()
        my_radio_button_style = "MyRadioButton.Toolbutton"
        radio_style_buttons.configure(my_radio_button_style, font=BASIC_FONT, background="white", anchor="c")
        radio_style_buttons.map(my_radio_button_style, foreground=[('selected', 'black'), ('!selected', 'gray')])

        # set up game radio buttons
        for val, game in GAMES.items():
            self.radio_button = ttk.Radiobutton(self, text=game, variable=self.chosen_game, value=val, style=my_radio_button_style, width=20)
            self.radio_button.bind("<Return>", partial(self.on_change_game, val))
            self.radio_button.grid(column=0, row=val+1)
            if val == 0:
                self.radio_button.focus_set()

        # set up buttons
        self.line = ttk.Separator(self, orient=tk.HORIZONTAL)
        self.line.grid(column=0, row=len(GAMES)+3, sticky=tk.EW, pady=5)

        self.button_play = ttk.Button(self, text="Play!", style=my_button_style)
        self.button_play.bind(LEFT_MOUSE_BUTTON, partial(self.on_play))
        self.button_play.bind("<Return>", partial(self.on_play))
        self.button_play.grid(column=0, row=len(GAMES)+4)
        self.button_quit = ttk.Button(self, text="Quit!", style=my_button_style, command=self.on_quit)
        self.button_quit.grid(column=0, row=len(GAMES)+5)
        self.button_quit.bind("<Return>", partial(self.on_quit))

    def on_change_game(self, *args):
        self.chosen_game.set(args[0])

    def on_play(self, *args):
        if self.controller:
            self.controller.click_play()

    def on_quit(self):
        self.master.destroy()

    def set_controller(self, controller):
        self.controller = controller

class BaseView(ttk.Frame):
    def __init__(self, parent: tk.Tk):
        super().__init__(parent)
        self.controller = None
        # Create menu bar
        menu_bar = tk.Menu(parent)
        file_menu = tk.Menu(menu_bar, tearoff=False, font=BASIC_FONT)
        file_menu.add_command(label="Quit", command=self.quit, underline=0)
        menu_bar.add_cascade(label="Menu", menu=file_menu, underline=0)
        parent.config(menu=menu_bar)

        self.grid_columnconfigure((15, 16), minsize=75)

        # insert title
        chosen_game_title = GAMES[self.master.chosen_game]
        ttk.Label(self, text=chosen_game_title, font=TITLE_FONT).grid(column=0, row=0, columnspan=17)


    def set_controller(self, controller):
        self.controller = controller

    def quit(self):
        self.master.destroy()