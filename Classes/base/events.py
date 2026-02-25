from dataclasses import dataclass


@dataclass
class ModelEvent:
    type: str
    data: dict


class ModelObserver:
    def on_model_change(self, event: ModelEvent) -> None:
        """Wird aufgerufen, wenn sich das Model ändert."""
        raise NotImplementedError
