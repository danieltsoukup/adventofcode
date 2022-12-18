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


def get_updated_total(digraph: nx.DiGraph, node: str, step: int) -> int:
    candidates = []

    for other_node in digraph.neighbors(node):
        # real -> virtual
        if (digraph.nodes[node]["virtual"] is False) or (
            digraph.nodes[other_node]["virtual"] is True
        ):
            candidates.append(
                {
                    "total": digraph.nodes[node]["flow"] * step
                    + digraph.nodes[other_node]["total"],
                    "open_valves": digraph.nodes[other_node]["open_valves"].union(
                        {node}
                    ),
                }
            )
        # real -> real
        elif (digraph.nodes[node]["virtual"] is False) or (
            digraph.nodes[other_node]["virtual"] is False
        ):
            candidates.append(
                {
                    "total": digraph.nodes[node]["flow"] * step
                    + digraph.nodes[other_node]["total"],
                    "open_valves": digraph.nodes[other_node]["open_valves"],
                }
            )
        # virtual -> real
        elif (digraph.nodes[node]["virtual"] is True) or (
            digraph.nodes[other_node]["virtual"] is False
        ):
            if (
                digraph.nodes[node]["pair"]
                not in graph.nodes[other_node]["open_valves"]
            ):
                candidates.append(
                    {
                        "total": digraph.nodes[node]["flow"] * step
                        + digraph.nodes[other_node]["total"],
                        "open_valves": digraph.nodes[other_node]["open_valves"].union(
                            {node}
                        ),
                    }
                )

    candidates = sorted(candidates, key=lambda x: x["total"])

    return candidates[-1]["total"], candidates[-1]["open_valves"]


def optimize_flow(digraph: nx.DiGraph, node: str, num_steps: int) -> int:

    for step in range(1, num_steps + 1):
        new_digraph = digraph.copy()
        for n in digraph.nodes:
            (
                new_digraph.nodes[n]["total"],
                new_digraph.nodes[n]["open_valves"],
            ) = get_updated_total(digraph, n, step)

        digraph = new_digraph

    return digraph.nodes[node]["total"]


def graph_to_flow_digraph(graph: nx.Graph) -> nx.DiGraph:
    # setup digraph with flow values
    digraph = nx.DiGraph()
    digraph.add_nodes_from(graph.nodes)
    virtual_open_nodes = [node + "_open" for node in graph.nodes]
    digraph.add_nodes_from(virtual_open_nodes)

    # add backward edges too
    digraph.add_edges_from(graph.edges)
    digraph.add_edges_from([(two, one) for one, two in graph.edges])

    # open action virtual edge
    virtual_edges_to_self = zip(graph.nodes, virtual_open_nodes)
    digraph.add_edges_from(virtual_edges_to_self)

    # open state to original close neighbour
    for node, virtual in zip(graph.nodes, virtual_open_nodes):
        for neighbour in graph.neighbors(node):
            digraph.add_edge(virtual, neighbour)

    # initilize flow
    for node, virtual in zip(graph.nodes, virtual_open_nodes):
        digraph.nodes[node]["flow"] = 0
        digraph.nodes[node]["virtual"] = False
        digraph.nodes[node]["pair"] = virtual

        digraph.nodes[virtual]["flow"] = graph.nodes[node]["flow"]
        digraph.nodes[virtual]["virtual"] = True
        digraph.nodes[virtual]["pair"] = node

    # initialize total
    for node in digraph.nodes:
        digraph.nodes[node]["total"] = 0
        digraph.nodes[node]["open_valves"] = set()

    return digraph


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

    digraph = graph_to_flow_digraph(graph)
    result = optimize_flow(digraph, "AA", 30)

    print(result)
