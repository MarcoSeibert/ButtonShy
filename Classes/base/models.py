import os
import random
from importlib import import_module

from functions import adjust_image


class BaseModel:
    def __init__(self, game_data):
        self.hand_cards = None
        self.score_cards = None
        self.game_data = game_data

        self.cards = self.create_deck_of_cards()

    def create_deck_of_cards(self):
        cards = []
        mapping_data = self.game_data["mapping"]
        chosen_game_compact = self.game_data["name"].replace(" ", "").title()
        card_class = getattr(import_module(f"Classes.{chosen_game_compact.lower()}.{chosen_game_compact}Model"), f"{chosen_game_compact}Card")

        fp = f"Resources/Assets/{self.game_data["name"]}/cards"
        for image in os.listdir(fp):
            page_nr, card_nr = image.split(".")[0].split("_")[1:]
            mapping_id = page_nr + "_" + card_nr
            card_id = mapping_data[mapping_id]["card_id"]
            side = mapping_data[mapping_id]["side"]

            adjusted_image = adjust_image(fp, image)

            card_in_list = next((card for card in cards if card.card_id == card_id), None)
            if card_in_list is None:
                new_card = card_class(card_id, side, adjusted_image)
                cards.append(new_card)
            else:
                card_in_list.add_image(side, adjusted_image)
        random.shuffle(cards)
        return cards

class BaseCard:
    def __init__(self, card_id, side, image):
        self.card_id = card_id
        if side == "front":
            self.front_image = image
            self.back_image = None
        elif side == "back":
            self.front_image = None
            self.back_image = image

    def add_image(self, side, image):
        if side == "front":
            self.front_image = image
        elif side == "back":
            self.back_image = image