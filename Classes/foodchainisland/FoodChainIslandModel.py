from collections import defaultdict

from Classes.base.models import BaseModel, BaseCard


class FoodChainIslandModel(BaseModel):
    def __init__(self, game_data: dict, options: dict = None) -> None:
        super().__init__(game_data, options)
        self.grid = defaultdict(lambda: defaultdict(BaseCard))
        # draw the cards
        for i, card in enumerate(self.cards[0]):
            x = i % 4
            y = i // 4
            self.grid[x][y] = card

    def create_decks_of_cards(self) -> tuple:
        def deck_selector(card_id: int | str) -> str:
            return "grid_cards" if isinstance(card_id, int) else "sea_animal_cards"

        return super()._create_decks_of_cards(deck_selector)
