from collections import defaultdict

INPUT_FILE = "2022/inputs/day8.txt"


def visible(inputs: list[str]) -> set:
    # save the current max of each row/col
    row_cache = defaultdict(lambda: -1)
    col_cache = defaultdict(lambda: -1)

    # count visible from left/up
    total = set()
    for row_id, row in enumerate(inputs):
        for col_id, number in enumerate(row):
            number = int(number)
            is_visible = False
            # look left
            if row_cache[row_id] < number:
                is_visible = True
                row_cache[row_id] = number
            # look up
            if col_cache[col_id] < number:
                is_visible = True
                col_cache[col_id] = number

            if is_visible:
                total.add((row_id, col_id))

    return total


def solver(inputs: list[str]) -> int:
    num_rows = len(inputs)
    num_cols = len(inputs[0])

    # visible left/up
    result_lu = visible(inputs)

    # visible down/right - index inverted
    result_rd = visible([line[::-1] for line in inputs[::-1]])
    result_rd = set([(num_rows - i - 1, num_cols - j - 1) for (i, j) in result_rd])

    # put together
    result = result_lu.union(result_rd)

    return len(result)


if __name__ == "__main__":
    # read inputs
    inputs = []
    with open(INPUT_FILE, "r") as file:
        for line in file:
            line = line.strip()
            inputs.append(line)

    print(solver(inputs))
