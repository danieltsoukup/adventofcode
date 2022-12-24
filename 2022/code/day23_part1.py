from collections import defaultdict

INPUT_FILE = "2022/inputs/day23.txt"


def read_input_elfs(input_path: str) -> set:
    with open(input_path, "r") as file:
        elfs = set()
        row = 0
        for line in file:
            line = list(line.strip())
            for col, char in enumerate(line):
                if char == ".":
                    pass
                elif char == "#":
                    elfs.add((row, col))
            row -= 1

    return elfs


def check_north_blocked(elfs: set[tuple[int, int]], elf: tuple[int, int]) -> bool:
    moved = set()
    moved.add((elf[0], elf[1] + 1))
    moved.add((elf[0] + 1, elf[1] + 1))
    moved.add((elf[0] - 1, elf[1] + 1))

    return len(elfs.intersection(moved)) > 0


def check_south_blocked(elfs: set[tuple[int, int]], elf: tuple[int, int]) -> bool:
    moved = set()
    moved.add((elf[0], elf[1] - 1))
    moved.add((elf[0] + 1, elf[1] - 1))
    moved.add((elf[0] - 1, elf[1] - 1))

    return len(elfs.intersection(moved)) > 0


def check_west_blocked(elfs: set[tuple[int, int]], elf: tuple[int, int]) -> bool:
    moved = set()
    moved.add((elf[0] - 1, elf[1]))
    moved.add((elf[0] - 1, elf[1] - 1))
    moved.add((elf[0] - 1, elf[1] + 1))

    return len(elfs.intersection(moved)) > 0


def check_east_blocked(elfs: set[tuple[int, int]], elf: tuple[int, int]) -> bool:
    moved = set()
    moved.add((elf[0] + 1, elf[1]))
    moved.add((elf[0] + 1, elf[1] - 1))
    moved.add((elf[0] + 1, elf[1] + 1))

    return len(elfs.intersection(moved)) > 0


def is_direction_blocked(
    elfs: set[tuple[int, int]], elf: tuple[int, int], direction: str
) -> bool:
    if direction == "N":
        return check_north_blocked(elfs, elf)
    elif direction == "S":
        return check_south_blocked(elfs, elf)
    elif direction == "W":
        return check_west_blocked(elfs, elf)
    elif direction == "E":
        return check_east_blocked(elfs, elf)


def direction_to_location(elf: tuple[int, int], direction: str) -> tuple[int, int]:
    if direction == "N":
        return (elf[0], elf[1] + 1)
    elif direction == "S":
        return (elf[0], elf[1] - 1)
    elif direction == "W":
        return (elf[0] - 1, elf[1])
    elif direction == "E":
        return (elf[0] + 1, elf[1])


def propose_move(
    elfs: set[tuple[int, int]], order: list[str]
) -> dict[tuple[int, int], tuple[int, int]]:
    proposal = dict()
    for elf in elfs:
        proposal[elf] = elf  # default is to stay put
        for direction in order:
            if is_direction_blocked(elfs, elf, direction):
                continue  # check next dir
            else:
                proposal[elf] = direction_to_location(elf, direction)
                break  # go to next elf

    return proposal


def filter_moves(
    proposal: dict[tuple[int, int], tuple[int, int]]
) -> dict[tuple[int, int], tuple[int, int]]:
    counter = defaultdict(int)
    for _, new_loc in proposal.items():
        counter[new_loc] += 1

    new_proposal = dict()
    for elf, new_loc in proposal.items():
        if counter[new_loc] == 1:  # only unique locations are used
            new_proposal[elf] = new_loc
        else:
            new_proposal[elf] = elf

    return new_proposal


def move_elfs(
    elfs: set[tuple[int, int]], proposal: dict[tuple[int, int], tuple[int, int]]
) -> set[tuple[int, int]]:
    return set([proposal[elf] for elf in elfs])


def update_order(order: list[str]) -> list[str]:
    return order[1:] + order[:1]


def get_rectangle_size(elfs: set[tuple[int, int]]) -> int:
    rows = [elf[0] for elf in elfs]
    height = max(rows) - min(rows) + 1
    cols = [elf[1] for elf in elfs]
    width = max(cols) - min(cols) + 1

    return height * width


if __name__ == "__main__":
    ROUNDS = 10

    elfs = read_input_elfs(INPUT_FILE)
    order = ["N", "S", "W", "E"]

    for _ in range(ROUNDS):
        move_proposal = propose_move(elfs, order)
        move_proposal = filter_moves(move_proposal)
        elfs = move_elfs(elfs, move_proposal)
        order = update_order(order)

        print(get_rectangle_size(elfs) - len(elfs))
