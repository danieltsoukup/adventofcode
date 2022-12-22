from collections import defaultdict
import re
from enum import Enum
import networkx as nx

INPUT_FILE = "2022/inputs/day22_test.txt"

# MAP_FIRST_LINE = 0
# MAP_LAST_LINE = 199
# PATH_LINE = 201


MAP_FIRST_LINE = 0
MAP_LAST_LINE = 11
PATH_LINE = 13


def read_path(line: str) -> list[str]:
    split = re.split(r"(\d+)", line.strip("\n"))
    split = [x for x in split if x]  # omit empty strings
    split = [int(x) if x.isnumeric() else x for x in split]

    return split


dir_to_idx = {"R": 0, "D": 1, "L": 2, "U": 3}
idx_to_dir = {idx: dir for dir, idx in dir_to_idx.items()}
dir_to_delta = {"R": (0, 1), "L": (0, -1), "U": (1, 0), "D": (-1, 0)}


def turn_left(pos: str) -> str:
    idx = dir_to_idx[pos]
    new_idx = (idx - 1) % 4

    return idx_to_dir[new_idx]


def turn_right(pos: str) -> str:
    idx = dir_to_idx[pos]
    new_idx = (idx + 1) % 4

    return idx_to_dir[new_idx]


def step(
    graph: nx.Graph, pos: tuple[int, int], dir: str, num_steps: int
) -> tuple[int, int]:
    current_position = pos
    delta = dir_to_delta[dir]
    counter = num_steps
    while counter > 0:
        next_position = (current_position[0] + delta[0], current_position[1] + delta[1])
        if next_position in nx.neighbors(graph, current_position):
            current_position = next_position
            counter -= 1
            continue
        else:
            break

    return current_position


if __name__ == "__main__":

    off_board = set()
    free_board_cells = set()
    wall_cells = set()

    NUM_LINES = MAP_LAST_LINE + 1
    NUM_COLS = -1

    line_counter = 0
    board_width = defaultdict(int)
    board_height = defaultdict(int)
    with open(INPUT_FILE, "r") as file:
        for line in file:
            if line_counter <= MAP_LAST_LINE:
                line = list(line.strip("\n"))
                NUM_COLS = max(NUM_COLS, len(line))

                for col_counter, cell in enumerate(line):
                    position = (line_counter, col_counter)
                    if cell == " ":
                        off_board.add(position)
                    elif cell == ".":
                        free_board_cells.add(position)
                        board_width[line_counter] += 1
                        board_height[col_counter] += 1
                    elif cell == "#":
                        wall_cells.add(position)
                        board_width[line_counter] += 1
                        board_height[col_counter] += 1
                    else:
                        raise UserWarning(f"Something wrong, character read {cell}")

            elif line_counter == PATH_LINE:
                path = read_path(line)

            else:
                pass

            line_counter += 1

    # form base graphs
    graph = nx.grid_2d_graph(NUM_LINES, NUM_COLS)
    board_graph = nx.subgraph(graph, free_board_cells.union(wall_cells))
    board_graph = nx.Graph(board_graph)

    print("Base", graph)
    print("Board", board_graph)
    # print(len(wall_cells), len(free_board_cells))

    # horizontal cyclical edges added
    for line_num in range(0, NUM_LINES):
        row = [node for node in board_graph if node[0] == line_num]
        min_col = min([node[1] for node in row])
        max_col = max([node[1] for node in row])
        start = (line_num, min_col)
        end = (line_num, max_col)
        assert start in board_graph and end in board_graph, "Node not in graph."
        board_graph.add_edge(start, end)

    # add vertical edges
    for col_num in range(0, NUM_COLS):
        col = [node for node in board_graph if node[1] == col_num]
        min_row = min([node[0] for node in col])
        max_row = max([node[0] for node in col])
        start = (min_row, col_num)
        end = (max_row, col_num)
        assert start in board_graph and end in board_graph, "Node not in graph."
        board_graph.add_edge(start, end)

    print("Board with cyclical", board_graph)

    # free board subgraph
    free_board_graph = nx.subgraph(board_graph, free_board_cells)

    print("Board without walls", free_board_graph)

    starting_row = 0
    starting_col = min(
        [node[1] for node in free_board_cells if node[0] == starting_row]
    )
    current_position = (starting_row, starting_col)
    current_direction = "R"

    for instruction in path:
        print(
            f"Pos {current_position} -- Dir: {current_direction} -- Instr: {instruction}"
        )
        if isinstance(instruction, int):
            current_position = step(
                free_board_graph, current_position, current_direction, instruction
            )
        elif instruction == "L":
            current_direction = turn_left(current_direction)
        elif instruction == "R":
            current_direction = turn_right(current_direction)
        else:
            raise UserWarning(f"Something wrong, instruction {instruction} not valid.")

    print(current_position)
