def read_inputs(path: str, split: bool = False) -> list[str]:
    inputs = []
    with open(path, "r") as file:
        for line in file:
            line = line.strip()
            if split:
                line = list(line)
            inputs.append(line)

    return inputs
