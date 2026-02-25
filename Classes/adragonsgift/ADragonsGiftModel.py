import json
import os
import random

import networkx as nx

from Classes.base.events import ModelEvent
from Classes.base.models import BaseModel, BaseCard
from Utils.functions import load_and_adjust_image


class ADragonsGiftModel(BaseModel):
    def __init__(self, game_data: dict, _) -> None:
        super().__init__(game_data, None)
        self.transport_cards = []
        self.village_cards, self.gift_cards = self.create_decks_of_cards()
        self.score = 0
        self.start_position_on_canvas = self.game_data.get("start_position")

        with open("Resources/Assets/A Dragon's Gift/cards_data.json", "r") as file:
            self.cards_data = json.load(file)["cards"]
        self.graph = nx.Graph()

        # draw three transport cards
        for _ in range(3):
            given_card = random.choice(self.gift_cards)
            self.gift_cards.remove(given_card)
            self.transport_cards.append(given_card)

        # draw a gift card
        given_card = random.choice(self.gift_cards)
        self.gift_cards.remove(given_card)
        self.gift_card = given_card

        # draw an initial hand card
        given_card = random.choice(self.village_cards)
        self.village_cards.remove(given_card)
        self.hand_card = given_card

    def play_first_card(self) -> None:
        card_to_play = self.village_cards[0]
        self.village_cards.remove(card_to_play)
        self.talk_to_observer(param="play_first_card", obj=card_to_play)
        self.add_card_to_graph(card_to_play, self.start_position_on_canvas)

    def talk_to_observer(self, param: str, obj: object = None) -> None:
        if param == "play_first_card":
            event = ModelEvent("FIRST_CARD_PLAYED", {"card": obj})
        else:
            event = ModelEvent(param.upper(), {})
        self.notify_observers(event)

    def add_card_to_graph(self, card_to_play: BaseCard, position: tuple) -> None:
        # todo
        print("Hi")

    def create_decks_of_cards(self) -> tuple:
        village_cards = []
        gift_cards = []
        mapping_data = self.game_data["mapping"]

        fp = f"Resources/Assets/{self.game_data["name"]}/cards"
        for image_file in os.listdir(fp):
            page_nr, card_nr = image_file.split(".")[0].split("_")[1:]
            mapping_id = page_nr + "_" + card_nr
            card_id = mapping_data[mapping_id]["card_id"]
            side = mapping_data[mapping_id]["side"]
            adjusted_photo_image, adjusted_photo = load_and_adjust_image(fp, image_file)
            if side == "front":
                self.front_image_dict[card_id] = adjusted_photo
            elif side == "back":
                self.back_image_dict[card_id] = adjusted_photo
            if card_id <= 12:
                relevant_deck = village_cards
            else:
                relevant_deck = gift_cards
            card_in_list = next(
                (card for card in relevant_deck if card.card_id == card_id), None
            )
            if card_in_list is None:
                new_card = BaseCard(card_id, side, adjusted_photo_image)
                relevant_deck.append(new_card)
            else:
                card_in_list.add_image(side, adjusted_photo_image)

        random.shuffle(village_cards)
        random.shuffle(gift_cards)
        return village_cards, gift_cards

    def is_placement_valid(self, grid_x: float, grid_y: float) -> bool:
        # todo
        return True
