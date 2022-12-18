import re
import networkx as nx
from functools import cache

INPUT_FILE = "2022/inputs/day16.txt"


def get_update(graph: nx.Graph, node: str, step: int) -> int:
    candidates = []
    # open valve option
    if node not in graph.nodes[node]["open_valves"]:
        now_open = {node}.union(graph.nodes[node]["open_valves"])
        now_total = graph.nodes[node]["flow"] * (step - 1) + graph.nodes[node]["total"]
        candidates.append({"total": now_total, "open_valves": now_open})

    # step options
    for other_node in graph.neighbors(node):
        candidates.append(
            {
                "total": graph.nodes[other_node]["total"],
                "open_valves": graph.nodes[other_node]["open_valves"],
            }
        )

    candidates = sorted(candidates, key=lambda x: x["total"])

    return candidates[0]["total"], candidates[0]["open_valves"]


def optimize_flow(graph: nx.Graph, node: str, num_steps: int) -> int:
    for step in range(1, num_steps + 1):
        for n in graph.nodes:
            total, open_valves = get_update(graph, n, step)
            graph.nodes[n]["total"] = total
            graph.nodes[n]["open_valves"] = open_valves

    return graph.nodes[node]["total"]


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
    for node in graph.nodes:
        graph.nodes[node]["flow"] = flow[node]
        graph.nodes[node]["total"] = 0
        graph.nodes[node]["open_valves"] = set()

    result = optimize_flow(graph, "AA", 30)

    print(result)
