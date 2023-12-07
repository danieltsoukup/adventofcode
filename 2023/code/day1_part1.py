import re

INPUT_FILE = "2023/inputs/day1.txt"

if __name__ == "__main__":
    total = 0
    with open(INPUT_FILE, "r") as file:
        for line in file:
            line = line.strip()

            line = re.sub(r"[a-z]", "", line)
            if len(line) > 1:
                total += int(line[0] + line[-1])
            else:
                total += int(line[0] + line[0])

    print(total)
