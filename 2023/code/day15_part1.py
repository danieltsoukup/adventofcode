import re
import math
import logging
import time

INPUT_FILE = "2023/inputs/day15.txt"

start_time = time.time()

logger = logging.Logger("logger", level=logging.DEBUG)
logger.addHandler(logging.StreamHandler())


def hash_encode(string: str) -> int:
    value = 0
    char_list = list(string)
    while char_list:
        char = char_list.pop(0)
        value += ord(char)
        value *= 17
        value = value % 256

    return value


if __name__ == "__main__":
    total = 0
    with open(INPUT_FILE, "r") as file:
        for line in file:
            line = line.strip()
            strings = line.split(",")

            for string in strings:
                total += hash_encode(string)

            logger.debug(len(strings))

    logger.info(f">> Result {total}")

    end_time = time.time()
    logger.info(f">> Elapsed time: {round(end_time - start_time, 2)} sec.")
