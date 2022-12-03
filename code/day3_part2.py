import string
from typing import List

letter_to_score = dict(zip(string.ascii_lowercase, range(1, 27)))
letter_to_score.update(dict(zip(string.ascii_uppercase, range(27, 53))))

total_score = 0
current_group = []
line_id = 1


def get_group_score(groups: List[str]) -> int:
    """
    Find the score for common letters in a list of strings.
    Assumes 3 groups and a single commone letter.
    """
    groups = [set(item) for item in groups]
    common_letters = list(groups[0].intersection(groups[1], groups[2]))

    return letter_to_score[common_letters[0]]


with open("inputs/day3.txt", "r") as file:
    for line in file:
        line = line.strip()

        # 1, 2 mod 3 - add to group
        if line_id % 3 in [1, 2]:
            current_group.append(line)

        # 0 mod 3 - add to group, find score and clear group
        else:
            current_group.append(line)
            total_score += get_group_score(current_group)
            current_group = []

        line_id += 1

print(total_score)
