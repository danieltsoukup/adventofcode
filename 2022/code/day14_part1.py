import re

INPUT_FILE = "2022/inputs/day14.txt"


class Cave:
    def __init__(self, blocked: set[tuple[int]], source: tuple[int], abyss: int):
        self.blocked = blocked
        self.source = source
        # self.dynamic_source = self.source
        self.abyss = abyss
        self.full = False

    def _add_block(self, rock: tuple[int]) -> None:
        self.blocked.add(rock)

    def drop_from_source(self):
        current_position = self.source
        while self._step(current_position) != current_position:
            current_position = self._step(current_position)
            # abyss check
            if current_position[1] > self.abyss:
                self.full = True
                break

        if not self.full:
            self._add_block(current_position)

    def _step(self, position: tuple[int]) -> tuple[int]:
        down = (position[0], position[1] + 1)
        down_left = (position[0] - 1, position[1] + 1)
        down_right = (position[0] + 1, position[1] + 1)

        if not (down in self.blocked):
            return down
        elif not (down_left in self.blocked):
            return down_left
        elif not (down_right in self.blocked):
            return down_right
        else:
            return position


def get_line_segment(point1: tuple[int], point2: tuple[int]) -> set[tuple[int]]:
    points = set()
    if point1[0] == point2[0]:
        if point1[1] < point2[1]:
            for y in range(point1[1], point2[1] + 1):
                points.add((point1[0], y))
        else:
            for y in range(point2[1], point1[1] + 1):
                points.add((point1[0], y))

    if point1[1] == point2[1]:
        if point1[0] < point2[0]:
            for x in range(point1[0], point2[0] + 1):
                points.add((x, point1[1]))
        else:
            for x in range(point2[0], point1[0] + 1):
                points.add((x, point1[1]))

    return points


if __name__ == "__main__":
    SOURCE = (500, 0)

    rocks = set()
    with open(INPUT_FILE, "r") as file:
        for line in file:
            line = line.strip()
            tuples = re.findall(r"(\d+),(\d+)", line)
            tuples = [(int(x), int(y)) for x, y in tuples]

            for point1, point2 in zip(tuples[:-1], tuples[1:]):
                points = get_line_segment(point1, point2)
                rocks = rocks.union(points)

    abyss_level = max([y for _, y in rocks]) + 1

    cave = Cave(blocked=rocks, source=SOURCE, abyss=abyss_level)

    sand_counter = 0
    while not cave.full:
        cave.drop_from_source()

        if not cave.full:
            sand_counter += 1

    print(sand_counter)
