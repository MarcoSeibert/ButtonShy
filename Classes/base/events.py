from dataclasses import dataclass


@dataclass
class ModelEvent:
    type: str  # z.B. "CARD_PLAYED"
    data: dict  # z.B. {"card_id": 15, "position": (18, 30)}


class ModelObserver:
    def on_model_change(self, event: ModelEvent) -> None:
        """Wird aufgerufen, wenn sich das Model ändert."""
        raise NotImplementedError
