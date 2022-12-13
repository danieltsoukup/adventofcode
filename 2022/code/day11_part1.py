from typing import TypedDict
import re

INPUT_FILE = "2022/inputs/day11.txt"


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


if __name__ == "__main__":
    troop_config = parse_monkey_inputs(INPUT_FILE)
    troop = {name: Monkey(troop_config[name]) for name in troop_config}

    for _ in range(20):
        for monkey in troop.values():
            monkey.turn(troop)

    print(get_monkey_result(troop))
