from day13_part1 import compare_packets
from ast import literal_eval

INPUT_FILE = "2022/inputs/day13.txt"

if __name__ == "__main__":
    all_inputs = [[[2]], [[6]]]

    with open(INPUT_FILE, "r") as file:
        for line in file:
            line = line.strip()
            if line:
                all_inputs.append(literal_eval(line))

    one = 300 - sum([compare_packets([[2]], other) for other in all_inputs[2:]]) + 1
    two = 300 - sum([compare_packets([[6]], other) for other in all_inputs[2:]]) + 2

    print(one * two)
