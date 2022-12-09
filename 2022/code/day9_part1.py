INPUT_FILE = "2022/inputs/day9.txt"


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

    # adjacent - remain in-place
    if max(delta) <= 1:
        displacement = (0, 0)
    # same axis - move next-to
    elif min(delta) == 0:
        displacement = (max(0, delta[0] - 1), max(0, delta[1] - 1))
    # diagonal - cross step and move next-to
    else:
        displacement = (
            delta[0] - 1 if delta[0] > 1 else delta[0],
            delta[1] - 1 if delta[0] > 1 else delta[1],
        )

    return (tail[0] + displacement[0], tail[1] + displacement[1])


head, tail = (0, 0), (0, 0)
tail_trace = set((tail))

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
