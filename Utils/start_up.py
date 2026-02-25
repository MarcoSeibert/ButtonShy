import json
import os
import time
from multiprocessing import Pool, cpu_count, Queue

import pymupdf
from PIL import Image

games_dict = {}
ASSET_BASE_PATH = "Resources/Assets"


def crop_and_resize_image(input_path: str, output_path: str, crop_margin: int) -> None:
    # Bild öffnen
    with Image.open(input_path) as image:
        # Bild in RGB-Modus konvertieren, falls notwendig
        if image.mode == "CMYK":
            image = image.convert("RGB")

        # Bild zuschneiden
        width, height = image.size
        cropped_image = image.crop(
            (crop_margin, crop_margin, width - crop_margin, height - crop_margin)
        )

        # Bild auf die ursprüngliche Größe skalieren
        resized_image = cropped_image.resize((width, height))

        # Bild speichern
        resized_image.save(output_path)


def extract_images(args: tuple) -> None:
    game_name, first_page = args
    pdf_path = f"Resources/PnPs/{game_name}.pdf"
    output_folder = f"{ASSET_BASE_PATH}/{game_name}/Cards/"
    os.makedirs(output_folder, exist_ok=True)
    doc = pymupdf.open(pdf_path)

    for page_num in range(len(doc)):
        if page_num < first_page:
            continue
        page = doc.load_page(page_num)
        for img_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_path = f"{output_folder}/{game_name}_{page_num}_{img_index}.png"
            with open(image_path, "wb") as f:
                f.write(image_bytes)

            # Bild zuschneiden und skalieren
            crop_and_resize_image(image_path, image_path, 40)


def create_assets(args: tuple) -> tuple:
    game_name, game_data = args
    start_time = time.time()
    game_asset_path = f"{ASSET_BASE_PATH}/{game_name}/Cards/"
    if os.path.exists(game_asset_path):
        for asset_file in os.listdir(game_asset_path):
            os.remove(os.path.join(game_asset_path, asset_file))

    first_page = 0
    for game in game_data:
        if game["name"] == game_name:
            first_page = game["first_page_with_cards"]
            break

    extract_images((game_name, first_page))
    elapsed = time.time() - start_time
    print(f"Created assets for {game_name}. Elapsed time: {elapsed:.2f} seconds")
    return game_name, elapsed


def process_game(args: tuple, result_queue: Queue = None) -> None:
    game_name, elapsed = create_assets(args)
    if result_queue:
        result_queue.put((game_name, elapsed))


def check_for_assets() -> None:
    with open("Resources/Games.json") as json_file:
        game_data = json.load(json_file)["games"]

    games_to_process = []
    for pnp_file in os.listdir("Resources/PnPs"):
        game_name = pnp_file.split(".")[0]
        for game in game_data:
            if game["name"] == game_name:
                games_to_process = get_games_to_process(
                    game, game_data, game_name, games_to_process
                )
                break

    if games_to_process:
        with Pool(cpu_count()) as pool:
            pool.starmap(process_game, [(args, None) for args in games_to_process])


def get_games_to_process(
    game: dict, game_data: dict, game_name: str, games_to_process: list
) -> list:
    nr_of_cards = (
        2 * game["double_sided_cards"] + game["single_sided_cards"] + game["backsides"]
    )
    game_asset_path = f"{ASSET_BASE_PATH}/{game_name}/Cards/"
    nr_of_assets = (
        sum(
            1
            for asset_file in os.listdir(game_asset_path)
            if asset_file.startswith(f"{game_name}_")
        )
        if os.path.exists(game_asset_path)
        else 0
    )
    if nr_of_assets != nr_of_cards:
        games_to_process.append((game_name, game_data))
    if "-" not in game_name:
        new_key = len(games_dict)
        games_dict[new_key] = game_name
    return games_to_process
