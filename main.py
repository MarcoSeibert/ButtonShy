import os
import simplejson as json
import pymupdf

from Classes.base.apps import StartApp


def extract_images(game_name, game_data):
    first_page = 0
    for game in game_data:
        if game["name"] == game_name:
            first_page = game["first_page_with_cards"]
            break

    pdf_path = f"Resources/PnPs/{game_name}.pdf"
    output_folder = "Resources/Assets/"
    doc = pymupdf.open(pdf_path)

    for page_num in range(len(doc)):
        if page_num < first_page:
            continue  # Überspringe Seiten vor first_page
        page = doc.load_page(page_num)
        for img_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            # Speichere das Bild mit Seitenzahl und Index im Dateinamen
            with open(f"{output_folder}/Sprawlopolis_{page_num}_{img_index}.png", "wb") as f:
                f.write(image_bytes)


def create_assets(game_name, game_data):
    print(f"Creating assets for game {game_name}...")
    # deleting existing files
    for asset_file in os.listdir("Resources/Assets"):
        if asset_file.split("_")[0] == game_name:
            os.remove("Resources/Assets/" + asset_file)
    extract_images(game_name, game_data)

def check_for_assets():
    with open("Resources/Games.json") as json_file:
        game_data = json.load(json_file)["games"]
    for pnp_file in os.listdir("Resources/PnPs"):
        game_name = pnp_file.split(".")[0]
        for game in game_data:
            if game["name"] == game_name:
                #check whether assets are already created
                nr_of_cards = game["nr_of_cards"]
                if game["double_sided_cards"]:
                    nr_of_cards *= 2
                nr_of_assets = 0
                for asset_file in os.listdir("Resources/Assets"):
                    if asset_file.split("_")[0] == game_name:
                        nr_of_assets += 1
                if nr_of_assets != nr_of_cards:
                    create_assets(game_name, game_data)
                break
        else:
            print(f"Game {game_name} is not in Games.json")



if __name__ == "__main__":
    check_for_assets()


    # app_start = StartApp()
    # app_start.mainloop()