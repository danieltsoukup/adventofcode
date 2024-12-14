import re
import math
import logging
import time
from dataclasses import dataclass

start_time = time.time()

INPUT_FILE = "2024/inputs/day14.txt"

logger = logging.Logger("logger", level=logging.INFO)
logger.addHandler(logging.StreamHandler())

WIDTH = 101
HEIGHT = 103
NUM_STEPS = 100


@dataclass
class Robot:
    x: int
    y: int
    vx: int
    vy: int

    def move(self, num_steps: int = NUM_STEPS) -> None:
        self.x += num_steps * self.vx
        self.x = self.x % WIDTH

        self.y += num_steps * self.vy
        self.y = self.y % HEIGHT

    def q1(self) -> bool:
        return self.x < WIDTH / 2 and self.y < HEIGHT / 2

    def q2(self) -> bool:
        return self.x < WIDTH / 2 and self.y > HEIGHT / 2

    def q3(self) -> bool:
        return self.x > WIDTH / 2 and self.y < HEIGHT / 2

    def q4(self) -> bool:
        return self.x > WIDTH / 2 and self.y > HEIGHT / 2


if __name__ == "__main__":
    total = 1
    robots = []
    with open(INPUT_FILE, "r") as file:
        for line in file:
            tuples = re.findall(r"(-?\d+),(-?\d+)", line)
            tuples = [(int(x), int(y)) for x, y in tuples]
            point, velocity = tuples
            robot = Robot(x=point[0], y=point[1], vx=velocity[0], vy=velocity[1])
            robot.move()

            logger.info(robot)

            robots.append(robot)

    total *= sum([robot.q1() for robot in robots])
    total *= sum([robot.q2() for robot in robots])
    total *= sum([robot.q3() for robot in robots])
    total *= sum([robot.q4() for robot in robots])

    logger.info(f">> Result {total}")

    end_time = time.time()
    logger.info(f">> Elapsed time: {round(end_time - start_time, 2)} sec.")
