from collections import Counter

import networkx as nx

direction_map = {
    "N": ((0, -1), "S"),
    "S": ((0, 1), "N"),
    "W": ((-1, 0), "E"),
    "E": ((1, 0), "W"),
}


def extend_path(
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


def add_blocks_to_graph(graph: nx.Graph, card: dict, position: tuple) -> None:
    for block in card["blocks"]:
        block_coords = (
            position[0] + block["coords"][0],
            position[1] + block["coords"][1],
        )
        graph.add_node(
            block_coords,
            colour=block["colour"],
            street=block["street"],
            is_virtual=False,
        )
        if graph.has_node(block_coords):
            edges_to_remove = list(graph.edges(block_coords))
            graph.remove_edges_from(edges_to_remove)


def add_streets_to_graph(graph: nx.Graph, card: dict, position: tuple) -> None:
    for block in card["blocks"]:
        block_coords = (
            position[0] + block["coords"][0],
            position[1] + block["coords"][1],
        )
        for direction in block["street"]:
            dx, dy = direction_map[direction][0]
            to_coords = (block_coords[0] + dx, block_coords[1] + dy)
            if not graph.has_node(to_coords):
                graph.add_node(to_coords, is_virtual=True, colour=None)
                graph.add_edge(block_coords, to_coords)
            elif graph.nodes[to_coords].get("is_virtual", False):
                graph.add_edge(block_coords, to_coords)
            else:
                complementary_dir = direction_map[direction][1]
                if complementary_dir in graph.nodes[to_coords].get("street", []):
                    graph.add_edge(block_coords, to_coords)


def is_valid_loop(nodes: list) -> bool:
    if len(nodes) < 4:
        return False

    # no backtracking
    if nodes[0] != nodes[-1] or nodes.count(nodes[0]) != 2:
        return False
    middle_elements = nodes[1:-1]
    element_counts = Counter(middle_elements)
    for count in element_counts.values():
        if count > 1:
            return False

    for i in range(len(nodes) - 1):
        x1, y1 = nodes[i]
        x2, y2 = nodes[i + 1]
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        if dx + dy != 1:
            return False
    return True


def calculate_streets_from_edges(
    graph: nx.Graph, streets: list, visited_nodes: set
) -> tuple:
    visited_edges = set()
    for u, v in graph.edges():
        if (u, v) in visited_edges or (v, u) in visited_edges:
            continue
        if not (u[0] == v[0] or u[1] == v[1]):
            continue

        path = extend_path(graph, u, v, visited_edges)
        path = extend_path(graph, v, u, visited_edges, path=path, reverse=True)

        non_virtual_blocks = [
            node for node in path if not graph.nodes[node].get("is_virtual", False)
        ]
        if len(non_virtual_blocks) > 0:
            streets.append(non_virtual_blocks)
            visited_nodes.update(non_virtual_blocks)
    return streets, visited_nodes


def has_valid_edge(graph: nx.Graph, node: tuple) -> bool:
    _direction_map = {"N": (0, -1), "S": (0, 1), "W": (-1, 0), "E": (1, 0)}
    node_streets = graph.nodes[node].get("street", [])
    for direction in node_streets:
        dx, dy = _direction_map.get(direction, (0, 0))
        neighbor_coords = (node[0] + dx, node[1] + dy)
        if graph.has_edge(node, neighbor_coords):
            return True
    return False


def find_isolated_streets(graph: nx.Graph, streets: list, visited_nodes: set) -> list:
    for node in graph.nodes():
        if not graph.nodes[node].get("is_virtual", False) and node not in visited_nodes:
            node_streets = graph.nodes[node].get("street", [])
            if node_streets and not has_valid_edge(graph, node):
                streets.append([node])
    return streets


def has_loop(street: list, loops: list, split_streets: list) -> tuple | None:
    is_loop = street[0] == street[-1]
    if is_loop:
        if is_valid_loop(street):
            loops.append(len(street) - 1)
        # Entferne den doppelten Startpunkt
        street = street[:-1]
        split_streets.append(street)
        return loops, split_streets
    return None


def split_streets_at_virtual_blocks(streets: list) -> tuple:
    split_streets = []
    loops = []
    for street in streets:
        if len(street) > 1:
            is_looping = has_loop(street, loops, split_streets)
            if is_looping:
                loops, split_streets = is_looping
                continue
            sub_streets = []
            current_sub_street = [street[0]]
            for i in range(1, len(street)):
                prev_node = street[i - 1]
                current_node = street[i]
                dx = abs(current_node[0] - prev_node[0])
                dy = abs(current_node[1] - prev_node[1])
                if dx + dy >= 2:
                    sub_streets.append(current_sub_street)
                    current_sub_street = [current_node]
                else:
                    current_sub_street.append(current_node)
            sub_streets.append(current_sub_street)
            split_streets.extend(sub_streets)
        else:
            split_streets.append(street)
    return split_streets, loops


def calculate_streets(graph_in: nx.Graph) -> tuple[dict, list]:
    graph = graph_in.copy()
    streets = []
    visited_nodes = set()

    streets, visited_nodes = calculate_streets_from_edges(graph, streets, visited_nodes)
    streets = find_isolated_streets(graph, streets, visited_nodes)
    split_streets, loops = split_streets_at_virtual_blocks(streets)

    street_block_counts = {}
    for i, street in enumerate(split_streets):
        street_block_counts[i] = {"length": len(street), "nodes": street}
    return street_block_counts, loops
