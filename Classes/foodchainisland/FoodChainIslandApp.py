from Classes.base.apps import BaseApp


class FoodChainIslandApp(BaseApp):
    def __init__(self, options: dict = None) -> None:
        super().__init__("Food Chain Island", options)
