import re
import networkx as nx
from itertools import product

VERBOSE = False
TEST = False

if TEST:
    INPUT_FILE = "2022/inputs/day22_test.txt"
    MAP_FIRST_LINE = 0
    MAP_LAST_LINE = 11
    PATH_LINE = 13
else:
    INPUT_FILE = "2022/inputs/day22.txt"
    MAP_FIRST_LINE = 0
    MAP_LAST_LINE = 199
    PATH_LINE = 201


def read_path(line: str) -> list[str]:
    split = re.split(r"(\d+)", line.strip("\n"))
    split = [x for x in split if x]  # omit empty strings
    split = [int(x) if x.isnumeric() else x for x in split]

    return split


dir_to_idx = {"R": 0, "D": 1, "L": 2, "U": 3}
idx_to_dir = {idx: dir for dir, idx in dir_to_idx.items()}
dir_to_delta = {"R": (0, 1), "L": (0, -1), "U": (-1, 0), "D": (1, 0)}

dir_to_angle = {"R": 90, "D": 180, "L": 270, "U": 0}
angle_to_dir = {angle: dir for dir, angle in dir_to_angle.items()}


def turn_angle(start_angle: int, delta: int) -> int:
    return (start_angle + delta) % 360


def turn_left(pos: str) -> str:
    idx = dir_to_idx[pos]
    new_idx = (idx - 1) % 4

    return idx_to_dir[new_idx]


def turn_right(pos: str) -> str:
    idx = dir_to_idx[pos]
    new_idx = (idx + 1) % 4

    return idx_to_dir[new_idx]


def step(
    graph: nx.Graph, current_pos: tuple[int, int], current_dir: str, num_steps: int
) -> tuple[tuple[int, int], str]:
    new_pos = current_pos
    new_dir = current_dir
    counter = num_steps
    while counter > 0:
        # get next pos by dir pointer
        next_position = graph.nodes[new_pos][current_dir]
        if next_position in nx.neighbors(graph, new_pos):
            # update direction: TODO
            direction_mapper = graph.edges[new_pos, next_position]["direction_mapper"]
            new_dir = direction_mapper(current_dir)
            new_pos = next_position
            counter -= 1
            continue
        else:
            break

    return new_pos, new_dir


def read_board():
    off_board = set()
    free_board_cells = set()
    wall_cells = set()

    NUM_LINES = MAP_LAST_LINE + 1
    NUM_COLS = -1

    line_counter = 0
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
                    elif cell == "#":
                        wall_cells.add(position)
                    else:
                        raise UserWarning(f"Something wrong, character read {cell}")

            elif line_counter == PATH_LINE:
                path = read_path(line)

            else:
                pass

            line_counter += 1

    return free_board_cells, wall_cells, NUM_LINES, NUM_COLS, path


def build_free_board_graph():
    free_board_cells, wall_cells, NUM_LINES, NUM_COLS, path = read_board()

    # form base graphs
    graph = nx.grid_2d_graph(NUM_LINES, NUM_COLS)

    # add pointers to neighbours
    for node in graph:
        for dir, delta in dir_to_delta.items():
            new_point = (node[0] + delta[0], node[1] + delta[1])
            if new_point in graph:
                graph.nodes[node][dir] = new_point

    board_graph = nx.subgraph(graph, free_board_cells.union(wall_cells))
    board_graph = nx.Graph(board_graph)

    print("Base", graph)
    print("Board", board_graph)

    #################
    # CUBE WRAPPING #
    #################

    # default mapping - identity
    nx.set_edge_attributes(board_graph, values=lambda x: x, name="direction_mapper")

    # S1 - S4
    S1_row = 0
    for S1_col in range(100, 150):
        # match nodes
        S4_row = 199
        S4_col = S1_col - 100  # map to 0-49
        start = (S1_row, S1_col)
        end = (S4_row, S4_col)
        # add direction change
        board_graph.add_edge(
            start, end, direction_mapper=lambda dir: dir
        )  # dir stays the same
        # add move reference
        board_graph.nodes[start]["U"] = end
        board_graph.nodes[end]["D"] = start

    print("Board with cyclical", board_graph)

    # S1 - S2
    S1_row = 49
    for S1_col in range(100, 150):
        S2_col = 99
        S2_row = S1_col - 50  # 50-99
        start = (S1_row, S1_col)
        end = (S2_row, S2_col)
        # add direction change
        board_graph.add_edge(
            start, end, direction_mapper=lambda dir: "L" if dir == "D" else "U"
        )  # down to left, right to up
        # add move reference
        board_graph.nodes[start]["D"] = end
        board_graph.nodes[end]["R"] = start

    print("Board with cyclical", board_graph)

    # S1 - B
    S1_col = 149
    for S1_row in range(0, 50):
        B_col = 99
        B_row = 149 - S1_row  # 149 -> 100
        start = (S1_row, S1_col)
        end = (B_row, B_col)
        board_graph.add_edge(
            start, end, direction_mapper=lambda _: "L"
        )  # always left after passing
        board_graph.nodes[start]["R"] = end
        board_graph.nodes[end]["R"] = start

    print("Board with cyclical", board_graph)

    # T - S4
    T_row = 0
    for T_col in range(50, 100):
        S4_col = 0
        S4_row = T_col + 100  # 150 -> 199
        start = (T_row, T_col)
        end = (S4_row, S4_col)
        board_graph.add_edge(
            start, end, direction_mapper=lambda dir: "R" if dir == "U" else "D"
        )  # up to right, left to down
        board_graph.nodes[start]["U"] = end
        board_graph.nodes[end]["L"] = start

    print("Board with cyclical", board_graph)

    # T - S3
    T_col = 50
    for T_row in range(0, 50):
        S3_col = 0
        S3_row = 149 - T_row  # 149 -> 100
        start = (T_row, T_col)
        end = (S3_row, S3_col)
        board_graph.add_edge(
            start, end, direction_mapper=lambda _: "R"
        )  # left to right
        board_graph.nodes[start]["L"] = end
        board_graph.nodes[end]["L"] = start

    print("Board with cyclical", board_graph)

    # free board subgraph
    free_board_graph = board_graph.subgraph(free_board_cells)

    return free_board_graph, free_board_cells, path


if __name__ == "__main__":
    free_board_graph, free_board_cells, path = build_free_board_graph()

    print("Board without walls", free_board_graph)
    print(list(list(free_board_graph.edges(data=True))[0][-1].keys()))

    starting_row = 0
    starting_col = min(
        [node[1] for node in free_board_cells if node[0] == starting_row]
    )
    current_position = (starting_row, starting_col)
    current_direction = "R"

    for i, instruction in enumerate(path):
        if VERBOSE:
            print(
                f"Step {i} -- Pos {current_position} -- Dir: {current_direction} -- Instr: {instruction}"
            )
        if isinstance(instruction, int):
            current_position, current_direction = step(
                free_board_graph, current_position, current_direction, instruction
            )
        elif instruction == "L":
            current_direction = turn_left(current_direction)
        elif instruction == "R":
            current_direction = turn_right(current_direction)
        else:
            raise UserWarning(f"Something wrong, instruction {instruction} not valid.")

    result = (
        1000 * (current_position[0] + 1)
        + 4 * (current_position[1] + 1)
        + dir_to_idx[current_direction]
    )

    print(result)
