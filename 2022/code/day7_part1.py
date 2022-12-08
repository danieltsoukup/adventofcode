from utils import Dir


INPUT_FILE = "2022/inputs/day7.txt"


class DirSolver(Dir):
    def __init__(self, parent):
        super().__init__(parent)

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
    current_working_dir = DirSolver(None)

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
