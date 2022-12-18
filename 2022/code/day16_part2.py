import networkx as nx
import re
from itertools import chain, combinations
from functools import cache
from tqdm import tqdm


def powerset(iterable):
    "powerset([1,2,3]) --> (1,) (2,) (3,) (1,2) (1,3) (2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(1, len(s)))


@cache
def recursive_optimizer(start_node: str, other_valves: tuple[str], steps: int):
    options = [0]
    for valve in other_valves:
        path_length = lengths[start_node][valve]
        remaining_steps = steps - path_length - 1  # go to valve and open
        rest_of_valves = tuple([v for v in other_valves if v != valve])

        if remaining_steps >= 0:  # only consider if time left to release
            options.append(
                remaining_steps * flow[valve]  # release
                + recursive_optimizer(
                    valve, rest_of_valves, remaining_steps
                )  # continue
            )

    return max(options)


INPUT_FILE = "2022/inputs/day16.txt"


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

    results = []
    for subset in tqdm(powerset(valve_nodes)):
        complement = tuple([v for v in valve_nodes if v not in subset])

        results.append(
            recursive_optimizer(start_node, subset, 26)
            + recursive_optimizer(start_node, complement, 26),
        )

    print(max(results))
