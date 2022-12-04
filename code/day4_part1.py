import re

INPUT_FILE = "inputs/day4.txt"

total = 0
with open(INPUT_FILE, "r") as file:
    for line in file:
        low1, high1, low2, high2 = re.findall(r"\d+", line)
        low1, high1 = int(low1), int(high1)
        low2, high2 = int(low2), int(high2)

        int2_subset_int1 = (low1 <= low2) and (high2 <= high1)
        int1_subset_int2 = (low2 <= low1) and (high1 <= high2)

        if int1_subset_int2 or int2_subset_int1:
            total += 1

print(total)
