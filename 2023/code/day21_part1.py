import networkx as nx
import re
import math
import logging
import time

start_time = time.time()


INPUT_FILE = "2023/inputs/day21.txt"

logger = logging.Logger("logger", level=logging.INFO)
logger.addHandler(logging.StreamHandler())

if __name__ == "__main__":
    total = 0
    row, col = 0, 0
    start_node = None
    node_list = []
    with open(INPUT_FILE, "r") as file:
        for line in file:
            line = line.strip()
            col = 0
            for char in line:
                current_node = (row, col)
                if char == "S":
                    start_node = current_node
                    node_list.append(current_node)
                elif char == ".":
                    node_list.append(current_node)
                else:
                    pass

                col += 1
            row += 1

    # create graph from nodes on a grid
    graph = nx.grid_2d_graph(row, col)
    graph = graph.subgraph(node_list)

    logger.info(f"Built graph on {len(graph)} nodes with {len(graph.edges())} edges.")
    logger.info(f"Start node {start_node}.")

    steps_away = [start_node]
    DIST = 64
    for _ in range(DIST):
        collector = []
        for node in steps_away:
            neighbors = nx.neighbors(graph, node)
            collector.extend(neighbors)

        steps_away = list(set(collector))

    result = len(steps_away)

    # ### BFS for nodes exactly 64 steps away ###

    # # set up node attributes
    # for node in graph:
    #     graph.nodes[node]["seen"] = False
    #     graph.nodes[node]["distance"] = None
    #     graph.nodes[node]["parent"] = None

    # # initialize at start
    # graph.nodes[start_node]["seen"] = True
    # graph.nodes[start_node]["distance"] = 0

    # # FIFO list
    # todo_queue = [start_node]
    # while todo_queue:
    #     next_node = todo_queue.pop(0)
    #     # explore unseen neighbors
    #     for node in nx.neighbors(graph, next_node):
    #         if graph.nodes[node]["seen"] is False:
    #             todo_queue.append(node)
    #             graph.nodes[node]["seen"] = True
    #             graph.nodes[node]["distance"] = 1 + graph.nodes[next_node]["distance"]
    #             graph.nodes[node]["parent"] = next_node

    logger.info(f"Result {result}.")
