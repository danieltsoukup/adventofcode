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

            for text in numbers_text_split:
                game_dict = dict()
                for color in ["red", "green", "blue"]:
                    game_dict[color] = get_color_count(text, color)

                tracker[game_id].append(game_dict)

                CHECK_NUM = 2**RED * 3**GREEN * 5**BLUE
                GAME_NUM = (
                    2 ** game_dict["red"]
                    * 3 ** game_dict["green"]
                    * 5 ** game_dict["blue"]
                )

                # check if this game is not possible  -> move to next
                if CHECK_NUM % GAME_NUM != 0:
                    possible = False

            # all possible
            if possible:
                print("adding", game_id)
                total += int(game_id)

    print(total)
