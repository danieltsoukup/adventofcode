import re
import numpy as np
from datetime import datetime

TEST = False

if TEST:
    INPUT_FILE = "2022/inputs/day19_test.txt"
else:
    INPUT_FILE = "2022/inputs/day19.txt"

ORE_ROW = 0
CLAY_ROW = 1
OBS_ROW = 2
GEODE_ROW = 3

NAME_TO_ROW = {"ore": ORE_ROW, "clay": CLAY_ROW, "obs": OBS_ROW, "geode": GEODE_ROW}

RESOURCE_COL = 0
ROBOT_COL = 1


def read_blueprint(line: str) -> dict[str : np.ndarray]:
    ore_array = Board._setup_empty_array()
    ore_array[ORE_ROW, ROBOT_COL] = 1
    cost = re.findall(r"ore robot costs (\d+) ore", line)[0]
    ore_array[ORE_ROW, RESOURCE_COL] = -1 * int(cost)

    clay_array = Board._setup_empty_array()
    clay_array[CLAY_ROW, ROBOT_COL] = 1
    cost = re.findall(r"clay robot costs (\d+) ore", line)[0]
    clay_array[ORE_ROW, RESOURCE_COL] = -1 * int(cost)

    obs_array = Board._setup_empty_array()
    obs_array[OBS_ROW, ROBOT_COL] = 1
    ore_cost, clay_cost = re.findall(
        r"obsidian robot costs (\d+) ore and (\d+) clay", line
    )[0]
    obs_array[ORE_ROW, RESOURCE_COL] = -1 * int(ore_cost)
    obs_array[CLAY_ROW, RESOURCE_COL] = -1 * int(clay_cost)

    geode_array = Board._setup_empty_array()
    geode_array[GEODE_ROW, ROBOT_COL] = 1
    ore_cost, obs_cost = re.findall(
        r"geode robot costs (\d+) ore and (\d+) obsidian", line
    )[0]
    geode_array[ORE_ROW, RESOURCE_COL] = -1 * int(ore_cost)
    geode_array[OBS_ROW, RESOURCE_COL] = -1 * int(obs_cost)

    blueprint = {
        "ore": ore_array,
        "clay": clay_array,
        "obs": obs_array,
        "geode": geode_array,
    }

    return blueprint


def board_to_string(board: np.ndarray) -> str:
    return np.array2string(board.reshape(-1), separator=",")


def board_from_string(board_string: str) -> np.ndarray:
    return np.array(eval(board_string), dtype=np.int16).reshape(3, 2)


class Board(object):
    def __init__(self, values: np.ndarray = None) -> None:
        self.values = self._get_initial_values(values)
        self.parent = None
        self.best_seen = -1

    def _get_initial_values(self, values) -> np.ndarray:
        return self._setup_empty_array() if values is None else values

    def mine(self) -> None:
        self.values[:, RESOURCE_COL] += self.values[:, ROBOT_COL]

    def build(self, robot_array: np.ndarray) -> None:
        self.values += robot_array

    def is_affordable(self, robot_array: np.ndarray) -> bool:
        return (self.values + robot_array).min() >= 0

    def could_be_mined(self, robot_array: np.ndarray) -> bool:
        needed_resources = robot_array[:, RESOURCE_COL] < 0
        available_miners = self.values[:, ROBOT_COL] > 0

        return np.all(available_miners[needed_resources])

    @classmethod
    def _setup_empty_array(self):
        return np.zeros((4, 2), dtype=np.int16)

    def get_robot_count(self, robot: str) -> int:
        row = NAME_TO_ROW[robot]
        return self.values[row, ROBOT_COL]

    def get_geode_count(self) -> int:
        return self.values[GEODE_ROW, RESOURCE_COL]

    def update_best_seen(self, value: int) -> None:
        self.best_seen = max(self.best_seen, value)
        if self.parent:
            self.parent.update_best_seen(value)


def get_robot_limit(
    blueprint: dict[str, np.ndarray], robot: str
) -> dict[str, np.ndarray]:

    row = NAME_TO_ROW[robot]
    limit = max([-robot_array[row, RESOURCE_COL] for robot_array in blueprint.values()])

    return limit


def theoretical_max(board: Board, steps: int) -> int:
    current_geode_count = board.get_geode_count()

    number_of_robots = board.get_robot_count("geode")
    future_prod_of_current_robots = steps * number_of_robots

    future_prod_of_future_robots = (steps) * (steps - 1) / 2

    return (
        current_geode_count
        + future_prod_of_current_robots
        + future_prod_of_future_robots
    )


def recursive_optimizer(
    board: Board, steps: int, blueprint: dict[str, np.ndarray]
) -> Board:
    if steps == 0:
        return board

    pruning_condition = board.best_seen > theoretical_max(board, steps)

    if pruning_condition:
        # print(f"Pruned with steps {steps}.")
        new_board = Board(board.values.copy())
        remaining_steps = steps
        while remaining_steps > 0:
            new_board.mine()
            remaining_steps -= 1
        return new_board

    else:
        sub_problems = []

        # OPTION 1 - mine until end
        new_board = Board(board.values.copy())
        remaining_steps = steps
        while remaining_steps > 0:
            new_board.mine()
            remaining_steps -= 1
        sub_problems.append(new_board)

        # OPTION 2 - build something
        for robot, robot_array in blueprint.items():
            robot_limit_codition = (
                board.get_robot_count(robot) < get_robot_limit(blueprint, robot)
                if robot != "geode"
                else True
            )
            mining_condition = board.could_be_mined(robot_array)

            if mining_condition and robot_limit_codition:
                new_board = Board(board.values.copy())
                new_board.parent = board
                new_board.best_seen = board.best_seen

                # mine until affordable
                remaining_steps = steps
                while not new_board.is_affordable(robot_array):
                    new_board.mine()
                    remaining_steps -= 1

                if remaining_steps >= 1:
                    # buy & mine in another step
                    new_board.mine()
                    new_board.build(robot_array)
                    remaining_steps -= 1
                    sub_problems.append(
                        recursive_optimizer(new_board, remaining_steps, blueprint)
                    )

                else:  # no steps left after mining to build
                    continue
            else:
                continue

        if sub_problems:
            best = max(sub_problems, key=lambda b: b.get_geode_count())
        else:
            best = board

        board.update_best_seen(best.get_geode_count())

        return best


if __name__ == "__main__":
    blueprints = []
    with open(INPUT_FILE, "r") as file:
        for line in file:
            blueprints.append(read_blueprint(line))

    starter_board = Board()
    starter_board.values[ORE_ROW, ROBOT_COL] = 1

    steps = 32
    optimal_geodes = []
    num_blueprints = 3  # len(blueprints)
    main_start = datetime.now()
    for i in range(num_blueprints):
        print(f"Working on blueprint {i+1}...")
        start = datetime.now()
        blueprint = blueprints[i]
        best = recursive_optimizer(starter_board, steps, blueprint)
        optimal_geodes.append(best.get_geode_count())
        print(best.values)
        print("--- Runtime:", datetime.now() - start)

    print("--- FINAL TIME:", datetime.now() - main_start)
    print("ANSWER:", optimal_geodes[0] * optimal_geodes[1] * optimal_geodes[2])
