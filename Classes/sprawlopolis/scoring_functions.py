from collections import defaultdict, deque

import networkx as nx


def calculate_connected_groups(graph: nx.Graph) -> dict:
    # Alle Knoten nach Farbe gruppieren
    color_groups = defaultdict(list)
    for node, data in graph.nodes(data=True):
        if not data.get("is_virtual", False):
            color_groups[data["color"]].append(node)

    result = {}

    for color, nodes in color_groups.items():
        visited = set()
        group_sizes = []
        group_nodes = []

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
                            neighbor in graph.nodes
                            and not graph.nodes[neighbor].get("is_virtual", False)
                            and graph.nodes[neighbor]["color"] == color
                            and neighbor not in visited
                        ):
                            visited.add(neighbor)
                            queue.append(neighbor)

                group_sizes.append(len(group))
                group_nodes.append(group)

        result[color] = {
            "group_count": len(group_sizes),
            "group_sizes": group_sizes,
            "group_nodes": group_nodes,
        }
    return result


def determine_end_type(graph: nx.Graph, nodes: list, index: int) -> None | str:
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
        (x2, y2)
        if graph.has_node((x2, y2)) and not graph.nodes[(x2, y2)]["is_virtual"]
        else "empty"
    )


# Card 1
def the_outskirts(graph: nx.Graph, streets: tuple) -> int:
    points = 0
    for i, street in streets[0].items():
        nodes = street["nodes"]
        start_point = determine_end_type(graph, nodes, 0)
        end_point = determine_end_type(graph, nodes, -1)
        if start_point != "empty" and end_point != "empty":
            print("+1")
            points += 1
        else:
            points -= 1
    return points


# Card 2
def bloom_boom(graph: nx.Graph, _) -> int:
    row_dict = defaultdict(int)
    col_dict = defaultdict(int)
    for node in graph.nodes():
        if graph.nodes[node]["is_virtual"]:
            continue
        x, y = node
        row_dict[y] += 0
        col_dict[x] += 0
        if graph.nodes[node]["color"] != "green":
            continue
        row_dict[y] += 1
        col_dict[x] += 1
    count_3_rows = sum(1 for value in row_dict.values() if value == 3)
    count_3_columns = sum(1 for value in col_dict.values() if value == 3)
    count_0_rows = sum(1 for value in row_dict.values() if value == 0)
    count_0_columns = sum(1 for value in col_dict.values() if value == 0)
    points = count_3_rows + count_3_columns - count_0_rows - count_0_columns
    return points


# Card 3
def go_green(graph: nx.Graph, _) -> int:
    points = 0
    for node in graph.nodes:
        if graph.nodes[node]["color"] == "green":
            points += 1
        elif graph.nodes[node]["color"] == "grey":
            points -= 3
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


# Card 5
def stacks_and_scrapers(graph: nx.Graph, _) -> int:
    points = 0
    for node in graph.nodes():
        if graph.nodes[node]["is_virtual"] or graph.nodes[node]["color"] != "grey":
            continue
        x, y = node
        neighbors = [(x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)]
        for neighbor in neighbors:
            if graph.has_node(neighbor) and graph.nodes[neighbor]["color"] not in [
                "blue",
                "grey",
            ]:
                break
        else:
            points += 2
    return points


# Card 6
def master_planned(graph: nx.Graph, _) -> int:
    groups = calculate_connected_groups(graph)
    orange_score = max(groups["orange"]["group_sizes"])
    grey_score = max(groups["grey"]["group_sizes"])
    return orange_score - grey_score


# Card 7
def central_perks(graph: nx.Graph, _) -> int:
    points = 0
    for node in graph.nodes:
        if graph.nodes[node]["is_virtual"] or graph.nodes[node]["color"] != "green":
            continue
        x, y = node
        neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        for neighbor in neighbors:
            if not graph.has_node(neighbor) or graph.nodes[neighbor]["is_virtual"]:
                points -= 2
                break
        else:
            points += 1
    return points


