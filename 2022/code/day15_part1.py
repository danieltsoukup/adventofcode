import re

INPUT_FILE = "2022/inputs/day15.txt"


def manhattan_distance(point1: tuple[int, int], point2: tuple[int, int]) -> int:
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])


def find_overlap_interval(
    point: tuple[int, int], distance: int, height: int
) -> tuple[int, int]:
    height_delta = abs(point[1] - height)
    if height_delta > distance:
        overlap = None
    else:
        slack = distance - height_delta
        overlap = (point[0] - slack, point[0] + slack)

    return overlap


def interval_union_size(intervals: set[tuple[int, int]]) -> int:
    end_points = [(start, "S") for start, _ in intervals] + [
        (end, "E") for _, end in intervals
    ]
    sorted_end_points = sorted(end_points, key=lambda pair: pair[0])
    start_counter = 0
    last_loc = None
    total = 0
    for loc, type_ in sorted_end_points:
        if last_loc is not None and start_counter > 0:
            total += loc - last_loc
        last_loc = loc

        if type_ == "S":
            start_counter += 1
            if start_counter == 1:
                total += 1
        else:
            start_counter -= 1

    return total


if __name__ == "__main__":
    y = 2000000
    overlaps = []
    beacon_at_height = set()
    with open(INPUT_FILE, "r") as file:
        for line in file:
            # parse input
            line.strip()
            tuples = re.findall(r"x=(-?\d+), y=(-?\d+)", line)
            sensor, beacon = [(int(x), int(y)) for x, y in tuples]

            if beacon[1] == y:
                beacon_at_height.add(beacon[0])

            # find overlap
            distance = manhattan_distance(sensor, beacon)
            interval = find_overlap_interval(sensor, distance, y)
            if interval is not None:
                overlaps.append(interval)

    print(interval_union_size(overlaps) - len(beacon_at_height))
