import os
import random

from PIL.ImageTk import PhotoImage

from Classes.base.events import ModelObserver, ModelEvent
from functions import load_and_adjust_image


class BaseCard:
    def __init__(self, card_id: str, side: str, image: PhotoImage) -> None:
        self.card_id = card_id
        if side == "front":
            self.front_image = image
            self.back_image = None
        elif side == "back":
            self.front_image = None
            self.back_image = image

    def add_image(self, side: str, image: PhotoImage) -> None:
        if side == "front":
            self.front_image = image
        elif side == "back":
            self.back_image = image


class BaseModel:
    def __init__(self, game_data: dict) -> None:

        self.golden_front_image_dict = {}
        self.golden_back_image_dict = {}
        self.cards_data = None
        self.back_image_dict = {}
        self.front_image_dict = {}
        self.active_card = None
        self.boardstate = None
        self.hand_cards = None
        self.score_cards = None
        self.game_data = game_data

        self.cards = self.create_deck_of_cards()

        self.observers: list[ModelObserver] = []

    def add_observer(self, observer: ModelObserver) -> None:
        """Fügt einen Observer hinzu (z.B. den Controller)."""
        self.observers.append(observer)

    def notify_observers(self, event: ModelEvent) -> None:
        """Benachrichtigt alle Observer über ein Event."""
        for observer in self.observers:
            observer.on_model_change(event)

    def play_card(self, card: BaseCard, position: tuple) -> None:
        raise NotImplementedError()

    def create_deck_of_cards(self) -> list:
        cards = []
        mapping_data = self.game_data["mapping"]

        fp = f"Resources/Assets/{self.game_data["name"]}/cards"
        for image_file in os.listdir(fp):
            page_nr, card_nr = image_file.split(".")[0].split("_")[1:]
            mapping_id = page_nr + "_" + card_nr
            card_id = mapping_data[mapping_id]["card_id"]
            side = mapping_data[mapping_id]["side"]
            adjusted_photo_image, adjusted_photo, golden_bordered_image = (
                load_and_adjust_image(fp, image_file)
            )
            if side == "front":
                self.front_image_dict[card_id] = adjusted_photo
                self.golden_front_image_dict[card_id] = golden_bordered_image
            elif side == "back":
                self.back_image_dict[card_id] = adjusted_photo
                self.golden_back_image_dict[card_id] = golden_bordered_image
            card_in_list = next(
                (card for card in cards if card.card_id == card_id), None
            )
            if card_in_list is None:
                new_card = BaseCard(card_id, side, adjusted_photo_image)
                cards.append(new_card)
            else:
                card_in_list.add_image(side, adjusted_photo_image)
        random.shuffle(cards)
        return cards

    def is_placement_valid(self, *args, **kwargs) -> None:
        raise NotImplementedError

    def add_card_to_graph(self, *args, **kwargs) -> None:
        raise NotImplementedError

    def draw_new_card(self, *args, **kwargs) -> None:
        raise NotImplementedError
