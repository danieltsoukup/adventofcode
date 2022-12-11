from utils import Monkey, MonkeyConfig, parse_monkey_inputs, get_monkey_result


INPUT_FILE = "2022/inputs/day11.txt"


class EfficientMonkey(Monkey):
    def __init__(self, config: MonkeyConfig, troop_config: dict[MonkeyConfig]):
        super().__init__(config)
        self.items: list[dict[int, int]] = self._get_modulo_items(troop_config)

    def _get_modulo_items(
        self, troop_config: dict[MonkeyConfig]
    ) -> list[dict[int, int]]:
        mods = set([config["test_divisible"] for config in troop_config.values()])
        modulo_items = [{mod: item % mod for mod in mods} for item in self.items]

        return modulo_items

    def _process_item(self, mod_item: dict[int, int]) -> dict[int, int]:
        for mod in mod_item:
            mod_item[mod] = self.operation(mod_item[mod]) % mod

        return mod_item

    def _evaluate_item(self, mod_item: dict[int, int]) -> bool:
        return mod_item[self.test] % self.test == 0


if __name__ == "__main__":
    troop_config = parse_monkey_inputs(INPUT_FILE)
    troop = {
        name: EfficientMonkey(troop_config[name], troop_config) for name in troop_config
    }

    for i in range(10000):
        for monkey in troop.values():
            monkey.turn(troop)

        if i % 100 == 0:
            print(f"Done {i}...")

    print(get_monkey_result(troop))
