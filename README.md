# Advent of Code 2022

See here the official [Advent of Code 2022](https://adventofcode.com/2022) challenges.

### Setup

To use the `makefile` for setting up the daily challenge, first:

1. Create a file called `cookies` and add a single line `MYAOCSESSIONID="..."` with your session id - you can get this by inspecting the Advent of Code website.
2. Run `source cookies` to save this environment variable.

Run `make files sessionid=$MYAOCSESSIONID day=X` to get the input for day X and create code files based on the template.

### Day 4

- Interval overlap - compare endpoints.

### Day 3

- Rucksack overlap - sets and intersections.

### Day 2

- Part 1/2: rock-paper-scissors game evaluation - lookup tables.

### Day 1

- Part 1: Extract the maximum sum from a list of lists of numbers separated by new-lines and empty lines.
- Part 2: Extract the sum of the top-3 groups - using max-heaps with `heapq`.
