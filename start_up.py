import json
import os
import time
from multiprocessing import Pool, cpu_count, Queue

import pymupdf

games_dict = {}
ASSET_BASE_PATH = "Resources/Assets"


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
            with open(
                f"{output_folder}/{game_name}_{page_num}_{img_index}.png", "wb"
            ) as f:
                f.write(image_bytes)


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
                nr_of_cards = (
                    2 * game["double_sided_cards"]
                    + game["single_sided_cards"]
                    + game["backsides"]
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
                break

    if games_to_process:
        with Pool(cpu_count()) as pool:
            pool.starmap(process_game, [(args, None) for args in games_to_process])
