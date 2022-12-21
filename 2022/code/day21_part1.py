import re
import networkx as nx

INPUT_FILE = "2022/inputs/day21.txt"


def node_from_string(line: str) -> dict[str]:
    node_name, definition = line.split(":")

    node = dict()
    node["name"] = node_name

    numbers = re.findall(r"\d+", definition)
    if numbers:
        node["value"] = int(numbers[0])
        node["operation"] = None
        node["neighbors"] = []
    else:
        left, operation, right = definition.strip().split(" ")
        node["operation"] = operation
        node["neighbors"] = [left, right]
        node["value"] = None

    return node


def digraph_from_nodes(nodes: list) -> nx.DiGraph:
    digraph = nx.DiGraph()
    for node in nodes:
        digraph.add_node(node["name"], value=node["value"], operation=node["operation"])
        for n in node["neighbors"]:
            digraph.add_edge(n, node["name"])

    return digraph


def find_node_value(digraph: nx.DiGraph, node: str) -> int:
    face_value = digraph.nodes[node]["value"]

    if face_value is None:
        # recursive call
        children = list(digraph.predecessors(node))
        child_values = [find_node_value(digraph, child) for child in children]

        assert (
            len(child_values) == 2
        ), f"There should be two values instead {len(child_values)}"

        # eval operation symbol
        operation = digraph.nodes[node]["operation"]
        if operation == "+":
            value = child_values[0] + child_values[1]
        elif operation == "-":
            value = child_values[0] - child_values[1]
        elif operation == "*":
            value = child_values[0] * child_values[1]
        elif operation == "/":
            value = child_values[0] / child_values[1]
        else:
            raise UserWarning(f"Something is wrong, unknown operation {operation}...")

        digraph.nodes[node]["value"] = value
        return value
    else:
        return face_value


if __name__ == "__main__":
    nodes = []
    with open(INPUT_FILE, "r") as file:
        for line in file:
            line = line.strip()
            node = node_from_string(line)
            nodes.append(node)

    digraph = digraph_from_nodes(nodes)
    print(digraph)

    root_value = find_node_value(digraph, "root")
    print(root_value)
