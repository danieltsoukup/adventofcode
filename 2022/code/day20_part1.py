INPUT_FILE = "2022/inputs/day20.txt"


if __name__ == "__main__":
    all_inputs = []
    index = 0
    with open(INPUT_FILE, "r") as file:
        for line in file:
            all_inputs.append((index, int(line.strip())))
            index += 1

    print(all_inputs)
