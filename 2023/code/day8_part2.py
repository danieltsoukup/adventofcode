"""
--- Part Two ---

The sandstorm is upon you and you aren't any closer to escaping the wasteland. You had the camel follow the instructions, but you've barely left your starting position. It's going to take significantly more steps to escape!

What if the map isn't for people - what if the map is for ghosts? Are ghosts even bound by the laws of spacetime? Only one way to find out.

After examining the maps a bit longer, your attention is drawn to a curious fact: the number of nodes with names ending in A is equal to the number ending in Z! If you were a ghost, you'd probably just start at every node that ends with A and follow all of the paths at the same time until they all simultaneously end up at nodes that end with Z.

For example:

LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)

Here, there are two starting nodes, 11A and 22A (because they both end with A). As you follow each left/right instruction, use that instruction to simultaneously navigate away from both nodes you're currently on. Repeat this process until all of the nodes you're currently on end with Z. (If only some of the nodes you're on end with Z, they act like any other node and you continue as normal.) In this example, you would proceed as follows:

    Step 0: You are at 11A and 22A.
    Step 1: You choose all of the left paths, leading you to 11B and 22B.
    Step 2: You choose all of the right paths, leading you to 11Z and 22C.
    Step 3: You choose all of the left paths, leading you to 11B and 22Z.
    Step 4: You choose all of the right paths, leading you to 11Z and 22B.
    Step 5: You choose all of the left paths, leading you to 11B and 22C.
    Step 6: You choose all of the right paths, leading you to 11Z and 22Z.

So, in this example, you end up entirely on nodes that end in Z after 6 steps.

Simultaneously start on every node that ends with A. How many steps does it take before you're only on nodes that end with Z?

"""

import re
import logging
import networkx as nx
import time
import math

start_time = time.time()

logger = logging.Logger("logger", level=logging.INFO)
logger.addHandler(logging.StreamHandler())

INPUT_FILE = "2023/inputs/day8.txt"


if __name__ == "__main__":
    total = 0
    row = 0
    graph = nx.DiGraph()
    with open(INPUT_FILE, "r") as file:
        for line in file:
            line = line.strip()
            if row == 0:
                steps = list(line)
                logger.debug(steps)
            elif line != "":
                source, left, right = re.findall("[A-Z]{3}", line)
                if left != right:
                    graph.add_edge(source, left, dir="L")
                    graph.add_edge(source, right, dir="R")
                else:
                    graph.add_edge(source, left, dir="RL")

            row += 1

    logger.debug(
        f"Graph created on {graph.number_of_nodes()} nodes and {graph.number_of_edges()} edges."
    )

    current_nodes: list[str] = [node for node in graph if node.endswith("A")]
    logger.info(f"Starting nodes: {current_nodes}")

    def step_in_dir(graph: nx.DiGraph, node: str, dir: str) -> str:
        """
        Find the L/R neighbor of a node based on the `dir` edge attribute.
        """
        neighbors = graph[node]
        filtered = [u for u in neighbors if dir in neighbors[u]["dir"]]
        assert len(filtered) == 1

        return filtered[0]

    logger.debug(step_in_dir(graph, "AAA", "R"))

    results: list[int] = []
    for node in current_nodes:
        step_count = 0
        current_node = node
        while not current_node.endswith("Z"):
            dir = steps[step_count % len(steps)]
            current_node = step_in_dir(graph, current_node, dir)
            step_count += 1

        results.append(step_count)

        logger.info(
            f"Node {node}\t solved in {step_count} steps \t got to {current_node}."
        )

    logger.info(f"LCM of steps: {math.lcm(*results)}")

    end_time = time.time()
    logger.info(f">> Elapsed time: {round(end_time - start_time, 2)} sec.")
