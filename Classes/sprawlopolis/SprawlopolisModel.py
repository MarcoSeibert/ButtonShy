from Classes.base.models import BaseModel, BaseCard
import random

from Classes.sprawlopolis.SprawlopolisBoardstate import SprawlopolisBoardstate


class SprawlopolisModel(BaseModel):
    def __init__(self, game_data):
        super().__init__(game_data)
        self.score_cards = []
        self.hand_cards = []
        self.number_of_decks = 1
        self.boardstate = SprawlopolisBoardstate

        # draw three scoring card
        for _ in range(3):
            given_card = random.choice(self.cards)
            self.cards.remove(given_card)
            self.score_cards.append(given_card)

        # draw first card
        first_card = self.cards[0]
        self.cards.remove(first_card)
        self.boardstate.add_card_to_board(self, first_card, (30, 18))
        # self.boardstate.play_card(card_id=first_card, position=(30, 18))

        # draw three initial hand cards
        for _ in range(3):
            given_card = random.choice(self.cards)
            self.cards.remove(given_card)
            self.hand_cards.append(given_card)


class SprawlopolisCard(BaseCard):
    def __init__(self, card_id, side, image):
        super().__init__(card_id, side, image)
        self.points = card_id
        self.blocks = None
        self.roads = None
