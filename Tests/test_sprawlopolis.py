import unittest

import networkx as nx

from Classes.sprawlopolis.functions import (
    add_blocks_to_graph,
    add_streets_to_graph,
    is_valid_loop,
    calculate_streets,
)

from Classes.sprawlopolis.scoring_functions import (
    calculate_connected_groups,
    the_outskirts,
    bloom_boom,
    go_green,
    block_party,
)


def add_card_to_graph(graph: nx.Graph, card: dict, position: tuple) -> None:
    add_blocks_to_graph(graph, card, position)
    add_streets_to_graph(graph, card, position)


class TestGraphFunctions(unittest.TestCase):
    def setUp(self) -> None:
        self.graph = nx.Graph()
        self.graph.add_node((0, 0), colour="red", is_virtual=False, street=[])
        self.graph.add_node((0, 1), colour="green", is_virtual=False, street=[])
        self.graph.add_node((1, 0), colour="blue", is_virtual=False, street=[])
        self.graph.add_node((1, 1), colour="yellow", is_virtual=False, street=[])

    def test_add_blocks_to_graph(self) -> None:
        card = {"blocks": [{"coords": [0, 0], "colour": "purple", "street": None}]}
        add_blocks_to_graph(self.graph, card, (0, 0))
        # Node is in the graph
        self.assertTrue(self.graph.has_node((0, 0)))
        # Node has new colour
        self.assertEqual(self.graph.nodes[(0, 0)]["colour"], "purple")
        # Edge got removed
        self.assertFalse(self.graph.has_edge((0, 0), (0, 1)))

    def test_add_streets_to_graph(self) -> None:
        card1 = {
            "blocks": [{"coords": [1, 0], "colour": "black", "street": ["N", "S"]}]
        }
        card2 = {
            "blocks": [{"coords": [1, 1], "colour": "indigo", "street": ["N", "W"]}]
        }
        # add the edge to a virtual block
        add_streets_to_graph(self.graph, card1, (0, 0))
        self.assertTrue(self.graph.has_edge((1, 0), (1, -1)))
        self.assertTrue(self.graph.has_node((1, -1)))
        self.assertTrue(self.graph.nodes[(1, -1)]["is_virtual"])
        # connect the two blocks with an edge, don't connect to the other side
        self.graph.nodes[(1, 0)]["street"] = card1["blocks"][0]["street"]
        self.graph.nodes[(0, 1)]["street"] = ["N", "S"]
        add_streets_to_graph(self.graph, card2, (0, 0))
        self.assertTrue(self.graph.has_edge((1, 0), (1, 1)))
        self.assertFalse(self.graph.has_edge((1, 1), (0, 1)))

    def test_is_valid_loop(self) -> None:
        nodes1 = [(0, 0), (0, 1), (1, 1), (1, 0), (0, 0)]
        nodes2 = [(0, 0), (0, 1), (1, 0), (0, 0)]
        nodes3 = [(0, 0), (0, 1), (1, 1), (1, 2), (0, 0)]
        nodes4 = [(0, 0), (0, 1), (1, 1), (1, 2)]
        nodes5 = [(0, 0), (0, 1), (0, 0)]
        nodes6 = [(0, 0), (0, 1), (0, 0), (0, 1), (0, 0)]
        # valid loop
        self.assertTrue(is_valid_loop(nodes1))
        # triangular loop => invalid
        self.assertFalse(is_valid_loop(nodes2))
        self.assertFalse(is_valid_loop(nodes3))
        # no loop
        self.assertFalse(is_valid_loop(nodes4))
        # too short, also no real loop
        self.assertFalse(is_valid_loop(nodes5))
        # no backtracking
        self.assertFalse(is_valid_loop(nodes6))

    def test_calculate_streets(self) -> None:
        streets0 = calculate_streets(self.graph)
        self.assertEqual(streets0, ({}, []))

        card1 = {
            "blocks": [
                {"coords": [0, 0], "colour": "beige", "street": ["N", "S"]},
                {"coords": [1, 0], "colour": "beige", "street": ["N", "S"]},
                {"coords": [1, 1], "colour": "beige", "street": ["N", "S"]},
                {"coords": [0, 1], "colour": "beige", "street": ["N", "S"]},
            ]
        }
        add_blocks_to_graph(self.graph, card1, (10, 10))
        add_streets_to_graph(self.graph, card1, (10, 10))
        streets1 = calculate_streets(self.graph)
        # nr of streets = 2
        self.assertEqual(len(streets1[0]), 2)
        # correct connections
        possible_streets = [[(10, 11), (10, 10)], [(11, 11), (11, 10)]]
        street_nodes1 = streets1[0][0]["nodes"]
        street_nodes2 = streets1[0][1]["nodes"]
        self.assertTrue(
            street_nodes1 == possible_streets[0] or street_nodes1 == possible_streets[1]
        )
        self.assertTrue(
            street_nodes2 == possible_streets[0] or street_nodes2 == possible_streets[1]
        )
        # no loop
        self.assertFalse(streets1[1])

        card2 = {
            "blocks": [
                {"coords": [0, 0], "colour": "beige", "street": ["N", "S"]},
                {"coords": [1, 0], "colour": "beige", "street": ["N", "S"]},
                {"coords": [1, 1], "colour": "beige", "street": ["N", "W"]},
                {"coords": [0, 1], "colour": "beige", "street": ["N", "E"]},
            ]
        }
        add_blocks_to_graph(self.graph, card2, (10, 12))
        add_streets_to_graph(self.graph, card2, (10, 12))
        streets2 = calculate_streets(self.graph)
        # nr of streets = 1
        self.assertEqual(len(streets2[0]), 1)
        # length of street = 8
        self.assertTrue(streets2[0][0]["length"], 8)
        # no loop
        self.assertFalse(streets2[1])

        card3 = {
            "blocks": [
                {"coords": [0, 0], "colour": "beige", "street": ["S", "E"]},
                {"coords": [1, 0], "colour": "beige", "street": ["S", "W"]},
                {"coords": [1, 1], "colour": "beige", "street": ["N", "S"]},
                {"coords": [0, 1], "colour": "beige", "street": ["N", "S"]},
            ]
        }
        add_blocks_to_graph(self.graph, card3, (10, 8))
        add_streets_to_graph(self.graph, card3, (10, 8))
        streets3 = calculate_streets(self.graph)
        # nr of streets = 1
        self.assertEqual(len(streets3[0]), 1)
        # length of street = 12
        self.assertTrue(streets3[0][0]["length"], 12)
        # one loop, length = 12
        self.assertEqual(streets3[1], [12])

    def test_calculate_connected_groups(self) -> None:
        expected = {
            "red": {"group_count": 1, "group_sizes": [1], "group_nodes": [[(0, 0)]]},
            "green": {"group_count": 1, "group_sizes": [1], "group_nodes": [[(0, 1)]]},
            "blue": {"group_count": 1, "group_sizes": [1], "group_nodes": [[(1, 0)]]},
            "yellow": {"group_count": 1, "group_sizes": [1], "group_nodes": [[(1, 1)]]},
        }
        self.assertEqual(expected, calculate_connected_groups(self.graph))
        self.assertFalse(calculate_connected_groups(self.graph).get("purple"))

        card1 = {
            "blocks": [
                {"coords": [0, 0], "colour": "purple", "street": []},
                {"coords": [1, 0], "colour": "purple", "street": []},
                {"coords": [1, 1], "colour": "purple", "street": []},
                {"coords": [0, 1], "colour": "purple", "street": []},
            ]
        }
        add_card_to_graph(self.graph, card1, (1, 0))
        result1 = calculate_connected_groups(self.graph)
        purple_result = result1.get("purple")
        expected_purple_result = {
            "group_count": 1,
            "group_sizes": [4],
            "group_nodes": [[(1, 0), (2, 0), (1, 1), (2, 1)]],
        }
        self.assertEqual(purple_result, expected_purple_result)

        card2 = {
            "blocks": [
                {"coords": [0, 0], "colour": "beige", "street": []},
                {"coords": [1, 0], "colour": "black", "street": []},
                {"coords": [1, 1], "colour": "beige", "street": []},
                {"coords": [0, 1], "colour": "black", "street": []},
            ]
        }

        add_card_to_graph(self.graph, card2, (1, 1))
        result2 = calculate_connected_groups(self.graph)
        purple_result = result2.get("purple")
        expected_purple_result = {
            "group_count": 1,
            "group_sizes": [2],
            "group_nodes": [[(1, 0), (2, 0)]],
        }
        self.assertEqual(purple_result, expected_purple_result)
        beige_result = result2.get("beige")
        expected_beige_result = {
            "group_count": 2,
            "group_sizes": [1, 1],
            "group_nodes": [[(1, 1)], [(2, 2)]],
        }
        self.assertEqual(beige_result, expected_beige_result)


