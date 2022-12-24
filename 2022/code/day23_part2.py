from day23_part1 import (
    read_input_elfs,
    propose_move,
    filter_moves,
    update_order,
)

INPUT_FILE = "2022/inputs/day23.txt"


def move_elfs(
    elfs: set[tuple[int, int]], proposal: dict[tuple[int, int], tuple[int, int]]
) -> tuple[set[tuple[int, int]], int]:
    new_elfs = set()
    move_counter = 0
    for elf in elfs:
        new_elfs.add(proposal[elf])
        move_counter += int(elf != proposal[elf])

    return new_elfs, move_counter


if __name__ == "__main__":
    elfs = read_input_elfs(INPUT_FILE)
    order = ["N", "S", "W", "E"]
    counter = 1
    round = 1

    while counter > 0:
        move_proposal = propose_move(elfs, order)
        move_proposal = filter_moves(move_proposal)
        elfs, counter = move_elfs(elfs, move_proposal)
        order = update_order(order)
        round += 1

    print(round - 1)
