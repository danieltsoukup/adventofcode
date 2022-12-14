INPUT_FILE = "2022/inputs/day13.txt"


def compare_packets(left: list, right: list) -> bool:
    #  at least one empty
    if len(left) == 0 and len(right) > 0:
        return True

    if len(right) == 0 and len(left) > 0:
        return False

    if len(right) == 0 and len(left) == 0:
        return None

    # both int
    if isinstance(left[0], int) and isinstance(right[0], int):
        if left[0] != right[0]:
            return left[0] < right[0]
        else:
            return compare_packets(left[1:], right[1:])

    # one is a list - add bracket and retry
    if isinstance(left[0], list) and isinstance(right[0], int):
        new_right = right.copy()
        new_right[0] = [new_right[0]]

        return compare_packets(left, new_right)

    if isinstance(left[0], int) and isinstance(right[0], list):
        new_left = left.copy()
        new_left[0] = [new_left[0]]

        return compare_packets(new_left, right)

    # both list
    if isinstance(left[0], list) and isinstance(right[0], list):
        # recursive call
        sub_result = compare_packets(left[0], right[0])
        # recursive unsuccessful in comparison - move on with the rest of the list
        if sub_result is None:
            return compare_packets(left[1:], right[1:])
        # recursive call successful
        else:
            return sub_result


if __name__ == "__main__":
    line_id = 0
    total = 0
    decisions = []
    with open(INPUT_FILE, "r") as file:
        for line in file:
            if line_id % 3 == 0:
                left = eval(line.strip())

            elif line_id % 3 == 1:
                right = eval(line.strip())

                decision = compare_packets(left, right)
                decisions.append(decision)

                if decision:
                    print("----------", line_id // 3 + 1)
                    total += line_id // 3 + 1
                else:
                    print("not", line_id // 3 + 1)
            else:
                pass

            line_id += 1

    print(total, sum(decisions), sum([not i for i in decisions]))
