from Classes.base.apps import BaseApp


class SprawlopolisApp(BaseApp):
    def __init__(self, chosen_game_name: str) -> None:
        super().__init__(chosen_game_name)
        self.model.play_first_card()
