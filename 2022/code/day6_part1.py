INPUT_FILE = "2022/inputs/day6.txt"

NUM_UNIQUE = 4

with open(INPUT_FILE, "r") as file:
    for line in file:
        line = line.strip()
        for idx in range(NUM_UNIQUE, len(line) - 1):
            if len(set(line[idx - NUM_UNIQUE : idx])) == NUM_UNIQUE:
                break
        break

print(idx)
