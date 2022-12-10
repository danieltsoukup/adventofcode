INPUT_FILE = "2022/inputs/day10.txt"

results = {20 + i * 40: 20 + i * 40 for i in range(6)}


def cycle_step(results: dict[int], cycle: int, X: int) -> tuple[dict[int], int]:
    if cycle in results:
        results[cycle] *= X

    return results, cycle + 1


X = 1
cycle = 1
with open(INPUT_FILE, "r") as file:
    for line in file:
        line = line.strip()
        if line == "noop":
            results, cycle = cycle_step(results, cycle, X)
        else:
            delta = line.split(" ")[1]
            delta = int(delta)
            for _ in range(2):
                results, cycle = cycle_step(results, cycle, X)
            X += delta

print(sum(results.values()))
