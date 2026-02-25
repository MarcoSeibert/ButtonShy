import json
import random

import networkx as nx

import Utils.Sprawlopolis.scoring_functions as sf
from Classes.base.events import ModelEvent
from Classes.base.models import BaseModel, BaseCard
from Utils.Sprawlopolis.functions import (
    calculate_streets,
    add_blocks_to_graph,
    add_streets_to_graph,
)


class SprawlopolisModel(BaseModel):
    def __init__(self, game_data: dict, options: dict = None) -> None:
        super().__init__(game_data, options)
        self.loops = []
        self.streets = {}
        self.score_cards = []
        self.hand_cards = []
        self.scores = {
            "streets": 0,
            "green": 0,
            "blue": 0,
            "orange": 0,
            "grey": 0,
            "goal_1": 0,
            "goal_2": 0,
            "goal_3": 0,
        }
        self.goal = 0
        self.start_position_on_canvas = self.game_data.get("start_position")

        with open("Resources/Assets/Sprawlopolis/cards_data.json", "r") as file:
            self.cards_data = json.load(file)["cards"]
        self.graph = nx.Graph()

        # draw three scoring cards
        for _ in range(3):
            given_card = random.choice(self.cards)
            self.cards.remove(given_card)
            self.score_cards.append(given_card)
            self.goal += given_card.card_id

        # draw three initial hand cards
        for _ in range(3):
            given_card = random.choice(self.cards)
            self.cards.remove(given_card)
            self.hand_cards.append(given_card)

    def play_first_card(self) -> None:
        card_to_play = self.cards[0]
        self.cards.remove(card_to_play)
        self.talk_to_observer(param="play_first_card", obj=card_to_play)
        self.add_card_to_graph(card_to_play, self.start_position_on_canvas)

    def talk_to_observer(self, param: str, obj: object = None) -> None:
        if param == "play_first_card":
            event = ModelEvent("FIRST_CARD_PLAYED", {"card": obj})
        else:
            event = ModelEvent(param.upper(), {})
        self.notify_observers(event)

    def draw_new_card(self) -> None:
        new_card = self.cards[0]
        self.cards.remove(new_card)
        self.hand_cards.append(new_card)
        self.talk_to_observer(param="draw_new_card", obj=new_card)

    def update_scores(self) -> None:
        # base scores
        self.streets = calculate_streets(self.graph)
        self.scores["streets"] = -len(self.streets[0])
        block_scores = sf.calculate_connected_groups(self.graph)
        for colour in block_scores:
            self.scores[colour] = max(block_scores[colour]["group_sizes"])
        # goal scores
        for i, card in enumerate(self.score_cards):
            points = self.scoring_functions_mapping[card.card_id](
                self.graph, self.streets
            )
            self.scores[f"goal_{i+1}"] = points

        self.talk_to_observer(param="update_scores")

    def add_card_to_graph(self, card_to_play: BaseCard, position: tuple) -> None:
        card = next(c for c in self.cards_data if c["id"] == card_to_play.card_id)

        add_blocks_to_graph(self.graph, card, position)
        add_streets_to_graph(self.graph, card, position)

        self.update_scores()

    def is_placement_valid(self, grid_x: float, grid_y: float) -> bool:
        card_coords = {
            (grid_x, grid_y),
            (grid_x + 1, grid_y),
            (grid_x + 1, grid_y + 1),
            (grid_x, grid_y + 1),
        }
        occupied_coords = {
            node[0] for node in self.graph.nodes(data=True) if not node[1]["is_virtual"]
        }
        allowed_coords = set(occupied_coords)
        for x, y in occupied_coords:
            allowed_coords.add((x + 1, y))
            allowed_coords.add((x - 1, y))
            allowed_coords.add((x, y + 1))
            allowed_coords.add((x, y - 1))
        return any(coord in allowed_coords for coord in card_coords)

    scoring_functions_mapping = {
        1: sf.the_outskirts,
        2: sf.bloom_boom,
        3: sf.go_green,
        4: sf.block_party,
        5: sf.stacks_and_scrapers,
        6: sf.master_planned,
        7: sf.central_perks,
        8: sf.the_burbs,
        9: sf.concrete_jungle,
        10: sf.the_strip,
        11: sf.mini_marts,
        12: sf.superhighway,
        13: sf.park_hopping,
        14: sf.looping_lanes,
        15: sf.skid_row,
        16: sf.morning_commute,
        17: sf.tourist_trap,
        18: sf.sprawlopolis,
    }
