from Classes.base.apps import BaseApp


class ADragonsGiftApp(BaseApp):
    def __init__(self) -> None:
        super().__init__("A Dragon's Gift")
        self.model.play_first_card()
