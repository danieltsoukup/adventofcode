import networkx as nx
from day24_part1 import lcm
from utils import read_inputs

INPUT_FILE = "2022/inputs/day24.txt"
CACHED_GRAPH = "2022/code/day24_maze_graph.pkl"


if __name__ == "__main__":
    inputs = read_inputs(INPUT_FILE, split=True)
    # drop walls
    inputs = inputs[1:-1]
    inputs = [row[1:-1] for row in inputs]

    # read board size
    num_rows = len(inputs)
    num_cols = len(inputs[0])
    least_common_mult = lcm(num_cols, num_rows)
    time_range = range(least_common_mult)

    print(f"-- Reading maze from {CACHED_GRAPH} --")
    start2end_maze_graph = nx.read_gpickle(CACHED_GRAPH)
    start2end_maze_graph.add_edges_from(
        [((t, "Start"), ((t + 1) % least_common_mult, "Start")) for t in time_range]
    )

    end2start_maze_graph = start2end_maze_graph.copy()
    end2start_maze_graph.remove_nodes_from(
        [node for node in start2end_maze_graph if node == "End" or node[1] == "Start"]
    )
    end2start_maze_graph.add_nodes_from([(t, "End") for t in time_range])
    end2start_maze_graph.add_node("Start")
    # add edges
    end2start_maze_graph.add_edges_from(
        [
            ((t, "End"), ((t + 1) % least_common_mult, (num_rows - 1, num_cols - 1)))
            for t in time_range
        ]
    )  # step into the board
    end2start_maze_graph.add_edges_from(
        [((t, "End"), ((t + 1) % least_common_mult, "End")) for t in time_range]
    )  # wait at end
    end2start_maze_graph.add_edges_from([((t, (0, 0)), "Start") for t in time_range])

    print(start2end_maze_graph)
    print(end2start_maze_graph)

    there = nx.shortest_path_length(
        start2end_maze_graph, source=(0, "Start"), target="End"
    )
    back = nx.shortest_path_length(
        end2start_maze_graph, source=(there % least_common_mult, "End"), target="Start"
    )
    and_there_again = nx.shortest_path_length(
        start2end_maze_graph,
        source=((there + back) % least_common_mult, "Start"),
        target="End",
    )

    print("Final: ", there + back + and_there_again)
