from utils import read_inputs

INPUT_FILE = "2022/inputs/day25.txt"


def pad_lists(list1: list[str], list2: list[str]) -> tuple[list[str]]:
    if len(list1) <= len(list2):
        padded_list1 = ["0"] * (len(list2) - len(list1)) + list1
        new_pair = padded_list1, list2
    else:
        padded_list2, _ = pad_lists(list2, list1)
        new_pair = list1, padded_list2

    return new_pair


SUM_TABLE = dict()

SUM_TABLE["="] = {"=": "-1", "-": "-2", "0": "=", "1": "-", "2": "0"}


SUM_TABLE["-"] = {"=": "-2", "-": "=", "0": "-", "1": "0", "2": "1"}


SUM_TABLE["0"] = {"=": "=", "-": "-", "0": "0", "1": "1", "2": "2"}

SUM_TABLE["1"] = {"=": "-", "-": "0", "0": "1", "1": "2", "2": "1="}

SUM_TABLE["2"] = {"=": "0", "-": "1", "0": "2", "1": "1=", "2": "1-"}


def recursive_snafu_add(
    list1: list[str], list2: list[str], carry_over: str = "0"
) -> list[str]:
    assert len(list1) == len(list2), "Lists should have same length."
    assert len(carry_over) == 1, "Should carry 1 digit only."

    if len(list1) == 0:
        return [carry_over] if carry_over != "0" else []
    else:
        digit1, digit2 = list1[-1], list2[-1]
        sum_of_original_digits = list(SUM_TABLE[digit1][digit2])
        if len(sum_of_original_digits) == 1:
            sum_with_carry_over = list(SUM_TABLE[sum_of_original_digits[0]][carry_over])
            last_digit = sum_with_carry_over[-1]
            new_carry_over = (
                sum_with_carry_over[0] if len(sum_with_carry_over) == 2 else "0"
            )
        else:
            new_carry_over, last_digit = recursive_snafu_add(
                sum_of_original_digits, ["0"] + [carry_over]
            )

        return recursive_snafu_add(list1[:-1], list2[:-1], new_carry_over) + [
            last_digit
        ]


if __name__ == "__main__":
    all_inputs = read_inputs(INPUT_FILE, split=True)
    result = ["0"]
    for number in all_inputs:
        result, number = pad_lists(result, number)
        result = recursive_snafu_add(result, number)

    print("".join(result))
