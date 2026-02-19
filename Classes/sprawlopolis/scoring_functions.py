from collections import defaultdict

import networkx as nx


# Card 1
def determine_point_type(graph: nx.Graph, nodes: list, index: int) -> None | str:
    direction_map = {"W": (-1, 0), "S": (0, 1), "E": (1, 0), "N": (0, -1)}
    node = nodes[index]
    x1, y1 = node
    direction = graph.nodes[node]["street"][index]
    dx, dy = direction_map[direction]
    x2, y2 = x1 + dx, y1 + dy
    if (x2, y2) in nodes:
        direction = graph.nodes[node]["street"][-1 - index]
        dx, dy = direction_map[direction]
        x2, y2 = x1 + dx, y1 + dy
    return (
        "block"
        if graph.has_node((x2, y2)) and not graph.nodes[(x2, y2)]["is_virtual"]
        else "empty"
    )


def the_outskirts(graph: nx.Graph, model: object) -> int:
    points = 0
    for i, street in model.streets.items():
        nodes = street["nodes"]
        start_point = determine_point_type(graph, nodes, 0)
        end_point = determine_point_type(graph, nodes, -1)
        if start_point == "block" and end_point == "block":
            points += 1
        else:
            points -= 1
    return points


# Card 4
def block_party(graph: nx.Graph, _) -> int:
    amount = 0
    for node in graph.nodes():
        if graph.nodes[node].get("is_virtual"):
            continue
        x, y = node
        neighbors = [(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)]
        all_neighbors_exist = True
        for neighbor in neighbors:
            if not graph.has_node(neighbor):
                all_neighbors_exist = False
                break
        if not all_neighbors_exist:
            continue
        colors = [graph.nodes[neighbor]["color"] for neighbor in neighbors]
        color = colors[0]
        if all(c == color for c in colors):
            amount += 1
    if amount > 5:
        points = 7
    else:
        points = 3 * amount - 8
    return points


# Card 15
def skid_row(graph: nx.Graph, _) -> int:
    points = 0
    for node in graph.nodes():
        grey_count = 0
        if graph.nodes[node]["is_virtual"] or graph.nodes[node]["color"] != "orange":
            continue
        else:
            x, y = node
            neighbors = [(x - 1, y), (x + 1, y), (x, y + 1), (x, y - 1)]
            for neighbor in neighbors:
                if (
                    graph.has_node(neighbor)
                    and graph.nodes[neighbor]["color"] == "grey"
                ):
                    grey_count += 1
            if grey_count >= 2:
                print(node, graph.nodes[node]["color"])
                points += 2
    return points


# Card 17
def tourist_trap(graph: nx.Graph, _) -> int:
    points = 0
    for node in graph.nodes():
        if graph.nodes[node].get("color") != "blue":
            continue
        empty_count = 0
        x, y = node
        neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        for neighbor in neighbors:
            if not graph.has_node(neighbor) or graph.nodes[neighbor]["is_virtual"]:
                empty_count += 1
        points += empty_count
    return points


# Card 18
def sprawlopolis(graph: nx.Graph, _) -> int:
    row_counts = defaultdict(int)
    column_counts = defaultdict(int)
    for node in graph.nodes():
        if graph.nodes[node].get("is_virtual"):
            continue
        x, y = node
        row_counts[y] += 1
        column_counts[x] += 1
    max_row_count = max(row_counts.values())
    max_column_count = max(column_counts.values())
    points = max_row_count + max_column_count
    return points
