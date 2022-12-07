from collections import defaultdict
from typing import Any


INPUT_FILE = "2022/inputs/day7.txt"

# Partly based on
# https://stackoverflow.com/questions/3009935/looking-for-a-good-python-tree-data-structure
class Dir(defaultdict):
    def __init__(self, parent):
        super().__init__(self)
        self.parent = parent
        self.size = None

    def __call__(self):
        return Dir(self)

    def get_files(self):
        """
        Depth-First generator over files.
        """
        for child in self:
            if isinstance(self[child], Dir):
                for file in self[child].get_files():
                    yield file
            else:
                yield self[child]

    def get_size(self):
        """
        Get total size.
        """
        if self.size is None:
            total = 0
            for child in self:
                if isinstance(self[child], Dir):
                    total += self[child].get_size()
                else:
                    total += self[child]

            self.size = total

        return self.size

    def get_answer(self):
        """
        Get sum of sizes at most LIMIT.
        """
        LIMIT = 100000

        total = 0
        if self.get_size() <= LIMIT:
            total += self.get_size()

        for child in self.values():
            if isinstance(child, Dir):
                total += child.get_answer()

        return total


with open(INPUT_FILE, "r") as file:
    current_working_dir = Dir(None)

    for line in file:
        line = line.strip()
        if line.startswith("$ cd"):
            new_dir_name = line.split(" ")[-1]
            if new_dir_name == "..":
                current_working_dir = current_working_dir.parent
            else:
                current_working_dir = current_working_dir[new_dir_name]

        elif line.startswith("dir"):
            continue

        elif line.startswith("$ ls"):
            continue

        else:
            size, file_name = line.split(" ")
            size = int(size)
            current_working_dir[file_name] = size

while current_working_dir.parent is not None:
    current_working_dir = current_working_dir.parent

print(current_working_dir.get_answer())
