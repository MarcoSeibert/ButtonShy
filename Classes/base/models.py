class BaseModel:
    def __init__(self, game_data):
        self.grid_size = game_data.get("grid_size", [1, 1])