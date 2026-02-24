from Classes.base.apps import BaseApp


class SprawlopolisApp(BaseApp):
    def __init__(self, chosen_game_name: str, options: dict = None) -> None:
        super().__init__(chosen_game_name, options)
        self.model.play_first_card()
