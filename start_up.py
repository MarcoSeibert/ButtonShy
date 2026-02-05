import json
import os
import time
import tkinter as tk
from multiprocessing import Pool, cpu_count, Manager, Queue
from threading import Thread
from tkinter import ttk

import pymupdf

games_dict = {}
ASSET_BASE_PATH = "Resources/Assets"


def extract_images(args: tuple) -> None:
    game_name, first_page = args
    pdf_path = f"Resources/PnPs/{game_name}.pdf"
    output_folder = f"{ASSET_BASE_PATH}/{game_name}/Cards/"
    os.makedirs(output_folder, exist_ok=True)  # Ensure the folder exists
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
    """Creates assets for a game and returns the name and elapsed time."""
    game_name, game_data = args
    start_time = time.time()
    # Delete existing assets for this game
    game_asset_path = f"{ASSET_BASE_PATH}/{game_name}/Cards/"
    if os.path.exists(game_asset_path):
        for asset_file in os.listdir(game_asset_path):
            os.remove(os.path.join(game_asset_path, asset_file))

    # Determine first_page
    first_page = 0
    for game in game_data:
        if game["name"] == game_name:
            first_page = game["first_page_with_cards"]
            break

    extract_images((game_name, first_page))
    elapsed = time.time() - start_time
    return game_name, elapsed


def process_game(args: tuple, result_queue: Queue) -> None:
    """Wrapper function for multiprocessing."""
    game_name, elapsed = create_assets(args)
    result_queue.put((game_name, elapsed))


def check_for_assets(result_queue: Queue, games_to_process: list) -> None:
    """Checks and creates assets, sends progress to the queue."""
    global games_dict

    if games_to_process:
        with Pool(cpu_count()) as pool:
            pool.starmap(
                process_game, [(args, result_queue) for args in games_to_process]
            )


def show_loading_window() -> None:
    """Shows a loading window with dynamic list, color coding, and remaining time."""
    root = tk.Tk()
    root.title("Loading Assets...")
    root.geometry("550x450")

    # Frame for the list of games
    list_frame = ttk.Frame(root)
    list_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Label for the title
    list_label = ttk.Label(list_frame, text="Games being processed:")
    list_label.pack(anchor=tk.W)

    # Text widget for the list of games (with scrollbar)
    game_list_text = tk.Text(
        list_frame, height=15, width=60, state="normal", wrap=tk.WORD
    )
    game_list_scroll = ttk.Scrollbar(
        list_frame, orient="vertical", command=game_list_text.yview
    )
    game_list_text.configure(yscrollcommand=game_list_scroll.set)
    game_list_scroll.pack(side=tk.RIGHT, fill=tk.Y)
    game_list_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    game_list_text.tag_config("done", foreground="green")

    # Progress bar and remaining time
    progress_frame = ttk.Frame(root)
    progress_frame.pack(pady=10, fill=tk.X)
    progress = ttk.Progressbar(
        progress_frame, orient="horizontal", length=300, mode="determinate"
    )
    progress.pack(pady=5)
    progress_label = ttk.Label(progress_frame, text="Progress: 0/0")
    progress_label.pack(side=tk.LEFT, padx=5)
    time_label = ttk.Label(progress_frame, text="Estimated time left: calculating...")
    time_label.pack(side=tk.RIGHT, padx=5)

    # Count games to be processed
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

    # Show all games in the list
    game_list_text.insert(
        tk.END, "\n".join([f"- {game[0]}" for game in games_to_process])
    )
    progress["maximum"] = len(games_to_process)
    manager = Manager()
    result_queue = manager.Queue()
    processed_names = []
    avg_time_per_game = 5.0  # Default estimate (will be updated)

    def update_progress() -> None:
        processed_games = 0
        total_elapsed = 0.0
        nonlocal avg_time_per_game

        while processed_games < progress["maximum"]:
            try:
                game_name, elapsed = result_queue.get(timeout=0.1)
                if game_name not in processed_names:
                    processed_names.append(game_name)
                    game_list_text.delete(1.0, tk.END)
                    for name, _ in games_to_process:
                        if name in processed_names:
                            game_list_text.insert(tk.END, f"✓ {name}\n", "done")
                        else:
                            game_list_text.insert(tk.END, f"- {name}\n")
                    total_elapsed += elapsed
                    avg_time_per_game = (
                        total_elapsed / len(processed_names) if processed_names else 5.0
                    )
                processed_games = len(processed_names)
                progress["value"] = processed_games
                progress_label.config(
                    text=f"Progress: {processed_games}/{progress['maximum']}"
                )

                # Calculate estimated remaining time
                remaining_games = progress["maximum"] - processed_games
                estimated_time_left = remaining_games * avg_time_per_game
                time_label.config(
                    text=f"Estimated time left: {estimated_time_left:.1f} seconds"
                )

                root.update()
            except:
                continue
        time_label.config(text="All games processed!")
        root.destroy()

    Thread(
        target=check_for_assets, args=(result_queue, games_to_process), daemon=True
    ).start()

    # Start progress updates
    root.after(10, update_progress)
    root.mainloop()
