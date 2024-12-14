import re
import math
import logging
import time

INPUT_FILE = "2024/inputs/day14.txt"

start_time = time.time()

logger = logging.Logger("logger", level=logging.INFO)
logger.addHandler(logging.StreamHandler())

if __name__ == "__main__":
    total = 0
    with open(INPUT_FILE, "r") as file:
        for line in file:
            line = line.strip()
            pass

    logger.info(f">> Result {total}")

    end_time = time.time()
    logger.info(f">> Elapsed time: {round(end_time - start_time, 2)} sec.")
