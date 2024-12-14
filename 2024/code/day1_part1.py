import re
import math
import logging
import time
import numpy as np

INPUT_FILE = "2024/inputs/day1.txt"

start_time = time.time()

logger = logging.Logger("logger", level=logging.INFO)
logger.addHandler(logging.StreamHandler())

if __name__ == "__main__":
    total = 0
    numbers = []
    with open(INPUT_FILE, "r") as file:
        for line in file:
            numbers.append(line.strip().split())

    first = sorted([int(one) for one, _ in numbers])
    second = sorted([int(two) for _, two in numbers])

    total = sum([abs(x - y) for x, y in zip(first, second)])

    logger.info(f">> Result {total}")

    end_time = time.time()
    logger.info(f">> Elapsed time: {round(end_time - start_time, 2)} sec.")
