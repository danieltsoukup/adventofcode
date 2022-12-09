from utils import read_inputs

# parse inputs
INPUT_FILE = "2022/inputs/day8.txt"
inputs = read_inputs(INPUT_FILE)
inputs = [[int(num) for num in row] for row in inputs]

row_count, col_count = len(inputs), len(inputs[0])


def get_score(line: list[int]):
    """Scenic score for the last element of a list looking left."""

    assert len(line) > 0, "Line should not be empty."

    # edge
    if len(line) == 1:
        return 0
    # blocked to the left
    elif line[-2] >= line[-1]:
        return 1
    # not blocked - recursive call without the neighbour
    else:
        new_line = line[:-2] + line[-1:]
        return 1 + get_score(new_line)


def get_line_score(line: list[int], idx: int) -> int:
    """Scenic score of a point on line."""
    left_score = get_score(line[: idx + 1])
    right_score = get_score(line[idx:][::-1])

    return left_score * right_score


def get_scenic_score(inputs: list[list[int]], row_idx, col_idx) -> int:
    """Local scenic score at single point on a grid."""
    row = inputs[row_idx]
    row_score = get_line_score(row, col_idx)

    col = [inputs[i][col_idx] for i in range(row_count)]
    col_score = get_line_score(col, row_idx)

    return row_score * col_score


# find max scenic score
max_score = -1
for row_idx, row in enumerate(inputs):
    for col_idx, number in enumerate(row):
        current_score = get_scenic_score(inputs, row_idx, col_idx)
        max_score = max(max_score, current_score)

print(max_score)
