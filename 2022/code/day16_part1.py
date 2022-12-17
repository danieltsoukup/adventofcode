import re
import networkx as nx
from functools import cache

INPUT_FILE = "2022/inputs/day16.txt"


@cache
def dummy_flow_optimizer(
    graph: nx.Graph,  # graph with flow attribute set on the nodes
    position: str,  # current positions
    total: int,  # current total
    steps_left: int,
):
    """
    Dummy recursive call - way too slow.
    """
    if steps_left == 0:
        return total
    else:
        # move
        move_max = []
        for neighbour in graph.neighbors(position):
            move_max.append(
                dummy_flow_optimizer(graph, neighbour, total, steps_left - 1)
            )
        move_max = max(move_max)

        # stay & open if needed
        new_total = total + sum(
            graph.nodes[node]["flow"]
            for node in graph.nodes
            if graph.nodes[node]["open"]
        )
        new_graph = graph.copy()
        new_graph.nodes[position]["open"] = True
        stay_max = dummy_flow_optimizer(new_graph, position, new_total, steps_left - 1)

        return max(stay_max, move_max)


if __name__ == "__main__":
    nodes, edges = set(), set()
    flow = dict()
    with open(INPUT_FILE, "r") as file:
        for line in file:
            line = line.strip()
            all_valves = re.findall(r"([A-Z]+)\b", line)
            valve, tunnels_to = all_valves[0], all_valves[1:]
            flow[valve] = int(re.findall(r"rate=(\d+)", line)[0])

            nodes.add(valve)
            edges = edges.union(set((valve, next_) for next_ in tunnels_to))

    # setup graph with flow values
    graph = nx.Graph()
    graph.add_nodes_from(nodes)
    graph.add_edges_from(edges)
    for node in graph.nodes:
        graph.nodes[node]["flow"] = flow[node]
        graph.nodes[node]["open"] = False

    print(dummy_flow_optimizer(graph, "AA", 0, 30))
