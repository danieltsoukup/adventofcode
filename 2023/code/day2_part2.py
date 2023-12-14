import re

INPUT_FILE = "2023/inputs/day2.txt"

RED = 12
GREEN = 13
BLUE = 14


def get_color_count(text: str, color: str) -> int:
    results = re.findall(f"([0-9]+) {color}", text)
    number_string = 0
    if len(results) > 0:
        number_string = results[0]

    return int(number_string)


if __name__ == "__main__":
    total = 0
    tracker = dict()

    with open(INPUT_FILE, "r") as file:
        for line in file:
            line = line.strip()
            game_text, numbers_text = line.split(":")
            game_id = re.findall(r"[0-9]+", game_text)[0]
            numbers_text_split = numbers_text.split(";")

            tracker[game_id] = []
            possible = True

            max_dict = {"red": 0, "green": 0, "blue": 0}

            for text in numbers_text_split:
                game_dict = dict()
                for color in ["red", "green", "blue"]:
                    game_dict[color] = get_color_count(text, color)

                for color in max_dict:
                    max_dict[color] = max(max_dict[color], game_dict[color])

                tracker[game_id].append(game_dict)

            # all possible
            if possible:
                total += max_dict["red"] * max_dict["blue"] * max_dict["green"]

    print(total)
