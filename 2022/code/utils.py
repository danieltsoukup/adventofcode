from collections import defaultdict
from typing import Any


def read_inputs(path: str) -> list[str]:
    inputs = []
    with open(path, "r") as file:
        for line in file:
            line = line.strip()
            inputs.append(line)

    return inputs


# Partly based on
# https://stackoverflow.com/questions/3009935/looking-for-a-good-python-tree-data-structure
class Dir(defaultdict):
    def __init__(self, parent):
        super().__init__(self)
        self.parent = parent
        self.size = None

    def __call__(self):
        return self.__class__(self)

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

    def get_dirs(self):
        """
        Depth-First generator over directories.
        """
        for child in self:
            if isinstance(self[child], Dir):
                for dir in self[child].get_dirs():
                    yield dir
        yield self

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
