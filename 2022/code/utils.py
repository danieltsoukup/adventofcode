from collections import defaultdict
from typing import Any, TypedDict
from math import copysign
import re


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


##############
### DAY 11 ###
##############


class MonkeyConfig(TypedDict):
    name: str
    starter_items: list[int]
    operation: callable
    if_true_pass_to: str
    if_false_pass_to: str
    test_divisible: int


class Monkey:
    def __init__(self, config: MonkeyConfig):
        self.name = config["name"]
        self.items = config["starter_items"]
        self.if_true_pass_to = config["if_true_pass_to"]
        self.if_false_pass_to = config["if_false_pass_to"]
        self.operation = config["operation"]
        self.test = config["test_divisible"]

        self.turn_counter = 0

    def turn(self, troop: dict) -> None:
        while self.items:
            item = self.items.pop(0)
            processed_item = self._process_item(item)
            if self._evaluate_item(processed_item):
                troop[self.if_true_pass_to].add_item(processed_item)
            else:
                troop[self.if_false_pass_to].add_item(processed_item)

            self.turn_counter += 1

    def add_item(self, item) -> None:
        self.items.append(item)

    def _evaluate_item(self, item: int) -> bool:
        return item % self.test == 0

    def _process_item(self, item: int) -> int:
        processed_item = self.operation(item)

        return processed_item // 3


def operation_factory(op_string: str) -> callable:
    def operation(old: int):
        new = eval(op_string.strip("new = "))
        return new

    return operation


def parse_monkey_inputs(input_file: str) -> dict[str, MonkeyConfig]:
    troop_config = dict()

    with open(input_file, "r") as file:
        for line in file:
            line = line.strip().lower()
            if line.startswith("monkey"):
                current_config = MonkeyConfig()
                current_config["name"] = line.strip(":")

            elif line.startswith("starting items"):
                current_config["starter_items"] = [
                    int(num) for num in re.findall(r"\d+", line)
                ]

            elif line.startswith("operation"):
                op_string = line.strip("operation:").strip()

                current_config["operation"] = operation_factory(op_string)

            elif line.startswith("test"):
                current_config["test_divisible"] = int(re.findall(r"\d+", line)[0])

            elif line.startswith("if true"):
                current_config["if_true_pass_to"] = re.findall(r"monkey \d+", line)[0]

            elif line.startswith("if false"):
                current_config["if_false_pass_to"] = re.findall(r"monkey \d+", line)[0]

            elif line == "":
                troop_config[current_config["name"]] = current_config

    troop_config[current_config["name"]] = current_config

    return troop_config


def get_monkey_result(troop: dict[str, Monkey]) -> int:
    counters = []
    for monkey in troop.values():
        counters.append(monkey.turn_counter)

    counters.sort()

    return counters[-1] * counters[-2]
