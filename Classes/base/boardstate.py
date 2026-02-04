from Classes.events import BoardStateEvent


class BaseBoardstate:
    def __init__(self, game_data):
        self.game_data = game_data
        self.board = None
        self.cards_in_hand = None
        self.cards_on_board = None

        self.scores = {}

        self.observers = []

    def add_observer(self, observer):
        print(f"Observer hinzugefügt: {observer}")  # Debug-Print
        self.observers.append(observer)

    def notify_observers(self, event):
        print(
            f"Benachrichtige {len(self.observers)} Observer: {[type(obs) for obs in self.observers]}"
        )
        for observer in self.observers:
            observer.on_boardstate_change(event)

    def play_card(self, card_id, position):
        print(f"Karte {card_id} auf Position {position} gespielt!")
        event = BoardStateEvent(
            "CARD_PLAYED", {"card_id": card_id, "position": position}
        )
        self.notify_observers(event)
