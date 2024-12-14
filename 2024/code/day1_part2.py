import re
import math
import logging
import time
from collections import Counter

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

    first = set([int(one) for one, _ in numbers])
    second_counter = Counter([int(two) for _, two in numbers])

    total = sum([one * second_counter[one] for one in first])

    logger.info(f">> Result {total}")

    end_time = time.time()
    logger.info(f">> Elapsed time: {round(end_time - start_time, 2)} sec.")
