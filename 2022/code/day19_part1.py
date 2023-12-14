import re
import numpy as np
from functools import cache
from datetime import datetime


TEST = False

if TEST:
    INPUT_FILE = "2022/inputs/day19_test.txt"
else:
    INPUT_FILE = "2022/inputs/day19.txt"

ORE_ROW = 0
CLAY_ROW = 1
OBS_ROW = 2

RESOURCE_COL = 0
ROBOT_COL = 1


def setup_empty_array():
    return np.zeros((3, 2), dtype=np.int16)


def read_blueprint(line: str) -> dict[str : np.ndarray]:
    ore_array = setup_empty_array()
    ore_array[ORE_ROW, ROBOT_COL] = 1
    cost = re.findall(r"ore robot costs (\d+) ore", line)[0]
    ore_array[ORE_ROW, RESOURCE_COL] = -1 * int(cost)

    clay_array = setup_empty_array()
    clay_array[CLAY_ROW, ROBOT_COL] = 1
    cost = re.findall(r"clay robot costs (\d+) ore", line)[0]
    clay_array[ORE_ROW, RESOURCE_COL] = -1 * int(cost)

    obs_array = setup_empty_array()
    obs_array[OBS_ROW, ROBOT_COL] = 1
    ore_cost, clay_cost = re.findall(
        r"obsidian robot costs (\d+) ore and (\d+) clay", line
    )[0]
    obs_array[ORE_ROW, RESOURCE_COL] = -1 * int(ore_cost)
    obs_array[CLAY_ROW, RESOURCE_COL] = -1 * int(clay_cost)

    geode_array = setup_empty_array()
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


def could_be_mined(board: np.ndarray, robot_array: np.ndarray) -> bool:
    needed_resources = robot_array[:, RESOURCE_COL] < 0
    available_miners = board[:, ROBOT_COL] > 0

    return np.all(available_miners[needed_resources])


def mine(board: np.ndarray) -> np.ndarray:
    new_board = board.copy()
    new_board[:, RESOURCE_COL] += new_board[:, ROBOT_COL]

    return new_board


def board_to_string(board: np.ndarray) -> str:
    return np.array2string(board.reshape(-1), separator=",")


def board_from_string(board_string: str) -> np.ndarray:
    return np.array(eval(board_string), dtype=np.int16).reshape(3, 2)


@cache
def recursive_optimizer(board_string: str, steps: int):
    board = board_from_string(board_string)
    # sanity check - can be removed at the end
    # assert board.min() >= 0 and steps >= 0

    # can't build and mine with new robots in <= 1 steps
    if steps <= 1:
        return 0

    else:
        optimal = [0]

        for robot, robot_array in blueprint.items():
            # check if we can afford it by further mining so that at least 1 step remains
            if could_be_mined(board, robot_array):
                mining_steps = 0
                new_board = board.copy()
                # mine until affordable
                while (new_board + robot_array).min() < 0:
                    new_board = mine(new_board)
                    mining_steps += 1

                remaining_steps = steps - mining_steps
                # did we ran out of time?
                # need one step to actually build the robot and then another to use it later
                if remaining_steps > 1:
                    # buy & mine in another step
                    new_board = mine(new_board)
                    new_board += robot_array
                    remaining_steps -= 1

                    new_board_string = board_to_string(new_board)
                    # if the robot was a geode, add the remaining steps to the recursive output
                    if robot == "geode":
                        optimal.append(
                            remaining_steps
                            + recursive_optimizer(new_board_string, remaining_steps)
                        )
                    else:
                        optimal.append(
                            recursive_optimizer(new_board_string, remaining_steps)
                        )
                else:  # at most one step remained after mining - no new robots will mine after purchase
                    continue
            else:
                continue

        return max(optimal)


if __name__ == "__main__":
    blueprints = []
    with open(INPUT_FILE, "r") as file:
        for line in file:
            blueprints.append(read_blueprint(line))

    starter_board = setup_empty_array()
    starter_board[ORE_ROW, ROBOT_COL] = 1
    starter_board_string = board_to_string(starter_board)

    steps = 24
    optimal_geodes = []
    for i in range(len(blueprints)):
        print(f"Working on blueprint {i+1}...")
        start = datetime.now()
        blueprint = blueprints[i]
        optimal = recursive_optimizer(starter_board_string, steps)
        optimal_geodes.append(optimal)
        print("--- Optimal:", optimal)
        print("--- Runtime:", datetime.now() - start)
        print(recursive_optimizer.cache_info())

        recursive_optimizer.cache_clear()

    print(sum([(i + 1) * opt for i, opt in enumerate(optimal_geodes)]))
