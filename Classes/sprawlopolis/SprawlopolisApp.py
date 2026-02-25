from Classes.base.apps import BaseApp


class SprawlopolisApp(BaseApp):
    def __init__(self, options: dict = None) -> None:
        super().__init__("Sprawlopolis", options)
        self.model.play_first_card()
