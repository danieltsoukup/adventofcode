import re
import math
import networkx as nx
import logging
import time

"""
--- Day 10: Pipe Maze ---

You use the hang glider to ride the hot air from Desert Island all the way up to the floating metal island. This island is surprisingly cold and there definitely aren't any thermals to glide on, so you leave your hang glider behind.

You wander around for a while, but you don't find any people or animals. However, you do occasionally find signposts labeled "Hot Springs" pointing in a seemingly consistent direction; maybe you can find someone at the hot springs and ask them where the desert-machine parts are made.

The landscape here is alien; even the flowers and trees are made of metal. As you stop to admire some metal grass, you notice something metallic scurry away in your peripheral vision and jump into a big pipe! It didn't look like any animal you've ever seen; if you want a better look, you'll need to get ahead of it.

Scanning the area, you discover that the entire field you're standing on is densely packed with pipes; it was hard to tell at first because they're the same metallic silver color as the "ground". You make a quick sketch of all of the surface pipes you can see (your puzzle input).

The pipes are arranged in a two-dimensional grid of tiles:

    | is a vertical pipe connecting north and south.
    - is a horizontal pipe connecting east and west.
    L is a 90-degree bend connecting north and east.
    J is a 90-degree bend connecting north and west.
    7 is a 90-degree bend connecting south and west.
    F is a 90-degree bend connecting south and east.
    . is ground; there is no pipe in this tile.
    S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.

Based on the acoustics of the animal's scurrying, you're confident the pipe that contains the animal is one large, continuous loop.

For example, here is a square loop of pipe:

.....
.F-7.
.|.|.
.L-J.
.....

If the animal had entered this loop in the northwest corner, the sketch would instead look like this:

.....
.S-7.
.|.|.
.L-J.
.....

In the above diagram, the S tile is still a 90-degree F bend: you can tell because of how the adjacent pipes connect to it.

Unfortunately, there are also many pipes that aren't connected to the loop! This sketch shows the same loop as above:

-L|F7
7S-7|
L|7||
-L-J|
L|-JF

In the above diagram, you can still figure out which pipes form the main loop: they're the ones connected to S, pipes those pipes connect to, pipes those pipes connect to, and so on. Every pipe in the main loop connects to its two neighbors (including S, which will have exactly two pipes connecting to it, and which is assumed to connect back to those two pipes).

Here is a sketch that contains a slightly more complex main loop:

..F7.
.FJ|.
SJ.L7
|F--J
LJ...

Here's the same example sketch with the extra, non-main-loop pipe tiles also shown:

7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ

If you want to get out ahead of the animal, you should find the tile in the loop that is farthest from the starting position. Because the animal is in the pipe, it doesn't make sense to measure this by direct distance. Instead, you need to find the tile that would take the longest number of steps along the loop to reach from the starting point - regardless of which way around the loop the animal went.

In the first example with the square loop:

.....
.S-7.
.|.|.
.L-J.
.....

You can count the distance each tile in the loop is from the starting point like this:

.....
.012.
.1.3.
.234.
.....

In this example, the farthest point from the start is 4 steps away.

Here's the more complex loop again:


..F7.
.FJ|.
SJ.L7
|F--J
LJ...

Here are the distances for each tile on that loop:

..45.
.236.
01.78
14567
23...

Find the single giant loop starting at S. How many steps along the loop does it take to get from the starting position to the point farthest from the starting position?

"""

INPUT_FILE = "2023/inputs/day10.txt"

start_time = time.time()

logger = logging.Logger("logger", level=logging.DEBUG)
logger.addHandler(logging.StreamHandler())


N = (-1, 0)
S = (1, 0)
W = (0, -1)
E = (0, 1)

code_to_delta = {
    "|": [N, S],
    "-": [E, W],
    "L": [N, E],
    "J": [N, W],
    "7": [S, W],
    "F": [S, E],
    "S": [S, E, W, N],
}

opposite = {"N": "S", "S": "N", "E": "W", "W": "E"}

# | is a vertical pipe connecting north and south.
# - is a horizontal pipe connecting east and west.
# L is a 90-degree bend connecting north and east.
# J is a 90-degree bend connecting north and west.
# 7 is a 90-degree bend connecting south and west.
# F is a 90-degree bend connecting south and east.
# . is ground; there is no pipe in this tile.
# S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.

if __name__ == "__main__":
    total = 0
    digraph = nx.DiGraph()
    row, col = 0, 0
    start_node = None
    node_list = []
    with open(INPUT_FILE, "r") as file:
        for line in file:
            line = line.strip()
            col = 0
            for char in line:
                from_node = (row, col)
                # add edges
                if char in code_to_delta:
                    node_list.append(from_node)
                    for delta in code_to_delta[char]:
                        to_node = (from_node[0] + delta[0], from_node[1] + delta[1])
                        digraph.add_edge(from_node, to_node, code=char)
                    if char == "S":
                        start_node = from_node

                col += 1
            row += 1

    digraph = digraph.subgraph(node_list)
    logger.info(f">> DiGraph on {len(digraph)} nodes and {len(digraph.edges())} edges.")
    graph = nx.Graph()
    graph.add_nodes_from(digraph.nodes())
    for u, v in digraph.edges():
        if (v, u) in digraph.edges():
            graph.add_edge(u, v)

    logger.debug(graph.edges())

    logger.info(f">> Graph on {len(graph)} nodes and {len(graph.edges())} edges.")

    logger.info(f"Start node degree: {nx.degree(graph, start_node)}")

    # BFS from S node and mark distance from S
    # look for the first time we hit a node that has a neighbor with dist <= its own
    # that will be the cycle and its furthest point
    logger.info(f">> Start at {start_node}")

    for node in graph:
        graph.nodes[node]["parent"] = None
        graph.nodes[node]["seen"] = False
        if node == start_node:
            graph.nodes[node]["distance"] = 0
        else:
            graph.nodes[node]["distance"] = math.inf

    def find_furthest_cycle_distance(
        graph: nx.Graph, start_node: tuple[int, int]
    ) -> int:
        graph.nodes[start_node]["seen"] = True
        queue = [start_node]
        while queue:
            # take next node in the FIFO queue
            current_node = queue.pop(0)
            for neighbor in nx.neighbors(graph, current_node):
                if graph.nodes[neighbor]["seen"] is False:
                    # discovered a new node
                    graph.nodes[neighbor]["seen"] = True
                    graph.nodes[neighbor]["parent"] = current_node
                    graph.nodes[neighbor]["distance"] = (
                        1 + graph.nodes[current_node]["distance"]
                    )
                    queue.append(neighbor)

                # if the neighbor was already seen and closer to the start along a different branch
                # then we found the circle
                elif (neighbor != graph.nodes[current_node]["parent"]) and (
                    graph.nodes[neighbor]["distance"]
                    <= graph.nodes[current_node]["distance"]
                ):
                    return graph.nodes[current_node]["distance"]

    # total = len(nx.find_cycle(graph, start_node))/2
    total = find_furthest_cycle_distance(graph, start_node)

    logger.info(f">> Result {total}")

    end_time = time.time()
    logger.info(f">> Elapsed time: {round(end_time - start_time, 2)} sec.")
