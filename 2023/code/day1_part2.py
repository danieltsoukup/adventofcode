import re

INPUT_FILE = "2023/inputs/day1.txt"


if __name__ == "__main__":
    total = 0
    with open(INPUT_FILE, "r") as file:
        for line in file:
            line = line.strip()

            text_to_digit = {
                "one": 1,
                "two": 2,
                "three": 3,
                "four": 4,
                "five": 5,
                "six": 6,
                "seven": 7,
                "eight": 8,
                "nine": 9,
                "zero": 0,
            }

            all_number_strings = list(text_to_digit.keys()) + [
                str(dig) for dig in range(10)
            ]

            def find_first(line: str) -> int:
                for digit in all_number_strings:
                    if line[: len(digit)] == digit:
                        if len(digit) == 1:
                            return int(digit)
                        else:
                            return text_to_digit[digit]

                return find_first(line[1:])

            def find_last(line: str) -> int:
                for digit in all_number_strings:
                    if line[-len(digit) :] == digit:
                        if len(digit) == 1:
                            return int(digit)
                        else:
                            return text_to_digit[digit]

                return find_last(line[:-1])

            total += find_first(line) * 10 + find_last(line)

        print(total)
