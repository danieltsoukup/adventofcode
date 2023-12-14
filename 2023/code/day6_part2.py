"""

--- Part Two ---

As the race is about to start, you realize the piece of paper with race times and record distances you got earlier actually just has very bad kerning. There's really only one race - ignore the spaces between the numbers on each line.

So, the example from before:

Time:      7  15   30
Distance:  9  40  200

...now instead means this:

Time:      71530
Distance:  940200

Now, you have to figure out how many ways there are to win this single race. In this example, the race lasts for 71530 milliseconds and the record distance you need to beat is 940200 millimeters. You could hold the button anywhere from 14 to 71516 milliseconds and beat the record, a total of 71503 ways!

How many ways can you beat the record in this one much longer race?

"""

import re
import logging
import math

logger = logging.Logger("logger", level=logging.DEBUG)
logger.addHandler(logging.StreamHandler())

INPUT_FILE = "2023/inputs/day6.txt"


if __name__ == "__main__":
    total = 1
    with open(INPUT_FILE, "r") as file:
        for line in file:
            line = line.strip()
            if line.startswith("Time"):
                times = re.findall("[0-9]+", line)
                times = [int("".join(times))]
                logger.debug(f"Times: {times}")
            elif line.startswith("Distance"):
                distances = re.findall("[0-9]+", line)
                distances = [int("".join(distances))]
                logger.debug(f"Distances: {distances}")

    def solve_binom(a: float, b: float, c: float) -> float:
        """
        Get the solution for a binomial equation.
        """
        return (-b + math.sqrt(b**2 - 4 * a * c)) / (2 * a)

    def get_speed(time, dist) -> int:
        """
        Find the smallest int strictly larger then the exact solution.
        """
        exact_sol = solve_binom(-1, time, -dist)
        if math.ceil(exact_sol) == exact_sol:
            return math.ceil(exact_sol) + 1
        else:
            return math.ceil(exact_sol)

    for time, dist in zip(times, distances):
        logger.debug(f"Time {time}, Dist {dist}")
        # solve for min speed such that speed x (time - speed) > dist
        # -dist + timexspeed - speed**2 > 0
        speed = get_speed(time, dist)

        # buffer = time + 1 - 2xspeed
        buffer = time + 1 - 2 * speed
        logger.debug(f" ---> Speed {speed}, Buffer {buffer}\n")

        total *= buffer

    logger.info(f"Result: {total}")
