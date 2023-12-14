import networkx as nx
from utils import read_inputs
from tqdm import tqdm
from math import gcd
import os


def lcm(a, b):
    return int(abs(a * b) / gcd(a, b))


INPUT_FILE = "2022/inputs/day24.txt"
CACHED_GRAPH = "2022/code/day24_maze_graph.pkl"

ARROW_TO_DELTA = {
    "^": (-1, 0),  # one row up
    "v": (1, 0),  # one row down
    ">": (0, 1),  # one col right
    "<": (0, -1),  # one col left
}


Arrows = set[tuple[tuple[int], tuple[int]]]


def parse_arrow_inputs(inputs: list[list[str]]) -> Arrows:
    arrows = set()
    for row in range(len(inputs)):
        for col in range(len(inputs[row])):
            arrow = inputs[row][col]
            if arrow in ARROW_TO_DELTA:
                delta = ARROW_TO_DELTA[arrow]
                arrows.add(((row, col), delta))
            else:
                continue

    return arrows


def move_arrows(arrows: Arrows, num_rows: int, num_cols: int) -> Arrows:
    new_arrows = set()
    for arrow in arrows:
        position, delta = arrow
        new_position = (
            (position[0] + delta[0]) % num_rows,
            (position[1] + delta[1]) % num_cols,
        )
        new_arrows.add((new_position, delta))

    return new_arrows


def build_maze(
    num_rows: int, num_cols: int, arrows: Arrows, cache: str = None
) -> nx.DiGraph:
    base_grid_graph = nx.grid_2d_graph(num_rows, num_cols)

    maze_graph = nx.DiGraph()
    least_common_mult = lcm(num_cols, num_rows)
    print(f"Grid size: {num_rows} x {num_cols} -- Time range: {least_common_mult}")

    time_range = range(least_common_mult)
    # add nodes
    for t in tqdm(time_range, desc="Nodes: "):
        maze_graph.add_nodes_from([(t, node) for node in base_grid_graph])
    # add edges across time
    for t in tqdm(time_range, desc="Edges: "):
        for node in base_grid_graph:
            # wait in-place
            maze_graph.add_edge((t, node), ((t + 1) % least_common_mult, node))
            # step to neighbour
            for other_node in nx.neighbors(base_grid_graph, node):
                maze_graph.add_edge(
                    (t, node), ((t + 1) % least_common_mult, other_node)
                )

    # add start and end node
    maze_graph.add_nodes_from([(t, "Start") for t in time_range])
    maze_graph.add_node("End")
    # add edges
    maze_graph.add_edges_from(
        [((t, "Start"), ((t + 1) % least_common_mult, (0, 0))) for t in time_range]
    )
    maze_graph.add_edges_from(
        [((t, (num_rows - 1, num_cols - 1)), "End") for t in time_range]
    )

    print("Before filtering: ", maze_graph)

    # filter for available positions
    arrows = parse_arrow_inputs(inputs)
    for t in tqdm(time_range, desc="Arrow subgraph: "):
        maze_graph.remove_nodes_from([(t, node) for node, _ in arrows])
        arrows = move_arrows(arrows, num_rows, num_cols)

    print("After filtering: ", maze_graph)

    if cache:
        nx.write_gpickle(maze_graph, cache)

    return maze_graph


if __name__ == "__main__":
    inputs = read_inputs(INPUT_FILE, split=True)
    # drop walls
    inputs = inputs[1:-1]
    inputs = [row[1:-1] for row in inputs]

    # read board size
    num_rows = len(inputs)
    num_cols = len(inputs[0])

    # setup graph
    arrows = parse_arrow_inputs(inputs)

    if os.path.exists(CACHED_GRAPH):
        print(f"-- Reading maze from {CACHED_GRAPH} --")
        maze_graph = nx.read_gpickle(CACHED_GRAPH)
    else:
        print("-- Building maze --")
        maze_graph = build_maze(num_rows, num_cols, arrows, cache=CACHED_GRAPH)

    print(maze_graph)

    print(nx.shortest_path_length(maze_graph, source=(0, "Start"), target="End"))
