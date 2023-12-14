import re

INPUT_FILE = "2023/inputs/day3.txt"


if __name__ == "__main__":
    total = 0

    # collect numbers and character pos
    number_list = []
    char_pos = []
    # start location of the number
    row = 0
    col = 0
    with open(INPUT_FILE, "r") as file:
        for line in file:
            line = line.strip()
            # find the numbers
            matches = re.finditer("[0-9]+", line)
            for m in matches:
                col, num = m.start(), m.group()
                number_list.append(((row, col), int(num)))
            # find characters
            matches = re.finditer("[^0-9.]", line)
            for m in matches:
                char_pos.append((row, m.start()))

            row += 1

    # check if the number is near a character
    for (row, start_col), num in number_list:
        valid = False
        # check each character position of the number
        for i in range(len(str(num))):
            col = start_col + i
            # check each direction
            for delta1 in [-1, 0, 1]:
                for delta2 in [-1, 0, 1]:
                    if (row + delta1, col + delta2) in char_pos:
                        valid = True
                    else:
                        pass
        if valid:
            total += num

    print(number_list)
    print(char_pos)
    print(total)
