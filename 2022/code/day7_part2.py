from day7_part1 import Dir


INPUT_FILE = "2022/inputs/day7.txt"

if __name__ == "__main__":
    # build tree
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

    # find root
    while current_working_dir.parent is not None:
        current_working_dir = current_working_dir.parent

    TOTAL_AVAILABLE = 70000000
    NEEDED = 30000000
    total_used = current_working_dir.get_size()
    total_free = TOTAL_AVAILABLE - total_used

    best_size = TOTAL_AVAILABLE

    for dir in current_working_dir.get_dirs():
        current_size = dir.get_size()
        if (total_free + current_size >= NEEDED) and (current_size < best_size):
            best_size = current_size

    print(best_size)
