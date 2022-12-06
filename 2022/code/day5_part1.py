import re

INPUT_FILE = "inputs/day5.txt"

NUM_STACKS = 9
STACK_WIDTH = 4
STACK_LAST_LINE = 8
INSTRUCTION_START_LINE = 11

stacks = {i: [] for i in range(1, NUM_STACKS + 1)}
line_number = 1
with open(INPUT_FILE, "r") as file:
    for line in file:
        line = line.strip("\n")

        # read starting stacks
        if line_number <= STACK_LAST_LINE:
            for i in range(NUM_STACKS):
                start_idx = i * STACK_WIDTH + 1
                end_idx = i * STACK_WIDTH + 2
                current_crate = line[start_idx:end_idx]
                if current_crate.strip():
                    stacks[i + 1].insert(0, current_crate)

        # move crates
        elif line_number >= INSTRUCTION_START_LINE:
            num_moved, from_stack, to_stack = re.findall(r"\d+", line)
            num_moved, from_stack, to_stack = (
                int(num_moved),
                int(from_stack),
                int(to_stack),
            )

            for _ in range(num_moved):
                stacks[to_stack].append(stacks[from_stack].pop())

        line_number += 1

# top crates
result = "".join([stacks[i].pop() for i in range(1, NUM_STACKS + 1)])

print(result)
