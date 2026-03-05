import json
import random

import networkx as nx

from Classes.base.events import ModelEvent
from Classes.base.models import BaseModel, BaseCard


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
        def deck_selector(card_id: int) -> str:
            return "village_cards" if card_id <= 12 else "gift_cards"

        return super()._create_decks_of_cards(deck_selector)

    def is_placement_valid(self, grid_x: float, grid_y: float) -> bool:
        # todo
        return True
