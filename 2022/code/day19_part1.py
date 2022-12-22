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
    return np.zeros((4, 2), dtype=np.int16)


def mine(board: np.ndarray) -> np.ndarray:
    new_board = board.copy()
    new_board[:, RESOURCE_COL] = new_board[:, RESOURCE_COL] + new_board[:, ROBOT_COL]

    return new_board


def board_to_string(board: np.ndarray) -> str:
    return np.array2string(board.reshape(-1), separator=",")


def board_from_string(board_string: str) -> np.ndarray:
    return np.array(eval(board_string), dtype=np.int16).reshape(4, 2)


@cache
def recursive_miner(board_string: str, steps: int) -> int:
    board = board_from_string(board_string)

    if steps == 0:
        return board[GEODE_ROW, RESOURCE_COL]
    else:
        options = []
        # just mine
        new_board = mine(board)
        options.append(recursive_miner(board_to_string(new_board), steps - 1))

        # build robot and mine
        for robot in blueprint:
            if (board + blueprint[robot]).min() >= 0:  # check if affordable
                # mine
                new_board = mine(board)
                # build
                new_board = new_board + blueprint[robot]
                options.append(recursive_miner(board_to_string(new_board), steps - 1))

        return max(options)


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
            geode_array[GEODE_ROW, ROBOT_COL] = 1
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

    starter_board = np.zeros((4, 2), dtype=np.int16)
    starter_board[ORE_ROW, ROBOT_COL] = 1

    STEPS = 19

    blueprint = blueprints[0]

    print(recursive_miner(board_to_string(starter_board), STEPS))

    # speed-up idea: remove geode count from the board and caching?
    print(recursive_miner.cache_info())