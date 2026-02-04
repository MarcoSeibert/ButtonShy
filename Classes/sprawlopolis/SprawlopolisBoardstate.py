from Classes.base.boardstate import BaseBoardstate


class SprawlopolisBoardstate(BaseBoardstate):
    def __init__(self, game_data):
        super().__init__(game_data)
        self.scores = {"orange": 0, "grey": 0, "blue": 0, "green": 0, "roads": 0}
        self.grid_size = self.game_data["grid_size"]

    def get_total_score(self) -> int:
        return sum(self.scores.values())

    def add_card_to_board(self, card, coordinates):
        pass
        # self.controller.draw_card(card, coordinates)
