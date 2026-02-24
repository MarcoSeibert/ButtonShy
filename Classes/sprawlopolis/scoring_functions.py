from collections import deque, defaultdict

import networkx as nx


def bfs_group(graph: nx.Graph, start_node: list, colour: str, visited: set) -> list:
    queue = deque([start_node])
    visited.add(start_node)
    group = []
    while queue:
        current = queue.popleft()
        group.append(current)
        x, y = current
        neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        for neighbor in neighbors:
            if (
                neighbor in graph.nodes
                and not graph.nodes[neighbor].get("is_virtual", False)
                and graph.nodes[neighbor]["colour"] == colour
                and neighbor not in visited
            ):
                visited.add(neighbor)
                queue.append(neighbor)
    return group


def calculate_connected_groups(graph: nx.Graph) -> dict:
    # Alle Knoten nach Farbe gruppieren
    colour_groups = defaultdict(list)
    for node, data in graph.nodes(data=True):
        if not data.get("is_virtual", False):
            colour_groups[data["colour"]].append(node)

    result = {}

    for colour, nodes in colour_groups.items():
        visited = set()
        group_sizes = []
        group_nodes = []
        for node in nodes:
            if node not in visited:
                group = bfs_group(graph, node, colour, visited)
                group_sizes.append(len(group))
                group_nodes.append(group)
        result[colour] = {
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
        if graph.nodes[node]["colour"] != "green":
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
        if graph.nodes[node]["colour"] == "green":
            points += 1
        elif graph.nodes[node]["colour"] == "grey":
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
        colours = [graph.nodes[neighbor]["colour"] for neighbor in neighbors]
        colour = colours[0]
        if all(c == colour for c in colours):
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
        if graph.nodes[node]["is_virtual"] or graph.nodes[node]["colour"] != "grey":
            continue
        x, y = node
        neighbors = [(x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)]
        for neighbor in neighbors:
            if graph.has_node(neighbor) and graph.nodes[neighbor]["colour"] not in [
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
        if graph.nodes[node]["is_virtual"] or graph.nodes[node]["colour"] != "green":
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
            points_for_this_group, visited_neighbors = calculate_points_for_group(
                graph, node, points_for_this_group, visited_neighbors
            )
        points.append(points_for_this_group)
    return max(points)


def calculate_points_for_group(
    graph: nx.Graph, node: list, points_for_this_group: int, visited_neighbors: list
) -> tuple:
    x, y = node
    neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    for neighbor in neighbors:
        if neighbor not in visited_neighbors and graph.has_node(neighbor):
            visited_neighbors.append(neighbor)
            if graph.nodes[neighbor]["colour"] == "green":
                points_for_this_group += 1
            elif graph.nodes[neighbor]["colour"] == "grey":
                points_for_this_group -= 2
    return points_for_this_group, visited_neighbors


# Card 9
def concrete_jungle(graph: nx.Graph, _) -> int:
    points = 0
    for node in graph.nodes():
        if graph.nodes[node]["is_virtual"] or graph.nodes[node]["colour"] != "grey":
            continue
        x, y = node
        diagonal_neighbors = [
            (x + 1, y + 1),
            (x + 1, y - 1),
            (x - 1, y - 1),
            (x - 1, y + 1),
        ]
        for neighbor in diagonal_neighbors:
            if graph.has_node(neighbor) and graph.nodes[neighbor]["colour"] == "grey":
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
        if graph.nodes[node]["colour"] != "blue":
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
        if streets[0][street]["length"] < 3:
            continue
        nodes = streets[0][street]["nodes"]
        for i in range(len(nodes) - 2):
            current_node = nodes[i]
            next_node = nodes[i + 1]
            next_next_node = nodes[i + 2]
            if (
                graph.nodes[current_node]["colour"] == "orange"
                and graph.nodes[next_node]["colour"] == "blue"
                and graph.nodes[next_next_node]["colour"] == "orange"
            ):
                points += 2
    return points


# Card 12
def superhighway(_, streets: tuple) -> int:
    longest_road = max([streets[0][street]["length"] for street in streets[0]])
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
            and graph.nodes[start_point]["colour"] == "green"
            and graph.nodes[end_point]["colour"] == "green"
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
        if graph.nodes[node]["is_virtual"] or graph.nodes[node]["colour"] != "orange":
            continue
        x, y = node
        neighbors = [(x - 1, y), (x + 1, y), (x, y + 1), (x, y - 1)]
        for neighbor in neighbors:
            if graph.has_node(neighbor) and graph.nodes[neighbor]["colour"] == "grey":
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
            if graph.has_node(node) and graph.nodes[node]["colour"] == "orange":
                street_has_orange = True
            elif graph.has_node(node) and graph.nodes[node]["colour"] == "blue":
                street_has_blue = True
        if street_has_orange and street_has_blue:
            points += 2
    return points


# Card 17
def tourist_trap(graph: nx.Graph, _) -> int:
    points = 0
    for node in graph.nodes():
        if graph.nodes[node].get("colour") != "blue":
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
