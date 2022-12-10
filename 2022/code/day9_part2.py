from utils import move, adjust_tail

INPUT_FILE = "2022/inputs/day9.txt"


class Rope:
    ROPE_LENGTH = 10

    def __init__(self):
        self.points = [(0, 0)] * self.ROPE_LENGTH

    @property
    def head(self):
        return self.points[0]

    @head.setter
    def head(self, new_head):
        self.points[0] = new_head

    @property
    def tail(self):
        return self.points[-1]


if __name__ == "__main__":
    rope = Rope()
    tail_trace = set()
    tail_trace.add(rope.tail)  # CAREFUL: set((0, 0)) is {0}

    with open(INPUT_FILE, "r") as file:
        for line in file:
            # process line
            line = line.strip()
            direction, num_steps = line.split(" ")
            num_steps = int(num_steps)

            for _ in range(num_steps):
                # move head
                rope.head = move(rope.head, direction, 1)
                # adjust the rest of the rope
                for i in range(1, len(rope.points)):
                    rope.points[i] = adjust_tail(rope.points[i - 1], rope.points[i])

                tail_trace.add(rope.tail)

    print(len(tail_trace))
