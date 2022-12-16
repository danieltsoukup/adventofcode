import re
from day15_part1 import find_overlap_interval, manhattan_distance, interval_union_size
from functools import reduce

INPUT_FILE = "2022/inputs/day15.txt"


if __name__ == "__main__":
    x_min, x_max = 0, 4000000
    y_min, y_max = 0, 4000000

    # read all sensors and beacons
    sensors, beacons, distances = [], [], []
    with open(INPUT_FILE, "r") as file:
        for line in file:
            line.strip()
            tuples = re.findall(r"x=(-?\d+), y=(-?\d+)", line)
            sensor, beacon = [(int(x), int(y)) for x, y in tuples]
            sensors.append(sensor)
            beacons.append(beacon)
            distances.append(manhattan_distance(sensor, beacon))

    for y in range(0, y_max + 1):
        # overlap at y
        overlaps = [
            find_overlap_interval(sensor, distance, y)
            for sensor, distance in zip(sensors, distances)
        ]
        overlaps = [interval for interval in overlaps if interval is not None]
        # limit to x range
        overlaps = [(max(x_min, low), min(x_max, high)) for low, high in overlaps]

        # union
        size = interval_union_size(overlaps)

        if size < x_max - x_min + 1:
            print("y:", y, "size", size)
            break

        # timer
        if y % 100000 == 0:
            print(f"Done {y}...")

    # getting x
    overlap_set = reduce(
        lambda x, y: x.union(y), [set(range(low, high + 1)) for low, high in overlaps]
    )
    uncovered = set(range(x_min, x_max + 1)).difference(set(overlap_set))

    print(list(uncovered))

    # freq
    freq = 4000000 * list(uncovered)[0] + y
    print("freq", freq)
