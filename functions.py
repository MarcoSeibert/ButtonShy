import os.path
from importlib import import_module

from PIL import Image, ImageTk, ImageDraw

from globals import CARD_SIZE


def start_game(app, chosen_game_name):
    app.destroy()
    app_class = getattr(
        import_module(f"Classes.{chosen_game_name.lower()}.{chosen_game_name}App"),
        f"{chosen_game_name}App",
    )
    app_game = app_class(chosen_game_name)
    app_game.focus_force()
    app_game.mainloop()


def get_game_data_by_name(json_data, game_name):
    for game in json_data:
        if game["name"] == game_name:
            return game
    return None


def adjust_image(fp, image_name, card_size=CARD_SIZE, radius=5, border_size=3):
    # Bild öffnen, drehen und Größe anpassen
    with Image.open(os.path.join(fp, image_name)) as img:
        img = img.convert("RGBA").rotate(-90, expand=True).resize(card_size)

        # Maske für abgerundete Ecken erstellen
        mask = Image.new("L", card_size, 0)
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, *card_size), radius, fill=255)
        img.putalpha(mask)

        # Rahmen hinzufügen
        border = Image.new(
            "RGBA",
            (card_size[0] + border_size * 2, card_size[1] + border_size * 2),
            (0, 0, 0, 0),
        )
        ImageDraw.Draw(border).rounded_rectangle(
            (0, 0, *border.size), radius + border_size, fill=(0, 0, 0, 255)
        )
        border.paste(img, (border_size, border_size), img)

        # Endgröße anpassen und zurückgeben
        return ImageTk.PhotoImage(border.resize(card_size))


def import_mvc_components(components, chosen_game_name: str):
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
