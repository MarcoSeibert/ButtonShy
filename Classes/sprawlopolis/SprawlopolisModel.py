import json
import random

import networkx as nx
from collections import deque, defaultdict

from Classes.base.events import ModelEvent
from Classes.base.models import BaseModel, BaseCard
import Classes.sprawlopolis.scoring_functions as sf


def _extend_path(
    graph: nx.Graph,
    start_node: tuple,
    end_node: tuple,
    visited_edges: set,
    path: list = None,
    reverse: bool = False,
) -> list:
    if path is None:
        path = [start_node, end_node]
    visited_edges.add((start_node, end_node))
    visited_edges.add((end_node, start_node))

    current_node = end_node
    while True:
        neighbors = [
            n
            for n in graph.neighbors(current_node)
            if (current_node, n) not in visited_edges
            and (n, current_node) not in visited_edges
            and (current_node[0] == n[0] or current_node[1] == n[1])
        ]
        if len(neighbors) != 1:
            break
        next_node = neighbors[0]
        # Vermeide Loops durch virtuelle Knoten
        if next_node == start_node and len(path) > 1:
            break
        visited_edges.add((current_node, next_node))
        visited_edges.add((next_node, current_node))
        if reverse:
            path.insert(0, next_node)
        else:
            path.append(next_node)
        current_node = next_node

    return path


