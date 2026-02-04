class BoardStateEvent:
    """Basis-Klasse für alle Events, die vom BoardState ausgelöst werden."""

    def __init__(self, event_type: str, data: dict):
        self.type = event_type  # z.B. "CARD_PLAYED"
        self.data = data  # z.B. {"card_id": "Technology", "position": (100, 200)}


# Optional: Spezifische Event-Klassen (falls du sie später brauchst)
class CardEvent(BoardStateEvent):
    def __init__(self, card, position: tuple):
        super().__init__("CARD_PLAYED", {"card_id": card.card_id, "position": position})


class ScoreEvent(BoardStateEvent):
    def __init__(self, player_id: str, new_score: int):
        super().__init__(
            "SCORE_UPDATED", {"player_id": player_id, "new_score": new_score}
        )
