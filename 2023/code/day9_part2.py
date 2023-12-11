"""
--- Part Two ---

Of course, it would be nice to have even more history included in your report. Surely it's safe to just extrapolate backwards as well, right?

For each history, repeat the process of finding differences until the sequence of differences is entirely zero. Then, rather than adding a zero to the end and filling in the next values of each previous sequence, you should instead add a zero to the beginning of your sequence of zeroes, then fill in new first values for each previous sequence.

In particular, here is what the third example history looks like when extrapolating back in time:

5  10  13  16  21  30  45
  5   3   3   5   9  15
   -2   0   2   4   6
      2   2   2   2
        0   0   0

Adding the new values on the left side of each sequence from bottom to top eventually reveals the new left-most history value: 5.

Doing this for the remaining example data above results in previous values of -3 for the first history and 0 for the second history. Adding all three new values together produces 2.

Analyze your OASIS report again, this time extrapolating the previous value for each history. What is the sum of these extrapolated values?

"""
import re
import logging


logger = logging.Logger("logger", level=logging.DEBUG)
logger.addHandler(logging.StreamHandler())

INPUT_FILE = "2023/inputs/day9.txt"


if __name__ == "__main__":
    total = 0
    rows = []
    with open(INPUT_FILE, "r") as file:
        for line in file:
            line = line.strip()
            rows.append([int(num) for num in re.findall("-?[0-9]+", line)])

    assert rows[1][0] == -4

    def diff_sequence(num_list: list[int]) -> list[int]:
        return [next - previous for previous, next in zip(num_list[:-1], num_list[1:])]

    assert diff_sequence([1, 2, 3]) == [1, 1]
    assert diff_sequence([-1, 2, 6]) == [3, 4]

    total = 0
    for num_list in rows:
        diffed_list = num_list
        first_values = [
            diffed_list[0]
        ]  # could just add the last values from the diffed lists to total
        diff_count = 0
        while len(set(diffed_list)) > 1:
            diffed_list = diff_sequence(diffed_list)
            first_values.append(diffed_list[0])
            diff_count += 1

        logger.debug(f"Diff count: {diff_count} \t last values {first_values[:5]}")

        # extrapolate first
        first_values.reverse()
        current = first_values[0]
        for value in first_values[1:]:
            current = value - current

        total += current

    logger.info(f"Result {total}")
