INPUT_FILE = "2022/inputs/day10.txt"

NUM_ROWS = 6
NUM_COLS = 40


def render_crt(crt: list[list[str]]) -> None:
    rows = [" ".join(row) for row in crt]
    result = "\n".join(rows)

    print(result)


def cycle_to_position(cycle: int) -> tuple[int, int]:
    row = (cycle - 1) // NUM_COLS
    col = (cycle - 1) % NUM_COLS

    return row, col


def crt_cycle_update(
    crt: list[list[str]], cycle: int, X: int
) -> tuple[list[list[str]], int]:
    row, col = cycle_to_position(cycle)
    if abs(col - X) <= 1:
        crt[row][col] = "#"

    return crt, cycle + 1


if __name__ == "__main__":
    crt = [["." for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]
    X = 1
    cycle = 1

    with open(INPUT_FILE, "r") as file:
        for line in file:
            line = line.strip()
            if line == "noop":
                crt, cycle = crt_cycle_update(crt, cycle, X)
            else:
                for _ in range(2):
                    crt, cycle = crt_cycle_update(crt, cycle, X)

                delta = line.split(" ")[1]
                delta = int(delta)
                X += delta

    render_crt(crt)