# Card 8
def the_burbs(graph: nx.Graph, _) -> int:
    points = []
    orange_nodes = calculate_connected_groups(graph)["orange"]["group_nodes"]
    max_size = len(max(orange_nodes, key=len))
    biggest_groups = [group for group in orange_nodes if len(group) == max_size]
    for group in biggest_groups:
        points_for_this_group = 0
        visited_neighbors = []
        for node in group:
            x, y = node
            neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
            for neighbor in neighbors:
                if neighbor not in visited_neighbors and graph.has_node(neighbor):
                    visited_neighbors.append(neighbor)
                    if graph.nodes[neighbor]["color"] == "green":
                        points_for_this_group += 1
                    elif graph.nodes[neighbor]["color"] == "grey":
                        points_for_this_group -= 2
        points.append(points_for_this_group)
    return max(points)


# Card 9
def concrete_jungle(graph: nx.Graph, _) -> int:
    points = 0
    for node in graph.nodes():
        if graph.nodes[node]["is_virtual"] or graph.nodes[node]["color"] != "grey":
            continue
        x, y = node
        diag_neighbors = [
            (x + 1, y + 1),
            (x + 1, y - 1),
            (x - 1, y - 1),
            (x - 1, y + 1),
        ]
        for neighbor in diag_neighbors:
            if graph.has_node(neighbor) and graph.nodes[neighbor]["color"] == "grey":
                points += 1
                break
    return points


# Card 10
def the_strip(graph: nx.Graph, _) -> int:
    row_dict = defaultdict(int)
    col_dict = defaultdict(int)
    for node in graph.nodes():
        if graph.nodes[node]["is_virtual"]:
            continue
        x, y = node
        row_dict[y] += 0
        col_dict[x] += 0
        if graph.nodes[node]["color"] != "blue":
            continue
        row_dict[y] += 1
        col_dict[x] += 1
    points = max(list(row_dict.values()) + list(col_dict.values()))
    return points


# Card 11
def mini_marts(graph: nx.Graph, streets: tuple) -> int:
    # todo Test for loops in the streets
    points = 0
    for street in streets[0]:
        if streets[0][street]["Length"] < 3:
            continue
        nodes = streets[0][street]["nodes"]
        for i in range(len(nodes) - 2):
            current_node = nodes[i]
            next_node = nodes[i + 1]
            next_next_node = nodes[i + 2]
            if (
                graph.nodes[current_node]["color"] == "orange"
                and graph.nodes[next_node]["color"] == "blue"
                and graph.nodes[next_next_node]["color"] == "orange"
            ):
                points += 2
    return points


# Card 12
def superhighway(_, streets: tuple) -> int:
    longest_road = max([streets[0][street]["Length"] for street in streets[0]])
    return int(longest_road / 2)


# Card 13
def park_hopping(graph: nx.Graph, streets: tuple) -> int:
    points = 0

    for i, street in streets[0].items():
        nodes = street["nodes"]
        start_point = determine_end_type(graph, nodes, 0)
        end_point = determine_end_type(graph, nodes, -1)
        if (
            start_point != end_point
            and start_point != "empty"
            and end_point != "empty"
            and graph.nodes[start_point]["color"] == "green"
            and graph.nodes[end_point]["color"] == "green"
        ):
            points += 3
    return points


# Card 14
def looping_lanes(_, streets: tuple) -> int:
    return sum(streets[1])


# Card 15
def skid_row(graph: nx.Graph, _) -> int:
    points = 0
    for node in graph.nodes():
        grey_count = 0
        if graph.nodes[node]["is_virtual"] or graph.nodes[node]["color"] != "orange":
            continue
        x, y = node
        neighbors = [(x - 1, y), (x + 1, y), (x, y + 1), (x, y - 1)]
        for neighbor in neighbors:
            if graph.has_node(neighbor) and graph.nodes[neighbor]["color"] == "grey":
                grey_count += 1
        if grey_count >= 2:
            points += 2
    return points


# Card 16
def morning_commute(graph: nx.Graph, streets: tuple) -> int:
    points = 0
    for street in streets[0]:
        street_has_orange = False
        street_has_blue = False
        nodes = streets[0][street]["nodes"]
        for node in nodes:
            if graph.has_node(node) and graph.nodes[node]["color"] == "orange":
                street_has_orange = True
            elif graph.has_node(node) and graph.nodes[node]["color"] == "blue":
                street_has_blue = True
        if street_has_orange and street_has_blue:
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
