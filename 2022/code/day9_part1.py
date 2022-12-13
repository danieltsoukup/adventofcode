from math import copysign


def move(head: tuple[int], direction: str, num_steps: int) -> tuple[int]:
    if direction == "L":
        new_head = (head[0], head[1] - num_steps)
    elif direction == "R":
        new_head = (head[0], head[1] + num_steps)
    elif direction == "U":
        new_head = (head[0] + num_steps, head[1])
    elif direction == "D":
        new_head = (head[0] - num_steps, head[1])
    else:
        raise ValueError(f"Unknown direction ({direction}).")

    return new_head


def adjust_tail(head: tuple[int], tail: tuple[int]) -> tuple[int]:
    delta = (head[0] - tail[0], head[1] - tail[1])
    abs_delta = (abs(delta[0]), abs(delta[1]))

    # adjacent - remain in-place
    if max(abs_delta) <= 1:
        displacement = (0, 0)
    # same axis - move next-to
    elif min(abs_delta) == 0:
        abs_displacement = (max(0, abs_delta[0] - 1), max(0, abs_delta[1] - 1))
        displacement = (
            copysign(abs_displacement[0], delta[0]),
            copysign(abs_displacement[1], delta[1]),
        )
    # diagonal - cross step and move next-to
    else:
        abs_displacement = (
            abs_delta[0] - 1 if abs_delta[0] > 1 else abs_delta[0],
            abs_delta[1] - 1 if abs_delta[1] > 1 else abs_delta[1],
        )

        displacement = (
            copysign(abs_displacement[0], delta[0]),
            copysign(abs_displacement[1], delta[1]),
        )

    return (int(tail[0] + displacement[0]), int(tail[1] + displacement[1]))


INPUT_FILE = "2022/inputs/day9.txt"


if __name__ == "__main__":
    head, tail = (0, 0), (0, 0)
    tail_trace = set()
    tail_trace.add(tail)  # CAREFUL: set((0, 0)) is {0}

    with open(INPUT_FILE, "r") as file:
        for line in file:
            # process line
            line = line.strip()
            direction, num_steps = line.split(" ")
            num_steps = int(num_steps)

            for _ in range(num_steps):
                head = move(head, direction, 1)
                tail = adjust_tail(head, tail)
                tail_trace.add(tail)

    print(len(tail_trace))
