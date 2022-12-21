from tqdm import tqdm
from day20_part1 import mix_element

INPUT_FILE = "2022/inputs/day20.txt"
KEY = 811589153
ROUNDS = 10

if __name__ == "__main__":
    all_inputs = []
    with open(INPUT_FILE, "r") as file:
        for line in file:
            all_inputs.append(int(line.strip()) * KEY)

    indices = list(range(len(all_inputs)))

    for _ in tqdm(range(ROUNDS)):
        for i in tqdm(range(len(all_inputs))):
            idx = indices.index(i)
            shift = all_inputs[idx]
            indices = mix_element(indices, idx, shift)
            all_inputs = mix_element(all_inputs, idx, shift)

    idx = all_inputs.index(0)
    one = (idx + 1000) % len(all_inputs)
    two = (idx + 2000) % len(all_inputs)
    three = (idx + 3000) % len(all_inputs)

    print(all_inputs[one] + all_inputs[two] + all_inputs[three])
