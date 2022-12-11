from utils import Monkey, parse_monkey_inputs, get_monkey_result


INPUT_FILE = "2022/inputs/day11.txt"


if __name__ == "__main__":
    troop_config = parse_monkey_inputs(INPUT_FILE)
    troop = {name: Monkey(troop_config[name]) for name in troop_config}

    for _ in range(20):
        for monkey in troop.values():
            monkey.turn(troop)

    print(get_monkey_result(troop))
