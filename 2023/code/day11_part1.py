import re
import math
import logging
import time
import numpy as np

INPUT_FILE = "2023/inputs/day11.txt"
start_time = time.time()

logger = logging.Logger("logger", level=logging.DEBUG)
logger.addHandler(logging.StreamHandler())

if __name__ == "__main__":
    total = 0
    galaxies = []
    row = 0
    col = 0
    with open(INPUT_FILE, "r") as file:
        for line in file:
            line = line.strip()
            col = 0
            for char in line:
                if char == "#":
                    galaxies.append((row, col))

                col += 1

            row += 1

    logger.debug(f"Galaxies {len(galaxies)}")

    expand_rows = [i for i in range(row) if i not in [j for j, _ in galaxies]]
    expand_cols = [i for i in range(col) if i not in [j for _, j in galaxies]]
    logger.debug(f"Expand rows {len(expand_rows)}, expand cols {len(expand_cols)}")

    row_count = np.zeros(row)
    row_count[expand_rows] += 1
    row_count = row_count.cumsum()
    logger.debug(row_count)

    col_count = np.zeros(col)
    col_count[expand_cols] += 1
    col_count = col_count.cumsum()
    logger.debug(col_count)

    for node1 in galaxies:
        for node2 in galaxies:
            dist = abs(node1[0] - node2[0]) + abs(node1[1] - node2[1])
            dist += abs(row_count[node1[0]] - row_count[node2[0]])
            dist += abs(col_count[node1[1]] - col_count[node2[1]])
            total += dist

    logger.info(f">> Result {total/2}")

    end_time = time.time()
    logger.info(f">> Elapsed time: {round(end_time - start_time, 2)} sec.")
