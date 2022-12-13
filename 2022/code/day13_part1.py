INPUT_FILE = "2022/inputs/day13.txt"


def compare_packets(left, right) -> bool:
    if len(left) == 0 and len(right) > 0:
        return True
    elif len(right) == 0 and len(left) > 0:
        return False
    elif len(right) == 0 and len(left) == 0:
        return None

    # both int
    elif isinstance(left[0], int) and isinstance(right[0], int):
        if left[0] != right[0]:
            return left[0] < right[0]
        else:
            return compare_packets(left[1:], right[1:])

    # both list
    elif isinstance(left[0], list) and isinstance(right[0], list):
        sub_result = compare_packets(left[0], right[0])
        if sub_result is None:
            return compare_packets(left[1:], right[1:])
        else:
            return sub_result

    # one is a list
    elif isinstance(left[0], list) and isinstance(right[0], int):
        return compare_packets(left[0], [right[0]])

    elif isinstance(left[0], int) and isinstance(right[0], list):
        return compare_packets([left[0]], right[0])


if __name__ == "__main__":
    line_id = 0
    total = 0

    with open(INPUT_FILE, "r") as file:
        for line in file:
            if line_id % 3 == 0:
                left = eval(line.strip())

            elif line_id % 3 == 1:
                right = eval(line.strip())

                if compare_packets(left, right):
                    print(line_id // 3 + 1)
                    total += line_id // 3 + 1
                else:
                    print("not", line_id // 3 + 1)
            else:
                pass

            line_id += 1

    print(total)
