import networkx as nx
from utils import read_inputs


INPUT_FILE = "2022/inputs/day12.txt"


def condition(
    node1: tuple[int, int], node2: tuple[int, int], grid_input: list[list[str]]
):

    heights = dict(zip("abcdefghijklmnopqrstuvwxyz", range(26)))
    heights["S"] = heights["a"]
    heights["E"] = heights["z"]

    source_letter = grid_input[node1[0]][node1[1]]
    source_height = heights[source_letter]
    target_letter = grid_input[node2[0]][node2[1]]
    target_height = heights[target_letter]

    return target_height - source_height <= 1


def find_letter(grid_input: list[list[str]], letter: str) -> tuple[int, int]:
    for i in range(len(grid_input)):
        for j in range(len(grid_input[0])):
            if grid_input[i][j] == letter:
                return (i, j)


if __name__ == "__main__":
    # read inputs
    grid_input = read_inputs(INPUT_FILE, split=True)
    num_rows, num_cols = len(grid_input), len(grid_input[0])
    base_grid_graph = nx.grid_2d_graph(num_rows, num_cols)

    # build subgraph
    climbing_graph = nx.DiGraph()
    for node1, node2 in base_grid_graph.edges():
        if condition(node1, node2, grid_input):
            climbing_graph.add_edge(node1, node2)

        if condition(node2, node1, grid_input):
            climbing_graph.add_edge(node2, node1)

    # get start and end
    start = find_letter(grid_input, "S")
    end = find_letter(grid_input, "E")

    # Dijkstra
    shortest_length = nx.shortest_path_length(climbing_graph, source=start, target=end)

    print(shortest_length)
