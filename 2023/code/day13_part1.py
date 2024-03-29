import re
import math
import logging
import time

"""
--- Day 13: Point of Incidence ---

With your help, the hot springs team locates an appropriate spring which launches you neatly and precisely up to the edge of Lava Island.

There's just one problem: you don't see any lava.

You do see a lot of ash and igneous rock; there are even what look like gray mountains scattered around. After a while, you make your way to a nearby cluster of mountains only to discover that the valley between them is completely full of large mirrors. Most of the mirrors seem to be aligned in a consistent way; perhaps you should head in that direction?

As you move through the valley of mirrors, you find that several of them have fallen from the large metal frames keeping them in place. The mirrors are extremely flat and shiny, and many of the fallen mirrors have lodged into the ash at strange angles. Because the terrain is all one color, it's hard to tell where it's safe to walk or where you're about to run into a mirror.

You note down the patterns of ash (.) and rocks (#) that you see as you walk (your puzzle input); perhaps by carefully analyzing these patterns, you can figure out where the mirrors are!

For example:

#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#

To find the reflection in each pattern, you need to find a perfect reflection across either a horizontal line between two rows or across a vertical line between two columns.

In the first pattern, the reflection is across a vertical line between two columns; arrows on each of the two columns point at the line between the columns:

123456789
    ><
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.
    ><
123456789

In this pattern, the line of reflection is the vertical line between columns 5 and 6. Because the vertical line is not perfectly in the middle of the pattern, part of the pattern (column 1) has nowhere to reflect onto and can be ignored; every other column has a reflected column within the pattern and must match exactly: column 2 matches column 9, column 3 matches 8, 4 matches 7, and 5 matches 6.

The second pattern reflects across a horizontal line instead:

1 #...##..# 1
2 #....#..# 2
3 ..##..### 3
4v#####.##.v4
5^#####.##.^5
6 ..##..### 6
7 #....#..# 7

This pattern reflects across the horizontal line between rows 4 and 5. Row 1 would reflect with a hypothetical row 8, but since that's not in the pattern, row 1 doesn't need to match anything. The remaining rows match: row 2 matches row 7, row 3 matches row 6, and row 4 matches row 5.

To summarize your pattern notes, add up the number of columns to the left of each vertical line of reflection; to that, also add 100 multiplied by the number of rows above each horizontal line of reflection. In the above example, the first pattern's vertical line has 5 columns to its left and the second pattern's horizontal line has 4 rows above it, a total of 405.

Find the line of reflection in each of the patterns in your notes. What number do you get after summarizing all of your notes?

"""

INPUT_FILE = "2023/inputs/day13.txt"


start_time = time.time()

logger = logging.Logger("logger", level=logging.DEBUG)
logger.addHandler(logging.StreamHandler())


def col_symmetry(block: list[str], idx: int) -> bool:
    """
    Find if there is a column symmetry at the given index.
    """
    full_length = len(block[0])
    length = min(idx, full_length - idx)
    prefix = "".join([line[idx - length : idx] for line in block])
    suffix = "".join([line[idx : idx + length][::-1] for line in block])

    return hash(prefix) == hash(suffix)


def transpose_block(block: list[str]) -> list[str]:
    new_block = ["" for _ in range(len(block[0]))]
    for line in block:
        new_block = [prefix + char for prefix, char in zip(new_block, line)]

    return new_block


if __name__ == "__main__":
    total = []
    blocks = []
    row = 0
    with open(INPUT_FILE, "r") as file:
        new_block = []
        for line in file:
            line = line.strip()
            if line != "":
                new_block.append(line)
            else:
                # column symmetry
                column_indices = [
                    idx
                    for idx in range(1, len(new_block[0]))
                    if col_symmetry(new_block, idx)
                ]
                if column_indices:
                    result = column_indices.pop()
                    total.append((result, "col"))
                else:
                    # row symmetry
                    new_block = transpose_block(new_block)
                    column_indices = [
                        idx
                        for idx in range(1, len(new_block[0]))
                        if col_symmetry(new_block, idx)
                    ]
                    result = column_indices.pop()
                    total.append((result, "row"))

                logger.debug(f"Symmetry: {result}")

                new_block = []

            row += 1

    summary = sum([num for num, type_ in total if type_ == "col"])
    summary += sum([100 * num for num, type_ in total if type_ == "row"])

    logger.info(f">> Total {summary}")

    end_time = time.time()
    logger.info(f">> Elapsed time: {round(end_time - start_time, 2)} sec.")
