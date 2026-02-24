from functools import partial
from tkinter import ttk
import pywinstyles
from PIL import ImageTk

from Classes.base.controllers import BaseController
from Classes.base.events import ModelEvent
from Classes.canvasgamecontroller import CanvasGameController
from Classes.sprawlopolis.SprawlopolisModel import SprawlopolisModel
from Classes.sprawlopolis.SprawlopolisView import SprawlopolisView
from globals import LEFT_MOUSE_BUTTON


class SprawlopolisController(BaseController, CanvasGameController):
    def __init__(self, model: SprawlopolisModel, view: SprawlopolisView) -> None:
        BaseController.__init__(self, model, view)
        CanvasGameController.__init__(self, model, view)

        # show goal scores
        self.view.goal_score.config(text=self.model.goal)  # type: ignore
        # add scoring cards to the grid
        self.scoring_card = ttk.Label(self.view.score_area)
        self.scoring_card = ttk.Label(self.view.score_area)
        self.scoring_card = ttk.Label(self.view.score_area)
        for i, card in enumerate(self.view.score_area.winfo_children()):
            card.grid(column=13, row=4 * i + 1, columnspan=2, rowspan=4)
            card.config(
                image=self.model.score_cards[i].back_image, background="#100001"
            )
            pywinstyles.set_opacity(card, color="#100001")

        # add initial hand cards to the grid
        for _ in range(3):
            self.hand_card = ttk.Label(self.view.hand_area)
        for i, card in enumerate(self.view.hand_area.winfo_children()):
            card.grid(column=1 + 2 * i, row=17, rowspan=2, columnspan=2)
        # add images to the cards
        for i, card in enumerate(self.view.hand_area.winfo_children()):
            card.config(
                image=self.model.hand_cards[i].front_image,
                background="#000001",
            )
            pywinstyles.set_opacity(card, color="#000001")
            card.bind(
                LEFT_MOUSE_BUTTON, partial(self.play_card, self.model.hand_cards[i])
            )

        # add deck to the grid
        self.next_card = ttk.Label(self.view.deck_area)
        self.next_card.grid(column=7, row=17, rowspan=2, columnspan=6)
        # add image to the card
        image = self.model.cards[0].front_image
        for card in self.view.deck_area.winfo_children():
            card.configure(image=image, background="#000001")
            pywinstyles.set_opacity(card, color="#000001")

    def on_model_change(self, event: ModelEvent) -> None:
        """Reagiert auf Events vom Model."""
        if event.type == "FIRST_CARD_PLAYED":
            self.controller_play_first_card(event)
        elif event.type == "DRAW_NEW_CARD":
            self.draw_new_card()
        elif event.type == "UPDATE_SCORES":
            self.update_scores()

    def controller_play_first_card(self, event: ModelEvent) -> None:
        card = event.data["card"]
        # update the deck
        image = self.model.cards[0].front_image
        for deck in self.view.deck_area.winfo_children():
            deck.configure(image=image, background="#000001")
        # show the first card on the canvas
        self.view.add_card_to_canvas(
            card, "front", (30, 18), self.grid_size, movable=False
        )

    def draw_new_card(self) -> None:
        if self.model.cards:
            image = self.model.cards[0].front_image
            for deck in self.view.deck_area.winfo_children():
                deck.configure(image=image, background="#000001")
        else:
            for deck in self.view.deck_area.winfo_children():
                deck.destroy()
        for i, card in enumerate(self.view.hand_area.winfo_children()):
            card.config(
                image=self.model.hand_cards[i].front_image,
                background="#000001",
            )

    def update_scores(self) -> None:
        scores = self.model.scores  # type: ignore
        self.view.orange_score.config(text=scores["orange"])  # type: ignore
        self.view.blue_score.config(text=scores["blue"])  # type: ignore
        self.view.grey_score.config(text=scores["grey"])  # type: ignore
        self.view.green_score.config(text=scores["green"])  # type: ignore
        self.view.street_score.config(text=scores["streets"])  # type: ignore

        self.view.goal_1.config(text=scores["goal_1"])  # type: ignore
        self.view.goal_2.config(text=scores["goal_2"])  # type: ignore
        self.view.goal_3.config(text=scores["goal_3"])  # type: ignore
        self.view.total_score.config(text=sum(scores.values()))  # type: ignore

    def press_turn(self, _) -> None:
        active_card_obj = None
        objs_with_movable_tag = self.view.canvas_area.find_withtag("movable")
        if objs_with_movable_tag:
            active_card_obj = objs_with_movable_tag[0]

        # change the image on the canvas
        old_image = self.model.front_image_dict[self.model.active_card.card_id]
        rotated_image = old_image.rotate(180, expand=True)
        self.model.front_image_dict[self.model.active_card.card_id] = rotated_image
        photo_image = ImageTk.PhotoImage(rotated_image)

        self.active_card_image = photo_image
        self.view.canvas_area.itemconfigure(active_card_obj, image=photo_image)

        # change the card data and image
        for i, card in enumerate(self.model.cards_data):
            if card["id"] == self.model.active_card.card_id:
                self.model.cards_data[i] = rotate_card_values(card)
                break
        self.model.active_card.front_image = photo_image

        # change the image in the hand area
        for i, card in enumerate(self.view.hand_area.winfo_children()):
            card.config(
                image=self.model.hand_cards[i].front_image,
                background="#000001",
            )


def rotate_card_values(card_data: dict) -> dict:
    def transform_coords(coords: list[int]) -> list[int]:
        return [1 - x for x in coords]

    def transform_direction(direction: str) -> str:
        direction_map = {
            "N": "S",
            "S": "N",
            "W": "E",
            "E": "W",
        }
        return direction_map.get(direction, direction)

    transformed = {
        "id": card_data["id"],
        "blocks": [
            {
                "coords": transform_coords(block["coords"]),
                "colour": block["colour"],
                "street": [transform_direction(d) for d in block["street"]],
            }
            for block in card_data["blocks"]
        ],
    }
    return transformed
