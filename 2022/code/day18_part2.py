import numpy as np
import networkx as nx


INPUT_FILE = "2022/inputs/day18.txt"


if __name__ == "__main__":
    total = 0
    with open(INPUT_FILE, "r") as file:
        nodes = []
        for line in file:
            node = line.strip().split(",")
            node = tuple(int(c) for c in node)
            nodes.append(node)

    nodes_array = np.array(nodes)

    base_grid_graph = nx.grid_graph(dim=tuple(nodes_array.max(axis=0) + 1))

    droplet_graph = nx.subgraph(base_grid_graph, nodes)

    total_sides = 6 * len(nodes)
    touching_sides = 2 * len(droplet_graph.edges())
    exterior = total_sides - touching_sides

    complement_nodes = set(nx.nodes(base_grid_graph)).difference(set(nodes))
    complement_subgraph = nx.subgraph(base_grid_graph, complement_nodes)
    components = nx.connected_components(complement_subgraph)

    component_sides = [
        6 * len(comp) - 2 * len(nx.subgraph(complement_subgraph, comp).edges())
        for comp in components
    ]

    print(exterior - sum(component_sides[1:]))