class SprawlopolisModel(BaseModel):
    def __init__(self, game_data: dict) -> None:
        super().__init__(game_data)
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

        with open("Resources/Assets/Sprawlopolis/cards_data.json", "r") as file:
            self.cards_data = json.load(file)["cards"]
        self.graph = nx.Graph()

        # draw three scoring card
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
        self.add_card_to_graph(card_to_play, (30, 18))

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
        self.scores["streets"] = -len(self.calculate_streets())
        self.streets = self.calculate_streets()
        block_scores = self.calculate_connected_groups()
        for color in block_scores:
            self.scores[color] = max(block_scores[color]["group_sizes"])
        # goal scores
        for i, card in enumerate(self.score_cards):
            points = self.scoring_functions_mapping[card.card_id](self.graph, self)
            self.scores[f"goal_{i+1}"] = points

        self.talk_to_observer(param="update_scores")

    def update_goal_scores(self) -> None:
        for i, card in enumerate(self.score_cards):
            points = self.scoring_functions_mapping[card.card_id](self.graph, self)
            self.scores[f"goal_{i+1}"] = points

    def add_card_to_graph(self, card_to_play: BaseCard, position: tuple) -> None:
        card = next(c for c in self.cards_data if c["id"] == card_to_play.card_id)

        # 1. Blöcke der Karte hinzufügen
        for block in card["blocks"]:
            block_coords = (
                position[0] + block["coords"][0],
                position[1] + block["coords"][1],
            )
            self.graph.add_node(
                block_coords,
                color=block["color"],
                street=block["street"],
                is_virtual=False,
            )
            # Falls der Block bereits existiert, entferne alle seine Kanten
            if self.graph.has_node(block_coords):
                edges_to_remove = list(self.graph.edges(block_coords))
                self.graph.remove_edges_from(edges_to_remove)

        # 2. Straßen als Kanten erstellen, nur bei passenden Richtungen
        for block in card["blocks"]:
            block_coords = (
                position[0] + block["coords"][0],
                position[1] + block["coords"][1],
            )
            for direction in block["street"]:
                dx, dy = self.direction_map[direction][0]
                to_coords = (block_coords[0] + dx, block_coords[1] + dy)
                # Prüfen, ob der Zielblock existiert und die komplementäre Straße hat
                if self.graph.has_node(to_coords):
                    # Immer eine Kante zu virtuellen Blöcken erstellen
                    if self.graph.nodes[to_coords].get("is_virtual", False):
                        self.graph.add_edge(block_coords, to_coords)
                    # Bei nicht-virtuellen Blöcken: Nur bei passender Straße
                    else:
                        complementary_dir = self.direction_map[direction][1]
                        if complementary_dir in self.graph.nodes[to_coords].get(
                            "street", []
                        ):
                            self.graph.add_edge(block_coords, to_coords)
                else:
                    # Virtuellen Knoten für Randstraße erstellen
                    self.graph.add_node(to_coords, is_virtual=True, color=None)
                    self.graph.add_edge(block_coords, to_coords)

        self.update_scores()
        self.update_goal_scores()

    def calculate_streets(self) -> dict:
        graph = self.graph.copy()
        streets = []
        visited_edges = set()
        visited_nodes = set()

        # 1. Straßen aus Kanten berechnen
        for u, v in graph.edges():
            if (u, v) in visited_edges or (v, u) in visited_edges:
                continue
            if not (u[0] == v[0] or u[1] == v[1]):
                continue

            path = _extend_path(graph, u, v, visited_edges)
            path = _extend_path(graph, v, u, visited_edges, path=path, reverse=True)

            non_virtual_blocks = [
                node for node in path if not graph.nodes[node].get("is_virtual", False)
            ]
            if len(non_virtual_blocks) > 0:
                streets.append(non_virtual_blocks)
                visited_nodes.update(non_virtual_blocks)

        # 2. Isolierte Blöcke (Straßen der Länge 1) hinzufügen
        for node in graph.nodes():
            if (
                not graph.nodes[node].get("is_virtual", False)
                and node not in visited_nodes
            ):
                node_streets = graph.nodes[node].get("street", [])
                if node_streets:
                    has_valid_edge = False
                    for direction in node_streets:
                        dx, dy = 0, 0
                        if direction == "N":
                            dx, dy = 0, -1
                        elif direction == "S":
                            dx, dy = 0, 1
                        elif direction == "W":
                            dx, dy = -1, 0
                        elif direction == "E":
                            dx, dy = 1, 0
                        neighbor_coords = (node[0] + dx, node[1] + dy)
                        if graph.has_edge(node, neighbor_coords):
                            has_valid_edge = True
                            break
                    if not has_valid_edge:
                        streets.append([node])

        # Straßen an virtuellen Blöcken teilen
        split_streets = []
        for street in streets:
            if len(street) > 1:
                # Prüfen, ob es sich um einen Loop handelt
                is_loop = street[0] == street[-1]
                if is_loop:
                    # Entferne den doppelten Startpunkt
                    street = street[:-1]
                    split_streets.append(street)
                    continue

                sub_streets = []
                current_sub_street = [street[0]]
                for i in range(1, len(street)):
                    prev_node = street[i - 1]
                    current_node = street[i]
                    # Prüfen, ob es einen Sprung in den Koordinaten gibt
                    dx = abs(current_node[0] - prev_node[0])
                    dy = abs(current_node[1] - prev_node[1])
                    # Teile die Straße, wenn dx + dy >= 2
                    if dx + dy >= 2:
                        sub_streets.append(current_sub_street)
                        current_sub_street = [current_node]
                    else:
                        current_sub_street.append(current_node)
                sub_streets.append(current_sub_street)
                split_streets.extend(sub_streets)
            else:
                split_streets.append(street)

        # Straßenlängen berechnen
        street_block_counts = {}
        for i, street in enumerate(split_streets):
            street_block_counts[i] = {"Length": len(street), "nodes": street}
        return street_block_counts

    def calculate_connected_groups(self) -> dict:
        # Alle Knoten nach Farbe gruppieren
        color_groups = defaultdict(list)
        for node, data in self.graph.nodes(data=True):
            if not data.get("is_virtual", False):
                color_groups[data["color"]].append(node)

        # Ergebnis: {Farbe: {"group_count": Anzahl Gruppen, "group_sizes": [Größe Gruppe 1, Größe Gruppe 2, ...]}}
        result = {}

        for color, nodes in color_groups.items():
            visited = set()
            group_sizes = []

            for node in nodes:
                if node not in visited:
                    # Neue Gruppe starten
                    queue = deque([node])
                    visited.add(node)
                    group = []

                    while queue:
                        current = queue.popleft()
                        group.append(current)

                        # Nachbarn prüfen (orthogonal: oben, unten, links, rechts)
                        x, y = current
                        neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]

                        for neighbor in neighbors:
                            if (
                                neighbor in self.graph.nodes
                                and not self.graph.nodes[neighbor].get(
                                    "is_virtual", False
                                )
                                and self.graph.nodes[neighbor]["color"] == color
                                and neighbor not in visited
                            ):
                                visited.add(neighbor)
                                queue.append(neighbor)

                    group_sizes.append(len(group))

            result[color] = {
                "group_count": len(group_sizes),
                "group_sizes": group_sizes,
            }

        return result

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

    # Mapping: Richtung → (Koordinatenänderung, komplementäre Richtung)
    direction_map = {
        "N": ((0, -1), "S"),
        "S": ((0, 1), "N"),
        "W": ((-1, 0), "E"),
        "E": ((1, 0), "W"),
    }

    scoring_functions_mapping = {
        1: sf.the_outskirts,
        4: sf.block_party,
        15: sf.skid_row,
        17: sf.tourist_trap,
        18: sf.sprawlopolis,
    }
