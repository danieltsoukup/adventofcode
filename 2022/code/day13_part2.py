from day13_part1 import compare_packets
from functools import cmp_to_key

INPUT_FILE = "2022/inputs/day13.txt"


def comparison_function(one, two):
    if compare_packets(one, two) is True:
        return -1

    if compare_packets(one, two) is False:
        return 1


if __name__ == "__main__":
    all_inputs = [[[2]], [[6]]]

    with open(INPUT_FILE, "r") as file:
        for line in file:
            line = line.strip()
            if line:
                all_inputs.append(eval(line))

    all_inputs = sorted(all_inputs, key=cmp_to_key(comparison_function))

    idx_one = all_inputs.index([[2]]) + 1
    idx_two = all_inputs.index([[6]]) + 1

    print(idx_one * idx_two)
