import os.path
from importlib import import_module
from typing import TYPE_CHECKING

import PIL
from PIL import Image, ImageTk, ImageDraw

from globals import CARD_SIZE

if TYPE_CHECKING:
    from Classes.base.apps import StartApp


def start_game(app: StartApp, chosen_game_name: str) -> None:
    app.destroy()
    app_class = getattr(
        import_module(f"Classes.{chosen_game_name.lower()}.{chosen_game_name}App"),
        f"{chosen_game_name}App",
    )
    app_game = app_class(chosen_game_name)
    app_game.focus_force()
    app_game.mainloop()


def get_game_data_by_name(json_data: dict, game_name: str) -> dict:
    for game in json_data:
        if game["name"] == game_name:
            return game
    return {}


def load_and_adjust_image(
    fp: str,
    image_name: str,
    card_size: tuple = CARD_SIZE,
    radius: int = 5,
    border_size: int = 3,
) -> tuple[ImageTk.PhotoImage, PIL.Image.Image, PIL.Image.Image]:
    # Bild öffnen, drehen und Größe anpassen
    with Image.open(os.path.join(fp, image_name)) as img:
        img = img.convert("RGBA").rotate(-90, expand=True)

        adjusted_image = adjust_image(img, border_size, card_size, radius)
        golden_border = adjust_image(
            img, border_size, card_size, radius, (255, 215, 0, 255)
        )

        return ImageTk.PhotoImage(adjusted_image), adjusted_image, golden_border


def adjust_image(
    img: Image.Image,
    border_size: int = 3,
    card_size: tuple = CARD_SIZE,
    radius: int = 5,
    color: tuple = (0, 0, 0, 255),
) -> Image.Image:
    # 1. Bild auf die gewünschte Größe skalieren
    img = img.resize(card_size)

    # 2. Originalbild zuschneiden (ohne Rahmen)
    original_img = img.crop(
        (
            border_size,
            border_size,
            card_size[0] - border_size,
            card_size[1] - border_size,
        )
    )

    # 3. Maske für das Originalbild erstellen (abgerundete Ecken)
    mask = Image.new("L", original_img.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, *original_img.size), radius, fill=255)
    original_img.putalpha(mask)

    # 4. Neues Bild mit Rahmen erstellen
    adjusted_image = Image.new(
        "RGBA",
        card_size,
        (0, 0, 0, 0),  # Transparenter Hintergrund
    )

    # 5. Rahmen zeichnen
    ImageDraw.Draw(adjusted_image).rounded_rectangle(
        (0, 0, card_size[0] - 1, card_size[1] - 1),
        radius + border_size,
        fill=color,
    )

    # 6. Originalbild (mit Maske) in den Rahmen einfügen
    adjusted_image.paste(
        original_img,
        (border_size, border_size),
        original_img,  # Maske wird automatisch verwendet
    )

    return adjusted_image
    # # Maske für abgerundete Ecken erstellen
    # img = img.resize(card_size)
    # mask = Image.new("L", card_size, 0)
    # ImageDraw.Draw(mask).rounded_rectangle((0, 0, *card_size), radius, fill=255)
    # img.putalpha(mask)
    # # Rahmen hinzufügen
    # adjusted_image = Image.new(
    #     "RGBA",
    #     (card_size[0] + border_size * 2, card_size[1] + border_size * 2),
    #     (0, 0, 0, 0),
    # )
    # ImageDraw.Draw(adjusted_image).rounded_rectangle(
    #     (0, 0, *adjusted_image.size), radius + border_size, fill=color
    # )
    # adjusted_image.paste(img, (border_size, border_size), img)
    # # Endgröße anpassen und zurückgeben
    # return adjusted_image.resize(card_size)


def import_mvc_components(components: dict, chosen_game_name: str) -> tuple:
    model_class = getattr(
        import_module(f"Classes.{chosen_game_name.lower()}.{chosen_game_name}Model"),
        components["model"],
    )
    controller_class = getattr(
        import_module(
            f"Classes.{chosen_game_name.lower()}.{chosen_game_name}Controller"
        ),
        components["controller"],
    )
    view_class = getattr(
        import_module(f"Classes.{chosen_game_name.lower()}.{chosen_game_name}View"),
        components["view"],
    )

    return model_class, view_class, controller_class
