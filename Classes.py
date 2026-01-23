# Base classes
class GameModel:
    def __init__(self):
        pass

class GameView:
    def render(self, model):
        # Generic rendering logic
        pass

class GameController:
    def handle_input(self, input):
        # Generic input handling
        pass

# Game-specific subclasses
# -opolis games
class OpolisModel(GameModel):
    def __init__(self):
        super().__init__()
        # Unique to -opolis games

class OpolisView(GameView):
    def render(self, model):
        # Custom rendering for -opolis games
        pass

class OpolisController(GameController):
    def handle_input(self, input):
        # Input:
        #   put a card on the board, confirm the card, reset the card, rotate the card
        #   rotate a card in hand
        pass