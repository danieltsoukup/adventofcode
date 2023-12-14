"""
--- Day 8: Haunted Wasteland ---

You're still riding a camel across Desert Island when you spot a sandstorm quickly approaching. When you turn to warn the Elf, she disappears before your eyes! To be fair, she had just finished warning you about ghosts a few minutes ago.

One of the camel's pouches is labeled "maps" - sure enough, it's full of documents (your puzzle input) about how to navigate the desert. At least, you're pretty sure that's what they are; one of the documents contains a list of left/right instructions, and the rest of the documents seem to describe some kind of network of labeled nodes.

It seems like you're meant to use the left/right instructions to navigate the network. Perhaps if you have the camel follow the same instructions, you can escape the haunted wasteland!

After examining the maps for a bit, two nodes stick out: AAA and ZZZ. You feel like AAA is where you are now, and you have to follow the left/right instructions until you reach ZZZ.

This format defines each node of the network individually. For example:

RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)

Starting with AAA, you need to look up the next element based on the next left/right instruction in your input. In this example, start with AAA and go right (R) by choosing the right element of AAA, CCC. Then, L means to choose the left element of CCC, ZZZ. By following the left/right instructions, you reach ZZZ in 2 steps.

Of course, you might not find ZZZ right away. If you run out of left/right instructions, repeat the whole sequence of instructions as necessary: RL really means RLRLRLRLRLRLRLRL... and so on. For example, here is a situation that takes 6 steps to reach ZZZ:

LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)

Starting at AAA, follow the left/right instructions. How many steps are required to reach ZZZ?
"""

import re
import logging
import math
from collections import Counter
import networkx as nx

logger = logging.Logger("logger", level=logging.DEBUG)
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

    current_node = "AAA"
    end_node = "ZZZ"
    step_count = 0

    def step_in_dir(graph: nx.DiGraph, node: str, dir: str) -> str:
        """
        Find the L/R neighbor of a node based on the `dir` edge attribute.
        """
        neighbors = graph[node]
        filtered = [u for u in neighbors if dir in neighbors[u]["dir"]]
        assert len(filtered) == 1

        return filtered[0]

    logger.debug(step_in_dir(graph, "AAA", "R"))

    while current_node != "ZZZ":
        logger.debug(current_node)
        dir = steps[step_count % len(steps)]
        current_node = step_in_dir(graph, current_node, dir)
        step_count += 1

    logger.info(f"Result: {step_count}")
