import tkinter as tk
from functools import partial
from math import sqrt, pi, exp
from tkinter import ttk
from tkinter.ttk import Label

from PIL import Image, ImageTk
from PIL.ImageTk import PhotoImage

from Utils.globals import TITLE_FONT, BASIC_FONT, BOLD_FONT, LEFT_MOUSE_BUTTON

DIFFICULTY01 = "Resources/Assets/Difficulty01.gif"


class MyLabel(ttk.Label):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.active = False
        self.value = 0


class OptionsModel:

    def __init__(self) -> None:
        self.options = {"difficulty": 1}


class OptionsView(tk.Toplevel):
    def __init__(self, parent: tk.Tk, game_name: str) -> None:
        super().__init__(parent)
        self.parent = parent
        self.game_name = game_name
        self.controller = None
        self.switch_difficulty = tk.PhotoImage(file=DIFFICULTY01, format="gif -index 0")

        self.title("Options")

        # Get screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate position to centre the window
        window_width = 500
        window_height = 500
        offset_x = (screen_width - window_width) // 2
        offset_y = (screen_height - window_height) // 2

        # Set geometry with position
        self.geometry(f"{window_width}x{window_height}+{offset_x}+{offset_y}")
        self.resizable(False, False)

        # Configure grid
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Configure styles
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
            foreground=[("selected", "black"), ("!selected", "grey")],
        )

        # Insert title
        ttk.Label(self, text="Options", font=TITLE_FONT).grid(
            column=0, row=0, columnspan=6, pady=20
        )

        ttk.Label(self, text="Difficulty", font=BOLD_FONT).grid(
            column=4, row=1, columnspan=2, pady=10
        )
        ttk.Label(self, text="Easy\n\nStandard\n\nHard", font=BASIC_FONT).grid(
            column=5, row=2, sticky="W", rowspan=5, padx=20
        )
        self.scale_difficulty = MyLabel(self, image=self.switch_difficulty)
        self.scale_difficulty.value = 1
        self.scale_difficulty.bind(LEFT_MOUSE_BUTTON, partial(self.on_click_diff))
        self.scale_difficulty.grid(column=4, row=2, rowspan=5, sticky="E", padx=20)

        # Add a button to confirm the options
        self.confirm_button = ttk.Button(
            self, text="Confirm", style=my_button_style, command=self.on_confirm
        )
        self.confirm_button.grid(column=0, row=6, pady=20)

        # Configure grid weights for rows and columns to center the widgets
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_rowconfigure(5, weight=1)
        self.grid_rowconfigure(6, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=1)
        self.grid_columnconfigure(5, weight=1)

    def set_controller(self, controller: object) -> None:
        self.controller = controller

    def on_confirm(self) -> None:
        if self.controller:
            self.controller.on_confirm()

    def on_click_diff(self, *args) -> None:
        event = None
        for arg in args:
            # Check for left mouse button event
            if arg.type == tk.EventType("4") and arg.num == 1:
                event = arg
        if self.controller:
            self.controller.click_diff(event)


class OptionsController:

    def __init__(self, model: OptionsModel, view: OptionsView) -> None:
        self.model = model
        self.view = view
        self.view.set_controller(self)

    def on_confirm(self) -> None:
        self.view.destroy()

    def click_diff(self, event: tk.Event) -> None:
        scale = event.widget
        y_click = event.y
        frames_scale = []
        match scale.value:
            case 0:
                scale.value = 1
                frames_scale = get_frames_from_gif(DIFFICULTY01)
                frames_scale.reverse()
            case 1:
                if y_click >= 96:
                    scale.value = 2
                    frames_scale = get_frames_from_gif(
                        "Resources/Assets/Difficulty12.gif"
                    )
                    frames_scale.reverse()
                else:
                    scale.value = 0
                    frames_scale = get_frames_from_gif(DIFFICULTY01)
            case 2:
                scale.value = 1
                frames_scale = get_frames_from_gif("Resources/Assets/Difficulty12.gif")
        play_gif(self.view, scale, frames_scale, False, [35, 2, 125])
        self.model.difficulty = scale.value
        self.model.options["difficulty"] = self.model.difficulty


class OptionsWindow:
    def __init__(self, parent: tk.Tk, game_name: str) -> None:
        self.model = OptionsModel()
        self.view = OptionsView(parent, game_name)
        self.controller = OptionsController(self.model, self.view)

    def get_options(self) -> dict:
        return self.model.options


def play_gif(
    view: OptionsView,
    label: Label,
    frames: list[PhotoImage],
    loop: bool,
    variable_delay: list[float],
) -> None:
    frame = None
    label.image = None
    # delay for scheduling later frames
    total_delay = 0
    # delay between frames
    delay_frames = 40
    # scheduling event for every frame
    for i, frame in enumerate(frames):
        if variable_delay:
            m = (len(frames) - 1) / 2
            l = variable_delay[0]
            s = variable_delay[1]
            a = variable_delay[2]
            delay_frames = smooth(i, m, l, s, a)
        view.after(
            total_delay,
            display_next_frame,
            view,
            frame,
            label,
            frames,
            loop,
            variable_delay,
        )
        total_delay += delay_frames
    # schedule restart after all frames are done
    if loop:
        view.after(
            total_delay,
            display_next_frame,
            view,
            frame,
            label,
            frames,
            loop,
            variable_delay,
            True,
        )
    else:
        label.image = frame
        label.config(image=label.image)


def smooth(x: int, m: float, l: float, s: float, a: float) -> int:
    # Using a normal distribution to get smooth animations
    return int(l - a / (s * sqrt(2 * pi)) * exp(-0.5 * ((x - m) / s) ** 2))


def display_next_frame(
    view: OptionsView,
    frame: PhotoImage,
    label: Label,
    frames: list[PhotoImage],
    loop: bool,
    variable_delay: bool,
    restart: bool = False,
) -> None:
    if restart:
        try:
            label.config
        except tk.TclError:
            return
        # start over after restart
        play_gif(view, label, frames, loop, variable_delay)
        return
    try:
        label.config(image=frame)
    except tk.TclError:
        return


def get_frames_from_gif(img: PhotoImage) -> list:
    with Image.open(img) as gif:
        index = 0
        frames = []
        while True:
            try:
                gif.seek(index)
                gif_transparent = gif.convert("RGBA")
                frame = ImageTk.PhotoImage(gif_transparent)
                frames.append(frame)
            except EOFError:
                break
            index += 1
        return frames
