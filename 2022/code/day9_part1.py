from utils import move, adjust_tail


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
