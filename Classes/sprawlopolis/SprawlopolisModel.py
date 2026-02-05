import json
import random

import networkx as nx
from PIL.ImageTk import PhotoImage

from Classes.base.events import ModelEvent
from Classes.base.models import BaseModel, BaseCard


class SprawlopolisModel(BaseModel):
    def __init__(self, game_data: dict) -> None:
        super().__init__(game_data)
        self.score_cards = []
        self.hand_cards = []

        with open("Resources/Assets/Sprawlopolis/cards_data.json", "r") as file:
            self.cards_data = json.load(file)["cards"]
        self.graph = nx.Graph()

        # draw three scoring card
        for _ in range(3):
            given_card = random.choice(self.cards)
            self.cards.remove(given_card)
            self.score_cards.append(given_card)

        # draw three initial hand cards
        for _ in range(3):
            given_card = random.choice(self.cards)
            self.cards.remove(given_card)
            self.hand_cards.append(given_card)

    def play_first_card(self) -> None:
        card_to_play = self.cards[0]
        self.cards.remove(card_to_play)
        self.play_card_to_observer(card_to_play, first_card=True)
        self.add_card_to_graph(card_to_play, (30, 18))

    def play_card_to_observer(
        self, card: SprawlopolisCard, first_card: bool = False
    ) -> None:
        if not first_card:
            event = ModelEvent("CARD_PLAYED", {"card": card})
        else:
            event = ModelEvent("FIRST_CARD_PLAYED", {"card": card})
        self.notify_observers(event)  # Benachrichtige alle Observer

    def add_card_to_graph(
        self, card_to_play: SprawlopolisCard, position: tuple
    ) -> None:
        card = next(
            c for c in self.cards_data if c["id"] == card_to_play.card_id
        )  # card_to_play.card_id)
        for block in card["blocks"]:
            block_coords = (
                position[0] + block["coords"][0],
                position[1] + block["coords"][1],
            )
            self.graph.add_node(block_coords, color=block["color"], is_border=False)

        for street in card["streets"]:
            from_coords = (
                position[0] + street["from"][0],
                position[1] + street["from"][1],
            )
            to_coords = (position[0] + street["to"][0], position[1] + street["to"][1])
            self.graph.add_edge(from_coords, to_coords, is_border=False)

        for border_street in card["border_streets"]:
            from_coords = (
                position[0] + border_street["from"][0],
                position[1] + border_street["from"][1],
            )
            match border_street["to"]:
                case "top":
                    direction = (0, -1)
                case "bottom":
                    direction = (0, 1)
                case "left":
                    direction = (-1, 0)
                case "right":
                    direction = (1, 0)
                case _:
                    direction = (0, 0)
            to_coords = tuple(x + y for x, y in zip(from_coords, direction))
            # print(from_coords, to_coords)
            self.graph.add_node(to_coords, color=None, is_border=True)
            self.graph.add_edge(from_coords, to_coords, is_border=True)
        #
        # G = self.graph
        #
        # # Line-Graph erstellen
        # line_graph = nx.line_graph(G)
        #
        # # Attribute der Kanten aus G in die Knoten des line_graph übertragen
        # for u, v, data in G.edges(data=True):
        #     if (u, v) in line_graph.nodes():
        #         line_graph.nodes[(u, v)].update(data)
        #     if (v, u) in line_graph.nodes():
        #         line_graph.nodes[(v, u)].update(data)
        #
        # # Zusammenhängende Komponenten (Straßen) identifizieren
        # straßen = list(nx.connected_components(line_graph))
        #
        # # Länge jeder Straße als Anzahl der einzigartigen nicht-Randknoten berechnen
        # for i, straße in enumerate(straßen, 1):
        #     # Alle Knoten der Kanten in dieser Straße sammeln
        #     unique_nodes = set()
        #     for edge in straße:
        #         u, v = edge
        #         # Nur Knoten hinzufügen, die keine Randknoten sind
        #         if not G.nodes[u].get("is_border", False):
        #             unique_nodes.add(u)
        #         if not G.nodes[v].get("is_border", False):
        #             unique_nodes.add(v)
        #     print(f"Straße {i}: Länge = {len(unique_nodes)} Blöcke")
        #
        # # Anzahl der Straßen
        # anzahl_straßen = len(straßen)
        # print(f"\nAnzahl der Straßen: {anzahl_straßen}")

        # print(nodes_to_remove)
        # line_graph.remove_nodes_from(nodes_to_remove)

        # straßen = list(nx.connected_components(line_graph))
        # for i, straße in enumerate(straßen, 1):
        #     print(f"Straße {i}: Länge = {len(straße)} Kanten")
        #     print(i, straße)
        # anzahl_straßen = len(straßen)
        # print(f"\nAnzahl der Straßen: {anzahl_straßen}")

        # Optional: Gesamtanzahl der Straßen
        # anzahl_straßen = len(straßen)
        # print(f"\nAnzahl der Straßen: {anzahl_straßen}")
        #
        # connected_gray_zones = find_connected_gray_zones(self.graph)
        # for i, zone in enumerate(connected_gray_zones, 1):
        #     print(f"Graue Zone {i}: {len(zone)} Blöcke ({len(zone)} Punkte)")


class SprawlopolisCard(BaseCard):
    def __init__(self, card_id: int, side: str, image: PhotoImage) -> None:
        super().__init__(card_id, side, image)
        self.points = card_id
        self.blocks = None


from collections import deque


def find_connected_gray_zones(graph: nx.Graph) -> list:
    # Alle grauen Blöcke finden (ohne Blockade-Prüfung)
    gray_nodes = [
        n for n, attr in graph.nodes(data=True) if attr.get("color") == "grey"
    ]

    visited = set()
    zones = []

    for node in gray_nodes:
        if node not in visited:
            # Neue Zone starten
            queue = deque([node])
            visited.add(node)
            zone = []

            while queue:
                current = queue.popleft()
                zone.append(current)

                # Nachbarn im Koordinatensystem prüfen
                for neighbor in get_neighbors(current):
                    if (
                        neighbor in graph.nodes
                        and graph.nodes[neighbor].get("color") == "grey"
                        and neighbor not in visited
                    ):
                        visited.add(neighbor)
                        queue.append(neighbor)

            zones.append(zone)

    return zones


def get_neighbors(coords: tuple) -> list:
    x, y = coords
    return [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