class TestScoringFunctions(unittest.TestCase):
    def setUp(self) -> None:
        self.graph = nx.Graph()
        self.streets = calculate_streets(self.graph)

    def test_the_outskirts(self) -> None:
        self.assertFalse(the_outskirts(self.graph, self.streets))
        # Example from card
        card = {
            "blocks": [
                {"coords": [0, 0], "colour": "beige", "street": ["N", "W"]},
                {"coords": [1, 0], "colour": "beige", "street": []},
                {"coords": [2, 0], "colour": "beige", "street": ["W", "E"]},
                {"coords": [3, 0], "colour": "beige", "street": ["W", "S"]},
                {"coords": [0, 1], "colour": "beige", "street": ["W", "E"]},
                {"coords": [1, 1], "colour": "beige", "street": ["W", "E"]},
                {"coords": [2, 1], "colour": "beige", "street": []},
                {"coords": [3, 1], "colour": "beige", "street": ["N", "S"]},
                {"coords": [0, 2], "colour": "beige", "street": ["N", "S"]},
                {"coords": [1, 2], "colour": "beige", "street": []},
                {"coords": [2, 2], "colour": "beige", "street": ["N", "W"]},
                {"coords": [3, 2], "colour": "beige", "street": []},
                {"coords": [0, 3], "colour": "beige", "street": ["N", "E"]},
                {"coords": [1, 3], "colour": "beige", "street": ["W", "E"]},
                {"coords": [2, 3], "colour": "beige", "street": ["W", "E"]},
                {"coords": [3, 3], "colour": "beige", "street": ["W", "S"]},
            ]
        }
        add_card_to_graph(self.graph, card, (0, 0))
        self.streets = calculate_streets(self.graph)
        points = the_outskirts(self.graph, self.streets)
        self.assertEqual(points, -1)

        # loop
        self.graph = nx.Graph()
        card = {
            "blocks": [
                {"coords": [0, 0], "colour": "beige", "street": ["S", "E"]},
                {"coords": [1, 0], "colour": "beige", "street": ["S", "W"]},
                {"coords": [1, 1], "colour": "beige", "street": ["N", "W"]},
                {"coords": [0, 1], "colour": "beige", "street": ["N", "E"]},
            ]
        }
        add_card_to_graph(self.graph, card, (0, 0))
        self.streets = calculate_streets(self.graph)
        points = the_outskirts(self.graph, self.streets)
        self.assertEqual(points, 1)

    def test_bloom_boom(self) -> None:
        self.assertFalse(bloom_boom(self.graph, None))
        # Example from card
        card = {
            "blocks": [
                {"coords": [1, 0], "colour": "green", "street": []},
                {"coords": [2, 0], "colour": "beige", "street": []},
                {"coords": [3, 0], "colour": "beige", "street": []},
                {"coords": [0, 1], "colour": "green", "street": []},
                {"coords": [1, 1], "colour": "green", "street": []},
                {"coords": [2, 1], "colour": "beige", "street": []},
                {"coords": [3, 1], "colour": "green", "street": []},
                {"coords": [0, 2], "colour": "beige", "street": []},
                {"coords": [1, 2], "colour": "beige", "street": []},
                {"coords": [2, 2], "colour": "beige", "street": []},
                {"coords": [3, 2], "colour": "green", "street": []},
                {"coords": [0, 3], "colour": "green", "street": []},
                {"coords": [1, 3], "colour": "green", "street": []},
                {"coords": [2, 3], "colour": "beige", "street": []},
                {"coords": [3, 3], "colour": "green", "street": []},
                {"coords": [1, 4], "colour": "beige", "street": []},
                {"coords": [2, 4], "colour": "beige", "street": []},
                {"coords": [3, 4], "colour": "beige", "street": []},
                {"coords": [1, 5], "colour": "green", "street": []},
                {"coords": [2, 5], "colour": "beige", "street": []},
            ]
        }
        add_card_to_graph(self.graph, card, (0, 0))
        points = bloom_boom(self.graph, None)
        self.assertEqual(points, 1)

        # no green at all
        self.graph = nx.Graph()
        card = {
            "blocks": [
                {"coords": [0, 0], "colour": "beige", "street": []},
                {"coords": [1, 0], "colour": "beige", "street": []},
                {"coords": [1, 1], "colour": "beige", "street": []},
                {"coords": [0, 1], "colour": "beige", "street": []},
            ]
        }
        add_card_to_graph(self.graph, card, (0, 0))
        points = bloom_boom(self.graph, None)
        self.assertEqual(points, -4)

        # all green
        card = {
            "blocks": [
                {"coords": [0, 0], "colour": "green", "street": []},
                {"coords": [1, 0], "colour": "green", "street": []},
                {"coords": [1, 1], "colour": "green", "street": []},
                {"coords": [0, 1], "colour": "green", "street": []},
            ]
        }
        add_card_to_graph(self.graph, card, (0, 0))
        points = bloom_boom(self.graph, None)
        self.assertEqual(points, 0)

        # all 3 green
        card = {
            "blocks": [
                {"coords": [2, 0], "colour": "green", "street": []},
                {"coords": [2, 1], "colour": "green", "street": []},
                {"coords": [2, 2], "colour": "green", "street": []},
                {"coords": [1, 2], "colour": "green", "street": []},
                {"coords": [0, 2], "colour": "green", "street": []},
            ]
        }
        add_card_to_graph(self.graph, card, (0, 0))
        points = bloom_boom(self.graph, None)
        self.assertEqual(points, 6)

    def test_go_green(self) -> None:
        self.assertFalse(go_green(self.graph, None))

        card = {"blocks": [{"coords": [0, 0], "colour": "green", "street": []}]}
        add_blocks_to_graph(self.graph, card, (0, 0))
        points = go_green(self.graph, None)
        self.assertEqual(points, 1)

        card = {"blocks": [{"coords": [0, 0], "colour": "grey", "street": []}]}
        add_blocks_to_graph(self.graph, card, (1, 0))
        points = go_green(self.graph, None)
        self.assertEqual(points, -2)

    def test_block_party(self) -> None:
        self.assertEqual(block_party(self.graph, None), -8)

        card = {
            "blocks": [
                {"coords": [0, 0], "colour": "black", "street": []},
                {"coords": [1, 0], "colour": "black", "street": []},
                {"coords": [1, 1], "colour": "black", "street": []},
                {"coords": [0, 1], "colour": "black", "street": []},
            ]
        }
        add_blocks_to_graph(self.graph, card, (0, 0))
        self.assertEqual(block_party(self.graph, None), -5)

        card = {
            "blocks": [
                {"coords": [0, 0], "colour": "green", "street": []},
                {"coords": [1, 0], "colour": "green", "street": []},
                {"coords": [1, 1], "colour": "green", "street": []},
                {"coords": [0, 1], "colour": "green", "street": []},
            ]
        }
        add_blocks_to_graph(self.graph, card, (2, 0))
        self.assertEqual(block_party(self.graph, None), -2)

        add_blocks_to_graph(self.graph, card, (4, 0))
        self.assertEqual(block_party(self.graph, None), 4)

        add_blocks_to_graph(self.graph, card, (5, 0))
        self.assertEqual(block_party(self.graph, None), 7)

        add_blocks_to_graph(self.graph, card, (7, 0))
        self.assertEqual(block_party(self.graph, None), 7)

        card = {
            "blocks": [
                {"coords": [0, 0], "colour": "blue", "street": []},
                {"coords": [1, 0], "colour": "blue", "street": []},
                {"coords": [2, 0], "colour": "blue", "street": []},
                {"coords": [3, 0], "colour": "blue", "street": []},
                {"coords": [4, 0], "colour": "blue", "street": []},
                {"coords": [5, 0], "colour": "blue", "street": []},
                {"coords": [6, 0], "colour": "blue", "street": []},
                {"coords": [7, 0], "colour": "blue", "street": []},
                {"coords": [8, 0], "colour": "blue", "street": []},
            ]
        }
        add_blocks_to_graph(self.graph, card, (0, 0))
        self.assertEqual(block_party(self.graph, None), -8)


if __name__ == "__main__":
    unittest.main()

# card = {"blocks": [{"coords": [0, 0], "colour": "black", "street": []}]}
# self.assertFalse(go_green(self.graph, self.streets))
