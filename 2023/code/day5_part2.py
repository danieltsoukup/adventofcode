"""
--- Part Two ---

Everyone will starve if you only plant such a small number of seeds. Re-reading the almanac, it looks like the seeds: line actually describes ranges of seed numbers.

The values on the initial seeds: line come in pairs. Within each pair, the first value is the start of the range and the second value is the length of the range. So, in the first line of the example above:

seeds: 79 14 55 13

This line describes two ranges of seed numbers to be planted in the garden. The first range starts with seed number 79 and contains 14 values: 79, 80, ..., 91, 92. The second range starts with seed number 55 and contains 13 values: 55, 56, ..., 66, 67.

Now, rather than considering four seed numbers, you need to consider a total of 27 seed numbers.

In the above example, the lowest location number can be obtained from seed number 82, which corresponds to soil 84, fertilizer 84, water 84, light 77, temperature 45, humidity 46, and location 46. So, the lowest location number is 46.

Consider all of the initial seed numbers listed in the ranges on the first line of the almanac. What is the lowest location number that corresponds to any of the initial seed numbers?

"""

import re
from collections import defaultdict
import math
import logging
import tqdm
from typing import List, Tuple

logger = logging.Logger("logger", level=logging.INFO)
logger.addHandler(logging.StreamHandler())

INPUT_FILE = "2023/inputs/day5.txt"


class Interval(object):
    """
    Single interval object representing the [start, start+length) half-open interval.
    """

    def __init__(self, start: int, length: int) -> None:
        self.start = start
        self.length = length


int1 = Interval(1, 3)
int2 = Interval(3, 3)


def find_index_of_largest_before(sorted_numbers: List[int], value: int) -> int:
    """
    Find the index of the largest element in numbers that is still at most value.
    Numbers is assumed to be SORTED.
    """
    n = len(sorted_numbers)
    if n == 1:
        if sorted_numbers[0] <= value:
            return 0
        else:
            return -1
    else:
        mid_point = n // 2
        if value < sorted_numbers[mid_point]:
            return find_index_of_largest_before(sorted_numbers[:mid_point], value)
        else:
            return mid_point + find_index_of_largest_before(
                sorted_numbers[mid_point:], value
            )


# testing
assert find_index_of_largest_before([1, 2, 5, 8], 0) == -1
assert find_index_of_largest_before([1, 2, 5, 8], 1) == 0
assert find_index_of_largest_before([1, 2, 5, 8], 6) == 2
assert find_index_of_largest_before([1, 2, 5, 8], 9) == 3


class SortedIntervalCollection(object):
    """
    A collection of intervals sorted by start point.
    """

    def __init__(self, intervals: List[Interval]) -> None:
        self.intervals = intervals
        self._sort()

    def _sort(self) -> None:
        self.intervals.sort(key=lambda interval: interval.start)

    def insert(self, new_interval: Interval) -> None:
        """
        Add new interval to the collection, preserving the sorted order.
        """
        if len(self.intervals) == 0:
            self.intervals.append(new_interval)
        else:
            # find new location
            start_points = [interval.start for interval in self.intervals]
            index = find_index_of_largest_before(start_points, new_interval.start)

            # the insert method puts new element before the index so add 1 to account for index=-1
            self.intervals.insert(index + 1, new_interval)

    def min(self) -> int:
        """
        Find the minimum of the interval collection.
        """
        return self.intervals[0].start

    def __iter__(self):
        yield from self.intervals


# check pre-sort
collection = SortedIntervalCollection([int2, int1])
assert collection.intervals[0] == int1

# try insert
int3 = Interval(2, 1)
collection.insert(int3)
assert collection.intervals[1] == int3

# try loop
assert [interval.start for interval in collection] == [1, 2, 3]


class MapTriple(object):
    def __init__(self, destination: int, source: int, length: int) -> None:
        self.destination = destination
        self.source = source
        self.length = length


class IntervalMapper(object):
    """
    Object to map one interval collection to another.
    """

    def __init__(self, mapper: List[MapTriple]) -> None:
        """
        Tuples represenent (destination-start, source-start, length)
        """
        self.mappers = mapper
        self._sort()

    def _sort(self) -> None:
        """
        Sort mapper by the source.
        """
        self.mappers.sort(key=lambda triple: triple.source)

    def map(self, int_collection: SortedIntervalCollection) -> SortedIntervalCollection:
        mapped_intervals: List[Interval] = []
        for interval in int_collection:
            for mapped_interval in self._map_interval(interval):
                mapped_intervals.append(mapped_interval)

        return SortedIntervalCollection(mapped_intervals)

    def _map_interval(self, interval: Interval) -> List[Interval]:
        if interval.length == 0:
            return []
        else:
            # index of relevant map triple
            index = find_index_of_largest_before(
                [triple.source for triple in self.mappers], interval.start
            )
            if index == -1:
                # find initial segment that stays in place, and make recursive call for the rest
                end_of_initial = min(
                    self.mappers[0].source, interval.start + interval.length
                )
                initial_segment = Interval(
                    interval.start, end_of_initial - interval.start
                )
                end_segment = Interval(
                    end_of_initial, interval.length - initial_segment.length
                )

                return [initial_segment] + self._map_interval(end_segment)

            else:
                map_triple = self.mappers[index]
                end_of_map_interval = map_triple.source + map_triple.length
                if interval.start < end_of_map_interval:
                    # if start of the interval is in the mapper interval then map initial segment and make recursive call
                    end_of_initial = min(
                        end_of_map_interval, interval.start + interval.length
                    )
                    initial_segment = Interval(
                        interval.start, end_of_initial - interval.start
                    )
                    end_segment = Interval(
                        end_of_initial, interval.length - initial_segment.length
                    )

                    # map the initial segment
                    delta = map_triple.destination - map_triple.source
                    mapped_initial = Interval(
                        initial_segment.start + delta, initial_segment.length
                    )
                    return [mapped_initial] + self._map_interval(end_segment)
                else:
                    # if start of the interval is past the mapper interval then whole interval stays in place
                    return [interval]


int1 = Interval(1, 4)
collection = SortedIntervalCollection([int1])
mapper = IntervalMapper([MapTriple(10, 0, 4)])
mapped_collection = mapper.map(collection)
assert mapped_collection.intervals[0].start == 4
assert mapped_collection.intervals[1].start == 11

if __name__ == "__main__":
    result = math.inf
    mappers = defaultdict(list)
    map_name = None
    seeds = []

    with open(INPUT_FILE, "r") as file:
        for line in file:
            line = line.strip()
            if line.startswith("seeds"):
                seeds = re.findall("[0-9]+", line)
                seeds = [int(num) for num in seeds]
            elif "map" in line:
                map_name = re.findall("([a-z]+)-to-([a-z]+)", line)[0]
            elif line == "":
                pass
            elif line[0].isdigit():
                dest_start, source_start, length = re.findall("[0-9]+", line)
                mappers[map_name].append(
                    MapTriple(int(dest_start), int(source_start), int(length))
                )

    map_collection = dict()
    for map_name in mappers:
        map_collection[map_name] = IntervalMapper(mappers[map_name])

    # take each seed range
    seed_collection = []
    for start, length in zip(seeds[::2], seeds[1::2]):
        seed_collection.append(Interval(start, length))

    collection = SortedIntervalCollection(seed_collection)

    for map_name, mapper in map_collection.items():
        collection = mapper.map(collection)
        logger.info(f"Done with {map_name}...")

    logger.info(f"Minimum: {collection.min()}")
