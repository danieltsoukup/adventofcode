import re
import networkx as nx
from functools import cache

INPUT_FILE = "2022/inputs/day16_test.txt"


@cache
def recursive_optimizer(start_node: str, other_valves: tuple[str], steps: int):
    options = [0]
    for valve in other_valves:
        path_length = lengths[start_node][valve]
        remaining_steps = steps - path_length - 1  # extra for opening
        rest_of_valves = tuple([v for v in other_valves if v != valve])
        if remaining_steps > 0:  # only consider if time left to release
            options.append(
                remaining_steps * flow[valve]
                + recursive_optimizer(valve, rest_of_valves, remaining_steps)
            )
        else:
            options.append(0)

    return max(options)


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

    # original graph
    graph = nx.Graph()
    graph.add_nodes_from(nodes)
    graph.add_edges_from(edges)

    lengths = dict(nx.all_pairs_shortest_path_length(graph))

    start_node = "AA"
    valve_nodes = tuple([node for node in flow if flow[node] > 0])

    result = recursive_optimizer(start_node, valve_nodes, 30)
    print(result)
