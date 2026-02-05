import random

class SprawlopolisModel(BaseModel):
    def __init__(self, game_data):
        super().__init__(game_data)
        self.score_cards = []
        self.hand_cards = []
        self.number_of_decks = 1

        # draw three scoring card
        for _ in range(3):
            given_card = random.choice(self.cards)
            self.cards.remove(given_card)
            self.score_cards.append(given_card)

        # draw first card
        # self.boardstate.add_card_to_board(self.dict_of_decks[game].deal(), (30, 18))

        # draw three initial hand cards
        for _ in range(3):
            given_card = random.choice(self.cards)
            self.cards.remove(given_card)
            self.hand_cards.append(given_card)

    def play_first_card(self):
        pass

    def init_boardstate(self):
        self.boardstate = SprawlopolisBoardstate(self.game_data)


class SprawlopolisCard(BaseCard):
    def __init__(self, card_id, side, image):
        super().__init__(card_id, side, image)
        self.points = card_id
        self.blocks = None
        self.roads = None