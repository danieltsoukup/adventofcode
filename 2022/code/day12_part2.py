import networkx as nx
from utils import read_inputs
from day12_part1 import condition, find_letter

INPUT_FILE = "2022/inputs/day12.txt"

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
    shortest_lengths = nx.shortest_path_length(climbing_graph, target=end)

    best = None
    for i in range(len(grid_input)):
        for j in range(len(grid_input[0])):
            if (grid_input[i][j] in {"a", "S"}) and ((i, j) in shortest_lengths):
                if best is None or best > shortest_lengths[(i, j)]:
                    best = shortest_lengths[(i, j)]

    print(best)
