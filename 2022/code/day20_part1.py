from tqdm import tqdm

INPUT_FILE = "2022/inputs/day20.txt"


def mix_element(my_list: list[int], idx: int, shift: int) -> list[int]:
    new_list = my_list.copy()
    # rotate element to the front
    new_list = new_list[idx:] + new_list[:idx]
    shift = shift % (len(new_list) - 1)
    # slide forward
    new_list = new_list[1 : shift + 1] + [new_list[0]] + new_list[shift + 1 :]

    return new_list


if __name__ == "__main__":
    all_inputs = []
    with open(INPUT_FILE, "r") as file:
        for line in file:
            all_inputs.append(int(line.strip()))

    indices = list(range(len(all_inputs)))

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
