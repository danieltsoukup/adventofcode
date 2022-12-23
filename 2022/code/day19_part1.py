import re
import numpy as np
from functools import cache

INPUT_FILE = "2022/inputs/day19_test.txt"

ORE_ROW = 0
CLAY_ROW = 1
OBS_ROW = 2
GEODE_ROW = 3

RESOURCE_COL = 0
ROBOT_COL = 1


def setup_empty_array():
    return np.zeros((3, 2), dtype=np.int16)


def mine(board: np.ndarray, times: int = 1) -> np.ndarray:
    new_board = board.copy()
    new_board[:, RESOURCE_COL] = (
        new_board[:, RESOURCE_COL] + times * new_board[:, ROBOT_COL]
    )

    return new_board


def board_to_string(board: np.ndarray) -> str:
    return np.array2string(board.reshape(-1), separator=",")


def board_from_string(board_string: str) -> np.ndarray:
    return np.array(eval(board_string), dtype=np.int16).reshape(3, 2)


def is_affordable(
    board: np.ndarray,
    robot_array: np.ndarray,
) -> bool:
    # check if affordable
    difference_after_build = board[:, RESOURCE_COL] + robot_array[:, RESOURCE_COL]
    enough_resources = difference_after_build.min() >= 0

    needed_for_robot = robot_array[:, RESOURCE_COL] < 0
    depleted = difference_after_build[needed_for_robot].min() == 0

    return enough_resources, depleted


def can_be_mined(board: np.ndarray, robot_array: np.ndarray) -> bool:
    needed_for_robot = robot_array[:, RESOURCE_COL] < 0
    mining = board[:, ROBOT_COL] > 0

    return np.all(needed_for_robot <= mining)


def mining_steps_needed(board: np.ndarray, robot_array: np.ndarray) -> int:
    difference = board[:, RESOURCE_COL] + robot_array[:, RESOURCE_COL]
    # assert (difference < 0).sum() > 0, "No need to mine."
    if (difference < 0).sum() == 0:
        return 0
    else:
        return -(difference[difference < 0].min())


def evaluate_future(board: np.ndarray, steps: int) -> int:
    pass


CACHE = dict()


def recursive_miner(board_string: str, steps: int) -> int:
    if (board_string, steps) in CACHE:
        return CACHE[(board_string, steps)]

    board = board_from_string(board_string)

    assert board.min() >= 0, f"something wrong, board is {board}"
    assert steps >= 0, "steps negative"

    if steps == 0:
        return 0
    else:
        options = [0]

        # build robot and mine
        for robot in blueprint:
            robot_array = blueprint[robot]
            enough_resources, depleted = is_affordable(board, robot_array)

            if enough_resources and not depleted:
                continue

            if can_be_mined(board, robot_array):
                needed_steps = mining_steps_needed(board, robot_array)
                if steps - needed_steps <= 0:
                    continue
                else:
                    # mine the resources needed + 1
                    new_board = mine(board, times=needed_steps + 1)
                    # build
                    new_board = new_board + robot_array

                    if robot == "geode":  # future mining of currently built robot
                        options.append(
                            (steps - 1 - needed_steps)
                            + recursive_miner(
                                board_to_string(new_board), steps - 1 - needed_steps
                            )
                        )
                    else:
                        options.append(
                            recursive_miner(
                                board_to_string(new_board), steps - 1 - needed_steps
                            )
                        )

            else:
                continue

        best = max(options)

        CACHE[(board_string, steps)] = best

        return best


if __name__ == "__main__":
    blueprints = []
    with open(INPUT_FILE, "r") as file:
        for line in file:
            line = line.strip()

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
            # geode_array[GEODE_ROW, ROBOT_COL] = 1
            ore_cost, obs_cost = re.findall(
                r"geode robot costs (\d+) ore and (\d+) obsidian", line
            )[0]
            geode_array[ORE_ROW, RESOURCE_COL] = -1 * int(ore_cost)
            geode_array[OBS_ROW, RESOURCE_COL] = -1 * int(obs_cost)

            blueprints.append(
                {
                    "ore": ore_array,
                    "clay": clay_array,
                    "obs": obs_array,
                    "geode": geode_array,
                }
            )

    starter_board = setup_empty_array()
    starter_board[ORE_ROW, ROBOT_COL] = 1

    STEPS = 20

    blueprint = blueprints[0]

    try:
        print(recursive_miner(board_to_string(starter_board), STEPS))
    except KeyboardInterrupt:
        # speed-up idea: remove geode count from the board and caching?
        print(recursive_miner.cache_info())
