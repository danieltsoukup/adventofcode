from day21_part1 import node_from_string, find_node_value, digraph_from_nodes
import networkx as nx

INPUT_FILE = "2022/inputs/day21.txt"


def is_predecessor(digraph: nx.DiGraph, node: str, other_node: str) -> bool:
    immediate_preds = list(digraph.predecessors(node))

    if other_node in immediate_preds or other_node == node:
        return True
    elif len(immediate_preds) == 0:
        return False
    else:
        return any(
            [is_predecessor(digraph, pred, other_node) for pred in immediate_preds]
        )


if __name__ == "__main__":
    nodes = []
    with open(INPUT_FILE, "r") as file:
        for line in file:
            line = line.strip()
            node = node_from_string(line)
            nodes.append(node)

    digraph = digraph_from_nodes(nodes)
    print(digraph)

    # pred's of root
    left, right = list(digraph.predecessors("root"))

    # set humn node value to None
    HUMN = "humn"
    digraph.nodes[HUMN]["value"] = None

    print(is_predecessor(digraph, left, HUMN))

    print(is_predecessor(digraph, right, HUMN))

    print(list(digraph.successors(left)))

    current_node = "root"
    left, right = list(digraph.predecessors(current_node))
    if is_predecessor(digraph, left, HUMN):
        digraph.nodes[left]["expected"] = find_node_value(digraph, right)
        current_node = left
    else:
        digraph.nodes[right]["expected"] = find_node_value(digraph, left)
        current_node = right

    while current_node != HUMN:
        print(current_node)
        left, right = list(digraph.predecessors(current_node))
        operation = digraph.nodes[current_node]["operation"]
        expected = digraph.nodes[current_node]["expected"]

        if is_predecessor(digraph, left, HUMN):
            right_value = find_node_value(digraph, right)
            if operation == "+":
                left_expected = expected - right_value
            elif operation == "-":
                left_expected = expected + right_value
            elif operation == "*":
                left_expected = expected / right_value
            elif operation == "/":
                left_expected = expected * right_value

            digraph.nodes[left]["expected"] = left_expected
            current_node = left

        else:
            left_value = find_node_value(digraph, left)
            if operation == "+":
                right_expected = expected - left_value
            elif operation == "-":
                right_expected = left_value - expected
            elif operation == "*":
                right_expected = expected / left_value
            elif operation == "/":
                right_expected = left_value / expected

            digraph.nodes[right]["expected"] = right_expected
            current_node = right

    print(digraph.nodes[current_node]["expected"])
