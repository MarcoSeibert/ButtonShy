import os
import random
from typing import Callable

from PIL import ImageTk
from PIL.ImageTk import PhotoImage

from Classes.base.events import ModelObserver, ModelEvent
from Utils.functions import load_and_adjust_image
from Utils.globals import CARD_SIZE_ON_SCREEN, HORIZONTAL_GAMES


class BaseCard:
    def __init__(self, card_id: int | str, side: str, image: PhotoImage) -> None:
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
    def __init__(self, game_data: dict, options: dict) -> None:
        self.cards_data = None
        self.back_image_dict = {}
        self.front_image_dict = {}
        self.active_card = None
        self.game_data = game_data
        self.options = options if options else {}

        self.cards = self.create_decks_of_cards()

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

    def create_decks_of_cards(self) -> list:
        def deck_selector(_) -> str:
            return "main_deck"

        return self._create_decks_of_cards(deck_selector)

    def _create_decks_of_cards(self, deck_selector: Callable) -> tuple:
        decks = {}

        mapping_data = self.game_data["mapping"]
        fp = f"Resources/Assets/{self.game_data["name"]}/cards"
        for image_file in os.listdir(fp):
            page_nr, card_nr = image_file.split(".")[0].split("_")[1:]
            mapping_id = page_nr + "_" + card_nr
            card_id = mapping_data[mapping_id]["card_id"]
            side = mapping_data[mapping_id]["side"]
            adjusted_image = load_and_adjust_image(fp, image_file)
            card_size_on_screen = (
                tuple(reversed(CARD_SIZE_ON_SCREEN))
                if self.game_data["name"] in HORIZONTAL_GAMES
                else CARD_SIZE_ON_SCREEN
            )
            adjusted_photo_image = ImageTk.PhotoImage(
                adjusted_image.resize(card_size_on_screen)
            )

            if side == "front":
                self.front_image_dict[card_id] = adjusted_image
            elif side == "back":
                self.back_image_dict[card_id] = adjusted_image

            # Bestimme, zu welcher Liste die Karte gehört
            deck_key = deck_selector(card_id)

            if deck_key not in decks:
                decks[deck_key] = []

            relevant_deck = decks[deck_key]
            card_in_list = next(
                (card for card in relevant_deck if card.card_id == card_id), None
            )
            if card_in_list is None:
                new_card = BaseCard(card_id, side, adjusted_photo_image)
                relevant_deck.append(new_card)
            else:
                card_in_list.add_image(side, adjusted_photo_image)

        # Mische die Decks
        for key in decks:
            random.shuffle(decks[key])

        # Gib die Decks zurück
        if len(decks) == 1:
            return list(decks.values())[0]
        else:
            return tuple(decks.values())

    def is_placement_valid(self, *args, **kwargs) -> None:
        raise NotImplementedError

    def add_card_to_graph(self, *args, **kwargs) -> None:
        raise NotImplementedError

    def draw_new_card(self, *args, **kwargs) -> None:
        raise NotImplementedError
