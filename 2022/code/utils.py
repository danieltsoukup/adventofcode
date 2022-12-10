from collections import defaultdict
from typing import Any
from math import copysign


def read_inputs(path: str) -> list[str]:
    inputs = []
    with open(path, "r") as file:
        for line in file:
            line = line.strip()
            inputs.append(line)

    return inputs


# Partly based on
# https://stackoverflow.com/questions/3009935/looking-for-a-good-python-tree-data-structure
class Dir(defaultdict):
    def __init__(self, parent):
        super().__init__(self)
        self.parent = parent
        self.size = None

    def __call__(self):
        return self.__class__(self)

    def get_files(self):
        """
        Depth-First generator over files.
        """
        for child in self:
            if isinstance(self[child], Dir):
                for file in self[child].get_files():
                    yield file
            else:
                yield self[child]

    def get_dirs(self):
        """
        Depth-First generator over directories.
        """
        for child in self:
            if isinstance(self[child], Dir):
                for dir in self[child].get_dirs():
                    yield dir
        yield self

    def get_size(self):
        """
        Get total size.
        """
        if self.size is None:
            total = 0
            for child in self:
                if isinstance(self[child], Dir):
                    total += self[child].get_size()
                else:
                    total += self[child]

            self.size = total

        return self.size


def move(head: tuple[int], direction: str, num_steps: int) -> tuple[int]:
    if direction == "L":
        new_head = (head[0], head[1] - num_steps)
    elif direction == "R":
        new_head = (head[0], head[1] + num_steps)
    elif direction == "U":
        new_head = (head[0] + num_steps, head[1])
    elif direction == "D":
        new_head = (head[0] - num_steps, head[1])
    else:
        raise ValueError(f"Unknown direction ({direction}).")

    return new_head


def adjust_tail(head: tuple[int], tail: tuple[int]) -> tuple[int]:
    delta = (head[0] - tail[0], head[1] - tail[1])
    abs_delta = (abs(delta[0]), abs(delta[1]))

    # adjacent - remain in-place
    if max(abs_delta) <= 1:
        displacement = (0, 0)
    # same axis - move next-to
    elif min(abs_delta) == 0:
        abs_displacement = (max(0, abs_delta[0] - 1), max(0, abs_delta[1] - 1))
        displacement = (
            copysign(abs_displacement[0], delta[0]),
            copysign(abs_displacement[1], delta[1]),
        )
    # diagonal - cross step and move next-to
    else:
        abs_displacement = (
            abs_delta[0] - 1 if abs_delta[0] > 1 else abs_delta[0],
            abs_delta[1] - 1 if abs_delta[1] > 1 else abs_delta[1],
        )

        displacement = (
            copysign(abs_displacement[0], delta[0]),
            copysign(abs_displacement[1], delta[1]),
        )

    return (int(tail[0] + displacement[0]), int(tail[1] + displacement[1]))
