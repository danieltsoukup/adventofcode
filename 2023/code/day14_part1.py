import re
import math
import logging
import time
from collections import defaultdict

INPUT_FILE = "2023/inputs/day14.txt"

start_time = time.time()

logger = logging.Logger("logger", level=logging.INFO)
logger.addHandler(logging.StreamHandler())

if __name__ == "__main__":
    total = 0
    row = 0
    col = 0
    space_counter = defaultdict(int)
    stone_collection = []
    with open(INPUT_FILE, "r") as file:
        for line in file:
            line = line.strip()
            col = 0
            for char in line:
                node = (row, col)
                if char == ".":
                    space_counter[node] = space_counter[(row - 1, col)] + 1
                elif char == "O":
                    stone_collection.append(node)
                    space_counter[node] = space_counter[(row - 1, col)]
                elif char == "#":
                    space_counter[node] = 0
                col += 1
            row += 1

    for node in stone_collection:
        total += (row - node[0]) + space_counter[node]

    logger.info(f">> Result {total}")

    end_time = time.time()
    logger.info(f">> Elapsed time: {round(end_time - start_time, 2)} sec.")
